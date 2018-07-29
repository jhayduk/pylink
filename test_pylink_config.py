import pygame
import pylink_config

def test_tile_size():
    """Should return the game's tile size in pixels"""
    assert pylink_config.tile_size == (48, 48)

def test_window_size_in_tiles():
    """Should return the game's window size in tiles"""
    assert pylink_config.window_size_in_tiles == (16, 15)

def test_window_size():
    """Should return the game's window size in pixels"""
    assert pylink_config.window_size == (16*48, 15*48)