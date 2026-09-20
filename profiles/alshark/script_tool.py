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
                            'sha256': digest(raw), 'editable': ident in ('051000:000', '051000:001'), 'tokens': tokens})
    return {'format': 'retrotext-alshark-v2', 'source_sha256': digest(data),
            'entries': entries, 'skipped': skipped}


def import_disk(data, document):
    expected = export_disk(data)
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
            result[a:a+n] = rebuild_entry(data[a:a+n], entry['tokens'])
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
