import asyncio

from aiogram.utils import executor

from api_calls import stats_type_post
from client_side import dp
from settings import (STATS_TYPES, STATS_TYPES_FILL_ON_START, WEATHER_PARSE,
                      logger)
from weather_parser import parse_weather


async def on_startup(_):
    logger.info('Старт работы бота')
    if STATS_TYPES_FILL_ON_START:
        for stat in STATS_TYPES.keys():
            param = STATS_TYPES.get(stat)
            response = stats_type_post(
                stat,
                param[0],
                param[1],
                param[2],
                param[3])
            if response.status_code == 201:
                logger.info(f'Добавлен тип данных: {stat}')
    if WEATHER_PARSE:
        asyncio.create_task(parse_weather())


async def on_shutdown(dispatcher: dp):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logger.info('Завершение работы бота')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True,
                           on_startup=on_startup, on_shutdown=on_shutdown)
