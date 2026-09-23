"""Guarded fitting adapter for boot-driver disk prompts and their runtime slots."""
import hashlib
import json
from pathlib import Path
from retrotext.localization import fingerprint, index_unique
from profiles.alshark.menu_patch import encode_ui

PACK = Path(__file__).with_name('disk-prompts.json')
SPECS = {'single': {'offset': 10327,
            'size': 67,
            'sha256': '26e5122180e470f51977d7082bd19a42359828bb21ca0563f9b596d23ddaab3a'},
 'dual': {'offset': 10394,
          'size': 103,
          'sha256': 'c7682d3e9680751dad4ddc9c522a6f3d921ee1bab3b326c4bac590708be8e53e'},
 'name-opening': {'offset': 10249,
                  'size': 13,
                  'sha256': '91c3b4c9aa7f7633545033a65b5ecd315ab987364aaa3530b801dccd20df126c'},
 'name-system': {'offset': 10262,
                 'size': 13,
                 'sha256': '6f188f6279bfd0d51fa6fcb139fc9ffe70f3e96823ac335d6809a4ca211c899e'},
 'name-data': {'offset': 10275,
               'size': 13,
               'sha256': '49b163819ee77fd3628f6acf0844462b08b84f37667f72fbb1be4190770a6c8b'},
 'name-visual': {'offset': 10288,
                 'size': 13,
                 'sha256': '0d48922b1cfcc4f279673547ec38c61137f33740992ff5da9dac243ba1643127'},
 'name-ending': {'offset': 10301,
                 'size': 13,
                 'sha256': '264bc4b51073140ed41ff622d0e889a2db9fc81675881ee90aefc72a4d11e7a2'},
 'name-user': {'offset': 10314,
               'size': 13,
               'sha256': '3fa3fd08f0bd99f4cf56f693760ca7356b94afc4a9beaf67da6db30ed6ea18a2'}}
# Only absolute destinations of existing one-byte digit writes change.
WRITES = ((0x2529, '883e6f08', '883e7708'),
          (0x2558, '883eb108', '883ebb08'),
          (0x255c, '882ed408', '882ede08'))


def patch_disk_prompts(opening, pack=None):
    pack = json.loads(PACK.read_text()) if pack is None else pack
    if pack['format'] != 'alshark-disk-prompts-v1':
        raise ValueError('Unsupported disk prompt pack')
    records = index_unique(pack['records'], 'disk prompt')
    if records.keys() != SPECS.keys():
        raise ValueError('Disk prompt record set changed')
    pending, manifest = [], []
    for ident, spec in SPECS.items():
        r = records[ident]
        a, size = spec['offset'], spec['size']
        if r['source'] != spec or hashlib.sha256(opening[a:a+size]).hexdigest() != spec['sha256']:
            raise ValueError('Disk prompt source mismatch')
        basis = fingerprint({k:r[k] for k in ('source','canonicalEnglish','context')})
        if (not isinstance(r['canonicalEnglish'], str) or not r['canonicalEnglish'].strip()
            or not r['review'].get('reviewer') or not r['review'].get('note')
            or r['review']['basis'] != basis or r['target']['basedOn'] != basis
            or r['target']['status'] != 'adapted'):
            raise ValueError('Disk prompt review/adaptation missing or stale')
        text = r['target']['inGameEnglish']
        lines = text.split('\n')
        if ident.startswith('name-'):
            if len(lines)!=1 or len(text)!=6:
                raise ValueError('Disk names must occupy exactly six cells')
        else:
            if len(lines)!=3 or any(len(line) > (17 if ident=='dual' else 15) for line in lines):
                raise ValueError('Disk prompt geometry exceeded')
            # Preserve name destinations and exact low-byte positions for drive writes.
            expected = ('       IN DRIVE 1', '       IN DRIVE 2') if ident=='dual' else ('      ', 'IN DRIVE 1')
            if tuple(lines[:2]) != expected:
                raise ValueError('Disk prompt runtime fields moved')
        encoded = encode_ui(text)+b'\0'
        if len(encoded)>size:
            raise ValueError('Disk prompt allocation exceeded')
        pending.append((a, encoded.ljust(size,b'\0')))
        manifest.append(dict(id=ident,offset=a,size=size,canonicalReview=basis,
                             adaptationHash=fingerprint(text),runtime_verified=False))
    for a, before, after in WRITES:
        if opening[a:a+4] != bytes.fromhex(before):
            raise ValueError('Disk prompt instruction guard mismatch')
        pending.append((a,bytes.fromhex(after)))
    # All source, editorial and instruction guards pass before any mutation.
    for a, data in pending:
        opening[a:a+len(data)] = data
    return dict(records=manifest,drive_write_offsets=[a for a,_,_ in WRITES],runtime_verified=False)
