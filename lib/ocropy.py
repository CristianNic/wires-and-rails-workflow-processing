"""
Interface to ocropus binaries for image row segmentation.
"""

import subprocess
import os
import numpy as np
from PIL import Image

from logger import setup_logger


ADD_SPACE_TO_IMAGE = 3


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
        # self._cleanup()
        if not success:
            # TODO throw exception so rq puts in failed queue / other recovery strategy
            return []

        pseg_path = image_file_path.replace('.png', '.pseg.png')
        lines = self._extract_raw_lines_from_pseg(pseg_path)

        bin_path = pseg_path.replace('pseg', 'bin')
        return self._save_lines(bin_path, lines)

    def _save_lines(self, path, lines):
        im = Image.open(path)
        width, height = im.size[:2]
        pathes = []
        for i, l in enumerate(lines):
            top = max(l['top'] - ADD_SPACE_TO_IMAGE, 0)
            bottom = min(l['bottom'] + ADD_SPACE_TO_IMAGE, height)
            part = im.crop((0, top, width,  bottom))
            file_name = '{}.{:04d}.png'.format(path, i)
            part.save(file_name)

            pathes.append(file_name)

        return pathes

    def _extract_line_from_pseg(self, pixels, idx):
        true_points = np.argwhere(pixels == idx)

        # take the smallest points and use them as the top left of your crop
        top = true_points.min(axis=0)[0]
        # take the largest points and use them as the bottom right of your crop
        bottom = true_points.max(axis=0)[0] + 1

        return top, bottom

    def _extract_raw_lines_from_pseg(self, pseg_path):
        """ extract lines coords from pseq file """
        img = np.array(Image.open(pseg_path))
        height, width = img.shape[0:2]

        # we use only blue pixels
        pixels = img[:, :, 2]

        lines = []
        max_line = np.max(pixels[pixels < 255])
        for line_id in range(1, max_line + 1):
            top, bottom = self._extract_line_from_pseg(pixels, line_id)

            lines.append({
                'id': line_id,
                'top': top,
                'bottom': bottom
            })

        return lines

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
