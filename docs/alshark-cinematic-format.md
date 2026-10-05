# Meteor cinematic adapter

The meteor cinematic is a different interpreter from the opening introduction.
The active code is on System at `0x14000`; the visually similar interpreter at
Opening `0x20000` has different `#X` semantics and must not be used as its spec.
This adapter covers the complete meteor stream, not every cinematic in the game.

## Loader and allocation evidence

System-relative `0x0044` records the cinematic selector from DL. At `0x0066`
the loader selects the four-byte descriptor at `0x105B + selector*4`, reads into
CS:8000, then at `0x00B4` follows the first word relative to 8000. Selector zero's
original descriptor is `00 67 07 08`: eight 1024-byte sectors beginning at
Opening `0xCF800`. Its entry pointer is `0x0F8E`, hence stream start `0xD078E`.
The original stream ends with its top-level zero at `0xD0F67`.

The animation index table occupies the beginning of that block. Its frame
references precede the stream. `#P` and animation registration handlers read
that table; they do not encode offsets into dialogue. The entire decoded meteor
stream is sequential: no included handler branches into its text. Rebuilding
from the unchanged entry pointer through at most block end `0xD1800` therefore
provides 4,210 bytes without changing the loader, frame indices or pointers.
The bytes after the original terminator include stale repeated text and zeros;
they are unreachable by this stream. The adapter does not assume they are an
independent free-space pool: it uses only this loaded stream's remaining extent.
Original disk hashes, complete block hash, entry pointer and interpreter hash
are retained in source provenance. Unused tail bytes remain unchanged.

## Text, animation and layout

System-relative `0x03AF` reads each byte. `0x043A` checks registered animation
identifiers before ordinary text processing; standalone A–G are animation
triggers in this scene. `#M/#D/#A/#B` register a trigger byte and a zero-terminated
frame-index sequence (`#M` also consumes one speed byte). `#L` loads an image and
clears registrations through `0x02AE`. The decoder tracks registrations and
refuses unknown top-level bytes.

`0x03D8` handles half-width kana `A6..DD`; otherwise text consumes a CP932 pair
at `0x03EB`. Ordinary ASCII English is unsafe. The adapter encodes Latin letters
and digits as full-width CP932 and punctuation as corresponding supported glyphs.
ASCII space remains the explicit space instruction. It preserves whitespace-only
runs, including the timing between the three gunshot effects.

The original dimensions at System `0x15046` and `0x15048` are 25 columns and five
rows. Each glyph increments the column; column 25 automatically advances a row.
`@` explicitly advances a row; reaching row five clears the text through `0x0393`.
`_` consumes a clear-mode operand and resets the cursor. `/` consumes a text-speed
operand, with FF restoring six ticks. `!` delays 60 ticks without resetting the
cursor. The adapter composes all text and original controls and rejects any
adaptation that would accidentally reach the automatic page clear.

The original commands, animation triggers, explicit page/line controls, text
speeds, sound IDs and terminator survive byte-for-byte and in order. Text length
changes naturally affect typewriter duration and animation cycles; this is not
frame-identical playback. No new page or line commands are inserted. `#X` in this
interpreter consumes one byte and sets the per-glyph sound selector (`0x084E`),
not the introduction interpreter's special-function dispatch. Other included
commands have individually decoded fixed operands; unsupported commands fail.

## Integration and validation

`export_records(images)` produces one canonical-compatible record,
`cinematic:meteor`, with all 343 original tokens. Its 74 text spans include
speaker names and deliberate pauses inside utterances. `compile_records(images,
records)` returns patched Opening bytes and per-record manifest entries. The
caller must enforce current editorial review and adaptation fingerprints; this
adapter enforces original source, complete token coverage, encoding, layout,
allocation and non-text preservation.

The independently authored complete English adaptation fits 3,220 of 4,210 bytes.
It includes all narration and speaker turns, including Penrose's changed behavior,
without omitting any page. Full original stream token roundtrip is byte-identical.
New tests cover animation payload zeros, control-preserving Latin, unknown bytes,
truncated operands, row/line wrapping, delays, missing adaptations and timing
spaces. Original-image compile confirms all changed bytes lie inside the loaded
stream extent, every immutable token remains identical and disk length is fixed.
Runtime font appearance, animation playback and return to the System scene still
require emulator validation; byte checks do not establish runtime approval.
