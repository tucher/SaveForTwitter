from twython import TwythonStreamer
from urllib import request
import base64
import os
import subprocess
import json
import sys
import datetime
import hashlib
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
prefix = Credentials.PREFIX


def handle_entities(entities, tweet_id):
    if 'urls' in entities:
        if len(entities['urls']) > 0:
            print('Urls:')
        for url_entry in entities['urls']:
            url = url_entry['expanded_url']
            try:
                subprocess.call(['wget', '-q', '--user-agent="User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12"', '-e', 'robots=off', '--wait=0.1', '--random-wait', '-E', '-H', '-k', '-K', '-p', '-np', '-l 1', '-P', prefix + tweet_id + '/' +
                                 hashlib.md5(url.encode()).hexdigest() + '/', url])
                print('Url downloaded: ', url)
            except:
                print('Cannot download url: ', url)

    if 'media' in entities:
        if len(entities['media']) > 0:
            print('Media:')
        for media in entities['media']:
            if 'type' in media and media['type'] == 'photo':
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


def handle_new_tweet(tweet_data):
    # 2015-02-11 15:35:10 +0000
    try:
        date = datetime.datetime.strptime(
            tweet_data['created_at'], '%Y-%m-%d %H:%M:%S %z')
    except:
        date = datetime.datetime.strptime(
            tweet_data['created_at'], '%a %b %d %H:%M:%S %z %Y')
    tweet_id = date.strftime('%Y-%m-%d_%H.%M.%S') + \
        "___" + str(tweet_data['id'])
    for key in printed_keys:
        print(key, ': ', tweet_data[key])
    print('')
    if not os.path.exists(prefix + tweet_id):
        os.makedirs(prefix + tweet_id)
    with open(prefix + tweet_id + '/data.json', 'a') as the_file:
        the_file.write(json.dumps(tweet_data, ensure_ascii=False))
    if 'entities' in tweet_data:
        handle_entities(tweet_data['entities'], tweet_id)
    if 'quoted_status' in tweet_data:
        q = tweet_data['quoted_status']
        if 'entities' in q:
            print(q['entities'])
            handle_entities(q['entities'], tweet_id)
    print('\n\n')


# trying to parse local data if present

if len(sys.argv) > 1:
    import execjs
    arch_dir_path = sys.argv[1]
    print("Processing twitter archive: ", arch_dir_path)
    with open(arch_dir_path + '/data/js/tweet_index.js', 'r') as the_file:
        tw_index_str = the_file.read()
        ctx = execjs.compile(tw_index_str)
        tweet_index = ctx.eval("tweet_index")
        for meta_data in tweet_index:
            file_name = arch_dir_path + '/' + meta_data['file_name']
            var_name = meta_data['var_name']
            with open(file_name, 'r') as m_file:
                tw_a_str = m_file.read()
                ctx_m = execjs.compile(
                    'var Grailbird = {}; Grailbird["data"] = {};' + tw_a_str)
                tw_list = ctx_m.eval("Grailbird.data." + var_name)
                for tweet in tw_list:
                    handle_new_tweet(tweet)


else:
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
