# R08 independent source inventory

QA inspected the original System/Data images and R07 catalog. This is static
source evidence; route traversal remains unverified.

## Entry and capital dependencies

Roy's root05c009 selects027 after Byuto victory2c. That control-only entry calls
05d002, the debrief and leave scene. It sets2d, changes station visibility42/0f
and calls Roy's leave reminder05c028. The station's secretary030, operator031
with yes032/no033, and blocked ship access034 are required changed responses.
The travel command in032 is `#Q 07 28 28`: world7,40 on map40, Mars Spaceport.
As independently established in R07, #Q's third byte is a direct map ID.

Port40 metadata System8e400 selects bank05f000. Its initial objects are029–040;
three later soldier objects088 require visibility5d. Tile trigger028 selects
059 after leave flag2d, offering return to CS Station. The port border returns
to Mars surface8. Ordinary border/exit map bytes encode destination plus one.

Mars surface8 metadata is System86400. Its four exits lead to port40,
capital Teswil73, Daina71 and Begi61. The capital metadata System96800 selects
bank057000. Its objects cover000–012 and014–032, plus numerous in-map door
transitions, two shared-bar partitions, and four entrances to shared building3.

## Shared interior partition proof

QA independently flooded original shared-map grids, conservatively treating
all nonzero tiles as traversable, and followed their in-map stair/door edges.
Both shared maps use tile set10hex; its zero tile retains blocking class10hex
under the collision mapper and movement tests established in R02.

| Map / entry world coordinate | Initial component | Required roots |
| --- | --- | --- |
| Bar2 /42,66 |158 tiles, x18–29/y21–35 |053046–051, calling078000–005 |
| Bar2 /20,60 |152 tiles, x0–14/y21–32 |053044–045, including the letter branches |
| Building3 /51,88 |181 tiles, x15–27/y30–46 |061009, stairs to010–012 |
| Building3 /9,126 |184 tiles, x0–9/y45–63 |061000, stairs to001–004 |
| Building3 /70,126 and34,126 |152 tiles each initially |061005–008 through internal doors |

Thus all thirteen initial building NPCs belong to the promised capital visit.
Bar2's other city partitions remain disconnected. The optional larger bar adds
an imperial-generals conversation and a runtime name17 reference; the smaller
bar includes the complete video-letter grant, full-inventory refusal and retry.

## Optional Begi is on the same mainland

The original Mars grid descriptor at System4799 is015a0509, loading96×96 tiles
from Systemb5000. Its attribute descriptor at3f59 is02060601, loading Datad400.
QA disassembled collision mappere4ca–e4e8: high-bit tile indices resolve through
the same attribute table before the high nibble becomes the collision property.
Movement checkb941–b95f accepts zero or70hex. A four-neighbor flood from the
port return tile23,20 reaches960 permitted tiles, including the capital entrance
49,48 and Begi entrance40,142. Daina165,66 is outside that component across
water. A non-wrapping flood already proves the two mainland town connections;
it is not necessary to assume an edge route.

Begi61 metadata System93800 selects bank063000. Its fourteen objects are
000–013 (007 has no text). Four triggers select014/015 bookshelf inspections,
016 Stea-ticket pickup, and017330-credit pickup. The inventory-full failure018
and established shared hotel/services remain dependencies. There are no ordinary
map exits beyond its surface border.

Historian004 has a later itemA6 branch to025. The history-book acquisition022
requires36, which is enabled by019 after later story34. These cannot be assumed
reachable merely because a generic item-test traversal includes both outcomes.
The final plan must either inventory the later sequence or explicitly guard
its source-proven unavailable item/state edge. Initial historian greeting and
speaker020 remain required.

Reproducible ignored evidence: `work/r08-qa-map-audit.py` and its JSON report.
The manager owns the final boundary and scope plan; no inventory gate approval
is implied by this discovery report.

## Video-letter activation

QA verified the original command chain: successful053055 handover grants itemA5
and sets30; party roots082000/002/003 each test30 and select082055, which calls
081025. The letter scene sets32, enabling081026–028 follow-up conversations.
The player should use party TALK after receiving the letter. No inventory-use
activation is implied. RE separately traces the resident TALK dispatcher.

The optional bar's names have additional table evidence: slot22 points to
System11282, a source name with a separator between Nobel and Sullivan;
slot21 at11288 contains Sullivan alone. Thus the divided working name has
source support, while the Latin spelling remains provisional. This does not
establish any other character relationship.

QA's independently written command traversal reproduced all506 entries and424
text-bearing dependencies of the production R08 closure. It decoded calls,
counted choices, random repeats, current flags, shop/item failure branches and
the source-proven unavailable encyclopedia edge directly from original tokens.

QA independently inspected all sixteen encounter-directory entries (nine unique
groups) on Mars8. Their sprites are1e/1f/20/21hex, resolving through the original
profile directory to12b8c/12ba3/12bba/12bd1 with types2/2/5/3. None can satisfy
the special Karma defeat-message predicate8/10. The established binary-action
lookup applies; these values do not introduce new visible ability-name strings.
