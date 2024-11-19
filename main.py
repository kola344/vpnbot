from fastapi import FastAPI
from bot_init import bot, dp
from typing import Any
from aiogram.types import Update
import config

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/webhook')
async def webhook(update: dict[str, Any]):
    '''АХАХАХХАХАХАХАХАХАХАХ'''
    await dp.feed_webhook_update(bot=bot, update=Update(**update))
    return {'status': 'ok'}

@app.on_event('startup')
async def startup():
    await bot.set_webhook(config.url+'/webhook', drop_pending_updates=True)