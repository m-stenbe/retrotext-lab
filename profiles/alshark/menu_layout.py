"""Scoped six-cell field/battle menu experiment for the supported disk version."""

# Opening file 0x3FD9 is driver address 0x1FD9. Six-byte records contain
# width, rows, x, y, and a little-endian string pointer. The driver consumes
# these at 0x1F0C and passes width/rows to its animated box renderer at 0x150B.
BOXES = (
    (0x3fd9, bytes.fromhex('05 06 04 0f 58 21'), 'field'),
    # The alternate field menu shares the selection-width instruction.
    (0x3fdf, bytes.fromhex('05 07 04 0f 4d 21'), 'alternate field'),
    (0x401b, bytes.fromhex('05 06 04 0f f8 23'), 'battle'),
)

# MOV byte ptr [1D3E], 0A. Selection XOR uses this count in VRAM bytes:
# two bytes (16 pixels) per full-width character. Patch the immediate only.
HIGHLIGHTS = ((0x98b6, 'field'), (0x81ce, 'battle'))


def widen_menus(opening, system):
    """Guard all targets before changing five bytes across the two images."""
    changes = []
    for offset, expected, name in BOXES:
        if opening[offset:offset+len(expected)] != expected:
            raise ValueError(f'{name} menu geometry mismatch at {offset:#x}')
        changes.append(('Opening', offset, 5, 6, f'{name} box width'))
    instruction = bytes.fromhex('c6 06 3e 1d 0a')
    for offset, name in HIGHLIGHTS:
        if system[offset:offset+len(instruction)] != instruction:
            raise ValueError(f'{name} highlight instruction mismatch at {offset:#x}')
        changes.append(('System', offset+4, 10, 12, f'{name} highlight byte width'))
    records = []
    for disk, offset, before, after, purpose in changes:
        image = opening if disk == 'Opening' else system
        image[offset] = after
        records.append(dict(disk=disk, offset=offset, before=before, after=after,
                            purpose=purpose, runtime_verified=False))
    return records
