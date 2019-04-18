from os.path import exists

# f= open("sessions/username_mateusz.txt","w+")

# make a new user session
# with open("sessions/username_mateusz.txt","w+") as f: 


def save_room(username, room_name):

    with open(f"sessions/{username}.txt","r+") as file:
        line_list = [file.readline(), file.readline(), file.readline()]
        
        # if more parameters in the file, use:
        # line_list = [file.readline()]
        # for i in (1,2):
        #     line_list.append(file.readline())

        line_list[2] = f"room_name = {room_name}"
        # now create a new session file
        new_lines = ''.join(line_list)

    with open(f"sessions/{username}.txt","w") as file:
        # file.truncat() # no atrribute truncate, in other script it works
        file.write(new_lines)





        # lines = file.read()
        # lines.replace('room_name =', 'room_name =') # go to the 3th line
        # lines.append("I'm here! :D")
        
        # session[user_name] = lines[2].strip().lstrip('room_name =')
        # print(session[user_name])


        

save_room('Mat','laser_weapon_armory')

def save_death_count():
    pass

def save_win_count():
    pass
        
        # save current death and win counts
        # save current room

# def load_session(username):

#     file_name = f"sessions/{username}.txt"
#     file_exists = exists(file_name)
#     # for new user while loging in
#     if not file_exists:
#         print("creating a file!")
#         with open(file_name, "w") as file: 
#             file.write('death=0\nwin=0')
#     print("the file exist, we can load it")

#     # load room name and score (deaths and wins number) here from the user session file 
#     with open(file_name, "r") as file: 
#             death_number = file.readline().strip().strip('death=')
#             win_number = file.readline().strip().strip('win=')
#             print(death_number)
#             print(win_number)

# load_session("Mats")


def load_session(username):

    file_name = f"sessions/{username}.txt"
    file_exists = exists(file_name)
    # for new user while loging in
    if not file_exists:
        # print("creating a file!")
        with open(file_name, "w") as file:
            file.write('death=0\nwin=0') 
            pass #created a file
    # print("the file exist, we can load it")

    # load room name and score (deaths and wins number) here from the user session file 
    with open(file_name, "r") as file: 
            session['death'] = file.readline().strip().strip('death=')
            session['win'] = file.readline().strip().strip('win=')
            # print(death_number)
            # print(win_number)


# check the score -> to each room
# count death and win
