#!/usr/bin/env python3
"""Prepare a local scene batch and readiness/playtest report without changing disks."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from profiles.alshark.localization import BIBLE, load_images, validate_sources, compile_adaptations
from retrotext.batches import prepare_batch, reading_sheet


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('original', type=Path)
    p.add_argument('document', type=Path)
    p.add_argument('--plan', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path, help='New directory under ignored work/')
    args = p.parse_args()
    try:
        root = Path(__file__).resolve().parents[2]
        output = args.output.resolve()
        if root / 'work' not in output.parents or output.exists():
            raise ValueError('Output must be a new directory under repository work/')
        original = args.original.resolve()
        if output == original or original in output.parents:
            raise ValueError('Output must be outside original disks')
        images = load_images(original)
        document = json.loads(args.document.read_text())
        bible = json.loads(BIBLE.read_text())
        validate_sources(images, document)
        packet = prepare_batch(document, bible, json.loads(args.plan.read_text()),
            lambda scenes: compile_adaptations(images, document, bible, scenes=scenes)[1])
        output.mkdir(parents=True)
        (output / 'packet.json').write_text(json.dumps(packet, ensure_ascii=False, indent=2)+'\n')
        (output / 'review-and-playtest.md').write_text(reading_sheet(packet))
        print(f"Prepared {len(packet['packets'])} scenes: {len(packet['readyScenes'])} validated for build, "
              f"{len(packet['deferredScenes'])} deferred. No disks changed.\n{output}")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        p.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
