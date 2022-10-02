from dataclasses import dataclass
from typing import List

from data.driver import Driver
from data.grand_prix import GrandPrix


@dataclass
class QualifyingResultItem:
    position: int
    driver: Driver
    Q1: str
    Q2: str
    Q3: str


@dataclass
class Qualifying:
    gp: GrandPrix
    grid: List[QualifyingResultItem]
