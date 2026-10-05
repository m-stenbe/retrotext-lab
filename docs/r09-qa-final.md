# R09 independent frozen-candidate audit

**PASS — static release candidate**, `work/r09-01-xp4`, October 5, 2026.
The cumulative candidate contains **1,064 adapted records in 107 scenes**,
adding 29 script records and the Daina map label while preserving all 1,034
earlier canonical texts and in-game adaptations. The section covers Daina's
reunion/escape and the Begi historian through the emblem and Stea lead.
Runtime route traversal remains pending.

All writers acknowledged the freeze before QA recorded production/test inputs.
The final catalog and release plan were added after replay and issue closure,
giving **206 frozen inputs**. Their hashes remained unchanged throughout the
independent compilation, build comparison and audit. Handoff documentation,
launchers and startup-smoke artifacts are outside this production snapshot.

Independent checks passed:

- Fresh 95-pack replay supplies the final catalog; source/editorial validation
  and the strict complete-section gate pass with no blockers. Manifest plan,
  catalog and bible fingerprints match the frozen inputs.
- Independently decoded closure contains 546 entries and 453 text dependencies,
  including all 29 new script records and the restored historian item branch.
- Independent cumulative compilation produces 1,064 records and 1,386 declared
  patch ranges. Every candidate range matches that compilation.
- Both IPS patches replay exactly from original disks. All six image sizes and
  manifest hashes match; Data, Ending, User and Visual remain original.
- Opening is identical to R08. All 5,635 changed System bytes relative to R08
  fall within declared cumulative compiler ranges.
- All 1,034 earlier canonical texts and fitted adaptations remain identical.
- XP4 code and metadata, progression tables, equipment statistics and Lucia's
  resident profile remain unchanged. All 280 equipment-name pointers and the
  guarded R05–R09 name aliases resolve to approved English encodings.
- All **202 regression tests pass**, including native renderer/trainer checks.
  The new historian header accepts its original source shape and rejects
  modified controls; the colored title call still rejects continuation pages.
- Public-file hygiene found no game images, screenshots or full source catalogs
  among the files prepared for publication. The getting-started instructions
  match current replay/build arguments and manifest fields.

| Artifact | SHA-256 |
| --- | --- |
| Frozen catalog file | `3fd1b76ea82223799d921d38715c830d2f646f26f28e39efe854793e182517c1` |
| Opening image | `623895c1024191069aee4792de1e1719e5b1cd8efe8e0606da0d816e061ad89b` |
| System image | `cce15db7f44caf317b20248331decdee1b976f4d9b4dfa3d5e7342a3b52b4c26` |

Ignored evidence is under `work/qa-pr-20261005/`: `r09-frozen-inputs.json`,
`r09-frozen-audit.json`, `r09-compiled-changes.json`, `r09-tests-native.log`,
`r09-independent-closure.json` and `r09-vehicle-route.json`.
See the [source inventory](r09-qa-source-inventory.md),
[editorial QA](r09-qa-editorial.md) and
[earlier-batch reproduction audit](pr-backlog-qa.md).

This approval supports committing and opening a PR before player testing.
Actual vehicle boarding, shore collision, event animations, recruitment,
inventory-full alternatives, display pacing and full route transitions still
require runtime verification.

## Isolated startup check

The final candidate ran for 1,800 frames in a separate emulator configuration
with copied disks, audio/network commands disabled and separate save/state paths.
The approved GUI run exited 0. RE inspected the screenshot: it shows the
RIGHT STUFF Presents startup logo. All six copied disk hashes remained unchanged;
the System image matches the audited hash above. The initial sandboxed GUI
attempt aborted before logging; the normal approved retry succeeded.

Evidence remains in `work/r09-final-smoke/boot-result.json` and
`work/r09-final-smoke/screenshots/boot.png` (screenshot SHA-256
`55712720005b1223033e703afec123fe45acb10f1d8cb774d2eb54c589fcdab7`).
This verifies startup only, not the Daina route or other gameplay transitions.
