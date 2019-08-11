"""
pylink3 - a Python3 version of NES Legend of Zelda

Done just for fun and for programming practice.
All copyrights are by they original owners.
"""
import sys
import pygame
import pylink_config
import overworld

if __name__ == '__main__':
    # Initialize the pygame engine
    pygame.init()
    pygame.display.set_caption('The Legend of Zelda')

    # Initialize the screen
    screen = pygame.display.set_mode(pylink_config.PYLINK_WINDOW.size)  # pylint: disable=invalid-name
    screen.fill((0, 0, 0))
    pygame.display.flip()

    # Load the overworld sheet
    overworld.init()
    screen.blit(overworld.submap(7, 7), pylink_config.PYLINK_MAP)
    pygame.display.flip()

    # Init the frame rate font
    fps_font = pygame.font.Font(None, 30)  # pylint: disable=invalid-name

    # Create a box for the score board
    score_board = pygame.Surface(pylink_config.PYLINK_SCOREBOARD.size)  # pylint: disable=invalid-name
    score_board.fill((0, 0, 0))
    score_board.convert()
    score_board_rect = score_board.get_rect()  # pylint: disable=invalid-name

    # Initialize the clock to keep track of frame rate
    clock = pygame.time.Clock() # pylint: disable=invalid-name

while 1:
    # Check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Update the clock
    clock.tick()
    score_board.fill((0, 0, 0))
    screen.blit(score_board, pylink_config.PYLINK_SCOREBOARD)
    fps = int(clock.get_fps())  # pylint: disable=invalid-name
    screen.blit(fps_font.render(str(fps), True, pygame.Color('white')), pylink_config.PYLINK_SCOREBOARD)

    # Update the screen
    pygame.display.update(pylink_config.PYLINK_SCOREBOARD)
