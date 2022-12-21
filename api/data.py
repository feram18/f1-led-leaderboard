import logging
import time
from dataclasses import dataclass, field
from typing import List, Optional

import requests

import constants
from data.circuit import Circuit
from data.constructor import Constructor
from data.driver import Driver
from data.finishing_status import FinishingStatus as Status
from data.gp_result import GPResult, DriverResult
from data.grand_prix import GrandPrix
from data.qualifying import Qualifying, QualifyingResultItem, Sprint
from data.session_status import SessionStatus
from data.standings import Standings, StandingsItem
from data.update_status import UpdateStatus
from utils import race_weekend, get_session_status, is_wcc_champion, is_wdc_champion


@dataclass
class Data:
    """
    Data class consisting of all the data to be displayed on matrix
    """
    constructors: dict = field(default_factory=dict)
    drivers: dict = field(default_factory=dict)
    constructor_standings: Standings = None
    driver_standings: Standings = None
    last_gp: GPResult = None
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
        self.fetch_qualifying()
        self.fetch_sprint()
        self.champions()

        self.last_updated = time.time()

    def update(self):
        self.constructor_standings = self.fetch_constructor_standings()
        self.driver_standings = self.fetch_driver_standings()
        self.last_gp = self.fetch_last_gp()
        self.schedule = self.fetch_schedule()
        self.next_gp = self.fetch_next_gp()
        self.fetch_qualifying()
        self.fetch_sprint()

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

    def fetch_qualifying(self):
        """
        Fetch next grand prix's qualifying data
        """
        if self.next_gp:
            status = get_session_status(self.next_gp.qualifying.dt)
            if status is SessionStatus.FINISHED:
                logging.debug('Fetching Qualifying Results')

                response = requests.get(constants.QUALIFYING_RESULTS_URL).json()

                if int(response['MRData']['total']) > 0:  # Qualifying results available
                    results = response['MRData']['RaceTable']['Races'][0]['QualifyingResults']
                    grid = [QualifyingResultItem(int(result['position']),
                                                 self.drivers.get(result['Driver']['driverId']),
                                                 result.get('Q1', None),
                                                 result.get('Q2', None),
                                                 result.get('Q3', None)) for result in results]
                    self.next_gp.qualifying.grid = grid

    def fetch_sprint(self):
        """
        Fetch next grand prix's sprint data
        """
        if self.next_gp.sprint:  # Sprint taking place
            status = get_session_status(self.next_gp.sprint.dt)
            if status is SessionStatus.FINISHED:
                logging.debug('Fetching Sprint Results')

                response = requests.get(constants.SPRINT_URL).json()

                if int(response['MRData']['total']) > 0:  # Sprint results available
                    results = response['MRData']['RaceTable']['Races'][0]['SprintResults']
                    grid = [QualifyingResultItem(int(result['position']),
                                                 self.drivers.get(result['Driver']['driverId'])) for result in results]
                    self.next_gp.sprint.grid = grid

    def fetch_schedule(self) -> List[GrandPrix]:
        """
        Fetch list of remaining grand prix in the current season
        :return: schedule: List of remaining GPs
        """
        logging.debug('Fetching Grand Prix Schedule')

        response = requests.get(constants.SCHEDULE_URL).json()
        schedule = response['MRData']['RaceTable']['Races']

        return [
            GrandPrix(int(gp['round']),
                      gp['raceName'],
                      Circuit(gp['Circuit']['circuitId'],
                              gp['Circuit']['circuitName'],
                              gp['Circuit']['Location']['locality'],
                              gp['Circuit']['Location']['country']),
                      gp['date'],
                      gp['time'],
                      Qualifying(gp['Qualifying']['date'],
                                 gp['Qualifying']['time']),
                      Sprint(gp['Sprint']['date'],
                             gp['Sprint']['time']) if gp.get('Sprint', None) else None)
            for gp in schedule[self.last_gp.gp.round:]]

    def champions(self):
        """
        Determine if there are champions for WDC & WCC
        """
        self.driver_standings.items[0].champion = is_wdc_champion(self.schedule, self.driver_standings)
        self.constructor_standings.items[0].champion = is_wcc_champion(self.schedule, self.constructor_standings)

    def should_update(self) -> bool:
        """
        Determines if data should be updated.
        i.e. If it is a race weekend and 15 minutes have passed since data was last fetched, an update is needed.
        :return: should_update: (bool)
        """
        if race_weekend(self.next_gp.dt):
            current_time = time.time()
            time_delta = current_time - self.last_updated
            return time_delta >= constants.UPDATE_RATE
        return False
