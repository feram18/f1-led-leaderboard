from dataclasses import dataclass
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
    status: GrandPrixStatus = GrandPrixStatus.UPCOMING

    def __post_init__(self):
        self.name = self.name.replace('Grand Prix', 'GP')  # Abbreviate Grand Prix
        self.date, self.time = self.convert_time(self.date, self.time)  # From UTC to local timezone
        if self.in_progress(self.date, self.time):
            self.status = GrandPrixStatus.IN_PROGRESS

    @staticmethod
    def convert_time(date: str, time: str) -> list:
        """
        Convert from UTC to local timezone
        :param date: str
        :param time: str
        :return: datetime: list
        """
        dt = datetime.strptime(f'{date} {time}'.replace('Z', ''), '%Y-%m-%d %H:%M:%S')
        dt = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)  # Convert to local timezone
        return dt.strftime(DATETIME_FORMAT).split(' ')  # Split date and time

    @staticmethod
    def in_progress(date: str, time: str) -> bool:
        """
        Determine (roughly) if GP is currently in progress (assuming there are no delays)
        :return: in_progress: bool
        """
        now = datetime.now()
        start_time = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
        end_time = start_time + timedelta(hours=2)
        return start_time < now <= end_time
