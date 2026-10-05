"""Section-level candidate gate; work-packet readiness is not route coverage."""
from .batches import prepare_batch
from .localization import fingerprint


DOMAINS = {'route', 'branches', 'cinematics', 'ui', 'names_items'}


def assess_release(document, bible, plan, check_scene):
    if plan.get('format') != 'retrotext-release-plan-v1' or not plan.get('boundary'):
        raise ValueError('Invalid release plan or missing playable boundary')
    if not plan.get('sourceHashes') or plan['sourceHashes'] != document.get('sourceHashes'):
        raise ValueError('Release plan source hashes do not match the catalog')
    inventories = plan.get('inventory', [])
    if {i['domain'] for i in inventories} != DOMAINS or len(inventories) != len(DOMAINS):
        raise ValueError('Release inventory must cover each required domain exactly once')
    required = plan.get('requiredRecords', [])
    if not required or len(required) != len(set(required)):
        raise ValueError('Release requires a nonempty unique record inventory')
    records = {r['id']: r for r in document['records']}
    if set(required) - records.keys():
        raise ValueError('Unknown required release record')
    blockers = []
    for item in inventories:
        if item['status'] not in ('open', 'mapped'):
            raise ValueError('Invalid inventory status')
        if item['status'] != 'mapped' or not item.get('evidence'):
            blockers.append(f"{item['domain']}: coverage mapping incomplete")
    for issue in plan.get('openIssues', []):
        blockers.append(f"{issue['id']}: {issue['summary']}")
    batch = dict(format='retrotext-batch-plan-v1', id=plan['id'], scenes=plan['scenes'],
                 compileTogether=plan.get('compileTogether', []))
    packet = prepare_batch(document, bible, batch, check_scene)
    members = {r['id'] for item in packet['packets'] for r in item['records']}
    for ident in sorted(members - set(required)):
        blockers.append(f'{ident}: selected scene member is missing from release inventory')
    for ident in required:
        if records[ident]['scene'] not in plan['scenes']:
            blockers.append(f'{ident}: required record is outside selected scenes')
    for item in packet['packets']:
        blockers.extend(f"{item['scene']['id']}: {issue}" for issue in item['issues'])
    return dict(format='retrotext-release-assessment-v1', id=plan['id'],
                boundary=plan['boundary'], planFingerprint=fingerprint(plan),
                documentFingerprint=packet['documentFingerprint'],
                bibleFingerprint=packet['bibleFingerprint'],
                sourceHashes=packet['sourceHashes'],
                status='blocked' if blockers else 'candidate_ready',
                runtimeVerified=False, requiredRecords=len(required),
                selectedScenes=plan['scenes'], readyScenes=packet['readyScenes'],
                deferredScenes=packet['deferredScenes'], blockers=blockers)
