"""Coordinated R01 name repack in already-used allocations; no code/font patch."""
from pathlib import Path
import hashlib
from retrotext.localization import make_record

# All offsets are System disk offsets. Source tables use offsets relative 10000.
BASE = 0x10000
SHARED = {0: 'SION', 1: 'SION', 2: 'SHOKO', 3: 'SHOKO', 4: 'KARU',
          6: 'JOE', 7: 'JOE', 12: 'LUCIA', 13: 'LUCIA', 14: 'MAMON',
          15: 'MAMON', 16: 'JIDO', 81: 'COSMA'}
ITEMS = {
    'item-name:shirt': (0x10A99, tuple(range(0x100B8, 0x100C4, 2)), 'SHIRT'),
    'item-name:protector': (0x10AA1, (0x100C6,), 'PROTECTR'),
    'item-name:camp-kit': (0x10CB0, (0x10144,), 'CAMP KIT'),
}
ABILITIES = {
    'ability-name:11': (0x110B3, (0x10316, 0x1036E), 'HEAL'),
    'ability-name:12': (0x110BA, (0x10318,), 'SLEEP'),
    'ability-name:13': (0x110C0, (0x1031A,), 'TELEKIN'),
    'ability-name:14': (0x110C7, (0x1031C,), 'ILLUSION'),
    'ability-name:15': (0x110D0, (0x1031E,), 'HEAT'),
    'ability-name:16': (0x110D4, (0x10320,), 'FREEZE'),
    'ability-name:17': (0x110DA, (0x10322,), 'THUNDER'),
    'ability-name:18': (0x110E4, (0x10324,), 'DIMENS'),
    'ability-name:19': (0x110ED, (0x10326,), 'QUAKE'),
    'ability-name:20': (0x110F2, (0x10328,), 'MINDSTRM'),
    'ability-name:21': (0x110FC, (0x1032A, 0x1032C), 'CURE'),
    'ability-name:54': (0x11196, (0x1036C, 0x10370), 'WARP'),
    'ability-name:57': (0x1119D, (0x10372,), 'LOCATE'),
    'ability-name:58': (0x111A4, (0x10374,), 'INVIS'),
}
SOURCES = {**ITEMS, **ABILITIES}
SPECIAL = {
    **{ident: (pointers, text) for ident, (_, pointers, text) in SOURCES.items()},
    'ui:System:011329': ((0x10456,), 'PLANET HOM'),
    'ui:System:011723': ((0x10508,), 'SAXEN CANYON'),
}
REQUIRED = {**{f'name:{i}': s for i, s in SHARED.items()},
            **{i: text for i, (_, text) in SPECIAL.items()}}
# Source location padding is recalculated for English by encode_label.
LABELS = {
    'SION': (('name:0', 'name:1'), 'wide', ''),
    'SHOKO': (('name:2', 'name:3'), 'wide', ''),
    'KARU': (('name:4',), 'wide', ''),
    'JOE': (('name:6', 'name:7'), 'wide', ''),
    'LUCIA': (('name:12', 'name:13'), 'wide', ''),
    'MAMON': (('name:14', 'name:15'), 'wide', ''),
    'JIDO': (('name:16',), 'wide', ''),
    'COSMA': (('name:81',), 'ascii', ' >'),
    'SHIRT': (('item-name:shirt',), 'ascii', ''),
    'PROTECTR': (('item-name:protector',), 'ascii', ''),
    'CAMP KIT': (('item-name:camp-kit',), 'ascii', ''),
    'PLANET HOM': (('ui:System:011329',), 'ascii', '  '),
    'SAXEN CANYON': (('ui:System:011723',), 'ascii', '>'),
}
LABELS.update({text: ((ident,), 'ascii', '')
               for ident, (_, _, text) in ABILITIES.items()})
SPANS = (
    (0x111DB, 0x111EA, ('SAXEN CANYON',)),
    (0x11207, 0x11214, ('PLANET HOM',)),
    (0x11235, 0x1125A, ('MAMON', 'DIMENS', 'MINDSTRM', 'SLEEP')),
    (0x114BF, 0x114C9, ('INVIS',)),
    (0x111EA, 0x111FD, ('SHOKO', 'THUNDER')),
    (0x10A99, 0x10A9D, ()),
    (0x10AA1, 0x10AA9, ('COSMA',)),
    (0x10CB0, 0x10CB9, ('ILLUSION',)),
    (0x11329, 0x11332, ('SION',)),
    (0x11722, 0x1172E, ('TELEKIN',)),
    (0x110B3, 0x11100, ('PROTECTR', 'KARU', 'JIDO', 'CAMP KIT', 'LOCATE',
                          'JOE', 'SHIRT', 'HEAL', 'HEAT', 'WARP', 'CURE')),
    (0x11196, 0x111AE, ('LUCIA', 'FREEZE', 'QUAKE')),
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def guard_original(images):
    hashes = dict(line.split('  ', 1)[::-1] for line in
                  (Path(__file__).parent/'SHA256SUMS.txt').read_text().splitlines())
    for disk in ('System', 'Opening'):
        if digest(images[disk]) != hashes[f'Alshark ({disk} Disk).hdm']:
            raise ValueError(f'{disk}: name source hash mismatch')
    # Guard the name load and ASCII conversion independently of the full hashes.
    system = images['System']
    if system[0x3F31:0x3F35] != bytes.fromhex('01080106'):
        raise ValueError('Name bank loader mismatch')
    if system[0x1B0C5:0x1B0CD] != bytes.fromhex('3c3e743a3c207433'):
        raise ValueError('Name spacing renderer mismatch')
    if system[0x1B100:0x1B108] != bytes.fromhex('e80e00e80b00ebb6'):
        raise ValueError('Name spacing advance mismatch')
    if system[0x1B0CD:0x1B0DF] != bytes.fromhex('3c41720f3c5b730b8ad8b419cd418bd0eb1b'):
        raise ValueError('Name renderer ASCII branch mismatch')


def export_records(images):
    """Additional records only; existing shared names and location UI stay valid."""
    guard_original(images)
    system = images['System']
    records = []
    for ident, (offset, pointers, _) in SOURCES.items():
        end = system.index(0, offset)+1
        raw = system[offset:end]
        source = dict(disk='System', offset=offset, size=len(raw), raw=raw.hex(),
                      text=raw[:-1].decode('cp932'), sha256=digest(raw),
                      pointers=[dict(offset=p, raw=system[p:p+2].hex()) for p in pointers],
                      allocationGroup='r01-required-names',
                      rendererOffset=0x1B0B1,
                      rendererSha256=digest(system[0x1B0B1:0x1B130]),
                      loaderOffset=0x3F31, loaderRaw='01080106')
        records.append(make_record(ident, 'name', source))
    return records


def _pointers(ident):
    if ident.startswith('name:'):
        return (0x10400 + 2*int(ident.split(':')[1]),)
    return SPECIAL[ident][0]


def encode_label(text, encoding, prefix=''):
    if not isinstance(text, str) or not text or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ ' for c in text):
        raise ValueError('Only reviewed uppercase letters/spaces are supported in these names')
    if len(text) > 12:
        raise ValueError('Name exceeds supported adapter name width')
    if encoding == 'ascii':
        if prefix:
            # All prefixed labels in this adapter are twelve-cell map titles.
            # Space advances two glyphs; > advances one. Recenter English.
            padding = (12 - len(text)) // 2
            prefix = ' ' * (padding // 2) + '>' * (padding % 2)
        return (prefix + text.replace(' ', '>')).encode('ascii') + b'\0'
    if encoding == 'wide':
        return prefix.encode('ascii') + ''.join(chr(ord(c)+0xFEE0) for c in text).encode('cp932') + b'\0'
    raise ValueError('Unknown name encoding')


def compile_names(images, translations):
    """Return (System bytes, {records, patches}) for the complete coordinated group.

    The caller must validate canonical/review/basedOn state for all REQUIRED IDs.
    All spelling choices are explicit; partial maps and silent new spellings fail.
    Apply every returned patch range after legacy name and fixed-menu patches.
    """
    guard_original(images)
    if not isinstance(translations, dict) or set(translations) != set(REQUIRED):
        raise ValueError('The complete required-name group must be selected')
    if translations != REQUIRED:
        raise ValueError('Name spellings changed; update the audited allocation plan')
    # Learned abilities and narrow inventory/equipment fields reserve eight name cells.
    if any(len(translations[ident]) > 8 for ident in ABILITIES):
        raise ValueError('Ability name exceeds eight-cell runtime field')
    if any(len(translations[ident]) > 8 for ident in ITEMS):
        raise ValueError('Item name exceeds eight-cell runtime field')
    source = images['System']
    expected_fields = {p for ident in REQUIRED for p in _pointers(ident)}
    # Every table pointer into any replaced span must be among the reviewed set.
    # This includes full-name aliases and all six Shirt aliases.
    for p in range(BASE, 0x105A0, 2):
        destination = BASE + int.from_bytes(source[p:p+2], 'little')
        if any(a <= destination < z for a, z, _ in SPANS) and p not in expected_fields:
            raise ValueError(f'Unreviewed alias into name repack at {p:#x}')
    for ident, (offset, pointers, _) in SOURCES.items():
        for p in pointers:
            if source[p:p+2] != (offset-BASE).to_bytes(2, 'little'):
                raise ValueError(f'{ident}: pointer mismatch')
    if source[0x10456:0x10458] != bytes.fromhex('2913') or source[0x10508:0x1050A] != bytes.fromhex('2217'):
        raise ValueError('Location pointer mismatch')
    output = bytearray(source)
    records = []
    patches = []
    for start, end, labels in SPANS:
        payload = bytearray()
        for label in labels:
            ids, encoding, prefix = LABELS[label]
            encoded = encode_label(label, encoding, prefix)
            destination = start+len(payload)
            payload.extend(encoded)
            pointers = []
            for ident in ids:
                for p in _pointers(ident):
                    pointers.append(p)
                    output[p:p+2] = (destination-BASE).to_bytes(2, 'little')
                    patches.append(dict(offset=p, size=2))
                records.append(dict(record=ident, disk='System', offset=destination,
                                    used=len(encoded), encoding=encoding,
                                    pointers=list(_pointers(ident)), text=label,
                                    runtime_verified=False))
        if len(payload) > end-start:
            raise ValueError(f'Name span overflow at {start:#x}')
        output[start:end] = payload.ljust(end-start, b'\0')
        patches.append(dict(offset=start, size=end-start))
    if {r['record'] for r in records} != set(REQUIRED):
        raise ValueError('Name allocation plan omitted a required record')
    return bytes(output), dict(records=records, patches=patches)
