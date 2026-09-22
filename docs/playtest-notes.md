# Alshark playtest notes

## Workflow

Translate and review connected scenes in batches, then play through longer
sections to assess context, character voices and layout. The next proposed
batch is the starting town through its first story event; its exact boundaries
still need mapping.

Keep a faithful, natural English draft separate from the constrained in-game
wording. If a line cannot fit without losing meaning, record the storage or
layout problem rather than treating an abbreviated version as final. Current
fixed allocations and full-cell lettering remain technical limitations.

For each playtest issue, record the speaker, location, preceding action,
screenshot timestamp, stable entry ID where known, and observed problem.
Review wording and cosmetic issues together after the section. Crashes, broken
events and progression blockers warrant immediate investigation.

The English suggestions below are editorial drafts, not verified replacements
that fit the current byte or display limits. No disk rebuild accompanies these
notes.

## Open issues — 2026-09-20

### Karu at the starting house — `051000:010`

- Screenshot: 15.52.42 (kept locally).
- Current wording: “SION, / PULSE, SWEAT / ABOVE NORMAL. / PLOTTING?”
- Report: awkward formatting and fragmented English make the question unclear.
  Review spacing and line breaks in context; the screenshot does not establish
  clipping.
- Source meaning: Sion's heart rate and perspiration are higher than usual;
  Karu asks whether he is plotting something.
- Editorial direction: “Sion, your heart rate and perspiration are above normal.
  Are you plotting something?” Preserve the measured, robotic observation
  without reducing the question to an isolated word.
- Status: deferred to the next editorial/layout batch.

### Woman near the starting house — `051000:007`

- Screenshot: 15.53.16 (kept locally).
- Current wording: “MORE GREENERY, / BUT HUGE BUGS / NEAR THE LAKE. /
  IT'S NOT SAFE!”
- Report: the compressed wording loses the connection between her thoughts.
- Source meaning: she welcomes the recent increase in greenery, but hears that
  many large insects are breeding near the lake and that it is dangerous there.
  The line does not explicitly say bushes cause monsters to appear.
- Editorial direction: “It's nice to see so much more greenery lately, but I
  hear large insects are breeding near the lake. It's dangerous out there.”
- Status: deferred to the next editorial/layout batch.

## Area draft build — 2026-09-20

The optional `--include-area` build adds 19 entries from the starting bank,
including Shoko's invitation, accept/refuse/reconsider branches, her handgun
conversation, town warnings, rest dialogue and selected later responses. This
is partial area coverage, not a complete town or next-area translation. Boot
with the new Opening disk as well as using the new System disk: UI edits live
on both. Existing play sessions and their disk images remain separate.

The field menu now uses STAT / ITEM / PLAN / EQP / ABIL / SYS. The System menu
uses SAVE / LOAD / TEXT / FORMAT (the original User Disk formatting operation).
Text speed uses FAST / NORM / SLOW. Abbreviations accommodate fixed storage;
fuller labels are a later UI improvement. Inventory-empty, no-equipment and
no-abilities messages are drafted. Equipment names such as Shirt, save/load
prompts, tactics screens and other submenus remain Japanese.

All new text is awaiting in-game review. Check menu selection/highlighting and
returning to the field, both answers to Shoko's invitation, speaking to her
again after refusing, her joining the party, and conversations with townspeople.
The invitation's yes/no prompt may still be Japanese. Later scenes, including
the main meteor-site event and Karu's subsequent joining scene, remain Japanese.
Record these coverage gaps as well as wording/layout issues during a longer run.

Specific editorial debts in the new temporary drafts:

- `051000:002`: retain Shoko's frustration at being treated as a child at 18.
  The first meteor remark is shortened; review her voice in context.
- `051000:004`: WYURIA and ZOLIAS are provisional spellings. The source
  identifies a kingdom and an empire; the compact draft omits these titles.
- `051000:006`: the source specifically describes radioactive waste near
  Hamack and Gigi made aggressive by mutation at Dust. The draft compresses
  this to pollution and wild mutant Gigi; restore detail when space permits.
- `051000:011`: Shoko says she "borrowed" two guns from her father's drawer.
  The fitting draft says she took two from Dad; restore the euphemism and
  drawer detail in the editorial pass.
- `051000:018`: the elder has lived on Hom for years and has never seen
  anything like this meteor. The draft retains the northern canyon location
  and surprise but omits Hom and the explicit length of residence.

Shoko's short/full-name IDs both display SHOKO for now, matching the existing
prototype convention. Preserve her full name in future glossary work. Earlier
Karu and lake-warning wording issues remain open.

## Playthrough screenshots 17:53–17:58 — 2026-09-20

Reviewed all 13 supplied Desktop screenshots; images stay local. The player
reports leaving town and approaching the cave. The field screenshots show
Shoko in the party and a completed battle. This demonstrates progress on the
accepted-invitation path, not coverage of every branch.

| Time | Observation / follow-up |
| --- | --- |
| 17.53.01 | Entry `051000:018` fits the box. Its inherited elderly-man speaker label remains Japanese (`051000:005`). Include that header in the next batch. |
| 17.53.54 | The second page of `051000:006` fits; wording/detail debts remain as recorded above. |
| 17.54.03 | The two-line HAND MEDICAL pickup fits, with FOUND on the second line. HAND is yellow but MEDICAL is white: investigate colour state across newlines before claiming item highlighting is preserved. Item name remains provisional. |
| 17.54.32 | Untranslated refusal: “I can't just take someone else's things.” Known shared helper `061000:021`; queue for translation. |
| 17.54.50 | Shoko's invitation and name render within the box. Choice labels remain Japanese: top Yes, bottom No. |
| 17.55.02 | Sion's canyon/Gigi reply fits. The choice window is still visible after accepting; establish whether this is original behaviour before treating it as a patch defect. |
| 17.56.02 | Inventory names remain Japanese: Hand Medical and Handgun. Pickup labels and inventory labels are separate coverage. |
| 17.56.17 | All six English field-menu rows are visible and PLAN is highlighted. Multiple underlying windows remain visible; investigate only if the user reports failed dismissal or persistent corruption. |
| 17.56.21 | PLAN opens “Talk” / “Change formation.” Prefer PARTY as the eventual parent label; current PLAN is too vague for this field submenu. |
| 17.56.38 | Character selection heading means “Whose?” (contextual English could be “Who?”). SION and SHOKO display correctly here. |
| 17.56.48 | Same selection view, but SHOKO's first glyph appears partly overwritten compared with 17.56.38. Record as a possible redraw issue; cause and reproducibility unconfirmed. |
| 17.57.21 | Battle menu remains Japanese: Attack / Special Abilities / Items / Equipment / Status / Retreat. Distinct from the translated field menu. |
| 17.58.03 | Battle-result text remains Japanese. It lists 2 experience, 4 credits, 0 scrap; preserve numeric substitutions and colours when translating. |

Next coverage priorities from this run: Yes/No, party/formation and character
selection labels, inventory names, shared pickup refusals, battle menu/results,
and the cave/meteor story sequence. No disk rebuild accompanies this review;
continue collecting context through the longer playthrough.

## Canyon, level-up and defeat screenshots 18:00–18:06 — 2026-09-20

Reviewed all eight supplied Desktop screenshots; images stay local. The player
reports that the last screen appeared after dying. No new disk build is made
for this review.

| Time | Observation / translation |
| --- | --- |
| 18.00.58 | Location title: Planet Hom. Add the shared location-title string to coverage. |
| 18.01.01 | Location title: Saxen Canyon (current provisional romanization). This identifies the next area reached. |
| 18.02.16 | Level up, Sion: PP +6, MP +3, IQ +3. Name substitution renders in English; heading, Japanese particle after the name, and “points” suffixes remain Japanese. |
| 18.02.20 | Sion continuation: R.Str +1, L.Str +10, Agl +7, Drb +4. Closing text means “Stats increased.” Preserve the separate numeric fields and page break. |
| 18.02.25 | Only the Level Up heading is visible. May be a transitional frame before the next character's text; a still image does not establish a missing-text defect. |
| 18.02.31 | Level up, Shoko: PP +8, MP +2, IQ +5. Her English name renders correctly in this context. |
| 18.02.35 | Shoko continuation: R.Str +4, L.Str +0, Agl +2, Drb +3; “Stats increased.” Zero gains can be displayed and must remain valid in the translation. |
| 18.06.09 | Post-defeat load prompt: “Loading data. Insert the User Disk into drive 2, then press any key.” This is a disk request, not evidence of an emulator crash. The screenshot does not establish whether a saved game exists. |

Next coverage additions: location names, complete multi-page level-up messages,
and save/load/disk-swap prompts. Dynamic stats and shared name substitutions
must remain intact. A player at the last prompt should place the current build's
User Disk in FDD2, retaining System in FDD1, and follow subsequent prompts.

## Screenshot-review build — 2026-09-20

`--include-review` includes the previous area draft and addresses the observed
coverage gaps in a separate build. New strings await runtime verification.

- Field menu: PARTY replaces PLAN; BAG replaces ITEM to recover the required
  storage. PARTY opens TALK / ROW (change formation). Character selection says
  WHO?; formation screens use ORDER / REORDER / NEW ORDER.
- Choice prompt: Y / N. Battle menu: ATTACK / ABIL / ITEM / EQP / STAT / FLEE.
- Save/load prompts name the User Disk and drive 2; the completion prompt
  requests Data Disk in drive 2. These preserve the original three-line format.
- Inventory names: KNIFE, GUN and MEDS. KNIFE and MEDS pickup messages now use
  the same short labels on one line, avoiding the observed newline colour reset.
  These are temporary abbreviated names, not a final item glossary. Other
  equipment names, including Shirt and Protector, remain Japanese.
- Location labels: HOM and SAXEN, abbreviated to the current storage limits.
- Elderly-man header: ELDER. The shared item refusal now reads
  “NOT MINE. / CAN'T TAKE IT”.
- Shared battle-result and level-up text is translated. Existing stat labels,
  numeric values, colour commands, name substitutions and page waits remain.
  Fixed-width text replacements leave every runtime field at its original
  byte position; display remains to be checked in the emulator.

The possible Shoko redraw issue remains unconfirmed. Karu/lake-warning editorial
debts, later cave/meteor events, additional abilities and other UI remain open.
This build does not attempt to resolve those by shortening meaning further.

Local launcher: `work/Launch Reviewed Draft.command`; disks are in
`work/review-draft-test`. Boot its Opening disk and use its System/Data disks
when prompted. A snapshot of the prior area's on-disk User Disk was copied to
this new folder without changing the source. At snapshot time it was identical
to the original supplied User Disk; this does not establish a saved game.
No live emulator state was transferred or restarted.

## Meteor-site playthrough — 2026-09-21, 13:11–13:27

Reviewed all 16 Desktop screenshots for today plus the attached 13.27.09 image.
Player reached the meteor-site cinematic and aftermath, then reported difficulty
returning with Sion at 7 PP and Shoko at 6 PP. No new build accompanies review.

- 13.11.14: GUN renders in equipment selection; Shirt remains Japanese.
- 13.13.33: confirmed ATTACK overlaps/clips the battle-menu right border.
  Generic 14-column UI validation is insufficient for this narrower menu.
  Next patch should use a measured per-menu limit (candidate ATK) or widen it.
- 13.17.15: KNIFE renders; action submenu still says Use / Discard in Japanese.
  These actions need priority translation because they affect item use.
- 13.19.02: untranslated meteor-site arrival, `051000:029`.
- 13.19.09: requests Opening Disk in drive 2; this event-specific prompt is
  separate from the translated save/load prompts.
- 13.19.49 and 13.19.52: cinematic narration begins with Sion and Shoko hiding
  behind rocks to observe the scene; partial captures while text is appearing.
- 13.20.00: narration describes an unidentified spaceship alongside the
  expedition's jet hovercraft. This uses the separate cinematic text path.
- 13.20.05: Shoko asks what the ship is and whether it belongs to the Federation
  military. Speaker label and dialogue remain Japanese in this renderer.
- 13.24.34: requests Data Disk in drive 2 after the cinematic.
- 13.25.00, .05 and .09: untranslated Jido/Sion aftermath, `051000:030`;
  English shared names already substitute inside Japanese dialogue.
- 13.25.27: interaction reports no reply.
- 13.25.46: Zolias soldier gives a confused, halting response; untranslated.
- 13.25.54: meteor is emitting white smoke at the bottom of a huge crater.
- Attached 13.27.09: GUN and KNIFE display in the status panel, Shirt remains
  Japanese. Stacked menus obscure underlying panels; this alone does not prove
  failed redraw or corruption. Both party members are critically low on PP.

Recovery research: the local PC-98 script explicitly contains the elder's Camp
Kit gift (`051000:017`, reached conditionally through `051000:005`) and Lucia's
early rest conversation (`051000:014`). Availability depends on story flags;
do not promise Lucia remains available after the meteor event. A Cosma medicine
shop has not been established. Guides for other ports describe the Camp Kit
as party recovery, but their exact mechanics/timing must not be assumed for
this build. Healing ability availability at Shoko's current stats is unverified.

## Wider menu test prepared — 2026-09-21

A separate `--widen-menus` build increases the normal field and on-foot battle
menu interiors from five to six full-width cells, with matching selection
highlights. The alternate field-menu record also widens because it shares the
highlight code. Exactly five bytes differ from the reviewed build; text and
menu action order are unchanged. ATTACK should now fit, pending runtime review.

Local launcher: `work/Launch Wide Menu Test.command`. Boot the new Opening disk,
then mount this build's System/Data disks at the prompt. Existing sessions are
not restarted. The reviewed build's on-disk User Disk was copied into the new
folder as a snapshot; this is not a transfer of unsaved live progress.

On the next test, check ATTACK fully inside its border, the highlight across
all six battle rows, normal field-menu navigation, entering/leaving submenus,
and returning to the map after cancellation. Capture any leftover borders or
highlight fragments. No claim of a redraw fix is made before this comparison.

## Wider menu and recovery follow-up — 2026-09-21, 13:40–14:03

Reviewed five new Desktop screenshots. No disk rebuild accompanies this review.

- 13.40.26: opening handoff still requests System Disk in drive 1 and Data Disk
  in drive 2, followed by any key. This prompt remains Japanese.
- 13.43.53: ATTACK now fits fully inside the battle-menu border. Its selected
  row highlight is aligned with the widened menu. All six labels are visible.
  This verifies this battle-menu state, not every highlight row or cancellation
  redraw; normal field-menu width remains only partially visible in this batch.
- 13.54.09: Camp Kit is present in the inventory, with its tent icon and
  untranslated Japanese item name.
- 13.54.20: inventory contains MEDS and Camp Kit; Use / Discard still needs
  translation. The WHO? target selector shows Sion and Shoko, with Shoko
  selected. The still does not establish which item is being used or its effect.
  Overlapping open windows alone are not evidence of a redraw bug.
- 14.03.38: untranslated Karu greeting: “Welcome back, Sion. Hello, Shoko.”
  Shared English names render within the Japanese dialogue. Match this return
  visit against the script before choosing the next translation target.

Player reports that reaching level 2 outside town helped, and that the elder
provided camping gear after leaving and re-entering town. Record this as an
observed successful sequence, not proof that re-entry alone unlocks the gift,
that level 2 is required, or that the gift can be obtained repeatedly. Exact
Camp Kit recovery, consumption and replenishment behavior remain unverified.

## Expanded menu labels prepared — 2026-09-21

`--expand-menu-labels` implies the wider-menu and reviewed translation builds.
It relocates six menu strings into a guarded resident-driver pool, preserving
row order, box position and action dispatch. Field/battle menus use the tested
six-cell geometry; the other affected boxes already accommodate these labels.

- Field: STATUS / ITEMS / PARTY / EQUIP / SKILLS / SYSTEM.
- Alternate field: DATA followed by the same six rows.
- Battle: ATTACK / SKILLS / ITEMS / EQUIP / STATUS / FLEE.
- Choice: YES / NO, replacing Y / N.
- System heading: SYSTEM; text speed: NORMAL instead of NORM.

Other item names and Use / Discard are unchanged. Local launcher:
`work/Launch Full Menu Test.command`, images in `work/full-menu-test`.
Use its Opening and System disks on the next restart. Existing sessions and
prior builds are untouched. Runtime checks needed: both YES and NO choices,
each field/battle highlight, submenu navigation/cancellation, and labels after
the Opening-to-System handoff. This is a text-relocation experiment, not a
claim that arbitrary unused-looking disk bytes are safe storage.

## Canonical-derived adaptation batch 01 — 2026-09-22

Seven entries across four reviewed sections now have separately authored,
validated adaptations: canyon directions (009), Lucia rest/suspicion (014/015),
work/inventory interactions (024–026), and the dead-Gigi exchange (028), all in
bank 051000. Full canonical wording is unchanged. The adaptation pack records
omissions, such as the inventory-full observation being implicit in the polite
request to make room, and Shoko's disgust expressed by “Ugh!” rather than an
additional “creepy.” Natural English and the important interaction remain.

Local launcher: `work/Launch Editorial Batch 01.command`; disk folder:
`work/editorial-batch-01-test`. Boot that Opening disk and use its System/Data
disks. Fifty tests pass; IPS roundtrips pass. Relative to the expanded-menu build,
253 changed bytes are confined to the seven selected allocations; Opening is
identical. Commands, name references, branch payloads, pointer tables, opaque
tails and image sizes retain the existing importer's checks.

The manifest lists 69 reviewed units as deferred, including the opening, Karu
and lake warning, and pending UI/name work. Their existing game text remains
provisional. This is not a claim that the full editorial review now fits.

Check the seven interactions when their story states are reachable. In particular,
verify Lucia's post-rest farewell, the suspicion branch, the highlighted/name
boundaries in Shoko's corpse reaction, and dismissal/return to movement. None has
been marked runtime-verified. Existing sessions were not restarted.

The copied User Disk comes from `full-menu-test`; at preparation time it is
identical to the supplied original and contains no verified personal save.
Live emulator state is not transferred. Use a separately saved current User Disk
if continuing personal progress rather than starting a new playtest.

## Expanded-menu and item coverage feedback — 2026-09-22, 19:03–19:12

Reviewed the five named Desktop screenshots. No rebuild or emulator operation
accompanies this review; the player is continuing through the canyon.

- 19.03.53: YES and NO render fully inside the choice box during Shoko's
  invitation/acceptance interaction. Player confirms the display looks good.
  The still does not verify both branch outcomes or every selection highlight.
- 19.04.13: STATUS / ITEMS / PARTY / EQUIP / SKILLS / SYSTEM all fit within the
  expanded field menu. EQUIP's highlight stays aligned with the interior width.
  Player confirms the menu looks good. Other rows' selected states and all
  submenu dismissal paths are not established by this one frame.
- 19.08.02: selecting FORMAT opens an untranslated User Disk creation prompt:
  it asks for a blank disk in drive 2, followed by any key. This is disk
  initialization, not ordinary saving. Opening 0x421c is the three-line prompt;
  0x4268 contains another related creation message. Review the whole formatting
  interaction, including completion/error/cancellation, before translating it.
  The already-reviewed canonical menu label is Format User Disk, while the
  in-game label still says FORMAT. No successful format or save is inferred.
- 19.11.53: the untranslated inventory entry is Camp Kit, alongside MEDS. Its
  compact shared label is at System 0x10cb0. The elder's translated gift text
  and this inventory name use separate storage; translating one did not cover
  the other. This screenshot does not establish the kit's recovery mechanics.
- 19.12.00: the untranslated equipped garment is Shirt, at System 0x10a99.
  GUN and KNIFE remain readable, and the helmet slot is empty. Shirt's current
  source name uses three half-width bytes; full-width SHIRT cannot simply be
  substituted in place. Preserve canonical wording and investigate allocation
  or pointer handling when this item-name batch is adapted.

The player reports that conversations generally flow better and feel more
consistent. Record this as overall editorial feedback, not per-entry runtime
approval for every line in batch 01. Next coverage priorities are the complete
formatting interaction and remaining inventory/equipment names, retaining the
canonical/context-review/adaptation workflow. Canyon feedback is still pending.

## Location-label consistency feedback — 2026-09-22

Player noticed the difference between Saxen Canyon in dialogue and the short
area label, and questioned Hom on the world map. Checked original System text:
0x11723 names the canyon explicitly; 0x11329 explicitly says Planet Hom.
The current patch inserts SAXEN (not SAXON) and HOM, both storage-driven
abbreviations. Canonical context should remain Saxen Canyon and Planet Hom.
The glossary already marks the Latin spellings provisional; no official spelling
has been established by this check. Do not silently change Hom to Home or Saxen
to Saxon. Restore the geographic qualifiers through the location-label fitting
adapter, keeping the name consistent across dialogue, glossary and map headers.
