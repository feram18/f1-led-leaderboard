import time

from constants import SLIDE_DELAY
from data.driver import Driver
from data.finishing_status import FinishingStatus
from data.gp_result import DriverResult
from renderer.renderer import Renderer
from utils import align_text, Position, Color, load_image, align_image


class LastGP(Renderer):
    """
    Render last grand prix's results

    Arguments:
        data (api.Data):                Data instance

    Attributes:
        gp_result (data.GPResult):      Last GP's results data
        offset (int):                   Row y-coord offset
        coords (dict):                  Coordinates dictionary
        text_y (int):                   Driver's position, code, time, status y-coord
        code_x (int):                   Driver's code x-coord
    """

    def __init__(self, matrix, canvas, draw, layout, data):
        super().__init__(matrix, canvas, draw, layout)
        self.data = data
        self.gp_result = self.data.last_gp
        self.offset = self.font_height + 2
        self.coords = self.layout.coords['last-gp']
        self.text_y = self.coords['result']['position']['y']
        self.code_x = self.coords['code']['x']

    def render(self):
        if self.gp_result:
            self.new_canvas(self.matrix.width, self.coords['row_height'] * len(self.gp_result.driver_results))

            # GP Name & Track Logo/Layout
            self.render_gp_name()
            self.render_graphic()
            self.matrix.SetImage(self.canvas)
            time.sleep(SLIDE_DELAY)

            self.clear()

            # Podium
            self.render_podiums(self.gp_result.driver_results[:3])
            self.matrix.SetImage(self.canvas)
            time.sleep(SLIDE_DELAY)

            self.clear()

            # Complete results
            for result in self.gp_result.driver_results:
                self.render_row(result)
            self.scroll_up(self.canvas)

            self.text_y = self.coords['result']['position']['y']  # Reset

    # TODO: Name text can be too long to fit on canvas
    def render_gp_name(self):
        x, y = align_text(self.font.getsize(self.gp_result.gp.name),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.TOP)
        self.draw.rectangle(((0, 0), (self.matrix.width, y + self.font_height)), fill=Color.RED)
        self.draw.text((x, y + 1), self.gp_result.gp.name, fill=Color.WHITE, font=self.font)

    def render_graphic(self):
        graphic = load_image(self.gp_result.gp.circuit.logo, tuple(self.coords['graphic']['size']))
        if not graphic:  # Set graphic to track image
            graphic = load_image(self.gp_result.gp.circuit.track, tuple(self.coords['graphic']['size']))

        x, y = align_image(graphic,
                           self.matrix.width,
                           self.matrix.height,
                           Position.CENTER,
                           Position.BOTTOM)
        self.canvas.paste(graphic, (x, y))

    def render_podiums(self, winners: list):
        podiums = ['1st', '2nd', '3rd']
        for podium, winner in zip(podiums, winners):
            self.render_podium_place(podium, winner.driver)

    def render_podium_place(self, place: str, winner: Driver):
        # Podium
        top = self.coords['podium'][place]['limits']['top']
        right = self.coords['podium'][place]['limits']['right']
        bottom = self.coords['podium'][place]['limits']['bottom']
        left = self.coords['podium'][place]['limits']['left']
        label_x = self.coords['podium'][place]['label']['x']
        label_y = self.coords['podium'][place]['label']['y']

        self.draw.rectangle(((left, top), (right, bottom)), fill=Color.WHITE)
        self.draw.text((label_x, label_y), place[0], fill=Color.BLACK, font=self.font)

        # Driver
        driver_x = self.coords['podium'][place]['code']['x']
        driver_y = self.coords['podium'][place]['code']['y']

        self.draw.rectangle(((left + 1, driver_y - 1), (right - 1, driver_y + self.font_height - 1)),
                            fill=winner.constructor.colors[0])
        self.draw.text((driver_x, driver_y), winner.code, fill=winner.constructor.colors[1], font=self.font)

        # Driver's flag
        flag_x = self.coords['podium'][place]['flag']['position']['x']
        flag_y = self.coords['podium'][place]['flag']['position']['y']
        flag = load_image(winner.flag, tuple(self.coords['podium'][place]['flag']['size']))

        self.canvas.paste(flag, (flag_x, flag_y))

    def render_row(self, result: DriverResult):
        bg, text = result.driver.constructor.colors
        self.render_background(bg)
        self.render_position(str(result.position), result.fastest_lap)
        self.render_code(text, result.driver.code)
        if result.status == FinishingStatus.FINISHED:
            rt = result.time if self.coords['options']['full_string'] else result.time[:7]
            self.render_result(text, rt)
        else:
            self.render_result(text, str(result.status.value))

        self.text_y += self.offset

    def render_background(self, bg_color: tuple):
        self.draw.rectangle(((self.code_x - 1, self.text_y - 1),
                             (self.matrix.width, self.text_y + self.font_height - 1)),
                            fill=bg_color)

    def render_position(self, position: str, fastest_lap: bool):
        if fastest_lap:
            bg_color = Color.PURPLE
            text_color = Color.WHITE
        else:
            bg_color = Color.WHITE
            text_color = Color.BLACK

        self.draw.rectangle(((0, self.text_y - 1),
                             (self.code_x - 3, self.text_y + self.font_height - 1)),
                            fill=bg_color)

        x = align_text(self.font.getsize(position),
                       col_width=self.coords['result']['width'],
                       x=Position.CENTER)[0]
        self.draw.text((x, self.text_y), position, fill=text_color, font=self.font)

    def render_code(self, text_color: tuple, code: str):
        self.draw.text((self.code_x, self.text_y), code, fill=text_color, font=self.font)

    def render_result(self, text_color: tuple, text: str):
        x = align_text(self.font.getsize(text),
                       col_width=self.matrix.width,
                       x=Position.RIGHT)[0]
        self.draw.text((x, self.text_y), text, fill=text_color, font=self.font)
