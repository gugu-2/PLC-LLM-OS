# Hardware Abstraction Layer (PAL)

## 1. The Vendor Lock-In Problem
Industrial automation is heavily segmented. Siemens PLCs require PROFINET and S7 communication. Allen-Bradley requires EtherNet/IP and CIP. Modbus TCP is the universal, albeit slow, fallback. 
LLMs cannot be expected to generate specific network packets for each proprietary protocol.

## 2. Protocol Abstraction Layer (`lumina_pal.py`)
Lumina solves this with its Protocol Abstraction Layer (PAL). 
The AI generates generic logic (e.g., `Write TRUE to Output_Valve_1`). The PAL acts as the translation layer.

### Supported Drivers:
- **`SiemensS7Driver`:** Uses `python-snap7` to read/write directly to Datablocks (DB) and memory markers on S7-1200 and S7-1500 controllers.
- **`RockwellCIPDriver`:** Uses `pycomm3` to communicate over Ethernet/IP to Logix5000 controllers via CIP path routing.
- **`ModbusTCPDriver`:** Uses `pymodbus` for universal register reading/writing (Coils, Holding Registers).

## 3. Graceful Mock Degradation
To enable rapid software iteration without requiring a million-dollar hardware lab, the PAL utilizes graceful mock degradation.
- When `server.py` initializes, the `PALManager` attempts to ping the physical PLCs at their configured IP addresses.
- If the hardware is unreachable (e.g., a developer working locally), the PAL seamlessly injects a `Mock` fallback driver. 
- The AI and the Frontend have absolutely no idea they are talking to a mock driver. Read/Write calls succeed instantly, allowing the 5Hz telemetry loop and the UI to function flawlessly without physical hardware.
