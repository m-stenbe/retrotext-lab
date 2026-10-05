# R08: Mars leave, Teswil and the video letter

This cumulative candidate contains **1,034 adapted records across 101 scenes**,
retaining all 878 R07 records. The 156 additions comprise 149 dialogue records
and seven person/map labels. Records can contain many turns; these counts are
not a whole-game completion percentage.

## Route and stopping point

After the Byuto mine victory, return to CS Station and report to Roy. The party
receives leave, but may not use Atraia. Speak to the secretary and operator to
travel to Mars Spaceport. Explore Teswil, including every shop, hotel, building
interior and both bar rooms, and the nearby mainland town of Begi.

The search yields a video letter. **Use party TALK after receiving it** to view
the message. The section includes the letter, its associated party conversations,
the optional used Jet Hovercraft purchase, and the mainland services and pickups.

**Stop before crossing the sea to Daina.** The letter's lead to Daina starts the
next section. Bus menus, fares, refusal and departure messages are translated,
but exploration at other bus destinations is outside this section. Buying a
vehicle or ticket does not extend the promised route. The opening staff-credit
artwork remains Japanese; original Latin map-art spellings are unchanged.

## Launch and continue

```sh
"/Users/mikaelstenberg/NewProject/retrotext-lab/work/Launch R08 Translation XP4.command"
```

The launcher uses `work/r08-01-xp4`, XP4 battle rewards, and separate emulator
configuration, saves, states and screenshots. Continue from an **in-game save**
with the new System and Opening disks and your existing User Disk. The candidate's
fresh User Disk has no previous progress. With the emulator closed, copy your
existing User Disk into the candidate, keeping the old disk as backup, or select
it when loading. Old emulator save states can restore old code and text.

## Player verification

- Report after Byuto. Check the full debrief, leave instructions, secretary,
  operator travel/cancel choices, blocked ship access and station return.
- Talk to Mars Spaceport travelers and staff. Check displayed destinations,
  prices and choice highlights. Other bus destinations remain outside scope.
- Visit Teswil's hotels and all shops. Check purchases, insufficient money,
  repeats, refusals, the turret-shop boycott, and the more expensive hotel scene.
- Speak to all street and building residents. Check the cleaner's repeated
  responses and Shaina's first visit, tea and subsequent welcome.
- Explore both bar rooms. Receive the video letter, check any full-inventory
  refusal and repeat, then choose party TALK to watch it.
- Visit Begi on the mainland: residents, bookshelves, hotel, shops, Stea Ticket
  and credit pickup, with their refusal/repeat alternatives.
- Check party conversations before and after the letter. If purchasing the used
  Jet Hovercraft, check price, refusal, repeat and vehicle controls, but stop
  before the sea crossing to Daina.

Unexpected Japanese on these inventoried surfaces is a release defect. Full
route traversal, visual appearance, timing and save/load behavior still need
player verification. Static validation and a startup check do not establish them.

## Reproduction and evidence

```sh
python3 -m profiles.alshark.replay ../alshark/original --output work/r08-replay-new.json
python3 profiles/alshark/build_demo.py ../alshark/original \
  --output work/r08-rebuild-new --expand-menu-labels --translate-disk-prompts \
  --exp-multiplier 4 --localization work/r08-replay-new.json \
  --release-plan profiles/alshark/release-mars-leave.json
```

The strict plan requires all 1,034 records together. Immutable commands, source
hashes, allocation bounds, pointer aliases and composed layouts remain checked.
Seven additional menu rectangles retain their original dimensions and gain
explicit label-size and original/output-command guards. Jaguma's short and full
source names have distinct canonical records; both use the given name JAGUMA
in a guarded shared allocation. The full working form is Jaguma Dorian.

Independent inventory covers 506 connected entries. Source collision data proves
that Begi is reachable on the mainland, while Daina is across water. The later
Begi encyclopedia path is excluded using its item acquisition and story-state
evidence, not because it is untranslated. Vehicle controls reuse the previously
reviewed UI; the Video Letter and shop/pickup item names are already cumulative.

See [RE evidence](r08-re-source-evidence.md),
[independent source inventory](r08-qa-source-inventory.md),
[editorial notes](r08-editorial.md), [editorial QA](r08-qa-editorial.md), and
[final QA](r08-qa-final.md). Canonical English retains full scene meaning and
per-record adaptation notes explain secondary omissions. New place/person terms
remain provisional source-based spellings; impact evidence is stored in ignored
`work/r08-terminology-impact.json`.

All **194 regression tests pass**, including native CPU renderer and trainer
checks. Independent binary QA verified all 1,355 compiler patch ranges, exact
IPS replay and preservation of all 878 earlier translations. An isolated
1,800-frame boot displayed the RIGHT STUFF logo and left all six copied disks
unchanged. Final QA records the fingerprints. Full route playtesting remains
pending.
