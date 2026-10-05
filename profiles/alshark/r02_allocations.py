"""One reviewed two-byte R02 script allocation shift in bank 052000.

Entry 008's original two-byte Japanese speaker header cannot hold GIRL.
The already adapted entry 009 has two verified zero padding bytes. Moving
their boundary by exactly two bytes keeps the bank end and all other entry
addresses unchanged. This is not a general allocator.
"""

from profiles.alshark.script import digest, decode_entry, encode_translation, rebuild_entry
from profiles.alshark.script_tool import SYSTEM_HASH, export_disk


BANK = 0x52000
POINTER_009 = BANK + 2*9
ENTRY_008 = '052000:008'
ENTRY_009 = '052000:009'
START_008 = 0x522f0
START_009 = 0x522fe
END_009 = 0x5232f
NEW_START_009 = START_009 + 2


def relocate_girl_header(original, rebuilt, edited_entries, selected):
    """Return guarded System bytes and allocation/pointer patch manifests.

    `rebuilt` is the normal importer output with entry 008 still original and
    entry 009 already adapted. `edited_entries` maps bank entry IDs to token
    documents, including the proposed GIRL translation for 008. The caller
    must defer only 008 from the normal importer and pass all adapted IDs in
    `selected`. No source bytes or controls outside this exact pair may move.
    """
    selected = set(selected)
    if ENTRY_008 not in selected:
        return bytes(rebuilt), []
    if ENTRY_009 not in selected:
        raise ValueError('R02 GIRL relocation requires adapted adjacent entry 009')
    if digest(original) != SYSTEM_HASH or len(original) != len(rebuilt):
        raise ValueError('R02 GIRL relocation requires the guarded original System image')
    exported = {entry['id']: entry for entry in export_disk(original)['entries']}
    left, right = exported[ENTRY_008], exported[ENTRY_009]
    if ((left['offset'], left['size'], right['offset'], right['size'])
            != (START_008, 14, START_009, END_009-START_009)):
        raise ValueError('R02 GIRL pair allocation changed')
    if any(t['kind'] == 'opaque_tail' for t in (*left['tokens'], *right['tokens'])):
        raise ValueError('R02 GIRL pair has an opaque tail')
    if original[POINTER_009:POINTER_009+2] != (START_009-BANK).to_bytes(2, 'little'):
        raise ValueError('R02 GIRL source pointer changed')
    if rebuilt[POINTER_009:POINTER_009+2] != original[POINTER_009:POINTER_009+2]:
        raise ValueError('R02 GIRL output pointer was already modified')
    if rebuilt[START_008:START_009] != original[START_008:START_009]:
        raise ValueError('R02 GIRL entry 008 must be deferred from the normal importer')
    try:
        left_tokens = edited_entries[ENTRY_008]['tokens']
        right_tokens = edited_entries[ENTRY_009]['tokens']
    except KeyError as exc:
        raise ValueError('R02 GIRL pair token document missing') from exc
    if len(left_tokens) != len(left['tokens']) or len(right_tokens) != len(right['tokens']):
        raise ValueError('R02 GIRL pair token count changed')
    left_bytes = bytearray()
    for source, edited in zip(left['tokens'], left_tokens):
        if source['kind'] == 'text' and source['id'] == 't001':
            if edited.get('translation') != 'GIRL':
                raise ValueError('R02 GIRL relocation permits only the reviewed GIRL header')
            if ({k:v for k,v in edited.items() if k != 'translation'}
                    != {k:v for k,v in source.items() if k != 'translation'}):
                raise ValueError('R02 GIRL source token changed')
            left_bytes += encode_translation('GIRL')
        else:
            if edited != source:
                raise ValueError('R02 GIRL non-header token changed')
            left_bytes += bytes.fromhex(source['raw'])
    if len(left_bytes) != 16 or len(left_bytes)+47 != END_009-START_008:
        raise ValueError('R02 GIRL shift is not exactly two bytes')
    expected_right = rebuild_entry(original[START_009:END_009], right_tokens)
    if rebuilt[START_009:END_009] != expected_right or expected_right[-2:] != b'\0\0':
        raise ValueError('R02 GIRL entry 009 is not the selected 47-byte adapted body')
    # The first terminator of 009 must remain inside its new 47-byte span.
    if not any(t['kind'] == 'end' for t in decode_entry(expected_right[:-2])):
        raise ValueError('R02 GIRL adjacent entry has no terminator')
    output = bytearray(rebuilt)
    output[START_008:END_009] = left_bytes + expected_right[:-2]
    output[POINTER_009:POINTER_009+2] = (NEW_START_009-BANK).to_bytes(2, 'little')
    manifests = [
        dict(id=ENTRY_008, disk='System', offset=START_008, size=16,
             sourceOffset=START_008, sourceSize=14,
             reason='Reviewed GIRL header gains two bytes from adjacent zero padding'),
        dict(id=ENTRY_009, disk='System', offset=NEW_START_009, size=47,
             sourceOffset=START_009, sourceSize=49,
             reason='Existing adapted entry shifts two bytes; commands and body unchanged'),
        dict(id='r02:pointer:052000:009', disk='System', offset=POINTER_009, size=2,
             before=original[POINTER_009:POINTER_009+2].hex(),
             after=output[POINTER_009:POINTER_009+2].hex(),
             reason='Bank-relative pointer follows the reviewed allocation boundary'),
    ]
    return bytes(output), manifests
