# R04 distress rescue, station induction, tour and first briefing

Read-only inspection of the hash-guarded original System image, 2026-09-24.
This is static evidence, not an emulator traversal. Full extracted source is
kept in ignored `work/r04-re-route-packet.json` and `work/r04-station-source.txt`.
The cumulative baseline is `work/r03-final-catalog.json`.

## Route and endpoint

The first Atraia cockpit event `083000:000` calls `054000:032` before flag14.
The distress call identifies a Mars civilian vessel with the same Zolias ship
seen during the earlier killings. Its final `#Q 34 3c 68` enters **map104**:
Q's payload is x,y,map, so the first byte must not be read as the map ID.

| Map | Metadata | Bank | Source roots |
| --- | --- | --- | --- |
| Civilian ship104 | System9e400 | 055000 | Tile triggers001,002,003,000 |
| CS station30 | System8bc00 | 05c000 | Arrival trigger001, crew/NPC objects000–013,024 |

Map104's eleven objects all have script index0; their visibility bytes0a–0d
are animation actors, not script IDs010–013. Its four tile events are
`(34,18,06,01,00)`, `(34,20,05,02,00)`, `(34,28,04,03,01)`, and
`(34,30,0c,00,01)` in hexadecimal. Event002 warns the party;001 overhears
the hostage exchange and jumps to004. Event004 is the continuous confrontation,
rescue and escort scene. It sets14 and ends `?I05 1e00; #Q09 0a1e`, entering
station30 at its arrival trigger. The resulting conscription conversation001
sets15 and adds the new crew member. Therefore rescue004 alone is not a complete
arrival boundary.

The station tour includes all ordinary NPC roots, both responses to the station
acronym question, repeat summons, scientist, hangar guard, secretary and Roy.
Scientist007 sets23, guard012 sets24, operator004 sets25. Four occurrences of
`#A 23 24 25 0e` require all three flags and dispatch014;014 sets26 and switches
Roy's visible object from the command room to his private room. Talking there
runs009→05d000:000, the complete first mission briefing, which sets16. The
endpoint is **after this briefing and immediate station follow-up interactions,
before leaving the station for the first assignment**. No destination mission,
space-flight combat or planet exploration is promised by that endpoint.

Station metadata has no explicit exit rows. Its ordinary border tuple is
`0a 23 63`: the established loader f6ca and movement handler1237 interpret this
as target map9 (target+1), destination(35,99). It is not a direct bridge pointer.
Physical traversal of that border remains a runtime check. The source inventory
conservatively includes bridge flag16 barks and takeoff text as additional
coverage, without claiming that this departure is within the promised route.

## State, dependencies and guarded inventory

`profiles/alshark/r04_flow.py` bounds story tests by cumulative R03 flags plus
14,15,16,23,24,25,26. Its closure has **85 entries,67 text-bearing records**, of
which **41 need new adaptations** relative to R03. Control-only entries remain
in the inventory. Later station branches29/2c/2d/49/4a and visibility5d actors
are excluded by source state, not by their bank position.

The global TALK roots must include082000:003 for the newly recruited warrior.
Flag15 selects Shoko028→07d000:031 and Joe029→07d000:030. Flag16 selects
Shoko030→081000:001, Joe031→081000:002 and warrior032→081000:000. Her pre16
response is the text in082000:003 itself. Conservative bridge additions are
083000:002,007,008,012. Earlier party/bridge/service text remains cumulative.

The previous generic R02 edge helper recognizes #A only with two flags plus
a target. R04 introduces three flags plus a target. The new inventory accepts
a counted flag list and checks every required flag against the bounded set;
this does not modify commands. Shared validation/layout adapters must likewise
retain and correctly follow these four-byte payloads.

## Animation and text surfaces

There is no `?V` text-cinematic command in the85-entry closure. Narrative during
the rescue, induction and briefing is ordinary immutable-token script text.
The counted `?I` dispatcher atdd39 indexes the word table atdd4d. Its selectors
used here are existing entity/display operations: selector0 atdda2 requests a
redraw; selector1 atdd77 drives actor records; selector2 atddb9 iterates actor
commands; selector4 atdef4 preservesSI, loads graphic resource13 and invokes
interrupt41 service12, then restoresSI and returns. Selector5 atdfad configures
map/party placement, and selector8 atdfef invokes display update routines0470
and041e (16-bit relative calls), preservingSI. These handlers do not contain
inline narrative strings. Source routines and original hashes remain immutable;
no new cinematic reinsertion adapter is required by the proven script closure.
This does not attest to animation timing or runtime image appearance.

New non-script source coverage comprises shared character names08/09 and map
labels30/104; the manager owns their guarded adapter and editorial packs.
Independent QA records the exact title pointers, source allocations and22 ship
interior aliases in `docs/r04-qa-source-inventory.md`. The source's leading title
markers must be retained. Existing menu, item/equipment, save/load and service
adapters remain required cumulative dependencies. No new shop, item award or
battle-initiation command occurs in this bounded route; the armed confrontation
is scripted animation rather than an inferred combat encounter.

## Validation

Four focused tests in `tests/test_alshark_r04_flow.py` pass against original
images. They exercise the three-flag summons, conservative route closure and
later-state exclusions, changed progression/missing-target rejection, original
map trigger/object decoding and altered-image rejection. These checks do not
establish natural English, fit, final image preservation or playable traversal;
those are integration and independent QA responsibilities.


## Opted-in narration continuation pages

The source dispatch table atf4ba maps ASCII `0` to selector9, `_` to15,
and `6` to19. The dispatch vector atf2fb resolves those to f35b, f2b6
and f371 respectively. Wait handlerf35b calls e6c6 and resumes the byte
reader. Clear handlerf2b6 preservesSI, invokes its clear/display helpers,
resets mode/cursor state, then falls throughf2db: `BB 0F05 B407 CD41`
sets the default display attributes through interrupt41 service7. Narration
handlerf371 is `BB 0D09 E9 67FF`: it selects BX090d and jumps back to
the same attribute service atf2de. It consumes no operand and no narrative
byte. The exact visible colour is not needed to prove restoration.

Consequently a continuation inside established control36 narration requires
bytes `30 5f 36` (wait, clear, restore original narration attributes), instead
of default continuation `30 5f`. `r04_pages.py` supplies this fixed separator,
source colour tracking and matched layout-token validation. It rejects speaker
headers, other nondefault attributes and mismatched restore markers. The
manager wires this only to explicitly opted-in R04 records; older pages keep
their existing rejection behavior. Original token metadata, allocation and
opaque-tail preservation remain mandatory. Two helper tests cover valid
restoration and all rejection cases; combined rebuild/layout tests are still
required in shared integration. These pages restore the original attribute
state, not an invented replacement style.


Shared header calls need attribute-state handling as well. Exact calls
`2350020b1a`, `2350020b24`, `2350020b25`, `2350020c01` resolve to
05c000:026/036/037 and05d000:001. Each target consists solely of optional
clear5f, header34, one text span, body35 and terminator00. Thus all finish in
default body mode, even when called from narration. `validate_header_calls`
guards those complete shapes and control bytes before using their side effects.
All other #P calls make the local pagination attribute state unknown until an
explicit reset; this prevents assuming that a callee preserves colour. The
added test proves reset36→default, changed-header rejection and unknown-call
page rejection. Seven focused flow/page tests pass after this addition.
