"""MR Star light device."""
import asyncio
from contextlib import AsyncExitStack

from bleak import BleakClient, BleakScanner, BLEDevice

from .color import HSColor, RGBColor, rgb_to_hs
from .commands import (
    format_brightness_command,
    format_color_command,
    format_command,
    format_effect_command,
    format_length_command,
    format_power_command,
    format_reverse_command,
    format_speed_command,
)
from .effect import Effect

# Device UUIDs
LIGHT_CHARACTERISTIC = "0000fff3-0000-1000-8000-00805f9b34fb"
LIGHT_SERVICE = "00002022-0000-1000-8000-00805f9b34fb"

class MrStarLight:
    """Represents a MR Star LED strip."""
    _address_or_ble_device: BLEDevice | str
    _client: BleakClient
    _client_stack: AsyncExitStack
    _lock: asyncio.Lock

    def __init__(self, address_or_ble_device: BLEDevice | str):
        self._address_or_ble_device = address_or_ble_device
        self._client_stack = AsyncExitStack()
        self._lock = asyncio.Lock()
        self._client = None

    @property
    def address(self) -> str:
        """The address (uuid or mac) of the device."""
        if isinstance(self._address_or_ble_device, BLEDevice):
            return self._address_or_ble_device.address
        return self._address_or_ble_device

    @property
    def is_connected(self) -> bool:
        """Check connection status between this client and the GATT server."""
        return self._client is not None and self._client.is_connected

    async def connect(self, timeout=10):
        """Connects to the device."""
        if self.is_connected:
            return
        async with self._lock:
            self._client = await self._client_stack.enter_async_context(
            BleakClient(self._address_or_ble_device, timeout=timeout))

    async def disconnect(self):
        """Disconnects from the device."""
        await self._client.disconnect()

    async def set_power(self, is_on: bool):
        """Sets the power state of the device."""
        await self.write(format_power_command(is_on))

    async def set_length(self, length: int):
        """Sets the power state of the device."""
        await self.write(format_length_command(length))

    async def set_effect(self, effect: Effect):
        """Sets the effect of the device."""
        await self.write(format_effect_command(effect))

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
        if not self.is_connected:
            raise RuntimeError("Device is not connected")
        await self._client.write_gatt_char(LIGHT_CHARACTERISTIC, payload)

    @staticmethod
    async def discover(timeout=10):
        """Discovers MR Star light device and returns the address."""
        device_found = asyncio.Event()
        address = None

        def handle_discovery(device, _):
            nonlocal address
            address = device.address
            device_found.set()

        async with BleakScanner(handle_discovery, service_uuids=[LIGHT_SERVICE]) as _:
            async with asyncio.timeout(timeout):
                await device_found.wait()

        device = MrStarLight(address)
        await device.connect()
        return device
