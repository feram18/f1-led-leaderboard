from PIL import ImageFont

from data.standings import StandingsItem
from renderer.renderer import Renderer
from utils import Color, align_text, Position, get_text_size


class ConstructorStandings(Renderer):
    """
    Render constructor standings

    Arguments:
        data (api.Data):                        Data instance

    Attributes:
        standings (list[StandingsItem]):        Constructor standings
        text_color (tuple):                     Text color
        offset (int):                           Row y-coord offset
        coords (dict):                          Coordinates dictionary
        text_y (int):                           Constructor's name & points y-coord
    """

    def __init__(self, matrix, canvas, draw, layout, data):
        super().__init__(matrix, canvas, draw, layout)
        self.data = data
        self.standings = self.data.constructor_standings.items
        self.text_color = Color.WHITE
        self.offset = self.font_height + 2
        self.coords = self.layout.coords['standings']['constructors']
        self.text_y = self.coords['name']['y']

    def render(self):
        self.new_canvas(self.matrix.width, self.coords['row_height'] * (len(self.standings) + 1) + 1)
        self.render_header()
        for constructor in self.standings:
            self.render_row(constructor)
        self.scroll_up(self.canvas)
        self.text_y = self.coords['name']['y']  # Reset

    def render_header(self):
        x, y = align_text(get_text_size(self.draw, 'Constructors', self.layout.font_bold),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.TOP)
        y += self.coords['header']['offset']['y']

        self.draw.rectangle(((0, 0), (self.matrix.width, y + self.font_height - 1)), Color.GRAY)
        self.draw.text((x, y), 'Constructors', Color.WHITE, self.layout.font_bold)

    def render_row(self, constructor: StandingsItem):
        bg_color, self.text_color = constructor.item.colors
        font = self.draw.getfont()
        if constructor.champion:
            bg_color, self.text_color = Color.GOLD, Color.WHITE
            font = self.layout.font_bold

        self.render_background(bg_color)
        self.render_name(constructor.item.name, font)
        self.render_points(f'{constructor.points:g}', font)

        self.text_y += self.offset

    def render_background(self, color: tuple):
        self.draw.rectangle(((0, self.text_y - 1),
                             (self.matrix.width, self.text_y + self.font_height - 1)),
                            color)

    def render_name(self, name: str, font: ImageFont):
        x = self.coords['name']['x']
        self.draw.text((x, self.text_y), name, self.text_color, font)

    def render_points(self, points: str, font: ImageFont):
        x = align_text(get_text_size(self.draw, points, font),
                       col_width=self.matrix.width,
                       x=Position.RIGHT)[0]
        self.draw.text((x, self.text_y), points, self.text_color, font)
