"""Restore source narration attributes after English reflow newlines.

Original @ and automatic wrap reset INT41 attributes. Japanese narration
reissues36 at each source line; English lines no longer coincide with those
spans. The compiler may restore36 after translated @, without changing any
original control, name, command, pointer or allocation.
"""


def encode_text(text, colour, *, preserve_narration=False):
    from profiles.alshark.script import encode_translation
    encoded = encode_translation(text)
    if preserve_narration and colour == '36':
        return encoded.replace(b'@', b'@6')
    return encoded


def validate_source(system):
    from profiles.alshark.r04_pages import validate_renderer_source
    validate_renderer_source(system)
    # @ moves the cursor then enters shared cursor/default-attribute reset.
    guards = {
        0xf344: '8b3e561d81c70005e97eff',
        0xf360: 'c606511d01bb0a05e973ff',
        0xf33f: 'c606511d00',
    }
    for offset, expected in guards.items():
        raw=bytes.fromhex(expected)
        if system[offset:offset+len(raw)] != raw:
            raise ValueError(f'Playtest narration source mismatch at {offset:x}')
