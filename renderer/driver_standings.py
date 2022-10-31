from PIL import ImageFont

from data.standings import StandingsItem
from renderer.renderer import Renderer
from utils import Color, align_text, Position, load_image


class DriverStandings(Renderer):
    """
    Render driver standings

    Arguments:
        data (api.Data):                        Data instance

    Attributes:
        standings (list[StandingsItem]):        Driver standings list
        text_color (tuple):                     Text color
        offset (int):                           Row y-coord offset
        coords (dict):                          Coordinates dictionary
        text_y (int):                           Driver's position, code, points y-coord
        flag_y (int):                            Driver's flag y-coord offset
        driver_x (int):                         Driver's code/lastname x-coord
    """

    def __init__(self, matrix, canvas, draw, layout, data):
        super().__init__(matrix, canvas, draw, layout)
        self.data = data
        self.standings = self.data.driver_standings.items
        self.text_color = Color.WHITE
        self.offset = self.font_height + 2
        self.coords = self.layout.coords['standings']['drivers']
        self.text_y = self.coords['place']['position']['y']
        self.flag_y = self.coords['flag']['position']['y']
        self.driver_x = self.coords['driver']['x']

    def render(self):
        self.new_canvas(self.matrix.width, self.coords['row_height'] * (len(self.standings) + 1) + 1)
        self.render_header()
        for driver in self.standings:
            self.render_row(driver)
        self.scroll_up(self.canvas)
        self.text_y, self.flag_y = self.coords['place']['position']['y'], self.coords['flag']['position']['y']  # Reset

    def render_header(self):
        x, y = align_text(self.layout.font_bold.getsize('Drivers'),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.TOP)
        y += self.coords['header']['offset']['y']

        self.draw.rectangle(((0, 0), (self.matrix.width, y + self.font_height - 1)), Color.GRAY)
        self.draw.text((x, y), 'Drivers', Color.WHITE, self.layout.font_bold)

    def render_row(self, driver: StandingsItem):
        # self.driver_x = self.coords['driver']['x']
        bg, self.text_color = driver.item.constructor.colors
        font = self.layout.font
        if driver.champion:
            bg, self.text_color = Color.GOLD, Color.WHITE
            font = self.layout.font_bold

        self.render_place(str(driver.position), driver.champion, font)
        # Note: Flag & Lastnames are exclusive. Cannot be combined.
        name = driver.item.code
        if self.coords['options']['flag']:
            self.render_flag(driver.item.flag)
            self.driver_x += tuple(self.coords['flag']['size'])[0] + 1
        elif self.coords['options']['lastname']:
            name = driver.item.lastname
        self.render_driver(name, bg, font)
        self.render_points(f'{driver.points:g}', font)

        self.flag_y += self.offset
        self.text_y += self.offset

    def render_place(self, position: str, champion: bool, font: ImageFont):
        bg, text = Color.WHITE, Color.BLACK
        if champion:
            bg, text = Color.GOLD, Color.WHITE
            position = 'C'
        self.draw.rectangle(((0, self.text_y - 1),
                             (self.coords['place']['width'] - 1, self.text_y + self.font_height - 1)),
                            bg)

        x = align_text(font.getsize(position),
                       col_width=self.coords['place']['width'] + 1,
                       x=Position.CENTER)[0]
        self.draw.text((x, self.text_y), position, text, font)

    def render_flag(self, path: str):
        flag = load_image(path, tuple(self.coords['flag']['size']))
        self.canvas.paste(flag, (self.coords['flag']['position']['x'], self.flag_y))

    def render_driver(self, name: str, color: tuple, font: ImageFont):
        self.draw.rectangle(((self.driver_x - 1, self.text_y - 1),
                             (self.matrix.width, self.text_y + self.font_height - 1)),
                            color)
        self.draw.text((self.driver_x, self.text_y), name, self.text_color, font)

    def render_points(self, points: str, font: ImageFont):
        x = align_text(font.getsize(points),
                       col_width=self.matrix.width,
                       x=Position.RIGHT)[0]
        self.draw.text((x, self.text_y), points, self.text_color, font)
