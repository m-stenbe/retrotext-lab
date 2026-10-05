"""Alshark catalog adapter. Existing importer remains the authority on bytes."""
import copy
import json
from pathlib import Path

from retrotext.localization import (FORMAT, make_record, validate_editorial, fingerprint,
                                   index_unique, review_scene)
from profiles.alshark.script_tool import export_disk, import_disk
from profiles.alshark.script import decode_entry, digest, translation_pages
from profiles.alshark.layout import validate_dialogue
from profiles.alshark.menu_patch import patch_menus
from profiles.alshark.menu_strings import MENUS
from profiles.alshark.names import SHARED as LEGACY_SHARED_NAMES
from profiles.alshark.r04_names import RENDERED_NAMES as R04_RENDERED_NAMES

ROOT = Path(__file__).resolve().parent
BIBLE = ROOT / 'localization-bible.json'
RENDERED_NAMES = {0: 'SION', 1: 'SION', 2: 'SHOKO', 3: 'SHOKO', 4: 'KARU',
                  6: 'JOE', 7: 'JOE', 12: 'LUCIA', 13: 'LUCIA',
                  14: 'MAMON', 15: 'MAMON', 16: 'JIDO', 81: 'COSMA'}
RENDERED_NAMES.update(R04_RENDERED_NAMES)
from profiles.alshark.r08_names import RENDERED_NAMES as R08_RENDERED_NAMES
RENDERED_NAMES.update(R08_RENDERED_NAMES)


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
    for ident, translated in LEGACY_SHARED_NAMES.items():
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
    from profiles.alshark.cinematic import export_records as cinematic_records
    from profiles.alshark.interface import export_records as interface_records
    from profiles.alshark.names import export_records as name_records
    records.extend(cinematic_records(images))
    records.extend(interface_records(images))
    records.extend(name_records(images))
    from profiles.alshark.r02_names import export_records as r02_name_records
    records.extend(r02_name_records(images))
    from profiles.alshark.r03_names import export_records as r03_name_records
    records.extend(r03_name_records(images))
    from profiles.alshark.r03_equipment import export_records as r03_equipment_records
    records.extend(r03_equipment_records(images))
    from profiles.alshark.r03_ui import export_records as r03_ui_records
    records.extend(r03_ui_records(images))
    from profiles.alshark.r04_names import export_records as r04_name_records
    records.extend(r04_name_records(images))
    from profiles.alshark.r05_names import export_records as r05_name_records
    records.extend(r05_name_records(images))
    from profiles.alshark.r06_names import export_records as r06_name_records
    from profiles.alshark.r06_ui import export_records as r06_ui_records
    records.extend(r06_name_records(images))
    from profiles.alshark.r07_names import export_records as r07_name_records
    records.extend(r07_name_records(images))
    from profiles.alshark.r08_names import export_records as r08_name_records
    records.extend(r08_name_records(images))
    from profiles.alshark.r09_names import export_records as r09_name_records
    records.extend(r09_name_records(images))
    records.extend(r06_ui_records(images))
    return dict(format=FORMAT, profile='alshark', sourceHashes={k: digest(v) for k, v in images.items()},
                scenes=[], records=records,
                coverageNotes=[
                    'All entries supported by the existing bank exporter; all resident menu-table strings; both start-menu copies; reviewed UI; selected shared names; two fixed combat scripts.',
                    'Meteor cinematic and R01 UI/names are catalogued; other cinematics, remaining tables and undiscovered text remain research tasks.',
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


def apply_adaptation_pack(document, pack, bible):
    """Attach separately authored fitting decisions to their exact review basis."""
    if pack['format'] != 'retrotext-adaptations-v1':
        raise ValueError('Unsupported adaptation pack')
    validate_editorial(document, bible)
    result = copy.deepcopy(document)
    records = index_unique(result['records'], 'record')
    edits = index_unique(pack['records'], 'adaptation')
    scenes = index_unique(result['scenes'], 'scene')
    selected = pack['scenes']
    if not selected or len(set(selected)) != len(selected) or set(selected) - scenes.keys():
        raise ValueError('Invalid adaptation scene selection')
    if {i for s in selected for i in scenes[s]['records']} != edits.keys():
        raise ValueError('Adaptations must cover complete selected scenes')
    for ident, edit in edits.items():
        record = records[ident]
        if record['review'] is None or edit['basedOn'] != record['review']['basis']:
            raise ValueError(f'{ident}: adaptation review basis mismatch')
        record['target'].update(status='adapted', inGameEnglish=copy.deepcopy(edit['inGameEnglish']),
                                basedOn=edit['basedOn'], reason=None, playtest=[])
        record['target']['notes'].extend(edit['notes'])
    validate_editorial(result, bible)
    return result


# Only these meteor-event calls have had their bank/index and connected layout
# reviewed. All other shared calls continue to fail closed.
METEOR_CALLS = {
    ('051000:030', '2350020200'): '053000:000',
    ('051000:033', '235002020d'): '053000:013',
}
REVIEWED_CALLS = {
    **METEOR_CALLS,
    ('082000:008', '2350022e26'): '07f000:038',
    ('082000:009', '2350022e27'): '07f000:039',
    ('082000:015', '2350022e29'): '07f000:041',
    ('082000:016', '2350022e2a'): '07f000:042',
    **{(f'051000:{i:03}', '2350020029'): '051000:041' for i in (34, 35, 36, 37)},
    ('051000:034', '2350021015'): '061000:021',
    ('051000:036', '2350021013'): '061000:019',
    ('051000:038', '2350021014'): '061000:020',
    ('051000:040', '2350021016'): '061000:022',
}


from profiles.alshark.r02_flow import CALLS as R02_CALLS
from profiles.alshark.r04_flow import CALLS as R04_CALLS
REVIEWED_CALLS.update(R04_CALLS)
from profiles.alshark.r05_flow import CALLS as R05_CALLS
REVIEWED_CALLS.update(R05_CALLS)
from profiles.alshark.r06_flow import CALLS as R06_CALLS
REVIEWED_CALLS.update(R06_CALLS)
from profiles.alshark.r07_flow import CALLS as R07_CALLS
REVIEWED_CALLS.update(R07_CALLS)
from profiles.alshark.r08_flow import CALLS as R08_CALLS
REVIEWED_CALLS.update(R08_CALLS)
from profiles.alshark.r09_flow import CALLS as R09_CALLS
REVIEWED_CALLS.update(R09_CALLS)
REVIEWED_CALLS.update({(link.source, link.command): link.target for link in R02_CALLS})
# R03 global-party dispatchers; each exact call is guarded by r03_flow.
REVIEWED_CALLS.update({
    ('082000:025', '2350022c22'): '07d000:034',
    ('082000:026', '2350022c21'): '07d000:033',
    ('082000:027', '2350022c20'): '07d000:032',
})

def composed_dialogue(ident, entries, selected, stack=()):
    """Inline reviewed calls for measurement, never for byte reinsertion.

    A callee's terminator returns to its caller; cursor/header state carries
    through the call. Requiring selected callees prevents measuring English
    while shipping an untranslated dependency.
    """
    if ident in stack:
        raise ValueError('Recursive shared-script layout')
    result = []
    from profiles.alshark.r04_pages import advance_colour, page_break_token
    from profiles.alshark.script_tool import R04_EDITABLE_IDS, R05_EDITABLE_IDS, R06_EDITABLE_IDS, R07_EDITABLE_IDS, R08_EDITABLE_IDS, R09_EDITABLE_IDS
    colour = 'default'
    for token in entries[ident]['tokens']:
        colour = advance_colour(colour, token)
        if token['kind'] == 'command' and token['raw'].startswith('2350'):
            target = REVIEWED_CALLS.get((ident, token['raw']))
            if target is None:
                raise ValueError(f'{ident}: shared-script layout adapter required')
            if target not in selected:
                raise ValueError(f'{ident}: selected adaptation required for shared callee {target}')
            # #P enters f2cd with DI unchanged: the current column becomes
            # the callee newline origin until a clear establishes the box origin.
            result.append(dict(kind='call_origin'))
            result.extend(composed_dialogue(target, entries, selected, (*stack, ident)))
        elif token['kind'] == 'text' and isinstance(token['translation'], list):
            for index, page in enumerate(translation_pages(token['translation'])):
                if index:
                    result.append(page_break_token(colour) if ident in R04_EDITABLE_IDS | R05_EDITABLE_IDS | R06_EDITABLE_IDS | R07_EDITABLE_IDS | R08_EDITABLE_IDS | R09_EDITABLE_IDS
                                  else dict(kind='page_break'))
                result.append(dict(kind='text', translation=page))
        elif token['kind'] not in ('end', 'opaque_tail'):
            result.append(token)
    return result


PARTY_BRANCHES = (
    ('082000:000', '2342020e10', '082000:016', '07f000:042'),
    ('082000:000', '2342021009', '082000:009', '07f000:039'),
    ('082000:007', '2342020e0f', '082000:015', '07f000:041'),
    ('082000:007', '234202100e', '082000:014', '082000:014'),
    ('082000:007', '2342020208', '082000:008', '07f000:038'),
)


def composed_branch(root, command, target, entries, selected):
    """Measure a reviewed taken branch with the caller's existing display state."""
    tokens = entries[root]['tokens']
    matches = [i for i, t in enumerate(tokens)
               if t['kind'] == 'command' and t['raw'] == command]
    if len(matches) != 1:
        raise ValueError('Reviewed branch command missing or ambiguous')
    prefix = dict(entries)
    prefix[root] = dict(tokens=tokens[:matches[0]])
    return (composed_dialogue(root, prefix, selected)
            + composed_dialogue(target, entries, selected))


def compile_adaptations(images, document, bible, *, scenes=None, full_images=False):
    """Return validated original-based bytes and selected allocations; no writes."""
    validate_sources(images, document)
    validate_editorial(document, bible)
    if scenes is not None:
        known = index_unique(document['scenes'], 'scene')
        if not scenes or len(set(scenes)) != len(scenes) or set(scenes) - known.keys():
            raise ValueError('Unknown, empty or duplicate localization scene selection')
    exported = export_disk(images['System'])
    entries = {e['id']: e for e in exported['entries']}
    from profiles.alshark.r02_flow import validate_source as validate_r02_source
    changed = []
    paged_entries = set()
    external_records = []
    for record in document['records']:
        if scenes is not None and record['scene'] not in scenes:
            continue
        target = record['target']
        if target['status'] == 'DOES_NOT_FIT':
            raise ValueError(f"{record['id']}: DOES_NOT_FIT: {target['reason']}")
        if target['status'] != 'adapted':
            if scenes is not None or record['canonicalEnglish'] is not None:
                raise ValueError(f"{record['id']}: canonical work has no approved adaptation; cannot silently reuse the legacy draft")
            continue
        if record['kind'] in ('cinematic', 'menu', 'ui', 'name', 'fixed_runtime_script'):
            external_records.append(record)
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
        for token in entry['tokens']:
            if token['kind'] == 'text':
                token['translation'] = edits[token['id']]
                if isinstance(token['translation'], list):
                    translation_pages(token['translation'])
                    paged_entries.add(entry['id'])
        changed.append(dict(id=record['id'], disk='System', offset=entry['offset'], size=entry['size'],
                            canonicalReview=record['review']['basis'],
                            adaptationHash=digest(json.dumps(edits, sort_keys=True).encode()),
                            extra_page_breaks=sum(len(v)-1 for v in edits.values() if isinstance(v, list)),
                            runtime_verified=False))
    validate_r02_source(entries)
    from profiles.alshark.r03_flow import validate_source as validate_r03_source
    validate_r03_source(entries)
    from profiles.alshark.r04_flow import validate_source as validate_r04_source
    validate_r04_source(entries)
    from profiles.alshark.r05_flow import validate_source as validate_r05_source
    validate_r05_source(entries)
    from profiles.alshark.r06_flow import validate_source as validate_r06_source
    validate_r06_source(entries)
    from profiles.alshark.r07_flow import validate_source as validate_r07_source
    validate_r07_source(entries)
    from profiles.alshark.r08_flow import validate_source as validate_r08_source
    validate_r08_source(entries)
    from profiles.alshark.r09_flow import validate_source as validate_r09_source
    validate_r09_source(entries)
    from profiles.alshark.r04_pages import validate_header_calls, validate_renderer_source
    validate_header_calls(entries)
    validate_renderer_source(images['System'])
    selected = {r['id'].removeprefix('script:') for r in changed}
    for root, command, target, dependency in PARTY_BRANCHES:
        if root in selected:
            if dependency not in selected:
                raise ValueError(f'{root}: selected party branch required: {dependency}')
            validate_dialogue(composed_branch(root, command, target, entries, selected), RENDERED_NAMES)
    # Flag 4 bypasses the first conversation and dispatches to the repeat entry.
    if '051000:030' in selected:
        # The repeat dispatcher is control-only and stays read-only. Measure its
        # actual selected callee as well as the first-time continuation.
        validate_dialogue(composed_dialogue('051000:033', entries, selected), RENDERED_NAMES)
    for ident in selected:
        try:
            validate_dialogue(composed_dialogue(ident, entries, selected), RENDERED_NAMES)
        except ValueError as exc:
            raise ValueError(f'{ident}: {exc}') from exc
    # Measure both sides of reviewed R02/R03 branches when their English packet
    # is selected. The section inventory separately requires the full closure.
    from profiles.alshark.r02_flow import control_edges, route_closure, apply_reviewed_menu_widths
    from profiles.alshark.r03_flow import control_edges as r03_edges, route_closure as r03_closure
    from profiles.alshark.r04_flow import control_edges as r04_edges, route_closure as r04_closure
    from profiles.alshark.r05_flow import control_edges as r05_edges, route_closure as r05_closure
    from profiles.alshark.r06_flow import control_edges as r06_edges, route_closure as r06_closure
    from profiles.alshark.r07_flow import control_edges as r07_edges, route_closure as r07_closure
    from profiles.alshark.r08_flow import control_edges as r08_edges, route_closure as r08_closure
    from profiles.alshark.r09_flow import control_edges as r09_edges, route_closure as r09_closure
    for control_edges, route_closure in ((control_edges, route_closure), (r03_edges, r03_closure),
                                       (r04_edges, r04_closure), (r05_edges, r05_closure),
                                       (r06_edges, r06_closure), (r07_edges, r07_closure), (r08_edges, r08_closure), (r09_edges, r09_closure)):
        route = route_closure(entries)
        active = selected | {i for i in route if not any(t['kind'] == 'text' for t in entries[i]['tokens'])}
        for root in sorted(route & active):
            root_dependencies = {i for i in route_closure(entries, (root,))
                                 if any(t['kind'] == 'text' for t in entries[i]['tokens'])}
            if not root_dependencies <= selected:
                continue
            for kind, target, command in control_edges(root, entries):
                if kind in ('P', 'N') or target not in active:
                    continue
                dependencies = {i for i in route_closure(entries, (target,))
                                if any(t['kind'] == 'text' for t in entries[i]['tokens'])}
                if not dependencies <= selected:
                    continue
                try:
                    validate_dialogue(composed_branch(root, command, target, entries, selected), RENDERED_NAMES)
                except ValueError as exc:
                    raise ValueError(f'{root} -> {target}: {exc}') from exc
    # Rebuild with all original commands intact first. The explicit geometry
    # overlay below changes only two source-guarded menu width parameters.
    from profiles.alshark.r02_allocations import relocate_girl_header, ENTRY_008
    normal_export = exported
    if ENTRY_008 in selected:
        normal_export = copy.deepcopy(exported)
        original_left = next(e for e in export_disk(images['System'])['entries'] if e['id'] == ENTRY_008)
        next(e for e in normal_export['entries'] if e['id'] == ENTRY_008)['tokens'] = original_left['tokens']
    rebuilt = import_disk(images['System'], normal_export, paged_entries=paged_entries,
                          narration_entries=selected)
    rebuilt, allocations = relocate_girl_header(images['System'], rebuilt, entries, selected)
    for allocation in allocations:
        if allocation['id'].startswith('r02:pointer:'):
            record = next(r for r in changed if r['id'] == 'script:' + ENTRY_008)
            record.setdefault('patches', [dict(disk='System', offset=record['offset'], size=record['size'])])
            record['patches'].append(dict(disk='System', offset=allocation['offset'], size=allocation['size']))
            record.setdefault('allocationChanges', []).append(allocation)
        else:
            record = next(r for r in changed if r['id'] == 'script:' + allocation['id'])
            record.update(offset=allocation['offset'], size=allocation['size'])
            record.setdefault('allocationChanges', []).append(allocation)
    from profiles.alshark.r07_flow import apply_reviewed_menu_widths as validate_r07_menus
    rebuilt, _ = validate_r07_menus(images['System'], rebuilt, entries, selected)
    from profiles.alshark.r08_flow import apply_reviewed_menu_widths as validate_r08_menus
    rebuilt, _ = validate_r08_menus(images['System'], rebuilt, entries, selected)
    from profiles.alshark.r09_flow import apply_reviewed_menu_widths as validate_r09_menus
    rebuilt, _ = validate_r09_menus(images['System'], rebuilt, entries, selected)
    rebuilt, geometry = apply_reviewed_menu_widths(images['System'], rebuilt, entries, selected)
    for patch in geometry:
        record = next(r for r in changed if r['id'] == 'script:' + patch['label'])
        record.setdefault('patches', [dict(disk=record['disk'], offset=record['offset'], size=record['size'])])
        record['patches'].append(dict(disk='System', offset=patch['offset'], size=patch['size']))
        record.setdefault('menuGeometry', []).append(patch)
    outputs = dict(images, System=rebuilt)
    cinematic = [r for r in external_records if r['kind'] == 'cinematic']
    from profiles.alshark.names import REQUIRED as NAME_GROUP
    from profiles.alshark.r02_names import REQUIRED as R02_NAME_GROUP
    from profiles.alshark.r03_names import REQUIRED as R03_NAME_GROUP
    from profiles.alshark.r03_equipment import REQUIRED as R03_EQUIPMENT_GROUP
    from profiles.alshark.r04_names import REQUIRED as R04_NAME_GROUP
    from profiles.alshark.r05_names import REQUIRED as R05_NAME_GROUP
    from profiles.alshark.r06_names import REQUIRED as R06_NAME_GROUP
    names = [r for r in external_records if r['id'] in NAME_GROUP]
    r02_names = [r for r in external_records if r['id'] in R02_NAME_GROUP]
    r03_names = [r for r in external_records if r['id'] in R03_NAME_GROUP]
    r03_equipment = [r for r in external_records if r['id'] in R03_EQUIPMENT_GROUP]
    r04_names = [r for r in external_records if r['id'] in R04_NAME_GROUP]
    r05_names = [r for r in external_records if r['id'] in R05_NAME_GROUP]
    r06_names = [r for r in external_records if r['id'] in R06_NAME_GROUP]
    from profiles.alshark.r07_names import REQUIRED as R07_NAME_GROUP
    r07_names = [r for r in external_records if r['id'] in R07_NAME_GROUP]
    from profiles.alshark.r08_names import REQUIRED as R08_NAME_GROUP
    r08_names = [r for r in external_records if r['id'] in R08_NAME_GROUP]
    from profiles.alshark.r09_names import REQUIRED as R09_NAME_GROUP
    r09_names = [r for r in external_records if r['id'] in R09_NAME_GROUP]
    from profiles.alshark.r03_ui import REQUIRED as R03_UI_GROUP
    r03_ui = [r for r in external_records if r['id'] in R03_UI_GROUP]
    from profiles.alshark.r06_ui import REQUIRED as R06_UI_GROUP
    r06_ui = [r for r in external_records if r['id'] in R06_UI_GROUP]
    interface = [r for r in external_records if r['kind'] != 'cinematic'
                 and r['id'] not in NAME_GROUP and r['id'] not in R02_NAME_GROUP
                 and r['id'] not in R03_NAME_GROUP and r['id'] not in R03_UI_GROUP
                 and r['id'] not in R03_EQUIPMENT_GROUP and r['id'] not in R04_NAME_GROUP
                 and r['id'] not in R05_NAME_GROUP and r['id'] not in R06_NAME_GROUP
                 and r['id'] not in R06_UI_GROUP and r['id'] not in R07_NAME_GROUP and r['id'] not in R08_NAME_GROUP and r['id'] not in R09_NAME_GROUP]
    if cinematic:
        from profiles.alshark.cinematic import compile_records
        outputs['Opening'], manifests = compile_records(images, cinematic)
        for r, manifest in zip(cinematic, manifests):
            manifest.update(id=r['id'], canonicalReview=r['review']['basis'],
                            adaptationHash=fingerprint(r['target']['inGameEnglish']), runtime_verified=False)
        changed.extend(manifests)
    if interface:
        from profiles.alshark.interface import compile_records
        compiled, manifests = compile_records(images, interface)
        for manifest in manifests:
            for patch in manifest['patches']:
                disk, a, size = patch['disk'], patch['offset'], patch['size']
                target = bytearray(outputs[disk])
                target[a:a+size] = compiled[disk][a:a+size]
                outputs[disk] = bytes(target)
        changed.extend(manifests)
    from profiles.alshark.r03_ui import compile_records as compile_r03_ui
    from profiles.alshark.r06_ui import compile_records as compile_r06_ui
    for ui_records, compile_ui in ((r03_ui, compile_r03_ui), (r06_ui, compile_r06_ui)):
        if not ui_records:
            continue
        compiled, manifests = compile_ui(images, ui_records)
        by_id = {r['id']:r for r in ui_records}
        for manifest in manifests:
            r = by_id[manifest['id']]
            manifest.update(canonicalReview=r['review']['basis'],
                            adaptationHash=fingerprint(r['target']['inGameEnglish']), runtime_verified=False)
            for patch in manifest['patches']:
                disk, a, size = patch['disk'], patch['offset'], patch['size']
                target = bytearray(outputs[disk])
                target[a:a+size] = compiled[disk][a:a+size]
                outputs[disk] = bytes(target)
        changed.extend(manifests)
    from profiles.alshark.names import compile_names as compile_r01_names
    from profiles.alshark.r02_names import compile_names as compile_r02_names
    from profiles.alshark.r03_names import compile_names as compile_r03_names
    from profiles.alshark.r03_equipment import compile_names as compile_r03_equipment
    from profiles.alshark.r04_names import compile_names as compile_r04_names
    from profiles.alshark.r05_names import compile_names as compile_r05_names
    from profiles.alshark.r06_names import compile_names as compile_r06_names
    from profiles.alshark.r07_names import compile_names as compile_r07_names
    from profiles.alshark.r08_names import compile_names as compile_r08_names
    from profiles.alshark.r09_names import compile_names as compile_r09_names
    for name_records, compile_names in ((names, compile_r01_names), (r02_names, compile_r02_names),
                                         (r03_names, compile_r03_names), (r03_equipment, compile_r03_equipment),
                                         (r04_names, compile_r04_names), (r05_names, compile_r05_names),
                                         (r06_names, compile_r06_names), (r07_names, compile_r07_names), (r08_names, compile_r08_names), (r09_names, compile_r09_names)):
        if not name_records:
            continue
        compiled, group = compile_names(images, {r['id']:r['target']['inGameEnglish'] for r in name_records})
        target = bytearray(outputs['System'])
        for patch in group['patches']:
            a, size = patch['offset'], patch['size']
            target[a:a+size] = compiled[a:a+size]
        outputs['System'] = bytes(target)
        by_id = {r['id']:r for r in name_records}
        for index, manifest in enumerate(group['records']):
            r = by_id[manifest['record']]
            manifest.update(id=r['id'],size=manifest['used'],canonicalReview=r['review']['basis'],
                            adaptationHash=fingerprint(r['target']['inGameEnglish']),
                            patches=[dict(disk='System', **p) for p in group['patches']] if index==0 else [])
        changed.extend(group['records'])
    return outputs if full_images else outputs['System'], changed
