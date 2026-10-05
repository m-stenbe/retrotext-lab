import copy
import unittest

from profiles.alshark.layout import validate_dialogue
from profiles.alshark.localization import composed_dialogue
from profiles.alshark.script import decode_entry, rebuild_entry


class MeteorLayoutTests(unittest.TestCase):
    def fixture(self, caller=b'ABCDEFGHIJKLM#P\x02\x02\x00Z\0', callee=b'AB\0'):
        entries = {}
        for ident, raw in [('051000:030', caller), ('053000:000', callee)]:
            tokens = decode_entry(raw)
            for token in tokens:
                if token['kind'] == 'text':
                    token['translation'] = token['source']
            entries[ident] = {'tokens': tokens}
        return entries

    def test_shared_call_carries_cursor_and_returns_before_caller_continues(self):
        entries = self.fixture()
        before = copy.deepcopy(entries)
        tokens = composed_dialogue('051000:030', entries, set(entries))
        self.assertEqual(''.join(t.get('translation', '') for t in tokens),
                         'ABCDEFGHIJKLMABZ')
        self.assertEqual(entries, before)
        with self.assertRaisesRegex(ValueError, 'exceeds'):
            validate_dialogue(tokens, {})

    def test_callee_clear_is_respected_but_wait_and_delay_do_not_clear(self):
        for callee, fits in [(b'_AB\0', True), (b'0!AB\0', False)]:
            entries = self.fixture(callee=callee)
            tokens = composed_dialogue('051000:030', entries, set(entries))
            if fits:
                validate_dialogue(tokens, {})
            else:
                with self.assertRaisesRegex(ValueError, 'exceeds'):
                    validate_dialogue(tokens, {})

    def test_unselected_or_unreviewed_callee_is_rejected(self):
        entries = self.fixture()
        with self.assertRaisesRegex(ValueError, 'selected adaptation required'):
            composed_dialogue('051000:030', entries, {'051000:030'})
        entries = self.fixture(caller=b'#P\x02\x02\x01\0')
        with self.assertRaisesRegex(ValueError, 'adapter required'):
            composed_dialogue('051000:030', entries, set(entries))

    def test_event_commands_branches_and_shared_call_survive_shorter_text(self):
        raw = (b'#B\x02\x04\x21#S\x01\x04'
               b'4$\x005LONG TEXT0#Z\x02\x01\x2c'
               b'_4$\x105MORE TEXT0?C\x01\x00#P\x02\x02\x00\0')
        tokens = decode_entry(raw)
        for token in tokens:
            if token['kind'] == 'text':
                token['translation'] = 'HI'
        rebuilt = rebuild_entry(raw, tokens)
        immutable = lambda ts: [(t['kind'], t['raw']) for t in ts
                                if t['kind'] not in ('text', 'opaque_tail')]
        self.assertEqual(len(raw), len(rebuilt))
        self.assertEqual(immutable(decode_entry(raw)), immutable(decode_entry(rebuilt)))
