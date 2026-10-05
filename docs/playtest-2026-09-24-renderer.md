# September24 narration and caption renderer corrections

The original immutable System image, R04 final catalog and Desktop screenshots
11.20.34,11.24.40,11.58.25 and12.04.32 establish two separate faults.

## Shared cursor, not independent headers

At original Systemf360, control34 executes `C606511D01 BB0A05 E973FF`.
It sets the header/delay flag and display attributes; it does **not** move or
reset the cursor. Control35 atf33f clears that flag and falls into newline
handlerf344. Only clear5f establishes a fresh top-of-window cursor.

The old validator reset its cursor at both34 and35. It consequently approved
caption fragments which the real interpreter concatenates. The affected source
records are052000:041 (hotel healing),053000:001 (dancer), and052000:013
(Jane's name-entry prompt). The first two contain repeated34+36 within one
caption; screenshots show the fragments run together and overrun the border.
Their source controls can remain immutable: explicit English newlines at the
span boundaries fix the layout. Jane likewise needs its original separating
newline restored before the next header/prompt sequence.

`layout.py` now models the actual shared cursor. Control34 preserves row/column;
35 advances a row;5f alone resets. The window has five physical rows, normally
one header and four body rows, also shown by the Jane screenshot. A direct
composed-dialogue audit of all240 adapted script records in the595-record R04
catalog identifies exactly those three failures. Branch composition and the
revised final catalog remain integration checks.

## Narration colour is line-scoped in the original interpreter

Dispatch tablef4ba maps36 to handlerf371, `BB0D09 E967FF`: it selectsBX090d
through interrupt41 attribute service7. Source narration repeats this control
at each Japanese source line. The screenshots identify its visible appearance
as cyan/blue. The intended style is a consistent narration style, including
runtime names when they occur inside that line; it is not selective emphasis
on words such as “IN”, “MUTATES” or the possessive afterKaru.

Explicit newline40 entersf344: `8B3E561D 81C70005 E97EFF`. It advancesDI,
then enters shared state initialization atf2cd, eventually setting default
attributesBX050f atf2db. Automatic source-line wrap also takes this path.
English reflow inserted newlines inside original36 text spans without reissuing
36; later immutable36 tokens switch it back. This exactly produces the mixed
cyan/white words in the rescue and biojunk screenshots. Runtime name substitution
atf38d does not independently reset attributes; it does take the same newline
path if its rendered width wraps. Bounded layout must therefore avoid unintended
wrapping, including inserted names.

`playtest_narration.encode_text` supplies an explicit compiler option which
encodes translated newlines as `40 36` while source narration36 is active.
Default, item/emphasis and other colours keep their existing encoding. This
restores the original narration attributes after English reflow; original
commands, controls, names, pointers and allocations remain unchanged. Existing
R04 continuation pages already encode `30 5f 36`, restoring the same narration
attributes after a clear. Guarded integration must check allocation growth and
source handlers; adding colour-restoration bytes is not permission to enlarge
an allocation or move an opaque suffix.

Sixteen focused cursor/pagination/narration tests pass, including rejection of
the old caption overflow, five-row accounting, per-newline narration restoration
and unchanged other-colour encoding. Final rebuilt-image tests and user emulator
verification remain separate. No original image or live emulator was changed.

The shared compiler integration now opts in only its selected reviewed script
records through `import_disk(..., narration_entries=selected)`. The generic
importer and `rebuild_entry` retain their default encoding when this option is
absent. The importer rejects IDs outside the editable source scope and checks
the original renderer before enabling restoration. Translation-only editing,
allocation limits and opaque suffix positions remain enforced by the existing
rebuilder. Twenty-two focused tests pass including original-disk confinement,
exact `@6`/`0_6` bytes, default behavior, immutable-command rejection and an
allocation that must fail after adding the restoration byte.

## Shared-call line origin and directed machine execution

The pickup suffix exposed a second shared-call detail: original #P handlerda3f
callsf2cd atda63 withDI unchanged. That initializer stores the currentDI as the
newline origin1d56. Consequently a newline **inside** the shared FOUND suffix
starts below the item-name end, not at the box's left edge. The corrected four
pickup callers051000:034–037 end their own labels with a newline **before**
calling051000:041; the suffix now contains FOUND without a leading newline.
The composed layout stream marks each #P origin change and tracks its absolute
column, so a future suffix cannot silently overrun the physical box.

Five directed machine tests in `tests/test_alshark_playtest_machine.py` execute
original16-bit x86 interpreter bytes under Unicorn2.1.4. The sandbox process
terminated on JIT startup; isolated execution outside the sandbox succeeded.
Original image files and emulator state remain untouched. The tests verify:

- Original34 appends at the existing cursor; runtime names retain narration attributes.
- Originalnewline resets090d to050f; inserted36 restores090d.
- Wait/clear/restore30,5f,36 restarts the next page in090d.
- Actual #P reproduces the old FOUND indentation at column4 afterMEDS, while
  newline-before-call places it at column0.
- The original native renderer from System1b0b1 executes in its7000-segment
  overlay: literalASCIIspace advances two cells and`>` one. CAMP>KIT and
  SUBM>GUN occupy8cells; SAXEN>CANYON andBASEMENT>BAR occupy12;
  >PLANET>HOM occupies11; the intentional two-space JOE prefix startsJ at4.

The harness mocks platform glyph mapping/drawing and stubs disk loading, input
wait and box drawing. Cursor, attributes, native spacing and #P interpreter
instructions execute unchanged. This is stronger than a layout simulation but
is not a screenshot or full-game traversal. Ignored machine evidence is saved
at `work/playtest-machine-results.json`. The frozen
`work/playtest-2026-09-24-final-catalog.json` independently passes all596 adapted
records;47 focused non-JIT tests also pass after shared-call integration.
