# R07 independent frozen-candidate audit

**PASS — static release candidate**, `work/r07-01-xp4`.
The candidate contains878 required/adapted records across88 scenes, adding57
reviewed records to R06. The route ends after Byuto's mine victory and immediate
follow-ups, before reporting to Roy again. This approval does not claim runtime
route traversal.

QA captured181 production, catalog and test-file hashes after the manager, RE
and localizer acknowledged the input freeze. All eight R07 packs matched the
independently reviewed editorial snapshot. No frozen file changed during the
build or audit. Handoff documents, launcher configuration and isolated boot
artifacts are outside that production snapshot.

Independent verification passed:

- Strict release assessment: candidate-ready, no blockers or deferred scenes.
- Original-source route inventory:319 entries,273 text-bearing dependencies;
  an independently written command traversal matched the production closure.
- Recompiled878 records into1193 declared patch ranges; every candidate range
  matched the independently compiled image.
- All821 R06 canonical texts and in-game adaptations remained identical.
- All six image sizes and manifest hashes matched. Both IPS files replayed
  exactly from original images; Data, Ending, User and Visual remained original.
- Opening is byte-identical to R06. All3854 changed System bytes relative to R06
  lie within declared compilation ranges.
- XP4 code and trainer metadata, progression table, equipment stat rows and
  resident growth data remained intact. All280 equipment name pointers resolved
  to their cumulative English labels; R05/R06/R07 label aliases matched their
  guarded encodings.
- The manager's fresh81-pack replay report records an exact catalog match;
  its document fingerprint agrees with the audited candidate manifest.

| Artifact | SHA-256 |
| --- | --- |
| Frozen catalog file | `f3191af471e4363c1a323110c8e4925b1ac18c0ad522279d3e057d7db0024dc2` |
| Opening image | `623895c1024191069aee4792de1e1719e5b1cd8efe8e0606da0d816e061ad89b` |
| System image | `56d8bc28c56bfdb932e6bf17de4991f31d5725ae885d90dc14eb79d9f5d3d319` |

Machine-readable evidence remains ignored in `work/r07-qa-frozen-inputs.json`,
`work/r07-qa-approved-packs.json`, `work/r07-qa-frozen-audit.json` and
`work/r07-replay-verification.json`. Source and editorial findings are recorded
in [source inventory](r07-qa-source-inventory.md) and
[editorial review](r07-qa-editorial.md).

Actual Byuto traversal, battle/warp behavior and visual pacing remain pending.
The manager ran an isolated copied-disk boot for1800 frames with exit0. QA
reviewed its report and screenshot, which displays “RIGHT STUFF Presents.”
All six smoke-copy hashes match the audited candidate, and the report records
no disk writes. This establishes startup only. The full test log records186
passing tests, including the native JIT checks; see ignored
`work/r07-test-output.txt` and `work/r07-final-smoke/boot-result.json`.
