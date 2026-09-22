# Alshark abbreviation and UI fitting audit — 2026-09-22

Audit of the actual `editorial-batch-01-test` disk images, verified against their patch manifest. No disk files, canonical translations, or build defaults were changed. This distinguishes effective on-disk labels from old compatibility drafts still present in source code.

## Scope

All **44 previously translated UI, shared-name and battle-result units** were compared with the reviewed canonical English. They contain multiple menu rows and runtime fields. The **32 dialogue/branch/pickup entries** are covered by the [full editorial review](editorial-review-2026-09-22.md); the first seven adapted entries are documented separately. This audit does not claim coverage of all untranslated game text.

## Findings that should drive the next changes

| Area | Effective game text | Canonical target / decision | Constraint or meaning issue |
| --- | --- | --- | --- |
| Combat | ATTACK / SKILLS / ITEMS / EQUIP / STATUS / FLEE | Attack / Abilities / Items / Equipment / Status / Flee | Abilities and Equipment need 9 cells; box/highlight currently cover 6. |
| Field | STATUS / ITEMS / PARTY / EQUIP / SKILLS / SYSTEM | Status / Items / Party / Equipment / Abilities / System | Same two 9-cell labels. Normal/alternate field menus share highlight code. |
| Alternate field | DATA plus the field menu | Data Display plus the field menu, pending behavior review | Full Data Display is 12 cells; cannot blindly use the normal menu's 9-cell sizing with a shared highlight. |
| Party submenu | TALK / ROW | Talk / Formation | Current box is 5 cells; Formation is 9. Original allocation 16 bytes; full pair 28. |
| System | SYSTEM / SAVE / LOAD / TEXT / FORMAT | System / Save / Load / Text Speed / Format User Disk | Text Speed is 10 cells and Format User Disk 16; current box is 8. Position/overlap and highlights need review. |
| Text speed | SPEED / FAST / NORMAL / SLOW | Text Speed / Fast / Normal / Slow | Text Speed already fits this menu's 11-cell width; string storage grows from 42 to 52 bytes. |
| Canyon heading | SAXEN | Saxen Canyon | Full name needs 25 bytes vs 11 original. Spelling stays provisional; not Saxon. |
| World-map heading | HOM | Planet Hom | Full name needs 21 bytes vs 9 original. Loss of planet context made the proper name look odd. |
| Inventory weapons | GUN / KNIFE | Handgun / Survival Knife | 15 vs 8 bytes; 29 vs 11 bytes. Pointer/allocation work, not just wider text windows. |
| Item name | MEDS | Unresolved medical-item term | Do not expand into an invented kit/device/medicine name merely because space becomes available. |
| Ability error | NO SKILLS. | {character} cannot use abilities. | Source states inability to use abilities, not necessarily absence of learned skills. Caller condition still needs tracing. |
| Character selectors | WHO? / WHO? | Select a character / Select a recipient | Current wording collapses subject/owner and recipient roles. Exact shorter adaptations can be chosen after layout review. |
| Formation headings | ORDER / REORDER / NEW ORDER | Current Formation / Change the party formation / New Formation | Headings and instruction need coherent terminology. New Formation plus numbered rows fits the original byte allocation, but display width is not yet proven. |
| Save/load/restore prompts | SAVE USER DISK / LOAD USER DISK / DATA DISK | Complete insertion/return instructions | Some missing information is implicit in the menu context; adapt as complete instructions, preserving disk/drive/key details. Wider menus do not fix these separate prompts. |
| Full-name variants | Given names only | Separate full names and Scrap Joe epithet | Source ID variants must stay distinct canonically; shared pools/pointers and name widths need coordinated review. Sion/Lucia surname unresolved. |

## What can stay compact

- YES / NO is already restored and confirmed readable. STATUS, ITEMS, PARTY and SYSTEM are also already restored; do not report their old abbreviations as current defects.
- ATTACK and FLEE are clear commands. They do not need longer wording to satisfy an expansion policy.
- START / LOAD are conventional, understandable labels. New Game / Load Game remain canonical, but changing them is lower priority; their individual 14-byte slots hold only seven full-width cells, while the full labels need eight/nine.
- NO ITEMS and NO GEAR TO EQUIP are understandable UI messages. They are not evidence that every English label must match unrestricted canonical prose verbatim.
- EXP and PTS are recognizable result-screen abbreviations. Keep clarity and numeric interpretation; the more important reward-message issue is the omitted per-member experience wording.
- PP, MP, IQ and the compact R.Str/L.Str/Agl/Drb labels are present in the original game. They were not all introduced by our translator. Do not invent full expansions or game mechanics; Drb remains unresolved. Equipment/status labels outside the modified spans require a separate renderer audit rather than assumptions based on English-looking text.

## Storage versus geometry

All counts below assume the currently verified full-width CP932 UI renderer (two bytes per Latin cell, one byte per row separator and terminator). They are measurements, not approval to insert text.

| Relocated menu | Current bytes | Full canonical bytes | Current width | Full canonical width |
| --- | ---: | ---: | ---: | ---: |
| `ui:Opening:004158` | 72 | 86 | 6 | 9 |
| `ui:Opening:00414d` | 81 | 111 | 6 | 12 |
| `ui:Opening:0043f8` | 70 | 84 | 6 | 9 |
| `ui:Opening:0048af` | 12 | 12 | 3 | 3 |
| `ui:Opening:0042d5` | 53 | 85 | 8 | 16 |
| `ui:Opening:004637` | 42 | 52 | 11 | 10 |

Current six-menu pool use: **330/512 bytes**. Full canonical rows for those six menus: **430/512 bytes**. Adding Talk / Formation in the same pool would total **458/512 bytes**, leaving 54. This is sufficient storage for that scoped menu batch, but not a general-purpose text heap. Additional prompts, item names and arbitrary strings must not be assumed to fit there or share the resident driver's lifetime/addressing.

Known geometry/highlight evidence:

- Opening table records `0x3FD9`, `0x3FDF`, `0x401B`: field, alternate field and on-foot battle. Current width bytes are 6. Battle Equipment/Abilities needs 9; corresponding highlight byte width would be 18 instead of 12.
- System field highlight immediate: `0x98BA`; battle: `0x81D2`. The alternate field menu shares the field instruction. Keep all menu/action row counts and dispatch order unchanged.
- Party record Opening `0x40FF` currently has width 5, two rows. System `0xB3D7` requests menu ID 0x31; `0xB3DF` sets highlight width 10 (immediate at `0xB3E3`). Formation would need width 9 and highlight 18, followed by navigation/erase tests.
- System and text-speed records are `0x3FFD` and `0x4075`. Their widths are 8 and 11. Widening System to show the complete 16-cell Format User Disk label requires a screen-position/overlap and highlight audit first.
- Ability-unavailable renderer at System `0xB239` requests a 15-cell/two-row box, places the character name separately, then renders the subject connector at `0xB25A` and message at `0xB263`. Its fixed name/body coordinates mean total box capacity alone does not prove a reflow fits.

## Separate untranslated coverage gaps

The Format User Disk creation prompt and its in-progress/completion/error interactions need a connected system-message pass. Camp Kit and Shirt are still Japanese shared inventory labels; this is missing coverage, not an English abbreviation regression. Translate/adapt those through canonical records and verified name-pointer handling. The camp item's exact recovery behavior and the medical item's nature remain unverified.

## Recommended implementation order

1. Add a verified fitting adapter for the resident menu pool, preserving canonical review bindings and row order. Test 9-cell combat labels first, then coordinate both field variants and their shared highlight.
2. Restore Formation and the Text Speed heading. Investigate System geometry and all Format prompts as one coherent interaction.
3. Handle location and item-name allocation/pointer constraints separately; keep unresolved terminology pending.
4. Review selectors, formation headings and ability-unavailable message as complete UI flows.
5. Revisit full names and battle result wording while preserving fixed runtime fields, then continue the dialogue-fitting backlog.

Every change still requires guards, source hashes, roundtrips, layout tests and in-game navigation/dismissal checks. The pool measurements do not justify relaxing any existing safeguard.

## Complete checked inventory

Full-width byte projections below are for the unrestricted canonical string; they are not necessarily the final adaptation. An unresolved/dynamic value is left unmeasured. Shared-name pools and relocated menu pools cannot be assessed as independent fixed source slots.

| Source reference | Effective current text | Canonical English | Original span bytes | Canonical bytes | Disposition |
| --- | --- | --- | ---: | ---: | --- |
| `ui:Opening:00414d` | DATA / STATUS / ITEMS / PARTY / EQUIP / SKILLS / SYSTEM | Data Display / Status / Items / Party / Equipment / Abilities / System | 62 | 111 | restore detail or review layout |
| `ui:Opening:004158` | STATUS / ITEMS / PARTY / EQUIP / SKILLS / SYSTEM | Status / Items / Party / Equipment / Abilities / System | 51 | 86 | restore detail or review layout |
| `ui:Opening:004294` | DATA DISK / DRIVE 2 / PRESS ANY KEY | The operation is complete. Put the Data Disk back in drive 2, then press any key. | 65 | 163 | restore detail or review layout |
| `ui:Opening:0042d5` | SYSTEM / SAVE / LOAD / TEXT / FORMAT | System / Save / Load / Text Speed / Format User Disk | 49 | 85 | clarify meaning |
| `ui:Opening:004306` | SAVE USER DISK / DRIVE 2 / PRESS KEY | To save your game, insert the User Disk into drive 2, then press any key. | 66 | 147 | restore detail or review layout |
| `ui:Opening:004348` | LOAD USER DISK / DRIVE 2 / PRESS KEY | To load your game, insert the User Disk into drive 2, then press any key. | 66 | 147 | restore detail or review layout |
| `ui:Opening:0043f8` | ATTACK / SKILLS / ITEMS / EQUIP / STATUS / FLEE | Attack / Abilities / Items / Equipment / Status / Flee | 56 | 84 | restore detail or review layout |
| `ui:Opening:004637` | SPEED / FAST / NORMAL / SLOW | Text Speed / Fast / Normal / Slow | 43 | 52 | restore detail or review layout |
| `ui:Opening:0046ec` | NO GEAR / TO EQUIP | There are no items available to equip. | 32 | 77 | clear compact form |
| `ui:Opening:004aec` | NO GEAR / TO EQUIP | There are no items available to equip. | 32 | 77 | clear compact form |
| `ui:Opening:0048af` | YES / NO | Yes / No | 7 | 12 | clear compact form |
| `ui:Opening:0048b6` | TALK / ROW | Talk / Formation | 16 | 28 | clarify meaning |
| `ui:Opening:00470c` | START | New Game | 14 | 16 | restore detail or review layout |
| `ui:Opening:00471b` | LOAD | Load Game | 14 | 18 | clear compact form |
| `ui:Opening:004b0c` | START | New Game | 14 | 16 | restore detail or review layout |
| `ui:Opening:004b1b` | LOAD | Load Game | 14 | 18 | clear compact form |
| `ui:System:001d72` | WHO? | Select a character | 10 | 37 | clarify meaning |
| `ui:System:001d7c` | WHO? | Select a recipient | 10 | 37 | clarify meaning |
| `ui:System:001dac` | ORDER | Current Formation | 11 | 35 | restore detail or review layout |
| `ui:System:001db7` | REORDER | Change the party formation. | 16 | 55 | restore detail or review layout |
| `ui:System:001dc7` | NEW ORDER / 1 / 2 / 3 / 4 / 5 | New Formation / 1 / 2 / 3 / 4 / 5 | 46 | 42 | restore detail or review layout |
| `ui:System:001e2b` | (subject connector omitted) | {character} | 4 | — | clear compact form |
| `ui:System:001e2f` | NO SKILLS. | cannot use abilities. | 24 | 43 | clarify meaning |
| `ui:System:001e98` | NO ITEMS. | You are not carrying any items. | 23 | 63 | clear compact form |
| `ui:System:0107aa` | KNIFE | Survival Knife | 11 | 29 | restore detail or review layout |
| `ui:System:010875` | GUN | Handgun | 8 | 15 | restore detail or review layout |
| `ui:System:010b74` | MEDS | {item.hand_medical} | 11 | — | investigate terminology |
| `ui:System:011329` | HOM | Planet Hom | 9 | 21 | restore detail or review layout |
| `ui:System:011723` | SAXEN | Saxen Canyon | 11 | 25 | restore detail or review layout |
| `name:0` | SION | Sion | 4 | 9 | working name not an abbreviation |
| `name:1` | SION | Sion {surname.asmaan} | 11 | — | investigate terminology |
| `name:2` | SHOKO | Shoko | 5 | 11 | working name not an abbreviation |
| `name:3` | SHOKO | Shoko Penrose | 14 | 27 | restore detail or review layout |
| `name:4` | KARU | Karu | 3 | 9 | working name not an abbreviation |
| `name:6` | JOE | Joe | 5 | 7 | working name not an abbreviation |
| `name:7` | JOE | Scrap Joe | 13 | 19 | restore detail or review layout |
| `name:12` | LUCIA | Lucia | 4 | 11 | working name not an abbreviation |
| `name:13` | LUCIA | Lucia {surname.asmaan} | 11 | — | investigate terminology |
| `name:14` | MAMON | Mamon | 4 | 11 | working name not an abbreviation |
| `name:15` | MAMON | Mamon Penrose | 13 | 27 | restore detail or review layout |
| `name:16` | JIDO | Jido | 5 | 9 | working name not an abbreviation |
| `name:81` | COSMA | Town of Cosma | 10 | 27 | restore detail or review layout |
| `fixed:System:001edf` | PARTY GAINS / EXP / CREDITS / SCRAP / GAINED, with numeric fields | Each party member gained {experience} experience points. / Credits gained: {credits} / Scrap gained: {scrap} | 73 | — | retain familiar abbreviations review sentence and fields |
| `fixed:System:001f28` | LEVEL UP / PP / MP / IQ / PTS / original compact stats / STATS IMPROVED | Level up! / {character} / PP +{pp_gain} / MP +{mp_gain} / IQ +{iq_gain} / R.Str. +{right_strength_gain} / L.Str. +{left_strength_gain} / Agility +{agility_gain} / {stat.drb} +{drb_gain} / Stats increased. | 176 | — | retain familiar abbreviations review sentence and fields |

## Reproduce

```sh
python3 profiles/alshark/audit_labels.py /path/to/original work/editorial-batch-01-test --output work/label-audit.json
```

The tool follows effective menu pointers in the built Opening disk instead of treating superseded short strings as live text. It checks original/patched hashes against the manifest and writes only its audit output. The complete engineering details remain in the ignored JSON; this document contains English findings and source references.
