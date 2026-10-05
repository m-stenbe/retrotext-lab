# R09 independent source inventory

QA independently decoded the original counted command edges, using the
established R08 roots plus Daina objects 000–008 and Lucia's TALK root
`082000:005`. With the additional reachable flags `34/36/37` and the formerly
unavailable encyclopedia item branch restored, traversal produces **546 entries,
453 text-bearing dependencies and 29 newly translated script records**. This
exactly matches the RE packet. The packet includes the new civilian restriction
when attempting to return to the military station.

The boundary includes Daina's reunion and escape, the return to Begi, the
historian's book request and full-inventory alternative, his historical account,
the emblem handover, and the resulting party responses. Departure to Stea and
unrelated destinations remain outside the declared section. Source-catalog and
independent traversal artifacts remain in `work/qa-pr-20261005/`.

## Vehicle crossing

Independent original-code disassembly confirms the terrain mapper at
`d142–d19b`. Collision property `40` is traversable for vehicle state 3 or at
least 5; property `50` is traversable only for states 2–5. Otherwise these
properties become blocking `10`. Directional movement checks reject `10`.
RE establishes that the purchased hovercraft is state 6, placed at tile
`41,43` on Mars.

An independent four-neighbor flood over the original 96×96 Mars tile grid and
its original attribute table connects that vehicle location to the Daina coast
at `82,33`. The shortest sampled path uses water, land and an exit tile. This
agrees with RE's more conservative land/water-only connectivity proof. There
are no newly selected literal text surfaces in the inspected boarding and
disembarking routines; existing vehicle menus remain cumulative.

This establishes static map connectivity and source inventory, not exact
sprite-body clearance or an emulator crossing. The disembark footprint test at
`b942–b95f` accepts land properties zero or `70`; the town-exit handler at
`0d31` diverts a boarded party to disembarking. Shore positioning, collisions,
vehicle persistence, encounters and the actual route remain runtime checks.

## Lucia's combat and field abilities

The original Lucia profile at `18b8` has class byte `0a`. Its combat slots
`+19..26` contain ability `10` hex (Freeze), and its field slots `+27..2c`
contain `39` hex (Location). Name pointers `10320/10372` resolve to
`110d4/1119d`; both already have reviewed cumulative adaptations
`ability-name:16` and `ability-name:57` (decimal record IDs).

The class learning pointer at `792d + 2*0a` selects `7945`, whose entry count
is zero. Thus this learning table introduces no additional Lucia ability names.
RE separately proves that recruitment selector `#W 0a` maps to party actor 7,
and actor 7 maps to TALK entry 5; selector and actor IDs must not be conflated.

No new ability-name gap was found. This is source-backed coverage, not a claim
that combat or every party interaction has been played.
