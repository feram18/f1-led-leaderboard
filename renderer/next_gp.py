import time

from constants import SLIDE_DELAY
from data.session_status import SessionStatus
from renderer.renderer import Renderer
from utils import Color, align_text, Position, align_image, load_image, get_text_size


class NextGP(Renderer):
    """
    Render next grand prix's information

    Arguments:
        data (api.Data):            Data instance

    Attributes:
        gp (data.GrandPrix):        Next GP's data
        coords (dict):              Coordinates dictionary
    """

    def __init__(self, matrix, canvas, draw, layout, data):
        super().__init__(matrix, canvas, draw, layout)
        self.data = data
        self.gp = self.data.next_gp
        self.coords = self.layout.coords['next-gp']

    def render(self):
        if self.gp:
            self.new_canvas(self.matrix.width, self.matrix.height)

            # GP name & logo
            self.render_logo()
            self.render_gp_name()
            self.matrix.SetImage(self.canvas)
            time.sleep(SLIDE_DELAY)

            self.clear()

            # Track layout & Date/Time/Status
            self.render_track()
            if self.gp.status == SessionStatus.UPCOMING:
                self.render_date()
                self.render_time()
            else:
                self.render_status()
            self.matrix.SetImage(self.canvas)
            time.sleep(SLIDE_DELAY)

    # TODO: Name text can be too long to fit on canvas
    def render_gp_name(self):
        x, y = align_text(get_text_size(self.draw, self.gp.name, self.layout.font_bold),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.TOP)
        self.draw.rectangle(((0, 0), (self.matrix.width, y + self.font_height)), Color.RED)
        self.draw.text((x, y + 1), self.gp.name, Color.WHITE, self.layout.font_bold)

    def render_logo(self):
        logo = load_image(self.gp.circuit.logo, tuple(self.coords['logo']['size']))
        if logo:
            x, y = align_image(logo,
                               self.matrix.width,
                               self.matrix.height - self.font_height - 1,
                               Position.CENTER,
                               Position.CENTER)
            y += self.font_height + 1
            self.canvas.paste(logo, (x, y))

    def render_date(self):
        x, y = align_text(get_text_size(self.draw, self.gp.date, self.draw.getfont()),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.BOTTOM)
        y -= self.font_height
        self.draw.text((x, y + 1), self.gp.date, Color.WHITE)

    def render_time(self):
        x, y = align_text(get_text_size(self.draw, self.gp.time, self.draw.getfont()),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.BOTTOM)
        self.draw.text((x, y + 1), self.gp.time, Color.WHITE)

    def render_track(self):
        track = load_image(self.gp.circuit.track, tuple(self.coords['track']['size']))
        if track:
            x, y = align_image(track,
                               self.matrix.width,
                               self.matrix.height,
                               Position.CENTER,
                               Position.TOP)
            self.canvas.paste(track, (x, y))

    def render_location(self):
        location = f'{self.gp.circuit.locality} {self.gp.circuit.country}'
        x, y = align_text(get_text_size(self.draw, location, self.draw.getfont()),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.BOTTOM)
        self.draw.text((x, y), location, Color.WHITE)

    def render_status(self):
        x, y = align_text(get_text_size(self.draw, self.gp.status.value, self.draw.getfont()),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.BOTTOM)
        self.draw.text((x, y), self.gp.status.value, Color.WHITE)
