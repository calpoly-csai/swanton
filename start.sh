#!/bin/bash

cd rasa-1.x/ && docker-compose run --env-file=rasa-1.x/arm-src.env -d rasa
cd .. && python3 -u run_assistant.py
