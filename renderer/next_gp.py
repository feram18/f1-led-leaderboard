import time
from rgbmatrix.graphics import DrawText, DrawLine
from renderer.renderer import Renderer
from data.gp_status import GrandPrixStatus
from utils import Color, align_text, Position, align_image, load_image


class NextGP(Renderer):
    """
    Render next grand prix's information

    Arguments:
        data (api.Data):                            Data instance

    Attributes:
        gp (data.GrandPrix):                        Next GP's data
        text_color (rgbmatrix.graphics.Color):      Text color
        coords (dict):                              Coordinates dictionary
        gp_name (str):                              Grand Prix's name
        gp_name_x (int):                            Grand Prix's name x-coord
        location (str):                             Grand Prix's location (city, country)
        date (str):                                 Grand Prix's date
        time (str):                                 Grand Prix's time
        status (str):                               Grand Prix's status
        logo (PIL.Image):                           Grand Prix's circuit logo image
        track (PIL.Image):                          Grand Prix's track layout image
    """

    def __init__(self, matrix, canvas, config, data):
        super().__init__(matrix, canvas, config)
        self.data = data

        self.gp = self.data.next_gp

        self.text_color = Color.WHITE.value

        self.coords = self.config.layout.coords['next-gp']

        self.gp_name = self.gp.name
        self.gp_name_x = align_text(self.gp_name,
                                    x=Position.CENTER,
                                    col_width=self.canvas.width,
                                    font_width=self.font.baseline - 1)
        self.location = f'{self.gp.circuit.locality} {self.gp.circuit.country}'
        self.date = self.gp.date
        self.time = self.gp.time
        self.status = self.gp.status
        self.logo = load_image(self.gp.circuit.logo, (64, 24))
        self.track = load_image(self.gp.circuit.track, (64, 20))

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

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    # TODO: Name text can be too long to fit on canvas
    def render_gp_name(self):
        y = self.coords['name']['y']
        for x in range(self.canvas.width):
            DrawLine(self.canvas, x, y - self.font.height, x, y, Color.RED.value)
        DrawText(self.canvas, self.font, self.gp_name_x, y, self.text_color, self.gp_name)

    def render_logo(self):
        x_offset = align_image(self.logo,
                               x=Position.CENTER,
                               col_width=self.canvas.width)
        y_offset = self.coords['logo']['y-offset']
        self.canvas.SetImage(self.logo, x_offset, y_offset)

    def render_date(self):
        x = align_text(self.date,
                       x=Position.CENTER,
                       col_width=self.canvas.width,
                       font_width=self.font.baseline - 1)
        y = self.coords['date']['y']
        DrawText(self.canvas, self.font, x, y, self.text_color, self.date)

    def render_time(self):
        x = align_text(self.time,
                       x=Position.CENTER,
                       col_width=self.canvas.width,
                       font_width=self.font.baseline - 1)
        y = self.coords['time']['y']
        DrawText(self.canvas, self.font, x, y, self.text_color, self.time)

    def render_track(self):
        x_offset = align_image(self.track,
                               x=Position.CENTER,
                               col_width=self.canvas.width)
        y_offset = self.coords['track']['y-offset']
        self.canvas.SetImage(self.track, x_offset, y_offset)

    def render_location(self):
        x = self.coords['location']['x']
        y = self.coords['location']['y']
        DrawText(self.canvas, self.font, x, y, self.text_color, self.location)

    def render_status(self):
        x = align_text(self.status.value,
                       x=Position.CENTER,
                       col_width=self.canvas.width,
                       font_width=self.font.baseline - 1)
        y = self.coords['status']['y']
        DrawText(self.canvas, self.font, x, y, self.text_color, self.status.value)
