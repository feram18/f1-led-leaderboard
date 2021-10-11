"""Class with utility functions"""

import os
import logging
import json
from typing import Tuple, Optional
from PIL import Image
from rgbmatrix.graphics import Font


def read_json(filename: str) -> dict:
    """
    Read from JSON file and return it as a dictionary
    :param filename: (str) JSON file
    :return: json: (dict) JSON file as a dict
    """
    if os.path.isfile(filename):
        with open(filename, 'r') as json_file:
            logging.debug(f'Reading JSON file at {filename}')
            return json.load(json_file)
    else:
        logging.error(f"Couldn't find file at {filename}")


def load_font(filename: str) -> Font:
    """
    Return Font object from given path. If file at path does not exist, set default 4x6 font.
    :param filename: (str) Location of font file
    :return: font: (rgbmatrix.graphics.Font) Font object
    """
    font = Font()
    if os.path.isfile(filename):
        font.LoadFont(filename)
    else:
        logging.warning(f"Couldn't find font {filename}. Setting font to default 4x6.")
        font.LoadFont('rpi-rgb-led-matrix/fonts/4x6.bdf')
    return font


def load_image(filename: str, size: Tuple[int, int] = (64, 32)) -> Image:
    """
    Return Image object from given file.
    :param filename: (str) Location of image file
    :param size: (int, int) Maximum width and height of image
    :return: image: (PIL.Image) Image file
    """
    if os.path.isfile(filename):
        with Image.open(filename) as image:
            image.thumbnail(size, Image.ANTIALIAS)
            return image.convert('RGB')
    else:
        logging.error(f"Couldn't find image {filename}")
        return None


def center_image(image_size: Tuple[int, int],
                 canvas_width: Optional[int] = 0,
                 canvas_height: Optional[int] = 0) -> (int, int):
    """
    Calculate x and y-coords to center image on canvas.
    :param canvas_width: (int) Canvas' width
    :param canvas_height: (int) Canvas' height
    :param image_size: (int, int) Image size
    :return: (x, y): (int, int) X, Y coordinates
    """
    x = abs(canvas_width//2 - image_size[0]//2)
    y = abs(canvas_height//2 - image_size[1]//2)
    return x, y


def align_text_center(string: str,
                      canvas_width: Optional[int] = 0,
                      canvas_height: Optional[int] = 0,
                      font_width: Optional[int] = 0,
                      font_height: Optional[int] = 0) -> (int, int):
    """
    Calculate x-coord to align text to center of canvas.
    :param string: (str) String of text to be displayed
    :param canvas_width: (int) Canvas' width
    :param canvas_height: (int) Canvas' height
    :param font_width: (int) Font's width
    :param font_height: (int) Font's height
    :return: (x, y): (int, int) X, Y coordinates
    """
    x = abs(canvas_width//2 - (len(string)*font_width) // 2)
    y = abs(canvas_height//2 + font_height//2)
    return x, y
