"""
Handles the Link playable character
"""
import os
import pygame
import numpy
import overworld
import pylink_config


def should_switch_maps(next_rect):
    """
    Check to see if next_rect would be off the map area, and return
    true if it is. This would indicate that the map needs to be
    switched to a new one.
    """
    return not pylink_config.PYLINK_MAP.contains(next_rect)


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
            Link.__instance = Link()
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
            # this class' move() method will be called and, if Link
            # is moving, the self.__step setting will toggle so that the
            # code knows which of the two sprites to show.
            # Once started, the move() method will get called
            # periodically.
            pygame.time.set_timer(pylink_config.MOVE_LINK, pylink_config.LINK_MOVE_INTERVAL_MSECS)

            # Setup Link's initial position.
            # Link's top left corner ends up in the center instead of him being dead
            # center at the start, but the tiles around are clear and this works
            # just fine.
            self.facing_direction = "down"
            self.__moving = False
            self.__step = 0
            self.__facing_left_subsurface = [None, None]
            self.__facing_up_subsurface = [None, None]
            self.__facing_right_subsurface = [None, None]
            self.__facing_down_subsurface = [None, None]
            self.__current_subsurface = self.__get_facing_down_subsurface(
                self.__step)
            self.__rect = pygame.Rect(pylink_config.PYLINK_MAP.center, self.__current_subsurface.get_size())
            self.velocity = pylink_config.LINK_STOPPED_VELOCITY
            Link.__instance = self

    def __get_facing_left_subsurface(self, step):
        """
        Return the subsurface that contains Link facing_direction left.
        This gets called only when Link switches to facing_direction in this direction,
        or when he takes a step.
        """
        if self.__facing_left_subsurface[0] is None:
            self.__facing_left_subsurface[0] = self.__sprite_sheet.subsurface(
                pygame.Rect(pylink_config.scale_nes_tuple_to_pylink((35, 11)), pylink_config.scale_nes_tuple_to_pylink((16, 16))))
            self.__facing_left_subsurface[0].set_colorkey(
                self.__facing_left_subsurface[0].get_at((0, 0)))
            # The image in the sprite sheet is actually facing_direction right, flip
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
            # The image in the sprite sheet is actually facing_direction right, flip
            # it to face left
            self.__facing_left_subsurface[1] = pygame.transform.flip(
                self.__facing_left_subsurface[1], True, False)
            # Turn off alpha so that colorkey works for transparency
            self.__facing_left_subsurface[1].set_alpha(None)
        return self.__facing_left_subsurface[step]

    def __get_facing_up_subsurface(self, step):
        """
        Return the subsurface that contains Link facing_direction up.
        This gets called only when Link switches to facing_direction in this direction,
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
        Return the subsurface that contains Link facing_direction right.
        This gets called only when Link switches to facing_direction in this direction,
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
        Return the subsurface that contains Link facing_direction down.
        This gets called only when Link switches to facing_direction in this direction,
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
        self.facing_direction = "left"
        self.__moving = True
        self.velocity = pylink_config.LINK_MOVE_LEFT_VELOCITY
        self.__current_subsurface = self.__get_facing_left_subsurface(
            self.__step)
        # Not every image of Link is the same size, so recalculate
        # his bounding rectangle after possibly switching facing_direction direction.
        self.__rect = pygame.Rect(
            self.__rect.topleft, self.__current_subsurface.get_size())

    def up_keydown(self):
        """
        This method is called when the up arrow key is pressed.
        """
        self.facing_direction = "up"
        self.__moving = True
        self.velocity = pylink_config.LINK_MOVE_UP_VELOCITY
        self.__current_subsurface = self.__get_facing_up_subsurface(
            self.__step)
        # Not every image of Link is the same size, so recalculate
        # his bounding rectangle after possibly switching facing_direction direction.
        self.__rect = pygame.Rect(
            self.__rect.topleft, self.__current_subsurface.get_size())

    def right_keydown(self):
        """
        This method is called when the right arrow key is pressed.
        """
        self.facing_direction = "right"
        self.__moving = True
        self.velocity = pylink_config.LINK_MOVE_RIGHT_VELOCITY
        self.__current_subsurface = self.__get_facing_right_subsurface(
            self.__step)
        # Not every image of Link is the same size, so recalculate
        # his bounding rectangle after possibly switching facing_direction direction.
        self.__rect = pygame.Rect(
            self.__rect.topleft, self.__current_subsurface.get_size())

    def down_keydown(self):
        """
        This method is called when the down arrow key is pressed.
        """
        self.facing_direction = "down"
        self.__moving = True
        self.velocity = pylink_config.LINK_MOVE_DOWN_VELOCITY
        self.__current_subsurface = self.__get_facing_down_subsurface(
            self.__step)
        # Not every image of Link is the same size, so recalculate
        # his bounding rectangle after possibly switching facing_direction direction.
        self.__rect = pygame.Rect(
            self.__rect.topleft, self.__current_subsurface.get_size())

    def arrow_keyup(self):
        """
        This method is called when any arrow key is released.
        """
        self.__moving = False
        self.velocity = pylink_config.LINK_STOPPED_VELOCITY

    # Used to simulate a switch statement for move.
    # This is indexed by self.facing_direction
    __toggle_steps_switcher = {
        "left": lambda self, step: self.__get_facing_left_subsurface(step),  # pylint: disable=protected-access
        "up": lambda self, step: self.__get_facing_up_subsurface(step),  # pylint: disable=protected-access
        "down": lambda self, step: self.__get_facing_down_subsurface(step),  # pylint: disable=protected-access
        "right": lambda self, step: self.__get_facing_right_subsurface(step)  # pylint: disable=protected-access
    }

    def can_move_to(self, to_rect):
        """
        Determine if it is valid to move the Link rectangle
        to the to_rect location on the current map.
        Return True if it is OK, and False if not.
        If an IndexError occurs at any point in the calculations,
        assume it is not safe to move and return False

        Right now this is cheating a bit. It turns out that the portion of
        the overworld map that Link can move on is almost always sand and
        is the same color, For now, the code is using the color of the
        pixels at corners of Link's current bounding rectangle in the
        direction of movement and comparing them with the ones at the
        proposed new location. If they are the same, it is assumed that it
        must be OK to move there, because it is, apparently, just as OK to
        stay in this position. This does assume that the pixel at that
        location on the surface is the color of the pixel in the background
        which means that the pixel has to be transparent on Link's image.
        Because of this, only some directions check the midpoint while
        others do not.

        Note that the "right" and "bottom" attributes of Rect are actually
        outside the actual Rect (they are more a size than a pixel
        coordinate). This means that these values need to be adjusted when
        used in the get_at() call to get a pixel.
        """
        # Get the color of the pixel at Link's current location and at the
        # proposed next location on the corners facing_direction the move
        game_window = pygame.display.get_surface()
        try:
            if self.facing_direction == "left":
                current_locations_colors = (
                    game_window.get_at(self.__rect.midleft),
                    game_window.get_at(tuple(numpy.add(self.__rect.bottomleft, (0, -1))))
                )
                next_locations_colors = (
                    game_window.get_at(to_rect.midleft),
                    game_window.get_at(tuple(numpy.add(to_rect.bottomleft, (0, -1))))
                )
            elif self.facing_direction == "up":
                current_locations_colors = (
                    game_window.get_at(self.__rect.topleft),
                    game_window.get_at(tuple(numpy.add(self.__rect.topright, (-1, 0))))
                )
                next_locations_colors = (
                    game_window.get_at(to_rect.topleft),
                    game_window.get_at(tuple(numpy.add(to_rect.topright, (-1, 0))))
                )
            elif self.facing_direction == "right":
                current_locations_colors = (
                    game_window.get_at(tuple(numpy.add(self.__rect.bottomright, (-1, -1))))
                )
                next_locations_colors = (
                    game_window.get_at(tuple(numpy.add(to_rect.bottomright, (-1, -1))))
                )
            elif self.facing_direction == "down":
                current_locations_colors = (
                    game_window.get_at(tuple(numpy.add(self.__rect.bottomleft, (0, -1)))),
                    game_window.get_at(tuple(numpy.add(self.__rect.midbottom, (0, -1)))),
                    game_window.get_at(tuple(numpy.add(self.__rect.bottomright, (-1, -1))))
                )
                next_locations_colors = (
                    game_window.get_at(tuple(numpy.add(to_rect.bottomleft, (0, -1)))),
                    game_window.get_at(tuple(numpy.add(to_rect.midbottom, (0, -1)))),
                    game_window.get_at(tuple(numpy.add(to_rect.bottomright, (-1, -1))))
                )
            else:
                raise Exception(f"Unknown facing_direction direction: '{self.facing_direction}'")
        except IndexError:
            return False

        # Return whether they are the same or not
        return current_locations_colors == next_locations_colors

    def switch_maps(self, facing_direction):
        """
        This is called from within the move method when we are switching to a
        new map. The new map will be the one to the facing_direction from the
        current one. What this means for Link is that he needs to move to the
        opposite end of the game screen.

        This method only moves where Link will be drawn next (i.e. it updates
        self.__rect). It does NOT handle getting the tile for the next step
        because that is expected to have been taken care of in the move method
        before this one is called.

        This method also does not check for collisions. It is assumed that the
        caller (the move method) has already verified that this move should be
        done.
        """
        game_window = pylink_config.PYLINK_MAP
        if facing_direction == "right":
            self.__rect = self.__rect.move(game_window.left - self.__rect.left, 0)
        elif facing_direction == "left":
            self.__rect = self.__rect.move(game_window.right - self.__rect.right, 0)
        elif facing_direction == "up":
            self.__rect = self.__rect.move(0, game_window.bottom - self.__rect.bottom)
        elif facing_direction == "down":
            self.__rect = self.__rect.move(0, game_window.top - self.__rect.top)
        else:
            raise Exception(f"Unknown facing_direction direction: '{facing_direction}'")

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
            self.__current_subsurface = self.__toggle_steps_switcher.get(self.facing_direction, lambda self, step: print("Unknown facing_direction direction: ", self.facing_direction))(self, self.__step)

            # Not every image of Link is the same size, so recalculate
            # his bounding rectangle after taking the step
            self.__rect = pygame.Rect(
                self.__rect.topleft, self.__current_subsurface.get_size())

            # Calculate the bounding rectangle of the planned next location
            next_rect = self.__rect.move(self.velocity)

            #
            # See if it is clear to move to the next location and
            # move if it is clear to do so.
            # If the move goe off an edge of the map, switch maps and move to
            # the other side of the new map.
            # If it is not clear to move, try reducing the velocity for the
            # next time around. Essentially, if Link can't move into a spot,
            # can he squeeze into it?
            #
            if self.can_move_to(next_rect):
                self.__rect = next_rect
            elif should_switch_maps(next_rect):
                overworld.Overworld.get_instance().switch_maps(self.facing_direction)
                self.switch_maps(self.facing_direction)
            else:
                self.velocity = tuple(map(round, numpy.multiply(self.velocity, 0.5)))

    def draw(self):
        """
        Draws Link to his current location on the screen.
        """
        pygame.display.get_surface().blit(self.__current_subsurface, self.__rect.topleft)
