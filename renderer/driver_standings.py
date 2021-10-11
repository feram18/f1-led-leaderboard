import time
from typing import List, Tuple
from PIL import Image
from rgbmatrix.graphics import DrawText, DrawLine
from renderer.renderer import Renderer
from data.color import Color
from utils import load_font, align_text_center, align_text_right


class DriverStandings(Renderer):
    """
    Render driver standings

    Arguments:
        data (data.Data):                           Data instance

    Attributes:
        standings (List[DriverStandingsItem]):      Driver standings list
        bg_color (rgbmatrix.graphics.Color):        Background color
        text_color (rgbmatrix.graphics.Font):       Text color
        font (rgbmatrix.graphics.Font):             Font instance
        offset (int):                               Row y-coord offset
        coords (dict):                              Coordinates dictionary
        header_x (int):                             Table header's x-coord
        header_y (int):                             Table header's y-coord
        position_x (int):                           Driver's position x-coord
        position_y (int):                           Driver's position y-coord
        flag_x_offset (int):                        Driver's flag x-coord offset
        flag_y_offset (int):                        Driver's flag y-coord offset
        code_x (int):                               Driver's code x-coord
        code_y (int):                               Driver's code y-coord
        points_x (int):                             Driver's points x-coord
        points_y (int):                             Driver's points y-coord
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data

        self.standings = self.data.driver_standings

        self.bg_color = Color.GRAY.value  # Table header's bg color
        self.text_color = Color.WHITE.value  # Table header's text color

        self.font = load_font(self.data.config.layout['fonts']['tom_thumb'])

        self.offset = self.font.height + 2

        self.coords = self.data.config.layout['coords']['standings']
        self.header_x = align_text_center('Drivers',
                                          canvas_width=self.canvas.width,
                                          font_width=self.font.baseline - 1)[0]
        self.header_y = self.coords['header']['y']
        self.position_x = self.coords['position']['x']
        self.position_y = self.coords['position']['y']
        self.flag_x_offset = self.coords['flag']['x']
        self.flag_y_offset = self.coords['flag']['y']
        self.code_x = self.coords['code']['x']
        self.code_y = self.coords['code']['y']
        self.points_x = self.coords['points']['x']
        self.points_y = self.coords['points']['y']

    def render(self):
        self.canvas.Clear()

        self.render_header()

        pages = [(0, 3),  # No.1 - 3
                 (3, 7),  # No.3 - 6
                 (7, 11),  # No.7 - 10
                 (11, 15),  # No.11 - 14
                 (15, 19),  # No.15 - 18
                 (19, len(self.standings))]  # No.19 - 20
        for page in pages:
            self.render_page(page)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_header(self):
        for x in range(self.canvas.width):
            DrawLine(self.canvas, x, self.header_y - self.font.height, x, self.header_y, self.bg_color)
        DrawText(self.canvas, self.font, self.header_x, self.header_y, self.text_color, 'Drivers')

    def render_page(self, page: Tuple[int, int]):
        for i in range(page[0], page[1]):
            self.render_row(i)
        time.sleep(5.0)

        # self.flag_y_offset = 0
        self.position_y = self.code_y = self.points_y = self.header_y  # Reset to top
        self.canvas.Clear()

    def render_row(self, i: int):
        self.bg_color = self.standings[i].driver.constructor.colors[0]
        self.text_color = self.standings[i].driver.constructor.colors[1]

        self.render_background()
        # self.render_flag(self.standings[i].driver.flag)
        self.render_position(self.standings[i].position)
        self.render_code(self.standings[i].driver.code)
        # self.render_lastname(self.standings[i].driver.lastname)
        self.render_points(self.standings[i].points)

        # self.flag_y_offset += self.offset
        self.position_y += self.offset
        self.code_y += self.offset
        self.points_y += self.offset

    def render_background(self):
        for x in range(self.code_x - 2, self.canvas.width):
            DrawLine(self.canvas, x, self.code_y - self.font.height, x, self.code_y, self.bg_color)

    def render_flag(self, flag: Image):
        self.canvas.SetImage(flag, self.flag_x_offset, self.flag_y_offset)

    def render_position(self, position: str):
        # Background
        for x in range(self.code_x - 3):
            DrawLine(self.canvas, x, self.code_y - self.font.height, x, self.code_y, Color.WHITE.value)

        # Number
        self.position_x = align_text_center(position,
                                            canvas_width=12,
                                            font_width=self.font.baseline - 1)[0]
        DrawText(self.canvas, self.font, self.position_x, self.position_y, Color.BLACK.value, position)

    def render_code(self, code: str):
        DrawText(self.canvas, self.font, self.code_x, self.code_y, self.text_color, code)

    def render_lastname(self, lastname: str):
        DrawText(self.canvas, self.font, self.code_x, self.code_y, self.text_color, lastname)

    def render_points(self, points: str):
        self.points_x = align_text_right(points, self.canvas.width, self.font.baseline - 1)
        DrawText(self.canvas, self.font, self.points_x, self.points_y, self.text_color, points)
