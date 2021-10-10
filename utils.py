"""Class with utility functions"""

import os
import logging
from typing import Tuple
from PIL import Image


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
