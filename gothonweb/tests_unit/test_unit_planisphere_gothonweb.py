### UNIT TESTS
import unittest
from gothonweb.planisphere_gothonweb import *

class TestGothonPlanisphere(unittest.TestCase):

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

    def test_gothon_game_map(self):
        start_room = load_room(START)
        
        self.assertEqual(start_room, start_place)
        self.assertEqual(start_place.go('shoot'), shoot)
        self.assertEqual(start_place.go('dodge'), dodge)
        self.assertEqual(start_place.go('tell a joke'), laser_weapon_armory)
    
        self.assertEqual(the_bridge.go('throw the bomb'), throw_the_bomb)
        self.assertEqual(the_bridge.go('slowly place the bomb'), escape_pod)

        self.assertEqual(laser_weapon_armory.go('right_code'), the_bridge)
        self.assertEqual(laser_weapon_armory.go('wrong_code'), wrong_code)

        self.assertEqual(escape_pod.go('right_pod'), the_end_winner)
        self.assertEqual(escape_pod.go('wrong_pod'), wrong_pod)

    def test_name_room(self):
        self.assertEqual(name_room(start_place), 'start_place')
        self.assertRaises(Exception, name_room, 'something')


    def test_load_room(self):
        self.assertRaises(Exception, load_room, 'something')
        self.assertEqual(dodge, load_room('dodge'))




# if __name__ == '__main__':
#     unittest.main()
