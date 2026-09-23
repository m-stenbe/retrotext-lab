# Optional battle EXP multiplier

`build_demo.py --exp-multiplier 4` makes a separate trainer build. Supported
factors are 1, 2, 4 and 8; the default is 1 and produces unchanged disk bytes.
This option is independent of translation selection. The current test build is
`work/dust-approach-04-xp4-test`, using the same translation and disk-prompt flags
as Dust Approach 04, plus the multiplier flag.

The patch requires an emulated 80386 or later because it uses two 32-bit stores
to clear the same eight bytes as the original four word stores. The player's
current Neko core configuration specifies Intel 80386. No core setting is changed.

## What changes

Each occupied party slot receives `min(base EXP * multiplier, 65535)` instead
of base EXP. Money and scrap are unchanged. Empty slots stay untouched. The
existing character restrictions, level-up routines, random stat growth and
ability checks after the award block remain in place. The original routine
checks for only one level-up per character per award; excess experience may
therefore need further battles to produce additional levels.

The result screen still reads base EXP from the original reward field. When
building with reviewed combat text, the trainer changes its heading to
BASE REWARDS to distinguish the unscaled display. The actual character EXP gets
the multiplier. The per-battle cap prevents the multiplied 16-bit award wrapping.
The game's existing 24-bit cumulative EXP addition is retained exactly, including
its native wrap behavior at the representation limit; this is not an overhaul of
maximum-level or cumulative-EXP handling.

## Reverse-engineering evidence

System 0x5E4F reads the encounter reward and 0x5E50 writes it to 0x1BF4. Credits
and scrap use 0x1BF6 and 0x1BF9. The display selector table at 0xF42D points to
those three fields. The shared award routine at 0x7836 is called from the battle
completion path at 0x61D8 and the alternate reward path at 0xE662. The latter
first copies returned EXP from ES to 0x1BF4 at 0xE652. This patch affects awards
through that shared routine; it does not claim that all possible scripted EXP
sources use it.

The five-slot loop reads IDs at 0x19DB and resolves each nonzero ID through
0x0AD2. Character record offsets 4..6 hold cumulative EXP; byte 3 supplies the
next-level threshold index. The lookup at 0x79B2 returns the threshold in DL:AX.
The unchanged code at 0x789E applies character restrictions and calls the level
routine at 0x79CC, then the existing ability-check path. No code cave, zero-filled
buffer, encounter-selection logic, disk allocation or pointer table is reused.

Only System 0x785E..0x789D is replaced. The same work fits its original 64 bytes:

- XLAT indexes the party table using the unchanged slot index.
- Two 386 dword stores clear exactly the same eight character status bytes.
- Unsigned MUL forms DX:AX. Nonzero high bits saturate the award to 65535.
- The original low-word ADD and high-byte ADC update the same three EXP bytes.
- A low-word compare followed by a high-byte subtract-with-borrow makes the same
  unsigned 24-bit threshold decision, retaining both original exit destinations.

Working registers inside the block are scratch; the original character resolver
and threshold lookup are still called. The patch does not move the stack or
alter loop control or the native level-up code. The original 64-byte code guard
and optional combat-heading guard are checked before any mutation. Reapplying
the patch fails rather than multiplying an already modified build.

## Verification

The machine-code tests use Unicorn to execute both original and replacement
blocks with the original pointer/threshold helpers. They compare character
memory and branch destinations in 1,125 paired cases across all three factors,
including zero awards, 16-bit multiplication boundaries, word carries, exact
thresholds, native 24-bit wrap and deterministic random values. Twenty additional
cases check empty slots across all five positions. Reward/credit/scrap fields,
neighbouring character bytes and the stack are checked as well.

All 65 tests pass with Unicorn installed; two execution tests are explicitly
skipped if that optional test dependency is absent. Install
`requirements-trainer-tests.txt` into a test environment, then run the suite.
The production patch builder needs only the standard library. On this macOS
setup Unicorn's JIT required execution outside the restricted sandbox.

The 4x build passes IPS roundtrips. Compared with Dust Approach 04, exactly 70
System bytes differ, all inside the award block or its 26-byte display heading;
all other disks are identical. A full default-1x rebuild also reproduces the
previous disk images exactly. Emulator playtesting remains pending: the tests
verify the award block, not an entire live battle or the random stat-growth code.

## Activating and playtesting

Use a fresh boot of the trainer build. A RetroArch state restores emulated RAM,
so loading a state from a normal build can also restore the normal award code.
To continue without replaying the story, load the old state in its matching
build, make a normal in-game save, then boot the trainer and load that save using
a copy of that User Disk. No personal save/state was transferred by the build.
Do not format a User Disk containing progress.

For a first battle, record character EXP before and after if the status screen
exposes it: the increase should be four times the displayed base award, up to
the per-battle cap. Check both Sion and another party member, normal level-up
messages/stat changes, and unchanged credit/scrap rewards. Keep the normal build
for comparison. Switching back to 1x stops future boosts; it does not undo EXP
already saved into a character.
