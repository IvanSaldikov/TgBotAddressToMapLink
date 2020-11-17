FROM python:3.9

WORKDIR /home

#ENV TELEGRAM_API_TOKEN=""
#ENV YANDEX_API_KEY =""
ENV TELEGRAM_ACCESS_ID=""
ENV TELEGRAM_PROXY_URL=""
ENV TELEGRAM_PROXY_LOGIN=""
ENV TELEGRAM_PROXY_PASSWORD=""

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt ./
RUN pip install -r requirements.txt && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY *.sql ./
RUN mkdir db
COPY db/* ./db/
RUN cat ./createdb.sql | sqlite3  ./db/addresses.db

ENTRYPOINT ["python3", "server.py"]