"""
Handles the Link playable character
"""
import os
import pygame
import numpy
import pylink_config

class Link(object):
    """
    The Link player object.
    This is a singleton object and must only be accessed with
    Link.getInstance(). That function will take care of creating the instance
    the first time it is called.
    """
    __instance = None
    @staticmethod
    def get_instance():
        """
        Get an instance of the Link object.
        Use this instead of 'new Link()' to get the player object.
        """
        if Link.__instance is None:
            Link()
        return Link.__instance

    def __init__(self):
        """
        Virtually private constructor.
        DO NOT USE 'new Link()', use 'Link.get_instance()' instead.
        """
        if Link.__instance is not None:
            raise Exception("This class is a singleton. Use 'Link.get_instance()' instead of 'new Link()'")
        else:
            self.__sprite_sheet = pygame.image.load(os.path.join(
                'assets', 'NES-TheLegendofZelda-Link.png'))
            self.__sprite_sheet = pygame.transform.scale(self.__sprite_sheet, tuple(
                pylink_config.NES_TO_PYLINK_SCALE_FACTOR * numpy.array(self.__sprite_sheet.get_size())))
            self.__sprite_sheet.convert()
            # Link's topleft corner ends up in the center instead of him being dead
            # center at the start, but the tiles around are clear and this works
            # just fine.
            self.__topleft = pylink_config.PYLINK_MAP.center
            Link.__instance = self

    def __forward(self):
        """
        Return the subsurface that contains Link facing forward.
        TODO: this will morph into some other way of doing this
        """

        forward_offset = pylink_config.scale_nes_tuple_to_pylink((1, 11))
        subsurface = self.__sprite_sheet.subsurface(
            pygame.Rect(forward_offset, pylink_config.PYLINK_TILE_SIZE))
        subsurface.set_colorkey(subsurface.get_at((0, 0)))
        # Turn off alpha so that colorkey works for transparency
        subsurface.set_alpha(None)
        return subsurface

    def blit(self):
        """
        Blits Link to his current loction on the screen.
        """
        pygame.display.get_surface().blit(self.__forward(), self.__topleft)
