# Localization work

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
