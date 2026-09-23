#!/usr/bin/env python3
"""Build a scoped opening-conversation experiment, preserving scene allocation."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('original', type=Path)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--include-followup', action='store_true',
                    help="Use the validated importer for Lucia's meteor warning")
parser.add_argument('--include-town', action='store_true',
                    help='Add Karu and two town conversations; implies --include-followup')
parser.add_argument('--include-pickups', action='store_true',
                    help='Add starting-house pickup messages; implies --include-town')
parser.add_argument('--include-area', action='store_true',
                    help='Add 19 town/branch drafts and basic menus; implies --include-pickups')
parser.add_argument('--include-review', action='store_true',
                    help='Include screenshot-review UI and combat drafts; implies --include-area')
parser.add_argument('--widen-menus', action='store_true',
                    help='Test six-cell field/battle boxes and matching highlights; implies --include-review')
parser.add_argument('--expand-menu-labels', action='store_true',
                    help='Test relocated full menu labels including YES/NO; implies --widen-menus')
parser.add_argument('--translate-disk-prompts', action='store_true',
                    help='Apply reviewed dynamic boot-driver disk prompts')
parser.add_argument('--localization', type=Path,
                    help='Overlay reviewed canonical-derived script adaptations; implies --include-review')
parser.add_argument('--localization-scenes', nargs='+',
                    help='Explicit complete scenes to build; other reviewed work is listed as deferred')
args = parser.parse_args()
if args.localization_scenes and not args.localization:
    parser.error('--localization-scenes requires --localization')
if args.localization:
    args.include_review = True
if args.expand_menu_labels:
    args.widen_menus = True
if args.widen_menus:
    args.include_review = True
if args.include_review:
    args.include_area = True
if args.include_area:
    args.include_pickups = True
if args.include_pickups:
    args.include_town = True
if args.include_town:
    args.include_followup = True
ROOT = Path(__file__).resolve().parent
OUT = args.output.resolve()
if OUT == args.original.resolve() or args.original.resolve() in OUT.parents:
    parser.error('Output must be separate from the original directory')
OUT.mkdir(parents=True, exist_ok=True)
hashes = dict(line.split('  ', 1)[::-1] for line in (ROOT / 'SHA256SUMS.txt').read_text().splitlines())
images = {}
for p in args.original.glob('*.hdm'):
    data = p.read_bytes()
    assert hashlib.sha256(data).hexdigest() == hashes[p.name]
    images[p.name] = data


def encode_dialogue(text):
    """Uppercase ASCII is supported; punctuation needs full-width CP932.

    @ = newline, {decimal ID} = existing $+byte name substitution.
    Other script commands cannot be introduced through this encoder.
    """
    text = re.sub(r"([,.]) +", r"\1", text)
    data = bytearray()
    for token in re.findall(r'\{\d+\}|.', text):
        if token.startswith('{'):
            data.extend((0x24, int(token[1:-1])))
        elif token in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ @':
            data.extend(token.encode('ascii'))
        elif token in ",.?!'":
            data.extend(chr(ord(token) + 0xFEE0).encode('cp932'))
        else:
            raise ValueError(f'Unsupported dialogue character: {token!r}')
    return bytes(data)


def fullwidth(text):
    return ''.join(chr(ord(c) + 0xFEE0) for c in text).encode('cp932') + b'\0'


translations = [
    ('LUCIA', 'DONE EATING,@DEAR?'),
    ('JIDO', "YES. {14} AND@I WILL STUDY@YESTERDAY'S@METEOR."),
    ('SION', 'I WANT TO SEE@THE METEOR@TOO!'),
    ('LUCIA', "NO, {0}.@YOU'RE STILL@TOO YOUNG."),
    ('JIDO', "{0}, I'M FREE@TOMORROW.@SHALL WE VISIT@{6}?"),
    ('SION', 'UNCLE {6}?@THE ONE@IN DUST?'),
    ('LUCIA', 'YOU REMEMBER@{0}? HE USED@TO PLAY WITH@YOU A LOT.'),
    ('SION', 'OF COURSE!@HE MADE ME@TOYS OUT OF@SCRAP.'),
    ('SION', 'I LIKE@UNCLE {6}!'),
    ('JIDO', '{6} WILL BE@HAPPY TO HEAR@THAT.'),
]
# Desktop screenshots from 2026-09-20 show ASCII letters occupying full cells.
# Use a conservative 14-cell line and four body rows, counting expanded names.
display_names = {0: 'SION', 6: 'JOE', 14: 'MAMON'}
for speaker, text in translations:
    expanded = re.sub(r'\{(\d+)\}', lambda m: display_names[int(m[1])], text)
    lines = expanded.split('@')
    assert len(lines) <= 4, (speaker, lines)
    assert all(len(line) <= 14 for line in lines), (speaker, lines)
original = images['Alshark (System Disk).hdm']
system = bytearray(original)
start, end = 0x51056, 0x51243
scene = original[start:end]
assert scene[-1] == 0
matches = list(re.finditer(rb'4\$(.)5', scene, re.S))
assert [m.group(1)[0] for m in matches[:7]] == [12, 16, 0, 12, 16, 0, 12]
parts = []
cursor = 0
dialogue_manifest = []
assert len(matches) == len(translations) == 10
for match, (speaker, text) in zip(matches, translations):
    a = match.end()
    z = scene.index(b'0', a)  # Page-end opcode; SJIS trail bytes cannot equal 0x30.
    old = scene[a:z]
    parts.extend((scene[cursor:a], encode_dialogue(text)))
    cursor = z
    dialogue_manifest.append(dict(speaker=speaker, source_offset=hex(start+a),
                                  source=old.decode('cp932'), translation=text))
tail = scene[cursor:]
old_farewell = '@じｬｱ、行ｯﾃｸﾙﾖ。'.encode('cp932')
assert tail.count(old_farewell) == 1
farewell = "WELL, I'M OFF."
assert len(farewell) <= 14
tail = tail.replace(old_farewell, encode_dialogue('@' + farewell))
parts.append(tail)
new_scene = b''.join(parts)
assert len(new_scene) <= len(scene), 'Scene exceeds its existing allocation'
system[start:end] = new_scene.ljust(len(scene), b'\0')
assert system[0x51000:start] == original[0x51000:start]  # All 43 entry pointers unchanged.
assert system[end:0x52000] == original[end:0x52000]  # Other scene entries untouched.

# $+ID resolves a pointer at table base 0x10400, relative to 0x10000.
# Name insertion lacks the dialogue's uppercase-ASCII conversion, so names use
# full-width CP932. Reuse only the selected characters' existing storage spans.
# Short/full-name IDs share a given name in this limited experiment.
storage = [
    (0x111DB, 0x111EA, [('LUCIA', [12, 13])]),
    (0x11207, 0x11214, [('MAMON', [14, 15])]),
    (0x11235, 0x1125A, [('JIDO', [16]), ('SION', [0, 1]),
                           ('COSMA', [81])]),
    (0x114BF, 0x114C9, [('JOE', [6, 7])]),
]
if args.include_town:
    # Repack only already-used name spans; preserve the later Karu variant ID 5.
    storage = [
        (0x111DB, 0x111EA, [('COSMA', [81])]),
        (0x11207, 0x11214, [('LUCIA', [12, 13])]),
        (0x11235, 0x1125A, [('MAMON', [14, 15]), ('JIDO', [16]),
                           ('SION', [0, 1]), ('JOE', [6, 7])]),
        (0x114BF, 0x114C9, [('KARU', [4])]),
    ]
assert original[0x11255:0x1125A] == 'ジド'.encode('cp932') + b'\0'
assert struct.unpack_from('<H', original, 0x104A2)[0] == 0x14BF
if args.include_area:
    # IDs 2/3 already occupy this contiguous span. Both use the given name in
    # this draft; no other names or pointers share these original strings.
    assert original[0x111ea:0x111fd] == 'ｼｮｰｺ\0ｼｮｰｺ・ペﾝﾛｰズ\0'.encode('cp932')
    storage.append((0x111ea, 0x111fd, [('SHOKO', [2, 3])]))
names = []
for a, z, entries in storage:
    data = bytearray()
    for name, ids in entries:
        dest = a + len(data)
        if name == 'COSMA':
            data.extend(b' >')
        data.extend(fullwidth(name))
        for ident in ids:
            struct.pack_into('<H', system, 0x10400 + ident * 2, dest - 0x10000)
        names.append(dict(name=name, ids=ids, disk_offset=hex(dest)))
    assert len(data) <= z-a
    system[a:z] = data.ljust(z-a, b'\0')

# Build the next conversation through the command-aware importer. Transplant
# only its unchanged allocation into this demo's independently patched image.
followup = None
if args.include_followup:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from profiles.alshark.script_tool import export_disk, import_disk
    document = export_disk(original)
    entry = next(e for e in document['entries'] if e['id'] == '051000:001')
    token = next(t for t in entry['tokens'] if t['id'] == 't006')
    token['translation'] = ',\nGO PLAY, BUT\nSTAY AWAY FROM\nTHE METEOR!'
    rendered = 'SION' + token['translation']
    if len(rendered.splitlines()) > 4 or any(len(line) > 14 for line in rendered.splitlines()):
        raise ValueError('Follow-up text exceeds the tested layout')
    imported = import_disk(original, document)
    a, n = entry['offset'], entry['size']
    if imported[:a] != original[:a] or imported[a+n:] != original[a+n:]:
        raise ValueError('Importer changed bytes outside the follow-up entry')
    system[a:a+n] = imported[a:a+n]
    followup = dict(entry_id=entry['id'], translation=token['translation'],
                    status='User verified follow-up display and dismissal on 2026-09-20')

town = []
if args.include_town:
    from profiles.alshark.layout import validate_dialogue
    document = export_disk(original)
    edits = json.loads((ROOT / 'town-draft.json').read_text(encoding='utf-8'))
    for entry in document['entries']:
        if entry['id'] not in edits:
            continue
        by_id = {t['id']: t for t in entry['tokens']}
        for token_id, translation in edits[entry['id']].items():
            if by_id[token_id]['kind'] != 'text':
                raise ValueError('Town draft targets a non-text token')
            by_id[token_id]['translation'] = translation
        validate_dialogue(entry['tokens'], {0: 'SION', 4: 'KARU'})
        town.append(dict(entry_id=entry['id'], offset=entry['offset'], size=entry['size']))
    if len(town) != len(edits):
        raise ValueError('Missing town draft entries')
    imported = import_disk(original, document)
    for entry in town:
        a, n = entry['offset'], entry['size']
        system[a:a+n] = imported[a:a+n]

pickups = []
if args.include_pickups:
    document = export_disk(original)
    edits = json.loads((ROOT / 'pickup-draft.json').read_text(encoding='utf-8'))
    if args.include_review:
        # Single-line names avoid the observed colour reset after a newline.
        # Match the short labels used in the inventory table in this draft.
        edits['051000:034']['t001'] = 'KNIFE'
        edits['051000:035']['t001'] = 'MEDS'
    by_entry = {e['id']: e for e in document['entries']}
    for entry_id, translations_by_token in edits.items():
        entry = by_entry[entry_id]
        by_token = {t['id']: t for t in entry['tokens']}
        for token_id, translation in translations_by_token.items():
            if by_token[token_id]['kind'] != 'text':
                raise ValueError('Pickup draft targets a non-text token')
            by_token[token_id]['translation'] = translation
        pickups.append(dict(entry_id=entry_id, offset=entry['offset'], size=entry['size']))
    suffix = by_entry['051000:041']['tokens']
    for entry_id in edits:
        if entry_id == '051000:041':
            continue
        # Inline only the reviewed bank-0/entry-41 call for layout checking.
        tokens = []
        for token in by_entry[entry_id]['tokens']:
            if token['kind'] == 'command' and token['raw'] == '2350020029':
                tokens.extend(t for t in suffix if t['kind'] != 'end')
            else:
                tokens.append(token)
        # Screenshot review: 16 cells clips the final punctuation; use 15.
        if entry_id == '061000:019':
            validate_dialogue(tokens, {0: 'SION', 12: 'LUCIA'}, columns=14)
        else:
            validate_dialogue(tokens, {}, columns=15)
    imported = import_disk(original, document)
    for entry in pickups:
        a, n = entry['offset'], entry['size']
        system[a:a+n] = imported[a:a+n]

area = []
if args.include_area:
    document = export_disk(original)
    edits = json.loads((ROOT / 'area-draft.json').read_text(encoding='utf-8'))
    if args.include_review:
        edits.update({
            '051000:005': {'t001': 'ELDER'},
            '061000:021': {'t004': "NOT MINE.\nCAN'T TAKE IT"},
        })
    for entry in document['entries']:
        if entry['id'] not in edits:
            continue
        by_token = {t['id']: t for t in entry['tokens']}
        for token_id, translation in edits[entry['id']].items():
            if by_token[token_id]['kind'] != 'text':
                raise ValueError('Area draft targets a non-text token')
            by_token[token_id]['translation'] = translation
        validate_dialogue(entry['tokens'], {0: 'SION', 2: 'SHOKO', 4: 'KARU', 12: 'LUCIA'})
        area.append(dict(entry_id=entry['id'], offset=entry['offset'], size=entry['size']))
    if len(area) != len(edits):
        raise ValueError('Missing area draft entries')
    imported = import_disk(original, document)
    for entry in area:
        a, n = entry['offset'], entry['size']
        system[a:a+n] = imported[a:a+n]

opening = bytearray(images['Alshark (Opening Disk).hdm'])
for old, new, offsets in [
    ('最初から始める', 'ＳＴＡＲＴ', [0x470C, 0x4B0C]),
    ('ロードスタート', 'ＬＯＡＤ', [0x471B, 0x4B1B]),
]:
    for off in offsets:
        assert opening[off:off+14] == old.encode('cp932')
        opening[off:off+14] = new.ljust(7, '\u3000').encode('cp932')

menus = []
combat_text = []
if args.include_area:
    from profiles.alshark.menu_patch import patch_menus
    menus = patch_menus(opening, system, reviewed=args.include_review)
if args.include_review:
    from profiles.alshark.combat_text import patch_combat_text
    combat_text = patch_combat_text(system, original)

menu_geometry = []
if args.widen_menus:
    from profiles.alshark.menu_layout import widen_menus
    menu_geometry = widen_menus(opening, system)

menu_strings = []
if args.expand_menu_labels:
    from profiles.alshark.menu_strings import expand_menu_strings
    menu_strings = expand_menu_strings(opening)

disk_prompts = None
if args.translate_disk_prompts:
    from profiles.alshark.disk_prompts import patch_disk_prompts
    disk_prompts = patch_disk_prompts(opening)

localization_records = []
if args.localization:
    from profiles.alshark.localization import BIBLE, compile_adaptations
    localization_document = json.loads(args.localization.read_text(encoding='utf-8'))
    localized, localization_records = compile_adaptations(
        {disk: images[f'Alshark ({disk} Disk).hdm'] for disk in ('Opening', 'System')},
        localization_document, json.loads(BIBLE.read_text(encoding='utf-8')),
        scenes=args.localization_scenes)
    for record in localization_records:
        a, n = record['offset'], record['size']
        system[a:a+n] = localized[a:a+n]


def make_ips(old, new):
    patch = bytearray(b'PATCH')
    i = 0
    while i < len(old):
        if old[i] == new[i]:
            i += 1
            continue
        start = i
        while i < len(old) and old[i] != new[i] and i-start < 65535:
            i += 1
        patch.extend(start.to_bytes(3, 'big') + (i-start).to_bytes(2, 'big') + new[start:i])
    patch.extend(b'EOF')
    # Verify the distributable patch independently reproduces the output.
    restored = bytearray(old)
    pos = 5
    while patch[pos:pos+3] != b'EOF':
        off = int.from_bytes(patch[pos:pos+3], 'big')
        size = int.from_bytes(patch[pos+3:pos+5], 'big')
        pos += 5
        restored[off:off+size] = patch[pos:pos+size]
        pos += size
    assert restored == new
    return patch


manifest = dict(status='Reflowed after screenshot review; revised wrapping awaiting runtime verification',
                dialogue=dialogue_manifest, names=names, followup=followup, town=town, pickups=pickups,
                area=area, menus=menus, combat_text=combat_text, menu_geometry=menu_geometry,
                menu_strings=menu_strings,
                localization=localization_records, disk_prompts=disk_prompts,
                localization_scope=dict(selected_scenes=args.localization_scenes,
                    deferred=[dict(id=r['id'], status=r['target']['status'], reason=r['target']['reason'])
                              for r in localization_document['records']
                              if r['canonicalEnglish'] is not None and args.localization_scenes is not None
                              and r['scene'] not in args.localization_scenes]) if args.localization else None,
                scene_original_bytes=len(scene), scene_used_bytes=len(new_scene), disks=[])
for name, original in images.items():
    modified = {'Alshark (System Disk).hdm': system,
                'Alshark (Opening Disk).hdm': opening}.get(name)
    dest = OUT / name
    if modified is None:
        if not dest.exists():
            dest.write_bytes(original)
        continue
    assert len(modified) == len(original)
    dest.write_bytes(modified)
    (OUT / (Path(name).stem + '.ips')).write_bytes(make_ips(original, modified))
    manifest['disks'].append(dict(name=name, source_sha256=hashlib.sha256(original).hexdigest(),
                                 patched_sha256=hashlib.sha256(modified).hexdigest()))
(OUT / 'patch-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
(OUT / 'Alshark-dialogue-test.cmd').write_text('np2kai ' + ' '.join(
    '"'+str(OUT/f'Alshark ({n} Disk).hdm')+'"' for n in ['Opening', 'Data'])+'\n')
print(f'Built ten speech turns, farewell, {len(names)-1} character names and Cosma title: scene {len(new_scene)}/{len(scene)} bytes; IPS round-trips pass.')

if followup:
    print('Included Lucia follow-up via the script importer; branch and entry allocation preserved.')

if town:
    print(f'Included {len(town)} town conversations via importer; layout checks passed.')

if pickups:
    print('Included four pickup labels, shared FOUND message and Lucia interruption; visual verification pending.')

if area:
    print(f'Included {len(area)} additional town/branch entries and {len(menus)} UI strings; runtime verification pending.')

if menu_geometry:
    print('Widened field/battle menus from five to six cells and highlights from 10 to 12 VRAM bytes; runtime verification pending.')
if menu_strings:
    print('Relocated six menus with expanded labels including YES/NO; runtime verification pending.')
