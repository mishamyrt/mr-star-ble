"""Test color conversions"""
from time import sleep

import pytest

from mr_star_ble import MrStarLight


@pytest.mark.asyncio
async def test_e2e():
    """Test RGB to HS conversion"""
    print("Connecting...")
    light = await MrStarLight.discover()
    await light.set_power(True)
    sleep(1)
    await light.set_power(False)
    sleep(1)
    await light.set_power(True)
    sleep(0.1)
    await light.set_brightness(1)
    sleep(1)
    await light.set_brightness(0.5)
    sleep(1)
    await light.set_brightness(0.01)
    print("Setting color...")
    await light.set_rgb_color((255, 0, 0))
    sleep(1)
    await light.set_rgb_color((0, 255, 0))
    sleep(1)
    await light.set_rgb_color((0, 0, 255))
    print("Disconnecting...")
    await light.disconnect()
