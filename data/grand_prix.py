from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from data.circuit import Circuit
from data.gp_status import GrandPrixStatus
from constants import DATE_FORMAT, TIME_FORMAT


@dataclass
class GrandPrix:
    """Data class to represent a Grand Prix"""
    round: int
    name: str
    circuit: Circuit
    date: str
    time: str
    dt: datetime = field(init=False)
    status: GrandPrixStatus = field(init=False)

    def __post_init__(self):
        self.name = self.name.replace('Grand Prix', 'GP')  # Abbreviate Grand Prix
        self.dt = self.convert_time(self.date, self.time)  # From UTC to local timezone
        self.date = self.dt.strftime(DATE_FORMAT)
        self.time = self.dt.strftime(TIME_FORMAT)
        self.status = self.get_status(self.dt)

    @staticmethod
    def convert_time(date: str, time: str) -> datetime:
        """
        Convert from UTC to local timezone
        :param date: GP's date (UTC)
        :param time: GP's time (UTC)
        :return: dt: GP's date & time (user's local timezone)
        """
        dt = datetime.strptime(f'{date} {time}'.replace('Z', ''), '%Y-%m-%d %H:%M:%S')
        dt = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)  # Convert to local timezone
        return dt

    @staticmethod
    def get_status(start_time: datetime) -> GrandPrixStatus:
        """
        Roughly determine the grand prix's current status. Does not account for delays.
        :param start_time: GP's start date & time
        :return: status: GP's status
        """
        now = datetime.now().astimezone(tz=None)
        end_time = start_time + timedelta(hours=2)
        if now < start_time:
            return GrandPrixStatus.UPCOMING
        elif start_time < now <= end_time:
            return GrandPrixStatus.IN_PROGRESS
        elif now >= end_time:
            return GrandPrixStatus.FINISHED
