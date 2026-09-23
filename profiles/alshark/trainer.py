"""Optional EXP trainer: replace only the per-character award/check block."""
import hashlib
from profiles.alshark.combat_text import fixed_text

START, END = 0x785e, 0x789e
ORIGINAL = bytes.fromhex('bedb19a0081c32e403f08a040ac07464e8619233c089443889443a89443c89443ea1f41b014404b0001044068a4403e822013a54067209753b3b440474027334')


def award_code(multiplier):
    if type(multiplier) is not int or multiplier not in (1, 2, 4, 8):
        raise ValueError('EXP multiplier must be 1, 2, 4 or 8')
    if multiplier == 1:
        return ORIGINAL
    code = bytearray()
    def emit(raw):
        code.extend(bytes.fromhex(raw))
    def call(address):
        displacement = (address - (START + len(code) + 3)) & 0xffff
        code.extend(b'\xe8' + displacement.to_bytes(2, 'little'))
    def branch(opcode, address):
        displacement = address - (START + len(code) + 2)
        if not -128 <= displacement <= 127:
            raise ValueError('Trainer branch out of range')
        code.extend((opcode, displacement & 0xff))
    emit('bbdb19 a0081c d7 0ac0')  # BX=party table; AL=index; XLAT; empty?
    branch(0x74, 0x78d2)
    call(0x0ad2)                  # existing character pointer resolver
    emit('6631c0 66894438 6689443c')  # same eight status bytes cleared (386+)
    emit('a1f41b')                # original unsigned 16-bit battle EXP
    code.extend(b'\xba' + multiplier.to_bytes(2, 'little'))
    emit('f7e2 f7da 19d2 09d0')   # MUL DX; NEG DX; SBB DX,DX; OR AX,DX -> saturation
    emit('014404 b000 104406')    # native 24-bit EXP add/carry, other fields untouched
    emit('8a4403')
    call(0x79b2)                  # original next-level threshold lookup
    emit('394404 8a4406 18d0')    # unsigned 24-bit XP < threshold via borrow
    branch(0x72, 0x78d2)
    if len(code) > END-START:
        raise ValueError('Trainer code allocation exceeded')
    return bytes(code).ljust(END-START, b'\x90')


def patch_exp_multiplier(system, multiplier, *, reviewed_text=False):
    code = award_code(multiplier)
    if multiplier == 1:
        return None
    if system[START:END] != ORIGINAL:
        raise ValueError('EXP award routine source mismatch')
    header = None
    if reviewed_text:
        expected = fixed_text('PARTY GAINS\nEXP   ', 26)
        if system[0x1edf:0x1edf+26] != expected:
            raise ValueError('Trainer reward heading source mismatch')
        header = fixed_text('BASE REWARDS\nEXP   ', 26)
    system[START:END] = code
    if header is not None:
        system[0x1edf:0x1edf+26] = header
    return dict(exp_multiplier=multiplier,offset=START,size=END-START,
                code_sha256=hashlib.sha256(code).hexdigest(),
                heading_offset=0x1edf if header is not None else None,
                reward_display='base EXP; multiplier applied per character',
                heading=dict(canonicalEnglish='Base battle rewards', inGameEnglish='BASE REWARDS') if header is not None else None,
                per_character_award_cap=65535,requires='80386 or later',
                progression='Native level-up checks and 24-bit cumulative EXP arithmetic retained',
                runtime_verified=False)
