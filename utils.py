"""Class with utility functions"""

import os
import logging
import json
import argparse
from enum import Enum
from typing import Tuple, Optional, List
from PIL import Image
from rgbmatrix.graphics import Font, Color as RGB
from rgbmatrix import RGBMatrixOptions


class Color(Enum):
    """Colors enum class"""

    # Standard colors
    RED = RGB(171, 0, 3)
    ORANGE = RGB(128, 128, 128)
    YELLOW = RGB(239, 178, 30)
    GREEN = RGB(124, 252, 0)
    BLUE = RGB(0, 45, 114)
    PURPLE = RGB(170, 40, 203)
    PINK = RGB(255, 143, 255)
    BROWN = RGB(65, 29, 0)
    GRAY = RGB(112, 128, 144)
    BLACK = RGB(0, 0, 0)
    WHITE = RGB(255, 255, 255)

    # Constructors' Background & Text Colors
    ALFA = [RGB(153, 0, 0),  WHITE]  # [Background, Text]
    ALPHATAURI = [RGB(39, 40, 79), WHITE]
    ALPINE = [RGB(14, 29, 45), WHITE]
    ASTON_MARTIN = [RGB(3, 87, 78), WHITE]
    FERRARI = [RGB(255, 0, 0), BLACK]
    HAAS = [RGB(236, 27, 59), WHITE]
    MCLAREN = [RGB(255, 134, 1), BLACK]
    MERCEDES = [RGB(0, 210, 190), BLACK]
    RED_BULL = [RGB(22, 25, 94), WHITE]
    WILLIAMS = [RGB(3, 168, 235), BLACK]


class Position(Enum):
    """Enum class for positioning on matrix' canvas"""
    TOP = 0
    RIGHT = 1
    CENTER = 2
    BOTTOM = 3


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
        return font

    logging.warning(f"Couldn't find font {filename}. Setting font to default 4x6.")
    font.LoadFont('rpi-rgb-led-matrix/fonts/4x6.bdf')
    return font


def load_image(filename: str,
               size: Tuple[int, int] = (64, 32),
               background: Color = Color.BLACK) -> Image:
    """
    Open Image file from given path
    :param background: Background color for PNG images
    :param filename: Path to the image file
    :param size: Maximum width and height of the image
    :return: image: Image file
    """
    if os.path.isfile(filename):
        with Image.open(filename) as original:
            if '.png' in filename:
                original = original.crop(original.getbbox())  # Non-empty pixels
                image = Image.new('RGB',  # Background img
                                  (original.width, original.height),
                                  (background.value.red, background.value.green, background.value.blue, 255))
                image.paste(original)  # Paste original on background
                image.thumbnail(size)  # Resize
                return image
            else:
                original.thumbnail(size)
                return original.convert('RGB')
    logging.error(f"Couldn't find image {filename}")


def align_text(text: str,
               x: Position = None, y: Position = None,
               col_width: int = 0, col_height: int = 0,
               font_width: int = 0, font_height: int = 0) -> (int, Optional[int]):
    """
    Calculate x, y coords to align text on canvas
    :param text: Text to align
    :param x: Text's horizontal position
    :param y: Text's vertical position
    :param col_width: Column's width
    :param col_height: Column's height
    :param font_width: Font's width
    :param font_height: Font's height
    :return: x, y: Coordinates
    """
    if x:
        if x == Position.RIGHT:
            x = col_width - (len(text) * font_width)
        elif x == Position.CENTER:
            x = abs(col_width//2 - (len(text) * font_width)//2)
        else:
            x = 0
        if x is not None and y is None:
            return x

    if y:
        if y == Position.CENTER:
            y = abs(col_height//2 + font_height//2)
        elif y == Position.BOTTOM:
            y = col_height
        else:
            y = font_height
        if y is not None and x is None:
            return y

    return x, y


def align_image(image: Image,
                x: Position = None, y: Position = None,
                col_width: int = 0, col_height: int = 0) -> (int, Optional[int]):
    """
    Calculate the x, y offsets to align image on canvas
    :param image: Image to align
    :param x: Image horizontal position
    :param y: Image vertical position
    :param col_width: Column's width
    :param col_height: Column's height
    :return: x, y: Coordinate offsets
    """
    if x:
        if x == Position.RIGHT:
            x = col_width - image.width
        elif x == Position.CENTER:
            x = abs(col_width//2 - image.width//2)
        else:
            x = 0
        if x is not None and y is None:
            return x

    if y:
        if y == Position.CENTER:
            y = abs(col_height//2 - image.height//2)
        elif y == Position.BOTTOM:
            y = col_height - image.height
        else:
            y = 0
        if y is not None and x is None:
            return y

    return x, y


def split_into_pages(lst: list, size: int) -> List[list]:
    """
    Split list into lists with of equal sizes, defined by size argument.
    :param lst: (list) List to split
    :param size: (int) chunk size
    :return: pages: List(list) Resulting lists
    """
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def args() -> argparse.Namespace:
    """
    CLI argument parser to configure matrix.
    :return: arguments: (argsparse.Namespace) Argument parser
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--led-rows',
                        action='store',
                        help='Display rows. 16 for 16x32, 32 for 32x32. (Default: 32)',
                        default=32,
                        type=int)
    parser.add_argument('--led-cols',
                        action='store',
                        help='Panel columns. Typically 32 or 64. (Default: 32)',
                        default=32,
                        type=int)
    parser.add_argument('--led-chain',
                        action='store',
                        help='Daisy-chained boards. (Default: 1)',
                        default=1,
                        type=int)
    parser.add_argument('--led-parallel',
                        action='store',
                        help='For Plus-models or RPi2: parallel chains. 1..3. (Default: 1)',
                        default=1,
                        type=int)
    parser.add_argument('--led-pwm-bits',
                        action='store',
                        help='Bits used for PWM. Range 1..11. (Default: 11)',
                        default=11,
                        type=int)
    parser.add_argument('--led-brightness',
                        action='store',
                        help='Sets brightness level. Range: 1..100. (Default: 100)',
                        default=100,
                        type=int)
    parser.add_argument('--led-gpio-mapping',
                        help='Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm',
                        choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'],
                        type=str)
    parser.add_argument('--led-scan-mode',
                        action='store',
                        help='Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced. (Default: 1)',
                        default=1,
                        choices=range(2),
                        type=int)
    parser.add_argument('--led-pwm-lsb-nanoseconds',
                        action='store',
                        help='Base time-unit for the on-time in the lowest significant bit in nanoseconds. '
                             '(Default: 130)',
                        default=130,
                        type=int)
    parser.add_argument('--led-show-refresh',
                        action='store_true',
                        help='Shows the current refresh rate of the LED panel.')
    parser.add_argument('--led-slowdown-gpio',
                        action='store',
                        help='Slow down writing to GPIO. Range: 0..4. (Default: 1)',
                        choices=range(5),
                        type=int)
    parser.add_argument('--led-no-hardware-pulse',
                        action='store',
                        help="Don't use hardware pin-pulse generation.")
    parser.add_argument('--led-rgb-sequence',
                        action='store',
                        help='Switch if your matrix has led colors swapped. (Default: RGB)',
                        default='RGB',
                        type=str)
    parser.add_argument('--led-pixel-mapper',
                        action='store',
                        help='Apply pixel mappers. e.g \"Rotate:90\"',
                        default='',
                        type=str)
    parser.add_argument('--led-row-addr-type',
                        action='store',
                        help='0 = default; 1 = AB-addressed panels; 2 = direct row select; '
                             '3 = ABC-addressed panels. (Default: 0)',
                        default=0,
                        type=int,
                        choices=[0, 1, 2, 3])
    parser.add_argument('--led-multiplexing',
                        action='store',
                        help='Multiplexing type: 0 = direct; 1 = strip; 2 = checker; 3 = spiral; 4 = Z-strip; '
                             '5 = ZnMirrorZStripe; 6 = coreman; 7 = Kaler2Scan; 8 = ZStripeUneven. (Default: 0)',
                        default=0,
                        type=int)

    return parser.parse_args()


def led_matrix_options(args_: argparse.Namespace) -> RGBMatrixOptions:
    """
    Set RGBMatrixOptions from parsed arguments.
    :param args_: (argsparse.Namespace) Parsed arguments from CLI
    :return: options: (rgbmatrix.RGBMatrixOptions) RGBMatrixOptions instance
    :exception AttributeError: If attribute is not found
    """
    options = RGBMatrixOptions()

    if args_.led_gpio_mapping is not None:
        options.hardware_mapping = args_.led_gpio_mapping

    options.rows = args_.led_rows
    options.cols = args_.led_cols
    options.chain_length = args_.led_chain
    options.parallel = args_.led_parallel
    options.row_address_type = args_.led_row_addr_type
    options.multiplexing = args_.led_multiplexing
    options.pwm_bits = args_.led_pwm_bits
    options.brightness = args_.led_brightness
    options.pwm_lsb_nanoseconds = args_.led_pwm_lsb_nanoseconds
    options.led_rgb_sequence = args_.led_rgb_sequence
    try:
        options.pixel_mapper_config = args_.led_pixel_mapper
    except AttributeError:
        logging.warning('Your compiled RGB Matrix Library is out of date. '
                        'The --led-pixel-mapper argument will not work until it is updated.')

    if args_.led_show_refresh:
        options.show_refresh_rate = 1

    if args_.led_slowdown_gpio is not None:
        options.gpio_slowdown = args_.led_slowdown_gpio

    if args_.led_no_hardware_pulse:
        options.disable_hardware_pulsing = True

    return options
