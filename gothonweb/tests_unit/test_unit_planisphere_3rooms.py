import unittest
from gothonweb.planisphere_3rooms import *

class Test3RoomsPlanisphere(unittest.TestCase):

    def test_room(self):
        gold = Room("GoldRoom",
                    """This room has gold in it you can grab. There's a
                    door to the north.""")

        self.assertEqual(gold.name, "GoldRoom")
        self.assertEqual(gold.paths, {})

    def test_room_paths(self):
        center = Room("Center", "Test room in the center.")
        north = Room("North", "Test room in the north.")
        south = Room("South", "Test room in the south.")

        center.add_paths({'north': north, 'south': south})

        self.assertEqual(center.go('north'), north)
        self.assertEqual(center.go('south'), south)

    def test_map(self):
        start = Room("Start", "You can go west and down a hole.")
        west = Room("Trees", "There are trees here, you can go east.")
        down = Room("Dungeon", "It's dark down here, you can go up.")

        start.add_paths({'west': west, 'down': down})
        west.add_paths({'east': start})
        down.add_paths({'up': start})

        self.assertEqual(start.go('west'), west)
        self.assertEqual(start.go('west').go('east'), start)
        self.assertEqual(start.go('down').go('up'), start)

    def test_3rooms_game_map(self):
        start_room = load_room(START)
        self.assertEqual(start_room, start_place)
        self.assertEqual(start_place.go('yes'), door_pick)
        self.assertEqual(start_place.go('something else'), None)

        self.assertEqual(door_pick.go('1'), door_1)
        self.assertEqual(door_pick.go('2'), door_2)

        self.assertEqual(door_1.go('exit'), next_pick)
        self.assertEqual(door_3.go('stay'), None)

        self.assertEqual(next_pick.go('leave'), the_end)
        self.assertEqual(next_pick.go('visit'), door_pick)

    def test_name_room(self):
        self.assertEqual(name_room(start_place), 'start_place')
        self.assertRaises(Exception, name_room, 'something')

    def test_load_room(self):
        self.assertRaises(Exception, load_room, 'something')
        self.assertEqual(door_pick, load_room('door_pick'))
