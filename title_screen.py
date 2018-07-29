"""Title screen event loop processing

Presents the animated title screen and waits for the user to hit
a key. Then transitions off the screen.

To go to the title screen, use title_screen.go()
"""
import sys
import pygame
import pygame.locals
import pylink_config
import tile_loader
import itertools
import numpy

def event_loop(screen, background_tiles):
    """Runs the event loop for the title screen

    Inputs:
        screen - A pygame screen instance.
        background_tiles - An array of the tiles to loop through to animate the screen
    """
    screen.fill((0, 0, 0))
    pygame.display.flip()
    background_loop = itertools.cycle(background_tiles)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                sys.exit()
        screen.blit(next(background_loop), (0, 0))
        pygame.display.flip()
        pygame.time.wait(150)

def go(screen):
    """Shows the title screen and waits for the user to hit 'start' (any key)

    Inputs:
        screen - A pygame screen instance.
    """
    table = tile_loader.load_tile_table(
        filename = "assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size = pylink_config.nes_window_size,
        border = (3, 3),
        offset = (0, 1),
        final_tile_size = pylink_config.window_size)
    background_tiles = [
        table[0][0],
        table[0][1],
        table[1][0],
        table[1][1],
        table[1][0],
        table[0][1]
    ]
    event_loop(screen, background_tiles)

if __name__=='__main__':
    """Draw the loaded and scaled tiles on the screen"""
    pygame.init()
    screen = pygame.display.set_mode(pylink_config.window_size)
    go(screen)
