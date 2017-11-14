#!/usr/bin/env bash

# If it's not a git repo, make it one
if ! [[ -d .git ]]; then
git init
git remote add origin https://github.com/austince/paranoia-bots.git
fi

git pull origin master

pip install -r requirements.txt

echo "Updated on $(date +%Y\ %m\ %d\ %H:%M:%S)" >> tweets.log