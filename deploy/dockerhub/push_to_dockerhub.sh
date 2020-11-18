#!/bin/bash
# Script for publishing (pushing) of Telegram_YandexMaps_Bot to Dockerhub
# (c) 2020 Ivan Saldikov, saldoz@ya.ru

# working dir
cd /home/www/code/tgbots/yandex_tg_bot
# cloning last repo
git clone https://github.com/IvanSaldoZ/YandexTgBot
# Remove old contaners from our computer
docker rmi $(docker images -q)
# Go into the app folder with Dockerfile
cd /YandexTgBot
# build new image based on Dockerfile in the folder /YandexTgBot for deployment with new vesion of our app
docker build -t klezcool/yandex_bot ./
# publish image to outside (it is requirement for Yandex API license agreement)
docker push klezcool/yandex_bot
# remove app folder from the disk-drive, because all is in the container
rm -rf ./YandexTgBot