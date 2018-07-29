import pygame
import tile_loader

class TestCountTiles(object):
    def test_count_tiles(self):
        """Should return the the correct number of tiles in each row and column"""
        num_tiles_in_each_row, num_tiles_in_each_col = tile_loader.count_tiles(
            image = pygame.image.load("assets/NES-TheLegendofZelda-OverworldTiles.png"),
            tile_size = (16, 16),
            border = (1, 1))
        assert (num_tiles_in_each_row, num_tiles_in_each_col) == (18, 9)

    def test_uneven_borders(self):
        """Should count correctly when borders are uneven and not all tiles fit.
        This coul happen on 'micelklaneous' tile sheets"""
        num_tiles_in_each_row, num_tiles_in_each_col = tile_loader.count_tiles(
            image = pygame.image.load("assets/NES-TheLegendofZelda-IntroAndFileSelect.png"),
            tile_size = (256, 240),
            border = (3, 4))
        assert (num_tiles_in_each_row, num_tiles_in_each_col) == (2, 3)


class TestTileUpperLeftCoordinates(object):

    def test_tile_0_0(self):
        """Should offset tile[0,0] by boarder"""
        x, y = tile_loader.tile_upper_left_coordinates(
            col = 0,
            row = 0,
            tile_size = (16, 16),
            border = (1, 1))
        assert (x, y) == (1, 1)

    def test_tile_0_1(self):
        """Should calculate for tile[0,1] correctly"""
        x, y = tile_loader.tile_upper_left_coordinates(
            col = 0,
            row = 1,
            tile_size = (16, 16),
            border = (1, 1))
        assert (x, y) == (1, 18)

    def test_tile_1_0(self):
        """Should calculate for tile[1,0] correctly"""
        x, y = tile_loader.tile_upper_left_coordinates(
            col = 1,
            row = 0,
            tile_size = (16, 16),
            border = (1, 1))
        assert (x, y) == (18, 1)

    def test_non_square_tiles(self):
        """Should work for non-square tiles as well"""
        x, y = tile_loader.tile_upper_left_coordinates(
            col = 1,
            row = 1,
            tile_size = (10, 32),
            border = (1, 1))
        assert (x, y) == (12, 34)
