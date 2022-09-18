import asyncio

from aiogram.utils import executor

from client_side import dp
from settings import logger
from weather_parser import parse_weather


async def on_startup(_):
    asyncio.create_task(parse_weather())


if __name__ == '__main__':
    logger.info('Старт работы бота')
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
