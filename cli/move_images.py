#!/usr/bin/env python
import argparse
from panoptes_client import Panoptes, SubjectSet
import os


def main(
         origin, destination, filter,
         dry_run, username, password):
    Panoptes.connect(username=username, password=password)

    origin = SubjectSet.find(origin)
    destination = SubjectSet.find(destination)

    for subject in origin.subjects:
        filtered = True
        for key, value in filter.items():
            if subject.metadata.get(key) != value:
                filtered = False
                break
        if not filtered:
            continue

        if dry_run:
            print('  Should move subject #{} with metadata {}'.format(
                subject.id, subject.metadata
            ))
            continue

        print('  Move subject #{} with metadata {}'.format(
            subject.id, subject.metadata
        ))

        destination.add(subject)
        # not working now
        # see https://github.com/zooniverse/panoptes-python-client/issues/221
        # origin.remove(subject)


if __name__ == '__main__':
    desc = """CLI tool tool for moving images
    """
    os.environ["PANOPTES_DEBUG"] = "yes"
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc)

    p.add_argument(
        "--origin", help="Origin subject set ID", type=int,
        default=None, required=True)
    p.add_argument(
        "--destination", help="Destination subject set ID", type=int,
        default=None, required=True)
    p.add_argument(
        "--filter", help="""Metadata comma separated filter
        values. Ex: field1=value,field2=value
        """, type=str, default="")

    p.add_argument("--username", help="panoptes username", required=True)
    p.add_argument("--password", help="panoptes password", required=True)

    p.add_argument(
        "--dry-run",
        help="Do not actually load info", action='store_true')

    args = p.parse_args()

    filter = {}
    try:
        for f in args.filter.split(','):
            key, value = f.split('=')
            filter[key] = value
    except Exception:
            p.error("can't parse --filter" + args.filter)

    args.filter = filter
    main(**vars(args))
