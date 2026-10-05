import unittest
from pathlib import Path

from profiles.alshark import r03_equipment as names


class R03EquipmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[2] / 'alshark' / 'original'
        if not (root / 'Alshark (System Disk).hdm').is_file():
            raise unittest.SkipTest('Original images unavailable')
        cls.images = {d: (root / f'Alshark ({d} Disk).hdm').read_bytes()
                      for d in ('Opening', 'System')}

    def test_source_alias_suffixes_and_prior_pool_preservation(self):
        records = names.export_records(self.images)
        self.assertEqual(len(records), 220)
        labels = {r['id']: 'TEST' for r in records}
        labels['r03-equipment:ship:05'] = '250MM AP'
        output, report = names.compile_names(self.images, labels)
        source = self.images['System']
        self.assertEqual(len(output), len(source))
        covered = set()
        for row in report['patches']:
            covered.update(range(row['offset'], row['offset']+row['size']))
        self.assertTrue(all(i in covered for i, (a, b) in enumerate(zip(source, output)) if a != b))
        for a, z in names.prior_spans(source):
            self.assertEqual(output[a:z], source[a:z])
        self.assertEqual(output[0x1055c:0x105a0], source[0x1055c:0x105a0])
        for row in report['records']:
            for pointer in row['pointers']:
                dest = names.BASE + int.from_bytes(output[pointer:pointer+2], 'little')
                self.assertEqual(dest, row['offset'])
                self.assertEqual(output[dest:dest+row['used']], names.encode_equipment(row['text']))
        owned = {p for row in report['records'] for p in row['pointers']}
        for pointer in range(names.BASE, names.POINTER_END, 2):
            if pointer in owned:
                continue
            old = names.BASE + int.from_bytes(source[pointer:pointer+2], 'little')
            new = names.BASE + int.from_bytes(output[pointer:pointer+2], 'little')
            self.assertEqual(old, new)
            self.assertEqual(source[old:source.index(0, old)+1],
                             output[new:output.index(0, new)+1])
        # Night Mask and IR Sight share original suffixes with prior R02 names.
        self.assertEqual(output[0x1007a:0x1007c], source[0x1007a:0x1007c])
        self.assertEqual(output[0x10088:0x1008a], source[0x10088:0x1008a])

    def test_unreviewed_alias_and_incomplete_group_rejected(self):
        source = bytearray(self.images['System'])
        source[0x10300:0x10302] = (names.SPECS['r03-equipment:item:01'][0]-names.BASE).to_bytes(2, 'little')
        with self.assertRaisesRegex(ValueError, 'Unreviewed'):
            names.guard_specs(bytes(source))
        with self.assertRaisesRegex(ValueError, 'Complete'):
            names.compile_names(self.images, {})

    def test_source_mutation_and_overflow_rejected(self):
        altered = dict(self.images, System=bytes(len(self.images['System'])))
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            names.export_records(altered)
        for value in ('TOO LONG NAME', 'BETA-ARM', 'beta', ''):
            with self.subTest(value=value), self.assertRaises(ValueError):
                names.encode_equipment(value)
        self.assertEqual(names.encode_equipment('250MM AP'), '２５０'.encode('cp932')+b'MM>AP\0')
