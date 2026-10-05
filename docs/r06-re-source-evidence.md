# R06 Porkin pursuit, space flight and Shoko's rescue

Original-image static inspection, 2026-09-28. Full source remains ignored in
`work/r06-re-route-packet.json`; the cumulative baseline is R05's final catalog.
This inventory does not claim a completed emulator traversal.

## Connected route and endpoint

The Saibal kidnapping sets story18 and enables Porkin object014's visibility
43/44. That object starts the Tomyu fight and sets19. Interacting again selects
017, the interrogation: it identifies Commander Geist at the military station,
sets28, removes43/15 and enables45–49. Town victory alternatives are now available.

Military Station31 is metadata System8c000, bank05e000. It has no ground tile
entrance from Zajil's surface. Its border returns to map0, the distinct space
mode. The next connected route therefore requires Atraia flight, landing and
potential space combat, rather than another surface-only section.

Space map0 metadata has a specialized format. Header15 points to a sixteen-word
sector directory atSystem843c0. Each sector has a count and eight-byte records:
type, little-endian x, little-endian y, destination map, destination x/y. The
sector starting843e0 contains Military Station31:
`0b 68 74 e8 6e 1f 22 34` (space7468,6ee8, destination31 at34,52).
The same sector contains CS Station30 at744c,6e2d, so the military station is
southeast of it in that sector. The original overlay is loaded from System14000
at7000:0. Service0e→1b0b receives the sector directory and metadata pointers;
1b64 chooses a sector; service11→2449 scans its count/eight-byte records and
24ba stores the destination map. It displays the landing confirmation and returns
state to the resident System code. This proves the connection without treating
space metadata as ordinary eighteen-byte town objects.

Station31 objects include Shoko000 (visibility45), Geist028 and guards025–027
(46), blocking fights001/002/003 (47/48/49), and ordinary station personnel
004–011 (15). Entry028 calls header013 and jumps000. The Geist fight000 uses
`?F 05 04 00 ff 1c 14`, removes46 and sets1a. The subsequent000 interaction
selects016: the reunion adds Shoko, removes45 and restores party visibilityfa.
All immediate station personnel's flag1a alternatives017–024 are included.

The endpoint is **after Shoko's reunion and immediate military-station / party
follow-ups, before reporting to Roy at CS Station for the next assignment**.
Returning to Roy after1a selects05c000025, which gives the next mission; that
explicit action is outside this section. `TERMINAL_EDGES` records this exact
05c000009 flag1a→025 boundary while retaining the source command and all
other optional CS interactions; it does not claim Roy is inaccessible. Other-planet exploration beyond its
landing notice is also outside it. Destination labels and all mapped flight UI
are translated, including optional navigation and ship-combat controls.

## Scripts and state alternatives

`r06_flow.py` retains R05 roots and adds Porkin014 and military-station roots
000–011/025–028, plus optional CS Station roots000–013/024. The closure has255 entries and53 newly text-bearing records
relative to R05. Story bounds add19,1a,27 (Porkin reward) and28. They retain
shop/service/ticket alternatives and earlier branches conservatively.

New Porkin postvictory dialogue is019–028, with the one-time100-credit reward
and its repeat. Saibal postvictory039–042/044–045 and hotel reunion morning036
are included. Party flag28 selects Joe008 and Welda009 in bank081000; flag1a
selects Shoko010, Joe011 and Welda012. Speakers are established by the headers
in082000 before the corresponding cross-bank calls. The exact call dictionary
is supplied for composed-layout validation. New pure shared headers05a012 and
05e013/014/015 all have clear/header/text/body/end shape.

Later station visibility5d, later shared-bar partitions and later assignment
flags are excluded by this bounded source state. The earlier R05 evidence
continues to establish Saibal bar partitioning and Zajil's wrapping surface.

## Flight menu geometry and runtime fields

All new menu widths are paired with source-guarded selector widths. Box descriptors
remain at their original screen anchors and retain row counts and choice order.
The selectors count bytes; a full-cell glyph occupies two bytes.

| Opening descriptor | Width | System selection instruction |
| --- | --- | --- |
| 40b1 /40b7, navigation | 5→7 | 16d33, shared |
| 40e1, ship battle | 5→7 | 1aa31 |
| 40e7 /40ed, fighter | 4→6 | 1aa7c /1aaba |
| 40bd, confirm/change | 2→6 | 16517 |
| 4021, vehicle battle | 5→6 | 827a |
| 404b, tank/on-foot | 3→4 | c697 |
| 411d, automatic/manual | 4→6 | 1ab02 |

`r06_ui.widen_menus` guards the original six-byte descriptors and matching
five-byte selector instructions before changing9 box-width bytes and8 selector
immediates. It checks screen bounds and deduplicates the shared navigation
selector. Original source hashes remain checked by the integrated compiler.

The navigation menu uses its five-option variant when the engine threshold and
state permit warp; otherwise it uses four options. Both are translated. The
repair action reuses the already guarded R03 service dialogs. The fighter loss
message atSystem1a035 is a separate literal and is included.

Landing prompt Opening4897 and warp confirmation47e0 each have four rows.
Overlay252f and26e4 write the runtime destination atDI321c in row0. The new
validation hook reserves row0, keeps row2 blank, requires the explanatory and
confirmation rows1/3, and enforces twelve cells. Generic menu width validation
alone does not protect this injected field.

The star-information header System1734f is rendered in half-width mode atDI0a3c.
Dynamic star/faction/force fields start at column4 on rows0/1/2. The unchanged
numeric templates at17382–1743e put planet and moon counts in columns4–6 and
12–14 of row3. Therefore the reviewed header is `STAR/GOVT/FOES` and
`PLAN    MOON`, with the four intervening cells reserved. `encode_fixed` guards
that field geometry. The native renderer at171eb maps uppercase ASCII to glyphs;
`>` advances one cell, literal ASCII space two. English spaces are encoded as
single-cell skips. No Japanese glyph, color or cursor routine is patched.

The HUD's literal System1714e spells the source ship name `Atlia`; the existing
working name is Atraia. The reviewed replacement is `ATRAIA`, six cells in its
original ten-byte allocation, using the proven31dc uppercase renderer. This
records a source spelling variant rather than changing the established name.

## Names and image surfaces

`r06_names.py` adds41 guarded records: space-mode and military-station map labels;
seven star-system names; three affiliation groups; and all29 unique landing
labels. Landing names are a separate inline table1654a–165a4, whose relative
base is14000, distinct from the shared names'10000 base. All pointer aliases and
original allocations are checked; no pointer is inferred from script adjacency.

The seven star IDs preserve the original Latin letters and numbers. The display
suffix `SYS` is an explicit abbreviation of System. Digits use the original
full-width glyph encoding, whereas letters use the established ASCII dispatch;
this fits each fourteen-byte allocation without weakening font validation.
Map labels use the existing reviewed centering adapter. Landing labels identify
destinations even when their subsequent exploration is beyond the route boundary.
Unestablished planet romanizations remain working spellings in the bible.

Independent QA decoded the original RLE space-map illustrations and inspected all
eight resulting images. Their labels are Latin/numeric, with no Japanese text.
They retain artwork spellings such as ZAZIL; this is separate from the current
working names, not a new original-image modification.

## Battle and validation

The station's battles use the established on-foot ?F interpreter, with the
Geist encounter additionally selecting its original background resource1c.
Party composition returns to the already covered Shoko, Joe, Karu and Welda
profiles; R05 covers Welda's innate abilities. On-foot targeting, rewards and
reload surfaces remain cumulative. Flight and fighter controls/results are
covered separately above; no playtest claim follows from static menu discovery.

Ten focused RE tests pass: route closure/state exclusions/source guards;
forty-one-name compilation, alias mutation and allocation preservation; all
seventeen geometry changes and shared selector consistency; runtime-field
rejection; literal-source/byte-boundary preservation; and current encounter exclusions for
the later Karma/boarding messages. Final cumulative fit,
image preservation, independent QA and player traversal remain integration checks.

## Source exclusions for later literal messages

The overlay also contains Karma's defeat message at179a0 and Russell Gaier's
boarding message at184bf. Neither is silently left as an unknown surface.

On-foot battle processing7e39 sets special state1a8c only when a defeated
profile's type byte is08 or0a. Loaderfb98–fba7 loads resource1b into segment6000;
its descriptor3f35 is0108070a, System11800. Encounter selection5e31 uses the map
header25 table; each group has an eight-byte header and eleven-byte enemies.
The profiles are selected by sprite−12hex through6000:02ae, and profile+0c
becomes the tested enemy+22 field. All Zajil surface groups use sprites24–27,
whose profile type values are6/2/2/2. Porkin and Saibal use sprite109, type4;
military-station groups use111/112, both type4. These are decimal sprite IDs.
Their source profiles are System12b02/12b19/12b30/12b47/132a5/132d3/132ea.
None can satisfy the08/0a predicate, so the Karma message is outside this route.

Space battle initialization4376 clears boarding state3a16. Its only setter is
5c55 in AI handler5c2f. The enemy AI dispatch table5296 maps entity type25
uniquely to5c2f; other ordinary enemy types9–24 select distinct handlers.
Initialization46d4 adds9 to the scenario ID, so this special handler requires
scenario16. Encounter group7 supplies only scenario16. The only region selecting
that group is System1860f, whose raw record is
`fb1177f08505791089ff07`; it requires flagfb through the151a bit8 test.
Overlay151a corresponds to resident1997, the flagfb bitmap byte/bit. No setter
for this flag occurs within the bounded R06 route. Ordinary groups0–6 select
scenarios0–15. The comparison with80 inside5c2f is an animation counter, **not**
an enemy ID; the exclusion depends on the dispatch/type/flag chain above.
Therefore the later Russell Gaier boarding message is outside this state.
