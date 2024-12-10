"""MR Star light device."""

from bleak import BleakClient

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
from .const import LIGHT_CHARACTERISTIC, Effect


class MrStarLight:
    """Represents a MR Star LED strip."""
    _client: BleakClient

    def __init__(self, client: BleakClient):
        self._client = client

    @property
    def is_connected(self) -> bool:
        """Check connection status between this client and the GATT server."""
        return self._client.is_connected

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
