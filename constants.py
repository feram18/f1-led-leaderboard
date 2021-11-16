"""Constants class"""

# Directories & Files
LAYOUT_FILE = 'config/layout/w{}h{}.json'
CONSTRUCTOR_LOGO_PATH = 'assets/img/constructors/{}.png'
COUNTRY_FLAG_PATH = 'assets/img/flags/{}.jpg'
NUMBER_IMAGE_PATH = 'assets/img/numbers/{}.png'
CIRCUIT_LOGO_PATH = 'assets/img/circuits/logos/{}.png'
TRACK_IMAGE_PATH = 'assets/img/circuits/tracks/{}.png'
F1_LOGO = 'assets/img/formula-1_logo.png'
ERROR_IMAGE = 'assets/img/error.png'

# ERGAST F1 API
BASE_URL = 'https://ergast.com/api/f1/current'
CONSTRUCTORS_URL = f'{BASE_URL}/constructors.json'
DRIVERS_URL = f'{BASE_URL}/drivers.json'
CONSTRUCTOR_STANDINGS_URL = f'{BASE_URL}/constructorStandings.json'
DRIVER_STANDINGS_URL = f'{BASE_URL}/driverStandings.json'
LAST_GP_RESULTS_URL = f'{BASE_URL}/last/results.json'
NEXT_GP_URL = f'{BASE_URL}/next.json'
QUALIFYING_RESULTS_URL = f'{BASE_URL}/next/qualifying.json'
SCHEDULE_URL = f'{BASE_URL}.json'

# Date/Time Formatting
DATE_FORMAT = '%a, %b %d'  # eg. Sun, Nov 14
TIME_FORMAT = '%H:%M'  # eg. 18:30

# Software
UPDATE_RATE = 60.0 * 60  # 1 hour
