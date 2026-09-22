import unittest

from profiles.alshark.audit_labels import audit, read_menu
from profiles.alshark.menu_patch import encode_ui


class LabelAuditTests(unittest.TestCase):
    def test_reads_effective_pointer_instead_of_abandoned_short_string(self):
        data = bytearray(0x6000)
        data[0x3fd9:0x3fdf] = bytes.fromhex('09 02 04 0f 00 2c')
        data[0x4158:0x415c] = b'OLD\0'
        text = encode_ui('ABILITIES\nEQUIPMENT') + b'\0'
        data[0x4c00:0x4c00+len(text)] = text
        menu = read_menu(data, 0x3fd9)
        self.assertEqual(menu['text'], 'ABILITIES\nEQUIPMENT')
        self.assertEqual((menu['columns'], menu['rows']), (9, 2))
        self.assertEqual(menu['address'], 0x4c00)

    def test_rejects_menu_pointer_outside_loaded_driver(self):
        data = bytearray(0x6000)
        data[0x3fd9:0x3fdf] = bytes.fromhex('06 02 04 0f ff ff')
        with self.assertRaises(ValueError):
            read_menu(data, 0x3fd9)

    def test_build_hash_mismatch_blocks_audit_before_catalog_use(self):
        manifest = {'disks': [dict(name='Alshark (Opening Disk).hdm',
                                  patched_sha256='incorrect', source_sha256='incorrect')]}
        with self.assertRaisesRegex(ValueError, 'differs from its patch manifest'):
            audit({'Opening': b'original'}, {'Opening': b'changed'}, manifest, {})
