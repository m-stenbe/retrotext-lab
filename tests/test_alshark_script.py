import copy
import unittest
from profiles.alshark.script import Unsupported, decode_entry, rebuild_entry
from profiles.alshark.script_tool import export_disk


class ScriptTests(unittest.TestCase):
    def test_zero_in_arguments_and_name_is_not_terminator(self):
        raw = b'#N\x02\x00\x044$\x005HELLO0\x00'
        tokens = decode_entry(raw)
        self.assertEqual([t['kind'] for t in tokens],
                         ['command', 'control', 'name', 'control', 'text', 'control', 'end'])
        self.assertEqual(tokens[2]['id'], 't002')
        self.assertEqual(tokens[2]['name_id'], 0)
        self.assertEqual(rebuild_entry(raw, tokens), raw)

    def test_cp932_trail_command_byte_and_noncanonical_mapping(self):
        # 0x40 is @ as an opcode, but a CP932 trail here. Preserve raw source.
        raw = b'5\x81\x40\x81\x60@' + 'テスト'.encode('cp932') + b'0\0'
        tokens = decode_entry(raw)
        self.assertEqual(tokens[1]['source'], '\u3000\uff5e\nテスト')
        self.assertEqual(rebuild_entry(raw, tokens), raw)

    def test_shorter_text_preserves_opaque_tail_position(self):
        raw = b'5LONG TEXT0\0\xe5\x00\x05'
        tokens = decode_entry(raw)
        tokens[1]['translation'] = 'HI'
        result = rebuild_entry(raw, tokens)
        self.assertEqual(len(result), len(raw))
        self.assertEqual(result[:5], b'5HI0\0')
        self.assertEqual(result[-3:], raw[-3:])

    def test_command_and_source_changes_rejected(self):
        raw = b'#N\x01\x015HELLO0\0'
        original = decode_entry(raw)
        for key, value in [('raw', '00'), ('source', 'OTHER')]:
            tokens = copy.deepcopy(original)
            tokens[2][key] = value
            with self.assertRaises(ValueError):
                rebuild_entry(raw, tokens)
        tokens = copy.deepcopy(original)
        tokens[0]['raw'] = '234e0100'
        with self.assertRaises(ValueError):
            rebuild_entry(raw, tokens)

    def test_unknown_truncated_and_unterminated_entries_rejected(self):
        for raw in [b';HELLO\0', b'#N\x03\0', b'$', b'\x81', b'HELLO']:
            with self.subTest(raw=raw), self.assertRaises(Unsupported):
                decode_entry(raw)

    def test_overflow_and_command_injection_rejected(self):
        raw = b'5HI0\0'
        for translation in ['TOO LONG', '#N', '$', 'lowercase', '\r', '@']:
            tokens = decode_entry(raw)
            tokens[1]['translation'] = translation
            with self.subTest(translation=translation), self.assertRaises(ValueError):
                rebuild_entry(raw, tokens)

    def test_wrong_disk_rejected(self):
        with self.assertRaisesRegex(ValueError, 'SHA-256'):
            export_disk(b'not the supported image')

    def test_display_controls_do_not_consume_following_text(self):
        raw = b'1236!>/HELLO0\0'
        tokens = decode_entry(raw)
        self.assertEqual([t['raw'] for t in tokens[:7]],
                         [bytes([c]).hex() for c in b'1236!>/'])
        self.assertEqual(tokens[7]['source'], 'HELLO')
        self.assertEqual(rebuild_entry(raw, tokens), raw)

    def test_display_arguments_can_be_zero_or_command_bytes(self):
        raw = b'(\0=\x23HELLO\0'
        tokens = decode_entry(raw)
        self.assertEqual([t['kind'] for t in tokens],
                         ['display_argument', 'display_argument', 'text', 'end'])
        self.assertEqual(rebuild_entry(raw, tokens), raw)
        for raw in (b'(', b'='):
            with self.assertRaises(Unsupported):
                decode_entry(raw)


class ImportTests(unittest.TestCase):
    def setUp(self):
        import struct
        from unittest.mock import patch
        from profiles.alshark.script import digest
        from profiles.alshark.script_tool import export_disk
        data = bytearray(0x84000)
        base = 0x51000
        struct.pack_into('<3H', data, base, 6, 32, 60)
        for offset, raw in [(6, b'5HELLO WORLD0\0'),
                            (32, b'#B\x02\x02\x0e5HELLO WORLD0\0'),
                            (60, b'5READ ONLY0\0')]:
            data[base+offset:base+offset+len(raw)] = raw
        self.data = bytes(data)
        # Synthetic fixture only: production still requires the original disk hash.
        self.supported = patch('profiles.alshark.script_tool.SYSTEM_HASH', digest(self.data))
        self.supported.start()
        self.addCleanup(self.supported.stop)
        self.document = export_disk(self.data)

    def test_roundtrip_and_second_entry_branch_preservation(self):
        from profiles.alshark.script_tool import import_disk
        self.assertEqual(import_disk(self.data, self.document), self.data)
        entry = self.document['entries'][1]
        self.assertTrue(entry['editable'])
        next(t for t in entry['tokens'] if t['kind']=='text')['translation'] = 'HI'
        rebuilt = import_disk(self.data, self.document)
        a, n = entry['offset'], entry['size']
        self.assertEqual(rebuilt[:a], self.data[:a])
        self.assertEqual(rebuilt[a+n:], self.data[a+n:])
        self.assertEqual(rebuilt[a:a+5], b'#B\x02\x02\x0e')

    def test_read_only_and_metadata_tampering_rejected(self):
        from profiles.alshark.script_tool import import_disk
        for mutate in (
            lambda d: d['entries'][2]['tokens'][1].update(translation='HI'),
            lambda d: d['entries'][2].update(editable=True),
            lambda d: d['entries'][1].update(offset=1),
            lambda d: d.update(format='retrotext-alshark-v1'),
        ):
            document = copy.deepcopy(self.document)
            mutate(document)
            with self.assertRaises(ValueError):
                import_disk(self.data, document)


class DigitTests(unittest.TestCase):
    def test_digits_are_glyphs_not_script_opcodes(self):
        from profiles.alshark.script import encode_translation
        encoded = encode_translation('80')
        self.assertEqual(encoded, '８０'.encode('cp932'))
        tokens = decode_entry(encoded + b'\0')
        self.assertEqual(tokens[0]['kind'], 'text')
        self.assertEqual(tokens[0]['source'], '８０')
