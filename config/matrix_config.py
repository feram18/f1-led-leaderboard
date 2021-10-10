from dataclasses import dataclass, field
from constants import LAYOUT_FILE
from utils import read_json


@dataclass
class MatrixConfig:
    """Matrix Configuration class"""
    width: int
    height: int
    layout: dict = field(init=False)

    def __post_init__(self):
        self.layout = read_json(LAYOUT_FILE.format(self.width, self.height))
