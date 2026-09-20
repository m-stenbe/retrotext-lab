#!/usr/bin/env python3
"""Read-only structural inventory; not a complete script interpreter."""
import argparse
import sys
import csv
import hashlib
import json
from pathlib import Path
import re
import struct

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from retrotext.banks import relative_table, split_candidate

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('original', type=Path)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
if not args.original.is_dir() or not list(args.original.glob('*.hdm')):
    parser.error('Original directory must contain .hdm images')
OUT = args.output
OUT.mkdir(parents=True, exist_ok=True)
HEADER = re.compile(rb'4\$(.)5', re.S)

def preview(raw):
    s = raw.decode('cp932', errors='backslashreplace')
    return ''.join(f'<{ord(c):02X}>' if ord(c) < 32 else c for c in s)

banks, entries, disk_stats, other_candidates = [], [], [], []
for path in sorted(args.original.glob('*.hdm')):
    data = path.read_bytes()
    markers = list(HEADER.finditer(data))
    covered = 0
    for base in range(0, len(data)-4095, 4096):
        raw = data[base:base+4096]
        pointers = relative_table(raw)
        if pointers is None:
            continue
        first = pointers[0]
        split_candidate(raw, pointers)
        if path.name != 'Alshark (System Disk).hdm' or not 0x51000 <= base <= 0x83000:
            other_candidates.append(dict(disk=path.name, base=hex(base), entries=len(pointers),
                                         note='Structure match only; not accepted as script bank'))
            continue
        hits = len(list(HEADER.finditer(raw)))
        covered += hits
        zeros = len(raw) - len(raw.rstrip(b'\0'))
        row = dict(base=f'0x{base:06X}', pointer_entries=len(pointers),
                   unique_offsets=len(set(pointers)), named_speech_markers=hits,
                   trailing_zero_bytes=zeros,
                   trailing_e5_bytes=len(raw)-len(raw.rstrip(b'\xe5')),
                   apparent_tail_after_terminator=max(0, zeros-1))
        banks.append(row)
        reconstructed = bytearray(raw[:first])
        for idx, (a, z) in enumerate(zip(pointers, pointers[1:] + (4096,))):
            part = raw[a:z]
            reconstructed.extend(part)
            entries.append(dict(bank=row['base'], entry=idx, offset=f'0x{base+a:06X}',
                                allocated_bytes=z-a, named_speech_markers=len(list(HEADER.finditer(part))),
                                diagnostic_cp932=preview(part.rstrip(b'\0'))))
        assert bytes(reconstructed) == raw, hex(base)
    disk_stats.append(dict(disk=path.name, sha256=hashlib.sha256(data).hexdigest(),
                           named_speech_markers=len(markers), markers_in_selected_banks=covered,
                           outside_bank_offsets=[hex(m.start()) for m in markers
                             if not any(int(r['base'],16) <= m.start() < int(r['base'],16)+4096
                                        for r in banks)] if path.name == 'Alshark (System Disk).hdm'
                           else [hex(m.start()) for m in markers]))

for name, rows in [('banks.tsv', banks), ('entries.tsv', entries)]:
    with (OUT/name).open('w', newline='') as f:
        if not rows:
            continue
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
summary = dict(method='4KB-aligned monotonic relative-pointer tables, selected System region; raw entry roundtrip verified',
               caveat='Entries contain commands, branches and text. Counts are not dialogue boxes or words. Zero tails are not proven free space.',
               banks=len(banks), pointer_entries=sum(r['pointer_entries'] for r in banks),
               named_speech_markers=sum(r['named_speech_markers'] for r in banks),
               trailing_e5_bytes=sum(r['trailing_e5_bytes'] for r in banks),
               apparent_tail_after_terminator=sum(r['apparent_tail_after_terminator'] for r in banks),
               banks_with_under_64_tail_bytes=sum(r['apparent_tail_after_terminator'] < 64 for r in banks),
               disks=disk_stats, unaccepted_structure_matches=other_candidates)
(OUT/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
print(json.dumps(summary, indent=2))
