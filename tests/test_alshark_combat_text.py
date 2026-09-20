import unicodedata
import unittest

from profiles.alshark.combat_text import fixed_text, patch_script_spans
from profiles.alshark.script import decode_entry


class FixedCombatTextTests(unittest.TestCase):
    def test_equivalent_glyphs_fill_span_without_extra_cells(self):
        encoded = fixed_text('HELLO!', 12)
        self.assertEqual(len(encoded), 12)
        self.assertEqual(unicodedata.normalize('NFKC', encoded.decode('cp932')), 'HELLO!')
        self.assertEqual(len(encoded.decode('cp932')), 6)
        with self.assertRaises(ValueError):
            fixed_text('HELLO!', 6)
        with self.assertRaises(ValueError):
            fixed_text('HI', 5)

    def test_runtime_name_and_numeric_offsets_do_not_move(self):
        original = b'3' + 'ＡＢＣＤＥＦ'.encode('cp932') + b'1@0$\x01(\x03\0'
        image = bytearray(original)
        patch_script_spans(image, original, 0, len(original), {'t001': 'HELLO!'})
        self.assertEqual(image[13:], original[13:])
        self.assertEqual(len(image), len(original))
        # Simulate the game's update through the original name-ID address.
        image[original.index(b'$') + 1] = 3
        tokens = decode_entry(image)
        self.assertEqual(next(t['name_id'] for t in tokens if t['kind'] == 'name'), 3)
        self.assertEqual(next(t['raw'] for t in tokens if t['kind'] == 'display_argument'), '2803')

    def test_unknown_token_rejects_whole_operation(self):
        original = 'ＡＢＣＤＥＦ\0'.encode('cp932')
        image = bytearray(original)
        with self.assertRaises(ValueError):
            patch_script_spans(image, original, 0, len(original),
                               {'t000': 'HELLO!', 't999': 'BAD'})
        self.assertEqual(image, original)
