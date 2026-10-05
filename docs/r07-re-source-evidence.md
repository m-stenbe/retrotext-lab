# R07 Roy assignment and Byuto mine

Original System image static inspection, October 2, 2026. Full decoded source
remains ignored in `work/r07-re-route-packet.json`. These findings establish
source inventory and control dependencies, not a completed emulator traversal.

## Route and story boundary

Roy's post-rescue branch `05c000:025` sets flag29 and assigns the Byuto
investigation. The secretary's 035 gives M861 directions and jumps041; scientist
039 grants engine item3a, with inventory-full038, and sets49. His repeat040 warns
against entering Zolias systems. Flag29 additionally selects bridge013/014 (Welda/Joe, as their root headers prove).

The entry is the R06 rescue debrief at Roy. The endpoint is the Byuto monster's
defeat, immediate town and party aftermath, and optional CS return, **before
reporting to Roy again**. The exact terminal edge is
`05c000:009 #B 2c 1b → 05c000:027`; its source bytes remain intact. Secretary029
is still included after victory. The next debrief and leave on Mars are excluded.

Byuto is map10 at System86c00, not map11 (Hom). Its two five-byte exits are
`57 6c 2f 01 37` and `25 31 62 3b 7e`, leading to town46 and mine97. Ordinary
exits and borders store target map **plus one**, as established in R05.
Town46 is System8fc00, mine97 System9c800; both use bank060000. Their borders
return to Byuto. Its surface wraps (header2 is zero) and has no NPC objects or
script triggers. Surface battles remain possible.

Town objects are ten unconditional entries000–009. The mine's ten trigger rows
select021 twice,029 twice,022 twice,023 four times. Entry021 and029 give hidden
passage hints. Entry022 includes the ceiling ambush and another passage hint.
Entry023 is the monster source confrontation, sets2c, and uses
`#Q 25 33 0a` to return to map10 at x37,y51. Unlike tile exits, #Q stores x,y and
a direct map ID. No new party member joins.

Town flag33 activates the investigation party triad081016–018; assignment29
activates013–015 and victory2c activates019–021. Each is called through the
appropriate speaker dispatcher082043–051. The one-time Ray Ball gift sets2a,
including inventory-full010 and repeat020; victory alternatives024–028 remain
reachable. Shop menus preserve all buy/leave/retry/insufficient-funds branches.

## Coverage and integration

`r07_flow.py` retains every R06 root, adds town/mine roots and the new story flags,
and guards the boss, gift, engine, return and shared-call commands. The proposed
name records are Byuto map10 at1131d (12 bytes, pointer10454), Kainan town46 at
1149e (11 bytes, pointer1049c), and mine97 at11706 (8 bytes, pointer10502).
Pointers use base10000 and the latter mine title begins with two spaces; the
other titles begin with space and `>`. A scan through1055c finds no other aliases
into these allocations. Existing R06 star/landing names cover M861 and Byuto;
existing R03 equipment names cover the engine and equipment merchandise.

Town46 also has two exits into the shared bar map2, at x99,y2. Independent QA floods the nonzero tile component from99,2 (tile49,1):167
tiles, bounds x41–53/y0–12, containing exactly053039–043. These five roots
and their existing speaker headers are included. No ordinary later-story bar room is inferred from
bank adjacency.

All scenes use already-supported dialogue, narration, menus, party headers and
shared calls. New shared calls must join the reviewed call dictionary in the
profile, and new text must join its guarded edit allowlist. Name insertion uses
the existing marker-aware guarded name mechanism. No progression command or
map metadata patch is required.


The final static closure has319 entries, with54 newly text-bearing scripts over
R06. Byuto surface10 and mine97 encounter tables contain sprites19/1c/1d/1e/80/6e
(hex). Their profile type bytes are2/3/2/2/9/2, respectively, so none can select
the later Karma defeat message's type8/type10 predicate. The R06 flagfb-gated
boarding encounter remains later state. Source hash, route closure, map rows,
terminal debrief edge, missing dependency rejection and profile types have
focused regression checks in `tests/test_alshark_r07_flow.py`.

## Enemy actions and menu rectangles

The six new encounter profiles do not introduce a new ability-name lookup.
Resident5ee3–5efc copies profile offsets0d–10 into runtime enemy offsets23–26.
Routine6b1a chooses one of these four action bytes and stores it at1c93;
6b76–6b96 and6bc9–6bec use that value to index the binary action descriptor
table20c8. The observed action IDs0e/0f/10/7a/69/6a are not offsets into the
separate ability-name table10300. Their descriptors are respectively2212,23e7,
2216,2360,2324,2329. Profile offsets13–16 supply the companion animation index.
The special-action category dispatches through6c36 to6d2f, which runs animation
9214, sound160d, and effect6f34;6f34 again reads descriptor20c8 and dispatches
its effect. No text renderer is introduced by selecting these IDs. Existing
battle menus, reward/level-up, targeting and reload inventory remain cumulative;
actual combat frames still require runtime verification.

The town tool menu's original `?N 06 02 0b 0c 0d` provides6 columns and2 rows;
its equipment menu `?N 05 03 0f 10 11 12` provides5 columns and3 rows. Reviewed
TOOLS/LEAVE and ARMS/ARMOR/LEAVE labels fit those rectangles. The R07 menu hook
validates adapted row counts/widths and source/output command preservation,
returning an empty patch list. It never changes the width or option ordering.
Five route/menu tests and three name guard/preservation tests pass against the
original images. Combined adaptation compilation remains an integration check.
