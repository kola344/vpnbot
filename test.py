from bot_init import bot, dp
import asyncio

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

import aiohttp
import asyncio
import hashlib

# Данные для подключения к API
API_URL = "https://194.87.55.42:51957/cbItC0jvngdbZWVN4m0jVA"
CERT_SHA256 = "5CFFBF3ABAE51BC5A9F7D2FC47064341D4FA93F03C13F842CF17D760FDCE77F7"

# Функция для проверки сертификата сервера
def verify_cert(cert):
    hash_object = hashlib.sha256(cert)
    return hash_object.hexdigest().upper() == CERT_SHA256

# Асинхронная функция для добавления нового клиента
async def add_client():
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/access-keys", ssl=False) as response:
            if response.status == 201:
                client_data = await response.json()
                return client_data  # возвращает данные для подключения к VPN
            else:
                return f"Ошибка добавления клиента: {response.status}, {await response.text()}"

# Асинхронная функция для удаления клиента по его ID
async def delete_client(client_id):
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{API_URL}/access-keys/{client_id}", ssl=False) as response:
            if response.status == 204:
                return "Клиент успешно удален"
            else:
                return f"Ошибка удаления клиента: {response.status}, {await response.text()}"

# Асинхронная функция для удаления всех клиентов
async def delete_all_clients():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/access-keys", ssl=False) as response:
            if response.status == 200:
                clients = (await response.json()).get('accessKeys', [])
                errors = []
                # Удаляем каждого клиента по его ID
                for client in clients:
                    client_id = client['id']
                    async with session.delete(f"{API_URL}/access-keys/{client_id}", ssl=False) as del_response:
                        if del_response.status != 204:
                            errors.append(f"Ошибка удаления клиента {client_id}: {del_response.status}")
                if errors:
                    return "Не все клиенты удалены: " + "; ".join(errors)
                else:
                    return "Все клиенты успешно удалены"
            else:
                return f"Ошибка получения списка клиентов: {response.status}, {await response.text()}"

# Примеры использования
async def main():
    # print(await add_client())
    print(await delete_client(9))
    # print(await delete_all_clients())

# Запуск главной асинхронной функции
asyncio.run(main())