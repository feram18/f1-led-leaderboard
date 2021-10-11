import time
import requests
import constants
from dataclasses import dataclass
from typing import List
from config.matrix_config import MatrixConfig
from data.update_status import UpdateStatus
from data.standings import ConstructorStandingsItem, DriverStandingsItem
from data.constructor import Constructor
from data.driver import Driver
from data.gp_result import GPResult, DriverResult
from data.gp_status import GrandPrixStatus
from data.finishing_status import FinishingStatus
from data.grand_prix import GrandPrix
from data.qualifying import Qualifying, QualifyingResultItem
from data.circuit import Circuit


@dataclass
class Data:
    """Data class consisting of all the data to be displayed on matrix"""
    config: MatrixConfig
    status: UpdateStatus = UpdateStatus.SUCCESS
    last_updated: float = None
    # constructors: List[Constructor] = None
    # drivers: List[Driver] = None
    constructor_standings: List[ConstructorStandingsItem] = None
    driver_standings: List[DriverStandingsItem] = None
    last_gp: GPResult = None
    qualifying: Qualifying = None
    next_gp: GrandPrix = None
    schedule: List[GrandPrix] = None

    def __post_init__(self):
        self.update()

    def update(self):
        self.fetch_constructor_standings()
        self.fetch_driver_standings()
        self.fetch_last_gp()
        self.fetch_next_gp()
        self.fetch_schedule()
        self.fetch_qualifying_results()

        self.last_updated = time.time()

    def fetch_constructor_standings(self):
        if self.constructor_standings is not None:
            self.constructor_standings.clear()  # Clear any existing data
        self.constructor_standings = [] * 10  # Initialize list

        response = requests.get(constants.CONSTRUCTOR_STANDINGS_URL).json()
        constructors = response['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

        for constructor in constructors:
            self.constructor_standings.append(
                ConstructorStandingsItem(Constructor(constructor['Constructor']['constructorId'],
                                                     constructor['Constructor']['name'],
                                                     constructor['Constructor']['nationality']),
                                         constructor['position'],
                                         constructor['points']))

    def fetch_driver_standings(self):
        if self.driver_standings is not None:
            self.driver_standings.clear()  # Clear any existing data
        self.driver_standings = [] * 20  # Initialize list

        response = requests.get(constants.DRIVER_STANDINGS_URL).json()
        drivers = response['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

        for driver in drivers:
            self.driver_standings.append(
                DriverStandingsItem(Driver(driver['Driver']['givenName'],
                                           driver['Driver']['familyName'],
                                           driver['Driver']['code'],
                                           driver['Driver']['permanentNumber'],
                                           driver['Driver']['nationality'],
                                           Constructor(driver['Constructors'][0]['constructorId'],
                                                       driver['Constructors'][0]['name'],
                                                       driver['Constructors'][0]['nationality'])),
                                    driver['position'],
                                    driver['points']))

    def fetch_last_gp(self):
        response = requests.get(constants.LAST_GP_RESULTS_URL).json()
        gp = response['MRData']['RaceTable']['Races'][0]

        gp = GrandPrix(int(gp['round']),
                       gp['raceName'],
                       Circuit(gp['Circuit']['circuitId'],
                               gp['Circuit']['circuitName'],
                               gp['Circuit']['Location']['locality'],
                               gp['Circuit']['Location']['country']),
                       gp['date'],
                       gp['time'],
                       GrandPrixStatus.FINISHED)

        results = response['MRData']['RaceTable']['Races'][0]['Results']
        for result in results:
            results = DriverResult(Driver(result['Driver']['givenName'],
                                          result['Driver']['familyName'],
                                          result['Driver']['code'],
                                          result['Driver']['permanentNumber'],
                                          result['Driver']['nationality'],
                                          Constructor(result['Constructor']['constructorId'],
                                                      result['Constructor']['name'],
                                                      result['Constructor']['nationality'])),
                                   result['position'],
                                   result['points'],
                                   result['laps'],
                                   FinishingStatus(result['status']).name,
                                   result['Time']['time']
                                   if FinishingStatus(result['status']).name == FinishingStatus.FINISHED else None,
                                   result['FastestLap']['rank'] == "1")
        self.last_gp = GPResult(gp, results)

    def fetch_next_gp(self):
        response = requests.get(constants.NEXT_GP_URL).json()
        gp = response['MRData']['RaceTable']['Races'][0]

        self.next_gp = GrandPrix(int(gp['round']),
                                 gp['raceName'],
                                 Circuit(gp['Circuit']['circuitId'],
                                         gp['Circuit']['circuitName'],
                                         gp['Circuit']['Location']['locality'],
                                         gp['Circuit']['Location']['country']),
                                 gp['date'],
                                 gp['time'])

    def fetch_qualifying_results(self):
        response = requests.get(constants.QUALIFYING_RESULTS_URL).json()

        if int(response['MRData']['total']) > 0:  # Qualifying results available
            results = response['MRData']['RaceTable']['Races'][0]['QualifyingResults']
            grid = [] * 20  # Qualifying results

            for result in results:
                grid.append(QualifyingResultItem(result['position'],
                                                 Driver(result['Driver']['givenName'],
                                                        result['Driver']['familyName'],
                                                        result['Driver']['code'],
                                                        result['Driver']['permanentNumber'],
                                                        result['Driver']['nationality'],
                                                        Constructor(result['Constructor']['constructorId'],
                                                                    result['Constructor']['name'],
                                                                    result['Constructor']['nationality'])),
                                                 result['Q1']))
            self.qualifying = Qualifying(self.next_gp, grid)

    def fetch_schedule(self):
        response = requests.get(constants.SCHEDULE_URL).json()
        schedule = response['MRData']['RaceTable']['Races']

        remaining_gps = []
        next_gp_id = self.next_gp.round
        for gp in schedule[next_gp_id:]:
            remaining_gps.append(GrandPrix(int(gp['round']),
                                           gp['raceName'],
                                           Circuit(gp['Circuit']['circuitId'],
                                                   gp['Circuit']['circuitName'],
                                                   gp['Circuit']['Location']['locality'],
                                                   gp['Circuit']['Location']['country']),
                                           gp['date'],
                                           gp['time']))
        self.schedule = remaining_gps

    def should_update(self) -> bool:
        """
        Returns Boolean value to determine if data should be updated.
        i.e. If 10 minutes have passed since data was last fetched, an update is needed.
        :return: should_update: (bool)
        """
        current_time = time.time()
        time_delta = current_time - self.last_updated
        return time_delta >= constants.UPDATE_RATE
