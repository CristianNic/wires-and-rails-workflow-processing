#!/usr/bin/env python
import logging
import argparse

import sys
sys.path.insert(0, "..")
from lib.ocropy import Ocropy  # noqa
# from lib.logger import setup_logger  # noqa
# # from lib.ocropy import Ocropy  # noqa

# logger = setup_logger('temp', 'log/ocropy_error.log')


def main(path, type):
    ocr = Ocropy(logging)

    ocr._extract_raw_rows(path)
    t = path.replace('.png', '.pseg.png')
    if type == 'rails':
        ocr._extract_elements_from_rails(t)
    else:
        ocr._extract_elements_from_tele(t)

    # teles = ['tele_1', 'tele_2', 'tele_3']
# for t in teles:
#     path = '/tmp/preview/' + t + '.png'
#     # print()
#     ocr._extract_elements_from_tele('/tmp/preview/' + t + '.pseg.png')


# rails = ['rails_1', 'rails_2']
# for t in rails:
#     path = '/tmp/preview/' + t + '.png'
#     print(ocr._extract_raw_rows(path))
#     


    # 

# teles = ['tele_1', 'tele_2', 'tele_3']
# for t in teles:
#     path = '/tmp/preview/' + t + '.png'
#     # print(ocr._extract_raw_rows(path))
#     


# rails = ['rails_1', 'rails_2']
# for t in rails:
#     path = '/tmp/preview/' + t + '.png'
#     print(ocr._extract_raw_rows(path))
#     ocr._extract_elements_from_rails('/tmp/preview/' + t + '.pseg.png')

    # print(subject)
    # queue_ops = QueueOperations(logger)
    # subject = Subject.find(subject)
    # subject_image_path = queue_ops.fetch_subject_image_to_tmp(subject)
    # logger.info("Saved image:" + subject_image_path)
    #     # column_image_paths = queue_ops.perform_column_segmentation(
    #     #     subject_id,
    #     #     subject_image_path,
    #     #     vertex_centroids
    #     # )
    #     # 
    # pass


# logger = setup_logger(cls.LOGGER_NAME, 'log/queue_operations.log')

# for column_image_path in column_image_paths:
#     queue_ops.upscale_small_images(column_image_path)
# row_paths_by_column = queue_ops.perform_row_segmentation(column_image_paths)
# queue_ops.push_new_row_subjects(subject,
# target_subject_set_id, row_paths_by_column)

# # from lib import ocropy


# teles = ['tele_1', 'tele_2', 'tele_3']
# for t in teles:
#     path = '/tmp/preview/' + t + '.png'
#     # print(ocr._extract_raw_rows(path))
#     ocr._extract_elements_from_tele('/tmp/preview/' + t + '.pseg.png')


# rails = ['rails_1', 'rails_2']
# for t in rails:
#     path = '/tmp/preview/' + t + '.png'
#     print(ocr._extract_raw_rows(path))
#     ocr._extract_elements_from_rails('/tmp/preview/' + t + '.pseg.png')

# #-workflow-processing/tmp/preview/.png

# # # ocr._merge_images([
# # #    '/tmp/sample_r/010001.bin.png',
# # #    '/tmp/sample_r/010002.bin.png'
# # # ])
#


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
