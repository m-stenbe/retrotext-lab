# Conservative Alshark script export/import

The tool supports the original System disk hash recorded in the profile. It
exports locally generated JSON; do not commit the extracted game script.

```sh
python3 profiles/alshark/script_tool.py export \
  '/path/to/Alshark (System Disk).hdm' work/script.json
python3 profiles/alshark/script_tool.py import \
  '/path/to/Alshark (System Disk).hdm' work/script.json \
  --output work/rebuilt.hdm
```

Keep the original disk separate. Import rejects either input as an output path.
The output image is built from the supplied original, not from the previous demo;
it does not include the demo's menu/name patches. Do not write to an image mounted
in an emulator. A normal rebuild replaces an existing output file.

## Editing

Entries have stable IDs based on original bank address and entry index. Tokens
have IDs based on their position in the original entry. Each text token contains
`source`, exact original `raw` bytes, and a `translation` initially set to null.
Only change `translation`. Leave null to preserve the original bytes exactly.
An empty string deliberately removes that text span.

Translations currently accept uppercase A–Z, digits 0–9, spaces, newline characters and
`, . ? ! '`. Newlines become the game's `@` instruction; punctuation is encoded
as full-width CP932. Digits encode as full-width CP932 glyphs, never ASCII script opcodes.
Lowercase and command characters are rejected rather
than silently interpreted as script instructions. Spaces are not removed.

Name references are separate immutable tokens with `name_id`, so text on either
side is edited separately. Names themselves stay Japanese in this tool. Speaker,
page and event commands remain immutable; this format does not allow changing
page breaks, branch logic, or name reference order.

Entries `051000:000` (opening breakfast), `051000:001` (Lucia's follow-up),
`051000:007`, `051000:009` (town residents), and `051000:010` (Karu) are editable.
The user verified Lucia's follow-up display and return to movement. The three
new entries still await visual verification. All other entries remain research-only until their references
have been checked. The document format is now `retrotext-alshark-v2`; re-export
from the original disk when using this decoder. Older documents are rejected.

An edit must fit within its original entry allocation. Following entry pointers
are unchanged. Any opaque suffix stays at its original offset. Shorter scripts
are padded after their top-level terminator. No byte-space expansion, branch
relocation, or automatic text wrapping is implemented. Byte capacity checks do
not guarantee that text fits the on-screen box; the opening experiment uses a
conservative 14 full-width cells per line and four body rows, including names.

## Decoder evidence and boundaries

Disassembly offsets below are offsets in the supported original System image.

- `0xF2E2`: reads a byte; zero returns from the text/script routine.
- `0xF4BA`: character dispatch table. It distinguishes commands from letters.
- `0xF44F`/`0xF45A` lead into command dispatch. `0xF471` and `0xF480`
  read the argument count. Thus `#`/`?`, command byte, length byte and payload
  form an indivisible token. The decoder preserves payloads; it does not claim
  to understand every command's behavior or references.
- `0xF38D`: `$` consumes the next byte as a name ID. ID zero is valid and must
  not terminate the entry.
- The decoder now recognizes every control in the dispatch table. `0`–`6`,
  `_`, `!`, `>`, `/` consume no arguments; `$`, `(` and `=` consume one byte.
  Spaces and `@` remain part of editable text. See the evidence below for the
  newly added classes. Recognizing a token boundary is not full semantic analysis.
- CP932 pairs are consumed together, including trail bytes that look like `@`
  or other ASCII syntax. Unedited raw bytes are retained rather than relying
  on a potentially noncanonical decode/encode roundtrip.

Unknown controls, malformed pairs, truncated commands and missing terminators
reject the entire entry. There is no resynchronization by searching for a later
speech marker. Anything after the first top-level zero remains an opaque suffix;
it may include padding, stale data or a branch destination. Static decoding does
not establish reachability or behavior. The physical 4 KB window end is still
an inventory boundary, not a proven universal loader limit.

## Additional control and branch evidence

| Byte | Handler | Observed behavior |
| --- | --- | --- |
| `1` | `0xF2DB` | Sets BX=0x050F, INT 41h AH=7, resumes script |
| `2` | `0xF365` | Sets BX=0x050A, same display-service call |
| `3` | `0xF36B` | Sets BX=0x0A0E, same display-service call |
| `6` | `0xF371` | Sets BX=0x090D, same display-service call |
| `!` | `0xF353` | CX=60, calls delay routine, resumes script |
| `>` | `0xF350` | Advances DI by one; no argument |
| `/` | `0xF3EC` | Toggles display mode byte 0x1D5C; no argument |
| `(` | `0xF3F7` | Consumes one selector, selects numeric display data |
| `=` | `0xF441` | Consumes one selector for a display helper |

The four numeric controls use the same service as the known colour controls.
Their exact visual colours are not required for extraction. A zero argument to
`(` or `=` is consumed as data, not as the script terminator.

Lucia's follow-up at 0x51243..0x51282 begins with `#Z` (2 arguments), the
speaker header, then `#B` with arguments 2 and 14. The # command lookup table at
0x33EB maps Z to 0xD7F0 and B to 0xD778. Z consumes its two settings and returns
to payload-start + argument-count (0xD7FF). B tests its first argument; if the
condition selects the other path, 0xD723 consumes the second argument as an
entry index, doubles it, and reads a pointer from the table at RAM 0x23EB.
Otherwise it resumes after the payload. The branch does not encode an offset
into this conversation's text. The importer leaves the table and payload fixed.
The branch target itself has not been translated by this change.

## Validation on 2026-09-20

- First version: 1,994 entries decoded and 255 skipped.
- Current version: all 2,249 inventoried entries decoded; **zero skipped**;
  4,528 text spans exposed. These are not dialogue-box or word counts, and
  exclude opaque suffixes, other disk regions and graphical text.
- Unchanged import reproduced all 1,261,568 System-disk bytes exactly.
- A local follow-up translation changes only the 64-byte allocation starting
  at 0x51243. Its command payloads, names and table pointers remain identical.
- Twenty synthetic tests cover token framing, binary arguments, text changes,
  unchanged import, branch preservation, read-only entries, metadata tampering,
  malformed input, overflow and unsupported translation characters.
- The default demo still reproduces the previous six output images exactly.

## Follow-up test build

```sh
python3 profiles/alshark/build_demo.py /path/to/original \
  --output work/importer-test --include-followup
```

This optional build applies the new importer to the original disk, then copies
only the follow-up entry into the existing English demo. Breakfast/menu/name
patches remain from the older builder. This is not yet an importer-driven build
of the entire demo. The follow-up says: SION, / GO PLAY, BUT / STAY AWAY FROM /
THE METEOR! All four lines are checked against the tested 14-cell limit.

After starting a new game and finishing breakfast, speak to Lucia to look for
the warning. Its conditional branch means a later story state may select another
conversation instead. Use this build's System disk when swapping.

The user verified the imported warning displays correctly and dismisses back to normal movement. The original demo
remains available, and existing playable images are unchanged. Next: validate
the follow-up in-game and map more branch targets before enabling broader edits.

## Karu and town test — 2026-09-20

`--include-town` implies `--include-followup`. English-only drafts live in
`profiles/alshark/town-draft.json`; extracted Japanese stays in ignored work files.

| Entry | Content | Review |
| --- | --- | --- |
| 051000:007 | Greenery and dangerous bugs near the lake | No event commands; fixed allocation |
| 051000:009 | Canyon to the north | No event commands; fixed allocation |
| 051000:010 | Karu observes Sion's pulse/sweat and asks what he is plotting | #B branches by entry index; #Z portrait/settings; immutable payloads |

Karu's #B branches retain argument pairs (16, 19) and (2, 16). These select other
entries under other story flags, so not all possible responses are translated.
The original short name reads カル (Karu); this spelling and SAXEN remain draft
romanizations. The short English wording is constrained by the current font and
allocation. The lake warning is condensed, retaining greenery, large bugs, the
lake location and danger. Karu's last question becomes PLOTTING?

The town build repacks only the existing demo name-storage spans. It adds name
ID 4 as full-width KARU and preserves the other translated display strings.
Name ID 5, its pointer and original storage are untouched. Since ID 4 is shared,
the short name changes wherever that ID is used, including untranslated dialogue.

The new layout checker includes expanded names, distinguishes speaker headers
from body text, and does not clear rows at the wait opcode `0`. It intentionally
rejects unreviewed display modes; it is not a universal rendering simulator.

All three edited command streams remain byte-identical when text is excluded.
Only their allocations, selected name pointers and existing name-storage spans
change relative to the previous importer test. Original disk and pointer tables
remain intact. The default demo output still matches the previous six images.

A separate local town-test launcher is prepared. The running importer test is
not modified or restarted. To check: launch the new build, use its System/Data
disks, start fresh, speak to Karu and the two town residents. Confirm layout and
normal movement after dismissing each conversation. New town coverage remains
unverified in the emulator until those checks are performed.

## Starting-house pickups — 2026-09-20

`--include-pickups` implies `--include-town` and `--include-followup`. It adds
editable entries 051000:034, :035, :036, :037 and :041. Re-export documents when
updating the tool so their read-only metadata matches the current profile.
English-only drafts live in `profiles/alshark/pickup-draft.json`.

The labels are SURVIVAL / KNIFE, HAND / MEDICAL, PROTECTOR, and 80 / CREDITS.
The common suffix is a space followed by FOUND! Item labels retain control `3`
(yellow in the observed game); the suffix retains control `6` (blue). Inventory
and equipment menu names are outside this patch. HAND MEDICAL is a provisional
literal item label; its gameplay function has not been checked.

### Call and award preservation

All four entries call bank 0, entry 41 through `#P` with payload 00 29. The
handler at System offset 0xDA3F saves SI/current bank, consumes a bank number and
entry index, loads the bank, resolves its relative-pointer table at RAM 0x23EB,
calls the display interpreter, restores the bank/SI and advances SI by two.
The translation does not change this call or the item-award/branch payloads.
Exactly four decoded calls to this bank/entry pair were found in the selected
inventory. This does not prove absence of callers in opaque or unscanned data.

All five rebuilt entries preserve their complete non-text token sequences.
The image differs from the town build only in these allocations, with no pointer
table, name, file-size, or other image changes. Unchanged full-disk import is
still byte-identical to the original.

### Layout and validation limits

Long labels split before the suffix call. The suffix itself does not insert a
newline: the #P handler enters the display interpreter with the current cursor,
so its line origin is not necessarily the left edge of the box.

The pickup draft uses a 16-cell budget instead of the conservative 14 used for
conversation text. PROTECTOR FOUND! occupies all 16 cells and specifically needs
an emulator check; the budget is experimental, not a proven general box width.
The layout checker inlines the reviewed suffix for measurement and preserves
columns across colour changes. It is not a full interpreter for arbitrary calls.

Digits now use the game's original full-width numeral encoding. A synthetic
test confirms that 80 becomes the two CP932 glyphs rather than executable ASCII
`8`/`0` bytes. A colour-layout test checks that switching colour does not reset
the current column. All 20 tests pass.

The local pickup-test launcher is ready. Start a fresh game, use its System and
Data images, search the starting-house shelves, and verify the translated labels,
yellow/blue colours, message dismissal and awarded equipment/credits. The current
session is not restarted and earlier test images are not overwritten. In-game
verification of these new pickup messages remains pending.

### Pickup screenshot correction, 15:25

The user's screenshot confirms the yellow item label and blue suffix. The final
exclamation mark in PROTECTOR FOUND! clips at the right border, so the 16-cell
trial was too wide. The suffix is now a space followed by FOUND (no punctuation),
and the pickup layout budget is 15 cells. A regression test rejects the former
16-cell text. This revision is built separately to avoid changing mounted images;
the revised right-edge spacing still needs visual verification. Item awards and
message dismissal are not established by the screenshot alone.

### Lucia interruption after searching the shelves

User screenshots at 15:31 show Lucia asking Sion what he is doing and Sion
reacting that he has been caught. The shared entry is 061000:019, called through
bank 16/entry 19 by the Protector pickup. It contains only the already-reviewed
#Z settings command, speaker/name/display controls and text. It is now editable
and included with --include-pickups.

The 48-byte allocation allows 29 bytes of text. The concise draft is SION! /
WHAT'S GOING / ON? followed by BUSTED. Both fit the 14-cell conversation limit
and the original allocation. Command bytes and name references remain identical;
the new image differs from pickup v2 only in this one entry. New English dialogue
awaits visual verification. The prior screenshot confirms PROTECTOR FOUND fits
with both colours. Finding an item does not by itself confirm it was awarded:
Lucia can interrupt the attempt. Award/branch commands are unchanged.

## Larger area draft and fixed UI strings — 2026-09-20

`--include-area` implies all earlier demo flags and adds the 19 entries listed
in `area-draft.json`. The editable allowlist now contains 30 entries. Re-export
older documents before editing: the importer rejects stale editable metadata.

New choice paths retain `#Y` argument bytes. Disassembly at System `0xD858`
saves/restores SI around the choice UI, indexes the counted payload with the
selected answer, then jumps to `0xD723`. That routine resolves an entry index
through the existing relative-pointer table at RAM `0x23EB`. Thus the two
choice targets remain entries 11/12 when text within entry 2 or 13 changes.
`#S`, `#M` and `#N` iterate counted flag arguments; `#W` consumes its one-byte
argument and preserves SI across its calls. `#X` processes its counted payload
and returns at its end. These commands, existing conditional entry branches,
name references, wait/clear controls and entry allocations stay unchanged.
This structural review does not replace testing every game-state branch.

Shoko name IDs 2/3 reuse only their original combined `0x111EA..0x111FD` storage,
with full-width SHOKO. Both resolve to the same given name in this prototype.

`menu_patch.py` uses a separate full-width CP932 encoder. Its eight guarded
replacements cover the field, System and text-speed menu strings, two copies
of the no-equipment message, empty inventory, and the name separator/body of
the no-abilities message. Complete menu strings retain their start addresses,
row counts and order; their internal row positions change. They are terminated
and padded within the original allocation. Source mismatches and overflow
fail before that string is mutated. No UI code or disk size changes.
Selection/highlighting and any possible internal UI references still need
runtime confirmation. Abbreviations and remaining untranslated UI are listed
in the playtest notes.

Validation: 24 synthetic tests pass, original System export/import is exact,
all 19 new entry command/name/control streams match their originals, and the
new System differences against pickup-v3 are confined to the declared entries,
Shoko storage/pointers and three UI message areas. The default six demo images
still match the earlier default build. Each generated IPS independently
reproduces its output image. New runtime coverage remains unverified.

## Screenshot-review UI and runtime fields — 2026-09-20

`--include-review` implies `--include-area`. It adds two editable event entries
(the elder's header and shared pickup refusal), bringing the allowlist to 32.
Their counted command payloads, waits and entry allocations remain unchanged.
Re-export older translation documents after this allowlist change.

The UI patch list grows to 24 guarded string regions. Selected item/location
strings are edited in place without repointing their name tables. Choice/menu
row counts and ordering remain unchanged. Some short labels are deliberately
abbreviated; see playtest notes for scope and outstanding gaps.

Shared result scripts at System `0x1EDF..0x1F28` and `0x1F28..0x1FD8` are
handled separately by `combat_text.py`. In particular, the level-up name ID can
change at runtime (the screenshots show both Sion and Shoko). Repacking this
script could move a field addressed by the game, so every edited text token
retains its original byte length. ASCII uppercase and equivalent full-width
CP932 uppercase glyphs are mixed to fill the span without adding visible cells.
This relies on the script renderer's existing support for both forms; it is
not a narrower font or an expanded allocation. Insufficient/excess capacity
rejects the edit. All edits in a script are checked before mutation.

Verification: 27 synthetic tests pass. A fixture simulates a runtime name-ID
write at its original address after text replacement. Local image checks verify
all non-text token bytes and offsets in both result scripts, normalized English
text, original export/import roundtrip, allowed disk-change regions, IPS
roundtrips and unchanged output of the previous `--include-area` build.
Screenshots are still needed to verify the new UI and result text visually.

## Menu geometry experiment — 2026-09-21

The six-byte menu records start at Opening disk `0x3FD9`, loaded as driver
address `0x1FD9`. Fields are width, row count, screen-position word and a
little-endian text pointer. Driver `0x1F0C` multiplies the menu ID in BL by six,
reads width into CL, rows into BL and position into DI, then calls the animated
box renderer at `0x150B` (Opening file `0x350B`). That renderer stores the target
width/height at `0x13AC/0x13AD` and draws 16-pixel-wide tiles until reaching them.
Text rendering starts at the unchanged box origin plus `0x0504`.

| Menu | ID | Opening record | Original bytes | New width |
| --- | --- | --- | --- | --- |
| Normal field | 00 | 3FD9 | 05 06 04 0F 58 21 | 6 |
| Alternate field | 01 | 3FDF | 05 07 04 0F 4D 21 | 6 |
| On-foot battle | 0B | 401B | 05 06 04 0F F8 23 | 6 |

The selection highlight is separate. System `0x1730` reads a byte count from
`0x1D3E` and XORs the corresponding VRAM width. The battle caller at `0x81CE`
and shared field caller at `0x98B6` each contain `C6 06 3E 1D 0A`, setting ten
VRAM bytes (80 pixels / five full-width cells). The experiment changes only
the immediate to `0C`, making the highlight twelve bytes / six cells wide.
Both field records must widen because their paths share that width assignment.
Text pointers, menu heights, positions and action-index dispatch remain intact.

`--widen-menus` implies `--include-review`. `menu_layout.py` guards all three
complete records and both complete instructions before changing either image.
The actual output differs from the reviewed build at exactly five byte offsets:
Opening `3FD9`, `3FDF`, `401B` (05 to 06), System `81D2`, `98BA` (0A to 0C).
Other content disks are identical. Tests cover atomic rejection, exact changed
fields and matched box/highlight widths. All 30 tests pass; six-row field and
battle labels fit the new six-cell interior in the local build check.

Runtime confirmation is still needed for box animation/borders, selected-row
highlighting, opening submenus, cancellation and screen restoration. This
experiment adds screen room only; it does not expand label storage or translate
additional text. Later vehicle/ship battle menus are outside this patch.
