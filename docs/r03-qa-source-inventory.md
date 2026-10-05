# R03 independent source and surface inventory

QA inspected the original System image and R02 catalog, then compared the proposed spaceport/mine boundary with RE's map evidence. This is static source evidence, not emulator traversal.

## Names and inventory

The map-title table is System `0x10440 + 2*mapID`. Three new titles are required through the first controllable ship bridge:

| Map | Original storage, including NUL | Pointer aliases | Canonical / proposed display |
| --- | --- | --- | --- |
| 42 | `0x1146c`, 11 bytes | `0x10494` | Hom Spaceport / HOM PORT |
| 96 | `0x116fe`, 8 bytes | `0x10500` | Abandoned Mine / MINE |
| 1 | `0x112bf`, 9 bytes | `0x10442` | Cockpit / BRIDGE |

The two-byte title marker is preserved. An initial overbroad scan incorrectly classified numeric bytes at `0x10594` as a markerless mine alias. Independent disassembly at System `0x79b2..0x79cb` proves that `0x1055c` begins a 24-bit progression table: the reader uses `3*index + 0xdd54` in segment5000, relative to the name load at `0xd7f8`. The corrected adapter scans pointers only before `0x1055c` and leaves this progression table intact. No candidate was built with the erroneous alias metadata. The source spans are disjoint from R01/R02 reviewed allocations. SPACEPORT requires twelve bytes including marker and NUL and cannot fit the original eleven-byte spaceport slot; total free bytes in nonadjacent spans do not permit overflowing a slot. HOM PORT preserves the planet qualifier while shortening the facility term. MINE omits “abandoned,” retained in canonical text and directions. BRIDGE is a contextual room label for Cockpit.

`profiles/alshark/r03_names.py` was authored by QA and therefore requires manager review rather than QA self-approval. Its five focused tests include original-based compilation, exact pointer targets, unexpected alias rejection, incomplete-group rejection, runtime width/allocation refusal, source hashes, and patch confinement. The stable three-name group emits six patch ranges. No new item gain or shop command appears in the reviewed `054000` port/mine text. RE reports map96 has only the lever trigger and two conditional ship objects, with no pickups; the final closure comparison passed.

## Party and endpoint surfaces

Independent party dispatch inspection identifies flag12 branches `082000:023→024` and `082000:002→025→07d000:034`. These add the Mars promise and Joe/Shoko's ship-safety argument, including the explicit direction north of Hamack. Flag13 changes party TALK to `082000:026→07d000:033` and `082000:027→07d000:032`; source context discusses the parents aboard the enemy ship, so their availability at the immediate bridge endpoint needs RE's state/dispatch interpretation, not chronology inferred from text.

Entry `054000:031` sets flag13 and executes `?I03`; RE proves this loads map1, so ending the inventory at the naming dialogue alone would miss the ship's title and immediate bridge interactions. Early bridge texts are `083000:001` (Shoko navigation/co-pilot), `004` (Joe's easy-controls boast), and `005` (Karu helping the new pilot). The cockpit trigger `083000:000` calls `054000:032` before flag14, starting the next rescue sequence. The frozen release must state its boundary relative to stepping onto that trigger and establish whether it stops at a player-controlled position.

RE proved the bottom bridge edge immediately reaches the ship service menu. QA independently decoded its six options and submenu handlers; the inventory therefore includes storage, equipment changes, repair, development, disassembly and System. Absence of a menu-button branch in the bridge loop does not exclude this edge-triggered menu. Existing R02 shops, equipment, abilities and shared UI remain cumulative requirements.

## Verification status

The final RE closure comparison, bridge menu/spawn proof, canonical/adaptation reviews, strict candidate gate, complete original-based compilation, frozen binary/IPS/trainer audit and R02 preservation comparison have passed. See [frozen candidate QA](r03-qa-final.md). Runtime route verification remains pending; boot evidence must not be described as dialogue, movement, shop, bridge or route validation.


## Ship service and equipment discovery

System `0xbad4` selects menu index0x32: Opening `0x48c6`, six original rows of four cells. The first five actions dispatch through `0xba95` to `0xbb33` (hangar), `0xbd77` (equipment), `0xc1b2` (repairs), `0xc2cb` (development), and `0xc57b` (disassembly); System uses `0xb047`. Supporting menu IDs are index0x10→`0x44b1` (unload/store), index0x11→`0x44bf` (existing English categories), index0x14→`0x451a` and index0x17→`0x45d0` (three-row target selectors with dynamic fighter/tank rows). The credits/scrap header `0x48fa` is already roman-letter text with fixed dynamic fields. The mere existence of index0x12 `0x4500` does not prove a caller; it is not included on table adjacency alone.

QA traced the ship's Joe messages through `0xbb20`: BL0x0c enters the System overlay loaded at `0x14000`, relative handler `0x3442`, whose CL-indexed pointer table is file `0x1747f`. The source-backed required message set covers the default prompt, empty/full hangar and inventory, withdraw/store results, development introduction/cost/result, insufficient scrap, absent fighter/tank, repair introduction/undamaged/cost, plus Joe's heading. RE owns the final guarded field adapter. QA reviewed all 23 new UI canonical/adaptation records against these sources.

Development scans normal item IDs 0x01–0xc0 and ship equipment IDs 0x01–0x58. System `0xc4e3` calculates a low-byte availability value from `floor(max(Joe IQ−761,0)/10)`; `0xc49c` includes each entry when this value reaches stat byte8. Cost is checked after selection (`0xc4f7`), so unaffordable labels are still visible. Original Joe IQ 821 gives value 6, but no arbitrary grinding/level limit is assumed. The release conservatively prepares all 280 scanned IDs; this does not change availability or promise late-story progression.

The stat reader `0xc747` selects segment6000 pointer table offset0 for items or0x200 for ship equipment. RE proves the load at `0xfb98..0xfba7`, index0x1b descriptor `0x3f35 = 01 08 07 0a`, loads ten sectors from System `0x11800`. The ignored `work/r03-qa-equipment-source.json` records all IDs, thresholds and source names. These deduplicate to 238 source strings, of which 18 already have R01/R02 translations. The new adapter covers 220 distinct labels. Some strings share suffix storage (Night Mask/Mask, infrared sight/Sight, and others), so original readable spans overlap; writable allocation is their union **minus all prior name pools**. Exact pointer targets are packed independently, preserving prior aliases and prior compiled labels. Numeric calibers use full-width CP932 digits; uppercase ASCII and spaces follow the previously proven renderer. Names have the established nine-cell inventory limit.


The direct resident-string audit of handlers `0xbb33..0xc689` found an additional fixed script at System `0x209a`: attempting to unload ship equipment branches at `0xbb6f` and displays Joe's warning that it is too heavy to carry (`0xbb93→0xd4ea`). QA reported this gap after the initial UI packet was ready; RE added the guarded source/name-token/layout adapter and localization added the warning. The other direct resident strings in this handler range are the three already translated R02 Joe strings. This adds one record beyond the 23-record UI packet reviewed initially.

Bridge menu reachability is now independently supported by RE's collision calculation and guarded flow tests: from spawn x38,y46, three downward steps reach the bottom edge and dispatch `0x129f→0x12d2→0xbad4` without crossing the cockpit trigger. The release therefore includes these services, not merely the naming dialogue. The ordinary party menu lacks a bridge input path; conservative flag13 party text remains included as bonus closure coverage.


## Frozen static closure check

QA independently reproduced the final original-based closure: 67 entries, 56 containing text, with no missing required record in the 550-record plan. All 220 equipment IDs and 19 service-adapter IDs are present. Original map metadata matches the documented port/mine/bridge roots and visibility conditions. No `?V` external cinematic command occurs in this closure; the ship reveal uses preserved scripted animation/transition commands. The R01 meteor cinematic remains cumulative. The final bridge path check reproduced six zero-collision cells along the downward path to the service menu, separate from the cockpit trigger.
