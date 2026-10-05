# Required name storage investigation

The meteor adapter does not provide a free pool for System inventory or location
names: those consumers use a different segment and load.

## Established reader and loader

System `0xFB86` selects destination segment 5000, offset D7F8, and calls the
indexed disk loader with index 14h. `0xFBC8` resolves the descriptor through
`0x3C83 + index*2`; index 14h points to `0x3F31`, whose bytes are
`01 08 01 06`. This reads six 1024-byte sectors starting at System `0x10000`.
The known loaded name region is therefore `0x10000..0x117FF`, and contains no
four-byte zero/filler runs. The E5 padding at `0x13C00` belongs to a different
load and is not safe storage for relative name pointers.

The name substitution handler at `0xF38D` indexes the table at runtime DBF8
(disk 10400), reads its relative pointer, and adds D7F8. At `0xF3AD` it handles
half-width kana A6..DD, otherwise consuming two bytes as a CP932 glyph. It does
not apply the dialogue interpreter's ASCII-letter conversion. Merely replacing
full-width names with ASCII is unsafe, even before inventory consumers are
considered. A renderer change would require separate implementation and review.

## Exact required references

| Name | Original string | Relative-pointer fields |
| --- | --- | --- |
| Shirt | 10A99 | 100B8, 100BA, 100BC, 100BE, 100C0, 100C2 |
| Protector | 10AA1 | 100C6 |
| Camp Kit | 10CB0 | 10144 |
| Planet Hom | 11329 | 10456 |
| Saxen Canyon | 11722 (includes leading display control) | 10508 |

Existing character/name repacks use five spans totaling 94 bytes, with 80 bytes
currently occupied. Their 14 spare bytes are fragmented. Adding expanded target
names also requires respecting each allocation's contiguous capacity, not just
an aggregate total.

Four identical raw strings have separate source allocations:

| Allocations | Pointer fields | Duplicate size |
| --- | --- | --- |
| 108C4 / 110DA | 10044 / 10322 | 10 |
| 10A42 / 1112D | 100A6 / 1033C | 9 |
| 11100 / 111AE | 1032E,10330,10332 / 10376,10378,1037A | 9 |
| 112C8 / 112DF | 10444 / 10448 | 11 |

These are research candidates, not an allocation authorization. Their combined
39 bytes do not supply the contiguous slots needed by all expanded names, and
sharing names across equipment/ability tables could complicate later terminology.
A broad compactor must classify every pointer and consumer, preserve strings that
have references into their interiors, and establish that names are not mutated
in place. No such compactor or name relocation has been implemented by this audit.

## Resolved: the UI name renderer supports ASCII

Further tracing the original ASCII item label at `0x10A90` resolved the missing
path. Ordinary UI names do **not** use the dialogue `$` reader. System wrappers
`0xF590..0xF5C6` call the far service at segment 7000 through `0xE15C`.
That module is the 32-sector System load at `0x14000`. Its entry table routes
item, ability, character and location labels through relative `0x70B1`.
At relative `0x70CD`, A–Z are converted through INT41/AH19 before drawing.
The original `BH` equipment prefix uses this path. ASCII spaces advance two glyph
cells and `>` advances one glyph cell. Other glyphs remain CP932 pairs/kana.

The required-name adapter therefore uses ASCII for Shirt, Protector, Camp Kit,
Planet Hom, Saxen Canyon and the UI-only Cosma location entry. All dialogue
character names remain full-width CP932, including every short/full-name alias.
All 2,249 exported scripts were checked for name ID81: no `$81` references occur.
Cosma's name-table ID is preserved. This does not assert that ASCII is safe for
arbitrary dialogue names or for undiscovered dynamic substitutions.

`profiles/alshark/names.py` now repacks twelve **existing** name storage spans,
237 bytes total, with 220 encoded bytes. It recalculates location-prefix padding for the twelve-cell title box. No unused pool, rendering code, loader, or unrelated string is
changed; neither duplicate-string coalescing nor whole-bank compaction is needed.
The original item/name table is scanned for aliases into every changed span,
rejecting any pointer field outside the reviewed set. Source hashes, loader bytes,
ASCII conversion instructions and exact required aliases are guarded. Source
records retain the original text and pointer fields. All 32 editorial records
must be adapted as one allocation group; a subset is rejected.

`compile_names(images, translations)` returns System bytes plus per-record
metadata and every changed allocation/pointer range. The manager applies those
ranges after legacy UI/name writes. It must validate all current editorial and
adaptation fingerprints first. Changed spellings require an explicit update to
this audited allocation plan. Five tests cover complete pointer resolution,
all Shirt aliases, full-width dialogue names, patch confinement, partial groups,
inconsistent aliases, unreviewed pointers, source hashes and control injection.
Actual font appearance, alignment, item use/equipment and location transitions
remain runtime QA tasks.


The same final allocation group includes fourteen ability names from the class3/4
learning table, so repeated battles with the optional EXP multiplier do not expose
untranslated newly learned ability labels. The two original contiguous ability
spans are `110B3..11100` and `11196..111AE`. Their pointer aliases remain distinct
IDs, including Healing IDs11/55, Cure21/22 and Teleport54/56. Every relevant pointer
is repointed to the corresponding English name; no ability mechanics or learning
threshold changes. Proposed labels are independently reviewed, with HEAL,
THUNDER, WARP and LOCATE documented as natural concise adaptations of their
canonical names. QA subsequently established the eight-cell learned-ability field and ten-cell
status list. TELEKIN, DIMENS, MINDSTRM and INVIS are explicit display abbreviations;
the complete canonical names remain unchanged. QUAKE fits completely. The adapter
enforces eight cells for abilities and item names in narrow inventory/equipment fields. This expands the catalog by
seventeen name records (three equipment/item labels and fourteen ability labels).
Every changed byte remains within the 52 declared allocation/pointer ranges;
remaining bank bytes and image size are unchanged. See the independent coverage
audit for renderer-specific field widths and regression tests.


September 24 playtest correction: the generic name renderer at System `1b0b1`
advances two glyph cells for ASCII space (`1b100` calls `1b111` twice), and
one for `>` (`1b103` calls once). English internal spaces now encode as `>`;
source Japanese padding is replaced by padding centered for a twelve-cell title.
Planet Hom, Saxen Canyon, Basement Bar and Joe retain their adapted wording.
Inventory selection reserves eight name cells plus its icon, rather than nine
name cells; equipment adaptations are rechecked against this narrower consumer.
Historical exported `maximumCells: 9` remains source-provenance metadata for the
old catalog; current compilation independently enforces the corrected eight-cell
consumer limit. Canonical names remain complete.
