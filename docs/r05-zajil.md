# R05: Zajil and the Saibal investigation

The cumulative candidate contains **701 adapted records across 72 scenes**, preserving
all 596 records from the September 24 playtest-fix build. R05 adds 98 script records
and seven location/ability labels. These are records, including multi-turn scenes,
not equal-sized lines or a whole-game completion percentage.

## Route and stopping points

Leave CS Station after the first mission briefing. The original border puts the
party on **Planet Zajil**; no intervening flight is assumed. Follow the surface
route to Saibal. The section covers its townspeople, all shops, underground bar,
guard fight, syndicate interrogation, hotel alternatives, kidnapping sequence
and immediate party conversations. Initial optional Porkin interactions and its
guard fight are included, along with Zajil Spaceport ticket services, choices,
refusals and boarding text.

Stop after the hotel kidnapping and immediate conversations, **before pursuing
Tomyu at Porkin**. Boarding a bus leaves the section; its departure text is English,
but exploration on Mars or Stea is not included. Taking off for spaceflight/ship
combat and later-story station visits are also outside this surface section.
Opening staff-credit artwork remains Japanese.

## Run and continue a save

```sh
"/Users/mikaelstenberg/NewProject/retrotext-lab/work/Launch R05 Translation XP4.command"
```

The launcher uses `work/r05-01-xp4`, XP4 battle rewards and separate configuration,
saves, states and screenshots. Original disks and earlier builds are preserved.
Continue from an **in-game save**, using the new System and Opening disks and your
existing User Disk. The candidate's fresh User Disk does not contain your previous
progress. Select the existing User Disk when loading, or copy it into the candidate
while the emulator is closed, retaining the old disk as backup. Old emulator save
states can restore old code and Japanese text from memory.

## Player verification sheet

- Leave the station, check the Zajil title, and enter Saibal; check the town title.
- Talk to all available townspeople, visit both shop counters and try purchase,
  refusal, insufficient-funds and full-inventory outcomes where practical.
- Visit the underground bar before and after interrogating the syndicate member.
  Check the rumor, price and drink-choice alternatives.
- At the scrapper, check the five-row instructions: 8 sells one scrap for five
  credits; 2 buys one scrap for five credits; hold Space to accelerate.
- Check the guard fight, combat results, Welda's Mental Recovery/Mental Attack
  labels and field ability display. Those are displayed as MINDHEAL/MINDATK.
- Check the syndicate interrogation and repeat conversation, ordinary hotel
  stay before the interrogation, and the kidnapping stay afterward. Read both
  letter pages and check speaker headings and party TALK after Shoko disappears.
- Optional: before the kidnapping, explore Porkin's residents, shops and guard
  encounter. Check Zajil Spaceport fares 100/150, ticket purchases, capacity/funds
  refusals and boarding choices. Cancel boarding to remain within the section.

Unexpected Japanese on these inventoried surfaces is a release defect. Full route
traversal, final text appearance, animation timing and save/load behavior still
need player verification; static checks and a boot smoke do not establish them.

## Reproduction and evidence

```sh
python3 -m profiles.alshark.replay ../alshark/original --output work/r05-replay-new.json
python3 profiles/alshark/build_demo.py ../alshark/original \
  --output work/r05-rebuild-new --expand-menu-labels --translate-disk-prompts \
  --exp-multiplier 4 --localization work/r05-replay-new.json \
  --release-plan profiles/alshark/release-station-departure.json
```

The strict section plan requires all 701 records together. The bounded original
closure has 168 entries, 139 with text, and 40 guarded calls. Original commands,
allocations, source hashes, pointer aliases and runtime field checks remain in
force. Five-row letter/exchange layouts use the existing validator; no renderer
limit was relaxed. Names use the existing centered-title and eight-cell ability
adapters. The terminology impact report is `work/r05-terminology-impact.json`.

All 168 regression tests pass, including the native CPU renderer and trainer
checks. See [RE evidence](r05-re-source-evidence.md),
[independent inventory](r05-qa-source-inventory.md),
[editorial QA](r05-qa-editorial.md) and [final candidate QA](r05-qa-final.md).
The manager owns scope, terminology, optional-town English and integration;
separate workers supplied RE, Saibal localization and independent QA.

Independent frozen binary QA passed: all 911 compiler patch ranges match the
candidate, both IPS patches reproduce the images exactly, and all 596 prior
English records are preserved. Opening is identical to the previous playtest-fix
build; the other four nonpatched disks remain original. An isolated 1,800-frame
boot exited successfully and rendered the RIGHT STUFF logo. Evidence is in
`work/r05-final-smoke/boot-result.json`; all six smoke copies remained unchanged.
This demonstrates boot only, not a route playthrough.
