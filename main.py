import logging
import sys
from logging.handlers import RotatingFileHandler

from PIL import Image, ImageDraw
from rgbmatrix import RGBMatrix

from api.data import Data
from config.layout import Layout
from renderer.loading import Loading
from renderer.main import MainRenderer
from utils import led_matrix_options, args
from version import __version__


def main():
    print(f'\U0001F3C1 F1-LED-Leaderboard - v{__version__} ({matrix.width}x{matrix.height})')
    layout = Layout(matrix.width, matrix.height)
    Loading(matrix, canvas, draw, layout)
    data = Data()
    MainRenderer(matrix, canvas, draw, layout, data)


if __name__ == '__main__':
    # Set logging level
    if '--debug' in sys.argv:
        LOG_LEVEL = logging.DEBUG
        sys.argv.remove('--debug')
    else:
        LOG_LEVEL = logging.WARNING

    # Set logger configuration
    logger = logging.getLogger('')  # root logger
    logger.setLevel(LOG_LEVEL)
    handler = RotatingFileHandler(filename='f1-led-leaderboard.log',
                                  maxBytes=5 * 1024 * 1024,  # 5MB
                                  backupCount=4)
    handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s: %(message)s',
                                           datefmt='%m/%d/%Y %I:%M:%S %p'))
    logger.addHandler(handler)

    # Initialize the matrix
    matrix = RGBMatrix(options=led_matrix_options(args()))
    canvas = Image.new('RGB', (matrix.width, matrix.height))
    draw = ImageDraw.Draw(canvas)
    matrix.SetImage(canvas)

    try:
        main()
    except Exception as e:  # For any random unhandled exceptions
        logging.exception(SystemExit(e))
    finally:
        matrix.Clear()
