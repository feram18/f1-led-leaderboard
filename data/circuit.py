import os
import logging
from dataclasses import dataclass
from constants import CIRCUIT_LOGO_PATH, TRACK_IMAGE_PATH


@dataclass
class Circuit:
    """Data class to represent a circuit"""
    id: str
    name: str
    locality: str
    country: str
    logo: str = None
    track: str = None

    def __post_init__(self):
        self.logo = self.get_logo(self.id)
        self.track = self.get_track(self.id)

    @staticmethod
    def get_logo(circuit_id: str) -> str:
        """
        Get circuit's logo.
        :param circuit_id: (str) Circuit's Id
        :return: logo_image: (str) Path to logo image
        """
        if os.path.isfile(CIRCUIT_LOGO_PATH.format(circuit_id)):
            return CIRCUIT_LOGO_PATH.format(circuit_id)
        else:
            # TODO: Set to country flag
            logging.error(f'No logo image found for {circuit_id}')

    @staticmethod
    def get_track(circuit_id: str) -> str:
        """
        Get circuit's track.
        :param circuit_id: (str) Circuit's Id
        :return: track_image: (str) Path to track image
        """
        if os.path.isfile(TRACK_IMAGE_PATH.format(circuit_id)):
            return TRACK_IMAGE_PATH.format(circuit_id)
        else:
            logging.error(f'No track image found for {circuit_id}')
