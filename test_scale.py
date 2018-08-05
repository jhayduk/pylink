"""Tests for scale.py"""
import scale

#pylint: disable-msg=no-self-use,too-few-public-methods,line-too-long
class TestCoordinate(object):
    """Tests for scale.coordinate()."""

    def test_origin(self):
        """Should retun 0, 0 for the origin."""
        assert scale.coordinates((0, 0)) == (0, 0)

    def test_far_corner(self):
        """Should correctly calculate the far right, bottom corner."""
        assert scale.coordinates((256, 240)) == (256*3, 240*3)

    def test_negative_values(self):
        """Should support negative values."""
        assert scale.coordinates((-100, -200)) == (-100*3, -200*3)

    def test_off_screen(self):
        """Should support large, off-screen values."""
        assert scale.coordinates((1234, 5678)) == (1234*3, 5678*3)
