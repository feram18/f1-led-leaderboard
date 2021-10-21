from rgbmatrix.graphics import DrawText
from renderer.renderer import Renderer
from utils import align_text_center, load_image, center_image
from constants import F1_LOGO
from version import __version__
from data.color import Color


class Loading(Renderer):
    """
    Render a splash screen while data is fetched

    Attributes:
        coords (dict):      Coordinates dictionary
    """

    def __init__(self, matrix, canvas, config):
        super().__init__(matrix, canvas, config)

        self.coords = self.config.layout.coords['loading']

    def render(self):
        self.canvas.Clear()

        self.render_logo()
        self.render_version()

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_version(self):
        x = align_text_center(string=__version__,
                              canvas_width=self.canvas.width,
                              font_width=self.font.baseline - 1)[0]
        y = self.coords['version']['y']
        DrawText(self.canvas, self.font, x, y, Color.WHITE.value, __version__)

    def render_logo(self):
        logo = load_image(F1_LOGO, (64, 28))
        x_offset, y_offset = center_image(logo.size,
                                          self.canvas.width,
                                          self.canvas.height)
        self.canvas.SetImage(logo, x_offset, y_offset)
