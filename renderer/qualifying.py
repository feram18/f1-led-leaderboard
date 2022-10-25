import time
from typing import List

from constants import SLIDE_DELAY
from data.session_status import SessionStatus
from data.qualifying import QualifyingResultItem
from renderer.renderer import Renderer
from utils import Color, align_text, Position


class Qualifying(Renderer):
    """
    Render qualifying results for upcoming grand prix

    Arguments:
        data (data.Data):                   Data instance

    Attributes:
        qualifying (data.Qualifying):       Qualifying data
        sprint (data.Sprint):               Sprint qualifying data
        coords (dict):                      Coordinates dictionary
        offset (int):                       Row y-coord offset
        position_x (int):                   Driver's grid position x-coord
        text_y (int):                       Driver's grid position & code y-coord
        code_x (int):                       Driver's code x-coord
    """

    def __init__(self, matrix, canvas, draw, layout, data):
        super().__init__(matrix, canvas, draw, layout)
        self.data = data
        self.qualifying = self.data.next_gp.qualifying
        self.sprint = self.data.next_gp.sprint
        self.coords = self.layout.coords['qualifying']
        self.offset = self.coords['row']['height'] // 2
        self.position_x = self.coords['grid']['odd']['result']['position']['x']
        self.text_y = self.coords['grid']['odd']['result']['position']['y']
        self.code_x = self.coords['grid']['odd']['code']['x']

    def render(self):
        if self.data.next_gp:
            if self.qualifying.grid:
                height = (self.coords['row']['height'] *
                          (len(self.qualifying.grid) // 2)) + self.coords['row']['height'] // 2
                self.new_canvas(self.matrix.width, height)

                self.render_grid(self.qualifying.grid)

                if self.sprint:
                    if not self.sprint.grid:
                        self.render_upcoming('Sprint', self.sprint.status)
                    else:
                        self.render_grid(self.sprint.grid)
            else:
                self.new_canvas(self.matrix.width, self.matrix.height)
                self.render_upcoming('Qualifying', self.qualifying.status)

    def render_header(self, header: str):
        x, y = align_text(self.layout.font_bold.getsize(header),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.TOP)
        y += self.coords['header']['offset']['y']

        self.draw.rectangle(((0, 0), (self.matrix.width, y + self.font_height - 1)), Color.RED)
        self.draw.text((x, y), header, Color.WHITE, self.layout.font_bold)

    def render_status(self, status: str):
        x, y = align_text(self.layout.font_bold.getsize(status),
                          self.matrix.width,
                          self.matrix.height)
        y += (self.font_height // 2)
        self.draw.text((x, y), status, Color.WHITE, self.layout.font_bold)

    def render_row(self, item: QualifyingResultItem):
        parity = 'even' if item.position % 2 == 0 else 'odd'
        self.position_x = self.coords['grid'][parity]['result']['position']['x']
        self.code_x = self.coords['grid'][parity]['code']['x']

        self.render_code(item.driver.code, item.driver.constructor.colors)
        self.render_position(str(item.position), self.coords['grid'][parity]['result']['width'])

        self.text_y += self.offset

    def render_position(self, position: str, pos_width: int):
        self.draw.rectangle(((self.position_x, self.text_y - 1),
                             (self.code_x - 2, self.text_y + self.font_height - 1)),
                            Color.WHITE)

        self.position_x += align_text(self.layout.font.getsize(position),
                                      col_width=pos_width,
                                      x=Position.CENTER)[0]
        self.draw.text((self.position_x, self.text_y), position, Color.BLACK, self.layout.font)

    def render_code(self, code: str, colors: List[tuple]):
        bg, text = colors
        self.draw.rectangle(((self.code_x - 1, self.text_y - 1),
                             (self.code_x + self.coords['row']['width'] - 1, self.text_y + self.font_height - 1)),
                            bg)
        self.draw.text((self.code_x, self.text_y), code, text, self.layout.font)

    def render_upcoming(self, header: str, status: SessionStatus):
        self.render_header(header)
        self.render_status(status.value)
        self.matrix.SetImage(self.canvas)
        time.sleep(SLIDE_DELAY)

    def render_grid(self, grid: list):
        for item in grid:
            self.render_row(item)
        self.scroll_up(self.canvas)
        self.text_y = self.coords['grid']['odd']['result']['position']['y']  # Reset
