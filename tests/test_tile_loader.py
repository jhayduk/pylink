"""Tests for tile_loader.py"""
import pytest
import pygame
import tile_loader


#pylint: disable-msg=no-self-use,too-few-public-methods,line-too-long
class TestCountTiles(object):
    """Tests for tile_loader.py::count_tiles()"""

    def test_count_tiles(self):
        """Should return the correct number of tiles in each row and column"""
        num_tiles_in_each_row, num_tiles_in_each_col = tile_loader.count_tiles(
            image=pygame.image.load("assets/NES-TheLegendofZelda-OverworldTiles.png"),
            tile_size=(16, 16),
            border=(1, 1))
        assert (num_tiles_in_each_row, num_tiles_in_each_col) == (18, 9)

    def test_uneven_borders(self):
        """Should count correctly when borders are uneven and not all tiles fit.
        This could happen on 'miscellaneous' tile sheets"""
        num_tiles_in_each_row, num_tiles_in_each_col = tile_loader.count_tiles(
            image=pygame.image.load("assets/NES-TheLegendofZelda-IntroAndFileSelect.png"),
            tile_size=(256, 240),
            border=(3, 3))
        assert (num_tiles_in_each_row, num_tiles_in_each_col) == (2, 4)

    def test_offset(self):
        """Should count correctly when there is an offset.
        This could happen on 'miscellaneous' tile sheets"""
        num_tiles_in_each_row, num_tiles_in_each_col = tile_loader.count_tiles(
            image=pygame.image.load("assets/NES-TheLegendofZelda-IntroAndFileSelect.png"),
            tile_size=(256, 240),
            border=(3, 3),
            offset=(-1, -1))
        assert (num_tiles_in_each_row, num_tiles_in_each_col) == (2, 4)


class TestTileUpperLeftCoordinates(object):
    """Tests for tile_loader.py::tile_upper_left_coordinates()"""

    def test_tile_0_0(self):
        """Should offset tile[0,0] by boarder"""
        tile_x, tile_y = tile_loader.tile_upper_left_coordinates(
            col=0,
            row=0,
            tile_size=(16, 16),
            border=(1, 1))
        assert (tile_x, tile_y) == (1, 1)

    def test_tile_0_1(self):
        """Should calculate for tile[0,1] correctly"""
        tile_x, tile_y = tile_loader.tile_upper_left_coordinates(
            col=0,
            row=1,
            tile_size=(16, 16),
            border=(1, 1))
        assert (tile_x, tile_y) == (1, 18)

    def test_tile_1_0(self):
        """Should calculate for tile[1,0] correctly"""
        tile_x, tile_y = tile_loader.tile_upper_left_coordinates(
            col=1,
            row=0,
            tile_size=(16, 16),
            border=(1, 1))
        assert (tile_x, tile_y) == (18, 1)

    def test_non_square_tiles(self):
        """Should work for non-square tiles as well"""
        tile_x, tile_y = tile_loader.tile_upper_left_coordinates(
            col=1,
            row=1,
            tile_size=(10, 32),
            border=(1, 1))
        assert (tile_x, tile_y) == (12, 34)

    def test_offset(self):
        """Should work correctly when there is an offset.
        This could happen on 'miscellaneous' tile sheets"""
        tile_x, tile_y = tile_loader.tile_upper_left_coordinates(
            col=0,
            row=0,
            tile_size=(16, 16),
            border=(3, 3),
            offset=(-1, -2))
        assert (tile_x, tile_y) == (2, 1)

    def test_title_offset(self):
        """Should give the correct coordinates of the first tile for the title screen"""
        tile_x, tile_y = tile_loader.tile_upper_left_coordinates(
            col=0,
            row=0,
            tile_size=(16, 16),
            border=(3, 3),
            offset=(0, 1))
        assert (tile_x, tile_y) == (3, 4)

    def test_waterfall_offset(self):
        """Should give the correct coordinates of the first waterfall tile for the title screen"""
        tile_x, tile_y = tile_loader.tile_upper_left_coordinates(
            col=0,
            row=0,
            tile_size=(32, 59),
            border=(6, 0),
            offset=(340, 514))
        assert (tile_x, tile_y) == (346, 514)

class TestLoadTileTable(object):
    """Tests for tile_loader.py::load_tile_table()"""

    #pylint: disable-msg=invalid-name,unused-variable
    def test_both_final_size_and_scaling_together(self):
        """Should raise a ValueError if both final size and scaling are given together"""
        with pytest.raises(ValueError, match=r'final_tile_size and tile_scaling cannot both be specified in the same call'):
            tile_table = tile_loader.load_tile_table(
                filename='junk',
                original_tile_size=(16, 16),
                final_tile_size=(48, 48),
                tile_scaling=(3, 3))
    #pylint: enable-msg=invalid-name,unused-variable
