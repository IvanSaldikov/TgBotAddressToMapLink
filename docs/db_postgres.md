Postgresql:
Работа с командной строкой на Windows:
pg_ctl -D "C:\Program Files\PostgreSQL\9.5\data" start
Далее заходим в консоль:
psql -h hostname -d ВАШАБАЗА -U ВАШЛОГИН
например: psql -h localhost -U postgres -d postgres
Далее исправляем кодировку если надо:
psql \! chcp 1251
# https://iu5bmstu.ru/index.php/PostgreSQL_-_Кириллица_в_psql_под_Windows
\l - вывод всех таблиц
\d - вывод таблиц и ключей
\dt - вывод всех таблиц внутри
\dS - список отношений
\du - список пользователей


Открытые порты в системе:
netstat -ltupn


### Docker-образ БД Postgres
https://hub.docker.com/_/postgres

```
  db:
    image: postgres
    restart: always
    ports:
      - 5432:5432
    volumes:
      - postgresql_volume:/var/lib/postgresql/data
    environment:
      POSTGRES_DB=
      POSTGRES_USER=
      POSTGRES_PASSWORD=
      PGDATA=/var/lib/postgresql/data/pgdata
      DB_HOST=
      DB_USER=
      DB_PASSWORD=
      DB_NAME=      
          
  adminer:
    image: adminer
    restart: always
    ports:
      - 8080:8080          
```

Adminer используется для работы с данными в браузере

Ну и `EXPOSE 5432` не забываем в `Dockerfile`.