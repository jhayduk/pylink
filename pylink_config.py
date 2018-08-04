"""Configuration for the pylink Game."""
import numpy

NES_WINDOW_SIZE = (256, 240)
"""Original NES screen resolution"""

NES_TILE_SIZE = (16, 16)
"""Original Zelda tile size"""

WINDOW_SIZE_IN_TILES = (16, 15)
"""Total game window size, in tiles"""

TILE_SIZE = (48, 48)
"""Size, in pixels, of each time in the game as (x, y)"""

TILE_SCALING = tuple(numpy.divide(TILE_SIZE, NES_TILE_SIZE))
"""
The amount (x_factor, y_factor) to scale each tile when loading.

Scaling is done by multiplying the size when the tile is loaded by
the factors given.
"""

WINDOW_SIZE = tuple(
    map(
        int,
        numpy.multiply(TILE_SIZE, WINDOW_SIZE_IN_TILES)
    )
)
"""Total window size, in pixels"""

MAP_UPPER_LEFT = tuple(map(int, numpy.multiply(TILE_SIZE, (0, 4))))
"""
The upper left location for the map in pixels.

This does leave room for the score board.
"""
