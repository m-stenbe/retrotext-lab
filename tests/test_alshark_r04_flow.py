import copy
from pathlib import Path
import unittest
from profiles.alshark.r04_flow import (control_edges, map_inventory, route_closure,
                                      selected_text_dependencies, validate_source)
from profiles.alshark.script_tool import export_disk

ORIGINAL = Path(__file__).resolve().parents[2] / 'alshark/original/Alshark (System Disk).hdm'


@unittest.skipUnless(ORIGINAL.is_file(), 'Original System image unavailable')
class R04FlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = ORIGINAL.read_bytes()
        cls.entries = {e['id']:e for e in export_disk(cls.system)['entries']}

    def test_counted_tour_flags_reach_summons(self):
        for ident in ('05c000:007','05c000:012','05c000:022','05c000:023'):
            self.assertIn(('A','05c000:014','2341042324250e'),
                          control_edges(ident,self.entries))
        changed=copy.deepcopy(self.entries)
        token=next(t for t in changed['05c000:007']['tokens'] if t['raw']=='2341042324250e')
        token['raw']='2341042324290e'
        self.assertFalse(any(e[0]=='A' for e in control_edges('05c000:007',changed)))

    def test_bounded_closure_and_later_exclusions(self):
        validate_source(self.entries)
        closure=route_closure(self.entries)
        self.assertEqual(len(closure),85)
        self.assertEqual(len(selected_text_dependencies(self.entries,())),67)
        for ident in ('055000:004','05c000:014','05d000:000','07d000:031',
                      '081000:000','081000:001','081000:002','082000:003'):
            self.assertIn(ident,closure)
        for ident in ('05c000:025','05c000:027','05c000:031','05c000:039',
                      '05c000:046','083000:013'):
            self.assertNotIn(ident,closure)

    def test_progression_and_source_hash_guards(self):
        entries=copy.deepcopy(self.entries)
        token=next(t for t in entries['05d000:000']['tokens'] if t['raw']=='23530116')
        token['raw']='23530117'
        with self.assertRaisesRegex(ValueError,'source command'):
            validate_source(entries)
        del entries['05c000:014']
        with self.assertRaisesRegex(ValueError,'branch target missing'):
            route_closure(entries)
        changed=bytearray(self.system);changed[0x9e400]^=1
        with self.assertRaisesRegex(ValueError,'hash mismatch'):
            map_inventory(changed)

    def test_original_map_roots_and_later_visibility(self):
        maps=map_inventory(self.system)
        self.assertEqual(maps[104]['bank'],'055000')
        self.assertEqual(maps[104]['triggers'],
                         ((52,24,6,1,0),(52,32,5,2,0),(52,40,4,3,1),(52,48,12,0,1)))
        self.assertEqual(maps[30]['bank'],'05c000')
        self.assertEqual(maps[30]['triggers'],((9,10,10,1,0),))
        self.assertEqual(maps[30]['objects'][-3:],((46,0x5d),)*3)
        self.assertEqual(maps[30]['exits'],())
