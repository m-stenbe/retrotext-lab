# September24 playtest screenshot QA

Independent QA visually inspected all22 Desktop screenshots dated2026-09-24, from10:48:28 through12:05:56. The baseline is `work/r04-final-catalog.json` / `work/r04-01-xp4`; neither candidate nor its played User Disk may be overwritten. These observations supersede earlier assumptions that static byte/cell validation established actual rendering. No fix is approved by this inventory.

| Screenshot time | Observation and source mapping | Classification |
| --- | --- | --- |
|10:48:28|SURVIVAL KNIFE followed by FOUND crossing right edge; pickup label `script:051000:034` plus shared pickup outcome/renderer.|Confirmed overflow; dynamic composed result needs validation.|
|10:48:56|MEDS FOUND fits inside the same style box, but FOUND begins on the next row at the name's ending horizontal position.|Comparator for cursor behavior; not proof that a simple newline resets x.|
|10:50:13|PLANET HOM starts far into a small title box and crosses its right edge; `ui:System:011329`.|Confirmed title overflow.|
|10:52:21|SAXEN CANYON crosses the title box; `ui:System:011723`.|Confirmed title overflow.|
|10:55:32|Meteor cinematic splits OPENED as OPE / NED; `cinematic:meteor` token083.|Confirmed automatic mid-word wrap.|
|10:55:49|Meteor cinematic splits OUR as OU / R; same record tokens115/117.|Confirmed joined-span mid-word wrap.|
|11:00:00|CAMP KIT's final T extends beyond selected item name area; icon consumes its own cell. `item-name:camp-kit`.|Confirmed narrow-inventory capacity defect.|
|11:06:01|STEELBODY reaches/crosses equipment-box edge; `r03-equipment:item:74`.|Confirmed narrow equipment consumer defect.|
|11:16:11|Jane introduction plus GIVE NAME? runs past right and bottom edges; `script:052000:013`.|Confirmed composed choice-prompt overflow.|
|11:16:32|PART TIME INVENTORY IS HARD ALONE. WANNA HELP? fits visible body; `script:052000:072`.|Screenshot alone cannot prove missing yes/no versus pre-choice wait. Inspect control flow.|
|11:19:34|PROTECTOR final R lies outside selected-name area, while SHIRT fits; `item-name:protector`.|Confirmed8-cell name capacity comparator.|
|11:20:34|SION AND PALSFULLY merges and overruns row; HEALED wraps with orphan Y. `script:052000:041`.|Confirmed narration control/cursor issue, not only English length.|
|11:22:29|Woman's Zolias warning fits four body lines, but the isolated I is visually separated from HERE.; `script:052000:014`.|User confirms excessive tab-like spacing was the concern. Inspect actual spaces and reflow; this is a readability defect, not overflow.|
|11:24:16|BASEMENT BAR overruns title box; `r02-location:2`.|Confirmed title overflow.|
|11:24:40|SION WATCHED AFLA / SHY DANCER merges narration segments and crosses box; `script:053000:001`. A yellow E remains at far right lower down.|Confirmed narration/cursor defect; possible residual text needs reproduced frame sequence.|
|11:28:47|Shop list CAMP KIT, TOOL SET, HAND SAT, TI BOOMER fits with prices, but spaces occupy wider gaps than letter cells.|Wider shop consumer comparator; does not validate inventory/equipment width.|
|11:35:34|JOE is left of the title-box center; `r02-location:103`, Joe's Room.|User confirms miscentering. Fixed Japanese padding was preserved despite the shorter English title.|
|11:38:03|SUBM GUN final N and PROTECTOR final R lie outside selected/equipment-name area; `r02-item:1d`, `item-name:protector`.|Confirms same limiting narrow consumer, including icon.|
|11:58:25|Karu injury narration alternates blue/white within composed sentences; `script:055000:004` tokens292–299. First line blue; later source36 yields blue possessive after white KARU.|Confirmed control36 semantics differ from persistent-colour model.|
|11:58:32|Continuation OFF BY A is blue, SOLDIER! white; same record token299 continuation plus301.|Confirms continuation restores only part of rendered context; page fitting is insufficient.|
|12:04:32|BIOJUNK. A blue, COMPOUND white, IN blue, KIDUN white, MUTATES blue, GENES.white, THE blue; `script:05d000:000` tokens054–060.|Strong repeated evidence that each source36 has line/segment semantics.|
|12:05:56|Seven Japanese ship-service rows while Joe's English greeting appears; `ui:Opening:004478`, unlike translated six-row0048c6.|Confirmed missed menu variant; trace connected selectors and subordinate UI.|

## Independent rendering facts

Inventory/equipment selection in11:19:34 fits eight name glyphs after one icon; PROTECTOR's ninth glyph falls outside. In11:00:00, the P-to-K distance in CAMP KIT is approximately three letter pitches, consistent with one ASCII space advancing two full-width cells. The shop comparator has a wider field and must not be used to approve the narrow consumer. Review all shared names against the strictest actual consumer, including icon, spaces and suffixes.

Titles contain original leading markers/padding plus user-facing text. Visual evidence shows the text starts well inside the box and can overrun it; a nominal twelve-character title limit without cursor/padding accounting is invalid. JOE's short title fits but is visibly left of center, as the user confirmed. The defect is obsolete centering padding.

Narration screenshots show blue first fragments and white text after internal line breaks or name substitution. Source36 repeatedly creates another blue fragment. This contradicts the prior layout model of a persistent colour that can merely be restored with `0_6`. RE must establish the actual interpreter's cursor/colour side effects and validate representative runtime frames. A successful compile, byte preservation, or generic boot cannot close this defect.

## Missed UI variants to investigate

The screenshot's seven-row menu is original Opening004478: hangar, armament changes, emergency repair, development, disassembly, landing and takeoff. The baseline catalog marks it untranslated. Also untranslated are00477d (five-row interstellar travel/space map/data/repair/cockpit),004788 (four-row suffix without interstellar travel), and004430 (combat menu). Their callers must establish reachability from the promised interval and new selector. Combat may remain outside scope, but adjacency alone neither includes nor excludes these menus. The earlier six-row service menu0048c6 does not substitute for004478.

## Approval status

Open. RE owns narration semantics, localization owns cinematic wrapping and Jane's connected prompts, manager owns name/title capacities and service-menu variants. QA owns this inventory and subsequent independent evidence review, not the implementation or packs it approves. Exact edited-source/catalog/build fingerprints and preservation of the original images and played baseline must be checked before final handoff. Runtime evidence must identify which representative rendering cases actually ran.

## Independent title geometry trace

The normal title caller at System0x0721 sets CX=12, BX=1 and DI=0x2d06 before window setup0xf5f3. It sets DI=0x320a before the sole direct call0x0733→0xf597. This is the standard content origin at box origin+0x0504, not an additional label prefix. Overlay entry BL04 resolves to0x705b (file0x1b05b), selects the location pointer table at runtime0xdc38 (file0x10440), and renders the string. There is no length-based centering calculation. Opening0x350b stores the requested width, and the horizontal content tile loop uses CX. The title field supplies12 full-glyph content cells.

Normal UI rendering at System0x1b0b1 treats ASCII space by calling the advance helper twice; each call advances DI by two in normal mode. Thus ASCII space occupies two glyph cells. The `>` branch calls the helper once and occupies one glyph cell. Earlier documentation describing these as one and half cells was incorrect for this normal-mode path. English content spaces need a proven one-cell encoding; new centering padding must be calculated from actual rendered width, not retained Japanese prefix bytes.

| Title | Map / pointer | Original string start / prefix | Current defect |
| --- | --- | --- | --- |
|Planet Hom|11 /0x10456|0x11329, two ASCII spaces|Four obsolete padding cells plus expanded English title overflow.|
|Saxen Canyon|100 /0x10508|0x11722, one `>`; the historical UI record begins one byte later|One obsolete padding cell plus title and oversized internal space overflow.|
|Basement Bar|2 /0x10444|0x112c8, two ASCII spaces|Four obsolete padding cells plus English title overflow.|
|Joe's Room|103 /0x1050e|0x11744, ASCII space plus `>`|Three padding cells followed by JOE leave unequal margins in the12-cell field.|

For a one-cell-encoded title of widthW, floor((12−W)/2) one-cell padding units gives nearest-left centering; odd remaining space cannot be split into half a normal glyph with the reviewed normal-mode `>` behavior. Repacking must still prove allocation and alias safety. Runtime title screenshots are required to confirm final visual alignment.

## Static review of revised packs

QA independently reviewed `work/playtest-localizer-replay-v4.json` and the current public packs. All117 changed equipment displays were compared with their canonical names. They preserve core item distinctions, numeric calibers and variants within eight text cells. The separate PROTECTR abbreviation is recognizable and retains canonical Protector. No editorial blocker was found.

The revised Jane introduction reserves three body rows and a fourth prompt row. Her original name-sharing/refusal controls remain intact. The stock-sorting job wording is natural and faithful; its wait before the choice remains source behavior. The woman's sentence preserves its meaning while placing I at the start of a balanced line. Hotel and dancer captions restore overnight/stage context and explicitly separate their spans. All20 meteor-cinematic changes are whitespace-only padding for the proven25-cell glyph wrap; no story wording or original timing/animation command changes.

An independent fresh original-based combined compilation of this snapshot passes596 records. QA measured compiled name bytes using actual UI semantics rather than string length: ASCII space occupies two cells, `>` one, letters/full-width pairs one. All280 development item/equipment IDs fit eight actual cells. Reviewed route titles fit twelve. Planet Hom renders one padding cell plus ten text cells; Saxen Canyon and Basement Bar use twelve text cells with no padding. JOE renders four padding cells plus three letters, leaving five cells on the right—the nearest-left alignment allowed by whole-cell padding.

Seven-row menu canonical English and adaptation preserve all actions and order. Independent original disassembly confirms System0xba6d selects menu0x0f,0xba76 sets seven rows, and0xba7b sets the original eight-byte selection width. The revised seven-cell box and fourteen-byte selection width agree. Its selection origin0x141c equals table0x4033's box origin0x0f18 plus0x0504. No action dispatch or row order changes are needed. This approves the static geometry change, not its runtime appearance.

Final renderer execution evidence, menu reachability decisions, frozen-candidate gate and binary/pointer/preservation audit remain pending. No claim of a completed visual fix follows from the compilation result alone.

## Final disposition

The historical open/pending statements above are superseded by [frozen final QA](playtest-2026-09-24-final-qa.md). Source, editorial, native cursor/attribute execution and binary audits pass for the stated candidate. Final game pixels and route traversal remain unverified. Related flight menus00477d/004788 and combat004430 remain deferred without new caller-reachability proof; full flight/first-mission UI coverage is not claimed.
