import tweepy

from euphamism import get_words, generate
from image import make_image
from secrets import app_key, app_secret, token_key, token_secret


auth = tweepy.OAuthHandler(app_key, app_secret)
auth.set_access_token(token_key, token_secret)
api = tweepy.API(auth)


def tweet(euphamism=None, definition='Masturbating.', mention=None, **kwargs):
    if euphamism is None:
        euphamism = generate(*get_words())
    print(euphamism)
    status = '{} - {}'.format(euphamism, definition)

    if mention is not None:
        status = '@{} {}'.format(mention, status)

    image = make_image(euphamism, definition)
    api.update_with_media(image, status=status, **kwargs)


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        euphamism = None
    elif len(sys.argv) == 2:
        euphamism = sys.argv[1]
    elif len(sys.argv) == 3:
        euphamism, definition = sys.argv[1:]
    else:
        print('too many arguments')
        sys.exit(1)

    tweet(euphamism)
