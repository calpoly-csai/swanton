#!/bin/sh

OS=$(lsb_release -si)
if [ $OS = "Debian" ]; then
	echo 'repo=rasa' > .env
else
	echo 'repo=koenvervloesem' > .env
fi
sudo docker-compose up -d
