import copy
import unittest
from unittest.mock import patch
from profiles.alshark import names


class NamesTests(unittest.TestCase):
    def fixture(self):
        data = bytearray(0x1C000)
        # Every overwritten allocation is represented by source bytes. These are
        # synthetic names, not original source scripts or copyrighted disk data.
        for a, z, _ in names.SPANS:
            data[a:z] = b'X'*(z-a)
        for ident, (offset, pointers, _) in names.SOURCES.items():
            for p in pointers:
                data[p:p+2] = (offset-names.BASE).to_bytes(2, 'little')
        data[0x10456:0x10458] = bytes.fromhex('2913')
        data[0x10508:0x1050A] = bytes.fromhex('2217')
        return {'System': bytes(data), 'Opening': bytes(0x6000)}

    def compile(self, images, targets=None):
        with patch.object(names, 'guard_original'):
            return names.compile_names(images, names.REQUIRED if targets is None else targets)

    def test_all_aliases_resolve_to_complete_names_and_changes_stay_in_plan(self):
        images = self.fixture()
        result, manifest = self.compile(images)
        covered = set()
        for p in manifest['patches']:
            covered.update(range(p['offset'], p['offset']+p['size']))
        for i, (old, new) in enumerate(zip(images['System'], result)):
            if old != new:
                self.assertIn(i, covered)
        self.assertEqual(len(images['System']), len(result))
        self.assertEqual({r['record'] for r in manifest['records']}, set(names.REQUIRED))
        for record in manifest['records']:
            for p in record['pointers']:
                offset = names.BASE+int.from_bytes(result[p:p+2], 'little')
                self.assertEqual(offset, record['offset'])
                raw = result[offset:result.index(0, offset)]
                if record['encoding'] == 'wide':
                    decoded = ''.join(chr(ord(c)-0xFEE0) for c in raw.decode('cp932'))
                    self.assertEqual(decoded, record['text'])
                else:
                    self.assertEqual(raw.decode('ascii').lstrip(' >').replace('>', ' '), record['text'])
        # Full-width dialogue names remain full-width even though menu names use ASCII.
        for record in manifest['records']:
            if record['record'].startswith('name:') and record['record'] != 'name:81':
                self.assertEqual(record['encoding'], 'wide')

    def test_requires_whole_group_and_consistent_reviewed_spellings(self):
        for mode in ('missing', 'renamed', 'alias'):
            targets = dict(names.REQUIRED)
            if mode == 'missing': targets.pop('name:13')
            if mode == 'renamed': targets['item-name:shirt'] = 'OTHER'
            if mode == 'alias': targets['name:1'] = 'OTHER'
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.compile(self.fixture(), targets)

    def test_unknown_pointer_alias_and_changed_item_pointer_rejected(self):
        for p in (0x10200, 0x100B8):
            images = self.fixture()
            data = bytearray(images['System'])
            data[p:p+2] = (0x111DB-names.BASE).to_bytes(2, 'little')
            images['System'] = bytes(data)
            before = copy.deepcopy(images)
            with self.assertRaises(ValueError):
                self.compile(images)
            self.assertEqual(images, before)

    def test_control_injection_and_unreviewed_glyphs_rejected(self):
        for text in ('A@B', 'A>B', 'A/B', 'A\0B', 'lower', '123', 'A'*13):
            with self.subTest(text=text), self.assertRaises(ValueError):
                names.encode_label(text, 'ascii')

    def test_original_hash_guard_is_mandatory(self):
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            names.compile_names(self.fixture(), names.REQUIRED)

    def test_ability_width_guard_survives_reviewed_spelling_updates(self):
        # The runtime learned-ability field reserves eight full cells. Updating
        # the reviewed spellings must not bypass that independent display bound:
        # a 9-character label can fit storage yet collide in a composed message.
        images = self.fixture()
        for text in ('MINDSTORM', 'TELEKINESIS'):
            targets = dict(names.REQUIRED, **{'ability-name:13': text})
            with self.subTest(text=text), patch.object(names, 'REQUIRED', targets):
                with self.assertRaisesRegex(ValueError, '(?i)ability|width'):
                    self.compile(images, targets)

    def test_compiled_ability_names_fit_the_runtime_field(self):
        _, manifest = self.compile(self.fixture())
        abilities = [r for r in manifest['records']
                     if r['record'].startswith('ability-name:')]
        self.assertEqual(len(abilities), len(names.ABILITIES))
        for record in abilities:
            with self.subTest(record=record['record']):
                self.assertLessEqual(len(record['text']), 8)


class PlaytestSpacingTests(unittest.TestCase):
    def test_title_padding_and_internal_spaces_fit_twelve_cells(self):
        # Expected physical positions from the native space/skip handlers;
        # these are the three screenshot overflows and off-center JOE.
        for text, prefix, left, end in [
            ('PLANET HOM', '  ', 1, 11),
            ('SAXEN CANYON', '>', 0, 12),
            ('BASEMENT BAR', '  ', 0, 12),
            ('JOE', ' >', 4, 7),
        ]:
            with self.subTest(text=text):
                raw = names.encode_label(text, 'ascii', prefix)[:-1]
                column = 0
                positions = []
                for byte in raw:
                    if byte == 0x20:
                        column += 2
                    elif byte == 0x3e:
                        column += 1
                    else:
                        positions.append(column)
                        column += 1
                self.assertEqual(positions[0], left)
                self.assertEqual(column, end)
                self.assertLessEqual(column, 12)

    def test_narrow_item_name_spaces_are_single_cell(self):
        self.assertEqual(names.encode_label('CAMP KIT', 'ascii'), b'CAMP>KIT\0')
        self.assertEqual(names.encode_label('SUBM GUN', 'ascii'), b'SUBM>GUN\0')
