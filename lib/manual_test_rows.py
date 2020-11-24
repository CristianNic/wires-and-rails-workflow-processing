#!/usr/bin/env python
import logging
import argparse

from ocropy import Ocropy
from queue_operations import QueueOperations


def main(path):
    ocr = Ocropy(logging)

    # we use the same upscale as in previous processing
    qo = QueueOperations(logging)
    qo.upscale_small_images(path)

    print(ocr.perform_row_segmentation(path))

    return


if __name__ == '__main__':
    desc = """test tool for row separation """

    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc)

    p.add_argument(
        "--path", help="Column image path", required=True)

    args = p.parse_args()
    main(**vars(args))
