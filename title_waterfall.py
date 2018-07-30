"""Waterfall animation for the title screen"""
import pygame
import pygame.locals
import pylink_config
import tile_loader

def background():
    table = tile_loader.load_tile_table(
        filename = "assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size = (32, 59),
        border = (6, 0),
        offset = (340, 513),
        tile_scaling = pylink_config.tile_scaling)
    return table[0][0]

def waves():
    table = tile_loader.load_tile_table(
        filename = "assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size = (32, 59),
        border = (6, 0),
        offset = (340, 513),
        tile_scaling = pylink_config.tile_scaling,
        colorkey_location = (0, 0))
    return table[0][1]

if __name__=='__main__':
    """Draw the loaded and scaled tiles on the screen"""
    pygame.init()
    screen = pygame.display.set_mode(pylink_config.window_size)
    screen.fill((0, 0, 0))
    table = tile_loader.load_tile_table(
        filename = "assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size = (32, 59),
        border = (6, 0),
        offset = (340, 513),
        tile_scaling = pylink_config.tile_scaling)
    screen.blit(background(), (0,0))
    screen.blit(waves(), (192, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
