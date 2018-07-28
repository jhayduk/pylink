import pygame
import pygame.locals

def count_tiles(image, tile_width, tile_height, border=0):
    """Count the number of tiles in a loaded image.

    Inputs:
        image - An image loaded with pygame.image.load
        tile_width - The width of each tile
        tile_height - The height of each tile
        border - The border around *each* tile.

    Returns:
        num_tiles_in_each_row
        num_tiles_in_each_column
    """
    image_width, image_height = image.get_size()
    num_tiles_in_each_row = ((image_width - border) / (tile_width + border))
    num_tiles_in_each_col = ((image_height - border) / (tile_height + border))
    return (num_tiles_in_each_row, num_tiles_in_each_col)

def tile_upper_left_coordinates(col, row, tile_width, tile_height, border=0):
    """Returns the upper left x and y coordinates of the tile at row, col

    Inputs:
        col - The 0-based col number of the tile
        row - The 0-based row number of the tile
        tile_width - The width of each tile
        tile_height - The height of each tile
        border - The border around *each* tile.

    Return:
        x - The 0-based x coordinate of the tile's upper left corner
        y - The 0-based y coordinate of the tile's upper left corner
    """
    x = border + (col * (tile_width + border))
    y = border + (row * (tile_height + border))
    return (x, y)

def load_tile_table(filename, tile_width, tile_height, border=0):
    """Load a tile sheet from a file.

    filename - The file to load the sheet from. Should be a png file
    tile_width - The width of each tile
    tile_height - The height of each tile
    border - The border around *each* tile.

    Each row is expected to be layed out as:
        border + tile_width + border + ... + tile_width + border

    Each column is similarly expected to be layed out as:
        border + tile_height + board + ... + tile_height +  border
    """
    image = pygame.image.load(filename).convert()
    num_tiles_in_each_row, num_tiles_in_each_col = count_tiles(image, tile_width, tile_height, border)
    tile_table = []
    for tile_row in range(0, num_tiles_in_each_col):
        line = []
        tile_table.append(line)
        for tile_col in range(0, num_tiles_in_each_row):
            x, y = tile_upper_left_coordinates(tile_col, tile_row, tile_width, tile_height, border)
            rect = (x, y, tile_width, tile_height)
            line.append(image.subsurface(rect))
    return tile_table

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    screen.fill((255, 255, 255))
    table = load_tile_table("NES-TheLegendofZelda-OverworldTiles.png", 16, 16, 1)
    for y, row in enumerate(table):
        for x, tile in enumerate(row):
            screen.blit(tile, (x*32, y*24))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
