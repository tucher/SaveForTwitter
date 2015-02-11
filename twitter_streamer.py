from twython import TwythonStreamer
from urllib import request
import base64
import os
import subprocess
import json
"""
скрипт слушает ленту пользователя, переданного через credentials.py,
печатает в консоль дату и текст твита и результат обработки медиа.
Обработка медиа заключается в том, что, если медиа есть,
создаётся каталог с именем id твита, туда кладутся картинки с названиями,
равными base64 от url источника картинки(так для каждой картинки),
создаётся подкаталог с названием равным base64 от url прикреплённой к твиту ссылки,
туда выкачивается полный вариант страницы, со структурой каталогов, соответствующей пути к странице в url 
(и так для каждой ссылки в твите).
"""


class SaverStreamer(TwythonStreamer):

    def on_success(self, data):
        if 'text' in data:
            handle_new_tweet(data)

    def on_error(self, status_code, data):
        print(status_code, data)

try:
    import Credentials
except Exception:
    Credentials = None

printed_keys = ['created_at', 'text']
prefix = 'DownloadedTweets/'


def handle_new_tweet(tweet_data):
    tweet_id = str(tweet_data['id'])
    for key in printed_keys:
        print(key, ': ', tweet_data[key])
    print('')
    if not os.path.exists(prefix + tweet_id):
        os.makedirs(prefix + tweet_id)
    with open(prefix + tweet_id + '/data.json', 'a') as the_file:
        the_file.write(json.dumps(tweet_data, ensure_ascii=False))
    if 'entities' in tweet_data:
        entities = tweet_data['entities']

        if 'urls' in entities:
            if len(entities['urls']) > 0:
                print('Urls:')
            for url_entry in entities['urls']:
                url = url_entry['expanded_url']
                try:
                    subprocess.call(['wget', '-q', '-p', '-k', '-P', prefix + tweet_id + '/' +
                                     base64.b64encode(bytes(url, "utf-8")).decode("ascii") + '/', url])
                    print('Url downloaded: ', url)
                except:
                    print('Cannot download url: ', url)

        if 'media' in entities:
            if len(entities['media']) > 0:
                print('Media:')
            for media in entities['media']:
                if media['type'] == 'photo':
                    media_url = media['media_url_https']
                    try:
                        request.urlretrieve(media_url,
                                            prefix + tweet_id + '/' +
                                            base64.b64encode(
                                                bytes(media_url, "utf-8")).decode("ascii")
                                            + os.path.splitext(media_url)[-1])
                        print('Image downloaded: ', media_url)
                    except:
                        print('Cannot download: ', media_url)
    print('\n\n')


APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

if Credentials is not None:
    APP_KEY = Credentials.APP_KEY
    APP_SECRET = Credentials.APP_SECRET
    OAUTH_TOKEN = Credentials.OAUTH_TOKEN
    OAUTH_TOKEN_SECRET = Credentials.OAUTH_TOKEN_SECRET

    stream = SaverStreamer(
        APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.user(**{'with': 'user'})
else:
    print('No credentials – no tweets')
