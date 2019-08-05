"""
pylink - a Python version of NES Legend of Zelda

Done just for fun and for programming practice.
All copyrights are by they original owners.
"""
import sys
import game_screen
import title_screen
import file_select_screen

if __name__ == '__main__':
    game_screen.init()
    if not title_screen.execute():
        sys.exit(0)
    SAVE_GAME = file_select_screen.execute()
    if SAVE_GAME is None:
        sys.exit(0)
    print "DEBUG ----> SAVE_GAME = " + str(SAVE_GAME)
