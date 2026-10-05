"""Guarded R02 item, Joe-ability and location labels in original name storage."""
import hashlib
from functools import lru_cache

from retrotext.localization import make_record
from profiles.alshark.names import BASE, SPANS as R01_SPANS, guard_original, encode_label

# Offset, original byte count including NUL, and every original pointer alias.
# Item 01 and 31 are excluded after the shop handler classified those payload
# positions as a selector and cancel option rather than displayed stock.
ITEMS = {
    0x1b: (0x1087d, 9, (0x10036,)),
    0x1d: (0x10891, 10, (0x1003a,)),
    0x23: (0x108ce, 9, (0x10046,)),
    0x3d: (0x109a1, 4, (0x1007a,)),
    0x44: (0x109d3, 7, (0x10088,)),
    0x4d: (0x10a03, 12, (0x10098, 0x1009a)),
    0x51: (0x10a30, 9, (0x100a2,)),
    0x75: (0x10b3f, 9, (0x100ea,)),
    0x93: (0x10c23, 10, (0x10126,)),
    0x9a: (0x10c67, 10, (0x10134,)),
    0x9c: (0x10c7d, 7, (0x10138,)),
    0xa3: (0x10cb9, 12, (0x10146,)),
}
ABILITIES = {
    # Joe starts with combat ID 23; class 7 learns ID 24 above IQ 1260.
    # These IDs are ability-local and distinct from item ID 23.
    0x23: (0x11136, 12, (0x1033e, 0x10340, 0x10342, 0x10344, 0x10346)),
    0x24: (0x11142, 10, (0x10348,)),
    # IDs 3e/3f/40 share the original Performance Analysis storage.
    0x40: (0x111b7, 9, (0x1037c, 0x1037e, 0x10380)),
    0x41: (0x111c0, 5, (0x10382,)),
    0x42: (0x111c5, 7, (0x10384,)),
}
LOCATIONS = {
    2: (0x112c8, 11, (0x10444,), '  '),
    48: (0x114b4, 11, (0x104a0,), ' >'),
    98: (0x1170e, 9, (0x10504,), '  '),
    103: (0x11744, 13, (0x1050e,), ' >'),
}
GROUPS = (
    ('r02-item', ITEMS, 9),
    ('r02-ability', ABILITIES, 8),
    ('r02-location', LOCATIONS, 12),
)
REQUIRED = {f'{prefix}:{key}' if prefix == 'r02-location' else f'{prefix}:{key:02x}'
            for prefix, entries, _ in GROUPS for key in entries}


def _ident(prefix, key):
    return f'{prefix}:{key}' if prefix == 'r02-location' else f'{prefix}:{key:02x}'


def _specs():
    for prefix, entries, limit in GROUPS:
        for key, spec in entries.items():
            a, size, pointers = spec[:3]
            marker = spec[3] if prefix == 'r02-location' else ''
            yield _ident(prefix, key), a, size, pointers, marker, limit


def _guard_spans(source):
    specs = list(_specs())
    spans = sorted((a, a+size) for _, a, size, _, _, _ in specs)
    if any(z > next_a for (_, z), (next_a, _) in zip(spans, spans[1:])):
        raise ValueError('Overlapping R02 name sources')
    if any(a < r01_z and r01_a < z for a, z in spans for r01_a, r01_z, _ in R01_SPANS):
        raise ValueError('R02 name storage overlaps R01 names')
    expected_pointers = {p for _, _, _, pointers, _, _ in specs for p in pointers}
    if len(expected_pointers) != sum(len(pointers) for _, _, _, pointers, _, _ in specs):
        raise ValueError('Duplicate R02 name pointer')
    for ident, a, size, pointers, marker, _ in specs:
        raw = source[a:a+size]
        if len(raw) != size or raw[-1:] != b'\0' or b'\0' in raw[:-1]:
            raise ValueError(f'{ident}: original source span changed')
        if marker and not raw.startswith(marker.encode('ascii')):
            raise ValueError(f'{ident}: original location marker changed')
        for p in pointers:
            if source[p:p+2] != (a-BASE).to_bytes(2, 'little'):
                raise ValueError(f'{ident}: pointer source mismatch at {p:#x}')
    for p in range(BASE, 0x105a0, 2):
        target = BASE+int.from_bytes(source[p:p+2], 'little')
        if any(a <= target < z for a, z in spans) and p not in expected_pointers:
            raise ValueError(f'Unreviewed alias into R02 name storage at {p:#x}')
    return specs, spans


def export_records(images):
    guard_original(images)
    source = images['System']
    specs, _ = _guard_spans(source)
    records = []
    for ident, a, size, pointers, marker, limit in specs:
        raw = source[a:a+size]
        records.append(make_record(ident, 'name', dict(
            disk='System', offset=a, size=size, raw=raw.hex(),
            text=raw[:-1].decode('cp932'), sha256=hashlib.sha256(raw).hexdigest(),
            pointers=[dict(offset=p, raw=source[p:p+2].hex()) for p in pointers],
            allocationGroup='r02-required-names', rendererOffset=0x1b0b1,
            maximumCells=limit, prefix=marker)))
    return records


def compile_names(images, translations):
    """Return (System bytes, records/patches), preserving nonreviewed bytes."""
    guard_original(images)
    if not isinstance(translations, dict) or set(translations) != REQUIRED:
        raise ValueError('Complete R02 name allocation group required')
    source = images['System']
    specs, source_spans = _guard_spans(source)
    pending = []
    for ident, _, _, pointers, marker, limit in specs:
        value = translations[ident]
        if ident.startswith('r02-item:'):
            limit = 8  # Nine-cell selection includes its item icon.
        if not isinstance(value, str) or len(value) > limit:
            raise ValueError(f'{ident}: exceeds {limit}-cell runtime field')
        pending.append((ident, value, encode_label(value, 'ascii', marker), pointers))

    # Merge only directly adjoining, individually guarded original strings.
    # The 11136..1114c and 111b7..111cc ability groups each consist only of
    # contiguous reviewed strings. Merging such spans permits clear labels
    # without consuming unknown data or altering an unreviewed source range.
    spans = []
    for a, z in source_spans:
        if spans and spans[-1][1] == a:
            spans[-1] = (spans[-1][0], z)
        else:
            spans.append((a, z))
    ordered = sorted(pending, key=lambda x: (-len(x[2]), x[0]))
    capacities = tuple(z-a for a, z in spans)

    @lru_cache(None)
    def place(index, remaining):
        if index == len(ordered):
            return ()
        length = len(ordered[index][2])
        seen = set()
        for bin_index, capacity in enumerate(remaining):
            if capacity < length or capacity in seen:
                continue
            seen.add(capacity)
            after = list(remaining)
            after[bin_index] -= length
            tail = place(index+1, tuple(after))
            if tail is not None:
                return (bin_index,) + tail
        return None

    assignment = place(0, capacities)
    if assignment is None:
        raise ValueError('R02 reviewed original allocations cannot fit all labels')
    bins = {a: bytearray() for a, _ in spans}
    placements = []
    for (ident, value, raw, pointers), bin_index in zip(ordered, assignment):
        start = spans[bin_index][0]
        destination = start+len(bins[start])
        bins[start].extend(raw)
        placements.append(dict(record=ident, text=value, offset=destination,
                               used=len(raw), pointers=list(pointers), encoding='ascii'))
    output = bytearray(source)
    patches = []
    for a, z in spans:
        output[a:z] = bins[a].ljust(z-a, b'\0')
        patches.append(dict(offset=a, size=z-a))
    for record in placements:
        for p in record['pointers']:
            output[p:p+2] = (record['offset']-BASE).to_bytes(2, 'little')
            patches.append(dict(offset=p, size=2))
    return bytes(output), dict(records=placements, patches=patches)
