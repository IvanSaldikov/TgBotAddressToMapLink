#!/bin/bash
# Script for deployment of Telegram_YandexMaps_Bot (by Ivan Saldikov)
# to Prod server and getting up Docker container based on the last sources from repository on GitHub
# (c) 2020 Ivan Saldikov, saldoz@ya.ru

# working dir = path to docker-compose.yaml file
cd /home/www/code/tgbots/yandex_tg_bot
# cloning last repo
git clone https://github.com/IvanSaldoZ/YandexTgBot
# Shutdown previous one, rebuild (--build meansd) the docker image, run container and run app inside of the container
# (in background if -d key is in) based on the new vesion
docker-compose up -d --build
# remove app folder from the disk-drive, because all is in the container already
rm -rf ./YandexTgBot