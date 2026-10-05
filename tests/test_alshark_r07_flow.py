import copy
from pathlib import Path
import unittest

from profiles.alshark.r07_flow import (
    route_closure, validate_source, map_inventory, control_edges, CALLS,
)
from profiles.alshark.r06_flow import route_closure as prior_closure
from profiles.alshark.script_tool import export_disk

ORIGINAL = Path(__file__).resolve().parents[2] / 'alshark/original/Alshark (System Disk).hdm'


@unittest.skipUnless(ORIGINAL.is_file(), 'Original System unavailable')
class R07FlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = ORIGINAL.read_bytes()
        cls.entries = {e['id']: e for e in export_disk(cls.system)['entries']}

    def test_connected_closure_includes_optional_paths_and_stops_at_next_debrief(self):
        validate_source(self.entries)
        closure = route_closure(self.entries)
        self.assertEqual(len(closure), 319)
        self.assertTrue(prior_closure(self.entries) <= closure)
        for ident in ('05c000:025', '05c000:029', '05c000:038',
                      '060000:010', '060000:020', '060000:029', '060000:031',
                      '053000:039', '053000:043', '081000:021', '083000:014'):
            self.assertIn(ident, closure)
        for ident in ('05c000:027', '05d000:002', '060000:032', '081000:022'):
            self.assertNotIn(ident, closure)
        self.assertFalse(any(target == '05c000:027' for _, target, _ in
                             control_edges('05c000:009', self.entries)))
        for (caller, raw), target in CALLS.items():
            self.assertIn(('P', target, raw), control_edges(caller, self.entries))

    def test_original_map_roots_and_actual_byuto_return(self):
        maps = map_inventory(self.system)
        self.assertEqual(maps[10]['bounded'], 0)
        self.assertEqual(maps[10]['objects'], ())
        self.assertEqual(maps[10]['triggers'], ())
        self.assertEqual(maps[10]['exits'], ((87,108,47,1,55),(37,49,98,59,126)))
        self.assertEqual(maps[46]['objects'], tuple((i,0) for i in range(10)))
        self.assertEqual({row[3] for row in maps[97]['triggers']}, {21,22,23,29})
        self.assertEqual(maps[46]['exits'], ((53,47,3,99,2),(54,47,3,99,2)))
        # #Q stores its third parameter directly, unlike tile exits.
        self.assertEqual(self.system[0xdb38:0xdb40].hex(), '32e40bc0740ea375')

    def test_source_and_missing_dependency_fail_closed(self):
        changed = copy.deepcopy(self.entries)
        changed['060000:023']['tokens'] = [t for t in changed['060000:023']['tokens']
                                           if t['raw'] != '2353012c']
        with self.assertRaisesRegex(ValueError, 'source command'):
            validate_source(changed)
        del changed['060000:010']
        with self.assertRaisesRegex(ValueError, 'branch target missing'):
            route_closure(changed)
        changed_system = bytearray(self.system)
        changed_system[0x86c00] ^= 1
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            map_inventory(changed_system)

    def test_byuto_enemy_profiles_do_not_trigger_later_karma_literal(self):
        s = self.system
        sprites = set()
        for offset, count in ((0x86c00,16),(0x9c800,16)):
            raw = s[offset:offset+1024]
            table = int.from_bytes(raw[25:27], 'little')
            for index in range(count):
                group = int.from_bytes(raw[table+2*index:table+2*index+2], 'little')
                sprites.update(raw[group+8+11*i] for i in range(raw[group]))
        self.assertEqual(sprites, {0x19,0x1c,0x1d,0x1e,0x80,0x6e})
        for sprite in sprites:
            pointer = 0x11aae+2*(sprite-0x12)
            profile = 0x11800+int.from_bytes(s[pointer:pointer+2], 'little')
            self.assertNotIn(s[profile+12], (8,10))

    def test_shop_labels_keep_original_rectangles_and_commands(self):
        from profiles.alshark.r07_flow import apply_reviewed_menu_widths
        entries = copy.deepcopy(self.entries)
        for ident, text in (('060000:011', 'TOOLS\nLEAVE'),
                            ('060000:015', 'ARMS\nARMOR\nLEAVE')):
            next(t for t in entries[ident]['tokens'] if t['kind']=='text')['translation'] = text
        selected = {'060000:011','060000:015'}
        rebuilt, patches = apply_reviewed_menu_widths(self.system,self.system,entries,selected)
        self.assertEqual(rebuilt,self.system)
        self.assertEqual(patches,[])
        next(t for t in entries['060000:015']['tokens'] if t['kind']=='text')['translation'] = 'WEAPONS\nARMOR\nLEAVE'
        with self.assertRaisesRegex(ValueError,'labels exceed'):
            apply_reviewed_menu_widths(self.system,self.system,entries,selected)
