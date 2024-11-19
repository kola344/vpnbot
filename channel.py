from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
import config

bot = Bot(token=config.token)

async def check_user(user_id: int) -> (bool, bool):
    try:
        member = await bot.get_chat_member(chat_id=config.channel_id_1, user_id=user_id)
        print(member.status.value, user_id)
        st1 = member.status.value in ("member", "administrator", "creator")
    except TelegramBadRequest as e:
        print(e)
        st1 = False
    try:
        member = await bot.get_chat_member(chat_id=config.channel_id_2, user_id=user_id)
        print(member.status.value, user_id)
        st2 = member.status.value in ("member", "administrator", "creator")
    except TelegramBadRequest as e:
        print(e)
        st2 = False
    return st1, st2