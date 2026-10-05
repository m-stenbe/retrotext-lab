# R03 Hom spaceport, abandoned mine and first bridge

Read-only evidence from the hash-guarded original PC-98 System/Data images,
2026-09-23. Disk offsets are hexadecimal. Full source and disassembly remain
under ignored `work/r03-re-*`. This is static evidence, not emulator traversal.

## Connected route and boundary

R02 ends with the Hamack report setting story flag `11`. Hom map 11 has the
unguarded spaceport exit `(39,98)→42`; the mine exit is `(27,7)→96`.
At the spaceport ticket barrier, `054000:034` tests `12` first (repeat
entry 030), then `11` (entry 029). The party cannot buy the queued tickets;
Joe proposes his ship hidden in the abandoned mine. Entry 029 sets `12`.
The next connected objective is therefore retrieving the ship, not immediately
flying to Mars.

| Map | Metadata / bank | Objects | Tile triggers |
| --- | --- | --- | --- |
| Hom Spaceport 42 | `8ec00` / `054000` | Entries 003–025; 006–012 require visibility `16`; three later objects select 036 with visibility `5d` | `(9,47)`→027 |
| Abandoned Mine 96 | `9c400` / `054000` | Two ship objects select 031 with visibility `f8` | `(15,37)`→001 |
| Bridge 1 | `84800` / `083000` | 001 (`fa`), 005 (`fe`), 004 (`fd`), 002 (`fb`), 003 (`fc`) | Cockpit `(16,21)`→000 |

All three maps have empty explicit exit lists. `r03_flow.map_inventory` parses
these original descriptors, counted 18-byte objects and five-byte triggers.
Port and mine border returns lead to Hom. The bridge uses a separate bounded
movement loop; its metadata border field is not an ordinary walk-off exit.

Mine entry 001 tests `1f`→028 (already-open repeat), then `0f`→002
(Joe opens the hidden mechanism). Entry 002 sets story flag `1f`, changes
map tiles through `?O`, sets tile-event flag 03 through `?M`, and requests
a redraw with `?I 00`. `?M` is not a cinematic call: handler `dc27`
uses the tile-event bitmap at `19b8`.

Ship interaction 031 introduces and renames the ship, sets story flag `13`,
then executes `?I 03`. This command dispatches at `dd39` through word table
`dd4d`; selector 03 invokes `ddca`. The handler runs entity/sound animation
`dde6`, clears visibility `f8`, sets map ID 1, and jumps to `0327` (the
16-bit target wraps; a disassembler may print `10327`). It does not call the
rescue scene. No new text-bearing cinematic interpreter stream occurs in this
route; the animations use existing entity and sound operations.

The endpoint is the first controllable bridge, including its three present
crew interactions and reachable service menus, **before stepping into the
cockpit**. Bridge root 000 is the next-section boundary: without later flag
`14`, it calls `054000:032`, the distress/boarding event. That record and
subsequent space-flight/battle surfaces are not implicitly included by the
ship acquisition boundary.

## Visibility, story state and script closure

Visibility flags use a different bitmap from story conditions. Initial
System `1998..19b7` includes `16` and `f8`, but not `5d`. Early scripts
clear bridge actors `fb/fc` (`051000:000`), enable Shoko `fa`
(`051000:011`), Karu `fe` (`051000:019`) and Joe `fd` (`05a000:039`).
The port's 036 objects require `5d`, set only on a later route; their call
`05e000:029` is not an R03 root. Mine ship visibility `f8` is cleared by
boarding itself, preventing an assumption of repeated acquisition.

The conservative closure in `r03_flow.py` contains **67 script entries, 56
with text**, of which **37 require new adaptations** relative to the frozen
R02 catalog. The new text entries are:

- `054000`: 001–003, 006–029, 031, 033–034.
- `07d000`: 032–034.
- `082000`: 024.
- `083000`: 001, 004, 005.

Control-only roots/dependencies are retained in the closure. Port ticket-holder
response 033 is included conservatively even though its flag `16` has no
setter before this endpoint. The global party closure adds these explicit paths:

| State | Dispatcher / callee |
| --- | --- |
| Mine lead `12` | Karu `082000:023→024`; Joe `082000:002→025→07d000:034` |
| Ship acquired `13` | Shoko `082000:000→026→07d000:033`; Joe `082000:002→027→07d000:032` |

The flag-13 global responses anticipate later danger, but the command bytes
unambiguously select them at `13`; no hexadecimal/decimal entry confusion is
involved. They remain conservative extra coverage: the bridge has direct
crew-object conversations and its service menu, not the ordinary global TALK
menu. Both later-party flag tests and later bridge actor responses are excluded
by the bounded setter set. Existing early party responses remain cumulative.

## The bridge service menu is reachable before the cockpit

This is a required part of R03, not an optional post-release surface. The
boarding handler enters `0346`, which loads map 1 via `facf`, then `0629`
loads character placements from `4b38`. The first word is `5e26`: player
screen x=38, y=94−48=46. Scroll state `1a18` is 24. The bridge loop
reads input at `03b2→e6be`, handles tiles/movement at `03cd→0ce5`,
then object collision at `03d0→e4ef`.

Move down from `(38,46)` to `(38,47)`, then `(38,48)`. One further down
input takes `129f→12d2→bad4`, opening the service menu. The cockpit
requires metadata x=16, equivalently screen x=32 at this scroll position;
the straight-down path stays at x=38 and cannot activate it.

The collision proof uses map-grid descriptor `01 55 08 01`, System
`abc00`; tileset 27's quadrant descriptor `02 3e 07 01`, Data `7d800`;
and its attribute descriptor `02 3e 08 01`, Data `7dc00`. Renderer
`e2f8` expands each source tile into four quadrant bytes, starting at map
row 12 for scroll 24. Collision reader `e4ca` resolves animated indices,
then keeps the high nibble of each attribute. Expanded screen rows 23/24,
columns 19/20, and the doorway in row 25, columns 19/20, all have collision
property zero. The adjacent row-25 cells 18/21 are walls (`10`). These are
the middle bottom cells tested for downward movement; the unchanged crew
placements do not intersect the bottom doorway. Thus the menu must not be
excluded merely because no action-button menu call appears in the bridge loop.

`bad4` shows table selector `32`, string Opening `48c6`, with six options.
Its selections route to hangar `bb33`, equipment `bd77`, repair `c1b2`,
development `c2cb`, disassembly `c57b`, and system `b047`. The credit/scrap
header uses selector `33`, Opening `48fa`. Ship parts, manufacture availability,
item names and stat displays are additional required inventory domains; see the
independent R03 QA inventory. No claim of completeness follows from the script
closure alone.

## Service-overlay message adapter

`bb20→bb2d` invokes overlay service `7000:3442`, loaded from System
`14000`. It looks up the message pointer at `347f + 2*CL`, draws the Joe
header at `34c3`, and renders the selected message with `3244`. The
renderer maps ASCII capitals through interrupt 41 service 19. A `>` skips
one full cell, a literal ASCII space skips two, and `@` advances a row.
The dedicated `r03_ui.py` encodes English spaces as single-cell skips,
keeps uppercase ASCII and supported full-width punctuation, and rejects
unsupported glyphs. It guards the original System hash and renderer bytes.

The service overlay exports 18 fixed allocations: Joe's header at `174c3` and
17 messages at `174c9`, `174ea`, `17519`, `17553`, `1757c`, `175a3`,
`175cc`, `175f2`, `17633`, `17669`, `176a1`, `176e8`, `17777`, `177a8`,
`177d5`, `177f0`, `1780a`. These cover greeting, empty/full hangar,
withdraw/store, manufacture, missing scrap, missing fighter/tank, and repair
alternatives. Adaptations retain their original allocations; command code,
pointers and unselected bytes do not move. Text allows at most 14 cells in
four message rows below the header.

Dynamic fields remain blank at their fixed coordinates (zero-based message
rows/columns): withdraw/store row 1 column 0 width 9; manufacture quote
row 0 column 0 width 9 and row 2 column 0 width 6; completed manufacture
row 0 column 3 width 9; repair cost row 1 column 5 width 5 and yes/no
selection row 3 column 0 width 8. Corresponding writes are at resident
`bd42`, `c558`, `c56b`, `c3db`, `c244` and its continuation. The compiler
rejects any text overlaying those fields.

The additional `fixed:System:00209a` record covers the hangar's attempt to
unload ship equipment as a carried item. At `bb6f` only type 1 follows the
ordinary item path; other equipment reaches `bb93→d4ea` with script `209a`.
Its original allocation ends at `20c8`. The adapter retains its speaker controls
and runtime Joe name, edits only `t004`, and uses the existing immutable script
rebuilder plus fourteen-column/four-row layout validation. This brings the
service adapter to **19 records**; the fixed script uses the field dialogue
renderer, not the overlay message renderer.

The scoped menu geometry helper widens only Opening table `4105` from four
to seven cells and `4039` from four to six cells, paired with System
selection-width instructions `baf8` and `bb41` (two VRAM bytes per cell).
Anchors, row counts, choices and all text pointer slots remain unchanged;
the existing interface adapter subsequently relocates the translated menu
strings into its guarded pool. Neither menu extends beyond the display.

## Validation limits

Focused source tests reject altered progression commands, missing closure
targets, changed map metadata, runtime-field overwrite and partial geometry
changes. They also verify that compiling a selected service header changes
only its original allocation. Static source, original hash and byte-preserving
checks do not establish runtime menu rendering, animation timing, name width,
selection behavior or save/load correctness. Those remain candidate/playtest
checks; no emulator traversal is attested here.
