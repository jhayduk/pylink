"""Waterfall animation for the title screen"""
import pygame
import pygame.locals
import pylink_config
import tile_loader

def background():
    """Return the waterfall's background image."""
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=(32, 59),
        border=(6, 0),
        offset=(340, 513),
        tile_scaling=pylink_config.TILE_SCALING)
    return table[0][0]

def waves():
    """Return the waves' image"""
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=(32, 59),
        border=(6, 0),
        offset=(340, 513),
        tile_scaling=pylink_config.TILE_SCALING,
        colorkey_location=(0, 0))
    return table[0][1]

def spray():
    """Return an array of images for the spray at the waterfall top."""
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=(34, 10),
        border=(0, 0),
        offset=(422, 521),
        tile_scaling=pylink_config.TILE_SCALING,
        colorkey_location=(0, 0))
    return [
        table[0][0],
        table[1][0],
        table[2][0],
        table[3][0],
        table[4][0]
    ]

if __name__ == '__main__':
    # Draw the loaded and scaled tiles on the screen.
    pygame.init()
    MAIN_SCREEN = pygame.display.set_mode(pylink_config.WINDOW_SIZE)
    MAIN_SCREEN.fill((0, 0, 0))
    MAIN_SCREEN.blit(background(), (0, 0))
    MAIN_SCREEN.blit(waves(), (192, 0))
    SPRAY_LIST = spray()
    for index in range(0, 5):
        MAIN_SCREEN.blit(SPRAY_LIST[index], (384, 24 + (30 * index)))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
