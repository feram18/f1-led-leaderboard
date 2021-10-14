import time
from rgbmatrix.graphics import DrawText, DrawLine
from renderer.renderer import Renderer
from data.color import Color
from data.gp_status import GrandPrixStatus
from utils import load_font, align_text_center, center_image


class NextGP(Renderer):
    """
    Render next grand prix's information

    Arguments:
        data (data.Data):                           Data instance

    Attributes:
        gp (data.GrandPrix):                        Next GP's data
        text_color (rgbmatrix.graphics.Font):       Text color
        font (rgbmatrix.graphics.Font):             Font instance
        coords (dict):                              Coordinates dictionary
        gp_name (str):                              Grand Prix's name
        gp_name (int):                              Grand Prix's name x-coord
        location (str):                             Grand Prix's location (city, country)
        date (str):                                 Grand Prix's date
        time (str):                                 Grand Prix's time
        status (str):                               Grand Prix's status
        logo (PIL.Image):                           Grand Prix's circuit logo image
        track (PIL.Image):                          Grand Prix's track layout image
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data

        self.gp = self.data.next_gp

        self.text_color = Color.WHITE.value

        self.font = load_font(self.data.config.layout['fonts']['tom_thumb'])

        self.coords = self.data.config.layout['coords']['next-gp']

        self.gp_name = self.gp.name
        self.gp_name_x = align_text_center(self.gp_name,
                                           canvas_width=self.canvas.width,
                                           font_width=self.font.baseline - 1)[0]
        self.location = f'{self.gp.circuit.locality} {self.gp.circuit.country}'
        self.date = self.gp.date
        self.time = self.gp.time
        self.status = self.gp.status
        self.logo = self.gp.circuit.logo
        self.track = self.gp.circuit.track

    def render(self):
        self.canvas.Clear()

        # Slide 1
        if self.logo is not None:
            self.render_logo()
        self.render_gp_name()
        time.sleep(7.5)

        self.canvas.Clear()

        # Slide 2
        self.render_track()
        self.render_date()
        if self.status == GrandPrixStatus.UPCOMING:
            self.render_time()
        else:
            self.render_status()
        time.sleep(7.5)

    def render_gp_name(self):
        y = self.coords['name']['y']
        for x in range(self.canvas.width):
            DrawLine(self.canvas, x, y - self.font.height, x, y, Color.RED.value)
        DrawText(self.canvas, self.font, self.gp_name_x, y, self.text_color, self.gp_name)

    def render_logo(self):
        x_offset = center_image(self.logo.size,
                                self.canvas.width)[0]
        y_offset = self.coords['logo']['y-offset']
        self.canvas.SetImage(self.logo, x_offset, y_offset)

    def render_date(self):
        x = align_text_center(self.date,
                              canvas_width=self.canvas.width,
                              font_width=self.font.baseline - 1)[0]
        y = self.coords['date']['y']
        DrawText(self.canvas, self.font, x, y, self.text_color, self.date)

    def render_time(self):
        x = align_text_center(self.time,
                              canvas_width=self.canvas.width,
                              font_width=self.font.baseline - 1)[0]
        y = self.coords['time']['y']
        DrawText(self.canvas, self.font, x, y, self.text_color, self.time)

    def render_track(self):
        x_offset = center_image(self.track.size,
                                self.canvas.width)[0]
        y_offset = self.coords['track']['y-offset']
        self.canvas.SetImage(self.track, x_offset, y_offset)

    def render_location(self):
        x = self.coords['location']['x']
        y = self.coords['location']['y']
        DrawText(self.canvas, self.font, x, y, self.text_color, self.location)

    def render_status(self):
        x = align_text_center(self.status.value,
                              canvas_width=self.canvas.width,
                              font_width=self.font.baseline - 1)[0]
        y = self.coords['status']['y']
        DrawText(self.canvas, self.font, x, y, self.text_color, self.status.value)
