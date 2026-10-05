"""Execute original 16-bit text handlers; mock only platform drawing/services.

Unicorn JIT may require execution outside the filesystem sandbox on macOS.
These tests do not launch or change a live emulator or any disk image.
"""
from pathlib import Path
import unittest
try:
    import unicorn as uc
    from unicorn import x86_const as reg
except ImportError:
    uc = None

ORIGINAL=Path(__file__).resolve().parents[2]/'alshark/original/Alshark (System Disk).hdm'


@unittest.skipUnless(uc is not None and ORIGINAL.is_file(),'Original image and Unicorn required')
class RendererMachineTests(unittest.TestCase):
    def execute(self, stream, callee=None):
        from profiles.alshark.playtest_narration import validate_source
        source=ORIGINAL.read_bytes();validate_source(source)
        u=uc.Uc(uc.UC_ARCH_X86,uc.UC_MODE_16)
        u.mem_map(0,0x100000);u.mem_write(0x20000,source[:0x10000])
        for register,value in ((reg.UC_X86_REG_CS,0x2000),(reg.UC_X86_REG_DS,0x2000),
                               (reg.UC_X86_REG_SS,0x2000),(reg.UC_X86_REG_SP,0xff00),
                               (reg.UC_X86_REG_SI,0x6000),(reg.UC_X86_REG_DI,0)):
            u.reg_write(register,value)
        u.mem_write(0x26000,stream);u.mem_write(0x2ff00,b'\x00\x90')
        u.mem_write(0x29000,b'\xf4');u.mem_write(0x21d4e,b'\x0f\x05')
        u.mem_write(0x21d50,b'\0'*4);u.mem_write(0x21d56,b'\0\0')
        # Source $00 name lookup reads 5000:dbf8 and adds d7f8.
        u.mem_write(0x50000+0xdbf8,(0x2000).to_bytes(2,'little'))
        u.mem_write(0x50000+0xf7f8,'ＳＩＯＮ'.encode('cp932')+b'\0')
        if callee is not None:
            u.mem_write(0x27000,callee)
            u.mem_write(0x223eb+41*2,(0x7000-0x23eb).to_bytes(2,'little'))
        attributes=[None];events=[];calls=[]
        def interrupt(machine,number,data):
            self.assertEqual(number,0x41)
            service=machine.reg_read(reg.UC_X86_REG_AH)
            if service==7:
                attributes[0]=machine.reg_read(reg.UC_X86_REG_BX)
            elif service in (0x17,0x18,0x19):
                # Native platform glyph lookup; retain ASCII identity for assertions.
                machine.reg_write(reg.UC_X86_REG_AX,machine.reg_read(reg.UC_X86_REG_BL))
            elif service in (5,6):
                events.append((machine.reg_read(reg.UC_X86_REG_DI),
                               machine.reg_read(reg.UC_X86_REG_DX),attributes[0]))
            else:
                self.fail(f'Unexpected platform service {service:x}')
        def code(machine,address,size,data):
            offset=address-0x20000
            if offset==0xda63:
                calls.append(machine.reg_read(reg.UC_X86_REG_DI))
            if offset in (0xfc4e,0xe6c6,0xf60f,0x160b):
                # Stub disk bank loading, input wait and box drawing only.
                # The interpreter, #P handler, cursor and attribute code run intact.
                if offset==0xf60f:machine.reg_write(reg.UC_X86_REG_DI,0)
                sp=machine.reg_read(reg.UC_X86_REG_SP)
                target=int.from_bytes(machine.mem_read(0x20000+sp,2),'little')
                machine.reg_write(reg.UC_X86_REG_SP,sp+2)
                machine.reg_write(reg.UC_X86_REG_IP,target)
        u.hook_add(uc.UC_HOOK_INTR,interrupt);u.hook_add(uc.UC_HOOK_CODE,code)
        u.emu_start(0x2f2cd,0x29000,count=100000)
        self.assertEqual(u.reg_read(reg.UC_X86_REG_IP),0x9000,'Interpreter did not return')
        return events,calls

    def test_original_newline_resets_and_inserted_control_restores_narration(self):
        old,_=self.execute(b'6ABC@DEF\0')
        new,_=self.execute(b'6ABC@6DEF\0')
        self.assertEqual([e[2] for e in old],[0x090d]*3+[0x050f]*3)
        self.assertEqual([e[2] for e in new],[0x090d]*6)
        self.assertEqual([e[0] for e in new],[0,2,4,0x500,0x502,0x504])

    def test_header_control_does_not_reset_and_name_keeps_narration_attributes(self):
        events,_=self.execute(b'46$\x00 A46B\0')
        # Four full-width name glyphs, space skip, A then B append on one row.
        self.assertEqual(events[-2][0],10)
        self.assertEqual(events[-1][0],12)
        self.assertTrue(all(e[2]==0x090d for e in events))

    def test_real_shared_call_reproduces_old_indent_and_fixes_origin(self):
        old,calls=self.execute(b'3MEDS#P\x02\x00\x29\0',b'6@6FOUND\0')
        new,new_calls=self.execute(b'3MEDS@#P\x02\x00\x29\0',b'6FOUND\0')
        self.assertEqual(calls,[8]);self.assertEqual(new_calls,[0x500])
        self.assertEqual(old[4][0],0x508)
        self.assertEqual(new[4][0],0x500)
        self.assertTrue(all(e[2]==0x090d for e in new[4:]))

    def test_continuation_clear_and_restore_draws_next_page_in_narration_style(self):
        events,_=self.execute(b'6ABC0_6DEF\0')
        self.assertEqual([e[0] for e in events],[0,2,4,0,2,4])
        self.assertTrue(all(e[2]==0x090d for e in events))

    def test_native_name_and_title_spacing_executes_original_renderer(self):
        source=ORIGINAL.read_bytes()
        from profiles.alshark.playtest_narration import validate_source
        validate_source(source)
        def render(raw):
            machine=uc.Uc(uc.UC_ARCH_X86,uc.UC_MODE_16)
            machine.mem_map(0,0x100000)
            # Resident overlay is loaded from file14000 into segment7000.
            machine.mem_write(0x70000,source[0x14000:0x24000])
            for register,value in ((reg.UC_X86_REG_CS,0x7000),(reg.UC_X86_REG_DS,0x7000),
                                   (reg.UC_X86_REG_SS,0x7000),(reg.UC_X86_REG_SP,0xff00),
                                   (reg.UC_X86_REG_BX,0x1000),(reg.UC_X86_REG_DI,0)):
                machine.reg_write(register,value)
            machine.mem_write(0x51000,(0x2000).to_bytes(2,'little'))
            machine.mem_write(0x5f7f8,raw+b'\0')
            machine.mem_write(0x7712f,b'\0')
            machine.mem_write(0x7ff00,b'\x00\x90')
            machine.mem_write(0x79000,b'\xf4')
            glyphs=[]
            def interrupt(cpu,number,data):
                self.assertEqual(number,0x41)
                service=cpu.reg_read(reg.UC_X86_REG_AH)
                if service==0x19:
                    cpu.reg_write(reg.UC_X86_REG_AX,cpu.reg_read(reg.UC_X86_REG_BL))
                elif service==5:
                    glyphs.append((chr(cpu.reg_read(reg.UC_X86_REG_DX)),
                                   cpu.reg_read(reg.UC_X86_REG_DI)//2))
                else:self.fail(f'Unexpected native renderer service {service:x}')
            machine.hook_add(uc.UC_HOOK_INTR,interrupt)
            machine.emu_start(0x770b1,0x79000,count=10000)
            self.assertEqual(machine.reg_read(reg.UC_X86_REG_IP),0x9000)
            return glyphs,machine.reg_read(reg.UC_X86_REG_DI)//2
        for raw,expected in ((b'CAMP>KIT',8),(b'SUBM>GUN',8),
                             (b'>PLANET>HOM',11),(b'SAXEN>CANYON',12),
                             (b'BASEMENT>BAR',12),(b'  JOE',7)):
            glyphs,end=render(raw)
            self.assertEqual(end,expected,(raw,glyphs))
            if raw==b'  JOE':self.assertEqual(glyphs[0],('J',4))
        normal,end=render(b'CAMP KIT')
        narrow,narrow_end=render(b'CAMP>KIT')
        self.assertEqual(normal[4],('K',6))
        self.assertEqual(narrow[4],('K',5))
        self.assertEqual(end-narrow_end,1)
