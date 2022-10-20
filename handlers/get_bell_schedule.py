from datetime import datetime, timedelta

from aiogram.utils.markdown import bold
from loguru import logger
from aiogram import types

from utils.bell_schedule import time_to_bell
from loader import last_request_time
from loader import dp


@logger.catch
@dp.message_handler(commands='get_bell_schedule')
async def _(message: types.Message):
    logger.info(f'{message.from_id} get bell schedule')

    if datetime.now() <= (last_request_time[1] + timedelta(minutes=3)):
        logger.info('timeout')

        #тут можно отправлять сообщение о таймауте

        return 
    last_request_time[1] = datetime.now()

    ttb = time_to_bell()
     
    answer = f'До конца пары осталось: {bold(ttb[1])}\n'
    answer += f'До начала пары осталось: {bold(ttb[0])}'
    
    if None in ttb:
        answer = f'Сегодня пары всё.\nЗавтра пара начнется в {bold(ttb[0].time())}'

    await message.answer(answer, parse_mode='markdown')