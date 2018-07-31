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
import title_waterfall

__shift_waves = False
"""If true, shift waves down this time through the event loop"""

def event_loop(screen, background_tiles, waterfall_background, waterfall_waves, waterfall_spray):
    """Runs the event loop for the title screen

    Inputs:
        screen - A pygame screen instance.
        background_tiles - An array of the tiles to loop through to animate the background
        waterfall_background - The tile for the background of the waterfall
        waterfall_waves - The tile for the waves on the waterfall
        waterfall_spray - An array of the tiles to loop through to animate the spray at
            the top of the waterfall
    """
    global __shift_waves
    screen.fill((0, 0, 0))
    pygame.display.flip()
    background_loop = itertools.cycle(background_tiles)
    spray_loop = itertools.cycle(waterfall_spray)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                sys.exit()
        screen.blit(next(background_loop), (0, 0))
        screen.blit(next(spray_loop), (237, 528))
        screen.blit(waterfall_background, (240, 543))
        if (__shift_waves):
            screen.blit(waterfall_waves, (240, 543))
        else:
            screen.blit(waterfall_waves, (240, 513))
        __shift_waves = not __shift_waves
        pygame.display.flip()
        pygame.time.wait(75)

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
    # When the animation loop runs, the same background is shown
    # for two frames in a row. The waterfall, moves at twice the rate
    # and this allows for that movement to occur on every loop through.
    # Note that the background images undulate back and forth through
    # the list
    background_tiles = [
        table[0][0], table[0][0],
        table[0][1], table[0][1],
        table[1][0], table[1][0],
        table[1][1], table[1][1],
        table[1][0], table[1][0],
        table[0][1], table[0][1]
    ]
    table = tile_loader.load_tile_table(
        filename = "assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size = (32, 59),
        border = (6, 0),
        offset = (340, 51),
        final_tile_size = pylink_config.window_size)
    waterfall_background = title_waterfall.background()
    waterfall_waves = title_waterfall.waves()
    waterfall_spray = title_waterfall.spray();
    event_loop(screen, background_tiles, waterfall_background, waterfall_waves, waterfall_spray)

if __name__=='__main__':
    """Draw the loaded and scaled tiles on the screen"""
    pygame.init()
    screen = pygame.display.set_mode(pylink_config.window_size)
    go(screen)
