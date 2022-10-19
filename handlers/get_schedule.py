from loguru import logger
from aiogram import types

from utils.schedule_parser import build_answer
from loader import schedule_parser
from loader import dp


@logger.catch
@dp.message_handler(commands='get_schedule')
async def _(message: types.Message):
    logger.info(f'{message.from_id} get schedule')

    schedule = schedule_parser.get_schedule()
    message_answer = build_answer(schedule)
    await message.answer(message_answer)