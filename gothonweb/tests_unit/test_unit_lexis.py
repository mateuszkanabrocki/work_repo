import unittest
from gothonweb.lexis_gothonweb import *

direction = ['north', 'south', 'east', 'west', 'down', 'up', 'left', 'right', 'back']
do = ['go', 'stop', 'kill', 'eat', 'run']
stop = ['the', 'in', 'of', 'from', 'at', 'it', 'a']
noun = ['door', 'bear', 'princess', 'cabinet']

class TestLexis(unittest.TestCase):

    def test_sentence(self):
        sent_test = Sentence(['noun', 'sub'], ['do', 'ver'], ['noun', 'obj'])
        self.assertEqual(sent_test.subject, 'sub')
        self.assertEqual(sent_test.do, 'ver')
        self.assertEqual(sent_test.object, 'obj')

    def test_peek(self):
        peek_test1 = [('noun', 'princess'), ('do', 'eat'), ('error', 'hm')]
        peek_test2 =[]
        self.assertEqual(peek(peek_test1), 'noun')
        self.assertEqual(peek(peek_test2), None)

    def test_match(self):
        match_test1 = [('noun', 'princess'), ('do', 'eat'), ('error', 'hm')]
        match_test2 = []
        match_test3 = [('noun', 'princess'), ('do', 'eat'), ('error', 'hm')]
        self.assertEqual(match(match_test1, 'noun'), ('noun', 'princess'))
        self.assertEqual(match(match_test2, 'noun'), None)
        self.assertEqual(match(match_test3, 'do'), None)

    def test_skip(self):
        skip_test = [('noun', 'princess'), ('noun', 'hat'), ('error', 'hm')]
        self.assertEqual(skip(skip_test, 'error'), skip_test)
        self.assertEqual(skip(skip_test, 'noun'), [('error', 'hm')])

    def test_parse_do(self):
        parse_do_test1 = [('stop', 'The'), ('stop', 'The'), ('do', 'go'), ('error', 'hm')]
        self.assertEqual(parse_do(parse_do_test1), ('do', 'go'))

    def test_parse_object(self):
        parse_object_test1 = [('stop', 'The'), ('number', '2'), ('noun', 'bear'), ('error', 'hm')]
        parse_object_test2 = [('stop', 'The'), ('direction', 'left'), ('error', 'hm')]
        self.assertEqual(parse_object(parse_object_test1), ('noun', 'bear'))
        self.assertEqual(parse_object(parse_object_test2), ('direction', 'left'))

    def test_parse_subject(self):
        parse_object_test1 = [('stop', 'The'), ('stop', 'The'), ('number', '2'), ('noun', 'bear'), ('error', 'hm')]
        parse_object_test2 = [('stop', 'The'), ('do', 'run'), ('error', 'hm')]
        self.assertEqual(parse_subject(parse_object_test1), ('noun', 'bear'))
        self.assertEqual(parse_subject(parse_object_test2), ('noun', 'player'))

    def test_parse_sentence(self):
        parse_sen_test1 = [('stop', 'The'), ('noun', 'bear'), ('do', 'eat'), ('noun', 'princess')]
        parse_sen_test2 = [('stop', 'The'), ('do', 'eat'), ('noun', 'princess')]
        parse_obj1 = parse_sentence(parse_sen_test1)
        parse_obj2 = parse_sentence(parse_sen_test2)
        self.assertEqual(parse_obj1, 'eat princess')
        self.assertEqual(parse_obj2, 'eat princess')
