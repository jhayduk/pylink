"""
The overworld map.

This module loads and manages the overworld map for the game.
The entire map is loaded and scaled once when the init() function is
called.

Only use this module to display the map and to transition to adjacent maps.
"""
import os
import pygame
import pylink_config

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
            Overworld()
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

        # Now, translate the window where it needs to be to be over the correct
        # subregion of the map. (Note that there is a frame around each region)
        map_window = map_window.move(
            ((column * pylink_config.PYLINK_MAP.width) + ((column + 1) * pylink_config.NES_TO_PYLINK_SCALE_FACTOR * 1)),
            ((row * pylink_config.PYLINK_MAP.height) + ((row + 1) * pylink_config.NES_TO_PYLINK_SCALE_FACTOR * 1)))

        # Next, create a subsurface where the window is now pointing and return it
        return self.__entire_overworld_map.subsurface(map_window)

    def blit(self):
        """
        Blits The entire current submap to the main window.
        """
        pygame.display.get_surface().blit(self.__submap(self.__current_submap), pylink_config.PYLINK_MAP)
