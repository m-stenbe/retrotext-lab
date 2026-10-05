# Editorial and fitting fixes from the September 24 playtest

The fixes retain the current story coverage. Canonical English remains separate
from the display adaptations; original images and the running candidate were not
modified by this work.

| Screenshot / symptom | Source and correction |
| --- | --- |
| 10.55.32 and 10.55.49, words split across cinematic rows | `cinematic:meteor`, especially tokens 083 and 115/117. The screenshots exactly confirm the existing 25-column width. The renderer wraps glyphs without looking for spaces. Twenty text spans across the complete cinematic now pad to word boundaries; no story wording or original commands change. |
| 11.16.11, Jane's yellow question runs into her dialogue | `052000:013`. A repeated style/header command does not reposition the body cursor. The removed original newline is restored. Town identification, introduction and question occupy three body rows, leaving the fourth for the choice prompt. |
| 11.16.32, awkward inventory-work invitation | `052000:072`. Canonical English now says she has a part-time job sorting stock. The display reads “I SORT STOCK / PART TIME.”, then “IT'S TOO MUCH / ON MY OWN. / CAN YOU HELP?” The original wait before the choice is intentional; choice commands and targets remain unchanged. |
| 11.22.29, excessive gap before “I” | `052000:014`. The prior adaptation contains one space, not a tab. Full-cell punctuation and space make that gap conspicuous. Preserve “I thought they would kill me,” placing “I” at the beginning of its own row and expanding the contraction to fit four balanced rows. |
| Joined hotel and dancer captions | `052000:041`, `053000:001`. Add explicit line boundaries because repeated style commands share the cursor. Restore the overnight stay in the hotel caption and stage context in the dancer caption. |
| Knife/medicine pickup continuation | All four relevant pickups call `051000:041`. The call records a new line origin at the current cursor. Each caller now advances to a new line before the call, and the FOUND helper has no leading newline. This avoids indenting FOUND relative to the item name’s end. |

The cinematic encoder now rejects an automatic break inside a word, including
breaks spanning a delay or adjacent text spans. It continues to reject overflow,
missing adaptations, modified timing-only spaces and changed non-text commands.
Seven focused cinematic tests pass. Original-image compilation uses 3,310 of
4,210 available bytes; all original non-text tokens and disk length are preserved.
Padding affects the typewriter duration, as any text-length change does; no sound,
animation or wait command is altered.

The Jane introduction and its name-sharing, refusal and repeat alternatives were
re-read together. The inventory job's offer, acceptance, refusal and both dismissal
outcomes were also reviewed. One erroneous context summary claiming that wages
could not be increased was corrected to say no wages could be paid, matching its
already-correct canonical text. Scene-review bases were updated only where this
editorial context or canonical wording changed.

The narration renderer correction adds a colour-restoration byte after line
breaks. Six tight allocations were adjusted without dropping story information:
`051000:027`, `051000:029`, `051000:041`, `054000:000`, `054000:032` and `061000:020`.
These remove redundant punctuation or use “ROGER!” for “UNDERSTOOD!”. The pickup helper’s newline was subsequently moved to its four callers after the shared-call line-origin behavior was established; the hotel
caption also drops its final exclamation. Canonical prose stays unrestricted.

The equipment icon consumes one of the nine list cells, leaving eight text cells.
A separate label review shortens **117 R02/R03 equipment labels**, plus the early
Protector display (`PROTECTR`). Most compound labels join their existing words;
long single words use explicit abbreviations such as `MICROCHP` and `CYBRSUIT`.
Caliber values, numbered variants and canonical names remain unchanged. Every
changed label records its previous and new display spelling in adaptation notes.
Location titles and ordinary dialogue are not subject to this equipment limit.

The shared cursor, narration-attribute and one-cell space implementation is owned
by RE/integration; this document records its editorial consequences. Final
cumulative replay, branch composition, name-storage and candidate-image checks
belong to the revised build's QA record. In-game appearance and interaction still
need verification in that new build.
