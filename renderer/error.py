import time
from rgbmatrix.graphics import DrawText
from renderer.renderer import Renderer
from utils import align_text_center, load_font, load_image
from constants import ERROR_IMAGE
from data.color import Color


class ErrorRenderer(Renderer):
    """
    Renderer for error messages

    Arguments:
        data (data.Data):                           Data instance

    Attributes:
        error_msg (str)                             Error message string
        error_image (PIL.Image):                    Error image
        font (rgbmatrix.graphics.Font):             Font for error msg
        text_color (rgbmatrix.graphics.Color):      Color for error msg
        error_msg_x (int):                          Error msg's x-coord
        error_msg_y (int):                          Error msg's y-coord
        image_x_offset (int):                       Error image x-coord offset
        image_y_offset (int):                       Error image y-coord offset
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data

        self.text_color = Color.RED.value

        self.coords = self.data.config.layout['coords']['error']

        self.font = load_font(self.data.config.layout['fonts']['tom_thumb'])

        self.error_msg = self.data.status
        self.error_msg_x, self.error_msg_y = align_text_center(self.error_msg,
                                                               self.canvas.width,
                                                               self.canvas.height,
                                                               self.font.baseline - 1,
                                                               self.font.height)

        self.error_image = load_image(ERROR_IMAGE, (4, 6))
        self.image_x_offset = self.coords['image']['x-offset']
        self.image_y_offset = self.coords['image']['y-offset']

    def render(self):
        self.canvas.Clear()

        self.render_error_msg()
        time.sleep(15.0)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_error_msg(self):
        DrawText(self.canvas, self.font, self.error_msg_x, self.error_msg_y, self.text_color, self.error_msg)

    def render_image(self):
        self.canvas.SetImage(self.error_image, self.image_x_offset, self.image_y_offset)
