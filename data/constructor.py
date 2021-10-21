import os
import logging
from dataclasses import dataclass
from data.color import Color
from constants import CONSTRUCTOR_LOGO_PATH


@dataclass
class Constructor:
    """Data class to represent a constructor (team)"""
    id: str
    name: str
    nationality: str
    logo: str = None
    colors: Color = None

    def __post_init__(self):
        self.name = self.name.replace('F1 Team', '')  # Shorten unnecessary portion

        self.colors = Color[self.id.upper()].value

    @staticmethod
    def get_logo(constructor_id) -> str:
        if os.path.isfile(CONSTRUCTOR_LOGO_PATH.format(constructor_id)):
            return CONSTRUCTOR_LOGO_PATH.format(constructor_id)
        else:
            logging.error(f'No logo image found for {constructor_id}')
