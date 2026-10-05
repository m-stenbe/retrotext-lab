import unittest
from profiles.alshark.cinematic import decode_stream, encode_text, fit_tokens


class CinematicTests(unittest.TestCase):
    def test_animation_operands_are_not_terminators_and_latin_is_not_a_trigger(self):
        raw = b'#MA\x01\x02\0,A' + '猫'.encode('cp932') + b'!#L\x00_\x00\0'
        tokens, used = decode_stream(raw)
        self.assertEqual(used, len(raw))
        texts = [t for t in tokens if t['kind'] == 'text']
        result = fit_tokens(tokens, {texts[0]['id']: 'A CAT!'})
        self.assertIn('Ａ'.encode('cp932'), result)
        immutable = lambda ts: [t['raw'] for t in ts if t['kind'] != 'text']
        self.assertEqual(immutable(tokens), immutable(decode_stream(result)[0]))

    def test_rejects_unknown_commands_truncation_and_literal_ascii(self):
        for raw in (b'#Q\0', b'#M', b'#MA\x01', b'#L', b'\x82', b'A\0'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                decode_stream(raw)
        for text in ('@', '#', '\n', '_', '/', '\0'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                encode_text(text)

    def test_row_wrap_and_explicit_newline_cannot_erase_page(self):
        tokens, _ = decode_stream('猫'.encode('cp932') + b'@!\0')
        ident = tokens[0]['id']
        fit_tokens(tokens, {ident: ' '*99})
        for length in (100, 125):
            with self.assertRaisesRegex(ValueError, 'auto-clear'):
                fit_tokens(tokens, {ident: ' '*length})
        tokens, _ = decode_stream('猫'.encode('cp932') + b'_\0' + '犬'.encode('cp932') + b'\0')
        fit_tokens(tokens, {t['id']: ' '*124 for t in tokens if t['kind'] == 'text'})

    def test_delay_does_not_clear_and_all_translations_are_required(self):
        tokens, _ = decode_stream('猫'.encode('cp932') + b'!' + '犬'.encode('cp932') + b'\0')
        ids = [t['id'] for t in tokens if t['kind'] == 'text']
        with self.assertRaisesRegex(ValueError, 'auto-clear'):
            fit_tokens(tokens, {ids[0]: ' '*124, ids[1]: 'B'})
        for adaptation in ({}, {ids[0]: 'A'}, {ids[0]: 'A', ids[1]: 'B', 'extra': 'C'}):
            with self.assertRaises(ValueError):
                fit_tokens(tokens, adaptation)

    def test_spacing_between_sound_effects_is_preserved(self):
        tokens, _ = decode_stream(b'#Z\x1b     #Z\x1b  \0')
        translations = {t['id']: t['text'] for t in tokens if t['kind'] == 'text'}
        self.assertEqual(fit_tokens(tokens, translations), b'#Z\x1b     #Z\x1b  \0')
        translations[next(iter(translations))] = ''
        with self.assertRaisesRegex(ValueError, 'timing spaces'):
            fit_tokens(tokens, translations)

    def test_word_wrap_is_checked_across_delays_and_text_spans(self):
        tokens, _ = decode_stream('猫'.encode('cp932') + b'!' + '犬'.encode('cp932') + b'\0')
        first, second = [t['id'] for t in tokens if t['kind'] == 'text']
        with self.assertRaisesRegex(ValueError, 'inside a word'):
            fit_tokens(tokens, {first: "The spacecraft's ramp ope", second: 'ned silently.'})
        fit_tokens(tokens, {first: "The spacecraft's ramp    ", second: 'opened silently.'})

    def test_screenshot_word_breaks_are_rejected_without_changing_controls(self):
        tokens, _ = decode_stream('猫'.encode('cp932') + b'\0')
        ident = tokens[0]['id']
        for text in ("The spacecraft's ramp opened silently.",
                     "Sion! They've captured our fathers!"):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'inside a word'):
                fit_tokens(tokens, {ident: text})
        encoded = fit_tokens(tokens, {ident: "Sion! They've captured   our fathers!"})
        self.assertEqual([t['raw'] for t in decode_stream(encoded)[0] if t['kind'] != 'text'], ['00'])
