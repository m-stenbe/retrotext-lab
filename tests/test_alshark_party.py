import unittest
from profiles.alshark.localization import composed_branch
from profiles.alshark.layout import validate_dialogue


class PartyBranchTests(unittest.TestCase):
    def fixture(self):
        return {
            'root': {'tokens': [
                {'kind': 'text', 'translation': '1234567890123'},
                {'kind': 'command', 'raw': '2342021009'},
                {'kind': 'text', 'translation': 'UNTAKEN FALLBACK'}]},
            'target': {'tokens': [{'kind': 'text', 'translation': 'XY'}]},
        }

    def test_taken_branch_keeps_caller_cursor_and_omits_fallback(self):
        entries = self.fixture()
        validate_dialogue(entries['target']['tokens'], {})
        composed = composed_branch('root', '2342021009', 'target', entries, {'target'})
        self.assertEqual(len(composed), 2)
        with self.assertRaisesRegex(ValueError, 'columns'):
            validate_dialogue(composed, {})
        entries['target']['tokens'][0]['translation'] = '\nXY'
        validate_dialogue(composed_branch('root', '2342021009', 'target', entries, {'target'}), {})

    def test_branch_source_must_be_unambiguous(self):
        entries = self.fixture()
        with self.assertRaisesRegex(ValueError, 'missing or ambiguous'):
            composed_branch('root', '2342020e10', 'target', entries, {'target'})
        entries['root']['tokens'].append(entries['root']['tokens'][1])
        with self.assertRaisesRegex(ValueError, 'missing or ambiguous'):
            composed_branch('root', '2342021009', 'target', entries, {'target'})
