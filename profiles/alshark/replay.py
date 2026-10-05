"""Replay versioned canonical/adaptation packs against fresh original sources."""
import json
from pathlib import Path
from profiles.alshark.localization import (BIBLE, catalog, load_images,
    apply_editorial_review, apply_adaptation_pack)

PACKS = ('editorial-review.json', 'adaptations-batch-01.json', 'adaptations-batch-02.json',
         'editorial-dust-approach.json', 'adaptations-batch-03.json',
         'editorial-meteor.json', 'adaptations-batch-04.json',
         'editorial-return-cosma.json', 'adaptations-batch-05.json',
         'adaptations-r01-town.json', 'editorial-r01-pickup-outcomes.json',
         'adaptations-r01-pickup-outcomes.json', 'editorial-r01-cinematic-ui.json',
         'adaptations-r01-cinematic-ui.json', 'editorial-r01-party-talk.json',
         'adaptations-r01-party-talk.json',
         'adaptations-r02-rumor.json', 'editorial-r02-names.json',
         'adaptations-r02-names.json',
         'editorial-r02-disassembly-ui.json', 'adaptations-r02-disassembly-ui.json',
         'editorial-r02-hamack-street.json', 'editorial-r02-fortune-uncle.json',
         'editorial-r02-hamack-job.json', 'editorial-r02-hamack-bar.json',
         'editorial-r02-hamack-services.json', 'editorial-r02-joe-meeting.json',
         'editorial-r02-party-closure.json', 'adaptations-r02-joe.json',
         'adaptations-r02-hamack-street.json', 'adaptations-r02-fortune-uncle.json',
         'adaptations-r02-hamack-job.json', 'adaptations-r02-party-closure.json',
         'adaptations-r02-hamack-bar.json', 'adaptations-r02-services.json',
         'editorial-r03-names.json', 'adaptations-r03-names.json',
         'editorial-r03-spaceport.json', 'adaptations-r03-spaceport.json',
         'editorial-r03-mine-ship.json', 'adaptations-r03-mine-ship.json',
         'editorial-r03-ship-ui.json', 'adaptations-r03-ship-ui.json',
         'editorial-r03-heavy-unload.json', 'adaptations-r03-heavy-unload.json',
         'editorial-r03-equipment.json', 'adaptations-r03-equipment.json',
         'editorial-r04-names.json', 'adaptations-r04-names.json',
         'editorial-r04-rescue.json', 'adaptations-r04-rescue.json',
         'editorial-r04-station.json', 'adaptations-r04-station.json',
         'editorial-playtest-bridge.json', 'adaptations-playtest-bridge.json',
         'editorial-r05-names.json', 'adaptations-r05-names.json',
         'editorial-r05-saibal.json', 'adaptations-r05-saibal.json',
         'editorial-r05-porkin.json', 'adaptations-r05-porkin.json',
         'editorial-r05-port.json', 'adaptations-r05-port.json',
         'editorial-r05-scrap.json', 'adaptations-r05-scrap.json',
         'editorial-r06-names.json', 'adaptations-r06-names.json',
         'editorial-r06-ui.json', 'adaptations-r06-ui.json',
         'editorial-r06-towns.json', 'adaptations-r06-towns.json',
         'editorial-r06-rescue.json', 'adaptations-r06-rescue.json',
         'editorial-r07-town.json', 'adaptations-r07-town.json',
         'editorial-r07-bar.json', 'adaptations-r07-bar.json',
         'editorial-r07-names.json', 'adaptations-r07-names.json',
         'editorial-r07-byuto.json', 'adaptations-r07-byuto.json',
         'editorial-r08-capital.json', 'adaptations-r08-capital.json',
         'editorial-r08-port.json', 'adaptations-r08-port.json',
         'editorial-r08-interiors.json', 'adaptations-r08-interiors.json',
         'editorial-r08-names.json', 'adaptations-r08-names.json',
         'editorial-r08-mars.json', 'adaptations-r08-mars.json',
         'editorial-r09-daina.json', 'adaptations-r09-daina.json',
         'editorial-r09-names.json', 'adaptations-r09-names.json')


def replay(original, packs=PACKS):
    images=load_images(original)
    bible=json.loads(BIBLE.read_text())
    document=catalog(images)
    for name in packs:
        pack=json.loads((Path(__file__).parent/name).read_text())
        apply=apply_editorial_review if pack['format']=='retrotext-editorial-review-v1' else apply_adaptation_pack
        document=apply(document,pack,bible)
    return images,document,bible


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original', type=Path)
    parser.add_argument('--output', type=Path, required=True,
                        help='Full source catalog destination; keep under ignored work/')
    args = parser.parse_args()
    if args.output.exists() or args.original.resolve() in args.output.resolve().parents:
        parser.error('Output must be a new file outside original images')
    _, document, _ = replay(args.original)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, ensure_ascii=False, indent=2)+'\n')
    print(f'Replayed {len(PACKS)} packs into {args.output}')
