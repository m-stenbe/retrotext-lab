"""Continuation-page geometry for existing narration control36.

The reviewed compiler alone may insert wait/clear/restore sequences. Source
controls, commands and names remain immutable; other colours fail closed.
"""


HEADER_CALLS = {
    # R09 historian: source-checked clear/header/body, not the colored book title.
    '2350021214': ('063000:020', ('5f','34','35')),
    # R06 reuses the same source-guarded pure speaker header shape.
    '235002090c': ('05a000:012', ('5f','34','35')),
    '2350020d0d': ('05e000:013', ('5f','34','35')),
    '2350020d0e': ('05e000:014', ('5f','34','35')),
    '2350020d0f': ('05e000:015', ('5f','34','35')),
    # R05 uses the same proven clear/header/body shape and renderer.
    '2350020a11': ('05b000:017', ('5f','34','35')),
    '2350020e13': ('05f000:019', ('5f','34','35')),
    '2350020223': ('053000:035', ('5f','34','35')),
    '2350020224': ('053000:036', ('5f','34','35')),
    '2350020225': ('053000:037', ('5f','34','35')),
    '2350020b1a': ('05c000:026', ('34','35')),
    '2350020b24': ('05c000:036', ('5f','34','35')),
    '2350020b25': ('05c000:037', ('5f','34','35')),
    '2350020c01': ('05d000:001', ('5f','34','35')),
}


def validate_header_calls(entries):
    for raw, (ident, controls) in HEADER_CALLS.items():
        tokens = entries[ident]['tokens']
        expected_kinds = (['control'] * (len(controls)-1) +
                          ['text','control','end'])
        if ([t['kind'] for t in tokens] != expected_kinds or
            tuple(t['raw'] for t in tokens if t['kind']=='control') != controls or
            tokens[-1]['raw'] != '00'):
            raise ValueError(f'R04 continuation header source guard mismatch: {ident}')


def advance_colour(colour, token):
    if token['kind'] == 'command' and token['raw'].startswith('2350'):
        return 'default' if token['raw'] in HEADER_CALLS else 'unknown-call'
    if token['kind'] != 'control':
        return colour
    raw = token['raw']
    if raw in ('34','35','5f','31'):
        return 'default'
    if raw in ('32','33','36'):
        return raw
    return colour


def page_separator(colour):
    if colour == 'default':
        return b'0_'
    if colour == '36':
        return b'0_6'
    raise ValueError('Continuation pages require default or reviewed narration colour36')


def page_break_token(colour):
    page_separator(colour)
    return dict(kind='page_break', restore_colour=colour)


def validate_page_break(colour, token, header=False):
    if header:
        raise ValueError('Extra pages cannot split a speaker header')
    restoration = token.get('restore_colour','default')
    if restoration != colour:
        raise ValueError('Continuation page colour restoration mismatch')
    page_separator(colour)


def validate_renderer_source(system):
    """Guard the original dispatch and handlers used by wait/clear/restore."""
    from hashlib import sha256
    from profiles.alshark.script_tool import SYSTEM_HASH
    if sha256(system).hexdigest() != SYSTEM_HASH:
        raise ValueError('R04 narration renderer original System hash mismatch')
    guards = {
        0xf4c6: '3009310a320b330c340d350e36135f0f',
        0xf35b: 'e868f3eb82',
        0xf2db: 'bb0f05b407cd41',
        0xf371: 'bb0d09e967ff',
    }
    for offset, expected in guards.items():
        raw = bytes.fromhex(expected)
        if system[offset:offset+len(raw)] != raw:
            raise ValueError(f'R04 narration renderer guard mismatch at {offset:x}')
