# CLI Tools

## Prerequirments

Python 3.5 (or later) and panoptes-client

	pip install panoptes-client

## CLI tool to upload new images with metadata

Full usage example:

	python3 add_files.py --path ../samples/ --metadata type-source-year-page --extension .bin.png  --delimiter "-" --username denys.potapov --password 12345678 --subjectset 76895

Will seach for all \*.bin.png files in folder, and split the filename to metadata type-source-year-page

Dry run (do not load anything, jsut preview the file metadata parsing):

	python3 add_files.py --path ../samples/ --metadata type-source-year-page --extension .bin.png --dry-run

Show all the params

	python3 add_files.py -h

## CLI tool for moving images

Usage example:

	python3 move_images.py --origin 76895 --destination 1234 --filter year=1874,source=WU --username denys.potapov --password 12345678

		ed: --origin, --destination, --username, --password
denys@denys-comp:~/prj-shared/upwork/rails/wires-and-rails-workflow-processing/cli$  

кому мені
Hi Denys,

I will try to use the  tool  tomorrow. I looked at the example you uploaded; the images and metadata are right, but I just want to make sure you only uploaded 3 images, as there are only 3 in that subject set.

The third item is described below:

My thoughts on the functions for the other CLI are as follows:

CLI tool to move images between subject sets based on matching a value in a specific metadata field

1. Should be able to specify origin subject set by number, destination subject set by number
2. Should be able to specify the metadata field
3. Should be able to specify the value taken by the metadata field
4. Some ability to do this with generality by specifying values for multiple metadata fields or only one, split by a delimiter.


So, I imagine a tool where I could call the command like this:

move_images --origin SUBJECTSETNUMBER1 --destination SUBJECTSETNUMBER2 --delimiter "-" --field "field1-field2" --value "value1-value2"

move_images --origin SUBJECTSETNUMBER1 --destination SUBJECTSETNUMBER2 --delimiter "-" --field "field1" --value "value1"
