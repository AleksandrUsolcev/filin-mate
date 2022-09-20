import asyncio

import requests

from settings import (LATITUDE, LONGITUDE, WEATHER_PARSE_INTERVAL,
                      WEATHER_TOKEN, logger)
from api_calls import weather_post

PATH = (f'https://api.openweathermap.org/data/2.5/weather?lat='
        f'{LATITUDE}&lon={LONGITUDE}&appid={WEATHER_TOKEN}&units=metric')


async def parse_weather():
    logger.info('Запуск сбора погодных данных')
    while True:
        try:
            response = requests.get(PATH)
            if response.status_code != 200:
                message = 'Ошибка сбора данных, код запроса: '
                logger.critical(message + response.status_code)
            code = response.json().get('weather')[0]['id']
            temp = int(response.json().get('main')['temp'])
            pressure = int(response.json().get('main')['pressure'] * 0.75)
            humidity = int(response.json().get('main')['humidity'])
            weather_post(code, temp, pressure, humidity)
            await asyncio.sleep(60 * WEATHER_PARSE_INTERVAL)
        except Exception as error:
            message = 'Неизвестная ошибка: '
            logger.critical(message + error)
            await asyncio.sleep(60 * WEATHER_PARSE_INTERVAL)
