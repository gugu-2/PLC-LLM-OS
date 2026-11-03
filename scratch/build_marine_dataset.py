# scratch/build_marine_dataset.py
import json
import uuid
import re
import sys

def build_dataset():
    prompt = """You are generating a SINGLE ultra-dense IEC 61131-3 Structured Text dataset for the **Marine Engineering & Mega Container Shipping** industry.

**Domain**: 24,000 TEU Ultra Large Container Vessel (ULCV) WinGD / MAN ME-GI Two-Stroke Low-Speed Dual-Fuel (LNG / Marine Gas Oil) 75 MW Main Propulsion Engine with 300-bar Hydraulic Gas Injection & Cryogenic Boil-Off Gas (BOG) Sub-cooler Re-liquefaction.

**Function Block Name**: `FB_Marine_ContainerVessel_DualFuelLNG_MEGI_BOG`

**Engineering Context**:
- 24,000 TEU Ultra Large Container Vessel (ULCV), length 400m, beam 61.5m, draft 16.5m, displacement ~240,000 metric tons.
- Propulsion: WinGD 12X92-DF / MAN B&W 11G95ME-C9.5-GI two-stroke low-speed crosshead diesel engine (75 MW MCR at 80.0 RPM direct-coupled to keyless fixed-pitch propeller).
- High-Pressure Fuel Gas Supply System (FGSS): 300-bar common-rail hydraulic booster accumulator rail, cryogenic high-pressure multi-piston LNG pump (0-320 bar), and Glycol-Water PCHE vaporizer.
- Cryogenic Boil-Off Gas (BOG) Handling: Multi-stage cryogenic BOG compressor cascade with Joule-Thomson expansion valve and subcooler re-liquefaction unit handling boil-off from 18,600 m3 Type B LNG fuel tanks (-162 °C).
- Dual-Fuel Combustion Dynamics: Pilot MGO micro-injection (1-2% fuel energy) for compression ignition, followed by high-pressure gas injection at 300 bar right after TDC. LNG energy substitution ratio reaching up to 95-98%.
- Dynamic Double-Wall Safety Piping: Engine fuel gas distribution rails enclosed in ventilated annular outer ducting continuously monitored by 2oo3 Triple Modular Redundancy (TMR) optical infrared LEL hydrocarbon sensors.
- Rapid Bumpless Fuel Changeover: Uninterrupted transfer between Gas Mode and 100% Diesel Mode in less than one engine stroke / revolution (<750 ms) without shaft speed dip or torque droop upon gas trip or supply instability.
- In-cylinder Combustion Monitoring: 2oo3 Kistler piezoresistive dynamic pressure transducers per cylinder monitoring Pmax (up to 215 bar), compression pressure, and dP/dθ knock detection with automated cylinder gas index trimming and timing retardation.
- Turbocharger Surge & Mechanical Protection: High-frequency casing vibration monitoring, turbine inlet temperature limit, main bearing lube oil pressure 2oo3 TMR voting, and crankcase optical oil mist detection.
- Rough Sea-State Torque Limiting: Wave-induced propeller emergence and racing detection with proactive governor torque derating and propeller pitch coordination to prevent mechanical overspeed and compressor surging.

**Required Mathematical Rigor**:
1. Discrete State-Space Matrix Model (6x6):
   - State vector x = [Shaft RPM deviation, Turbocharger RPM deviation, Scavenge Air Pressure deviation, 300-bar Gas Rail Pressure deviation, Mean Indicated Pressure deviation, Cryogenic Subcooler Temperature deviation]
   - Full numerical matrices A (6x6), B (6x4), C (6x6), D (6x4) evaluated at 10 ms discrete scan cycle.
   - Dynamic propagation: x_{k+1} = A*x_k + B*u_k, y_k = C*x_k + D*u_k with complete matrix algebra.
2. Model Predictive Control (MPC) Receding Horizon Quadratic Cost Functional:
   - Penalty matrices Q (6x6 state tracking), R (4x4 control effort favoring LNG substitution over MGO), S (4x4 control slew rate damping), and P (6x6 Riccati terminal cost).
   - Iterative quadratic program solver (projected gradient descent with box constraints) calculating optimal gas/MGO fuel indices and hydraulic pump displacement.
3. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting:
   - Double-wall annular hydrocarbon LEL sensors (A, B, C) with median selection, 10% LEL warning, 30% LEL emergency trip, and discrepancy timer debouncing.
   - Main bearing lube oil pressure sensors (A, B, C) with 3.0 bar shutdown trip.
   - 12-cylinder Kistler combustion pressure sensors (A, B, C per cylinder) with mid-value selection, cylinder balancing, and knock detection.
4. Fuel Gas Train (FVT) Block-and-Bleed & Cryogenic Safety Logic:
   - Dynamic inert N2 purge sequence with block-and-bleed valve sequencing.
   - Pressure decay leak testing (rate-of-decay dP/dt evaluation).
   - Cryogenic BOG subcooler Joule-Thomson expansion valve control and compressor anti-surge recirculating valve modulation.
5. ISA-18.2 Multi-Tiered Alarm Hierarchy & 32-bit Diagnostic Status Words:
   - Prioritized alarms: Annular gas leak HH, Cylinder knock HH, Main bearing low pressure LL, Turbocharger surge HH, Crankcase oil mist HH, Scavenge fire HH.
   - Packed into DWORD bitfields with bitwise operators.
6. Multi-Stage Master Finite State Machine (FSM):
   - Minimum 10 states: ENGINE_STANDBY_MGO_PRELUBE (0), DIESEL_SLOW_TURNING_BLOWDOWN (10), MGO_CRUISING_PROPULSION_STABLE (20), GAS_VALVE_TRAIN_N2_INERT_PURGE (30), FVT_PRESSURE_DECAY_LEAK_TEST (40), GAS_RAIL_300BAR_HYDRAULIC_PRESSURIZE (50), BUMPLESS_DIESEL_TO_LNG_TRANSITION (60), HIGH_EFFICIENCY_DUAL_FUEL_CRUISE (70), ROUGH_SEAS_PROPELLER_PITCH_LIMIT (80), GAS_TRIP_FAILSAFE_DIESEL_FALLBACK (90), POST_TRIP_N2_VENT_AND_PURGE (100), EMERGENCY_SHUTDOWN_COOLDOWN (110).

**Output Format**:
- Code fenced with TRIPLE backticks and `iec-st`: ` ```iec-st `
- First line: `FUNCTION_BLOCK FB_Marine_ContainerVessel_DualFuelLNG_MEGI_BOG`
- Last line: `END_FUNCTION_BLOCK`
- Minimum length: 65,000 to 90,000+ characters of deeply engineered Structured Text.

Save output to `data/swarm_raw/agent_<uuid>.json` and reply: `EVOLUTION COMPLETE: Marine Container Vessel Dual Fuel LNG MEGI BOG`"""

    print("Generating code...")
    # We will assemble code in parts
    return prompt

if __name__ == "__main__":
    build_dataset()
