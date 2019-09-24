#!/usr/bin/env python
import logging
import argparse

from ocropy import Ocropy
from queue_operations import QueueOperations


def main(path, type):
    ocr = Ocropy(logging)

    # we use the same upscale as in previous processing
    qo = QueueOperations(logging)
    qo.upscale_small_images(path)

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
