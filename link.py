"""
Handles the Link playable character
"""
import os
import pygame
import numpy
import pylink_config

__link_sprite_sheet = None  # pylint: disable=invalid-name


def __forward():
    """
    Return the subsurface that contains Link facing forward.
    TODO: this will morph into some other way of doing this
    """
    global __link_sprite_sheet  # pylint: disable=global-statement,invalid-name

    forward_offset = pylink_config.scale_nes_tuple_to_pylink((1, 11))
    subsurface = __link_sprite_sheet.subsurface(pygame.Rect(forward_offset, pylink_config.PYLINK_TILE_SIZE))
    subsurface.set_colorkey(subsurface.get_at((0, 0)))
    # Turn off alpha so that colorkey works for transparency
    subsurface.set_alpha(None)
    return subsurface

def init():
    """
    Initialize the Link character and draw it on the starting point on the
    screen. Call this after the overworld map has been drawn.
    """
    global __link_sprite_sheet  # pylint: disable=global-statement,invalid-name

    if __link_sprite_sheet is None:
        __link_sprite_sheet = pygame.image.load(os.path.join(
            'assets', 'NES-TheLegendofZelda-Link.png'))
        __link_sprite_sheet = pygame.transform.scale(__link_sprite_sheet, tuple(
            pylink_config.NES_TO_PYLINK_SCALE_FACTOR * numpy.array(__link_sprite_sheet.get_size())))
        __link_sprite_sheet.convert()
    # Link's topleft corner ends up in the center instead of him being dead
    # center at the start, but the tiles around are clear and this works
    # just fine.
    pygame.display.get_surface().blit(__forward(), pylink_config.PYLINK_MAP.center)
    pygame.display.flip()
