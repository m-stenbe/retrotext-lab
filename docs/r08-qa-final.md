# R08 independent frozen-candidate audit

**PASS — static release candidate**, `work/r08-01-xp4`.
The cumulative candidate contains 1,034 required/adapted records across 101
scenes, adding 156 reviewed records to R07. Coverage includes the Mars leave
route, Teswil's shops/interiors/bars, optional mainland Begi, hovercraft purchase,
and Lucia's video letter viewed through party TALK. It stops before crossing
the sea to Daina. This approval does not claim runtime route traversal.

QA captured 196 production, catalog and test-file hashes after all writers
acknowledged the freeze. All ten R08 packs matched the independently reviewed
editorial snapshot, and no frozen file changed during the build or final audit.
Handoff documents, launcher configuration and isolated boot artifacts are outside
that production snapshot.

Independent checks passed:

- The builder's strict release assessment is candidate-ready, with no blockers;
  its plan, catalog and bible fingerprints match the frozen inputs.
- Independent source traversal reproduces 506 entries and 424 text dependencies,
  including both capital bar partitions, all building interiors, Begi and the
  source-proven unavailable encyclopedia branch.
- Recompilation produced 1,034 records and 1,355 declared patch ranges; every
  candidate range matched the independently compiled image.
- All 878 R07 canonical texts and in-game adaptations remain identical.
- All six disk sizes and manifest hashes match. Both IPS files replay exactly
  from original images; Data, Ending, User and Visual remain original.
- Opening is identical to R07. All 9,238 changed System bytes relative to R07
  lie within declared compilation ranges.
- XP4 code and trainer metadata, progression table, equipment stat rows and
  resident growth data remain intact. All 280 equipment name pointers and the
  guarded R05–R08 name aliases resolve to the approved English encodings.
- The fresh 91-pack replay report records an exact catalog match, with the
  same document fingerprint as the candidate. The full test log records 194
  passing tests, including the native JIT checks.

| Artifact | SHA-256 |
| --- | --- |
| Frozen catalog file | `454c402befbf7740ebe422b33f440f644dba8cc5387e46dc4fe0328ec446306e` |
| Opening image | `623895c1024191069aee4792de1e1719e5b1cd8efe8e0606da0d816e061ad89b` |
| System image | `f6afd78dee5dfdd6f4128c4316390f86ff32392ca885b5e55c3f6ac9321b8b64` |

Ignored audit artifacts: `work/r08-qa-frozen-inputs.json`,
`work/r08-qa-approved-packs.json`, `work/r08-qa-frozen-audit.json`,
`work/r08-replay-verification.json` and `work/r08-test-output.txt`.
See also the [source inventory](r08-qa-source-inventory.md) and
[editorial review](r08-qa-editorial.md).

The isolated startup smoke test completed 1,800 frames with exit code 0.
QA reviewed `work/r08-final-smoke/boot-result.json` and its screenshot, which
shows the RIGHT STUFF Presents opening logo. All six copied disks remained
unchanged and match the audited candidate hashes. This verifies startup;
runtime traversal, vehicle behavior and visual pacing remain pending.
