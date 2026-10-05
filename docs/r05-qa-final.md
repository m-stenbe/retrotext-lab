# R05 independent frozen candidate QA

Candidate `work/r05-01-xp4`, catalog `work/r05-final-catalog.json`, and plan
`profiles/alshark/release-station-departure.json` passed independent QA.
The strict gate declares701 required/compiled records across72 scenes, with
runtime verification false. This includes all596 prior adapted records and
105 newly translated records (98 scripts and seven names).

QA captured117 production/catalog file hashes after writer acknowledgments.
All ten R05 pack hashes matched the independently reviewed snapshot, and no
frozen production input changed during compilation or audit. Handoff documents
and separate launcher/boot artifacts are outside those frozen inputs.

The original-based audit independently compiled all701 records and matched
all911 declared compiler patch ranges against candidate bytes, accounting for
the established XP4 reward-heading override. Both IPS files replay exactly to
the delivered images:198 Opening records and921 System records. Data, Ending,
User and Visual images remain byte-identical to originals.

The bounded source closure has168 entries,139 containing text; all139 are in
the release requirements. All596 previous canonical and adapted English values
remain unchanged. Compared with R04-02, Opening has zero byte differences and
System has5,681; every difference is confined to reviewed cumulative compiler
patches. Welda's original profile, progression table and equipment/stat data
are unchanged. All11 new name pointers and280 equipment/development pointers
resolve to their bounded English labels. XP4's exact code and metadata match
the prior candidate.

Independent [source inventory](r05-qa-source-inventory.md) and
[editorial review](r05-qa-editorial.md) document map-number correction, world
wrapping, the Saibal bar partition, guard-combat coverage, Welda's previously
missing ability names, two-choice menu rows, continuation-page corrections
and the verified scrap-exchange direction. All identified static/editorial
release defects are resolved in this frozen candidate.

The reproducible audit is `work/r05-qa-audit.py`; detailed results and hashes
are in `work/r05-qa-frozen-audit.json`. The patched System SHA-256 is
`39154a3a4746525abcf959e3be3cb20fbb64f922dbf71d94e41c0fd5bb0f0d3e`;
Opening is
`bc8f7602e5b3b05c780002b6f65407059b6a32e3d7dd68693bf9f8f4b5d2ed83`.
This is static, editorial and binary verification. Actual movement, fights,
exchange controls, ticket transactions, letter display, save/load and the full
translated route still require runtime/player verification. Any isolated boot
smoke evidence must be reported separately from route traversal.
