from nose.tools import assert_in, assert_equal, assert_raises
from gothonweb.planisphere_3rooms import *


def test_room():
    gold = Room("GoldRoom",
                """This room has gold in it you can grab. There's a
                door to the north.""")
    assert_equal(gold.name, "GoldRoom")
    assert_equal(gold.paths, {})


def test_room_paths():
    center = Room("Center", "Test room in the center.")
    north = Room("North", "Test room in the north.")
    south = Room("South", "Test room in the south.")

    center.add_paths({'north': north, 'south': south})
    assert_equal(center.go('north'), north)
    assert_equal(center.go('south'), south)


def test_map():
    start = Room("Start", "You can go west and down a hole.")
    west = Room("Trees", "There are trees here, you can go east.")
    down = Room("Dungeon", "It's dark down here, you can go up.")

    start.add_paths({'west': west, 'down': down})
    west.add_paths({'east': start})
    down.add_paths({'up': start})

    assert_equal(start.go('west'), west)
    assert_equal(start.go('west').go('east'), start)
    assert_equal(start.go('down').go('up'), start)


def test_3rooms_game_map():
    start_room = load_room(START)
    assert_equal(start_room, start_place)
    assert_equal(start_place.go('yes'), door_pick)
    assert_equal(start_place.go('something else'), None)

    assert_equal(door_pick.go('1'), door_1)
    assert_equal(door_pick.go('2'), door_2)

    assert_equal(door_1.go('exit'), next_pick)
    assert_equal(door_3.go('stay'), None)

    assert_equal(next_pick.go('leave'), the_end)
    assert_equal(next_pick.go('visit'), door_pick)


def test_name_room():
    assert_equal(name_room(start_place), 'start_place')
    assert_raises(Exception, name_room, 'something')


def test_load_room():
    assert_raises(Exception, load_room, 'something')
    assert_equal(door_pick, load_room('door_pick'))
