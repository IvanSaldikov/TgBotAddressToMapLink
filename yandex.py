# Класс для работы с картами Яндекса

import requests

class YandexMap:
    """Класс для работы с Я.Картами"""
    # https://yandex.ru/dev/maps/geocoder/doc/desc/examples/geocoder_examples.html/
    # https://developer.tech.yandex.ru/services/3
    # https://pypi.org/project/yandex-maps/ (только для второй версии Python)

    # Ключ API для Яндекс-карт (JavaScript API и HTTP Геокодер)
    YANDEX_API_KEY = ""

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
