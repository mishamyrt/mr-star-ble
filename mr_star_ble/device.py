"""Keep alive wrapper for MR Star Garland."""
import asyncio
from logging import getLogger

from bleak import BleakClient, BLEDevice
from bleak.exc import BleakDeviceNotFoundError, BleakError

from .light import MrStarLight

_LOGGER = getLogger(__name__)

class MrStarDevice:
    """Wrapper to keep the connection with MR Star Garland alive."""
    _client: BleakClient
    _ttl: int
    _lock: asyncio.Lock
    _stopping: asyncio.Event
    _stopped: asyncio.Event
    _connected: asyncio.Event
    _active: bool

    def __init__(self, address_or_ble_device: BLEDevice | str, ttl=120):
        """Initialize the wrapper."""
        self._client = BleakClient(address_or_ble_device)
        self._ttl = ttl
        self._lock = asyncio.Lock()
        self._stopping = asyncio.Event()
        self._stopped = asyncio.Event()
        self._connected = asyncio.Event()

    @property
    def is_connected(self) -> bool:
        """Check connection status between this client and the Mr Star device."""
        return self._client.is_connected

    async def connect(self, await_connected: bool = True):
        """Start the keep alive task."""
        self._stopped.clear()
        asyncio.create_task(self._keep_alive())
        if await_connected:
            await self._connected.wait()

    async def disconnect(self):
        """Stop the keep alive task."""
        self._stopping.set()
        await self._stopped.wait()

    async def __aenter__(self):
        _LOGGER.debug("Acquiring lock for context %s", self._client.address)
        await self._lock.acquire()
        return MrStarLight(self._client)

    async def __aexit__(self, exc_type, exc_value, traceback):
        _LOGGER.debug("Releasing lock for context %s", self._client.address)
        self._lock.release()

    async def _keep_alive(self):
        """Keep alive task."""
        while True:
            async with self._lock:
                if self._client.is_connected:
                    await self._client.disconnect()
                    self._connected.clear()
                try:
                    await self._client.connect()
                    self._connected.set()
                except BleakDeviceNotFoundError:
                    _LOGGER.debug("Device %s not found", self._client.address)
                except BleakError:
                    _LOGGER.debug("Error connecting to device %s", self._client.address)
            try:
                async with asyncio.timeout(self._ttl):
                    await self._stopping.wait()
                    await self._client.disconnect()
                    self._connected.clear()
                    self._stopped.set()
                    _LOGGER.debug("Disconnected from device %s", self._client.address)
                    break
            except asyncio.TimeoutError:
                _LOGGER.debug("Session timeout for device %s", self._client.address)
