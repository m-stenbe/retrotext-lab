# R02 Dust, Joe and early Hamack source evidence

Read-only inspection of the hash-guarded original System disk, 2026-09-23.
Offsets are disk offsets. The ignored `work/r02-re-closure.txt` is a broad
control-edge trace; it is not a story-state-filtered release inventory.
The R01 catalog has 2,367 exported records and 138 R01 adaptations. R02
translations must be added cumulatively.

## Map entrypoints and route

The loader, object visibility, border, exit and trigger formats are established
in [r01-map-entrypoints.md](r01-map-entrypoints.md). Applying them gives:

| Map | Metadata | Bank | Static entrypoints |
| --- | --- | --- | --- |
| Hom 11 | System `0x87000` | `082000` | Exit `(13,116)` to Dust 98; exit `(17,98)` to Hamack 48. Party TALK uses global bank `082000`. |
| Dust 98 | System `0x9cc00` | `051000` | No objects or tile scripts. Exit `(118,9)` to Joe's room 103. |
| Joe's room 103 | System `0x9e000` | `053000` | Objects 025 (visibility 8), 027 (visibility 9); no tile scripts. Border returns to Dust. |
| Hamack 48 | System `0x90400` | `052000` | 28 objects: 000–026 in object order plus 060 (visibility 5); no tile scripts. Exits `(1,77)` and `(2,77)` to underground bar map 2. Border returns to Hom. |
| Shared underground bar 2 | System `0x84c00` | `053000` | Hamack enters `(27,2)` from the bar door at `(27,0)`. Map 2 also has doors to Saibal, Kainan, Teswil and Hogra. See partition caveat below. |

Joe's room object 027 is the six-byte, control-only `#P 09 27` call to
`05a000:039`. That 1,784-byte encounter ends with `#W 07`, `#S 0f`,
`#N 09`, `#M fd`: Joe joins, flag `0f` is set, and the room NPC visibility
changes. Object 025 checks flag `1e`, sets it on first interaction, calls
`054000:035` (the sleeping Joe interaction), and subsequently selects 026.
Both first and repeat object paths must be retained.

The shared bar map contains 38 unconditional objects, but they are not one
Hamack room. Its exits are `(27,0)` to Hamack 48, `(67,0)` to Saibal 53,
`(99,0)` to Kainan 46, `(42,67)` and `(20,61)` to Teswil 73, and `(85,42)`
to Hogra 58. The map grid is independently source-proven: loader `0xfc89`
uses descriptor table `0x4779`; map 2's descriptor `01 58 01 04` loads
4,096 tile bytes from System disk `0xb0000` into segment `5000:0000`.
A flood fill that conservatively treats **every nonzero tile as walkable**
finds Hamack's door tile `(13,1)` in a 322-tile component bounded by
x=0–17, y=0–17, containing exactly objects 053000:001–012. Saibal's
object component is x=21–37, y=0–13 (029–034); Kainan's is x=41–53,
y=0–12 (039–043); lower components contain 044–064.

Zero tiles are blocking in this map's tile set. Header byte 3 is `0x10`;
loader `0xf77a` selects its third tile-attribute descriptor `02 26 02 01`,
Data disk `0x4c400`. Tile ID 0 maps to attribute `0x14`; the collision
mapper at `0xe4ca–0xe4e8` keeps high nibble `0x10`. Movement check
`0xb941–0xb95f` permits only zero collision property or `0x70`, so a
`0x10` zero-tile gap blocks traversal. This proves that Hamack's entrance
cannot reach the other town clusters in the original bar grid. The later
video-letter 053000:054–056 is selected by flags `2d`/`30` from object
044 in a lower component, outside the Hamack bar.

## Script and story-state closure

The broad static closure from Hamack 48's 28 object entries, bar objects
053000:001–012, and Joe's room 025/027 has 96 records before party TALK,
`#U` random targets and shop menu targets. It includes control-only
dependencies and possible branch alternatives:

| Bank | Records in this broad closure |
| --- | --- |
| `051000` | 022–027 (job calls back into the Cosma bank) |
| `052000` | 000–026, 031–033, 040–045, 057–076, 081–082, 084 |
| `053000` | 001–012, 014–027, 035–037 |
| `054000` | 035 |
| `05a000` | 039 |

After adding reviewed `#H`, `#F`, `#U`, `?N` and party edges, the
transitive parser in `profiles/alshark/r02_flow.py` finds 143 script
entries, of which 124 have text. Twenty of those text entries are already
adapted in the frozen R01 catalog; 104 require new R02 adaptations. This
is the bounded static packet after the shared-bar partition proof. It
excludes resident UI and item/name tables, which have
their own source inventory.

Shops and bar add targets reached through `#H` and `?N` selectors that a
simple `#B/#G/#P/#Y` graph walk misses: Hamack shop 022→081 and
027–029; item shop 023→082 and 030/034/039; bar 025→drink menu 080 and
051–056; hotel 026→040/041/049/050. Menu text 078/079/080 belongs in the
catalog and the route inventory. The weapon and item shop menus have distinct
purchase, insufficient money, cancel and return paths; the hotel has sleep,
decline and insufficient money paths.

The three reviewed `?N` menus have explicit width, row and destination
framing: bar `052000:025` uses four columns, three rows, labels 080 and
choices 051/052/053; armor shop selector 081 uses four columns, three rows,
labels 078 and choices 027/030/028; item shop selector 082 uses six columns,
two rows, labels 079 and choices 034/050. The label entries contain the
visible menu rows; verify their rendered cells against the declared menu
geometry, including choice cursor alignment. Entry 032 uses `#U 03 2e 2f
30` to choose randomly among fortune responses 046/047/048. This adds
three visible text records omitted by the simple edge walk. The direct
town object 021 also uses `#U 03 23 24 25` to choose randomly among
035/036/037 (pond lap, streetlight count or level challenge). All six
random outcomes are available early and require English adaptations.

The optional Hamack delivery job is connected: girl 008→072 offers work,
selects 058 (accept) or 057 (decline); 058 calls `051000:027`, which sets
flag `0b` and changes Shoko's party arrangement. Counter interaction uses
063–071 plus `051000:022–026`; recipient 004 selects 074/075/076. Flags
`0a`, `0b`, `0c`, `0d` track job offer, acceptance, can delivery and payment.
The item shop 023 switches to counter clerk 067 when flag `0b` is set.
Inventory-full and failure paths are part of this optional job.

In the local bar, 004 sets `1b`; 005 then selects 014, whose choice selects
015 or 016. Entry 016 sets `1c`. Entry 011 can route to paid informant 020;
020 checks `1d` and offers payment; 022 sets `1d`, and 024 gives the lead to
the spaceport and possible Mars flight, setting story flag `11`. Entry 012
selects the Joe acquaintance response 018 after flag `0f` is set. Speaker
labels 035–037 are separate referenced records. Preserve all choice and
payment alternatives, including no money, refusal, repeat and re-query.

Immediately after flag `11` is set, party TALK changes. Shoko dispatcher
`082000:000` selects 022; Karu dispatcher `082000:001` selects 023; Joe
dispatcher `082000:002` selects 021. Sion's existing `082000:007` flag-`0f`
path remains the current branch. Thus 021–023 are required at the release
endpoint, as is Joe's earlier default TALK in 002.

After Joe joins but before the paid report, flag `0f` selects Sion
`082000:010`, which uses `#U` to choose 011/012/013; Shoko 018; and
Karu 020. In Sion and Karu's dispatchers, the `0f` test precedes the
`0b` job test, so job responses 017/019 are only reachable if the
player detours to Hamack and takes the job **before** meeting Joe.
Hom's Hamack exit has no story guard, making that detour possible in the
declared starting state. The transitive closure in
`profiles/alshark/r02_flow.py` includes these branches while filtering
later-party flags that cannot be set by this route.

## Two handler checks needed for safe adaptation

The System command table at `0x33eb` maps `#O` to `0xd7b1`. The handler
reads `count−1` story flag bytes and checks each through `0xf294` against
bitmap `0x1978`; if any is set, it branches through the shared `#B` target
path at `0xd79d` using the last payload byte. Otherwise it skips the payload
at `0xd7fe`. Joe's `082000:002` command `#O 03 83 84 e4` therefore branches
to entry 228 if flag 83 **or** 84 is set. Neither belongs to fresh early R02
setters. Its final three text spans (`t063`, `t069`, `t075`) are the early
default, and the original command must remain immutable. Flag `11` later
selects 021 before those spans.

The same table maps `#H` to `0xd8ee`. At `0xd908` the first payload byte is
stored as the menu selector; `0xd983–0xd9ce` uses `count−2` following bytes
as merchandise IDs. Menu cancel (`AL=ff`) skips the payload at `0xd93b`;
the post-selection funds check uses the final byte as its insufficient-money
branch target at `0xd93e–0xd94c`. Thus:

| Shop script | Selector | Actual merchandise IDs | Insufficient-money target |
| --- | --- | --- | --- |
| `052000:027` | `01` | `03`, `1a`, `1b`, `1d` | entry 029 |
| `052000:030` | `01` | `3d`, `4d`, `51`, `63`, `75` | entry 029 |
| `052000:034` | `03` | `81`, `a2`, `a3`, `9a`, `93` | entry 049 |

Do not treat selector `01` or final branch bytes `1d`/`31` as merchandise
IDs. They are control data, not inventory-name exposure.

The `#F` handler at `0xda71` parses the amount then uses the final payload
byte as the insufficient-money branch. Hotel entry 041 uses
`#F 03 01 01 27` (10 credits, failure entry 039); drink entries 055 and
056 use `#F 03 01 02 36` (20 credits) and `#F 03 01 01 36`
(10 credits), respectively, both failing to entry 054. The adjacent
052/053 entries are the price/choice dialogue, not the debit instruction.

## Guarded fortune-teller header allocation

The girl entry `052000:008` begins at `0x522f0` and has 14 bytes: one
opening control byte, a two-byte Japanese speaker name, a closing control
byte, immutable `#B` and `#G` commands, and a terminator. `GIRL` needs four
ASCII bytes, so ordinary rebuilding exceeds its allocation by two bytes.
The adjacent R01-adapted entry `052000:009` begins at `0x522fe`, occupies
49 bytes, and has a 47-byte rebuilt body followed by two zero padding bytes.
Neither source entry has an opaque tail. The reviewed
`r02_allocations.relocate_girl_header` helper moves only their common
boundary two bytes: 008 becomes 16 bytes, 009 begins at `0x52300` with
47 bytes, and the pair still ends at `0x5232f`. The bank-relative pointer
for entry 009 at `0x52012` changes from `fe 02` to `00 03`; command bytes and
all later entry addresses stay fixed. The helper verifies the whole original
System hash, source and rebuilt pair, selected adaptation, exact header text,
padding, and pointer before patching.

## Reinsertion and evidence limits

The route closure in `r02_flow.py` contains 143 script entries, including
control-only dispatchers and 124 text-bearing entries. Of those, 20 were
already R01 adapted, leaving 104 R02 text-bearing script records. Source
links alone do not prove that every optional path can be reached under the
release's actual flag state. The bar's static tile separation is proven;
object collision, trigger activation and runtime text/layout behavior remain
separate verification work. No emulator traversal is attested here.
