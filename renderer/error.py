import time
from rgbmatrix.graphics import DrawText
from renderer.renderer import Renderer
from utils import align_text_center, load_font, load_image
from constants import ERROR_IMAGE
from data.color import Color


class Error(Renderer):
    """
    Renderer for error messages

    Arguments:
        data (data.Data):                       Data instance

    Attributes:
        font (rgbmatrix.graphics.Font):         Font instance
        coords (dict):                          Coordinates dictionary
        error_msg (str)                         Error message string
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data

        self.font = load_font(self.data.config.layout['fonts']['tom_thumb'])

        self.coords = self.data.config.layout['coords']['error']

        self.error_msg = self.data.status

    def render(self):
        self.canvas.Clear()

        self.render_error_msg()
        time.sleep(15.0)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_error_msg(self):
        x, y = align_text_center(self.error_msg,
                                 self.canvas.width,
                                 self.canvas.height,
                                 self.font.baseline - 1,
                                 self.font.height)
        DrawText(self.canvas, self.font, x, y, Color.RED.value, self.error_msg)

    def render_image(self):
        error_image = load_image(ERROR_IMAGE, (4, 6))
        x_offset = self.coords['image']['x-offset']
        y_offset = self.coords['image']['y-offset']
        self.canvas.SetImage(error_image, x_offset, y_offset)
