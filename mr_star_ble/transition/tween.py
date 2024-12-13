"""Tween animation."""
from functools import partial
from typing import Callable

from mr_star_ble.color import HSColor

from .diff import forward_diff, looped_diff
from .frame import get_frame_time

HUE_MAX = 360

Differ = Callable[[float, float], float]

class ValueTween:
    """Tween iterator between two values."""
    _from_value: float
    _to_value: float
    _step: float
    _duration: float
    _frame: int
    _frame_count: int
    _diff: Differ
    _loop_max: float

    @property
    def from_value(self) -> float:
        """Returns from value."""
        return self._from_value

    @property
    def to_value(self) -> float:
        """Returns to value."""
        return self._to_value

    def __init__(
            self,
            from_value: float,
            to_value: float,
            duration: float,
            loop_max: float | None = None):
        self._from_value = from_value
        self._to_value = to_value
        self._duration = duration
        if loop_max is None:
            self._diff = forward_diff
        else:
            self._diff = partial(looped_diff, max_value=loop_max)

        self._loop_max = loop_max
        self.__iter__()

    def __iter__(self):
        delta = self._diff(self._from_value, self._to_value)
        # Skip start and end frames
        self._frame_count = int(self._duration / get_frame_time()) - 2
        self._step = delta / self._frame_count
        self._frame = 0
        return self

    def __next__(self):
        if self._frame == self._frame_count:
            raise StopIteration
        self._frame += 1
        value = self._from_value + (self._step * self._frame)
        if self._loop_max is None:
            return value
        if value <= 0:
            return self._loop_max + value
        elif value >= self._loop_max:
            return value - self._loop_max
        return value

class HSColorTween:
    """Tween iterator between two HS colors."""
    _from: HSColor
    _to: HSColor

    def __init__(
            self,
            from_value: HSColor,
            to_value: HSColor,
            duration: float):
        hue_from, value_from = from_value
        hue_to, value_to = to_value

        self._hue = ValueTween(
            hue_from,
            hue_to,
            duration,
            loop_max=HUE_MAX)
        self._value = ValueTween(
            value_from,
            value_to,
            duration)

    def __iter__(self):
        self._hue.__iter__()
        self._value.__iter__()
        return self

    def __next__(self):
        hue = self._hue.__next__()
        value = self._value.__next__()
        if hue == HUE_MAX:
            hue = 0
        return int(hue), value
