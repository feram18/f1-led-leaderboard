from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from data.circuit import Circuit
from data.gp_status import GrandPrixStatus
from constants import DATETIME_FORMAT


@dataclass
class GrandPrix:
    """Data class to represent a Grand Prix"""
    round: int
    name: str
    circuit: Circuit
    date: str
    time: str
    status: GrandPrixStatus = field(init=False)

    def __post_init__(self):
        self.name = self.name.replace('Grand Prix', 'GP')  # Abbreviate Grand Prix
        self.date, self.time = self.convert_time(self.date, self.time)  # From UTC to local timezone
        self.status = self.get_status(self.date, self.time)

    @staticmethod
    def convert_time(date: str, time: str) -> list:
        """
        Convert from UTC to local timezone
        :param date: GP's date (UTC)
        :param time: GP's time (UTC)
        :return: date_time: GP's date & time (user's local timezone)
        """
        dt = datetime.strptime(f'{date} {time}'.replace('Z', ''), '%Y-%m-%d %H:%M:%S')
        dt = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)  # Convert to local timezone
        return dt.strftime(DATETIME_FORMAT).split(' ')  # Split date and time

    @staticmethod
    def get_status(date: str, time: str) -> GrandPrixStatus:
        """
        Roughly determine the grand prix's current status. Does not (currently) account for delays.
        :param date: GP's date
        :param time: GP's time
        :return: status: GP's status
        """
        now = datetime.now()
        start_time = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
        end_time = start_time + timedelta(hours=2)
        if now < start_time:
            return GrandPrixStatus.UPCOMING
        elif start_time < now <= end_time:
            return GrandPrixStatus.IN_PROGRESS
        elif now >= end_time:
            return GrandPrixStatus.FINISHED
