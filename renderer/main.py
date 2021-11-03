from data.update_status import UpdateStatus
from renderer.renderer import Renderer
from renderer.constructor_standings import ConstructorStandings
from renderer.driver_standings import DriverStandings
from renderer.last_gp import LastGP
from renderer.schedule import Schedule
from renderer.next_gp import NextGP
from renderer.qualifying import Qualifying
from renderer.error import Error
from renderer.test import Test


class MainRenderer(Renderer):
    """
    Handle the rendering of different boards
    (Constructor & Driver Standings, Schedule, Last & Next GP, & Qualifying)

    Arguments:
        data (api.Data):                Data instance

    Attributes:
        status (data.UpdateStatus):     Update status
    """

    def __init__(self, matrix, canvas, config, data):
        super().__init__(matrix, canvas, config)
        self.data = data
        self.status = self.data.status

    def render(self):
        while self.status is UpdateStatus.SUCCESS:
            try:
                self.render_constructor_standings()
                # self.render_driver_standings()
                # self.render_last_gp()
                # self.render_schedule()
                # self.render_next_gp()
                # self.render_qualifying()
                self.render_test()

                if self.data.should_update():
                    self.data.update()

            except KeyboardInterrupt as e:
                raise SystemExit(' Exiting...') from e

        self.render_error()

    def render_constructor_standings(self):
        ConstructorStandings(self.matrix, self.canvas, self.config, self.data).render()

    def render_driver_standings(self):
        DriverStandings(self.matrix, self.canvas, self.config, self.data).render()

    def render_last_gp(self):
        LastGP(self.matrix, self.canvas, self.config, self.data).render()

    def render_schedule(self):
        Schedule(self.matrix, self.canvas, self.config, self.data).render()

    def render_next_gp(self):
        NextGP(self.matrix, self.canvas, self.config, self.data).render()

    def render_qualifying(self):
        Qualifying(self.matrix, self.canvas, self.config, self.data).render()

    def render_error(self):
        Error(self.matrix, self.canvas, self.config, self.data).render()

    def render_test(self):
        Test(self.matrix, self.canvas, self.config).render()
