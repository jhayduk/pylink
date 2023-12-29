"""Tests for tile_loader.py"""
import pylink_config

def test_tile_size():
    """Should return the game's tile size in pixels"""
    assert pylink_config.TILE_SIZE == (48, 48)

def test_window_size_in_tiles():
    """Should return the game's window size in tiles"""
    assert pylink_config.WINDOW_SIZE_IN_TILES == (16, 15)

def test_window_size():
    """Should return the game's window size in pixels"""
    assert pylink_config.WINDOW_SIZE == (16*48, 15*48)
