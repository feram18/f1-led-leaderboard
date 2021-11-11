import time
from rgbmatrix.graphics import DrawText, DrawLine
from renderer.renderer import Renderer
from utils import Color, align_text, Position, split_into_pages


class Qualifying(Renderer):
    """
    Render qualifying results for upcoming grand prix

    Arguments:
        data (data.Data):                   Data instance

    Attributes:
        qualifying (data.Qualifying):       Qualifying data
        coords (dict):                      Coordinates dictionary
        offset (int):                       Row y-coord offset
        header_x (int):                     Table header's x-coord
        position_x (int):                   Driver's grid position x-coord
        position_y (int):                   Driver's grid position y-coord
        code_x (int):                       Driver's code x-coord
        code_y (int):                       Driver's code y-coord
    """

    def __init__(self, matrix, canvas, config, data):
        super().__init__(matrix, canvas, config)
        self.data = data
        self.qualifying = self.data.qualifying

        self.coords = self.config.layout.coords['qualifying']

        self.offset = 4
        self.header_x = align_text('Qualifying',
                                   x=Position.CENTER,
                                   col_width=self.canvas.width,
                                   font_width=self.font.baseline - 1)
        self.position_x = self.coords['grid']['odd']['position']['x']
        self.position_y = self.coords['grid']['odd']['position']['y']
        self.code_x = self.coords['grid']['odd']['code']['x']
        self.code_y = self.coords['grid']['odd']['code']['y']

    def render(self):
        self.canvas.Clear()

        if self.qualifying is None:
            self.render_header()
            x, y = align_text('Upcoming',
                              Position.CENTER,
                              Position.CENTER,
                              self.canvas.width,
                              self.canvas.height,
                              self.font.baseline - 1,
                              self.font.height)
            DrawText(self.canvas, self.font, x, y, Color.WHITE.value, 'Upcoming')
            time.sleep(7.0)
        else:
            # Render grid
            pages = split_into_pages(self.qualifying.grid, 7)  # 1-7, 8-14, 15-20
            for page in pages:
                self.render_page(page)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_header(self):
        y = self.coords['header']['y']

        # Background
        for x in range(self.canvas.width):
            DrawLine(self.canvas, x, y - self.font.height, x, y, Color.RED.value)

        # Header
        DrawText(self.canvas, self.font, self.header_x, y, Color.WHITE.value, 'Qualifying')

    def render_page(self, page: list):
        for item in page:
            self.render_row(item.position, item.driver.code, item.driver.constructor.colors)
        time.sleep(7.0)

        self.position_y = self.code_y = self.font.height  # Reset to top
        self.canvas.Clear()

    def render_row(self, position: int, code: str, colors: Color):
        parity = 'even' if position % 2 == 0 else 'odd'
        self.position_x = self.coords['grid'][parity]['position']['x']
        self.code_x = self.coords['grid'][parity]['code']['x']

        self.render_code(code, colors[0], colors[1])
        self.render_position(str(position))

        self.position_y += self.offset
        self.code_y += self.offset

    def render_position(self, position: str):
        # Background
        for x in range(self.position_x, self.code_x - 1):
            DrawLine(self.canvas, x, self.position_y - self.font.height, x, self.position_y, Color.WHITE.value)

        self.position_x += align_text(position,
                                      Position.CENTER,
                                      col_width=12,
                                      font_width=self.font.baseline - 1)

        # Position
        DrawText(self.canvas, self.font, self.position_x, self.position_y, Color.BLACK.value, position)

    def render_code(self, code: str, bg_color: Color, text_color: Color):
        # Background
        for x in range(self.code_x - 1, self.code_x + 20):
            DrawLine(self.canvas, x, self.code_y - self.font.height, x, self.code_y, bg_color)

        # Code
        DrawText(self.canvas, self.font, self.code_x, self.code_y, text_color, code)
