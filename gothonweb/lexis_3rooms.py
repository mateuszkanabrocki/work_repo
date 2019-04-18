# direction = ['north', 'south', 'east', 'west', 'down', 'up', 'left', 'right', 'back']
# do = ['go', 'stop', 'kill', 'eat', 'run']
# stop = ['the', 'in', 'of', 'from', 'at', 'it', 'a']
# noun = ['door', 'bear', 'princess', 'cabinet']
from planisphere_gothonweb import direction, do, stop, noun
# 3rooms
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
    print(">>>>", sentence_cleaned)
    for i in '.,;:?!':
        sentence_cleaned = sentence_cleaned.replace(i, '')
        print(">>>>", sentence_cleaned)
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
    print(">>>> lexicon:", lexicon)
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
    # in case there is a stop mark following th enumber
    skip(word_list, 'stop')
    skip(word_list, 'number')
    skip(word_list, 'stop')
    skip(word_list, 'error')

    if peek(word_list) == 'do':
        return match(word_list, 'do')
    # else:
    #     raise ParserError("Expected a do next. Don't know the word.")

def parse_object(word_list):
    skip(word_list, 'stop')
    skip(word_list, 'number')
    skip(word_list, 'error')
    next_word = peek(word_list)

    if next_word == 'noun':
        return match(word_list, 'noun')
    elif next_word == 'direction':
        return match(word_list, 'direction')
    # else:
    #     raise ParserError("Expected a noun or direction next. Don't know the word.")

def parse_subject(word_list):
    skip(word_list, 'stop')
    skip(word_list, 'number')
    skip(word_list, 'error')
    next_word = peek(word_list)

    if next_word == 'noun':
        return match(word_list, 'noun')
    elif next_word == 'do':
        return ('noun', 'player')
    # else:
    #     raise ParserError("Expected a do next. Don't know the word.")

def parse_sentence(word_list):
    subj = parse_subject(word_list)
    do = parse_do(word_list)
    obj = parse_object(word_list)

    if obj is None:
        sentence_parsed = f'{do[1]}'
        return sentence_parsed
    else:
        sentence_parsed = f'{do[1]} {obj[1]}'
        return sentence_parsed
        

# def parse_sentence(word_list):
#     print(">>>i'm in parse sentence function")
#     subj = parse_subject(word_list)
#     print(">>>>subj", subj)
#     do = parse_do(word_list)
#     print(">>>>do", do)
#     obj = parse_object(word_list)
#     print(">>>>obj", obj)
#     obj=('noun', 'princess')
#     sentence_object_parsed = Sentence(subj, do, obj) # here the function returns None, whyy? :o
#     print(sentensce_object_parsed.do, sentence_object_parsed.obj)
#     if sentence_object_parsed.obj is None:
#         print(">>>> if")
#         sentence_parsed = f'{sentence_object_parsed.do}'
#         print(">>>>", sentence_parsed)
#         return sentence_parsed
#     else:
#         print(">>>> else")
#         sentence_parsed = f'{sentence_object_parsed.do} {sentence_object_parsed.obj}'
#         print(">>>>", sentence_parsed)
#         return sentence_parsed
        


# sen = parse_sentence(ex49_lexicon.scan('the bear run south?'))
# print(sen.subject, sen.do, sen.object)


# input_obj = parse_sentence(scan(input("Type the sentence:> ")))
# print(input_obj.subject, input_obj.do, input_obj.object)