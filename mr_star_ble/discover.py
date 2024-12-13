"""Discover MR Star light device."""
import asyncio

from bleak import BleakScanner, BLEDevice

from .const import LIGHT_SERVICE


async def discover(timeout=10) -> list[BLEDevice]:
    """Discovers MR Star light device and returns the address."""
    devices: list[BLEDevice] = []

    def handle_discovery(device: BLEDevice, _):
        if device not in devices:
            devices.append(device)

    async with BleakScanner(handle_discovery, service_uuids=[LIGHT_SERVICE]) as _:
        await asyncio.sleep(timeout)

    return devices
