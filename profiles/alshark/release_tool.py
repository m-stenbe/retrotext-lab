#!/usr/bin/env python3
"""Report whole-section readiness, including missing coverage; never edits disks."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from profiles.alshark.localization import BIBLE, load_images, validate_sources, compile_adaptations
from retrotext.releases import assess_release


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('original', type=Path)
    p.add_argument('document', type=Path)
    p.add_argument('--plan', type=Path, required=True)
    args = p.parse_args()
    try:
        images = load_images(args.original)
        document = json.loads(args.document.read_text())
        bible = json.loads(BIBLE.read_text())
        validate_sources(images, document)
        report = assess_release(document, bible, json.loads(args.plan.read_text()),
            lambda scenes: compile_adaptations(images, document, bible, scenes=scenes)[1])
        print(json.dumps(report, indent=2))
        return 0 if report['status'] == 'candidate_ready' else 2
    except (ValueError, OSError, KeyError, TypeError) as exc:
        p.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    sys.exit(main())
