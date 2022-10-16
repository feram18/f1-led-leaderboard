from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from data.driver import Driver
from data.session_status import SessionStatus
from utils import convert_time, get_session_status


@dataclass
class QualifyingResultItem:
    position: int
    driver: Driver
    Q1: str = None
    Q2: str = None
    Q3: str = None


@dataclass
class Qualifying:
    date: str
    time: str
    dt: datetime = field(init=False)
    status: SessionStatus = SessionStatus.UPCOMING
    grid: List[QualifyingResultItem] = None

    def __post_init__(self):
        self.dt = convert_time(self.date, self.time)
        self.status = get_session_status(self.dt)


@dataclass
class Sprint(Qualifying):
    ...
