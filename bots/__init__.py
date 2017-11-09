import random

from .corpus import load_corpus
from .twitter_setup import load_botenv, get_bot_api, get_bot_username

# Choose a random bot to run
bot_id = random.choice([1, 2])

# Loads random by default
load_botenv(bot_id)

api = get_bot_api()

username = get_bot_username()

bot_usernames = load_corpus('twitter/paranoia_bots')
other_bot_usernames = filter(lambda other_bot_name: other_bot_name != username,
                             bot_usernames)
