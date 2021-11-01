import time
import logging
import requests
import constants
from dataclasses import dataclass, field
from typing import List
from data.update_status import UpdateStatus
from data.standings import ConstructorStandingsItem, DriverStandingsItem
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
    constructor_standings: List[ConstructorStandingsItem] = field(default_factory=list)
    driver_standings: List[DriverStandingsItem] = field(default_factory=list)
    last_gp: GPResult = field(init=False)
    qualifying: Qualifying = None
    next_gp: GrandPrix = None
    schedule: List[GrandPrix] = field(default_factory=list)
    status: UpdateStatus = UpdateStatus.SUCCESS
    last_updated: float = None

    def __post_init__(self):
        self.initialize()

    def initialize(self):
        self.fetch_constructors()
        self.fetch_drivers()
        self.fetch_constructor_standings()
        self.fetch_driver_standings()
        self.fetch_last_gp()
        self.fetch_schedule()
        self.fetch_next_gp()
        self.fetch_qualifying_results()

        self.last_updated = time.time()

    def update(self):
        self.fetch_constructor_standings()
        self.fetch_driver_standings()
        self.fetch_last_gp()
        self.fetch_next_gp()
        self.fetch_qualifying_results()

        self.last_updated = time.time()

    def fetch_constructors(self):
        logging.debug('Fetching Constructors List')
        self.constructors = {}  # Initialize dict

        response = requests.get(constants.CONSTRUCTORS_URL).json()
        constructors = response['MRData']['ConstructorTable']['Constructors']

        for constructor in constructors:
            self.constructors[constructor['constructorId']] = Constructor(constructor['constructorId'],
                                                                          constructor['name'],
                                                                          constructor['nationality'])

    def fetch_drivers(self):
        logging.debug('Fetching Drivers List')
        self.drivers = {}  # Initialize dict

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

    def fetch_constructor_standings(self):
        logging.debug('Fetching Constructor Standings')
        if self.constructor_standings is not None:
            self.constructor_standings.clear()  # Clear any existing data
        self.constructor_standings = [] * 10  # Initialize list

        response = requests.get(constants.CONSTRUCTOR_STANDINGS_URL).json()
        constructors = response['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

        for constructor in constructors:
            self.constructor_standings.append(
                ConstructorStandingsItem(self.constructors.get(constructor['Constructor']['constructorId']),
                                         int(constructor['position']),
                                         float(constructor['points'])))

    def fetch_driver_standings(self):
        logging.debug('Fetching Driver Standings')
        if self.driver_standings is not None:
            self.driver_standings.clear()  # Clear any existing data
        self.driver_standings = []  # Initialize list

        response = requests.get(constants.DRIVER_STANDINGS_URL).json()
        drivers = response['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

        for driver in drivers:
            self.driver_standings.append(DriverStandingsItem(self.drivers.get(driver['Driver']['driverId']),
                                                             int(driver['position']),
                                                             float(driver['points'])))

    def fetch_last_gp(self):
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
        driver_results = []
        for result in results:
            driver_results.append(
                DriverResult(self.drivers.get(result['Driver']['driverId']),
                             int(result['position']),
                             float(result['points']),
                             int(result['laps']),
                             Status(result['status']),
                             result['Time']['time'] if Status(result['status']) == Status.FINISHED else None,
                             result['FastestLap']['rank'] == "1" if result.get('FastestLap') is not None else False))
        self.last_gp = GPResult(gp, driver_results)

    def fetch_next_gp(self):
        logging.debug("Fetching Next Grand Prix's data")
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
        logging.debug('Fetching Qualifying Results')
        response = requests.get(constants.QUALIFYING_RESULTS_URL).json()

        if int(response['MRData']['total']) > 0:  # Qualifying results available
            results = response['MRData']['RaceTable']['Races'][0]['QualifyingResults']
            grid = [] * 20  # Qualifying results

            for result in results:
                grid.append(QualifyingResultItem(int(result['position']),
                                                 self.drivers.get(result['Driver']['driverId']),
                                                 result.get('Q1', None),
                                                 result.get('Q2', None),
                                                 result.get('Q3', None)))
            self.qualifying = Qualifying(self.next_gp, grid)

    def fetch_schedule(self):
        logging.debug('Fetching Grand Prix Schedule')
        response = requests.get(constants.SCHEDULE_URL).json()
        schedule = response['MRData']['RaceTable']['Races']

        remaining_gps = []
        for gp in schedule[self.last_gp.gp.round:]:
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
        Determines if data should be updated.
        i.e. If 15 minutes have passed since data was last fetched, an update is needed.
        :return: should_update: (bool)
        """
        current_time = time.time()
        time_delta = current_time - self.last_updated
        return time_delta >= constants.UPDATE_RATE
