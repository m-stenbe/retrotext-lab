"""Reviewed R02 script links and menu framing from the original System disk.

This module records immutable control geometry. It does not grant edit rights,
patch bytes, infer physical walkability, or mark a section ready.
"""

from dataclasses import dataclass
from profiles.alshark.script import decode_entry


@dataclass(frozen=True)
class Link:
    source: str
    command: str
    target: str
    kind: str


def _link(source, raw, target, kind):
    return Link(source, raw, target, kind)


# #P uses bank index, then entry. These are all calls in the bounded
# Dust/Joe/Hamack-town/Hamack-bar static closure, including control-only roots.
CALLS = (
    _link('053000:002', '2350020223', '053000:035', 'speaker'),
    _link('053000:004', '2350020225', '053000:037', 'speaker'),
    _link('053000:006', '2350020225', '053000:037', 'speaker'),
    _link('053000:008', '2350020223', '053000:035', 'speaker'),
    _link('053000:011', '2350020223', '053000:035', 'speaker'),
    _link('053000:012', '2350020224', '053000:036', 'speaker'),
    _link('053000:025', '2350020323', '054000:035', 'sleeping-joe'),
    _link('053000:027', '2350020927', '05a000:039', 'joe-meeting'),
    _link('052000:058', '235002001b', '051000:027', 'job-accept'),
    _link('052000:061', '2350020019', '051000:025', 'job-absence'),
    _link('052000:062', '235002001a', '051000:026', 'job-request'),
    _link('052000:064', '2350020018', '051000:024', 'job-inventory-full'),
    _link('052000:068', '2350020016', '051000:022', 'job-dismissal'),
    _link('052000:070', '2350020017', '051000:023', 'job-payment'),
)


# Branch targets are entry IDs within the source's bank. The command bytes,
# including source flag and choice order, are preserved verbatim. These cases
# carry English text or can change the visible composed layout.
BRANCHES = (
    _link('052000:004', '2342020d4c', '052000:076', 'flag'),
    _link('052000:004', '2342020c4a', '052000:074', 'flag'),
    _link('052000:008', '2342020e48', '052000:072', 'flag'),
    _link('052000:008', '23470149', '052000:073', 'goto'),
    _link('052000:012', '2342020921', '052000:033', 'flag'),
    _link('052000:012', '235902201f', '052000:032', 'choice'),
    _link('052000:012', '235902201f', '052000:031', 'choice'),
    _link('052000:013', '234202072c', '052000:044', 'flag'),
    _link('052000:013', '234202082d', '052000:045', 'flag'),
    _link('052000:013', '2359022b2a', '052000:043', 'choice'),
    _link('052000:013', '2359022b2a', '052000:042', 'choice'),
    _link('052000:019', '2342020f54', '052000:084', 'flag'),
    _link('052000:023', '2342020b43', '052000:067', 'flag'),
    _link('052000:026', '2359022928', '052000:041', 'choice'),
    _link('052000:026', '2359022928', '052000:040', 'choice'),
    _link('052000:060', '2342020b47', '052000:071', 'flag'),
    _link('052000:067', '234202003f', '052000:063', 'flag'),
    _link('052000:072', '2342020f49', '052000:073', 'flag'),
    _link('052000:072', '2342020b3d', '052000:061', 'flag'),
    _link('052000:072', '2342020a3b', '052000:059', 'flag'),
    _link('052000:072', '2359023a39', '052000:058', 'choice'),
    _link('052000:072', '2359023a39', '052000:057', 'choice'),
    _link('053000:005', '2342021b0e', '053000:014', 'flag'),
    _link('053000:011', '2342021c13', '053000:019', 'flag'),
    _link('053000:014', '235902100f', '053000:016', 'choice'),
    _link('053000:014', '235902100f', '053000:015', 'choice'),
    _link('053000:020', '2342021d18', '053000:024', 'flag'),
    _link('053000:020', '2359021615', '053000:022', 'choice'),
    _link('053000:020', '2359021615', '053000:021', 'choice'),
    _link('082000:000', '2342021116', '082000:022', 'party-flag11'),
    _link('082000:001', '2342021117', '082000:023', 'party-flag11'),
    _link('082000:002', '2342021115', '082000:021', 'party-flag11'),
    _link('082000:000', '2342020f12', '082000:018', 'party-flag0f'),
    _link('082000:001', '2342020f14', '082000:020', 'party-flag0f'),
    _link('082000:001', '2342020b13', '082000:019', 'party-flag0b'),
    _link('082000:007', '2342020f0a', '082000:010', 'party-flag0f'),
    _link('082000:007', '2342020b11', '082000:017', 'party-flag0b'),
)


@dataclass(frozen=True)
class Menu:
    source: str
    command: str
    columns: int
    rows: int
    labels: str
    choices: tuple[str, ...]


# ?N payload: columns, rows, label-entry, then one branch entry per row.
MENUS = (
    Menu('052000:025', '3f4e06040350333435', 4, 3, '052000:080',
         ('052000:051', '052000:052', '052000:053')),
    Menu('052000:081', '3f4e0604034e1b1e1c', 4, 3, '052000:078',
         ('052000:027', '052000:030', '052000:028')),
    Menu('052000:082', '3f4e0506024f2232', 6, 2, '052000:079',
         ('052000:034', '052000:050')),
)


# The #U handler at 0xd739 picks one byte by a random index modulo the
# command count and jumps to that entry. These are palm-reading alternatives.
RANDOM = ('052000:032', '2355032e2f30',
          ('052000:046', '052000:047', '052000:048'))
TOWN_RANDOM = ('052000:021', '235503232425',
               ('052000:035', '052000:036', '052000:037'))
PARTY_RANDOM = ('082000:010', '2355030b0c0d',
                ('082000:011', '082000:012', '082000:013'))

# #H handler at 0xd8ee consumes selector, count-2 merchandise IDs, then an
# insufficient-money target. Cancel returns through 0xd93b→0xd7fe without
# taking this branch. Last bytes 0x1d and 0x31 are script entries, not items.
SHOP_LISTS = (
    ('052000:027', '23480601031a1b1d1d', 1, (3, 0x1a, 0x1b, 0x1d), '052000:029'),
    ('052000:030', '234807013d4d5163751d', 1, (0x3d, 0x4d, 0x51, 0x63, 0x75), '052000:029'),
    ('052000:034', '2348070381a2a39a9331', 3, (0x81, 0xa2, 0xa3, 0x9a, 0x93), '052000:049'),
)

# #F amount bytes are BCD-like tens/units in this early shop path; final
# byte is the insufficient-funds branch entry, not a price digit.
MONEY = (
    ('052000:041', '234603010127', '052000:039'),
    ('052000:055', '234603010236', '052000:054'),
    ('052000:056', '234603010136', '052000:054'),
)


def validate_source(entries):
    """Reject a changed/missing source command or an absent linked entry.

    `entries` is the `id`-keyed map from `script_tool.export_disk`.
    This deliberately leaves control-only entries unchanged.
    """
    def tokens(ident):
        try:
            return entries[ident]['tokens']
        except KeyError as exc:
            raise ValueError(f'R02 source entry missing: {ident}') from exc

    def require(ident, command):
        found = [t for t in tokens(ident)
                 if t['kind'] == 'command' and t['raw'] == command]
        if len(found) != 1:
            raise ValueError(f'{ident}: R02 command missing or ambiguous: {command}')

    for link in (*CALLS, *BRANCHES):
        require(link.source, link.command)
        tokens(link.target)
    for menu in MENUS:
        require(menu.source, menu.command)
        for target in (menu.labels, *menu.choices):
            tokens(target)
        payload = bytes.fromhex(menu.command)[3:]
        if (payload[:3] != bytes((menu.columns, menu.rows,
                                  int(menu.labels[-3:]) ))
                or len(menu.choices) != menu.rows
                or tuple(payload[3:]) != tuple(int(i[-3:]) for i in menu.choices)):
            raise ValueError(f'{menu.source}: R02 menu framing mismatch')
    for root, command, targets in (RANDOM, TOWN_RANDOM, PARTY_RANDOM):
        require(root, command)
        for target in targets:
            tokens(target)
        if tuple(bytes.fromhex(command)[3:]) != tuple(int(i[-3:]) for i in targets):
            raise ValueError(f'{root}: R02 random branch framing mismatch')
    for root, command, selector, items, no_money in SHOP_LISTS:
        require(root, command)
        tokens(no_money)
        if bytes.fromhex(command)[3:] != bytes((selector, *items, int(no_money[-3:]))):
            raise ValueError(f'{root}: R02 shop list framing mismatch')
    for root, command, failure in MONEY:
        require(root, command)
        tokens(failure)
        if bytes.fromhex(command)[-1] != int(failure[-3:]):
            raise ValueError(f'{root}: R02 money branch framing mismatch')


ROUTE_ROOTS = (
    *(f'052000:{i:03}' for i in
      (0, 1, 2, 3, 4, 5, 22, 6, 23, 24, 7, 8, 25, 9, 10, 11,
       26, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 60)),
    *(f'053000:{i:03}' for i in range(1, 13)),
    '053000:025', '053000:027',
    '082000:000', '082000:001', '082000:002', '082000:007',
)

# These flags are established by the R01 named route and the early R02 route.
# Later-story party tests are excluded; non-party branches remain conservative.
EARLY_PARTY_FLAGS = frozenset((0, 1, 2, 4, 6, 0x0a, 0x0b, 0x0c, 0x0d,
                               0x0e, 0x0f, 0x10, 0x11, 0x35))


def control_edges(ident, entries):
    """Decode all established local control edges, including menu choices.

    This is an edge inventory, not proof that each branch is taken in play.
    Unknown command types have no *known* script edge; their bytes are still
    subject to the immutable source guard in the existing exporter.
    """
    bank = int(ident.split(':')[0], 16)
    result = []
    def same(index):
        return f'{bank:06x}:{index:03}'
    for token in entries[ident]['tokens']:
        if token['kind'] != 'command':
            continue
        b = bytes.fromhex(token['raw'])
        op, payload = chr(b[1]), b[3:]
        if b[0] == ord('?'):
            if op == 'N' and len(payload) >= 4:
                result.extend((op, same(i), token['raw']) for i in payload[2:])
            continue
        if op == 'P' and len(payload) == 2:
            result.append((op, f'{0x51000+0x1000*payload[0]:06x}:{payload[1]:03}', token['raw']))
        elif op == 'B' and len(payload) == 2:
            if not ident.startswith('082000:') or payload[0] in EARLY_PARTY_FLAGS:
                result.append((op, same(payload[1]), token['raw']))
        elif op == 'O' and len(payload) >= 2:
            if not ident.startswith('082000:') or any(i in EARLY_PARTY_FLAGS for i in payload[:-1]):
                result.append((op, same(payload[-1]), token['raw']))
        elif op in ('Y', 'U'):
            result.extend((op, same(i), token['raw']) for i in payload)
        elif op in ('G',) and len(payload) == 1:
            result.append((op, same(payload[0]), token['raw']))
        elif op in ('A', 'C', 'I') and len(payload) == 3:
            result.append((op, same(payload[-1]), token['raw']))
        elif op in ('F', 'H') and len(payload) >= 2:
            result.append((op, same(payload[-1]), token['raw']))
    return result


def route_closure(entries, roots=ROUTE_ROOTS):
    """Transitively collect known static edges from source-proven roots."""
    pending = list(roots)
    seen = set()
    while pending:
        ident = pending.pop()
        if ident in seen:
            continue
        if ident not in entries:
            raise ValueError(f'R02 branch target missing: {ident}')
        seen.add(ident)
        pending.extend(target for _, target, _ in control_edges(ident, entries)
                       if target not in seen)
    return seen


def selected_text_dependencies(entries, selected, roots=ROUTE_ROOTS):
    """Return reachable text entries absent from a selected adaptation set.

    Traverses control-only dispatchers and menu selections recursively. Caller
    can compare returned IDs with the cumulative R01/R02 selection; visible
    English in resident UI and names is inventoried separately.
    """
    selected = set(selected)
    return {ident for ident in route_closure(entries, roots)
            if any(t['kind'] == 'text' for t in entries[ident]['tokens'])} - selected


# ?N at System 0xdced reads width as its first payload byte, doubles it for
# the renderer's VRAM cell advance, then reads row count and label entry.
# Existing original menus use widths up to nine. The reviewed R02 English
# labels require five cells in these two menus, at the same fixed anchor
# 0x2d06 and unchanged three-row selection order.
WIDENED_MENUS = (
    ('052000:081', '052000:078', 5),
    ('052000:025', '052000:080', 5),
)


def apply_reviewed_menu_widths(original, rebuilt, entries, selected):
    """Patch only reviewed ?N width bytes after normal script rebuilding.

    `entries` is the exporter map with selected text translations attached.
    Both original and rebuilt must be System-image bytes. Return new bytes and
    audit manifests; the caller must include them in its patch accounting.
    """
    selected = set(selected)
    if len(original) != len(rebuilt):
        raise ValueError('R02 menu overlay requires equal-sized System images')
    result = bytearray(rebuilt)
    manifest = []
    width_by_label = {label: width for _, label, width in WIDENED_MENUS}
    for menu in MENUS:
        source_id, label_id = menu.source, menu.labels
        if label_id not in selected:
            continue
        new_width = width_by_label.get(label_id, menu.columns)
        label_entry = entries[label_id]
        text = [t.get('translation') for t in label_entry['tokens']
                if t['kind'] == 'text']
        if len(text) != 1 or not isinstance(text[0], str):
            raise ValueError(f'{label_id}: one adapted menu label span required')
        lines = text[0].split('\n')
        if (len(lines) != menu.rows or any(not line or len(line) > new_width
                                            for line in lines)):
            raise ValueError(f'{label_id}: labels exceed reviewed {new_width}×{menu.rows} menu')
        if new_width > 9 or new_width < menu.columns:
            raise ValueError(f'{source_id}: unreviewed menu width')
        entry = entries[source_id]
        raw = bytes.fromhex(menu.command)
        def command_position(data):
            a, z = entry['offset'], entry['offset'] + entry['size']
            pos = a
            matches = []
            for token in decode_entry(data[a:z]):
                if token['kind'] == 'command' and token['raw'] == menu.command:
                    matches.append(pos)
                pos += len(bytes.fromhex(token['raw']))
            if len(matches) != 1:
                raise ValueError(f'{source_id}: menu source/output guard failed')
            return matches[0]
        source_start = command_position(original)
        start = command_position(result)
        if original[source_start:source_start+len(raw)] != raw or result[start:start+len(raw)] != raw:
            raise ValueError(f'{source_id}: menu source/output guard failed')
        if new_width == menu.columns:
            continue
        width_offset = start + 3
        if result[width_offset] != menu.columns:
            raise ValueError(f'{source_id}: original menu width changed')
        result[width_offset] = new_width
        manifest.append(dict(id=source_id, label=label_id, disk='System',
                             offset=width_offset, size=1,
                             before=f'{menu.columns:02x}', after=f'{new_width:02x}',
                             rows=menu.rows, choices=list(menu.choices),
                             reason='Reviewed English labels need five menu cells; ?N width only'))
    return bytes(result), manifest
