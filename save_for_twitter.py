"""
    The MIT License (MIT)
    Copyright (c) 2014 Marat S.
"""

from twython import Twython

try:
    import Credentials
except Exception:
    Credentials = None

"""
    код, который выкачивает твиты аккаунта через API твиттера,
    выдирает оттуда все ссылки, в том числе на картинки,
    выкачивает и кладёт на диск в виде
    [
        {
            idтвита: N,
            дата: Date,
            другие параметры твита...,
            текст_твита_с_ссылками_заменёнными_на_медиа_айдишники: Text,
            медиа: {
                медиаid1:binaryData,
                медиаid2:binaryData
            }
        },
        {....}
    ]
"""


def connectToTwitter():

    APP_KEY = ''
    APP_SECRET = ''

    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''

    if Credentials is not None:
        APP_KEY = Credentials.APP_KEY
        APP_SECRET = Credentials.APP_SECRET
        OAUTH_TOKEN = Credentials.OAUTH_TOKEN
        OAUTH_TOKEN_SECRET = Credentials.OAUTH_TOKEN_SECRET

    if APP_KEY == '' or OAUTH_TOKEN == '':
        print("You should setup twitter application,"
              "and use its Credentials in APP_KEY etc.")
        return

    return Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def loadTimeline(twitter):
    return twitter.get_user_timeline()


# def replace_url_in_twit_with_id_to_media_id():
def analyseMediaInTwit(text, media):
    indices = _allIndicesOfMedia(text, media)
    print(indices)


def _allIndicesOfMedia(text, media):
    indicesArray = []

    if 'urls' in media:
        a = _indicesOfMedia(text, media['urls'])
        if len(a) > 0:
            indicesArray.append(a)

    if 'media' in media:
        a = _indicesOfMedia(text, media['media'])
        if len(a) > 0:
            indicesArray.append(a)

    reveredUrlIndices = sorted(indicesArray, reverse=True)
    return reveredUrlIndices


def _indicesOfMedia(text, media):
    indicesArray = []
    for mediaUrl in media:
        # urlStarts = mediaUrl['indices'][0]
        # urlEnds   = mediaUrl['indices'][1]
        indicesArray += mediaUrl['indices']

    return indicesArray


def saveForTwitterTimeline():
    twitter = connectToTwitter()
    if twitter:
        timelineJson = None
        try:
            timelineJson = loadTimeline(twitter)
        except Exception:
            print('Credentials are wrong??')
        else:
            for twitMeta in timelineJson:
                if 'entities' in twitMeta:
                    analyseMediaInTwit(twitMeta['text'], twitMeta['entities'])

        # parsed = parseTimeline(timelineJson)
        # saveToDisk(parsed)


def main():
    saveForTwitterTimeline()

if __name__ == '__main__':
    main()
