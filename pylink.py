"""
pylink - a Python version of NES Legend of Zelda

Done just for fun and for programming practice.
All copyrights are by they original owners.
"""
import pygame
import pygame.locals
import pylink_config
import title_screen

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('The Legend of Zelda')
    SCREEN = pygame.display.set_mode(pylink_config.WINDOW_SIZE)
    title_screen.execute(SCREEN)
