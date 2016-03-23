from subprocess import check_call
from time import sleep
from random import random

MIN_PAUSE = 1 * 60 * 60
MAX_PAUSE = 3 * 60 * 60
DELTA = MAX_PAUSE - MIN_PAUSE

# i dont want to store the entire wordnet corpus in memory at all times on my
# server, so we're just gonna spawn twooters on the (ir)reg

while True:
    sleep(MIN_PAUSE + (random() * DELTA))
    check_call(['python', 'tweet.py'])
