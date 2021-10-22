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
        :return: logo_path: (str) Path to logo image
        """
        if os.path.isfile(CIRCUIT_LOGO_PATH.format(circuit_id)):
            return CIRCUIT_LOGO_PATH.format(circuit_id)
        else:
            # TODO: Set to country flag
            logging.error(f'No logo image found for {circuit_id}')

    @staticmethod
    def get_track(circuit_id: str) -> str:
        """
        Get path to circuit's track image.
        :param circuit_id: (str) Circuit's id
        :return: track_path: (str) Path to track image
        """
        if os.path.isfile(TRACK_IMAGE_PATH.format(circuit_id)):
            return TRACK_IMAGE_PATH.format(circuit_id)
        else:
            logging.error(f'No track image found for {circuit_id}')
