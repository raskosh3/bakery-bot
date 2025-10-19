#!/bin/bash
cd /var/www/www-root/data/www/ваш-домен
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
