Postgresql:
Работа с командной строкой на Windows:
pg_ctl -D "C:\Program Files\PostgreSQL\9.5\data" start
Далее заходим в консоль:
psql -h hostname -d ВАШАБАЗА -U ВАШЛОГИН
например: psql -h localhost -U postgres -d postgres
Далее исправляем кодировку если надо:
psql \! chcp 1251
# https://iu5bmstu.ru/index.php/PostgreSQL_-_Кириллица_в_psql_под_Windows
\l - вывод всех пользователей и таблиц
\d - вывод таблиц и ключей
\dt - вывод всех таблиц внутри
\dS - список отношений


Открытые порты в системе:
netstat -ltupn
