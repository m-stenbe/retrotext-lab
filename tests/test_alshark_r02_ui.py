import unittest
from profiles.alshark.interface import encode_scrap_ui, R02_SCRAP_UI


class ScrapUITests(unittest.TestCase):
    def source(self):
        data = bytearray(0x10000)
        data[0xf55c:0xf567] = bytes.fromhex('3c4172183c5b7306e8c3ff')
        return data

    def test_compact_labels_fit_fixed_spans_with_reserved_fields(self):
        values = {0x1e5b: 'JOE\n', 0x1e63: 'SCRAP?',
                  0x1e6e: '          FOR\n      SCRAP'}
        for offset, text in values.items():
            result = encode_scrap_ui(self.source(), offset, text)
            self.assertLessEqual(len(result), R02_SCRAP_UI[offset])
            self.assertTrue(result.endswith(b'\0'))
        raw = encode_scrap_ui(self.source(), 0x1e6e, values[0x1e6e])
        self.assertTrue(raw.startswith(b' '*9))
        self.assertTrue(raw.split(b'@')[1].startswith(b' '*5))
        self.assertIn('？'.encode('cp932'), encode_scrap_ui(self.source(), 0x1e63, 'SCRAP?'))

    def test_runtime_field_overlap_and_row_changes_rejected(self):
        for offset, text in [(0x1e6e, 'ITEM FOR\n     SCRAP'),
                             (0x1e6e, '         FOR\nSCRAP'),
                             (0x1e6e, '         FOR'),
                             (0x1e5b, 'JOE'),
                             (0x1e63, 'SCRAP?\nYES')]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                encode_scrap_ui(self.source(), offset, text)

    def test_renderer_and_character_guards(self):
        damaged = self.source()
        damaged[0xf560] = 0
        with self.assertRaisesRegex(ValueError, 'renderer'):
            encode_scrap_ui(damaged, 0x1e63, 'SCRAP?')
        for text in ('Scrap?', 'SCRAP/KEEP', 'SCRAP>'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                encode_scrap_ui(self.source(), 0x1e63, text)
