import copy
from pathlib import Path
import unittest

from profiles.alshark import r09_flow as flow
from profiles.alshark.r08_flow import route_closure as prior_closure
from profiles.alshark.script_tool import export_disk

ORIGINAL = Path(__file__).resolve().parents[2] / 'alshark/original/Alshark (System Disk).hdm'


@unittest.skipUnless(ORIGINAL.is_file(), 'Original System unavailable')
class R09FlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = ORIGINAL.read_bytes()
        cls.entries = {e['id']: e for e in export_disk(cls.system)['entries']}

    def test_reunion_historian_and_new_party_closure(self):
        flow.validate_source(self.entries)
        closure = flow.route_closure(self.entries)
        self.assertEqual(len(closure), 546)
        self.assertTrue(prior_closure(self.entries) <= closure)
        for ident in ('062000:009', '062000:010', '062000:016',
                      '063000:019', '063000:022', '063000:024', '063000:025',
                      '05f000:085', '082000:005', '081000:031', '080000:003'):
            self.assertIn(ident, closure)
        self.assertIn(('C', '063000:025', '23430301a619'),
                      flow.control_edges('063000:004', self.entries))
        self.assertNotIn('080000:004', closure)
        self.assertEqual(len([i for i in closure-prior_closure(self.entries)
                              if any(t['kind']=='text' for t in self.entries[i]['tokens'])]),29)

    def test_map_roots_and_escape_boundary(self):
        maps = flow.map_inventory(self.system)
        self.assertEqual(maps[71]['bank'], '062000')
        self.assertEqual({r[0] for r in maps[71]['objects']}, set(range(9)))
        self.assertEqual(maps[71]['border'], (9, 165, 67))
        self.assertFalse(maps[71]['exits'])
        self.assertFalse(maps[71]['triggers'])

    def test_source_and_missing_dependencies_fail_closed(self):
        entries = copy.deepcopy(self.entries)
        entries['062000:009']['tokens'] = [t for t in entries['062000:009']['tokens']
                                           if t['raw'] != '2357010a']
        with self.assertRaisesRegex(ValueError, 'source command'):
            flow.validate_source(entries)
        del entries['063000:024']
        with self.assertRaisesRegex(ValueError, 'branch target missing'):
            flow.route_closure(entries)

    def test_shop_menu_preserves_rectangle(self):
        entries = copy.deepcopy(self.entries)
        token = next(t for t in entries['062000:013']['tokens'] if t['kind']=='text')
        token['translation'] = 'TOOLS\nEXIT'
        rebuilt, patches = flow.apply_reviewed_menu_widths(self.system, self.system, entries, {'062000:013'})
        self.assertEqual(rebuilt, self.system)
        self.assertFalse(patches)
        token['translation'] = 'BUY TOOLS\nEXIT'
        with self.assertRaisesRegex(ValueError, 'labels exceed'):
            flow.apply_reviewed_menu_widths(self.system, self.system, entries, {'062000:013'})

    def test_recruitment_selector_maps_to_lucia_talk(self):
        # The selector is 0a; its party actor ID is 7, not 0a.
        self.assertIn(bytes.fromhex('5773d8'), self.system[0x33eb:0x3450])
        self.assertEqual(self.system[0xd873:0xd87c], bytes.fromhex('ac5756e8be32e85a29'))
        self.assertEqual(self.system[0xb71:0xb7a], bytes.fromhex('b4073c0abee7197441'))
        self.assertEqual(self.system[0xbd7:0xbd9], bytes.fromhex('8825'))
        self.assertEqual(self.system[0xb43d+7], 5)
