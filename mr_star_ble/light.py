"""MR Star light device."""
import asyncio

from bleak import BleakClient, BleakScanner

from .color import HSColor, RGBColor, rgb_to_hs
from .commands import (
    format_brightness_command,
    format_color_command,
    format_command,
    format_power_command,
    format_reverse_command,
    format_speed_command,
)

# Device UUIDs
LIGHT_CHARACTERISTIC = "0000fff3-0000-1000-8000-00805f9b34fb"
LIGHT_SERVICE = "00002022-0000-1000-8000-00805f9b34fb"

class MrStarLight:
    """Represents a MR Star light device."""
    address: str
    client: BleakClient

    def __init__(self, address):
        self.address = address

    @property
    def is_connected(self):
        """Check connection status between this client and the GATT server."""
        return self.client.is_connected

    async def connect(self):
        """Connects to the device."""
        self.client = BleakClient(self.address)
        await self.client.connect()

    async def disconnect(self):
        """Disconnects from the device."""
        await self.client.disconnect()

    async def set_power(self, is_on: bool):
        """Sets the power state of the device."""
        await self.write(format_power_command(is_on))

    async def set_reverse(self, is_on: bool):
        """Sets the power state of the device."""
        await self.write(format_reverse_command(is_on))

    async def set_speed(self, speed: float):
        """Sets the power state of the device."""
        await self.write(format_speed_command(speed))

    async def set_brightness(self, brightness: int):
        """Sets the brightness of the device."""
        await self.write(format_brightness_command(brightness))

    async def set_hs_color(self, color: HSColor):
        """Sets the color of the device."""
        await self.write(format_color_command(color))

    async def set_rgb_color(self, color: RGBColor):
        """Sets the color of the device."""
        await self.set_hs_color(rgb_to_hs(color))

    async def write_command(self, command: int, argument: bytes):
        """Writes a payload to the device."""
        await self.write(format_command(command, argument))

    async def write(self, payload: bytes):
        """Writes a raw payload to the device."""
        await self.client.write_gatt_char(LIGHT_CHARACTERISTIC, payload)

    @staticmethod
    async def discover(timeout=10):
        """Discovers MR Star light device and returns the address."""
        device_found = asyncio.Event()
        address = None

        def callback(device, _):
            nonlocal address
            address = device.address
            device_found.set()

        async with BleakScanner(callback, service_uuids=[LIGHT_SERVICE]) as _:
            async with asyncio.timeout(timeout):
                await device_found.wait()

        device = MrStarLight(address)
        await device.connect()
        return device
