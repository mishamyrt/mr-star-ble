"""Animation frame utils."""

import asyncio

_FRAMERATE = 30
_FRAME_TIME = 1 / _FRAMERATE

def set_framerate(framerate: int):
    """Sets global framerate for all animation iterators."""
    global _FRAMERATE # pylint: disable=global-statement
    global _FRAME_TIME # pylint: disable=global-statement
    _FRAMERATE = framerate
    _FRAME_TIME = 1 / _FRAMERATE

def get_frame_time() -> float:
    """Returns global frame time for all animation iterators."""
    return _FRAME_TIME

async def sleep_frame():
    """Sleeps the frame time."""
    await asyncio.sleep(_FRAME_TIME)
