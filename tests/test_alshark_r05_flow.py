import copy
from pathlib import Path
import unittest
from profiles.alshark.r05_flow import (route_closure, selected_text_dependencies,
    validate_source, map_inventory, CALLS, control_edges)
from profiles.alshark.script_tool import export_disk

ORIGINAL = Path(__file__).resolve().parents[2] / 'alshark/original/Alshark (System Disk).hdm'

@unittest.skipUnless(ORIGINAL.is_file(), 'Original System unavailable')
class R05FlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = ORIGINAL.read_bytes()
        cls.entries = {e['id']:e for e in export_disk(cls.system)['entries']}

    def test_closure_retains_full_services_and_excludes_pursuit(self):
        validate_source(self.entries)
        closure = route_closure(self.entries)
        self.assertEqual(len(closure),168)
        for ident in ('05b000:035','05b000:022','05a000:018','05a000:038',
                      '05f000:014','05f000:050','05f000:057','081000:007'):
            self.assertIn(ident,closure)
        for ident in ('05a000:014','05a000:017','05b000:036','05b000:039',
                      '053000:054','05f000:088'):
            self.assertNotIn(ident,closure)
        for (caller,raw),target in CALLS.items():
            self.assertIn(('P',target,raw),control_edges(caller,self.entries))

    def test_original_map_roots_and_wrapping_surface(self):
        maps=map_inventory(self.system)
        self.assertEqual(maps[9]['bounded'],0)
        self.assertEqual(maps[9]['objects'],())
        self.assertEqual(maps[9]['triggers'],())
        self.assertEqual(maps[9]['exits'],((50,28,42,17,62),(55,34,54,31,126),(111,118,51,31,62)))
        self.assertEqual(maps[53]['bank'],'05b000')
        self.assertEqual(maps[50]['objects'][12],(14,0x43))
        self.assertEqual(maps[41]['objects'][-1],(88,0x5d))

    def test_source_mutation_or_missing_branch_rejected(self):
        changed=copy.deepcopy(self.entries)
        changed['05b000:035']['tokens']=[t for t in changed['05b000:035']['tokens'] if t['raw']!='23530118']
        with self.assertRaisesRegex(ValueError,'source command'):
            validate_source(changed)
        del changed['05f000:057']
        with self.assertRaisesRegex(ValueError,'branch target missing'):
            route_closure(changed)
        system=bytearray(self.system);system[0x86800]^=1
        with self.assertRaisesRegex(ValueError,'hash mismatch'):
            map_inventory(system)
