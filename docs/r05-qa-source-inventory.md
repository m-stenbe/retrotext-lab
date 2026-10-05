# R05 independent source inventory

QA inspected the immutable original System disk, verified its known SHA-256,
and independently decoded the station departure surface and its town exits.
Full source titles and metadata are retained only in ignored
`work/r05-qa-map-inventory.json`; the read-only reproduction script is
`work/r05-qa-map-inventory.py`. This is static source evidence, not a route
traversal or a release approval.

## Station departure and correct exit numbering

Station30's border enters map9 at (35,99). Map9's descriptor `01430301`
selects **System** `0x86800`; its title pointer `0x10452` selects `0x11311`,
Planet Zajil. Its script bank is082000; metadata contains no objects or tile
script triggers. Global party TALK still applies.

Five-byte exits store (x,y,**target map plus one**,destination x,destination y).
Original handler `0x0d38` reads the third byte, stores it in `0x1cfa`, and
reads the final coordinates; `0x1253..0x125c` subtracts one before assigning
the actual map ID. Reading the raw target as a map ID incorrectly identifies
unrelated towns. The three original map9 exits are:

| World coordinate | Raw target | Actual destination | Bank |
| --- | --- | --- | --- |
| (50,28) | 42 | map41, Zajil Spaceport; (17,62) | 05f000 |
| (55,34) | 54 | map53, Saibal; (31,126) | 05b000 |
| (111,118) | 51 | map50, Porkin; (31,62) | 05a000 |

The exit records have no story-flag field. The handler has a global suppression
check at `0x0d31`, but the table supplies no evidence that the optional port or
Porkin town is locked by story progression. Both need a pre-endpoint interaction
inventory for a section promising optional Zajil surface exploration.

## The apparent Hyuris border is not a departure route

Map9's nominal border tuple is `(16,8,60)`, which would target map15 in a
bounded map. However, map9's header begins `40 40 00`: width64, height64,
**bounded mode zero**. Original loader `0xf6de..0xf6ea` reads these three bytes
sequentially into `0x1d0b`, `0x1d0d`, and `0x1a15`; its exact bytes are guarded
by the QA script. Map30's mode is one.

The movement handlers test `0x1a15` in all four directions. With zero mode,
up (`0x0fbf→0x0fde`), down (`0x108a→0x10b2`), left
(`0x110a→0x1129`) and right (`0x11d5→0x11fd`) select coordinate wrapping.
The respective wrap operations add/subtract four times the map dimension at
`0x0fee`, `0x10c9`, `0x1139`, and `0x1214`. Their branches bypass the
bounded-map calls to border loader `0x1237`. Thus ordinary map9 walking does
not follow its nominal Hyuris border. No translation of Hyuris is required
merely because that unused tuple is present.

## Saibal bar partition

Saibal's two bar doors at (51,87)/(52,87) both enter map2 at (67,2).
An independent flood fill from source tile (33,1), conservatively treating
all nonzero map tiles as traversable, finds236 tiles bounded by
x21–37,y0–13. Exactly object entries053000:029–034 fall inside.
The established original bar-grid/attribute evidence proves tile zero is a
blocking gap (Data `0x4c400`, attribute14, collision10), so unrelated town
bar partitions remain outside this entry's component. This does not prove
runtime doorway movement.

## Remaining review

The proposed boundary follows Saibal's investigation through the hotel
kidnapping, before pursuit into the next hostile area. The manager must bind
that boundary to source flags and complete optional port/Porkin interactions,
bar branches, jobs/services, names, party changes and combat/UI dependencies.
Any exceptional renderer or unsupported allocation remains an engineering
blocker. Frozen source-to-English review, full closure comparison and candidate
binary QA are pending.

## Welda combat coverage defect

Independent QA found three missing ability-name records in the cumulative
baseline. Actor5's pointer at System `0x1b65` selects profile `0x1877` with
shared name ID08 (Welda). Its item/equipment bytes at +15..18 are
`19 00 44 63` (hexadecimal), all covered by earlier equipment/name packs.
Its fourteen combat slots at +19..26 begin with IDs19/1a (decimal25/26),
then zeros. Its six field slots at +27..2c begin with ID3d (decimal61),
then zeros. The source name pointers select `0x11100`, `0x11109` and
`0x111ae`, respectively. None has an adapted record in the baseline.

The first and third source terms denote mental/spirit recovery; the second
mental/spirit attack. Effect names require source-context review before
claiming HP/MP behavior. Class09 at profile+2 selects learning-table pointer
`0x793f→0x7945`, whose count is zero. Therefore the original profile supplies
no additional learned abilities for this class. The established learning writer
separates the fourteen combat and six field slots; profile+2d is not another
field ability. Manager/RE are resolving the three missing names before release.

QA also enumerated every merchandise ID from the seven bounded `#H` calls
in05a000:030/031/034/036 and05b000:024/027/031, excluding the shop selector
and insufficient-funds target bytes. All merchandise names have cumulative
reviewed adaptations. Item81 uses the older fixed UI record at `0x10b74`
(MEDS); the remaining required item pointers appear in the prior name packs.
This closes new shop-name discovery, separately from ticket and Welda ability
names and from runtime transactions.

## Final closure review

All previously identified static inventory issues are resolved in the frozen
R05 candidate. The105 new records include the three Welda ability groups and
all their aliases, four map labels, optional Porkin guard battle, port ticket
and boarding text, shared scrap exchange and the complete Saibal scene set.
The final bounded closure has168 entries,139 text-bearing records; all139 are
required by the701-record/72-scene plan. No new text cinematic stream is
present. The original standard on-foot battle/UI path remains cumulative.
The reviewed exchange controls are8 to sell scrap for credits and2 to buy
scrap, at five credits per scrap, with held Space acceleration. The endpoint
is after kidnapping and immediate responses, before pursuing Tomyu in Porkin;
other-planet exploration and ship flight remain explicit route boundaries.
See [frozen candidate QA](r05-qa-final.md) for exact binary evidence. These
findings do not establish emulator traversal.
