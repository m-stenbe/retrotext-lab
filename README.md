# Retrotext Lab

Experimental tools for researching and translating vintage Japanese computer
games. The first profile targets **Alshark for PC-98**.

The reusable layer detects little-endian relative-pointer tables and splits
candidate blocks losslessly. Game profiles own offsets, encodings, script
commands and patch rules. PC-88/PC-98 hardware alone does not imply compatible
engines. **No other game or PC-88 format is currently supported.**

## Current capabilities

- Alshark structural audit: candidate blocks, entry slices, diagnostic CP932
  text, source hashes and per-disk marker counts.
- Reproducible Alshark demo: START/LOAD menu, breakfast conversation, selected
  shared names and Cosma location title. Builds local images and IPS patches.
- Conservative command-aware export/import with immutable commands, stable IDs,
  exact unchanged roundtrip, and thirty-two opening/town/pickup entries enabled for editing.
- Optional area draft: nineteen more conversations/branches, Shoko's name,
  basic field/system/text-speed menus and three common UI messages.
- Synthetic tests for block slicing and script validation.
- Separate canonical English, connected-scene context, editorial review,
  terminology impact and technical adaptations. See the
  [localization workflow](docs/localization-workflow.md) and
  [Alshark localization bible](profiles/alshark/localization-bible.json).

New translation work follows source/context → canonical English → editorial
review → technical adaptation → ROM validation → playtest → editorial feedback.
Existing compressed drafts remain provisional. Unacceptable fitting is recorded
as `DOES_NOT_FIT`, not solved by silently degrading English. The generic editorial
layer lives in `retrotext/localization.py`; encoding/layout remain profile-specific.

The [2026-09-22 editorial review](docs/editorial-review-2026-09-22.md) covers all
76 previously drafted dialogue/UI/name/result units, with canonical English,
context, findings and unresolved terms. It does not change the current ROM build.
The [abbreviation audit](docs/abbreviation-audit-2026-09-22.md) checks the effective
menu pointers and labels in the built disks, separates storage from geometry,
and prioritizes restorations without expanding familiar abbreviations blindly.

The script decoder is partial and the importer keeps existing entry allocations.
This is not a general reinserter or full English translation. Physical roundtrip
validation does not prove safe text relocation. See the
[script format and usage](docs/alshark-script-format.md) for editing instructions
and current limitations.

## Run

Python 3.10+; standard library only. From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 profiles/alshark/audit.py /path/to/original --output work/audit
python3 profiles/alshark/build_demo.py /path/to/original --output work/demo
# Optional: adds Lucia's follow-up through the new importer
python3 profiles/alshark/build_demo.py /path/to/original --output work/importer-test --include-followup
# Adds Karu and two nearby town conversations as well
python3 profiles/alshark/build_demo.py /path/to/original --output work/town-test --include-town
# Adds four starting-house pickup labels and their shared found message
python3 profiles/alshark/build_demo.py /path/to/original --output work/pickup-test --include-pickups
# Larger temporary batch, including the previous drafts and basic menus
python3 profiles/alshark/build_demo.py /path/to/original --output work/area-draft-test --include-area
# Screenshot-review batch: battle/results, party UI, selected items and disk prompts
python3 profiles/alshark/build_demo.py /path/to/original --output work/review-draft-test --include-review
# Optional six-cell battle/field menu experiment (includes the reviewed draft)
python3 profiles/alshark/build_demo.py /path/to/original --output work/wide-menu-test --widen-menus
# Expanded menu labels using a guarded resident string pool (experimental)
python3 profiles/alshark/build_demo.py /path/to/original --output work/full-menu-test --expand-menu-labels
# Source-preserving localization sidecar; no automatic translation or ROM edits
python3 profiles/alshark/localization_tool.py export /path/to/original work/localization.json
```

Provide your own original disk images. The demo expects the six filenames and
hashes in `profiles/alshark/SHA256SUMS.txt`. Keep originals separate from outputs.
Run without Python's `-O` flag: the experimental builder uses assertions for
source, allocation and patch validation.

The generated `.cmd` lists Opening and Data. In Neko Project II kai, the opening
later requests System in drive 1 and Data in drive 2; use the generated images.
Choose START for the breakfast scene. Emulator installation and BIOS are separate.
Rebuilding overwrites demo System/Opening outputs, preserving an existing User
disk. Do not rebuild images while the emulator is using them.

No game images, firmware, extracted scripts, screenshots or third-party tools
are distributed here. Keep generated research under ignored `work/`.

## Research and next steps

See [Alshark research](docs/alshark-research.md) for measured findings and limits.
See [playtest notes](docs/playtest-notes.md) for context, wording and layout
issues, and the workflow for reviewing longer sections together.
The first inventory has 48 candidate windows, 2,249 pointer entries and 1,322
named-speech markers in those windows. These are not word/page totals.

1. Decode script commands and preserve their arguments exactly.
2. Separate dialogue, choices and substitutions into editable records.
3. Establish loader boundaries and references before relocating text.
4. Build a validated reinsertion pipeline and rendering-width checks.
5. Investigate narrower Latin lettering and lowercase.
6. Map UI, combat and graphics text; test across the game.

Contributions should use synthetic fixtures and identify the game/version each
finding applies to. Do not contribute game images or full extracted scripts.

MIT license for the code and original documentation. Game content and third-party
software remain subject to their respective rights.
