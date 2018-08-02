"""Scrolling intro text for the title screen"""
import pygame
import pygame.locals
import numpy
import pylink_config
import tile_loader

def location(elaspsed_secs):
    """Returns the (x, y) location to put the title screen at for the given elaspsed_secs time"""
    if (elaspsed_secs < 16.0):
        return tuple(map(int, numpy.multiply((2, pylink_config.nes_window_size[1]), pylink_config.tile_scaling)))

    if (16.0 <= elaspsed_secs < 23.5):
        return tuple(map(int, numpy.multiply((2, pylink_config.nes_window_size[1] - (29.467 * (elaspsed_secs - 16.0))), pylink_config.tile_scaling)))

    if (23.5 <= elaspsed_secs < 27.5):
        return tuple(map(int, numpy.multiply((2, pylink_config.nes_window_size[1] - 221.25), pylink_config.tile_scaling)))

    if (27.5 <= elaspsed_secs <= 74.5):
        return tuple(map(int, numpy.multiply((2, pylink_config.nes_window_size[1] - 221.25 - ((713.0 / (74.5 - 27.5)) * (elaspsed_secs - 27.5))), pylink_config.tile_scaling)))

def intro_text():
    """Loads the intro text and treasure list"""
    table = tile_loader.load_tile_table(
        filename = "assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size = (252, 960),
        border = (0, 0),
        offset = (523, 14),
        tile_scaling = pylink_config.tile_scaling,
        colorkey_location = (0, 0))
    return table[0][0]

if __name__=='__main__':
    """Draw the loaded and scaled tiles on the screen"""
    pygame.init()
    screen = pygame.display.set_mode(pylink_config.window_size)
    screen.fill((0, 0, 0))
    screen.blit(intro_text(), (2 * pylink_config.tile_scaling[0], 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
