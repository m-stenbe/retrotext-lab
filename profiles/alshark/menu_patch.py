"""Fixed-allocation UI drafts. These strings use full-width CP932, not scripts."""


def encode_ui(text):
    result = bytearray()
    for char in text:
        if char == '\n':
            result.extend(b'@')
        elif char == ' ':
            result.extend('\u3000'.encode('cp932'))
        elif char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!'":
            result.extend(chr(ord(char) + 0xfee0).encode('cp932'))
        else:
            raise ValueError(f'Unsupported UI character: {char!r}')
    return bytes(result)


def replace_ui(data, offset, source, translation, *, menu=False):
    old = source.encode('cp932') + b'\0'
    new = encode_ui(translation) + b'\0'
    if data[offset:offset + len(old)] != old:
        raise ValueError(f'UI source mismatch at {offset:#x}')
    if len(new) > len(old):
        raise ValueError(f'UI overflow at {offset:#x}: {len(new)}/{len(old)}')
    if menu and source.count('@') != translation.count('\n'):
        raise ValueError('Menu row count changed')
    if any(len(line) > 14 for line in translation.split('\n')):
        raise ValueError('UI draft exceeds conservative width')
    data[offset:offset + len(old)] = new.ljust(len(old), b'\0')
    return dict(offset=offset, size=len(old), translation=translation,
                used_bytes=len(new), runtime_verified=False)


def patch_menus(opening, system):
    records = []
    # Repack rows within each complete string; keep its entry address and row
    # order. No code, pointer tables, disk sizes or following strings move.
    opening_edits = [
        (0x4158, 'ステｰタス@アイテム@作戦@装備変更@特殊能力@システム',
         'STAT\nITEM\nPLAN\nEQP\nABIL\nSYS', True),
        (0x42d5, '〈システム〉@セｰブ@ロｰド@メッセｰジ@UDフォｰマット',
         'SYS\nSAVE\nLOAD\nTEXT\nFORMAT', True),
        (0x4637, '〈メッセｰジスピｰド〉@   速ｲ@   普通@   遅ｲ',
         'SPEED\nFAST\nNORM\nSLOW', True),
        (0x46ec, '装備の対象ﾄﾅﾙアイテムが@ｱﾘﾏｾﾝ。',
         'NO GEAR\nTO EQUIP', False),
        (0x4aec, '装備の対象ﾄﾅﾙアイテムが@ｱﾘﾏｾﾝ。',
         'NO GEAR\nTO EQUIP', False),
    ]
    system_edits = [
        (0x1e98, '何ﾓアイテムｦ持ｯﾃｲﾏｾﾝ。', 'NO ITEMS.', False),
        (0x1e2b, 'ﾊ、', ' ', False),
        (0x1e2f, '特殊能力ｦ使ｳｺﾄがでｷﾅｲ。', 'NO SKILLS.', False),
    ]
    for disk, data, edits in [('Opening', opening, opening_edits),
                              ('System', system, system_edits)]:
        for offset, source, translation, menu in edits:
            record = replace_ui(data, offset, source, translation, menu=menu)
            records.append(dict(disk=disk, **record))
    return records
