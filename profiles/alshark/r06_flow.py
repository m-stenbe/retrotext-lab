"""Guarded Porkin pursuit / military-station rescue and reunion source inventory.

See docs/r06-re-source-evidence.md. Flags bound this static inventory; this
module does not establish runtime walkability or modify progression commands.
"""
from hashlib import sha256
from profiles.alshark.r05_flow import STORY_FLAGS as R05_FLAGS, ROUTE_ROOTS as R05_ROOTS
from profiles.alshark.r02_flow import control_edges as prior_edges
from profiles.alshark.script_tool import SYSTEM_HASH

STORY_FLAGS = R05_FLAGS | {0x19,0x1a,0x27,0x28}
PORKIN_ROOTS = ('05a000:014',)
STATION_ROOTS = tuple(f'05e000:{i:03}' for i in (*range(12),25,26,27,28))
CS_ROOTS = tuple(f'05c000:{i:03}' for i in range(14)) + ('05c000:024',)
# The explicit next-assignment boundary, not an inaccessible interaction.
TERMINAL_EDGES = {('05c000:009', '2342021a19'): '05c000:025'}
ROUTE_ROOTS = R05_ROOTS + PORKIN_ROOTS + STATION_ROOTS + CS_ROOTS
COMMANDS = (
 ('05a000:014','23530119'),('05a000:017','23530128'),
 ('05a000:017','234d054546474849'),('05e000:000','3f4606050400ff1c14'),
 ('05e000:000','2353011a'),('05e000:016','23570104'),
 ('05e000:016','234e0145'),('05e000:016','234d01fa'),
)


def control_edges(ident, entries):
    """Keep counted choices/calls and only flags possible through the Shoko reunion.

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
            raise ValueError(f'R06 branch target missing: {ident}')
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
            raise ValueError(f'{ident}: R06 source command missing or ambiguous: {raw}')
    for (ident, raw), target in CALLS.items():
        if ('P', target, raw) not in control_edges(ident, entries):
            raise ValueError(f'{ident}: R06 source call missing: {raw}')
    route_closure(entries)


def map_inventory(system):
    if sha256(system).hexdigest()!=SYSTEM_HASH:
        raise ValueError('R06 original System hash mismatch')
    result={}
    for map_id, expected in ((30,0x8bc00),(31,0x8c000),(9,0x86800),(53,0x91800),(50,0x90c00),(41,0x8e800),(2,0x84c00)):
        desc=system[0x4575+map_id*4:0x4579+map_id*4]
        offset=desc[1]*0x2000+(desc[2]-1)*0x400
        if desc[0]!=1 or offset!=expected:
            raise ValueError(f'R06 map {map_id}: descriptor mismatch')
        raw=system[offset:offset+desc[3]*0x400]
        p=int.from_bytes(raw[15:17],'little')
        objects=tuple((raw[p+1+n*18+12],raw[p+1+n*18+13]) for n in range(raw[p]))
        def records(word):
            p=int.from_bytes(raw[word:word+2],'little'); rows=[]
            while raw[p]:
                rows.append(tuple(raw[p:p+5]));p+=5
            return tuple(rows)
        result[map_id]=dict(offset=offset,bank=f'{0x51000+raw[8]*4096:06x}',
                           bounded=raw[2],
                           objects=objects,exits=records(13),triggers=records(19),
                           border=tuple(raw[10:13]))
    return result




CALLS = {('053000:029', '2350020224'): '053000:036', ('053000:031', '2350020223'): '053000:035', ('053000:033', '2350020225'): '053000:037', ('053000:034', '2350020225'): '053000:037', ('05a000:014', '235002090c'): '05a000:012', ('05a000:017', '235002090c'): '05a000:012', ('05a000:019', '2350020621'): '057000:033', ('05b000:005', '2350020621'): '057000:033', ('05b000:015', '2350020a11'): '05b000:017', ('05b000:018', '2350020a11'): '05b000:017', ('05b000:034', '2350020a11'): '05b000:017', ('05c000:000', '2350020b25'): '05c000:037', ('05c000:001', '2350020b25'): '05c000:037', ('05c000:002', '2350020b1a'): '05c000:026', ('05c000:003', '2350020b1a'): '05c000:026', ('05c000:004', '2350020b1a'): '05c000:026', ('05c000:005', '2350020b1a'): '05c000:026', ('05c000:009', '2350020b25'): '05c000:037', ('05c000:009', '2350020c00'): '05d000:000', ('05c000:010', '2350020b24'): '05c000:036', ('05c000:011', '2350020b1a'): '05c000:026', ('05c000:013', '2350020b1a'): '05c000:026', ('05c000:019', '2350020b18'): '05c000:024', ('05d000:000', '2350020c01'): '05d000:001', ('05e000:000', '2350020d0d'): '05e000:013', ('05e000:001', '2350020d0e'): '05e000:014', ('05e000:002', '2350020d0e'): '05e000:014', ('05e000:003', '2350020d0e'): '05e000:014', ('05e000:004', '2350020d0d'): '05e000:013', ('05e000:005', '2350020d0f'): '05e000:015', ('05e000:006', '2350020d0f'): '05e000:015', ('05e000:007', '2350020d0f'): '05e000:015', ('05e000:008', '2350020d0f'): '05e000:015', ('05e000:009', '2350020d0e'): '05e000:014', ('05e000:010', '2350020d0e'): '05e000:014', ('05e000:011', '2350020d0e'): '05e000:014', ('05e000:025', '2350020d0e'): '05e000:014', ('05e000:026', '2350020d0e'): '05e000:014', ('05e000:027', '2350020d0e'): '05e000:014', ('05e000:028', '2350020d0d'): '05e000:013', ('05f000:000', '2350020321'): '054000:033', ('05f000:001', '2350020e13'): '05f000:019', ('05f000:002', '2350020e13'): '05f000:019', ('05f000:003', '2350020e13'): '05f000:019', ('05f000:009', '2350020e13'): '05f000:019', ('05f000:013', '2350020e13'): '05f000:019', ('05f000:014', '2350020e13'): '05f000:019', ('05f000:015', '2350020e13'): '05f000:019', ('05f000:018', '2350020e13'): '05f000:019', ('05f000:020', '2350020e13'): '05f000:019', ('05f000:021', '2350020e13'): '05f000:019', ('05f000:025', '2350020e32'): '05f000:050', ('05f000:026', '2350020e39'): '05f000:057', ('05f000:027', '2350020e13'): '05f000:019', ('082000:008', '2350022e26'): '07f000:038', ('082000:009', '2350022e27'): '07f000:039', ('082000:015', '2350022e29'): '07f000:041', ('082000:016', '2350022e2a'): '07f000:042', ('082000:025', '2350022c22'): '07d000:034', ('082000:026', '2350022c21'): '07d000:033', ('082000:027', '2350022c20'): '07d000:032', ('082000:028', '2350022c1f'): '07d000:031', ('082000:029', '2350022c1e'): '07d000:030', ('082000:030', '2350023001'): '081000:001', ('082000:031', '2350023002'): '081000:002', ('082000:032', '2350023000'): '081000:000', ('082000:033', '2350023003'): '081000:003', ('082000:034', '2350023004'): '081000:004', ('082000:035', '2350023005'): '081000:005', ('082000:036', '2350023006'): '081000:006', ('082000:037', '2350023007'): '081000:007', ('082000:038', '2350023008'): '081000:008', ('082000:039', '2350023009'): '081000:009', ('082000:040', '235002300a'): '081000:010', ('082000:041', '235002300b'): '081000:011', ('082000:042', '235002300c'): '081000:012', ('083000:000', '2350020320'): '054000:032'}
