"""Loads images and icons for the game"""
import pygame
import pylink_config
import tile_loader
import game_screen

def file_select_background():
    """Return the background image for the file select menu."""
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=pylink_config.NES_WINDOW_SIZE,
        border=(0, 0),
        offset=(3, 504),
        final_tile_size=pylink_config.WINDOW_SIZE)
    return table[0][0]

# def intro_text():
#     """
#     Load the intro text and treasure list.
#     """
#     table = tile_loader.load_tile_table(
#         filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
#         original_tile_size=(252, 24),
#         border=(0, 0),
#         offset=(260, 609),
#         tile_scaling=pylink_config.TILE_SCALING,
#         colorkey_location=(0, 0))
#     return table[0][0]

def pink_heart():
    """Return the pink heart image."""
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=(8, 8),
        border=(0, 0),
        offset=(278, 734),
        tile_scaling=pylink_config.TILE_SCALING,
        colorkey_location=(0, 0))
    return table[0][0]

def red_heart():
    """Return the red heart image."""
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=(8, 8),
        border=(0, 0),
        offset=(270, 734),
        tile_scaling=pylink_config.TILE_SCALING,
        colorkey_location=(0, 0))
    return table[0][0]

def pink_cursor():
    """Return the red heart image."""
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=(8, 8),
        border=(0, 0),
        offset=(262, 734),
        tile_scaling=pylink_config.TILE_SCALING)
    return table[0][0]

if __name__ == '__main__':
    # Draw the loaded and scaled tiles on the screen
    game_screen.init()
    game_screen.blit(pink_cursor(), (0, 0))
    game_screen.blit(red_heart(), (32, 0))
    game_screen.blit(pink_heart(), (64, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
