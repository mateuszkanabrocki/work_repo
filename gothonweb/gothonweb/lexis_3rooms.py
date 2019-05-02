#lexis 3rooms

from planisphere_gothonweb import direction, do, stop, noun


class ParserError(Exception):
    pass


class Sentence(object):

    def __init__(self, subject, do, obj):
        # take ('noun','princess') return 'princess'
        self.subject = subject[1]
        self.do = do[1]
        self.object = obj[1]


def scan(sentence):
    sentence_cleaned = sentence.strip()
    for i in '.,;:?!':
        sentence_cleaned = sentence_cleaned.replace(i, '')
    words_lowercase = sentence_cleaned.lower().split()
    words = sentence_cleaned.split()
    lexicon = []
    adress = -1

    for i in words_lowercase:
        adress += 1
        if i in direction:
            lexicon.append(('direction', i))
        elif i in do:
            lexicon.append(('do', i))
        elif i in stop:
            lexicon.append(('stop', i))
        elif i in noun:
            lexicon.append(('noun', i))
        else:
            try:
                lexicon.append(('number', int(i)))
            except ValueError:
                lexicon.append(('error', words[adress]))
    return lexicon


# take ('noun','princess') return 'noun'
def peek(word_list):
    if word_list:
        word = word_list[0]
        return word[0]
    else:
        return None


# take ('noun','princess') and 'noun' pop and return ('noun','princess')
def match(word_list, expecting):
    if word_list:
        word = word_list.pop(0)

        if word[0] == expecting:
            return word
        else:
            return None
    else:
        return None


def skip(word_list, word_type):
    while peek(word_list) == word_type:
        match(word_list, word_type)
    return word_list


def parse_do(word_list):
    # skip stop marks, numbers and again stop marks
    # in case there is a stop mark following th nuumber
    skip(word_list, 'stop')
    skip(word_list, 'number')
    skip(word_list, 'stop')
    skip(word_list, 'error')

    if peek(word_list) == 'do':
        return match(word_list, 'do')


def parse_object(word_list):
    skip(word_list, 'stop')
    skip(word_list, 'number')
    skip(word_list, 'error')
    next_word = peek(word_list)

    if next_word == 'noun':
        return match(word_list, 'noun')
    elif next_word == 'direction':
        return match(word_list, 'direction')


def parse_subject(word_list):
    skip(word_list, 'stop')
    skip(word_list, 'number')
    skip(word_list, 'error')
    next_word = peek(word_list)

    if next_word == 'noun':
        return match(word_list, 'noun')
    elif next_word == 'do':
        return ('noun', 'player')


def parse_sentence(word_list):
    do = parse_do(word_list)
    obj = parse_object(word_list)

    if obj is None:
        sentence_parsed = f'{do[1]}'
        return sentence_parsed
    else:
        sentence_parsed = f'{do[1]} {obj[1]}'
        return sentence_parsed
