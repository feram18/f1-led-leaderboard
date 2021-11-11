from rgbmatrix.graphics import DrawText
from renderer.renderer import Renderer
from utils import Color, align_text, Position, load_image, align_image
from constants import F1_LOGO
from version import __version__


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
        x = align_text(__version__,
                       x=Position.CENTER,
                       col_width=self.canvas.width,
                       font_width=self.font.baseline - 1)
        y = self.coords['version']['y']
        DrawText(self.canvas, self.font, x, y, Color.WHITE.value, __version__)

    def render_logo(self):
        logo = load_image(F1_LOGO, (64, 28))
        x_offset, y_offset = align_image(logo,
                                         Position.CENTER,
                                         Position.CENTER,
                                         self.canvas.width,
                                         self.canvas.height)
        self.canvas.SetImage(logo, x_offset, y_offset)
