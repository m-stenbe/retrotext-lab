"""Candidate detection, not a script interpreter or relocation policy."""
import struct


def relative_table(block, max_table_bytes=512):
    """Detect a monotonic LE16 table with first offset equal to table length.

    Duplicate pointers are supported. Binary data can produce false positives.
    """
    if len(block) < 2:
        return None
    first = struct.unpack_from('<H', block)[0]
    if first % 2 or not 4 <= first <= min(max_table_bytes, len(block)):
        return None
    pointers = struct.unpack_from('<' + 'H'*(first//2), block)
    if not all(first <= p < len(block) for p in pointers):
        return None
    if any(a > b for a, b in zip(pointers, pointers[1:])):
        return None
    return pointers


def split_candidate(block, pointers):
    """Lossless physical slices, including padding and residual data."""
    pointers = tuple(pointers)
    if pointers != relative_table(block, len(block)):
        raise ValueError('Pointers do not match the candidate table')
    prefix = block[:pointers[0]]
    parts = [block[a:z] for a, z in zip(pointers, pointers[1:] + (len(block),))]
    if prefix + b''.join(parts) != block:
        raise ValueError('Roundtrip failed')
    return prefix, parts
