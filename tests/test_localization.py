import copy
import unittest

from retrotext.localization import (FORMAT, make_record, review_scene,
                                   validate_editorial, terminology_impact)


class LocalizationTests(unittest.TestCase):
    def fixture(self):
        records = [make_record(i, 'dialogue', {'raw': '00'}) for i in ('a', 'b')]
        for r in records:
            r['scene'] = 'visit'
            r['canonicalEnglish'] = 'Welcome back. How have you been?'
        doc = dict(format=FORMAT, records=records, scenes=[dict(id='visit', records=['a', 'b'],
                   terminology=['character.friend'], storyState='Before departure')])
        bible = dict(terms=[dict(id='character.friend', english='Friend', status='working')])
        return doc, bible

    def reviewed(self):
        doc, bible = self.fixture()
        review_scene(doc, 'visit', bible, 'Test editor', 'Read both lines and checked context.')
        r = doc['records'][0]
        r['target'].update(status='adapted', inGameEnglish={'t001': 'WELCOME BACK.'},
                           basedOn=r['review']['basis'])
        return doc, bible

    def test_canonical_has_no_rom_font_or_length_limit(self):
        doc, bible = self.fixture()
        doc['records'][0]['canonicalEnglish'] = '“You’re back!” she said. ' * 100
        review_scene(doc, 'visit', bible, 'Editor', 'Reviewed continuous scene.')
        validate_editorial(doc, bible)

    def test_adaptation_changes_do_not_modify_canonical_or_source(self):
        doc, bible = self.reviewed()
        before = copy.deepcopy(doc['records'][0])
        doc['records'][0]['target']['inGameEnglish'] = {'t001': 'HELLO AGAIN.'}
        validate_editorial(doc, bible)
        for key in ('source', 'canonicalEnglish', 'context', 'review'):
            self.assertEqual(doc['records'][0][key], before[key])

    def test_following_line_context_and_term_changes_invalidate_review(self):
        for change in ('following', 'context', 'term'):
            doc, bible = self.reviewed()
            if change == 'following':
                doc['records'][1]['canonicalEnglish'] = 'We have never met.'
            elif change == 'context':
                doc['scenes'][0]['storyState'] = 'After departure'
            else:
                bible['terms'][0]['english'] = 'Neighbor'
            with self.assertRaisesRegex(ValueError, 'stale'):
                validate_editorial(doc, bible)

    def test_whole_scene_must_have_canonical_before_review(self):
        doc, bible = self.fixture()
        doc['records'][1]['canonicalEnglish'] = None
        with self.assertRaises(ValueError):
            review_scene(doc, 'visit', bible, 'Editor', 'Reviewed')
        self.assertTrue(all(r['review'] is None for r in doc['records']))

    def test_does_not_fit_needs_reason_and_preserves_canonical(self):
        doc, bible = self.reviewed()
        target = doc['records'][0]['target']
        target.update(status='DOES_NOT_FIT', reason=None)
        with self.assertRaises(ValueError):
            validate_editorial(doc, bible)
        target['reason'] = 'Four rows cannot preserve the warning and speaker intent.'
        validate_editorial(doc, bible)

    def test_no_adaptation_without_review_and_no_stale_adaptation_after_rereview(self):
        doc, bible = self.reviewed()
        doc['records'][0]['review'] = None
        with self.assertRaises(ValueError):
            validate_editorial(doc, bible)
        doc['records'][0]['canonicalEnglish'] = 'Goodbye.'
        review_scene(doc, 'visit', bible, 'Editor', 'Reviewed changed scene.')
        with self.assertRaisesRegex(ValueError, 'adaptation is stale'):
            validate_editorial(doc, bible)

    def test_terminology_impact_includes_scene_peers(self):
        doc, _ = self.fixture()
        self.assertEqual(terminology_impact(doc, 'character.friend'), ['a', 'b'])

    def test_duplicate_ids_and_unknown_terms_are_rejected(self):
        doc, bible = self.fixture()
        doc['records'].append(copy.deepcopy(doc['records'][0]))
        with self.assertRaises(ValueError):
            validate_editorial(doc, bible)
        doc, bible = self.fixture()
        doc['records'][0]['context']['terminology'] = ['unknown']
        with self.assertRaises(ValueError):
            review_scene(doc, 'visit', bible, 'Editor', 'Reviewed')
