"""
Lumina Unidirectional Data Diode (Application Layer Simulation)
=============================================================
Simulates a physical layer 1 optical data diode (like Owl Cyber Defense)
using strict UDP unidirectional casting.

- The TX side (Plant/PLC network) can only broadcast UDP out.
- The RX side (AI/Server network) can only bind and listen, with no route back.
"""

import asyncio
import json
import logging
from typing import Callable, Any, Dict

logger = logging.getLogger("lumina.diode")

UDP_DIODE_IP = "127.0.0.1"
UDP_DIODE_PORT = 9999

class UnidirectionalDiodeTX:
    """The Transmitter (Plant side). Strictly sends data out."""
    def __init__(self, ip: str = UDP_DIODE_IP, port: int = UDP_DIODE_PORT):
        self.ip = ip
        self.port = port
        self.transport = None

    class DiodeTXProtocol(asyncio.DatagramProtocol):
        def connection_made(self, transport):
            pass

    async def connect(self):
        loop = asyncio.get_running_loop()
        self.transport, _ = await loop.create_datagram_endpoint(
            lambda: self.DiodeTXProtocol(),
            remote_addr=(self.ip, self.port)
        )
        logger.info(f"Data Diode TX engaged targeting {self.ip}:{self.port}")

    def send_telemetry(self, telemetry: Dict[str, Any]):
        if self.transport:
            try:
                payload = json.dumps(telemetry).encode('utf-8')
                self.transport.sendto(payload)
            except Exception as e:
                logger.error(f"Diode TX Error: {e}")

    def close(self):
        if self.transport:
            self.transport.close()


class UnidirectionalDiodeRX:
    """The Receiver (AI side). Strictly listens, cannot reply."""
    def __init__(self, on_message: Callable[[Dict[str, Any]], None], ip: str = UDP_DIODE_IP, port: int = UDP_DIODE_PORT):
        self.on_message = on_message
        self.ip = ip
        self.port = port
        self.transport = None

    class DiodeRXProtocol(asyncio.DatagramProtocol):
        def __init__(self, callback: Callable[[Dict[str, Any]], None]):
            self.callback = callback

        def connection_made(self, transport):
            pass

        def datagram_received(self, data, addr):
            try:
                payload = json.loads(data.decode('utf-8'))
                self.callback(payload)
            except Exception as e:
                logger.error(f"Diode RX Decode Error: {e}")

    async def listen(self):
        loop = asyncio.get_running_loop()
        self.transport, _ = await loop.create_datagram_endpoint(
            lambda: self.DiodeRXProtocol(self.on_message),
            local_addr=(self.ip, self.port)
        )
        logger.info(f"Data Diode RX listening on {self.ip}:{self.port}")

    def close(self):
        if self.transport:
            self.transport.close()
