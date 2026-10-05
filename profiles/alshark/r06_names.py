"""Guarded R06 character and map labels, confined to reviewed original spans."""
from hashlib import sha256

from retrotext.localization import make_record
from profiles.alshark.names import BASE, SPANS, guard_original, encode_label as prior_encode_label
from profiles.alshark.r02_names import _specs as r02_specs
from profiles.alshark.r03_names import _specs as r03_specs
from profiles.alshark.r03_equipment import guard_specs as equipment_spans

SPECS = {'r06-location:0': (70324, 11, (66624,), ' >', 'ascii', 12, 65536), 'r06-location:31': (70661, 12, (66686,), ' ', 'ascii', 12, 65536), 'r06-star-name:011768': (71528, 14, (66880,), '', 'ascii', 12, 65536), 'r06-star-name:011776': (71542, 14, (66882,), '', 'ascii', 12, 65536), 'r06-star-name:011784': (71556, 14, (66884,), '', 'ascii', 12, 65536), 'r06-star-name:011792': (71570, 14, (66886,), '', 'ascii', 12, 65536), 'r06-star-name:0117a0': (71584, 14, (66888,), '', 'ascii', 12, 65536), 'r06-star-name:0117ae': (71598, 14, (66890,), '', 'ascii', 12, 65536), 'r06-star-name:0117bc': (71612, 14, (66892,), '', 'ascii', 12, 65536), 'r06-star-name:0117ca': (71626, 9, (66894, 66896), '', 'ascii', 12, 65536), 'r06-star-name:0117dd': (71645, 9, (66898, 66902), '', 'ascii', 12, 65536), 'r06-star-name:0117d3': (71635, 10, (66900, 66904, 66906), '', 'ascii', 12, 65536), 'r06-landing-name:0165a6': (91558, 8, (91466, 91468, 91470, 91472, 91474, 91476, 91478, 91480, 91544), '', 'ascii', 12, 81920), 'r06-landing-name:0165ae': (91566, 9, (91482, 91546), '', 'ascii', 12, 81920), 'r06-landing-name:0165b7': (91575, 10, (91484, 91548), '', 'ascii', 12, 81920), 'r06-landing-name:0165c1': (91585, 10, (91486,), '', 'ascii', 12, 81920), 'r06-landing-name:0165cb': (91595, 7, (91488, 91550), '', 'ascii', 12, 81920), 'r06-landing-name:0165d2': (91602, 10, (91490, 91552), '', 'ascii', 12, 81920), 'r06-landing-name:0165dc': (91612, 9, (91492, 91554), '', 'ascii', 12, 81920), 'r06-landing-name:0165e5': (91621, 11, (91494, 91556), '', 'ascii', 12, 81920), 'r06-landing-name:0165f0': (91632, 9, (91496,), '', 'ascii', 12, 81920), 'r06-landing-name:0165f9': (91641, 11, (91498,), '', 'ascii', 12, 81920), 'r06-landing-name:016604': (91652, 12, (91500,), '', 'ascii', 12, 81920), 'r06-landing-name:016610': (91664, 10, (91502,), '', 'ascii', 12, 81920), 'r06-landing-name:01661a': (91674, 9, (91504,), '', 'ascii', 12, 81920), 'r06-landing-name:016623': (91683, 10, (91506,), '', 'ascii', 12, 81920), 'r06-landing-name:01662d': (91693, 10, (91508,), '', 'ascii', 12, 81920), 'r06-landing-name:016637': (91703, 10, (91510,), '', 'ascii', 12, 81920), 'r06-landing-name:016641': (91713, 8, (91512,), '', 'ascii', 12, 81920), 'r06-landing-name:016649': (91721, 9, (91514,), '', 'ascii', 12, 81920), 'r06-landing-name:016652': (91730, 8, (91516,), '', 'ascii', 12, 81920), 'r06-landing-name:01665a': (91738, 7, (91518,), '', 'ascii', 12, 81920), 'r06-landing-name:016661': (91745, 8, (91520,), '', 'ascii', 12, 81920), 'r06-landing-name:016669': (91753, 8, (91522,), '', 'ascii', 12, 81920), 'r06-landing-name:016671': (91761, 9, (91524,), '', 'ascii', 12, 81920), 'r06-landing-name:01667a': (91770, 9, (91526,), '', 'ascii', 12, 81920), 'r06-landing-name:016683': (91779, 11, (91528,), '', 'ascii', 12, 81920), 'r06-landing-name:01668e': (91790, 11, (91530, 91532, 91534), '', 'ascii', 12, 81920), 'r06-landing-name:016699': (91801, 11, (91536, 91538), '', 'ascii', 12, 81920), 'r06-landing-name:0166a4': (91812, 11, (91540,), '', 'ascii', 12, 81920), 'r06-landing-name:0166af': (91823, 15, (91542,), '', 'ascii', 12, 81920)}
REQUIRED = set(SPECS)
EXPECTED = {'r06-location:0': 'SPACE', 'r06-location:31': 'MIL STN', 'r06-star-name:011768': 'M264 SYS', 'r06-star-name:011776': 'M861 SYS', 'r06-star-name:011784': 'W505 SYS', 'r06-star-name:011792': 'Z091 SYS', 'r06-star-name:0117a0': 'W183 SYS', 'r06-star-name:0117ae': 'Z127 SYS', 'r06-star-name:0117bc': 'Z254 SYS', 'r06-star-name:0117ca': 'MARS FED', 'r06-star-name:0117dd': 'WYURIA', 'r06-star-name:0117d3': 'ZOLIAS', 'r06-landing-name:0165a6': 'STEA', 'r06-landing-name:0165ae': 'MARS', 'r06-landing-name:0165b7': 'ZAJIL', 'r06-landing-name:0165c1': 'BYUTO', 'r06-landing-name:0165cb': 'HOM', 'r06-landing-name:0165d2': 'JUKE', 'r06-landing-name:0165dc': 'TILS', 'r06-landing-name:0165e5': 'WYULTRIA', 'r06-landing-name:0165f0': 'HYURIS', 'r06-landing-name:0165f9': 'BAIDEN', 'r06-landing-name:016604': 'BYUDOS', 'r06-landing-name:016610': 'BYEZA', 'r06-landing-name:01661a': 'NOMIKE', 'r06-landing-name:016623': 'SARTALIA', 'r06-landing-name:01662d': 'POREDA', 'r06-landing-name:016637': 'ZOKAHEL', 'r06-landing-name:016641': 'YOSNU', 'r06-landing-name:016649': 'VON', 'r06-landing-name:016652': 'ASK', 'r06-landing-name:01665a': 'SACHI', 'r06-landing-name:016661': 'TRIM', 'r06-landing-name:016669': 'GOR', 'r06-landing-name:016671': 'BORUA', 'r06-landing-name:01667a': 'CS STN', 'r06-landing-name:016683': 'MIL STN', 'r06-landing-name:01668e': 'SUPPLY STN', 'r06-landing-name:016699': 'DEF STN', 'r06-landing-name:0166a4': 'HIDDEN STN', 'r06-landing-name:0166af': 'BARBAS'}
POOLS = tuple((a,a+n,(ident,)) for ident,(a,n,*_) in SPECS.items())
POINTER_RANGES = ((0x10000,0x1055c,0x10000),(0x1654a,0x165a6,0x14000))


def encode_label(value,encoding,prefix):
    if any(c.isdigit() for c in value):
        if encoding!='ascii' or prefix:
            raise ValueError('R06 numbered label format changed')
        from profiles.alshark.menu_patch import encode_ui
        data=bytearray()
        for c in value:
            if 'A'<=c<='Z':data.extend(c.encode('ascii'))
            elif c==' ':data.extend(b'>')
            elif '0'<=c<='9':data.extend(encode_ui(c))
            else:raise ValueError('R06 unsupported numbered label glyph')
        return bytes(data)+b'\0'
    return prior_encode_label(value,encoding,prefix)


def _guard(source):
    prior = [(a, z) for a, z, _ in SPANS]
    prior += [(a, a+n) for _, a, n, _, _, _ in (*r02_specs(), *r03_specs())]
    prior += equipment_spans(source)
    from profiles.alshark.r04_names import POOLS as r04_pools
    prior += [(a,z) for a,z,_ in r04_pools]
    from profiles.alshark.r05_names import POOLS as r05_pools
    prior += [(a,z) for a,z,_ in r05_pools]
    for a, z, _ in POOLS:
        if any(a < old_z and old_a < z for old_a, old_z in prior):
            raise ValueError('R06 name pool overlaps prior allocation')
    known = {p for _, _, pointers, _, _, _, _ in SPECS.values() for p in pointers}
    for ident, (a, n, pointers, prefix, _, _, base) in SPECS.items():
        raw = source[a:a+n]
        if len(raw) != n or raw[-1:] != b'\0' or b'\0' in raw[:-1]:
            raise ValueError(f'{ident}: source extent changed')
        if not raw.startswith(prefix.encode('ascii')):
            raise ValueError(f'{ident}: location prefix changed')
        for p in pointers:
            if source[p:p+2] != (a-base).to_bytes(2, 'little'):
                raise ValueError(f'{ident}: original alias changed at {p:#x}')
    for left,right,base in POINTER_RANGES:
        for p in range(left,right,2):
            a=base+int.from_bytes(source[p:p+2],'little')
            if any(start<=a<end for start,end,_ in POOLS) and p not in known:
                raise ValueError(f'Unreviewed R06 name alias at {p:#x}')


def export_records(images):
    guard_original(images)
    source = images['System']
    _guard(source)
    result = []
    for ident, (a, n, pointers, prefix, encoding, limit, base) in SPECS.items():
        raw = source[a:a+n]
        result.append(make_record(ident, 'name', dict(
            disk='System', offset=a, size=n, raw=raw.hex(),
            text=raw[:-1].decode('cp932'), sha256=sha256(raw).hexdigest(),
            pointers=[dict(offset=p, raw=source[p:p+2].hex()) for p in pointers],
            allocationGroup='r06-required-names', maximumCells=limit,
            prefix=prefix, encoding=encoding, pointerBase=base)))
    return result


def compile_names(images, translations):
    guard_original(images)
    if not isinstance(translations, dict) or set(translations) != REQUIRED:
        raise ValueError('Complete R06 name allocation group required')
    if translations != EXPECTED:
        raise ValueError('R06 spellings changed; review runtime widths and allocation plan')
    source = images['System']
    _guard(source)
    output = bytearray(source)
    records, patches = [], []
    for a, z, identifiers in POOLS:
        data, destinations = bytearray(), {}
        for ident in identifiers:
            _, _, pointers, prefix, encoding, limit, base = SPECS[ident]
            value = translations[ident]
            if len(value) > limit:
                raise ValueError(f'{ident}: runtime field overflow')
            raw = encode_label(value, encoding, prefix)
            if raw not in destinations:
                destinations[raw] = a + len(data)
                data.extend(raw)
            offset = destinations[raw]
            records.append(dict(record=ident, text=value, offset=offset,
                                used=len(raw), pointers=list(pointers), encoding=encoding))
            for p in pointers:
                output[p:p+2] = (offset-base).to_bytes(2, 'little')
                patches.append(dict(offset=p, size=2))
        if len(data) > z-a:
            raise ValueError('R06 original name allocation overflow')
        output[a:z] = data.ljust(z-a, b'\0')
        patches.append(dict(offset=a, size=z-a))
    return bytes(output), dict(records=records, patches=patches)
