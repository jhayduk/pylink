import pytest
import pygame
import title_intro_text

class TestLocation(object):

    def test_less_than_16_secs(self):
        """Should place at bottom of window when less than 16 secs"""
        assert title_intro_text.location(8) == (6, 720)

    def test_16_secs(self):
        """Should place at bottom of window at the 16 second mark"""
        assert title_intro_text.location(16) == (6, 720)

    def test_23_5_secs(self):
        """Should be offset enough to show the whole intro text at 23.5 second mark"""
        assert title_intro_text.location(23.5) == (6, 56)

    def test_27_5_secs(self):
        """Should still be at the same offset to show the intro text at the 27.5 second mark"""
        assert title_intro_text.location(27.5) == (6, 56)

    def test_74_5_secs(self):
        """Should have scrolled the entire treasure list up by the 74.5 second mark"""
        assert title_intro_text.location(74.5) == (6, 56 - (713*3) + 1)

