### PyTest
# try: # used for unittest so it doesn't throw an error 'can't import pytest'
#     import pytest
# except:
#     pass

import pytest
from gothonweb.planisphere_gothonweb import *


def test_room():
    gold = Room("GoldRoom",
                """This room has gold in it you can grab. There's a
                door to the north.""")
    assert gold.name == "GoldRoom"
    assert gold.paths == {}

def test_room_paths():
    center = Room("Center", "Test room in the center.")
    north = Room("North", "Test room in the north.")
    south = Room("South", "Test room in the south.")

    center.add_paths({'north': north, 'south': south})

    assert center.go('north') == north
    assert center.go('south') == south

def test_map():
    start = Room("Start", "You can go west and down a hole.")
    west = Room("Trees", "There are trees here, you can go east.")
    down = Room("Dungeon", "It's dark down here, you can go up.")

    start.add_paths({'west': west, 'down': down})
    west.add_paths({'east': start})
    down.add_paths({'up': start})

    assert start.go('west') == west
    assert start.go('west').go('east') == start
    assert start.go('down').go('up') == start

def test_gothon_game_map():
    start_room = load_room(START)
    
    assert start_room == start_place
    assert start_place.go('shoot') == shoot
    assert start_place.go('dodge') == dodge
    assert start_place.go('tell a joke') == laser_weapon_armory

    assert the_bridge.go('throw the bomb') == throw_the_bomb
    assert the_bridge.go('slowly place the bomb') == escape_pod

    assert laser_weapon_armory.go('right_code') == the_bridge
    assert laser_weapon_armory.go('wrong_code') == wrong_code

    assert escape_pod.go('right_pod') == the_end_winner
    assert escape_pod.go('wrong_pod') == wrong_pod

def test_name_room():
    assert name_room(start_place) == 'start_place'
    pytest.raises(Exception, name_room, 'something')

def test_load_room():
    pytest.raises(Exception, load_room, 'something')
    assert load_room('dodge') == dodge




# if __name__ == '__main__':
#     unittest.main()
