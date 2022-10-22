from loguru import logger
from aiogram import types
from config import ADMIN_ID

from loader import dp, bot


@dp.message_handler(commands=['send'])
async def _(message: types.Message):
    logger.info(f'{message.from_id} send')
    if str(message.from_user.id) in ADMIN_ID:
        new_text = message.text.replace('/send', '')
        if new_text.strip() != '': 
            logger.success('message sent')
            await bot.send_message(message.chat.id, new_text)
        await message.delete()
    else:
        logger.error('message nоt sent')
        await message.reply('❌')