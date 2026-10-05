# R06 independent frozen-candidate audit

**PASS — static release candidate**, `work/r06-01-xp4`.
The candidate contains821 required records across79 scenes, including120 newly
reviewed records. It ends before reporting the rescue to Roy; optional CS-station
conversations are included, while Roy's next-assignment branch is an explicit
terminal edge. This approval does not claim player traversal or runtime coverage.

QA captured129 production/catalog hashes after the manager's full freeze. All
eight R06 pack hashes matched the independently reviewed editorial snapshot.
No frozen file changed during the build and independent audit. Handoff docs,
launcher files and isolated boot artifacts are outside that production snapshot.

Independent checks passed:

- Strict section-candidate assessment, current plan/catalog/bible fingerprints,
  and no unresolved blockers.
- All255 source-closure entries and219 text entries covered by the required
  inventory, including the explicitly bounded CS-station return.
- Recompiled821 records and compared all1133 declared patch ranges with the
  candidate disks. All701 earlier canonical texts and adaptations are unchanged.
- Replayed both IPS files exactly from immutable originals:245 Opening patch
  records and1064 System patch records.
- Every byte changed from R05 falls within declared cumulative compiler ranges
  or the reviewed geometry changes. All nine menu widths and eight distinct
  selection-width instructions match the approved values.
- All41 new name records resolve through their guarded pointer aliases. The
  280 equipment/development names remain English and within their runtime fields.
- Original progression table, enemy/equipment statistics and Welda profile bytes
  remain intact; XP4 code and metadata exactly match the earlier candidate.
- Data, Ending, User and Visual disks remain byte-identical to the originals.

The separate source inventory documents flight callers, dynamic name fields,
star-statistic header reservations and exclusions for later Karma/boarding text.
QA decoded and visually inspected all eight original map diagrams: their baked
labels are Latin/numeric, with no Japanese requiring an image patch.

| Disk | SHA-256 |
| --- | --- |
| Opening | `623895c1024191069aee4792de1e1719e5b1cd8efe8e0606da0d816e061ad89b` |
| System | `58065b62a5089a52d56d24415aab4f285579e66faaa98b692d6e4ec2159063ba` |

Reproducible audit: `work/r06-qa-audit.py`. Detailed results:
`work/r06-qa-frozen-audit.json`. Approved-pack and frozen-production manifests:
`work/r06-qa-approved-packs.json`, `work/r06-qa-frozen-inputs.json`.
Source catalogs, extracted scripts and decoded source images remain ignored in
`work/`. Player verification is still required for the complete connected route.
