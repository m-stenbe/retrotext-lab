# R02 Joe disassembly UI

The three original System strings at `0x1e5b` (8 bytes), `0x1e63`
(11 bytes), and `0x1e6e` (42 bytes) are a Joe heading, a disassembly
confirmation, and an item-to-scrap result template. The source allocations
and their pointers remain fixed.

Original code `0xbd55` draws the box, sets DI to `0x4108`, and loads the
heading through `0xbd6b`. Its final newline leaves DI at `0x4608`.
`0xc5e0` loads the result template; `0xc5e6` then explicitly positions the
item name at `0x4608`, and `0xc5f5` positions the amount at `0x4b08`.
The template's first nine cells and second-row first five cells therefore
remain blank for those runtime fields. `0xc601` loads the confirmation at
DI `0x5508`; `0xc607` calls the established yes/no selector.

The resident renderer at `0xf533` recognizes ASCII uppercase letters at
`0xf55c..0xf567`, converts them through `0xf52a`, and uses its normal full
cell glyph renderer. ASCII spaces advance a full cell through `0xf58c`,
and `@` starts the next row through `0xf582`. The new adapter guards the
uppercase conversion instructions and allows compact ASCII uppercase and
spaces only in these three reviewed strings. The question mark retains
full-width CP932 encoding. This uses the existing font without a font patch.

The English confirmation is `SCRAP?`, in the context of the existing
DISASSEMBLE menu action. The result reads `[item] FOR / [amount] SCRAP`;
extra separator spaces follow the unchanged 9/5-cell runtime fields.
The adapter rejects field overlap, extra rows, unsupported characters,
renderer changes and allocation overflow. Actual emulator display and
confirmation behavior still require candidate testing.
