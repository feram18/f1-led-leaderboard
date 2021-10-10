from dataclasses import dataclass
from PIL import Image
from data.constructor import Constructor
from constants import COUNTRY_FLAG_PATH
from utils import load_image


@dataclass
class Driver:
    """Data class to represent a driver"""
    firstname: str
    lastname: str
    code: str
    number: str
    nationality: str
    constructor: Constructor
    flag: Image = None

    def __post_init__(self):
        self.flag = load_image(COUNTRY_FLAG_PATH.format(self.nationality), (12, 6))
