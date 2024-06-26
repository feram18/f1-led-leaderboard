"""Class with utility functions"""
import argparse
import json
import logging
import os
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Tuple

from PIL import Image, ImageFont, BdfFontFile
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ModuleNotFoundError:  # used for testing
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

from constants import FONTS_DIR, LIB_FONTS_DIR
from data.session_status import SessionStatus


class Color:
    """Colors utility class"""

    RED = 171, 0, 3, 255
    ORANGE = 128, 128, 128, 255
    YELLOW = 239, 178, 30, 255
    GREEN = 124, 252, 0, 255
    BLUE = 0, 45, 114, 255
    PURPLE = 170, 40, 203, 255
    PINK = 255, 143, 255, 255
    BROWN = 65, 29, 0, 255
    GRAY = 112, 128, 144, 255
    BLACK = 0, 0, 0, 255
    WHITE = 255, 255, 255, 255
    GOLD = 197, 150, 30, 255


class Position(Enum):
    """Enum class for positioning on matrix canvas"""

    TOP = 'top'
    RIGHT = 'right'
    CENTER = 'center'
    BOTTOM = 'bottom'
    LEFT = 'left'


# Dictionary to match nationalities to country
NATIONALITIES = {
    'American': 'United States',
    'Australian': 'Australia',
    'Austrian': 'Austria',
    'Belgian': 'Belgium',
    'Brazilian': 'Brazil',
    'British': 'UK',
    'Canadian': 'Canada',
    'Chinese': 'China',
    'Danish': 'Denmark',
    'Dutch': 'Netherlands',
    'Finnish': 'Finland',
    'French': 'France',
    'German': 'Germany',
    'Italian': 'Italy',
    'Japanese': 'Japan',
    'Mexican': 'Mexico',
    'Monegasque': 'Monaco',
    'New Zealander': 'New Zealand',
    'Polish': 'Poland',
    'Russian': 'Russia',
    'Spanish': 'Spain',
    'Thai': 'Thailand'
}


def read_json(filename: str) -> dict:
    """
    Read from JSON file and return it as a dictionary
    @param filename: JSON file
    @return: JSON as a dict
    """
    if os.path.isfile(filename):
        with open(filename, 'r') as json_file:
            logging.debug(f'Reading JSON file at {filename}')
            return json.load(json_file)
    logging.error(f"Couldn't find file at {filename}")


def load_font(path: str) -> ImageFont:
    """
    Return ImageFont object from given font name
    @param path: Font path
    @return: font: ImageFont object
    """
    if os.path.isfile(path):
        return ImageFont.load(path)
    logging.error(f"Couldn't find font {path}.")


def convert_font(filename: str) -> str:
    """
    Convert from BDF to PIL font
    @param filename: Font filename
    @return Font name
    """
    name = filename\
        .replace(f'{FONTS_DIR}/', '') \
        .replace(f'{LIB_FONTS_DIR}/', '') \
        .replace('.bdf', '')
    with open(filename, 'rb') as fp:
        p = BdfFontFile.BdfFontFile(fp)
        p.save(f'{FONTS_DIR}/{name}')
        return name


def load_image(filename: str,
               size: Tuple[int, int],
               background: tuple = Color.BLACK) -> Image:
    """
    Open Image file from given path
    @param filename: Path to the image file
    @param size: Maximum width and height of the image
    @param background: Background color for PNG images
    @return: Image file
    """
    if filename and os.path.isfile(filename):
        with Image.open(filename) as original:
            if '.png' in filename:
                original = original.crop(original.getbbox())  # Non-empty pixels
                image = Image.new('RGB',  # Background img
                                  (original.width, original.height),
                                  background)
                image.paste(original)  # Paste original on background
                image.thumbnail(size)  # Resize
                return image
            else:  # Non-transparent images
                original.thumbnail(size)
                return original.convert('RGB')
    logging.error(f"Couldn't find image {filename}")


def get_text_size(draw, text, font) -> Tuple[int, int]:
    """
    Get the width and height of a string of text given a font
    @param draw: ImageDraw instance in use
    @param text: Text to get the size of
    @param font: Font to use to draw text
    @return: text size (width, height)
    """
    text_bbox = draw.textbbox((0, 0), text, font)
    return text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]


def align_text(text_size: Tuple[int, int],
               col_width: int = 0,
               col_height: int = 0,
               x: Position = Position.CENTER,
               y: Position = Position.CENTER) -> Tuple[int, int]:
    """
    Calculate x, y coords to align text on canvas
    @param text_size: (width, height) in pixels
    @param x: Text's horizontal position
    @param y: Text's vertical position
    @param col_width: Column's width
    @param col_height: Column's height
    @return: (x, y) coordinates
    """
    if x == Position.RIGHT:
        x = col_width - text_size[0]
    elif x == Position.CENTER:
        x = abs(col_width//2 - text_size[0]//2)
    elif x == Position.LEFT:
        x = 0

    if y == Position.CENTER:
        y = abs(col_height//2 - text_size[1]//2)
    elif y == Position.BOTTOM:
        y = col_height - text_size[1]
    elif y == Position.TOP:
        y = 0

    return x, y


def align_image(image: Image,
                col_width: int = 0,
                col_height: int = 0,
                x: Position = Position.CENTER,
                y: Position = Position.CENTER) -> Tuple[int, int]:
    """
    Calculate the x, y offsets to align image on canvas
    @param image: Image to align
    @param col_width: Column's width
    @param col_height: Column's height
    @param x: Image horizontal position
    @param y: Image vertical position
    @return: (x, y) coordinates
    """
    if x == Position.RIGHT:
        x = col_width - image.width
    elif x == Position.CENTER:
        x = abs(col_width//2 - image.width//2)
    elif x == Position.LEFT:
        x = 0

    if y == Position.CENTER:
        y = abs(col_height//2 - image.height//2)
    elif y == Position.BOTTOM:
        y = col_height - image.height
    elif y == Position.TOP:
        y = 0

    return x, y


def convert_time(date: str, time: str) -> datetime:
    """
    Convert from UTC to local timezone
    @param date: GP's date (UTC)
    @param time: GP's time (UTC)
    @return: GP's date & time (user's local timezone)
    """
    dt = datetime.strptime(f'{date} {time}'.replace('Z', ''), '%Y-%m-%d %H:%M:%S')
    dt = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)  # Convert to local timezone
    return dt


def race_weekend(date: datetime) -> bool:
    """
    Determine if today is race weekend (i.e. Practice, Qualifying, or Race day).
    @param date: GP's date
    @return: race_weekend: bool
    """
    today = datetime.today()
    if today.weekday() > 3:  # is weekend
        gp_day = date.date().day
        return gp_day - 2 <= today.day <= gp_day
    return False


def is_wdc_champion(races: list, standings) -> bool:
    """
    Determine if there's a champion for the World Driver's Championship
    @param races: List of remaining races
    @param standings: Driver standings
    @return: bool value
    """
    max_remaining_pts = len(races) * 26  # Pos. 1 + Fastest Lap
    for race in races:
        if race.sprint:
            max_remaining_pts += 8  # Pos. 1
    return standings.items[1].points + max_remaining_pts < standings.items[0].points


def is_wcc_champion(races: list, standings) -> bool:
    """
    Determine if there's a champion for the World Constructor's Championship
    @param races: List of remaining races
    @param standings: Constructor standings
    @return: is_wdc_champion bool value
    """
    max_remaining_pts = len(races) * (25 + 19 + 1)  # Pos. 1 + Pos. 2 + Fastest Lap
    for race in races:
        if race.sprint:
            max_remaining_pts += (8 + 7)  # Pos. 1 + Pos. 2
    return standings.items[1].points + max_remaining_pts < standings.items[0].points


def get_session_status(start_time: datetime) -> SessionStatus:
    """
    Roughly determine the session's current status. Does not account for delays.
    @param start_time: GP's start date & time
    @return: status: GP's status
    """
    now = datetime.now().astimezone(tz=None)
    end_time = start_time + timedelta(hours=2)
    if now < start_time:
        return SessionStatus.UPCOMING
    elif start_time < now <= end_time:
        return SessionStatus.IN_PROGRESS
    elif now >= end_time:
        return SessionStatus.FINISHED


def args() -> argparse.Namespace:
    """
    CLI argument parser to configure matrix.
    @return: parser: (argsparse.Namespace) Argument parser
    """
    parser = argparse.ArgumentParser(prog='F1-LED-Leaderboard')

    parser.add_argument('--led-rows',
                        action='store',
                        help='Display rows. 16 for 16x32, 32 for 32x64, etc. (Default: 32)',
                        type=int,
                        default=32)
    parser.add_argument('--led-cols',
                        action='store',
                        help='Display columns. 32 for 16x32, 64 for 32x62, etc. (Default: 64)',
                        type=int,
                        default=64)
    parser.add_argument('--led-multiplexing',
                        action='store',
                        help='Multiplexing type: 0 = direct; 1 = strip; 2 = checker; 3 = spiral; 4 = Z-strip; '
                             '5 = ZnMirrorZStripe; 6 = coreman; 7 = Kaler2Scan; 8 = ZStripeUneven. (Default: 0)',
                        type=int,
                        choices=range(9),
                        default=0)
    parser.add_argument('--led-row-addr-type',
                        action='store',
                        help='Addressing of rows: 0 = default; 1 = AB-addressed panels; 2 = direct row select; '
                             '3 = ABC-addressed panels. (Default: 0)',
                        type=int,
                        choices=range(4),
                        default=0)
    parser.add_argument('--led-panel-type',
                        action='store',
                        help='Chipset of the panel. Supported panel types: FM6126A; FM6127.',
                        type=str,
                        choices=['FM6126A', 'FM6127'],
                        default='')
    parser.add_argument('--led-gpio-mapping',
                        help='Name of GPIO mapping used: regular, adafruit-hat, adafruit-hat-pwm, compute-module',
                        type=str,
                        choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm', 'compute-module'],
                        default='regular')
    parser.add_argument('--led-slowdown-gpio',
                        action='store',
                        help="Slow down writing to GPIO. Needed for faster Pi's and/or slower panels. Range: 0..4. "
                             '(Default: 1)',
                        type=int,
                        choices=range(5),
                        default=1)
    parser.add_argument('--led-chain',
                        action='store',
                        help='Number of daisy-chained boards. (Default: 1)',
                        type=int,
                        default=1)
    parser.add_argument('--led-parallel',
                        action='store',
                        help='For Plus-models or RPi2: parallel chains. 1..3. (Default: 1)',
                        type=int,
                        default=1)
    parser.add_argument('--led-pixel-mapper',
                        action='store',
                        help='Apply pixel mappers: '
                             'Mirror (Horizontal) = \"Mirror:H\"; '
                             'Mirror (Vertical) = \"Mirror:V\"; '
                             'Rotate (Degrees) = eg. \"Rotate: 90\"; '
                             'U-Mapper = \"U-mapper\"',
                        type=str,
                        default='')
    parser.add_argument('--led-brightness',
                        action='store',
                        help='Brightness level. Range: 1..100. (Default: 100)',
                        type=int,
                        choices=range(101),
                        default=100)
    parser.add_argument('--led-pwm-bits',
                        action='store',
                        help='Bits used for PWM. Range 1..11. (Default: 11)',
                        type=int,
                        choices=range(12),
                        default=11)
    parser.add_argument('--led-show-refresh',
                        action='store_true',
                        help='Shows the current refresh rate of the LED panel.')
    parser.add_argument('--led-limit-refresh',
                        action='store',
                        help='Limit refresh rate to this frequency in Hz. Useful to keep a constant refresh rate on '
                             'loaded system. 0=no limit. (Default: 0)',
                        type=int,
                        default=0)
    parser.add_argument('--led-scan-mode',
                        action='store',
                        help='Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced. (Default: 1)',
                        type=int,
                        choices=range(2),
                        default=1)
    parser.add_argument('--led-pwm-lsb-nanoseconds',
                        action='store',
                        help='Base time-unit for the on-time in the lowest significant bit in nanoseconds. '
                             '(Default: 130)',
                        type=int,
                        default=130)
    parser.add_argument('--led-pwm-dither-bits',
                        action='store',
                        help='Time dithering of lower bits (Default: 0)',
                        type=int,
                        default=0)
    parser.add_argument('--led-no-hardware-pulse',
                        action='store',
                        help="Don't use hardware pin-pulse generation.")
    parser.add_argument('--led-inverse',
                        action='store',
                        help='Switch if your matrix has inverse colors on.')
    parser.add_argument('--led-rgb-sequence',
                        action='store',
                        help='Switch if your matrix has led colors swapped. (Default: RGB)',
                        type=str,
                        default='RGB')

    return parser.parse_args()


def led_matrix_options(args_: argparse.Namespace) -> RGBMatrixOptions:
    """
    Set RGBMatrixOptions from parsed arguments.
    @param args_: (argsparse.Namespace) Parsed arguments from CLI
    @return: options: (rgbmatrix.RGBMatrixOptions) RGBMatrixOptions instance
    :exception AttributeError: If attribute is not found
    """
    options = RGBMatrixOptions()

    options.rows = args_.led_rows
    options.cols = args_.led_cols
    options.multiplexing = args_.led_multiplexing
    options.row_address_type = args_.led_row_addr_type

    if args_.led_panel_type is not None:
        options.panel_type = args_.led_panel_type

    if args_.led_gpio_mapping is not None:
        options.hardware_mapping = args_.led_gpio_mapping

    if args_.led_slowdown_gpio is not None:
        options.gpio_slowdown = args_.led_slowdown_gpio

    options.chain_length = args_.led_chain
    options.parallel = args_.led_parallel
    options.pixel_mapper_config = args_.led_pixel_mapper
    options.brightness = args_.led_brightness
    options.pwm_bits = args_.led_pwm_bits

    if args_.led_show_refresh:
        options.show_refresh_rate = 1

    options.limit_refresh_rate_hz = args_.led_limit_refresh
    options.scan_mode = args_.led_scan_mode
    options.pwm_lsb_nanoseconds = args_.led_pwm_lsb_nanoseconds
    options.pwm_dither_bits = args_.led_pwm_dither_bits

    if args_.led_no_hardware_pulse:
        options.disable_hardware_pulsing = True

    if args_.led_inverse:
        options.inverse_colors = args_.led_inverse

    options.led_rgb_sequence = args_.led_rgb_sequence

    return options
