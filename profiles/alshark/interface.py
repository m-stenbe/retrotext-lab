"""Guarded R01 resident-menu relocation and fixed UI adapters.

The Opening driver loads 0x2000..0x5fff; this pool is disjoint from menus at
0x4c00..0x4dff and disk names at 0x4e00..0x4e59. Only existing menu pointers
are retargeted. Fixed System strings retain their address and allocation.
"""
from profiles.alshark.menu_patch import encode_ui
from profiles.alshark.menu_layout import widen_menus
from profiles.alshark.script import digest, decode_entry
from profiles.alshark.combat_text import patch_script_spans
from retrotext.localization import make_record

POOL = 0x4f00
POOL_END = 0x5f00
EXTRA_SYSTEM = (0x1d5e, 0x1d86, 0x1d99, 0x1e47, 0x1e50, 0x1ed2,
                0x1e5b, 0x1e63, 0x1e6e)
START_LABELS = {0x470c, 0x471b, 0x4b0c, 0x4b1b}
# Existing System runtime prefix R/_/A/r/m/> remains untouched.
HEAVY_SUFFIX = 0x1eaf + len('R/＿/A/ｒｍ/>'.encode('cp932'))
FIXED_RANGES = {0x1edf: 0x1f28, 0x1f28: 0x1fd8, 0x1fd8: 0x1ff3}
FIXED_EDIT_IDS = {
    0x1edf: {'t000','t004','t008','t012'},
    # Remaining spans are existing English stat labels/spacing around immutable
    # indexed runtime fields; keep their original glyph/mode representation.
    0x1f28: {'t001','t006','t008','t010','t012','t025','t035','t041','t047'},
    0x1fd8: {'t000','t002'},
}
# Glyph-column/newline shapes from the reviewed fixed-runtime layouts. Changing
# these requires a new renderer/field-layout review, not merely spare bytes.
FIXED_SHAPES = {
    0x1edf: {'t000': (11,6), 't004': (0,8), 't008': (0,8), 't012': (0,7)},
    0x1f28: {'t001': (10,), 't006': (0,5), 't008': (4,4), 't010': (4,4),
             't012': (4,0), 't025': (4,1), 't035': (4,1), 't041': (4,1), 't047': (4,14)},
    0x1fd8: {'t000': (7,5), 't002': (0,8)},
}


# The resident renderer converts ASCII A-Z through f52a and advances ASCII
# spaces by a full cell (f58c). Use this only for these reviewed fixed fields.
R02_SCRAP_UI = {0x1e5b: 8, 0x1e63: 11, 0x1e6e: 42}


def encode_scrap_ui(system, offset, value):
    if system[0xf55c:0xf567] != bytes.fromhex('3c4172183c5b7306e8c3ff'):
        raise ValueError('R02 resident ASCII renderer guard changed')
    if (not isinstance(value, str) or any(c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ ?\n" for c in value)):
        raise ValueError('Unsupported R02 scrap UI character')
    lines = value.split('\n')
    if any(len(line) > 14 for line in lines):
        raise ValueError('R02 scrap UI exceeds fourteen cells')
    if offset == 0x1e5b and (len(lines) != 2 or lines[1] != ''):
        raise ValueError('Joe header must retain its final newline')
    if offset == 0x1e63 and len(lines) != 1:
        raise ValueError('Disassembly confirmation must stay on one row')
    if offset == 0x1e6e:
        # c5e6 draws the item at 4608; c5f5 draws the amount at 4b08.
        # Template base is 4608, row stride 500: protect 9/5 leading cells.
        if (len(lines) != 2 or not lines[0].startswith(' '*9)
                or not lines[1].startswith(' '*5)):
            raise ValueError('R02 item/amount placeholder fields changed')
    output = bytearray()
    for char in value:
        if char == '\n':
            output.extend(b'@')
        elif char == '?':
            output.extend(encode_ui(char))
        else:
            output.extend(char.encode('ascii'))
    return bytes(output) + b'\0'


def export_records(images):
    data = images['System']
    result = []
    for a in (*EXTRA_SYSTEM, HEAVY_SUFFIX):
        z = data.index(0, a)+1
        raw = data[a:z]
        result.append(make_record(f'ui:System:{a:06x}', 'ui', dict(disk='System',
            offset=a,size=z-a,raw=raw.hex(),text=raw[:-1].decode('cp932'),sha256=digest(raw))))
    a, z = 0x1fd8, 0x1ff3
    raw = data[a:z]
    result.append(make_record(f'fixed:System:{a:06x}', 'fixed_runtime_script',
        dict(disk='System',offset=a,size=z-a,raw=raw.hex(),sha256=digest(raw),tokens=decode_entry(raw))))
    return result


def compile_records(images, records):
    output = {disk: bytearray(data) for disk,data in images.items()}
    opening = images['Opening']
    tables = {}
    for a in range(0x3fd9,0x414d,6):
        raw=opening[a:a+6]
        offset=int.from_bytes(raw[4:],'little')+0x2000
        tables.setdefault(offset,[]).append((a,raw))
    if output['Opening'][POOL:POOL_END] != bytes(POOL_END-POOL):
        raise ValueError('R01 resident UI pool is not empty')
    cursor=POOL
    manifest=[]
    geometry=[]
    if any(r['source']['disk']=='Opening' and r['source']['offset'] in (0x414d,0x4158,0x43f8) for r in records):
        geometry=widen_menus(output['Opening'],output['System'])
    if any(r['source']['disk']=='Opening' and r['source']['offset'] in (0x48c6, 0x44b1, 0x4478) for r in records):
        from profiles.alshark.r03_ui import widen_menus as widen_r03_menus
        geometry.extend(widen_r03_menus(output['Opening'], output['System']))
    from profiles.alshark.r06_ui import MENU_GEOMETRY, validate_translation, widen_menus as widen_r06_menus
    r06_offsets = {int.from_bytes(bytes.fromhex(raw)[4:], 'little') + 0x2000
                   for _, raw, _, _ in MENU_GEOMETRY}
    if any(r['source']['disk']=='Opening' and r['source']['offset'] in r06_offsets for r in records):
        geometry.extend(widen_r06_menus(output['Opening'], output['System']))
    for r in records:
        validate_translation(r)
        src=r['source'];disk=src['disk'];a=src['offset'];size=src['size']
        if images[disk][a:a+size] != bytes.fromhex(src['raw']):
            raise ValueError('UI immutable source mismatch')
        value=r['target']['inGameEnglish'];patches=[]
        if r['kind']=='fixed_runtime_script':
            if disk!='System' or FIXED_RANGES.get(a)!=a+size:
                raise ValueError('Unreviewed fixed-runtime UI range')
            if not isinstance(value,dict) or set(value)!=FIXED_EDIT_IDS[a]:
                raise ValueError('Fixed-runtime adaptation must cover exactly the reviewed text spans')
            if any(not isinstance(text,str) or tuple(map(len,text.split('\n')))!=FIXED_SHAPES[a][ident]
                   for ident,text in value.items()):
                raise ValueError('Fixed-runtime glyph/field layout changed')
            patch_script_spans(output[disk],images[disk],a,a+size,value)
            patches.append(dict(disk=disk,offset=a,size=size))
        elif disk=='System' and a in R02_SCRAP_UI:
            if size != R02_SCRAP_UI[a]:
                raise ValueError('R02 scrap UI allocation changed')
            encoded = encode_scrap_ui(images['System'], a, value)
            if len(encoded) > size:
                raise ValueError(f'{r["id"]}: R02 scrap UI needs {len(encoded)}/{size} bytes')
            output[disk][a:a+size] = encoded.ljust(size, b'\0')
            patches.append(dict(disk=disk, offset=a, size=size))
        elif disk=='Opening' and a in START_LABELS:
            if not isinstance(value,str) or len(value)>7 or '\n' in value:
                raise ValueError('Startup label geometry exceeded')
            output[disk][a:a+size]=encode_ui(value.ljust(7))
            patches.append(dict(disk=disk,offset=a,size=size))
        elif disk=='Opening' and a in tables:
            lines=value.split('\n')
            for table,raw in tables[a]:
                width=output[disk][table];rows=raw[1]
                if len(lines)!=rows or any(len(line)>width for line in lines):
                    raise ValueError(f'{r["id"]}: menu geometry exceeded ({width}x{rows})')
            encoded=encode_ui(value)+b'\0'
            if cursor+len(encoded)>POOL_END:
                raise ValueError('R01 resident UI pool overflow')
            output[disk][cursor:cursor+len(encoded)]=encoded
            patches.append(dict(disk=disk,offset=cursor,size=len(encoded)))
            for table,_ in tables[a]:
                output[disk][table+4:table+6]=(cursor-0x2000).to_bytes(2,'little')
                patches.append(dict(disk=disk,offset=table+4,size=2))
            cursor+=len(encoded)
        else:
            max_rows=src['text'].count('@')+1
            if (not isinstance(value,str) or len(value.split('\n'))>max_rows
                    or any(len(line)>14 for line in value.split('\n'))):
                raise ValueError('Fixed UI layout exceeded')
            encoded=encode_ui(value)+b'\0'
            if len(encoded)>size:
                raise ValueError(f'{r["id"]}: fixed UI needs {len(encoded)}/{size} bytes')
            output[disk][a:a+size]=encoded.ljust(size,b'\0')
            patches.append(dict(disk=disk,offset=a,size=size))
        manifest.append(dict(id=r['id'],disk=disk,offset=a,size=size,patches=patches,
            canonicalReview=r['review']['basis'],adaptationHash=digest(str(value).encode()),runtime_verified=False))
    if geometry:
        manifest[0]['patches'].extend(dict(disk=x['disk'],offset=x['offset'],size=1) for x in geometry)
    return {disk:bytes(data) for disk,data in output.items()},manifest
