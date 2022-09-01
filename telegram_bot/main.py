import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FILIN_TOKEN = os.getenv('FILIN_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(f'logs/{__file__}.log', maxBytes=50000000,
                              backupCount=10)

formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(message)s *** (%(name)s, '
    'имя файла: %(filename)s, функция: %(funcName)s, строка: %(lineno)s)'
)

handler.setFormatter(formatter)
logger.addHandler(handler)
