from nose.tools import *
# from ex49.parser import *
from lexis_gothonweb import *

direction = ['north', 'south', 'east', 'west', 'down', 'up', 'left', 'right', 'back']
do = ['go', 'stop', 'kill', 'eat', 'run']
stop = ['the', 'in', 'of', 'from', 'at', 'it', 'a']
noun = ['door', 'bear', 'princess', 'cabinet']

def test_sentence():
    sent_test = Sentence(['noun', 'sub'], ['do', 'ver'], ['noun', 'obj'])
    assert_equal(sent_test.subject, 'sub')
    assert_equal(sent_test.do, 'ver')
    assert_equal(sent_test.object, 'obj')

def test_peek():
    peek_test1 = [('noun', 'princess'), ('do', 'eat'), ('error', 'hm')]
    peek_test2 =[]
    assert_equal(peek(peek_test1), 'noun')
    assert_equal(peek(peek_test2), None)

def test_match():
    match_test1 = [('noun', 'princess'), ('do', 'eat'), ('error', 'hm')]
    match_test2 = []
    match_test3 = [('noun', 'princess'), ('do', 'eat'), ('error', 'hm')]
    assert_equal(match(match_test1, 'noun'), ('noun', 'princess'))
    assert_equal(match(match_test2, 'noun'), None)
    assert_equal(match(match_test3, 'do'), None)

def test_skip():
    skip_test = [('noun', 'princess'), ('noun', 'hat'), ('error', 'hm')]
    assert_equal(skip(skip_test, 'error'), skip_test)
    assert_equal(skip(skip_test, 'noun'), [('error', 'hm')])

def test_parse_do():
    parse_do_test1 = [('stop', 'The'), ('stop', 'The'), ('do', 'go'), ('error', 'hm')]
    parse_do_test2 = [('stop', 'The'), ('noun', 'Jeff'), ('error', 'hm')]
    assert_equal(parse_do(parse_do_test1), ('do', 'go'))
    # assert_raises(ParserError, parse_do, parse_do_test2)

def test_parse_object():
    parse_object_test1 = [('stop', 'The'), ('number', '2'), ('noun', 'bear'), ('error', 'hm')]
    parse_object_test2 = [('stop', 'The'), ('direction', 'left'), ('error', 'hm')]
    parse_object_test3 = [('stop', 'The'), ('stop', 'in'), ('do', 'go'), ('error', 'hm')]
    assert_equal(parse_object(parse_object_test1), ('noun', 'bear'))
    assert_equal(parse_object(parse_object_test2), ('direction', 'left'))
    # assert_raises(ParserError, parse_object, parse_object_test3)

def test_parse_subject():
    parse_object_test1 = [('stop', 'The'), ('stop', 'The'), ('number', '2'), ('noun', 'bear'), ('error', 'hm')]
    parse_object_test2 = [('stop', 'The'), ('do', 'run'), ('error', 'hm')]
    parse_object_test3 = [('stop', 'The'), ('stop', 'in'), ('direction', 'right'), ('error', 'hm')]
    assert_equal(parse_subject(parse_object_test1), ('noun', 'bear'))
    assert_equal(parse_subject(parse_object_test2), ('noun', 'player'))
    # assert_raises(ParserError, parse_subject, parse_object_test3)

def test_parse_sentence():
    parse_sen_test1 = [('stop', 'The'), ('noun', 'bear'), ('do', 'eat'), ('noun', 'princess')]
    parse_sen_test2 = [('stop', 'The'), ('do', 'eat'), ('noun', 'princess')]
    parse_obj1 = parse_sentence(parse_sen_test1)
    parse_obj2 = parse_sentence(parse_sen_test2)
    assert_equal(parse_obj1, 'eat princess')
    assert_equal(parse_obj2, 'eat princess')
    # assert_equal(parse_obj1.subject, 'bear')
    # assert_equal(parse_obj1.do, 'eat')
    # assert_equal(parse_obj1.object, 'princess')
    # assert_equal(parse_obj2.subject, 'player')
    # assert_equal(parse_obj2.do, 'eat')
    # assert_equal(parse_obj2.object, 'princess')
