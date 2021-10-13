from dataclasses import dataclass
from typing import List
from data.grand_prix import GrandPrix
from data.driver import Driver


@dataclass
class QualifyingResultItem:
    position: int
    driver: Driver
    Q1: str = None
    Q2: str = None
    Q3: str = None


@dataclass
class Qualifying:
    gp: GrandPrix
    grid: List[QualifyingResultItem]
