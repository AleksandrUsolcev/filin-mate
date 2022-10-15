import asyncio

from aiogram.utils import executor

from client_side import dp
from settings import WEATHER_PARSE, logger
from weather_parser import parse_weather


async def on_startup(_):
    logger.info('Старт работы бота')
    if WEATHER_PARSE:
        asyncio.create_task(parse_weather())


async def on_shutdown(dispatcher: dp):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logger.info('Завершение работы бота')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True,
                           on_startup=on_startup, on_shutdown=on_shutdown)
