"""Game screen utilities

The intent is that all game screen actions can go through this module
so that other code does not need to worry about the specifics and does
not need to pass around things like the screen surface.

Note that coordinates are always given in game coordinates. Any scaling
is expected to be done externaly.
"""
import pygame
import pygame.locals
import pylink_config
import screen

def init():
    """Initialze the game context and the screen.

    Initializes the screen, clears it to all black and sets the title.
    """
    pygame.init()
    pygame.display.set_caption('The Legend of Zelda')
    screen.surface = pygame.display.set_mode(pylink_config.WINDOW_SIZE)
    fill((0, 0, 0))

def fill(color):
    """
    Fill Surface with a solid color.

    Wraps pygame.Surface.fill

    Args:
        color: The (r, g, b) color to fill the surface with.

    Returns:
        Rect: A rectangle rectangle is the area of the affected pixels.
    """
    screen.surface.fill(color)

def blit(source, dest):
    """
    Draws a source Surface onto the game Surface.

    Wraps pygame.Surface.blit

    Args:
        source: The source image.
        dest: Dest is a pair of coordinates representing where to place
            the upper left corner of the source onto the game surface.

    Returns:
        Rect: A rectangle rectangle is the area of the affected pixels,
        excluding any pixels outside the destination Surface, or
        outside the clipping area.
    """
    screen.surface.blit(source, dest)

if __name__ == '__main__':
    # Create the screen and show it blank
    init()
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
