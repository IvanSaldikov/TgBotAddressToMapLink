# Основной и единственный модуль программы Телеграм-бота (бакэнд).
# Этому боту можно отправить строку адреса, а бот вернет ссылку на Яндекс.Карты,
# по которой можно перейти и посмотреть, что там по этому адресу
# Также бот умеет сохранять введенные адреса, ссылки, категории.
# Бот доступен по адресу @gotoyam_bot или https://t.me/gotoyam_bot.
#
# (c) Ivan Saldikov 2020, saldoz@ya.ru

"""Сервер Telegram бота, непосредственно запускаемый"""
import configparser
import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, executor, types

from yandex import YandexMap
from categories import Category
from addresses import Address
import exceptions

input_mode = 0
proxy_enabled = False
logging.basicConfig(level=logging.INFO)

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
PROXY_URL = os.getenv("TELEGRAM_PROXY_URL")
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
if proxy_enabled:
    PROXY_AUTH = aiohttp.BasicAuth(
        login=os.getenv("TELEGRAM_PROXY_LOGIN"),
        password=os.getenv("TELEGRAM_PROXY_PASSWORD")
    )

# Если нет токенов в переменных окрежния - то пытаемся читать из файла окружения
if TELEGRAM_API_TOKEN is None:
    tokens = configparser.ConfigParser()
    try:
        tokens.read('.env')
        TELEGRAM_API_TOKEN = tokens.get('KEYS', 'TELEGRAM_API_TOKEN')
    except exceptions.NotCorrectMessage as e:
        print('Error: TELEGRAM_API_TOKEN not set not in Envoronment nor in .env file.')
        exit(100)

if YANDEX_API_KEY is None:
    tokens = configparser.ConfigParser()
    try:
        tokens.read('.env')
        YANDEX_API_KEY = tokens.get('KEYS', 'YANDEX_API_KEY')
    except exceptions.NotCorrectMessage as e:
        print('Error: YANDEX_API_KEY not set not in Envoronment nor in .env file.')
        exit(101)

bot = Bot(token=TELEGRAM_API_TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "*GoToYaM Bot*\n\n"
        "Бот для преобразования адреса в ссылку, ведущую на Яндекс.Карты, где находится этот адрес.\n\n"
        "Добавить адрес: например, введите _Нахимовский проспект 1_\n\n"
        "Мои адреса: /addresses\n\n"
        "Категории адресов: /categories\n\n"
        "Автор: Иван Сальдиков (c) 2020\n"
        "saldoz@ya.ru"
        , parse_mode='Markdown')


@dp.message_handler(lambda message: message.text.startswith('/deladdr'))
async def del_address(message: types.Message):
    """Удаляет одну запись об адресе по её идентификатору"""
    row_id = int(message.text[8:])
    Address().delete_address(row_id)
    answer_message = (
        f'Адрес был успешно *удален*\n\n'
        f"Мои адреса: /addresses\n\n"
        f"Главное меню: /start\n\n"
    )
    await message.answer(answer_message, parse_mode='Markdown')


@dp.message_handler(lambda message: message.text.startswith('/delcat'))
async def del_category(message: types.Message):
    """Удаляет одну запись об адресе по её идентификатору"""
    cat_id = int(message.text[7:])
    cat = Category(message.from_user.id)
    if cat.get_cat_addr_stat(cat_id) == 0:
        cat.delete_category(cat_id)
        answer_message = (
            f'Категория была успешно *удалена*\n\n'
        )
    else:
        answer_message = (
            f'*Нельзя удалять НЕпустую категорию.*\n\n'
            f'*Удалите сначала адреса из этой категории, а затем удалите категорию.*\n\n'
        )
    answer_message += (
        f"Мои адреса: /addresses\n\n"
        f"Мои категории: /categories\n\n"
        f"Главное меню: /start\n\n"
    )
    await message.answer(answer_message, parse_mode='Markdown')


@dp.message_handler(lambda message: message.text.startswith('/addtocat'))
async def add_to_category(message: types.Message):
    """Удаляет одну запись об адресе по её идентификатору"""
    addr_id = int(message.text[9:])
    addr_name = Address().get_name_by_id(message.from_user.id, addr_id)
    all_categories = Category(message.from_user.id).get_all_categories()
    if not all_categories:
        await message.answer(
            "Список категорий пуст\n\n"
            "*Для добавления категории введите* /addcat\n\n"
            "Мои адреса: /addresses\n\n"
            "Начальный экран: /start"
            , parse_mode='Markdown'
        )
        return
    categories_rows = [
        f"*{category_one.name}* - /choosecat{addr_id}to{category_one.id}\n"
        for category_one in all_categories]
    answer_message = f"Выберите категорию, в которую необходимо переместить адрес *{addr_name}*:\n\n" + "\n\n" \
        .join(categories_rows) + \
                     "\n\nНачальный экран: /start" + \
                     "\n\nМои адреса: /addresses" + \
                     "\n\nМои категории: /categories"
    await message.answer(answer_message, parse_mode='Markdown')


@dp.message_handler(lambda message: message.text.startswith('/choosecat'))
async def change_addr_cat(message: types.Message):
    """Меняем категорию адреса"""
    addr_id_to_cat = message.text[10:]
    rows = addr_id_to_cat.split('to')
    try:
        addr_id = int(rows[0])
        cat_id = int(rows[1])
        Category(message.from_user.id).change_category_address(addr_id, cat_id)
        cat_name = Category(message.from_user.id).get_category_name(cat_id)
        addr_name = Address().get_name_by_id(message.from_user.id, addr_id)
        answer_message = f"Адрес *{addr_name}* теперь находится в новой категории *{cat_name}*\n\n" + \
                         f"Просмотреть содержимое в новой категории: /showcataddr{cat_id}"
    except:
        answer_message = f"Ошибка при передаче параметров"

    answer_message += "\n\nМои адреса: /addresses" + \
                      "\n\nМои категории: /categories" + \
                      "\n\nНачальный экран: /start"
    await message.answer(answer_message, parse_mode='Markdown')


@dp.message_handler(lambda message: message.text.startswith('/goto'))
async def goto_address(message: types.Message):
    """Показывает ссылку на адрес на Яндекс.Картах по её идентификатору"""
    row_id = int(message.text[5:])
    link_to_yamaps = Address().get_link_ya_map(message.from_user.id, row_id)
    answer_message = (
        f"Ссылка на Яндекс.Карты: {link_to_yamaps}.\n\n"
        f"Мои адреса: /addresses\n\n"
        f"Главное меню: /start\n\n"
    )
    await message.answer(answer_message, parse_mode='Markdown')


@dp.message_handler(lambda message: message.text.startswith('/showcataddr'))
async def showcataddr(message: types.Message):
    """Показываем адреса в определенной категории"""
    cat_id = message.text[12:]
    cat_id = -1 if cat_id == 'None' else int(cat_id)
    cat_name = Category(message.from_user.id).get_category_name(cat_id)
    all_addresses = Address().get_all_addresses(message.from_user.id, cat_id)
    if not all_addresses:
        await message.answer(
            f"Список адресов в категории *{cat_name}* пуст.\n\n"
            "Для добавления адреса в данную категорию перейдите в список всех адресов.\n\n"
            "Список моих адресов: /addresses\n\n"
            "Список моих категорий: /categories\n\n"
            "Начальный экран: /start"
            , parse_mode='Markdown')
        return

    addresses_rows = [
        f"*{address_one.address}* - /goto{address_one.id}\n"
        f"/addtocat{address_one.id} - переместить этот адрес в другую категорию\n"
        f"/deladdr{address_one.id} - удалить данный адрес из базы"
        for address_one in all_addresses]
    answer_message = f"Список адресов в категории *{cat_name}*:\n\n" + "\n\n" \
        .join(addresses_rows) + \
                     "\n\nСписок моих категорий: /categories" + \
                     "\n\nСписок моих адресов: /addresses" + \
                     "\n\nНачальный экран: /start"
    await message.answer(answer_message, parse_mode='Markdown')


def show_cat_title(cat_name, cat_id):
    """Вовзаращаем строку операции для названия категории только если она существует"""
    if cat_name is not None:
        return f'Категория: _{cat_name}_ - /showcataddr{cat_id}\n'
    else:
        return ''


@dp.message_handler(commands=['addresses'])
async def show_user_addresses(message: types.Message):
    """Отправляет список всех адресов пользователя"""
    all_addresses = Address().get_all_addresses_and_cats(message.from_user.id)
    if not all_addresses:
        await message.answer(
            "Список адресов пуст.\n\n"
            "*Для добавления адреса, просто введите его в строку и отправьте боту*.\n\n"
            "Список моих категорий: /categories\n\n"
            "Начальный экран: /start\n\n"
            , parse_mode='Markdown')
        return

    addresses_rows = [
        f"*{address_one.address}* - /goto{address_one.id}\n"
        f"{show_cat_title(address_one.category_name, address_one.cat_id)}"
        f"/addtocat{address_one.id} - добавить этот адрес в категорию\n"
        f"/deladdr{address_one.id} - удалить данный адрес из базы"
        for address_one in all_addresses]
    answer_message = "Мой список адресов:\n\n" + "\n\n" \
        .join(addresses_rows) + \
                     "\n\nСписок моих категорий: /categories" + \
                     "\n\nНачальный экран: /start"
    await message.answer(answer_message, parse_mode='Markdown')


def show_delcat_title(cat_id, counter):
    """Вовзаращаем строку операции для удаления категории только если категория НЕ пустая"""
    if counter == 0:
        return f"/delcat{cat_id} - удалить данную категорию"
    else:
        return ''


@dp.message_handler(commands=['categories'])
async def show_user_categories(message: types.Message):
    """Отправляет список всех категорий адресов пользователя"""
    all_categories = Category(message.from_user.id).get_all_categories()
    if not all_categories:
        await message.answer(
            "Список категорий пуст.\n\n"
            "*Для добавления категории введите* /addcat\n\n"
            "Мои адреса: /addresses\n\n"
            "Начальный экран: /start"
            , parse_mode='Markdown'
        )
        return
    categories_rows = [
        f"*{category_one.name}* ({category_one.addr_counter})\n"
        f"/showcataddr{category_one.id} - просмотреть адреса категории\n"
        f"{show_delcat_title(category_one.id, category_one.addr_counter)}"
        for category_one in all_categories]
    answer_message = "Список категорий:\n\n" + "\n\n" \
        .join(categories_rows) + \
                     "\n\nДобавить категорию: /addcat" + \
                     "\n\nМои адреса: /addresses" + \
                     "\n\nНачальный экран: /start"
    await message.answer(answer_message, parse_mode='Markdown')


@dp.message_handler(commands=['addcat'])
async def add_category(message: types.Message):
    """Переходит в режим добавления категории"""
    global input_mode
    input_mode = 1
    answer_message = "*Отправьте боту название новой категории для добавления*\n\n" + \
                     "Список категорий: /categories\n\n" + \
                     "Мои адреса: /addresses\n\n" + \
                     "Начальный экран: /start\n\n"
    await message.answer(answer_message, parse_mode='Markdown')


@dp.message_handler()
async def add_address(message: types.Message):
    """Добавляет новый адрес"""
    global input_mode
    answer_message = ''
    try:
        # Добавляем адрес
        if input_mode == 0:
            yandex_map = YandexMap(YANDEX_API_KEY)
            yandex_answer = yandex_map.get_geocode(message.text)
            link_to_yamaps = 'Ничего не найдено, попробуйте повторить попытку позже'
            is_shown = 0
            # Если пришел нормальный ответ от API (два числа через пробел)
            if yandex_answer != -1:
                arr = str(yandex_answer).split()
                if len(arr) == 2:
                    long = arr[0]
                    wide = arr[1]
                    link_to_yamaps = yandex_map.form_href_to_yamap(long, wide)
                    is_shown = 1
            Address().add_address(message.text,
                                  link_to_yamaps,
                                  message.from_user.id,
                                  is_shown)
            answer_message = (
                f"Ссылка на Яндекс.Карты: {link_to_yamaps}.\n\n"
            )
        # Добавляем категорию
        elif input_mode == 1:
            input_mode = 0
            cat_name = str(message.text).replace('*', '')
            Category(message.from_user.id).add_category(cat_name)
            answer_message = (
                f"Новая категория успешно добавлена: *{cat_name}*\n\n"
            )
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message += (
        f"Мои адреса: /addresses\n\n"
        f"Мои категории: /categories\n\n"
        f"Главное меню: /start\n\n"
    )
    await message.answer(answer_message, parse_mode='Markdown')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
