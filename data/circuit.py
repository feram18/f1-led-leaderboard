import logging
import os
from dataclasses import dataclass, field

from constants import CIRCUIT_LOGO_PATH, TRACK_IMAGE_PATH, COUNTRY_FLAG_PATH


@dataclass
class Circuit:
    """Data class to represent a circuit"""
    id: str
    name: str
    locality: str
    country: str
    logo: str = field(init=False)  # Path to logo image
    track: str = field(init=False)  # Path to track image

    def __post_init__(self):
        self.logo = self.get_logo(self.id, self.country)
        self.track = self.get_track(self.id)

    @staticmethod
    def get_logo(circuit_id: str, country: str) -> str:
        """
        Get path to circuit's logo image.
        :param circuit_id: Circuit's id
        :param country: Country
        :return: img_path: Path to logo image
        """
        img_path = CIRCUIT_LOGO_PATH.format(circuit_id)
        if os.path.isfile(img_path):
            return img_path
        logging.warning(f'No logo image found for {circuit_id}. Setting country flag.')
        return COUNTRY_FLAG_PATH.format(country)

    @staticmethod
    def get_track(circuit_id: str) -> str:
        """
        Get path to circuit's track image.
        :param circuit_id: Circuit's id
        :return: img_path: Path to track image
        """
        img_path = TRACK_IMAGE_PATH.format(circuit_id)
        if os.path.isfile(img_path):
            return img_path
        logging.error(f'No track image found for {circuit_id}')
