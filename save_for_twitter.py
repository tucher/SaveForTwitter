#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from twython import Twython

import codecs
import sys
streamWriter = codecs.lookup('utf-8')[-1]
sys.stdout = streamWriter(sys.stdout)

try:
	import Credentials
except Exception, e:
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

	if Credentials != None:
		APP_KEY = Credentials.APP_KEY
		APP_SECRET = Credentials.APP_SECRET
		OAUTH_TOKEN = Credentials.OAUTH_TOKEN
		OAUTH_TOKEN_SECRET = Credentials.OAUTH_TOKEN_SECRET

	if APP_KEY == '':
		print 'You should setup twitter application, and use its Credentials in APP_KEY etc.'
		return

	if OAUTH_TOKEN == '':
		print('no token')

		twitter = Twython(APP_KEY, APP_SECRET)
		auth = twitter.get_authentication_tokens()

		if auth:
			OAUTH_TOKEN = auth['oauth_token']
			OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

			print 'open this url:', auth['auth_url']
			print 'and enter pin:'
			x = input()

			if x:
				twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
				final_step = twitter.get_authorized_tokens(x)

				OAUTH_TOKEN = final_step['oauth_token']
				OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']

				print('OAUTH_TOKEN: ', OAUTH_TOKEN)
				print('OAUTH_TOKEN_SECRET: ', OAUTH_TOKEN_SECRET)
				print('↑ store that data in Credentials.py')
				print 'enter 0:'
				input()

	if OAUTH_TOKEN != '':
		print('tokened')
		return Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def loadTimeline(twitter):
	return twitter.get_user_timeline()

def saveForTwitterTimeline():
	twitter = connectToTwitter()
	if twitter:
		timelineJson = loadTimeline(twitter)
		for j in timelineJson:
			t = j
			for i in j['entities']['urls']:
				a0 = i['indices'][0] / 2
				a1 = i['indices'][1] / 2
				# print t[:a0], '!!!!!!!!!!!!!', t[a1:]
				# print i['indices']
				pass
			print j['id'], j['text'] # j['created_at'], 
		# parsed = parseTimeline(timelineJson)
		# saveToDisk(parsed)

def main():
	saveForTwitterTimeline()

if __name__ == '__main__':
	main()
