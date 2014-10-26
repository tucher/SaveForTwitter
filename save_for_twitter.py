#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from twython import Twython

"""
	код, который выкачивает твиты аккаунта через API твиттера, 
	выдирает оттуда все ссылки, в том числе на картинки, 
	выкачивает и кладёт на диск в виде 
	[
		{
			idтвита:N, 
			дата:Date, 
			другие параметры твита..., 
			текст_твита_с_ссылками_заменёнными_на_ медиа_айдишники: Text,
			медиа:{
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
				print('store that ↑ data')
				print 'enter 0:'
				input()
	
	if OAUTH_TOKEN != '':
		print('tokened')

		twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
		return twitter

def loadTimeline(t):
	timeline = t.get_user_timeline()
	return timeline

def saveForTwitterTimeline():
	twitter = connectToTwitter()
	if twitter:
		timelineJson = loadTimeline(twitter)
		# print(timelineJson[0])
		for j in timelineJson:
			print j['id'], j['created_at'], j['text']
		# parsed = parseTimeline(timelineJson)
		# saveToDisk(parsed)

def main():
	saveForTwitterTimeline()

if __name__ == '__main__':
	main()
