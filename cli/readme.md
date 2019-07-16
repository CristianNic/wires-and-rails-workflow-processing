# CLI Tools

## Prerequirments

python 3.6 

## CLI tool to upload new images with metadata
My thoughts on the functions for the CLI are as follows:



1. should be able to specify meta-data format in image title and have CLI parse it (e.g., telegraph-WU-1874-0001.png, provide CLI with separator "-" and specify order of metadata as "type", "source", 'year', "page")
2. should be able to specify the subject set to which it will be added, by number. (This will allow flexibility going forward to put it in a specific subject set which might not yet exist)
3. should be able to ingest a whole directory/set of directories recursively.


So, I imagine a CLI tool where I could call the command like this:

add_files --directory 'path/to/directory/to/ingest'  --delimiter '-' (character the divides metadata items in the file name) --metadata "delimiter-separated-list-of-metadata-fields" --subjectset NUMBER

python3 add_files.py --path ../../task.2.sample/ --metadata type-source-year-page --extension .bin.png
