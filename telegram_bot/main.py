from aiogram.utils import executor

from client_side import dp
from settings import logger

if __name__ == '__main__':
    logger.info('Старт работы бота')
    executor.start_polling(dp, skip_updates=True)
