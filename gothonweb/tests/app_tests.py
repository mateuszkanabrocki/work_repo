from nose.tools import *
from app import app, load_session, save_session
import planisphere
from flask import Flask, session
from os import remove
from os.path import exists

# set TESTING=True - make it easier to debug
app.config['TESTING'] = True
# make requests to the app without running the server
web = app.test_client()

# Note:
# if any test_app# go wrong you should remove
# c:/windows/system32/projects/gothonweb/sessions/test_app#.txt

def test_exist():
    rv = web.get('/', follow_redirects=True)
    assert_equal(rv.status_code, 200) # there is a page

    rv = web.get('/login', follow_redirects=True)
    assert_equal(rv.status_code, 200)

    rv = web.get('/logout', follow_redirects=True)
    assert_equal(rv.status_code, 200)

    # rv = web.get('/nextgame', follow_redirects=True)
    # assert_equal(rv.status_code, 200)

    # rv = web.get('/score', follow_redirects=True)
    # assert_equal(rv.status_code, 200)

    rv = web.get('/game', follow_redirects=True)
    assert_equal(rv.status_code, 200)

    rv = web.get('/hello', follow_redirects=True)
    assert_equal(rv.status_code, 404) # no page

def test_not_logged_in():

    rv = web.get('/', follow_redirects=True)
    assert_in(b"click here to login", rv.data)

def test_log_in():

    rv = web.get('/login', follow_redirects=True)
    assert_in(b"Login", rv.data)

def test_log_in():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_log_in'}
        rv = web.post('/login', follow_redirects=True, data=data)
        assert_in(b"continue", rv.data)
        assert_in(b"log out", rv.data)
        rv = web.get('/logout', follow_redirects=True)
        assert_in(b"click here to login", rv.data)
        remove("c:/windows/system32/projects/gothonweb/sessions/test_log_in.txt")
        rv = web.get('/logout', follow_redirects=True)

def test_app1():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_app1'}
        rv = web.post('/login', follow_redirects=True, data=data)
        rv = web.get('/game', follow_redirects=True)
        assert_in(b"have invaded your ship ", rv.data)
        assert_equal(session.get('room_name'), 'central_corridor')
        remove("c:/windows/system32/projects/gothonweb/sessions/test_app1.txt")
        rv = web.get('/logout', follow_redirects=True) 

def test_app2():
    rv = web.get('/game', follow_redirects=True)
    assert_in(b"You Died", rv.data)
    rv = web.get('/logout', follow_redirects=True)

def test_app3():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_app3'}
        rv = web.post('/login', follow_redirects=True, data=data)
        rv = web.get('/game', follow_redirects=True)
        assert_in(b"Gothons of Planet Percal #25 have invaded your ship ", rv.data)
        data = {'action': 'dodge!'}
        rv = web.post('/game', follow_redirects=True, data=data)
        assert_in(b"Like a world class boxer", rv.data)
        assert_in(b"Play Again?", rv.data)
        assert_in(b"logout", rv.data)
        assert_in(b"score", rv.data)
        remove("c:/windows/system32/projects/gothonweb/sessions/test_app3.txt")
        rv = web.get('/logout', follow_redirects=True)

def test_app4():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_app4'}
        rv = web.post('/login', follow_redirects=True, data=data)
        rv = web.get('/game', follow_redirects=True)
        data = {'action': 'shoot!'}
        rv = web.post('/game', follow_redirects=True, data=data)
        assert_in(b"Quick on the draw you yank", rv.data)
        assert_in(b"Play Again?", rv.data)
        remove("c:/windows/system32/projects/gothonweb/sessions/test_app4.txt")
        rv = web.get('/logout', follow_redirects=True)

def test_app5():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_app5'}
        rv = web.post('/login', follow_redirects=True, data=data)
        rv = web.get('/game', follow_redirects=True)
        data = {'action': 'tell a joke'}
        rv = web.post('/game', follow_redirects=True, data=data)
        assert_in(b"Lucky for you they made you learn", rv.data)
        remove("c:/windows/system32/projects/gothonweb/sessions/test_app5.txt")
        rv = web.get('/logout', follow_redirects=True)

def test_app6():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_app6'}
        rv = web.post('/login', follow_redirects=True, data=data)
        rv = web.get('/game', follow_redirects=True)
        data = {'action': 'tell a joke'}
        rv = web.post('/game', follow_redirects=True, data=data)
        data = {'action': '0132'}
        rv = web.post('/game', follow_redirects=True, data=data)
        assert_in(b"The container clicks open and the seal breaks, letting gas out.", rv.data)
        remove("c:/windows/system32/projects/gothonweb/sessions/test_app6.txt")
        rv = web.get('/logout', follow_redirects=True)

def test_app7():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_app7'}
        rv = web.post('/login', follow_redirects=True, data=data)
        rv = web.get('/game', follow_redirects=True)
        data = {'action': 'tell a joke'}
        rv = web.post('/game', follow_redirects=True, data=data)
        data = {'action': 'wrong_code'}
        rv = web.post('/game', follow_redirects=True, data=data)
        assert_in(b"The lock buzzes one last", rv.data)
        assert_in(b"Play Again?", rv.data)
        remove("c:/windows/system32/projects/gothonweb/sessions/test_app7.txt")
        rv = web.get('/logout', follow_redirects=True)

def test_app8():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_app8'}
        rv = web.post('/login', follow_redirects=True, data=data)
        rv = web.get('/game', follow_redirects=True)
        data = {'action': 'tell a joke'}
        rv = web.post('/game', follow_redirects=True, data=data)
        data = {'action': '0132'}
        rv = web.post('/game', follow_redirects=True, data=data)
        data = {'action': 'slowly place the bomb'}
        rv = web.post('/game', follow_redirects=True, data=data)
        assert_in(b"You point your blaster at the bomb", rv.data)
        remove("c:/windows/system32/projects/gothonweb/sessions/test_app8.txt")
        rv = web.get('/logout', follow_redirects=True)

def test_app9():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_app9'}
        rv = web.post('/login', follow_redirects=True, data=data)
        rv = web.get('/game', follow_redirects=True)
        data = {'action': 'tell a joke'}
        rv = web.post('/game', follow_redirects=True, data=data)
        data = {'action': '0132'}
        rv = web.post('/game', follow_redirects=True, data=data)
        data = {'action': 'throw the bomb'}
        rv = web.post('/game', follow_redirects=True, data=data)
        assert_in(b"In a panic you throw the bomb", rv.data)
        remove("c:/windows/system32/projects/gothonweb/sessions/test_app9.txt")
        rv = web.get('/logout', follow_redirects=True) 

def test_app10():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_app10'}
        rv = web.post('/login', follow_redirects=True, data=data)
        rv = web.get('/game', follow_redirects=True)
        data = {'action': 'tell a joke'}
        rv = web.post('/game', follow_redirects=True, data=data)
        data = {'action': '0132'}
        rv = web.post('/game', follow_redirects=True, data=data)
        data = {'action': 'slowly place the bomb'}
        rv = web.post('/game', follow_redirects=True, data=data)
        data = {'action': '2'}
        rv = web.post('/game', follow_redirects=True, data=data)
        assert_in(b"You won!", rv.data)
        remove("c:/windows/system32/projects/gothonweb/sessions/test_app10.txt")
        rv = web.get('/logout', follow_redirects=True)
    
def test_app11():
    with app.test_client() as web:
        
        # rv = web.get('/logout', follow_redirects=True)
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_app11'}
        rv = web.post('/login', follow_redirects=True, data=data)
        rv = web.get('/game', follow_redirects=True)
        data = {'action': 'tell a joke'}
        rv = web.post('/game', follow_redirects=True, data=data)
        data = {'action': '0132'}
        rv = web.post('/game', follow_redirects=True, data=data)
        data = {'action': 'slowly place the bomb'}
        rv = web.post('/game', follow_redirects=True, data=data)
        data = {'action': 'wrong_pod'}
        rv = web.post('/game', follow_redirects=True, data=data)
        assert_in(b"into jam jelly", rv.data)

        rv = web.get('/score', follow_redirects=True)
        assert_in(b"Current place: wrong_pod", rv.data)
        assert_in(b"You died 1 time", rv.data)
        remove("c:/windows/system32/projects/gothonweb/sessions/test_app11.txt")
        rv = web.get('/logout', follow_redirects=True)

def test_app12():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_app12'}
        rv = web.post('/login', follow_redirects=True, data=data)
        rv = web.get('/game', follow_redirects=True)
        assert_in(b"Gothons of Planet Percal #25 have invaded your ship ", rv.data)
        data = {'action': 'something else'}
        rv = web.post('/game', follow_redirects=True, data=data)
        assert_in(b"have invaded your ship and destroyed", rv.data)
        assert_in(b"logout", rv.data)
        assert_in(b"score", rv.data)

        rv = web.get('/score', follow_redirects=True)
        assert_in(b"Current place:", rv.data)
        remove("c:/windows/system32/projects/gothonweb/sessions/test_app12.txt")
        rv = web.get('/logout', follow_redirects=True)

def test_app13():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_app12'}
        rv = web.post('/login', follow_redirects=True, data=data)
        rv = web.get('/game', follow_redirects=True)
        assert_in(b"Gothons of Planet Percal #25 have invaded your ship ", rv.data)
        data = {'action': 'something else'}
        rv = web.post('/game', follow_redirects=True, data=data)
        assert_in(b"have invaded your ship and destroyed", rv.data)
        assert_in(b"logout", rv.data)
        assert_in(b"score", rv.data)
        remove("c:/windows/system32/projects/gothonweb/sessions/test_app12.txt")
        rv = web.get('/logout', follow_redirects=True)

def test_load_session1():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_load_session1'}
        rv = web.post('/login', follow_redirects=True, data=data)
        load_session('new_user')
        file_exists = exists('c:/windows/system32/projects/gothonweb/sessions/new_user.txt')
        assert file_exists
        remove("c:/windows/system32/projects/gothonweb/sessions/new_user.txt")
        remove("c:/windows/system32/projects/gothonweb/sessions/test_load_session1.txt")
        rv = web.get('/logout', follow_redirects=True)

def test_load_session2():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_load_session2'}
        rv = web.post('/login', follow_redirects=True, data=data)
        load_session('new_user')
        file_name = 'c:/windows/system32/projects/gothonweb/sessions/new_user.txt'
        with open(file_name, "r") as file:
            file_lines = file.readlines()
            print(">>>")
        assert_equal(file_lines[0], 'death_count = 0\n')
        assert_equal(file_lines[1], 'win_count = 0\n')
        assert_equal(file_lines[2], 'room_name = central_corridor')
        remove("c:/windows/system32/projects/gothonweb/sessions/new_user.txt")
        remove("c:/windows/system32/projects/gothonweb/sessions/test_load_session2.txt")
        rv = web.get('/logout', follow_redirects=True)

def test_save_session():
    with app.test_client() as web:
        rv = web.get('/login', follow_redirects=True)
        data = {'username': 'test_save_session'}
        rv = web.post('/login', follow_redirects=True, data=data)
        assert_raises(FileNotFoundError, save_session, 'new_user1', 2, 3, 'central_corridor')
        remove("c:/windows/system32/projects/gothonweb/sessions/test_save_session.txt")
        rv = web.get('/logout', follow_redirects=True)
