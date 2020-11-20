FROM python:3.9

WORKDIR /home

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt ./
RUN pip install -r requirements.txt && apt-get update
#  && apt-get install sqlite3
COPY *.py ./
COPY *.sql ./
RUN mkdir db
#COPY db/* ./db/
#RUN cat ./createdb_postgresql.sql | sqlite3  ./db/addresses.db

# Для базы данных
EXPOSE 5432

ENTRYPOINT ["python3", "server.py"]