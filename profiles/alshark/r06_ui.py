"""Source-guarded flight menu geometry and runtime destination fields."""

# Opening box geometry and System overlay selection instruction(s).
# Selection widths are bytes (two bytes per full-width cell).
MENU_GEOMETRY = (
    (0x40bd, '02022e37b227', 6, ((0x16517,4),)),
    (0x4021, '050404233024', 6, ((0x827a,10),)),
    (0x404b, '030212280e25', 4, ((0xc697,6),)),
    (0x411d, '040224412729', 6, ((0x1ab02,8),)),
    (0x40b1, '05051c1e7d27', 7, ((0x16d33,10),)),
    (0x40b7, '05041c1e8827', 7, ((0x16d33,10),)),
    (0x40e1, '05051c1e4928', 7, ((0x1aa31,10),)),
    (0x40e7, '04021e237a28', 6, ((0x1aa7c,8),)),
    (0x40ed, '04011e238d28', 6, ((0x1aaba,8),)),
)

DESTINATION_FIELDS = {'ui:Opening:0047e0', 'ui:Opening:004897'}


def validate_translation(record):
    """Reserve the first prompt row for the runtime destination name.

    Both original four-row prompts place the injected name at DI=321c,
    leaving row two blank and the confirmation on the final row.
    """
    if record['id'] not in DESTINATION_FIELDS:
        return
    value = record['target']['inGameEnglish']
    if not isinstance(value,str):
        raise ValueError('R06 destination prompt requires text')
    lines=value.split('\n')
    if (len(lines)!=4 or lines[0] or lines[2] or not lines[1] or not lines[3]
            or any(len(line)>12 for line in lines)):
        raise ValueError('R06 destination runtime field / confirmation rows changed')


def widen_menus(opening,system):
    """Apply only to originals before pointer relocation; keep anchors/rows."""
    selections={}
    for offset,raw,width,instructions in MENU_GEOMETRY:
        expected=bytes.fromhex(raw)
        if opening[offset:offset+6]!=expected:
            raise ValueError('R06 menu source geometry changed')
        if expected[2]//2+width>40:
            raise ValueError('R06 menu exceeds screen')
        for instruction,old in instructions:
            field = b'\x3e\x1d' if instruction in (0x827a,0xc697) else b'\x09\x17'
            if system[instruction:instruction+5]!=b'\xc6\x06'+field+bytes([old]):
                raise ValueError('R06 menu selection geometry changed')
            patch=(old,width*2)
            if instruction in selections and selections[instruction]!=patch:
                raise ValueError('R06 conflicting selection geometry')
            selections[instruction]=patch
    patches=[]
    for offset,raw,width,_ in MENU_GEOMETRY:
        old=opening[offset];opening[offset]=width
        patches.append(dict(disk='Opening',offset=offset,before=old,after=width,
                            purpose='R06 flight menu width',runtime_verified=False))
    for instruction,(old,new) in selections.items():
        system[instruction+4]=new
        patches.append(dict(disk='System',offset=instruction+4,before=old,after=new,
                            purpose='R06 flight selection width',runtime_verified=False))
    return patches


# Existing strings outside the resident menu table use the flight overlay's
# uppercase glyph dispatch and one-cell '>' skip, not the generic UI encoder.
FIXED_SPECS = {0x1714e:10, 0x1a035:25, 0x1734f:37}
REQUIRED = frozenset(f'ui:System:{a:06x}' for a in FIXED_SPECS)


def export_records(images):
    from profiles.alshark.names import guard_original
    from profiles.alshark.script import digest
    from retrotext.localization import make_record
    guard_original(images)
    result=[]
    for a,n in FIXED_SPECS.items():
        raw=images['System'][a:a+n]
        if raw[-1:]!=b'\0' or b'\0' in raw[:-1]:
            raise ValueError('R06 flight literal extent changed')
        result.append(make_record(f'ui:System:{a:06x}','ui',dict(
            disk='System',offset=a,size=n,raw=raw.hex(),text=raw[:-1].decode('cp932'),
            sha256=digest(raw))))
    return result


def encode_fixed(offset,value):
    from profiles.alshark.menu_patch import encode_ui
    if not isinstance(value,str) or not value:
        raise ValueError('R06 flight literal requires text')
    if offset==0x1734f:
        lines=value.split('\n')
        if (len(lines)!=4 or any(not l or len(l)>4 for l in lines[:3])
                or len(lines[3])!=12 or lines[3][4:8]!=' '*4):
            raise ValueError('R06 star header overwrites runtime fields')
    elif offset==0x1714e:
        if value!='ATRAIA':
            raise ValueError('R06 ship HUD spelling/field changed')
    elif offset==0x1a035:
        if '\n' in value or len(value)>14:
            raise ValueError('R06 fighter loss exceeds message field')
    else:
        raise ValueError('Unknown R06 flight literal')
    raw=bytearray()
    for c in value:
        if c=='\n':raw.extend(b'@')
        elif c==' ':raw.extend(b'>')
        elif 'A'<=c<='Z':raw.extend(c.encode('ascii'))
        else:raw.extend(encode_ui(c))
    raw.append(0)
    if len(raw)>FIXED_SPECS[offset]:
        raise ValueError('R06 flight literal allocation overflow')
    return bytes(raw)


def compile_records(images,records):
    source={r['id']:r for r in export_records(images)}
    system=images['System']
    if system[0x171eb:0x17209]!=bytes.fromhex(
            '3c3e743c3c2074353c4074393c41720f3c5b730b8ad8b419cd418bd0eb19'):
        raise ValueError('R06 flight renderer source changed')
    output={disk:bytearray(data) for disk,data in images.items()}
    seen=set();manifest=[]
    for record in records:
        ident=record['id']
        if ident not in source or ident in seen or record['source']!=source[ident]['source']:
            raise ValueError('R06 immutable flight source changed or duplicate')
        seen.add(ident);spec=record['source'];a=spec['offset'];n=spec['size']
        raw=encode_fixed(a,record['target']['inGameEnglish'])
        output['System'][a:a+n]=raw.ljust(n,b'\0')
        manifest.append(dict(id=ident,disk='System',offset=a,size=n,
            patches=[dict(disk='System',offset=a,size=n)]))
    return {disk:bytes(data) for disk,data in output.items()},manifest
