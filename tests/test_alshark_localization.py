import copy
import unittest
from unittest.mock import patch

from profiles.alshark.localization import validate_sources, apply_editorial_review
from retrotext.localization import FORMAT, make_record, fingerprint, validate_editorial


class LocalizationSourceTests(unittest.TestCase):
    def fixture(self):
        r = make_record('script:test', 'script', {'entry': {'tokens': [
            {'id': 't000', 'kind': 'command', 'raw': '2350020029'},
            {'id': 't001', 'kind': 'text', 'raw': '4142', 'source': 'AB'},
        ], 'offset': 10, 'size': 8, 'editable': False}}, {'t001': 'OLD'})
        return dict(format=FORMAT, profile='alshark', sourceHashes={'System': 'hash'},
                    coverageNotes=[], scenes=[], records=[r])

    def check(self, expected, edited):
        with patch('profiles.alshark.localization.catalog', return_value=expected):
            validate_sources({}, edited)

    def test_editorial_fields_are_independent_of_source(self):
        original = self.fixture()
        edited = copy.deepcopy(original)
        edited['records'][0]['canonicalEnglish'] = 'Natural English without a byte limit.'
        edited['records'][0]['context']['intent'] = 'A friendly welcome'
        self.check(original, edited)

    def test_original_bytes_commands_and_allowlist_cannot_be_changed(self):
        for field in ('raw', 'command', 'offset', 'editable', 'remove'):
            original = self.fixture()
            edited = copy.deepcopy(original)
            entry = edited['records'][0]['source']['entry']
            if field == 'raw':
                entry['tokens'][1]['raw'] = '4143'
            elif field == 'command':
                entry['tokens'][0]['raw'] = '2350020028'
            elif field == 'remove':
                edited['records'] = []
            else:
                entry[field] = True if field == 'editable' else 11
            with self.assertRaises(ValueError):
                self.check(original, edited)

    def test_changed_legacy_text_cannot_bypass_workflow_as_legacy(self):
        original = self.fixture()
        edited = copy.deepcopy(original)
        edited['records'][0]['target']['inGameEnglish']['t001'] = 'NEW'
        with self.assertRaisesRegex(ValueError, 'canonical/review/adaptation'):
            self.check(original, edited)


class EditorialPackTests(unittest.TestCase):
    def fixture(self):
        records = [make_record(i, 'script', {'raw': i}, {'t001': 'OLD'}) for i in ('a', 'b')]
        document = dict(format=FORMAT, sourceHashes={'System': 'synthetic'}, scenes=[], records=records)
        pack = dict(format='retrotext-editorial-review-v1', sourceHashes=document['sourceHashes'],
                    reviewer='Test editor', scenes=[dict(id='scene', records=['a', 'b'],
                    terminology=[], reviewNote='Synthetic editorial review, not game dialogue.')],
                    records=[dict(id=r['id'], sourceFingerprint=fingerprint(r['source']),
                    canonicalEnglish='A complete natural English sentence.', context=r['context'],
                    findings=['Existing abbreviation loses detail.'],
                    adaptationAssessment={'status': 'needs_adaptation', 'reason': None}) for r in records])
        return document, pack, {'terms': []}

    def test_attaches_review_without_changing_source_or_approving_fit(self):
        document, pack, bible = self.fixture()
        before = copy.deepcopy(document)
        reviewed = apply_editorial_review(document, pack, bible)
        self.assertEqual(document, before)
        validate_editorial(reviewed, bible)
        for old, new in zip(document['records'], reviewed['records']):
            self.assertEqual(old['source'], new['source'])
            self.assertEqual(old['target']['inGameEnglish'], new['target']['inGameEnglish'])
            self.assertEqual(new['target']['status'], 'draft')
            self.assertIsNotNone(new['review'])

    def test_late_source_mismatch_cannot_partially_hydrate(self):
        document, pack, bible = self.fixture()
        before = copy.deepcopy(document)
        pack['records'][-1]['sourceFingerprint'] = 'changed'
        with self.assertRaisesRegex(ValueError, 'fingerprint mismatch'):
            apply_editorial_review(document, pack, bible)
        self.assertEqual(document, before)

    def test_fitting_blocker_is_retained_and_existing_work_not_overwritten(self):
        document, pack, bible = self.fixture()
        pack['records'][0]['adaptationAssessment'] = dict(status='DOES_NOT_FIT', reason='Meaning cannot fit.')
        reviewed = apply_editorial_review(document, pack, bible)
        self.assertEqual(reviewed['records'][0]['target']['status'], 'DOES_NOT_FIT')
        validate_editorial(reviewed, bible)
        with self.assertRaises(ValueError):
            apply_editorial_review(reviewed, pack, bible)

    def test_missing_or_duplicate_review_members_rejected(self):
        for members in (['a'], ['a', 'b', 'b']):
            document, pack, bible = self.fixture()
            pack['scenes'][0]['records'] = members
            with self.assertRaises(ValueError):
                apply_editorial_review(document, pack, bible)
