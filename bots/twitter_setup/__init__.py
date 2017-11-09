from os import path, environ

import twitter
from dotenv import load_dotenv

dir_path = path.dirname(path.realpath(__file__))


def load_botenv(bot_id):
    load_dotenv(dotenv_path=path.join(dir_path, "bot_dotenvs", ".bot" + str(bot_id) + ".env"))


def get_bot_username():
    return str(environ.get("TW_USERNAME"))


def get_bot_api():
    return twitter.Api(consumer_key=environ.get("TW_CONSUMER_KEY"),
                       consumer_secret=environ.get("TW_CONSUMER_SECRET"),
                       access_token_key=environ.get("TW_ACCESS_TOKEN"),
                       access_token_secret=environ.get("TW_ACCESS_SECRET"))
