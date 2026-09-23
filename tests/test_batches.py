import copy
import unittest
from retrotext.batches import prepare_batch, reading_sheet
from retrotext.localization import FORMAT, make_record, review_scene


class BatchTests(unittest.TestCase):
    def fixture(self):
        r = make_record('a', 'script', {'raw': '00'})
        r.update(scene='visit', canonicalEnglish='How have you been?')
        doc = dict(format=FORMAT, records=[r], scenes=[dict(id='visit', records=['a'])])
        bible = dict(terms=[])
        review_scene(doc, 'visit', bible, 'Editor', 'Read scene')
        r['target'].update(status='adapted', basedOn=r['review']['basis'], inGameEnglish='HELLO')
        plan = dict(format='retrotext-batch-plan-v1', id='test', scenes=['visit'])
        return doc, bible, plan

    def test_ready_requires_profile_checks_and_does_not_mutate(self):
        doc, bible, plan = self.fixture()
        before = copy.deepcopy(doc)
        calls = []
        packet = prepare_batch(doc, bible, plan, lambda ids: calls.append(ids) or [])
        self.assertEqual(calls, [['visit'], ['visit']])
        self.assertEqual(packet['readyScenes'], ['visit'])
        self.assertEqual(doc, before)
        packet['packets'][0]['records'][0]['source']['raw'] = 'ff'
        self.assertEqual(doc, before)
        self.assertIn('How have you been?', reading_sheet(packet))

    def test_profile_blocker_is_reported(self):
        def fail(ids):
            raise ValueError('shared-script layout adapter required')
        packet = prepare_batch(*self.fixture(), fail)
        self.assertEqual(packet['readyScenes'], [])
        self.assertIn('shared-script', packet['packets'][0]['issues'][0])

    def test_stale_review_blocks_all_readiness(self):
        doc, bible, plan = self.fixture()
        doc['records'][0]['canonicalEnglish'] = 'Changed meaning'
        packet = prepare_batch(doc, bible, plan, lambda ids: self.fail('Must not compile'))
        self.assertIn('stale', packet['globalEditorialError'])
        self.assertFalse(packet['readyScenes'])

    def test_dnf_and_missing_canonical_do_not_silently_adapt(self):
        doc, bible, plan = self.fixture()
        doc['records'][0]['target'].update(status='DOES_NOT_FIT', reason='Needs another page')
        packet = prepare_batch(doc, bible, plan, lambda ids: self.fail('Must not compile'))
        self.assertIn('Needs another page', reading_sheet(packet))
        r = doc['records'][0]
        r.update(canonicalEnglish=None, review=None)
        r['target']['status'] = 'untranslated'
        packet = prepare_batch(doc, bible, plan, lambda ids: self.fail('Must not compile'))
        self.assertIn('canonical English needed', reading_sheet(packet))

    def test_bad_selection_rejected(self):
        for selected in ([], ['missing'], ['visit', 'visit']):
            doc, bible, plan = self.fixture()
            plan['scenes'] = selected
            with self.assertRaises(ValueError):
                prepare_batch(doc, bible, plan, lambda ids: [])
