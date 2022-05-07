import time
from typing import Tuple
from rgbmatrix.graphics import DrawText, DrawLine
from renderer.renderer import Renderer
from utils import Color, align_text, Position, load_image


class DriverStandings(Renderer):
    """
    Render driver standings

    Arguments:
        data (api.Data):                            Data instance

    Attributes:
        standings (list[StandingsItem]):            Driver standings list
        bg_color (rgbmatrix.graphics.Color):        Background color
        text_color (rgbmatrix.graphics.Font):       Text color
        offset (int):                               Row y-coord offset
        coords (dict):                              Coordinates dictionary
        position_y (int):                           Driver's position y-coord
        flag_y_offset (int):                         Driver's flag y-coord offset
        code_x (int):                               Driver's code x-coord
        code_y (int):                               Driver's code y-coord
        points_y (int):                             Driver's points y-coord
    """

    def __init__(self, matrix, canvas, config, data):
        super().__init__(matrix, canvas, config)
        self.data = data

        self.standings = self.data.driver_standings.items

        self.bg_color = Color.GRAY.value
        self.text_color = Color.WHITE.value

        self.offset = self.font.height + 2

        self.coords = self.config.layout.coords['standings']

        self.position_y = self.coords['position']['y']
        self.flag_y_offset = self.coords['flag']['y-offset']
        self.code_x = self.coords['code']['x']
        self.code_y = self.coords['code']['y']
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
        header_x = align_text('Drivers',
                              x=Position.CENTER,
                              col_width=self.canvas.width,
                              font_width=self.font.baseline - 1)
        y = self.coords['header']['y']

        for x in range(self.canvas.width):
            DrawLine(self.canvas, x, y - y, x, y, self.bg_color)
        DrawText(self.canvas, self.font, header_x, y, self.text_color, 'Drivers')

    def render_page(self, page: Tuple[int, int]):
        for i in range(page[0], page[1]):
            self.render_row(i)
        time.sleep(5.0)

        # self.flag_y_offset = 0
        self.position_y = self.code_y = self.points_y = self.font.height  # Reset to top
        self.canvas.Clear()

    def render_row(self, i: int):
        self.bg_color = self.standings[i].item.constructor.colors[0]
        self.text_color = self.standings[i].item.constructor.colors[1]

        self.render_background()
        # self.render_flag(self.standings[i].item.flag)
        self.render_position(str(self.standings[i].position))
        self.render_code(self.standings[i].item.code)
        # self.render_lastname(self.standings[i].item.lastname)
        self.render_points(f'{self.standings[i].points:g}')

        # self.flag_y_offset += self.offset
        self.position_y += self.offset
        self.code_y += self.offset
        self.points_y += self.offset

    def render_background(self):
        for x in range(self.code_x - 1, self.canvas.width):
            DrawLine(self.canvas, x, self.code_y - self.font.height, x, self.code_y, self.bg_color)

    def render_flag(self, flag_path: str):
        flag = load_image(flag_path, (12, 6))
        x_offset = self.coords['flag']['x-offset']
        self.canvas.SetImage(flag, x_offset, self.flag_y_offset)

    def render_position(self, position: str):
        # Background
        for x in range(self.code_x - 2):
            DrawLine(self.canvas, x, self.code_y - self.font.height, x, self.code_y, Color.WHITE.value)

        # Number
        x = align_text(position,
                       x=Position.CENTER,
                       col_width=12,
                       font_width=self.font.baseline - 1)
        DrawText(self.canvas, self.font, x, self.position_y, Color.BLACK.value, position)

    def render_code(self, code: str):
        DrawText(self.canvas, self.font, self.code_x, self.code_y, self.text_color, code)

    def render_lastname(self, lastname: str):
        DrawText(self.canvas, self.font, self.code_x, self.code_y, self.text_color, lastname)

    def render_points(self, points: str):
        x = align_text(points,
                       x=Position.RIGHT,
                       col_width=self.canvas.width,
                       font_width=self.font.baseline - 1)
        DrawText(self.canvas, self.font, x, self.points_y, self.text_color, points)
