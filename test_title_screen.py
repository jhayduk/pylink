import pytest
import pygame
import title_screen

class TestAlphaValue(object):

    def test_less_than_8_secs(self):
        """Should return 0 if less than 8 seconds"""
        assert title_screen.alphaValue(4) == 0

    def test_8_secs(self):
        """Should start off with 0 at the 8 second mark"""
        assert title_screen.alphaValue(8) == 0

    def test_16_secs(self):
        """Should hit 255 at 16 seconds"""
        assert title_screen.alphaValue(16) == 255

    def test_12_secs(self):
        """Should be 128 when halfway to 16 seconds (at 12 seconds)"""
        assert title_screen.alphaValue(12) == 127

    def test_greater_than_16_secs(self):
        """Should stay at 255 past 16 seconds"""
        assert title_screen.alphaValue(20) == 255
