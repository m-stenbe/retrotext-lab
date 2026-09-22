"""Alshark catalog adapter. Existing importer remains the authority on bytes."""
import copy
import json
from pathlib import Path

from retrotext.localization import (FORMAT, make_record, validate_editorial, fingerprint,
                                   index_unique, review_scene)
from profiles.alshark.script_tool import export_disk, import_disk
from profiles.alshark.script import decode_entry, digest
from profiles.alshark.layout import validate_dialogue
from profiles.alshark.menu_patch import patch_menus
from profiles.alshark.menu_strings import MENUS

ROOT = Path(__file__).resolve().parent
BIBLE = ROOT / 'localization-bible.json'
RENDERED_NAMES = {0: 'SION', 1: 'SION', 2: 'SHOKO', 3: 'SHOKO', 4: 'KARU',
                  6: 'JOE', 7: 'JOE', 12: 'LUCIA', 13: 'LUCIA',
                  14: 'MAMON', 15: 'MAMON', 16: 'JIDO', 81: 'COSMA'}


def load_images(directory):
    hashes = dict(line.split('  ', 1)[::-1] for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines())
    images = {}
    for disk in ('Opening', 'System'):
        name = f'Alshark ({disk} Disk).hdm'
        data = (Path(directory)/name).read_bytes()
        if digest(data) != hashes[name]:
            raise ValueError(f'{disk}: source SHA-256 mismatch')
        images[disk] = data
    return images


def catalog(images):
    exported = export_disk(images['System'])
    legacy = {}
    for filename in ('town-draft.json', 'pickup-draft.json', 'area-draft.json'):
        for key, value in json.loads((ROOT/filename).read_text()).items():
            legacy.setdefault(key, {}).update(value)
    legacy.setdefault('051000:001', {})['t006'] = ',\nGO PLAY, BUT\nSTAY AWAY FROM\nTHE METEOR!'
    legacy['051000:034']['t001'] = 'KNIFE'
    legacy['051000:035']['t001'] = 'MEDS'
    legacy.setdefault('051000:005', {})['t001'] = 'ELDER'
    legacy.setdefault('061000:021', {})['t004'] = "NOT MINE.\nCAN'T TAKE IT"
    records = [make_record('script:'+e['id'], 'script', dict(disk='System', entry=e), legacy.get(e['id']))
               for e in exported['entries']]
    # All resident menu-table strings, including currently untranslated menus.
    opening = images['Opening']
    ui = patch_menus(bytearray(opening), bytearray(images['System']), reviewed=True)
    drafts = {(r['disk'], r['offset']): r['translation'] for r in ui}
    for offset, expected, text in MENUS:
        drafts['Opening', int.from_bytes(bytes.fromhex(expected)[4:], 'little')+0x2000] = text
    spans = {}
    for offset in range(0x3fd9, 0x414d, 6):
        address = int.from_bytes(opening[offset+4:offset+6], 'little')+0x2000
        end = opening.index(0, address)+1
        spans['Opening', address] = (end-address, 'menu')
    for r in ui:
        spans.setdefault((r['disk'], r['offset']), (r['size'], 'ui'))
    # Both copies of the start menu are patched by the existing demo builder.
    for offset, text in ((0x470c, 'START'), (0x471b, 'LOAD'),
                         (0x4b0c, 'START'), (0x4b1b, 'LOAD')):
        # These are individually patched 14-byte labels, even where a table
        # pointer also addresses the combined two-row menu starting here.
        spans['Opening', offset] = (14, 'menu')
        drafts['Opening', offset] = text
    for (disk, offset), (size, kind) in sorted(spans.items()):
        raw = images[disk][offset:offset+size]
        source = dict(disk=disk, offset=offset, size=size, raw=raw.hex(),
                      text=raw.rstrip(b'\0').decode('cp932'), sha256=digest(raw))
        records.append(make_record(f'ui:{disk}:{offset:06x}', kind, source, drafts.get((disk, offset))))
    # Preserve distinct short/full-name sources even when legacy drafts collapsed them.
    for ident, translated in RENDERED_NAMES.items():
        pointer_offset = 0x10400+ident*2
        pointer = images['System'][pointer_offset:pointer_offset+2]
        offset = int.from_bytes(pointer, 'little')+0x10000
        end = images['System'].index(0, offset)+1
        raw = images['System'][offset:end]
        records.append(make_record(f'name:{ident}', 'name', dict(disk='System', offset=offset,
            size=len(raw), raw=raw.hex(), text=raw[:-1].decode('cp932'), sha256=digest(raw),
            pointer_offset=pointer_offset, pointer_raw=pointer.hex()), translated))
    for start, end in ((0x1edf, 0x1f28), (0x1f28, 0x1fd8)):
        raw = images['System'][start:end]
        records.append(make_record(f'fixed:System:{start:06x}', 'fixed_runtime_script',
            dict(disk='System', offset=start, size=len(raw), raw=raw.hex(),
                 sha256=digest(raw), tokens=decode_entry(raw))))
    return dict(format=FORMAT, profile='alshark', sourceHashes={k: digest(v) for k, v in images.items()},
                scenes=[], records=records,
                coverageNotes=[
                    'All entries supported by the existing bank exporter; all resident menu-table strings; both start-menu copies; reviewed UI; selected shared names; two fixed combat scripts.',
                    'Cinematic extraction, remaining item/ability/name tables and other undiscovered text remain research tasks.',
                    'Legacy adaptations are not canonical translations. Some hardcoded legacy scenes/fixed combat drafts have not been migrated.',
                    'Only supported script records can be applied through this adapter; other kinds can be localized/reviewed now but require a verified fitting adapter.'
                ])


def apply_editorial_review(document, pack, bible):
    """Hydrate a public English-only review into a local source-preserving catalog.

    This records editorial review, never technical fit or a runtime approval.
    Return a copy so a failed late source guard cannot partially modify input.
    """
    if pack['format'] != 'retrotext-editorial-review-v1':
        raise ValueError('Unsupported editorial review pack')
    if pack['sourceHashes'] != document['sourceHashes']:
        raise ValueError('Editorial pack source hashes do not match')
    result = copy.deepcopy(document)
    records = index_unique(result['records'], 'record')
    edits = index_unique(pack['records'], 'editorial record')
    scenes = index_unique(pack['scenes'], 'editorial scene')
    existing_scenes = index_unique(result['scenes'], 'scene')
    if existing_scenes.keys() & scenes.keys():
        raise ValueError('Review scenes already exist; use a fresh catalog to hydrate a revised pack')
    members = [i for scene in scenes.values() for i in scene['records']]
    if len(members) != len(set(members)) or set(members) != edits.keys():
        raise ValueError('Every editorial record must belong to exactly one review scene')
    for ident, edit in edits.items():
        record = records[ident]
        if fingerprint(record['source']) != edit['sourceFingerprint']:
            raise ValueError(f'{ident}: editorial source fingerprint mismatch')
        if record['canonicalEnglish'] is not None or record['scene'] is not None:
            raise ValueError(f'{ident}: existing editorial work would be overwritten')
        record['canonicalEnglish'] = edit['canonicalEnglish']
        record['context'] = copy.deepcopy(edit['context'])
        record['target']['status'] = 'draft'
        record['target']['notes'].extend(edit['findings'])
        record['target']['notes'].append('Editorial review only; existing ROM text is unchanged.')
    result['scenes'].extend(copy.deepcopy(pack['scenes']))
    for scene in pack['scenes']:
        for ident in scene['records']:
            records[ident]['scene'] = scene['id']
        review_scene(result, scene['id'], bible, pack['reviewer'], scene['reviewNote'])
    for ident, edit in edits.items():
        if edit['adaptationAssessment']['status'] == 'DOES_NOT_FIT':
            record = records[ident]
            record['target'].update(status='DOES_NOT_FIT', basedOn=record['review']['basis'],
                                    reason=edit['adaptationAssessment']['reason'])
    validate_editorial(result, bible)
    return result


def validate_sources(images, document):
    expected = catalog(images)
    for key in ('format', 'profile', 'sourceHashes', 'coverageNotes'):
        if document[key] != expected[key]:
            raise ValueError(f'Immutable catalog field changed: {key}')
    a, b = document['records'], expected['records']
    if len(a) != len(b):
        raise ValueError('Source catalog changed; records may not be removed')
    for actual, original in zip(a, b):
        if any(actual[k] != original[k] for k in ('id', 'kind', 'source')):
            raise ValueError(f"Immutable source changed: {original['id']}")
        if actual['target']['status'] == 'legacy_provisional':
            if actual['target']['inGameEnglish'] != original['target']['inGameEnglish']:
                raise ValueError('Changed legacy text must follow the canonical/review/adaptation workflow')


def compile_adaptations(images, document, bible):
    """Return validated original-based bytes and selected allocations; no writes."""
    validate_sources(images, document)
    validate_editorial(document, bible)
    exported = export_disk(images['System'])
    entries = {e['id']: e for e in exported['entries']}
    changed = []
    for record in document['records']:
        target = record['target']
        if target['status'] == 'DOES_NOT_FIT':
            raise ValueError(f"{record['id']}: DOES_NOT_FIT: {target['reason']}")
        if target['status'] != 'adapted':
            if record['canonicalEnglish'] is not None:
                raise ValueError(f"{record['id']}: canonical work has no approved adaptation; cannot silently reuse the legacy draft")
            continue
        if record['kind'] != 'script':
            raise ValueError(f"{record['id']}: fitting adapter not yet verified for {record['kind']}")
        entry = entries[record['source']['entry']['id']]
        if not entry['editable']:
            raise ValueError(f"{record['id']}: control-flow review required before reinsertion")
        edits = target['inGameEnglish']
        text_ids = {t['id'] for t in entry['tokens'] if t['kind'] == 'text'}
        if not isinstance(edits, dict) or set(edits) != text_ids:
            raise ValueError(f"{record['id']}: adaptation must cover exactly the text tokens")
        # Shared-script calls need composed layout checking, not an isolated entry.
        if any(t['kind'] == 'command' and t['raw'].startswith('2350') for t in entry['tokens']):
            raise ValueError(f"{record['id']}: shared-script layout adapter required")
        for token in entry['tokens']:
            if token['kind'] == 'text':
                token['translation'] = edits[token['id']]
        validate_dialogue(entry['tokens'], RENDERED_NAMES)
        changed.append(dict(id=record['id'], offset=entry['offset'], size=entry['size'],
                            canonicalReview=record['review']['basis'],
                            adaptationHash=digest(json.dumps(edits, sort_keys=True).encode()),
                            runtime_verified=False))
    # Preserves every original command, branch, pointer, name ID and opaque tail.
    rebuilt = import_disk(images['System'], exported)
    return rebuilt, changed
