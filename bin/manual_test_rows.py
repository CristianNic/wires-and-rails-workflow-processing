import logging
import sys
sys.path.insert(0, "..")

# from lib import ocropy
from lib.ocropy import Ocropy  # noqa
# from lib.logger import setup_logger  # noqa


# logger = setup_logger('temp', '/../../app/log/ocropy_error.log')

ocr = Ocropy(logging)
# print(ocr._extract_raw_rows('/tmp/sample.t.png'))
ocr._extract_lines_from_pseg('/tmp/sample.pseg.png')