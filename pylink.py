"""pylink - a Python version of NES Legend of Zelda

Done just for fun and for programming practice.
All copyrights are by they original owners.
"""
import pygame
import pygame.locals
import pylink_config
import title_screen

if __name__=='__main__':
    """Draw the loaded and scaled tiles on the screen"""
    pygame.init()
    screen = pygame.display.set_mode(pylink_config.window_size)
    title_screen.go(screen)
