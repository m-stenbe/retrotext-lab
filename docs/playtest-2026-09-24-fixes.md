# September 24 playtest revision

This revision fixes the 22 screenshots from the clean R04 playthrough. It retains
R04's story boundary and adds the seven-action bridge menu encountered after the
first briefing. Flight, combat and the subsequent mission are not claimed as
translated by this revision.

- Blue is the original narration style. Translated line breaks now restore its
  attributes, avoiding arbitrary white segments within the same narration.
- Correct cursor behavior prevents Jane's prompt and the hotel/dancer captions
  from running together. Pickup callers start a new line before the shared FOUND
  script, which otherwise inherits the cursor's horizontal origin.
- Generic name spaces use the renderer's one-cell skip. Location padding is
  recalculated for a twelve-cell box, including Planet Hom, Saxen Canyon,
  Basement Bar and Joe. The complete first two names remain intact.
- Item and equipment labels fit eight name cells plus the icon. The previous
  nine-character allowance was incorrect for inventory and equipment screens.
- The meteor cinematic uses word-aware padding, preserving timing/animation
  commands. Validation rejects automatic line breaks inside words.
- The woman describing the Zolias troops starts “I” on its own line, removing
  the conspicuous space after the preceding punctuation.

Canonical wording, abbreviations and the related Jane dialogue review are in
[the editorial notes](playtest-2026-09-24-editorial.md). Source/renderer evidence
and independent findings are in [the screenshot inventory](playtest-2026-09-24-qa.md)
and [renderer notes](playtest-2026-09-24-renderer.md).

## Rechecking in game

Check the four house pickups, both early world-map titles, item/equipment lists,
meteor cinematic, Jane's introduction and choice, hotel and dancer narration,
Joe's room title, Karu and Kidun narration, and the seven-action bridge menu.
Static validation and interpreter checks do not replace this visual playthrough.
The earlier R04 build and its saves are kept separately.

## Build and launch

The revised candidate is `work/r04-02-xp4`, built from originals with the complete
`release-playtest-fixes.json` gate: 596 adapted records across 62 scenes.
Launch `work/Launch R04 Fixes XP4.command`. The original XP4 progression setting
and the user's keyboard configuration are retained.

All 162 tests pass, including five tests executing original 16-bit renderer code.
Those tests mock platform glyph lookup/drawing; they establish cursor and
attribute behavior, not full emulator screenshots. The separate 1,800-frame
RetroArch boot smoke exited successfully and rendered the opening logo. Complete
visual rechecking of the changed scenes is still pending.

After the original-based image/IPS audit, the played R04 User Disk was copied once
into this new build. Its hash equals the pristine User Disk, so this copy does
not establish that playthrough progress was saved to disk.
`work/r04-02-xp4/save-migration.json` records matching source
and destination hashes plus the pristine candidate User Disk backup. Continue
using the game's normal Load option; previous emulator save states are not
imported because they also retain old loaded scripts. The old R04 build and all
original disk images remain unchanged.
