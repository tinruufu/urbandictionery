from random import choice
import re

from nltk.corpus import wordnet
from inflect import engine

inflect = engine()


def prepare():
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

    return list(verbs), list(nouns)


def generate(verbs, nouns):
    verb_words = choice(verbs).split(' ')
    verb_words[0] = inflect.present_participle(verb_words[0])

    return '{} the {}'.format(
        ' '.join(verb_words), choice(nouns)
    )


if __name__ == '__main__':
    verbs, nouns = prepare()
    for i in xrange(30):
        print generate(verbs, nouns)
