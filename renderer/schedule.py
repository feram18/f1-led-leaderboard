import time
from rgbmatrix.graphics import DrawText, DrawLine
from renderer.renderer import Renderer
from data.color import Color
from utils import load_font, align_text_center, split_into_pages


class Schedule(Renderer):
    """
    Render schedule of remaining grand prix in the current season

    Arguments:
        data (data.Data):                       Data instance

    Attributes:
        schedule ():                            GP schedule
        font (rgbmatrix.graphics.Font):         Font instance
        offset (int):                           Row y-coord offset
        coords (dict):                          Coordinates dictionary
        round_x (int):                          Round x-coord
        round_y (int):                          Round y-coord
        country_x (int):                        Country x-coord
        country_y (int):                        Country y-coord
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data

        self.schedule = self.data.schedule

        self.font = load_font(self.data.config.layout['fonts']['tom_thumb'])

        self.offset = self.font.height + 2

        self.coords = self.data.config.layout['coords']['schedule']
        self.round_x = self.coords['round']['x']
        self.round_y = self.coords['round']['y']
        self.country_x = self.coords['country']['x']
        self.country_y = self.coords['country']['y']

    def render(self):
        self.canvas.Clear()

        self.render_header()
        for gp in (self.schedule[:3]):  # Up to index 3
            self.render_row(str(gp.round), gp.circuit.country)
        time.sleep(7.0)

        pages = split_into_pages(self.schedule[3:], 4)  # From index 4 - end
        for page in pages:
            self.render_page(page)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_header(self):
        bg_color = Color.GRAY.value
        text_color = Color.WHITE.value
        x = align_text_center('Schedule',
                              canvas_width=self.canvas.width,
                              font_width=self.font.baseline - 1)[0]
        y = self.coords['header']['y']

        for x in range(self.canvas.width):
            DrawLine(self.canvas, x, y - y, x, y, bg_color)
        DrawText(self.canvas, self.font, x, y, text_color, 'Schedule')

    def render_page(self, page: list):
        self.canvas.Clear()
        self.round_y = self.country_y = self.font.height  # Reset to top

        for i in range(len(page)):
            self.render_row(str(page[i].round), page[i].circuit.country)
        time.sleep(5.0)

    def render_row(self, round_no: str, country: str):
        self.render_round_number(round_no)
        self.render_background()
        self.render_country(country)

        self.round_y += self.offset
        self.country_y += self.offset

    def render_round_number(self, round_no: str):
        # Background
        for x in range(self.country_x - 2):
            DrawLine(self.canvas, x, self.country_y - self.font.height, x, self.country_y, Color.RED.value)

        # Round Number
        self.round_x = align_text_center(round_no,
                                         canvas_width=12,
                                         font_width=self.font.baseline - 1)[0]
        DrawText(self.canvas, self.font, self.round_x, self.round_y, Color.WHITE.value, round_no)

    def render_background(self):
        bg_color = Color.WHITE.value
        for x in range(self.country_x - 1, self.canvas.width):
            DrawLine(self.canvas, x, self.country_y - self.font.height, x, self.country_y, bg_color)

    def render_country(self, country: str):
        text_color = Color.RED.value
        DrawText(self.canvas, self.font, self.country_x, self.country_y, text_color, country)
