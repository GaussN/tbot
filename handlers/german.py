from random import choice
import os

from loguru import logger
from aiogram import types

from loader import dp


@logger.catch
@dp.message_handler(commands='german')
async def _(message: types.Message):
    logger.info(f'PRANK Z GERMANA')

    if not os.path.exists('./media'):
        logger.warning('./media does not exist')
        return

    await message.answer('на php пишет', reply=True)