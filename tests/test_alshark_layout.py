import unittest
from profiles.alshark.layout import validate_dialogue


def text(value):
    return {'kind': 'text', 'translation': value}


class LayoutTests(unittest.TestCase):
    def test_wait_does_not_clear_rows(self):
        tokens = [text('A\nB\nC\nD'), {'kind': 'control', 'raw': '30'}, text('\nE')]
        with self.assertRaises(ValueError):
            validate_dialogue(tokens, {})

    def test_name_width_and_text_accumulate(self):
        tokens = [{'kind': 'name', 'name_id': 4}, text('ABCDEFGHIJK')]
        with self.assertRaises(ValueError):
            validate_dialogue(tokens, {4: 'KARU'})

    def test_header_and_clear_are_separate(self):
        tokens = [{'kind': 'control', 'raw': '34'}, text('KARU'),
                  {'kind': 'control', 'raw': '35'}, text('A\nB\nC\nD'),
                  {'kind': 'control', 'raw': '5f'}, text('E')]
        validate_dialogue(tokens, {})

    def test_unknown_layout_mode_rejected(self):
        with self.assertRaises(ValueError):
            validate_dialogue([{'kind': 'control', 'raw': '2f'}], {})

    def test_colour_change_keeps_current_column(self):
        tokens = [{'kind': 'control', 'raw': '33'}, text('PROTECTOR'),
                  {'kind': 'control', 'raw': '36'}, text(' FOUND!')]
        validate_dialogue(tokens, {}, columns=16)
        with self.assertRaises(ValueError):
            validate_dialogue(tokens, {}, columns=14)
