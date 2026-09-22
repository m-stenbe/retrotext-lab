# Canonical localization and technical adaptation

The canonical English script is the intended English-language game, free of
storage, font and layout constraints. The in-game adaptation is a separate
technical deliverable. Existing uppercase drafts are **legacy provisional
adaptations**, never automatically authoritative translations.

The new game-independent layer is `retrotext/localization.py`: records, scene
context, editorial review fingerprints, adaptation state and terminology impact.
The Alshark adapter owns source discovery, byte offsets, immutable tokens, the
supported reinsertion allowlist, font rules, runtime names and layout limits.
We retain the current project layout; no speculative PC-98 abstraction or
automatic support for other engines is claimed. Another profile can reuse the
editorial layer while supplying its own source and fitting validators.

## Data and provenance

`canonicalEnglish` is unrestricted Unicode prose. It can contain complete
dialogue, speaker labels and contextual placeholders appropriate to an editor.
It is never fed to the ROM encoder. `target.inGameEnglish` contains only the
separately prepared adaptation (a token-ID-to-text mapping for Alshark scripts).
The `source` object retains the original exporter record, raw bytes, token IDs,
commands, name references, allocation and hashes; it is immutable. Other text
types retain their original byte spans and relevant pointer provenance.

Each record has a scene and context: speaker, listener, intent, tone, terminology
IDs, uncertainty and notes. Each scene lists records in reading order, including
branch alternatives, and records participants, location, story state, narrative
purpose, earlier/later context, evidence and unresolved questions. Null/empty
metadata means unknown, not permission to fill gaps by guessing. Entry adjacency
does not prove conversational order. Follow counted commands and known branches
and use playtest evidence; following dialogue may belong to another entry.

The catalog includes all currently decoded bank entries and resident menu-table
strings, reviewed UI spans, selected short/full shared names, and the two known
fixed combat scripts. It does **not** claim complete game coverage: cinematic
extraction, remaining name/item/ability tables and other text still need mapping.
Use the same canonical/context model as those sources become available.

## Working on a connected scene

1. Gather participants, preceding/following dialogue, branch alternatives, story
   state, earlier-event references and terminology. Record evidence and unknowns.
2. Translate the complete scene into natural canonical English. Preserve meaning,
   characterization, humor, emotional subtext and conversational flow. Do not
   carry Japanese syntax into English when it makes dialogue awkward. Investigate
   ambiguous items, technology, factions and abilities instead of locking a
   literal reading. Keep unknown decisions explicit in the bible.
3. Read the entire canonical scene continuously as an English RPG script. Check
   distinct voices, logical responses, pronouns, omissions, jokes/euphemisms,
   politeness, uncertainty and anger; terminology must agree. Remove unintended
   added certainty or explicitness. Correct canonical English first.
4. Record editorial review only after doing that work. The review command is an
   attestation, not an automated quality judgment. It fingerprints the whole
   scene's source, canonical prose, context and referenced bible terms.
5. Adapt from canonical English and its intent. Preserve, in order: core meaning;
   character voice/intent; relationships/context; natural English; important
   story information; secondary detail; similarity to Japanese syntax. Explain
   meaningful omissions in target notes. Do not independently retranslate each
   Japanese token or silently equate a short UI label with canonical terminology.
6. Validate font/encoding, cells, lines, original page breaks, allocation,
   immutable commands, name substitutions and runtime fields through the profile.
   If adequate English cannot fit, use `DOES_NOT_FIT` and a concrete reason.
   Relocation, additional pages, narrower Latin glyphs or new allocations are
   engineering investigations; none permits casually changing command bytes.
7. Build a separate test image, play it, and record observations against that
   build/adaptation. Gameplay/editorial feedback goes back to canonical English
   when meaning or voice needs correction, then to its adaptation.

Changing canonical text, scene context or a referenced term makes editorial review
stale. Re-reviewing does not silently approve old adaptations: update `basedOn`
only after checking the adaptation against the new review. Technical success is
not editorial approval; editorial approval is not runtime verification.

## Local commands

Run from the repository root; full Japanese catalogs remain ignored in `work/`.

```sh
python3 profiles/alshark/localization_tool.py export /path/to/original work/localization.json
python3 profiles/alshark/localization_tool.py scene /path/to/original work/localization.json \
  --scene-id house-karu --records script:051000:010 --output work/karu-context.json
```

That creates a scene scaffold, **not** a finding that this entry is the entire
conversation. Inspect its tokens/branches and add connected records and context
as needed before writing canonical English. Edit the JSON independently of the
engineering export. Use stable bible term IDs in context/scene terminology lists.

```sh
python3 profiles/alshark/localization_tool.py review /path/to/original work/karu-context.json \
  --scene-id house-karu --reviewer 'Editor name' \
  --note 'Describe the actual continuous-scene/context review' --output work/karu-reviewed.json
```

After review, prepare each record's `target.inGameEnglish`; set `status` to
`adapted` and copy that record's `review.basis` to `target.basedOn`. Keep notes
about omissions, choices and unresolved gameplay checks. To flag a blocker, set
`status` to `DOES_NOT_FIT`, retain the same review basis, and record a reason such
as “The four-row layout cannot preserve the warning and Karu's measured voice;
further shortening would damage the scene.” A failed technical validation never
automatically shortens text or modifies canonical English.

```sh
python3 profiles/alshark/localization_tool.py validate /path/to/original work/karu-adapted.json
python3 profiles/alshark/build_demo.py /path/to/original --output work/localized-test \
  --expand-menu-labels --localization work/karu-adapted.json
python3 profiles/alshark/localization_tool.py impact /path/to/original work/karu-adapted.json \
  --term character.karu
```

Validation/build rejects stale reviews, stale adaptations, altered source
metadata, changed legacy text masquerading as unchanged, fitting failures and
DOES_NOT_FIT blockers. Untranslated/legacy/draft records are not inserted by this
overlay. A record with new canonical English but no reviewed adaptation blocks
this build rather than silently retaining its old compressed line. Earlier draft
builds stay reproducible; do not use that compatibility
path for new translations. The manifest records selected review/adaptation hashes.

The initial reinsertion adapter supports existing allowlisted dialogue entries
with the existing conservative 14-cell/four-row validator. It refuses shared
script-call layouts until composed validation is connected. Menus, items/names,
cinematics and fixed-runtime text can have canonical/editorial records now, but
their new adaptations must get a verified adapter to the existing specialized
patchers before this workflow can insert them. Unsupported types fail explicitly;
they do not fall back to unconstrained writes. Existing specialized patches and
legacy pickup builds remain unchanged.

`compile` produces an original-based System validation image. It is not the full
demo and does not patch shared names; use `build_demo --localization` for playtests.

## Migration and bible

Do not spend the current reverse-engineering effort rewriting every old draft.
When a scene is next touched, reconstruct/review canonical English from Japanese
and context, then reconsider its existing constrained adaptation. In particular,
Karu's diagnostic line and the greenery/lake warning need full contextual review;
their terse legacy English is not a style guide.

`profiles/alshark/localization-bible.json` keeps working names, full-name unknowns,
relationships, evidence-based voice notes, places, factions, technology, items,
weapons, abilities and story-stage facts. Provisional spellings remain provisional.
When a term changes, `impact` identifies direct users and their scene peers;
review fingerprints also invalidate affected reviewed scenes. Legacy drafts with
no term references still need a text search/manual migration audit. Public bible
and workflow files contain English notes; original source remains local.
