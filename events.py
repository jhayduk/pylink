"""
Detects and dispaches event.s
"""
import sys
import pygame
import pylink_config
from link import Link

class Events(object):
    """
    The event handler.
    This detects events and distributes them to other objects.
    This is a singleton object and must only be accessed with
    Events.getInstance(). That function will take care of creating the
    instance the first time it is called.
    """
    __instance = None

    @staticmethod
    def get_instance():
        """
        Get an instance of the Events object.
        Use this instead of 'new Events()' to get the player object.
        """
        if Events.__instance is None:
            Events()
        return Events.__instance

    def __init__(self):
        """
        Virtually private constructor.
        DO NOT USE 'new Events()', use 'Events.get_instance()' instead.
        """
        if Events.__instance is not None:
            raise Exception("This class is a singleton. Use 'Events.get_instance()' instead of 'new Events()'")
        else:
            self.link = Link.get_instance()
            Events.__instance = self

    # In order to mimic a switch statement, the functions called for
    # each keydown event are listed here and then called from the
    # __event_switcher whenever a keydown event occurs
    __keydown_switcher = {
        pygame.K_LEFT: lambda self: self.link.left_keydown(),
        pygame.K_UP: lambda self: self.link.up_keydown(),
        pygame.K_RIGHT: lambda self: self.link.right_keydown(),
        pygame.K_DOWN: lambda self: self.link.down_keydown()
    }

    # In order to mimic a switch statement, the functions called for
    # each keyup event are listed here and then called from the
    # __event_switcher whenever a keyup event occurs
    __keyup_switcher = {
        pygame.K_LEFT: lambda self: self.link.arrow_keyup(),
        pygame.K_UP: lambda self: self.link.arrow_keyup(),
        pygame.K_RIGHT: lambda self: self.link.arrow_keyup(),
        pygame.K_DOWN: lambda self: self.link.arrow_keyup()
    }

    # In order to mimic a switch statement, the functions called for
    # each of the events received are listed here and then called within the
    # event loop when a particular event occurs
    __event_switcher = {
        pygame.QUIT: lambda self, event: sys.exit(),
        pygame.KEYDOWN: lambda self, event: self.__keydown_switcher.get(event.key, lambda self: None)(self),  # pylint: disable=protected-access
        pygame.KEYUP: lambda self, event: self.__keyup_switcher.get(event.key, lambda self: None)(self),  # pylint: disable=protected-access
        pylink_config.MOVE_LINK: lambda self, event: self.link.move()
    }

    def process(self):
        """
        Process any events in the queue.
        This is expected to be called once each frame from the main loop.
        """
        for event in pygame.event.get():
            self.__event_switcher.get(event.type, lambda self, event: None)(self, event)
