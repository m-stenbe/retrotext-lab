import unittest
from unittest.mock import patch
from pathlib import Path

from profiles.alshark import r03_names


LABELS = {'r03-location:1': 'BRIDGE', 'r03-location:42': 'HOM PORT', 'r03-location:96': 'MINE'}


class R03NameTests(unittest.TestCase):
    def fixture(self):
        system = bytearray(0x1c000)
        for _, a, size, pointers, marker, _ in r03_names._specs():
            raw = marker.encode('ascii') + b'X'*(size-len(marker)-1) + b'\0'
            system[a:a+size] = raw
            for p in pointers:
                system[p:p+2] = (a+r03_names.POINTER_DELTAS.get(p, 0)-r03_names.BASE).to_bytes(2, 'little')
        return {'System': bytes(system), 'Opening': bytes(0x6000)}

    def compile(self, images, labels=LABELS):
        with patch.object(r03_names, 'guard_original'):
            return r03_names.compile_names(images, labels)

    def test_complete_group_aliases_and_patch_confinement(self):
        images = self.fixture()
        result, manifest = self.compile(images)
        self.assertEqual(set(LABELS), r03_names.REQUIRED)
        self.assertEqual(len(result), len(images['System']))
        self.assertEqual(result[0x1055c:0x105a0], images['System'][0x1055c:0x105a0])
        self.assertEqual({r['record'] for r in manifest['records']}, set(LABELS))
        covered = set()
        for patch_range in manifest['patches']:
            covered.update(range(patch_range['offset'], patch_range['offset']+patch_range['size']))
        for i, (old, new) in enumerate(zip(images['System'], result)):
            if old != new:
                self.assertIn(i, covered)
        for record in manifest['records']:
            for p in record['pointers']:
                offset = r03_names.BASE+int.from_bytes(result[p:p+2], 'little')
                self.assertEqual(offset, record['offset']+r03_names.POINTER_DELTAS.get(p, 0))
                text = result[offset:result.index(0, offset)].decode('ascii')
                self.assertEqual(text.lstrip(' >').replace('>', ' '), record['text'])
    def test_original_alias_guards_and_complete_group(self):
        original = self.fixture()
        for p, value in ((0x10494, 0), (0x10200, 0x1146c-r03_names.BASE)):
            images = dict(original)
            data = bytearray(original['System'])
            data[p:p+2] = value.to_bytes(2, 'little')
            images['System'] = bytes(data)
            with self.subTest(pointer=hex(p)), self.assertRaises(ValueError):
                self.compile(images)
        incomplete = dict(LABELS)
        del incomplete['r03-location:96']
        with self.assertRaisesRegex(ValueError, 'Complete'):
            self.compile(original, incomplete)

    def test_runtime_width_and_allocation_failure_are_explicit(self):
        images = self.fixture()
        for ident, value in [('r03-location:42', 'HOM SPACEPORT'),
                             ('r03-location:96', 'ABANDONED MINE')]:
            labels = dict(LABELS, **{ident: value})
            with self.subTest(record=ident), self.assertRaises(ValueError):
                self.compile(images, labels)
        with self.assertRaisesRegex(ValueError, 'allocations cannot fit'):
            self.compile(images, {ident: 'X'*12 for ident in LABELS})

    def test_source_hash_guard_is_not_optional(self):
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            r03_names.export_records(self.fixture())

    def test_original_location_title_pointer_evidence(self):
        original = (Path(__file__).resolve().parents[2] / 'alshark' / 'original' /
                    'Alshark (System Disk).hdm')
        if not original.is_file():
            self.skipTest('Original System image is not available')
        images = {'System': original.read_bytes(), 'Opening':
                  (original.parent / 'Alshark (Opening Disk).hdm').read_bytes()}
        records = {r['id']: r for r in r03_names.export_records(images)}
        self.assertEqual(records['r03-location:42']['source']['offset'], 0x1146c)
        self.assertEqual(records['r03-location:96']['source']['offset'], 0x116fe)
        result, report = r03_names.compile_names(images, LABELS)
        self.assertEqual(len(report['patches']), 6)
        self.assertEqual(len(result), len(images['System']))
        self.assertEqual(result[0x1055c:0x105a0], images['System'][0x1055c:0x105a0])
