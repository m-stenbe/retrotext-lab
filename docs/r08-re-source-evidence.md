# R08 Leave on Mars and the capital investigation

Original-image static source inspection, October 2, 2026. Decoded source remains
ignored in `work/r08-re-route-packet.json`. The bounded inventory contains506
entries and149 newly text-bearing script records over R07. This is not an
emulator traversal claim.

## Entry, boundary and reachable alternatives

Roy009's flag2c branch selects027, which calls05d002. The debrief sets2d,
grants leave and explicitly forbids using Atraia. Roy028, secretary030,
operator031 with depart032/defer033, and guard034 cover all immediate station
alternatives. Departure032's `#Q 07 28 28` enters Mars Spaceport map40 at7,40.
Port roots028–040 include ticket counters, travelers and return-to-CS choice059;
its return061 branches to086 in this bounded state, entering station30.
Other-planet bus departure/refusal notices and ticket menus remain translated,
while exploration after taking those optional buses is outside this section.

The intended section includes Mars Spaceport, Teswil and all its shops,
interiors and bars, optional Begi on the same mainland, the jet hovercraft
purchase, Lucia's video letter and the resulting party responses. Its endpoint
is **before following the letter across the sea to Daina**. This is a geographic
and story boundary, not an assertion that the purchased vehicle cannot cross.

Mars surface8 at86400 has four exits to port40, Teswil73, Daina71 and Begi61.
As in R05, tile-exit destinations store map ID plus one. Independent QA's
source collision/grid flood reaches port, Teswil and Begi from the arrival coast,
but not Daina across the sea. See `r08-qa-source-inventory.md` for exact map
component evidence. Including Begi avoids an untranslated mainland detour.

Teswil73 at96800 uses bank057000, with unconditional roots000–012/014–032.
Its in-map doors connect the shop interiors, while two exits enter shared bar2
at42,66 and20,60, and four enter shared building3. QA establishes bar roots
053044–051 and building roots061000–012. The bar's054–057 branches cover letter
handover, inventory full/retry and repeat. Six shared calls select078000–005,
including the optional imperial-generals conversation. Building cleaner repeat
uses random061014–016; Shaina's first visit/repeat/tea alternatives are included.

Begi61 at93800 uses bank063000: roots000–013 and triggers014–017 (books,
Stea ticket,330-credit pickup). Its historian's itemA6 branch004→025 is
explicitly excluded by item state: A6 can first be granted by022, selected after
flag36; flag36 is set by019 after flag34, which belongs to the excluded Daina
story. The source command is guarded and remains unchanged. The normal greeting,
header020, pickup-full018 and all current shops are included. This exclusion
does not remove a reachable current-state alternative merely to fit text.

## Video letter and party trigger

Entry053055 grants itemA5 and sets30. Party dispatch roots082000/002/003 have
`#B 30 37`, selecting082055, whose `#P 30 19` calls081025. The latter presents
the complete letter and sets32; subsequent party lines026–028 discuss Daina.
Thus the proven viewing action is **Talk to a party member after receiving the
letter**; inventory Use is not asserted. Earlier leave party lines022–024 remain
included. Resident Talk dispatchb3d7 opens the action menu, and its first option
loads bank31 atb3fd, maps the selected actor via tableb43d, and calls the normal
script routinesd4d7/d4c1. All participant speaker headers remain source-owned.

## Names and technical surfaces

Five new map-title allocations are guarded: map8 at11306/11 bytes/pointer10450;
map40 at11451/13/10490; map61 at11531/12/104ba; map73 at115c0/11/104d2;
map3 at112d3/12/10446. Their display spellings are MARS, MARS PORT, BEGI,
TESWIL and TESWIL BLDG. The first three use original ` >` prefixes, the last
two a single space. All use established marker-aware centering and twelve-cell
limits. There are no additional pointer aliases into those spans.

The optional bar references shared name17, with original short/full slots17/18
at1125a/7 and11261/14 bytes and pointers10422/10424. Working canonical spellings
are Jaguma and Jaguma Dorian, based on those source labels, not an official
romanization. As with R04's Welda, both displayed forms use JAGUMA in one shared
full-width allocation within their21-byte combined original pool. No unrelated
name or font storage is repurposed. Runtime layout includes both name IDs.
Video LetterA5 and every current shop/ticket item already have reviewed R03
names, so no overlapping replacement item allocation is added.

Seven source-guarded menu rectangles are validated without changing command
bytes: Teswil tool6×2, weapon5×2, frame/engine6×3, turret/missile4×3; port bus6×4;
Begi tool6×2 and weapon/armor5×3. The adapter rejects labels with excessive
rows or columns and checks the immutable menu commands in source and output.
Shared headers/calls and new narration entries use the existing composed-layout
and continuation-page adapters. No progression or map metadata changes are needed.

## Ground vehicle and encounters

The hovercraft purchase057035 sets22 and uses existing `?I09` subtype0e to place
the vehicle on Mars. Boarding/disembarking use residentb98f–ba1f; vehicle state
19d8 selects its stats throughc765, while foot state is zero. These paths reuse
already translated R06 vehicle selection and battle menus (Opening404b/4021,
Systemc697/827a) and R03 equipment/services. The inspected boarding state-change
routine introduces no literal text. Ground travel after purchase remains within
the mainland boundary until the explicit Daina crossing.

All sixteen Mars surface encounter groups have sprites1e/1f/20/21 (hex). Their
profiles at12b8c/12ba3/12bba/12bd1 have types2/2/5/3; none meets the type8/type10
Karma-message predicate. Their action bytes are binary combat descriptors,
following the already documented R07 action-table20c8 dispatch. No new enemy
name or ability-label table is selected. Runtime targeting, vehicle boarding,
combat frames and the exact walking route still require playtest verification.
