"""Test color conversions"""

import asyncio

import pytest

from mr_star_ble import Effect, MrStarDevice, discover


@pytest.mark.asyncio
async def test_power():
    """Test RGB to HS conversion"""
    ble_device = await discover()
    device = MrStarDevice(ble_device)
    await device.connect()
    async with device as light:
        await light.set_power(False)
        await asyncio.sleep(0.2)
        await light.set_power(True)
        await asyncio.sleep(0.5)
        await light.set_power(False)
        await asyncio.sleep(0.5)
        await light.set_power(True)
    await device.disconnect()

@pytest.mark.asyncio
async def test_brightness():
    """Test RGB to HS conversion"""
    ble_device = await discover()
    device = MrStarDevice(ble_device)
    await device.connect()
    async with device as light:
        brightness = 0.1
        while brightness <= 1:
            await light.set_brightness(brightness)
            await asyncio.sleep(0.2)
            brightness += 0.1
    await device.disconnect()

@pytest.mark.asyncio
async def test_color():
    """Test RGB to HS conversion"""
    ble_device = await discover()
    device = MrStarDevice(ble_device)
    await device.connect()
    async with device as light:
        await light.set_rgb_color((255, 0, 0))
        await asyncio.sleep(0.5)
        await light.set_rgb_color((0, 255, 0))
        await asyncio.sleep(0.5)
        await light.set_rgb_color((0, 0, 255))
        await asyncio.sleep(0.5)
        await light.set_rgb_color((255, 255, 0))
        await asyncio.sleep(0.5)
        await light.set_rgb_color((255, 0, 255))
        await asyncio.sleep(0.5)
        await light.set_rgb_color((0, 255, 255))
        await asyncio.sleep(0.5)
        await light.set_rgb_color((255, 255, 255))
    await device.disconnect()

# @pytest.mark.asyncio
# async def test_effect():
#     """Test RGB to HS conversion"""
#     ble_device = await discover()
#     device = MrStarDevice(ble_device)
#     await device.connect()
#     async with device as light:
#         for effect in Effect:
#             await light.set_effect(effect)
#             await asyncio.sleep(0.5)
#     await device.disconnect()

@pytest.mark.asyncio
async def test_speed():
    """Test RGB to HS conversion"""
    ble_device = await discover()
    device = MrStarDevice(ble_device)
    await device.connect()
    async with device as light:
        await light.set_effect(Effect.SYMPHONY)
        speed = 0.1
        while speed <= 1:
            await light.set_speed(speed)
            await asyncio.sleep(0.2)
            speed += 0.1
    await device.disconnect()

@pytest.mark.asyncio
async def test_reverse():
    """Test RGB to HS conversion"""
    ble_device = await discover()
    device = MrStarDevice(ble_device)
    await device.connect()
    async with device as light:
        await light.set_reverse(False)
        await light.set_effect(Effect.YELLOW_OPEN_CLOSE)
        await asyncio.sleep(0.5)
        await light.set_reverse(True)
        await asyncio.sleep(0.5)
        await light.set_reverse(False)
    await device.disconnect()
