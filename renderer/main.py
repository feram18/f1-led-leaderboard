from data.update_status import UpdateStatus
from renderer.constructor_standings import ConstructorStandings
from renderer.driver_standings import DriverStandings
from renderer.error import Error
from renderer.last_gp import LastGP
from renderer.next_gp import NextGP
from renderer.qualifying import Qualifying
from renderer.renderer import Renderer
from renderer.schedule import Schedule


class MainRenderer(Renderer):
    """
    Handle the rendering of different boards
    (Constructor & Driver Standings, Schedule, Last & Next GP, & Qualifying)

    Arguments:
        data (api.Data):                    Data instance

    Attributes:
        status (data.UpdateStatus):         Update status
    """

    def __init__(self, matrix, canvas, draw, layout, data):
        super().__init__(matrix, canvas, draw, layout)
        self.data = data
        self.status = self.data.status
        self.constructor_standings = ConstructorStandings(self.matrix, self.canvas, self.draw, self.layout, self.data)
        self.driver_standings = DriverStandings(self.matrix, self.canvas, self.draw, self.layout, self.data)
        self.last_gp = LastGP(self.matrix, self.canvas, self.draw, self.layout, self.data)
        self.schedule = Schedule(self.matrix, self.canvas, self.draw, self.layout, self.data)
        self.next_gp = NextGP(self.matrix, self.canvas, self.draw, self.layout, self.data)
        self.qualifying = Qualifying(self.matrix, self.canvas, self.draw, self.layout, self.data)
        self.error = Error(self.matrix, self.canvas, self.draw, self.layout, self.data)
        self.render()

    def render(self):
        while self.status is UpdateStatus.SUCCESS:
            try:
                self.constructor_standings.render()
                self.driver_standings.render()
                self.last_gp.render()
                self.schedule.render()
                self.next_gp.render()
                self.qualifying.render()
                if self.data.should_update():
                    self.data.update()
            except KeyboardInterrupt as e:
                raise SystemExit(' Exiting...') from e
        self.error.render()
