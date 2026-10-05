import unittest

from profiles.alshark.script import decode_entry, rebuild_entry
from profiles.alshark.localization import composed_dialogue
from profiles.alshark.layout import validate_dialogue


class R04PageIntegrationTests(unittest.TestCase):
    def test_narration_emits_restore_and_preserves_commands(self):
        source = b'#S\x01\x146' + b'A' * 80 + b'0\0'
        tokens = decode_entry(source)
        next(t for t in tokens if t['kind'] == 'text')['translation'] = ['FIRST PAGE', 'SECOND PAGE']
        with self.assertRaisesRegex(ValueError, 'reviewed adaptation'):
            rebuild_entry(source, tokens)
        result = rebuild_entry(source, tokens, allow_pages=True, allow_narration_pages=True)
        self.assertEqual(len(result), len(source))
        self.assertTrue(result.startswith(b'#S\x01\x146FIRST PAGE0_6SECOND PAGE0\0'))
        composed = composed_dialogue('054000:032', {'054000:032': dict(tokens=tokens)}, {'054000:032'})
        validate_dialogue(composed, {})

    def test_roy_header_call_resets_narration_before_new_pages(self):
        source = b'6INTRO0#P\x02\x0b\x25' + b'A' * 80 + b'0\0'
        tokens = decode_entry(source)
        texts = [t for t in tokens if t['kind'] == 'text']
        texts[0]['translation'] = 'INTRO'
        texts[1]['translation'] = ['FIRST', 'SECOND']
        header = decode_entry(b'_4ROY5\0')
        next(t for t in header if t['kind'] == 'text')['translation'] = 'ROY'
        entries = {'05c000:001': dict(tokens=tokens), '05c000:037': dict(tokens=header)}
        validate_dialogue(composed_dialogue('05c000:001', entries, set(entries)), {})
        result = rebuild_entry(source, tokens, allow_pages=True, allow_narration_pages=True)
        self.assertIn(b'FIRST0_SECOND', result)
        self.assertNotIn(b'FIRST0_6SECOND', result)

    def test_restored_narration_still_checks_every_page_and_header(self):
        for prefix, pages in ((b'6', ['OK', 'A' * 15]), (b'4', ['ONE', 'TWO']),
                              (b'3', ['ONE', 'TWO'])):
            tokens = decode_entry(prefix + b'A' * 50 + b'0\0')
            next(t for t in tokens if t['kind'] == 'text')['translation'] = pages
            with self.subTest(prefix=prefix), self.assertRaises(ValueError):
                validate_dialogue(composed_dialogue('054000:032',
                    {'054000:032': dict(tokens=tokens)}, {'054000:032'}), {})
