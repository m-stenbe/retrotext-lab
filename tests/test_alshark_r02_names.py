import unittest
from unittest.mock import patch
from pathlib import Path

from profiles.alshark import r02_names


LABELS = {
    'r02-item:1b': 'BROWNING', 'r02-item:1d': 'SUBM GUN',
    'r02-item:23': 'RAY GUN', 'r02-item:3d': 'MASK',
    'r02-item:44': 'SIGHT', 'r02-item:4d': 'EVASRING',
    'r02-item:51': 'TISHIELD', 'r02-item:75': 'TI BODY',
    'r02-item:93': 'TIBOOMER', 'r02-item:9a': 'HAND SAT',
    'r02-item:9c': 'CAN', 'r02-item:a3': 'TOOL SET',
    'r02-ability:23': 'DRIVER', 'r02-ability:24': 'BUBBLE',
    'r02-ability:40': 'ANALYZE', 'r02-ability:41': 'CUSTOM',
    'r02-ability:42': 'MECH FIX',
    'r02-location:2': 'BASEMENT BAR', 'r02-location:48': 'HAMACK',
    'r02-location:98': 'DUST', 'r02-location:103': 'JOE ROOM',
}


class R02NameTests(unittest.TestCase):
    def fixture(self):
        system = bytearray(0x1c000)
        for _, a, size, pointers, marker, _ in r02_names._specs():
            raw = marker.encode('ascii') + b'X'*(size-len(marker)-1) + b'\0'
            system[a:a+size] = raw
            for p in pointers:
                system[p:p+2] = (a-r02_names.BASE).to_bytes(2, 'little')
        return {'System': bytes(system), 'Opening': bytes(0x6000)}

    def compile(self, images, labels=LABELS):
        with patch.object(r02_names, 'guard_original'):
            return r02_names.compile_names(images, labels)

    def test_complete_group_aliases_and_patch_confinement(self):
        images = self.fixture()
        result, manifest = self.compile(images)
        self.assertEqual(set(LABELS), r02_names.REQUIRED)
        self.assertEqual(len(result), len(images['System']))
        self.assertEqual({r['record'] for r in manifest['records']}, set(LABELS))
        covered = set()
        for patch_range in manifest['patches']:
            covered.update(range(patch_range['offset'], patch_range['offset']+patch_range['size']))
        for i, (old, new) in enumerate(zip(images['System'], result)):
            if old != new:
                self.assertIn(i, covered)
        for record in manifest['records']:
            for p in record['pointers']:
                offset = r02_names.BASE+int.from_bytes(result[p:p+2], 'little')
                self.assertEqual(offset, record['offset'])
                text = result[offset:result.index(0, offset)].decode('ascii')
                self.assertEqual(text.lstrip(' >').replace('>', ' '), record['text'])
        self.assertEqual(len(next(r for r in manifest['records']
                                  if r['record'] == 'r02-ability:40')['pointers']), 3)
        self.assertEqual(len(next(r for r in manifest['records']
                                  if r['record'] == 'r02-ability:23')['pointers']), 5)

    def test_original_alias_guards_and_complete_group(self):
        original = self.fixture()
        for p, value in ((0x1037c, 0), (0x10200, 0x111b7-r02_names.BASE)):
            images = dict(original)
            data = bytearray(original['System'])
            data[p:p+2] = value.to_bytes(2, 'little')
            images['System'] = bytes(data)
            with self.subTest(pointer=hex(p)), self.assertRaises(ValueError):
                self.compile(images)
        incomplete = dict(LABELS)
        del incomplete['r02-location:103']
        with self.assertRaisesRegex(ValueError, 'Complete'):
            self.compile(original, incomplete)

    def test_runtime_width_and_allocation_failure_are_explicit(self):
        images = self.fixture()
        for ident, value in [('r02-item:9c', 'CANNEDFOOD'),
                             ('r02-ability:40', 'PERFORMANCE'),
                             ('r02-location:2', 'UNDERGROUND BAR')]:
            labels = dict(LABELS, **{ident: value})
            with self.subTest(record=ident), self.assertRaises(ValueError):
                self.compile(images, labels)
        too_large = {ident: ('X' * (8 if ident.startswith('r02-item:') else
                                     8 if ident.startswith('r02-ability:') else 12))
                     for ident in LABELS}
        with self.assertRaisesRegex(ValueError, 'allocations cannot fit'):
            self.compile(images, too_large)

    def test_source_hash_guard_is_not_optional(self):
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            r02_names.export_records(self.fixture())

    def test_joe_combat_and_field_slots_and_class_learning_table(self):
        original = (Path(__file__).resolve().parents[2] / 'alshark' / 'original' /
                    'Alshark (System Disk).hdm')
        if not original.is_file():
            self.skipTest('Original System image is not available')
        system = original.read_bytes()
        joe = 0x1837
        self.assertEqual(system[joe], 7)  # class 7
        self.assertEqual(system[joe+0x15:joe+0x19], bytes.fromhex('1d004463'))
        self.assertEqual(system[joe+0x19], 0x23)  # initial combat ability
        self.assertEqual(system[joe+0x27:joe+0x2d], bytes.fromhex('404142000000'))
        self.assertEqual(system[0x793b:0x793d], (0x79a0).to_bytes(2, 'little'))
        self.assertEqual(system[0x79a0:0x79a4], bytes.fromhex('01ec0424'))
        records = {r['id']: r for r in r02_names.export_records(
            {'System': system, 'Opening': (original.parent / 'Alshark (Opening Disk).hdm').read_bytes()}
        )}
        self.assertEqual(records['r02-ability:23']['source']['text'], '万能ドﾗｲバｰ')
        self.assertEqual(records['r02-ability:24']['source']['text'], '電磁バブﾙ')
