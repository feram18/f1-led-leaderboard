import os
import logging
from dataclasses import dataclass
from PIL import Image
from constants import CIRCUIT_LOGO_PATH, TRACK_IMAGE_PATH
from utils import load_image


@dataclass
class Circuit:
    """Data class to represent a circuit"""
    id: str
    name: str
    locality: str
    country: str
    logo: Image = None
    track: Image = None

    def __post_init__(self):
        self.logo = self.get_logo(self.id)
        self.track = self.get_track(self.id)

    @staticmethod
    def get_logo(circuit_id: str) -> Image:
        """
        Get circuit's logo.
        :param circuit_id: (str) Circuit's Id
        :return: logo: (PIL.Image)
        """
        if os.path.isfile(CIRCUIT_LOGO_PATH.format(circuit_id)):
            return load_image(CIRCUIT_LOGO_PATH.format(circuit_id), (64, 25))
        else:
            # TODO: Set to country flag
            logging.error(f'No logo image found for {circuit_id}')

    @staticmethod
    def get_track(circuit_id: str) -> Image:
        """
        Get circuit's track.
        :param circuit_id: (str) Circuit's Id
        :return: track: (PIL.Image)
        """
        if os.path.isfile(TRACK_IMAGE_PATH.format(circuit_id)):
            return load_image(TRACK_IMAGE_PATH.format(circuit_id), (64, 20))
        else:
            logging.error(f'No track image found for {circuit_id}')
