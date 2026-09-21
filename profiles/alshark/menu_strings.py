"""Experimental relocation of selected resident-driver menu strings."""

from profiles.alshark.menu_patch import encode_ui

# Boot reads sixteen 0x400-byte sectors from disk 0x2000 into segment 0800.
# The original resident image ends at disk 0x4c00; this zero-filled tail is
# inside that load. Runtime use of the new pool still requires playtesting.
POOL_START = 0x4c00
POOL_SIZE = 0x200
MENUS = (
    # Record, expected record AFTER widen_menus, replacement rows.
    (0x3fd9, '06 06 04 0f 58 21', 'STATUS\nITEMS\nPARTY\nEQUIP\nSKILLS\nSYSTEM'),
    (0x3fdf, '06 07 04 0f 4d 21', 'DATA\nSTATUS\nITEMS\nPARTY\nEQUIP\nSKILLS\nSYSTEM'),
    (0x401b, '06 06 04 0f f8 23', 'ATTACK\nSKILLS\nITEMS\nEQUIP\nSTATUS\nFLEE'),
    (0x40f9, '03 02 18 19 af 28', 'YES\nNO'),
    (0x3ffd, '08 05 08 14 d5 22', 'SYSTEM\nSAVE\nLOAD\nTEXT\nFORMAT'),
    (0x4075, '0b 04 0c 1e 37 26', 'SPEED\nFAST\nNORMAL\nSLOW'),
)


def expand_menu_strings(opening):
    """Validate the entire plan, then write text and change table pointers only."""
    if opening[POOL_START:POOL_START+POOL_SIZE] != bytes(POOL_SIZE):
        raise ValueError('Resident menu string pool is not empty')
    payload = bytearray()
    records = []
    for offset, expected_hex, text in MENUS:
        expected = bytes.fromhex(expected_hex)
        if opening[offset:offset+6] != expected:
            raise ValueError(f'Expanded menu record mismatch at {offset:#x}')
        lines = text.split('\n')
        if len(lines) != expected[1] or any(len(line) > expected[0] for line in lines):
            raise ValueError(f'Expanded menu layout overflow at {offset:#x}')
        encoded = encode_ui(text) + b'\0'
        destination = POOL_START + len(payload)
        records.append(dict(record_offset=offset, original_pointer=int.from_bytes(expected[4:], 'little'),
                            pointer=destination-0x2000, offset=destination, size=len(encoded),
                            translation=text, runtime_verified=False))
        payload.extend(encoded)
    if len(payload) > POOL_SIZE:
        raise ValueError('Resident menu string pool overflow')
    opening[POOL_START:POOL_START+len(payload)] = payload
    for record in records:
        offset = record['record_offset'] + 4
        opening[offset:offset+2] = record['pointer'].to_bytes(2, 'little')
    return records
