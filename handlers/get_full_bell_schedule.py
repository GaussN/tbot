from datetime import datetime, timedelta

from aiogram.utils.markdown import bold
from loguru import logger
from aiogram import types

from utils.check_timeout import check_timeout
from utils.bell_schedule import time_to_bell
from utils import delete_message
from config import TIMEOUT
from config import BELLS
from loader import messages
from loader import dp


@logger.catch
@dp.message_handler(commands='get_full_bell_schedule')
async def _(message: types.Message):
    logger.info(f'{message.from_id} get full bell schedule')

    await message.delete()

    if not check_timeout(index_in_lrtl=2, timeout=TIMEOUT):
        logger.info(f'timeout')
        return
    
    now = datetime.now()
    week_day = datetime.weekday(now)
    # week_day = 6 # deb

    message_answer = 'Сегодня звонков нет'

    if week_day != 6:
        message_answer = f'Расписание звонков на {now.strftime("%d/%m")}\n'

        i = 1
        for bells in BELLS[week_day]:
            message_answer += f'{i:02}) {bells[0]} - {bells[1]}\n'
            i += 1

    chat_id = message.chat.id
    msg = await message.answer(message_answer)

    await delete_message(chat_id, msg, 2)