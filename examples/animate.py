"""Example of updating the state of a MR Star light device."""
import asyncio

from bleak import BleakClient

from mr_star_ble import MrStarAPI, discover
from mr_star_ble.transition import animate_color, animate_power, set_framerate

ADDRESS = "DF821C47-03A6-D4C5-D545-B7D3EE0B3172"

async def main():
    """Updates the state of a MR Star light device."""
    dev = await discover()

    client = BleakClient(dev)
    print("Connecting...")
    await client.connect()
    api = MrStarAPI(client)
    # hue_range = transition.ValueRange(0, 360)
    # print(hue_range.shortest_diff(360, 20))
    set_framerate(25)
    await api.set_rgb_color((255, 0, 0))
    await animate_color(api, (0, 100), (120, 100), duration=1)
    await asyncio.sleep(3)
    await animate_power(api, False, 1.0, duration=1.2)
    await asyncio.sleep(3)
    await animate_power(api, True, 1.0, duration=1.2)
    await asyncio.sleep(3)
    await animate_color(api, (120, 100.0), (0, 100.0), duration=1)

    #     await transition.sleep_frame()
    # await client.disconnect()

    # api = MrStarAPI(client)
    # animator = MrStarAnimator(api, framerate=30)
    # await animator.set_brightness(1, duration=1.2)
    # await asyncio.sleep(2)
    # await animator.set_brightness(0, duration=1.2)
    # await animator.set_brightness(1, duration=2)
    # await animator.set_brightness(1, duration=1)
    # await animator.set_brightness(0.5, duration=1)
        # await light.set_rgb_color((255, 0, 0))

asyncio.run(main())
