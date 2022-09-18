import os

from dotenv import load_dotenv

import exceptions as exc

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FILIN_TOKEN = os.getenv('FILIN_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
ENDPOINT = os.getenv('ENDPOINT', default='http://127.0.0.1:8000/api/1.0/')

HEADERS = {'Authorization': 'Bearer ' + FILIN_TOKEN}

DIFF_TIME = 0

STATS_TYPES = ['pulse', 'saturation', 'pressure',
               'sugar', 'heat', 'sleep', 'weight', 'height']

ERRORS = {
    'user_not_found': exc.UserNotFoundError,
    'stat_type_not_found': exc.StatTypeNotFoundError,
    'stat_incorrect_value': exc.IncorrectValueError
}


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = RotatingFileHandler(f'logs/{__file__}.log', maxBytes=50000000,
#                               backupCount=10)

# formatter = logging.Formatter(
#     '%(asctime)s, %(levelname)s, %(message)s *** (%(name)s, '
#     'имя файла: %(filename)s, функция: %(funcName)s, строка: %(lineno)s)'
# )

# handler.setFormatter(formatter)
# logger.addHandler(handler)
