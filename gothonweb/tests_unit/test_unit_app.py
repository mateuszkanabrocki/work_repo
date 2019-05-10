import sys
import os
this_module = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_module, '../gothonweb/'))

import unittest
from app import app, load_session, save_session
import planisphere_gothonweb
from planisphere_gothonweb import planisphere_gothonweb_path
from flask import Flask, session
from os.path import exists
from shutil import copyfile
from testing_functions import delete_file


# make it easier to debug
app.config['TESTING'] = True
# make requests to the app without running the server
web = app.test_client()

gothonweb_path = os.path.join(os.path.dirname(__file__), '../..')
planisphere_path = os.path.join(os.path.dirname(__file__), '../gothonweb/planisphere')


class TestApp(unittest.TestCase):

    def setUp(self):
        copyfile(planisphere_gothonweb_path, planisphere_path)
        try:
            delete_file('new_user', gothonweb_path)
            delete_file('test_gothonweb', gothonweb_path)
        except:
            pass

    def tearDown(self):
        pass

    def test_exist(self):
        rv = web.get('/', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)  # 200-the page exists

        rv = web.get('/login', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

        rv = web.get('/logout', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

        # rv = web.get('/nextgame', follow_redirects=True)
        # self.assertEqual(rv.status_code, 200)

        # rv = web.get('/score', follow_redirects=True)
        # self.assertEqual(rv.status_code, 200)

        rv = web.get('/game', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

        rv = web.get('/hello', follow_redirects=True)
        self.assertEqual(rv.status_code, 404) # 404-the page doesn't exist

    def test_not_logged_in(self):
        rv = web.get('/', follow_redirects=True)
        self.assertIn(b"click here to login", rv.data)

    def test_log_in(self):
        rv = web.get('/login', follow_redirects=True)
        self.assertIn(b"Login", rv.data)

    def test_log_in2(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                self.assertIn(b"continue", rv.data)
                self.assertIn(b"log out", rv.data)
                rv = web.get('/logout', follow_redirects=True)
                self.assertIn(b"click here to login", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def test_app1(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                self.assertIn(b"have invaded your ship ", rv.data)
                self.assertEqual(session.get('room_name'), 'start_place')

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True) 

    def test_app2(self):
        rv = web.get('/game', follow_redirects=True)
        self.assertIn(b"You Died", rv.data)
        rv = web.get('/logout', follow_redirects=True)

    def test_app3(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                self.assertIn(b"Gothons of Planet Percal #25 have invaded your ship ", rv.data)
                data = {'action': 'dodge'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"Like a world class boxer", rv.data)
                self.assertIn(b"Play Again?", rv.data)
                self.assertIn(b"logout", rv.data)
                self.assertIn(b"score", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_app4(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                data = {'action': 'shoot'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"Quick on the draw you yank", rv.data)
                self.assertIn(b"Play Again?", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_app5(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                data = {'action': 'tell a joke'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"Lucky for you they made you learn", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_app6(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                data = {'action': 'tell a joke'}
                rv = web.post('/game', follow_redirects=True, data=data)
                data = {'action': 'right_code'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"The container clicks open and the seal breaks, letting gas out.", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_app7(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                data = {'action': 'tell a joke'}
                rv = web.post('/game', follow_redirects=True, data=data)
                data = {'action': 'wrong_code'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"The lock buzzes one last", rv.data)
                self.assertIn(b"Play Again?", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_app8(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                data = {'action': 'tell a joke'}
                rv = web.post('/game', follow_redirects=True, data=data)
                data = {'action': 'right_code'}
                rv = web.post('/game', follow_redirects=True, data=data)
                data = {'action': 'slowly place the bomb'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"You point your blaster at the bomb", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_app9(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                data = {'action': 'tell a joke'}
                rv = web.post('/game', follow_redirects=True, data=data)
                data = {'action': 'right_code'}
                rv = web.post('/game', follow_redirects=True, data=data)
                data = {'action': 'throw the bomb'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"In a panic you throw the bomb", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True) 

    def  test_app10(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                data = {'action': 'tell a joke'}
                rv = web.post('/game', follow_redirects=True, data=data)
                data = {'action': 'right_code'}
                rv = web.post('/game', follow_redirects=True, data=data)
                data = {'action': 'slowly place the bomb'}
                rv = web.post('/game', follow_redirects=True, data=data)
                data = {'action': 'right_pod'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"You won!", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_app11(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                data = {'action': 'tell a joke'}
                rv = web.post('/game', follow_redirects=True, data=data)
                data = {'action': 'right_code'}
                rv = web.post('/game', follow_redirects=True, data=data)
                data = {'action': 'slowly place the bomb'}
                rv = web.post('/game', follow_redirects=True, data=data)
                data = {'action': 'wrong_pod'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"into jam jelly", rv.data)

                rv = web.get('/score', follow_redirects=True)
                self.assertIn(b"Current place: Death", rv.data)
                self.assertIn(b"You died 1 time", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_app12(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                self.assertIn(b"Gothons of Planet Percal #25 have invaded your ship ", rv.data)
                data = {'action': 'something else'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"have invaded your ship and destroyed", rv.data)
                self.assertIn(b"logout", rv.data)
                self.assertIn(b"score", rv.data)

                rv = web.get('/score', follow_redirects=True)
                self.assertIn(b"Current place:", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_app13(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                self.assertIn(b"Gothons of Planet Percal #25 have invaded your ship ", rv.data)
                data = {'action': 'something else'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"have invaded your ship and destroyed", rv.data)
                self.assertIn(b"logout", rv.data)
                self.assertIn(b"score", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_load_session1(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                load_session('new_user')
                file_exists = exists(f'{gothonweb_path}/gothonweb/gothonweb/sessions/new_user_gothonweb.txt')
                assert file_exists
                delete_file('new_user_gothonweb', gothonweb_path)
                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_load_session2(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                load_session('new_user')
                file_name = f'{gothonweb_path}/gothonweb/gothonweb/sessions/new_user_gothonweb.txt'
                with open(file_name, "r") as file:
                        file_lines = file.readlines()
                        self.assertEqual(file_lines[0], 'death_count = 0\n')
                        self.assertEqual(file_lines[1], 'win_count = 0\n')
                        self.assertEqual(file_lines[2], 'room_name = start_place')

                delete_file('new_user_gothonweb', gothonweb_path)
                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_lexis1(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                self.assertIn(b"Gothons of Planet Percal #25 have invaded your ship ", rv.data)
                data = {'action': 'dodge'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"Like a world class boxer", rv.data)
                self.assertIn(b"Play Again?", rv.data)
                self.assertIn(b"logout", rv.data)
                self.assertIn(b"score", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_lexis2(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                self.assertIn(b"Gothons of Planet Percal #25 have invaded your ship ", rv.data)
                data = {'action': 'kill him!'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"Quick on the draw you yank", rv.data)
                self.assertIn(b"Play Again?", rv.data)
                self.assertIn(b"logout", rv.data)
                self.assertIn(b"score", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)

    def  test_lexis3(self):
        with app.test_client() as web:
                rv = web.get('/login', follow_redirects=True)
                data = {'username': 'test'}
                rv = web.post('/login', follow_redirects=True, data=data)
                rv = web.get('/game', follow_redirects=True)
                data = {'action': 'tell him a good joke!'}
                rv = web.post('/game', follow_redirects=True, data=data)
                self.assertIn(b"Lucky for you they made you learn", rv.data)

                delete_file('test_gothonweb', gothonweb_path)
                rv = web.get('/logout', follow_redirects=True)
