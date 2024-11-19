from aiogram import Router, F
from aiogram.types import Message
from vpn import add_client, del_client
from database import dynamic
from channel import check_user
import config
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import time

router = Router()

@router.message(F.text == '/start')
async def start(message: Message):
    if time.time() - config.last_client_update >= 3600 * 24:
        config.last_client_update = time.time()
        del_client.del_all_clients()
    await message.answer("Инструкция по подключению:\ntelegra.ph")
    st1, st2 = await check_user(message.chat.id)
    if st1 and st2:
        if message.chat.id in dynamic.users_data:
            await message.answer(
                f"➡️ У вас уже есть соединение VPN, данные для подключения:\n\n```{dynamic.users_data[message.chat.id]['vpn_string']}```\n\n❕Подключение сбрасывается раз в сутки!",
                parse_mode="Markdown")
        else:
            vpn_string = add_client.connect(str(message.chat.id))
            dynamic.users_data[message.chat.id] = {'vpn_string': vpn_string}
            await message.answer(
                f"✔️ Вы успешно создали соединение VPN, данные для подключения:\n\n```{vpn_string}```\n\n❕Подключение сбрасывается раз в сутки!",
                parse_mode="Markdown")
    else:
        try:
            del_client.delete_client(dynamic.users_data[message.chat.id]["vpn_string"])
        except:
            pass
        if message.chat.id in dynamic.users_data:
            dynamic.users_data.pop(message.chat.id)
        keyboard = []
        if not st1:
            keyboard.append([InlineKeyboardButton(text='ЧЗХ', url='https://t.me/+XPI7y5G08bZkNzdi')])
        if not st2:
            keyboard.append([InlineKeyboardButton(text="Промокодочная", url='https://t.me/+5U2hmZ3VonI5ZWEy')])
        keyboard.append([InlineKeyboardButton(text='☑️ Проверить', callback_data='check_user')])
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await message.answer("Вы не подписаны на каналы", reply_markup=markup)

@router.message(F.text)
async def vpn_connect(message: Message):
    if time.time() - config.last_client_update >= 3600 * 24:
        config.last_client_update = time.time()
        del_client.del_all_clients()
    await message.answer("Инструкция по подключению:\ntelegra.ph")
    await message.answer("Для получения ВПН введите /start")

@router.callback_query(F.data == 'check_user')
async def check_user_callback(call):
    if time.time() - config.last_client_update >= 3600 * 24:
        config.last_client_update = time.time()
        del_client.del_all_clients()
    await call.message.edit_text("🔎 Проверяю")
    st1, st2 = await check_user(call.message.chat.id)
    print(st1, st2)
    if st1 and st2:
        await call.message.answer("Инструкция по подключению:\ntelegra.ph")
        await call.message.answer("Чтобы получить данные для подключения, введите /start")
    else:
        try:
            del_client.delete_client(dynamic.users_data[call.message.chat.id]["vpn_string"])
        except:
            pass
        if call.message.chat.id in dynamic.users_data:
            dynamic.users_data.pop(call.message.chat.id)
        keyboard = []
        if not st1:
            keyboard.append([InlineKeyboardButton(text='ЧЗХ', url='https://t.me/+XPI7y5G08bZkNzdi')])
        if not st2:
            keyboard.append([InlineKeyboardButton(text="Промокодочная", url='https://t.me/+rJyP4zXtgMFlYzA6')])
        keyboard.append([InlineKeyboardButton(text='☑️ Проверить', callback_data='check_user')])
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await call.message.answer("Вы не подписаны на каналы", reply_markup=markup)
