import logging
import sys
sys.path.insert(0, "..")

# from lib import ocropy
from lib.ocropy import Ocropy  # noqa
# from lib.logger import setup_logger  # noqa


# logger = setup_logger('temp', '/../../app/log/ocropy_error.log')

ocr = Ocropy(logging)

teles = ['tele_1', 'tele_2', 'tele_3']
for t in teles:
    path = '/tmp/preview/' + t + '.png'
    # print(ocr._extract_raw_rows(path))
    ocr._extract_elements_from_tele('/tmp/preview/' + t + '.pseg.png')


rails = ['rails_1', 'rails_2']
for t in rails:
    path = '/tmp/preview/' + t + '.png'
    print(ocr._extract_raw_rows(path))
    ocr._extract_elements_from_rails('/tmp/preview/' + t + '.pseg.png')

# /home/denys/prj-shared/upwork/rails/wires-and-rails-workflow-processing/tmp/preview/.png
# # 

# # ocr._merge_images([
# #    '/tmp/sample_r/010001.bin.png',
# #    '/tmp/sample_r/010002.bin.png'
# # ])