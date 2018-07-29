import pygame
import pygame.locals
import pylink_config

def count_tiles(image, tile_size, border=0):
    """Count the number of tiles in a loaded image.

    Inputs:
        image - An image loaded with pygame.image.load
        tile_size - The (width, height) of each tile in the file
        border - The border around *each* tile in the file.

    Returns:
        num_tiles_in_each_row
        num_tiles_in_each_column
    """
    image_width, image_height = image.get_size()
    num_tiles_in_each_row = ((image_width - border) / (tile_size[0] + border))
    num_tiles_in_each_col = ((image_height - border) / (tile_size[1] + border))
    return (num_tiles_in_each_row, num_tiles_in_each_col)

def tile_upper_left_coordinates(col, row, tile_size, border=0):
    """Returns the upper left x and y coordinates of the tile at row, col

    Inputs:
        col - The 0-based col number of the tile in the file
        row - The 0-based row number of the tile in the file
        tile_size - The (width, height) of each tile in the file
        border - The border around *each* tile in the file.

    Return:
        x - The 0-based x coordinate of the tile's upper left corner in the file
        y - The 0-based y coordinate of the tile's upper left corner in the file
    """
    x = border + (col * (tile_size[0] + border))
    y = border + (row * (tile_size[1] + border))
    return (x, y)

def load_tile_table(filename, original_tile_size, border=0, final_tile_size=(-1, -1)):
    """Load a tile sheet from a file.

    filename - The file to load the sheet from. Should be a png file.
    original_tile_size - The (width, height) of each tile in the file
    border - The border around *each* tile in the file
    final_tile_size - The (width, height) each tile should be scaled to for the game

    Each row is expected to be layed out as:
        border + tile width + border + ... + tile width + border

    Each column is similarly expected to be layed out as:
        border + tile height + board + ... + tile height +  border
    """
    if (final_tile_size == (-1, -1)):
        final_tile_size = original_tile_size
    image = pygame.image.load(filename).convert()
    num_tiles_in_each_row, num_tiles_in_each_col = count_tiles(image, original_tile_size, border)
    tile_table = []
    for tile_row in range(0, num_tiles_in_each_col):
        line = []
        tile_table.append(line)
        for tile_col in range(0, num_tiles_in_each_row):
            x, y = tile_upper_left_coordinates(tile_col, tile_row, original_tile_size, border)
            rect = (x, y, original_tile_size[0], original_tile_size[1])
            line.append(pygame.transform.smoothscale(image.subsurface(rect), final_tile_size))
    return tile_table

if __name__=='__main__':
    """Draw the loaded and scaled tiles on the screen"""
    pygame.init()
    screen = pygame.display.set_mode((1280, 1024))
    screen.fill((255, 255, 255))
    table = load_tile_table("assets/NES-TheLegendofZelda-OverworldTiles.png", (16, 16), 1, pylink_config.tile_size)
    for y, row in enumerate(table):
        for x, tile in enumerate(row):
            screen.blit(tile, (x*pylink_config.tile_size[0], y*pylink_config.tile_size[1]))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
