from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

import api_calls as api
from converters import stats_converter
from exceptions import UserNotFoundError
from settings import STATS_TYPES, TELEGRAM_TOKEN, logger

bot = Bot(token=str(TELEGRAM_TOKEN))
dp = Dispatcher(bot)


@dp.message_handler(commands=list(STATS_TYPES.keys()))
async def stats_add(message: types.Message):
    stat_type = message.get_command().replace('/', '')
    stat_type = STATS_TYPES.get(stat_type)
    data = message.get_args()
    telegram_id = message.from_user.id
    try:
        data = stats_converter(message.get_args(), stat_type)
        if stat_type == 'pressure':
            api.stats_post(telegram_id, 'lower', data[0])
            api.stats_post(telegram_id, 'upper', data[1])
            await bot.send_message(telegram_id, 'Данные успешно внесены')
        else:
            api.stats_post(telegram_id, stat_type, data[0])
            await bot.send_message(telegram_id, 'Данные успешно внесены')
    except UserNotFoundError:
        api.patient_post(telegram_id)
        logger.info(f'Новый пользователь telegram_id({telegram_id})')
        await stats_add(message)
    except Exception as error:
        info = f' (telegram_id({telegram_id}) stat({stat_type}) data({data}))'
        logger.error(str(error) + info)
        await bot.send_message(telegram_id, error.message)
