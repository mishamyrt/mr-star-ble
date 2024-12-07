"""MR Star device color utils."""
from colorsys import rgb_to_hsv

RGBColor = tuple[int, int, int]
HSColor = tuple[int, float] # Hue 0-360, Saturation 0-100

def rgb_to_hs(rgb: RGBColor) -> HSColor:
    """Convert RGB color to hue and saturation."""
    red, green, blue = rgb
    hue, saturation, _ = rgb_to_hsv(
        float(red / 255),
        float(green / 255),
        float(blue / 255)
    )
    return int(hue * 360), saturation * 100
