"""Class with utility functions"""

import os
import logging
import json
from typing import Tuple
from PIL import Image


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
