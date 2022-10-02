from constants import F1_LOGO
from renderer.renderer import Renderer
from utils import Color, align_text, Position, load_image, align_image
from version import __version__


class Loading(Renderer):
    """
    Render a splash screen while data is fetched

    Attributes:
        coords (dict):      Coordinates dictionary
    """

    def __init__(self, matrix, canvas, draw, layout):
        super().__init__(matrix, canvas, draw, layout)
        self.coords = self.layout.coords['loading']
        self.render()

    def render(self):
        self.render_logo()
        self.render_version()
        self.matrix.SetImage(self.canvas)

    def render_version(self):
        x, y = align_text(self.font.getsize(__version__),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.BOTTOM)
        self.draw.text((x, y), __version__, fill=Color.WHITE, font=self.font)

    def render_logo(self):
        logo = load_image(F1_LOGO, tuple(self.coords['image']['size']))
        x, y = align_image(logo,
                           self.matrix.width,
                           self.matrix.height)
        self.canvas.paste(logo, (x, y))
