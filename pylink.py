"""pylink - a Python version of NES Legend of Zelda

Done just for fun and for programming practice.
All copyrights are by they original owners.
"""
import pygame
import pygame.locals
import pylink_config
import tile_loader

if __name__=='__main__':
    """Draw the loaded and scaled tiles on the screen"""
    pygame.init()
    screen = pygame.display.set_mode(pylink_config.window_size)
    screen.fill((0, 0, 0))
    table = tile_loader.load_tile_table(
        filename = "assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size = pylink_config.nes_window_size,
        border = (3, 4),
        final_tile_size = pylink_config.window_size)
    screen.blit(table[2][0], (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
