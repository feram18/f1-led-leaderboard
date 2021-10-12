"""Predefined Color objects class"""
from enum import Enum
from rgbmatrix.graphics import Color as RGB


class Color(Enum):
    """Colors enum class"""

    # Standard colors
    RED = RGB(171, 0, 3)
    ORANGE = RGB(128, 128, 128)
    YELLOW = RGB(239, 178, 30)
    GREEN = RGB(124, 252, 0)
    BLUE = RGB(0, 45, 114)
    PURPLE = RGB(51, 0, 111)
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
