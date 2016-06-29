from nltk import pos_tag


_DT = 'Those among a given set who masturbate.',
DEFS = {
    'CD': 'How many times a day a you masturbate.',
    'DT': _DT,
    'FW': 'Masturbieren.',
    'IN': 'In a position recently masturbated in by.',
    'JJ': 'Masturbatory.',
    'JJR': 'More prone to masturbate.',
    'JJS': 'The most prone to masturbate.',
    'NN': 'Masturbation.',
    'NNS': 'Masturbators.',
    'NNP': 'The Masturbator.',
    'NNPS': 'The Masturbators.',
    'PDT': _DT,
    'PRP': 'That which masturbates.',
    'PRP$': 'Belonging to a masturbator.',
    'RB': 'In a manner reminiscent of masturbation.',
    'RBR': 'More reminiscent of masturbation.',
    'RBS': 'The most reminiscent of masturbation.',
    'UH': 'An exclamation one might use while masturbating.',
    'VB': 'Masturbate.',
    'VBD': 'Masturbated.',
    'VBG': 'Masturbating.',
    'VBN': 'Masturbated.',
    'VBP': 'Masturbate.',
    'VBZ': 'Masturbates.',
}


def define(phrase):
    tag, = [r[1] for r in pos_tag([phrase])]
    return DEFS.get(tag, 'Masturbating.')


if __name__ == '__main__':
    from sys import argv
    from titlecase import titlecase

    for arg in argv[1:]:
        print '{} - {}'.format(titlecase(arg), define(arg))
