import unittest
from pathlib import Path
from unittest.mock import patch

from profiles.alshark import r08_names as names


class R08NameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        original = Path(__file__).resolve().parents[2] / 'alshark' / 'original'
        if not (original / 'Alshark (System Disk).hdm').is_file():
            raise unittest.SkipTest('Original disk images unavailable')
        cls.images = {disk: (original / f'Alshark ({disk} Disk).hdm').read_bytes()
                      for disk in ('System', 'Opening')}

    def test_aliases_pools_and_progression_preservation(self):
        output, report = names.compile_names(self.images, names.EXPECTED)
        source = self.images['System']
        self.assertEqual(len(output), len(source))
        self.assertEqual(output[0x1055c:0x10799], source[0x1055c:0x10799])
        covered = {i for p in report['patches']
                   for i in range(p['offset'], p['offset'] + p['size'])}
        self.assertTrue(all(i in covered for i, (a, b) in enumerate(zip(source, output)) if a != b))
        self.assertEqual(len(report['records']), 7)
        destinations = {}
        for r in report['records']:
            ident = r['record']
            _, _, _, prefix, encoding, _ = names.SPECS[ident]
            raw = names.encode_label(names.EXPECTED[ident], encoding, prefix)
            for p in r['pointers']:
                a = names.BASE + int.from_bytes(output[p:p+2], 'little')
                self.assertEqual(output[a:output.index(0, a)+1], raw)
                destinations[ident] = a

    def test_unknown_alias_and_source_pointer_fail_closed(self):
        for p, target in ((0x10450, 0), (0x10448, 0x1306)):
            source = bytearray(self.images['System'])
            source[p:p+2] = target.to_bytes(2, 'little')
            with self.subTest(pointer=p), patch.object(names, 'guard_original'):
                with self.assertRaisesRegex(ValueError, 'alias'):
                    names.compile_names(dict(self.images, System=bytes(source)), names.EXPECTED)

    def test_partial_or_unreviewed_names_rejected(self):
        for mapping in ({'r08-location:8': 'MARS'}, dict(names.EXPECTED, **{'r08-location:8': 'A DIFFERENT NAME'})):
            with self.subTest(mapping=mapping), self.assertRaises(ValueError):
                names.compile_names(self.images, mapping)
        source = bytearray(self.images['System'])
        source[0x11306] ^= 1
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            names.export_records(dict(self.images, System=bytes(source)))
