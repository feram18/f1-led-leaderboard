import logging
import os
from dataclasses import dataclass, field
from typing import List

from constants import CONSTRUCTOR_LOGO_PATH
from utils import Color

# Constructors' Background & Text Colors
COLORS = {   # [Background, Text]
    "ALFA": [(153, 0, 0), Color.WHITE],
    "ALPHATAURI": [(39, 40, 79), Color.WHITE],
    "ALPINE": [(14, 29, 45), Color.WHITE],
    "ASTON_MARTIN": [(3, 87, 78), Color.WHITE],
    "FERRARI":  [(255, 0, 0), Color.BLACK],
    "HAAS": [(236, 27, 59), Color.WHITE],
    "MCLAREN": [(255, 134, 1), Color.BLACK],
    "MERCEDES": [(0, 210, 190), Color.BLACK],
    "RED_BULL": [(22, 25, 94), Color.WHITE],
    "WILLIAMS": [(3, 168, 235), Color.BLACK]
}


@dataclass
class Constructor:
    """Data class to represent a constructor (team)"""
    id: str
    name: str
    nationality: str
    logo: str = field(init=False)  # Path to logo image
    colors: List[tuple] = field(init=False)

    def __post_init__(self):
        self.name = self.name.replace('F1 Team', '')  # Shorten unnecessary portion
        self.colors = COLORS[self.id.upper()]

    @staticmethod
    def get_logo(constructor_id: str) -> str:
        """
        Get path to constructor's logo image
        @param constructor_id: Constructor's id
        @return: path to logo image
        """
        img_path = CONSTRUCTOR_LOGO_PATH.format(constructor_id)
        if os.path.isfile(img_path):
            return img_path
        logging.error(f'No logo image found for {constructor_id}')
