"""File select screen event loop processing

Presents the file select screen and processes the user input
for it.

To go to the title screen, use file_select_screen.execute()
"""
import pygame
import pygame.locals
import pylink_config
import tile_loader
import game_screen

_START_TITLE_FADE_AT_SECS = 8.0
_FINISH_TITLE_FADE_AT_SECS = 16.0

def event_loop(screen, background):
    """
    Run the event loop for the file select screen

    Args:
        screen: A pygame screen instance.
        background_tiles: An array of the tiles to loop through to
            animate the background.
    """
    screen.blit(background, (0, 0))
    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return

def execute():
    """
    Show the file select screen and process user input
    """
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=pylink_config.NES_WINDOW_SIZE,
        border=(0, 0),
        offset=(3, 504),
        final_tile_size=pylink_config.WINDOW_SIZE)
    background = table[0][0]
    event_loop(game_screen, background)

if __name__ == '__main__':
    # Load and display the file select screen
    game_screen.init()
    execute()
