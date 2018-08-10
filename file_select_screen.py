"""File select screen event loop processing

Presents the file select screen and processes the user input
for it.

To go to the title screen, use file_select_screen.execute()
"""
import pygame
import pygame.locals
import numpy
import pylink_config
import tile_loader
import game_screen

_MENU = [
    {"item":"file1", "icon_location": (117, 279)},
    {"item":"file2", "icon_location": (117, 351)},
    {"item":"file3", "icon_location": (117, 423)},
    {"item":"register", "icon_location": (117, 504)},
    {"item":"elimination", "icon_location": (117, 552)}
]

#pylint: disable-msg=invalid-name
_current_menu_index = 0
#pylint: enable-msg=invalid-name

def next_menu_item(direction):
    """
    Return the next menu item in the list.

    Args:
        direction: If direction is positive, return the next item
            counting left-to-right. If direction is negative, return the
            next item counting right-to-left. If direction is 0, return
            the current item without moving. When counting, loop around
            the end of the list in both directions.

    Returns:
        dictionary: The menu item as a dictionary,
    """
    #pylint: disable-msg=invalid-name,global-statement
    global _current_menu_index
    #pylint: enable-msg=invalid-name,global-statement
    _current_menu_index += numpy.sign(direction)
    if _current_menu_index >= len(_MENU):
        _current_menu_index = 0
    elif _current_menu_index < 0:
        _current_menu_index = len(_MENU) - 1
    return _MENU[_current_menu_index]

# -v TODO out
#pylint: disable-msg=unused-argument
# -^ TODO out
def event_loop(screen, background, cursor, red_heart, pink_heart):
    """
    Run the event loop for the file select screen

    Args:
        screen: A pygame screen instance.
        background_tiles: An array of the tiles to loop through to
            animate the background.
        cursor: The pink cursor block.
        pink_heart: The pink heart used as the file selector.
        red_heart: The red heart used as the life indicator
    """
    screen.blit(background, (0, 0))
    screen.blit(pink_heart, next_menu_item(0)["icon_location"])
    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    pygame.mixer.music.play()
                    screen.blit(background, (0, 0))
                    screen.blit(
                        pink_heart,
                        next_menu_item(1)["icon_location"])
                    pygame.display.flip()
                if event.key in [pygame.K_UP, pygame.K_w]:
                    pygame.mixer.music.play()
                    screen.blit(background, (0, 0))
                    screen.blit(
                        pink_heart,
                        next_menu_item(-1)["icon_location"])
                    pygame.display.flip()

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
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=(8, 8),
        border=(1, 1),
        offset=(261, 733),
        tile_scaling=pylink_config.TILE_SCALING)
    cursor = table[0][0]
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=(8, 8),
        border=(1, 1),
        offset=(269, 733),
        tile_scaling=pylink_config.TILE_SCALING,
        colorkey_location=(0, 0))
    red_heart = table[0][0]
    pink_heart = table[0][1]
    pygame.mixer.init()
    pygame.mixer.music.load('assets/LOZ_Get_Rupee.wav')
    event_loop(game_screen, background, cursor, red_heart, pink_heart)

if __name__ == '__main__':
    # Load and display the file select screen
    game_screen.init()
    execute()
