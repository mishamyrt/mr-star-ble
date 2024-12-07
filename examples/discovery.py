"""Example of automatically discovering and connecting to a MR Star light device."""
import asyncio

from mr_star_ble import MrStarLight


async def main():
    """Auto discover and connect to a MR Star light device."""
    print("Connecting...")
    device = await MrStarLight.discover()
    if device.is_connected:
        print(f"Connected to {device.address}")
        await device.disconnect()
    else:
        print(f"Failed to connect to {device.address}")

asyncio.run(main())
