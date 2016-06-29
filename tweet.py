import tweepy

from euphamism import get_words, generate
from image import make_image
from secrets import app_key, app_secret, token_key, token_secret


auth = tweepy.OAuthHandler(app_key, app_secret)
auth.set_access_token(token_key, token_secret)
api = tweepy.API(auth)


def tweet(euphamism=None):
    if euphamism is None:
        euphamism = generate(*get_words())
    print euphamism
    status = '{} - Masturbating.'.format(euphamism)

    image = make_image(euphamism, 'Masturbating.')
    api.update_with_media(image, status=status)


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        euphamism = None
    elif len(sys.argv) == 2:
        euphamism = sys.argv[1]
    else:
        print 'too many arguments'
        sys.exit(1)

    tweet(euphamism)
