from abc import ABC, abstractmethod


class Renderer(ABC):
    """
    Base Renderer abstract class

    Arguments:
        matrix (rgbmatrix.RGBMatrix):           RGBMatrix instance
        canvas (rgbmatrix.Canvas):              Canvas associated with matrix
        config (config.MatrixConfig):           MatrixConfig instance

    Attributes:
        font (rgbmatrix.graphics.Font):         Default font
    """

    def __init__(self, matrix, canvas, config):
        self.matrix = matrix
        self.canvas = canvas
        self.config = config
        self.font = self.config.layout.font

    @abstractmethod
    def render(self):
        pass
