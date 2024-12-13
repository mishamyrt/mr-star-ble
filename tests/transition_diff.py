"""integer utils tests"""
from mr_star_ble.transition.diff import forward_diff, looped_diff

HUE_MAX = 360

def test_forward_diff():
    """Test split_uint16"""
    assert forward_diff(0, 0) == 0
    assert forward_diff(0, 1) == 1
    assert forward_diff(255, 10) == -245
    assert forward_diff(10, 255) == 245

def test_looped_diff():
    """Test split_uint16"""
    assert looped_diff(0, 360, HUE_MAX) == 0
    assert looped_diff(0, 1, HUE_MAX) == 1
    assert looped_diff(359, 0, HUE_MAX) == 1
    assert looped_diff(0, 359, HUE_MAX) == -1
    assert looped_diff(30, 350, HUE_MAX) == -40
    assert looped_diff(350, 30, HUE_MAX) == 40
    assert looped_diff(30, 30, HUE_MAX) == 0
