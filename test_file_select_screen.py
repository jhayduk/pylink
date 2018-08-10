"""Tests for file_select_screen.py"""
import file_select_screen

#pylint: disable-msg=no-self-use,too-few-public-methods,line-too-long,invalid-name
class TestNextMenuItem(object):
    """Tests for file_select_screen.next_menu_item()."""

    def test_01_start(self):
        """Should start at first item."""
        assert file_select_screen.next_menu_item(0)["item"] == "file1"

    def test_02_down_to_second_item(self):
        """Should go to second item after first."""
        assert file_select_screen.next_menu_item(1)["item"] == "file2"

    def test_03_still_second_item(self):
        """Should stay at second item."""
        assert file_select_screen.next_menu_item(0)["item"] == "file2"

    def test_04_back_to_first_item(self):
        """Should go back to first item if negative."""
        assert file_select_screen.next_menu_item(-1)["item"] == "file1"

    def test_05_down_to_second_item(self):
        """Should walk down to second item after first."""
        assert file_select_screen.next_menu_item(1)["item"] == "file2"

    def test_06_down_to_third_item(self):
        """Should walk down to third item after second."""
        assert file_select_screen.next_menu_item(1)["item"] == "file3"

    def test_07_down_to_fourth_item(self):
        """Should walk down to fourth item after third."""
        assert file_select_screen.next_menu_item(1)["item"] == "register"

    def test_08_down_to_fifth_item(self):
        """Should walk down to fifth item after fourth."""
        assert file_select_screen.next_menu_item(1)["item"] == "elimination"

    def test_09_wrap_down_around_bottom_to_first_item(self):
        """Should wrap back to first after fifth."""
        assert file_select_screen.next_menu_item(1)["item"] == "file1"

    def test_10_wrap_up_around_top_to_fifth_item(self):
        """Should wrap around top to fifth item after first."""
        assert file_select_screen.next_menu_item(-1)["item"] == "elimination"

    def test_11_up_to_fourth_item(self):
        """Should walk up to fourth item after fifth."""
        assert file_select_screen.next_menu_item(-1)["item"] == "register"

    def test_12_up_to_third_item(self):
        """Should walk up to third item after fourth."""
        assert file_select_screen.next_menu_item(-1)["item"] == "file3"

    def test_13_up_to_second_item(self):
        """Should walk up to second item after third."""
        assert file_select_screen.next_menu_item(-1)["item"] == "file2"

    def test_14_up_to_first_item(self):
        """Should walk up to first item after second."""
        assert file_select_screen.next_menu_item(-1)["item"] == "file1"

    def test_15_wrap_up_around_top_to_fifth_item(self):
        """Should wrap around top to fifth item after first."""
        assert file_select_screen.next_menu_item(-1)["item"] == "elimination"
