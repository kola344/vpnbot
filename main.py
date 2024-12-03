from fastapi import FastAPI
from bot_init import bot, dp
from typing import Any
from aiogram.types import Update
import config
from aiohttp import ClientSession
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/webhook')
async def webhook(update: dict[str, Any]):
    '''АХАХАХХАХАХАХАХАХАХАХ'''
    await dp.feed_webhook_update(bot=bot, update=Update(**update))
    return {'status': 'ok'}

@app.post("/followers")
async def get_followers():
    async with ClientSession() as session:
        tiktok_followers = await follower_tiktok(session)
        nuum_followers = await follower_nuum(session)
        telegram_followers = await follower_tg(session)

    return JSONResponse(
        content={
            "tiktok": tiktok_followers,
            "nuum": nuum_followers,
            "telegram": telegram_followers
        }
    )

async def follower_nuum(session: ClientSession):
    try:
        url = "https://nuum.ru/api/v2/broadcasts/public?with_extra=true&channel_name=4zh&with_deleted=true"
        async with session.get(url, ssl=False) as response:
            response.raise_for_status()
            data = await response.json()
            return data.get("result", {}).get("channel", {}).get("followers_count", 4000)
    except Exception as e:
        print(e)
        return 4500

async def follower_tg(session: ClientSession):
    try:
        url = "https://t.me/+KzLfDZh9lMY0MWFi"
        async with session.get(url, ssl=False) as response:
            response.raise_for_status()
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            text = soup.select_one("div.tgme_page_extra").text
            numbers = [str(num) for num in text.split() if num.isdigit()]
            return ''.join(numbers) if numbers else 6000
    except Exception as e:
        print(e)
        return 6500

async def follower_tiktok(session: ClientSession):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
        }
        username = "che_obzor"
        url = f"https://app.jagajam.com/v4/search?q={username}&socialTypes[0]=TT&page=1&perPage=10&token=&trackTotal=true&extended=true"
        async with session.get(url, headers=headers, ssl=False) as response:
            response.raise_for_status()
            data = await response.json()
            return data["data"][0]["usersCount"]
    except Exception as e:
        print(e)
        return 63000

@app.on_event('startup')
async def startup():
    await bot.set_webhook(config.url+'/webhook', drop_pending_updates=True)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)