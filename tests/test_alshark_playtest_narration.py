import unittest
from profiles.alshark.playtest_narration import encode_text
from profiles.alshark.layout import validate_dialogue


def control(raw):
    return dict(kind='control',raw=raw)


def text(value):
    return dict(kind='text',translation=value)


class PlaytestNarrationTests(unittest.TestCase):
    def test_restore_only_narration_at_english_newlines(self):
        self.assertEqual(encode_text('FIRST\nSECOND','36',preserve_narration=True),b'FIRST@6SECOND')
        self.assertEqual(encode_text('FIRST\nSECOND','36'),b'FIRST@SECOND')
        for colour in ('default','32','33'):
            self.assertEqual(encode_text('FIRST\nSECOND',colour,preserve_narration=True),b'FIRST@SECOND')

    def test_repeated_header_never_resets_cursor(self):
        bad=[control('34'),control('36'),text('SION WATCHED A'),
             control('34'),control('36'),text('FLASHY DANCER')]
        with self.assertRaisesRegex(ValueError,'exceeds'):
            validate_dialogue(bad,{})
        good=[control('34'),control('36'),text('SION WATCHED\n'),
              control('34'),control('36'),text('A DANCER')]
        validate_dialogue(good,{})

    def test_header_to_body_advances_existing_cursor(self):
        validate_dialogue([control('34'),text('NAME'),control('35'),
                           text('ONE\nTWO\nTHREE\nFOUR')],{})
        with self.assertRaisesRegex(ValueError,'exceeds'):
            validate_dialogue([text('ONE\nTWO\nTHREE\nFOUR\n'),
                               control('34'),text('NAME'),control('35'),text('BODY')],{})
        validate_dialogue([text('ONE\nTWO\nTHREE\nFOUR\nFIVE')],{})

    def test_rebuild_opt_in_keeps_source_and_restores_each_page(self):
        from profiles.alshark.script import decode_entry, rebuild_entry
        raw=b'#S\x01\x046'+b'A'*48+b'\0'
        tokens=decode_entry(raw)
        next(t for t in tokens if t['kind']=='text')['translation']=['ONE\nTWO','THREE\nFOUR']
        out=rebuild_entry(raw,tokens,allow_pages=True,allow_narration_pages=True,
                          preserve_narration=True)
        self.assertTrue(out.startswith(b'#S\x01\x046ONE@6TWO0_6THREE@6FOUR\0'))
        legacy=rebuild_entry(raw,tokens,allow_pages=True,allow_narration_pages=True)
        self.assertTrue(legacy.startswith(b'#S\x01\x046ONE@TWO0_6THREE@FOUR\0'))
        self.assertEqual(len(out),len(raw))
        tokens[0]['raw']='23530105'
        with self.assertRaisesRegex(ValueError,'Only translation'):
            rebuild_entry(raw,tokens,allow_pages=True,preserve_narration=True)

    def test_added_attribute_bytes_still_obey_allocation(self):
        from profiles.alshark.script import decode_entry, rebuild_entry
        raw=b'6ABC\0';tokens=decode_entry(raw)
        next(t for t in tokens if t['kind']=='text')['translation']='A\nB'
        self.assertEqual(rebuild_entry(raw,tokens),b'6A@B\0')
        with self.assertRaisesRegex(ValueError,'allocation'):
            rebuild_entry(raw,tokens,preserve_narration=True)

    def test_original_import_is_scoped_and_byte_preserving(self):
        from pathlib import Path
        from profiles.alshark.script_tool import export_disk, import_disk
        original=Path(__file__).resolve().parents[2]/'alshark/original/Alshark (System Disk).hdm'
        if not original.is_file():
            self.skipTest('Original System image unavailable')
        source=original.read_bytes();document=export_disk(source)
        entry=next(e for e in document['entries'] if e['id']=='053000:001')
        for t in entry['tokens']:
            if t['kind']=='text':t['translation']='A\nB'
        out=import_disk(source,document,narration_entries={'053000:001'})
        a,n=entry['offset'],entry['size']
        self.assertEqual(out[:a],source[:a]);self.assertEqual(out[a+n:],source[a+n:])
        self.assertIn(b'A@6B',out[a:a+n])
        with self.assertRaisesRegex(ValueError,'reviewed editable scope'):
            import_disk(source,document,narration_entries={'invalid'})
