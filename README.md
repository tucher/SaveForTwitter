SaveForTwitter
==============
> код, который выкачивает твиты аккаунта через API твиттера, 
> выдирает оттуда все ссылки, в том числе на картинки, 
> выкачивает и кладёт на диск 


Чтобы запустить, нужно создать рядом с twitter_streamer.py файл Credentials.py в виде
```
PREFIX = '/etc/nginx/html/twitter_archive/'
APP_KEY = 'APP_KEY'
APP_SECRET = 'APP_SECRET'
OAUTH_TOKEN = 'OAUTH_TOKEN'
OAUTH_TOKEN_SECRET = 'OAUTH_TOKEN_SECRET'
```


Токены получать на сайте твиттера.
