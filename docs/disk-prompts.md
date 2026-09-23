# Dynamic disk prompts

The 2026-09-23 11:57 screenshot shows the shared two-drive prompt, not an ordinary
script entry. The Opening disk's resident boot driver builds it dynamically.

`disk-prompts.json` is a dedicated canonical/context/review/adaptation sidecar
for these fixed driver fields. It preserves source offsets, lengths and hashes;
canonical instructions use named disk/drive placeholders without layout limits.
`disk_prompts.py` is the fitting adapter. It checks editorial fingerprints,
source spans, runtime field positions, font, allocation and geometry before any
write. This specialized sidecar does not imply generic UI support in the script
catalog compiler.

The name pointer table at Opening 0x27FD selects six 12-byte labels plus NUL:
Opening, System, Data, Visual, Ending and User. Each call copies exactly six words
into its template. English names retain that size, using full-width space padding.
INTRO is the six-cell adaptation for the Opening disk; the actual image filename
remains Opening Disk. Other labels are SYSTEM, DATA, VISUAL, ENDING and USER.

Single-drive template: 0x2857, 67 bytes, inside a 15-cell/five-row box. The adapter
uses three rows: disk name, IN DRIVE n, PRESS ANY KEY. The instruction at 0x2529
writes BH into the CP932 digit's low byte. Only its address operand moves from
0x086F to 0x0877.

Two-drive template: 0x289A, 103 bytes, inside a 17-cell/three-row box. It becomes:

```text
SYSTEM IN DRIVE 1
DATA   IN DRIVE 2
PRESS ANY KEY.
```

The second name slot remains at 0x28BD (35 bytes after the first); pointers and
copy lengths are unchanged. Digit writes at 0x2558 and 0x255C still use BH and CH,
respectively; only destinations change, from 0x08B1/0x08D4 to 0x08BB/0x08DE.
The driver supplies CP932 low bytes 0x50/0x51 for drive 1/2. No disk checking,
loading, wait behavior or dialog geometry changes. The fitting adapter guards
all three original instructions before writing anything.

Add `--translate-disk-prompts` to the batch-03 build command in
`dust-approach-batch-03.md`, with a new output directory. It is opt-in so older
builds remain reproducible. The manifest records canonical/adaptation hashes and
the instruction offsets under `disk_prompts`.

Validation: 61 tests pass, including simulated runtime name/drive substitution
for all labels and both drive numbers, and atomic rejection of source,
instruction, stale-review, field-position and geometry failures. IPS roundtrips
pass. Compared with Dust Approach 03, System is identical and all 186 changed
Opening bytes lie in the guarded name/template/instruction spans. No save or
emulator state was modified. In-game visual confirmation is still pending.
