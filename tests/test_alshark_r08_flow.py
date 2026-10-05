import copy
from pathlib import Path
import unittest

from profiles.alshark.r08_flow import (
    route_closure, validate_source, map_inventory, control_edges, CALLS,
    apply_reviewed_menu_widths, MENUS,
)
from profiles.alshark.r07_flow import route_closure as prior_closure
from profiles.alshark.script_tool import export_disk

ORIGINAL = Path(__file__).resolve().parents[2] / 'alshark/original/Alshark (System Disk).hdm'


@unittest.skipUnless(ORIGINAL.is_file(), 'Original System unavailable')
class R08FlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = ORIGINAL.read_bytes()
        cls.entries = {e['id']: e for e in export_disk(cls.system)['entries']}

    def test_full_connected_closure_retains_rooms_and_current_item_state(self):
        validate_source(self.entries)
        closure = route_closure(self.entries)
        self.assertEqual(len(closure), 506)
        self.assertTrue(prior_closure(self.entries) <= closure)
        for ident in ('05d000:002','05c000:034','05f000:059','057000:058',
                      '053000:056','061000:017','061000:016','063000:018',
                      '078000:001','081000:025','081000:028'):
            self.assertIn(ident, closure)
        for ident in ('062000:000','063000:019','063000:022','063000:025','081000:029'):
            self.assertNotIn(ident, closure)
        self.assertFalse(any(target=='063000:025' for _,target,_ in
                             control_edges('063000:004',self.entries)))
        for (caller,raw),target in CALLS.items():
            self.assertIn(('P',target,raw),control_edges(caller,self.entries))
        # Receiving the letter enables Talk's script, then a new party state.
        self.assertIn(('B','082000:055','2342023037'),control_edges('082000:000',self.entries))
        self.assertIn(('P','081000:025','2350023019'),control_edges('082000:055',self.entries))

    def test_original_map_roots_and_optional_mainland(self):
        maps = map_inventory(self.system)
        self.assertEqual(maps[8]['bounded'],0)
        self.assertEqual(maps[8]['objects'],())
        self.assertEqual(maps[8]['triggers'],())
        self.assertEqual({row[2]-1 for row in maps[8]['exits']},{40,73,71,61})
        self.assertEqual({row[0] for row in maps[73]['objects']},set(range(13))|set(range(14,33)))
        self.assertEqual({row[3] for row in maps[61]['triggers']},{14,15,16,17})
        self.assertEqual({row[0] for row in maps[3]['objects']},set(range(13)))

    def test_source_and_missing_dependency_fail_closed(self):
        changed = copy.deepcopy(self.entries)
        changed['063000:004']['tokens'] = [t for t in changed['063000:004']['tokens']
                                          if t['raw']!='23430301a619']
        with self.assertRaisesRegex(ValueError,'source command'):
            validate_source(changed)
        del changed['053000:056']
        with self.assertRaisesRegex(ValueError,'branch target missing'):
            route_closure(changed)
        system = bytearray(self.system);system[0x86400]^=1
        with self.assertRaisesRegex(ValueError,'hash mismatch'):
            map_inventory(system)

    def test_mars_profiles_exclude_later_karma_literal(self):
        s = self.system;r=s[0x86400:0x86800]
        table=int.from_bytes(r[25:27],'little');sprites=set()
        for index in range(16):
            group=int.from_bytes(r[table+2*index:table+2*index+2],'little')
            sprites.update(r[group+8+11*n] for n in range(r[group]))
        self.assertEqual(sprites,{0x1e,0x1f,0x20,0x21})
        for sprite in sprites:
            pointer=0x11aae+2*(sprite-0x12)
            profile=0x11800+int.from_bytes(s[pointer:pointer+2],'little')
            self.assertNotIn(s[profile+12],(8,10))

    def test_all_new_menu_rectangles_and_unchanged_command_bytes(self):
        entries=copy.deepcopy(self.entries);selected=set()
        for source,label,command,width,rows in MENUS:
            next(t for t in entries[label]['tokens'] if t['kind']=='text')['translation']='\n'.join(['X'*width]*rows)
            selected.add(label)
        rebuilt,patches=apply_reviewed_menu_widths(self.system,self.system,entries,selected)
        self.assertEqual(rebuilt,self.system);self.assertEqual(patches,[])
        next(t for t in entries['057000:051']['tokens'] if t['kind']=='text')['translation']='TURRETS\nMISSILES\nEXIT'
        with self.assertRaisesRegex(ValueError,'labels exceed'):
            apply_reviewed_menu_widths(self.system,self.system,entries,selected)
