from copy import copy
from datetime import datetime, timedelta

from loguru import logger
from aiogram import types

from utils.schedule_parser import build_answer
from loader import last_request_time
from loader import schedule_parser
from loader import dp


@logger.catch
@dp.message_handler(commands='get_schedule')
async def _(message: types.Message):
    logger.info(f'{message.from_id} get schedule')

    if datetime.now() <= (last_request_time[0] + timedelta(minutes=3)):
        logger.info('timeout')

        #тут можно отправлять сообщение о таймауте

        return 
    last_request_time[0] = datetime.now()


    schedule = schedule_parser.get_schedule()
    message_answer = build_answer(schedule)
    await message.answer(message_answer)