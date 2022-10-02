from dataclasses import dataclass
from typing import List

from data.driver import Driver
from data.finishing_status import FinishingStatus
from data.grand_prix import GrandPrix


@dataclass
class DriverResult:
    """Data class to represent a Grand Prix's driver's result"""
    driver: Driver
    position: int
    points: float
    laps: int
    status: FinishingStatus
    time: str
    fastest_lap: bool


@dataclass
class GPResult:
    """Data class to represent a Grand Prix's results"""
    gp: GrandPrix
    driver_results: List[DriverResult]
