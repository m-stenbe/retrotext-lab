# Dust approach and Hamack: batch 03

This batch advances beyond the replayed opening. Fourteen new records in nine
scene groups have canonical English and a contextual editorial review. Ten
records in six groups also have validated in-game adaptations. This is partial
route/Hamack coverage, not a translation of the complete Dust/Joe encounter.

## Playable coverage

| Entries | Content |
| --- | --- |
| 082000:001 | Sion asks Karu about Joe; Karu points to Dust south of Hamack |
| 052000:013, 043, 042, 044, 045 | Jane introduces Hamack and herself; name-sharing/refusal and repeat branches |
| 052000:001 | Scrap has value as well as money |
| 052000:009 | Suggestion to seek informants at the underground bar |
| 052000:014 | A woman's frightened account of Zolias soldiers visiting |
| 052000:015 | A man's optimism about the planet becoming green |

The reviewed working spellings remain provisional where previously noted. Jane
is a new working romanization. The bible gains a separately referenced route
fact and story stage, without changing earlier glossary fingerprints. All prior
canonical/context/review/adaptation records remain exactly unchanged.

Karu's longer joining scene (051000:019) and a girl's rumor about Joe at Dust
(052000:019, with greeting alternative 084) have canonical English but are
explicitly deferred. The joining scene needs the image-playback explanation and
search invitation on a single existing page. The rumor needs location, hearsay,
insult and description of Joe's inventions, plus the current runtime name omits
his Scrap epithet. Neither is solved by telegraphic English. Joe's party
conversation pointing toward Hamack's bar (082000:002) is canonically reviewed
but its #O dispatcher still needs control-flow investigation before reinsertion.
The first encounter with Joe and exact map/event triggers remain unmapped here.

## Preservation review and scope

The ten playable entries are added individually to the existing editable
allowlist. No importer, layout rule, allocation, pointer or opcode handling is
relaxed. Existing source catalogs must be regenerated; never hand-edit their
`editable` metadata. Prior public review/adaptation packs replay unchanged
because no previously reviewed record's source metadata changed.

Four NPC entries use only the existing header/body, wait and end controls. Jane's
013 entry has #B condition/entry pairs (7,44) and (8,45); #Y targets entries 43
and 42. Her responses set flags 7/8 with #S. Existing disassembly establishes
these as entry-index dispatch and counted flag operations (see
`alshark-script-format.md`); text bytes are not their jump addresses. Repeat
entries contain only names/text/header controls. The empty t009 adaptation in
013 removes a redundant blank text newline immediately before a header reset;
its token remains present and every actual control is immutable.

082000:001 contains fourteen #B condition/entry dispatches before its own
conversation, followed by the familiar header/wait/clear/name sequence. Payloads
and table positions stay fixed. Its other state-dependent destinations are not
claimed translated. No shared-script #P or new display mode is enabled. The
unreviewed #O entry stays read-only. Static structural safety does not prove
runtime branch activation or appearance.

Validation: 59 tests pass, including a synthetic bank regression for Jane's
conditional targets, yes/no branches, flag commands, zero-valued name ID, bank
pointers and neighboring read-only entry. Full unchanged import is byte-identical.
The public packs replay to exactly the local catalog. IPS roundtrips and all
source/editorial/layout/allocation checks pass. Compared with batch 02, all 473
changed System bytes lie in these ten allocations; decoded immutable tokens are
unchanged and Opening is identical. The cumulative build includes 23 selected
canonical-derived entries in twelve scenes. Runtime playtesting is pending.

## Reproduce

Regenerate the catalog and replay the versioned English packs in order. This
preserves source provenance while accommodating the expanded allowlist:

```python
import json
from pathlib import Path
from profiles.alshark.localization import (
    BIBLE, catalog, load_images, apply_editorial_review, apply_adaptation_pack,
)
images = load_images('/path/to/original')
bible = json.loads(BIBLE.read_text())
document = catalog(images)
for apply, name in [
    (apply_editorial_review, 'editorial-review.json'),
    (apply_adaptation_pack, 'adaptations-batch-01.json'),
    (apply_adaptation_pack, 'adaptations-batch-02.json'),
    (apply_editorial_review, 'editorial-dust-approach.json'),
    (apply_adaptation_pack, 'adaptations-batch-03.json'),
]:
    document = apply(document, json.loads(Path('profiles/alshark', name).read_text()), bible)
Path('work/adapted-batch-03.json').write_text(
    json.dumps(document, ensure_ascii=False, indent=2) + '\n')
```

```sh
python3 profiles/alshark/batch_tool.py /path/to/original work/adapted-batch-03.json \
  --plan profiles/alshark/batch-dust-approach.json --output work/dust-approach-packet-03
python3 profiles/alshark/build_demo.py /path/to/original --output work/dust-approach-03-test \
  --expand-menu-labels --localization work/adapted-batch-03.json \
  --localization-scenes story-canyon-directions story-lucia-rest story-work-interactions \
  story-dead-gigi story-shoko-invitation story-wasteland-and-return route-karu-dust \
  hamack-jane hamack-scrap hamack-informants hamack-soldiers hamack-greenery
```

## Playtest and save states

Check Karu's party conversation after joining, then Hamack's NPCs. For Jane,
check both choices and their repeat greetings. The prompt uses the header area;
its color and position need runtime confirmation. Note which route/state actually
exposes each conversation. The generated packet includes per-scene checklists.

Save states are useful checkpoints, but keep an in-game save as well when
switching patch builds. Upstream NP2kai's `flagsave_mem`/`flagload_mem` explicitly
save and restore emulated memory:
[NP2kai state implementation](https://github.com/AZO234/NP2kai/blob/master/statsave.c).
Consequently an older state may restore already-loaded old script text; this is
an inference from the emulator implementation, not a tested result for the
player's particular state files. Freshly booting the new patch and loading an
in-game save provides a cleaner test. If testing from a state, verify that the
mounted disks belong to the intended build and that the new conversation is
actually displayed. An area transition has not been proven to refresh all text.

No running emulator, state files or player saves were changed. The new folder's
User Disk is the builder's default, not a verified transfer of player progress.
