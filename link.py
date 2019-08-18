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
            self.__facing = "down"
            self.__moving = False
            self.__current_subsurface = self.__get_facing_down_subsurface()
            Link.__instance = self

    __facing_left_subsurface = None
    def __get_facing_left_subsurface(self):
        """
        Return the subsurface that contains Link facing left.
        """
        if self.__facing_left_subsurface is None:
            left_offset = pylink_config.scale_nes_tuple_to_pylink((35, 11))
            self.__facing_left_subsurface = self.__sprite_sheet.subsurface(
                pygame.Rect(left_offset, pylink_config.PYLINK_TILE_SIZE))
            self.__facing_left_subsurface.set_colorkey(
                self.__facing_left_subsurface.get_at((0, 0)))
            # The image in the sprite sheet is actually facing right, flip
            # it to face left
            self.__facing_left_subsurface = pygame.transform.flip(
                self.__facing_left_subsurface, True, False)
            # Turn off alpha so that colorkey works for transparency
            self.__facing_left_subsurface.set_alpha(None)
        return self.__facing_left_subsurface

    __facing_up_subsurface = None
    def __get_facing_up_subsurface(self):
        """
        Return the subsurface that contains Link facing up.
        """
        if self.__facing_up_subsurface is None:
            forward_offset = pylink_config.scale_nes_tuple_to_pylink((69, 11))
            self.__facing_up_subsurface = self.__sprite_sheet.subsurface(
                pygame.Rect(forward_offset, pylink_config.PYLINK_TILE_SIZE))
            self.__facing_up_subsurface.set_colorkey(
                self.__facing_up_subsurface.get_at((0, 0)))
            # Turn off alpha so that colorkey works for transparency
            self.__facing_up_subsurface.set_alpha(None)
        return self.__facing_up_subsurface

    __facing_right_subsurface = None
    def __get_facing_right_subsurface(self):
        """
        Return the subsurface that contains Link facing right.
        """
        if self.__facing_right_subsurface is None:
            right_offset = pylink_config.scale_nes_tuple_to_pylink((35, 11))
            self.__facing_right_subsurface = self.__sprite_sheet.subsurface(
                pygame.Rect(right_offset, pylink_config.PYLINK_TILE_SIZE))
            self.__facing_right_subsurface.set_colorkey(
                self.__facing_right_subsurface.get_at((0, 0)))
            # Turn off alpha so that colorkey works for transparency
            self.__facing_right_subsurface.set_alpha(None)
        return self.__facing_right_subsurface

    __facing_down_subsurface = None
    def __get_facing_down_subsurface(self):
        """
        Return the subsurface that contains Link facing down.
        """
        if self.__facing_down_subsurface is None:
            forward_offset = pylink_config.scale_nes_tuple_to_pylink((1, 11))
            self.__facing_down_subsurface = self.__sprite_sheet.subsurface(
                pygame.Rect(forward_offset, pylink_config.PYLINK_TILE_SIZE))
            self.__facing_down_subsurface.set_colorkey(
                self.__facing_down_subsurface.get_at((0, 0)))
            # Turn off alpha so that colorkey works for transparency
            self.__facing_down_subsurface.set_alpha(None)
        return self.__facing_down_subsurface

    def left_keydown(self):
        """
        This method is called when the left arrow key is pressed.
        """
        self.__facing = "left"
        self.__moving = True
        self.__current_subsurface = self.__get_facing_left_subsurface()

    def up_keydown(self):
        """
        This method is called when the up arrow key is pressed.
        """
        self.__facing = "up"
        self.__moving = True
        self.__current_subsurface = self.__get_facing_up_subsurface()

    def right_keydown(self):
        """
        This method is called when the right arrow key is pressed.
        """
        self.__facing = "right"
        self.__moving = True
        self.__current_subsurface = self.__get_facing_right_subsurface()

    def down_keydown(self):
        """
        This method is called when the down arrow key is pressed.
        """
        self.__facing = "down"
        self.__moving = True
        self.__current_subsurface = self.__get_facing_down_subsurface()

    def blit(self):
        """
        Blits Link to his current loction on the screen.
        """
        pygame.display.get_surface().blit(self.__current_subsurface, self.__topleft)
