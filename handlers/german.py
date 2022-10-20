from random import choice
import os

from loguru import logger
from aiogram import types

from loader import dp


@logger.catch
@dp.message_handler(commands='german')
async def _(message: types.Message):
    logger.info(f'PRANK Z GERMANA')

    await message.answer('на php пишет', reply=True)