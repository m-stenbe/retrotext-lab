# R01: first proactive section pass

This build targets the Cosma → Hom overworld → Saxen Canyon meteor event → Cosma
return/Karu route. Hamack, Dust and other overworld detours belong to later
sections; already adapted material there remains included as cumulative bonus
content. The original opening title/staff-credit artwork remains Japanese.

**Final candidate: 138 adapted records across 33 scenes; the section gate passes.**
This includes cumulative bonus content outside the R01 boundary. The catalog has
141 reviewed canonical records; three later Joe/Hamack records still need fitting.
These counts are not a whole-game completion percentage.

The machine-readable release plan and its generated assessment distinguish source
coverage from runtime verification. The player should verify English and behavior;
ordinary untranslated branches remain a project defect, not a discovery assignment.

## What changed

- The complete meteor cinematic now has a guarded adapter and all 74 text spans
  adapted from the independently reviewed canonical script. Its 269 animation,
  timing, page and other nontext tokens remain unchanged.
- Nineteen pending town/house records and two missing pickup outcomes are adapted.
  Lake warning, Karu and longer conversations use seven reviewed continuation
  breaks instead of dropping their meaning to fit. Continuation pages clear the
  original speaker heading, as the game normally does.
- Eighteen additional interface messages cover item actions, capacity, disk
  creation/errors, abilities and battle outcomes. Existing UI and battle-result
  translations are now represented as explicit reviewed adaptations.
- Equipment, location and all class 3/4 learned-ability names use coordinated,
  guarded storage. QA caught a real width error: ability lists allow ten cells,
  but the learned-name field only eight. TELEKIN, DIMENS, MINDSTRM and INVIS are
  documented display abbreviations; canonical names remain complete.
- QA corrected NO SKILLS to CANNOT USE. and separated the learned ability from
  its surrounding sentence. Inventory/discard item names are limited to nine
  cells; source pointer aliases and immutable runtime fields are preserved.
- Fifteen source-backed terminology entries were added without inventing ability
  mechanics or resolving the uncertain Protector/Hand Medical item types.

- Map-source discovery found and added seven global party TALK records, covering
  Sion/Shoko before the expedition, grief afterward and Lucia's disappearance.
  Taken branches are checked with their inherited caller display state.

The screenshot's Jido line is included in the complete aftermath conversation:
“S...SION... / SHOKO... / WHY... HERE?”

## Run the cumulative local build

Quit the older emulator instance before starting this one:

```sh
zsh "/Users/mikaelstenberg/NewProject/retrotext-lab/work/Launch R01 Translation XP4.command"
```

The launcher uses `work/r01-04-xp4`, separate emulator configuration/save-state
folders, and 4× battle EXP as in the previous test build. Start from a fresh boot.
Old emulator save states can restore old text already loaded into emulated RAM;
use the game's disk-based save/load flow when resuming an existing in-game save.
No live emulator disks, original images or existing save directories were edited.

## Reproduce and assess

The replay command writes a full source catalog, which belongs in ignored `work/`:

```sh
python3 -m profiles.alshark.replay ../alshark/original --output work/r01-fresh.json
python3 profiles/alshark/release_tool.py ../alshark/original work/r01-fresh.json \
  --plan profiles/alshark/release-opening-cosma.json
python3 profiles/alshark/build_demo.py ../alshark/original --output work/r01-rebuild \
  --localization work/r01-fresh.json \
  --release-plan profiles/alshark/release-opening-cosma.json \
  --expand-menu-labels --translate-disk-prompts --exp-multiplier 4
```

The release gate must pass before the final command creates a section candidate.
It will refuse any remaining discovery/adaptation blocker rather than silently
building a ready subset. `patch-manifest.json` records build kind, scope/catalog/
bible fingerprints, source/patched hashes, declared patch ranges and adaptations.

## Verification and remaining runtime work

Source checks include exact original-image hashes, original command/runtime-field
preservation, name aliases, menu geometry, composed shared calls, allocation and
font checks. The builder independently applies each generated IPS to its original
image and checks the result byte for byte. Tests exercise overflow, stale source,
partial name groups, unreviewed pointers and page/control injection rejection.

The test suite ran 99 tests: 97 passed and two optional Unicorn checks skipped.
A fresh replay of the versioned packs reproduces the final catalog exactly.

An isolated RetroArch/NP2Kai run reached the logo and opening credit sequence using
copied disks, system files and separate save directories. This establishes boot
execution, not successful completion of the route. The final candidate was
separately booted for 1,800 frames and rendered the RIGHT STUFF logo; evidence is
in ignored `work/r01-final-smoke/boot-result.json`. Independent final image/IPS/
canonical-range QA is recorded in `work/r01-qa-final-04.json`. Full gameplay transitions,
cinematic timing, font appearance and interaction behavior remain unverified in
runtime; the manifest must not imply otherwise.

Player verification, after the source gate passes, should focus on:

- Breakfast, invitation choices, optional Cosma conversations and party TALK.
- Pickups, exhausted/full-inventory outcomes and inventory/equipment names.
- Canyon arrival, the full cinematic and Jido/soldier/crater conversations.
- Return to Cosma, Karu joining and party dialogue at each story state.
- Wrapping, speaker identity, menu selection, ordinary combat and save/load.

Source evidence is in the [map and party branch inventory](r01-map-entrypoints.md),
[coverage audit](r01-coverage-audit.md),
[cinematic format](alshark-cinematic-format.md) and
[name storage investigation](alshark-name-storage.md).
