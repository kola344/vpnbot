# from bot_init import bot, dp
# import asyncio
#
# async def main():
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot)
#
# if __name__ == '__main__':
#     asyncio.run(main())

import requests
print(requests.post('https://kola344-vpnbot-31c6.twc1.net/followers').text)