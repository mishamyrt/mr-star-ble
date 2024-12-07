# MR Star BLE [![Quality assurance](https://github.com/mishamyrt/mr-star-ble/actions/workflows/qa.yaml/badge.svg)](https://github.com/mishamyrt/mr-star-ble/actions/workflows/qa.yaml)

This library allows you to control BLE devices supported by MR Star application via Python.

## Installation

```bash
pip install mr_star_ble
```

## Usage

```python
import asyncio
from mr_star_ble import MrStarLight

async def main():
    # Find and connect to a MR Star light device
    device = await MrStarLight.discover()
    await device.connect()
    # Set the light state
    await device.set_power(False)
    await device.set_brightness(0.01)
    await device.set_rgb_color((255, 0, 0))

asyncio.run(main())
```