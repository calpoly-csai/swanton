#!/bin/bash
sleep 60 && cd /root/swanton/rasa-1.x/ && docker-compose --env-file ./x86-src.env up -d 
