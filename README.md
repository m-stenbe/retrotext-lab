# Retrotext Lab

Experimental tools for researching and translating vintage Japanese computer
games. The first profile targets **Alshark for PC-98**.

The reusable layer detects little-endian relative-pointer tables and splits
candidate blocks losslessly. Game profiles own offsets, encodings, script
commands and patch rules. PC-88/PC-98 hardware alone does not imply compatible
engines. **No other game or PC-88 format is currently supported.**

## Current capabilities

- Alshark structural audit: candidate blocks, entry slices, diagnostic CP932
  text, source hashes and per-disk marker counts.
- Reproducible Alshark demo: START/LOAD menu, breakfast conversation, selected
  shared names and Cosma location title. Builds local images and IPS patches.
- Synthetic tests for table detection and lossless block slicing.

This is not yet a command-aware extractor, general reinserter, or full English
translation. Physical roundtrip validation does not prove safe text relocation.

## Run

Python 3.10+; standard library only. From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 profiles/alshark/audit.py /path/to/original --output work/audit
python3 profiles/alshark/build_demo.py /path/to/original --output work/demo
```

Provide your own original disk images. The demo expects the six filenames and
hashes in `profiles/alshark/SHA256SUMS.txt`. Keep originals separate from outputs.
Run without Python's `-O` flag: the experimental builder uses assertions for
source, allocation and patch validation.

The generated `.cmd` lists Opening and Data. In Neko Project II kai, the opening
later requests System in drive 1 and Data in drive 2; use the generated images.
Choose START for the breakfast scene. Emulator installation and BIOS are separate.
Rebuilding overwrites demo System/Opening outputs, preserving an existing User
disk. Do not rebuild images while the emulator is using them.

No game images, firmware, extracted scripts, screenshots or third-party tools
are distributed here. Keep generated research under ignored `work/`.

## Research and next steps

See [Alshark research](docs/alshark-research.md) for measured findings and limits.
The first inventory has 48 candidate windows, 2,249 pointer entries and 1,322
named-speech markers in those windows. These are not word/page totals.

1. Decode script commands and preserve their arguments exactly.
2. Separate dialogue, choices and substitutions into editable records.
3. Establish loader boundaries and references before relocating text.
4. Build a validated reinsertion pipeline and rendering-width checks.
5. Investigate narrower Latin lettering and lowercase.
6. Map UI, combat and graphics text; test across the game.

Contributions should use synthetic fixtures and identify the game/version each
finding applies to. Do not contribute game images or full extracted scripts.

MIT license for the code and original documentation. Game content and third-party
software remain subject to their respective rights.
