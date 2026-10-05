# R06 independent source inventory

QA independently inspected the original System/Opening images and the cumulative
R05 catalog. This is static source evidence. The route starts after the hotel
kidnapping and follows Tomyu's confession toward Zajil's military station;
the manager owns the final endpoint and integration.

## Story changes and accessible responses

Porkin014's fight sets story19. Reinteraction selects017, which identifies
Commander Geist, summons the Federation police, sets28, clears visibility43/15
and enables45–49. The aftermath therefore requires more than Tomyu's encounter:
Porkin019–028 and Saibal039–042/044/045 contain changed townspeople responses.
QA reviewed all16 manager-authored canonical records against source, including
the100-credit reward and composed Porkin003→020 town description.

Military station map31's original descriptor selects System8c000/bank05e000.
Its objects include initial hostile visibility45–49 and earlier ordinary
station personnel visibility15. There is no surface map9 entrance in the
three ordinary exit rows. Ship flight is a route dependency, not incidental
bonus content. The station's border returns to space map0.

## Flight and combat UI callers

Systeme15c enters the original7000:0 overlay, whose image begins at System14000.
Service10 dispatches to overlay2278. The action input at2309 invokes2d05,
which selects resident menu25 (four choices) or24 (five choices). Menu24
requires engine output at least2400 and an unset original condition bit.
Both variants use the same selector and include map, data, emergency repairs
and cockpit. The five-choice variant additionally exposes interstellar travel.

The command table2d4b dispatches to26c4 (travel),2738 (space map),2e78 (data),
2d55 (repair), and2fac (cockpit). Repair shares previously covered Joe service
messages through343f; it is not a separate unreviewed Japanese repair dialog.
Ship combat4376's input loop43f8 invokes6a1f, selecting menu2c; fighter launch
and recall use2d/2e. Related automatic repair/control and feedback menus are
explicit calls within6a1f..6b63. Resident menu12 is the ground vehicle battle
menu, reached at System8271; menu19 is Tank/On Foot atc689.

The source proves menu highlight widths must change with frame widths. The
selector copies1709 bytes per highlight row; each full-width glyph occupies
two bytes. Guarded immediate locations are:

| Menu | Opening width byte | System highlight immediate | Original bytes |
| --- | --- | --- | --- |
| Flight variants24/25 | 40b1/40b7 | 16d37 | 5 cells /10 bytes |
| Confirm/Change26 | 40bd | 1651b | 2 cells /4 bytes |
| Ship combat2c | 40e1 | 1aa35 | 5 cells /10 bytes |
| Fighter launch2d | 40e7 | 1aa80 | 4 cells /8 bytes |
| Fighter recall2e | 40ed | 1aabe | 4 cells /8 bytes |
| Ground vehicle battle0c | 4021 | 827e | 5 cells /10 bytes |
| Tank/On Foot13 | 404b | c69b | 3 cells /6 bytes |
| Auto/Manual36 | 411d | 1ab06 | 4 cells /8 bytes |

The original Confirm/Change menu is only two cells wide, so even EDIT requires
coordinated widening. Flight/combat origins are byte column32, fighter column34,
confirmation column50; proposed widths remain within the80-byte screen row.
No option row count or branch order may change.

## Newly discovered names and overlay messages

The Space Map action2738 exposes a detail panel at32db independently of
successful travel. It draws all seven stellar-system names and their
political affiliations. System10540..1054c point to seven14-byte allocations
at11768/11776/11784/11792/117a0/117ae/117bc. Affiliation pointers1054e/10550
share117ca (9 bytes),10554/10558/1055a share117d3 (10 bytes), and10552/10556
share117dd (9 bytes). These are ten distinct source strings, fourteen pointers,
immediately before the immutable progression table at1055c.

The detail-panel headings at System1734f are outside the Opening resident
menu catalog and need explicit guarded coverage. They label star, nation,
enemy strength, planet count and moon count. The header renderer uses its
original narrow mode. Dynamic star and affiliation labels start at DI0a40 and
0f40; numeric templates begin1440. Heading changes must preserve those fields.

QA also found the direct ship-battle destruction message at System1a035,
rendered by overlay5fae→31dc, and the fixed Latin ship-name display at1714e
called by HUD30b6→30ec. The latter's original Atlia spelling differs from the
working Atraia term and requires an explicit manager terminology decision.
Late-story literals at179a0 (Karma) and184bf (boarding another ship) require
caller/state exclusions, not inclusion solely because they share the overlay.
Star numeric templates and the debug list01–17 contain no Japanese words.

## Review state

The manager's23 resident UI canonical strings preserve source action order,
conditional variants, destination placeholders and repair/control meanings.
The localizer's current37 story canonical records preserve the confrontation,
rescue, uncertainty about the kidnapping, restored party and post-rescue hotel
branch. Adaptation/layout review and frozen candidate QA remain pending.

## Independently decoded map artwork

QA reconstructed the original INT41/AH12 bitmap decoder from Opening driver
1ea8..1f0b (disk3ea8..3f0b). Its first bytes specify byte-column width and
height. Each column contains four vertical bitplanes, with literal, repeated
byte and literal-run operations. The guarded decoder in ignored
`work/r06-qa-map-images.py` successfully consumes all eight source assets from
the overlay27da descriptor table within their original sector allocations.

QA visually inspected the decoded galaxy map and seven stellar-system diagrams.
**All embedded labels use Latin letters and numbers; no Japanese text appears.**
The galaxy diagram is192×192; the seven details are160×160. The original art
includes stellar identifiers, planet/satellite abbreviations and station labels.
Some spellings (for example ZAZIL and CHAUSNOMU) differ from the provisional
working script terms; the manager has that source evidence for the bible.
No bitmap translation is required to eliminate Japanese in this browsable UI.

The individual decoded images, montage and descriptor/consumption report remain
ignored under `work/r06-qa-map-*`. RGB values use a standard diagnostic palette;
this is text/content inspection, not a claim that emulator colors were checked.
The original map bitmap bytes remain unchanged.

## Late flight literals and CS return boundary

Karma's death narration is selected only by the special battle marker at
resident1a8c. RE traced that marker to enemy profile class8 or10; the reviewed
Zajil/Porkin/Saibal/station encounters instead use classes2,4,6. It is not the
ordinary party-defeat message. See the RE source report for encounter rows.

The Russell Gaier boarding narration requires overlay3a16. Battle initialization
clears that flag. RE traced its setter to AI handler5c2f, selected only by entity
type25, produced by scenario16 in encounter group7 behind story flagfb. QA
independently checked the source dispatch table at System19296: types9–24 use
other handlers5513–5b87, while type25 alone selects5c2f. The group7 region row
at System1860f begins flagfb; the current rescue state does not set that flag.
The handler's comparison against80 concerns an animation counter, not an enemy
ID. Neither excluded late literal is a general failure/help prompt.

QA inspected CS-station roots002–013 and024 under rescue flags19/1a/28.
Their later4a/2d/2c/29/49 branches remain false and existing16 branches select
already translated R04 lines. Roy's root009 alone selects new025 via flag1a;
that record reports the rescue and assigns the next mission. The final source inventory includes these optional CS roots and marks the
unchanged Roy009→025 branch as an explicit terminal edge. QA recomputed255
reachable entries with no text dependencies missing from the release plan.
The endpoint is before reporting to Roy; no physical return to CS was exercised
by QA.
