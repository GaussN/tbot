from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        BotCommand('get_schedule', 'вернет расписание на неделю'),
        BotCommand('get_bell_schedule', 'вернет времядо конца и начала пары'),
        #BotCommand('german', 'Герман')
    ])