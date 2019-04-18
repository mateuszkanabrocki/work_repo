direction = []
do = ['yes', 'yeah', 'sure', 'ready', 'go', '1', 'one',
        '2', 'two', '3', 'three', 'quit', 'exit', 'leave', 'room']
stop = ['the', 'in', 'of', 'from', 'at', 'it', 'a', 'him']
noun = []


class Room(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}

    def go(self, direction):
        return self.paths.get(direction, None)

    def add_paths(self, paths):
        self.paths.update(paths)


START = 'start_place'


start_place = Room('Welcome!',
    """
    Hi there. Welcome to this simple text adventure game.
    Are you ready to play?
    """)


door_pick = Room('Pick the door', 
"""
Imagine you're in a dark room with 3 doors.
Which door do you choose?

Pick wisely...
""")


door_1 = Room('Room no. 1', 
"""
(Unfortunately this part will be covered in Polish)

Wchodzisz do pierwszego pokoju.
W pokoju widzisz kota, który leci w Twoim kierunku.
Jak nazywa się ten kot?




...KotLecik!


Do you want to stay with a cat or exit the room?
""")


door_2 = Room('Room no. 2', 
"""
(Unfortunately this part will be covered in Polish)

Wchodzisz do drugiego pokoju.
Jesteś na VI Miedzyregionalnych Zawodach Jeździeckich
w Cieszynie.
Następna konkurencja to wyścig z przekodami.
W konkurencji bierze udział ślepy koń, który udziela
właśnie wywiadu tuż przed rozpoczęciem wyścigiem.

Co mówi ślepy koń na wyścigach z przeszkodami?





...Nie widzę przeszkód.


Do you want to stay here or exit the room?
""")


door_3 = Room('Room no. 3', 
"""
(Unfortunately this part will be covered in Polish)

Wchodzisz do trzeciego pokoju.
Przed sobą widzisz złomiarza ciągnącego
za sobą worek z puszkami.
Za złomiarzem podąża jego pies.

Jak nazywa się pies złomiarza?






...Puszek


Do you want to stay here or exit the room?
""")


next_pick = Room('Another pick?', 
"""
Do you want to visit another room
or leave the game?
""")


the_end = Room('Happy Ending', 
"""
Hope you enjoyed the game
Have a nice day!
""")


class Map(object):

    dict = {'door_pick': door_pick,
            'door_1': door_1,
            'door_2': door_2,
            'door_3': door_3,
            'next_pick': next_pick,
            'the_end': the_end
           }

door_1.add_paths({
    'quit': Map.dict['next_pick'],
    'leave': Map.dict['next_pick'],
    'exit': Map.dict['next_pick']
})

door_2.add_paths({
    'quit': Map.dict['next_pick'],
    'leave': Map.dict['next_pick'],
    'exit': Map.dict['next_pick']
})

door_3.add_paths({
    'quit': Map.dict['next_pick'],
    'leave': Map.dict['next_pick'],
    'exit': Map.dict['next_pick']
})

next_pick.add_paths({
    'leave': Map.dict['the_end'],
    'yes': Map.dict['the_end'],
    'visit': Map.dict['door_pick'],
    'room': Map.dict['door_pick']
})

door_pick.add_paths({
    '1': Map.dict['door_1'],
    'one': Map.dict['door_1'],
    '2': Map.dict['door_2'],
    'two': Map.dict['door_2'],
    '3': Map.dict['door_3'],
    'three': Map.dict['door_3']
})

start_place.add_paths({
    'yes': Map.dict['door_pick'],
    'ready': Map.dict['door_pick'],
    'go': Map.dict['door_pick']
})

def load_room(name):
    white_list = ('start_place', 'door_pick', 'next_pick', 'door_3', 'door_2', 'door_1', 'the_end')
    print('load room name', name)
    if name not in white_list:
        raise Exception(f'You can\'t run load_room with {name} as a parameter.')
    return globals().get(name)

def name_room(room):
    white_list = ('start_place', 'door_pick', 'next_pick', 'door_3', 'door_2', 'door_1', 'the_end')
    print("next_room", room)
    print("next_room.name", room.name)
    # give room object get room name
    for key, value in globals().items():
        if value == room and key in white_list:
            return key

    # raise Exception(f'You can\'t run name_room with {name} as a parameter.')