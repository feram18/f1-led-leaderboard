import os
import logging
from dataclasses import dataclass, field
from utils import Color
from constants import CONSTRUCTOR_LOGO_PATH


@dataclass
class Constructor:
    """Data class to represent a constructor (team)"""
    id: str
    name: str
    nationality: str
    logo: str = field(init=False)  # Path to logo image
    colors: Color = field(init=False)

    def __post_init__(self):
        self.name = self.name.replace('F1 Team', '')  # Shorten unnecessary portion
        self.colors = Color[self.id.upper()].value

    @staticmethod
    def get_logo(constructor_id: str) -> str:
        """
        Get path to constructor's logo image
        :param constructor_id: (str) Constructor's id
        :return: logo_path: (str) path to logo image
        """
        if os.path.isfile(CONSTRUCTOR_LOGO_PATH.format(constructor_id)):
            return CONSTRUCTOR_LOGO_PATH.format(constructor_id)
        else:
            logging.error(f'No logo image found for {constructor_id}')
