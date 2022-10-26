from loader import messages
from loader import dp


async def delete_message(chat_id, message, num):
    if chat_id not in messages:
        messages[chat_id] = [None]*4
    if messages[chat_id][num] is not None:
        await dp.bot.delete_message(chat_id, messages[chat_id][num].message_id)
    messages[chat_id][num] = message