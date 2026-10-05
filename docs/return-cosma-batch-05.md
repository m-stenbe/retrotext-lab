# Return to Cosma: batch 05

All twelve player screenshots from 2026-09-23 14.26.42–14.30.18 map to three
previously unadapted records. All three now have validated in-game English:

| Screenshots | Entry | Coverage |
| --- | --- | --- |
| 14.26.42, 14.26.48 | 054000:000 | Zolias soldier's broken final words and quiet death |
| 14.26.55 | 052000:083 | Smoking meteor in the huge crater |
| 14.29.46–14.30.18 (nine frames) | 051000:019 | Complete nine-turn conversation with Karu, Lucia missing, and Karu joining |

These were missing coverage, not evidence that build 06 failed to load. The
screenshots confirm the source scene and speakers, not runtime appearance of the
new English. The preceding Opening cinematic remains outside this build's scope.

## Editorial decisions

The existing canonical Karu scene remains unchanged. Its earlier DOES_NOT_FIT
assessment tried to retain every explanatory detail. This adaptation explicitly
omits the older-model rationale and the separate No use, while preserving the
lack of video playback, resignation, the invitation to find Mom and Karu's reply.
The constrained page reads:

```text
HE CAN'T PLAY
VIDEO. WELL,
KARU, LET'S
FIND MOM.
```

All nine exchanges remain, including both greetings, Karu's named self-reference,
Lucia leaving without a word and Sion asking whether she gave a destination.
The full canonical text still contains the older-model explanation.

The crater caption retains meteor, smoke and large pit but omits white and the
explicit bottom-of-pit position. The soldier keeps broken speech, quiet eye
closure and death; the narration uses he after the explicit ZOLIAS SOLDIER
header. No cause of injury, recognition or additional event is invented.

New canonical/editorial work is in `editorial-return-cosma.json`; all three
adaptations are in `adaptations-batch-05.json`. The Karu record and scene in
`editorial-dust-approach.json` are refreshed against the newly exported allowlist
metadata and screenshot evidence. Its canonical English is unchanged; no other
previous catalog record changes. Old source catalogs must be regenerated.

## Preservation and checks

Only the three entries are newly allowlisted. Soldier/crater entries contain
only established text, header/body/color, wait/clear and terminator controls.
Karu retains #Z, #W, #N, #M and #S with their exact payloads. The existing
`alshark-script-format.md` disassembly review establishes counted flag handling
and #W's single argument / preservation of SI; these are not offsets into text.
No new control, page, pointer, renderer change or shared-script adapter is needed.

| Entry | Used / allocated bytes |
| --- | --- |
| 051000:019 | 292 / 296 |
| 052000:083 | 32 / 33 |
| 054000:000 | 86 / 86 |

Standard suite: 69 tests run, 67 pass, 2 optional CPU-emulation tests skip.
An attempt to enable the locally installed Unicorn library exited with signal 4
before test results; no optional CPU-emulation success is claimed for this run.
The EXP implementation is unchanged.

Full original disk import remains byte-identical. New IPS roundtrips pass.
All 394 System byte changes versus build 06 are within these three allocations;
Opening is byte-identical. Non-text token sequences match the originals exactly.
Every other catalog record is exactly unchanged. Existing entries, pointers,
commands, name references, allocation boundaries and page controls are preserved.
Runtime display, return to movement and party-join behavior await playtesting.

## Build

Local build: `work/return-cosma-07-xp4-test/`.
Launcher: `work/Launch Return to Cosma 07 XP4.command`.
Cumulative canonical-derived coverage: 30 entries in 17 scenes, plus the existing
legacy translations. Expanded menus, disk prompts and 4x EXP are retained.
No live emulator, existing disk, saved game or savestate was changed.

Replay the packs listed in `meteor-batch-04.md` from a fresh catalog, using the
updated `editorial-dust-approach.json`, then apply `editorial-return-cosma.json`
and `adaptations-batch-05.json`. Save as `work/adapted-batch-05.json`. Build with
the previous scene selection plus `return-karu-joins meteor-soldier meteor-crater`
and `--expand-menu-labels --translate-disk-prompts --exp-multiplier 4`.

Playtest both soldier pages, the crater caption, all nine Karu turns and return
to movement with Karu present. An old emulator state can restore already-loaded
Japanese text; confirm the English conversation is actually being displayed
before judging its layout.
