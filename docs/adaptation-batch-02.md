# Second canonical-derived adaptation batch

Six entries in two connected scene groups now have reviewed adaptations:
Shoko's invitation (051000:002, 011, 012, 013), and the old woman's wasteland
warning/return report (008, 021). The existing canonical English, context,
source metadata and editorial fingerprints are unchanged.

Shoko retains her age and indignation, Dad's quoted refusal, the invitation,
Sion's hesitation, the handgun reveal, the euphemistic “borrowed,” two weapons
for protection, the gendered refusal taunt and the knowing retry question.
The adaptation omits “this morning,” the separate “Honestly,” and the drawer
and laugh in the weapon reveal. The retry becomes “Heh... Coming after all?”
The warning retains the wasteland and canyon origin; the return report retains
“as if” rather than asserting possession. That return line reuses the existing
adaptation after comparing it with canonical intent.

The profile's original allocations, immutable tokens and 14-cell/four-row
limits are unchanged. No new page breaks or commands were added. The pack
includes every text token of every entry in both selected scenes.

Reproduce after preparing the first batch catalog:

```sh
python3 profiles/alshark/localization_tool.py adapt /path/to/original work/adapted-batch-01.json \
  --adaptation-pack profiles/alshark/adaptations-batch-02.json --output work/adapted-batch-02.json
python3 profiles/alshark/build_demo.py /path/to/original --output work/editorial-batch-02-playtest \
  --expand-menu-labels --localization work/adapted-batch-02.json \
  --localization-scenes story-canyon-directions story-lucia-rest story-work-interactions \
  story-dead-gigi story-shoko-invitation story-wasteland-and-return
python3 profiles/alshark/batch_tool.py /path/to/original work/adapted-batch-02.json \
  --plan profiles/alshark/batch-town-and-canyon.json --output work/town-batch-02-final
```

Validation: 58 tests pass; source/editorial/layout/allocation checks and IPS
roundtrips pass. Compared with batch 01, Opening is identical and all 419 changed
System bytes are inside these six entry allocations. The combined build selects
13 entries in six scenes. The batch packet reports six ready scenes and eight
still deferred; this is not complete town or canyon coverage.

Playtest Shoko's initial invitation, refusal and retry, then acceptance and weapon
reveal. Check the highlighted handgun, pauses and the final “Let's go!” line.
Check the old woman's warning before departure and her return report when the
story reaches that branch. These paths have not yet been runtime-verified for
this build. No emulator was restarted and no live save/state was transferred.
