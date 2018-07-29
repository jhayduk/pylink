import pygame
import tile_loader

def test_count_tiles():
    """Should return the the correct number of tiles in each row and column"""
    num_tiles_in_each_row, num_tiles_in_each_col = tile_loader.count_tiles(
        pygame.image.load("assets/NES-TheLegendofZelda-OverworldTiles.png"),
        (16, 16),
        1)
    assert (num_tiles_in_each_row, num_tiles_in_each_col) == (18, 9)

class TestTileUpperLeftCoordinates(object):

    def test_tile_0_0(self):
        """Should offset tile[0,0] by boarder"""
        x, y = tile_loader.tile_upper_left_coordinates(0, 0, (16, 16), 1)
        assert (x, y) == (1, 1)

    def test_tile_0_1(self):
        """Should calculate for tile[0,1] correctly"""
        x, y = tile_loader.tile_upper_left_coordinates(0, 1, (16, 16), 1)
        assert (x, y) == (1, 18)

    def test_tile_1_0(self):
        """Should calculate for tile[1,0] correctly"""
        x, y = tile_loader.tile_upper_left_coordinates(1, 0, (16, 16), 1)
        assert (x, y) == (18, 1)

    def test_non_square_tiles(self):
        """Should work for non-square tiles as well"""
        x, y = tile_loader.tile_upper_left_coordinates(1, 1, (10, 32), 1)
        assert (x, y) == (12, 34)
