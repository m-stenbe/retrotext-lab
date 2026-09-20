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


def patch_menus(opening, system, *, reviewed=False):
    records = []
    # Repack rows within each complete string; keep its entry address and row
    # order. No code, pointer tables, disk sizes or following strings move.
    opening_edits = [
        (0x4158, 'ステｰタス@アイテム@作戦@装備変更@特殊能力@システム',
         'STAT\nBAG\nPARTY\nEQP\nABIL\nSYS' if reviewed else 'STAT\nITEM\nPLAN\nEQP\nABIL\nSYS', True),
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
    if reviewed:
        opening_edits += [
            (0x48af, 'ﾊｲ@ｲｲｴ', 'Y\nN', True),
            (0x48b6, '話ｼｶｹﾙ@隊列変更', 'TALK\nROW', True),
            (0x43f8, 'アタック@特殊能力@アイテム@装備変更@ステータス@戦闘離脱',
             'ATTACK\nABIL\nITEM\nEQP\nSTAT\nFLEE', True),
            (0x4306, 'デｰタｦセｰブｼﾏｽ。@ユｰザｰディスクｦドライブ２ﾆ@入ﾚ、何ｶキｰｦ押ｼﾃｸだｻｲ',
             'SAVE USER DISK\nDRIVE 2\nPRESS KEY', False),
            (0x4348, 'デｰタｦロｰドｼﾏｽ。@ユｰザｰディスクｦドライブ２ﾆ@入ﾚ、何ｶキｰｦ押ｼﾃｸだｻｲ',
             'LOAD USER DISK\nDRIVE 2\nPRESS KEY', False),
            (0x4294, '作業が終了ｼﾏｼﾀ。@デｰタディスクｦドライブ２ﾆ@戻ｼ、何ｶキｰｦ押ｼﾃｸだｻｲ',
             'DATA DISK\nDRIVE 2\nPRESS ANY KEY', False),
        ]
        system_edits += [
            (0x1d72, '＜誰ﾉ？＞', 'WHO?', False),
            (0x1d7c, '＜誰ﾆ？＞', 'WHO?', False),
            (0x1dac, '〈現隊列〉', 'ORDER', False),
            (0x1db7, ' 隊列ｦ変更ｼﾏｽ。', 'REORDER', False),
            (0x1dc7, '〈新隊列〉@（１）@（２）@（３）@（４）@（５）',
             'NEW ORDER\n1\n2\n3\n4\n5', True),
            (0x107aa, 'ｻバｲバﾙﾅｲﾌ', 'KNIFE', False),
            (0x10875, 'ﾊﾝドガﾝ', 'GUN', False),
            (0x10b74, 'ﾊﾝドﾒデｨｶﾙ', 'MEDS', False),
            (0x11329, '  惑星ﾎﾑ', 'HOM', False),
            # Keep the preceding '>' location-display control at 0x11722.
            (0x11723, 'ザｸｾﾝｷｬﾆｵﾝ', 'SAXEN', False),
        ]
    for disk, data, edits in [('Opening', opening, opening_edits),
                              ('System', system, system_edits)]:
        for offset, source, translation, menu in edits:
            record = replace_ui(data, offset, source, translation, menu=menu)
            records.append(dict(disk=disk, **record))
    return records
