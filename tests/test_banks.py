import struct
import unittest
from retrotext.banks import relative_table, split_candidate


class BankTests(unittest.TestCase):
    def test_duplicate_pointers_and_binary_arguments(self):
        block = struct.pack('<3H', 6, 6, 10) + b'A\0B\xff' + b'C\0\xe5\xe5'
        pointers = relative_table(block)
        self.assertEqual(pointers, (6, 6, 10))
        prefix, parts = split_candidate(block, pointers)
        self.assertEqual(parts[0], b'')
        self.assertEqual(parts[1], b'A\0B\xff')
        self.assertEqual(prefix + b''.join(parts), block)

    def test_invalid_tables(self):
        for data in [b'', b'\x04', b'\x03\0abc',
                     struct.pack('<3H', 6, 9, 8)+b'abcd',
                     struct.pack('<2H', 4, 99)+b'abcd']:
            with self.subTest(data=data):
                self.assertIsNone(relative_table(data))

    def test_wrong_pointer_list(self):
        with self.assertRaises(ValueError):
            split_candidate(struct.pack('<2H', 4, 6)+b'abcd', (4, 7))
