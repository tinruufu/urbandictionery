import os
from random import choice
import re

from inflect import engine
from nltk.corpus import wordnet
import requests
from titlecase import titlecase

inflect = engine()

CACHE_PATH = os.path.join(os.path.dirname(__file__), 'word-cache')
SLURS = requests.get(
    'https://raw.githubusercontent.com/dariusk/wordfilter/'
    'master/lib/badwords.json'
).json()


def populate_cache():
    verbs, nouns = (set(), set())
    for wordset, kind in [
        (verbs, wordnet.VERB),
        (nouns, wordnet.NOUN),
    ]:
        for synset in wordnet.all_synsets(kind):
            for lemma in filter(
                lambda l: all((
                    not re.search(r'\d', l.name()),
                    l.count() > 0,
                )), synset.lemmas()
            ):
                wordset.add(lemma.name().replace('_', ' '))

    os.mkdir(CACHE_PATH)

    for words, filename in [
        (verbs, 'verbs'),
        (nouns, 'nouns'),
    ]:
        with open(os.path.join(CACHE_PATH, filename), 'w') as f:
            f.writelines((u'{}\n'.format(w) for w in words))


def is_slur(word):
    for slur in SLURS:
        if slur in word:
            return True

    return False


def get_words():
    if not os.path.isdir(CACHE_PATH):
        populate_cache()

    return [
        [l.strip()
         for l in open(os.path.join(CACHE_PATH, filename)).readlines()
         if not is_slur(l)]
        for filename in ['verbs', 'nouns']
    ]


def generate(verbs, nouns):
    verb_words = choice(verbs).split(' ')
    verb_words[0] = inflect.present_participle(verb_words[0])

    return titlecase('{} the {}'.format(
        ' '.join(verb_words), choice(nouns)
    ))


if __name__ == '__main__':
    verbs, nouns = get_words()
    for i in xrange(30):
        print generate(verbs, nouns)
