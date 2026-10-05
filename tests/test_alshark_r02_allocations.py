import copy
from pathlib import Path
import unittest

from profiles.alshark.r02_allocations import (
    END_009, ENTRY_008, ENTRY_009, NEW_START_009, POINTER_009,
    START_008, START_009, relocate_girl_header,
)
from profiles.alshark.script import decode_entry, rebuild_entry
from profiles.alshark.script_tool import export_disk


ORIGINAL = Path(__file__).resolve().parents[2] / 'alshark' / 'original' / 'Alshark (System Disk).hdm'


@unittest.skipUnless(ORIGINAL.is_file(), 'Original System image is not available')
class R02AllocationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = ORIGINAL.read_bytes()
        cls.source = {entry['id']: entry for entry in export_disk(cls.original)['entries']}

    def setUp(self):
        self.edited = copy.deepcopy(self.source)
        right_tokens = self.edited[ENTRY_009]['tokens']
        next(t for t in right_tokens if t['id'] == 't001')['translation'] = 'OUTLAW'
        next(t for t in right_tokens if t['id'] == 't003')['translation'] = (
            'INFORMANTS?\nTRY THE BAR\nUNDERGROUND.'
        )
        self.rebuilt = bytearray(self.original)
        self.rebuilt[START_009:END_009] = rebuild_entry(
            self.original[START_009:END_009], right_tokens
        )
        next(t for t in self.edited[ENTRY_008]['tokens'] if t['id'] == 't001')[
            'translation'
        ] = 'GIRL'

    def test_exact_boundary_shift_and_preserved_commands(self):
        patched, manifests = relocate_girl_header(
            self.original, bytes(self.rebuilt), self.edited,
            {ENTRY_008, ENTRY_009},
        )
        self.assertEqual(len(patched), len(self.original))
        self.assertEqual(patched[POINTER_009:POINTER_009+2], b'\x00\x03')
        self.assertEqual(patched[NEW_START_009:END_009],
                         self.rebuilt[START_009:END_009-2])
        self.assertEqual(patched[START_008:NEW_START_009],
                         bytes.fromhex('344749524c352342020e482347014900'))
        self.assertEqual([m['size'] for m in manifests], [16, 47, 2])
        self.assertEqual([m['offset'] for m in manifests],
                         [START_008, NEW_START_009, POINTER_009])
        changed = {i for i, (a, b) in enumerate(zip(self.rebuilt, patched)) if a != b}
        allowed = set(range(START_008, END_009)) | {POINTER_009, POINTER_009+1}
        self.assertLessEqual(changed, allowed)
        self.assertEqual(len([t for t in decode_entry(patched[START_008:NEW_START_009])
                              if t['kind'] == 'command']), 2)
        self.assertEqual(
            [t['raw'] for t in decode_entry(patched[NEW_START_009:END_009])
             if t['kind'] == 'command'],
            [t['raw'] for t in self.source[ENTRY_009]['tokens'] if t['kind'] == 'command'],
        )

    def test_unselected_is_noop(self):
        patched, manifests = relocate_girl_header(
            self.original, bytes(self.rebuilt), self.edited, {ENTRY_009}
        )
        self.assertEqual(patched, bytes(self.rebuilt))
        self.assertEqual(manifests, [])

    def test_requires_adapted_neighbor_and_deferred_header(self):
        with self.assertRaisesRegex(ValueError, 'requires adapted adjacent'):
            relocate_girl_header(self.original, bytes(self.rebuilt), self.edited,
                                 {ENTRY_008})
        modified = bytearray(self.rebuilt)
        modified[START_008] ^= 1
        with self.assertRaisesRegex(ValueError, 'deferred'):
            relocate_girl_header(self.original, bytes(modified), self.edited,
                                 {ENTRY_008, ENTRY_009})

    def test_rejects_padding_or_header_changes(self):
        modified = bytearray(self.rebuilt)
        modified[END_009-1] = 1
        with self.assertRaisesRegex(ValueError, '47-byte adapted body'):
            relocate_girl_header(self.original, bytes(modified), self.edited,
                                 {ENTRY_008, ENTRY_009})
        next(t for t in self.edited[ENTRY_008]['tokens'] if t['id'] == 't001')[
            'translation'
        ] = 'GALS'
        with self.assertRaisesRegex(ValueError, 'reviewed GIRL header'):
            relocate_girl_header(self.original, bytes(self.rebuilt), self.edited,
                                 {ENTRY_008, ENTRY_009})

    def test_rejects_unreviewed_source(self):
        original = bytearray(self.original)
        original[START_008] ^= 1
        with self.assertRaisesRegex(ValueError, 'guarded original'):
            relocate_girl_header(bytes(original), bytes(self.rebuilt), self.edited,
                                 {ENTRY_008, ENTRY_009})


if __name__ == '__main__':
    unittest.main()
