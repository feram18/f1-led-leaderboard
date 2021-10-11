from data.update_status import UpdateStatus
from renderer.renderer import Renderer
from renderer.constructor_standings import ConstructorStandings
from renderer.driver_standings import DriverStandings
from renderer.next_gp import NextGP
from renderer.error import Error


class MainRenderer(Renderer):
    """
    Handle the rendering of different boards

    Arguments:
        data (data.Data):               Data instance

    Attributes:
        status (data.UpdateStatus):     Update status
    """

    def __init__(self, matrix, canvas, data):
        super().__init__(matrix, canvas)
        self.data = data
        self.status = self.data.status

    def render(self):
        while self.status is UpdateStatus.SUCCESS:
            try:
                self.render_constructor_standings()
                self.render_driver_standings()
                self.render_next_gp()

                if self.data.should_update():
                    self.data.update()

            except KeyboardInterrupt as e:
                raise SystemExit(' Exiting...') from e

        self.render_error()

    def render_constructor_standings(self):
        ConstructorStandings(self.matrix, self.canvas, self.data).render()

    def render_driver_standings(self):
        DriverStandings(self.matrix, self.canvas, self.data).render()

    def render_next_gp(self):
        NextGP(self.matrix, self.canvas, self.data).render()

    def render_error(self):
        Error(self.matrix, self.canvas, self.data).render()
