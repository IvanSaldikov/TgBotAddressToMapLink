# Основной и единственный модуль программы Телеграм-бота (бакэнд).
# Этому боту можно отправить строку адреса, а бот вернет ссылку на Яндекс.Карты,
# по которой можно перейти и посмотреть, что там по этому адресу
# Бот доступен по адресу @gotoyam_bot или https://t.me/gotoyam_bot.
# https://www.youtube.com/watch?v=Kh16iosOTIQ
# https://github.com/alexey-goloburdin/telegram-finance-bot

"""Сервер Telegram бота, запускаемый непосредственно"""

import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, executor, types

import exceptions
#import expenses
#from categories import Categories
#from middlewares import AccessMiddleware

from yandex import YandexMap



logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
PROXY_URL = os.getenv("TELEGRAM_PROXY_URL")
YANDEX_TOKEN = os.getenv("YANDEX_API_KEY")
#PROXY_AUTH = aiohttp.BasicAuth(
#    login=os.getenv("TELEGRAM_PROXY_LOGIN"),
#    password=os.getenv("TELEGRAM_PROXY_PASSWORD")
#)


bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот для преобразования адреса в ссылку, ведущую на Яндекс.Карты, где находится этот адрес\n\n"
        "Добавить адрес: Нахимовский проспект 1\n"
        #"Все мои адреса: /adresses\n"
        #"Последние адреса: /last_adresses\n"
        #"Категории трат: /categories"
    )


@dp.message_handler()
async def add_address(message: types.Message):
    """Добавляет новый адрес"""
    try:
        # address = addresses.add_address(message.text)
        yandex_map = YandexMap(YANDEX_TOKEN)
        yandex_answer = yandex_map.get_geocode(message.text)
        link_to_yamaps = 'Ничего не найдено, попробуйте повторить попытку позже'
        # Если пришел нормальный ответ от API (два числа через пробел)
        if yandex_answer != -1:
            arr = str(yandex_answer).split()
            if len(arr) == 2:
                long = arr[0]
                wide = arr[1]
                link_to_yamaps = yandex_map.form_href_to_yamap(long, wide)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Ваша ссылка: {link_to_yamaps}.\n\n"
        )
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)