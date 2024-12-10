"""integer utils"""

UINT16_MAX = 65535

# 0 - 65535
UInt16 = int

# 0 - 255
UInt8 = int

def split_uint16(value: UInt16) -> tuple[UInt8, UInt8]:
    """Splits uint16 value into low and high bytes."""
    if 0 > value or value > UINT16_MAX:
        raise ValueError(f"Value must be between 0 and {UINT16_MAX}, got {value}")
    low_byte = value & 0xFF
    high_byte = (value >> 8) & 0xFF
    return high_byte, low_byte
