import unittest

from profiles.alshark.menu_patch import encode_ui, replace_ui


class UiTests(unittest.TestCase):
    def test_repacked_rows_preserve_surrounding_bytes_and_allocation(self):
        source = 'ＡＡＡＡ@ＢＢＢＢ'
        old = source.encode('cp932') + b'\0'
        image = bytearray(b'LEFT' + old + b'RIGHT')
        replace_ui(image, 4, source, 'YES\nNO', menu=True)
        self.assertEqual(image[:4], b'LEFT')
        self.assertEqual(image[4 + len(old):], b'RIGHT')
        self.assertEqual(len(image), 4 + len(old) + 5)
        self.assertEqual(image[4:4 + len(encode_ui('YES\nNO'))],
                         'ＹＥＳ@ＮＯ'.encode('cp932'))

    def test_invalid_edits_leave_image_unchanged(self):
        for source, replacement, menu in [
            ('Ａ@Ｂ', 'TOO LONG\nB', True),
            ('Ａ@Ｂ', 'A', True),
            ('Ｃ@Ｄ', 'A\nB', True),
        ]:
            image = bytearray('Ａ@Ｂ\0'.encode('cp932'))
            original = bytes(image)
            with self.assertRaises(ValueError):
                replace_ui(image, 0, source, replacement, menu=menu)
            self.assertEqual(image, original)

    def test_digits_and_punctuation_are_fullwidth(self):
        self.assertEqual(encode_ui('80!'), '８０！'.encode('cp932'))


if __name__ == '__main__':
    unittest.main()
