# R06: Porkin pursuit and military-station rescue

This cumulative candidate contains **821 adapted records across 79 scenes**,
including all 701 R05 records. The 120 additions cover 53 script records, 26
flight-interface records and 41 destination/name records. Records can contain
multiple turns; these counts are not a whole-game completion percentage.

## Route and stopping point

Continue after the Saibal hotel kidnapping. Pursue Tomyu at Porkin, then follow
the lead to Zajil Military Station. Reach the station by spaceflight; it has no
ground entrance. On the space map the military station is southeast of CS Station.
The section includes the confrontation, rescue and reunion, immediate station
and party conversations, and changed Porkin/Saibal responses.

You may return to CS Station, but **stop before reporting to Roy for the next
assignment**. Exploration on other planets or unrelated stations is outside this
section. Their destination labels are translated for the flight interface.
Original space-map artwork already uses Latin captions; its variant spellings
remain visible. Opening staff-credit artwork remains Japanese.

## Run and continue a save

```sh
"/Users/mikaelstenberg/NewProject/retrotext-lab/work/Launch R06 Translation XP4.command"
```

The launcher uses `work/r06-01-xp4`, XP4 battle rewards and separate configuration,
saves, states and screenshots. Continue from an **in-game save**, using the new
System and Opening disks and your existing User Disk. The candidate's fresh User
Disk does not contain previous progress. Select the existing User Disk when
loading, or copy it into the candidate while the emulator is closed, retaining
the old disk as backup. Old emulator save states can restore old code and text
from memory.

## Player verification sheet

- Pursue Tomyu in Porkin after the kidnapping. Check the fight, interrogation,
  repeated dialogue and party TALK. Revisit townspeople and the one-time reward.
- Check flight navigation and battle menus, fighter controls, automatic/manual
  options, repairs and refusal messages. Check that highlights select the visible
  choice and destination names/counts do not overwrite neighboring text.
- Select the military station near CS Station. Check destination confirmation,
  cancellation, approach and landing labels.
- Talk to station personnel, confront Geist, then speak again to complete the
  reunion. Check names, speaker headings, choices and combat results.
- Revisit station personnel and party TALK after the rescue. Optional: revisit
  Porkin, Saibal and the hotel for changed responses.
- On returning to CS Station, stop before speaking to Roy about the next mission.

Unexpected Japanese on these inventoried surfaces is a release defect. Full
route traversal, final appearance, timing and save/load behavior still need player
verification; static checks and a boot smoke do not establish them.

## Reproduction and evidence

```sh
python3 -m profiles.alshark.replay ../alshark/original --output work/r06-replay-new.json
python3 profiles/alshark/build_demo.py ../alshark/original \
  --output work/r06-rebuild-new --expand-menu-labels --translate-disk-prompts \
  --exp-multiplier 4 --localization work/r06-replay-new.json \
  --release-plan profiles/alshark/release-porkin-pursuit.json
```

The strict release plan requires all 821 records together. Commands, source
hashes, original name pools, pointer aliases and protected runtime fields remain
checked. Nine menu boxes and eight selection widths are widened with original-byte
guards. Late Karma and Russell messages are excluded by documented story-state
and encounter predicates, not by untranslated-text filtering.

See [source evidence](r06-re-source-evidence.md),
[independent inventory](r06-qa-source-inventory.md),
[editorial review](r06-editorial.md), [editorial QA](r06-qa-editorial.md)
and [final candidate QA](r06-qa-final.md).
The manager owns scope, terminology, town/UI/name English and integration;
separate workers supplied RE, rescue localization and independent QA.
Terminology impact evidence is `work/r06-terminology-impact.json`.

All **178 regression tests pass**, including native CPU renderer and trainer
checks. Full route playtesting remains pending.

Independent frozen binary QA passed: all 1,133 compiler patch ranges match the
candidate, both IPS patches reproduce the images exactly, and all 701 previous
English records are preserved. The other four disks remain original. An isolated
1,800-frame boot exited successfully and rendered the RIGHT STUFF logo; all six
smoke disk copies remained unchanged. Evidence is in
`work/r06-final-smoke/boot-result.json`. This verifies startup only.
