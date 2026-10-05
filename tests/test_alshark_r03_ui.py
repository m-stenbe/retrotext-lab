import copy
from pathlib import Path
import unittest

from profiles.alshark.r03_ui import (compile_records, encode_message, export_records,
                                    widen_menus)
ROOT = Path(__file__).resolve().parents[2] / 'alshark/original'


class ServiceLayoutTests(unittest.TestCase):
    def test_single_cell_spaces_and_dynamic_field_guards(self):
        self.assertEqual(encode_message(0x174c3, 'JOE\n'), b'JOE@\0')
        self.assertEqual(encode_message(0x17553, 'TAKE\n         OUT'), b'TAKE@>>>>>>>>>OUT\0')
        with self.assertRaisesRegex(ValueError, 'runtime field'):
            encode_message(0x17553, 'TAKE\nITEM OUT')
        with self.assertRaisesRegex(ValueError, 'fourteen cells'):
            encode_message(0x174c9, 'A'*15)
        with self.assertRaisesRegex(ValueError, 'glyph'):
            encode_message(0x174c9, 'Lowercase')


@unittest.skipUnless((ROOT / 'Alshark (System Disk).hdm').is_file(), 'Original images unavailable')
class ServiceSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.images = {d: (ROOT / f'Alshark ({d} Disk).hdm').read_bytes()
                      for d in ('System', 'Opening')}

    def test_compile_preserves_all_outside_selected_header(self):
        record = export_records(self.images)[0]
        record['target']['inGameEnglish'] = 'JOE\n'
        output, manifest = compile_records(self.images, [record])
        self.assertEqual(output['Opening'], self.images['Opening'])
        self.assertEqual(output['System'][0x174c3:0x174c9], b'JOE@\0\0')
        self.assertEqual(output['System'][:0x174c3], self.images['System'][:0x174c3])
        self.assertEqual(output['System'][0x174c9:], self.images['System'][0x174c9:])
        self.assertEqual(manifest[0]['size'], 6)
        changed = copy.deepcopy(record)
        changed['source']['offset'] += 1
        with self.assertRaisesRegex(ValueError, 'immutable'):
            compile_records(self.images, [changed])

    def test_menu_width_and_highlight_change_together(self):
        opening, system = map(bytearray, (self.images['Opening'], self.images['System']))
        patches = widen_menus(opening, system)
        self.assertEqual(len(patches), 6)
        for disk, result in (('Opening', opening), ('System', system)):
            changes = {i for i, (a,b) in enumerate(zip(self.images[disk], result)) if a != b}
            self.assertEqual(changes, {p['offset'] for p in patches if p['disk'] == disk})
        self.assertEqual((opening[0x4105], system[0xbafc]), (7,14))
        with self.assertRaisesRegex(ValueError, 'geometry'):
            widen_menus(opening, system)

    def test_heavy_item_script_preserves_speaker_and_rejects_bad_layout(self):
        record = export_records(self.images)[-1]
        self.assertEqual(record['id'], 'fixed:System:00209a')
        record['target']['inGameEnglish'] = {'t004': 'HEY! TOO HEAVY\nTO CARRY!'}
        output, manifest = compile_records(self.images, [record])
        self.assertEqual(output['System'][0x209a:0x209f], self.images['System'][0x209a:0x209f])
        self.assertEqual(output['System'][:0x209a], self.images['System'][:0x209a])
        self.assertEqual(output['System'][0x20c8:], self.images['System'][0x20c8:])
        record['target']['inGameEnglish'] = {'t004': 'A'*15}
        with self.assertRaisesRegex(ValueError, 'Dialogue exceeds'):
            compile_records(self.images, [record])
        record['target']['inGameEnglish'] = {'t002': 'NAME'}
        with self.assertRaisesRegex(ValueError, 'exactly text'):
            compile_records(self.images, [record])
