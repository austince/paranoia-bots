import random
from os import environ, path, mkdir, remove
import subprocess

import requests
import pafy

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

dir_path = path.dirname(path.realpath(__file__))
download_dir = path.join(dir_path, 'downloads')

if not path.exists(download_dir):
    mkdir(download_dir)

random_youtube_api_url = "https://randomyoutube.net/api/getvid?api_token=" + environ.get('RANDOM_YOUTUBE_API_KEY')
youtube_api_key = environ.get('YOUTUBE_API_KEY')


class APIException(Exception):
    pass


# https://github.com/cubbK/youtubeRandomVideoNodeJs/
def genereaza_cuvint():
    text = ""
    possible_chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    for i in range(0, 3):
        text += random.choice(possible_chars)
    return text


def get_youtube_url_youtube_api(query=genereaza_cuvint()):
    youtube_api_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50' \
                      '&key=' + youtube_api_key \
                      + '&q=' + query
    res = requests.get(youtube_api_url)
    if res.ok:
        data = res.json()
        vids = filter(lambda v: v["id"]["kind"] == 'youtube#video', data["items"])
        vid_id = random.choice(vids)["id"]["videoId"]
        return 'https://www.youtube.com/watch?v=' + vid_id, vid_id


def get_random_youtube_url():
    res = requests.get(random_youtube_api_url)
    if res.ok:
        data = res.json()
        if res.status_code == 429:
            raise APIException("Can't access api", res)
        return 'https://www.youtube.com/watch?v=' + data["vid"], data["vid"]
    else:
        raise APIException("Can't access api", res)


def download_file(url, to_filepath):
    if not path.exists(to_filepath):
        open(to_filepath, 'a')

    res = requests.get(url, stream=True)
    if res.ok:
        with open(to_filepath, 'wb') as f:
            chunk_num = 0
            for chunk in res.iter_content(chunk_size=1024):
                chunk_num += 1
                if chunk_num % 20000 == 0:
                    print("Downloaded " + str(chunk_num) + " chunks")
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
    else:
        raise Exception("Can't download file", res)


def download_youtube_video(query='', max_len=450):
    url, vid_id = None, None
    video = None

    max_tries = 10
    num_tries = 0
    while video is None or video.length < max_len:
        url, vid_id = get_youtube_url_youtube_api(query=query)
        try:
            video = pafy.new(url)
        except IOError:
            print("Error getting youtube video for " + str(vid_id))
            video = None

        num_tries += 1
        if num_tries >= max_tries:
            # Default to random
            print("Defaulting to random!")
            return download_random_youtube_video(max_len=max_len)

    best = video.getbest(preftype='mp4')

    filepath = path.join(download_dir, str(vid_id) + ".mp4")
    download_file(best.url, filepath)
    return filepath


def download_random_youtube_video(max_len=450):
    """

    :param max_len: in seconds, defaults to 7.5 mins which is about 13.5 mb on avg
    :return:
    """
    rand_url, vid_id = None, None
    video = None

    while video is None or video.length < max_len:
        try:
            rand_url, vid_id = get_random_youtube_url()
        except APIException:
            # Fall back to the regular youtube api
            print("Falling back to google api")
            rand_url, vid_id = get_youtube_url_youtube_api(query=genereaza_cuvint())

        try:
            video = pafy.new(rand_url)
        except IOError:
            print("Error getting youtube video for " + str(vid_id))
            video = None

    best = video.getbest(preftype='mp4')

    filepath = path.join(download_dir, str(vid_id) + ".mp4")
    download_file(best.url, filepath)
    return filepath


def prefix_file(filepath, prefix):
    filename = path.basename(filepath)
    filedir = path.dirname(filepath)
    return path.join(filedir, prefix + filename)


def reverse_video(filepath):
    reversed_path = prefix_file(filepath, "reversed-")
    subprocess.call([
        "ffmpeg",
        "-y",
        "-i", filepath,
        "-vf", "reverse",  # Reverse the video
        "-af", "areverse",  # and the audio ...
        reversed_path
    ])
    return reversed_path


def trim_video(filepath, length=15):
    """

    :param filepath:
    :param length: seconds, defaults to 15s for twitter
    :return:
    """
    trimmed_path = prefix_file(filepath, "trimmed-")
    subprocess.call([
        "ffmpeg",
        "-y",
        "-i", filepath,
        "-t", str(length),
        trimmed_path
    ])
    return trimmed_path


def reverse_and_trim(filepath):
    # Trim and remove original
    print("Trimming")
    trimmed_path = trim_video(filepath)
    remove(filepath)

    # Reverse and remove trimmed
    print("Reversing")
    reversed_path = reverse_video(trimmed_path)
    remove(trimmed_path)

    # return the finished path
    return reversed_path


def get_random_reversed():
    filepath = download_random_youtube_video()
    return reverse_and_trim(filepath)


def get_reversed(query):
    filepath = download_youtube_video(query=query)
    return reverse_and_trim(filepath)


if __name__ == "__main__":
    print(get_random_reversed())
