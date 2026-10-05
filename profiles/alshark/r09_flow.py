"""Guarded Daina reunion and Begi historian route source inventory.

The static closure preserves commands and does not claim runtime traversal.
See docs/r09-re-source-evidence.md for the boundary and evidence.
"""
from hashlib import sha256
from profiles.alshark.r08_flow import STORY_FLAGS as R08_FLAGS, ROUTE_ROOTS as R08_ROOTS
from profiles.alshark.r08_flow import CALLS as R08_CALLS, validate_source as prior_validate
from profiles.alshark.r02_flow import control_edges as prior_edges
from profiles.alshark.script_tool import SYSTEM_HASH

STORY_FLAGS = R08_FLAGS | {0x34, 0x36, 0x37}
TERMINAL_EDGES = {}
EXCLUDED_ITEM_EDGES = {}
DAINA_ROOTS = tuple(f'062000:{i:03}' for i in range(9))
ROUTE_ROOTS = R08_ROOTS + DAINA_ROOTS + ('082000:005',)
COMMANDS = (
    ('062000:001', '2342023209'), ('062000:001', '234202340a'),
    ('062000:009', '23530134'), ('062000:009', '2357010a'),
    ('062000:009', '235103946008'), ('063000:019', '23530136'),
    ('063000:022', '23490301a618'), ('063000:025', '23530137'),
    ('063000:025', '23490301a718'), ('05f000:061', '2342023455'),
)
CALLS = R08_CALLS | {('062000:011', '2350020129'): '052000:041', ('062000:012', '2350020626'): '057000:038', ('063000:019', '2350021214'): '063000:020', ('063000:021', '2350021214'): '063000:020', ('063000:021', '2350021217'): '063000:023', ('063000:022', '2350021217'): '063000:023', ('063000:025', '2350021214'): '063000:020', ('063000:025', '235002121a'): '063000:026', ('063000:026', '2350021214'): '063000:020', ('082000:059', '235002301d'): '081000:029', ('082000:060', '235002301e'): '081000:030', ('082000:061', '235002301f'): '081000:031', ('082000:062', '2350022f00'): '080000:000', ('082000:063', '2350022f01'): '080000:001', ('082000:064', '2350022f02'): '080000:002', ('082000:065', '2350022f03'): '080000:003'}


def control_edges(ident, entries):
    """Keep counted choices/calls and only flags possible through the historian's Stea lead.

    #A accepts a counted list of all required flags plus a final entry ID;
    the station uses THREE flags, not the two-flag shape seen in R02.
    """
    result = [e for e in prior_edges(ident, entries)
              if e[0] not in ('A','B','O') and (ident,e[2]) not in EXCLUDED_ITEM_EDGES]
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
            raise ValueError(f'R09 branch target missing: {ident}')
        seen.add(ident)
        pending.extend(target for _,target,_ in control_edges(ident,entries))
    return seen


def selected_text_dependencies(entries, selected, roots=ROUTE_ROOTS):
    return {i for i in route_closure(entries, roots)
            if any(t['kind']=='text' for t in entries[i]['tokens'])} - set(selected)


def validate_source(entries):
    prior_validate(entries)
    for ident, raw in COMMANDS:
        if ident not in entries or sum(t['kind']=='command' and t['raw']==raw
                                      for t in entries[ident]['tokens']) != 1:
            raise ValueError(f'{ident}: R09 source command missing or ambiguous: {raw}')
    for (ident, raw), target in CALLS.items():
        if ('P', target, raw) not in control_edges(ident, entries):
            raise ValueError(f'{ident}: R09 source call missing: {raw}')
    route_closure(entries)



def map_inventory(system):
    """Return guarded original metadata; exit/border map bytes are one-based."""
    if sha256(system).hexdigest() != SYSTEM_HASH:
        raise ValueError('R09 original System hash mismatch')
    result = {}
    for map_id, expected in ((8,0x86400),(71,0x96000),(61,0x93800)):
        desc = system[0x4575+map_id*4:0x4579+map_id*4]
        offset = desc[1]*0x2000+(desc[2]-1)*0x400
        if desc[0] != 1 or offset != expected:
            raise ValueError(f'R09 map {map_id}: descriptor mismatch')
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


MENUS = (('062000:003','062000:013','3f4e0506020d0e0f',6,2),)


def apply_reviewed_menu_widths(original, rebuilt, entries, selected):
    """Validate English against the original shop rectangles; no widening needed.

    Preserve both original menu width bytes, row counts and option order. This
    hook has the same integration interface as R02's explicit width overlay.
    """
    from profiles.alshark.script import decode_entry
    if len(original) != len(rebuilt):
        raise ValueError('R09 menu validation requires equal-sized System images')
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
                raise ValueError(f'{source_id}: R09 menu source/output guard failed')
    return rebuilt, []
