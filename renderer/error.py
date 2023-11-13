import time

from constants import ERROR_IMAGE, SLIDE_DELAY
from renderer.renderer import Renderer
from utils import Color, align_text, Position, load_image, align_image, get_text_size


class Error(Renderer):
    """
    Renderer for error messages

    Arguments:
        data (api.Data):        Data instance

    Attributes:
        coords (dict):          Coordinates dictionary
        msg (str):              Error message string
    """

    def __init__(self, matrix, canvas, draw, layout, data):
        super().__init__(matrix, canvas, draw, layout)
        self.data = data
        self.coords = self.layout.coords['error']
        self.msg = self.data.status

    def render(self):
        self.clear()
        self.render_image()
        self.render_error_msg()
        self.matrix.SetImage(self.canvas)
        time.sleep(SLIDE_DELAY * 2)

    def render_error_msg(self):
        x, y = align_text(get_text_size(self.draw, self.msg, self.layout.font_bold),
                          self.matrix.width,
                          self.matrix.height)
        self.draw.text((x, y), self.msg, Color.RED, self.layout.font_bold)

    def render_image(self):
        img = load_image(ERROR_IMAGE, tuple(self.coords['image']['size']))
        x, y = align_image(img,
                           self.matrix.width,
                           self.matrix.height,
                           Position.CENTER,
                           Position.TOP)
        self.canvas.paste(img, (x, y + 1))
