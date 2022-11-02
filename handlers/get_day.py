from datetime import datetime

from aiogram.types import Message
from loguru import logger 

from utils.bell_schedule import get_last_lesson
from utils.schedule_parser import build_day
from utils import delete_message
from utils import check_timeout
from config import TIMEOUT
from loader import schedule_parser
from loader import messages
from loader import dp
from config import BELLS


@logger.catch
@dp.message_handler(commands='get_day')
async def get_day_schedule(message: Message):
    logger.info(f'{message.from_id} get day schedule')
    
    now = datetime.now()
    week_day = datetime.weekday(now)

    logger.debug(f'{now=}')
    logger.debug(f'{week_day=}')

    await message.delete()

    if not check_timeout(index_in_lrtl=3, timeout=TIMEOUT):
        logger.info(f'timeout')
        return

    message_answer = 'Сегодня пар нет'
    if week_day != 6:
        schedule = schedule_parser.get_schedule(week_day)

        days = ('Понедельник', 'Вторник', 'Среда', 'Четверг' ,'Пятница' ,'Суббота')
        message_answer = f'{days[week_day]}\n' # если сегодня вс то вернет пары на пн
        message_answer += build_day(schedule)

    last_lesson = get_last_lesson(schedule)
    end_time = datetime.strptime(BELLS[week_day][last_lesson][1], '%H.%M')

    if now.time() > end_time.time():
        message_answer = 'Пары закончились'

    chat_id = message.chat.id
    msg = await message.answer(message_answer)
    
    await delete_message(chat_id, msg, 1)