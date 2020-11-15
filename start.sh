#!/bin/bash

cd rasa-1.x/ && docker-compose up -d
cd .. && python3 -u run_assistant.py
