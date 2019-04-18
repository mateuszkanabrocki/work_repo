from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
from flask import make_response
import planisphere

app = Flask(__name__)



@app.route("/")
def index():

    # def delete_cookie():
    #     res = make_response("Cookie Removed")
    #     res.set_cookie('username', 'bar', max_age=0)
    # this is used to "setup" the session with starting values
    
    # session['room_name'] = planisphere.START # 'central_corridor'
    # print(session['username'])
    # session['room_name']
    if 'username' in session:
        username = session['username']
        print("logging in")
        return render_template("logged_in.html", username=username)
        # wait here for a while
        # add logout option during the game
        # return redirect(url_for("game"))
    return redirect(url_for("login"))


@app.route("/clear_session")
def clear_session():
    session.clear() # save the score after wining
    return redirect(url_for("/"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("log_in.html")
    else:
        username = request.form.get('username')
        session['username'] = username
        return redirect(url_for("game"))
    

@app.route("/game", methods=['GET', 'POST'])
def game():
    room_name = session.get('room_name')
    # By default, the Flask route responds to the GET requests.
    if request.method == "GET":
        # if there is a room_name
        if room_name:
            # get a room
            room = planisphere.load_room(room_name)
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
                session['room_name'] = planisphere.name_room(next_room)

        return redirect(url_for("game"))

# YOU SHOULD CHANGE THIS IF YOU PUT ON THE INTERNET
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# check if module is run directly (not imported)
if __name__ == "__main__":
    app.run()