#!/usr/bin/env python
import argparse
from pathlib import Path
from panoptes_client import Panoptes, SubjectSet, Subject


def main(
         origin, destination, filter,
         dry_run, username, password):
    print(filter)

#          path, extension, delimiter, metadata,
#          , subjectset):
#     # prepare metadata
#     metadata = metadata.split(delimiter)

#     # iterate over files pattern
#     files = []
#     pathes = Path(path).glob('**/*' + extension)
#     for file in sorted(pathes):
#         # crop any extension, ex .bin.png
#         file_stem = file.name[:-len(extension)]

#         # get metadata from filename
#         f_metadata = file_stem.split(delimiter)
#         assert len(f_metadata) == len(metadata), (
#             "Can't parse metadata {} for file {}".format(metadata, str(file)))

#         files.append({
#             'file_name': str(file),
#             'metadata': dict(zip(metadata, f_metadata))
#         })

#     if dry_run:
#         for file in files:
#             print('  Preview {} with metadata: {}'.format(
#                 file['file-_name'], file['metadata']))
#         return

#     Panoptes.connect(username=username, password=password)
#     subjectset = SubjectSet.find(subjectset)
#     project = subjectset.links.project

#     subjects = []
#     for file in files:
#         print('  Loading {} with metadata: {}'.format(
#             file['file_name'], file['metadata']))
#         if dry_run:
#             continue

#         subject = Subject()
#         subject.links.project = project
#         subject.add_location(file['file_name'])
#         subject.metadata.update(file['metadata'])
#         subject.save()
#         subjects.append(subject)

#     print('  Saving all...')
#     subjectset.add(subjects)
#     print('  Done')


if __name__ == '__main__':
    desc = """CLI tool tool for moving images
    """

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
