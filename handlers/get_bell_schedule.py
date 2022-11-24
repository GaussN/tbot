from datetime import datetime

from aiogram.utils.markdown import bold
from loguru import logger
from aiogram import types

from utils.check_timeout import check_timeout
from utils.bell_schedule import time_to_bell
from utils import delete_message
from config import TIMEOUT
from loader import messages
from loader import dp


@logger.catch
@dp.message_handler(commands='get_bell_schedule')
async def _(message: types.Message):
    logger.info(f'{message.from_id} get bell schedule')

    await message.delete()

    if not check_timeout(index_in_lrtl=1, timeout=TIMEOUT):
        logger.info(f'timeout')
        return
    
    ttb = time_to_bell()
    
    message_answer = ''

    logger.debug(f'ttb: {ttb}')

    if ttb == (None, None):
        message_answer = 'На этой неделе всё'
    elif None not in ttb:
        time_str = ''
        if ttb[1].hour != 0:
            time_str += bold(ttb[1].hour)
            time_str += ' ' + ('часов' if ttb[1].hour == 0 else 'час' if ttb[1].hour == 1 else 'часа') + ' '
        time_str += bold(ttb[1].minute)
        time_str += ' ' + ('минут' if (20 > ttb[1].minute > 10  or ttb[1].minute % 10 == 0) else 'минута' if ttb[1].minute%10 == 1 else 'минут' if ttb[1].minute%10 >= 5 else 'минуты') + ' '

        message_answer = f'До конца пары осталось: {time_str}\n'
        
        time_str = ''
        if ttb[0].hour != 0:
            time_str += bold(ttb[0].hour)
            time_str += ' ' + ('часов' if ttb[0].hour == 0 else 'час' if ttb[0].hour == 1 else 'часа') + ' '
        time_str += bold(ttb[0].minute)
        time_str += ' ' + ('минут' if (20 > ttb[0].minute > 10 or ttb[0].minute % 10 == 0) else 'минута' if ttb[0].minute%10 == 1 else 'минут' if ttb[0].minute%10 >= 5 else 'минуты') + ' '
        # time_str += ' ' + ('минут' if (20 >= ttb[0].minute >= 10 or ttb[0].minute % 10 < 5 or ttb[0].minute % 10 == 0) else 'минута' if ttb[0].minute % 10 == 1 else 'минуты') + ' '
    
        message_answer += f'До начала пары осталось: {time_str}'
    elif ttb[1] is None: 
        dzisiajalbojutro = 'завтра '
        if ttb[0].time() > datetime.now().time():
            dzisiajalbojutro = ''
        message_answer = f'Сегодня пары всё.\nПара начнется {dzisiajalbojutro}в {bold(ttb[0].time())}'
    else:
        message_answer = f'На этой недели всё по звонкам'
    
    chat_id = message.chat.id
    msg = await message.answer(message_answer, parse_mode='markdown')
    
    await delete_message(chat_id, msg, 3)