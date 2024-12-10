"""Discover MR Star light device."""
import asyncio

from bleak import BleakScanner, BLEDevice

from .const import LIGHT_SERVICE


async def discover(timeout=10) -> BLEDevice:
    """Discovers MR Star light device and returns the address."""
    device_found = asyncio.Event()
    founded_device: BLEDevice = None

    def handle_discovery(device: BLEDevice, _):
        nonlocal founded_device
        founded_device = device
        device_found.set()

    async with BleakScanner(handle_discovery, service_uuids=[LIGHT_SERVICE]) as _:
        async with asyncio.timeout(timeout):
            await device_found.wait()

    if founded_device is None:
        raise RuntimeError("Device not found")
    return founded_device
