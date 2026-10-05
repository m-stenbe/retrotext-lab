# Translate ahead; verify complete playable sections

The player should receive a substantially translated route and verify its English,
display and behavior. Source discovery, missing-text detection and ordinary scope
completion are project work. Screenshots are useful defect evidence, not the primary
translation queue. A successful build of a few scenes does not establish that the
route connecting them is translated.

## Roles and handoffs

| Role | Owns | Delivers |
| --- | --- | --- |
| Manager / integrator | Release boundary, game-state map, bible, issue queue, integration and handoff | Frozen work packets, reviewed integration, cumulative candidate and launch command |
| RE | Source discovery, triggers, pointers, formats, call dependencies, renderer/fitting support | Proven source/context packets, adapter changes with preservation evidence, explicit unknowns |
| Localizer | Complete connected scenes and alternatives | Natural canonical English, editorial review, terminology proposals, separate adaptations with omission notes |
| QA | Independent scope and change review | Inventory comparison, source/layout/roundtrip results, transition/smoke evidence and defects |

These are responsibilities, not different trust levels. No role bypasses the
session's filesystem/network permissions. The manager does not need to run outside
the sandbox. Git publishing remains subject to the user's authorization; a diagram
is not standing permission to push. Current agents share a workspace: use disjoint
file ownership or isolated checkouts for implementation. Workers submit proposals
for shared bible/plan changes; the manager integrates them and runs impact checks.
QA reviews a specific catalog/diff snapshot and does not approve its own edits.
Completed batches can be committed and opened as PRs after applicable automated
validation, before player testing. PRs must state their exact translated boundary,
validation evidence and pending runtime checks. Player testing gates claims of
runtime verification, not code review. A passing candidate gate does not change
that distinction, and PR publication still requires user authorization.
Before final QA records pack hashes, the manager freezes the inputs and receives
acknowledgment from every writer. Any later edit requires a reviewed diff and new
fingerprints; a completed build alone does not prove it used the approved packs.

Use parallel agents for substantial sections, not for every small repair. RE can
map the next dependency while localization handles proven scenes and QA checks a
previous completed packet. A localizer need not wait for an entire game decoder.
Do not translate disconnected lines simply because their allocations are easy.

## Section cycle

1. Define entry/exit story conditions and the optional interactions available in
   that interval. Inventory route triggers, choices/repeats, shared calls,
   cinematics, gameplay UI, save/load/disk prompts, names/items and location labels.
   Record unexplored paths as blockers. Bank adjacency is not chronology.
2. RE gathers complete source packets with evidence and unknowns. Manager assigns
   stable scene/record IDs, explicit owners and dependencies. Batch by connected
   scenes, not an arbitrary string count; assess effort with turns/pages as well.
3. Localizer translates and reviews whole scenes, then adapts from canonical English.
   Missing space becomes an engineering/fitting task, not silent degradation.
   Keep the existing localization workflow, provenance and command protections.
4. Manager integrates packets; QA checks the entire promised section against the
   inventory, including untranslated and unmapped paths. Partial packets may produce
   internal experimental builds but do not redefine the promised section.
5. Run the strict section gate, build cumulative images, verify preservation and
   applicable tests, and perform reproducible boot/transition checks where tooling
   permits. Record unavailable runtime checks honestly. Produce a candidate with
   one launcher, a start/save-state instruction, exact route boundary, known issues
   and a short branch verification sheet. Do not change a live emulator's disks.
6. Player verifies translated content: naturalness, names, wrapping, choices,
   movement and story transitions. Unexpected Japanese inside the promised route
   is a release defect. Meanwhile prepare the next substantial section; do not
   wait for screenshots to decide what to translate next.

Manager review closes the loop before handoff. Close an issue or mark an inventory
domain mapped only with evidence; shrinking scope to get a green result is not a
fix. Scope changes must be explicit. Experimental builds remain available when
requested, with their partial status stated.

## Current release queue

**R01: fresh boot / Cosma opening → complete meteor event → return to Cosma and
Karu joining.** Includes the intervening cinematic and required gameplay surfaces.
The machine-readable plan is `profiles/alshark/release-opening-cosma.json`.

The first implementation pass has a cumulative **138 adapted records in 33
scenes**, including the complete 74-span meteor cinematic, 21 newly adapted town
and pickup records, 18 additional interface messages and 17 equipment/ability
name records. Existing UI, results and shared names now have explicit reviewed
adaptations. Already translated Dust/Hamack material remains included as bonus
content; that route is not yet complete.

The localizer resolved the two fitting blockers with explicit continuation pages.
RE added guarded cinematic, resident UI and coordinated name adapters. Independent
QA found and corrected ability-field overflow, an incorrect inability message and
missing separation before a learned ability. Fifteen source-backed terminology
entries have been added. All versioned packs replay from original images.

The final R01 source inventory is mapped and the candidate gate passes. Runtime
route validation remains pending. The machine-readable plan remains authoritative
for discovery blockers. Compiled
record counts do not close map-object or combat-flow coverage by themselves. See
[r01-first-pass.md](r01-first-pass.md) for the runnable build and validation evidence.

**R02: Dust / Joe encounter → early Hamack information gathering.** The
source-mapped cumulative candidate now contains 266 adapted records in 44 scenes,
including the 143-entry static route closure, 21 new names and three Joe UI
strings. The boundary ends at the spaceport/Mars lead, before departure. See
[R02 handoff](r02-dust-hamack.md) for the launcher, exclusions and verification
sheet. Runtime traversal remains pending. Next discovery should cover the
spaceport/Mars route as a connected section.


**R03: Hom Spaceport → abandoned mine → first controllable Atraia bridge.**
The cumulative candidate has 550 adapted records in 54 scenes: 37 new story
records, 24 menu/service messages, three map labels and 220 equipment names.
Bridge service menus are reachable before the next cockpit trigger, so their
full potential development-name list is included. See [R03 handoff](r03-spaceport.md).
Next source mapping should begin with `083000:000 → 054000:032`, the cockpit
rescue/distress event, and follow its connected route rather than assuming Mars
is immediately next.

**R04: cockpit distress call → civilian-ship rescue → CS station first briefing.**
The cumulative candidate contains 595 adapted records in 61 scenes, adding41
dialogue records and four name/location records. Recruitment, the complete tour,
both acronym-answer branches, conditional party dialogue and station follow-ups
are included. The endpoint is before walking off CS station; the border targets
map9 surface, so neither flight nor the Zajil mission is promised. See the
[R04 handoff](r04-rescue-station.md) and `release-rescue-station.json`. Next mapping
starts from station departure after briefing flag16. Runtime traversal remains
pending.

**R05: CS Station departure → Zajil surface → Saibal investigation and kidnapping.**
The cumulative candidate contains 701 adapted records in 72 scenes, retaining the
596-record September 24 baseline. Initial optional Porkin and Zajil Spaceport
interactions are included, with shop alternatives, two guard fights, seven new
map/ability labels, bar, exchange instructions and party responses. The endpoint
is before pursuing Tomyu at Porkin; bus destination exploration and spaceflight
are excluded. See [R05 handoff](r05-zajil.md) and
`profiles/alshark/release-station-departure.json`. Next mapping begins with
Porkin object 014 after the kidnapping enables visibility 43/44. Runtime route
verification remains pending.

**R06: Porkin pursuit → flight → military-station rescue.**
The cumulative candidate contains 821 adapted records in 79 scenes, retaining
all 701 R05 records. Includes town aftermath, rescue and reunion, immediate
station/party follow-ups, flight controls and destination labels. Optional return
to CS Station is covered up to, but not including, reporting to Roy for the next
assignment. Other planets' landing labels do not promise exploration there.
See [R06 handoff](r06-porkin-rescue.md) and
`profiles/alshark/release-porkin-pursuit.json`. Next mapping begins with Roy's
post-rescue branch `05c000:025`. Runtime route verification remains pending.

**R07: Roy post-rescue assignment → Byuto / Kainan → mine victory and aftermath.**
The cumulative candidate contains 878 adapted records in 88 scenes, retaining
all 821 R06 records. Includes engine grant/refusal/repeat, warp travel, Kainan
shops and optional bar, Ray Ball gift, mine passages/ambush/boss, town and party
follow-ups, and three map labels. Stop before Roy's next report after victory.
See [R07 handoff](r07-byuto-mine.md) and
`profiles/alshark/release-byuto-mine.json`. Next mapping begins with
`05c000:027` and its connected debrief/leave route. Runtime traversal remains
pending.

**R08: post-Byuto debrief / leave → Mars mainland → Lucia video letter.**
The cumulative candidate contains 1,034 adapted records in 101 scenes, retaining
all 878 R07 records. Includes station transport, Mars Spaceport, all Teswil
shops/hotels/buildings and both bar rooms, optional mainland Begi, used Jet
Hovercraft purchase and video-letter receipt/playback through party TALK.
Stop before crossing the sea to Daina. See [R08 handoff](r08-mars-leave.md) and
`profiles/alshark/release-mars-leave.json`. Next mapping follows the Daina
memorial/reunion lead across the sea, including the vehicle route. Runtime
traversal remains pending.

**R09: Daina sea crossing → memorial reunion/escape → Begi historian.**
The cumulative candidate contains 1,064 adapted records in 107 scenes, retaining
all 1,034 R08 records. Includes Daina services/residents, the complete reunion and
ambush, Lucia's recruitment-related dialogue, Begi encyclopedia/history/emblem
sequence, inventory-full and repeat alternatives, changed station-return response
and post-historian party TALK. Stop before departure to Stea. Independent source
mapping covers 546 entries and proves a static hovercraft route across water;
exact movement and event playback remain runtime checks. See the
[R09 handoff](r09-daina-begi.md) and `profiles/alshark/release-daina-begi.json`.
Next mapping follows the Stea/Myuntos lead, including transport and connected
optional interactions. Runtime traversal remains pending.

## Enforced candidate gate

`release_tool.py` checks source hashes and current editorial/fitting state and
reports whole-section readiness:

```sh
python3 profiles/alshark/release_tool.py ../alshark/original work/r01-final-catalog.json \
  --plan profiles/alshark/release-opening-cosma.json
```

Exit 0 means candidate-ready, 2 means known blockers, 1 means invalid input/check
failure. R01 now has 33 technically ready scenes and no deferred adapted scenes;
discovery blockers are reported separately from technical readiness. JSON output can be saved under
ignored `work/`; it contains no full source script.

Build the current gated R01 candidate from its final catalog:

```sh
python3 profiles/alshark/build_demo.py ../alshark/original --output work/r01-candidate \
  --localization work/r01-final-catalog.json \
  --release-plan profiles/alshark/release-opening-cosma.json \
  --expand-menu-labels --translate-disk-prompts --exp-multiplier 4
```

The builder checks the gate before creating output. It requires the entire planned
scene set, all required records, five inventory domains with evidence, no open
issues, current source/editorial checks and combined technical compilation. It
rejects conflicting subset selections. The manifest records scope/catalog/bible
fingerprints and identifies a `section_candidate`; runtime verification remains
false until independently demonstrated. Builds without a release plan are marked
`experimental`. This gate checks the declared inventory, not unknown game content;
manager/RE/QA evidence remains essential to discovery completeness.

## Progress that reflects useful work

Report each section's discovery status, required records/scenes, reviewed canonical
work, adapted work, engineering blockers, and tested branches separately. Snapshot
and fingerprint the plan/catalog at handoff. Catalog records
include control-only entries and exclude undiscovered text; percentages of them
are not percentages of the whole game or a useful schedule estimate. Large
multi-turn entries also take more work than single labels.
See [translation progress](progress.md) for current counts and explicit denominators.

The intended milestone is a playable translated section, followed by the next
section—not another launcher for a handful of screenshot lines.
