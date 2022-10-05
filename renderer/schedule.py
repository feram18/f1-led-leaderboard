from data.grand_prix import GrandPrix
from renderer.renderer import Renderer
from utils import Color, align_text, Position


class Schedule(Renderer):
    """
    Render schedule of remaining grand prix in the current season

    Arguments:
        data (api.Data):                        Data instance

    Attributes:
        schedule (List[data.GrandPrix]):        GP schedule
        offset (int):                           Row y-coord offset
        coords (dict):                          Coordinates dictionary
        text_y (int):                           Round & Country y-coord
        country_x (int):                        Country x-coord
    """

    def __init__(self, matrix, canvas, draw, layout, data):
        super().__init__(matrix, canvas, draw, layout)
        self.data = data
        self.schedule = self.data.schedule
        self.offset = self.font_height + 2
        self.coords = self.layout.coords['schedule']
        self.country_x = self.coords['country']['x']
        self.text_y = self.coords['round']['position']['y']

    def render(self):
        if self.schedule:
            self.new_canvas(self.matrix.width, self.coords['row_height'] * (len(self.schedule) + 1) + 1)
            self.render_header()
            for gp in self.schedule:
                self.render_row(gp)
            self.scroll_up(self.canvas)
            self.text_y = self.coords['round']['position']['y']  # Reset

    def render_header(self):
        x, y = align_text(self.font.getsize('Schedule'),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.TOP)
        y += self.coords['header']['y']

        self.draw.rectangle(((0, 0), (self.matrix.width, y + self.font_height - 1)), fill=Color.GRAY)
        self.draw.text((x, y), 'Schedule', fill=Color.WHITE, font=self.font)

    def render_row(self, gp: GrandPrix):
        self.render_round_no(str(gp.round))
        self.render_country(gp.circuit.country)

        self.text_y += self.offset

    def render_round_no(self, round_no: str):
        self.draw.rectangle(((0, self.text_y - 1),
                             (self.coords['round']['width'] - 1, self.text_y + self.font_height - 1)),
                            fill=Color.RED)

        x = align_text(self.font.getsize(round_no),
                       col_width=self.coords['round']['width'] + 1,
                       x=Position.CENTER)[0]
        self.draw.text((x, self.text_y), round_no, fill=Color.WHITE, font=self.font)

    def render_country(self, country: str):
        self.draw.rectangle(((self.country_x - 1, self.text_y - 1),
                             (self.matrix.width, self.text_y + self.font_height - 1)),
                            fill=Color.WHITE)
        self.draw.text((self.country_x, self.text_y), country, fill=Color.RED, font=self.font)
