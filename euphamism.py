from random import choice
import re

from nltk.corpus import wordnet
from inflect import engine

inflect = engine()

VERBS, NOUNS = (set(), set())

for wordset, kind in [
    (VERBS, wordnet.VERB),
    (NOUNS, wordnet.NOUN),
]:
    for synset in wordnet.all_synsets(kind):
        for lemma in filter(
            lambda l: all((
                not re.search(r'\d', l.name()),
                l.count() > 0,
            )), synset.lemmas()
        ):
            wordset.add(lemma.name().replace('_', ' '))

VERBS, NOUNS = (list(VERBS), list(NOUNS))


def generate():
    verb_words = choice(VERBS).split(' ')
    verb_words[0] = inflect.present_participle(verb_words[0])

    return '{} the {}'.format(
        ' '.join(verb_words), choice(NOUNS)
    )


if __name__ == '__main__':
    for i in xrange(30):
        print generate()
