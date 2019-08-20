#!/usr/bin/env python
import logging
import argparse

from ocropy import Ocropy


def main(path, type):
    ocr = Ocropy(logging)

    ocr._extract_raw_rows(path)
    t = path.replace('.png', '.pseg.png')
    if type == 'rails':
        ocr._extract_elements_from_rails(t)
    else:
        ocr._extract_elements_from_tele(t)


if __name__ == '__main__':
    desc = """test tool for row separation """

    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc)

    p.add_argument(
        "--path", help="Column image path", required=True)

    p.add_argument(
        "--type", help="Page type (rails, tele)",
        choices=["rails", "tele"], required=True)

    args = p.parse_args()
    main(**vars(args))
