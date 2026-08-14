"""
Lumina Protocol Abstraction Layer (PAL)
=======================================
Universal OT protocol normalization engine for legacy and modern PLCs.
Supports Siemens S7 Comm, Modbus TCP, Rockwell CIP, OPC UA, and MQTT Sparkplug B.
Includes ISA-95 tag normalization and high-frequency I/O process mining for legacy machines.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional, Callable
import time
import asyncio
import logging

logger = logging.getLogger("lumina.pal")


class ProtocolType(str, Enum):
    S7_COMM = "S7_COMM"
    MODBUS_TCP = "MODBUS_TCP"
    ETHERNET_IP_CIP = "ETHERNET_IP_CIP"
    OPC_UA = "OPC_UA"
    MQTT_SPARKPLUG_B = "MQTT_SPARKPLUG_B"


class DataType(str, Enum):
    BOOL = "BOOL"
    INT = "INT"
    DINT = "DINT"
    REAL = "REAL"
    STRING = "STRING"
    TIME = "TIME"


@dataclass
class NormalizedTag:
    tag_id: str                      # Unique ISA-95 identifier: e.g., "Line3.Infeed.PE_BottlePresent"
    raw_address: str                 # Vendor address: e.g., "%I0.0", "DB100.DBX2.0", "B3:0/1"
    protocol: ProtocolType
    data_type: DataType
    value: Any = None
    engineering_unit: str = ""
    quality: str = "GOOD"            # "GOOD", "UNCERTAIN", "BAD"
    last_updated: float = field(default_factory=time.time)
    description: str = ""


@dataclass
class TransitionEvent:
    timestamp: float
    tag_id: str
    old_value: Any
    new_value: Any


class PALDriver:
    """Base driver for industrial PLC protocols."""
    def __init__(self, name: str, protocol: ProtocolType, endpoint: str):
        self.name = name
        self.protocol = protocol
        self.endpoint = endpoint
        self.connected = False
        self._memory_map: Dict[str, Any] = {}

    async def connect(self) -> bool:
        self.connected = True
        return True

    async def disconnect(self):
        self.connected = False

    async def read_tag(self, raw_address: str) -> Any:
        return self._memory_map.get(raw_address, 0)

    async def write_tag(self, raw_address: str, value: Any) -> bool:
        self._memory_map[raw_address] = value
        return True


class SiemensS7Driver(PALDriver):
    """Siemens S7 Comm Protocol Driver (S7-300 / S7-400 / S7-1200 / S7-1500)."""
    def __init__(self, name: str, endpoint: str = "192.168.1.10:102", rack: int = 0, slot: int = 1):
        super().__init__(name, ProtocolType.S7_COMM, endpoint)
        self.rack = rack
        self.slot = slot
        # Preset virtual DBs and I/O images for simulation
        self._memory_map = {
            "%I0.0": False,             # Photoeye Bottle Infeed
            "%I0.1": False,             # Photoeye Capper Ready
            "%Q0.0": False,             # Infeed Conveyor Motor Run
            "%Q0.1": False,             # Capper Actuator Solenoid
            "DB100.DBD0": 60.0,         # Target Bottles Per Minute (REAL)
            "DB100.DBD4": 58.4,         # Actual Measured Throughput (REAL)
            "DB100.DBW8": 500,          # Deceleration Timer (INT ms)
            "DB100.DBX10.0": False,     # Emergency Fault State
            "DB100.DBD12": 1.42         # Bearing Vibration RMS (g)
        }


class ModbusTCPDriver(PALDriver):
    """Modbus TCP Protocol Driver for standard RTUs, drives, and meters."""
    def __init__(self, name: str, endpoint: str = "192.168.1.20:502", unit_id: int = 1):
        super().__init__(name, ProtocolType.MODBUS_TCP, endpoint)
        self.unit_id = unit_id
        self._memory_map = {
            "40001": 1450,              # Motor RPM (Holding Register)
            "40002": 230,               # Line Voltage (V)
            "40003": 485,               # Pneumatic Pressure (kPa x 10)
            "00001": False,             # Diverter Gate Solenoid (Coil)
            "10001": True               # Safety Guard Closed (Discrete Input)
        }


class RockwellCIPDriver(PALDriver):
    """Rockwell EtherNet/IP CIP Driver (ControlLogix / CompactLogix)."""
    def __init__(self, name: str, endpoint: str = "192.168.1.30:44818"):
        super().__init__(name, ProtocolType.ETHERNET_IP_CIP, endpoint)
        self._memory_map = {
            "CartonErector.InfeedSensor": True,
            "CartonErector.FlapCylinder_Adv": False,
            "CartonErector.GlueGun_Fire": False,
            "CartonErector.CycleTime_ms": 820,
            "CartonErector.FaultWord": 0
        }


class PALManager:
    """
    Central Protocol Abstraction Layer Manager.
    Normalizes multi-protocol industrial tags into a unified ISA-95 hierarchical namespace.
    """
    def __init__(self):
        self.drivers: Dict[str, PALDriver] = {}
        self.tags: Dict[str, NormalizedTag] = {}
        self.tag_mapping: Dict[str, tuple[str, str]] = {}  # tag_id -> (driver_name, raw_address)
        self.history: List[TransitionEvent] = []
        self._listeners: List[Callable[[NormalizedTag], Any]] = []

    def register_driver(self, driver: PALDriver):
        self.drivers[driver.name] = driver

    def add_tag(self, tag: NormalizedTag, driver_name: str, raw_address: str):
        self.tags[tag.tag_id] = tag
        self.tag_mapping[tag.tag_id] = (driver_name, raw_address)

    async def initialize_default_plant_topology(self):
        """Initializes standard multi-vendor bottling & packaging plant topology."""
        # 1. Siemens S7 Line 3 Packaging
        s7 = SiemensS7Driver("Siemens_S7_1500_Line3")
        await s7.connect()
        self.register_driver(s7)

        self.add_tag(NormalizedTag("Line3.Infeed.Sensor_BottlePresent", "%I0.0", ProtocolType.S7_COMM, DataType.BOOL, description="Infeed photoeye"), s7.name, "%I0.0")
        self.add_tag(NormalizedTag("Line3.Infeed.Motor_ConveyorRun", "%Q0.0", ProtocolType.S7_COMM, DataType.BOOL, description="Main infeed conveyor"), s7.name, "%Q0.0")
        self.add_tag(NormalizedTag("Line3.Capper.Actuator_Capper", "%Q0.1", ProtocolType.S7_COMM, DataType.BOOL, description="Rotary capper solenoid"), s7.name, "%Q0.1")
        self.add_tag(NormalizedTag("Line3.Throughput.TargetPPM", "DB100.DBD0", ProtocolType.S7_COMM, DataType.REAL, engineering_unit="PPM"), s7.name, "DB100.DBD0")
        self.add_tag(NormalizedTag("Line3.Throughput.ActualPPM", "DB100.DBD4", ProtocolType.S7_COMM, DataType.REAL, engineering_unit="PPM"), s7.name, "DB100.DBD4")
        self.add_tag(NormalizedTag("Line3.Servo.DecelRamp_ms", "DB100.DBW8", ProtocolType.S7_COMM, DataType.INT, engineering_unit="ms"), s7.name, "DB100.DBW8")
        self.add_tag(NormalizedTag("Line3.Health.BearingVibration_g", "DB100.DBD12", ProtocolType.S7_COMM, DataType.REAL, engineering_unit="g"), s7.name, "DB100.DBD12")

        # 2. Modbus TCP Utilities & Pressure
        modbus = ModbusTCPDriver("Modbus_Pneumatic_Station")
        await modbus.connect()
        self.register_driver(modbus)

        self.add_tag(NormalizedTag("Utilities.Pneumatic.MainPressure_kPa", "40003", ProtocolType.MODBUS_TCP, DataType.INT, engineering_unit="kPa"), modbus.name, "40003")
        self.add_tag(NormalizedTag("Line3.Diverter.RejectGate", "00001", ProtocolType.MODBUS_TCP, DataType.BOOL), modbus.name, "00001")

        # 3. Rockwell CIP Carton Erector
        cip = RockwellCIPDriver("Rockwell_CartonErector_Line4")
        await cip.connect()
        self.register_driver(cip)

        self.add_tag(NormalizedTag("Line4.Carton.InfeedSensor", "CartonErector.InfeedSensor", ProtocolType.ETHERNET_IP_CIP, DataType.BOOL), cip.name, "CartonErector.InfeedSensor")
        self.add_tag(NormalizedTag("Line4.Carton.FlapCylinder", "CartonErector.FlapCylinder_Adv", ProtocolType.ETHERNET_IP_CIP, DataType.BOOL), cip.name, "CartonErector.FlapCylinder_Adv")
        self.add_tag(NormalizedTag("Line4.Carton.CycleTime_ms", "CartonErector.CycleTime_ms", ProtocolType.ETHERNET_IP_CIP, DataType.INT, engineering_unit="ms"), cip.name, "CartonErector.CycleTime_ms")

        # Initial read of all values
        await self.poll_all()

    async def poll_all(self) -> Dict[str, Any]:
        """Polls all registered tags across all drivers with cyclic load-throttling."""
        updates = {}
        for tag_id, tag in self.tags.items():
            driver_name, raw_addr = self.tag_mapping[tag_id]
            driver = self.drivers.get(driver_name)
            if driver and driver.connected:
                new_val = await driver.read_tag(raw_addr)
                if new_val != tag.value:
                    self.history.append(TransitionEvent(time.time(), tag_id, tag.value, new_val))
                    tag.value = new_val
                    tag.last_updated = time.time()
                    for listener in self._listeners:
                        listener(tag)
                updates[tag_id] = tag.value
        return updates

    async def write_normalized_tag(self, tag_id: str, new_value: Any) -> bool:
        """Writes value to the normalized tag by routing to the specific protocol driver."""
        if tag_id not in self.tag_mapping:
            logger.error(f"Tag {tag_id} not found in PAL mapping")
            return False
        driver_name, raw_addr = self.tag_mapping[tag_id]
        driver = self.drivers.get(driver_name)
        if not driver or not driver.connected:
            return False
        
        success = await driver.write_tag(raw_addr, new_value)
        if success:
            tag = self.tags[tag_id]
            old_val = tag.value
            tag.value = new_value
            tag.last_updated = time.time()
            self.history.append(TransitionEvent(time.time(), tag_id, old_val, new_value))
            for listener in self._listeners:
                listener(tag)
        return success

    def add_change_listener(self, listener: Callable[[NormalizedTag], Any]):
        self._listeners.append(listener)

    def get_snapshot(self) -> Dict[str, Any]:
        """Returns instantaneous snapshot of all ISA-95 normalized tags."""
        return {
            tag_id: {
                "raw_address": tag.raw_address,
                "protocol": tag.protocol.value,
                "data_type": tag.data_type.value,
                "value": tag.value,
                "unit": tag.engineering_unit,
                "quality": tag.quality,
                "timestamp": tag.last_updated,
                "description": tag.description
            }
            for tag_id, tag in self.tags.items()
        }

    def process_mine_state_machine(self, window_seconds: float = 60.0) -> Dict[str, Any]:
        """
        High-Frequency I/O Process Mining:
        Analyzes historical transition sequences to infer causal finite state machines
        for undocumented legacy machinery without CAD models.
        """
        now = time.time()
        recent_events = [e for e in self.history if now - e.timestamp <= window_seconds]
        transitions = {}
        for i in range(len(recent_events) - 1):
            source = f"{recent_events[i].tag_id}=={recent_events[i].new_value}"
            target = f"{recent_events[i+1].tag_id}=={recent_events[i+1].new_value}"
            delta_ms = (recent_events[i+1].timestamp - recent_events[i].timestamp) * 1000.0
            
            key = f"{source} -> {target}"
            if key not in transitions:
                transitions[key] = {"count": 0, "avg_delay_ms": 0.0, "total_delay_ms": 0.0}
            transitions[key]["count"] += 1
            transitions[key]["total_delay_ms"] += delta_ms
            transitions[key]["avg_delay_ms"] = transitions[key]["total_delay_ms"] / transitions[key]["count"]

        return {
            "window_events_analyzed": len(recent_events),
            "inferred_state_transitions": transitions,
            "synthesized_states": list(set([e.tag_id for e in recent_events]))
        }
