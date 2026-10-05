"""Guarded first-bridge menus and Joe's service-overlay messages.

ASCII capitals are rendered by overlay 7000:3244. A source '>' advances
one cell; a literal space advances two. See docs/r03-re-source-evidence.md.
"""
from profiles.alshark.script import digest, decode_entry, rebuild_entry
from profiles.alshark.layout import validate_dialogue
import copy
from profiles.alshark.script_tool import SYSTEM_HASH
from profiles.alshark.menu_patch import encode_ui
from retrotext.localization import make_record

OFFSETS = (0x174c3, 0x174c9, 0x174ea, 0x17519, 0x17553, 0x1757c,
           0x175a3, 0x175cc, 0x175f2, 0x17633, 0x17669, 0x176a1,
           0x176e8, 0x17777, 0x177a8, 0x177d5, 0x177f0, 0x1780a)
FIXED_ID = 'fixed:System:00209a'
FIXED_START, FIXED_END = 0x209a, 0x20c8
REQUIRED = frozenset(f'ui:System:{a:06x}' for a in OFFSETS) | {FIXED_ID}
# (zero-based row, start column, protected cell count).
FIELDS = {0x17553: ((1, 0, 9),), 0x175cc: ((1, 0, 9),),
          0x17669: ((0, 0, 9), (2, 0, 6)),
          0x176e8: ((0, 3, 9),),
          0x1780a: ((1, 5, 5), (3, 0, 8))}


def export_records(images):
    system = images['System']
    if digest(system) != SYSTEM_HASH:
        raise ValueError('R03 service UI requires original System image')
    records = []
    for offset in OFFSETS:
        end = system.index(0, offset) + 1
        raw = system[offset:end]
        records.append(make_record(f'ui:System:{offset:06x}', 'ui', dict(
            disk='System', offset=offset, size=len(raw), raw=raw.hex(),
            text=raw[:-1].decode('cp932'), sha256=digest(raw))))
    raw = system[FIXED_START:FIXED_END]
    records.append(make_record(FIXED_ID, 'fixed_runtime_script', dict(
        disk='System', offset=FIXED_START, size=len(raw), raw=raw.hex(),
        sha256=digest(raw), tokens=decode_entry(raw))))
    return records


def encode_message(offset, value):
    if not isinstance(value, str) or not value:
        raise ValueError('R03 service UI needs nonempty text')
    lines = value.split('\n')
    if len(lines) > 4 or any(len(line) > 14 for line in lines):
        raise ValueError('R03 service UI exceeds fourteen cells / four rows')
    if offset == 0x174c3 and (len(lines) != 2 or lines[1] or len(lines[0]) > 14):
        raise ValueError('R03 Joe header must retain final newline')
    for row, col, size in FIELDS.get(offset, ()):
        if row >= len(lines) or lines[row][col:col+size] != ' '*size:
            raise ValueError(f'R03 service UI runtime field changed: row {row}, col {col}')
    result = bytearray()
    for char in value:
        if char == '\n':
            result.extend(b'@')
        elif char == ' ':
            result.extend(b'>')
        elif 'A' <= char <= 'Z':
            result.extend(char.encode('ascii'))
        elif char in "0123456789.,!?'":
            result.extend(encode_ui(char))
        else:
            raise ValueError(f'Unsupported R03 service UI glyph: {char!r}')
    return bytes(result) + b'\0'


def compile_records(images, records):
    source = {r['id']: r for r in export_records(images)}
    system = images['System']
    # Uppercase ASCII dispatch, single-cell skip, newline, and double-space
    # semantics belong to this loaded overlay, not the field renderer.
    if system[0x17253:0x17271] != bytes.fromhex(
            '3c3e743c3c2074353c4074393c41720f3c5b730b8ad8b419cd418bd0eb19'):
        raise ValueError('R03 service renderer guard changed')
    output = {disk: bytearray(data) for disk, data in images.items()}
    manifest, seen = [], set()
    for record in records:
        ident = record['id']
        if ident not in source or ident in seen or record['source'] != source[ident]['source']:
            raise ValueError('R03 service immutable source changed or duplicate record')
        seen.add(ident)
        spec = record['source']
        if ident == FIXED_ID:
            edits = record['target']['inGameEnglish']
            if (not isinstance(edits, dict) or set(edits) != {'t004'}
                    or not isinstance(edits['t004'], str)):
                raise ValueError('R03 heavy-item script requires exactly text t004')
            tokens = copy.deepcopy(spec['tokens'])
            tokens[4]['translation'] = edits['t004']
            validate_dialogue(tokens, {6: 'JOE'})
            encoded = rebuild_entry(bytes.fromhex(spec['raw']), tokens)
        else:
            encoded = encode_message(spec['offset'], record['target']['inGameEnglish'])
        if len(encoded) > spec['size']:
            raise ValueError(f'{ident}: service UI needs {len(encoded)}/{spec["size"]} bytes')
        start = spec['offset']
        output['System'][start:start+spec['size']] = encoded.ljust(spec['size'], b'\0')
        manifest.append(dict(id=ident, disk='System', offset=start, size=spec['size'],
                             patches=[dict(disk='System', offset=start, size=spec['size'])]))
    return {disk: bytes(data) for disk, data in output.items()}, manifest


MENU_GEOMETRY = (
    (0x4033, '0407180f7824', 7, 0xba7b, 8),
    (0x4105, '0406180fc628', 7, 0xbaf8, 8),
    (0x4039, '04021028b124', 6, 0xbb41, 8),
)


def widen_menus(opening, system):
    """Patch reviewed box and matching selection widths, preserving anchors.

    Call on pristine originals before menu strings are relocated. Both boxes
    remain inside the 40-cell display with their original selection order.
    """
    patches = []
    for offset, raw, width, instruction, old in MENU_GEOMETRY:
        expected = bytes.fromhex(raw)
        if opening[offset:offset+6] != expected:
            raise ValueError('R03 menu source geometry changed')
        if system[instruction:instruction+5] != b'\xc6\x06\x3e\x1d' + bytes([old]):
            raise ValueError('R03 menu selection geometry changed')
        if expected[2]//2 + width > 40:
            raise ValueError('R03 menu exceeds screen')
    for offset, raw, width, instruction, old in MENU_GEOMETRY:
        for disk, image, pos, before, after in (
                ('Opening', opening, offset, 4, width),
                ('System', system, instruction+4, old, width*2)):
            image[pos] = after
            patches.append(dict(disk=disk, offset=pos, before=before, after=after,
                                purpose='R03 bridge menu width', runtime_verified=False))
    return patches
