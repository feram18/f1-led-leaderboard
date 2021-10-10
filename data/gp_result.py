from dataclasses import dataclass
from typing import List
from data.driver import Driver
from data.grand_prix import GrandPrix
from data.finishing_status import FinishingStatus


@dataclass
class DriverResult:
    """Data class to represent a Grand Prix's driver's result"""
    driver: Driver
    position: str
    points: str
    laps: str
    status: FinishingStatus
    time: str = None
    fastest_lap: bool = False


@dataclass
class GPResult:
    """Data class to represent a Grand Prix's results"""
    gp: GrandPrix
    results: List[DriverResult]
