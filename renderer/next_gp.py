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
        logo (PIL.Image):                           Grand Prix's circuit logo image
        track (PIL.Image):                          Grand Prix's track layout image
    """

    def __init__(self, matrix, canvas, config, data):
        super().__init__(matrix, canvas, config)
        self.data = data
        self.gp = self.data.next_gp
        self.text_color = Color.WHITE.value
        self.coords = self.config.layout.coords['next-gp']
        self.logo = None
        self.track = None

    def render(self):
        if self.gp:
            self.canvas.Clear()

            self.logo = load_image(self.gp.circuit.logo, (64, 24))
            self.track = load_image(self.gp.circuit.track, (64, 20))

            # Slide 1
            self.render_logo()
            self.render_gp_name()
            time.sleep(7.5)

            self.canvas.Clear()

            # Slide 2
            self.render_track()
            self.render_date()
            if self.gp.status == GrandPrixStatus.UPCOMING:
                self.render_time()
            else:
                self.render_status()
            time.sleep(7.5)

            self.canvas = self.matrix.SwapOnVSync(self.canvas)

    # TODO: Name text can be too long to fit on canvas
    def render_gp_name(self):
        name_x = align_text(self.gp.name,
                            x=Position.CENTER,
                            col_width=self.canvas.width,
                            font_width=self.font.baseline - 1)
        y = self.coords['name']['y']

        for x in range(self.canvas.width):
            DrawLine(self.canvas, x, y - self.font.height, x, y, Color.RED.value)
        DrawText(self.canvas, self.font, name_x, y, self.text_color, self.gp.name)

    def render_logo(self):
        if self.logo:
            x_offset = align_image(self.logo,
                                   x=Position.CENTER,
                                   col_width=self.canvas.width)
            y_offset = self.coords['logo']['y-offset']
            self.canvas.SetImage(self.logo, x_offset, y_offset)

    def render_date(self):
        x = align_text(self.gp.date,
                       x=Position.CENTER,
                       col_width=self.canvas.width,
                       font_width=self.font.baseline - 1)
        y = self.coords['date']['y']
        DrawText(self.canvas, self.font, x, y, self.text_color, self.gp.date)

    def render_time(self):
        x = align_text(self.gp.time,
                       x=Position.CENTER,
                       col_width=self.canvas.width,
                       font_width=self.font.baseline - 1)
        y = self.coords['time']['y']
        DrawText(self.canvas, self.font, x, y, self.text_color, self.gp.time)

    def render_track(self):
        if self.track:
            x_offset = align_image(self.track,
                                   x=Position.CENTER,
                                   col_width=self.canvas.width)
            y_offset = self.coords['track']['y-offset']
            self.canvas.SetImage(self.track, x_offset, y_offset)

    def render_location(self):
        location = f'{self.gp.circuit.locality} {self.gp.circuit.country}'
        x = self.coords['location']['x']
        y = self.coords['location']['y']
        DrawText(self.canvas, self.font, x, y, self.text_color, location)

    def render_status(self):
        x = align_text(self.gp.status.value,
                       x=Position.CENTER,
                       col_width=self.canvas.width,
                       font_width=self.font.baseline - 1)
        y = self.coords['status']['y']
        DrawText(self.canvas, self.font, x, y, self.text_color, self.gp.status.value)
