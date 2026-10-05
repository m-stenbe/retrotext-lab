import unittest
from profiles.alshark.interface import compile_records,POOL,POOL_END


class InterfaceTests(unittest.TestCase):
    def fixture(self):
        opening=bytearray(0x6000);system=bytes(0x12000)
        opening[0x407b:0x4081]=bytes.fromhex('040208236226')
        raw=b'AB@CD\0';opening[0x4662:0x4662+len(raw)]=raw
        r=dict(id='ui:Opening:004662',kind='menu',source=dict(disk='Opening',offset=0x4662,size=len(raw),raw=raw.hex()),review=dict(basis='synthetic'),target=dict(inGameEnglish='USE\nDROP'))
        return dict(Opening=bytes(opening),System=system),r

    def test_pointer_relocation_preserves_source_and_geometry(self):
        images,r=self.fixture();out,records=compile_records(images,[r])
        self.assertEqual(out['Opening'][0x4662:0x4668],images['Opening'][0x4662:0x4668])
        self.assertEqual(out['Opening'][0x407b:0x407f],images['Opening'][0x407b:0x407f])
        self.assertEqual(int.from_bytes(out['Opening'][0x407f:0x4081],'little'),POOL-0x2000)
        self.assertEqual(out['System'],images['System'])
        allowed=[(p['offset'],p['offset']+p['size']) for p in records[0]['patches']]
        self.assertTrue(all(any(a<=i<z for a,z in allowed) for i,(a,b) in enumerate(zip(images['Opening'],out['Opening'])) if a!=b))

    def test_geometry_source_and_pool_guards(self):
        for change in ('width','rows','source','pool'):
            images,r=self.fixture()
            if change=='width':r['target']['inGameEnglish']='TOO LONG\nDROP'
            if change=='rows':r['target']['inGameEnglish']='USE'
            if change=='source':r['source']['raw']='00'*r['source']['size']
            if change=='pool':
                b=bytearray(images['Opening']);b[POOL_END-1]=1;images['Opening']=bytes(b)
            with self.assertRaises(ValueError):compile_records(images,[r])

    def test_fixed_runtime_rejects_storage_fitting_but_overwide_text(self):
        # Synthetic reward script retains the real token structure and 73-byte
        # allocation; no original game text is needed for this regression.
        raw = (b'A'*26 + b'3(\x001' + b'A'*12 + b'3(\x011'
               + b'A'*10 + b'3(\x021' + b'A'*12 + b'\0')
        system = bytearray(0x12000)
        system[0x1edf:0x1f28] = raw
        images = dict(Opening=bytes(0x6000), System=bytes(system))
        values = {'t000': 'A'*11+'\n'+'A'*6, 't004': '\n'+'A'*8,
                  't008': '\n'+'A'*8, 't012': '\n'+'A'*7}
        record = dict(id='fixed:System:001edf', kind='fixed_runtime_script',
                      source=dict(disk='System',offset=0x1edf,size=len(raw),raw=raw.hex()),
                      review=dict(basis='synthetic'),target=dict(inGameEnglish=values))
        compile_records(images, [record])
        for text in ('A'*26, 'A'*10+'\n'+'A'*7):
            values['t000'] = text
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'layout'):
                compile_records(images, [record])

    def test_fixed_ui_rejects_extra_rows_even_when_bytes_fit(self):
        raw = b'A'*31+b'\0'
        system = bytearray(0x12000)
        system[0x1d5e:0x1d5e+len(raw)] = raw
        images = dict(Opening=bytes(0x6000), System=bytes(system))
        record = dict(id='ui:System:001d5e',kind='ui',
                      source=dict(disk='System',offset=0x1d5e,size=len(raw),
                                  raw=raw.hex(),text='A'*31),
                      review=dict(basis='synthetic'),
                      target=dict(inGameEnglish='A\nB\nC\nD\nE'))
        with self.assertRaisesRegex(ValueError, 'layout'):
            compile_records(images, [record])
