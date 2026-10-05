"""Source-backed Hom spaceport / abandoned mine / first bridge route.

See docs/r03-re-source-evidence.md. This inventory never changes commands or
removes a release blocker. The cockpit trigger is the explicit next section.
"""
from hashlib import sha256

from profiles.alshark.r02_flow import EARLY_PARTY_FLAGS, control_edges as r02_edges
from profiles.alshark.script_tool import SYSTEM_HASH

STORY_FLAGS = EARLY_PARTY_FLAGS | {0x12, 0x13, 0x1f}
PORT_ROOTS = tuple(f'054000:{i:03}' for i in range(3, 28))
MINE_ROOTS = ('054000:001', '054000:031')
BRIDGE_ROOTS = ('083000:001', '083000:004', '083000:005')
PARTY_ROOTS = ('082000:000', '082000:001', '082000:002', '082000:007')
ROUTE_ROOTS = PORT_ROOTS + MINE_ROOTS + BRIDGE_ROOTS + PARTY_ROOTS
NEXT_SECTION_ROOT = '083000:000'

# Commands carrying the critical route progression. Every command remains
# immutable under normal export/reinsertion, including already-satisfied tests.
COMMANDS = (
    ('054000:027', '2342021621'), ('054000:027', '23470122'),
    ('054000:034', '234202121e'), ('054000:034', '234202111d'),
    ('054000:029', '23530112'),
    ('054000:001', '2342021f1c'), ('054000:001', '2342020f02'),
    ('054000:002', '2353011f'), ('054000:002', '3f4d0103'),
    ('054000:002', '3f490100'),
    ('054000:031', '23530113'), ('054000:031', '3f490103'),
    ('082000:023', '2342021218'),
    ('082000:002', '2342021219'), ('082000:025', '2350022c22'),
    ('082000:000', '234202131a'), ('082000:026', '2350022c21'),
    ('082000:002', '234202131b'), ('082000:027', '2350022c20'),
    ('083000:000', '2342021408'), ('083000:000', '2350020320'),
)


def control_edges(ident, entries):
    """Conservative edges, with later-story party/bridge tests excluded.

    Port flag16's ticket-holder response is kept as additional coverage although
    no setter occurs before the endpoint. Global TALK after flag13 is retained
    conservatively; it is not a claim that the bridge offers that menu.
    """
    if ident.split(':')[0] not in ('082000', '083000'):
        return r02_edges(ident, entries)
    result = [e for e in r02_edges(ident, entries) if e[0] not in ('B', 'O')]
    bank = ident.split(':')[0]
    for token in entries[ident]['tokens']:
        if token['kind'] != 'command':
            continue
        raw = bytes.fromhex(token['raw'])
        payload = raw[3:]
        if raw[:2] == b'#B' and len(payload) == 2 and payload[0] in STORY_FLAGS:
            result.append(('B', f'{bank}:{payload[-1]:03}', token['raw']))
        elif raw[:2] == b'#O' and len(payload) >= 2 and set(payload[:-1]) & STORY_FLAGS:
            result.append(('O', f'{bank}:{payload[-1]:03}', token['raw']))
    return result


def route_closure(entries, roots=ROUTE_ROOTS):
    pending, seen = list(roots), set()
    while pending:
        ident = pending.pop()
        if ident in seen:
            continue
        if ident not in entries:
            raise ValueError(f'R03 branch target missing: {ident}')
        seen.add(ident)
        pending.extend(target for _, target, _ in control_edges(ident, entries))
    return seen


def selected_text_dependencies(entries, selected, roots=ROUTE_ROOTS):
    return {i for i in route_closure(entries, roots)
            if any(t['kind'] == 'text' for t in entries[i]['tokens'])} - set(selected)


def validate_source(entries):
    for ident, raw in COMMANDS:
        if ident not in entries or sum(t['kind'] == 'command' and t['raw'] == raw
                                      for t in entries[ident]['tokens']) != 1:
            raise ValueError(f'{ident}: R03 source command missing or ambiguous: {raw}')
    route_closure(entries)


def map_inventory(system):
    """Guard and parse the exact counted metadata, including excluded objects.

    Visibility flags are not story flags. No walkability inference is made.
    """
    if sha256(system).hexdigest() != SYSTEM_HASH:
        raise ValueError('R03 original System hash mismatch')
    result = {}
    for map_id, expected_offset in ((42, 0x8ec00), (96, 0x9c400), (1, 0x84800)):
        desc = system[0x4575 + map_id*4:0x4579 + map_id*4]
        offset = desc[1]*0x2000 + (desc[2]-1)*0x400
        if desc[0] != 1 or offset != expected_offset:
            raise ValueError(f'R03 map {map_id}: descriptor mismatch')
        raw = system[offset:offset+desc[3]*0x400]
        pos = int.from_bytes(raw[15:17], 'little')
        objects = tuple((raw[pos+1+n*18+12], raw[pos+1+n*18+13])
                        for n in range(raw[pos]))
        def records(word):
            p = int.from_bytes(raw[word:word+2], 'little')
            rows = []
            while raw[p]:
                rows.append(tuple(raw[p:p+5]))
                p += 5
            return tuple(rows)
        result[map_id] = dict(offset=offset, bank=f'{0x51000+raw[8]*4096:06x}',
                              objects=objects, exits=records(13), triggers=records(19),
                              border=tuple(raw[10:13]))
    return result


def bridge_menu_path(system, data):
    """Reproduce the doorway's collision cells on the straight-down route.

    This verifies static tile availability, not emulator movement/timing. NPC
    placements and the movement-bound branch are independently source guarded.
    """
    from pathlib import Path
    sums = dict(line.split('  ', 1)[::-1] for line in
                (Path(__file__).parent / 'SHA256SUMS.txt').read_text().splitlines())
    if (sha256(system).hexdigest() != SYSTEM_HASH or
            sha256(data).hexdigest() != sums['Alshark (Data Disk).hdm']):
        raise ValueError('R03 bridge collision source hash mismatch')
    grid = system[0xabc00:0xac000]
    quadrants, attrs = data[0x7d800:0x7dc00], data[0x7dc00:0x7e000]
    def collision(col, row):
        tile = grid[((row//2+12) % 25)*32 + col//2]
        glyph = quadrants[tile*4 + (row % 2)*2 + col % 2]
        return attrs[attrs[glyph] if glyph >= 128 else glyph] & 0xf0
    cells = {(col,row): collision(col,row)
             for row in (23,24,25) for col in (19,20)}
    if any(cells.values()):
        raise ValueError('R03 bridge doorway collision changed')
    return dict(screen_path=((38,46),(38,47),(38,48)),
                action='DOWN once more opens System bad4', collision=cells,
                cockpit_metadata=(16,21))
