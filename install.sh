#!/usr/bin/env bash

# Pycorpora requires a download
pip install pycorpora --install-option="--corpora-zip-url=https://github.com/dariusk/corpora/archive/master.zip"
pip install -r requirements.txt
python -m nltk.downloader all

rm -f cron.txt
python cron_setup.py >> cron.txt

crontab cron.txt