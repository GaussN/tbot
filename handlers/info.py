from random import choice
import os

from loguru import logger
from aiogram import types

from loader import dp


@logger.catch
@dp.message_handler(commands='info')
async def _(message: types.Message):
    logger.info(f'INFO')

    await message.answer(f'''
<b>/get_schedule</b> - Получить расписание на неделю. Расписание всегда актуальное, бот парсит его перед ответом

<b>/get_bell_schedule</b> - Получить время до конца урока(пары) и время до начала следующего урока (пары)

<b>/get_full_bell_schedule</b> - Получить полное расписание звонков
    ''', parse_mode='html')