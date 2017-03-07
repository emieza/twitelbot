# TwiTelBot: a bot to send Tweets to Telegram chats

This software uses several libraries:
- telepot
- tweepy
- redis
- redisworks

## Requirements

It is recommended to use latest PIP installer along with Virtualenv to install libraries and not disturbing your operating system:

    https://pip.pypa.io/en/stable/installing/
    https://virtualenv.pypa.io

You need to also install Redis in your machine. In Debian/Ubuntu would be:
    # apt-get install redis-server


## Installation

Once inside your environment, check the dependencies indicated in requirements.txt
    $ pip install -r < requirements.txt


## Telegram Setup
You need to get a telegram bot TOKEN from BOT FATHER.

Include it in the file tokens.py

## Twitter Setup
You need to create an application and get your credentials.

Include them in the file tokens.py

## Run it!
You can now start your bot with:
    $ python twitelbot.py


## Known issues
It seems that redisworks library misses the final underscores of strings when you stop the client and restart the connection. So, it may seem that you are following successfully a twitter account like "enric_" but after restarting the bot, the library will read "enric" (though in Redis db is still stored ok).

