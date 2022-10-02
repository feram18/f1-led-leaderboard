from dataclasses import dataclass, field
from typing import List

from data.constructor import Constructor
from data.driver import Driver


@dataclass
class StandingsItem:
    item: Driver or Constructor
    position: int = 1
    points: float = 0


@dataclass
class Standings:
    items: List[StandingsItem] = field(default_factory=list)
