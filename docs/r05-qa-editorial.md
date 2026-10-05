# R05 independent editorial review

QA read the original Japanese and canonical English for all50 Saibal/bar/party
records, then separately reviewed the in-game adaptations. Review covered
ordinary and post-interrogation street reactions, underground-bar hostility,
shopping and hotel branches, the initial fight and interrogation, the full
ransom letter and kidnapping scene, and party responses before/after kidnapping.
The actors and context follow source headers and dispatches; the bar's six
objects are the independently proven Saibal partition.

The first adaptation review found two two-choice menu labels split over three
rows, several avoidable single-word continuation pages, an overly literal arrest
phrase and a changed threat idiom. The localizer corrected menu023/030 to two
rows, rebalanced whole phrases across pages, changed party004 to hauling Tomyu
in, and changed interrogation018 to telling him his days are numbered. QA
reviewed the revised text and found these corrections acceptable. The narration
retains the letter's false courtesy, threat, destination and Shoko's kidnapping.
Welda's graphic threat in party007 reflects the original rather than adding
violence; her female identity and abrasive voice remain consistent.

QA also reviewed the manager's26 Porkin and19 Zajil Spaceport records against
original source. No material fidelity defect was found. Ticket prices100/150,
Mars/Stea destinations, native Myuntos population, full-capacity refusal,
insufficient-money response and syndicate combat recognition are preserved.
Minor polish suggestions were to name cash in Porkin037's short refusal and
use an idiomatic shop boast in004. Further shared scrap and boarding records,
new names, final fingerprint freshness and binary/layout checks remain pending
until the integration freeze. This review does not assert runtime traversal.

The additional boarding records05f000:050/057 are faithful to their Mars/Stea
source destinations. The seven new map/ability canonical names are approved:
the four map identities match their original pointers, and Mental Recovery /
Mental Attack preserve the ability source terms without inventing effect
mechanics. Their MINDHEAL/MINDATK displays fit the established eight-cell limit.

QA found a substantive reversed-control defect in the first scrap-exchange
translation. The original diagram places8 below the upward arrow on the left,
and2 above the downward arrow on the right. Handler `?I06→0xdf0f` confirms
that direction bit1 exchanges one scrap for five credits; bit2 does the reverse.
The credit balance at19f1 is independently identified by the money-check/debit
handler `0xda71/0xda8b/0xda0d`. The exchange loop reads those balances,
subtracts/adds5 credits and adds/subtracts1 scrap accordingly. Holding Space
(bit20) executes five conversion calls instead of one on each input loop.
The correct instruction is **8 sells scrap for credits;2 buys scrap with
credits**. The manager is correcting canonical text and display labels before
freeze. This source interpretation is not a runtime controller test.

The manager applied the verified exchange-direction correction to both
canonical text and the UP8/DOWN2 adaptation. QA inspected the result.
Final manager fit review also corrected Porkin009 to explicitly deny knowing
anything, rebalanced the shop boast across two meaningful pages, and preserved
the syndicate member's stammer with supported punctuation. All105 new records
(98 script records and seven names) now have acceptable source-to-English
review. The ten reviewed pack hashes are stored in ignored
`work/r05-qa-approved-packs.json`; subsequent changes require diff review and
new fingerprints. Technical candidate/binary checks and runtime traversal
remain separate.
