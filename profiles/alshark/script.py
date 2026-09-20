"""Conservative linear Alshark decoder. Not a control-flow interpreter."""
import hashlib


class Unsupported(ValueError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def decode_entry(data):
    """Preserve every byte, exposing only established text spans.

    #/? framing follows the count reader at System 0xF471/0xF480.
    $ consumes one ID (0xF38D). The dispatch table is at 0xF4BA.
    Unknown controls reject the entire entry. Bytes after the first top-level
    terminator remain opaque; they may be padding, residual data or branch data.
    """
    tokens = []
    i = 0
    while i < len(data):
        start = i
        b = data[i]
        if b == 0:
            tokens.append({'kind': 'end', 'raw': '00'})
            if i+1 < len(data):
                tokens.append({'kind': 'opaque_tail', 'raw': data[i+1:].hex()})
            for index, token in enumerate(tokens):
                token['id'] = f't{index:03d}'
            return tokens
        if b in (ord('#'), ord('?')):
            if i+3 > len(data):
                raise Unsupported(f'Truncated counted command at {i}')
            i += 3 + data[i+2]
            if i > len(data):
                raise Unsupported(f'Command arguments exceed entry at {start}')
            tokens.append({'kind': 'command', 'raw': data[start:i].hex()})
        elif b == ord('$'):
            if i+2 > len(data):
                raise Unsupported(f'Truncated name reference at {i}')
            tokens.append({'kind': 'name', 'name_id': data[i+1], 'raw': data[i:i+2].hex()})
            i += 2
        elif b in b'0123456_!>/':
            tokens.append({'kind': 'control', 'raw': data[i:i+1].hex()})
            i += 1
        elif b in b'(=':
            if i+2 > len(data):
                raise Unsupported(f'Truncated indexed display control at {i}')
            tokens.append({'kind': 'display_argument', 'raw': data[i:i+2].hex()})
            i += 2
        else:
            chars = []
            while i < len(data):
                b = data[i]
                if b == 0x40:
                    chars.append('\n'); i += 1
                elif b == 0x20 or 0x41 <= b <= 0x5a or 0xa6 <= b < 0xde:
                    chars.append(bytes([b]).decode('cp932')); i += 1
                elif 0x81 <= b <= 0x9f or 0xe0 <= b <= 0xef:
                    if i+2 > len(data):
                        raise Unsupported(f'Truncated CP932 pair at {i}')
                    try:
                        chars.append(data[i:i+2].decode('cp932'))
                    except UnicodeDecodeError as exc:
                        raise Unsupported(f'Invalid CP932 pair at {i}') from exc
                    i += 2
                else:
                    break
            if not chars:
                raise Unsupported(f'Unsupported byte 0x{b:02X} at {i}')
            tokens.append({'kind': 'text', 'raw': data[start:i].hex(),
                           'source': ''.join(chars), 'translation': None})
    raise Unsupported('No top-level terminator before entry boundary')


def encode_translation(text):
    if not isinstance(text, str):
        raise ValueError('Translation must be a string or null')
    result = bytearray()
    for c in text:
        if c == '\n':
            result.append(0x40)
        elif c == ' ' or 'A' <= c <= 'Z':
            result.extend(c.encode('ascii'))
        elif c in ",.?!'0123456789":
            result.extend(chr(ord(c)+0xfee0).encode('cp932'))
        else:
            raise ValueError(f'Unsupported translation character {c!r}; use uppercase English')
    return bytes(result)


def rebuild_entry(original, edited):
    """Immutable commands and source metadata; text changes stay in allocation."""
    expected = decode_entry(original)
    if len(expected) != len(edited):
        raise ValueError('Token list changed')
    parts = []
    for source, token in zip(expected, edited):
        candidate = dict(token)
        translation = candidate.get('translation')
        if source['kind'] == 'text':
            candidate['translation'] = None
        if candidate != source:
            raise ValueError('Only translation fields may be edited')
        parts.append(encode_translation(translation)
                     if source['kind'] == 'text' and translation is not None
                     else bytes.fromhex(source['raw']))
    result = b''.join(parts)
    if len(result) > len(original):
        raise ValueError(f'Entry needs {len(result)} bytes; allocation is {len(original)}')
    # Moving opaque suffixes is not safe: preserve them at their original offsets.
    if expected and expected[-1]['kind'] == 'opaque_tail':
        tail = bytes.fromhex(expected[-1]['raw'])
        body = b''.join(parts[:-1])
        available = len(original)-len(tail)
        if len(body) > available:
            raise ValueError('Edit would move opaque tail')
        return body.ljust(available, b'\0') + tail
    return result.ljust(len(original), b'\0')
