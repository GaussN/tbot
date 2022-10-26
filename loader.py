from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher

from utils.schedule_parser import ScheduleParser
from config import PARSING_LINK
from config import BOT_TOKEN


bot: Bot = Bot(token=BOT_TOKEN, parse_mode=None)
dp: Dispatcher = Dispatcher(bot)
schedule_parser: ScheduleParser = ScheduleParser(PARSING_LINK)

# перое значение для запроса расписания 
# второе значение для запроса времени до звонка 
last_request_time = [
    datetime.now() - timedelta(minutes=3), 
    datetime.now() - timedelta(minutes=3), 
    datetime.now() - timedelta(minutes=3), 
    datetime.now() - timedelta(minutes=3), 
]
# бот должен удалять старые сообщения с расписанием при запросе новых 
# тут будут храниться старые(id)
# перое значение для сообщения с расписанием 
# второе значение для сообщения с временем до звонка 
messages = {}