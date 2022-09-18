from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

import api_calls as api
import exceptions as exc
from settings import STATS_TYPES, TELEGRAM_TOKEN

bot = Bot(token=str(TELEGRAM_TOKEN))
dp = Dispatcher(bot)


@dp.message_handler(commands=STATS_TYPES)
async def save_pulse(message: types.Message):
    stat_type = message.get_command().replace('/', '')
    data = message.get_args()
    try:
        api.stats_post(message.from_user.id, stat_type, data)
        await bot.send_message(message.from_user.id, 'Данные успешно внесены')
    except exc.UserNotFoundError:
        api.patient_post(message.from_user.id)
        api.stats_post(message.from_user.id, 'pulse', data)
        await bot.send_message(message.from_user.id, 'Данные успешно внесены')
    except exc.TimeDifferenceError:
        await bot.send_message(message.from_user.id, f'Нельзя вносить данные чаще чем раз в {api.DIFF_TIME} минут')
    except exc.IncorrectValueError:
        await bot.send_message(message.from_user.id, 'Некорректные данные')
    except exc.StatTypeNotFoundError:
        await bot.send_message(message.from_user.id, 'В базе отсутствует приведенный тип показателей')

# @dp.message_handler()
# async def echo_send(message: types.Message):
#     # await message.answer(message.text)
#     # await message.reply(message.text)
#     await bot.send_message(message.from_user.id, message.from_user.first_name)
