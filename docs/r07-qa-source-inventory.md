# R07 independent source inventory

QA inspected the original System image and the cumulative R06 catalog. This is
static evidence; no route traversal has been performed.

## Connected maps and optional bar

The original location table at System10440 identifies map10 as Byuto and map11
as Hom. Byuto map10 metadata is System86c00. Its two ordinary exit records are
`576c2f0137` and `2531623b7e`: they lead to town46 and mine97 respectively,
because ordinary map exits encode the destination plus one. Its header byte2
is zero, retaining the previously established wrapping surface movement mode.

Town46 metadata is System8fc00, bank060000, with objects000–009. Its two bar
doors enter shared map2 at world99,2. QA independently repeated the nonzero-tile
flood fill on original Systemb0000..b0fff starting at tile49,1. The component
contains167 tiles, bounded x41–53,y0–12, and exactly the five object entries
053000039–043. The original Data4c400 zero-tile attribute remains14hex, with
blocking class10hex; this is the same proven partition mechanism as R02/R05.
The bar is required optional coverage and does not connect to other bar regions.

Mine97 metadata is System9c800, also bank060000. Its ten trigger rows select
021 (two approach tiles),029 (two hidden-passage tiles),022 (two ambush tiles),
and023 (four boss approach tiles). There are no ordinary map objects or exits;
the bounded-map border returns to Byuto at37,51. Boss023 also returns to Byuto
at37,51 via command `#Q 25 33 0a`.

The #Q handler at Systemdac8 reads the first two payload bytes into BX/CX.
Its ordinary path at db38 reads and zero-extends the third byte and stores it
directly at resident1775; it does not decrement it. Thus script #Q uses a direct
map ID, unlike ordinary map exit records. This distinction avoids mistaking the
boss destination for Hom or for map37.

## State and branches

Roy025 sets29 and assigns Byuto. The existing CS roots expose secretary035,
lab039, full-hangar038, and repeats040/041 after engine-grant flag49. Party
callers select081013–015 after29. Town/bar witnesses set33, selecting081016–018.
The one-time town gift sets2a, with full-inventory010 and repeat019/020.
Boss023 sets2c, selecting town024–028 and party081019–021.

The proposed endpoint retains optional CS return but stops before Roy's
flag2c report branch009→027, which invokes the next continuous briefing.
The manager owns the actual scope plan and terminal-edge integration.

## Encounter exclusion checks

QA read all sixteen group-directory pointers from each map's header25 and
collected the original eight-byte group headers and eleven-byte enemy rows.
Byuto's surface uses sprite hex19,1c,1d,1e. Mine97 uses these monsters plus
sprite80 and6e in the boss group at System9c9fa; its ambush group at9c99a uses1d.

The resource1b profile-pointer table at System11aae indexes sprite−12hex.
Relevant profile offsets/types are12b19/2,12b5e/3,12b75/2,12b8c/2,133fe/9,
and132bc/2 respectively. None has type8 or10, the original predicate for the
special Karma defeat narration. The R06 exclusion therefore remains valid on
this route. Enemy ability-name and encounter-message coverage still requires
integration review; this source exclusion alone does not approve all combat UI.

QA independently disassembled the enemy-action selector with Capstone. At6b1a
it draws an index0–3, loads runtime actor+23..26 into1c93, and loads profile
+13..16 into1c94. At6b76..6b93 and6bc9..6be9 it uses the selected action to
index the effect descriptor table20c8 and copy effect fields. These are action
and animation identifiers, not indices in the visible ability-name table10300.
RE's downstream category4 trace covers the Byuto-specific special effects.
Together with existing battle-renderer coverage this closes the suspected new
enemy ability-name surface; it does not assert a runtime visual check.

An independently written command traversal reproduced all319 entries of the
R07 closure, including counted choices, random responses, calls, shop/item
failure branches, current story flags and the explicit next-debrief terminal
edge. This corroborates the production closure rather than merely invoking it.
