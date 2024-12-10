"""Example of updating the state of a MR Star light device."""
import asyncio

from mr_star_ble import MrStarDevice

ADDRESS = "DF821C47-03A6-D4C5-D545-B7D3EE0B3172"

async def main():
    """Updates the state of a MR Star light device."""
    device = MrStarDevice(ADDRESS)
    print("Connecting...")
    await device.connect()
    print("Enabling...")
    async with device as light:
        await light.set_power(True)
        print("Setting brightness...")
        await light.set_brightness(0.01)
        print("Setting color...")
        await light.set_rgb_color((255, 0, 0))

asyncio.run(main())
