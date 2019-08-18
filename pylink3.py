"""
pylink3 - a Python3 version of NES Legend of Zelda

Done just for fun and for programming practice.
All copyrights are by they original owners.
"""
import pygame
import pylink_config
from events import Events
from link import Link
from overworld import Overworld

if __name__ == '__main__':
    # Initialize the pygame engine
    pygame.init()
    pygame.display.set_caption('The Legend of Zelda')

    # Initialize the screen
    screen = pygame.display.set_mode(pylink_config.PYLINK_WINDOW.size)  # pylint: disable=invalid-name
    screen.fill((0, 0, 0))
    pygame.display.flip()

    # Load the overworld sheet and display the starting position
    overworld = Overworld.get_instance()  # pylint: disable=invalid-name

    # Load Link's sprite sheet and place him at the starting position
    # on the map.
    link = Link.get_instance()  # pylint: disable=invalid-name

    # Init the frame rate font
    fps_font = pygame.font.Font(None, 30)  # pylint: disable=invalid-name

    # Create a box for the score board
    score_board = pygame.Surface(pylink_config.PYLINK_SCOREBOARD.size)  # pylint: disable=invalid-name
    score_board.fill((0, 0, 0))
    score_board.convert()
    score_board_rect = score_board.get_rect()  # pylint: disable=invalid-name

    # Initialize the clock to keep track of frame rate
    clock = pygame.time.Clock() # pylint: disable=invalid-name

    # Initialize the events handler.
    events = Events.get_instance()  # pylint: disable=invalid-name

    while 1:
        # Check for and process events
        events.process()

        # Update the clock
        clock.tick()
        score_board.fill((0, 0, 0))
        screen.blit(score_board, pylink_config.PYLINK_SCOREBOARD)
        fps = int(clock.get_fps())  # pylint: disable=invalid-name
        screen.blit(fps_font.render(str(fps), True, pygame.Color('white')), pylink_config.PYLINK_SCOREBOARD)

        # Redraw the map area one layer at a time
        overworld.blit()
        link.blit()

        # Flip the screen to update everything
        # Update the scoreboard section
        # pygame.display.update(pylink_config.PYLINK_SCOREBOARD)
        pygame.display.flip()
