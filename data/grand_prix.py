from dataclasses import dataclass, field
from datetime import datetime

from constants import DATE_FORMAT, TIME_FORMAT
from data.circuit import Circuit
from data.session_status import SessionStatus
from data.qualifying import Qualifying, Sprint
from utils import convert_time, get_session_status


@dataclass
class GrandPrix:
    """Data class to represent a Grand Prix"""
    round: int
    name: str
    circuit: Circuit
    date: str
    time: str
    qualifying: Qualifying = None
    sprint: Sprint = None
    dt: datetime = field(init=False)
    status: SessionStatus = field(init=False)

    def __post_init__(self):
        self.name = self.name.replace('Grand Prix', 'GP')  # Abbreviate Grand Prix
        self.dt = convert_time(self.date, self.time)  # From UTC to local timezone
        self.date = self.dt.strftime(DATE_FORMAT)
        self.time = self.dt.strftime(TIME_FORMAT)
        self.status = get_session_status(self.dt)
