"""Tests for events.py"""
from events import Events
import pygame
import pytest


class TestEventsConstructors:
    """Tests for the constructor and get_instance for events.py"""

    @pytest.fixture
    def initialize_display(self):
        pygame.init()
        pygame.display.set_mode((1,1))
        yield
        pygame.quit()

    def test_get_instance_not_none(self, initialize_display):
        """Should not return None"""
        assert Events.get_instance() is not None

    def test_get_instance_returns_singleton(self, initialize_display):
        """Should return the same object no matter how many times it is called"""
        first_object = Events.get_instance()
        second_object = Events.get_instance()
        assert first_object is second_object
