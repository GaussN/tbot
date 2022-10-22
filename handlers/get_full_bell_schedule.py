from datetime import datetime, timedelta

from aiogram.utils.markdown import bold
from loguru import logger
from aiogram import types

from utils.check_timeout import check_timeout
from utils.bell_schedule import time_to_bell
from config import BELLS
from loader import messages
from loader import dp


@logger.catch
@dp.message_handler(commands='get_full_bell_schedule')
async def _(message: types.Message):
    logger.info(f'{message.from_id} get full bell schedule')

    await message.delete()

    if not check_timeout(index_in_lrtl=2):
        logger.info(f'timeout')
        return
    
    now = datetime.now()
    week_day = datetime.weekday(now)
    # week_day = 6 # deb

    answer = 'Сегодня звонков нет'

    if week_day != 6:
        answer = f'Расписание звонков на {now.strftime("%d/%m")}\n'

        i = 1
        for bells in BELLS[week_day]:
            answer += f'{i:02}) {bells[0]} - {bells[1]}\n'
            i += 1


    msg = await message.answer(answer, parse_mode='markdown')
    if messages[2] is not None:
        await dp.bot.delete_message(message.chat.id, messages[2].message_id)
    messages[2] = msg