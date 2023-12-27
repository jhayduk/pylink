"""Tests for link.py"""
from link import Link
import pygame
import pylink_config
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


class TestLinkSwitchMaps:
    """Test for the switch_maps method"""

    @pytest.fixture
    def init_link(self):
        """
        Gets a pointer to the Link singleton instance and then make sure
        it is positioned in its normal starting position.
        """
        self.link = Link.get_instance()
        self.link._Link__rect = pygame.Rect(384, 456, 45, 48)

    def test_move_right(self, init_link):
        """Should switch Link to the left edge of the map window"""
        self.link.switch_maps("right")
        assert self.link._Link__rect.left == pylink_config.PYLINK_MAP.left

    def test_move_down(self, init_link):
        """Should switch Link to the top edge of the map window"""
        self.link.switch_maps("down")
        assert self.link._Link__rect.top == pylink_config.PYLINK_MAP.top

    def test_move_left(self, init_link):
        """Should switch Link to the left edge of the map window"""
        self.link.switch_maps("left")
        assert self.link._Link__rect.right == pylink_config.PYLINK_MAP.right

    def test_move_up(self, init_link):
        """Should switch Link to the bottom edge of the map window"""
        self.link.switch_maps("up")
        assert self.link._Link__rect.bottom == pylink_config.PYLINK_MAP.bottom
