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
        self.text_y = self.coords['position']['y']
        self.flag_y = self.coords['flag']['position']['y']
        self.driver_x = self.coords['driver']['x']

    def render(self):
        self.new_canvas(self.matrix.width, self.coords['row_height'] * (len(self.standings) + 1) + 1)
        self.render_header()
        for driver in self.standings:
            self.render_row(driver)
        self.scroll_up(self.canvas)
        self.text_y, self.flag_y = self.coords['position']['y'], self.coords['flag']['position']['y']  # Reset

    def render_header(self):
        x, y = align_text(self.font.getsize('Drivers'),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.TOP)
        y += self.coords['header']['offset']['y']

        self.draw.rectangle(((0, 0), (self.matrix.width, y + self.font_height - 1)), fill=Color.GRAY)
        self.draw.text((x, y), 'Drivers', fill=Color.WHITE, font=self.font)

    def render_row(self, driver: StandingsItem):
        bg_color, self.text_color = driver.item.constructor.colors

        self.render_background(bg_color)
        if self.coords['options']['flag']:
            self.render_flag(driver.item.flag)
        self.render_position(str(driver.position))
        if self.coords['options']['lastname']:
            self.render_driver(driver.item.lastname)
        else:
            self.render_driver(driver.item.code)
        self.render_points(f'{driver.points:g}')

        self.flag_y += self.offset
        self.text_y += self.offset

    def render_background(self, color: tuple):
        self.draw.rectangle(((self.driver_x - 1, self.text_y - 1),
                             (self.matrix.width, self.text_y + self.font_height - 1)),
                            fill=color)

    def render_flag(self, flag_path: str):
        flag = load_image(flag_path, tuple(self.coords['flag']['size']))
        self.canvas.paste(flag, (self.coords['flag']['position']['x'], self.flag_y))

    def render_position(self, position: str):
        self.draw.rectangle(((0, self.text_y - 1),
                             (self.driver_x - 3, self.text_y + self.font_height - 1)),
                            fill=Color.WHITE)

        # TODO: [HARD-CODED VALUE]
        x = align_text(self.font.getsize(position),
                       col_width=12,
                       x=Position.CENTER)[0]
        self.draw.text((x, self.text_y), position, fill=Color.BLACK, font=self.font)

    def render_driver(self, name: str):
        self.draw.text((self.driver_x, self.text_y), name, fill=self.text_color, font=self.font)

    def render_points(self, points: str):
        x = align_text(self.font.getsize(points),
                       col_width=self.matrix.width,
                       x=Position.RIGHT)[0]
        self.draw.text((x, self.text_y), points, fill=self.text_color, font=self.font)
