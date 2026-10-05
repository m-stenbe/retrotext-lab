# Build and run the Alshark English patch

The current cumulative candidate covers the opening through Daina
and the Begi historian. See the [R09 route and limits](r09-daina-begi.md).
Automated validation passes for that candidate; full route playtesting is pending.

## What you need

- Python 3.10 or later; the patch builder uses the standard library.
- Your own six original Alshark PC-98 `.hdm` disk images, with the exact filenames
  and SHA-256 hashes in [SHA256SUMS.txt](../profiles/alshark/SHA256SUMS.txt).
- A PC-98 emulator and its required firmware, installed separately. Existing
  project playtests use Neko Project II kai.

This repository supplies tools and English translation packs. Game disks,
firmware, source catalogs and emulator binaries are not included.

## Build the cumulative candidate

Clone the repository and run the commands from its root. If testing a PR, check
out that PR's branch first so the tools, packs and release plan match.

```sh
git clone https://github.com/m-stenbe/retrotext-lab.git
cd retrotext-lab
```

Keep originals in a separate directory. Replace `/path/to/original` below with
that directory, containing all six images. Use a new output directory for each
candidate and close any emulator using its images before rebuilding.

```sh
python3 -m profiles.alshark.replay /path/to/original --output work/r09-catalog.json
python3 profiles/alshark/build_demo.py /path/to/original \
  --output work/r09-english \
  --localization work/r09-catalog.json \
  --release-plan profiles/alshark/release-daina-begi.json \
  --expand-menu-labels --translate-disk-prompts
```

Replay reconstructs the reviewed translations from the versioned packs and your
original disks; no pre-existing files in `work/` are required. It refuses to
overwrite a catalog, so use a new filename on a later run. The builder validates
the complete release plan before producing a section candidate. Do not remove
`--release-plan` to get around an error. Run Python normally, without `-O`, so
assertion-based preservation checks remain active.

The command keeps normal experience rewards. For the optional faster-leveling
playtest build, add `--exp-multiplier 4` (requires a 386-or-later emulated CPU).

The output directory contains all six game images, two IPS patches for the
System and Opening disks, `patch-manifest.json`, and an emulator launch command.
The manifest records source/output hashes, selected records and gate results.
The builder verifies that applying each IPS patch reconstructs its output image.

## Start or continue in the emulator

1. Open the generated **Opening Disk** in floppy drive 1 and **Data Disk** in
   drive 2. `Alshark-dialogue-test.cmd` contains the equivalent `np2kai` command;
   run that command if `np2kai` is installed on your command path, or select the
   images in your emulator's UI.
2. Follow the game's disk prompts. When it requests **System** in drive 1 and
   **Data** in drive 2, use the images from the new output directory. Mixing an
   old System or Opening image with the new candidate can restore old text.
3. Choose START for a new game, or LOAD to continue from an in-game save.

To retain existing progress, close the emulator, back up your existing **User
Disk**, then copy it over the fresh User Disk in the output directory, or select
your existing User Disk when prompted. A fresh User Disk has no previous saves.
Keep the backup. Continue from an in-game save: an old emulator save state may
restore old code and text. Never copy or rebuild disks while an emulator is
writing to them.

Follow the current section handoff's stopping point and verification checklist.
Translated destination labels do not promise translated exploration everywhere.
The R09 handoff's absolute macOS launcher path is a convenience for its original
workspace; the build commands above work without that launcher.

## IPS patches and common problems

The builder already creates patched disks; you do not need to apply IPS again.
If using its IPS output separately, apply each patch once to a copy of the exact
matching original disk, then compare its SHA-256 with `patched_sha256` in the
manifest. IPS itself does not enforce the source hash. Never patch an already
patched image or your only original copy.

- **Missing image or hash mismatch:** check all six filenames and hashes against
  `SHA256SUMS.txt`. Do not rename a different game revision to bypass the check.
- **Catalog already exists:** use a fresh catalog path and output directory.
- **Release gate or fitting error:** retain the error and build command for a
  report; dropping the gate produces an experiment, not a complete candidate.
- **Old Japanese text after updating:** confirm both patched disks are mounted
  and load an in-game save instead of an older emulator state. Unexpected
  Japanese within the documented route is a defect to report.

## Reviewing and contributing

Run the regression suite from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

Tests requiring original disks or native emulator tooling may skip if those
local dependencies are absent; report skips separately from passes. Follow the
[localization workflow](localization-workflow.md) and
[section release workflow](section-release-workflow.md) for translation changes.

Completed batches may be committed and submitted as PRs before player testing.
Include automated validation evidence, the translated route boundary and any
pending runtime checks. A PR is reviewable work; it does not establish that the
whole route has been played. Keep game disks, extracted source catalogs and
screenshots under ignored `work/`, out of public commits.
