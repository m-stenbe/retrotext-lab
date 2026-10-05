#!/usr/bin/env python3
"""Export conservative editable records; import within existing entry allocations."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from retrotext.banks import relative_table
from profiles.alshark.script import Unsupported, decode_entry, digest, rebuild_entry

SYSTEM_HASH = '7df885bfe0bacb7c37809364a993e6ad506e5cd25eac1882eac6c7627bce75d5'
EDITABLE_IDS = {
    f'051000:{index:03d}' for index in (
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
        19, 20, 21, 24, 25, 26, 28, 29, 30, 34, 35, 36, 37, 41,
    )
} | {'061000:019', '061000:020', '061000:021', '061000:022', '082000:000', '082000:001', '082000:002', '082000:007', '082000:014', '07f000:038', '07f000:039', '07f000:041', '07f000:042', '053000:000', '053000:013', '054000:000'} | {
    f'052000:{index:03d}' for index in (1, 9, 13, 14, 15, 42, 43, 44, 45, 83)
}

# R02 Hamack map48 NPC roots: original counted commands/entry indices stay fixed.
EDITABLE_IDS |= {f'052000:{i:03d}' for i in
                 (0,2,3,4,5,6,7,8,10,11,12,16,17,18,19,20,21,84)}


# R02 connected text allocations; immutable dispatch/call bytes retain targets.
# Route and handler evidence: docs/r02-re-source-evidence.md.
EDITABLE_IDS |= ({f'051000:{i:03d}' for i in (22,23,27)}
                 | {f'052000:{i:03d}' for i in
                    (*range(22,38), *range(39,77), 78,79,80,81,82)}
                 | {f'053000:{i:03d}' for i in
                    (*range(1,13), *range(14,28),35,36,37)}
                 | {'054000:035','05a000:039'}
                 | {f'082000:{i:03d}' for i in (11,12,13,17,18,19,20,21,22,23)})


# R03 Hom spaceport and abandoned-mine sources; see r03 RE evidence.
EDITABLE_IDS |= ({f'054000:{i:03d}' for i in (1,2,3,*range(6,30),31,33,34)}
                 | {'082000:024','07d000:032','07d000:033','07d000:034',
                    '083000:001','083000:004','083000:005'})

# R04 rescue, station induction/tour and first briefing. Source closure and
# counted branch/call evidence: r04_flow.py and docs/r04-re-source-evidence.md.
R04_EDITABLE_IDS = ({'054000:032', '055000:001', '055000:002', '055000:004'}
    | {f'05c000:{i:03}' for i in (*range(9), *range(10,15),16,17,18,20,21,22,23,24,26,36,37)}
    | {'05d000:000','05d000:001','07d000:030','07d000:031',
       '081000:000','081000:001','081000:002','082000:003',
       '083000:002','083000:007','083000:008','083000:012'})
EDITABLE_IDS |= R04_EDITABLE_IDS


# R05 source-mapped initial Zajil towns, port and kidnapping route.
# Exact immutable flow inventory: r05_flow.py and docs/r05-re-source-evidence.md.
R05_EDITABLE_IDS = {
    '053000:029',
    '053000:030',
    '053000:031',
    '053000:032',
    '053000:033',
    '053000:034',
    '053000:038',
    '057000:033',
    '05a000:000',
    '05a000:001',
    '05a000:002',
    '05a000:003',
    '05a000:004',
    '05a000:005',
    '05a000:006',
    '05a000:007',
    '05a000:008',
    '05a000:009',
    '05a000:010',
    '05a000:011',
    '05a000:013',
    '05a000:015',
    '05a000:016',
    '05a000:018',
    '05a000:029',
    '05a000:030',
    '05a000:031',
    '05a000:032',
    '05a000:033',
    '05a000:034',
    '05a000:035',
    '05a000:036',
    '05a000:037',
    '05a000:038',
    '05b000:000',
    '05b000:001',
    '05b000:002',
    '05b000:003',
    '05b000:004',
    '05b000:005',
    '05b000:006',
    '05b000:007',
    '05b000:008',
    '05b000:009',
    '05b000:010',
    '05b000:011',
    '05b000:012',
    '05b000:013',
    '05b000:014',
    '05b000:015',
    '05b000:017',
    '05b000:018',
    '05b000:019',
    '05b000:020',
    '05b000:021',
    '05b000:022',
    '05b000:023',
    '05b000:024',
    '05b000:025',
    '05b000:026',
    '05b000:027',
    '05b000:028',
    '05b000:029',
    '05b000:030',
    '05b000:031',
    '05b000:032',
    '05b000:033',
    '05b000:034',
    '05b000:035',
    '05b000:037',
    '05b000:038',
    '05b000:043',
    '05f000:001',
    '05f000:002',
    '05f000:003',
    '05f000:004',
    '05f000:005',
    '05f000:006',
    '05f000:007',
    '05f000:008',
    '05f000:009',
    '05f000:010',
    '05f000:013',
    '05f000:014',
    '05f000:015',
    '05f000:018',
    '05f000:019',
    '05f000:020',
    '05f000:021',
    '05f000:022',
    '05f000:027',
    '05f000:050',
    '05f000:057',
    '081000:003',
    '081000:004',
    '081000:005',
    '081000:006',
    '081000:007',
}
EDITABLE_IDS |= R05_EDITABLE_IDS


# R06 source-mapped Porkin pursuit and military-station rescue.
# Guarded roots, calls and story-state bounds live in r06_flow.py.
R06_EDITABLE_IDS = {
    '05a000:012',
    '05a000:014',
    '05a000:017',
    '05a000:019',
    '05a000:020',
    '05a000:021',
    '05a000:022',
    '05a000:023',
    '05a000:024',
    '05a000:025',
    '05a000:026',
    '05a000:027',
    '05a000:028',
    '05b000:036',
    '05b000:039',
    '05b000:040',
    '05b000:041',
    '05b000:042',
    '05b000:044',
    '05b000:045',
    '05e000:000',
    '05e000:001',
    '05e000:002',
    '05e000:003',
    '05e000:004',
    '05e000:005',
    '05e000:006',
    '05e000:007',
    '05e000:008',
    '05e000:009',
    '05e000:010',
    '05e000:011',
    '05e000:013',
    '05e000:014',
    '05e000:015',
    '05e000:016',
    '05e000:017',
    '05e000:018',
    '05e000:019',
    '05e000:020',
    '05e000:021',
    '05e000:022',
    '05e000:023',
    '05e000:024',
    '05e000:025',
    '05e000:026',
    '05e000:027',
    '05e000:028',
    '081000:008',
    '081000:009',
    '081000:010',
    '081000:011',
    '081000:012',
}
EDITABLE_IDS |= R06_EDITABLE_IDS

# Source-mapped CS assignment, Byuto settlement/mine and connected party talk.
# See r07_flow.py and docs/r07-re-source-evidence.md.
R07_EDITABLE_IDS = ({f'053000:{i:03}' for i in range(39,44)}
    | {f'05c000:{i:03}' for i in (25,29,35,38,39,40,41)}
    | {f'060000:{i:03}' for i in (*range(30),31)}
    | {f'081000:{i:03}' for i in range(13,22)}
    | {'083000:013', '083000:014'})
EDITABLE_IDS |= R07_EDITABLE_IDS

# Source-mapped Mars leave, capital investigation and optional mainland Begi.
# See r08_flow.py and docs/r08-re-source-evidence.md.
R08_EDITABLE_IDS = {
    '053000:044',
    '053000:045',
    '053000:046',
    '053000:047',
    '053000:049',
    '053000:050',
    '053000:051',
    '053000:054',
    '053000:055',
    '053000:056',
    '053000:057',
    '057000:000',
    '057000:001',
    '057000:002',
    '057000:003',
    '057000:004',
    '057000:005',
    '057000:006',
    '057000:007',
    '057000:008',
    '057000:009',
    '057000:010',
    '057000:011',
    '057000:012',
    '057000:013',
    '057000:014',
    '057000:015',
    '057000:016',
    '057000:017',
    '057000:018',
    '057000:019',
    '057000:020',
    '057000:021',
    '057000:022',
    '057000:023',
    '057000:024',
    '057000:025',
    '057000:026',
    '057000:027',
    '057000:028',
    '057000:029',
    '057000:030',
    '057000:031',
    '057000:032',
    '057000:034',
    '057000:035',
    '057000:036',
    '057000:038',
    '057000:039',
    '057000:040',
    '057000:041',
    '057000:042',
    '057000:043',
    '057000:044',
    '057000:045',
    '057000:046',
    '057000:047',
    '057000:048',
    '057000:049',
    '057000:051',
    '057000:056',
    '057000:057',
    '057000:058',
    '057000:059',
    '057000:060',
    '057000:061',
    '057000:062',
    '05c000:028',
    '05c000:030',
    '05c000:031',
    '05c000:032',
    '05c000:033',
    '05c000:034',
    '05d000:002',
    '05f000:031',
    '05f000:032',
    '05f000:033',
    '05f000:034',
    '05f000:035',
    '05f000:036',
    '05f000:037',
    '05f000:038',
    '05f000:039',
    '05f000:040',
    '05f000:041',
    '05f000:042',
    '05f000:043',
    '05f000:056',
    '05f000:058',
    '05f000:059',
    '061000:000',
    '061000:001',
    '061000:002',
    '061000:003',
    '061000:004',
    '061000:005',
    '061000:006',
    '061000:007',
    '061000:008',
    '061000:009',
    '061000:010',
    '061000:011',
    '061000:012',
    '061000:014',
    '061000:015',
    '061000:016',
    '061000:017',
    '061000:018',
    '063000:000',
    '063000:001',
    '063000:002',
    '063000:003',
    '063000:004',
    '063000:005',
    '063000:006',
    '063000:008',
    '063000:009',
    '063000:010',
    '063000:011',
    '063000:012',
    '063000:013',
    '063000:014',
    '063000:015',
    '063000:016',
    '063000:017',
    '063000:018',
    '063000:020',
    '063000:029',
    '063000:030',
    '063000:031',
    '063000:032',
    '063000:033',
    '063000:034',
    '063000:035',
    '063000:036',
    '063000:037',
    '078000:000',
    '078000:001',
    '078000:002',
    '078000:003',
    '078000:004',
    '078000:005',
    '081000:022',
    '081000:023',
    '081000:024',
    '081000:025',
    '081000:026',
    '081000:027',
    '081000:028',
}
EDITABLE_IDS |= R08_EDITABLE_IDS


# Source-mapped Daina reunion and Begi historian follow-through; see r09_flow.py.
R09_EDITABLE_IDS = {
    '05f000:085',
    '062000:002',
    '062000:003',
    '062000:004',
    '062000:005',
    '062000:006',
    '062000:007',
    '062000:008',
    '062000:009',
    '062000:010',
    '062000:013',
    '062000:014',
    '062000:015',
    '062000:016',
    '063000:019',
    '063000:021',
    '063000:022',
    '063000:023',
    '063000:024',
    '063000:025',
    '063000:026',
    '080000:000',
    '080000:001',
    '080000:002',
    '080000:003',
    '081000:029',
    '081000:030',
    '081000:031',
    '082000:005',
}
EDITABLE_IDS |= R09_EDITABLE_IDS


def export_disk(data):
    if digest(data) != SYSTEM_HASH:
        raise ValueError('Unsupported System disk version (SHA-256 mismatch)')
    entries, skipped = [], []
    for base in range(0x51000, 0x84000, 4096):
        pointers = relative_table(data[base:base+4096])
        if pointers is None:
            continue
        for index, (a, z) in enumerate(zip(pointers, pointers[1:] + (4096,))):
            ident = f'{base:06x}:{index:03d}'
            raw = data[base+a:base+z]
            try:
                tokens = decode_entry(raw)
            except Unsupported as exc:
                skipped.append({'id': ident, 'reason': str(exc)})
                continue
            entries.append({'id': ident, 'offset': base+a, 'size': len(raw),
                            'sha256': digest(raw), 'editable': ident in EDITABLE_IDS, 'tokens': tokens})
    return {'format': 'retrotext-alshark-v2', 'source_sha256': digest(data),
            'entries': entries, 'skipped': skipped}


def import_disk(data, document, *, paged_entries=(), narration_entries=()):
    expected = export_disk(data)
    if set(paged_entries) - {e['id'] for e in expected['entries'] if e['editable']}:
        raise ValueError('Extra-page entry is not in the reviewed editable scope')
    if set(narration_entries) - {e['id'] for e in expected['entries'] if e['editable']}:
        raise ValueError('Narration entry is not in the reviewed editable scope')
    if narration_entries:
        from profiles.alshark.playtest_narration import validate_source
        validate_source(data)
    if document.keys() != expected.keys():
        raise ValueError('Document schema changed')
    for key in ('format', 'source_sha256', 'skipped'):
        if document[key] != expected[key]:
            raise ValueError(f'Immutable field changed: {key}')
    if len(document['entries']) != len(expected['entries']):
        raise ValueError('Entry list changed')
    result = bytearray(data)
    for source, entry in zip(expected['entries'], document['entries']):
        metadata = {k:v for k,v in entry.items() if k != 'tokens'}
        if metadata != {k:v for k,v in source.items() if k != 'tokens'}:
            raise ValueError('Entry metadata changed')
        if not source['editable'] and entry['tokens'] != source['tokens']:
            raise ValueError(f"{source['id']}: edits disabled until control-flow references are verified")
        a, n = source['offset'], source['size']
        try:
            result[a:a+n] = rebuild_entry(data[a:a+n], entry['tokens'],
                                          allow_pages=entry['id'] in paged_entries,
                                          allow_narration_pages=entry['id'] in R04_EDITABLE_IDS | R05_EDITABLE_IDS | R06_EDITABLE_IDS | R07_EDITABLE_IDS | R08_EDITABLE_IDS | R09_EDITABLE_IDS,
                                          preserve_narration=entry['id'] in narration_entries)
        except ValueError as exc:
            raise ValueError(f"{source['id']}: {exc}") from exc
    return bytes(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['export', 'import'])
    parser.add_argument('original', type=Path, help='Original System Disk image')
    parser.add_argument('document', type=Path)
    parser.add_argument('--output', type=Path, help='New disk image for import')
    args = parser.parse_args()
    try:
        data = args.original.read_bytes()
        if args.action == 'export':
            if args.document.resolve() == args.original.resolve():
                raise ValueError('Document must not overwrite input')
            document = export_disk(data)
            args.document.parent.mkdir(parents=True, exist_ok=True)
            args.document.write_text(json.dumps(document, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            print(f"Exported {len(document['entries'])} entries; skipped {len(document['skipped'])}")
        else:
            if args.output is None:
                raise ValueError('--output is required for import')
            if args.output.resolve() in (args.original.resolve(), args.document.resolve()):
                raise ValueError('Output must be separate from inputs')
            result = import_disk(data, json.loads(args.document.read_text(encoding='utf-8')))
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(result)
            print(f'Wrote {len(result)} bytes; identical to original: {result == data}')
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
