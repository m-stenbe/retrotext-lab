# Retrotext Lab

Experimental tools for researching and translating vintage Japanese computer
games. The first profile targets **Alshark for PC-98**.

The reusable layer detects little-endian relative-pointer tables and splits
candidate blocks losslessly. Game profiles own offsets, encodings, script
commands and patch rules. PC-88/PC-98 hardware alone does not imply compatible
engines. **No other game or PC-88 format is currently supported.**

The latest cumulative section is [R09: Daina reunion and the Begi historian](docs/r09-daina-begi.md),
with 1,064 adapted records in 107 scenes and a runnable XP4 launcher. Full route
playtesting remains pending.

## Translation progress

As of R09 (October 5, 2026), **1,064 records across 107 scenes** are adapted.
The translated route runs from the opening through Daina's reunion and the
Begi historian, stopping before departure to Stea.

| Coverage measure | Adapted / known | Progress |
| --- | ---: | ---: |
| Decoded dialogue/script entries containing text | 623 / 1,564 | **39.8%** |
| All known text records, including names and UI | 1,064 / 2,014 | **52.8%** |

These measure **currently discovered text, not whole-game completion**. Entries
vary from short labels to long scenes, and further text still needs discovery.
All 202 regression tests, the strict section build, binary-preservation checks
and a startup check pass. **Full route playtesting remains pending.** See the
[progress notes](docs/progress.md) for counting methods and limitations.

## How to patch your own copy

You need **Python 3.10+**, your own original **Alshark PC-98** disk images, and a
PC-98 emulator with its required firmware. Game disks and firmware are not
included. The commands below generate patched copies and IPS files locally.

### 1. Get the tools and prepare your disks

```sh
git clone https://github.com/m-stenbe/retrotext-lab.git
cd retrotext-lab
```

While [PR #1](https://github.com/m-stenbe/retrotext-lab/pull/1) is unmerged,
check out its version before continuing:

```sh
git fetch origin pull/1/head
git switch --detach FETCH_HEAD
```

Put all six original images in a separate folder:

```text
Alshark (Data Disk).hdm
Alshark (Ending Disk).hdm
Alshark (Opening Disk).hdm
Alshark (System Disk).hdm
Alshark (User Disk).hdm
Alshark (Visual Disk).hdm
```

Their filenames and SHA-256 hashes must match
[SHA256SUMS.txt](profiles/alshark/SHA256SUMS.txt); the builder checks the originals.
Keep an untouched backup and use a fresh output folder.

### 2. Build the English disks

Replace `/path/to/original` with your original-image folder. Run from the
repository root, with the emulator closed:

```sh
python3 -m profiles.alshark.replay "/path/to/original" --output work/r09-catalog.json
python3 profiles/alshark/build_demo.py "/path/to/original" \
  --output work/r09-english \
  --localization work/r09-catalog.json \
  --release-plan profiles/alshark/release-daina-begi.json \
  --expand-menu-labels --translate-disk-prompts
```

This creates all six playable images in `work/r09-english/`, plus System and
Opening IPS patches and `patch-manifest.json`. **The output disks are already
patched; do not apply IPS to them again.** Normal experience rewards are retained;
optionally add `--exp-multiplier 4` for faster leveling on an emulated 386+ CPU.
On subsequent builds, choose a new catalog filename and update `--localization`
to match; replay refuses to overwrite an existing catalog. Keep `--release-plan`
and run Python without `-O` so validation stays enabled.

### 3. Play or continue an existing save

1. Mount the generated **Opening Disk** in drive 1 and **Data Disk** in drive 2.
2. When prompted, switch drive 1 to the generated **System Disk**, keeping
   **Data Disk** in drive 2. Follow later disk prompts using this output folder.
3. Choose START, or LOAD with your existing User Disk. To retain progress, close
   the emulator, back up that User Disk, then copy it over the fresh output User
   Disk or select it when prompted. Use an **in-game save**; an older emulator
   save state can restore old code and text.

If applying the generated IPS files separately, use an IPS patcher to apply
`Alshark (System Disk).ips` to a copy of the matching original System image and
`Alshark (Opening Disk).ips` to a copy of the matching original Opening image.
Compare the outputs with `patched_sha256` in the manifest. IPS does not check
source hashes for you.

See the [full setup and troubleshooting guide](docs/getting-started.md) and
[R09 route checklist](docs/r09-daina-begi.md) for details.

## Current capabilities

- Alshark structural audit: candidate blocks, entry slices, diagnostic CP932
  text, source hashes and per-disk marker counts.
- Reproducible cumulative Alshark section builds from versioned English packs
  and original disks, producing local images, IPS patches and validation manifests.
- Conservative command-aware export/import with immutable commands, stable IDs,
  exact unchanged roundtrip and source-mapped entries enabled for editing.
- Guarded dialogue, cinematic, menu, runtime UI and name adapters, with separate
  canonical English and storage/layout fitting. Older partial demos remain available.
- Regression tests for script preservation, pointers, layouts, section gates,
  renderer behavior and the optional experience multiplier.
- Separate canonical English, connected-scene context, editorial review,
  terminology impact and technical adaptations. See the
  [localization workflow](docs/localization-workflow.md) and
  [Alshark localization bible](profiles/alshark/localization-bible.json).

New translation work follows source/context → canonical English → editorial
review → technical adaptation → ROM validation → playtest → editorial feedback.
Plan substantial playable sections with the [section release workflow](docs/section-release-workflow.md).
The current cumulative boundary is described in the section handoff above;
`--release-plan` blocks partial coverage from being packaged as a section candidate.
Existing per-scene demo builds remain experiments.
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

For the cumulative translation, use the [getting-started guide](docs/getting-started.md).
The optional demo commands below are smaller engineering experiments.

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

## Current playable section

See the [R09 handoff](docs/r09-daina-begi.md) for the cumulative opening
through Daina and the Begi historian candidate, launcher, reproducible build commands, source
coverage and runtime limitations.
