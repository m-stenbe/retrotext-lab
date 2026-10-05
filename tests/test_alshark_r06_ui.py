from pathlib import Path
import copy
import unittest
from profiles.alshark import r06_ui as ui

ORIGINAL=Path(__file__).resolve().parents[2]/'alshark/original'

@unittest.skipUnless((ORIGINAL/'Alshark (System Disk).hdm').is_file(),'Original images unavailable')
class R06UITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.images={d:(ORIGINAL/f'Alshark ({d} Disk).hdm').read_bytes() for d in ('System','Opening')}

    def test_menu_boxes_and_shared_highlights_change_only_guarded_bytes(self):
        output={d:bytearray(v) for d,v in self.images.items()}
        patches=ui.widen_menus(output['Opening'],output['System'])
        self.assertEqual(len(patches),17)
        for disk,original in self.images.items():
            changed={i for i,(a,b) in enumerate(zip(original,output[disk])) if a!=b}
            self.assertEqual(changed,{p['offset'] for p in patches if p['disk']==disk})
        for offset,_,width,instructions in ui.MENU_GEOMETRY:
            self.assertEqual(output['Opening'][offset],width)
            for instruction,_ in instructions:
                self.assertEqual(output['System'][instruction+4],width*2)
        output['System'][0x16d33]^=1
        with self.assertRaisesRegex(ValueError,'geometry changed'):
            ui.widen_menus(bytearray(self.images['Opening']),output['System'])

    def test_runtime_destination_and_star_fields_cannot_be_overwritten(self):
        record={'id':'ui:Opening:004897','target':{'inGameEnglish':'\nLAND HERE?\n\nOK?'}}
        ui.validate_translation(record)
        for value in ('NAME\nLAND HERE?\n\nOK?','\nLAND HERE?\nOK?','\nLAND HERE?\nTEXT\nOK?'):
            record['target']['inGameEnglish']=value
            with self.assertRaisesRegex(ValueError,'runtime field'):
                ui.validate_translation(record)
        ui.encode_fixed(0x1734f,'STAR\nGOVT\nFOES\nPLAN    MOON')
        for value in ('STARNAME\nGOVT\nFOES\nPLAN    MOON','STAR\nGOVT\nFOES\nPLANETS MOON'):
            with self.assertRaisesRegex(ValueError,'runtime fields'):
                ui.encode_fixed(0x1734f,value)

    def test_literal_compilation_preserves_source_and_uses_single_cell_spaces(self):
        values={0x1714e:'ATRAIA',0x1a035:'FIGHTER DOWN!',0x1734f:'STAR\nGOVT\nFOES\nPLAN    MOON'}
        records=ui.export_records(self.images)
        for r in records:r['target']['inGameEnglish']=values[r['source']['offset']]
        output,manifest=ui.compile_records(self.images,records)
        patches={i for m in manifest for p in m['patches'] for i in range(p['offset'],p['offset']+p['size'])}
        self.assertTrue(all(i in patches for i,(a,b) in enumerate(zip(self.images['System'],output['System'])) if a!=b))
        self.assertIn(b'PLAN>>>>MOON\0',output['System'][0x1734f:0x17374])
        changed=copy.deepcopy(records);changed[0]['source']['size']+=1
        with self.assertRaisesRegex(ValueError,'immutable'):
            ui.compile_records(self.images,changed)
