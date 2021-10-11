from rgbmatrix.graphics import DrawText
from renderer.renderer import Renderer
from utils import align_text_center, load_font, load_image, center_image
from constants import F1_LOGO
from version import __version__
from data.color import Color


class Loading(Renderer):
    """
    Render a splash screen while data is fetched

    Arguments:
        config (config.MatrixConfig):               MatrixConfig instance

    Attributes:
        text_color (rgbmatrix.graphics.Color):      Color instance
        font (rgbmatrix.graphics.Font):             Font instance
        logo (PIL.Image):                           Software logo image
        logo_x_offset (int):                        Logo image x-coord
        logo_y_offset (int):                        Logo image y-coord
        version_x (int):                            Version text x-coord
        version_y (int):                            Version text y-coord
    """

    def __init__(self, matrix, canvas, config):
        super().__init__(matrix, canvas)
        self.config = config

        self.text_color = Color.WHITE.value

        self.coords = self.config.layout['coords']['loading']

        self.font = load_font(self.config.layout['fonts']['tom_thumb'])

        self.logo = load_image(F1_LOGO, (64, 28))
        self.logo_x_offset, self.logo_y_offset = center_image(self.logo.size,
                                                              self.canvas.width,
                                                              self.canvas.height)

        self.version_x = align_text_center(string=__version__,
                                           canvas_width=self.canvas.width,
                                           font_width=self.font.baseline - 1)[0]
        self.version_y = self.coords['version']['y']

    def render(self):
        self.canvas.Clear()

        self.render_logo()
        self.render_version()

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_version(self):
        DrawText(self.canvas, self.font, self.version_x, self.version_y, self.text_color, __version__)

    def render_logo(self):
        self.canvas.SetImage(self.logo, self.logo_x_offset, self.logo_y_offset)
