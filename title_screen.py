"""Title screen event loop processing

Presents the animated title screen and waits for the user to hit
a key. Then transitions off the screen.

To go to the title screen, use title_screen.go()
"""
import sys
import time
import pygame
import pygame.locals
import pylink_config
import tile_loader
import itertools
import numpy
import title_waterfall
import title_intro_text

def alphaValue(elapsed_ns):
    """Used to fade out the screen between 8 and 16 seconds in"""
    if (elapsed_ns < 8.0):
        return 0
    if (elapsed_ns > 16.0):
        return 255
    return int((elapsed_ns - 8.0) * (255.0 / 8.0))

def event_loop(
    screen,
    background_tiles,
    waterfall_background,
    waterfall_waves,
    waterfall_spray,
    intro_text):
    """Runs the event loop for the title screen

    Inputs:
        screen - A pygame screen instance.
        background_tiles - An array of the tiles to loop through to animate the background
        waterfall_background - The tile for the background of the waterfall
        waterfall_waves - The tile for the waves on the waterfall
        waterfall_spray - An array of the tiles to loop through to animate the spray at
            the top of the waterfall
        intro_text - The intro text to scroll as one image.
    """
    title_frametime_msecs = 75
    shift_waves = False
    start_time_secs = time.time();

    screen.fill((0, 0, 0))
    pygame.display.flip()
    background_loop = itertools.cycle(background_tiles)
    spray_loop = itertools.cycle(waterfall_spray)
    alphaSurface = pygame.Surface(pylink_config.window_size)
    alphaSurface.fill((0, 0, 0))
    alphaSurface.set_alpha(0)
    while 1:
        elapsed_secs = time.time() - start_time_secs
        if (elapsed_secs >= 82.75):
            elapsed_secs = 0
            start_time_secs = time.time();
            pygame.mixer.music.play()

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return

        if (elapsed_secs < 16):
            # Show waterfall
            screen.blit(next(background_loop), (0, 0))
            screen.blit(next(spray_loop), (237, 528))
            screen.blit(waterfall_background, (240, 543))
            if (shift_waves):
                screen.blit(waterfall_waves, (240, 543))
            else:
                screen.blit(waterfall_waves, (240, 513))
            shift_waves = not shift_waves
            alphaSurface.set_alpha(alphaValue(elapsed_secs))
            screen.blit(alphaSurface,(0,0))
            pygame.display.flip()
            pygame.time.wait(title_frametime_msecs)
        elif (16 <= elapsed_secs < 23.5):
            # scroll intro story up
            screen.fill((0, 0, 0))
            screen.blit(intro_text, title_intro_text.location(elapsed_secs))
            pygame.display.flip()
        elif (23.5 <= elapsed_secs < 27.5):
            # pause intro story
            pass
        elif (27.5 <= elapsed_secs < 74.5):
            # scroll rest of intro/items list
            screen.fill((0, 0, 0))
            screen.blit(intro_text, title_intro_text.location(elapsed_secs))
            pygame.display.flip()
        elif (74.5 <= elapsed_secs):
            # pause item list
            pass

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
    waterfall_spray = title_waterfall.spray()
    intro_text = title_intro_text.intro_text()
    pygame.mixer.music.load('assets/01Intro.mp3')
    pygame.mixer.music.play()
    event_loop(screen, background_tiles, waterfall_background, waterfall_waves, waterfall_spray, intro_text)
    pygame.mixer.music.stop()

if __name__=='__main__':
    """Draw the loaded and scaled tiles on the screen"""
    pygame.init()
    screen = pygame.display.set_mode(pylink_config.window_size)
    go(screen)
