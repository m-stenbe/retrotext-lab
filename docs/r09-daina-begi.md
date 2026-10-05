# R09: Daina reunion and the Begi historian

This cumulative section adds **30 adapted records in six scenes**, bringing the
translation to **1,064 records across 107 scenes**. It retains all 1,034 R08
adaptations. One of the new records is the long Daina reunion and ambush; record
counts do not represent equal amounts of dialogue.

## Route and stopping point

After viewing Lucia's video letter through party TALK, use the Jet Hovercraft
to cross the sea to Daina. The section includes the village's residents, hotel,
item shop and memorial, the reunion and escape, Lucia's party dialogue, and the
return to Begi to consult the historian.

Complete the historian's encyclopedia request, read his account, receive the
Trefoil Emblem and check the resulting party conversations. **Stop before
departing for Stea.** Mars Spaceport's changed station-return response is also
included. Other planets, unrelated bus destinations and later story routes remain
outside this section. Original opening credit artwork and Latin map-art
spellings remain unchanged.

## Build and continue

Follow the [getting-started guide](getting-started.md) for disk requirements,
emulator setup and preserving existing saves. From the repository root:

```sh
python3 -m profiles.alshark.replay /path/to/original --output work/r09-catalog.json
python3 profiles/alshark/build_demo.py /path/to/original \
  --output work/r09-english --expand-menu-labels --translate-disk-prompts \
  --localization work/r09-catalog.json \
  --release-plan profiles/alshark/release-daina-begi.json
```

The local XP4 launcher is:

```sh
"/Users/mikaelstenberg/NewProject/retrotext-lab/work/Launch R09 Translation XP4.command"
```

It uses separate configuration, saves, states and screenshots. On other machines,
use the portable build instructions above. Add `--exp-multiplier 4` for the
optional XP4 playtest build. Use a fresh output
directory and continue from an in-game save with the new System and Opening
disks and your backed-up existing User Disk. Older emulator states may restore
old code and text.

## Player verification

- Buy or board the Jet Hovercraft, cross to Daina, disembark and enter the village.
  Check shore movement, encounters and vehicle persistence after the event.
- Speak to all residents; try hotel and shop choices, refusals, repeats and
  insufficient money. Check the original two-row shop selection geometry.
- Inspect the monument, follow the full reunion and ambush, then inspect it again.
  Check narration pages, names, timing, scripted movement and the escape transition.
- Check Lucia's recruitment, TALK, Freeze and Locate displays, and the other
  party members' immediate reactions. Check the changed Mars Port response when
  requesting transport back to the military station.
- Visit the Begi historian, fetch his encyclopedia from the bookshelf and return
  it. Check full-inventory retries, the history lesson, Trefoil Emblem handover
  and repeat lead. Read every party member's resulting TALK response.

Unexpected Japanese on these inventoried surfaces is a defect. Full route
traversal, visual appearance, animation timing and save/load behavior remain
pending player verification; static validation does not establish those results.

## Source and technical evidence

Independent source traversal matches the **546-entry cumulative route closure**,
including 29 new text-bearing scripts and the Daina map label. Static inspection
and independent tile connectivity checks establish the hovercraft route across
water; exact sprite clearance and disembark behavior still need runtime checks.
Lucia's current abilities are already translated and her inspected learning
table adds no new ability names.

The Daina label has a guarded allocation and pointer alias. Shop choices retain
their original rectangle and command bytes. The historian's verified speaker
header now supports continuation pages; the colored encyclopedia title remains
subject to the existing rejection rules. Source hashes, immutable commands,
allocation limits and composed layout checks remain enforced.

The terminology impact report covers all seven new provisional terms and their
scene peers; those connected scenes received editorial review. Existing terms
and the 1,034 prior adaptations are preserved. The report remains under ignored
`work/r09-terminology-impact.json`.

See [RE evidence](r09-re-source-evidence.md),
[independent source inventory](r09-qa-source-inventory.md),
[editorial QA](r09-qa-editorial.md), [final QA](r09-qa-final.md), and the
[prior-batch validation](pr-backlog-qa.md). All 202 regression tests pass, including
native renderer and trainer checks. The strict section gate passes for all 1,064
records. Independent binary QA verified all 1,386 compiler patch ranges, exact IPS
replay and preservation of every earlier adaptation. PR review can precede player
testing.

An isolated 1,800-frame startup check exited successfully and displayed the RIGHT
STUFF logo. All six copied disks remained unchanged. This confirms startup only;
full route and visual verification remain pending.
