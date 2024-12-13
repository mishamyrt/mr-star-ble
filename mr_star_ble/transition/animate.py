"""MR Star light animation utils"""


from mr_star_ble.api import MrStarAPI
from mr_star_ble.color import HSColor

from .frame import sleep_frame
from .tween import HSColorTween, ValueTween


async def animate_brightness(
        api: MrStarAPI,
        from_value: float,
        to_value: float,
        duration=1.0):
    """Sets the brightness of the device."""
    for value in ValueTween(from_value, to_value, duration):
        await api.set_brightness(value)
        await sleep_frame()

async def animate_power(
        api: MrStarAPI,
        is_on: bool,
        current_brightness: float,
        duration=1.2):
    """Animates lights power off."""
    if is_on:
        await api.set_brightness(0)
        await api.set_power(True)
        await animate_brightness(api, 0, current_brightness, duration)
    else:
        await animate_brightness(api, current_brightness, 0, duration)
        await api.set_power(False)
        await api.set_brightness(current_brightness)

async def animate_color(
        api: MrStarAPI,
        from_color: HSColor,
        to_color: HSColor,
        duration=1.0):
    """Sets the color of the device."""
    for color in HSColorTween(from_color, to_color, duration):
        await api.set_hs_color(color)
        await sleep_frame()
