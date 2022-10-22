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
        time_str = ''
        #{bold(f"{ttb[1].hour} час {ttb[1].minute} минут")}
        time_str += bold(ttb[1].hour)
        time_str += ' ' + ('часов' if ttb[1].hour == 0 else 'час' if ttb[1].hour == 1 else 'часа') + ' '
        time_str += bold(ttb[1].minute)
        time_str += ' ' + ('минут' if 20 >= ttb[1].minute >= 10 else 'минута' if ttb[1].hour%10 == 1 else 'минуты' if ttb[1].minute%10<=5 else 'минут') + ' '

        answer = f'До конца пары осталось: {time_str}\n'
        
        time_str = ''
        #{bold(f"{ttb[0].hour} час {ttb[0].minute} минут")}
        time_str += bold(ttb[0].hour)
        time_str += ' ' + ('часов' if ttb[0].hour == 0 else 'час' if ttb[0].hour == 1 else 'часа') + ' '
        time_str += bold(ttb[0].minute)
        time_str += ' ' + ('минут' if 20 >= ttb[0].minute >= 10 else 'минута' if ttb[0].hour%10 == 1 else 'минуты' if ttb[0].minute%10<=5 else 'минут') + ' '
    
        answer += f'До начала пары осталось: {time_str}'
    elif ttb[0] is not None: 
        answer = f'Сегодня пары всё.\nЗавтра пара начнется в {bold(ttb[0].time())}'
    else:
        answer = f'На этой недели всё по звонкам'
    

    msg = await message.answer(answer, parse_mode='markdown')
    if messages[1] is not None:
        await dp.bot.delete_message(message.chat.id, messages[1].message_id)
    messages[1] = msg