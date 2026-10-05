import unittest
from profiles.alshark.r04_pages import (advance_colour, page_separator,
                                      page_break_token, validate_page_break)

class R04NarrationPageTests(unittest.TestCase):
    def test_narration_restore_and_existing_controls(self):
        colour=advance_colour('default',dict(kind='control',raw='36'))
        self.assertEqual(page_separator(colour),b'0_6')
        self.assertEqual(advance_colour(colour,dict(kind='name',name_id=0)),colour)
        validate_page_break(colour,page_break_token(colour))
        for raw in ('31','34','35','5f'):
            self.assertEqual(advance_colour(colour,dict(kind='control',raw=raw)),'default')
        self.assertEqual(page_separator('default'),b'0_')

    def test_unreviewed_colour_header_and_reset_rejected(self):
        for colour in ('32','33','37','unknown'):
            with self.assertRaises(ValueError):
                page_separator(colour)
        with self.assertRaisesRegex(ValueError,'restoration mismatch'):
            validate_page_break('36',dict(kind='page_break'))
        with self.assertRaisesRegex(ValueError,'speaker header'):
            validate_page_break('36',page_break_token('36'),header=True)
        with self.assertRaisesRegex(ValueError,'restoration mismatch'):
            validate_page_break('default',page_break_token('36'))

    def test_shared_header_resets_and_unreviewed_calls_fail_closed(self):
        from profiles.alshark.r04_pages import HEADER_CALLS, validate_header_calls
        import copy
        entries={}
        for raw,(ident,controls) in HEADER_CALLS.items():
            entries[ident]={'tokens':[
                *[dict(kind='control',raw=r) for r in controls[:-1]],
                dict(kind='text',raw='4142'),dict(kind='control',raw=controls[-1]),
                dict(kind='end',raw='00')]}
            self.assertEqual(advance_colour('36',dict(kind='command',raw=raw)),'default')
        validate_header_calls(entries)
        changed=copy.deepcopy(entries)
        changed['05d000:001']['tokens'][-2]['raw']='36'
        with self.assertRaisesRegex(ValueError,'header source guard'):
            validate_header_calls(changed)
        unknown=advance_colour('36',dict(kind='command',raw='2350020029'))
        with self.assertRaises(ValueError):
            page_separator(unknown)
        self.assertEqual(advance_colour(unknown,dict(kind='control',raw='35')),'default')
