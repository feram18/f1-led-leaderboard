import time
from rgbmatrix.graphics import DrawText
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
        name (str):                                 Grand Prix's name
        name_x (int):                               Grand Prix's name x-coord
        name_y (int):                               Grand Prix's name y-coord
        location (str):                             Grand Prix's location (city, country)
        location_x (int):                           Grand Prix's location x-coord
        location_y (int):                           Grand Prix's location y-coord
        date (str):                                 Grand Prix's date
        date_x (int):                               Grand Prix's date x-coord
        date_y (int):                               Grand Prix's date y-coord
        time (str):                                 Grand Prix's time
        time_x (int):                               Grand Prix's time x-coord
        time_y (int):                               Grand Prix's time y-coord
        status (str):                               Grand Prix's status
        status_x (int):                             Grand Prix's status x-coord
        status_y (int):                             Grand Prix's status y-coord
        logo (PIL.Image):                           Grand Prix's circuit logo image
        logo_x_offset (int):                        Grand Prix's circuit logo image x-coord offset
        logo_y_offset (int):                        Grand Prix's circuit logo image y-coord offset
        track (PIL.Image):                          Grand Prix's track layout image
        track_x_offset (int):                       Grand Prix's track layout image x-coord offset
        track_y_offset (int):                       Grand Prix's track layout image y-coord offset
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data

        self.gp = self.data.next_gp

        self.text_color = Color.WHITE.value

        self.font = load_font(self.data.config.layout['fonts']['tom_thumb'])

        self.coords = self.data.config.layout['coords']['next-gp']

        self.name = self.gp.name
        self.name_x = align_text_center(self.name,
                                        canvas_width=self.canvas.width,
                                        font_width=self.font.baseline - 1)[0]
        self.name_y = self.coords['name']['y']

        self.location = f'{self.gp.circuit.locality} {self.gp.circuit.country}'
        self.location_x = self.coords['location']['x']
        self.location_y = self.coords['location']['y']

        self.date = self.gp.date
        self.date_x = align_text_center(self.date,
                                        canvas_width=self.canvas.width,
                                        font_width=self.font.baseline - 1)[0]
        self.date_y = self.coords['date']['y']

        self.time = self.gp.time
        self.time_x = align_text_center(self.time,
                                        canvas_width=self.canvas.width,
                                        font_width=self.font.baseline - 1)[0]
        self.time_y = self.coords['time']['y']

        self.status = self.gp.status
        self.status_x = align_text_center(self.status.value,
                                          canvas_width=self.canvas.width,
                                          font_width=self.font.baseline - 1)[0]
        self.status_y = self.coords['status']['y']

        self.logo = self.gp.circuit.logo
        self.logo_x_offset = center_image(self.logo.size,
                                          self.canvas.width)[0]
        self.logo_y_offset = self.coords['logo']['y-offset']

        self.track = self.gp.circuit.track
        self.track_x_offset = center_image(self.track.size,
                                           self.canvas.width)[0]
        self.track_y_offset = self.coords['track']['y-offset']

    def render(self):
        self.canvas.Clear()

        # Slide 1
        if self.logo is not None:
            self.render_logo()
        self.render_name()
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

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_name(self):
        DrawText(self.canvas, self.font, self.name_x, self.name_y, self.text_color, self.name)

    def render_logo(self):
        self.canvas.SetImage(self.logo, self.logo_x_offset, self.logo_y_offset)

    def render_date(self):
        DrawText(self.canvas, self.font, self.date_x, self.date_y, self.text_color, self.date)

    def render_time(self):
        DrawText(self.canvas, self.font, self.time_x, self.time_y, self.text_color, self.time)

    def render_track(self):
        self.canvas.SetImage(self.track, self.track_x_offset, self.track_y_offset)

    def render_location(self):
        DrawText(self.canvas, self.font, self.location_x, self.location_y, self.text_color, self.location)

    def render_status(self):
        DrawText(self.canvas, self.font, self.status_x, self.status_y, self.text_color, self.status.value)
