import pytest
from app import app, load_session, save_session
import planisphere_gothonweb
from flask import Flask, session
from os.path import exists
from shutil import copyfile
from testing_functions import delete_file


# make it easier to debug
app.config['TESTING'] = True
# make requests to the app without running the server
web = app.test_client()

# NOSETESTS SETUP DATA
windows_gothonweb_path = 'c:/windows/system32/projects'
linux_gothonweb_path = '/home/mateusz/python_repo/working_repo'
gothonweb_path = linux_gothonweb_path  # change depending on gothonweb directory location on your PC

# In case of nosetests errors try to run nosetests twice
# it will make a default game setup so tests can run properly.


def setup_module(module):
    copyfile('planisphere_gothonweb.py', 'planisphere.py')
    try:
            delete_file('new_user', gothonweb_path)
            delete_file('test_gothonweb', gothonweb_path)
    except:
            pass


def test_exist():
    rv = web.get('/', follow_redirects=True)
    assert rv.status_code == 200  # 200-the page exists

    rv = web.get('/login', follow_redirects=True)
    assert rv.status_code == 200

    rv = web.get('/logout', follow_redirects=True)
    assert rv.status_code, 200

    # rv = web.get('/nextgame', follow_redirects=True)
    # assert rv.status_code == 200

    # rv = web.get('/score', follow_redirects=True)
    # assert rv.status_code == 00

    rv = web.get('/game', follow_redirects=True)
    assert rv.status_code == 200

    rv = web.get('/hello', follow_redirects=True)
    assert rv.status_code == 404 # 404-the page doesn't exist

def test_not_logged_in():
    rv = web.get('/', follow_redirects=True)
    assert b"click here to login" in rv.data

def test_log_in():
    rv = web.get('/login', follow_redirects=True)
    assert b"Login" in rv.data

def test_log_in2():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            assert b"continue" in rv.data
            assert b"log out" in rv.data
            rv = web.get('/logout', follow_redirects=True)
            assert b"click here to login" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def test_app1():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            rv = web.get('/game', follow_redirects=True)
            assert b"have invaded your ship " in rv.data
            assert session.get('room_name') == 'start_place'

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True) 

def test_app2():
    rv = web.get('/game', follow_redirects=True)
    assert b"You Died" in rv.data
    rv = web.get('/logout', follow_redirects=True)

def test_app3():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            rv = web.get('/game', follow_redirects=True)
            assert b"Gothons of Planet Percal #25 have invaded your ship " in rv.data
            data = {'action': 'dodge'}
            rv = web.post('/game', follow_redirects=True, data=data)
            assert b"Like a world class boxer" in rv.data
            assert b"Play Again?" in rv.data
            assert b"logout" in rv.data
            assert b"score" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_app4():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            rv = web.get('/game', follow_redirects=True)
            data = {'action': 'shoot'}
            rv = web.post('/game', follow_redirects=True, data=data)
            assert b"Quick on the draw you yank" in rv.data
            assert b"Play Again?" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_app5():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            rv = web.get('/game', follow_redirects=True)
            data = {'action': 'tell a joke'}
            rv = web.post('/game', follow_redirects=True, data=data)
            assert b"Lucky for you they made you learn" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_app6():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            rv = web.get('/game', follow_redirects=True)
            data = {'action': 'tell a joke'}
            rv = web.post('/game', follow_redirects=True, data=data)
            data = {'action': 'right_code'}
            rv = web.post('/game', follow_redirects=True, data=data)
            assert b"The container clicks open and the seal breaks, letting gas out." in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_app7():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            rv = web.get('/game', follow_redirects=True)
            data = {'action': 'tell a joke'}
            rv = web.post('/game', follow_redirects=True, data=data)
            data = {'action': 'wrong_code'}
            rv = web.post('/game', follow_redirects=True, data=data)
            assert b"The lock buzzes one last" in rv.data
            assert b"Play Again?" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_app8():
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
            assert b"You point your blaster at the bomb" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_app9():
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
            assert b"In a panic you throw the bomb" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True) 

def  test_app10():
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
            assert b"You won!" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_app11():
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
            assert b"into jam jelly" in rv.data

            rv = web.get('/score', follow_redirects=True)
            assert b"Current place: Death" in rv.data
            assert b"You died 1 time" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_app12():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            rv = web.get('/game', follow_redirects=True)
            assert b"Gothons of Planet Percal #25 have invaded your ship " in rv.data
            data = {'action': 'something else'}
            rv = web.post('/game', follow_redirects=True, data=data)
            assert b"have invaded your ship and destroyed" in rv.data
            assert b"logout" in rv.data
            assert b"score" in rv.data

            rv = web.get('/score', follow_redirects=True)
            assert b"Current place:" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_app13():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            rv = web.get('/game', follow_redirects=True)
            assert b"Gothons of Planet Percal #25 have invaded your ship " in rv.data
            data = {'action': 'something else'}
            rv = web.post('/game', follow_redirects=True, data=data)
            assert b"have invaded your ship and destroyed" in rv.data
            assert b"logout" in rv.data
            assert b"score" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_load_session1():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            load_session('new_user')
            file_exists = exists(f'{gothonweb_path}/gothonweb/sessions/new_user_gothonweb.txt')
            assert file_exists

            delete_file('new_user_gothonweb', gothonweb_path)
            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_load_session2():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            load_session('new_user')
            file_name = f'{gothonweb_path}/gothonweb/sessions/new_user_gothonweb.txt'
            with open(file_name, "r") as file:
                    file_lines = file.readlines()
                    assert file_lines[0] == 'death_count = 0\n'
                    assert file_lines[1] == 'win_count = 0\n'
                    assert file_lines[2] == 'room_name = start_place'

            delete_file('new_user_gothonweb', gothonweb_path)
            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_lexis1():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            rv = web.get('/game', follow_redirects=True)
            assert b"Gothons of Planet Percal #25 have invaded your ship " in rv.data
            data = {'action': 'dodge'}
            rv = web.post('/game', follow_redirects=True, data=data)
            assert b"Like a world class boxer" in rv.data
            assert b"Play Again?" in rv.data
            assert b"logout" in rv.data
            assert b"score" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_lexis2():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            rv = web.get('/game', follow_redirects=True)
            assert b"Gothons of Planet Percal #25 have invaded your ship " in rv.data
            data = {'action': 'kill him!'}
            rv = web.post('/game', follow_redirects=True, data=data)
            assert b"Quick on the draw you yank" in rv.data
            assert b"Play Again?" in rv.data
            assert b"logout" in rv.data
            assert b"score" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)

def  test_lexis3():
    with app.test_client() as web:
            rv = web.get('/login', follow_redirects=True)
            data = {'username': 'test'}
            rv = web.post('/login', follow_redirects=True, data=data)
            rv = web.get('/game', follow_redirects=True)
            data = {'action': 'tell him a good joke!'}
            rv = web.post('/game', follow_redirects=True, data=data)
            assert b"Lucky for you they made you learn" in rv.data

            delete_file('test_gothonweb', gothonweb_path)
            rv = web.get('/logout', follow_redirects=True)
