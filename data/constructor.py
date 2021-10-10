from dataclasses import dataclass
from PIL import Image
from data.color import Color
from constants import CONSTRUCTOR_LOGO_PATH
from utils import load_image


@dataclass
class Constructor:
    """Data class to represent a constructor (team)"""
    id: str
    name: str
    nationality: str
    logo: Image = None
    colors: Color = None

    def __post_init__(self):
        self.name = self.name.replace('F1 Team', '')  # Shorten unnecessary portion
        self.logo = load_image(CONSTRUCTOR_LOGO_PATH.format(self.id), (6, 4))
        self.colors = Color[self.id.upper()].value
