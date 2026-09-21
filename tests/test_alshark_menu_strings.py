import unittest
import unicodedata

from profiles.alshark.menu_strings import MENUS, POOL_START, POOL_SIZE, expand_menu_strings


class ExpandedMenuTests(unittest.TestCase):
    def fixture(self):
        data = bytearray(0x6000)
        for offset, expected, _ in MENUS:
            data[offset:offset+6] = bytes.fromhex(expected)
        return data

    def test_driver_pointers_resolve_complete_rows_within_boxes(self):
        data = self.fixture()
        before = bytes(data)
        records = expand_menu_strings(data)
        allowed = set(range(POOL_START, POOL_START+POOL_SIZE))
        for record in records:
            offset = record['record_offset']
            allowed.update((offset+4, offset+5))
            address = int.from_bytes(data[offset+4:offset+6], 'little') + 0x2000
            self.assertGreaterEqual(address, POOL_START)
            end = data.index(0, address)
            self.assertLess(end, POOL_START+POOL_SIZE)
            text = unicodedata.normalize('NFKC', data[address:end].decode('cp932'))
            self.assertEqual(text.replace('@', '\n'), record['translation'])
            self.assertEqual(len(text.split('@')), data[offset+1])
            self.assertTrue(all(len(row) <= data[offset] for row in text.split('@')))
        self.assertEqual(len(before), len(data))
        self.assertTrue(all(i in allowed for i, (a, b) in enumerate(zip(before, data)) if a != b))

    def test_occupied_pool_and_late_record_mismatch_leave_image_unchanged(self):
        for target in (POOL_START+POOL_SIZE-1, MENUS[-1][0]+4):
            data = self.fixture()
            data[target] ^= 1
            before = bytes(data)
            with self.assertRaises(ValueError):
                expand_menu_strings(data)
            self.assertEqual(data, before)
