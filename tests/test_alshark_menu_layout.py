import unittest

from profiles.alshark.menu_layout import BOXES, HIGHLIGHTS, widen_menus


class MenuGeometryTests(unittest.TestCase):
    def fixture(self):
        opening, system = bytearray(0x5000), bytearray(0xa000)
        for offset, record, _ in BOXES:
            opening[offset:offset+6] = record
        for offset, _ in HIGHLIGHTS:
            system[offset:offset+5] = bytes.fromhex('c6 06 3e 1d 0a')
        return opening, system

    def test_only_width_fields_change_and_highlights_match(self):
        opening, system = self.fixture()
        originals = [bytes(opening), bytes(system)]
        records = widen_menus(opening, system)
        self.assertEqual(len(records), 5)
        for before, after, expected_offsets in (
            (originals[0], opening, {x[0] for x in BOXES}),
            (originals[1], system, {x[0]+4 for x in HIGHLIGHTS}),
        ):
            self.assertEqual(len(before), len(after))
            self.assertEqual({i for i, (a, b) in enumerate(zip(before, after)) if a != b},
                             expected_offsets)
        self.assertTrue(all(opening[a] == 6 for a, _, _ in BOXES))
        self.assertTrue(all(system[a+4] == 2*opening[BOXES[0][0]] for a, _ in HIGHLIGHTS))

    def test_bad_last_guard_does_not_partially_patch_other_image(self):
        opening, system = self.fixture()
        system[HIGHLIGHTS[-1][0]+4] = 0x0e
        originals = bytes(opening), bytes(system)
        with self.assertRaises(ValueError):
            widen_menus(opening, system)
        self.assertEqual((opening, system), originals)

    def test_changed_text_pointer_is_rejected(self):
        opening, system = self.fixture()
        opening[BOXES[0][0]+4] ^= 1
        with self.assertRaises(ValueError):
            widen_menus(opening, system)
