"""Guarded meteor cinematic stream adapter; see docs/alshark-cinematic-format.md."""
import hashlib
from pathlib import Path
from retrotext.localization import make_record

BLOCK = 0xCF800
SIZE = 0x2000
START = BLOCK + 0xF8E
END = 0xD0F68
IDENT = 'cinematic:meteor'
# Handler operand counts in the System interpreter, not the Opening intro engine.
FIXED = {'L': 1, 'E': 2, 'P': 2, 'O': 0, 'X': 1, 'Z': 1, 'C': 0,
         'F': 2, 'T': 1, 'S': 1, 'U': 2, 'G': 3, 'H': 3}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def _originals(images):
    hashes = dict(line.split('  ', 1)[::-1] for line in
                  (Path(__file__).parent / 'SHA256SUMS.txt').read_text().splitlines())
    for disk in ('System', 'Opening'):
        if sha(images[disk]) != hashes[f'Alshark ({disk} Disk).hdm']:
            raise ValueError(f'{disk}: cinematic source hash mismatch')


def decode_stream(raw):
    """Decode the audited meteor command subset; reject unknown bytes/commands."""
    tokens = []
    p = 0
    active = set()
    while p < len(raw):
        start = p
        c = raw[p]
        p += 1
        kind = 'control'
        if c == 0:
            kind = 'end'
        elif c == 35:
            if p >= len(raw):
                raise ValueError('Truncated cinematic command')
            command = chr(raw[p])
            p += 1
            if command in 'MDAB':
                if p >= len(raw):
                    raise ValueError('Missing animation identifier')
                active.add(raw[p])
                p += 1
                while p < len(raw) and raw[p]:
                    p += 1
                p += 1
                if command == 'M':
                    p += 1
            elif command in FIXED:
                p += FIXED[command]
                if command == 'L':
                    active.clear()
            else:
                raise ValueError(f'Unsupported cinematic command #{command}')
            kind = 'command'
        elif c in (95, 47):
            p += 1
        elif c in (64, 33) or c in active:
            pass
        elif c == 32 or 0xA6 <= c < 0xDE:
            kind = 'text'
        elif 0x81 <= c <= 0x9F or 0xE0 <= c <= 0xFC:
            p += 1
            kind = 'text'
        else:
            raise ValueError(f'Unsupported cinematic byte {c:02x} at {start:x}')
        if p > len(raw):
            raise ValueError('Truncated cinematic operand or glyph')
        piece = raw[start:p]
        if kind == 'text' and tokens and tokens[-1]['kind'] == 'text':
            tokens[-1]['raw'] += piece.hex()
            tokens[-1]['text'] += piece.decode('cp932')
        else:
            token = dict(id=f't{len(tokens):03d}', kind=kind, offset=start, raw=piece.hex())
            if kind == 'text':
                token['text'] = piece.decode('cp932')
            tokens.append(token)
        if kind == 'end':
            return tokens, p
    raise ValueError('Missing cinematic terminator')


def export_records(images):
    _originals(images)
    opening = images['Opening']
    if opening[BLOCK:BLOCK+2] != bytes.fromhex('8e0f'):
        raise ValueError('Meteor entry pointer mismatch')
    tokens, consumed = decode_stream(opening[START:BLOCK+SIZE])
    if START + consumed != END:
        raise ValueError('Meteor stream extent mismatch')
    source = dict(disk='Opening', offset=START, size=BLOCK+SIZE-START,
                  raw=opening[START:BLOCK+SIZE].hex(),
                  sha256=sha(opening[START:BLOCK+SIZE]), tokens=tokens,
                  blockOffset=BLOCK, blockSize=SIZE,
                  blockSha256=sha(opening[BLOCK:BLOCK+SIZE]),
                  pointerOffset=BLOCK, pointerRaw='8e0f',
                  streamSize=consumed, columns=25, rows=5,
                  interpreterDisk='System', interpreterOffset=0x14000,
                  interpreterSha256=sha(images['System'][0x14000:0x1506D]))
    return [make_record(IDENT, 'cinematic', source)]


def encode_text(text):
    """Use full-width CP932 Latin: ASCII letters are interpreter opcodes."""
    if not isinstance(text, str):
        raise ValueError('Cinematic text must be a string')
    out = bytearray()
    for c in text:
        if c == ' ':
            out.append(32)
        elif c.isascii() and (c.isalpha() or c.isdigit()):
            out.extend(chr(ord(c.upper()) + 0xFEE0).encode('cp932'))
        elif c in ".,!?'-:;()":
            replacement = {'-': '－', "'": '’'}.get(c, chr(ord(c)+0xFEE0))
            out.extend(replacement.encode('cp932'))
        else:
            raise ValueError(f'Unsupported cinematic glyph {c!r}')
    return bytes(out)


def fit_tokens(tokens, translations):
    expected = {t['id'] for t in tokens if t['kind'] == 'text'}
    if not isinstance(translations, dict) or set(translations) != expected:
        raise ValueError('Every cinematic text token must have exactly one adaptation')
    row = col = 0
    wrapped_word = False
    output = bytearray()
    for token in tokens:
        raw = bytes.fromhex(token['raw'])
        if token['kind'] == 'text':
            text = translations[token['id']]
            if token['text'].isspace() and text != token['text']:
                raise ValueError('Cinematic timing spaces must be preserved')
            raw = encode_text(text)
            for character in text:
                if wrapped_word and not character.isspace():
                    raise ValueError(f"{token['id']}: cinematic would wrap inside a word; pad at a word boundary")
                wrapped_word = False
                col += 1
                if col == 25:
                    row += 1
                    col = 0
                    wrapped_word = not character.isspace()
                if row >= 5:
                    raise ValueError(f"{token['id']}: cinematic page would auto-clear")
        elif raw == b'@':
            row += 1
            col = 0
            wrapped_word = False
            if row >= 5:
                raise ValueError(f"{token['id']}: cinematic newline would auto-clear")
        elif raw[:1] == b'_':
            row = col = 0
            wrapped_word = False
        output.extend(raw)
    decoded, consumed = decode_stream(bytes(output))
    immutable = lambda ts: [t['raw'] for t in ts if t['kind'] != 'text']
    if consumed != len(output) or immutable(decoded) != immutable(tokens):
        raise ValueError('Cinematic controls changed during encoding')
    return bytes(output)


def compile_records(images, records):
    """Return (Opening bytes, per-record patch metadata), after editorial selection.

    Caller remains responsible for current canonical/editorial/basedOn checks.
    This layer rechecks every original byte and validates complete text/layout.
    """
    originals = {r['id']: r for r in export_records(images)}
    output = bytearray(images['Opening'])
    manifest = []
    seen = set()
    for record in records:
        ident = record['id']
        if ident not in originals or ident in seen:
            raise ValueError('Unknown or duplicate cinematic record')
        seen.add(ident)
        original = originals[ident]
        if record['kind'] != 'cinematic' or record['source'] != original['source']:
            raise ValueError('Immutable cinematic source changed')
        if record['target']['status'] != 'adapted':
            raise ValueError('Cinematic record has no completed adaptation')
        source = record['source']
        encoded = fit_tokens(source['tokens'], record['target']['inGameEnglish'])
        if len(encoded) > source['size']:
            raise ValueError('Cinematic stream exceeds loaded block allocation')
        # Keep unused original bytes, including unreachable stale text, intact.
        output[START:START+len(encoded)] = encoded
        manifest.append(dict(record=ident, disk='Opening', offset=START,
                             size=source['size'], used=len(encoded),
                             sha256=sha(encoded), columns=25, rows=5))
    return bytes(output), manifest
