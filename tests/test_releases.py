import copy
import unittest

from retrotext.localization import FORMAT, make_record, review_scene
from retrotext.releases import DOMAINS, assess_release


class ReleaseTests(unittest.TestCase):
    def fixture(self):
        records = [make_record(i, 'script', {'raw': i}) for i in ('a', 'b')]
        doc = dict(format=FORMAT, sourceHashes={'System': 'synthetic'}, records=records,
                   scenes=[dict(id=i, records=[i]) for i in ('a', 'b')])
        bible = {'terms': []}
        for r in records:
            r.update(scene=r['id'], canonicalEnglish='Hello.')
            review_scene(doc, r['id'], bible, 'Editor', 'Synthetic scene review')
            r['target'].update(status='adapted', basedOn=r['review']['basis'], inGameEnglish='HELLO')
        plan = dict(format='retrotext-release-plan-v1', id='first-section',
                    boundary={'start': 'Start', 'end': 'Return'}, sourceHashes=doc['sourceHashes'],
                    scenes=['a', 'b'], requiredRecords=['a', 'b'], openIssues=[],
                    inventory=[dict(domain=d, status='mapped', evidence=['Synthetic evidence'])
                               for d in sorted(DOMAINS)])
        return doc, bible, plan

    def test_complete_selection_is_candidate_not_runtime_approval(self):
        args = self.fixture()
        before = copy.deepcopy(args)
        calls = []
        report = assess_release(*args, lambda scenes: calls.append(scenes) or [])
        self.assertEqual(report['status'], 'candidate_ready')
        self.assertFalse(report['runtimeVerified'])
        self.assertEqual(calls[-1], ['a', 'b'])
        self.assertEqual(args, before)

    def test_ready_scripts_do_not_cover_an_unmapped_cinematic(self):
        doc, bible, plan = self.fixture()
        next(i for i in plan['inventory'] if i['domain'] == 'cinematics')['status'] = 'open'
        self.assertEqual(assess_release(doc, bible, plan, lambda _: [])['status'], 'blocked')

    def test_subset_or_incomplete_inventory_cannot_pass(self):
        for field in ('scenes', 'requiredRecords'):
            doc, bible, plan = self.fixture()
            plan[field] = ['a']
            self.assertEqual(assess_release(doc, bible, plan, lambda _: [])['status'], 'blocked')

    def test_pending_adaptation_blocks_whole_section(self):
        doc, bible, plan = self.fixture()
        doc['records'][1]['target']['status'] = 'draft'
        report = assess_release(doc, bible, plan, lambda _: [])
        self.assertEqual(report['status'], 'blocked')
        self.assertEqual(report['readyScenes'], ['a'])

    def test_source_drift_and_missing_evidence_fail(self):
        doc, bible, plan = self.fixture()
        plan['sourceHashes'] = {'System': 'different'}
        with self.assertRaisesRegex(ValueError, 'source hashes'):
            assess_release(doc, bible, plan, lambda _: [])
        plan['sourceHashes'] = doc['sourceHashes']
        plan['inventory'][0]['evidence'] = []
        self.assertEqual(assess_release(doc, bible, plan, lambda _: [])['status'], 'blocked')

    def test_coupled_allocations_compile_as_a_whole(self):
        doc, bible, plan = self.fixture()
        plan['compileTogether'] = [['a', 'b']]
        def compile(scenes):
            if set(scenes) != {'a', 'b'}:
                raise ValueError('Incomplete shared allocation')
            return []
        self.assertEqual(assess_release(doc, bible, plan, compile)['status'], 'candidate_ready')
        for groups in ([['a'], ['a', 'b']], [['a', 'missing']], [[]], [['a', 'a']]):
            plan['compileTogether'] = groups
            with self.assertRaisesRegex(ValueError, 'coupled compilation'):
                assess_release(doc, bible, plan, compile)

    def test_coupled_group_does_not_hide_pending_member(self):
        doc, bible, plan = self.fixture()
        plan['compileTogether'] = [['a', 'b']]
        doc['records'][1]['target']['status'] = 'draft'
        self.assertEqual(assess_release(doc, bible, plan, lambda _: [])['status'], 'blocked')

    def test_combined_compilation_must_pass_and_open_issues_block(self):
        def compile(scenes):
            if len(scenes) > 1:
                raise ValueError('Combined allocation failure')
            return []
        with self.assertRaisesRegex(ValueError, 'Combined allocation'):
            assess_release(*self.fixture(), compile)
        doc, bible, plan = self.fixture()
        plan['openIssues'] = [dict(id='RE-1', summary='Unidentified text path')]
        self.assertEqual(assess_release(doc, bible, plan, lambda _: [])['status'], 'blocked')
