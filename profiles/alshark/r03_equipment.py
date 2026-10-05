"""Guarded names exposed by the acquired ship's development/equipment menus.

Full source strings may share suffixes. Writable storage is their union minus
all prior allocation pools. Every exact pointer target is repacked separately;
prior translated suffixes and their pointers remain owned by the prior adapter.
"""
import hashlib
from retrotext.localization import make_record
from profiles.alshark.names import BASE, SPANS, guard_original
from profiles.alshark.r02_names import _specs as r02_specs
from profiles.alshark.r03_names import _specs as r03_specs

POINTER_END = 0x1055c
# record ID: (original offset, NUL-inclusive size, exact aliases)
SPECS = {
    'r03-equipment:item:01': (0x10799, 9, (65538,)),
    'r03-equipment:item:02': (0x107a2, 8, (65540,)),
    'r03-equipment:item:04': (0x107b5, 7, (65544,)),
    'r03-equipment:item:05': (0x107bc, 6, (65546,)),
    'r03-equipment:item:06': (0x107c2, 9, (65548,)),
    'r03-equipment:item:07': (0x107cb, 8, (65550,)),
    'r03-equipment:item:08': (0x107d3, 10, (65552,)),
    'r03-equipment:item:09': (0x107dd, 11, (65554,)),
    'r03-equipment:item:0a': (0x107e8, 8, (65556,)),
    'r03-equipment:item:0b': (0x107f0, 8, (65558,)),
    'r03-equipment:item:0c': (0x107f8, 10, (65560,)),
    'r03-equipment:item:0d': (0x10802, 10, (65562,)),
    'r03-equipment:item:0e': (0x1080c, 7, (65564,)),
    'r03-equipment:item:0f': (0x10813, 9, (65566,)),
    'r03-equipment:item:10': (0x1081c, 10, (65568,)),
    'r03-equipment:item:11': (0x10826, 11, (65570,)),
    'r03-equipment:item:12': (0x10831, 10, (65572,)),
    'r03-equipment:item:13': (0x1083b, 11, (65574,)),
    'r03-equipment:item:14': (0x10846, 7, (65576,)),
    'r03-equipment:item:15': (0x1084d, 11, (65578,)),
    'r03-equipment:item:16': (0x10858, 8, (65580,)),
    'r03-equipment:item:17': (0x10860, 11, (65582,)),
    'r03-equipment:item:18': (0x1086b, 10, (65584, 65586)),
    'r03-equipment:item:1c': (0x10886, 11, (65592,)),
    'r03-equipment:item:1e': (0x1089b, 9, (65596,)),
    'r03-equipment:item:1f': (0x108a4, 11, (65598,)),
    'r03-equipment:item:20': (0x108af, 11, (65600,)),
    'r03-equipment:item:21': (0x108ba, 10, (65602,)),
    'r03-equipment:item:22': (0x108c4, 10, (65604,)),
    'r03-equipment:item:24': (0x108d7, 11, (65608,)),
    'r03-equipment:item:25': (0x108e2, 10, (65610,)),
    'r03-equipment:item:26': (0x108ec, 10, (65612,)),
    'r03-equipment:item:27': (0x108f6, 7, (65614,)),
    'r03-equipment:item:28': (0x108fd, 10, (65616,)),
    'r03-equipment:item:29': (0x10907, 9, (65618,)),
    'r03-equipment:item:2a': (0x10910, 10, (65620,)),
    'r03-equipment:item:2b': (0x1091a, 7, (65622,)),
    'r03-equipment:item:2c': (0x10921, 8, (65624,)),
    'r03-equipment:item:2d': (0x10929, 7, (65626,)),
    'r03-equipment:item:2e': (0x10930, 9, (65628,)),
    'r03-equipment:item:2f': (0x10939, 11, (65630,)),
    'r03-equipment:item:30': (0x10944, 9, (65632,)),
    'r03-equipment:item:31': (0x1094d, 11, (65634,)),
    'r03-equipment:item:32': (0x10958, 11, (65636,)),
    'r03-equipment:item:33': (0x10963, 9, (65638,)),
    'r03-equipment:item:34': (0x1096c, 10, (65640,)),
    'r03-equipment:item:35': (0x10976, 10, (65642,)),
    'r03-equipment:item:36': (0x10980, 10, (65644,)),
    'r03-equipment:item:37': (0x1098a, 11, (65646,)),
    'r03-equipment:item:38': (0x10995, 9, (65648,)),
    'r03-equipment:item:39': (0x1099e, 7, (65650, 65652, 65654, 65656, 65660)),
    'r03-equipment:item:3f': (0x109a5, 7, (65662,)),
    'r03-equipment:item:40': (0x109ac, 9, (65664,)),
    'r03-equipment:item:41': (0x109b5, 6, (65666,)),
    'r03-equipment:item:42': (0x109bb, 9, (65668,)),
    'r03-equipment:item:43': (0x109c4, 9, (65670,)),
    'r03-equipment:item:45': (0x109cd, 13, (65674,)),
    'r03-equipment:item:46': (0x109da, 7, (65676,)),
    'r03-equipment:item:47': (0x109e1, 6, (65678,)),
    'r03-equipment:item:48': (0x109e9, 7, (65680,)),
    'r03-equipment:item:49': (0x109f0, 9, (65682,)),
    'r03-equipment:item:4a': (0x109f9, 10, (65684,)),
    'r03-equipment:item:4b': (0x109e7, 9, (65686,)),
    'r03-equipment:item:4e': (0x10a0f, 11, (65692,)),
    'r03-equipment:item:4f': (0x10a1a, 12, (65694,)),
    'r03-equipment:item:50': (0x10a26, 10, (65696,)),
    'r03-equipment:item:52': (0x10a39, 9, (65700,)),
    'r03-equipment:item:53': (0x10a42, 9, (65702,)),
    'r03-equipment:item:54': (0x10a4b, 10, (65704,)),
    'r03-equipment:item:55': (0x10a55, 8, (65706,)),
    'r03-equipment:item:56': (0x10a5d, 12, (65708,)),
    'r03-equipment:item:57': (0x10a69, 11, (65710,)),
    'r03-equipment:item:58': (0x10a74, 7, (65712,)),
    'r03-equipment:item:59': (0x10a7b, 11, (65714,)),
    'r03-equipment:item:5a': (0x10a86, 10, (65716,)),
    'r03-equipment:item:5b': (0x10a90, 9, (65718,)),
    'r03-equipment:item:62': (0x10a9d, 4, (65732,)),
    'r03-equipment:item:64': (0x10aa9, 10, (65736,)),
    'r03-equipment:item:65': (0x10ab3, 7, (65738,)),
    'r03-equipment:item:66': (0x10aba, 9, (65740,)),
    'r03-equipment:item:67': (0x10ac3, 7, (65742,)),
    'r03-equipment:item:68': (0x10aca, 9, (65744,)),
    'r03-equipment:item:69': (0x10ad3, 9, (65746,)),
    'r03-equipment:item:6a': (0x10adc, 9, (65748,)),
    'r03-equipment:item:6b': (0x10ae5, 10, (65750,)),
    'r03-equipment:item:6c': (0x10aef, 9, (65752,)),
    'r03-equipment:item:6d': (0x10af8, 7, (65754,)),
    'r03-equipment:item:6e': (0x10aff, 10, (65756,)),
    'r03-equipment:item:6f': (0x10b09, 8, (65758,)),
    'r03-equipment:item:70': (0x10b11, 9, (65760,)),
    'r03-equipment:item:71': (0x10b1a, 8, (65762,)),
    'r03-equipment:item:72': (0x10b22, 8, (65764,)),
    'r03-equipment:item:73': (0x10b2a, 11, (65766,)),
    'r03-equipment:item:74': (0x10b35, 10, (65768,)),
    'r03-equipment:item:76': (0x10b48, 10, (65772,)),
    'r03-equipment:item:77': (0x10b52, 11, (65774,)),
    'r03-equipment:item:78': (0x10b5d, 12, (65776,)),
    'r03-equipment:item:79': (0x10b69, 11, (65778,)),
    'r03-equipment:item:82': (0x10b7f, 10, (65796,)),
    'r03-equipment:item:83': (0x10b89, 10, (65798,)),
    'r03-equipment:item:84': (0x10b93, 9, (65800,)),
    'r03-equipment:item:85': (0x10b9e, 7, (65802,)),
    'r03-equipment:item:86': (0x10b9c, 9, (65804,)),
    'r03-equipment:item:87': (0x10ba5, 12, (65806,)),
    'r03-equipment:item:88': (0x10bb1, 10, (65808,)),
    'r03-equipment:item:89': (0x10bbb, 10, (65810,)),
    'r03-equipment:item:8a': (0x10bc5, 11, (65812,)),
    'r03-equipment:item:8b': (0x10bd0, 12, (65814,)),
    'r03-equipment:item:8c': (0x10bdc, 11, (65816,)),
    'r03-equipment:item:8d': (0x10be7, 7, (65818,)),
    'r03-equipment:item:8e': (0x10bee, 13, (65820,)),
    'r03-equipment:item:8f': (0x10bfb, 11, (65822,)),
    'r03-equipment:item:90': (0x10c06, 9, (65824,)),
    'r03-equipment:item:91': (0x10c0f, 11, (65826,)),
    'r03-equipment:item:92': (0x10c1a, 9, (65828,)),
    'r03-equipment:item:94': (0x10c2d, 7, (65832,)),
    'r03-equipment:item:95': (0x10c34, 9, (65834,)),
    'r03-equipment:item:96': (0x10c3d, 9, (65836,)),
    'r03-equipment:item:97': (0x10c46, 10, (65838,)),
    'r03-equipment:item:98': (0x10c50, 13, (65840,)),
    'r03-equipment:item:99': (0x10c5d, 10, (65842,)),
    'r03-equipment:item:9b': (0x10c71, 12, (65846,)),
    'r03-equipment:item:9d': (0x10c84, 9, (65850,)),
    'r03-equipment:item:9e': (0x10c8d, 10, (65852,)),
    'r03-equipment:item:9f': (0x10c97, 8, (65854,)),
    'r03-equipment:item:a0': (0x10c9f, 7, (65856,)),
    'r03-equipment:item:a1': (0x10ca6, 10, (65858,)),
    'r03-equipment:item:a4': (0x10cc5, 12, (65864,)),
    'r03-equipment:item:a5': (0x10cd1, 9, (65866,)),
    'r03-equipment:item:a6': (0x10cda, 15, (65868,)),
    'r03-equipment:item:a7': (0x10ce9, 13, (65870,)),
    'r03-equipment:item:a8': (0x10cf6, 9, (65872, 65874)),
    'r03-equipment:item:aa': (0x10cff, 11, (65876,)),
    'r03-equipment:item:ab': (0x10d0a, 15, (65878,)),
    'r03-equipment:item:ac': (0x10d19, 12, (65880,)),
    'r03-equipment:item:ad': (0x10d25, 8, (65882,)),
    'r03-equipment:item:ae': (0x10d2d, 9, (65884,)),
    'r03-equipment:item:af': (0x10d36, 7, (65886,)),
    'r03-equipment:item:b0': (0x10d3d, 11, (65888,)),
    'r03-equipment:item:b1': (0x10d48, 8, (65890, 65892, 65894, 65896, 65898, 65900, 65902, 65904, 65906, 65908, 65910, 65912, 65914, 65916, 65918)),
    'r03-equipment:item:c0': (0x10d50, 12, (65920,)),
    'r03-equipment:ship:01': (0x10d69, 10, (66050,)),
    'r03-equipment:ship:02': (0x10d73, 10, (66052,)),
    'r03-equipment:ship:03': (0x10d7d, 13, (66054,)),
    'r03-equipment:ship:04': (0x10d8a, 11, (66056,)),
    'r03-equipment:ship:05': (0x10d95, 15, (66058,)),
    'r03-equipment:ship:06': (0x10da4, 8, (66060,)),
    'r03-equipment:ship:07': (0x10dac, 12, (66062,)),
    'r03-equipment:ship:08': (0x10db8, 11, (66064,)),
    'r03-equipment:ship:09': (0x10dc3, 7, (66066,)),
    'r03-equipment:ship:0a': (0x10dca, 9, (66068,)),
    'r03-equipment:ship:0b': (0x10dd3, 9, (66070,)),
    'r03-equipment:ship:0c': (0x10ddc, 8, (66072,)),
    'r03-equipment:ship:0d': (0x10de4, 13, (66074,)),
    'r03-equipment:ship:0e': (0x10df1, 11, (66076,)),
    'r03-equipment:ship:0f': (0x10dfc, 7, (66078,)),
    'r03-equipment:ship:10': (0x10e03, 9, (66080,)),
    'r03-equipment:ship:11': (0x10e0c, 11, (66082,)),
    'r03-equipment:ship:12': (0x10e17, 15, (66084,)),
    'r03-equipment:ship:13': (0x10e26, 12, (66086,)),
    'r03-equipment:ship:14': (0x10e32, 12, (66088,)),
    'r03-equipment:ship:15': (0x10e3e, 12, (66090,)),
    'r03-equipment:ship:16': (0x10e4a, 11, (66092,)),
    'r03-equipment:ship:17': (0x10e55, 12, (66094,)),
    'r03-equipment:ship:18': (0x10e61, 14, (66096,)),
    'r03-equipment:ship:19': (0x10e6f, 13, (66098,)),
    'r03-equipment:ship:1a': (0x10e7c, 15, (66100,)),
    'r03-equipment:ship:1b': (0x10e8b, 10, (66102,)),
    'r03-equipment:ship:1c': (0x10e95, 13, (66104,)),
    'r03-equipment:ship:1d': (0x10ea2, 10, (66106,)),
    'r03-equipment:ship:1e': (0x10eac, 10, (66108,)),
    'r03-equipment:ship:1f': (0x10eb6, 9, (66110,)),
    'r03-equipment:ship:20': (0x10ebf, 10, (66112,)),
    'r03-equipment:ship:21': (0x10ec9, 9, (66114,)),
    'r03-equipment:ship:22': (0x10ed2, 12, (66116,)),
    'r03-equipment:ship:23': (0x10ede, 12, (66118,)),
    'r03-equipment:ship:24': (0x10eea, 11, (66120,)),
    'r03-equipment:ship:25': (0x10ef5, 8, (66122,)),
    'r03-equipment:ship:26': (0x10efd, 10, (66124,)),
    'r03-equipment:ship:27': (0x10f07, 11, (66126,)),
    'r03-equipment:ship:28': (0x10f12, 13, (66128,)),
    'r03-equipment:ship:29': (0x10f1f, 6, (66130,)),
    'r03-equipment:ship:2a': (0x10f25, 7, (66132,)),
    'r03-equipment:ship:2b': (0x10f2c, 10, (66134,)),
    'r03-equipment:ship:2c': (0x10f36, 7, (66136,)),
    'r03-equipment:ship:2d': (0x10f3d, 11, (66138,)),
    'r03-equipment:ship:2e': (0x10f48, 6, (66140,)),
    'r03-equipment:ship:2f': (0x10f4e, 12, (66142,)),
    'r03-equipment:ship:30': (0x10f5a, 9, (66144,)),
    'r03-equipment:ship:31': (0x10f63, 6, (66146,)),
    'r03-equipment:ship:32': (0x10f69, 11, (66148,)),
    'r03-equipment:ship:33': (0x10f74, 12, (66150,)),
    'r03-equipment:ship:34': (0x10f80, 6, (66152,)),
    'r03-equipment:ship:35': (0x10f86, 11, (66154,)),
    'r03-equipment:ship:36': (0x10f91, 10, (66156, 66158, 66160, 66162)),
    'r03-equipment:ship:3a': (0x10f9b, 12, (66164,)),
    'r03-equipment:ship:3b': (0x10fa7, 8, (66166,)),
    'r03-equipment:ship:3c': (0x10faf, 7, (66168,)),
    'r03-equipment:ship:3d': (0x10fb6, 8, (66170,)),
    'r03-equipment:ship:3e': (0x10fbe, 13, (66172,)),
    'r03-equipment:ship:3f': (0x10fcb, 10, (66174,)),
    'r03-equipment:ship:40': (0x10fd5, 10, (66176,)),
    'r03-equipment:ship:41': (0x10fdf, 11, (66178,)),
    'r03-equipment:ship:42': (0x10fea, 12, (66180,)),
    'r03-equipment:ship:43': (0x10ff6, 8, (66182,)),
    'r03-equipment:ship:44': (0x10ffe, 7, (66184,)),
    'r03-equipment:ship:45': (0x11005, 6, (66186, 66188, 66190, 66192, 66194)),
    'r03-equipment:ship:4a': (0x1100b, 7, (66196,)),
    'r03-equipment:ship:4b': (0x11012, 8, (66198,)),
    'r03-equipment:ship:4c': (0x1101a, 11, (66200,)),
    'r03-equipment:ship:4d': (0x11025, 8, (66202,)),
    'r03-equipment:ship:4e': (0x1102d, 12, (66204,)),
    'r03-equipment:ship:4f': (0x11039, 9, (66206,)),
    'r03-equipment:ship:50': (0x11042, 9, (66208,)),
    'r03-equipment:ship:51': (0x1104b, 5, (66210,)),
    'r03-equipment:ship:52': (0x11050, 7, (66212,)),
    'r03-equipment:ship:53': (0x11057, 8, (66214,)),
    'r03-equipment:ship:54': (0x1105f, 10, (66216,)),
    'r03-equipment:ship:55': (0x11069, 10, (66218,)),
    'r03-equipment:ship:56': (0x11073, 10, (66220, 66222, 66224, 66226, 66228, 66230, 66232, 66234, 66236, 66238, 66240, 66242, 66244, 66246, 66248, 66250, 66252, 66254, 66256, 66258, 66260, 66262, 66264, 66266, 66268, 66270, 66272, 66274, 66276, 66278, 66280, 66282, 66284, 66286, 66288, 66290, 66292, 66294, 66296, 66298, 66300, 66302)),
}
REQUIRED = set(SPECS)


def prior_spans(source):
    spans = [(a, z) for a, z, _ in SPANS]
    spans += [(a, a+size) for _, a, size, _, _, _ in (*r02_specs(), *r03_specs())]
    spans += [(a, source.index(0, a)+1) for a in (0x107aa, 0x10875, 0x10b74)]
    return spans


def guard_specs(source):
    prior = prior_spans(source)
    known = {p for _, _, pointers in SPECS.values() for p in pointers}
    if len(known) != sum(len(x[2]) for x in SPECS.values()):
        raise ValueError('Duplicate R03 equipment pointer')
    prior_pointers = set()
    for p in range(BASE, POINTER_END, 2):
        target = BASE + int.from_bytes(source[p:p+2], 'little')
        if any(a <= target < z for a, z in prior):
            prior_pointers.add(p)
    covered = set()
    for ident, (a, size, pointers) in SPECS.items():
        raw = source[a:a+size]
        if len(raw) != size or raw[-1:] != b'\0' or b'\0' in raw[:-1]:
            raise ValueError(f'{ident}: original string extent changed')
        if not pointers:
            raise ValueError(f'{ident}: missing source consumer')
        for p in pointers:
            if source[p:p+2] != (a-BASE).to_bytes(2, 'little'):
                raise ValueError(f'{ident}: pointer mismatch at {p:#x}')
            if p in prior_pointers:
                raise ValueError(f'{ident}: pointer owned by prior names')
        covered.update(range(a, a+size))
    for p in range(BASE, POINTER_END, 2):
        target = BASE + int.from_bytes(source[p:p+2], 'little')
        if target in covered and p not in known and p not in prior_pointers:
            raise ValueError(f'Unreviewed equipment alias at {p:#x}')
    for a, z in prior:
        covered.difference_update(range(a, z))
    spans = []
    for address in sorted(covered):
        if spans and spans[-1][1] == address:
            spans[-1] = (spans[-1][0], address+1)
        else:
            spans.append((address, address+1))
    return spans


def encode_equipment(value):
    if (not isinstance(value, str) or not value or len(value) > 8
            or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ' for c in value)):
        raise ValueError('Equipment names require at most eight uppercase/digit cells')
    # A-Z and spaces have a proven ASCII path. Digits use their original
    # full-width CP932 glyphs, not an assumed ASCII-digit renderer behavior.
    return b''.join(chr(ord(c)+0xfee0).encode('cp932') if c.isdigit()
                    else ('>' if c == ' ' else c).encode('ascii') for c in value) + b'\0'


def export_records(images):
    guard_original(images)
    source = images['System']
    spans = guard_specs(source)
    records = []
    for ident, (a, size, pointers) in SPECS.items():
        raw = source[a:a+size]
        records.append(make_record(ident, 'name', dict(
            disk='System', offset=a, size=size, raw=raw.hex(),
            text=raw[:-1].decode('cp932'), sha256=hashlib.sha256(raw).hexdigest(),
            pointers=[dict(offset=p, raw=source[p:p+2].hex()) for p in pointers],
            allocationGroup='r03-equipment-names', rendererOffset=0x1b0b1,
            maximumCells=9, allocationSpans=[dict(offset=x, size=z-x) for x, z in spans])))
    return records


def compile_names(images, translations):
    guard_original(images)
    if not isinstance(translations, dict) or set(translations) != REQUIRED:
        raise ValueError('Complete R03 equipment name allocation group required')
    source = images['System']
    spans = guard_specs(source)
    pending = sorted(((ident, value, encode_equipment(value))
                      for ident, value in translations.items()), key=lambda r: (-len(r[2]), r[0]))
    bins = {a: bytearray() for a, _ in spans}
    placements = []
    for ident, value, raw in pending:
        choices = [(z-a-len(bins[a]), a) for a, z in spans if z-a-len(bins[a]) >= len(raw)]
        if not choices:
            raise ValueError('R03 reviewed equipment allocations cannot fit labels')
        _, a = min(choices)
        offset = a+len(bins[a])
        bins[a].extend(raw)
        placements.append(dict(record=ident, text=value, offset=offset, used=len(raw),
                               pointers=list(SPECS[ident][2]), encoding='ascii-wide-digits'))
    output = bytearray(source)
    patches = []
    for a, z in spans:
        output[a:z] = bins[a].ljust(z-a, b'\0')
        patches.append(dict(offset=a, size=z-a))
    for row in placements:
        for p in row['pointers']:
            output[p:p+2] = (row['offset']-BASE).to_bytes(2, 'little')
            patches.append(dict(offset=p, size=2))
    return bytes(output), dict(records=placements, patches=patches)
