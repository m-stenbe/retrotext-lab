# R02: Dust, Joe and early Hamack

The cumulative candidate contains **266 adapted records in 44 scenes**, up from
R01's 138 records in 33 scenes: **128 additions**. A record can hold a whole
conversation, a short message or one label; this is not a percentage of the game.
Joe's meeting alone renders as 46 reviewed dialogue pages.

The promised new section starts after Karu joins in Cosma, covers Dust and Joe's
meeting, and continues through early Hamack information gathering. It includes
available town conversations, the optional job and delivery, shops, inn, drinks,
fortune branches, the Hamack bar, relevant party TALK, 21 additional item/ability/
location labels and three Joe disassembly UI strings. The endpoint is the
spaceport/Mars lead (story flag 0x11), before entering that next route. Earlier
R01 material, including the meteor scene, remains included. Ray Gun is translated
bonus content; it is not asserted to be Joe's starting equipment.

## Run this build

From Terminal:

```sh
"/Users/mikaelstenberg/NewProject/retrotext-lab/work/Launch R02 Translation XP4.command"
```

The launcher uses `work/r02-01-xp4`, four-times battle EXP, and isolated core,
save-state and screenshot directories. Original images and previous builds are
preserved. Start fresh or use an in-game save with the new disk set; loading an
old emulator save state can restore old script data from memory. No existing
playthrough save or running emulator was modified.

## What to verify

The source-derived inventory covers 143 reachable script entries, including 124
text entries and their control dependencies. This is a static coverage claim;
full emulator traversal is still pending. Please verify translated behavior:

- Dust: sleeping Joe, the full meeting, Joe joining, and party TALK afterward.
- Hamack: town speakers, the information lead and party TALK before and after it.
- Job: accept/refuse, completion/pay and delivery destination/result. The job's
  earlier party responses precede Joe joining; use a suitable earlier save.
- Services: buy/cancel/insufficient money, hotel recovery, drinks and fortunes.
- Bar: its twelve reachable objects, named informants and the spaceport lead.
- Joe: inventory/abilities and disassembly confirmation/result alignment.

Unexpected Japanese in these mapped interactions is a release defect. Unrelated
Hom detours, the spaceport/Mars route and later-story return visits are outside
this section. Original staff-credit artwork is still Japanese.

## Reproduce and evidence

```sh
python3 -m profiles.alshark.replay ../alshark/original --output work/r02-replay-new.json
python3 profiles/alshark/build_demo.py ../alshark/original \
  --output work/r02-rebuild-new --expand-menu-labels --translate-disk-prompts \
  --exp-multiplier 4 --localization work/r02-replay-new.json \
  --release-plan profiles/alshark/release-dust-hamack.json
```

The release gate requires every declared record and scene, current source and
editorial fingerprints, composed layout and allocation checks, and no open
coverage issue. Two reviewed shop/bar menu widths change from four to five cells.
A guarded two-byte transfer from the following already translated entry gives
GIRL its full speaker label; only that donor entry's pointer moves. Coordinated
name storage preserves all reviewed pointer aliases. These exceptions are
explicit in the compiler and manifest, not unchecked writes.

Independent frozen-candidate QA passes: both IPS patches reproduce the exact
images, all six disk hashes are verified, R01 content is preserved, and the XP4
trainer matches its expected bytes.

The suite runs 118 tests: 116 pass and two optional Unicorn checks are skipped.
[Source inventory](r02-qa-source-inventory.md), [RE evidence](r02-re-source-evidence.md),
[editorial QA](r02-qa-editorial.md), and the [model experiment](r02-model-experiment.md)
record the review and its limits. The isolated 1,800-frame boot test exited successfully and rendered the RIGHT
STUFF opening logo; audio was disabled. Evidence is in
`work/r02-final-smoke/boot-result.json`. Boot success does not establish route
validation. Frozen binary checks are documented in [final QA](r02-qa-final.md).
