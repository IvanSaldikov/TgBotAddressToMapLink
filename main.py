# Основной и единственный модуль программы Телеграм-бота (бакэнд).
# Этому боту можно отправить строку адреса, а бот вернет ссылку на Яндекс.Карты,
# по которой можно перейти и посмотреть, что там по этому адресу
# Бот доступен по адресу @gotoyam_bot или https://t.me/gotoyam_bot.

# Подключаем Telegram API и библиотеку requests для запросов к API Яндекса
import telebot
import requests


class YandexMap:
    """Класс для работы с Я.Картами"""
    # https://yandex.ru/dev/maps/geocoder/doc/desc/examples/geocoder_examples.html/
    # https://developer.tech.yandex.ru/services/3
    # https://pypi.org/project/yandex-maps/ (только для второй версии Python)

    # Ключ API для Яндекс-карт (JavaScript API и HTTP Геокодер)
    YANDEX_API_KEY = "{YOUR_TOKEN_API_KEY_HERE}"

    def get_geocode(self, addr):
        """Метод для получения ширины и долготы по введенному адресу с помощьюч API Яндекс-карт"""
        URL = f"https://geocode-maps.yandex.ru/1.x/?apikey={self.YANDEX_API_KEY}&geocode={addr}&format=json&results=1&lang=ru_RU"
        result = requests.get(URL).json()
        # return result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        # Возвращаем координаты точки адреса, введенного пользователем
        return result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']

    def form_href_to_yamap(self, long, wide):
        """Формируем ссылку на карты для перехода"""
        # https://yandex.ru/blog/mapsapi/18681
        # http://maps.yandex.ru/?ll=30.373136,60.006291&spn=0.067205,0.018782&z=15&l=map,stv,pht
        return f"http://maps.yandex.ru/?ll={long},{wide}&spn=0.067205,0.018782&z=15&l=map,stv,pht&text={wide}%20{long}"


class TelegramBot:
    """Класс для работы с Телеграм-ботом"""
    # https://prognote.ru/web-dev/beck-end/basics-of-creating-a-telegram-bot-in-python/
    # https://habr.com/ru/post/442800/

    # Токен для Телеграм-бота
    TG_TOKEN = '{YOUR_TOKEN_API_KEY_HERE}'

    def run_bot(self, yandex_map):
        """Запускам в работу ТГ-бота"""
        self.bot = telebot.TeleBot(self.TG_TOKEN)

        # Обработка входящих сообщений - текстовых (text)
        @self.bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            """Возвращаем геокод по введенному адресу в бота message.text"""
            link_to_yamaps = 'Ничего не найдено, попробуйте повторить попытку позже'
            yandex_answer = yandex_map.get_geocode(message.text)
            # Если пришел нормальный ответ от API (два числа через пробел)
            arr = str(yandex_answer).split()
            if len(arr) == 2:
                long = arr[0]
                wide = arr[1]
                link_to_yamaps = yandex_map.form_href_to_yamap(long, wide)
            # Отправляем ответное сообщение пользователю со ссылкой
            self.bot.send_message(message.from_user.id, link_to_yamaps)

        # Запускаем слежение за командами пользователям из чата
        self.bot.polling(timeout=0, none_stop=True, interval=30)


if __name__ == '__main__':

    # Создаем класс Яндекс-карт, а затем передаем его Тг-Боту и запускаем бота
    yandex_map = YandexMap()
    bot = TelegramBot()
    bot.run_bot(yandex_map)
