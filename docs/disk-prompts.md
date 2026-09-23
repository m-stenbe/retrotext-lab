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

The original name pointer table at Opening 0x27FD selects six 12-byte labels
plus NUL. The updated adapter relocates all six labels to 0x4E00..0x4E59,
with seven full-width cells plus NUL per label. This is separate from the menu
pool at 0x4C00..0x4DFF and inside the resident 0x2000..0x5FFF disk load.
It guards the original pointer table and empty destination before writing.
The labels are OPENING, SYSTEM, DATA, VISUAL, ENDING and USER, padded to seven
cells. OPENING now matches the image name; the earlier INTRO workaround was
rejected in playtest because it obscured which disk to insert.

Three `mov cx,6` instructions at 0x2538, 0x2571 and 0x2588 become `mov cx,7`.
The following `rep movsw` instructions and all disk-selection logic remain intact.
The original name slots remain unchanged on disk; the pointer table uses the new
resident labels. Source hashes still guard those original slots.

Single-drive template: 0x2857, 67 bytes, inside a 15-cell/five-row box:

```text
OPENING
IN DRIVE 2
PRESS ANY KEY.
```

The instruction at 0x2529 still writes BH into the CP932 digit's low byte;
its destination changes from original 0x086F to 0x0879.

Two-drive template: 0x289A, 103 bytes, inside a 17-cell/three-row box:

```text
SYSTEM  DRIVE 1
DATA    DRIVE 2
PRESS ANY KEY.
```

Each of the first two rows includes two trailing full-width spaces so the second
name slot remains at 0x28BD (35 bytes after the first). Digit writes at 0x2558 and
0x255C still use BH and CH, with destinations 0x08B7 and 0x08DA. The driver supplies
CP932 low bytes 0x50/0x51 for drives 1/2. No disk checking, loading, wait behavior
or dialog geometry changes. All guards pass before any mutation.

Add `--translate-disk-prompts` to the batch-03 build command in
`dust-approach-batch-03.md`, with a new output directory. It is opt-in so older
builds remain reproducible. The manifest records canonical/adaptation hashes and
the instruction offsets under `disk_prompts`.

Validation: the suite exercises runtime substitutions for all six labels and
both drives in single and dual prompts, copy counts, pointer resolution, and
atomic rejection of source, instruction, stale-review, field-position, geometry,
pool and pointer-table failures. Original asset builds and IPS checks are also
required. The previous six-cell single prompt was observed in the 2026-09-23
13.47.06 screenshot; the new seven-cell version awaits in-game verification.
