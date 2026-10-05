import copy
from collections import deque
from pathlib import Path
import unittest

from profiles.alshark.r02_flow import (apply_reviewed_menu_widths,
                                       control_edges, route_closure,
                                       validate_source)
from profiles.alshark.script_tool import export_disk
from profiles.alshark.script import rebuild_entry


ORIGINAL = Path(__file__).resolve().parents[2] / 'alshark' / 'original' / 'Alshark (System Disk).hdm'
DATA = Path(__file__).resolve().parents[2] / 'alshark' / 'original' / 'Alshark (Data Disk).hdm'


@unittest.skipUnless(ORIGINAL.is_file(), 'Original System image is not available')
class R02FlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = ORIGINAL.read_bytes()
        cls.entries = {e['id']: e for e in export_disk(cls.system)['entries']}

    def test_reviewed_source_and_route_edges(self):
        validate_source(self.entries)
        closure = route_closure(self.entries)
        self.assertIn('05a000:039', closure)
        self.assertIn('053000:024', closure)
        self.assertIn('082000:021', closure)
        self.assertIn('082000:022', closure)
        self.assertIn('082000:023', closure)
        self.assertIn('052000:046', closure)
        self.assertIn('052000:047', closure)
        self.assertIn('052000:048', closure)
        self.assertNotIn('082000:228', closure)
        self.assertNotIn('053000:054', closure)
        self.assertEqual({e[1] for e in control_edges('052000:032', self.entries)},
                         {'052000:046', '052000:047', '052000:048'})

    def test_menu_overlay_changes_only_two_reviewed_width_bytes(self):
        entries = copy.deepcopy(self.entries)
        entries['052000:078']['tokens'][0]['translation'] = 'ARMS\nARMOR\nEXIT'
        entries['052000:080']['tokens'][0]['translation'] = 'BOOZE\nJUICE\nMILK'
        patched, manifest = apply_reviewed_menu_widths(
            self.system, self.system, entries, {'052000:078', '052000:080'})
        self.assertEqual(len(manifest), 2)
        changed = {i for i, (a, b) in enumerate(zip(self.system, patched)) if a != b}
        self.assertEqual(changed, {m['offset'] for m in manifest})
        self.assertEqual({m['before'] for m in manifest}, {'04'})
        self.assertEqual({m['after'] for m in manifest}, {'05'})
        self.assertEqual({tuple(m['choices']) for m in manifest},
                         {('052000:027', '052000:030', '052000:028'),
                          ('052000:051', '052000:052', '052000:053')})

    def test_menu_overlay_rejects_unreviewed_label_or_changed_command(self):
        entries = copy.deepcopy(self.entries)
        entries['052000:078']['tokens'][0]['translation'] = 'WEAPONS\nARMOR\nEXIT'
        with self.assertRaisesRegex(ValueError, 'exceed reviewed'):
            apply_reviewed_menu_widths(self.system, self.system, entries, {'052000:078'})
        entries['052000:078']['tokens'][0]['translation'] = 'ARMS\nARMOR\nEXIT'
        good, manifest = apply_reviewed_menu_widths(
            self.system, self.system, entries, {'052000:078'})
        with self.assertRaisesRegex(ValueError, 'source/output guard'):
            apply_reviewed_menu_widths(self.system, good, entries, {'052000:078'})
        self.assertEqual(len(manifest), 1)

    def test_menu_width_follows_rebuilt_command_after_shorter_text(self):
        entries = copy.deepcopy(self.entries)
        entries['052000:080']['tokens'][0]['translation'] = 'BOOZE\nJUICE\nMILK'
        source = entries['052000:025']
        before = self.system[source['offset']:source['offset'] + source['size']]
        changed_tokens = copy.deepcopy(source['tokens'])
        first_text = next(t for t in changed_tokens if t['kind'] == 'text')
        first_text['translation'] = 'BAR'
        after = rebuild_entry(before, changed_tokens)
        rebuilt = bytearray(self.system)
        rebuilt[source['offset']:source['offset'] + source['size']] = after
        patched, manifest = apply_reviewed_menu_widths(
            self.system, bytes(rebuilt), entries, {'052000:080'})
        self.assertEqual(len(manifest), 1)
        self.assertEqual(manifest[0]['offset'], source['offset'] + after.index(bytes.fromhex('3f4e06040350333435')) + 3)
        self.assertEqual({i for i, (a, b) in enumerate(zip(rebuilt, patched)) if a != b},
                         {manifest[0]['offset']})

    def test_unchanged_width_menu_still_checks_label_geometry(self):
        entries = copy.deepcopy(self.entries)
        entries['052000:079']['tokens'][0]['translation'] = 'TOOLS\nEXIT'
        patched, manifest = apply_reviewed_menu_widths(
            self.system, self.system, entries, {'052000:079'})
        self.assertEqual(patched, self.system)
        self.assertEqual(manifest, [])
        entries['052000:079']['tokens'][0]['translation'] = 'TOOLKIT\nEXIT'
        with self.assertRaisesRegex(ValueError, 'exceed reviewed'):
            apply_reviewed_menu_widths(self.system, self.system, entries, {'052000:079'})

    @unittest.skipUnless(DATA.is_file(), 'Original Data image is not available')
    def test_hamack_bar_isolated_by_blocking_zero_tiles(self):
        grid_desc = self.system[0x4779 + 8:0x4779 + 12]
        self.assertEqual(grid_desc, bytes.fromhex('01580104'))
        grid = self.system[0xb0000:0xb1000]
        attribute_desc = self.system[0x3f39 + 12*0x10 + 8:0x3f39 + 12*0x10 + 12]
        self.assertEqual(attribute_desc, bytes.fromhex('02260201'))
        self.assertEqual(DATA.read_bytes()[0x4c400] & 0xf0, 0x10)
        # Include every nonzero tile, even any that collision also blocks.
        todo = deque([(13, 1)])
        reached = {(13, 1)}
        while todo:
            x, y = todo.popleft()
            for u, v in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if (0 <= u < 64 and 0 <= v < 64 and
                    grid[v*64+u] != 0 and (u, v) not in reached):
                    reached.add((u, v))
                    todo.append((u, v))
        self.assertEqual(len(reached), 322)
        self.assertEqual(max(x for x, _ in reached), 17)
        self.assertNotIn((33, 1), reached)  # Saibal entrance
        self.assertNotIn((49, 1), reached)  # Kainan entrance
        meta = self.system[0x84c00:0x85400]
        start = int.from_bytes(meta[15:17], 'little')
        local = []
        for n in range(meta[start]):
            obj = meta[start + 1 + 18*n:start + 1 + 18*(n+1)]
            if (obj[8]//2, obj[9]//2) in reached:
                local.append(obj[12])
        self.assertEqual(local, list(range(1, 13)))


if __name__ == '__main__':
    unittest.main()
