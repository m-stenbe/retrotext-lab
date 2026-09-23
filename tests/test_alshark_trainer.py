import random
import unittest
from profiles.alshark.trainer import START, END, ORIGINAL, award_code, patch_exp_multiplier
from profiles.alshark.combat_text import fixed_text
try:
    import unicorn as uc
    from unicorn import x86_const as reg
except ImportError:
    uc = None


class TrainerGuardTests(unittest.TestCase):
    def test_default_is_identical_and_invalid_multiplier_rejected(self):
        original = bytearray(b'X'*0x10000)
        original[START:END] = ORIGINAL
        before = bytes(original)
        self.assertIsNone(patch_exp_multiplier(original,1))
        self.assertEqual(bytes(original),before)
        for value in (0,3,16,True,'4'):
            with self.assertRaises(ValueError):patch_exp_multiplier(original,value)
            self.assertEqual(bytes(original),before)

    def test_all_guards_before_mutation_and_scope(self):
        for corrupt in ('code','heading',None):
            data = bytearray(b'X'*0x10000)
            data[START:END] = ORIGINAL
            data[0x1edf:0x1ef9] = fixed_text('PARTY GAINS\nEXP   ',26)
            if corrupt=='code':data[START] ^= 1
            if corrupt=='heading':data[0x1edf] ^= 1
            before = bytes(data)
            if corrupt:
                with self.assertRaises(ValueError):patch_exp_multiplier(data,4,reviewed_text=True)
                self.assertEqual(bytes(data),before)
            else:
                result=patch_exp_multiplier(data,4,reviewed_text=True)
                self.assertEqual(result['exp_multiplier'],4)
                self.assertEqual(len(data),len(before))
                self.assertTrue(all(START<=i<END or 0x1edf<=i<0x1ef9
                    for i,(a,b) in enumerate(zip(before,data)) if a!=b))
                with self.assertRaises(ValueError):patch_exp_multiplier(data,4,reviewed_text=True)


@unittest.skipIf(uc is None, 'Install requirements-trainer-tests.txt to execute x86 verification')
class TrainerMachineTests(unittest.TestCase):
    def setUp(self):
        self.cpu = uc.Uc(uc.UC_ARCH_X86,uc.UC_MODE_16)
        self.cpu.mem_map(0,0x80000)
        # Original character-pointer and threshold helpers, no game assets needed.
        self.cpu.mem_write(0xad2,bytes.fromhex('fec832e4d1e0055d1b8bf08b048bf0c3'))
        self.cpu.mem_write(0x79b2,bytes.fromhex('32e48bd8d1e003d881c354ddb800508ec0268b074343268a17c3'))
        self.destination=None
        def stop(cpu,address,size,user):
            if address in (0x789e,0x78d2):
                self.destination=address
                cpu.emu_stop()
        self.cpu.hook_add(uc.UC_HOOK_CODE,stop)

    def execute(self,code,reward,total,threshold,slot=0,present=True):
        cpu=self.cpu
        for r in (reg.UC_X86_REG_CS,reg.UC_X86_REG_DS,reg.UC_X86_REG_SS,reg.UC_X86_REG_ES):cpu.reg_write(r,0)
        for r in (reg.UC_X86_REG_EAX,reg.UC_X86_REG_EBX,reg.UC_X86_REG_ECX,reg.UC_X86_REG_EDX,
                  reg.UC_X86_REG_ESI,reg.UC_X86_REG_EDI,reg.UC_X86_REG_EBP):cpu.reg_write(r,0xa5a50011)
        cpu.reg_write(reg.UC_X86_REG_ESP,0x9000)
        cpu.reg_write(reg.UC_X86_REG_EFLAGS,2)
        cpu.mem_write(START,code)
        cpu.ctl_remove_cache(START,END)
        cpu.mem_write(0x19db,b'\0'*5)
        cpu.mem_write(0x19db+slot,bytes([1 if present else 0]))
        cpu.mem_write(0x1c08,bytes([slot]))
        cpu.mem_write(0x1bf4,reward.to_bytes(2,'little'))
        cpu.mem_write(0x1bf6,b'\x12\x34\x56\x78\x9a')
        cpu.mem_write(0x1b5d,(0x2100).to_bytes(2,'little'))
        character=bytearray([0xa5]*64)
        character[0]=1; character[3]=2;character[4:7]=total.to_bytes(3,'little')
        cpu.mem_write(0x2100,bytes(character))
        cpu.mem_write(0x50000+0xdd54+2*3,threshold.to_bytes(3,'little'))
        self.destination=None
        cpu.emu_start(START,0x78d3,count=100)
        self.assertIsNotNone(self.destination)
        self.assertEqual(cpu.reg_read(reg.UC_X86_REG_SP),0x9000)
        self.assertEqual(bytes(cpu.mem_read(0x1bf4,7)),reward.to_bytes(2,'little')+b'\x12\x34\x56\x78\x9a')
        return bytes(cpu.mem_read(0x2100,64)),self.destination,bytes(character)

    def test_machine_code_matches_native_award_for_scaled_reward(self):
        rng=random.Random(230923)
        cases=[(reward,total,threshold) for reward in (0,1,8191,8192,16383,16384,32767,32768,65535)
               for total in (0,65534,65535,65536,0xffff00)
               for threshold in (0,1,65535,65536,0xffffff)]
        cases += [(rng.randrange(65536),rng.randrange(0x1000000),rng.randrange(0x1000000)) for _ in range(150)]
        for factor in (2,4,8):
            for index,(reward,total,threshold) in enumerate(cases):
                with self.subTest(factor=factor,reward=reward,total=total,threshold=threshold):
                    scaled=min(reward*factor,65535)
                    expected,branch,before=self.execute(ORIGINAL,scaled,total,threshold,index%5)
                    actual,actual_branch,_=self.execute(award_code(factor),reward,total,threshold,index%5)
                    self.assertEqual(actual,expected)
                    self.assertEqual(actual_branch,branch)
                    value=(total+scaled)&0xffffff  # native cumulative width is unchanged
                    self.assertEqual(int.from_bytes(actual[4:7],'little'),value)
                    self.assertEqual(actual_branch,0x789e if value>=threshold else 0x78d2)
                    self.assertEqual(actual[7:0x38],before[7:0x38])
                    self.assertEqual(actual[0x38:0x40],b'\0'*8)

    def test_empty_slots_do_not_receive_exp_or_status_changes(self):
        for factor in (1,2,4,8):
            for slot in range(5):
                actual,branch,before=self.execute(award_code(factor),65535,1200,1400,slot,False)
                self.assertEqual(actual,before)
                self.assertEqual(branch,0x78d2)
