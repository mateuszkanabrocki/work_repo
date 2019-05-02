import pytest
from gothonweb.planisphere_3rooms import *


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

def test_3rooms_game_map():
    start_room = load_room(START)
    assert start_room == start_place
    assert start_place.go('yes') == door_pick
    assert start_place.go('something else') == None

    assert door_pick.go('1') == door_1
    assert door_pick.go('2') == door_2

    assert door_1.go('exit') == next_pick
    assert door_3.go('stay') == None

    assert next_pick.go('leave') == the_end
    assert next_pick.go('visit') == door_pick

def test_name_room():
    assert name_room(start_place) == 'start_place'
    pytest.raises(Exception, name_room, 'something')

def test_load_room():
    pytest.raises(Exception, load_room, 'something')
    assert door_pick == load_room('door_pick')
