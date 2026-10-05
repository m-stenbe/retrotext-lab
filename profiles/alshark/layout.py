"""Conservative layout check for the selected full-cell dialogue drafts."""


def validate_dialogue(tokens, names, columns=14, rows=4):
    """Validate the shared physical cursor; wait control 0 does not clear the box.

    Limited to the reviewed scripts. Unknown display modes fail closed.
    Names must be supplied as the strings used in the target demo.
    """
    row = column = origin = 0
    header = False
    colour = 'default'
    for token in tokens:
        kind = token['kind']
        if kind == 'call_origin':
            origin = column
            header = False
            colour = 'default'
            continue
        if kind == 'page_break':
            if 'restore_colour' in token:
                from profiles.alshark.r04_pages import validate_page_break
                validate_page_break(colour, token, header=header)
                row = column = origin = 0
                continue
            if header:
                raise ValueError('Extra pages cannot split a speaker header')
            if colour != 'default':
                raise ValueError('Extra pages would reset a non-default text colour')
            row = column = origin = 0
            continue
        if kind == 'control':
            raw = token['raw']
            if raw == '5f':
                row = column = origin = 0
                header = False
                colour = 'default'
            elif raw == '34':
                # f360 changes attributes/delay mode, not the cursor.
                header = True
                colour = 'default'
            elif raw == '35':
                # f33f clears header mode and falls into newline f344.
                row += 1
                column = origin
                header = False
                colour = 'default'
            elif raw in ('32', '33', '36'):
                colour = raw
            elif raw == '31':
                colour = 'default'
            elif raw not in ('30', '31', '32', '33', '36', '21'):
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
                column = origin
            else:
                column += 1
            if column > columns or row >= rows + 1:
                raise ValueError(f'Dialogue exceeds {columns} columns or available rows')
