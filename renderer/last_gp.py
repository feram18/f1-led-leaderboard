import time
from rgbmatrix.graphics import DrawText, DrawLine
from renderer.renderer import Renderer
from data.color import Color
from data.driver import Driver
from data.finishing_status import FinishingStatus
from utils import load_font, align_text_center, align_text_right, center_image, split_into_pages, load_image


class LastGP(Renderer):
    """
    Render last grand prix's results

    Arguments:
        data (api.Data):                        Data instance

    Attributes:
        gp_result (data.GPResult):              Last GP's results data
        font (rgbmatrix.graphics.Font):         Font instance
        offset (int):                           Row y-coord offset
        coords (dict):                          Coordinates dictionary
        logo (PIL.Image):                       Grand Prix's circuit logo
        gp_name (str):                          Grand Prix's name
        gp_name_x (int):                        Grand Prix's name x-coord
        position_y (int):                       Driver's position y-coord
        code_x (int):                           Driver's code x-coord
        code_y (int):                           Driver's code y-coord
        time_y (int):                           Driver's time y-coord
        status_y (int):                         Driver's status y-coord
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data

        self.gp_result = self.data.last_gp

        self.font = load_font(self.data.config.layout['fonts']['tom_thumb'])

        self.offset = self.font.height + 2

        self.coords = self.data.config.layout['coords']['last-gp']

        self.logo = self.gp_result.gp.circuit.logo if not None else self.gp_result.gp.circuit.track
        self.logo = load_image(self.logo, (64, 24))

        self.gp_name = self.gp_result.gp.name
        self.gp_name_x = align_text_center(self.gp_name,
                                           canvas_width=self.canvas.width,
                                           font_width=self.font.baseline - 1)[0]
        self.position_y = self.coords['position']['y']
        self.code_x = self.coords['code']['x']
        self.code_y = self.coords['code']['y']
        self.time_y = self.coords['time']['y']
        self.status_y = self.coords['status']['y']

    def render(self):
        self.canvas.Clear()

        # Slide 1
        self.render_gp_name()
        if self.logo is not None:
            self.render_logo()
        time.sleep(7.0)

        self.canvas.Clear()

        # Slide 2
        self.render_podium(self.gp_result.driver_results[:3])  # Podium winners
        time.sleep(7.0)

        self.canvas.Clear()

        # Complete results
        pages = split_into_pages(self.gp_result.driver_results, 4)  # No.1-4, 5-9, 10-13, 14-17, 18-20
        for page in pages:
            self.render_page(page)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    # TODO: Name text can be too long to fit on canvas
    def render_gp_name(self):
        y = self.coords['name']['y']
        for x in range(self.canvas.width):
            DrawLine(self.canvas, x, y - self.font.height, x, y, Color.RED.value)
        DrawText(self.canvas, self.font, self.gp_name_x, y, Color.WHITE.value, self.gp_name)

    def render_logo(self):
        x_offset = center_image(self.logo.size,
                                self.canvas.width)[0]
        y_offset = self.coords['logo']['y-offset']
        self.canvas.SetImage(self.logo, x_offset, y_offset)

    def render_podium(self, winners: list):
        places = ['1st', '2nd', '3rd']
        for place, winner in zip(places, winners):
            self.render_podium_place(place, winner.driver)

    def render_podium_place(self, place: str, winner: Driver):
        top = self.coords['podium'][place]['limits']['top']
        right = self.coords['podium'][place]['limits']['right']
        bottom = self.coords['podium'][place]['limits']['bottom']
        left = self.coords['podium'][place]['limits']['left']
        flag_x_offset = self.coords['podium'][place]['flag']['x-offset']
        flag_y_offset = self.coords['podium'][place]['flag']['y-offset']
        winner_x = self.coords['podium'][place]['code']['x']
        winner_y = self.coords['podium'][place]['code']['y']
        label_x = self.coords['podium'][place]['label']['x']
        label_y = self.coords['podium'][place]['label']['y']

        # Podium
        for x in range(left, right):
            DrawLine(self.canvas, x, top, x, bottom, Color.WHITE.value)
        DrawText(self.canvas, self.font, label_x, label_y, Color.BLACK.value, place[0])

        # Winner
        for x in range(left + 1, right - 1):
            DrawLine(self.canvas, x, winner_y - self.font.height, x, winner_y, winner.constructor.colors[0])
        DrawText(self.canvas, self.font, winner_x, winner_y, winner.constructor.colors[1], winner.code)

        # Winner's flag
        self.canvas.SetImage(winner.flag, flag_x_offset, flag_y_offset)

    def render_page(self, page: list):
        for item in page:
            self.render_row(item.driver.constructor.colors,
                            str(item.position),
                            item.fastest_lap,
                            item.driver.code,
                            item.time,
                            item.status)
        time.sleep(5.0)

        self.position_y = self.code_y = self.time_y = self.status_y = self.font.height  # Reset to top
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_row(self,
                   colors: Color,
                   position: str,
                   fastest_lap: bool,
                   code: str,
                   race_time: str,
                   status: FinishingStatus):
        self.render_background(colors[0])
        self.render_position(position, fastest_lap)
        self.render_code(colors[1], code)
        if status == FinishingStatus.FINISHED:
            self.render_race_time(colors[1], race_time)
        else:
            self.render_status(colors[1], status.value)

        self.position_y += self.offset
        self.code_y += self.offset
        self.time_y += self.offset
        self.status_y += self.offset

    def render_background(self, bg_color: Color):
        for x in range(self.code_x - 1, self.canvas.width):
            DrawLine(self.canvas, x, self.code_y - self.font.height, x, self.code_y, bg_color)

    def render_position(self, position: str, fastest_lap: bool):
        if fastest_lap:
            bg_color = Color.PURPLE.value
            text_color = Color.WHITE.value
        else:
            bg_color = Color.WHITE.value
            text_color = Color.BLACK.value

        # Background
        for x in range(self.code_x - 2):
            DrawLine(self.canvas, x, self.position_y - self.font.height, x, self.position_y, bg_color)

        # Number
        x = align_text_center(position,
                              canvas_width=12,
                              font_width=self.font.baseline - 1)[0]
        DrawText(self.canvas, self.font, x, self.position_y, text_color, position)

    def render_code(self, text_color: Color, code: str):
        DrawText(self.canvas, self.font, self.code_x, self.code_y, text_color, code)

    # TODO: Time text for rance winner is too long
    def render_race_time(self, text_color: Color, race_time: str):
        x = align_text_right(race_time, self.canvas.width, self.font.baseline - 1)
        DrawText(self.canvas, self.font, x, self.time_y, text_color, race_time)

    # TODO: DNF-type status too long
    def render_status(self, text_color: Color, status: str):
        x = align_text_right(status, self.canvas.width, self.font.baseline - 1)
        DrawText(self.canvas, self.font, x, self.status_y, text_color, status)
