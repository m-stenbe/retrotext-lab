import copy
from pathlib import Path
import unittest

from profiles.alshark.r03_flow import (bridge_menu_path, map_inventory, route_closure,
                                      selected_text_dependencies, validate_source)
from profiles.alshark.script_tool import export_disk

ORIGINAL = Path(__file__).resolve().parents[2] / 'alshark/original/Alshark (System Disk).hdm'


@unittest.skipUnless(ORIGINAL.is_file(), 'Original System image unavailable')
class R03FlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = ORIGINAL.read_bytes()
        cls.entries = {e['id']: e for e in export_disk(cls.system)['entries']}

    def test_complete_bounded_closure(self):
        validate_source(self.entries)
        closure = route_closure(self.entries)
        self.assertEqual(len(closure), 67)
        self.assertEqual(len(selected_text_dependencies(self.entries, ())), 56)
        for ident in ('054000:029', '054000:031', '054000:028', '07d000:034',
                      '082000:024', '083000:001', '083000:004', '083000:005'):
            self.assertIn(ident, closure)
        for ident in ('054000:032', '054000:036', '083000:000', '083000:008', '082000:228'):
            self.assertNotIn(ident, closure)

    def test_guard_rejects_changed_progression_and_missing_target(self):
        entries = copy.deepcopy(self.entries)
        token = next(t for t in entries['054000:031']['tokens'] if t['raw'] == '3f490103')
        token['raw'] = '3f490104'
        with self.assertRaisesRegex(ValueError, 'source command'):
            validate_source(entries)
        del entries['083000:001']
        with self.assertRaisesRegex(ValueError, 'branch target missing'):
            route_closure(entries)

    def test_maps_retain_conditional_objects_and_next_event(self):
        maps = map_inventory(self.system)
        self.assertEqual(maps[42]['bank'], '054000')
        self.assertEqual(maps[42]['objects'][-3:], ((36, 0x5d),)*3)
        self.assertEqual(maps[96]['objects'], ((31, 0xf8),)*2)
        self.assertEqual(maps[96]['triggers'], ((15, 37, 0, 1, 0),))
        self.assertEqual(maps[1]['triggers'], ((16, 21, 0, 0, 0),))
        changed = bytearray(self.system)
        changed[0x8481e] ^= 1
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            map_inventory(changed)

    def test_bridge_downward_doorway_precedes_cockpit(self):
        data = ORIGINAL.with_name('Alshark (Data Disk).hdm').read_bytes()
        proof = bridge_menu_path(self.system, data)
        self.assertEqual(proof['screen_path'], ((38,46),(38,47),(38,48)))
        self.assertEqual(set(proof['collision'].values()), {0})
        self.assertNotEqual(proof['screen_path'][0][0]//2, proof['cockpit_metadata'][0])
