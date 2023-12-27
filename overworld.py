"""
The overworld map.

This module loads and manages the overworld map for the game.
The entire map is loaded and scaled once when the init() function is
called.

Only use this module to display the map and to transition to adjacent maps.
"""
import os
import numpy
import pygame
import pylink_config

#
# The offsets below are used by switch_map to shift to the next map
# in a given direction. This is a hash map of direction to offset that
# can be added to the current submap's index to get to the next one.
#
switch_map_offsets = {
    "right": (1, 0),
    "down": (0, 1),
    "left": (-1, 0),
    "up": (0, -1)
}


class Overworld(object):
    """
    The Overworld map.
    This is a singleton object and must only be accessed with
    Overworld.getInstance(). That function will take care of creating the
    instance the first time it is called.
    The object created manages the overworld map and keeps track of which map
    should be displayed at any given time and draws it when blitted.
    """
    __instance = None

    @staticmethod
    def get_instance():
        """
        Get an instance of the Overworld object.
        Use this instead of 'new Overworld()' to get the overworld object.
        """
        if Overworld.__instance is None:
            Overworld.__instance = Overworld()
        return Overworld.__instance

    def __init__(self):
        """
        Virtually private constructor.
        DO NOT USE 'new Overworld()', use 'Overworld.get_instance()' instead.
        """
        if Overworld.__instance is not None:
            raise Exception(
                "This class is a singleton. Use 'Link.get_instance()' instead of 'new Link()'")
        else:
            self.__entire_overworld_map = pygame.image.load(os.path.join(
                'assets', 'NES-TheLegendofZelda-Overworld.png'))
            self.__entire_overworld_map = pygame.transform.scale(
                self.__entire_overworld_map, pylink_config.scale_nes_tuple_to_pylink(self.__entire_overworld_map.get_size()))
            self.__entire_overworld_map.convert()
            # set self.__current_submap to the starting map
            self.__current_submap = (7, 7)
            Overworld.__instance = self


    def __submap(self, current_submap):
        """
        Return the region of the overworld map referenced by (column, row).
        This is returned as a pygame Surface object.
        TODO: It would be better to have these as constants and not
        recalculated every time.
        """
        column, row = current_submap
        # First get a copy of the map rect object, this gets us a window of the
        # correct size.
        map_window = pylink_config.PYLINK_MAP.copy()

        # Next, reset the window's base to (0, 0)
        map_window.topleft = (0, 0)

        # Now, translate the window where it needs to be over the correct
        # subregion of the map. (Note that there is a frame around each region)
        map_window = map_window.move(
            ((column * pylink_config.PYLINK_MAP.width) + ((column + 1) * pylink_config.NES_TO_PYLINK_SCALE_FACTOR * 1)),
            ((row * pylink_config.PYLINK_MAP.height) + ((row + 1) * pylink_config.NES_TO_PYLINK_SCALE_FACTOR * 1)))

        # Next, create a subsurface where the window is now pointing and return it
        return self.__entire_overworld_map.subsurface(map_window)

    def switch_maps(self, direction):
        """
        Change maps to the next one in the direction of the direction input
        parameter. This is called from within the move method of the Link
        character when he is walking off the edge of the current map.

        It is assumed that there is another map in the direction requested.
        It is the responsibility of the map itself to have a border of
        blocking tiles on any edge that is the edge of the map.
        """
        self.__current_submap = tuple(numpy.add(self.__current_submap, switch_map_offsets[direction]))

    def draw(self):
        """
        Draws the entire current submap to the main window.
        """
        pygame.display.get_surface().blit(self.__submap(self.__current_submap), pylink_config.PYLINK_MAP)
