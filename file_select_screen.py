"""File select screen event loop processing

Presents the file select screen and processes the user input
for it.

To go to the title screen, use file_select_screen.execute()
"""
import pickle
import pygame
import pygame.locals
import numpy
import game_screen
import images
import registration_screen

# -v TBD - Take this out
#pylint: disable-msg=duplicate-code
# -^ TBD - Take this out
#pylint: disable-msg=invalid-name
_menu = [
    {"item":"file1", "marker_location": (117, 279)},
    {"item":"file2", "marker_location": (117, 351)},
    {"item":"file3", "marker_location": (117, 423)},
    {"item":"register", "marker_location": (117, 504)},
    {"item":"elimination", "marker_location": (117, 552)}
]
_REGISTER_ITEM_INDEX = len(_menu) - 2
_ELIMINATION_ITEM_INDEX = len(_menu) - 1

_current_menu_index = 0
#pylint: enable-msg=invalid-name

def set_selectable(menu_index, selectable):
    """Set the selectable flag for the given item in the menu"""
    _menu[menu_index]["selectable"] = selectable

def load_save_game(filename):
    """
    Loads the named filename to a dictionary.

    Args:
        filename: The name of the save game file. Technically, this
            could be anything, but game1.sav, game2.sav and game3.sav
            are the only officially used names.

    Returns:
        A dictionary containing the saved game parameters, or None if
        there is no file by that name or if there was some trouble while
        loading it.
    """
    try:
        return pickle.load(open(filename, "rb"))
    except IOError:
        return None

def next_menu_item(direction):
    """
    Return the next selectable menu item in the list.

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
    if _current_menu_index >= len(_menu):
        _current_menu_index = 0
    elif _current_menu_index < 0:
        _current_menu_index = len(_menu) - 1
    if _menu[_current_menu_index].get("selectable") or direction == 0:
        return _menu[_current_menu_index]
    # Call again to find the next selectable menu item
    return next_menu_item(direction)

def init_menu():
    """
    Loads current save game info and initializes file select info
    """
    #pylint: disable-msg=invalid-name,global-statement
    global _menu
    global _current_menu_index
    #pylint: enable-msg=invalid-name,global-statement

    # Set elimination as non-selectable until we see a file load
    _menu[_ELIMINATION_ITEM_INDEX]['selectable'] = False

    num_selectable_files = 0
    for index in range(3):
        _menu[index]['save_game'] = load_save_game(
            'game' + str(index) + '.sav')
        if _menu[index]['save_game'] is not None:
            _menu[index]['selectable'] = True
            num_selectable_files += 1
            # Actual file means elimination is now possible
            _menu[_ELIMINATION_ITEM_INDEX]['selectable'] = True

    _menu[_REGISTER_ITEM_INDEX]['selectable'] = num_selectable_files < 3

    # Now, step to first item so that the next_menu_item logic
    # can find the next selectable menu item
    _current_menu_index = len(_menu) - 1
    next_menu_item(1)

def event_loop(background, pink_heart):
    """
    Run the event loop for the file select screen

    Args:
        background_tiles: An array of the tiles to loop through to
            animate the background.
        pink_heart: The pink heart used as the file selector.

    Returns:
        save_game: A dictionary containing the selected save game
            information, or None if the game should exit.
    """
    game_screen.blit(background, (0, 0))
    game_screen.blit(pink_heart, next_menu_item(0)["marker_location"])
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
                    game_screen.blit(background, (0, 0))
                    game_screen.blit(
                        pink_heart,
                        next_menu_item(1)["marker_location"])
                    pygame.display.flip()
                if event.key in [pygame.K_UP, pygame.K_w]:
                    pygame.mixer.music.play()
                    game_screen.blit(background, (0, 0))
                    game_screen.blit(
                        pink_heart,
                        next_menu_item(-1)["marker_location"])
                    pygame.display.flip()
                if event.key == pygame.K_RETURN:
                    if _current_menu_index == _REGISTER_ITEM_INDEX:
                        registration_screen.execute()

def execute():
    """
    Show the file select screen and process user input

    Returns:
        save_game: A dictionary containing the selected save game
            information, or None if the game should exit.
    """
    pygame.mixer.init()
    pygame.mixer.music.load('assets/LOZ_Get_Rupee.wav')
    init_menu()
    return event_loop(
        images.file_select_background(),
        images.pink_heart()
    )

if __name__ == '__main__':
    # Load and display the file select screen
    game_screen.init()
    execute()
