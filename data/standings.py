from dataclasses import dataclass
from data.constructor import Constructor
from data.driver import Driver


@dataclass
class ConstructorStandingsItem:
    constructor: Constructor
    position: str = "1"
    points: str = "0"


@dataclass
class DriverStandingsItem:
    driver: Driver
    position: str = "1"
    points: str = "0"
