# Параметры конфигурации приложения

from environs import Env
import aiohttp

# Инициализация переменной для чтения переменных окружения или файла-.env
env = Env()
env.read_env()

# Прокси для Телеграма - неактуально, потому что разблокировали в России,
# но в некоторых случаях может быть нужно
proxy_enabled = False
# Читаем переменные окружения
TELEGRAM_API_TOKEN = env.str("TELEGRAM_API_TOKEN")
YANDEX_API_KEY = env.str("YANDEX_API_KEY")
PROXY_URL = None
PROXY_AUTH = None
if proxy_enabled:
    PROXY_URL = env.str("TELEGRAM_PROXY_URL", '')
    PROXY_AUTH = aiohttp.BasicAuth(
        login=env.str("TELEGRAM_PROXY_LOGIN"),
        password=env.str("TELEGRAM_PROXY_PASSWORD")
    )
# Считываем настройки базы данных
DB_HOST = env.str("DB_HOST")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_NAME = env.str("DB_NAME")
DB_TYPE = env.int("DB_TYPE", 1)  # Database type: 1 - Postgresql, 0 - SQLite3
