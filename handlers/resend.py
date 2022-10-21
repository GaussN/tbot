import os

from loguru import logger
from aiogram import types
from config import GROUP_ID
from config import ADMIN_ID

from loader import dp, bot


@dp.message_handler(commands=['send'])
async def _(message: types.Message):
    
    if str(message.from_user.id) in str(ADMIN_ID):
        new_text = message.text.replace('/send', '')
        await bot.send_message(GROUP_ID, new_text)
    else:
        await message.reply('❌')