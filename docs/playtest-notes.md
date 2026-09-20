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
