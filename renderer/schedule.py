import time
from typing import List
from rgbmatrix.graphics import DrawText, DrawLine
from renderer.renderer import Renderer
from data.color import Color
from utils import load_font, align_text_center


class Schedule(Renderer):
    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data

        self.schedule = self.data.schedule

        self.bg_color = Color.GRAY.value
        self.text_color = Color.WHITE.value

        self.font = load_font(self.data.config.layout['fonts']['tom_thumb'])

        self.offset = self.font.height + 2

        self.coords = self.data.config.layout['coords']['schedule']
        self.header_x = align_text_center('Schedule',
                                          canvas_width=self.canvas.width,
                                          font_width=self.font.baseline - 1)[0]
        self.header_y = self.coords['header']['y']
        self.round_x = self.coords['round']['x']
        self.round_y = self.coords['round']['y']
        self.gp_name_x = self.coords['gp']['x']
        self.gp_name_y = self.coords['gp']['y']

    def render(self):
        self.canvas.Clear()

        self.render_header()
        for gp in (self.schedule[:3]):  # Up to index 3
            self.render_row(str(gp.round), gp.circuit.country)
        time.sleep(7.0)

        pages = self.split_pages(self.schedule[3:], 4)  # From index 4 - end
        for page in pages:
            self.render_page(page)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_header(self):
        for x in range(self.canvas.width):
            DrawLine(self.canvas, x, self.header_y - self.header_y, x, self.header_y, self.bg_color)
        DrawText(self.canvas, self.font, self.header_x, self.header_y, self.text_color, 'Schedule')

    def render_page(self, page: list):
        self.canvas.Clear()
        self.round_y = self.gp_name_y = self.font.height  # Reset to top

        for i in range(len(page)):
            self.render_row(str(page[i].round), page[i].circuit.country)
        time.sleep(5.0)

    def render_row(self, round_no: str, gp_name: str):
        self.render_round_number(round_no)
        self.render_background()
        self.render_country(gp_name)

        self.round_y += self.offset
        self.gp_name_y += self.offset

    def render_round_number(self, round_no: str):
        # Background
        for x in range(self.gp_name_x - 3):
            DrawLine(self.canvas, x, self.gp_name_y - self.font.height, x, self.gp_name_y, Color.RED.value)

        # Round Number
        self.round_x = align_text_center(round_no,
                                         canvas_width=12,
                                         font_width=self.font.baseline - 1)[0]
        DrawText(self.canvas, self.font, self.round_x, self.round_y, Color.WHITE.value, round_no)

    def render_background(self):
        self.bg_color = Color.WHITE.value
        for x in range(self.gp_name_x - 2, self.canvas.width):
            DrawLine(self.canvas, x, self.gp_name_y - self.font.height, x, self.gp_name_y, self.bg_color)

    def render_country(self, country: str):
        self.text_color = Color.RED.value
        DrawText(self.canvas, self.font, self.gp_name_x, self.gp_name_y, self.text_color, country)

    @staticmethod
    def split_pages(lst: list, size: int) -> List[list]:
        return [lst[i:i + size] for i in range(0, len(lst), size)]
