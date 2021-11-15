import os
import logging
from dataclasses import dataclass, field
from constants import CIRCUIT_LOGO_PATH, TRACK_IMAGE_PATH


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
        self.logo = self.get_logo(self.id)
        self.track = self.get_track(self.id)

    @staticmethod
    def get_logo(circuit_id: str) -> str:
        """
        Get path to circuit's logo image.
        :param circuit_id: (str) Circuit's Id
        :return: img_path: (str) Path to logo image
        """
        img_path = CIRCUIT_LOGO_PATH.format(circuit_id)
        if os.path.isfile(img_path):
            return img_path
        else:
            # TODO: Set to country flag
            logging.error(f'No logo image found for {circuit_id}')

    @staticmethod
    def get_track(circuit_id: str) -> str:
        """
        Get path to circuit's track image.
        :param circuit_id: (str) Circuit's id
        :return: img_path: (str) Path to track image
        """
        img_path = TRACK_IMAGE_PATH.format(circuit_id)
        if os.path.isfile(img_path):
            return img_path
        logging.error(f'No track image found for {circuit_id}')
