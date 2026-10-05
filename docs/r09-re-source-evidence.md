# R09 Daina reunion and the Begi historian

Original-image static inspection, October 5, 2026. The decoded source packet stays
in ignored `work/r09-re-route-packet.json`. The cumulative closure contains 546
entries, including 40 additional entries and 29 new text-bearing script records.
This evidence establishes source coverage; runtime traversal remains pending.

## Boundary and source inventory

Begin after Lucia's video letter in R08. Cross the sea in the purchased Jet
Hovercraft, visit Daina, inspect the memorial, complete the reunion and escape,
then follow the party's lead to the historian in Begi. Include the encyclopedia
search, inventory-full retries, history lesson, emblem and Stea lead, and all
immediate party responses. Stop before taking transportation to Stea. The existing
Mars mainland interiors remain included cumulatively. Other-planet exploration
remains outside the boundary.

Daina map 71 selects System metadata 0x96000 and bank 062000. Its twelve objects
use script IDs 000–008; duplicate IDs include scene figures whose visibility is
controlled by flags 46/47. The map has no trigger or exit-list records. Its border
is raw `(9,165,67)`, returning to surface map 8 because map-border destinations
are one-based. Surface 8 has only the four previously inventoried destination
exits: Mars Port, Teswil, Begi and Daina. Crossing water does not add an unknown
fifth town exit.

Memorial dispatcher 062001 checks flag 34 for repeat inscription 010, then flag
32 for reunion 009, and otherwise also shows 010. Therefore both the inscription
and the full event are required. Scene 009 includes narration, conversations,
scripted movements and an ambush/flashbang escape; it does not invoke a new combat
encounter command. Its final commands hide scene figures 46/47, set flag 34, execute the
recruitment selector `#W 0a`, and teleport the party through `#Q 94 60 08` to Mars map 8
at (148,96). Those commands remain immutable.

Daina hotel 002 calls the existing shared hotel entries through 011/012. Item
shop 003 selects labels 013 and branches 014/015; its insufficient-money branch
016 remains included. The five residents 004–008 explain the memorial and village.
The complete new script inventory is:

- 062002–010 and 062013–016: Daina services, residents, memorial and reunion.
- 063019, 063021–026: Begi historian and encyclopedia follow-through.
- 081029–031 and 082005: post-reunion party dialogue, including Lucia's new TALK root.
- 080000–003: post-historian party dialogue.
- 05f085: changed Mars Port response when requesting return to CS Station.

The resulting 29 records vary greatly in size: 062009 is one long, multi-speaker
story scene, while 062013 is only two menu labels. Counts are not word-based
translation progress.

## Hovercraft crossing

Purchase 057035 preserves `?I 0e 29 2b 08 00`. Resident dispatch at 0xdd39
indexes table 0xdd4d; subtype 0e selects 0xe016, which writes the sixth vehicle
record at 0x1a76. The following bytes place it at tile (41,43) on map 8. This is
the Jet Hovercraft slot, not a newly allocated vehicle or invented sailing mode.
Collision mapping at 0xd142–0xd19b resolves high-bit tile aliases and extracts
the high attribute nibble. Class 40 is permitted for vehicle 3 or 5 and above;
class 50 is permitted only for vehicles 2–5. The hovercraft's state 6 therefore
passes class 40 water and still blocks class 50.

An independent RE grid flood using the original Mars grid and attribute table,
starting at the purchase tile, reaches Daina's entrance tile (82,33) through
classes 00 and 40. The accepted 00/40/70 component has 7,245 tiles. The explicit
path and reproducible script remain in ignored `work/r09-re-crossing.json` and
`work/r09-re-crossing.py`. This tile connectivity check is not a runtime movement
replay: sprite footprint and the precise boarding/disembark controls still need
playtesting. It establishes a source-grounded sea route and, together with the
complete four-exit surface inventory, prevents inventing additional sea towns.

## Historian and party state

After flag 34, Begi historian 063004 selects 019, which sets 36 and goes to 021.
The bookshelf trigger 014 tests 36 and selects 022, granting encyclopedia item A6
with inventory-full branch 024 and clearing 36. Historian 004's A6 item test now
selects 025. This is why R08's source-backed unavailable-item exclusion must be
removed in R09 rather than carried forward. Entry 025 consumes A6, explains the
historical deception, calls Stea lead 026, grants emblem A7 with full-inventory
branch 024, and sets 37. Repeat historian dialogue is 026. The existing speaker
header 020 and title fragment 023 are composed dependencies, not independent
conversations.

Flag 34 selects party 082059–061, calling 081029–031. Lucia has a separate base
TALK entry 082005 after joining. Flag 37 selects 082062–065, calling 080000–003.
No flag 38-or-later branches are included. Port return dispatcher 05f061 tests
34 and selects 085: Welda refuses to bring a civilian to the military station.
The earlier return path remains included for before-reunion access.

Recruitment has resident-code evidence: command table 0x33eb maps W to 0xd873.
That handler consumes the selector and calls 0x0b37 (the disassembler reports
0x10b37 before 16-bit wrapping). At 0x0b71–0x0b78, selector 0a selects party
actor 7; 0x0bd7 stores it in the party slots beginning at 0x19db. TALK reads
that actor and indexes table 0xb43d, whose actor-7 entry is 5. Thus Lucia
selects 082005; the recruitment selector is not itself the actor ID.

The existing Mars surface encounter groups, resident travel/combat/UI menus,
and equipment/service labels remain applicable. QA independently verified Lucia's
resident profile at 0x18b8: existing Freeze (ability-name:16) and Locate
(ability-name:57) slots, and zero additional IQ-learning entries at 0x7945. Thus
her addition requires no new ability-name allocation.

## Technical integration and preservation

`r09_flow.py` retains all R08 roots and calls, adds flags 34/36/37 and Daina/Lucia
roots, and guards the critical source commands above. It fails on missing branch
targets. The one new menu uses its original 6-column, 2-row geometry:
062003 command `3f4e0506020d0e0f`, labels 062013. The adapter checks source/output
command identity and English dimensions without widening or patching the command.

`r09_names.py` adds only `r09-location:71`, displayed as DAINA. Its original span
is System 0x115ab, 11 bytes, with pointer at 0x104ce and the original ` >` prefix.
The guarded ASCII adaptation fits within that span. The adapter checks the full
original image hash, all prior allocation pools, pointer aliases and the approved
spelling. Historian speaker call 2350021214 is added to the existing guarded
continuation header table: original 063020 has exactly controls 5f/34, speaker
text, control35 and end. This establishes default-colour continuation state.
The title call 2350021217 leaves colour33 and is not treated as a header;
original31/36 controls restore the caller state before body pagination.
No new shared-character names are needed; names referenced by the
reunion already have reviewed allocations. Encyclopedia A6 and emblem A7
already have the complete R03 item-name coverage.

Eight focused source/preservation tests pass with
`python3 -m unittest discover -s tests -p 'test_alshark_r09*.py'`. They exercise the
cumulative closure and new item branch, root/map inventory, missing-command and
missing-target failures, menu bounds, name aliases and changed-byte containment.
Original disks are required for these checks; public tests skip them if absent.

Actual hovercraft boarding, sea traversal, event animations, party recruitment,
combat display and inventory-full retries still require runtime verification.
The section gate must not claim those observations were performed.
