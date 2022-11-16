from dataclasses import dataclass, field

from PIL import ImageFont

from utils import read_json, load_font
from constants import LAYOUT_FILE


@dataclass
class Layout:
    """Matrix Layout class"""
    width: int
    height: int
    coords: dict = field(init=False)
    font: ImageFont = field(init=False)
    font_bold: ImageFont = field(init=False)

    def __post_init__(self):
        self.coords = read_json(LAYOUT_FILE.format(self.width, self.height))
        self.font = load_font(self.coords['font']['regular'])
        bold = self.coords.get('font').get('bold', None)
        self.font_bold = load_font(bold) if bold else self.font
