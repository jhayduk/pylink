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
            # Load the sprite sheet with all of Link's images, and scale it
            # to the game's scale.
            self.__sprite_sheet = pygame.image.load(os.path.join(
                'assets', 'NES-TheLegendofZelda-Link.png'))
            self.__sprite_sheet = pygame.transform.scale(self.__sprite_sheet, tuple(
                pylink_config.NES_TO_PYLINK_SCALE_FACTOR * numpy.array(self.__sprite_sheet.get_size())))
            self.__sprite_sheet.convert()

            # Start the periodic event for changing steps. When this fires,
            # this class' toggle_steps() method will be caled and, if Link
            # is moving, the self.__step setting will toggle so that the
            # code knows which of the two sprites to show.
            # Once started, the toggle_steps() method will get called
            # periodically.
            pygame.time.set_timer(pylink_config.TOGGLE_LINKS_STEPS, pylink_config.LINK_STEP_TOGGLE_INTERVAL_MSECS)

            # Setup Link's initial position.
            # Link's topleft corner ends up in the center instead of him being dead
            # center at the start, but the tiles around are clear and this works
            # just fine.
            self.__topleft = pylink_config.PYLINK_MAP.center
            self.__facing = "down"
            self.__moving = False
            self.__step = 0
            self.__current_subsurface = self.__get_facing_down_subsurface(
                self.__step)
            Link.__instance = self

    __facing_left_subsurface = [None, None]
    def __get_facing_left_subsurface(self, step):
        """
        Return the subsurface that contains Link facing left.
        """
        for index, offset in enumerate([(35, 11), (52, 11)]):
            if self.__facing_left_subsurface[index] is None:
                self.__facing_left_subsurface[index] = self.__sprite_sheet.subsurface(pygame.Rect(pylink_config.scale_nes_tuple_to_pylink(offset), pylink_config.PYLINK_TILE_SIZE))
                self.__facing_left_subsurface[index].set_colorkey(
                    self.__facing_left_subsurface[index].get_at((0, 0)))
                # The image in the sprite sheet is actually facing right, flip
                # it to face left
                self.__facing_left_subsurface[index] = pygame.transform.flip(
                    self.__facing_left_subsurface[index], True, False)
                # Turn off alpha so that colorkey works for transparency
                self.__facing_left_subsurface[index].set_alpha(None)
        return self.__facing_left_subsurface[step]

    __facing_up_subsurface = [None, None]
    def __get_facing_up_subsurface(self, step):
        """
        Return the subsurface that contains Link facing up.
        """
        for index, offset in enumerate([(69, 11), (86, 11)]):
            if self.__facing_up_subsurface[index] is None:
                self.__facing_up_subsurface[index] = self.__sprite_sheet.subsurface(pygame.Rect(pylink_config.scale_nes_tuple_to_pylink(offset), pylink_config.PYLINK_TILE_SIZE))
                self.__facing_up_subsurface[index].set_colorkey(
                    self.__facing_up_subsurface[index].get_at((0, 0)))
                # Turn off alpha so that colorkey works for transparency
                self.__facing_up_subsurface[index].set_alpha(None)
        return self.__facing_up_subsurface[step]

    __facing_right_subsurface = [None, None]
    def __get_facing_right_subsurface(self, step):
        """
        Return the subsurface that contains Link facing right.
        """
        for index, offset in enumerate([(35, 11), (52, 11)]):
            if self.__facing_right_subsurface[index] is None:
                self.__facing_right_subsurface[index] = self.__sprite_sheet.subsurface(
                    pygame.Rect(pylink_config.scale_nes_tuple_to_pylink(offset), pylink_config.PYLINK_TILE_SIZE))
                self.__facing_right_subsurface[index].set_colorkey(self.__facing_right_subsurface[index].get_at((0, 0)))
                # Turn off alpha so that colorkey works for transparency
                self.__facing_right_subsurface[index].set_alpha(None)
        return self.__facing_right_subsurface[step]

    __facing_down_subsurface = [None, None]
    def __get_facing_down_subsurface(self, step):
        """
        Return the subsurface that contains Link facing down.
        """
        for index, offset in enumerate([(1, 11), (18, 11)]):
            if self.__facing_down_subsurface[index] is None:
                self.__facing_down_subsurface[index] = self.__sprite_sheet.subsurface(pygame.Rect(pylink_config.scale_nes_tuple_to_pylink(offset), pylink_config.PYLINK_TILE_SIZE))
                self.__facing_down_subsurface[index].set_colorkey(
                    self.__facing_down_subsurface[index].get_at((0, 0)))
                # Turn off alpha so that colorkey works for transparency
                self.__facing_down_subsurface[index].set_alpha(None)
        return self.__facing_down_subsurface[step]

    def left_keydown(self):
        """
        This method is called when the left arrow key is pressed.
        """
        self.__facing = "left"
        self.__moving = True
        self.__current_subsurface = self.__get_facing_left_subsurface(self.__step)

    def up_keydown(self):
        """
        This method is called when the up arrow key is pressed.
        """
        self.__facing = "up"
        self.__moving = True
        self.__current_subsurface = self.__get_facing_up_subsurface(self.__step)

    def right_keydown(self):
        """
        This method is called when the right arrow key is pressed.
        """
        self.__facing = "right"
        self.__moving = True
        self.__current_subsurface = self.__get_facing_right_subsurface(self.__step)

    def down_keydown(self):
        """
        This method is called when the down arrow key is pressed.
        """
        self.__facing = "down"
        self.__moving = True
        self.__current_subsurface = self.__get_facing_down_subsurface(self.__step)

    def arrow_keyup(self):
        """
        This method is called when any arrow key is released.
        """
        self.__moving = False

    # Used to simulate a switch statement for toggle_steps.
    # This is indexed by self.__facing
    __toggle_steps_switcher = {
        "left": lambda self, step: self.__get_facing_left_subsurface(step),  # pylint: disable=protected-access
        "up": lambda self, step: self.__get_facing_up_subsurface(step),  # pylint: disable=protected-access
        "down": lambda self, step: self.__get_facing_down_subsurface(step),  # pylint: disable=protected-access
        "right": lambda self, step: self.__get_facing_right_subsurface(step)  # pylint: disable=protected-access
    }

    def toggle_steps(self):
        """
        If Link is moving, toggle the __step setting and set the
        __current_surface to the correct one with the new step.
        """
        if self.__moving:
            if self.__step == 0:
                self.__step = 1
            else:
                self.__step = 0
            self.__current_subsurface = self.__toggle_steps_switcher.get(self.__facing, lambda self, step: print("Unknown facing direction: ", self.__facing))(self, self.__step)

    def blit(self):
        """
        Blits Link to his current location on the screen.
        """
        pygame.display.get_surface().blit(self.__current_subsurface, self.__topleft)
