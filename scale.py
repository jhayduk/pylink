"""Provide scaling utilities for game screen.

In general, all coordinates in the game code are in original NES
values where tiles are 16x16 pixels and the full screen is 256x240
pixels. The scaling to whatever the games screen actually is, which is
usually 3 times that size, is encapulated here so that the code can
talk all in one common coordinate system, and changes to scaling are
in one place.

       x
   +------->
   |
 y |
   |
   v
"""
import numpy
import pylink_config

def coordinates(nes_coordinates):
    """
    Convert original NES coordinates to game screen coordinates.

    Args:
        nes_coordinate: A tuple representing the (x, y) coordinate in
            the original NES scale.

    Returns:
        (scaled_x, scaled_y): The x and y coordinates scaled to the size
            of the game screen
    """
    return tuple(
        map(
            int,
            numpy.multiply(
                nes_coordinates,
                pylink_config.TILE_SCALING
            )
        )
    )
