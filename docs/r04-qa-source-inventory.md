# R04 independent source inventory

QA independently inspected the original System image and R03 catalog. This is static source evidence; no route traversal is claimed. The proposed connected scope begins at the R03 cockpit trigger, follows the rescue aboard the civilian ship, and includes the ensuing station induction and tour. The manager owns the final endpoint and must include state-dependent text available there.

## Connected route and boundary

`083000:000` calls `054000:032` while flag14 is unset. The rescue introduction ends with `#Q 34 3c 68`, entering map104. Its original map descriptor is `01 4f 02 01`, pointing to System `0x9e400`, with bank055000. Its four trigger rows refer to entries001,002,003,000; these are not four adjacent independent scenes. Entry001 explicitly jumps to004 after the overheard conversation and animation. Entry004 is a substantial continuous confrontation, hostage rescue and escort scene. It sets flag14, invokes `?I05 1e00`, and ends `#Q09 0a1e` to map30.

Map30's descriptor selects System `0x8bc00` and bank05c000. Its arrival trigger is `(09,0a,0a,01,00)`, so the resulting recruitment conversation001 is a required dependency of the rescue. Stopping at the last line of055000:004 would omit this transition. Entry001 sets flag15. The station tour exposes operator, scientist, guard, secretary and Roy interactions, including a yes/no explanation of the station acronym. Tour flags23/24/25 gate entry014, which raises flag26 and directs the party to the commander's private room. Entry009 dispatches into05d000:000, the first mission briefing, which sets flag16. A before-briefing endpoint is defensible if explicit; an after-briefing endpoint requires changed station/bridge/party interactions as well.

Map104's eleven metadata objects have zero in the normal script-index field and values10–13 in the visibility field; they must not be interpreted as missing bank055000 entries010–013. Ordinary exits are absent. Map30's eighteen metadata objects and arrival trigger need visibility/state filtering; bank adjacency alone would incorrectly include much later missions and station escape/game-over branches.

## Names and party dispatch

Two newly encountered map labels have independent original source evidence:

| Map | Pointer | Original span including NUL | Aliases |
| --- | --- | --- | --- |
| 30, station | `0x1047c` | `0x113fb`, 10 bytes | One |
| 104, ship interior | `0x10510` | `0x11751`, 8 bytes | 22 exact pointers |

The ship-interior title aliases occupy `0x10510..0x10530` and `0x10536..0x1053e`, each in steps of two. The original title has two leading spaces; the station title has one leading space. A guarded shared allocation must preserve these source markers and aliases, and leave the progression table beginning0x1055c intact. Welda's shared name IDs08/09 are absent from the R03 catalog's exported name records and require explicit adapter/editorial coverage. The rescue narration identifies her as female and over two metres tall; gruff speech does not change those pronouns.

Party TALK adds Welda root082000:003 to the earlier party roots. After flag15, Shoko dispatches028→07d000:031 and Joe029→07d000:030. After flag16, Shoko030→081000:001, Joe031→081000:002 and Welda032→081000:000. Welda's pre16 base bark is in082000:003 itself. Excluding the new party root would miss reachable English coverage even with all station NPCs translated.

## Open verification work

RE must prove the invoked animation routines' text dependencies, station movement/visibility and endpoint state. Name/runtime widths, native menu calls, shared headers, save/load and prior bridge services remain inventory domains, not assumptions closed by translating the story records. QA will compare the final bounded source closure to the machine-readable release requirements and independently review canonical/adapted text before examining a frozen cumulative candidate.

## Final source-bound scope review

RE's completed map/animation evidence and guarded closure are consistent with the independent inventory. The closure has85 entries,67 text-bearing records and41 newly adapted dialogue records. Station border metadata is `0a 23 63`, selecting map9 at(35,99); therefore the endpoint is after the first briefing and station follow-ups, before walking out of CS Station. Bridge flag16 responses are conservative bonus coverage. Map104's nominal border selects already translated Dust98; the static audit does not claim that border is physically accessible or blocked.

The four variable-count station `#A` commands correctly require flags23/24/25 and reach summons014. No new shop, item award, battle-initiation or `?V` command appears in the bounded closure. RE inspected the invoked entity/display selector handlers; narrative remains in ordinary script records. Four flow tests pass. Save/load and bridge services retain cumulative earlier coverage. This closes static discovery for the declared interval; movement, display timing and runtime route traversal remain separate unverified checks.
