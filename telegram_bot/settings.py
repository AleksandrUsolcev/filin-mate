import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

FILIN_TOKEN = os.getenv('FILIN_TOKEN')

WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')

ENDPOINT = os.getenv('ENDPOINT', default='http://127.0.0.1:8000/api/1.0/')

HEADERS = {'Authorization': 'Bearer ' + FILIN_TOKEN}

DIFF_TIME = 2

WEATHER_PARSE = False

WEATHER_PARSE_INTERVAL = 30

LATITUDE = 55.777110

LONGITUDE = 37.508503

STATS_TYPES = {
    'pulse': ['Пульс', 20, 290, 'int'],
    'saturation': ['Сатурация', 20, 100, 'int'],
    'lower': ['Нижнее давление', 20, 320, 'int'],
    'upper': ['Верхнее давление', 20, 320, 'int'],
    'sugar': ['Сахар в крови', 0, 70, 'float'],
    'heat': ['Температура тела', 33, 43, 'float'],
    'sleep': ['Время сна', 0, 24, 'float'],
    'weight': ['Вес', 1, 450, 'float'],
    'height': ['Рост', 30, 260, 'float'],
    'health': ['Физическое состояние', 1, 10, 'int'],
    'mental': ['Психологическое состояние', 1, 10, 'int']
}

STATS_TYPES_FILL_ON_START = True

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
