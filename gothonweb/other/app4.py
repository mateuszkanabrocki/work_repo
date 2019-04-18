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

def save_room(username, death_count, win_count, room_name):

    with open(f"sessions/{username}.txt","r") as file:
        line_list = [file.readline(), file.readline(), file.readline()]
        
        # if more parameters in the file, use:
        # line_list = [file.readline()]
        # for i in (1,2):
        #     line_list.append(file.readline())

        line_list[0] = f"death_count = {death_count}\n"
        line_list[1] = f"win_count = {win_count}\n"
        line_list[2] = f"room_name = {room_name}"
        # now create a new session file
        print(line_list)
        new_lines = ''.join(line_list)
        print(new_lines)
    with open(f"sessions/{username}.txt","w") as file:
        # file.truncat()
        file.write(new_lines)
        # print(">>>>FILE", file.read())
@app.route("/")
def index():
    # session['room_name'] = planisphere.START # 'central_corridor'
    # change nosetests after deleting
    # session.clear()
    if 'username' in session:
        # username = session['username']
        username = session['username']
        load_session(session.get('username'))
        return render_template("logged_in.html", username=username)
    return render_template("not_logged_in.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        # load_session(session.get('username'))
        return redirect(url_for('index'))
    return render_template("log_in.html")

@app.route('/logout')
def logout():
    session.clear()
    # session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/nextgame')
def nextgame():
    save_room(session['username'], session['death_count'], session['win_count'], 'central_corridor')
    return redirect(url_for('index'))

@app.route('/score')
def score():
    death_count = session['death_count']
    # print(death_count)
    win_count = session['win_count']
    # print(win_count)
    room_name = session['room_name']
    # print(room_name)
    return render_template("score.html", death_count=death_count,
                           win_count=win_count, room_name=room_name)
    
@app.route("/game", methods=['GET', 'POST'])
def game():
    # load room name and score here from the user session file
    # load_session(session.get('username'))
    # print(session['room_name'])
    # print(session.get('room_name'))
    room_name = session.get('room_name')
    # by default, the Flask route responds to the GET requests
    if request.method == "GET":
        # if there is a room_name
        if room_name:
            # get a room
            room = planisphere.load_room(room_name)
            if room.name in 'Death':
                # add 1 to session['death_score']
                session['death_count'] += 1
            elif room.name in 'The End':
                # add 1 to session['win_score']
                session['win_count'] += 1

            return render_template("show_room.html", room=room)

            #if user starts from '/game' not 'from '/'
        else:
            return render_template("you_died.html")
    else:
        action = request.form.get('action')
        if room_name and action:
            # get a room
            room = planisphere.load_room(room_name)
            # get next room
            next_room = room.go(action)

            if not next_room:
                # save current room name
                session['room_name'] = planisphere.name_room(room)
            else:
                # save next room name
                # save room name to the user session file
                session['room_name'] = planisphere.name_room(next_room)

        session_data = [session['username'], session['death_count'], session['win_count'], session['room_name']]
        save_room(session['username'], session['death_count'], session['win_count'], session['room_name'])

        return redirect(url_for("game"))

# YOU SHOULD CHANGE THIS IF YOU PUT ON THE INTERNET
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# check if module is run directly (not imported)
if __name__ == "__main__":
    app.run()
    