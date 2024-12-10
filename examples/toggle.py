"""Example of automatically discovering and connecting to a MR Star light device."""
import asyncio

from mr_star_ble import discover
from mr_star_ble.device import MrStarDevice


async def toggle_light(device: MrStarDevice, count: int, interval: float):
    """Toggle the power state of the device a number of times."""
    async with device as light:
        while count > 0:
            await light.set_power(False)
            await asyncio.sleep(interval)
            await light.set_power(True)
            await asyncio.sleep(interval)
            count -= 1

async def main():
    """Auto discover and connect to a MR Star light device."""
    print("Discovering...")
    ble_device = await discover(timeout=20)
    print(f"Device discovered at {ble_device.address}")
    device = MrStarDevice(ble_device, ttl=20)
    await device.connect()
    asyncio.create_task(toggle_light(device, 10, 1))
    await asyncio.sleep(30)
    await device.disconnect()

asyncio.run(main())
