# CLI Tools

## Prerequirments

Python 3.5 (or later) and panoptes-client

	pip install panoptes-client

## CLI tool to upload new images with metadata

Full usage exaple:

	python3 add_files.py --path ../samples/ --metadata type-source-year-page --extension .bin.png  --delimiter "-" --username denys.potapov --password 12345678 --subjectset 76895

Will seach for all \*.bin.png files in folder, and split the filename to metadata type-source-year-page

Dry run (do not load anything, jsut preview the file metadata parsing):

	python3 add_files.py --path ../samples/ --metadata type-source-year-page --extension .bin.png --dry-run

Show all the params

	python3 add_files.py -h
