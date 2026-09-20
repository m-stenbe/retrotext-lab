# Alshark translation feasibility audit — 2026-09-20

## Conclusion

Promising, but not yet a low-effort full translation. The opening's readable text
and pointer structure recur widely. The next engineering milestone should be a
command-aware extractor/reinserter, followed by a narrow-font experiment. No
original or playable disk images were changed during this audit.

## Reproducible local findings

Run `python3 profiles/alshark/audit.py /path/to/original --output work/audit`. It reads the six original images and
writes this directory's summary.json, banks.tsv and entries.tsv. Source SHA-256
hashes are recorded. All 48 selected windows reconstruct byte-for-byte from their
pointer-table bytes and extracted entry slices.

- 48 multi-entry table candidates on the System disk at 4 KB boundaries:
  0x51000–0x78000 and 0x7C000–0x83000.
- 2,249 pointer entries; these are event/script entry points, NOT translated
  sentences, pages or words. Some entries are very short commands.
- 1,322 occurrences of the experimentally verified `4 $ <speaker ID> 5` header
  lie in those windows. System has 1,348 occurrences altogether, leaving 26
  outside the selected layout. These counts are byte-pattern observations;
  some occurrences could be inactive data rather than reachable conversations.
- Ending has one occurrence of that pattern; Opening, Data, Visual and User
  have none. Absence does NOT imply no text: menus, anonymous dialogue, graphics
  and other encodings are not covered by this marker.
- Other pointer-shaped patterns occur in graphics-heavy disks and are explicitly
  excluded from the script inventory. 0x79000/0x7A000/0x7B000 have a possible
  single-entry table pointing to an immediate zero; also excluded.
- The output includes raw CP932 diagnostic renderings, retaining visible control
  bytes. These are research extracts, not a clean translation spreadsheet.

## Space: what is and is not established

The selected 4 KB windows contain 11,264 trailing 0xE5 bytes in aggregate. These
are apparent filler, not proven allocatable space. Almost no zero padding occurs
at the ends. Other windows end with readable text, and physical bytes after a
logical terminator can contain residual data. Therefore this audit does not
establish true logical lengths, loader read sizes, or safe expansion limits.

Only the opening scene's existing allocation has been safely reused so far:
493 bytes originally, 455 bytes after the latest English patch. That is a
single deliberately concise translation sample, not evidence that all English
will fit. The pointer structure suggests repacking within a loaded block may
work, but references and event opcodes must be understood before relocating.

## Remaining work and risks

1. Parse command lengths and arguments. A zero byte can occur in a name ID or
   event argument, so splitting every string at zero corrupts the script.
2. Decode display text separately from event commands, including anonymous
   speakers, page continuations, choices, substitutions and branching.
3. Establish bank loading and pointer references. Demonstrate an unchanged
   semantic roundtrip, then test a deliberately longer translated scene with
   subsequent entry pointers updated.
4. Inventory item/equipment/spell names, status/combat/system messages and place
   names outside the event tables. We have already patched shared name pointers,
   but the complete tables and all references are not mapped.
5. Investigate half-width Latin and lowercase. The current uppercase text works
   but occupies full cells, forcing short phrasing and manual line breaks.
   A narrower renderer could improve both readability and translation fidelity;
   it will not automatically increase byte storage capacity.
6. Inspect opening/ending and graphics for additional text. A raw CP932 scan
   cannot prove that all text is found or uncompressed.
7. Test conversations and branches throughout the game, including loading,
   saving and transitions. Disk swapping is a separate usability improvement.

No defensible word count or completion-time estimate yet. The inventory is
already much larger than the breakfast example, but not fully classified.

## External research

Searches used Alshark/PC-98/English translation/patch/project/romhacking and the
Japanese title. No verified released English patch or public Alshark-specific
extraction project was found. This is a search result, not proof of absence.

- Data Crystal lists Alshark under PC-9801/PC-9821 translation requests. The
  search index exposes the row; direct page retrieval returned HTTP 403.
  https://datacrystal.tcrf.net/wiki/Translations_Request_List
- 46 OkuMen's Appareden repository provides a useful primary-source workflow
  example: text extraction, pointer handling, typesetting, reinsertion, graphics
  work, and testing aids. It also documents dictionary compression for that
  game. Its engine/file formats differ; these are design references, not tools
  demonstrated to work on Alshark.
  https://github.com/46OkuMen/appareden
- Generation MSX's 'Alshark (English)' is a translated TITLE field on an
  unreleased MSX2 listing, not evidence of an English game patch.
  https://generation-msx.nl/software/the-right-stuff/alshark/6119

I did not establish a measurable recent increase in popularity. Discussion and
requests establish interest, not audience size or a trend.
