# dance_party_game.py 2019-06-01
# Author: Mateusz Kanabrocki <mateusz.kanabrocki@gmail.com>
# Copyright: This module has been placed in the public domain
# https://github.com/mateuszkanabrocki/projects

"""
A simple text adventure game called dance party game.
This is the engine module responsible for the main game logic.
This module defines the following:

Classes:

- `Engine`, downloads game scenerio module and scenes from the scenerio module.

How To Use This Module
======================
(See the individual classes, methods, attributes and functions for details.)

Run this module in the default project directory configuration.
"""

__docformat__ = 'restructuredtext'

from sys import exit
from dance_party_scenerio import ZoukScenerio


class Engine(object):

    """
    This class represents a game engine.

    The object can be initialized with no given parameters.

    Attributes
    ----------
    scenerio: class Scenerio
        class containing game data run by the engine

    Methods
    -------
    def download(self, scenerio: ZoukScenerio) -> None
        download game scenerio data from the Scenerio class
        and save it as scenerio attribute
    play(self) -> None
        run the game using the downloaded game scenerio
    """

    def __init__(self) -> None:
        """Initialize a `Scene` object."""
        # set a time variable for a sleep function
        self.time = 1

    def download(self, scenerio: ZoukScenerio) -> None:
        """Download game scenerio data.

        Save the game scenerio data from the object ZoukScenerio
        of the Scenerio class and save it as scenerio attribute.

        Parameters:

        - `scenerio`: class Scenerio, class containing all the game data needed
           to run the game
        """

        self.scenerio = scenerio

    # play a game
    def play(self) -> None:
        """Run the game using the downloaded game scenerio."""

        next_game_name = None

        while next_game_name not in ('game_over', 'last_scene'):
            next_game_name = self.scenerio.next_scene()

        self.scenerio.next_scene()
        exit()
