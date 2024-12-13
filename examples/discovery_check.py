"""Example of automatically discovering and connecting to a MR Star light device."""
import asyncio

from bleak import BleakClient

from mr_star_ble import discover


async def main():
    """Auto discover and connect to a MR Star light device."""
    print("Searching...")
    devices = await discover()
    if len(devices) == 0:
        print("No devices found")
        return
    print(f"Devices found: {len(devices)}")
    for device in devices:
        print(f"Connecting to {device.address}...")
        client = BleakClient(device)
        await client.connect()
        print(f"Connected to {device.address}")
        await client.disconnect()

asyncio.run(main())
