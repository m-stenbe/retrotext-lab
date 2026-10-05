# September 24 playtest fixes: frozen independent QA

Approved as a candidate for player verification: `work/r04-02-xp4`, built from `profiles/alshark/release-playtest-fixes.json` and `work/playtest-2026-09-24-final-catalog.json`. This is cumulative through the R04 station briefing, stopping before leaving the station. Full route traversal and final pixel appearance have not been verified.

## Frozen source and editorial review

QA reviewed all 22 supplied screenshots and mapped them to source records in [the screenshot inventory](playtest-2026-09-24-qa.md). The final catalog contains 596 required, adapted and compiled records in 62 scenes. All 595 previous records remain; the seven-row ship-service menu is added. The inherited plan note mentioning 595 is historical; the actual gate, catalog and compilation contain 596.

The complete final adaptation set was compared with the approved localizer v5 snapshot. Canonical English, context, review state and target values agree. Fresh replay normalizes repeated adaptation notes in 56 records and removes two obsolete pickup notes from `script:051000:041`; these notes-only changes were independently inspected and approved. Compared with the previous release, 134 adaptations change and only the stock-sorting job record changes canonical English. All 117 equipment abbreviations retain their canonical distinctions; Protector separately becomes PROTECTR. Meteor changes pad words without changing story wording or original animation/timing commands. Additional spaces can affect typewriter elapsed time.

The final five-record pickup correction is approved: four caller labels end with a newline before their original shared call, and the shared FOUND outcome has no leading newline. This is required because the actual shared-call entry captures the current cursor as its new line origin. Earlier newline placement inside the callee retained the unwanted indent.

All 90 production inputs in `work/playtest-2026-09-24-frozen-inputs.json` still match their frozen hashes. The independently recomputed catalog fingerprint is `19e4ce37844f292b3dfa69803c55eb37a1f2b37f15951b1c047f9e2043205d58`.

## Independent binary and scope audit

`work/playtest-2026-09-24-qa-audit.py` independently compiled the catalog from original images, checked 795 compiler patch ranges against the candidate, validated manifest fingerprints and checked the cumulative route closure: 85 entries, including 67 text-bearing entries, all covered by required records. The gate reports candidate-ready with runtime verification false. Map104's nominal border returns to already translated map98; unknown border walkability does not create an untranslated destination. The station exit leads to map9 and remains the endpoint boundary.

Opening and System IPS files were parsed independently and replayed onto original images. Their 198 and 749 records respectively are sorted, nonoverlapping and terminate correctly; replay yields the exact candidate bytes. Every image retains its original 1,261,568-byte size. Changes from R04-01 are confined to approved new/prior compiler allocations and exact menu-width edits: 3,204 bytes in Opening and 10,740 in System. The XP4 trainer code and metadata match the prior build exactly. Original progression and equipment-stat tables are unchanged. All 280 development item/equipment IDs resolve correctly and fit the eight-cell name limit. R04's 25 name/location pointers match the rebuilt allocations and aliases.

| Image | SHA-256 |
| --- | --- |
| Opening | `bc8f7602e5b3b05c780002b6f65407059b6a32e3d7dd68693bf9f8f4b5d2ed83` |
| System | `2a7b2198b1e54232535c8d085cc6330f833a21440edb9f734d98aec63cc45553` |

Data, Ending, Visual and User remain byte-identical to their originals. All 35 protected inputs remain unchanged: 22 screenshots, six original disks, six played R04-01 disks and the previous final catalog. Detailed results are in `work/playtest-2026-09-24-qa-frozen-audit.json`.

The screenshot-targeted seven-row menu is covered. Related untranslated menus Opening00477d/004788 and combat004430 remain deferred; no new caller-reachability proof establishes their exclusion. This candidate does not claim flight, first-mission, or post-briefing menu closure. Those surfaces need source discovery in the next section; translating the seven-row variant is not proof of complete ship UI coverage.

## Renderer evidence and its limits

QA independently reviewed the native harness in `tests/test_alshark_playtest_machine.py` and its five passing results in `work/playtest-machine-results.json`. It executes the original 16-bit interpreter and name-renderer overlay. It proves that control34 appends rather than resetting the cursor, control36 sets narration attributes, ordinary newline resets those attributes, inserted @6 restores them, and continuation0_6 restores them after clearing. Name substitution retains the active narration attributes. The original shared-call handler reproduces the old FOUND indent and the corrected left origin.

The native overlay also proves that normal-mode ASCII space occupies two glyph cells while `>` occupies one. CAMP>KIT and SUBM>GUN occupy eight cells, Saxen Canyon and Basement Bar twelve, and Planet Hom eleven including its new leading pad. JOE's first glyph is at cell four, the nearest-left centered position in twelve whole cells. These results support the independently traced inventory and title geometry rather than relying on nominal string length.

Platform glyph lookup/drawing and selected disk-loading, input-wait and box services are stubbed. Thus these are directed cursor/attribute execution tests, not complete rendered frames or a route playthrough. The seven-row menu geometry has source and binary evidence, but no post-fix menu screenshot. Jane's choices, the woman's spacing, the hotel/dancer captions, cinematic wrap, title alignment and inventory clipping still require confirmation in final game pixels. No renderer defect is declared fully visually verified merely because text fits or compilation passes.

The manager's complete suite reports 162 tests passed, zero skips, including the five native renderer tests and two trainer tests (`work/playtest-test-results.json`). The isolated boot smoke reports exit0 after 1,800 frames and a RIGHT STUFF logo; all six smoke disks match the candidate. That demonstrates boot only, not story transitions.

## User-disk transfer and final preservation

After the frozen audit, the manager copied the played R04-01 User Disk once into the new candidate and recorded `work/r04-02-xp4/save-migration.json`. QA independently checked the source, destination and pristine candidate backup. All have SHA-256 `619118093eeed49fbc1b2b7bb1ec41d99969bf14a573bb65ab90adba4f0a13a1`; the copy changed zero bytes. This preserves the provided disk but does not establish that it contains saved progress. Old emulator states were not imported.

Post-transfer checks confirm all six candidate image hashes, all 90 frozen production inputs and all 35 protected inputs remain unchanged. Evidence: `work/playtest-2026-09-24-qa-post-migration.json`. QA changed no implementation or editorial pack it approved and made no commits.
