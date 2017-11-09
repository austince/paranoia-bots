#!/usr/bin/env bash

pip install -r requirements.txt

python cron_setup.py >> cron.txt

crontab cron.txt