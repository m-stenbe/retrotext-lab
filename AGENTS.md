# Localization work

Work proactively in substantial, connected playable sections. Read
`docs/section-release-workflow.md` and the active `release-*.json` plan before
choosing new translation work. The player verifies a translated section; do not
depend on player screenshots to discover routine missing coverage. Unexpected
Japanese inside a promised section is a release defect.

Completed batches may be committed and submitted for PR review before the player
tests them. Run the applicable automated checks and document source coverage,
candidate boundaries and pending runtime verification. Player testing is required
to claim runtime verification, not to open a PR. Publishing still requires the
user's authorization; this policy is not standing permission to push or merge.

For substantial sections, coordinate bounded RE, localization and independent QA
work with a manager/integrator. Keep shared-file ownership explicit; the manager
owns the bible, scope plan and integration. Roles do not change sandbox permissions
or authorize publishing. Small fixes do not require a new agent team.

Use `build_demo.py --release-plan` for section candidates. Ready-subset builds
without that flag are experiments, not complete sections for player verification.
Do not remove blockers or reduce scope merely to obtain a passing gate. Resolve
them with evidence, or explicitly explain a material boundary change to the user.

Read `docs/localization-workflow.md` before adding or revising translations.
The workflow is source/context → canonical English → connected-scene editorial
review → technical adaptation → ROM validation → playtest → editorial feedback.

Never promote existing compressed drafts to canonical English without reviewing
the Japanese and context. Do not rewrite all legacy drafts merely to migrate
them. Canonical English has no ROM font, byte, cell or line limit. If a natural,
faithful adaptation cannot fit, record DOES_NOT_FIT with an engineering reason.

Keep the existing byte-preserving exporter/importer, immutable commands, source
hashes, pointer guards, runtime-field checks, layout checks and tests intact.
New canonical work belongs in the localization sidecar, not directly in legacy
draft JSON or hardcoded patch strings. Extend the profile's fitting adapter for
unsupported text types before releasing new adaptations; never bypass checks.

Maintain `profiles/alshark/localization-bible.json`. Record evidence and unknowns;
do not invent relationships, voice traits, full names or official romanizations.
After a terminology change, run the impact report and review affected scenes.

Keep full source catalogs, game images and screenshots in ignored `work/`.
Public commits contain tools, tests, English editorial references and research
notes, not original disks or full extracted Japanese scripts.
