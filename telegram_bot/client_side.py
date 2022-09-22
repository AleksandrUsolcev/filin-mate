import time
import os
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

import api_calls as api
from converters import stats_converter
from exceptions import UserNotFoundError
from messages import HELP_MESSAGES, START_MESSAGES, STATS_MESSAGES
from plots import save_img
from settings import STATS_TYPES, TELEGRAM_TOKEN, logger
from states import StatStates

bot = Bot(token=str(TELEGRAM_TOKEN))
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    user = message.from_user.id
    await state.reset_state()
    await bot.send_sticker(user, START_MESSAGES.get('sticker_id'))
    await bot.send_message(user, START_MESSAGES.get('message'))


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    user = message.from_user.id
    await state.reset_state()
    await bot.send_message(user, HELP_MESSAGES.get('message'),
                           parse_mode='html')


@dp.message_handler(commands=list(STATS_TYPES.keys()))
async def stats_add(message: types.Message):
    stat_type = message.get_command().replace('/', '')
    data = message.get_args()
    telegram_id = message.from_user.id
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    if data.strip():
        try:
            data = stats_converter(message.get_args(), stat_type)
            if stat_type == 'pressure':
                api.stats_post(telegram_id, 'lower', data[0])
                api.stats_post(telegram_id, 'upper', data[1])
            else:
                api.stats_post(telegram_id, stat_type, data[0])
            await bot.send_message(telegram_id, 'Данные успешно внесены')
        except UserNotFoundError:
            api.patient_post(telegram_id)
            logger.info(f'Новый пользователь telegram_id({telegram_id})')
            await stats_add(message)
        except Exception as error:
            info = (f' (telegram_id({telegram_id}) '
                    f'stat({stat_type}) data({data}))')
            logger.error(str(error) + info)
            error = error.message.format(stat=message.get_command())
            await bot.send_message(telegram_id, error)
    else:
        await state.set_state(stat_type)
        await message.reply(STATS_MESSAGES[stat_type], reply=False)


@dp.message_handler(state=StatStates.all())
async def state_stats_add(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    telegram_id = message.from_user.id
    data = message.text
    if data.strip():
        try:
            data = stats_converter(message.text, await state.get_state())
            if await state.get_state() == 'pressure':
                api.stats_post(telegram_id, 'lower', data[0])
                api.stats_post(telegram_id, 'upper', data[1])
            else:
                api.stats_post(telegram_id, await state.get_state(), data[0])
            await bot.send_message(telegram_id, 'Данные успешно внесены')
        except UserNotFoundError:
            api.patient_post(telegram_id)
            logger.info(f'Новый пользователь telegram_id({telegram_id})')
            await state_stats_add(message)
        except Exception as error:
            info = (f' (telegram_id({telegram_id}) '
                    f'stat({await state.get_state()}) data({data}))')
            logger.error(str(error) + info)
            error = error.message.format(stat=('/' + await state.get_state()))
            await bot.send_message(telegram_id, error)
    await state.reset_state()


@dp.message_handler(commands=['plot'])
async def send_plot(message: types.Message):
    telegram_id = message.from_user.id
    img = save_img(telegram_id, time.time())
    await bot.send_photo(telegram_id, photo=open(img, 'rb'))
    os.remove(img)
