# R03 independent editorial review

QA reviewed the original Japanese tokens in the R02 source catalog directly against the new English packets, reading connected conversations in full. No source catalog is published here.

The 26-record spaceport packet preserves the ticket frustrations, three-day delay, widow's lost travel companion, sibling embarrassment, proposed retirement and all turns of Joe's unfinished scrap-built ship reveal. QA requested correction of entry006's ungrammatical standby wording, entry018's dangling one-word continuation page, and punctuation in entry016. The localizer corrected these in `adaptations-r03-spaceport.json` and added explicit omission notes for the planet contempt in008, aimless travel in024, and the shortened unfinished-ship reluctance/internal aside in029. The current port packet is editorially acceptable; manager integration must retain current fingerprints and compile all scenes.

QA independently reviewed the manager's three location canonical/adaptation records. Cockpit→BRIDGE labels the same control room; Hom Spaceport→HOM PORT retains the planet; Abandoned Mine→MINE omits the qualifier, which remains in dialogue and canonical text. These changes and source allocation constraints are explicitly documented in the adaptation notes. The manager separately reviewed QA's technical name adapter.

The 11-record mine/ship canonical packet covers the new party hints, machinery and lever, open-door repeat, full naming conversation, and three immediate bridge crew lines. QA identified one comic timing defect: Shoko's first insult in031 must be simply “How tacky!” rather than “What a tacky name!” because Joe initially thinks she is insulting the ship. The subsequent line clarifies that it is the name she dislikes. The localizer corrected canonical and adaptation together to “How tacky!” / HOW TACKY!. The rest of the packet preserves the original meanings, including the naming hesitation and the direction north of Hamack. The final 11 adaptations were reviewed against canonical text and immutable name-token positions and approved.

The 23-record ship UI packet was also independently reviewed: five Opening menu/selector strings and 18 Joe message strings preserve actions, failure conditions, tone, and protected item/amount/choice fields. No editorial correction was required.

This editorial review is independent of static fitting and does not establish runtime display, navigation or menu behavior.


QA also found the extra ship-equipment unload warning at System `0x209a`; its source meaning is that the selected equipment is too heavy to carry personally, rather than merely an inventory-capacity failure. QA approved the added record's canonical English and HEY! THAT'S / TOO HEAVY TO / CARRY! adaptation, including its preserved Joe header.
