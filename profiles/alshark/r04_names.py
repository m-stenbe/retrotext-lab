"""Guarded R04 character and map labels, confined to reviewed original spans."""
from hashlib import sha256

from retrotext.localization import make_record
from profiles.alshark.names import BASE, SPANS, guard_original, encode_label
from profiles.alshark.r02_names import _specs as r02_specs
from profiles.alshark.r03_names import _specs as r03_specs
from profiles.alshark.r03_equipment import guard_specs as equipment_spans

# Shared name slots 8/9 retain distinct canonical records. Their displayed given
# name deliberately shares one full-width string, as with earlier party names.
SPECS = {
    'name:8': (0x11214, 6, (0x10410,), '', 'wide', 8),
    'name:9': (0x1121a, 13, (0x10412,), '', 'wide', 8),
    'r04-location:30': (0x113fb, 10, (0x1047c,), ' ', 'ascii', 12),
    'r04-location:104': (0x11751, 8,
        tuple(range(0x10510, 0x10532, 2)) + tuple(range(0x10536, 0x10540, 2)),
        '  ', 'ascii', 12),
}
REQUIRED = set(SPECS)
RENDERED_NAMES = {8: 'WELDA', 9: 'WELDA'}
EXPECTED = {'name:8': 'WELDA', 'name:9': 'WELDA',
            'r04-location:30': 'CS STN', 'r04-location:104': 'SHIP'}
POINTER_END = 0x1055c
POOLS = ((0x11214, 0x11227, ('name:8', 'name:9')),
         (0x113fb, 0x11405, ('r04-location:30',)),
         (0x11751, 0x11759, ('r04-location:104',)))


def _guard(source):
    prior = [(a, z) for a, z, _ in SPANS]
    prior += [(a, a+n) for _, a, n, _, _, _ in (*r02_specs(), *r03_specs())]
    prior += equipment_spans(source)
    for a, z, _ in POOLS:
        if any(a < old_z and old_a < z for old_a, old_z in prior):
            raise ValueError('R04 name pool overlaps prior allocation')
    known = {p for _, _, pointers, _, _, _ in SPECS.values() for p in pointers}
    for ident, (a, n, pointers, prefix, _, _) in SPECS.items():
        raw = source[a:a+n]
        if len(raw) != n or raw[-1:] != b'\0' or b'\0' in raw[:-1]:
            raise ValueError(f'{ident}: source extent changed')
        if not raw.startswith(prefix.encode('ascii')):
            raise ValueError(f'{ident}: location prefix changed')
        for p in pointers:
            if source[p:p+2] != (a-BASE).to_bytes(2, 'little'):
                raise ValueError(f'{ident}: original alias changed at {p:#x}')
    for p in range(BASE, POINTER_END, 2):
        a = BASE + int.from_bytes(source[p:p+2], 'little')
        if any(left <= a < right for left, right, _ in POOLS) and p not in known:
            raise ValueError(f'Unreviewed R04 name alias at {p:#x}')


def export_records(images):
    guard_original(images)
    source = images['System']
    _guard(source)
    result = []
    for ident, (a, n, pointers, prefix, encoding, limit) in SPECS.items():
        raw = source[a:a+n]
        result.append(make_record(ident, 'name', dict(
            disk='System', offset=a, size=n, raw=raw.hex(),
            text=raw[:-1].decode('cp932'), sha256=sha256(raw).hexdigest(),
            pointers=[dict(offset=p, raw=source[p:p+2].hex()) for p in pointers],
            allocationGroup='r04-required-names', maximumCells=limit,
            prefix=prefix, encoding=encoding)))
    return result


def compile_names(images, translations):
    guard_original(images)
    if not isinstance(translations, dict) or set(translations) != REQUIRED:
        raise ValueError('Complete R04 name allocation group required')
    if translations != EXPECTED:
        raise ValueError('R04 spellings changed; review runtime widths and allocation plan')
    source = images['System']
    _guard(source)
    output = bytearray(source)
    records, patches = [], []
    for a, z, identifiers in POOLS:
        data, destinations = bytearray(), {}
        for ident in identifiers:
            _, _, pointers, prefix, encoding, limit = SPECS[ident]
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
                output[p:p+2] = (offset-BASE).to_bytes(2, 'little')
                patches.append(dict(offset=p, size=2))
        if len(data) > z-a:
            raise ValueError('R04 original name allocation overflow')
        output[a:z] = data.ljust(z-a, b'\0')
        patches.append(dict(offset=a, size=z-a))
    return bytes(output), dict(records=records, patches=patches)
