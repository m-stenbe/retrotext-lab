"""Guarded Roy leave / Mars capital investigation source inventory.

See docs/r08-re-source-evidence.md. Flags bound this static inventory; this
module does not establish runtime walkability or modify progression commands.
"""
from hashlib import sha256
from profiles.alshark.r07_flow import STORY_FLAGS as R07_FLAGS, ROUTE_ROOTS as R07_ROOTS
from profiles.alshark.r02_flow import control_edges as prior_edges
from profiles.alshark.script_tool import SYSTEM_HASH

STORY_FLAGS = R07_FLAGS | {0x22, 0x2b, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32}
TERMINAL_EDGES = {}
# The encyclopedia is first acquired behind post-Daina flag34/36. It cannot
# be carried in this bounded pre-Daina interval; retain its command unchanged.
EXCLUDED_ITEM_EDGES = {('063000:004', '23430301a619'): '063000:025'}
PORT_ROOTS = tuple(f'05f000:{i:03}' for i in range(28,41))
CAPITAL_ROOTS = tuple(f'057000:{i:03}' for i in (*range(13), *range(14,33)))
BEGI_ROOTS = tuple(f'063000:{i:03}' for i in range(18))
BAR_ROOTS = tuple(f'053000:{i:03}' for i in range(44,52))
INTERIOR_ROOTS = tuple(f'061000:{i:03}' for i in range(13))
ROUTE_ROOTS = R07_ROOTS + PORT_ROOTS + CAPITAL_ROOTS + BEGI_ROOTS + BAR_ROOTS + INTERIOR_ROOTS
COMMANDS = (
    ('05c000:027', '2350020c02'), ('05d000:002', '2353012d'),
    ('05c000:032', '235103072828'), ('057000:035', '23530122'),
    ('053000:055', '23490301a538'), ('053000:055', '23530130'),
    ('081000:025', '23530132'),
    ('063000:004', '23430301a619'),
)
CALLS = {('05e000:005', '2350020d0f'): '05e000:015', ('05f000:059', '2350020e13'): '05f000:019', ('082000:052', '2350023016'): '081000:022', ('05e000:025', '2350020d0e'): '05e000:014', ('082000:043', '235002300d'): '081000:013', ('05c000:001', '2350020b25'): '05c000:037', ('05d000:002', '2350020c01'): '05d000:001', ('05d000:002', '2350020b1c'): '05c000:028', ('082000:046', '2350023010'): '081000:016', ('057000:037', '2350020129'): '052000:041', ('053000:043', '2350020223'): '053000:035', ('053000:057', '2350020224'): '053000:036', ('05e000:006', '2350020d0f'): '05e000:015', ('05c000:011', '2350020b1a'): '05c000:026', ('05f000:015', '2350020e13'): '05f000:019', ('05c000:035', '2350020b24'): '05c000:036', ('05f000:031', '2350020e13'): '05f000:019', ('05f000:025', '2350020e32'): '05f000:050', ('053000:048', '2350020225'): '053000:037', ('053000:048', '2350022702'): '078000:002', ('082000:047', '2350023011'): '081000:017', ('083000:000', '2350020320'): '054000:032', ('05e000:007', '2350020d0f'): '05e000:015', ('082000:058', '235002301c'): '081000:028', ('082000:050', '2350023014'): '081000:020', ('082000:028', '2350022c1f'): '07d000:031', ('063000:002', '2350020621'): '057000:033', ('05c000:027', '2350020c02'): '05d000:002', ('082000:009', '2350022e27'): '07f000:039', ('05c000:019', '2350020b18'): '05c000:024', ('05f000:060', '2350020321'): '054000:033', ('082000:034', '2350023004'): '081000:004', ('057000:063', '235002063b'): '057000:059', ('05e000:004', '2350020d0d'): '05e000:013', ('05c000:004', '2350020b1a'): '05c000:026', ('05f000:000', '2350020321'): '054000:033', ('05c000:013', '2350020b1a'): '05c000:026', ('082000:054', '2350023018'): '081000:024', ('082000:048', '2350023012'): '081000:018', ('082000:037', '2350023007'): '081000:007', ('082000:032', '2350023000'): '081000:000', ('082000:031', '2350023002'): '081000:002', ('053000:039', '2350020224'): '053000:036', ('082000:040', '235002300a'): '081000:010', ('05f000:021', '2350020e13'): '05f000:019', ('082000:015', '2350022e29'): '07f000:041', ('05e000:001', '2350020d0e'): '05e000:014', ('082000:027', '2350022c20'): '07d000:032', ('05f000:018', '2350020e13'): '05f000:019', ('05f000:014', '2350020e13'): '05f000:019', ('053000:041', '2350020225'): '053000:037', ('053000:044', '2350020224'): '053000:036', ('053000:050', '2350022704'): '078000:004', ('05e000:000', '2350020d0d'): '05e000:013', ('082000:029', '2350022c1e'): '07d000:030', ('082000:039', '2350023009'): '081000:009', ('063000:028', '2350020626'): '057000:038', ('05c000:002', '2350020b1a'): '05c000:026', ('082000:008', '2350022e26'): '07f000:038', ('05b000:015', '2350020a11'): '05b000:017', ('082000:026', '2350022c21'): '07d000:033', ('05a000:019', '2350020621'): '057000:033', ('053000:056', '2350020224'): '053000:036', ('05c000:003', '2350020b1a'): '05c000:026', ('05c000:000', '2350020b25'): '05c000:037', ('082000:016', '2350022e2a'): '07f000:042', ('053000:034', '2350020225'): '053000:037', ('05b000:034', '2350020a11'): '05b000:017', ('05f000:020', '2350020e13'): '05f000:019', ('082000:057', '235002301b'): '081000:027', ('053000:054', '2350020224'): '053000:036', ('05e000:010', '2350020d0e'): '05e000:014', ('05e000:028', '2350020d0d'): '05e000:013', ('05f000:027', '2350020e13'): '05f000:019', ('05c000:041', '2350020b24'): '05c000:036', ('05f000:026', '2350020e39'): '05f000:057', ('082000:049', '2350023013'): '081000:019', ('05f000:030', '2350020e02'): '05f000:002', ('05f000:049', '2350020e3a'): '05f000:058', ('057000:052', '235002063b'): '057000:059', ('05e000:026', '2350020d0e'): '05e000:014', ('053000:046', '2350022700'): '078000:000', ('05c000:025', '2350020b25'): '05c000:037', ('063000:004', '2350021214'): '063000:020', ('082000:030', '2350023001'): '081000:001', ('082000:053', '2350023017'): '081000:023', ('05e000:009', '2350020d0e'): '05e000:014', ('05a000:017', '235002090c'): '05a000:012', ('05f000:009', '2350020e13'): '05f000:019', ('082000:041', '235002300b'): '081000:011', ('053000:055', '2350020224'): '053000:036', ('082000:033', '2350023003'): '081000:003', ('082000:045', '235002300f'): '081000:015', ('05e000:008', '2350020d0f'): '05e000:015', ('05f000:002', '2350020e13'): '05f000:019', ('082000:044', '235002300e'): '081000:014', ('082000:025', '2350022c22'): '07d000:034', ('05f000:041', '2350020e13'): '05f000:019', ('053000:049', '2350022703'): '078000:003', ('05f000:032', '2350020e13'): '05f000:019', ('05e000:003', '2350020d0e'): '05e000:014', ('082000:036', '2350023006'): '081000:006', ('05e000:027', '2350020d0e'): '05e000:014', ('05e000:002', '2350020d0e'): '05e000:014', ('05f000:048', '2350020e39'): '05f000:057', ('05b000:018', '2350020a11'): '05b000:017', ('060000:002', '2350020621'): '057000:033', ('05f000:029', '2350020e03'): '05f000:003', ('082000:038', '2350023008'): '081000:008', ('063000:027', '2350020129'): '052000:041', ('082000:035', '2350023005'): '081000:005', ('053000:047', '2350022701'): '078000:001', ('053000:031', '2350020223'): '053000:035', ('082000:051', '2350023015'): '081000:021', ('053000:029', '2350020224'): '053000:036', ('05c000:005', '2350020b1a'): '05c000:026', ('05f000:047', '2350020e38'): '05f000:056', ('057000:064', '235002063b'): '057000:059', ('05d000:000', '2350020c01'): '05d000:001', ('05c000:010', '2350020b24'): '05c000:036', ('05a000:014', '235002090c'): '05a000:012', ('082000:056', '235002301a'): '081000:026', ('05b000:005', '2350020621'): '057000:033', ('053000:033', '2350020225'): '053000:037', ('05f000:033', '2350020e13'): '05f000:019', ('082000:055', '2350023019'): '081000:025', ('082000:042', '235002300c'): '081000:012', ('053000:051', '2350022705'): '078000:005', ('05f000:013', '2350020e13'): '05f000:019', ('05c000:009', '2350020b25'): '05c000:037', ('05c000:009', '2350020c00'): '05d000:000', ('05f000:042', '2350020e13'): '05f000:019', ('05f000:003', '2350020e13'): '05f000:019', ('05e000:011', '2350020d0e'): '05e000:014', ('05f000:001', '2350020e13'): '05f000:019'}


def control_edges(ident, entries):
    """Keep counted choices/calls and only flags possible through the capital video letter.

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
            raise ValueError(f'R08 branch target missing: {ident}')
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
            raise ValueError(f'{ident}: R08 source command missing or ambiguous: {raw}')
    for (ident, raw), target in CALLS.items():
        if ('P', target, raw) not in control_edges(ident, entries):
            raise ValueError(f'{ident}: R08 source call missing: {raw}')
    route_closure(entries)



def map_inventory(system):
    """Return guarded original metadata; exit/border map bytes are one-based."""
    if sha256(system).hexdigest() != SYSTEM_HASH:
        raise ValueError('R08 original System hash mismatch')
    result = {}
    for map_id, expected in ((8,0x86400),(40,0x8e400),(61,0x93800),(73,0x96800),(2,0x84c00),(3,0x85000)):
        desc = system[0x4575+map_id*4:0x4579+map_id*4]
        offset = desc[1]*0x2000+(desc[2]-1)*0x400
        if desc[0] != 1 or offset != expected:
            raise ValueError(f'R08 map {map_id}: descriptor mismatch')
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
    ('057000:001','057000:039','3f4e050602272829',6,2),
    ('057000:008','057000:046','3f4e0505022e2f30',5,2),
    ('057000:012','057000:013','3f4e0606030d3f4038',6,3),
    ('057000:050','057000:051','3f4e050403333438',4,3),
    ('05f000:042','05f000:043','3f4e0706042b2c2d2e14',6,4),
    ('063000:001','063000:029','3f4e0506021d1e1f',6,2),
    ('063000:003','063000:033','3f4e06050321222324',5,3),
)


def apply_reviewed_menu_widths(original, rebuilt, entries, selected):
    """Validate English against the original shop rectangles; no widening needed.

    Preserve both original menu width bytes, row counts and option order. This
    hook has the same integration interface as R02's explicit width overlay.
    """
    from profiles.alshark.script import decode_entry
    if len(original) != len(rebuilt):
        raise ValueError('R08 menu validation requires equal-sized System images')
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
                raise ValueError(f'{source_id}: R08 menu source/output guard failed')
    return rebuilt, []
