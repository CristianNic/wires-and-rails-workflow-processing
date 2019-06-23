"""
Interface to ocropus binaries for image row segmentation.
"""

import subprocess
import os
import numpy as np
from PIL import Image

from .logger import setup_logger


def file_name_to_int(path):
    """ helper funftion for sorting sub images"""
    file_name = os.path.basename(path)
    parts = file_name.split('.')
    return int(parts[0], 16)


class Ocropy:
    """
    Interface to ocropus scripts for image row segmentation.
    """

    ERROR_LOGGER_NAME = 'ocropy_error'

    def __init__(self, logger):
        self._logger = logger
        self._error_logger = setup_logger(self.ERROR_LOGGER_NAME, 'log/ocropy_error.log')

    def perform_row_segmentation(self, image_file_path):
        """Run row segmentation on the provided path and return the new row absolute filepaths"""
        success = self._execute_row_segmentation_command(image_file_path)
        self._cleanup()
        if not success:
            # TODO throw exception so rq puts in failed queue / other recovery strategy
            return False
        name, _ext = os.path.splitext(image_file_path)
        # The name and the resulting ocropus directory have the exact same name
        return [os.path.join(name, file) for file in os.listdir(name)]

    def _extract_raw_rows(self, image_file_path):
        """Run row segmentation on the provided path and return the new row absolute filepaths"""
        success = self._execute_row_segmentation_command(image_file_path)
        # self._cleanup()
        if not success:
            # TODO throw exception so rq puts in failed queue / other recovery strategy
            return False
        return self._get_list_of_sub_images(image_file_path)

    def _get_list_of_sub_images(self, path):
        name, _ext = os.path.splitext(path)
        files = [os.path.join(name, file) for file in os.listdir(name)]
        files.sort(key=file_name_to_int)

        return files

    def _extract_lines_from_pseg(self, pseg_path):
        """ extract lines coords from pseq file """
        img = np.array(Image.open(pseg_path))
        height, width = img.shape[0:2]
        print(height, width)
        # we use only blue pixels
        pixels = img[:, :, 2]

        line_idx = np.min(pixels, axis=1)
        lines = []
        top, current_line_id = 0, line_idx[0]
        for x, line_id in enumerate(line_idx):
            if line_id == current_line_id:
                continue
            # new line started
            if current_line_id != 255:
                rows = pixels[top:x-1]
                # set dots to 1
                print(rows)
                rows[rows < 255] = 1
                rows[rows > 1] = 0
                columns = np.sum(rows, axis=0)
                lines.append({
                    'id': current_line_id,
                    'top': top,
                    'bottom': x - 1,
                    'columns': columns
                })
                print(x-1 - top)
                print(columns)
                exit(0)
            current_line_id = line_id
            top = x

        print(lines)
        print(rows_idx)

    def _try_subprocess_cmd(self, cmd):
        self._logger.debug('Running cmd in subprocess: %s', str(cmd))
        try:
            cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            self._logger.debug('Result of ocropus cmd: %s', cmd_result)
            return True
        except subprocess.CalledProcessError as exception:
            self._logger.debug('Command return code was greater than zero. See error log.')
            self._error_logger.error('Cmd: %s', str(cmd))
            self._error_logger.error('Return code: %s', exception.returncode)
            self._error_logger.error('Cmd output: %s', exception.output)
            return False

    def _execute_row_segmentation_command(self, image_file_path):
        nlbin_cmd = ['ocropus-nlbin', image_file_path]
        if not self._try_subprocess_cmd(nlbin_cmd):
            return False
        gpageseg_cmd = ['ocropus-gpageseg', '-n', '-d', '--maxcolseps=0', '--maxseps=0',
                        '--hscale=100', image_file_path]
        return self._try_subprocess_cmd(gpageseg_cmd)

    def _cleanup(self):
        self._try_subprocess_cmd(['rm', '-f', '_1thresh.png', '_2grad.png', '_3seps.png',
                                  '_4seps.png', '_cleaned.png', '_colwsseps.png', '_lineseeds.png',
                                  '_seeds.png'])
