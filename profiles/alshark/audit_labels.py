#!/usr/bin/env python3
"""Read-only audit of effective labels in a manifest-verified Alshark build."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import unicodedata

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from profiles.alshark.localization import load_images, catalog, ROOT
from profiles.alshark.menu_patch import encode_ui
from profiles.alshark.menu_strings import POOL_SIZE
from profiles.alshark.script import decode_entry


def display(raw):
    return unicodedata.normalize('NFKC', raw.split(b'\0', 1)[0].decode('cp932')).replace('@', '\n').strip()


def read_menu(data, record_offset):
    record = data[record_offset:record_offset+6]
    address = int.from_bytes(record[4:6], 'little')+0x2000
    if len(record) != 6 or not 0x2000 <= address < 0x6000:
        raise ValueError('Invalid resident menu pointer')
    end = data.index(0, address, 0x6000)+1
    return dict(record_offset=record_offset, address=address, columns=record[0],
                rows=record[1], text=display(data[address:end]), used_bytes=end-address)


def classify(ident):
    if ident.endswith(('0042d5', '001e2f', '0048b6', '001d72', '001d7c')):
        return 'clarify_meaning'
    if ident.endswith('010b74') or ident in ('name:1', 'name:13'):
        return 'investigate_terminology'
    if ident in ('fixed:System:001edf', 'fixed:System:001f28'):
        return 'retain_familiar_abbreviations_review_sentence_and_fields'
    if ident.endswith(('0048af', '00471b', '004b1b', '001e98', '0046ec', '004aec', '001e2b')):
        return 'clear_compact_form'
    if ident.startswith('name:') and ident not in ('name:3', 'name:7', 'name:15', 'name:81'):
        return 'working_name_not_an_abbreviation'
    return 'restore_detail_or_review_layout'


def audit(originals, built, manifest, editorial):
    for disk in ('Opening', 'System'):
        name = f'Alshark ({disk} Disk).hdm'
        proof = next(r for r in manifest['disks'] if r['name'] == name)
        if hashlib.sha256(built[disk]).hexdigest() != proof['patched_sha256']:
            raise ValueError(f'{disk}: build differs from its patch manifest')
        if hashlib.sha256(originals[disk]).hexdigest() != proof['source_sha256']:
            raise ValueError(f'{disk}: manifest source does not match original')
    source_records = {r['id']: r for r in catalog(originals)['records']}
    refs = {}
    for offset in range(0x3fd9, 0x414d, 6):
        original = read_menu(originals['Opening'], offset)
        refs.setdefault(original['address'], []).append(read_menu(built['Opening'], offset))
    items = []
    for review in editorial['records']:
        ident = review['id']
        if ident.startswith('script:'):
            continue
        r = source_records[ident]; source = r['source']; disk = source['disk']
        menu_refs = refs.get(source['offset'], []) if disk == 'Opening' else []
        # Startup records are individual fixed 14-byte labels, not the entire
        # two-row table string at the same address.
        start_label = source['offset'] in (0x470c, 0x471b, 0x4b0c, 0x4b1b) and disk == 'Opening'
        if start_label:
            menu_refs = []
        if ident.startswith('name:'):
            po = source['pointer_offset']
            address = int.from_bytes(built[disk][po:po+2], 'little')+0x10000
            end = built[disk].index(0, address)+1
            current = display(built[disk][address:end])
            if ident == 'name:81' and current.startswith('>'):
                current = current[1:].lstrip()  # Location renderer control, not a glyph.
        elif menu_refs:
            current = menu_refs[0]['text']
        elif r['kind'] == 'fixed_runtime_script':
            tokens = decode_entry(built[disk][source['offset']:source['offset']+source['size']])
            current = ''.join(unicodedata.normalize('NFKC', t['source']) if t['kind']=='text'
                              else '{'+t['kind']+':'+t['raw']+'}' for t in tokens)
        else:
            current = display(built[disk][source['offset']:source['offset']+source['size']])
        canonical = review['canonicalEnglish']
        # Hypothetical unchanged full-width encoding, NOT a proposed insertion.
        # Wrapping, name substitutions and fixed-runtime fields need their own adapters.
        needed = None
        try:
            if not ident.startswith('fixed:') and '{' not in canonical:
                needed = len(encode_ui(canonical.upper())) + (0 if start_label else 1)
        except ValueError:
            pass
        items.append(dict(id=ident, current=current, canonical=canonical,
            disposition=classify(ident), source_allocation_bytes=source['size'],
            canonical_fullwidth_bytes=needed, canonical_longest_line=max(map(len,canonical.split('\n'))),
            menu_records=menu_refs, storage='relocated_menu_pool' if menu_refs and menu_refs[0]['address']!=source['offset'] else ('repacked_name_pool' if ident.startswith('name:') else 'original_span'),
            findings=review['findings']))
    proposals=[]
    byid={i['id']:i for i in items}
    for row in manifest.get('menu_strings',[]):
        ident=f"ui:Opening:{row['original_pointer']+0x2000:06x}"
        i=byid[ident]
        proposals.append(dict(id=ident,current_bytes=row['size'],
            canonical_bytes=i['canonical_fullwidth_bytes'],
            current_columns=i['menu_records'][0]['columns'],
            canonical_columns=i['canonical_longest_line']))
    return dict(status='Audit only: no disks or translations changed',
        build_hashes={k:hashlib.sha256(v).hexdigest() for k,v in built.items()},
        scope={'ui_name_and_result_units':len(items),'dialogue_entries_reviewed_separately':32},
        pool={'capacity':POOL_SIZE,'current_used':sum(r['size'] for r in manifest.get('menu_strings',[])),
              'canonical_projection':sum(r['canonical_bytes'] for r in proposals),'menus':proposals,
              'note':'Storage arithmetic only. Wider geometry, highlights, positioning, pointer guards and runtime tests remain required.'},
        items=items)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('original',type=Path); p.add_argument('build',type=Path); p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    if any(a.output.resolve()==d.resolve() or d.resolve() in a.output.resolve().parents for d in (a.original,a.build)):
        p.error('Audit output must be separate from original and build directories')
    originals=load_images(a.original)
    built={d:(a.build/f'Alshark ({d} Disk).hdm').read_bytes() for d in originals}
    result=audit(originals,built,json.loads((a.build/'patch-manifest.json').read_text()),
                 json.loads((ROOT/'editorial-review.json').read_text()))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'scope':result['scope'],'pool':result['pool']},indent=2))


if __name__=='__main__':
    main()
