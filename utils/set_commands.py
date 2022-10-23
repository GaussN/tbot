from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        BotCommand('get_schedule', '| Получить расписание занятий'),
        BotCommand('get_day', '| Получить расписание занятий на день'),
        BotCommand('get_bell_schedule', '| Получить время до конца и до начала пары'),
        BotCommand('get_full_bell_schedule', '| Получить полное расписание звонков'),
        BotCommand('info', '| Информация о боте')
        #BotCommand('german', 'Герман')
    ])