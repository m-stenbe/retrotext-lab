# R02 independent source and surface inventory

Read-only QA against the original System disk (`7df885bfe0bacb7c37809364a993e6ad506e5cd25eac1882eac6c7627bce75d5`) and the R01 final catalog. This inventory identifies text and table dependencies; it does not claim that every interaction is reachable in the bounded story state or that a translated image has passed emulator traversal.

## Hamack stores, work, bar and hotel

The original Hamack script bank is `052000`. The following record offsets and links come from its original pointer table and decoded command tokens:

| Surface | Records and original System offsets | Dependencies |
| --- | --- | --- |
| Weapon shop | `022` `0x52661`, `027` `0x527a2`, `028` `0x527c3`, `029` `0x527e6`, `030` `0x52804`, menu `078` `0x52efa` | `#H` stock selectors in 027/030; menu has weapon, armor and leave choices. |
| Item shop | `023` `0x526d2`, `034` `0x5285d`, menu `079` `0x52f0c` | 023 tests job flag `0x0b` and may route to 067; 034 contains stock selection and another-purchase choice. |
| Bar | `025` `0x5271f`, `051`–`056` `0x52b46`–`0x52c0a`, menu `080` `0x52f1d` | Alcohol/juice/milk menu; minor-drinking refusal, money/confirmation, drink outcomes. |
| Hotel | `026` `0x52748`, `039`–`041` `0x528ca`–`0x52925` | Ten-credit offer, insufficient funds, rest/recovery and departure. |
| Optional job | `008` `0x522f0`, `057`–`076` `0x52c69`–`0x52edd`; `051000:022`–`027` `0x51a02`–`0x51b6a` | 008→072 solicitation; 058→051000:027 accepts and sets flag `0x0b`; 063 issues canned goods ID `0x9c`; 004/074–076 handle recipient; 068/070 call dismissal/no-pay and paid 200-credit endings; 060/071 handle Shoko at hotel. Further control and story-state proof belongs to RE. |

The shop `#H` payloads are `01 03 1a 1b 1d 1d` (weapon), `01 3d 4d 51 63 75 1d` (armor) and `03 81 a2 a3 9a 93 31` (item shop). Handler evidence in `r02_flow.py` classifies the leading `01`/`03` as selector bytes, then merchandise IDs, then a script target `1d`/`31`; those last bytes are entries `052000:029/049` (money-failure text), not item IDs. The displayed stock IDs are `03,1a,1b,1d,3d,4d,51,63,75,81,a2,a3,9a,93`. Canned goods are `9c`. R01 already adapts `03,1a,63,81,a2`; the remaining labels need coordinated name records, reviewed adaptations, source/pointer guards and the nine-cell inventory field check. Item `01` (Ice Needle) and item `31` (Zaizer Cannon) are not established shop stock by these commands.

Most Hamack commercial UI is in bank `052000` rather than an additional resident Opening string. Existing R01 generic item/status prompts cover Opening `0x4662/0x466b/0x467b/0x46a6/0x46c4/0x46d7` and System `0x1d5e/0x1e47/0x1e50/0x1e98`. Three additional Joe resident strings have now been exported and adapted: System `0x1e5b` (8 bytes including terminator, Joe heading), `0x1e63` (11-byte disassembly confirmation), and `0x1e6e` (42-byte item/scrap result template). The actual `BE imm16` loads are at `0xbd6b`, `0xc601`, and `0xc5e0` respectively. Source disassembly at `0xc5e6/0xc5f5` establishes the nine-cell item-name and five-cell amount writes in the result template; independent original-based compilation changes only these three ranges. The still-untranslated Opening `0x4430`–`0x45d0` and `0x477d`–`0x49cf` groups describe tank/ship/space commands in their source text. This is source classification, not a runtime claim that none is visible in R02. Credit amounts appear in script text: hotel 10, bar 20/10, job payment 200. Shop price rendering remains to be checked in a frozen candidate.

## Joe and location-name expansion

Actor 4's profile pointer is System `0x1b63`→`0x1837`; its first byte names Joe with shared name ID 7. The party TALK dispatch table at `0xb43d` maps actor 4 to `082000:002` (`0x823d5`), which contains the Hamack bar/informant lead. A corrected offset read gives Joe's item/equipment bytes at profile `+0x15..0x18 = 1d 00 44 63`: `1d` Submachine Gun (`0x10891`), `44` aiming device (`0x109d3`), and `63` Protector (R01). Their exact display roles still need loader/renderer confirmation. The following byte at `+0x19 = 23` is instead the first **combat ability** slot, ID `0x23` (decimal 35, Universal Driver). My earlier classification of this byte as item ID `23` (Ray Blaster) was a QA offset error; the extra item-name record is harmless but not required by Joe's initial gear. The expanded R02 name packet includes both item `44` and item `23` as separate records.

The original learning-slot writer at `0x7904` selects combat slots `+0x19..0x26` (14 bytes) for ability IDs below decimal 55 and field slots `+0x27..0x2c` (six bytes) for IDs 55 and above. Joe's starting combat slot `+0x19 = 23` resolves to `万能ドﾗｲバｰ` (Universal Driver) at `0x11136`, with five ability-pointer aliases `0x1033e/40/42/44/46`. His six field slots are `40 41 42 00 00 00`; IDs `40` Performance Analysis (`0x111b7`), `41` Custom (`0x111c0`) and `42` Mech Repair (`0x111c5`) are translated. Byte `+0x2d = 46` lies outside those six slots and is not an additional starting ability. The class-7 table pointer at `0x793b` selects `0x79a0`, one threshold/ID pair: IQ strictly greater than 1260 grants combat ability decimal 36 (`0x24`), `電磁バブﾙ` (Electromagnetic Bubble) at `0x11142`. The level-up class filter at `0x78a0` skips classes 5–6 but lets class 7 through, so repeated XP4 grinding can expose this name before the R02 endpoint. Both newly proven ability IDs have guarded R02 name records; actual acquisition timing remains a runtime question.

The map-title pointer table at System `0x10440+2*mapID` gives additional R02 labels:

| Map ID | Pointer | Source storage | Original title |
| --- | --- | --- | --- |
| 2 | `0x10444` | `0x112c8` | Underground Bar |
| 48 | `0x104a0` | `0x114b4` | Hamack town |
| 98 | `0x10504` | `0x1170e` | Dust |
| 103 | `0x1050e` | `0x11744` | Joe's room |

These four titles are absent from the R01 catalog and require alias/width review in the R02 name adapter. Jane is embedded in script `052000:013/044/045`; those entries do not use a shared name token for her name. This does not exclude other references elsewhere.

## Shared underground bar partition

Independently repeated the source-grid check in `docs/r02-re-source-evidence.md`: map 2's descriptor at System `0x4779+8` loads 4,096 tile bytes at `0xb0000`; metadata is `0x84c00`, and tile zero's Data-disk attribute at `0x4c400` is `0x14` (collision property `0x10`). A separate flood fill from Hamack's entrance tile `(13,1)`, treating **all nonzero tiles as walkable**, reaches exactly 322 cells within x=0–17, y=0–17 and exactly object entries `053000:001`–`012`. The other 26 map objects lie in disconnected nonzero components. RE's movement-handler disassembly says property `0x10` blocks passage. Thus the later-town clusters in the shared bar map are statically outside the Hamack entrance's component; actual doorway transitions still await runtime traversal.

## Scripted cinematic check

Original metadata for maps 48 (Hamack), 98 (Dust), 103 (Joe's room) and 2 (shared bar) contains zero tile-script records at header+19. Scanning all 143 entries in `r02_flow.route_closure` finds no `?V` (`3f56`) command; the R01 meteor trigger entry `051000:029` does contain `?V 01 01`. This supports no **new scripted cinematic stream** in the bounded R02 static closure. It does not rule out ordinary map animation or prove emulator behavior. The cumulative R01 meteor stream remains required in the R02 build.

## QA gates still open

The initial seeded R02 plan listed none of the shop, hotel, bar, work menu, Joe ability or new location-title records; the manager has since expanded its required inventory, including the three newly found Joe resident UI strings. The R01-inventoried owner/target fields (`0x1d72/0x1d7c`), ability headings (`0x1d86/0x1d99`), unavailable message (`0x1e2b/0x1e2f`), and R02 disassembly fields (`0x1e5b/0x1e63/0x1e6e`) cover identified resident text near Joe's actions. The remaining Opening `0x4430`–`0x45d0` group describes tank, ship, and space controls in its source. No additional fixed Japanese Joe-action UI has a proven route in this bounded source inventory; dynamic outcomes and renderer behavior remain runtime questions. Canonical Japanese-to-English review, adaptation validation, combined build and exact binary/IPS/source-hash checks follow on a frozen catalog and build. A successful static comparison cannot verify movement, menu rendering, price fields, save-state behavior or map transitions; those remain runtime checks.
