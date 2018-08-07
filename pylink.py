"""
pylink - a Python version of NES Legend of Zelda

Done just for fun and for programming practice.
All copyrights are by they original owners.
"""
import game_screen
import title_screen
import file_select_screen

if __name__ == '__main__':
    game_screen.init()
    if title_screen.execute():
        file_select_screen.execute()
