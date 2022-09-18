import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

FILIN_TOKEN = os.getenv('FILIN_TOKEN')

WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')

LATITUDE = 55.777110

LONGITUDE = 37.508503

ENDPOINT = os.getenv('ENDPOINT', default='http://127.0.0.1:8000/api/1.0/')

HEADERS = {'Authorization': 'Bearer ' + FILIN_TOKEN}

DIFF_TIME = 2

STATS_TYPES = [
    'pulse',
    'saturation',
    'pressure',
    'sugar',
    'heat',
    'sleep',
    'weight',
    'height'
]

LOGS_NAME = 'history.log'

LOGS_MAX_BYTES = 10000000

LOGS_COUNT = 5

logger = logging.getLogger(LOGS_NAME)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOGS_NAME, maxBytes=LOGS_MAX_BYTES,
                              backupCount=LOGS_COUNT)

formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(message)s *** (%(name)s, '
    'файл: %(filename)s, функция: %(funcName)s, строка: %(lineno)s)'
)

handler.setFormatter(formatter)
logger.addHandler(handler)
