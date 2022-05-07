import time
import logging
import requests
import constants
from dataclasses import dataclass, field
from typing import List, Optional
from data.update_status import UpdateStatus
from data.standings import StandingsItem, Standings
from data.constructor import Constructor
from data.driver import Driver
from data.gp_result import GPResult, DriverResult
from data.finishing_status import FinishingStatus as Status
from data.grand_prix import GrandPrix
from data.qualifying import Qualifying, QualifyingResultItem
from data.circuit import Circuit


@dataclass
class Data:
    """Data class consisting of all the data to be displayed on matrix"""
    constructors: dict = field(default_factory=dict)
    drivers: dict = field(default_factory=dict)
    constructor_standings: Standings = None
    driver_standings: Standings = None
    last_gp: GPResult = None
    qualifying: Qualifying = None
    next_gp: GrandPrix = None
    schedule: List[GrandPrix] = None
    status: UpdateStatus = UpdateStatus.SUCCESS
    last_updated: float = None

    def __post_init__(self):
        self.initialize()

    def initialize(self):
        self.fetch_constructors()
        self.fetch_drivers()
        self.constructor_standings = self.fetch_constructor_standings()
        self.driver_standings = self.fetch_driver_standings()
        self.last_gp = self.fetch_last_gp()
        self.schedule = self.fetch_schedule()
        self.next_gp = self.fetch_next_gp()
        self.qualifying = self.fetch_qualifying()

        self.last_updated = time.time()

    def update(self):
        self.constructor_standings = self.fetch_constructor_standings()
        self.driver_standings = self.fetch_driver_standings()
        self.last_gp = self.fetch_last_gp()
        self.schedule = self.fetch_schedule()
        self.next_gp = self.fetch_next_gp()
        self.qualifying = self.fetch_qualifying()

        self.last_updated = time.time()

    def fetch_constructors(self):
        logging.debug('Fetching Constructors List')

        response = requests.get(constants.CONSTRUCTORS_URL).json()
        constructors = response['MRData']['ConstructorTable']['Constructors']

        for constructor in constructors:
            self.constructors[constructor['constructorId']] = Constructor(constructor['constructorId'],
                                                                          constructor['name'],
                                                                          constructor['nationality'])

    def fetch_drivers(self):
        logging.debug('Fetching Drivers List')

        response = requests.get(constants.DRIVER_STANDINGS_URL).json()
        drivers = response['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

        for driver in drivers:
            self.drivers[driver['Driver']['driverId']] = Driver(driver['Driver']['driverId'],
                                                                driver['Driver']['givenName'],
                                                                driver['Driver']['familyName'],
                                                                driver['Driver']['code'],
                                                                int(driver['Driver']['permanentNumber']),
                                                                driver['Driver']['nationality'],
                                                                self.constructors.get(
                                                                    driver['Constructors'][0]['constructorId']))

    def fetch_constructor_standings(self) -> Standings:
        """
        Fetch current constructor standings
        :return: standings: Constructor standings
        """
        logging.debug('Fetching Constructor Standings')

        response = requests.get(constants.CONSTRUCTOR_STANDINGS_URL).json()
        constructors = response['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

        return Standings([StandingsItem(self.constructors.get(constructor['Constructor']['constructorId']),
                                        int(constructor['position']),
                                        float(constructor['points'])) for constructor in constructors])

    def fetch_driver_standings(self) -> Standings:
        """
        Fetch current driver standings
        :return: standings: Driver standings
        """
        logging.debug('Fetching Driver Standings')

        response = requests.get(constants.DRIVER_STANDINGS_URL).json()
        drivers = response['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

        return Standings([StandingsItem(self.drivers.get(driver['Driver']['driverId']),
                                        int(driver['position']),
                                        float(driver['points'])) for driver in drivers])

    def fetch_last_gp(self) -> GPResult:
        """
        Fetch last grand prix's race results
        :return: last_gp: Last GP's race results
        """
        logging.debug("Fetching Last Grand Prix's data")

        response = requests.get(constants.LAST_GP_RESULTS_URL).json()
        gp = response['MRData']['RaceTable']['Races'][0]
        gp = GrandPrix(int(gp['round']),
                       gp['raceName'],
                       Circuit(gp['Circuit']['circuitId'],
                               gp['Circuit']['circuitName'],
                               gp['Circuit']['Location']['locality'],
                               gp['Circuit']['Location']['country']),
                       gp['date'],
                       gp['time'])

        results = response['MRData']['RaceTable']['Races'][0]['Results']
        dr = [DriverResult(self.drivers.get(result['Driver']['driverId']),
                           int(result['position']),
                           float(result['points']),
                           int(result['laps']),
                           Status(result['status']),
                           result['Time']['time'] if Status(result['status']) == Status.FINISHED else None,
                           result['FastestLap']['rank'] == '1' if result.get('FastestLap') is not None else False)
              for result in results]
        return GPResult(gp, dr)

    def fetch_next_gp(self) -> Optional[GrandPrix]:
        """
        Fetch next grand prix's data
        :return: next_gp: Next GP's data
        """
        logging.debug("Fetching Next Grand Prix's data")

        if self.schedule:
            return self.schedule[0]

    def fetch_qualifying(self) -> Optional[Qualifying]:
        """
        Fetch next grand prix's qualifying data
        :return: qualifying: GP's qualifying data
        """
        logging.debug('Fetching Qualifying Results')

        response = requests.get(constants.QUALIFYING_RESULTS_URL).json()

        if int(response['MRData']['total']) > 0:  # Qualifying results available
            results = response['MRData']['RaceTable']['Races'][0]['QualifyingResults']
            grid = [QualifyingResultItem(int(result['position']),
                                         self.drivers.get(result['Driver']['driverId']),
                                         result.get('Q1', None),
                                         result.get('Q2', None),
                                         result.get('Q3', None)) for result in results]
            return Qualifying(self.next_gp, grid)

    def fetch_schedule(self) -> List[GrandPrix]:
        """
        Fetch list of remaining grand prix in the current season
        :return: schedule: List of remaining GPs
        """
        logging.debug('Fetching Grand Prix Schedule')

        response = requests.get(constants.SCHEDULE_URL).json()
        schedule = response['MRData']['RaceTable']['Races']

        return [GrandPrix(int(gp['round']),
                          gp['raceName'],
                          Circuit(gp['Circuit']['circuitId'],
                                  gp['Circuit']['circuitName'],
                                  gp['Circuit']['Location']['locality'],
                                  gp['Circuit']['Location']['country']),
                          gp['date'],
                          gp['time']) for gp in schedule[self.last_gp.gp.round:]]

    def should_update(self) -> bool:
        """
        Determines if data should be updated.
        i.e. If 15 minutes have passed since data was last fetched, an update is needed.
        :return: should_update: (bool)
        """
        current_time = time.time()
        time_delta = current_time - self.last_updated
        return time_delta >= constants.UPDATE_RATE
