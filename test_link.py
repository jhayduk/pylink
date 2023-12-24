"""Tests for link.py"""
from link import Link
import pygame
import pytest


class TestLinkConstructors:
    """Tests for the constructor and get_instance for link.py"""

    @pytest.fixture
    def initialize_display(self):
        pygame.init()
        pygame.display.set_mode((1,1))
        yield
        pygame.quit()

    def test_get_instance_not_none(self, initialize_display):
        """Should not return None"""
        assert Link.get_instance() is not None

    def test_get_instance_returns_singleton(self, initialize_display):
        """Should return the same object no matter how many times it is called"""
        first_object = Link.get_instance()
        second_object = Link.get_instance()
        assert first_object is second_object
