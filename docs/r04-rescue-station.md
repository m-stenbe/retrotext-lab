# R04: Distress rescue and the first station assignment

The cumulative candidate contains **595 adapted records across 61 scenes**,
including all 550 previous records. R04 adds 41 dialogue records and four
character/location labels. Several records contain long conversations or
narrated sequences; these counts are not equally sized lines or a whole-game
completion percentage.

The new route begins at Atraia's cockpit after R03. It covers the distress call,
boarding and rescue, station recruitment, the complete station tour, both
acronym-answer branches, the first mission briefing, immediate station follow-up
interactions and conditional party conversations. **Stop before leaving CS
station for the assignment.** The station border targets map9, not the bridge.
Flight, surface exploration and the Zajil assignment itself are outside this
section. Some later bridge barks are translated as additional coverage.

## Run

```sh
"/Users/mikaelstenberg/NewProject/retrotext-lab/work/Launch R04 Translation XP4.command"
```

The launcher uses `work/r04-01-xp4`, four-times battle EXP and separate emulator
options, saves, states and screenshots. Previous candidates and original images
are preserved. Continue using an in-game save and the new System/Opening disks;
old emulator save states can restore old text from memory. The new User Disk is
not a copy of your previous playthrough: select your existing User Disk when
loading that save, or copy it into the new build only while the emulator is
closed, keeping the old disk as a backup.

## Player verification

- Enter the cockpit and check the distress-call dialogue and boarding transition.
- Check the warning and overheard conversation aboard the civilian craft, then
  the full confrontation and rescue. Watch narration continuation pages, names,
  animation transitions and the shift between narration and speaker headings.
- At CS station, check the recruitment conversation and Welda's displayed name.
- Speak to all available station personnel. Try both answers to the acronym
  question and repeat conversations before and after the summons.
- Visit the scientist, hangar guard and acronym operator to complete the tour;
  the commander then calls the party to his private room.
- Read the first mission briefing and subsequent secretary/commander responses.
  Check party TALK alternatives. Stop before leaving the station.

Unexpected Japanese on these inventoried surfaces is a release defect. Opening
staff-credit artwork remains Japanese. Full route traversal, save/load and visual
appearance remain player verification work.

## Engineering and reproduction

The source closure contains 85 entries, 67 with text, including cumulative
dependencies. Source-backed flow handles the station's three-flag summons;
original story commands, flags, allocations and pointer targets are preserved.
Four new name records resolve 25 pointers, including 22 existing aliases of the
generic ship-interior title. The full canonical name Welda Muretts has the
documented shortened WELDA display; CS STN abbreviates the station label.

Long narration supports explicit wait/clear/restore continuation pages. The
adapter guards the original interpreter and four shared speaker-header calls,
which reset attributes before ordinary dialogue. Unknown effects, other text
attributes, header splits and allocation overflow still fail closed. No new
text relocation or gameplay changes were needed.

```sh
python3 -m profiles.alshark.replay ../alshark/original --output work/r04-replay-new.json
python3 profiles/alshark/build_demo.py ../alshark/original \
  --output work/r04-rebuild-new --expand-menu-labels --translate-disk-prompts \
  --exp-multiplier 4 --localization work/r04-replay-new.json \
  --release-plan profiles/alshark/release-rescue-station.json
```

The full test suite runs 147 tests, with 145 passing and two optional Unicorn
checks skipped. See [source evidence](r04-re-source-evidence.md),
[independent inventory](r04-qa-source-inventory.md) and
[editorial review](r04-qa-editorial.md). Three GPT-6 Astra workers at medium
effort performed RE, localization and independent QA, with Astra managing
scope, names, integration and release preparation.

Independent [frozen binary QA](r04-qa-final.md) confirms all 595 compiled records,
exact replay of both IPS patches, the prior 550 canonical/adapted records,
unchanged equipment/progression data and unchanged four nonpatched disks.
An isolated 1,800-frame boot exited successfully and rendered the opening logo;
evidence is in `work/r04-final-smoke/boot-result.json`. Audio was disabled. This
is boot evidence only, not validation of the translated route in the emulator.
