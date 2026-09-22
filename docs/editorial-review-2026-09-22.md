# Alshark editorial review — 2026-09-22

All previously drafted English through the expanded-menu build has been reviewed against the original PC-98 source and available branch/playtest context. This is an editorial deliverable, not a new ROM build. Existing game text and saves are unchanged.

## Coverage and outcome

| Category | Reviewed units |
| --- | ---: |
| Dialogue/branch/pickup entries | 32 |
| Menu/UI/item/location strings, including both startup copies | 29 |
| Shared short/full names and town label | 13 |
| Fixed battle reward and level-up scripts | 2 |
| **Total** | **76** |

These are storage/semantic units, not individual spoken lines. The breakfast entry alone contains ten turns and a farewell. Related branch alternatives were read together, without pretending adjacent NPC entries are one conversation. The review also read untranslated neighboring entries for context; it does not claim to translate the entire town, cinematic or later chapter. No individual ability names had been translated in the reviewed builds.

Canonical English below is unrestricted by encoding, byte capacity or box size. Brace references identify dynamic values or deliberately unresolved glossary terms; they are not intended to appear literally in the game. Full Japanese source and raw bytes remain in the ignored local catalog.

## Changes to prioritize

1. **Preserve voice and meaning:** fix the opening vocative, restore the expedition group, Jido’s rare/tentative day off, Shoko’s “borrowed” guns and Karu’s actual question.
2. **Restore story information:** radioactive waste, western Hamack, breeding insects, directions and hearsay qualifiers. Do not turn reported news or similes into established facts.
3. **Clarify UI:** identify the User Disk in Format, distinguish owner/recipient selection, name Formation clearly, and express inability to use abilities without asserting none are known.
4. **Keep identity:** full-name slots and Scrap Joe’s epithet need canonical forms independent of short display names. The shared Sion/Lucia surname remains unresolved.
5. **Resolve terms through context:** medical item, Protector equipment type, Gigi classification, Drb expansion, and provisional faction/location spellings.

**Explicit fitting blockers:** the lake warning and Karu’s diagnostic conversation cannot be approved as the current telegraphic adaptations. Their four-row/14-cell layout needs engineering investigation. Other canonical text still awaits technical adaptation; an editorial judgment is not a proof of fit.

## Review status

- `needs_adaptation`: 46 units.
- `acceptable_provisional`: 22 units.
- `DOES_NOT_FIT`: 2 units.
- `needs_context`: 6 units.

`acceptable_provisional` means the existing short form is defensible in context, not that it has been promoted to canonical wording or reinserted by the new workflow. `needs_adaptation` includes both substantive corrections and completing the separate fitting pass. `needs_context` keeps an unresolved interpretation explicit.

## Reproduce the local reviewed catalog

```sh
python3 profiles/alshark/localization_tool.py export /path/to/original work/review-source-catalog.json
python3 profiles/alshark/localization_tool.py apply-review /path/to/original work/review-source-catalog.json \
  --review-pack profiles/alshark/editorial-review.json --output work/editorial-reviewed.json
```

The English-only review pack is versioned. It identifies original source through hashes/fingerprints, and hydration checks those before attaching the canonical English to the local raw-source catalog. The reviewed catalog deliberately cannot build yet: it contains pending adaptations and explicit fitting blockers. Do not bypass those states by pasting canonical strings directly into legacy patch files.

## Canonical script and findings

### story-breakfast

Establish family warmth, Sion's curiosity, Joe's connection to the family, and Lucia's prohibition.

**State:** Before the meteor expedition leaves; before Shoko joins.

#### script:051000:000

**Canonical English**

> Lucia: Have you finished eating already, dear?
> Jido: Yes. I'm going with Mamon and the others to investigate the meteor that fell yesterday.
> Sion: You're so lucky! I want to see the meteor too!
> Lucia: Hee hee... No, Sion. You're still too young.
> Jido: Oh, Sion. It looks like I can finally take a day off tomorrow. Shall I take you to see Joe?
> Sion: Joe? You mean Uncle Joe, who lives in Dust?
> Lucia: Oh, you remember him, Sion? He used to spend a lot of time playing with you.
> Sion: Of course I remember! He made all sorts of toys for me out of scrap.
> Sion: I like Uncle Joe!
> Jido: Joe will be glad to hear that. Well, I'd better get going.

**Review of current adaptation**

- Existing draft loses Mamon “and the others,” the rarity/tentativeness of Jido's day off, and some affectionate/playful delivery.
- “YOU REMEMBER SION?” is an ambiguous vocative. Make the remembered person explicit: “You remember him, Sion?”
- The final response means Joe would be happy to hear Sion likes him. Jido then announces his own departure; these are not unrelated stock phrases.
- Keep “Uncle Joe” as Sion's familiar address, without asserting biological kinship.

#### script:051000:001

**Canonical English**

> Lucia: Sion, you can go out and play, but you are absolutely not to go and see that meteor!

**Review of current adaptation**

- “GO PLAY, BUT STAY AWAY FROM THE METEOR!” retains the main instruction, but canonical English should preserve the explicit permission/firm prohibition contrast.

### story-shoko-invitation

Establish Shoko's frustration at being treated as a child, her initiative, Sion's caution, and the borrowed weapons.

**State:** Before departure; invitation, acceptance/refusal, then a possible repeat invitation.

Branch: Entry 002 offers choice targets 011 (accept) and 012 (refuse). Entry 013 offers the same choice again. Do not read 011 then 012 as one conversation.

#### script:051000:002

**Canonical English**

> Shoko: Oh, hello, Sion. That meteor last night was something, wasn't it?
> Shoko: Dad said he was going to investigate it this morning, so I asked him to take me along. And he just said, “No!”
> Shoko: I'm eighteen, and he still treats me like a child! Honestly!
> Shoko: Say, why don't we go together?

**Review of current adaptation**

- The draft keeps the facts but turns an expressive complaint into a report. Restore the quoted refusal and indignation.
- Eighteen is explicit; do not write Shoko as a small child.

#### script:051000:011

**Canonical English**

> Shoko: Then it's settled! What's wrong?
> Sion: Well... I was just thinking about all the Gigi in Saxen Canyon...
> Shoko: We'll be fine. Look.
> Sion: That's a handgun! What are you doing with that?!
> Shoko: Hee hee... I just “borrowed” them from Dad's drawer. There are two, so we can protect ourselves.
> Shoko: Come on, let's go!

**Review of current adaptation**

- “I TOOK TWO FROM DAD” loses both the drawer and the knowingly euphemistic “borrowed.” This is characterization, not expendable filler.
- Do not imply she received permission or that Dad handed the guns to her.
- The handgun reveal is an exclamation followed by an alarmed question; retain the reaction across the highlighted item name.

#### script:051000:012

**Canonical English**

> Shoko: What? You coward... Some man you are!

**Review of current adaptation**

- Current “YOU COWARD! SOME MAN YOU ARE!” conveys the intended sting. Do not neutralize the taunt or invent stronger abuse.

#### script:051000:013

**Canonical English**

> Shoko: Hee hee... Changed your mind? You want to go after all, don't you?

**Review of current adaptation**

- “SO, YOU WANT TO GO NOW?” preserves the question but loses her knowing amusement and “after all.”

### story-young-man

Provide expedition information, then react to Sion's changed appearance.

**State:** Entry 003 before the expedition aftermath; conditional alternative 020 later.

Branch: Entry 003 has a conditional branch to 020. These are different story states.

#### script:051000:003

**Canonical English**

> Young man: Hey, Sion. That meteor last night was something, huh? Looks like my dad went to Saxen Canyon with Dr. Penrose and the others to investigate it.

**Review of current adaptation**

- Restore “looks like” and “the others”: the draft makes secondhand news categorical and reduces the group to two people.
- The source speaker label is Young Man, not a named character. Dr. Penrose is not a separate new canonical name without cross-checking shared names.

#### script:051000:020

**Canonical English**

> Young man: What's wrong? You look pale. Did something happen?

**Review of current adaptation**

- The current draft is a reasonable concise adaptation; canonical restores the opening concern.

### story-war-news

Convey secondhand news of war and anxiety about the world.

**State:** Ambient town conversation; no exact flag prerequisite established.

#### script:051000:004

**Canonical English**

> Old woman: I hear war has finally broken out between the Kingdom of {faction.wyuria} and the {faction.zolias} Empire. What a dangerous world we live in.

**Review of current adaptation**

- The draft drops Kingdom/Empire, the reported nature of the news, and the sense that the conflict has finally broken out.
- The braces deliberately defer uncertain English spellings to the glossary. Existing WYURIA/ZOLIAS are not official romanizations.
- Unresolved: Romanizations remain unresolved; the source explicitly distinguishes a kingdom and an empire.

### story-pollution

Connect development and greenery with a specific radioactive-waste warning.

**State:** Ambient town conversation.

#### script:051000:006

**Canonical English**

> Woman: So much of Hom has been developed now, and it's getting greener. But I hear the area around Hamack, the town to the west, is contaminated with radioactive waste.
> Woman: Especially Dust, the waste-disposal site. They say it's full of Gigi that have mutated and become vicious.

**Review of current adaptation**

- Restore radioactive waste, Hamack's western location, development on Hom, and reported rather than firsthand knowledge.
- Mutations making Gigi vicious matter; “MUTANT GIGI RUN WILD” is compressed but does not explain the relationship as clearly.
- Do not call the development terraforming or say greenery caused the mutations; those mechanisms are not established here.
- Unresolved: Hamack spelling remains provisional; Gigi's exact creature classification remains open.

### story-lake-warning

Friendly observation about greenery followed by a reported local danger.

**State:** Ambient town conversation.

#### script:051000:007

**Canonical English**

> Young woman: It's nice to see so much more greenery lately. But I hear there are lots of large insects breeding near the lake, and it's dangerous out there.

**Review of current adaptation**

- Current text loses the positive opening, breeding, abundance and hearsay; it sounds like a list of facts.
- The speaker is labeled a young woman, distinct from the girl in entry 009.
- Do not imply the vegetation itself causes monsters.
- `DOES_NOT_FIT`: The current single four-row, 14-cell body cannot naturally retain the positive observation, breeding insects and reported danger. Add display space/pages or narrower rendering rather than reducing the canonical line to fragments.

### story-wasteland-and-return

Warn about creatures outside town; later report seeing Sion's mother leave.

**State:** Entry 008 before the return-state branch; 021 after the relevant story flag.

Branch: Entry 008 conditionally branches to 021; these are not consecutive lines.

#### script:051000:008

**Canonical English**

> Old woman: Don't go outside town! There are fearsome insects from the canyon roaming the wasteland.

**Review of current adaptation**

- “CANYON BUGS” can sound like a species name. The source says the insects came from the canyon.

#### script:051000:021

**Canonical English**

> Old woman: Your mother? She wandered out of town in a daze, as though something had possessed her.

**Review of current adaptation**

- The existing adaptation largely retains this meaning. Keep “as if/as though” so the comparison does not become an established supernatural fact.

### story-canyon-directions

Identify the canyon to the north.

**State:** Ambient town conversation.

#### script:051000:009

**Canonical English**

> Girl: Saxen Canyon? That's the big canyon to the north, isn't it?

**Review of current adaptation**

- The draft is close; the full canonical sentence should keep the conversational confirmation.

### story-old-man

Show an older resident anticipating the party's needs and recalling an unprecedented meteor.

**State:** Conditional gift and ambient meteor discussion.

Branch: Entry 005 is a speaker/dispatch entry with conditional routes to 017 and 018; the gift is not automatically followed by the meteor comment.

#### script:051000:005

**Canonical English**

> Old Man

**Review of current adaptation**

- ELDER implies a formal community role that the generic Japanese label does not establish. Prefer Old Man as the canonical label.

#### script:051000:017

**Canonical English**

> Old man: You needn't say a word. I understand. Here, take this Camp Kit with you.

**Review of current adaptation**

- “I KNOW” loses the warm implication that he understands without being told.
- The source gift does not promise unlimited replacements or specify recovery mechanics.

#### script:051000:018

**Canonical English**

> Old man: That meteor seems to have fallen in the canyon north of town. I've lived on Hom for many years, but I've never seen anything like it.

**Review of current adaptation**

- Restore “seems,” north of this town, and his long residence on Hom. The draft presents the location as certain and drops the life-experience context.

### story-karu-diagnostic

Let Karu notice Sion's agitation and ask a suspicious question.

**State:** Diagnostic conversation with a conditional Shoko greeting.

Context: Following return scene 051000:019 has Karu refer to itself by name; Sion identifies it as an older model without image-playback equipment. This supports a measured machine voice, without inventing model details.

Context: 051000:019 establishes limited recall, an older model and absent image-playback equipment; 051000:027 shows Karu agreeing to work alongside Sion.

Branch: Entry 010 can branch to 016; the later return conversation 019 is context only and remains outside the already-translated scope.

#### script:051000:010

**Canonical English**

> Karu: Sion, your heart rate and perspiration are higher than usual. Are you up to something?

**Review of current adaptation**

- “PULSE, SWEAT ABOVE NORMAL. PLOTTING?” is a provisional technical abbreviation, not an acceptable canonical voice.
- Higher than usual is relative to Sion's usual state; do not turn it into a diagnosis of illness.
- The suspicious question can be mildly comic without making Karu accusatory or omniscient.
- `DOES_NOT_FIT`: With SION substituted at the start, the existing four-row/14-cell body and non-clearing wait cannot carry both the complete diagnostic observation and a natural suspicious question. Investigate more display space or narrower Latin text.

#### script:051000:016

**Canonical English**

> Karu: Shoko, how are you?

**Review of current adaptation**

- “HI!” drops the question. The canonical greeting must retain the friendly inquiry.

### story-lucia-rest

Offer rest or express suspicion depending on story state.

**State:** Conditional follow-ups from the initial meteor warning.

Context: 051000:001 branches to 014, which has a conditional route to 015. Recovery commands occur before the farewell in 014.

Branch: 014: rest and send-off; 015: suspicion branch. Do not treat the suspicion as necessarily spoken after resting.

#### script:051000:014

**Canonical English**

> Lucia: Oh my, you both look exhausted. What happened? Come over here and rest a while.
> [After resting]
> Lucia: Off you go, then. Take care!

**Review of current adaptation**

- The existing draft omits her question about what happened.
- The farewell is the conventional send-off for someone leaving; it does not mean Lucia herself is leaving.

#### script:051000:015

**Canonical English**

> Lucia: There's something odd about you two... You're not planning to go and see that meteor, are you?!

**Review of current adaptation**

- The draft communicates the suspicion, but fuller English better preserves the disbelieving, pointed question.

### story-found-items

Name discoveries, preserve shared pickup composition, and distinguish being caught from refusing to take someone else's property.

**State:** Starting-house pickups and related item-taking interactions; separate item branches.

Branch: 034–037 call the shared found suffix at 041. The name and suffix are components of one message, not separate dialogue.

Branch: The Lucia interruption at 061000:019 and refusal at 061000:021 are related interactions, not asserted to follow every pickup.

#### script:051000:034

**Canonical English**

> Survival Knife

**Review of current adaptation**

- KNIFE drops the weapon's identifying qualifier; keep Survival Knife in canonical terminology.

#### script:051000:035

**Canonical English**

> {item.hand_medical}

**Review of current adaptation**

- MEDS is a provisional display label, not a determination that this is loose medicine. Resolve the item's nature before choosing a canonical English name.
- Unresolved: Canonical name unresolved; placeholder is intentional.

#### script:051000:036

**Canonical English**

> {item.protector}

**Review of current adaptation**

- PROTECTOR is a provisional transliteration. Confirm the equipment type before replacing it with a specific armor name.
- Unresolved: Canonical name unresolved; placeholder is intentional.

#### script:051000:037

**Canonical English**

> 80 credits

**Review of current adaptation**

- The source amount is 80; keep the number and currency together in the semantic message. The old line split is technical only.

#### script:051000:041

**Canonical English**

> You found {item_or_amount}.

**Review of current adaptation**

- The source is a suffix. Canonical English describes the complete message, not the fragment “FOUND.”
- A natural adaptation may use “{item} found.” The current engine emits the item first; moving “You found” before it is an engineering change, not a text-only replacement.

#### script:061000:019

**Canonical English**

> Lucia: Sion! What are you doing?!
> Sion: Tch. She caught me.

**Review of current adaptation**

- “WHAT'S GOING ON?” is less direct than Lucia's challenge about what he is doing.
- “BUSTED.” is a plausible colloquial adaptation of being caught, but the canonical line should retain the irritated reaction.

#### script:061000:021

**Canonical English**

> I can't just take someone else's things without asking.

**Review of current adaptation**

- “NOT MINE. CAN'T TAKE IT” conveys the restriction but loses the permission/moral nuance and sounds mechanical.
- Unresolved: This entry clears a speaker header rather than naming a speaker; do not claim a voiced Sion line as established.

### story-work-interactions

Explain inventory capacity and direct the player to the person handling work.

**State:** Work-related branches; not necessarily reachable during the first town visit.

Context: Untranslated surrounding entries 022/023 concern dismissal/pay, and 027 concerns accepting work while Shoko waits at a hotel. These contextual entries are not newly translated in this review.

#### script:051000:024

**Canonical English**

> Oh, it looks like you're carrying too much. Please make some room and come back.

**Review of current adaptation**

- The current draft is too brusque for the polite request and omits coming back. Do not invent a physical bag-count mechanic.

#### script:051000:025

**Canonical English**

> Where on earth have you been?! The woman at the counter was furious!

**Review of current adaptation**

- “The girl at the counter” may imply an age not established by the colloquial address. Use woman unless later context identifies her.
- Keep the past tense: the line reports how she reacted.

#### script:051000:026

**Canonical English**

> Ask the woman at the counter about work.

**Review of current adaptation**

- The old adaptation is serviceable. Canonical English restores the person being referred to.

### story-dead-gigi

Sion notices something odd; Shoko reacts with disgust and presses him to remove it.

**State:** Interaction with a Gigi corpse; exact location not established by this entry.

#### script:051000:028

**Canonical English**

> Sion: Huh? What's a dead Gigi doing here?
> Shoko: Ugh, it's creepy! Hurry up and get rid of it, Sion!
> Sion: All right, all right. I get it.

**Review of current adaptation**

- The draft broadly works, but Shoko's urgency and Sion's resigned response should remain conversational rather than a bare command/acknowledgment.

### ui-menus-and-messages

Keep commands clear, distinguish selection roles, and preserve complete disk instructions.

**State:** Field/battle menus, startup, inventory, formation, saves and loads.

#### ui:Opening:00414d

**Canonical English**

> Data Display
> Status
> Items
> Party
> Equipment
> Abilities
> System

**Review of current adaptation**

- DATA is ambiguous without knowing the display command. Keep its exact behavior flagged; other rows match the normal field menu.

#### ui:Opening:004158

**Canonical English**

> Status
> Items
> Party
> Equipment
> Abilities
> System

**Review of current adaptation**

- Expanded labels are clearer. SKILLS is a constrained synonym for canonical Abilities; keep one canonical category across field and battle.
- PARTY is supported by the actual Talk/Formation submenu, despite the broader Japanese label.

#### ui:Opening:004294

**Canonical English**

> The operation is complete. Put the Data Disk back in drive 2, then press any key.

**Review of current adaptation**

- Restore the completion and “back” information; the draft only gives the disk instruction.

#### ui:Opening:0042d5

**Canonical English**

> System
> Save
> Load
> Text Speed
> Format User Disk

**Review of current adaptation**

- FORMAT hides which disk is affected. The canonical option must explicitly identify the User Disk.
- TEXT opens message speed; Text Speed is clearer. Treat space needed for a clear formatting option as a UI task.

#### ui:Opening:004306

**Canonical English**

> To save your game, insert the User Disk into drive 2, then press any key.

**Review of current adaptation**

- SAVE USER DISK can read as an instruction to save the disk itself. Restore the operation and insertion instruction.

#### ui:Opening:004348

**Canonical English**

> To load your game, insert the User Disk into drive 2, then press any key.

**Review of current adaptation**

- LOAD USER DISK lacks the insertion instruction; canonical should distinguish loading game data from changing disks.

#### ui:Opening:0043f8

**Canonical English**

> Attack
> Abilities
> Items
> Equipment
> Status
> Flee

**Review of current adaptation**

- These are commands/categories, so concise labels are natural English. SKILLS remains a technical adaptation of Abilities, not a change in the canonical mechanic.

#### ui:Opening:004637

**Canonical English**

> Text Speed
> Fast
> Normal
> Slow

**Review of current adaptation**

- NORMAL is an improvement over NORM. Canonical heading should say what speed is being adjusted.

#### ui:Opening:0046ec

**Canonical English**

> There are no items available to equip.

**Review of current adaptation**

- NO GEAR TO EQUIP is a reasonable compact UI adaptation. Do not say the character is unable to equip anything in general.

#### ui:Opening:004aec

**Canonical English**

> There are no items available to equip.

**Review of current adaptation**

- Duplicate message: keep identical terminology and meaning in both storage locations.

#### ui:Opening:0048af

**Canonical English**

> Yes
> No

**Review of current adaptation**

- Expanded YES/NO is appropriate. These options inherit the meaning of the preceding question; do not reinterpret the branch targets.

#### ui:Opening:0048b6

**Canonical English**

> Talk
> Formation

**Review of current adaptation**

- ROW is not a good canonical label for changing party formation. Keep the two commands distinct.

#### ui:Opening:00470c

**Canonical English**

> New Game

**Review of current adaptation**

- START is serviceable but less explicit than New Game.

#### ui:Opening:00471b

**Canonical English**

> Load Game

**Review of current adaptation**

- LOAD is a reasonable constrained menu label.

#### ui:Opening:004b0c

**Canonical English**

> New Game

**Review of current adaptation**

- Second start-menu copy; must agree with the first.

#### ui:Opening:004b1b

**Canonical English**

> Load Game

**Review of current adaptation**

- Second load-menu copy; must agree with the first.

#### ui:System:001d72

**Canonical English**

> Select a character

**Review of current adaptation**

- The source asks “whose?”; this is the owner/subject selector. WHO? loses its distinction from the recipient selector.

#### ui:System:001d7c

**Canonical English**

> Select a recipient

**Review of current adaptation**

- The source asks “to whom?”; keep recipient selection distinct from selecting whose information/equipment to inspect.

#### ui:System:001dac

**Canonical English**

> Current Formation

**Review of current adaptation**

- ORDER is understandable but less specific than the canonical party-formation heading.

#### ui:System:001db7

**Canonical English**

> Change the party formation.

**Review of current adaptation**

- REORDER is a compact instruction, not the full canonical message.

#### ui:System:001dc7

**Canonical English**

> New Formation
> 1
> 2
> 3
> 4
> 5

**Review of current adaptation**

- The numbered positions must remain in order. Do not rename this command as an attack order without evidence.

#### ui:System:001e2b

**Canonical English**

> {character}

**Review of current adaptation**

- Subject component of the following ability-unavailable sentence; Japanese particles have no standalone English equivalent. Keep the runtime name, not an English replacement particle.

#### ui:System:001e2f

**Canonical English**

> cannot use abilities.

**Review of current adaptation**

- Compose with {character} to form a complete sentence. NO SKILLS asserts a lack of skills; the source states inability to use abilities, which is not necessarily the same condition.

#### ui:System:001e98

**Canonical English**

> You are not carrying any items.

**Review of current adaptation**

- NO ITEMS is an acceptable compact system message.

#### ui:System:0107aa

**Canonical English**

> Survival Knife

**Review of current adaptation**

- Use the same canonical weapon name as the pickup; KNIFE remains a constrained adaptation.

#### ui:System:010875

**Canonical English**

> Handgun

**Review of current adaptation**

- GUN is broader than the source; preserve Handgun as the canonical item name.

#### ui:System:010b74

**Canonical English**

> {item.hand_medical}

**Review of current adaptation**

- MEDS is provisional. The source does not by itself settle whether this is medicine, a kit or a device.
- Unresolved: Exact medical-item name unresolved.

#### ui:System:011329

**Canonical English**

> Planet Hom

**Review of current adaptation**

- HOM omits the planet qualifier. Preserve it in canonical location text.

#### ui:System:011723

**Canonical English**

> Saxen Canyon

**Review of current adaptation**

- SAXEN drops the geographic feature; use the full working name consistently.

### reference-shared-names

Keep short names, full names, epithets and location qualifiers distinct.

**State:** Names reused across dialogue and UI; no new story chronology.

#### name:0

**Canonical English**

> Sion

**Review of current adaptation**

- Current given-name form is consistent with the working glossary; no claim of official romanization.

#### name:1

**Canonical English**

> Sion {surname.asmaan}

**Review of current adaptation**

- The original is a full name. Legacy SION discards the surname. Preserve a glossary placeholder until its English spelling is decided.

#### name:2

**Canonical English**

> Shoko

**Review of current adaptation**

- Current given-name form is consistent with the working glossary; no claim of official romanization.

#### name:3

**Canonical English**

> Shoko Penrose

**Review of current adaptation**

- The original full name must not collapse to SHOKO in the canonical layer. Penrose is a working rendering, not a claim of an official spelling.

#### name:4

**Canonical English**

> Karu

**Review of current adaptation**

- Working transliteration remains provisional; use consistently pending contrary evidence.

#### name:6

**Canonical English**

> Joe

**Review of current adaptation**

- Current given-name form is consistent with the working glossary; no claim of official romanization.

#### name:7

**Canonical English**

> Scrap Joe

**Review of current adaptation**

- The full/name-variant source contains the Scrap epithet. JOE currently loses this identifying nickname.

#### name:12

**Canonical English**

> Lucia

**Review of current adaptation**

- Current given-name form is consistent with the working glossary; no claim of official romanization.

#### name:13

**Canonical English**

> Lucia {surname.asmaan}

**Review of current adaptation**

- Restore the shared surname in the canonical full-name slot; romanization unresolved.

#### name:14

**Canonical English**

> Mamon

**Review of current adaptation**

- Current given-name form is consistent with the working glossary; no claim of official romanization.

#### name:15

**Canonical English**

> Mamon Penrose

**Review of current adaptation**

- The original full-name slot contains Penrose. MAMON is only the current constrained form.

#### name:16

**Canonical English**

> Jido

**Review of current adaptation**

- Working romanization remains provisional. Source ID 16 supplies a given name, not a full name.

#### name:81

**Canonical English**

> Town of Cosma

**Review of current adaptation**

- The original location label explicitly identifies a town. COSMA is a shorter display form.

### ui-battle-results

Report gains clearly while keeping all dynamic numeric and character fields.

**State:** Battle rewards and level-up pages.

#### fixed:System:001edf

**Canonical English**

> Each party member gained {experience} experience points.
> Credits gained: {credits}
> Scrap gained: {scrap}

**Review of current adaptation**

- “PARTY GAINS EXP” loses the explicit each-member wording. Make experience distribution clear.
- The Japanese sentence includes “each,” but actual credit/scrap distribution needs a gameplay/code check before describing them as separate per-character awards.
- Keep numeric fields 0, 1 and 2 at their existing byte offsets; this canonical prose is not an insertion recipe.
- Unresolved: Whether credits and scrap are pooled or awarded per member needs mechanics confirmation.

#### fixed:System:001f28

**Canonical English**

> Level up!
> {character}
> PP +{pp_gain}
> MP +{mp_gain}
> IQ +{iq_gain}
> R.Str. +{right_strength_gain}
> L.Str. +{left_strength_gain}
> Agility +{agility_gain}
> {stat.drb} +{drb_gain}
> Stats increased.

**Review of current adaptation**

- PTS is a defensible technical abbreviation; canonical gains should be visibly gains, not current totals.
- Do not expand PP/MP/IQ into guessed mechanics. “Drb” also needs a verified full English stat name; preserve a glossary reference rather than guessing.
- Name substitution, numbers 3–9, page waits, and compact stat-rendering controls must remain intact. Zero gains are valid.
- Unresolved: Full expansion/mechanics of PP, MP, IQ and Drb are not established by this review.

