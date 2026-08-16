import asyncio
import time
import psutil
import json
import logging
import sys
import os

# Add parent directory to path so we can import lumina
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lumina.backend.lumina_diode import UnidirectionalDiodeTX, UnidirectionalDiodeRX

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("load_test")

class DiodeTest:
    def __init__(self):
        self.packets_sent = 0
        self.packets_received = 0
        self.running = True
        self.cpu_usage = []
        self.mem_usage = []

    def on_message(self, payload):
        self.packets_received += 1

    async def monitor_system(self):
        while self.running:
            self.cpu_usage.append(psutil.cpu_percent(interval=None))
            self.mem_usage.append(psutil.virtual_memory().percent)
            await asyncio.sleep(1)

    async def sender(self, tx: UnidirectionalDiodeTX):
        while self.running:
            payload = {"seq": self.packets_sent, "data": "dummy_payload_for_load_testing" * 10}
            tx.send_telemetry(payload)
            self.packets_sent += 1
            # Adjust frequency to high, e.g. 1000 packets per second
            await asyncio.sleep(0.001)

    async def run(self):
        # 1. Initialize
        rx = UnidirectionalDiodeRX(on_message=self.on_message)
        await rx.listen()

        tx = UnidirectionalDiodeTX()
        await tx.connect()

        self.running = True
        
        # Start tasks
        psutil.cpu_percent() # initial call
        monitor_task = asyncio.create_task(self.monitor_system())
        sender_task = asyncio.create_task(self.sender(tx))

        # Wait for exactly 7 minutes
        duration = 420
        logger.info(f"Starting {duration}-second load test...")
        await asyncio.sleep(duration)
        logger.info("Load test complete.")

        self.running = False
        await monitor_task
        await sender_task
        
        tx.close()
        rx.close()

        # Calculate stats
        drop_rate = 0.0
        if self.packets_sent > 0:
            drop_rate = (self.packets_sent - self.packets_received) / self.packets_sent * 100

        avg_cpu = sum(self.cpu_usage) / len(self.cpu_usage) if self.cpu_usage else 0
        avg_mem = sum(self.mem_usage) / len(self.mem_usage) if self.mem_usage else 0
        max_cpu = max(self.cpu_usage) if self.cpu_usage else 0
        max_mem = max(self.mem_usage) if self.mem_usage else 0

        result = {
            "packets_sent": self.packets_sent,
            "packets_received": self.packets_received,
            "packets_dropped": self.packets_sent - self.packets_received,
            "drop_rate_percent": drop_rate,
            "duration_seconds": duration,
            "cpu_avg_percent": avg_cpu,
            "cpu_max_percent": max_cpu,
            "mem_avg_percent": avg_mem,
            "mem_max_percent": max_mem,
        }
        
        print("\n--- RESULTS JSON ---")
        print(json.dumps(result, indent=4))

if __name__ == "__main__":
    asyncio.run(DiodeTest().run())
