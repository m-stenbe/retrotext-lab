"""Guarded rescue / CS station tour and first briefing source inventory.

See docs/r04-re-source-evidence.md. Flags bound this static inventory; this
module does not establish runtime walkability or modify progression commands.
"""
from hashlib import sha256
from profiles.alshark.r03_flow import STORY_FLAGS as R03_FLAGS
from profiles.alshark.r02_flow import control_edges as prior_edges
from profiles.alshark.script_tool import SYSTEM_HASH

STORY_FLAGS = R03_FLAGS | {0x14, 0x15, 0x16, 0x23, 0x24, 0x25, 0x26}
RESCUE_ROOTS = ('083000:000',) + tuple(f'055000:{i:03}' for i in range(4))
STATION_ROOTS = tuple(f'05c000:{i:03}' for i in range(14)) + ('05c000:024',)
PARTY_ROOTS = tuple(f'082000:{i:03}' for i in (0,1,2,3,7))
BRIDGE_ROOTS = tuple(f'083000:{i:03}' for i in (1,2,4,5))
ROUTE_ROOTS = RESCUE_ROOTS + STATION_ROOTS + PARTY_ROOTS + BRIDGE_ROOTS
COMMANDS = (
 ('083000:000','2350020320'), ('054000:032','235103343c68'),
 ('055000:001','23470104'), ('055000:004','23530114'),
 ('055000:004','235103090a1e'), ('05c000:001','23530115'),
 ('05c000:004','23530125'), ('05c000:007','23530123'),
 ('05c000:012','23530124'), ('05c000:014','23530126'),
 ('05c000:009','2350020c00'), ('05d000:000','23530116'),
)


def control_edges(ident, entries):
    """Keep counted choices/calls and only flags possible before departure.

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
            raise ValueError(f'R04 branch target missing: {ident}')
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
            raise ValueError(f'{ident}: R04 source command missing or ambiguous: {raw}')
    route_closure(entries)


def map_inventory(system):
    if sha256(system).hexdigest()!=SYSTEM_HASH:
        raise ValueError('R04 original System hash mismatch')
    result={}
    for map_id, expected in ((104,0x9e400),(30,0x8bc00)):
        desc=system[0x4575+map_id*4:0x4579+map_id*4]
        offset=desc[1]*0x2000+(desc[2]-1)*0x400
        if desc[0]!=1 or offset!=expected:
            raise ValueError(f'R04 map {map_id}: descriptor mismatch')
        raw=system[offset:offset+desc[3]*0x400]
        p=int.from_bytes(raw[15:17],'little')
        objects=tuple((raw[p+1+n*18+12],raw[p+1+n*18+13]) for n in range(raw[p]))
        def records(word):
            p=int.from_bytes(raw[word:word+2],'little'); rows=[]
            while raw[p]:
                rows.append(tuple(raw[p:p+5]));p+=5
            return tuple(rows)
        result[map_id]=dict(offset=offset,bank=f'{0x51000+raw[8]*4096:06x}',
                           objects=objects,exits=records(13),triggers=records(19),
                           border=tuple(raw[10:13]))
    return result


# Exact source-backed cross-bank calls, including control-only dispatchers.
CALLS = {
    ('05c000:000', '2350020b25'): '05c000:037',
    ('05c000:001', '2350020b25'): '05c000:037',
    ('05c000:002', '2350020b1a'): '05c000:026',
    ('05c000:003', '2350020b1a'): '05c000:026',
    ('05c000:004', '2350020b1a'): '05c000:026',
    ('05c000:005', '2350020b1a'): '05c000:026',
    ('05c000:009', '2350020b25'): '05c000:037',
    ('05c000:009', '2350020c00'): '05d000:000',
    ('05c000:010', '2350020b24'): '05c000:036',
    ('05c000:011', '2350020b1a'): '05c000:026',
    ('05c000:013', '2350020b1a'): '05c000:026',
    ('05c000:019', '2350020b18'): '05c000:024',
    ('05d000:000', '2350020c01'): '05d000:001',
    ('082000:008', '2350022e26'): '07f000:038',
    ('082000:009', '2350022e27'): '07f000:039',
    ('082000:015', '2350022e29'): '07f000:041',
    ('082000:016', '2350022e2a'): '07f000:042',
    ('082000:025', '2350022c22'): '07d000:034',
    ('082000:026', '2350022c21'): '07d000:033',
    ('082000:027', '2350022c20'): '07d000:032',
    ('082000:028', '2350022c1f'): '07d000:031',
    ('082000:029', '2350022c1e'): '07d000:030',
    ('082000:030', '2350023001'): '081000:001',
    ('082000:031', '2350023002'): '081000:002',
    ('082000:032', '2350023000'): '081000:000',
    ('083000:000', '2350020320'): '054000:032',
}
