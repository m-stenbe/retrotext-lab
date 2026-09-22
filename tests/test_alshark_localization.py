import copy
import unittest
from unittest.mock import patch

from profiles.alshark.localization import validate_sources
from retrotext.localization import FORMAT, make_record


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
