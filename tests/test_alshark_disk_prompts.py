import copy
import hashlib
import json
import unittest
from unittest.mock import patch
from profiles.alshark import disk_prompts as prompts
from retrotext.localization import fingerprint


class DiskPromptTests(unittest.TestCase):
    def fixture(self):
        data = bytearray(0x5000)
        pack = json.loads(prompts.PACK.read_text())
        specs = {}
        for r in pack['records']:
            a,n = r['source']['offset'],r['source']['size']
            data[a:a+n] = b'X'*n
            r['source']['sha256'] = hashlib.sha256(b'X'*n).hexdigest()
            specs[r['id']] = copy.deepcopy(r['source'])
            basis = fingerprint({k:r[k] for k in ('source','canonicalEnglish','context')})
            r['review']['basis'] = r['target']['basedOn'] = basis
        for a,before,_ in prompts.WRITES:data[a:a+4] = bytes.fromhex(before)
        return data,pack,specs

    def test_runtime_substitution_all_names_and_drives(self):
        data,pack,specs = self.fixture()
        with patch.object(prompts,'SPECS',specs):prompts.patch_disk_prompts(data,pack)
        names=[r for r in pack['records'] if r['id'].startswith('name-')]
        for r in names:
            a=r['source']['offset'];label=r['target']['inGameEnglish']
            for drive in (1,2):
                mem=bytearray(data)
                mem[0x2857:0x2863]=data[a:a+12]
                dest=int.from_bytes(mem[0x252b:0x252d],'little')+0x2000
                mem[dest]=0x4f+drive
                text=bytes(mem[0x2857:mem.index(0,0x2857)]).decode('cp932')
                normalize=lambda s:s.replace('　',' ').translate(str.maketrans({chr(i+0xfee0):chr(i) for i in range(33,127)})).replace('@','\n')
                self.assertEqual(normalize(text),f'{label}\nIN DRIVE {drive}\nPRESS ANY KEY.')
                for other in names:
                    dual=bytearray(data);b=other['source']['offset']
                    dual[0x289a:0x28a6]=data[a:a+12]
                    dual[0x28bd:0x28c9]=data[b:b+12]
                    for ins,value in ((0x2558,drive),(0x255c,3-drive)):
                        dest=int.from_bytes(dual[ins+2:ins+4],'little')+0x2000
                        dual[dest]=0x4f+value
                    text=bytes(dual[0x289a:dual.index(0,0x289a)]).decode('cp932')
                    self.assertEqual(normalize(text),f'{label} IN DRIVE {drive}\n{other["target"]["inGameEnglish"]} IN DRIVE {3-drive}\nPRESS ANY KEY.')

    def test_guards_fail_before_any_write(self):
        for mode in ('source','instruction','review','slot','overflow'):
            data,pack,specs=self.fixture()
            if mode=='source':data[0x2857]=0
            if mode=='instruction':data[0x255c]=0
            r=pack['records'][0]
            if mode=='review':r['canonicalEnglish']='Changed instruction'
            if mode=='slot':r['target']['inGameEnglish']='BAD\nIN DRIVE 1\nPRESS ANY KEY.'
            if mode=='overflow':r['target']['inGameEnglish']='      \nIN DRIVE 1\n'+'X'*16
            before=bytes(data)
            with patch.object(prompts,'SPECS',specs), self.assertRaises(ValueError):
                prompts.patch_disk_prompts(data,pack)
            self.assertEqual(bytes(data),before)
