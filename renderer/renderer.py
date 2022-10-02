import time
from abc import ABC, abstractmethod

from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix

from config.layout import Layout
from constants import DELAY, SCROLL_DELAY
from utils import Color


class Renderer(ABC):
    """
    Base Renderer abstract class

    Arguments:
        matrix (rgbmatrix.RGBMatrix):       RGBMatrix instance
        canvas (PIL.Image):                 Image canvas associated with matrix
        draw (PIL.ImageDraw):               ImageDraw instance
        layout (config.Layout):              Layout instance

    Attributes:
        font (PIL.ImageFont):               Default font.py
        font_width (int):                   Font's character width
        font_height (int):                  Font's character height
    """

    def __init__(self, matrix, canvas, draw, layout):
        self.matrix: RGBMatrix = matrix
        self.canvas: Image = canvas
        self.draw: ImageDraw = draw
        self.layout: Layout = layout
        self.font: ImageFont = self.layout.font
        self.font_width, self.font_height = self.font.getsize(' ')

    @abstractmethod
    def render(self):
        pass

    def clear(self):
        self.draw.rectangle(((0, 0), (self.matrix.width, self.matrix.height)), fill=Color.BLACK)

    def new_canvas(self, width: int, height: int):
        self.clear()
        self.canvas = Image.new('RGB', (width, height))
        self.draw = ImageDraw.Draw(self.canvas)

    def scroll_up(self, image: Image):
        self.matrix.SetImage(self.canvas)
        time.sleep(DELAY)

        pos, bottom = 0, -(image.height - self.matrix.height)
        while pos != bottom:
            self.matrix.SetImage(self.canvas, 0, pos)
            pos -= 1
            time.sleep(SCROLL_DELAY)
        time.sleep(DELAY)
