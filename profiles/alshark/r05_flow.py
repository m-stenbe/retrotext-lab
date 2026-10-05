"""Guarded Zajil surface / Saibal investigation through kidnapping source inventory.

See docs/r05-re-source-evidence.md. Flags bound this static inventory; this
module does not establish runtime walkability or modify progression commands.
"""
from hashlib import sha256
from profiles.alshark.r04_flow import STORY_FLAGS as R04_FLAGS
from profiles.alshark.r02_flow import control_edges as prior_edges
from profiles.alshark.script_tool import SYSTEM_HASH

STORY_FLAGS = R04_FLAGS | {0x17, 0x18}
SAIBAL_ROOTS = tuple(f'05b000:{i:03}' for i in (*range(17),18))
BAR_ROOTS = tuple(f'053000:{i:03}' for i in range(29,35))
PORKIN_ROOTS = tuple(f'05a000:{i:03}' for i in (*range(12),13,15,16))
PORT_ROOTS = tuple(f'05f000:{i:03}' for i in range(8))
PARTY_ROOTS = tuple(f'082000:{i:03}' for i in (0,1,2,3,7))
BRIDGE_ROOTS = tuple(f'083000:{i:03}' for i in (0,1,2,4,5))
ROUTE_ROOTS = SAIBAL_ROOTS + BAR_ROOTS + PORKIN_ROOTS + PORT_ROOTS + PARTY_ROOTS + BRIDGE_ROOTS
COMMANDS = (
 ('05b000:015','2342021622'), ('05b000:034','3f4606080100ffff13'),
 ('05b000:034','234e0111'), ('05b000:018','23530117'),
 ('05b000:021','2342021723'), ('05b000:035','23530118'),
 ('05b000:035','234d024344'), ('05a000:005','2342021612'),
 ('05a000:018','234e0114'), ('05f000:025','235103072828'),
 ('05f000:026','2351030f2827'),
)


def control_edges(ident, entries):
    """Keep counted choices/calls and only flags possible through the Saibal kidnapping.

    #A accepts a counted list of all required flags plus a final entry ID;
    the station uses THREE flags, not the two-flag shape seen in R02.
    """
    result = [e for e in prior_edges(ident, entries)
              if e[0] not in ('A','B','O')]
    bank = ident.split(':')[0]
    for token in entries[ident]['tokens']:
        if token['kind'] != 'command':
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
            raise ValueError(f'R05 branch target missing: {ident}')
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
            raise ValueError(f'{ident}: R05 source command missing or ambiguous: {raw}')
    for (ident, raw), target in CALLS.items():
        if ('P', target, raw) not in control_edges(ident, entries):
            raise ValueError(f'{ident}: R05 source call missing: {raw}')
    route_closure(entries)


def map_inventory(system):
    if sha256(system).hexdigest()!=SYSTEM_HASH:
        raise ValueError('R05 original System hash mismatch')
    result={}
    for map_id, expected in ((9,0x86800),(53,0x91800),(50,0x90c00),(41,0x8e800),(2,0x84c00)):
        desc=system[0x4575+map_id*4:0x4579+map_id*4]
        offset=desc[1]*0x2000+(desc[2]-1)*0x400
        if desc[0]!=1 or offset!=expected:
            raise ValueError(f'R05 map {map_id}: descriptor mismatch')
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



# Exact immutable calls in the bounded source closure.
CALLS = {('053000:029', '2350020224'): '053000:036', ('053000:031', '2350020223'): '053000:035', ('053000:033', '2350020225'): '053000:037', ('053000:034', '2350020225'): '053000:037', ('05b000:005', '2350020621'): '057000:033', ('05b000:015', '2350020a11'): '05b000:017', ('05b000:018', '2350020a11'): '05b000:017', ('05b000:034', '2350020a11'): '05b000:017', ('05f000:000', '2350020321'): '054000:033', ('05f000:001', '2350020e13'): '05f000:019', ('05f000:002', '2350020e13'): '05f000:019', ('05f000:003', '2350020e13'): '05f000:019', ('05f000:009', '2350020e13'): '05f000:019', ('05f000:013', '2350020e13'): '05f000:019', ('05f000:014', '2350020e13'): '05f000:019', ('05f000:015', '2350020e13'): '05f000:019', ('05f000:018', '2350020e13'): '05f000:019', ('05f000:020', '2350020e13'): '05f000:019', ('05f000:021', '2350020e13'): '05f000:019', ('05f000:025', '2350020e32'): '05f000:050', ('05f000:026', '2350020e39'): '05f000:057', ('05f000:027', '2350020e13'): '05f000:019', ('082000:008', '2350022e26'): '07f000:038', ('082000:009', '2350022e27'): '07f000:039', ('082000:015', '2350022e29'): '07f000:041', ('082000:016', '2350022e2a'): '07f000:042', ('082000:025', '2350022c22'): '07d000:034', ('082000:026', '2350022c21'): '07d000:033', ('082000:027', '2350022c20'): '07d000:032', ('082000:028', '2350022c1f'): '07d000:031', ('082000:029', '2350022c1e'): '07d000:030', ('082000:030', '2350023001'): '081000:001', ('082000:031', '2350023002'): '081000:002', ('082000:032', '2350023000'): '081000:000', ('082000:033', '2350023003'): '081000:003', ('082000:034', '2350023004'): '081000:004', ('082000:035', '2350023005'): '081000:005', ('082000:036', '2350023006'): '081000:006', ('082000:037', '2350023007'): '081000:007', ('083000:000', '2350020320'): '054000:032'}
