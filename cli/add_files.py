#!/usr/bin/env python
import argparse
from pathlib import Path
from panoptes_client import Panoptes, SubjectSet, Subject


def main(
         path, extension, delimiter, metadata,
         dry_run, username, password, subjectset):
    # prepare metadata
    metadata = metadata.split(delimiter)

    # iterate over files pattern
    files = []
    pathes = Path(path).glob('**/*' + extension)
    for file in sorted(pathes):
        # crop any extension, ex .bin.png
        file_stem = file.name[:-len(extension)]

        # get metadata from filename
        f_metadata = file_stem.split(delimiter)
        assert len(f_metadata) == len(metadata), (
            "Can't parse metadata {} for file {}".format(metadata, str(file)))

        files.append({
            'file_name': str(file),
            'metadata': dict(zip(metadata, f_metadata))
        })

    if dry_run:
        for file in files:
            print('  Preview {} with metadata: {}'.format(
                file['file-_name'], file['metadata']))
        return

    Panoptes.connect(username=username, password=password)
    subjectset = SubjectSet.find(subjectset)
    project = subjectset.links.project

    subjects = []
    for file in files:
        print('  Loading {} with metadata: {}'.format(
            file['file_name'], file['metadata']))
        if dry_run:
            continue

        subject = Subject()
        subject.links.project = project
        subject.add_location(file['file_name'])
        subject.metadata.update(file['metadata'])
        subject.save()
        subjects.append(subject)

    print('  Saving all...')
    subjectset.add(subjects)
    print('  Done')


if __name__ == '__main__':
    desc = """CLI tool to upload new images with metadata.
    """

    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc)

    p.add_argument(
        "--path", help="path to directory to read images", required=True)
    p.add_argument(
        "--metadata",
        help="delimeter separated metadata fields", required=True)

    p.add_argument(
        "--extension", help="file extension (default png)", default=".png")
    p.add_argument(
        "--delimiter",
        help="file name metadata delimeter (default -)", default="-")

    p.add_argument(
        "--dry-run",
        help="Do not actually load info", action='store_true')
    p.add_argument("--username", help="panoptes username", default=None)
    p.add_argument("--password", help="panoptes password", default=None)
    p.add_argument(
        "--subjectset", help="Subject set ID", type=int, default=None)

    args = p.parse_args()
    args_dict = vars(args)
    if args.dry_run:
        main(**args_dict)
        exit(0)

    for a in ['username', 'password', 'subjectset']:
        if args_dict[a] is None:
            p.error(
                "the following arguments are required: --{}".format(a))

    main(**vars(args))
