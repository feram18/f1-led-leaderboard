from dataclasses import dataclass, field
from rgbmatrix.graphics import Font
from utils import read_json, load_font
from constants import LAYOUT_FILE


@dataclass
class Layout:
    """Matrix Layout class"""
    width: int
    height: int
    coords: dict = field(init=False)
    font: Font = field(init=False)

    def __post_init__(self):
        self.coords = read_json(LAYOUT_FILE.format(self.width, self.height))
        self.font = load_font('rpi-rgb-led-matrix/fonts/tom-thumb.bdf')
