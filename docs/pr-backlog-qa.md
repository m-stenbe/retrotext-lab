# Accumulated R01–R08 PR validation

Independent validation on October 5, 2026 reproduced the accumulated R08
candidate before R09 integration. All 91 versioned packs replayed from the
original disks. The replayed catalog exactly equals the previous R08 final
catalog, SHA-256 `454c402befbf7740ebe422b33f440f644dba8cc5387e46dc4fe0328ec446306e`.

The strict R08 build passed and all six resulting disk images are byte-identical
to the previous audited R08 XP4 candidate. This validates reproducibility of
the accumulated work; it does not establish runtime route traversal.

Commands used from the repository root **before R09 integration**:

```sh
python3 -m profiles.alshark.replay ../alshark/original \
  --output work/qa-pr-20261005/r08-replay.json
python3 profiles/alshark/build_demo.py ../alshark/original \
  --output work/qa-pr-20261005/r08-build \
  --expand-menu-labels --translate-disk-prompts --exp-multiplier 4 \
  --localization work/qa-pr-20261005/r08-replay.json \
  --release-plan profiles/alshark/release-mars-leave.json
PYTHONPATH=work/trainer-test-deps python3 -m unittest discover -s tests -v
```

The final PR includes R09 and its replay command applies 95 packs. To reconstruct
an R08 translation baseline with the final code, call
`replay(original, packs=PACKS[:91])` from `profiles.alshark.replay`. That fresh
catalog also contains the newly discovered, unadapted Daina label, so its whole
catalog hash differs. The exact catalog hash above belongs to the pre-R09 code
snapshot. Final R09 QA separately checks preservation of all 1,034 earlier
canonical texts and adaptations.

All 194 regression tests passed, including the native renderer and trainer
checks. The default dependency-free run passed with seven native checks skipped;
the existing local Unicorn dependency enabled them. Native execution required
the ordinary sandbox escalation because sandboxed execution aborted. Local
logs and disk comparisons remain in ignored `work/qa-pr-20261005/`.

An initial audit of 268 tracked or nonignored candidate public files found no
game images, screenshots, full extracted source catalogs or raw source payloads.
Short source quotations in technical/editorial research are not complete
scripts. `docs/getting-started.md` was checked against the builder arguments,
manifest fields, generated launch command, original hash list and repository
remote. Player testing remains pending and does not prevent submitting this
validated work for PR review.
