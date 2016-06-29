import re

import tweepy

from tweet import auth, tweet
from define import define


def strip_tweet_text(text):
    return re.sub(r'(\s+|^)@\S+\b', '', text).strip()


class Listener(tweepy.StreamListener):
    def on_connect(self):
        print 'okay, im listening'

    def on_status(self, status):
        term = strip_tweet_text(status.text)
        definition = define(term)
        tweet(
            term, definition,
            mention=status.user.screen_name,
            in_reply_to_status_id=status.id,
        )

    def on_error(self, error):
        print error
        return True


if __name__ == '__main__':
    listener = Listener()
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=['@urbandictionery'])
