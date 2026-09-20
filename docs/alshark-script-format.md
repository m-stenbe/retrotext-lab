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

Translations currently accept uppercase A–Z, spaces, newline characters and
`, . ? ! '`. Newlines become the game's `@` instruction; punctuation is encoded
as full-width CP932. Lowercase, ASCII digits and command characters are rejected rather
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
- Eighteen synthetic tests cover token framing, binary arguments, text changes,
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
