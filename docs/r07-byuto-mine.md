# R07: Roy's assignment and the Byuto mine

This cumulative candidate contains **878 adapted records across 88 scenes**,
retaining all 821 R06 records. The 57 additions comprise 54 dialogue records and
three map labels. Records can contain multiple turns; this is not a whole-game
completion percentage.

## Route and stopping point

After rescuing Shoko, return to CS Station and report to Roy. Follow the
secretary's directions, collect the interstellar engine from the laboratory,
and travel to Byuto in the M861 system. Visit Kainan, including its shops and
optional bar, then investigate the mine. Hidden passages, the ambush, the boss,
the optional Ray Ball gift and its alternatives, and subsequent town and party
responses are included.

You may return to CS Station, but **stop before reporting to Roy again after
the Byuto victory**. That report starts the next section. Exploration of other
planets and unrelated stations remains outside this candidate. Opening staff
credit artwork remains Japanese; original Latin map-art spellings remain intact.

## Launch and continue

```sh
"/Users/mikaelstenberg/NewProject/retrotext-lab/work/Launch R07 Translation XP4.command"
```

The launcher uses `work/r07-01-xp4`, XP4 battle rewards and separate emulator
configuration, saves, states and screenshots. Continue from an **in-game save**
using the new System and Opening disks with your existing User Disk. The fresh
candidate User Disk has no previous progress. With the emulator closed, copy
your existing User Disk into the candidate, keeping the old disk as backup,
or select it when loading. Old emulator save states can restore old code/text.

## Player verification

- Report to Roy after Shoko's rescue. Check the full briefing and party TALK.
- Ask the secretary for directions; visit the lab. Check engine grant, the
  full-inventory refusal if available, repeat dialogue and fitting instructions.
- Check Atraia upgrade advice, warp selection, destination confirmation and
  landing on Byuto.
- Talk to every Kainan resident and bar patron. Check shop choice highlights,
  purchases, insufficient funds, Ray Ball grant, full inventory and repeats.
- Follow all mine passage hints; check ambush, boss narration, battle and return.
- Revisit town residents and party TALK after victory. At CS Station, check
  optional follow-ups but stop before the next Roy report.

Unexpected Japanese on these inventoried surfaces is a release defect. Full
route traversal, visual appearance, timing and save/load behavior still need
player verification. Static checks and a boot smoke cannot establish them.

## Reproduction and evidence

```sh
python3 -m profiles.alshark.replay ../alshark/original --output work/r07-replay-new.json
python3 profiles/alshark/build_demo.py ../alshark/original \
  --output work/r07-rebuild-new --expand-menu-labels --translate-disk-prompts \
  --exp-multiplier 4 --localization work/r07-replay-new.json \
  --release-plan profiles/alshark/release-byuto-mine.json
```

The strict plan requires all 878 records together. Source hashes, immutable
commands, allocation limits, name aliases and composed layouts remain checked.
New shop menus retain their original geometry and have explicit rectangle
validation. Three label allocations are guarded against prior pools. Enemy
combat action values were traced to effect/animation descriptors rather than
assumed to be new displayed ability names.

See [RE evidence](r07-re-source-evidence.md),
[independent inventory](r07-qa-source-inventory.md),
[mission editorial review](r07-editorial.md),
[editorial QA](r07-qa-editorial.md), and [final QA](r07-qa-final.md).
The manager additionally reviewed the complete town, shop, bar and map-label
packets from Japanese context. Canonical prose preserves details shortened in
the ROM; individual adaptation notes record those omissions. New working terms
are Eibe, Kainan and interstellar engine; impact evidence is stored in ignored
`work/r07-terminology-impact.json`.

All **186 regression tests pass**, including native CPU renderer and trainer
checks. Independent binary QA verified all 1,193 compiler patch ranges, exact IPS
replay and preservation of all 821 previous translations. The isolated
1,800-frame boot displayed the RIGHT STUFF logo and left all six copied disks
unchanged. See final QA for fingerprints. Full route playtesting remains pending.
