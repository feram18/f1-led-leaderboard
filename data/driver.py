import logging
import os
from dataclasses import dataclass, field

from constants import COUNTRY_FLAG_PATH
from data.constructor import Constructor
from utils import NATIONALITIES


@dataclass
class Driver:
    """Data class to represent a driver"""
    id: str
    firstname: str
    lastname: str
    code: str
    number: int
    nationality: str
    constructor: Constructor
    flag: str = field(init=False)

    def __post_init__(self):
        self.flag = self.get_flag(NATIONALITIES.get(self.nationality))

    @staticmethod
    def get_flag(country: str) -> str:
        """
        Get path to flag's image file.
        :param country: Driver's country of origin
        :return: img_path: Path to flag image
        """
        img_path = COUNTRY_FLAG_PATH.format(country)
        if os.path.isfile(img_path):
            return img_path
        logging.error(f'No flag image found for {country}')
