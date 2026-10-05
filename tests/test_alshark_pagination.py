import unittest
from profiles.alshark.script import decode_entry, rebuild_entry
from profiles.alshark.layout import validate_dialogue
from profiles.alshark.localization import composed_dialogue


class PaginationTests(unittest.TestCase):
    def fixture(self, prefix=b'4$\x005', pages=None):
        raw=prefix+b'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123\0'
        # ASCII digits are controls in source; immutable controls remain after text.
        tokens=decode_entry(raw)
        next(t for t in tokens if t['kind']=='text')['translation']=pages or ['FIRST PAGE','SECOND PAGE']
        return raw,tokens

    def test_opt_in_and_exact_wait_clear_with_source_commands_unchanged(self):
        raw,tokens=self.fixture(prefix=b'#S\x01\x044$\x005')
        with self.assertRaisesRegex(ValueError,'reviewed adaptation'):
            rebuild_entry(raw,tokens)
        out=rebuild_entry(raw,tokens,allow_pages=True)
        self.assertTrue(out.startswith(b'#S\x01\x044$\x005FIRST PAGE0_SECOND PAGE0123\0'))
        self.assertEqual(len(out),len(raw))

    def test_empty_pages_script_injection_and_overflow_rejected(self):
        for pages in (['A',''], ['A'], ['A','#S'], ['A','_'], ['A'*50,'B']):
            raw,tokens=self.fixture(pages=pages)
            with self.assertRaises(ValueError):
                rebuild_entry(raw,tokens,allow_pages=True)

    def test_header_and_colour_splits_rejected(self):
        for prefix in (b'4',b'6',b'3'):
            _,tokens=self.fixture(prefix=prefix)
            with self.assertRaisesRegex(ValueError,'speaker header|colour'):
                validate_dialogue(composed_dialogue('a',{'a':{'tokens':tokens}},{'a'}),{0:'SION'})

    def test_every_page_and_following_name_is_measured(self):
        _,tokens=self.fixture(pages=['FIRST','A'*14])
        tokens.insert(-1,dict(kind='name',name_id=0,raw='2400'))
        with self.assertRaisesRegex(ValueError,'exceeds'):
            validate_dialogue(composed_dialogue('a',{'a':{'tokens':tokens}},{'a'}),{0:'SION'})
