"""Configuration for the pylink Game."""
import pygame
import numpy

NES_TO_PYLINK_SCALE_FACTOR = 3

def scale_nes_tuple_to_pylink(nes_tuple):
    """
    Scale up an NES tuple to its pylink size.
    """
    return tuple(NES_TO_PYLINK_SCALE_FACTOR * numpy.array(nes_tuple))

#: The entire screen
NES_WINDOW_SIZE = (256, 240) # deprecated
NES_WINDOW = pygame.Rect((0, 0), (256, 240))
PYLINK_WINDOW = pygame.Rect((0, 0), scale_nes_tuple_to_pylink(NES_WINDOW.size))

#: The scoreboard section at the top of the screen
NES_SCOREBOARD = pygame.Rect((0, 0), (256, (4 * 16)))
PYLINK_SCOREBOARD = pygame.Rect((0, 0), scale_nes_tuple_to_pylink(NES_SCOREBOARD.size))

#: The map section under the scoreboard
NES_MAP = pygame.Rect((0, (4 * 16)), (256, (240 - (4 * 16))))
PYLINK_MAP = pygame.Rect(scale_nes_tuple_to_pylink(NES_MAP.topleft), scale_nes_tuple_to_pylink(NES_MAP.size))

#: The size of each tile
NES_TILE_SIZE = (16, 16)
PYLINK_TILE_SIZE = scale_nes_tuple_to_pylink(NES_TILE_SIZE)

#: Total game window size, in tiles
WINDOW_SIZE_IN_TILES = (16, 15)

#: Size, in pixels, of each tile in the game as (x, y)
TILE_SIZE = (48, 48)

#: The amount (x_factor, y_factor) to scale each tile when loading.
#:
#: Scaling is done by multiplying the size when the tile is loaded by
#: the factors given.
TILE_SCALING = tuple(numpy.divide(TILE_SIZE, NES_TILE_SIZE))

#: Total window size, in pixels
WINDOW_SIZE = tuple(
    map(
        int,
        numpy.multiply(TILE_SIZE, WINDOW_SIZE_IN_TILES)
    )
)

# The upper left location for the map in pixels.
# This does leave room for the score board.
MAP_UPPER_LEFT = tuple(map(int, numpy.multiply(TILE_SIZE, (0, 4))))

#
# Timing for the main character (Link)
#
LINK_MOVE_INTERVAL_MSECS = 50
LINK_STOPPED_VELOCITY = (0, 0)
LINK_MOVE_LEFT_VELOCITY = scale_nes_tuple_to_pylink((-6, 0))
LINK_MOVE_UP_VELOCITY = scale_nes_tuple_to_pylink((0, -6))
LINK_MOVE_RIGHT_VELOCITY = scale_nes_tuple_to_pylink((6, 0))
LINK_MOVE_DOWN_VELOCITY = scale_nes_tuple_to_pylink((0, 6))

# User defined events.
# These are placed here, so they can be shared because the events module
# imports the other modules that need this information, and defining
# them in the events module itself causes a circular dependency.
MOVE_LINK = pygame.USEREVENT + 1
