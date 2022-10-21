from datetime import datetime, timedelta

from aiogram.utils.markdown import bold
from loguru import logger
from aiogram import types

from utils.check_timeout import check_timeout
from utils.bell_schedule import time_to_bell
from loader import messages
from loader import dp


@logger.catch
@dp.message_handler(commands='get_bell_schedule')
async def _(message: types.Message):
    logger.info(f'{message.from_id} get bell schedule')

    await message.delete()

    if not check_timeout(index_in_lrtl=1):
        logger.info(f'timeout')
        return
    
    ttb = time_to_bell()
     
    if None not in ttb:
        answer = f'До конца пары осталось: {bold(f"{ttb[1].hour} час {ttb[1].minute} минут")}\n'
        answer += f'До начала пары осталось: {bold(f"{ttb[0].hour} час {ttb[0].minute} минут")}'
    elif ttb[0] is not None: 
        answer = f'Сегодня пары всё.\nЗавтра пара начнется в {bold(ttb[0].time())}'
    else:
        answer = f'На этой недели всё'
    

    msg = await message.answer(answer, parse_mode='markdown')
    if messages[1] is not None:
        await dp.bot.delete_message(message.chat.id, messages[1].message_id)
    messages[1] = msg