import pygame
import pygame.locals
import numpy
import pylink_config

def count_tiles(image, tile_size, border=(0, 0), offset=(0, 0)):
    """Count the number of tiles in a loaded image.

    Inputs:
        image - An image loaded with pygame.image.load
        tile_size - The (width, height) of each tile in the file
        border - The (width, height) border around *each* tile in the file.
        offset - The (width, height) of the initial offset used to find the first tile

    Returns:
        num_tiles_in_each_row
        num_tiles_in_each_column
    """
    image_width, image_height = tuple(map(int, numpy.subtract(image.get_size(), offset)))
    num_tiles_in_each_row = ((image_width - border[0]) / (tile_size[0] + border[0]))
    num_tiles_in_each_col = ((image_height - border[1]) / (tile_size[1] + border[1]))
    return (num_tiles_in_each_row, num_tiles_in_each_col)

def tile_upper_left_coordinates(col, row, tile_size, border=(0, 0), offset=(0, 0)):
    """Returns the upper left x and y coordinates of the tile at row, col

    Inputs:
        col - The 0-based col number of the tile in the file
        row - The 0-based row number of the tile in the file
        tile_size - The (width, height) of each tile in the file
        border - The (width, height) border around *each* tile in the file.
        offset - The (width, height) of the initial offset used to find the first tile

    Return:
        x - The 0-based x coordinate of the tile's upper left corner in the file
        y - The 0-based y coordinate of the tile's upper left corner in the file
    """
    x = offset[0] + border[0] + (col * (tile_size[0] + border[0]))
    y = offset[1] + border[1] + (row * (tile_size[1] + border[1]))
    return (x, y)

def load_tile_table(
    filename,
    original_tile_size,
    border = (0 ,0),
    offset = (0, 0),
    final_tile_size=(None, None),
    tile_scaling=(None, None),
    colorkey_location = (None, None)):
    """Load a tile sheet from a file.

    filename - The file to load the sheet from. Should be a png file.
    original_tile_size - The (width, height) of each tile in the file
    border - The (width, height) of the border around *each* tile in the file
    offset - The (wdith, height) of the initial offset used to find the first tile
    final_tile_size - The (width, height) each tile should be scaled to for the game
    tile_scaling - The amount (width, height) each tile should be scaled to for the game
    colorkey_location - If present, the location within the image to sample for the colorkey

    Each row is expected to be layed out as:
        offset width + border + tile width + border + ... + tile width + border

    Each column is similarly expected to be layed out as:
        offset height + border + tile height + board + ... + tile height +  border
    """
    if ((final_tile_size != (None, None)) and (tile_scaling != (None, None))):
        raise ValueError('final_tile_size and tile_scaling cannot both be specified in the same call')

    if (tile_scaling == (None, None)):
        tile_scaling = (1, 1)

    if (final_tile_size == (None, None)):
        final_tile_size = tuple(map(int, numpy.multiply(original_tile_size, tile_scaling)))

    image = pygame.image.load(filename).convert()
    num_tiles_in_each_row, num_tiles_in_each_col = count_tiles(image, original_tile_size, border, offset)
    tile_table = []
    for tile_row in range(0, num_tiles_in_each_col):
        line = []
        tile_table.append(line)
        for tile_col in range(0, num_tiles_in_each_row):
            x, y = tile_upper_left_coordinates(tile_col, tile_row, original_tile_size, border, offset)
            rect = (x, y, original_tile_size[0], original_tile_size[1])
            surface = pygame.transform.scale(image.subsurface(rect), final_tile_size)
            if (colorkey_location != (None, None)):
                colorkey = surface.get_at(colorkey_location)
                surface.set_colorkey(colorkey)
            line.append(surface)
    return tile_table

if __name__=='__main__':
    """Draw the loaded and scaled tiles on the screen"""
    pygame.init()
    screen = pygame.display.set_mode(pylink_config.window_size)
    screen.fill((0, 0, 0))
    table = load_tile_table(
        filename = "assets/NES-TheLegendofZelda-OverworldTiles.png",
        original_tile_size = (16, 16),
        border = (1, 1),
        offset = (0, 0),
        final_tile_size = pylink_config.tile_size)
    for y, row in enumerate(table):
        for x, tile in enumerate(row):
            screen.blit(
                tile,
                (
                    pylink_config.map_upper_left[0] + (x * pylink_config.tile_size[0]),
                    pylink_config.map_upper_left[1] + (y * pylink_config.tile_size[1])
                )
            )
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
