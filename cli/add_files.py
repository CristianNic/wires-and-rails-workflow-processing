#!/usr/bin/env python
import argparse
from pathlib import Path


def main(
         path, extension, delimiter, metadata, dry_run):
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
            'metadata':  dict(zip(metadata, f_metadata))
        })

    for file in files:
        print('  Storing {} with metadata: {}'.format(
            file['file_name'], file['metadata']))


if __name__ == '__main__':
    desc = """CLI tool to upload new images with metadata:\n
    \n
    python3 add_files.py
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
    args = p.parse_args()
    main(**vars(args))

    # parser.add_argument("output", help="output image")
    # parser.add_argument("--cosinus", action="store_true")
    # parser.add_argument("--relict", action="store_true")
    # parser.add_argument(
    #     "--scale", type=float, default=5, help="result scale")
    # parser.add_argument(
    #     "--blur", type=float, default=0, help="gaussian blur")
    # parser.add_argument(
    #     "--blur2", type=float, default=1, help="blur2")
    # parser.add_argument(
    #     "--milky", type=float, default=30, help="milky way percent")
    # parser.add_argument(
    #     "--random", type=int, default=0, help="randomness percent")
    # parser.add_argument(
    #     "--preview", action='store_true', help="place star in center")
    # parser.add_argument(
    #     "sizes", nargs='+', type=str,
    #     help="""brightnes and flares intervals and size in percent
    #     sample 0-100=150 100-200=300 0-200=0-0% 200-250=0-500%
    #     """)
    

    # sizes = [0] * 256
    # flares = [(0, 0)] * 256

    # for size in args.sizes:
    #     try:
    #         i, v = size.split('=')

    #         s, e = i.split('-')
    #         s, e = int(s), int(e)

    #         if '%' in v:
    #             f = v[:-1].split('-')
    #             flare = (int(f[0]), int(f[1]))
    #             flares[s:e + 1] = [flare] * (e - s + 1)
    #         else:
    #             sizes[s:e + 1] = [float(v)] * (e - s + 1)
    #     except Exception:
    #         parser.error("invalid interval format: " + size)

    # source = Image.open(args.input)
    # light = Image.open(args.input).convert('L')
    # w, h = source.size

    # out = StarImage(
    #     int(w * args.scale),
    #     int(h * args.scale),
    #     args.random,
    #     args.relict,
    #     args.preview,
    #     args.blur,
    #     args.blur2,
    #     args.milky)

    # for y in range(h):
    #     for x in range(w):
    #         c = source.getpixel((x, y))
    #         l = light.getpixel((x, y))
    #         s = sizes[l] / 100.0
    #         f = flares[l]
    #         if s == 0:
    #             continue
    #         if args.cosinus:
    #             out.draw_cos_pixel(c, s)
    #         else:
    #             out.draw_pixel(c, s, f)
    #     print("Progress: {:2.0f}%".format((float(y) * 100 / h)))

    # # if blur > 0:
    # #     out = out.image.filter(ImageFilter.GaussianBlur(radius=blur))

    # out.save(args.output)
