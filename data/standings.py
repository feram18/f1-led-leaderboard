from dataclasses import dataclass
from data.constructor import Constructor
from data.driver import Driver


@dataclass
class ConstructorStandingsItem:
    constructor: Constructor
    position: int = 1
    points: float = 0


@dataclass
class DriverStandingsItem:
    driver: Driver
    position: int = 1
    points: float = 0
