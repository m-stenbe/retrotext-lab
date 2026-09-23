"""Read-only scene work packets. Profile callbacks retain all fitting authority."""
from copy import deepcopy
from .localization import fingerprint, index_unique, validate_editorial


def prepare_batch(document, bible, plan, check_scene):
    if plan.get('format') != 'retrotext-batch-plan-v1' or not plan.get('id'):
        raise ValueError('Invalid batch plan')
    scenes = index_unique(document['scenes'], 'scene')
    records = index_unique(document['records'], 'record')
    selected = plan['scenes']
    if not selected or len(set(selected)) != len(selected) or set(selected) - scenes.keys():
        raise ValueError('Unknown, empty or duplicate scene selection')
    context_ids = plan.get('contextRecords', [])
    if len(set(context_ids)) != len(context_ids) or set(context_ids) - records.keys():
        raise ValueError('Unknown or duplicate context record')
    # Same global gate as builds: stale work anywhere must not appear build-ready.
    editorial_error = None
    try:
        validate_editorial(document, bible)
    except ValueError as exc:
        editorial_error = str(exc)
    terms = index_unique(bible['terms'], 'term')
    referenced = set()
    packets, ready = [], []
    for ident in selected:
        scene = scenes[ident]
        if not scene['records']:
            raise ValueError(f'{ident}: empty scene')
        members = [records[i] for i in scene['records']]
        if any(r['scene'] != ident for r in members):
            raise ValueError('Inconsistent scene membership')
        referenced.update(scene.get('terminology', []))
        issues = []
        for r in members:
            referenced.update(r['context']['terminology'])
            if not r['canonicalEnglish']:
                issues.append(f"{r['id']}: canonical English needed")
            elif not r['review']:
                issues.append(f"{r['id']}: connected-scene editorial review needed")
            if r['target']['status'] == 'DOES_NOT_FIT':
                issues.append(f"{r['id']}: DOES_NOT_FIT: {r['target']['reason']}")
            elif r['target']['status'] != 'adapted':
                issues.append(f"{r['id']}: adaptation needed")
        if editorial_error:
            issues.append('Global editorial gate: ' + editorial_error)
        changes = []
        if not issues:
            try:
                changes = check_scene([ident])
            except ValueError as exc:
                issues.append('Profile validation: ' + str(exc))
        if not issues:
            ready.append(ident)
        packets.append(dict(scene=scene, records=members, issues=issues,
                            status='blocked' if issues else 'validated_for_build',
                            validatedChanges=changes))
    context = [records[i] for i in context_ids]
    for r in context:
        referenced.update(r['context']['terminology'])
    if referenced - terms.keys():
        raise ValueError('Unknown terminology in batch')
    # Validate ready scenes together too; do not infer compatibility from isolated checks.
    if ready:
        check_scene(ready)
    return deepcopy(dict(format='retrotext-batch-packet-v1', plan=plan,
        documentFingerprint=fingerprint(document), bibleFingerprint=fingerprint(bible),
        sourceHashes=document.get('sourceHashes'), packets=packets,
        contextRecords=context, terminology=[terms[i] for i in sorted(referenced)],
        readyScenes=ready, deferredScenes=[i for i in selected if i not in ready],
        coverageNotes=document.get('coverageNotes', []), globalEditorialError=editorial_error))


def reading_sheet(packet):
    lines = [f"# Batch: {packet['plan']['id']}", '',
        'Generated work packet, not editorial approval or evidence of runtime success.',
        'Scene order is a work order; branch alternatives are not consecutive dialogue.', '',
        f"Catalog fingerprint: `{packet['documentFingerprint']}`", '',
        '## Readiness', '',
        'Validated for build: ' + (', '.join(packet['readyScenes']) or 'none'),
        'Deferred: ' + (', '.join(packet['deferredScenes']) or 'none'), '']
    for p in packet['packets']:
        s = p['scene']
        lines += [f"## {s['id']}", '', f"Status: {p['status']}", '']
        for key in ('participants', 'location', 'storyState', 'purpose', 'previousContext',
                    'followingContext', 'branchAlternatives', 'uncertainty', 'notes'):
            if s.get(key):
                lines += [f"{key}: {s[key]}", '']
        for r in p['records']:
            lines += [f"### {r['id']}", '', r['canonicalEnglish'] or '[Canonical English needed]', '']
            if r['context'].get('uncertainty'):
                lines += [f"Uncertainty: {r['context']['uncertainty']}", '']
        if p['issues']:
            lines += ['Blockers:', ''] + ['- ' + issue for issue in p['issues']] + ['']
        lines += ['Playtest after building this scene:', '',
            '- [ ] Record build manifest/hash, save/story state, and route used.',
            '- [ ] Check available branch alternatives; record unvisited branches.',
            '- [ ] Check speakers, names, wrapping, highlights, and complete messages.',
            '- [ ] Read for intent, voice, terminology, and natural responses.',
            '- [ ] Record feedback with entry ID where known; screenshots when useful.', '']
    return '\n'.join(lines)
