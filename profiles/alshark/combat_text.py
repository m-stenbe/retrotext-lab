"""Translate shared result text without moving runtime fields or code references."""
from profiles.alshark.script import decode_entry, encode_translation


def fixed_text(text, size):
    """Use equivalent full-cell ASCII/CP932 glyphs to occupy exactly size bytes.

    Both forms already render in the script engine. Unlike padding with spaces,
    this preserves the intended number of visible cells. No opcodes are added.
    """
    pieces = [encode_translation(char) for char in text]
    extra = size - sum(map(len, pieces))
    if extra < 0:
        raise ValueError('Fixed text exceeds its original span')
    for index, char in enumerate(text):
        if not extra:
            break
        if char == ' ' or 'A' <= char <= 'Z':
            pieces[index] = ('\u3000' if char == ' ' else chr(ord(char) + 0xfee0)).encode('cp932')
            extra -= 1
    if extra:
        raise ValueError('Fixed text is too short to fill its span without padding')
    return b''.join(pieces)


def patch_script_spans(data, original, start, end, edits):
    tokens = decode_entry(original[start:end])
    found = set()
    changes = []
    cursor = start
    for token in tokens:
        raw = bytes.fromhex(token['raw'])
        if token['id'] in edits:
            if token['kind'] != 'text':
                raise ValueError('Fixed script edit targets a non-text token')
            if data[cursor:cursor+len(raw)] != raw:
                raise ValueError('Fixed script source changed')
            text = edits[token['id']]
            replacement = fixed_text(text, len(raw))
            changes.append((cursor, replacement))
            found.add(token['id'])
        cursor += len(raw)
    if found != set(edits):
        raise ValueError('Unknown fixed script token')
    # Validate every replacement before mutating any span.
    for offset, replacement in changes:
        data[offset:offset+len(replacement)] = replacement
    return dict(offset=start, size=end-start, translations=edits,
                runtime_verified=False)


def patch_combat_text(data, original):
    return [
        patch_script_spans(data, original, 0x1edf, 0x1f28, {
            't000': 'PARTY GAINS\nEXP   ',
            't004': '\nCREDITS ', 't008': '\nSCRAP   ',
            't012': '\nGAINED.',
        }),
        patch_script_spans(data, original, 0x1f28, 0x1fd8, {
            't001': 'LEVEL UP!!', 't006': '\nPP   ',
            't008': ' PTS\nMP  ', 't010': ' PTS\nIQ  ', 't012': ' PTS\n',
            't025': ' PTS\nL', 't035': ' PTS\nA', 't041': ' PTS\nD',
            't047': ' PTS\nSTATS IMPROVED',
        }),
    ]
