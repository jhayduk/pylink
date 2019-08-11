"""Configuration for the pylink Game."""
import pygame
import numpy

NES_TO_PYLINK_SCALE_FACTOR = 3

#: The entire screen
NES_WINDOW_SIZE = (256, 240) # deprecated
NES_WINDOW = pygame.Rect((0, 0), (256, 240))
PYLINK_WINDOW = pygame.Rect((0, 0), tuple(NES_TO_PYLINK_SCALE_FACTOR * numpy.array(NES_WINDOW.size)))

#: The scoreboard section at the top of the screen
NES_SCOREBOARD = pygame.Rect((0, 0), (256, (4 * 16)))
PYLINK_SCOREBOARD = pygame.Rect((0, 0), tuple(NES_TO_PYLINK_SCALE_FACTOR * numpy.array(NES_SCOREBOARD.size)))

#: The map section under the map
NES_MAP = pygame.Rect((0, (4 * 16)), (256, (240 - (4 * 16))))
PYLINK_MAP = pygame.Rect(tuple(NES_TO_PYLINK_SCALE_FACTOR * numpy.array(
    NES_MAP.topleft)), tuple(NES_TO_PYLINK_SCALE_FACTOR * numpy.array(NES_MAP.size)))

#: Original Zelda tile size
NES_TILE_SIZE = (16, 16)

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

#: The upper left location for the map in pixels.
#: This does leave room for the score board.
MAP_UPPER_LEFT = tuple(map(int, numpy.multiply(TILE_SIZE, (0, 4))))
