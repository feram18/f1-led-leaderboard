import time
from typing import List

from constants import SLIDE_DELAY
from data.qualifying import QualifyingResultItem
from renderer.renderer import Renderer
from utils import Color, align_text, Position, get_text_size


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
        self.qualifying = self.data.next_gp.qualifying if self.data.next_gp else None
        self.sprint = self.data.next_gp.sprint if self.data.next_gp else None
        self.coords = self.layout.coords['qualifying']
        self.offset = self.coords['row']['height'] // 2
        self.position_x = self.coords['grid']['odd']['result']['position']['x']
        self.text_y = self.coords['grid']['odd']['result']['position']['y']
        self.code_x = self.coords['grid']['odd']['code']['x']

    def render(self):
        if self.data.next_gp:
            if self.qualifying.grid:
                rh = self.coords['row']['height']
                height = ((rh * (len(self.qualifying.grid) // 2)) + (rh // 2)) + self.coords['header']['height']
                self.new_canvas(self.matrix.width, height)
                self.render_header('Qualifying')
                self.render_grid(self.qualifying.grid)

                if self.sprint:
                    self.new_canvas(self.matrix.width, height)
                    self.render_header('Sprint')
                    if self.sprint.grid:
                        self.render_grid(self.sprint.grid)
                    else:
                        self.render_status(self.sprint.status.value)
            else:
                self.render_header('Qualifying')
                self.render_status(self.qualifying.status.value)

    def render_header(self, header: str):
        x, y = align_text(get_text_size(self.draw, header, self.layout.font_bold),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.TOP)
        y += self.coords['header']['offset']['y']

        self.draw.rectangle(((0, 0), (self.matrix.width, y + self.font_height - 1)), Color.RED)
        self.draw.text((x, y), header, Color.WHITE, self.layout.font_bold)

    def render_status(self, status: str):
        x, y = align_text(get_text_size(self.draw, status, self.layout.font_bold),
                          self.matrix.width,
                          self.matrix.height)
        y += (self.font_height // 2)
        self.draw.text((x, y), status, Color.WHITE, self.layout.font_bold)
        self.matrix.SetImage(self.canvas)
        time.sleep(SLIDE_DELAY)

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

        self.position_x += align_text(get_text_size(self.draw, position, self.draw.getfont()),
                                      col_width=pos_width,
                                      x=Position.CENTER)[0]
        self.draw.text((self.position_x, self.text_y), position, Color.BLACK)

    def render_code(self, code: str, colors: List[tuple]):
        bg, text = colors
        self.draw.rectangle(((self.code_x - 1, self.text_y - 1),
                             (self.code_x + self.coords['row']['width'] - 1, self.text_y + self.font_height - 1)),
                            bg)
        self.draw.text((self.code_x, self.text_y), code, text)

    def render_grid(self, grid: list):
        for item in grid:
            self.render_row(item)
        self.scroll_up(self.canvas)
        self.text_y = self.coords['grid']['odd']['result']['position']['y']  # Reset
