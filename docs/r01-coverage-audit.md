# R01 independent source coverage audit — 2026-09-23

The 39-record seed is not a complete inventory. Source inspection identifies two
omitted pickup messages, several omitted resident gameplay messages, and two
missing equipment/item names. The work/job conversation belongs to a Hamack
interaction chain, not to Cosma merely because some of its strings share Cosma's
bank. No emulator run or complete world-event graph was obtained by this audit.

Evidence: original Opening and System images passed `load_images` SHA-256 guards;
`work/adapted-batch-05.json` was inspected without mutation. Snapshot fingerprint:
`6645ba1221eb78ec507e4fbf463f81a36d1f7ba3e63f62c6fc1fa43f7de2624b`.
The exact source hashes and decoded call evidence are in ignored
`work/r01-qa-call-evidence.json`. English summaries below are discovery notes,
not editorially approved adaptation packs. All offsets are original disk offsets.
`work/r01-qa-menu-geometry.json` records all 62 resident menu-table records with
original width/rows/coordinates/pointer and source bytes; keep it ignored.

## Directly connected story omissions and control dependencies

| Source | Offset | Evidence and action |
| --- | --- | --- |
| `script:061000:020` | System `0x614d6` | Cannot carry the item; give up. Called by `051000:038`, itself the failure index `0x26` in the Hand Medical award `#I 01 81 26` at `051000:035`. Add canonical/adaptation work and verify the award-handler branch semantics. |
| `script:061000:022` | System `0x61508` | Nothing left here. `051000:036` checks flag `0x35` and branches to entry 40 (`#B 35 28`); `051000:040` calls this message through `#P 10 16`. Include the repeat/exhausted pickup path. |
| `script:051000:038` | System `0x51fd7` | Control-only wait plus `#P 10 14`: inventory-full pickup continuation. Preserve and inventory dependency; do not count as newly translated dialogue. |
| `script:051000:039` | System `0x51fde` | Control-only award `#I 01 63 26` plus flag `#S 35`. Reached from Protector pickup `036` through `#B 10 27`; shared failure route is entry 38. |
| `script:051000:040` | System `0x51fe9` | Control-only shared empty-pickup call. |
| `script:051000:042` | System `0x51ff9` | Control-only knife award `#I 01 03 26`, reached from `034` through `#B 02 2a`; shared failure route is entry 38. |
| `script:051000:031` | System `0x51f41` | Soldier dispatcher: checks flag 6, branches to 33, otherwise sets flag 6 and calls `054000:000`. First and repeat paths must both be covered. |
| `script:051000:032` | System `0x51f50` | Crater dispatcher calls `052000:083`. |
| `script:051000:033` | System `0x51f56` | Repeat interaction calls `053000:013`. Already translated callee, but the dispatcher must be in the dependency inventory. |

For pickups, `#P` preserves caller display state. Validate whole composed messages,
including suffix `051000:041`, item color changes, wait/clear placement, and the
failure/repeat paths. A record-local layout pass is insufficient.

Within the ordinary Cosma dialogue seed, decoded `#B/#Y` links already cover
Lucia's warning/rest/suspicion (`001→014→015`), Shoko's repeat/accept/refuse
(`002→013`, `002/013→011/012`), young man's return reaction (`003→020`), wasteland
warning/return report (`008→021`), and Karu's greeting/return (`010→016/019`).
This checks these known entry links, not every map object that can start dialogue.
The old-man inventory check `#C 01 a2 12` still needs handler-level confirmation;
its listed continuations `017/018` are already in the seed.

## Work/job classification

Exact decoded cross-bank calls establish the following grouping:

| Hamack source | Cosma-bank callee | Meaning |
| --- | --- | --- |
| `052000:058` | `051000:027` | Accept job; Sion and Karu work, Shoko waits at the hotel |
| `052000:061` | `051000:025` | Counter clerk angry about the absence |
| `052000:062` | `051000:026` | Ask the counter clerk for work |
| `052000:064` | `051000:024` | Inventory full |
| `052000:068` | `051000:022` | Dismissal without wages |
| `052000:070` | `051000:023` | Dismissal with 200 credits |

Hamack girl `052000:008` branches to `072`; `072` offers work and selects
`058/057` via `#Y 3a 39`. The item shop at `052000:023` checks job flag `0x0b`
and selects counter-clerk entry `067`. The job sequence further includes `063`
(delivery request), `065/066` (delivery reminders), `068/069` (failure/item
handling), `070` (paid completion), `060/071` (Shoko at the hotel), and
`004/074/075/076` (recipient and delivery outcomes).

**Classification:** these are Hamack optional-work dependencies, suitable for the
R02 packet. Existing R01 entries `024/025/026` are not a complete job scene. Their
presence in bank `051000` does not prove R01 reachability. Conversely, the audit
does not prove that the world map prevents an early Hamack detour. Before removing
them from a temporal "all available interactions" promise, map the exits/flags
or explicitly define R01 as the Cosma–canyon route with Hamack excluded. The job's
dialogue assumes Karu is present, but dialogue content alone is not a trigger guard.

## Required gameplay surfaces missing from the seed

These resident Opening strings are already catalogued but untranslated. Their
table records prove they are wired into resident UI; exact availability depends
on the corresponding action and state. They are not speculative bank neighbors.

| Catalog suffix / source offset | Table record | Gameplay exposure |
| --- | --- | --- |
| `ui:Opening:004662` | `0x407b` | Item use/discard menu |
| `ui:Opening:00466b` | `0x4081` | Use/discard/disassemble variant; disassembly availability before Joe is unproven |
| `ui:Opening:00467b` | `0x4087` | Cannot remove equipment with full inventory |
| `ui:Opening:0046a6` | `0x408d` | Item cannot be used here |
| `ui:Opening:0046c4` | `0x4093` | Item has no effect |
| `ui:Opening:0046d7` | `0x4099` | Item cannot be discarded |
| `ui:Opening:00421c` | `0x3feb` | Prepare a blank User Disk for formatting |
| `ui:Opening:004268` | `0x3ff1` | Formatting in progress |
| `ui:Opening:0045e2` | `0x4069` | Write-protected disk prompt |
| `ui:Opening:00461e` | `0x406f` | Format failure |

The latter two are exceptional conditions, not required destructive playtest
actions. Verify text and guarded handling with test images/mocks; never format
the player's existing User Disk to exercise them.

Original System resident messages not present in the inspected catalog:

| Offset | Meaning / exposure |
| --- | --- |
| `0x1d5e` | Inventory full; item-award failure path |
| `0x1d86`, `0x1d99` | Combat / field special-ability headings |
| `0x1e47`, `0x1e50` | Discard item suffix and confirmation |
| `0x1eaf` | Overweight right-hand equipment warning; includes embedded display controls |
| `0x1ed2` | Failed escape from combat |
| `0x1fd8` | Learned a new ability, following level-up; contains runtime `=01` substitution |

The word-sized address patterns for these strings also occur in System code:
`1d5e→d96c`, `1d86→7462/b226`, `1d99→b1d7`, `1e47→9990/b2b3`,
`1e50→b2ba`, `1eaf→9fe5/9fe8`, `1ed2→6659`, `1fd8→78f5/e2c7`.
These are **operand search anchors**, not disassembled call proofs. Inspect the
surrounding instructions before accepting a new adapter or changing span bounds.
Ability acquisition is conditional on level/class; 4× EXP makes it especially
important to inventory, but its R01 level threshold is not yet mapped.

Existing English legacy patches also need inclusion in the release inventory:
field/battle/party/yes-no/start/system menus; save/load and return-to-Data-Disk
prompts; dynamic disk prompts; no-items/no-skills/no-equipment results;
`fixed:System:001edf` combat rewards and `fixed:System:001f28` level-up. Presence
in an experimental patch is not canonical completion. Status/equipment labels
at Opening `0x418b/0x438a` already contain English letters and renderer controls;
audit their rendered output instead of treating their untranslated status as
proof of Japanese text. Do not include vehicle/ship/debug menus solely because
they share the resident menu table.

## Item and name exposure

| Original source | Pointer evidence | Exposure |
| --- | --- | --- |
| System `0x10a99`, 4 bytes including terminator | Item pointer aliases `0x100b8..0x100c2`, IDs `0x5c..0x61` | Shirt: manager identified as required equipment; this audit confirms source/aliases, not initial-party setup. Full-width SHIRT cannot fit this original span. |
| System `0x10aa1`, 8 bytes including terminator | Item pointer `0x100c6`, ID `0x63` | Protector: pickup `051000:036/039`; equipment and inventory name absent from current catalog |
| System `0x10cb0`, 9 bytes including terminator | Item pointer `0x10144`, ID `0xa2` | Camp Set: old-man gift `051000:017`; inventory/use name absent from current catalog |
| System `0x107aa` | Item pointer `0x10006`, ID `0x03` | Survival Knife: pickup and equipment; existing legacy KNIFE |
| System `0x10875` | Item pointer `0x10034`, ID `0x1a` | Handgun: Shoko gives weapons in `051000:011`; existing legacy GUN |
| System `0x10b74` | Pointer aliases `0x100f4..0x10102`, IDs `0x7a..0x81` | Hand Medical: `051000:035` awards ID `0x81`; existing legacy MEDS. Preserve alias semantics. |

Short/full character names and Cosma/Hom/Saxen titles have partial legacy
translations; inventory all actual status/party/title exposures separately from
dialogue substitutions. Other nearby location names do not become R01 solely by
proximity in their table. Encounter species names, ability names, initial equipment
and combat action/status messages still require encounter/party initialization
mapping. This audit has not identified all those source spans.

## Remaining discovery blockers and QA handoff

1. Map object/event dispatch for Cosma, canyon and meteor state transitions;
   record fresh, invitation accepted/refused, meteor completed and Karu-joined
   states. Bank call closure alone cannot establish world reachability.
2. Close cinematic coverage with the independent cinematic adapter work and
   compare every reachable event text segment, not just existing screenshots.
3. Add the two pickup outcomes and resident messages above with full adapter
   validation; verify successful, full-inventory and repeat interactions.
4. Map early encounters, loss/retry, fleeing, status ailments, ability acquisition,
   save slots/load selection and disk-error paths. Current two fixed combat
   scripts do not prove combat completeness; save/load menu labels do not prove
   save/load-flow completeness.
5. Compare the final cumulative candidate against this inventory and run
   reproducible smoke/transition checks. No runtime success is attested here.

Until these unknowns have evidence, keep route/branches/UI/names discovery open.
This is a concrete expansion queue, not an exhaustive all-game inventory or a
claim that all observed strings can be inserted with the current adapters.

## Follow-up: handler and name geometry evidence

Independent 16-bit disassembly of the hash-verified original System resolves two
earlier branch questions. The command table at `0x33eb` points `#C` to `0xd8c9`:
it consumes inventory selector and item, calls the item search through `0xd8e1`,
and branches via `0xd723` using its third payload byte when the result is not
`0xff`. Thus the old-man `#C 01 a2 12` checks the Camp Set and selects entry 18
when present. `#I` at `0xd88b` consumes selector, item and failure entry; an award
failure from `0xb870` selects that failure entry through `0xd724`. Target `0xff`
uses the generic failure helper instead. This proves `035/039/042→038→061000:020`
and the old-man gift's generic inventory-full path without needing screenshots.

The direct UI name renderer at System `0x1b0b1` converts ASCII capitals through
the driver (`0x1b0cd..0x1b0dd`, INT 41h AH=19h), unlike dialogue `$` substitution
at `0xf38d`. Its normal mode draws a full-width glyph then advances DI twice
(`0x1b11b..0x1b128`); it does not wrap or clip to a box width. Therefore storage
capacity and an arbitrary common 12-character cap cannot establish name fit.

| Consumer | Original code evidence | Safe constraint for the current patch |
| --- | --- | --- |
| Inventory list | `0xb3a3`: CX=9, BX=15, DI=`0x0a0c`; `0xf5f3` stores width CL in `0x1d4e`. Text starts `0x0f10`; selection highlight at `0xb3c3` is 18 VRAM bytes. | Nine full-width cells. Protector uses all nine; Camp Kit and Shirt fit. |
| Discard confirmation | `0xb2a8` item starts at DI=`0x4108`; `0xb2af` places the sentence suffix at `0x411a`. | The fixed suffix starts nine full-width cells after the item name. Names longer than nine overlap it. |
| Equipment detail | `0xa454`: CX=13; item name called through `0xa47e→0xf5b5`. | Current item names fit its 13-cell box. |
| Ability lists | `0xb1cd` field list and `0xb21c` combat list use CX=10, through `0xf5f3`; names call `0xb1ef→0xf5a5→0x1b08e`. | Ten cells. The original proposed 11-cell Telekinesis adaptation exceeded this. |
| Learned-ability message | `0xf441..0xf44c` consumes `=ID`, calls `0xf5a5` at `0xf444`, then restores DI and advances it by `0x10`. | Existing runtime field reserves eight full-width cells. Current adapter now constrains ability names to eight; the fixed five-cell indentation plus that field fits the 14-cell dialogue. |
| Save-slot list | `0xb61f` uses a 15-cell, ten-row box; `0xb651` renders numbered entries. `0xb676→0xf59e→0x1b078` renders the saved location with half-width mode (`0x712f=1`), then the level label starts at the preserved DI plus `0x10`. | Location names have a distinct half-width consumer. Do not apply normal full-width arithmetic to this path. Current location labels fit before its level field. |

For save/load, `0xb61f..0xb693` constructs ten numbered slots from the existing
numerals at `0x1df5`, location lookup and `L.` at `0x1e27`; no extra Japanese slot
caption appears in this inspected path. Load helper `0xfca0` calls the resident
disk interface, reads a slot, checks the empty-slot marker `0x0505`, and either
copies state or returns failure. Existing load/save/data-return prompts remain
the separately inventoried resident menus. This does not prove every error or
post-defeat overlay path; those remain separate transition checks.

The following independent regression tests now exercise the discovered risks:
`test_alshark_names.py` rejects overwidth abilities even when the reviewed spelling
map is updated, and checks every compiled ability fits eight cells.
`test_alshark_interface.py` rejects a storage-fitting 26-cell reward line, altered
runtime-field line shape, and five rows substituted for a one-line fixed UI string.
All seven names tests and four interface tests passed after the fixes.

## Follow-up: ordinary battle targeting, status and defeat source closure

The earlier targeting/reload questions were inspected as caller paths, rather
than inferred from missing string-search results. This closes the ordinary
on-foot UI source-discovery questions below; runtime appearance and control
behavior remain unverified until exercised in the candidate.

**Targeting is a sprite-coordinate interaction.** The on-foot action menu is
selected at System `0x81c5` with resident menu index `0x0b` (the already translated
battle menu). Attack dispatch is `0x81ee→0x8205→0x83ec`. With multiple targets,
`0x8415` calls input handler `0x856d`, which reads `0x3474` and updates cursor
coordinates `0x4f42/0x4f43`. `0x8424..0x8455` checks those coordinates against
enemy sprite bounding boxes; bit `0x80` in enemy record byte `+9` marks the
highlighted target. Confirm/cancel selects the matching enemy index or returns
failure. No enemy-name table or target-caption string is read in this path.

Its refresh loop `0x60ad→0x60ea` invokes party, enemy and effect drawing at
`0x611c/0x6147/0x6167`; `0x610d→0xcbea` draws the cursor object. The party/enemy
drawers call `0xcbea/0xcd97`, then `0xcc48/0xcda0`, and ultimately the tile blitter
at `0xf0f3`, which consumes tile bytes, including the transparent `0xff` marker.
`0xcd56..0xcd60` translates the target bit into a graphic highlight selector.
This is graphical selection, not an untranslated named-enemy menu.

**Damage and status updates use numeric state and graphic/effect selectors.**
`0x7ead→0x7f08` compares damage with target vitality and selects feedback IDs;
`0x160d` passes these IDs to INT 42h AH=1. `0x7eb0..0x7ed4` updates vitality and
death flags. `0x87dd..0x8899` translates status bits and vitality/magic thresholds
into a numeric state nibble in combat record byte `+0x0b`; it does not select a
text string. The related recovery/tick path `0x889d..0x8925` updates those bits
and calls the same state/damage helpers. No Japanese damage sentence or textual
ailment label was found in these directly inspected routines. Visual status
feedback still needs a runtime check; this is not a claim about every late-game
battle animation or every graphical asset.

The Status action itself is `0x823e→0x98de`, returning to the existing owner
selection/status/equipment/ability UI. Special Abilities follows
`0x82fd→0xb21b` to the already inventoried combat-ability heading and name list;
the no-ability branch `0x8349→0xb248` uses the existing character-name and
ability-unavailable message. These are reused surfaces, not additional source
records hidden in the battle menu.

**Defeat rejoins the normal load flow.** Party defeat sets `0x347d` at `0x7ed4`;
`0x61c0` detects it and branches through `0x6224` cleanup to `0x0101`. After reset
and graphical housekeeping, `0x0131` explicitly jumps to `0x00a7`. At `0x00b0`
resident menu index 8 displays the existing User Disk load prompt (Opening
`0x4348`); `0x00be→0xb61f` draws save slots, `0x00c1→0xb641` selects one, and
`0x00ca→0xfca0` loads it. Failure repeats slot selection; success calls
`0x00d5→0xb5e2`, whose resident menu index 5 is the existing Data Disk return
prompt (Opening `0x4294`). No separate retry/game-over caption is selected in
this directly traced control flow.

There is therefore no newly identified untranslated source string blocking
these ordinary battle/targeting/status/defeat UI paths after the known menu,
ability, flee, reward, level-up and disk-prompt records are integrated. Keep
target selection, damage/status visibility, failed escape and defeat/reload on
the runtime verification checklist. Do not describe this bounded source finding
as proof that the entire game's combat artwork or later overlays are localized.

### Inventory-domain judgment and final image checks

For the declared **Cosma–Saxen Canyon–meteor–Cosma return** route, the inspected
UI and name/item source inventory can be marked mapped once the integrated packs
and the separate Party/Talk scene dependencies are present. No additional
untranslated UI, item, equipment or ability-label source was found in this
bounded audit. Runtime display checks remain pending; mapping is not their
substitute. Hamack/Dust, vehicle/ship/debug UI and startup staff artwork are
outside this judgment. World/map route coverage remains the separate RE audit.

Party Talk is not a hidden name-rendering gap: `0xb415` reads an actor ID from
`0x19db`, then indexes dispatch table `0xb43d`. The actor lookup at `0x0ad2`
uses pointer table `0x1b5d`: actor 1 maps to profile `0x1777` and name ID 1
(Sion), actor 2 to `0x17b7` and name ID 3 (Shoko), actor 3 to `0x17f7` and name
ID 4 (Karu). The Talk destinations are consequently `082000:007`, `082000:000`
and `082000:001`; their dialogue belongs in the route/branch inventory. Do not
confuse those array IDs with the `#W` object/profile selectors 3 and 5.

Independent checks of `work/r01-03-xp4` verified all six image sizes and original
source hashes, both patched-image manifest hashes, byte-identical copies of the
four unmodified images, and exact reconstruction of both modified images from
their IPS patches. Every current item/ability pointer alias resolves to the
reviewed short label, with item names at most nine and ability names at most
eight cells. The declared 4× EXP trainer separately replaces the reward heading
with Base Rewards; this intentional override must be applied before comparing
final bytes with the canonical-overlay compiler. Evidence is recorded locally in
`work/r01-qa-final-03.json`. Later builds require their own artifact checks.

**Frozen final candidate check: PASS.** `work/r01-04-xp4` was independently
checked against `work/r01-final-catalog.json` and the final release plan. All six
image sizes/source hashes, the two modified-image manifest hashes, four unchanged
images and both IPS roundtrips pass. Every canonical patch range matches a fresh
compiler run plus the declared trainer; the complete 138-record localization
manifest and 33-scene candidate-ready release assessment also match exactly.
Current item/ability aliases resolve to the bounded reviewed names. Report:
`work/r01-qa-final-04.json`. Catalog fingerprint:
`0b6ebd2ce591d922cad8c8a4655b70e1379072bb07799802217542926cb65dc6`;
plan fingerprint:
`d88cfa2df07b2cdca82cf7019745893e963f243a43eda7ed585e9f094e1b55c3`.
This is an independent artifact/source-validation pass; runtime verification
remains false rather than being inferred from successful compilation.
