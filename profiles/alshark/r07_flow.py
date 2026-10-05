"""Guarded Roy assignment / Byuto mine and aftermath source inventory.

See docs/r07-re-source-evidence.md. Flags bound this static inventory; this
module does not establish runtime walkability or modify progression commands.
"""
from hashlib import sha256
from profiles.alshark.r06_flow import STORY_FLAGS as R06_FLAGS, ROUTE_ROOTS as R06_ROOTS
from profiles.alshark.r02_flow import control_edges as prior_edges
from profiles.alshark.script_tool import SYSTEM_HASH

STORY_FLAGS = R06_FLAGS | {0x29, 0x2a, 0x2c, 0x33, 0x49}
# Reporting after the Byuto victory begins the next assignment.
TERMINAL_EDGES = {('05c000:009', '2342022c1b'): '05c000:027'}
BYUTO_ROOTS = tuple(f'060000:{i:03}' for i in (*range(10),21,22,23,29))
BAR_ROOTS = tuple(f'053000:{i:03}' for i in range(39,44))
ROUTE_ROOTS = R06_ROOTS + BYUTO_ROOTS + BAR_ROOTS
COMMANDS = (
    ('05c000:009', '2342022c1b'),
    ('05c000:025', '23530129'),
    ('05c000:035', '23470129'),
    ('05c000:039', '234903023a26'),
    ('05c000:039', '23530149'),
    ('060000:009', '234903018d0a'),
    ('060000:009', '2353012a'),
    ('060000:022', '3f4606060900ffff13'),
    ('060000:023', '3f4608060a811e000fff14'),
    ('060000:023', '2353012c'),
    ('060000:023', '23510325330a'),
)
CALLS = {
    ('053000:039', '2350020224'): '053000:036',
    ('053000:041', '2350020225'): '053000:037',
    ('053000:043', '2350020223'): '053000:035',
    ('05c000:025', '2350020b25'): '05c000:037',
    ('05c000:035', '2350020b24'): '05c000:036',
    ('05c000:041', '2350020b24'): '05c000:036',
    ('060000:002', '2350020621'): '057000:033',
    **{(f'082000:{i+43:03}', f'23500230{i+13:02x}'): f'081000:{i+13:03}' for i in range(9)},
}


def control_edges(ident, entries):
    """Keep counted choices/calls and only flags possible through the Byuto victory.

    #A accepts a counted list of all required flags plus a final entry ID;
    the station uses THREE flags, not the two-flag shape seen in R02.
    """
    result = [e for e in prior_edges(ident, entries)
              if e[0] not in ('A','B','O')]
    bank = ident.split(':')[0]
    for token in entries[ident]['tokens']:
        if token['kind'] != 'command':
            continue
        if (ident, token['raw']) in TERMINAL_EDGES:
            continue
        raw = bytes.fromhex(token['raw']); payload = raw[3:]
        if raw[:2] == b'#B' and len(payload)==2 and payload[0] in STORY_FLAGS:
            result.append(('B',f'{bank}:{payload[-1]:03}',token['raw']))
        elif raw[:2] == b'#O' and len(payload)>=2 and set(payload[:-1]) & STORY_FLAGS:
            result.append(('O',f'{bank}:{payload[-1]:03}',token['raw']))
        elif raw[:2] == b'#A' and len(payload)>=2 and set(payload[:-1]) <= STORY_FLAGS:
            result.append(('A',f'{bank}:{payload[-1]:03}',token['raw']))
    return result


def route_closure(entries, roots=ROUTE_ROOTS):
    pending, seen = list(roots), set()
    while pending:
        ident = pending.pop()
        if ident in seen:
            continue
        if ident not in entries:
            raise ValueError(f'R07 branch target missing: {ident}')
        seen.add(ident)
        pending.extend(target for _,target,_ in control_edges(ident,entries))
    return seen


def selected_text_dependencies(entries, selected, roots=ROUTE_ROOTS):
    return {i for i in route_closure(entries, roots)
            if any(t['kind']=='text' for t in entries[i]['tokens'])} - set(selected)


def validate_source(entries):
    for ident, raw in COMMANDS:
        if ident not in entries or sum(t['kind']=='command' and t['raw']==raw
                                      for t in entries[ident]['tokens']) != 1:
            raise ValueError(f'{ident}: R07 source command missing or ambiguous: {raw}')
    for (ident, raw), target in CALLS.items():
        if ('P', target, raw) not in control_edges(ident, entries):
            raise ValueError(f'{ident}: R07 source call missing: {raw}')
    route_closure(entries)



def map_inventory(system):
    """Return guarded original metadata; exit/border map bytes are one-based."""
    if sha256(system).hexdigest() != SYSTEM_HASH:
        raise ValueError('R07 original System hash mismatch')
    result = {}
    for map_id, expected in ((10,0x86c00),(46,0x8fc00),(97,0x9c800),(2,0x84c00)):
        desc = system[0x4575+map_id*4:0x4579+map_id*4]
        offset = desc[1]*0x2000+(desc[2]-1)*0x400
        if desc[0] != 1 or offset != expected:
            raise ValueError(f'R07 map {map_id}: descriptor mismatch')
        raw = system[offset:offset+desc[3]*0x400]
        p = int.from_bytes(raw[15:17], 'little')
        objects = tuple((raw[p+1+n*18+12],raw[p+1+n*18+13]) for n in range(raw[p]))
        def records(word):
            p = int.from_bytes(raw[word:word+2], 'little'); rows = []
            while raw[p]:
                rows.append(tuple(raw[p:p+5])); p += 5
            return tuple(rows)
        result[map_id] = dict(offset=offset, bank=f'{0x51000+raw[8]*4096:06x}',
                             bounded=raw[2], objects=objects, exits=records(13),
                             triggers=records(19), border=tuple(raw[10:13]))
    return result


MENUS = (
    ('060000:000', '060000:011', '3f4e0506020b0c0d', 6, 2),
    ('060000:030', '060000:015', '3f4e0605030f101112', 5, 3),
)


def apply_reviewed_menu_widths(original, rebuilt, entries, selected):
    """Validate English against the original shop rectangles; no widening needed.

    Preserve both original menu width bytes, row counts and option order. This
    hook has the same integration interface as R02's explicit width overlay.
    """
    from profiles.alshark.script import decode_entry
    if len(original) != len(rebuilt):
        raise ValueError('R07 menu validation requires equal-sized System images')
    for source_id, label_id, command, width, rows in MENUS:
        if label_id not in selected:
            continue
        texts = [t.get('translation') for t in entries[label_id]['tokens']
                 if t['kind'] == 'text']
        if len(texts) != 1 or not isinstance(texts[0], str):
            raise ValueError(f'{label_id}: one adapted menu label span required')
        lines = texts[0].split('\n')
        if len(lines) != rows or any(not line or len(line) > width for line in lines):
            raise ValueError(f'{label_id}: labels exceed original {width}x{rows} menu')
        entry = entries[source_id]
        for data in (original, rebuilt):
            tokens = decode_entry(data[entry['offset']:entry['offset']+entry['size']])
            if sum(t['kind'] == 'command' and t['raw'] == command for t in tokens) != 1:
                raise ValueError(f'{source_id}: R07 menu source/output guard failed')
    return rebuilt, []
