from loguru import logger
from aiogram import types

from utils.check_timeout import check_timeout
from utils.schedule_parser import build_answer
from utils import delete_message
from config import TIMEOUT
from loader import schedule_parser
from loader import messages
from loader import dp


@logger.catch
@dp.message_handler(commands='get_schedule')
async def _(message: types.Message):
    logger.info(f'{message.from_id} get schedule')

    await message.delete()

    if not check_timeout(index_in_lrtl=0, timeout=TIMEOUT):
        logger.info(f'timeout')
        return

    schedule = schedule_parser.get_schedule()
    message_answer = build_answer(schedule)
    chat_id = message.chat.id
    msg = await message.answer(message_answer)
    
    await delete_message(chat_id, msg, 0)
