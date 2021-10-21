from dataclasses import dataclass, field
from config.layout import Layout


@dataclass
class MatrixConfig:
    """Matrix Configuration class"""
    width: int
    height: int
    layout: Layout = field(init=False)

    def __post_init__(self):
        self.layout = Layout(self.width, self.height)
