"""Integer diff utils."""

def forward_diff(from_value: float, to_value: float) -> float:
    """Returns forward-front difference between two values."""
    return to_value - from_value

def looped_diff(from_value: float, to_value: float, max_value: float) -> float:
    """Returns shortest difference between two values."""
    forward = forward_diff(from_value, to_value)
    backward = (max_value - max(from_value, to_value) + min(from_value, to_value))
    if backward < abs(forward):
        if from_value < to_value:
            backward *= -1
        return backward
    return forward
