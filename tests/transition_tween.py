"""tween utils tests"""
import pytest

from mr_star_ble.transition.frame import set_framerate
from mr_star_ble.transition.tween import HSColorTween, ValueTween


def test_forward_diff_tween():
    """Test forward diff tween between two values."""
    set_framerate(6)
    tween = ValueTween(0, 1, 1)
    assert next(tween) == 0.25
    assert next(tween) == 0.5
    assert next(tween) == 0.75
    assert next(tween) == 1
    with pytest.raises(StopIteration):
        next(tween)

    tween = ValueTween(1, 0, 1)
    assert next(tween) == 0.75
    assert next(tween) == 0.5
    assert next(tween) == 0.25
    assert next(tween) == 0
    with pytest.raises(StopIteration):
        next(tween)

def test_looped_diff_tween():
    """Test looped diff tween between two values."""
    set_framerate(4)
    hue_tween = ValueTween(0, 100, 1, loop_max=360)
    assert next(hue_tween) == 50
    assert next(hue_tween) == 100

    with pytest.raises(StopIteration):
        next(hue_tween)

    set_framerate(10)
    hue_tween = ValueTween(0, 350, 1, loop_max=360)
    assert next(hue_tween) == 358.75
    assert next(hue_tween) == 357.5
    assert next(hue_tween) == 356.25
    assert next(hue_tween) == 355.0
    assert next(hue_tween) == 353.75
    assert next(hue_tween) == 352.5
    assert next(hue_tween) == 351.25
    assert next(hue_tween) == 350

    with pytest.raises(StopIteration):
        next(hue_tween)

def test_hs_tween():
    """Test HS tween between two values."""
    set_framerate(6)
    tween = HSColorTween((0, 0), (100, 100), 1)
    assert next(tween) == (25, 25)
    assert next(tween) == (50, 50)
    assert next(tween) == (75, 75)
    assert next(tween) == (100, 100)

    with pytest.raises(StopIteration):
        next(tween)

    tween = HSColorTween((100, 100), (0, 0), 1)
    assert next(tween) == (75, 75)
    assert next(tween) == (50, 50)
    assert next(tween) == (25, 25)
    assert next(tween) == (0, 0)

    with pytest.raises(StopIteration):
        next(tween)

    tween = HSColorTween((0, 0), (350, 0), 1)
    assert next(tween) == (357, 0)
    assert next(tween) == (355, 0)
    assert next(tween) == (352, 0)
    assert next(tween) == (350, 0)

    with pytest.raises(StopIteration):
        next(tween)
