# Meteor arrival and aftermath: batch 04

The playable batch translates four script entries: arrival (051000:029),
Jido's final conversation (051000:030), Sion and Shoko's continuation
(053000:000), and the no-reply repeat interaction (053000:013).
The cumulative build selects 27 canonical-derived entries in 14 scenes.
The Opening cinematic remains Japanese; its separate animation/text interpreter
is not covered by the System script adapter. This is not full meteor-event
in-game coverage.

English canonical text and contextual review are in `editorial-meteor.json`;
separately fitted adaptations are in `adaptations-batch-04.json`. The previous
review/adaptation packs replay unchanged. New bible evidence lives in a separate
story term, leaving previous fingerprints intact. The source-supported reading
of Jido's broken final speech is that the soldiers were pursuing someone who
came in the meteor; neither Alshark's identity nor nature is asserted.

## Engineering and validation

The four entries alone are added to the editable allowlist. Arrival retains its
cinematic/event commands. The delay control `!` is now accepted for layout:
System 0xF353 delays for 60 ticks and resumes; it does not reset the cursor.
The earlier format research already documents this handler.

The aftermath's flag-4 branch targets entry 33. That control-only dispatcher
remains read-only and calls bank 2, entry 13 (053000:013). The first-time path
calls bank 2, entry 0 (053000:000). The existing #P handler research establishes
bank/index lookup and cursor continuity. Layout validation now composes exactly
these two reviewed calls, requires adapted callees in the selected build, and
retains cursor state across call/return. Other shared calls still fail closed.
The actual importer still writes each entry separately in its original allocation.
No branch, command, name reference, pointer, wait, clear or opaque tail is edited.

Validation: 69 tests run, 67 pass and 2 optional-emulator tests skip. New synthetic
tests cover cursor continuity, callee clears, waits/delays, unselected/unknown
callees and preservation of event commands. Full original import is byte-identical;
IPS roundtrips pass. All 958 changed System bytes relative to build 05 are inside
these four allocations; Opening is identical. All decoded immutable tokens in
the new entries match the original. Runtime display and branch playtesting remain
pending.

## Build and play

Local output: `work/meteor-english-06-xp4-test/`.
Launcher: `work/Launch Meteor English 06 XP4.command`.
It retains expanded menus, corrected disk prompts and 4x EXP.
`work/meteor-english-06-xp4-test/English scene guide.md` includes the canonical
arrival/aftermath script and an English reading translation of the preceding
cinematic, to support continuing a session whose loaded text is still Japanese.

No running emulator or existing save/state is changed. All inspected User Disk
copies match the supplied original, so there is no verified in-game progress save
to transfer. Old emulator states can restore old loaded script text. Use a fresh
boot and an in-game save when available; loading an old state is not proof that
the new dialogue is active. The new build's User Disk is the default disk.

Reproduce by exporting a fresh catalog, then applying these packs in order with
`apply_editorial_review` / `apply_adaptation_pack`:

1. `editorial-review.json`
2. `adaptations-batch-01.json`
3. `adaptations-batch-02.json`
4. `editorial-dust-approach.json`
5. `adaptations-batch-03.json`
6. `editorial-meteor.json`
7. `adaptations-batch-04.json`

Save as `work/adapted-batch-04.json`. Build with the batch-03 scene selection plus
`meteor-arrival meteor-aftermath`, using `--expand-menu-labels
--translate-disk-prompts --exp-multiplier 4`. Validate arrival's color/line flow,
Jido's speaker turns and pauses, transition into Shoko's continuation, return to
movement, then the repeat no-reply interaction.
