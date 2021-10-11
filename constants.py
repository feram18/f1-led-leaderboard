"""Constants class"""

# Directories & Files
LAYOUT_FILE = 'config/layout/w{}h{}.json'
CONSTRUCTOR_LOGO_PATH = 'assets/img/constructors/{}.png'
COUNTRY_FLAG_PATH = 'assets/img/flags/{}.jpg'
CIRCUIT_LOGO_PATH = 'assets/img/circuits/logos/{}.jpg'
TRACK_IMAGE_PATH = 'assets/img/circuits/tracks/{}.jpg'

# ERGAST F1 API
BASE_URL = 'https://ergast.com/api/f1/current'
CONSTRUCTOR_STANDINGS_URL = f'{BASE_URL}/constructorStandings.json'
DRIVER_STANDINGS_URL = f'{BASE_URL}/driverStandings.json'
LAST_GP_RESULTS_URL = f'{BASE_URL}/last/results.json'
NEXT_GP_URL = f'{BASE_URL}/next.json'
QUALIFYING_RESULTS_URL = f'{BASE_URL}/next/qualifying.json'
SCHEDULE_URL = f'{BASE_URL}.json'

# Date/Time Formatting
DATETIME_FORMAT = '%Y-%m-%d %H:%M'

# Software
UPDATE_RATE = 15.0 * 60  # 15 minutes