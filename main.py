import sys
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from rgbmatrix import RGBMatrix
from config.matrix_config import MatrixConfig
from api.data import Data
from renderer.loading import Loading
from renderer.main import MainRenderer
from version import __version__
from utils import led_matrix_options, args


def main():
    # Print script details on startup
    print(f'\U0001F3C1 F1-LED-Leaderboard - v{__version__} ({matrix.width}x{matrix.height})')

    # Read software preferences from config.json
    config = MatrixConfig(matrix.width, matrix.height)

    # Create canvas
    canvas = matrix.CreateFrameCanvas()

    # Render loading splash screen
    Loading(matrix, canvas, config).render()

    # Fetch initial data
    data = Data()

    # Begin rendering screen rotation
    MainRenderer(matrix, canvas, config, data).render()


if __name__ == '__main__':
    # Get logging level
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
    handler.setFormatter(Formatter(fmt='%(asctime)s %(levelname)s: %(message)s',
                                   datefmt='%m/%d/%Y %I:%M:%S %p'))
    logger.addHandler(handler)

    # Check matrix configuration arguments
    matrixOptions = led_matrix_options(args())

    # Initialize the matrix
    matrix = RGBMatrix(options=matrixOptions)

    try:
        main()
    except Exception as e:  # For any random unhandled exceptions
        logging.exception(SystemExit(e))
    finally:
        matrix.Clear()
