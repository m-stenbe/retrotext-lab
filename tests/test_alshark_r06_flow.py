import copy
from pathlib import Path
import unittest
from profiles.alshark.r06_flow import (route_closure, selected_text_dependencies,
    validate_source, map_inventory, CALLS, control_edges)
from profiles.alshark.script_tool import export_disk

ORIGINAL = Path(__file__).resolve().parents[2] / 'alshark/original/Alshark (System Disk).hdm'

@unittest.skipUnless(ORIGINAL.is_file(), 'Original System unavailable')
class R06FlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = ORIGINAL.read_bytes()
        cls.entries = {e['id']:e for e in export_disk(cls.system)['entries']}

    def test_closure_retains_full_services_and_excludes_pursuit(self):
        validate_source(self.entries)
        closure = route_closure(self.entries)
        self.assertEqual(len(closure),255)
        self.assertIn('05c000:009',closure)
        self.assertIn('2342021a19',[t['raw'] for t in self.entries['05c000:009']['tokens']])
        self.assertFalse(any(target=='05c000:025' for _,target,_ in control_edges('05c000:009',self.entries)))
        for ident in ('05b000:035','05b000:022','05a000:018','05a000:038',
                      '05f000:014','05f000:050','05f000:057','081000:007'):
            self.assertIn(ident,closure)
        for ident in ('05c000:025','05e000:029','053000:054','05f000:088'):
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
        changed['05e000:000']['tokens']=[t for t in changed['05e000:000']['tokens'] if t['raw']!='2353011a']
        with self.assertRaisesRegex(ValueError,'source command'):
            validate_source(changed)
        del changed['05f000:057']
        with self.assertRaisesRegex(ValueError,'branch target missing'):
            route_closure(changed)
        system=bytearray(self.system);system[0x86800]^=1
        with self.assertRaisesRegex(ValueError,'hash mismatch'):
            map_inventory(system)

    def test_current_encounters_cannot_trigger_later_karma_or_boarding_text(self):
        s=self.system
        sprites=set()
        for offset,indices in ((0x86800,range(16)),(0x90c00,range(2)),
                               (0x91800,range(1)),(0x8c000,range(4))):
            raw=s[offset:offset+1024]
            table=int.from_bytes(raw[25:27],'little')
            for index in indices:
                group=int.from_bytes(raw[table+2*index:table+2*index+2],'little')
                sprites.update(raw[group+8+11*i] for i in range(raw[group]))
        self.assertEqual(sprites,{24,25,26,27,109,111,112})
        for sprite in sprites:
            pointer=0x11800+0x2ae+2*(sprite-0x12)
            profile=0x11800+int.from_bytes(s[pointer:pointer+2],'little')
            self.assertNotIn(s[profile+12],(8,10))
        self.assertEqual(s[0x1860f:0x1861a].hex(),'fb1177f08505791089ff07')
        self.assertEqual(s[0x18689+7*8:0x18689+8*8],bytes([16])*8)
        for entity in range(9,26):
            target=int.from_bytes(s[0x19296+2*entity:0x19298+2*entity],'little')
            self.assertEqual(target==0x5c2f,entity==25)
