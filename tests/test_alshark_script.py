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
        for raw in [b'!HELLO\0', b'#N\x03\0', b'$', b'\x81', b'HELLO']:
            with self.subTest(raw=raw), self.assertRaises(Unsupported):
                decode_entry(raw)

    def test_overflow_and_command_injection_rejected(self):
        raw = b'5HI0\0'
        for translation in ['TOO LONG', '#N', '$', 'lowercase', '\r', '0']:
            tokens = decode_entry(raw)
            tokens[1]['translation'] = translation
            with self.subTest(translation=translation), self.assertRaises(ValueError):
                rebuild_entry(raw, tokens)

    def test_wrong_disk_rejected(self):
        with self.assertRaisesRegex(ValueError, 'SHA-256'):
            export_disk(b'not the supported image')
