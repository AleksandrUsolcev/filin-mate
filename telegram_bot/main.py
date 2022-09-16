import logging
from mailbox import Message
import os
from logging.handlers import RotatingFileHandler

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FILIN_TOKEN = os.getenv('FILIN_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')


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

bot = Bot(token=str(TELEGRAM_TOKEN))
dp = Dispatcher(bot)


@dp.message_handler()
async def echo_send(message: types.Message):
    # await message.answer(message.text)
    # await message.reply(message.text)
    await bot.send_message(message.from_user.id, message.from_user.first_name)

executor.start_polling(dp, skip_updates=True)
