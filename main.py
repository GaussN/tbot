from aiogram import executor
from loguru import logger

from handlers import dp


async def startup(dp):
    from utils import set_commands
    await set_commands(dp)


if __name__ == '__main__':
    logger.info('start')
    executor.start_polling(dp, on_startup=startup)