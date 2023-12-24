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
    Link.get_instance(). That function will take care of creating the instance
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
        DO NOT USE 'Link()', use 'Link.get_instance()' instead.
        """
        if Link.__instance is not None:
            raise Exception("This class is a singleton. Use 'Link.get_instance()' instead of 'Link()'")
        else:
            # Load the sprite sheet with all of Link's images, and scale it
            # to the game's scale.
            self.__sprite_sheet = pygame.image.load(os.path.join(
                'assets', 'NES-TheLegendofZelda-Link.png'))
            self.__sprite_sheet = pygame.transform.scale(self.__sprite_sheet, tuple(
                pylink_config.NES_TO_PYLINK_SCALE_FACTOR * numpy.array(self.__sprite_sheet.get_size())))
            self.__sprite_sheet.convert()

            # Start the periodic event for changing steps. When this fires,
            # this class' move() method will be caled and, if Link
            # is moving, the self.__step setting will toggle so that the
            # code knows which of the two sprites to show.
            # Once started, the move() method will get called
            # periodically.
            pygame.time.set_timer(pylink_config.MOVE_LINK, pylink_config.LINK_MOVE_INTERVAL_MSECS)

            # Setup Link's initial position.
            # Link's topleft corner ends up in the center instead of him being dead
            # center at the start, but the tiles around are clear and this works
            # just fine.
            self.__facing = "down"
            self.__moving = False
            self.__step = 0
            self.__facing_left_subsurface = [None, None]
            self.__facing_up_subsurface = [None, None]
            self.__facing_right_subsurface = [None, None]
            self.__facing_down_subsurface = [None, None]
            self.__current_subsurface = self.__get_facing_down_subsurface(
                self.__step)
            self.__rect = pygame.Rect(pylink_config.PYLINK_MAP.center, self.__current_subsurface.get_size())
            self.__velocity = pylink_config.LINK_STOPPED_VELOCITY
            Link.__instance = self

    def __get_facing_left_subsurface(self, step):
        """
        Return the subsurface that contains Link facing left.
        This gets called only when Link switches to facing in this direction,
        or when he takes a step.
        """
        if self.__facing_left_subsurface[0] is None:
            self.__facing_left_subsurface[0] = self.__sprite_sheet.subsurface(
                pygame.Rect(pylink_config.scale_nes_tuple_to_pylink((35, 11)), pylink_config.scale_nes_tuple_to_pylink((16, 16))))
            self.__facing_left_subsurface[0].set_colorkey(
                self.__facing_left_subsurface[0].get_at((0, 0)))
            # The image in the sprite sheet is actually facing right, flip
            # it to face left
            self.__facing_left_subsurface[0] = pygame.transform.flip(
                self.__facing_left_subsurface[0], True, False)
            # Turn off alpha so that colorkey works for transparency
            self.__facing_left_subsurface[0].set_alpha(None)

        if self.__facing_left_subsurface[1] is None:
            self.__facing_left_subsurface[1] = self.__sprite_sheet.subsurface(
                pygame.Rect(pylink_config.scale_nes_tuple_to_pylink((52, 12)), pylink_config.scale_nes_tuple_to_pylink((15, 15))))
            self.__facing_left_subsurface[1].set_colorkey(
                self.__facing_left_subsurface[1].get_at((0, 0)))
            # The image in the sprite sheet is actually facing right, flip
            # it to face left
            self.__facing_left_subsurface[1] = pygame.transform.flip(
                self.__facing_left_subsurface[1], True, False)
            # Turn off alpha so that colorkey works for transparency
            self.__facing_left_subsurface[1].set_alpha(None)
        return self.__facing_left_subsurface[step]

    def __get_facing_up_subsurface(self, step):
        """
        Return the subsurface that contains Link facing up.
        This gets called only when Link switches to facing in this direction,
        or when he takes a step.
        """
        for index, offset in enumerate([(69, 11), (86, 11)]):
            if self.__facing_up_subsurface[index] is None:
                self.__facing_up_subsurface[index] = self.__sprite_sheet.subsurface(pygame.Rect(
                    pylink_config.scale_nes_tuple_to_pylink(offset), pylink_config.scale_nes_tuple_to_pylink((14, 16))))
                self.__facing_up_subsurface[index].set_colorkey(
                    self.__facing_up_subsurface[index].get_at((0, 0)))
                # Turn off alpha so that colorkey works for transparency
                self.__facing_up_subsurface[index].set_alpha(None)
        return self.__facing_up_subsurface[step]

    def __get_facing_right_subsurface(self, step):
        """
        Return the subsurface that contains Link facing right.
        This gets called only when Link switches to facing in this direction,
        or when he takes a step.
        """
        if self.__facing_right_subsurface[0] is None:
            self.__facing_right_subsurface[0] = self.__sprite_sheet.subsurface(
                pygame.Rect(pylink_config.scale_nes_tuple_to_pylink((35, 11)), pylink_config.scale_nes_tuple_to_pylink((16, 16))))
            self.__facing_right_subsurface[0].set_colorkey(
                self.__facing_right_subsurface[0].get_at((0, 0)))
            # Turn off alpha so that colorkey works for transparency
            self.__facing_right_subsurface[0].set_alpha(None)
        if self.__facing_right_subsurface[1] is None:
            self.__facing_right_subsurface[1] = self.__sprite_sheet.subsurface(
                pygame.Rect(pylink_config.scale_nes_tuple_to_pylink((52, 12)), pylink_config.scale_nes_tuple_to_pylink((15, 15))))
            self.__facing_right_subsurface[1].set_colorkey(
                self.__facing_right_subsurface[1].get_at((0, 0)))
            # Turn off alpha so that colorkey works for transparency
            self.__facing_right_subsurface[1].set_alpha(None)
        return self.__facing_right_subsurface[step]

    def __get_facing_down_subsurface(self, step):
        """
        Return the subsurface that contains Link facing down.
        This gets called only when Link switches to facing in this direction,
        or when he takes a step.
        """
        for index, offset in enumerate([(1, 11), (18, 11)]):
            if self.__facing_down_subsurface[index] is None:
                self.__facing_down_subsurface[index] = self.__sprite_sheet.subsurface(pygame.Rect(
                    pylink_config.scale_nes_tuple_to_pylink(offset), pylink_config.scale_nes_tuple_to_pylink((15, 16))))
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
        self.__velocity = pylink_config.LINK_MOVE_LEFT_VELOCITY
        self.__current_subsurface = self.__get_facing_left_subsurface(
            self.__step)
        # Not every image of Link is the same size, so recalculate the
        # his bounding rectangle after possibly switching facing direction.
        self.__rect = pygame.Rect(
            self.__rect.topleft, self.__current_subsurface.get_size())

    def up_keydown(self):
        """
        This method is called when the up arrow key is pressed.
        """
        self.__facing = "up"
        self.__moving = True
        self.__velocity = pylink_config.LINK_MOVE_UP_VELOCITY
        self.__current_subsurface = self.__get_facing_up_subsurface(
            self.__step)
        # Not every image of Link is the same size, so recalculate the
        # his bounding rectangle after possibly switching facing direction.
        self.__rect = pygame.Rect(
            self.__rect.topleft, self.__current_subsurface.get_size())

    def right_keydown(self):
        """
        This method is called when the right arrow key is pressed.
        """
        self.__facing = "right"
        self.__moving = True
        self.__velocity = pylink_config.LINK_MOVE_RIGHT_VELOCITY
        self.__current_subsurface = self.__get_facing_right_subsurface(
            self.__step)
        # Not every image of Link is the same size, so recalculate the
        # his bounding rectangle after possibly switching facing direction.
        self.__rect = pygame.Rect(
            self.__rect.topleft, self.__current_subsurface.get_size())

    def down_keydown(self):
        """
        This method is called when the down arrow key is pressed.
        """
        self.__facing = "down"
        self.__moving = True
        self.__velocity = pylink_config.LINK_MOVE_DOWN_VELOCITY
        self.__current_subsurface = self.__get_facing_down_subsurface(
            self.__step)
        # Not every image of Link is the same size, so recalculate the
        # his bounding rectangle after possibly switching facing direction.
        self.__rect = pygame.Rect(
            self.__rect.topleft, self.__current_subsurface.get_size())

    def arrow_keyup(self):
        """
        This method is called when any arrow key is released.
        """
        self.__moving = False
        self.__velocity = pylink_config.LINK_STOPPED_VELOCITY

    # Used to simulate a switch statement for move.
    # This is indexed by self.__facing
    __toggle_steps_switcher = {
        "left": lambda self, step: self.__get_facing_left_subsurface(step),  # pylint: disable=protected-access
        "up": lambda self, step: self.__get_facing_up_subsurface(step),  # pylint: disable=protected-access
        "down": lambda self, step: self.__get_facing_down_subsurface(step),  # pylint: disable=protected-access
        "right": lambda self, step: self.__get_facing_right_subsurface(step)  # pylint: disable=protected-access
    }

    def __it_is_ok_to_move(self, to_rect):
        """
        Determine if it is valid to move the Link rectangle
        to the to_rect location on the current map.
        Return True if it is OK, and False if not.
        If there an IndexError occurs at any point in the calculations,
        assume it is not safe to move and return False

        Right now this is cheating a bit and using the color of the
        pixels at corners of Link's current bounding rectangle in the
        direction of movement and comparing them with the ones at the
        proposed newn location. If they are the same, it is assumed that it
        must be OK to move there, because it is, apparanetly, just as OK to
        stay in this position. This does assume that the pixel at that
        location on the surface is the color of the pixel in the background
        which means that the pixel has to be transparent on Link's image.
        Because of this, only some directions check the midpoint while
        others do not.
        """
        # Get the color of the pixel at Link's current location and at the
        # propesed next location on the corners facing the move
        try:
            if self.__facing == "left":
                current_locations_colors = (
                    pygame.display.get_surface().get_at(self.__rect.midleft),
                    pygame.display.get_surface().get_at(self.__rect.bottomleft)
                )
                next_locations_colors = (
                    pygame.display.get_surface().get_at(to_rect.midleft),
                    pygame.display.get_surface().get_at(to_rect.bottomleft)
                )
            elif self.__facing == "up":
                current_locations_colors = (
                    pygame.display.get_surface().get_at(self.__rect.midleft),
                    pygame.display.get_surface().get_at(self.__rect.midright)
                )
                next_locations_colors = (
                    pygame.display.get_surface().get_at(to_rect.midleft),
                    pygame.display.get_surface().get_at(to_rect.midright)
                )
            elif self.__facing == "right":
                current_locations_colors = (
                    pygame.display.get_surface().get_at(self.__rect.midright),
                    pygame.display.get_surface().get_at(self.__rect.bottomright)
                )
                next_locations_colors = (
                    pygame.display.get_surface().get_at(to_rect.midright),
                    pygame.display.get_surface().get_at(to_rect.bottomright)
                )
            elif self.__facing == "down":
                current_locations_colors = (
                    pygame.display.get_surface().get_at(self.__rect.bottomleft),
                    pygame.display.get_surface().get_at(self.__rect.midbottom),
                    pygame.display.get_surface().get_at(self.__rect.bottomright)
                )
                next_locations_colors = (
                    pygame.display.get_surface().get_at(to_rect.bottomleft),
                    pygame.display.get_surface().get_at(to_rect.midbottom),
                    pygame.display.get_surface().get_at(to_rect.bottomright)
                )
            else:
                raise Exception("Unknown facing direction: '" + self.__facing + "'")
        except IndexError:
            return False

        # Return whether they are the same or not
        return current_locations_colors == next_locations_colors

    def move(self):
        """
        If Link is moving, toggle the __step setting, set the
        __current_surface to the correct one with the new step,
        and shift the location
        """
        if self.__moving:
            # Change the step image.
            if self.__step == 0:
                self.__step = 1
            else:
                self.__step = 0
            self.__current_subsurface = self.__toggle_steps_switcher.get(self.__facing, lambda self, step: print("Unknown facing direction: ", self.__facing))(self, self.__step)

            # Not every image of Link is the same size, so recalculate the
            # his bounding rectangle after taking the step
            self.__rect = pygame.Rect(
                self.__rect.topleft, self.__current_subsurface.get_size())

            # Calculate the bounding rectangle of the planned next location
            next_rect = self.__rect.move(self.__velocity)

            # See if it is clear to move to the next location and
            # move if it is clear to do so
            if self.__it_is_ok_to_move(next_rect):
                self.__rect = self.__rect.move(self.__velocity)

    def blit(self):
        """
        Blits Link to his current location on the screen.
        """
        pygame.display.get_surface().blit(self.__current_subsurface, self.__rect.topleft)
