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
as full-width CP932. Lowercase, digits and command characters are rejected rather
than silently interpreted as script instructions. Spaces are not removed.

Name references are separate immutable tokens with `name_id`, so text on either
side is edited separately. Names themselves stay Japanese in this tool. Speaker,
page and event commands remain immutable; this format does not allow changing
page breaks, branch logic, or name reference order.

Only entry `051000:000` (the verified opening breakfast scene) is editable for
now. Other decoded entries are research-only. This is an intentional guard until
control-flow references have been checked for each supported class of entry.

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
- The tested opening uses `0`, `4`, `5`, `_`, `@`, spaces, uppercase Latin,
  half-width kana, CP932 two-byte characters and the counted commands above.
- CP932 pairs are consumed together, including trail bytes that look like `@`
  or other ASCII syntax. Unedited raw bytes are retained rather than relying
  on a potentially noncanonical decode/encode roundtrip.

Unknown controls, malformed pairs, truncated commands and missing terminators
reject the entire entry. There is no resynchronization by searching for a later
speech marker. Anything after the first top-level zero remains an opaque suffix;
it may include padding, stale data or a branch destination. Static decoding does
not establish reachability or behavior. The physical 4 KB window end is still
an inventory boundary, not a proven universal loader limit.

## Validation on 2026-09-20

- 1,994 entries decoded; 255 skipped from the 2,249-entry inventory.
- 2,376 text spans exposed (not dialogue-box or word counts).
- Skipped first unsupported controls: `6` (106), `3` (87), `!` (54),
  `1` (6), `2` (2). They are known dispatch-table symbols, but their semantics
  and effects are deliberately not implemented in this first decoder.
- Unchanged import reproduced all 1,261,568 System-disk bytes exactly.
- A local first-line translation changed only the opening entry allocation;
  all parsed non-text command tokens remained identical.
- A change to a read-only entry was rejected.
- Synthetic tests cover binary zeros in arguments/name IDs, CP932 trail-byte
  ambiguity, opaque suffix positioning, tampering, malformed input, overflow,
  unsupported translation characters and wrong image hashes.

The new importer output has not yet been tested in the emulator. The old demo
builder remains available and the user's existing playable images are unchanged.

Next: decode the five remaining control classes, map branch-reference behavior,
and enable a second scene after establishing its relocation constraints.
