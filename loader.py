from aiogram import Bot, Dispatcher

from utils.schedule_parser import ScheduleParser
from config import PARSING_LINK
from config import BOT_TOKEN


bot: Bot = Bot(token=BOT_TOKEN, parse_mode=None)
dp: Dispatcher = Dispatcher(bot)
schedule_parser: ScheduleParser = ScheduleParser(PARSING_LINK)