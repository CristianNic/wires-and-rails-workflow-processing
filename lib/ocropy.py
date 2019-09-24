"""
Interface to ocropus binaries for image row segmentation.
"""

import subprocess
import os
import numpy as np
from PIL import Image

from logger import setup_logger

NOIZE_SIZE = 2
BORDER_SPACE = 3

RAILS_INDENT = 2

TELE_INDENT = 7

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

    def _merge_images(self, pathes, remove=True, padding=3):
        """ TODO: check if we need it"""
        images = list(map(Image.open, pathes))
        widths, heights = zip(*(i.size for i in images))

        total_height = sum(heights) - (padding * len(images) - 1) * 2
        max_width = max(widths)

        result = Image.new(images[0].mode, (max_width, total_height), (255))
        # crop
        y_offset = padding
        for im in images:
            width, height = im.size
            im = im.crop((0, padding, width, height - padding * 2))
            result.paste(im, (0, y_offset))
            y_offset += height - padding * 4

        result.save(pathes[0] + 'new.png')
        #    new_im.save('test.jpg')

    def _get_list_of_sub_images(self, path):
        name, _ext = os.path.splitext(path)
        files = [os.path.join(name, file) for file in os.listdir(name)]
        files.sort(key=file_name_to_int)

        return files

    def _extract_elements_from_rails(self, pseg_path):
        return self._extract_elements_from_any(pseg_path, RAILS_INDENT)

    def _extract_elements_from_tele(self, pseg_path):
        return self._extract_elements_from_any(pseg_path, TELE_INDENT)

    def _extract_elements_from_any(self, pseg_path, indent):
        raw_lines = self._extract_raw_lines_from_pseg(pseg_path)

        # calculate average x_size
        x_size = np.median([r['x_size'] for r in raw_lines])
        print('x_size', x_size)
        curent_left = raw_lines[0]['left']
        curent_parent = 0
        for i, line in enumerate(raw_lines):
            print(i, 'diff', (line['left'] - curent_left) / x_size)
            if line['left'] > curent_left + x_size * indent:
                line['parent'] = False
                raw_lines[curent_parent]['bottom'] = max(
                    raw_lines[curent_parent]['bottom'],
                    line['bottom'])
            else:
                line['parent'] = True
                curent_left = line['left']
                curent_parent = i
        # for l in raw_lines:
        #     print(l)
        lines = [l for l in raw_lines if l['parent']]
        self._save_lines(pseg_path.replace('pseg', 'bin'), lines)

    def _save_lines(self, path, lines):
        im = Image.open(path)
        width, height = im.size[:2]
        for i, l in enumerate(lines):
            print(l)
            top = max(l['top'] - ADD_SPACE_TO_IMAGE, 0)
            bottom = min(l['bottom'] + ADD_SPACE_TO_IMAGE, height)
            part = im.crop((0, top, width,  bottom))
            part.save('{}.{:04d}.png'.format(path, i))

    def _extract_line_from_pseg(self, pixels, idx):
        true_points = np.argwhere(pixels == idx)

        # take the smallest points and use them as the top left of your crop
        top = true_points.min(axis=0)[0]
        # take the largest points and use them as the bottom right of your crop
        bottom = true_points.max(axis=0)[0] + 1
        # plus 1 because slice isn't
        out = pixels[top:bottom, :].copy()
        out[out != idx] = 0
        out[out != 0] = 1

        return out, top, bottom

    def _extract_raw_lines_from_pseg(self, pseg_path):
        """ extract lines coords from pseq file """
        img = np.array(Image.open(pseg_path))
        height, width = img.shape[0:2]

        # we use only blue pixels
        pixels = img[:, :, 2]

        lines = []
        max_line = np.max(pixels[pixels < 255])
        for line_id in range(1, max_line + 1):
            rows, top, bottom = self._extract_line_from_pseg(pixels, line_id)

            columns = np.sum(rows, axis=0)
            x_size, left = self._detect_left(columns)
            lines.append({
                'id': line_id,
                'top': top,
                'bottom': bottom,
                'x_size': x_size,
                'left': left,
            })

        return lines

    def _detect_left(self, columns):
        letter_columns = columns[np.nonzero(columns)]
        x_size = np.median(letter_columns)  # size of small letters

        # print(columns)
        # filter noize
        columns[columns < x_size / NOIZE_SIZE] = 0
        columns[columns > x_size * NOIZE_SIZE] = 0
        # print(columns)
        # check if we have border on the left
        char_start = np.argmax(columns > 0)
        char_end = char_start + np.argmax(columns[char_start:] == 0)
        space_end = char_end + np.argmax(columns[char_end:] > 0)

        if (space_end - char_end) > (char_end - char_start) * BORDER_SPACE:
            return x_size, space_end

        return x_size, char_start

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
