from aiogram import Bot, Dispatcher
from bot import router
import config

bot = Bot(token=config.token)
dp = Dispatcher()
dp.include_router(router)
