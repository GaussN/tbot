from loguru import logger
from aiogram import types

from utils.check_timeout import check_timeout
from utils.schedule_parser import build_answer
from loader import schedule_parser
from loader import messages
from loader import dp


@logger.catch
@dp.message_handler(commands='get_schedule')
async def _(message: types.Message):
    logger.info(f'{message.from_id} get schedule')

    await message.delete()

    if not check_timeout(index_in_lrtl=0, timeout=1):
        logger.info(f'timeout')
        return

    schedule = schedule_parser.get_schedule()
    message_answer = build_answer(schedule)
    msg = await message.answer(message_answer)
    if messages[0] is not None:
        await dp.bot.delete_message(message.chat.id, messages[0].message_id)
    messages[0] = msg