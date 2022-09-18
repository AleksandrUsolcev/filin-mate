from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

import api_calls as api
from exceptions import UserNotFoundError
from settings import STATS_TYPES, TELEGRAM_TOKEN, logger

bot = Bot(token=str(TELEGRAM_TOKEN))
dp = Dispatcher(bot)


@dp.message_handler(commands=STATS_TYPES)
async def stats_add(message: types.Message):
    stat_type = message.get_command().replace('/', '')
    data = message.get_args()
    telegram_id = message.from_user.id
    try:
        api.stats_post(telegram_id, stat_type, data)
        await bot.send_message(telegram_id, 'Данные успешно внесены')
    except UserNotFoundError:
        api.patient_post(telegram_id)
        api.stats_post(telegram_id, stat_type, data)
        await bot.send_message(telegram_id, 'Данные успешно внесены')
    except Exception as error:
        info = f' (telegram_id({telegram_id}) stat({stat_type}) data({data}))'
        logger.info(str(error) + info)
        await bot.send_message(telegram_id, error.message)


# @dp.message_handler()
# async def echo_send(message: types.Message):
#     # await message.answer(message.text)
#     # await message.reply(message.text)
#     await bot.send_message(message.from_user.id, message.from_user.first_name)
