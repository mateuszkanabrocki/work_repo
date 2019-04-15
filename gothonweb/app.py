from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
from flask import make_response
from os.path import exists
import planisphere


app = Flask(__name__)


def load_session(username):

    file_name = f"sessions/{username}.txt"
    user_exists = exists(file_name)

    # create a user cookies file
    if not user_exists:
        with open(file_name, "w") as file:
            file.write('death_count = 0\nwin_count = 0\nroom_name = central_corridor')

    # load session cookies from the file
    with open(file_name, "r") as file:
        session['death_count'] = int(file.readline().strip().strip('death_count = '))
        session['win_count'] = int(file.readline().strip().strip('win_count = '))
        session['room_name'] = file.readline().strip().replace('room_name = ', '')

def save_session(username, death_count, win_count, room_name):

    # read the session file data
    with open(f"sessions/{username}.txt","r") as file:
        line_list = [file.readline(), file.readline(), file.readline()]
        line_list[0] = f"death_count = {death_count}\n"
        line_list[1] = f"win_count = {win_count}\n"
        line_list[2] = f"room_name = {room_name}"
        new_lines = ''.join(line_list)

    # make a new session file    
    with open(f"sessions/{username}.txt","w") as file:
        file.write(new_lines)


@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        load_session(session.get('username'))
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
    # assign the session[room_name] value
    save_session(session['username'], session['death_count'], session['win_count'], 'central_corridor')
    return redirect(url_for('index'))

@app.route('/score')
def score():
    death_count = session['death_count']
    win_count = session['win_count']
    room_name = session['room_name']
    return render_template("score.html", death_count=death_count,
                           win_count=win_count, room_name=room_name)
    
@app.route("/game", methods=['GET', 'POST'])
def game():
    room_name = session.get('room_name')
    # by default, the Flask route responds to the GET requests
    if request.method == "GET":
        if room_name:
            # get a room object
            room = planisphere.load_room(room_name)
            # if user died
            if room.name in 'Death':
                session['death_count'] += 1
            # if user won
            elif room.name in 'Happy Ending':
                session['win_count'] += 1
            return render_template("show_room.html", room=room)
        #if user starts from '/game' not 'from '/'and with  no account
        else:
            return render_template("you_died.html")
    else:
        action = request.form.get('action')
        if room_name and action:
            # get a room object
            room = planisphere.load_room(room_name)
            # get next room object
            next_room = room.go(action)

            if not next_room:
                # save current room name
                session['room_name'] = planisphere.name_room(room)
            else:
                # save next room name
                session['room_name'] = planisphere.name_room(next_room)

        session_data = [session['username'], session['death_count'], session['win_count'], session['room_name']]
        save_session(session['username'], session['death_count'], session['win_count'], session['room_name'])

        return redirect(url_for("game"))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# module is run directly (not imported)
if __name__ == "__main__":
    app.run()
    