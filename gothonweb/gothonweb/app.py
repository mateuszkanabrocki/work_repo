from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
from flask import make_response
from os.path import exists
from shutil import copyfile

import planisphere
import lexis


app = Flask(__name__)


def load_session(username):
    if session.get('game'):
        file_name = f"sessions/{username}_{session.get('game')}.txt"
    else:
        session['game'] = 'gothonweb'
        file_name = f"sessions/{username}_{session.get('game')}.txt"
    user_exists = exists(file_name)
    # create a user cookies file
    if not user_exists:
        with open(file_name, "w") as file:
            file.write('death_count = 0\nwin_count = 0\nroom_name = start_place')
    # load session cookies from the file
    with open(file_name, "r") as file:
        session['death_count'] = int(file.readline().strip().strip('death_count = '))
        session['win_count'] = int(file.readline().strip().strip('win_count = '))
        session['room_name'] = file.readline().strip().replace('room_name = ', '')


def save_session(username, game, death_count, win_count, room_name):
    # read the session file data
    try:
        with open(f"sessions/{username}_{game}.txt", "r") as file:
            line_list = [file.readline(), file.readline(), file.readline()]
            line_list[0] = f"death_count = {death_count}\n"
            line_list[1] = f"win_count = {win_count}\n"
            line_list[2] = f"room_name = {room_name}"
            new_lines = ''.join(line_list)
        # make a new session file
        with open(f"sessions/{username}_{game}.txt", "w") as file:
            file.write(new_lines)
    except:
        load_session(session['username'])


@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        load_session(username)
        return render_template("logged_in.html", username=username)
    return render_template("not_logged_in.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template("log_in.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/nextgame')
def nextgame():
    # assign the session[room_name] start value
    save_session(session['username'], session['game'], session['death_count'],
                 session['win_count'], 'start_place')
    return redirect(url_for('index'))


@app.route('/score')
def score():
    death_count = session['death_count']
    win_count = session['win_count']
    game = session['game']
    room = room = planisphere.load_room(session['room_name'])
    return render_template("score.html", death_count=death_count,
                           win_count=win_count, room=room, game=game)


@app.route('/choose_a_game')
def choose_a_game():
    return render_template("choose_a_game.html")


@app.route('/change_a_game', methods=['GET', 'POST'])
def change_a_game():
    # load a map(planisphere)
    game_name = request.form.get('game_name')
    session['game'] = game_name
    print('session[game]', session['game'])
    game_file_name = f"planisphere_{game_name}.py"
    game_file_name = game_file_name.replace(" ", "")

    lexis_file_name = f"lexis_{game_name}.py"
    lexis_file_name = lexis_file_name.replace(" ", "")
    print('game_file_name', game_file_name)
    print('lexis_file_name', lexis_file_name)

    try:
        copyfile(game_file_name, 'planisphere.py')
        copyfile(lexis_file_name, 'lexis.py')
    except:
        return render_template("choose_a_game.html")

    session['room_name'] = 'start_place'
    room = planisphere.load_room(session['room_name'])
    return render_template("changed_a_game.html", room=room)


@app.route("/game", methods=['GET', 'POST'])
def game():
    room_name = session.get('room_name')
    # by default, the Flask route responds to the GET requests
    if request.method == "GET":
        if room_name:
            room = planisphere.load_room(session['room_name'])
            # if user failed
            if room.name in 'Death':
                session['death_count'] += 1
            # if user won
            elif room.name in 'Happy Ending':
                session['win_count'] += 1
            return render_template("show_room.html", room=room)
        # if user starts from '/game' instead of from '/'and has no account
        else:
            return render_template("you_died.html")
    else:
        action = request.form.get('action')
        if session['room_name'] and action:
            room = planisphere.load_room(session['room_name'])
            # get next room
            next_room = room.go(action)
            if not next_room:
                try:
                    action = lexis.parse_sentence(lexis.scan(action))
                    next_room = room.go(action)
                except:
                    pass
            if not next_room:
                # save current room name
                session['room_name'] = planisphere.name_room(room)
            else:
                # save next room name
                session['room_name'] = planisphere.name_room(next_room)

        save_session(session['username'], session['game'],
                     session['death_count'], session['win_count'],
                     session['room_name'])

        return redirect(url_for("game"))


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# module is run directly (not imported)
if __name__ == "__main__":
    # only for development server - for changing a game functionality
    app.run(debug=True)
