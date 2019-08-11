"""
The overworld map.

This module loads and manages the overworld map for the game.
The entire map is loaded and scaled once when the init() function is
called.
"""
import os
import pygame
import numpy
import pylink_config

__overworld_map = None # pylint: disable=invalid-name

def init():
    """
    Load and scale the entire map.
    This function must be called before any other functions in the
    module are called.
    """
    global __overworld_map # pylint: disable=global-statement,invalid-name

    if __overworld_map is None:
        __overworld_map = pygame.image.load(os.path.join(
            'assets', 'NES-TheLegendofZelda-Overworld.png'))
        __overworld_map = pygame.transform.scale(__overworld_map, tuple(pylink_config.NES_TO_PYLINK_SCALE_FACTOR * numpy.array(__overworld_map.get_size())))
        __overworld_map.convert()

def submap(x, y):  # pylint: disable=invalid-name
    """
    Return the region of the overworld map referenced by x (column)
    and y (row). This is returned as a pygame Surface object.
    """
    global __overworld_map  # pylint: disable=global-statement,invalid-name

    # First get a copy of the map rect object, this gets us a window of the
    # correct size.
    map_window = pylink_config.PYLINK_MAP.copy()

    # Next, reset the window's base to (0, 0)
    map_window.topleft = (0, 0)

    # Now, translate the window where it needs to be to be over the correct
    # subregion of the map. (Note that there is a frame around each region)
    map_window = map_window.move(
        ((x * pylink_config.PYLINK_MAP.width) + ((x + 1) * pylink_config.NES_TO_PYLINK_SCALE_FACTOR * 1)),
        ((y * pylink_config.PYLINK_MAP.height) + ((y + 1) * pylink_config.NES_TO_PYLINK_SCALE_FACTOR * 1)))

    # Next, create a subsurface where the window is now pointing and return it
    return __overworld_map.subsurface(map_window)
