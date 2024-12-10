"""MR Star light device commands."""
from .color import HSColor
from .const import COMMAND_PREFIX, COMMAND_SUFFIX, Command, Effect
from .int import split_uint16


def format_command(command: Command, args: bytes) -> bytes:
    """Formats command with prefix and suffix."""
    if len(args) == 0:
        raise ValueError("Command cannot be empty")
    return bytes([COMMAND_PREFIX, command.value, len(args), *args, COMMAND_SUFFIX])

def format_power_command(is_on: bool) -> bytes:
    """Formats power command."""
    return format_command(Command.SET_POWER, [(1 if is_on else 0)])

def format_brightness_command(brightness: float) -> bytes:
    """Formats brightness command."""
    if brightness < 0 or brightness > 1:
        raise ValueError("Brightness must be between 0 and 1")
    brightness_value = int(1024 * brightness)
    high_byte, low_byte = split_uint16(brightness_value)

    return format_command(Command.SET_BRIGHTNESS, [
        high_byte, low_byte, 0x00, 0x00, 0x00, 0x00
    ])

def format_color_command(color: HSColor) -> bytes:
    """Formats color command."""
    hue, sat = color
    hue_high, hue_low = split_uint16(hue)
    sat_high, sat_low = split_uint16(int(sat * 10))

    return format_command(Command.SET_COLOR, bytes([
        hue_high, hue_low, sat_high, sat_low, 0x00, 0x00
    ]))

def format_reverse_command(is_on: bool) -> bytes:
    """Formats reverse command."""
    return format_command(Command.SET_REVERSE, [(1 if is_on else 0)])

def format_speed_command(speed: float) -> bytes:
    """Formats speed command."""
    if speed < 0 or speed > 1:
        raise ValueError("Speed must be between 0 and 1")
    speed_value = int(100 * speed)
    return format_command(Command.SET_SPEED, [speed_value])

def format_effect_command(effect: Effect) -> bytes:
    """Formats effect command."""
    effect_high, effect_low = split_uint16(effect.value)
    return format_command(Command.SET_EFFECT, [effect_high, effect_low])

def format_length_command(led_count: int) -> bytes:
    """Formats length command."""
    if led_count < 8 or led_count > 300:
        raise ValueError("LED count must be between 8 and 300")
    count_high, count_low = split_uint16(led_count)
    return format_command(Command.SET_LENGTH, [count_high, count_low])
