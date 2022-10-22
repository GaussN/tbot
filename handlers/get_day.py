from calendar import week
from datetime import datetime

from aiogram.types import Message
from loguru import logger 

from utils.schedule_parser import build_day
from utils import check_timeout
from loader import schedule_parser
from loader import messages
from loader import dp

@dp.message_handler(commands='get_day')
async def get_day_schedule(message: Message):
    logger.info(f'{message.from_id} get day schedule')
    
    now = datetime.now()
    week_day = datetime.weekday(now)

    await message.delete()

    if not check_timeout(index_in_lrtl=3, timeout=1):
        logger.info(f'timeout')
        return

    # проверка на выходной есть внутри 
    schedule = schedule_parser.get_schedule(week_day)

    days = ('Понедельник', 'Вторник', 'Среда', 'Четверг' ,'Пятница' ,'Суббота')
    message_answer = f'{days[week_day%6]}\n'
    message_answer += build_day(schedule)

    msg = await message.answer(message_answer)
    if messages[3] is not None:
        await dp.bot.delete_message(message.chat.id, messages[3].message_id)
    messages[3] = msg