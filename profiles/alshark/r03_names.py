"""Guarded R03 spaceport, mine and cockpit titles in original name storage."""
import hashlib
from functools import lru_cache

from retrotext.localization import make_record
from profiles.alshark.names import BASE, SPANS as R01_SPANS, guard_original, encode_label
from profiles.alshark.r02_names import _specs as r02_specs

# Original byte counts include NUL; every source pointer alias is listed.
LOCATIONS = {
    1: (0x112bf, 9, (0x10442,), ' >'),
    42: (0x1146c, 11, (0x10494,), ' >'),
    96: (0x116fe, 8, (0x10500,), '  '),
}
# The pointer tables end before the 24-bit progression values at 0x1055c.
POINTER_END = 0x1055c
POINTER_DELTAS = {}
GROUPS = (('r03-location', LOCATIONS, 12),)
REQUIRED = {f'r03-location:{key}' for key in LOCATIONS}


def _ident(prefix, key):
    return f'{prefix}:{key}' if prefix == 'r03-location' else f'{prefix}:{key:02x}'


def _specs():
    for prefix, entries, limit in GROUPS:
        for key, spec in entries.items():
            a, size, pointers = spec[:3]
            marker = spec[3] if prefix == 'r03-location' else ''
            yield _ident(prefix, key), a, size, pointers, marker, limit


def _guard_spans(source):
    specs = list(_specs())
    spans = sorted((a, a+size) for _, a, size, _, _, _ in specs)
    if any(z > next_a for (_, z), (next_a, _) in zip(spans, spans[1:])):
        raise ValueError('Overlapping R03 name sources')
    if any(a < r01_z and r01_a < z for a, z in spans for r01_a, r01_z, _ in R01_SPANS):
        raise ValueError('R03 name storage overlaps R01 names')
    prior_spans = [(a, a+size) for _, a, size, _, _, _ in r02_specs()]
    if any(a < old_z and old_a < z for a, z in spans for old_a, old_z in prior_spans):
        raise ValueError('R03 name storage overlaps R02 names')
    expected_pointers = {p for _, _, _, pointers, _, _ in specs for p in pointers}
    if len(expected_pointers) != sum(len(pointers) for _, _, _, pointers, _, _ in specs):
        raise ValueError('Duplicate R03 name pointer')
    for ident, a, size, pointers, marker, _ in specs:
        raw = source[a:a+size]
        if len(raw) != size or raw[-1:] != b'\0' or b'\0' in raw[:-1]:
            raise ValueError(f'{ident}: original source span changed')
        if marker and not raw.startswith(marker.encode('ascii')):
            raise ValueError(f'{ident}: original location marker changed')
        for p in pointers:
            if source[p:p+2] != (a+POINTER_DELTAS.get(p, 0)-BASE).to_bytes(2, 'little'):
                raise ValueError(f'{ident}: pointer source mismatch at {p:#x}')
    for p in range(BASE, POINTER_END, 2):
        target = BASE+int.from_bytes(source[p:p+2], 'little')
        if any(a <= target < z for a, z in spans) and p not in expected_pointers:
            raise ValueError(f'Unreviewed alias into R03 name storage at {p:#x}')
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
            pointers=[dict(offset=p, raw=source[p:p+2].hex(), delta=POINTER_DELTAS.get(p, 0)) for p in pointers],
            allocationGroup='r03-required-names', rendererOffset=0x1b0b1,
            maximumCells=limit, prefix=marker)))
    return records


def compile_names(images, translations):
    """Return (System bytes, records/patches), preserving nonreviewed bytes."""
    guard_original(images)
    if not isinstance(translations, dict) or set(translations) != REQUIRED:
        raise ValueError('Complete R03 name allocation group required')
    source = images['System']
    specs, source_spans = _guard_spans(source)
    pending = []
    for ident, _, _, pointers, marker, limit in specs:
        value = translations[ident]
        if not isinstance(value, str) or len(value) > limit:
            raise ValueError(f'{ident}: exceeds {limit}-cell runtime field')
        pending.append((ident, value, encode_label(value, 'ascii', marker), pointers))

    # Use only individually guarded original strings, merging adjacent spans.
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
        raise ValueError('R03 reviewed original allocations cannot fit all labels')
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
            output[p:p+2] = (record['offset']+POINTER_DELTAS.get(p, 0)-BASE).to_bytes(2, 'little')
            patches.append(dict(offset=p, size=2))
    return bytes(output), dict(records=placements, patches=patches)
