#!/usr/bin/env bash

# Pycorpora requires a download
pip install pycorpora --install-option="--corpora-zip-url=https://github.com/dariusk/corpora/archive/master.zip"
pip install -r requirements.txt
python -m nltk.downloader all

rm -f cron.txt
python cron_setup.py >> tweeter-cron.txt

# Append new cronjob to the list
crontab -l | cat - tweeter-cron.txt > crontab.txt
rm tweeter-cron.txt
crontab crontab.txt