"""Test color conversions"""
from mr_star_ble.color import rgb_to_hs


def test_rgb_to_hs():
    """Test RGB to HS conversion"""
    assert rgb_to_hs((255, 255, 255)) == (0, 0)
    assert rgb_to_hs((255, 0, 0)) == (0, 100)
    assert rgb_to_hs((0, 255, 0)) == (120, 100)
    assert rgb_to_hs((0, 0, 255)) == (240, 100)
    assert rgb_to_hs((128, 128, 0)) == (60, 100)
    assert rgb_to_hs((0, 0, 0)) == (0, 0)
