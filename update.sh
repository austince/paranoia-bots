#!/usr/bin/env bash

git pull

pip install -r requirements.txt

echo "Updated on $(date +%Y\ %m\ %d\ %H:%M:%S)" >> tweets.log