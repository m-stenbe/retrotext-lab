#!/usr/bin/env python3
"""Manage local canonical scripts without modifying engineering exports."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from profiles.alshark.localization import BIBLE, catalog, load_images, validate_sources, compile_adaptations
from retrotext.localization import index_unique, review_scene, terminology_impact, validate_editorial


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['export', 'scene', 'review', 'validate', 'compile', 'impact'])
    p.add_argument('original', type=Path, help='Directory of original disks')
    p.add_argument('document', type=Path, help='Local localization JSON, normally in work/')
    p.add_argument('--output', type=Path)
    p.add_argument('--bible', type=Path, default=BIBLE)
    p.add_argument('--scene-id')
    p.add_argument('--records', nargs='+', help='Ordered catalog IDs; include connected branch alternatives')
    p.add_argument('--reviewer')
    p.add_argument('--note')
    p.add_argument('--term')
    args = p.parse_args()
    try:
        images = load_images(args.original)
        bible = json.loads(args.bible.read_text())
        if args.action == 'export':
            destination = args.document
            result = catalog(images)
        else:
            document = json.loads(args.document.read_text())
            validate_sources(images, document)
            destination = args.output
            if args.action == 'scene':
                if not args.scene_id or not args.records:
                    raise ValueError('--scene-id and --records required')
                if args.scene_id in index_unique(document['scenes'], 'scene'):
                    raise ValueError('Scene already exists; edit its context in the document')
                records = index_unique(document['records'], 'record')
                if len(set(args.records)) != len(args.records):
                    raise ValueError('Duplicate scene member')
                for ident in args.records:
                    if records[ident]['scene'] is not None:
                        raise ValueError('Record already belongs to a scene')
                document['scenes'].append(dict(id=args.scene_id, records=args.records,
                    participants=[], location=None, storyState=None, purpose=None,
                    previousContext=[], followingContext=[], branchAlternatives=[],
                    terminology=[], evidence=[], uncertainty=[], notes=[]))
                for ident in args.records:
                    records[ident]['scene'] = args.scene_id
                result = document
            elif args.action == 'review':
                review_scene(document, args.scene_id, bible, args.reviewer or '', args.note or '')
                result = document
            elif args.action in ('validate', 'compile'):
                validate_editorial(document, bible)
                rebuilt, changes = compile_adaptations(images, document, bible)
                if args.action == 'validate':
                    print(f'Editorial/source checks pass; {len(changes)} adapted entries pass existing ROM/layout validation.')
                    return
                result = rebuilt
            else:
                if not args.term:
                    raise ValueError('--term is required')
                print(json.dumps(terminology_impact(document, args.term), indent=2))
                return
        if destination is None:
            raise ValueError('--output required; keep input documents as checkpoints')
        dest = destination.resolve()
        if dest == args.original.resolve() or args.original.resolve() in dest.parents:
            raise ValueError('Output must be outside the original disk directory')
        if dest == args.bible.resolve() or (args.action != 'export' and dest == args.document.resolve()):
            raise ValueError('Output must be separate from inputs')
        destination.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(result, bytes):
            destination.write_bytes(result)
            print('Wrote original-based System validation image; use build_demo --localization for a complete demo.')
        else:
            destination.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            print(f'Wrote {destination}')
    except (ValueError, OSError, KeyError, TypeError) as exc:
        p.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
