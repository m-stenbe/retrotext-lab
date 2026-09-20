"""Conservative layout check for the selected full-cell dialogue drafts."""


def validate_dialogue(tokens, names, columns=14, rows=4):
    """Validate headers/body separately; wait control 0 does not clear the box.

    Limited to the reviewed scripts. Unknown display modes fail closed.
    Names must be supplied as the strings used in the target demo.
    """
    row = column = 0
    header = False
    for token in tokens:
        kind = token['kind']
        if kind == 'control':
            raw = token['raw']
            if raw in ('34', '35', '5f'):
                row = column = 0
                header = raw == '34'
            elif raw != '30':
                raise ValueError(f'Unreviewed layout control {raw}')
            continue
        if kind in ('command', 'end', 'opaque_tail'):
            continue
        if kind == 'name':
            if token['name_id'] not in names:
                raise ValueError('Missing rendered name for layout validation')
            text = names[token['name_id']]
        elif kind == 'text':
            text = token['translation']
            if text is None:
                raise ValueError('Draft must translate every text span before layout validation')
        else:
            raise ValueError(f'Unsupported layout token {kind}')
        for c in text:
            if c == '\n':
                row += 1
                column = 0
            else:
                column += 1
            if column > columns or row >= (1 if header else rows):
                raise ValueError(f'Dialogue exceeds {columns} columns or available rows')
