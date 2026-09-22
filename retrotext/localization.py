"""Game-independent editorial state, separate from byte-preserving exporters.

No encoders or cell limits belong here. Review fingerprints bind canonical
English to its scene context and terminology; adaptations bind to that review.
"""
import hashlib
import json

FORMAT = 'retrotext-localization-v1'
STATUSES = {'untranslated', 'legacy_provisional', 'draft', 'adapted', 'DOES_NOT_FIT'}


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def make_record(ident, kind, source, legacy=None):
    return dict(id=ident, kind=kind, source=source, scene=None,
                context=dict(speaker=None, listener=None, intent=None, tone=None,
                             terminology=[], uncertainty=[], notes=[]),
                canonicalEnglish=None, review=None,
                target=dict(status='legacy_provisional' if legacy else 'untranslated',
                            inGameEnglish=legacy, basedOn=None, reason=None,
                            notes=[], playtest=[]))


def index_unique(records, label):
    result = {}
    for record in records:
        ident = record['id']
        if ident in result:
            raise ValueError(f'Duplicate {label}: {ident}')
        result[ident] = record
    return result


def review_basis(document, record, bible):
    scenes = index_unique(document['scenes'], 'scene')
    scene = scenes.get(record['scene'])
    if scene is None or record['id'] not in scene['records']:
        raise ValueError(f"{record['id']}: assign a connected scene before review")
    records = index_unique(document['records'], 'record')
    terms = index_unique(bible['terms'], 'term')
    members = []
    referenced = set(scene.get('terminology', []))
    for ident in scene['records']:
        member = records[ident]
        if member['scene'] != scene['id']:
            raise ValueError('Scene membership must agree in both directions')
        if not isinstance(member['canonicalEnglish'], str) or not member['canonicalEnglish'].strip():
            raise ValueError(f'{ident}: complete canonical English for the whole scene first')
        referenced.update(member['context']['terminology'])
        members.append({k: member[k] for k in ('id', 'source', 'context', 'canonicalEnglish')})
    missing = referenced - terms.keys()
    if missing:
        raise ValueError(f'Unknown terminology: {sorted(missing)}')
    return fingerprint(dict(scene=scene, members=members,
                            terminology=[terms[k] for k in sorted(referenced)]))


def review_scene(document, scene_id, bible, reviewer, note):
    """Record a human/editor attestation, never infer review from a test pass."""
    if not reviewer.strip() or not note.strip():
        raise ValueError('Reviewer and editorial review note are required')
    scene = index_unique(document['scenes'], 'scene')[scene_id]
    records = index_unique(document['records'], 'record')
    plans = [(records[i], review_basis(document, records[i], bible)) for i in scene['records']]
    if not plans:
        raise ValueError('Cannot review an empty scene')
    for record, basis in plans:
        record['review'] = dict(basis=basis, reviewer=reviewer, note=note)


def validate_editorial(document, bible):
    if document['format'] != FORMAT:
        raise ValueError('Unsupported localization document')
    records = index_unique(document['records'], 'record')
    scenes = index_unique(document['scenes'], 'scene')
    index_unique(bible['terms'], 'term')
    for scene in scenes.values():
        if len(set(scene['records'])) != len(scene['records']):
            raise ValueError('Duplicate scene member')
        for ident in scene['records']:
            if ident not in records or records[ident]['scene'] != scene['id']:
                raise ValueError('Unknown or inconsistent scene member')
    for record in records.values():
        target = record['target']
        if target['status'] not in STATUSES:
            raise ValueError(f"{record['id']}: unknown target status")
        canonical = record['canonicalEnglish']
        if canonical is not None and (not isinstance(canonical, str) or not canonical.strip()):
            raise ValueError('Canonical English must be nonempty text or null')
        if record['scene'] is not None:
            if record['scene'] not in scenes or record['id'] not in scenes[record['scene']]['records']:
                raise ValueError('Unknown or inconsistent scene assignment')
        review = record['review']
        if review is not None:
            if not review.get('reviewer') or not review.get('note'):
                raise ValueError('Incomplete editorial attestation')
            if review['basis'] != review_basis(document, record, bible):
                raise ValueError(f"{record['id']}: editorial review is stale (scene or terminology changed)")
        if target['status'] in ('adapted', 'DOES_NOT_FIT'):
            if review is None:
                raise ValueError(f"{record['id']}: canonical scene review required")
            if target['basedOn'] != review['basis']:
                raise ValueError(f"{record['id']}: adaptation is stale")
        if target['status'] == 'adapted' and not target['inGameEnglish']:
            raise ValueError('Adapted text is missing')
        if target['status'] == 'DOES_NOT_FIT' and not target['reason']:
            raise ValueError('DOES_NOT_FIT requires an engineering issue description')


def terminology_impact(document, term_id):
    """Find direct references and scene peers requiring another editorial pass."""
    scene_ids = {s['id'] for s in document['scenes'] if term_id in s.get('terminology', [])}
    scene_ids.update(r['scene'] for r in document['records'] if term_id in r['context']['terminology'])
    return [r['id'] for r in document['records']
            if term_id in r['context']['terminology'] or (r['scene'] is not None and r['scene'] in scene_ids)]
