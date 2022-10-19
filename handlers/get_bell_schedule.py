from loguru import logger
from aiogram import types

from utils.bell_schedule import time_to_bell
from loader import dp


@logger.catch
@dp.message_handler(commands='get_bell_schedule')
async def _(message: types.Message):
    logger.info(f'{message.from_id} get bell schedule')

    ttb = time_to_bell()
    answer = f'До конца пары осталось: {ttb[1]}\n'
    answer += f'До начала пары осталось: {ttb[0]}'
    await message.answer(answer)