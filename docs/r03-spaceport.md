# R03: Hom Spaceport, the abandoned mine and Atraia

This cumulative candidate contains **550 adapted records across 54 scenes**, up
from R02's 266/44. The **284 additions** comprise 37 story/dialogue records,
24 menu/service records, three location titles and 220 equipment names. A record
may contain many dialogue pages or a single label; this is not a whole-game
completion percentage or a count of equally sized translation tasks.

The new section begins after the Hamack spaceport lead. It covers Hom Spaceport,
Joe's proposal, the abandoned mine's mechanism and repeat, the ship reveal and
naming, and the first controllable bridge. It includes the three initial crew
conversations and the service menu reached by walking south from bridge spawn.
The endpoint is **before stepping into the cockpit**, which starts the next
rescue/distress event. Mars, subsequent flight/combat and unrelated Hom detours
remain outside this section. Earlier R01/R02 translations are retained.

## Run

```sh
"/Users/mikaelstenberg/NewProject/retrotext-lab/work/Launch R03 Translation XP4.command"
```

The launcher uses `work/r03-01-xp4`, four-times battle EXP, and separate core
options, saves, states and screenshots. R02's existing candidate and the original
disks are preserved. Use the new disk set and an in-game save; old emulator save
states can restore old text from memory. This build does not automatically copy
or overwrite your existing playthrough's User Disk.

## Player verification

- Spaceport: travelers, counter staff, ticket barrier and Joe's complete ship
  proposal; repeat the barrier after receiving the mine lead.
- Mine: mechanism interaction with Joe, the already-open repeat, ship reveal,
  naming conversation and transition onto the bridge.
- Party: the mine directions and Mars promise after the lead. Additional flag-13
  global TALK lines are translated conservatively, but the bridge uses direct
  crew interactions rather than the normal global TALK menu.
- Bridge: speak with Shoko, Joe and Karu. Walk south from the initial position to
  open ship services. Check selection highlights, hangar unload/store, equipment,
  repairs, development, scrap and System. Check empty/full/insufficient-resource
  outcomes where available. Ship gear's too-heavy-to-carry refusal is included.
- Names: location titles and item/equipment lists should be readable; caliber
  numbers remain distinct. Abbreviations are constrained to the nine-cell fields.

Unexpected Japanese in these mapped surfaces is a release defect. Original
staff-credit artwork is still Japanese. Full route traversal, menu behavior and
save/load remain player verification work; static coverage is not a runtime claim.

## Why the name inventory expanded

Ship development scans 280 normal/ship equipment IDs, with eligibility based on
Joe's IQ and cost checked after selection. An unaffordable name can still appear.
The candidate translates the full potential union without imposing an arbitrary
level/grinding cap: 238 distinct original strings, including 18 existing R01/R02
translations and 220 new labels. This changes no availability, stats, costs or
story flags. High-threshold names are preparedness, not a claim that later story
content is included. Provisional romanizations and Night/Knight or Task/Tusk
ambiguities remain explicit in the localization bible.

Name source strings can share suffix storage. The guarded adapter repacks only
newly reviewed storage, excluding every prior name pool. All exact aliases are
preserved, including distinct names that originally shared suffixes. A numeric
progression table beginning at System `0x1055c` is explicitly excluded from pointer
scanning and writes; an early mistaken alias classification was corrected before
any candidate build.

## Validation and reproduction

The complete suite runs 134 tests: 132 pass, two optional Unicorn checks skip.
The source inventory has 67 conservative script entries, including 56 with text;
all required text and control dependencies are covered. No new text-bearing
cinematic stream was found. New menu widths are paired with their selection
widths, and service-message dynamic fields remain protected.

```sh
python3 -m profiles.alshark.replay ../alshark/original --output work/r03-replay-new.json
python3 profiles/alshark/build_demo.py ../alshark/original \
  --output work/r03-rebuild-new --expand-menu-labels --translate-disk-prompts \
  --exp-multiplier 4 --localization work/r03-replay-new.json \
  --release-plan profiles/alshark/release-spaceport.json
```

The build must pass the complete section gate; subset builds are experiments.
See [RE evidence](r03-re-source-evidence.md), [source inventory](r03-qa-source-inventory.md),
[editorial review](r03-qa-editorial.md), and [frozen binary QA](r03-qa-final.md). Both IPS patches reproduce the exact
candidate; all 266 prior R02 translations, equipment stats and progression data
are preserved. An isolated 1,800-frame boot exited successfully and rendered the
opening logo (`work/r03-final-smoke/boot-result.json`); audio was disabled. This
does not establish runtime route validation.
Three GPT-6 Astra workers at medium effort performed RE, localization and QA,
with Astra managing integration and authoring the new names for independent review.
