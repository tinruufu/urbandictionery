import tweepy

from euphamism import generate
from image import make_image
from secrets import app_key, app_secret, token_key, token_secret


def tweet():
    euphamism = generate()
    print euphamism
    status = '{} - masturbating'.format(euphamism)

    auth = tweepy.OAuthHandler(app_key, app_secret)
    auth.set_access_token(token_key, token_secret)
    image = make_image(euphamism, 'masturbating')
    tweepy.API(auth).update_with_media(image, status=status)


if __name__ == '__main__':
    tweet()
