# Основной и единственный модуль программы Телеграм-бота (бакэнд).
# Этому боту можно отправить строку адреса, а бот вернет ссылку на Яндекс.Карты,
# по которой можно перейти и посмотреть, что там по этому адресу
# Бот доступен по адресу @gotoyam_bot или https://t.me/gotoyam_bot.
# https://www.youtube.com/watch?v=Kh16iosOTIQ
# https://github.com/alexey-goloburdin/telegram-finance-bot

"""Сервер Telegram бота, запускаемый непосредственно"""
import configparser
import logging
import os

from aiogram import Bot, Dispatcher, executor, types

import exceptions
#import expenses
#from categories import Categories
#from middlewares import AccessMiddleware

from yandex import YandexMap
import addresses



logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
PROXY_URL = os.getenv("TELEGRAM_PROXY_URL")
YANDEX_TOKEN = os.getenv("YANDEX_API_KEY")
#PROXY_AUTH = aiohttp.BasicAuth(
#    login=os.getenv("TELEGRAM_PROXY_LOGIN"),
#    password=os.getenv("TELEGRAM_PROXY_PASSWORD")
#)

# Если Windows - то пытаемся читать из файла окружения
if API_TOKEN == None:
    tokens = configparser.ConfigParser()
    tokens.read('.env')
    API_TOKEN = tokens.get('KEYS', 'TELEGRAM_API_TOKEN')

if YANDEX_TOKEN == None:
    tokens = configparser.ConfigParser()
    tokens.read('.env')
    YANDEX_TOKEN = tokens.get('KEYS', 'YANDEX_API_KEY')

#print('TELEGRAM_API_TOKEN', API_TOKEN)
#print('YANDEX_API_TOKEN', YANDEX_TOKEN)


bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот для преобразования адреса в ссылку, ведущую на Яндекс.Карты, где находится этот адрес\n\n"
        "Добавить адрес: Нахимовский проспект 1\n\n"
        "Все мои адреса: /addresses\n\n"
        #"Последние адреса: /last_adresses\n"
        #"Категории трат: /categories"
        "Автор: Сальдиков Иван (c) 2020\n"
        "saldoz@ya.ru"
    )


@dp.message_handler(commands=['addresses'])
async def show_user_addresses(message: types.Message):
    """Отправляет список всех адресов пользователя"""
    all_addresses = addresses.get_all_addresses(message.from_user.id)
    if not all_addresses:
        await message.answer("Вы ещё не сохранили ни одного адреса")
        return

    addresses_rows = [
        f"*{address_one.address}* - /goto{address_one.id}\n"
        f"/addtocat - добавить в категорию\n"
        f"/del{address_one.id} - удалить адрес"
        for address_one in all_addresses]
    answer_message = "Ваш список адресов:\n\n" + "\n\n"\
            .join(addresses_rows) + \
            "\n\nНачальный экран: /start"
    await message.answer(answer_message, parse_mode= "Markdown")

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
        db_id = addresses.add_address(message.text,
                                      link_to_yamaps,
                                      message.from_user.id)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Ваша ссылка на Яндекс.Карты: {link_to_yamaps}.\n\n"
        f"Все Ваши адреса: /addresses\n\n"
        f"Главное меню: /start\n\n"
        )
    await message.answer(answer_message)

@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись об адресе по её идентификатору"""
    row_id = int(message.text[4:])
    addresses.delete_address(row_id)
    answer_message = (
        f"Все Ваши адреса: /addresses\n\n"
        f"Главное меню: /start\n\n"
        )
    await message.answer(answer_message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

