#!/bin/bash
# Script for deployment of Telegram_YandexMaps_Bot (by Ivan Saldikov)
# to Prod server and getting up Docker container based on the last Dockerhub image
# (c) 2020 Ivan Saldikov, saldoz@ya.ru

# working dir
cd /home/www/code/tgbots/yandex_tg_bot
# Shutdown previous one, rebuild the docker image, run container and run app inside of the container
# based on the new vesion
# -d - means run in background
# --build means stop and run docker containers in docker-compose.yaml file
docker-compose up -d --build