# R01 map entrypoint evidence

Read-only inspection of the hash-guarded original System image, 2026-09-23.
This closes discovery of the static talk/examine/event entrypoints on the three
maps in the Cosma–meteor–Cosma route. It does not assert that the translated
candidate has passed an emulator traversal or that all reachable Hom towns are
part of R01. The ignored `work/r01-route-inventory.json` records source hashes,
metadata offsets, individual object offsets and exit/trigger bytes.

## Loader and dispatch evidence

System `0xfc72` indexes the four-byte map descriptor table at `0x4575` by
current map ID `[0x1775]`, loading metadata into `2000:3483`. A descriptor is
(disk, logical track, sector, sector count); the disk offset is
`track*0x2000 + (sector-1)*0x400`. The metadata header's byte 8 chooses the
script bank through `0xf6fc→0xfc4e`; the bank descriptor table is `0x40fd`.
Bank 0 is System `0x51000`, bank `0x31` is System `0x82000`.

`0xf71c` establishes three metadata pointers: word at header+13 selects exits,
+15 selects the counted object list, and +19 selects tile script triggers.
Objects occupy 18 bytes each. Interaction dispatch `0xd316..0xd365` tests
visibility byte +13 against bitmap `0x1998` (zero means unconditional), then
`0xd4a3` reads entry byte +12. `0xd4d7` resolves that entry in the current
script bank and `0xd50a` displays it. Drawing at `0x088e` uses the same visibility
condition. Inventory both enabled and conditionally enabled objects.

Tile-property `0x30` dispatches to `0x0d4f`: five-byte trigger records hold
(x, y, event flag, script entry, display mode), terminated by x=0. Flags are
checked/set in bitmap `0x19b8`; the script entry reaches `0xd4b5`. These trigger
coordinates are metadata coordinates, not screenshot pixels.

Tile-property `0x20` dispatches to `0x0d09`: five-byte exit records hold
(x, y, target map plus one, destination x, destination y), terminated by x=0.
`0x1253` subtracts one from the target. Border exits instead use header+10
(target map plus one) and +11/+12 coordinates, initialized by `0xf6ca` and
used by `0x1237`. Collision accessibility still needs runtime checking.

## Complete static route-map inventory

| Map | Metadata | Script bank | Objects and tile events |
| --- | --- | --- | --- |
| Cosma, ID 49 | System `0x90800`, 1024 bytes | `051000` | Twelve objects: entries 000–010 and 028. Five tile triggers: 000, 034, 035, 036, 037. |
| Planet Hom, ID 11 | System `0x87000`, 1024 bytes | `082000` | Zero objects and zero tile script triggers. Global party TALK remains available. |
| Saxen Canyon / meteor site, ID 100 | System `0x9d400`, 1024 bytes | `051000` | Five objects: 032, 032, 030, 031, 033. Two tiles both trigger 029. |

Cosma object entries 000/001/002 have visibility flags 1/2/3, respectively;
003–009 are unconditional; 010 has flag 4; 028 has flag 7. Thus 028 (the dead
Gigi interaction) is a source-proven Cosma entrypoint, not merely nearby text.
Cosma tile triggers are: (20,16)→000, (49,27)→034, (51,7)→035,
(13,11)→036, (25,5)→037. These cover breakfast and four pickups.

Canyon objects use flags 0/2/6/6/6 in the order listed above. Trigger coordinates
(47,23) and (48,23) both select 029 with event flag 2. Entry 029 starts the
meteor event and sets story flag `0x10`. Entry 031 includes the initial/repeat
soldier dispatch; 032 includes the crater dispatch. Include their cross-bank
callees, documented in `r01-coverage-audit.md`, rather than only the dispatchers.
Both Cosma and canyon have no explicit exit records; their border target is Hom.

Location-name identity is independently backed by the map title pointer table
at System `0x10440 + 2*mapID`: map 49→`0x114bf` (Cosma), 11→`0x11329`
(Planet Hom), 100→`0x11722` (Saxen Canyon). Header byte 7 is not the title ID.

## Route boundary and Hom exits

Hom's border target is map 100 (Saxen Canyon), destination (51,126). Its five
explicit exits are (27,7)→96, (101,50)→49, (17,98)→48, (39,98)→42,
and (13,116)→98. The corresponding locations are abandoned mine, Cosma,
Hamack, Hom spaceport and Dust. Map 96 is the abandoned mine, not the meteor
site; no hypothetical map-96-to-100 redirect is needed to explain this route.

R01 is the named Cosma–meteor route, not every destination accessible from Hom.
The metadata contains no exit-level story flag. Do not describe Hamack/Dust/
spaceport/mine as proven inaccessible before the release endpoint. Bank 051000
job entries 022–027 are not route entrypoints merely because of their bank;
Hamack source calls establish their separate context. Conversely, later return
visits to route maps may enable additional story branches and are outside the
bounded initial story state.

## Global party TALK is a separate required entrypoint family

System `0xb3f1` runs the party selection path. At `0xb3fd..0xb3ff` it loads
bank `0x31` regardless of the current route map. The selected party slot indexes
`0x19db`, and the resulting actor index selects from table `0xb43d`, whose
nine bytes are `07 07 00 01 02 03 04 05 06`. The selected script entry is
passed to `0xd4d7`; the original map bank is restored at `0xb434..0xb437`.
Do not infer completeness from the current map's object bank alone.

Independent QA traced actor lookup `0x0ad2` through profile table `0x1b5d`: actor
IDs 1/2/3 are Sion/Shoko/Karu. Their party TALK entries are therefore
082000 entries 007/000/001. The `#W` payload uses a separate selector and
must not be substituted for these actor IDs. The R01-relevant paths discovered by the localizer
include Sion 007→008/014 and Shoko 000→009, with shared 07f000 entries
038/039. The manager/localizer must inventory and adapt those linked records
and classify later-story branches against their flag setters. The static map
inventory does not itself prove every branch's story-state feasibility.

## Completion classification

Static route object and tile-trigger discovery is source-backed and complete
for maps 49, 11 and 100. Script call/choice/condition closure and party TALK
closure are separate gates; newly discovered party records must be translated
before claiming route text completion. Cinematic stream coverage, resident UI,
item/ability names and combat messages have their own adapter/audit evidence.
Runtime route traversal, trigger activation, composed dialogue rendering,
save/load transitions and selection behavior still require player/emulator
validation of the candidate. Original bitmap staff-credit artwork during boot
is an incidental untranslated limitation and must not be represented as a
fully translated boot sequence.

## Bounded story-state and party branch closure

A fresh original game initializes all 32 story-flag bytes at System
`0x1978..0x1997` to zero. The script set/reset handlers at `0xd750`/`0xd764`
operate on this bitmap through `0xf281`/`0xf289`; conditional `#B` at `0xd777`
tests it through `0xf294`. NPC visibility (`0x1998`) and tile event flags
(`0x19b8`) are separate bitmaps and cannot activate party story branches.

Starting with the route-map entries above, expansion of `#B`, `#Y`, `#G`,
`#P`, `#C` outcomes and `#I` failure continuations discovers 45 records:
051000:000–021 and 028–042; 052000:083; 053000:000/013;
054000:000; and 061000:019–022. This includes both successful and unsuccessful
choices rather than assuming the happy path. The ignored
`work/r01-party-closure.json` records the seeds, closure, all setters and every
condition in each of the three party dispatch records.

The entire closure has only these story-flag setters (hexadecimal flag IDs):

| Flag | Source record(s) |
| --- | --- |
| `00` | 051000:011, 014 |
| `01` | 051000:002 |
| `02` | 051000:011 — invitation accepted |
| `04` | 051000:030 |
| `06` | 051000:031 |
| `0e` | 051000:019 — Karu joins at the release endpoint |
| `10` | 051000:029 — meteor event |
| `35` | 051000:039 — Protector pickup |

Intersecting those setters with **every** condition in the complete 082000
000/001/007 dispatch chains leaves only the following relevant party branches.
Their order is important: endpoint flag `0e` takes priority over meteor flag
`10`, and meteor flag `10` takes priority over invitation flag `02`.

| Phase | Sion TALK | Shoko TALK | Karu TALK |
| --- | --- | --- | --- |
| Before invitation | 007 default | Not yet joined | Not yet joined |
| Invitation accepted, before meteor | 007→008→07f000:038 | 000 default | Not yet joined |
| Meteor complete, before Karu joins | 007→014 | 000→009→07f000:039 | Not yet joined |
| Karu joined (endpoint) | 007→015→07f000:041 | 000→016→07f000:042 | 001 default |

The endpoint branches are required even though the release stops at Karu
joining: the player can select party TALK immediately afterward. Dispatchers
008/009/015/016 contain only their preserved cross-bank call and terminator;
the translated content lives in the indicated 07f000 records. These party
records/callees introduce no additional story-flag setters or nested branches.

All other tests in the three dispatch chains are false in the fresh-game,
named-route closure. In particular, full-catalog `#S` inspection finds flag
`0b` only in 051000:027 (Hamack work acceptance), `0f` only in 05a000:039
(the subsequent Joe meeting), and `11` only in 053000:024 (a later informant
report about Lucia going to the spaceport). None belongs to the 45-record
route closure. Higher story flags likewise have no setter in this closure.
This is a boundary classification, not a claim that optional Hom destinations
are physically inaccessible. An imported save with later flags set is outside
the initial R01 verification state.

With 082000:000/007/014 and 07f000:038/039/041/042 added to the already translated
Karu conversation, and the four control-only party dispatchers inventoried,
the source-backed route/choice/party branch closure is complete. Runtime
activation, story-state persistence and visual QA retain the separate pending
status described above.
