import os
import logging
from dataclasses import dataclass
from data.constructor import Constructor
from constants import COUNTRY_FLAG_PATH


@dataclass
class Driver:
    """Data class to represent a driver"""
    firstname: str
    lastname: str
    code: str
    number: int
    nationality: str
    constructor: Constructor
    flag: str = None

    def __post_init__(self):
        self.flag = self.get_flag(self.nationality)

    @staticmethod
    def get_flag(nationality: str) -> str:
        if os.path.isfile(COUNTRY_FLAG_PATH.format(nationality)):
            return COUNTRY_FLAG_PATH.format(nationality)
        else:
            logging.error(f'No flag image found for {nationality}')
