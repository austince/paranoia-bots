"""
Bot name: Paranoia Bots
Author: Austin Cawley-Edwards
Twitter handles: paranoiabot1, paranoiabot2
"""

import random
import re
import time
import os
import inspect
import twitter
import nltk

# Generation functions
from bots.tweet_makers import brainwash, jim_butcher, all_wondering, make_simple_response
# loaded corpi
from bots.tweet_makers import nouns, people, body_parts

from bots import api, bot_id, other_bot_usernames
from bots.corpus import load_corpus

from youtube_reverser import reverser

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

debug = False

last_checked_basename = 'last-checked'
last_checked_filename = last_checked_basename + str(bot_id) + ".txt"
log_time_format = "%Y-%m-%d %H:%M"


# Save and load last time this was run
# Used in time range for twitter search
# IN FORMAT: YYYY-MM-DD
# Right now just gm time, will deal with utc if necessary.
def save_last_checked(since_id):
    if debug:
        return
    with open(last_checked_filename, 'w') as f:
        f.write(str(since_id))


def last_checked_exists():
    return os.path.exists(last_checked_filename)


def load_last_checked():
    with open(last_checked_filename, 'r') as f:
        return f.readline()


# Should also check the ethical concerns
def is_valid_tweet(tweet):
    """
    Makes sure a string fits the parameters for twitter
    :param tweet: str
    :return:
    """
    return len(tweet) <= 140


def get_last_mentions():
    """
    Gets all mentions for the current bot since the last time checked
    :return:
    """
    if not debug and last_checked_exists():
        last_checked_id = load_last_checked()
        tweets = api.GetMentions(since_id=last_checked_id)
    else:
        tweets = api.GetMentions()

    if len(tweets) > 0:
        save_last_checked(tweets[0].id)
    return tweets


def get_random_tweet(term):
    return random.choice(api.GetSearch(term=term))


def clean_tweet_text(text):
    # Remove all @ tags, urls, then excess whitespace
    handle_patt = re.compile('(@|http|https)([^\s]*)')
    return handle_patt.sub('', text).strip()


def get_all_tagged(tag, tagged):
    tagged_items = filter(lambda i: i[1] == tag, tagged)
    return [item[0] for item in tagged_items]


def get_nouns(tagged):
    return get_all_tagged('NN', tagged)


def get_verbs(tagged):
    """
    All present-tense verbs
    :param tagged:
    :return:
    """
    return get_all_tagged('VBP', tagged)


def similar_nouns(nltk_text, response_nouns=nouns):
    n = random.choice(response_nouns)

    if '_word_context_index' not in [prop for prop, thing in inspect.getmembers(nltk_text)]:
        # Build word index only once
        nltk_text.similar(n)

    sim_nouns = nltk_text._word_context_index.similar_words(n)
    return sim_nouns[0] if len(sim_nouns) > 0 else random.choice(response_nouns)


def random_video_tweet():
    reversed_path = reverser.get_random_reversed()
    try:
        with open(reversed_path, 'rb') as media:
            api.PostUpdate("#TrustNoOne", media=media)
    except twitter.TwitterError:  # if an error, let us know
        print('- error posting video!')
    finally:
        os.remove(reversed_path)


def video_tweet(query, response, reply_id):
    reversed_path = reverser.get_reversed(query)
    try:
        print("Posting video")
        with open(reversed_path, 'rb') as media:
            api.PostUpdate(response, media=media, in_reply_to_status_id=reply_id)
    except twitter.TwitterError:  # if an error, let us know
        print('- error posting video!')
    finally:
        os.remove(reversed_path)


def respond_to_tweet(tweet, nltk_text, tag_user=False, respond_to_user=False):
    text = clean_tweet_text(tweet.text)
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)

    tweet_nouns = get_nouns(tagged)
    if len(tweet_nouns) == 0:
        print("No nouns in this tweet :/")
        noun = similar_nouns(nltk_text)
    else:
        noun = similar_nouns(nltk_text, response_nouns=tweet_nouns)

    res = make_simple_response(noun)

    if tag_user:
        res += '@' + tweet.user.screen_name

    if not respond_to_user:
        tweet.id = None  # Remove id from tweet so it doesn't get quoted

    print('Response: ' + res)

    if debug:
        return

    if random.random() * 2 < 1:
        # half the time, tweet a video response???
        print("Video response for " + noun)
        video_tweet(noun, res, reply_id=tweet.id)
    else:
        try:
            api.PostUpdate(res, in_reply_to_status_id=tweet.id)
        except twitter.TwitterError:  # if an error, let us know
            print('- error responding!')


def post_tweet(tweet):
    status = None
    print('posting tweet...')
    print(tweet)
    try:
        if not debug:
            status = api.PostUpdate(tweet)  # try posting
        print('- success!')
    except twitter.TwitterError:  # if an error, let us know
        print('- error posting!')
    return status


if __name__ == "__main__":
    # if debug:
    #     brown_word_text = nltk.Text([word.lower() for word in nltk.corpus.brown.words()][:1000])
    # else:
    #     brown_word_text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
    print("Building paranoid text")
    # dalloway = nltk.tokenize.word_tokenize(load_corpus('books/mrs-dalloway'))
    # catcher = nltk.tokenize.word_tokenize(load_corpus('books/catcher-in-the-rye'))
    # bell_jar = nltk.tokenize.word_tokenize(load_corpus('books/the-bell-jar'))
    # tender = nltk.tokenize.word_tokenize(load_corpus('books/tender-is-the-night'))
    # paranoid_text = catcher + dalloway + bell_jar + tender
    paranoid_text = load_corpus('words/paranoid')  # prebuilt and saved
    paranoid_nltk_text = nltk.Text(paranoid_text)

    # Respond to all mentions
    print("---------------- BOT:" + str(bot_id) + " ----------------")
    print(time.strftime(log_time_format, time.gmtime()))
    print('\n')

    print("Getting last mentions")
    mentions = get_last_mentions()
    print("Responding to tweets")
    for mention in mentions:
        print("Responding to @" + mention.user.screen_name + ": " + mention.text)
        respond_to_tweet(mention, paranoid_nltk_text, respond_to_user=True)

    # Grab a random tweet and respond to it

    terms_list = nouns + people + body_parts
    term = random.choice(terms_list)
    print("Getting random tweet for " + term)
    rand_tweet = get_random_tweet(term)
    print(rand_tweet.text)
    # Respond to random tweet

    respond_to_tweet(rand_tweet, paranoid_nltk_text)
    # respond_to_tweet(rand_tweet, brown_word_text)

    # Generate a new tweet and tweet it at another paranoid bot
    tweet_text = None
    num_attempts = 0
    while tweet_text is None or not is_valid_tweet(tweet_text):
        tweet_maker = random.choice([
            brainwash,
            jim_butcher,
            all_wondering
        ])

        print('Trying to make a valid tweet')
        tweet_text = tweet_maker() + "@" + random.choice(other_bot_usernames)

        num_attempts += 1
        if num_attempts > 10:
            print("Couldn't create a tweet. Blame the NSA.")
            exit(1)  # Bye

    post_tweet(tweet_text)
    print("------------------- DONE WITH THIS RUN!!! -------------------")
