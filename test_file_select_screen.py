"""Tests for file_select_screen.py"""
import pytest
import file_select_screen

@pytest.fixture()
def all_selectable():
    """Initialize the menu so all are selectable."""
    for index in range(0, 5):
        file_select_screen.set_selectable(index, True)

@pytest.fixture()
def odd_selectable():
    """Initialize the menu so only the odd indexes are selectable."""
    for index in range(0, 5):
        file_select_screen.set_selectable(index, False)
    for index in range(1, 5, 2):
        file_select_screen.set_selectable(index, True)


#pylint: disable-msg=no-self-use,too-few-public-methods,line-too-long,invalid-name,redefined-outer-name,unused-argument
class TestNextMenuItem(object):
    """Tests for file_select_screen.next_menu_item()."""

    def test_01_start(self, all_selectable):
        """Should start at first item."""
        assert file_select_screen.next_menu_item(0)["item"] == "file1"

    def test_02_down_to_second_item(self, all_selectable):
        """Should go to second item after first."""
        assert file_select_screen.next_menu_item(1)["item"] == "file2"

    def test_03_still_second_item(self, all_selectable):
        """Should stay at second item."""
        assert file_select_screen.next_menu_item(0)["item"] == "file2"

    def test_04_back_to_first_item(self, all_selectable):
        """Should go back to first item if negative."""
        assert file_select_screen.next_menu_item(-1)["item"] == "file1"

    def test_05_down_to_second_item(self, all_selectable):
        """Should walk down to second item after first."""
        assert file_select_screen.next_menu_item(1)["item"] == "file2"

    def test_06_down_to_third_item(self, all_selectable):
        """Should walk down to third item after second."""
        assert file_select_screen.next_menu_item(1)["item"] == "file3"

    def test_07_down_to_fourth_item(self, all_selectable):
        """Should walk down to fourth item after third."""
        assert file_select_screen.next_menu_item(1)["item"] == "register"

    def test_08_down_to_fifth_item(self, all_selectable):
        """Should walk down to fifth item after fourth."""
        assert file_select_screen.next_menu_item(1)["item"] == "elimination"

    def test_09_wrap_down_around_bottom_to_first_item(self, all_selectable):
        """Should wrap back to first after fifth."""
        assert file_select_screen.next_menu_item(1)["item"] == "file1"

    def test_10_wrap_up_around_top_to_fifth_item(self, all_selectable):
        """Should wrap around top to fifth item after first."""
        assert file_select_screen.next_menu_item(-1)["item"] == "elimination"

    def test_11_up_to_fourth_item(self, all_selectable):
        """Should walk up to fourth item after fifth."""
        assert file_select_screen.next_menu_item(-1)["item"] == "register"

    def test_12_up_to_third_item(self, all_selectable):
        """Should walk up to third item after fourth."""
        assert file_select_screen.next_menu_item(-1)["item"] == "file3"

    def test_13_up_to_second_item(self, all_selectable):
        """Should walk up to second item after third."""
        assert file_select_screen.next_menu_item(-1)["item"] == "file2"

    def test_14_up_to_first_item(self, all_selectable):
        """Should walk up to first item after second."""
        assert file_select_screen.next_menu_item(-1)["item"] == "file1"

    def test_15_wrap_up_around_top_to_fifth_item(self, all_selectable):
        """Should wrap around top to fifth item after first."""
        assert file_select_screen.next_menu_item(-1)["item"] == "elimination"

    def test_16_skip_forward_unselectable(self, odd_selectable):
        """Should skip unselectable in forward direction."""
        assert file_select_screen.next_menu_item(1)["item"] == "file2"

    def test_17_skip_reverse_unselectable(self, odd_selectable):
        """Should skip unselectable in reverse direction."""
        assert file_select_screen.next_menu_item(-1)["item"] == "register"
