# R05 Zajil surface and Saibal investigation

Read-only inspection of original hash-guarded images, 2026-09-28. Full Japanese
source stays in `work/r05-re-route-packet.json`. The cumulative baseline is
`work/r05-baseline-catalog.json`, including the September 24 bridge-menu fixes.
This is static discovery, not a played route or an assertion of timing.

## Entry, progression and boundary

CS Station30's border `0a 23 63` enters map9 at (35,99). Map9 is **Planet
Zajil**, despite the station dialogue describing its orbit as Mars. Preserve
that discrepancy as source evidence; do not invent an intervening flight.
The name pointer at10452 resolves to11311. The map descriptor at4599 is
`01 43 03 01`, System86800, bank082000. No objects or tile script triggers
exist on this surface.

Exit rows hold x,y,**target map plus one**,destination x,y. Original handler
0d38 loads the third byte;125a subtracts one. Consequently map9 reaches:

| Trigger | Destination | Metadata | Bank |
| --- | --- | --- | --- |
| (50,28) | Zajil Port41, (17,62) | System8e800 | 05f000 |
| (55,34) | Saibal53, (31,126) | System91800 | 05b000 |
| (111,118) | Porkin50, (31,62) | System90c00 | 05a000 |

The source boundary is the complete Saibal investigation, guard confrontation,
syndicate interrogation, hotel kidnapping and immediate party responses, before
pursuing Tomyu at Porkin. Initial Porkin and port interactions are included as
optional surface detours. After kidnapping, interacting with Tomyu's newly
visible object014 begins the next pursuit; it is outside this section. Taking
an interplanetary bus also leaves the section: ticket sales, boarding choices,
no-ticket branches and departure narration are covered, destination maps are not.
Flight/ship combat is a separate action beyond this surface section.

Saibal object015 tests briefing flag16 and dispatches034, whose battle command
is `?F 08 01 00 ff ff 13`. It removes visibility11. Object018 performs the
interrogation, sets story17 and repeats via037. Hotel021 preserves payment,
refusal, insufficient-funds and ordinary-stay paths; flag17 selects035, the
kidnapping. That scene removes Shoko, enables visibility43/44, clears12/13/fa,
and sets story18. Flag1a's later reunion morning036 is outside this interval.
Porkin initial guard005 selects018 at flag16 and runs the same fight, clearing
visibility14. Tomyu014 instead uses visibility43/44 enabled by kidnapping;
its fight sets19 and opens the later interrogation/postvictory network. Those
are excluded by the explicit pursuit boundary, not by adjacency or difficulty.

## Complete static inventory

`r05_flow.py` contains 168 entries, 139 text-bearing records and 40 exact #P
edges. Relative to the baseline, 98 text records require new adaptations.
Roots cover Saibal000–016/018, its bar029–034, initial Porkin000–011/013/015/016,
Zajil Port000–007, the five established party TALK dispatchers, and bridge
objects as cumulative conservative coverage. Control-only nodes and every
choice/menu/shop-failure branch remain in the closure.

Saibal's two doors enter shared bar2 at(67,2). The independently repeated
nonzero-tile flood fill reaches a 236-tile component bounded x21–37,y0–13,
containing exactly053000:029–034. Prior R02 collision evidence proves the
zero-tile gaps block passage. Other bar partitions are not connected to this
entrance. See the independent QA inventory for the actual object coordinates.

State bounds add17/18 to R04's cumulative flags. They retain all earlier
branches conservatively. Party flag17 routes Shoko033→081000003,
Joe034→081000004 and Welda035→081000005; flag18 routes Joe036→081000006 and
Welda037→081000007. The caller's preceding name header proves each speaker.
Port conditional later visibility5d objects088 remain outside this state.

Map9 header byte2 is zero: the surface wraps instead of taking its nominal
border target15. QA independently traced f6df's three LODSB reads, with byte2
stored at1a15 by f6e8. Each direction's movement handler tests this mode;
zero-mode goes through wrapping, e.g.110a→1129→1139, without bounded-border
111f. Thus the header's map15 fallback is not a reachable ordinary border exit.
This is a mode proof, not an assumption that the terrain edges are sealed.

## UI, services, battle and labels

Saibal/Porkin shop menus, inventory-full, insufficient funds, refusal and repeat
responses are explicit script dependencies. Item names include ticket9d/9f and
all offered equipment; the cumulative R03 equipment adapter is required.
The shared scrap exchange057000033 is new visible text. Its `?I06` dispatcher
atdd4d selectsdf0f: key input changes existing credit/scrap numeric fields,
checks balance, supports acceleration and redraws via b8f9/0310. No additional
inline narrative string appears in df0f–dfac. Its instructional text is in033.

The two initial scripted battles have identical `?F` payloads. Dispatch table
maps ?F toe16c; e179 stores battle selector80, and e1df calls the established
battle loop6197. Action processing6197→6290, victory61d8→7836 and defeat
6219→e15c use cumulative on-foot combat/results/reload surfaces. The R01
source audit established graphical targeting and numeric damage/status feedback,
without a named-enemy selection caption. Independent QA found three required Welda abilities, now added below. Combat animation,
encounter balance and runtime traversal remain untested.

Four new map labels have guarded adapters in `r05_names.py`:

| Map | Text allocation | Pointer | English |
| --- | --- | --- | --- |
| 9 | 11311,12 bytes | 10452 | ZAJIL |
| 41 | 1145e,14 bytes | 10492 | ZAJIL PORT |
| 50 | 114c9,12 bytes | 104a4 | PORKIN |
| 53 | 114eb,12 bytes | 104aa | SAIBAL |

Each has one alias. The adapter guards the original ` >` prefix and uses the
existing reviewed 12-cell centering adapter for the displayed label. It guards
original hashes, all pointer aliases, limits, pool conflicts (including R04),
complete label selection and reviewed spellings. Existing bar2 label remains
cumulative. All other name references in script are established party headers.

Welda's actor5 profile1b65→1877 equips combat abilities25/26 and field61.
These require Mental Recovery / Mental Attack / Mental Recovery labels. Original
allocations11100,11109,111ae each have9 bytes. Their respective pointer aliases
are1032e/10330/10332,10334,and10376/10378/1037a. The R05 adapter includes all
three groups with eight-cell ASCII bounds. Alias IDs23/24 and59/60 share the
same original names; all aliases are preserved. Class9's learning table has
zero entries, so no additional level-up abilities arise from this profile.
Canonical labels do not imply an unverified HP/MP effect.

## Five-row letter and exchange display

Both the kidnapping letter035 and exchange instruction033 use repeated control34
with original color controls. Handlerf360 sets1d51 and attributes, **not the
cursor**. Existing layout validation already tracks five physical rows0–4 and
14 columns, allowing explicit newlines inside reviewed text tokens. Original
clear/wait/header/color commands must remain unchanged. No new renderer adapter
or relaxed row bound is needed; extra continuation pages inside header mode
remain forbidden. Source-backed pure shared headers05b017,05f019 and053035–037
all have shape clear/header/text/body/end and may be registered as known
attribute resets for ordinary continuation pages in callers.

## Validation

Six focused tests pass: bounded dependency closure and later exclusions,
original map decoding and wrapping-mode byte, source mutation/missing-target
rejection, seven name pools with byte-change boundaries, unknown aliases and
partial/unreviewed names. Final adaptation fit, cumulative image preservation,
independent QA and emulator traversal are separate integration obligations.


## Verified scrap exchange controls

The correct controls are **8 / up sells one scrap for five credits** and
**2 / down buys one scrap for five credits**. The source diagram places the
8 key with the upward conversion from scrap to credits and the 2 key with the
downward conversion. This is verified against the interpreter, not inferred
from the order of extracted text spans.

The ordinary payment command #F enters da7a, compares its amount against
19f1/19f3, then calls da0d to subtract that amount. Saibal hotel021's original
`#F 01 02 16` charges its stated twenty credits, establishing those fields as
credits. Exchange handler df26 loads CX/BH from19ee/19f0 (scrap) and DX/BL
from19f1/19f3 (credits). Direction bit1 selects df98, which subtracts one scrap
and adds five credits; direction bit2 selects df82, which subtracts five credits
and adds one scrap. Both helpers check available balance before exchanging.

Input helper e6be polls INT41 service8 and stores its state in3474 on every
loop. The exchange tests bit20 of that state and invokes the conversion helper
five times instead of once while it is set. Thus **hold Space to speed up** is
supported by the source: this is a held-state accelerator, not a toggle. The
English adaptation must preserve these directions and the five-to-one rate.
