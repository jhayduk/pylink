"""Configuration for the pylink Game."""
import numpy

nes_window_size = (256, 240)
"""Original NES screen resolution"""

nes_tile_size = (16, 16)
"""Original Zelda tile size"""

window_size_in_tiles = (16, 15)
"""Total game window size, in tiles"""

tile_size = (48, 48)
"""Size, in pixels, of each time in the game as (x, y)"""

window_size = tuple(map(int, numpy.multiply(tile_size, window_size_in_tiles)))
"""Total window size, in pixels"""

map_upper_left = tuple(map(int, numpy.multiply(tile_size, (0, 4))))
"""The uppler left location for the map in pixels leaving room for the score board"""
