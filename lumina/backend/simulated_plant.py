"""
Lumina Packaging Plant Physics Simulator
=========================================
Provides real-time kinematic, pneumatic, and electrical emulation of a
high-speed consumer packaged goods (CPG) packaging line with dynamic fault injection.
"""

import asyncio
import time
import math
import random
from typing import Dict, Any, List, Optional
try:
    from lumina.backend.lumina_pal import PALManager, TagDataType
except ImportError:
    from lumina_pal import PALManager, TagDataType


class SimulatedPackagingPlant:
    """
    Emulates physical plant dynamics:
      - Line 3: Bottle Infeed & Rotary Capper (Siemens S7-1500 + Sinamics S120 Servo)
      - Line 4: High-Speed Carton Erector (Modbus Pneumatic Island + Rockwell GuardLogix)
    """
    def __init__(self, pal: PALManager):
        self.pal = pal
        self.running = False
        
        # Physical plant states
        self.line3_running = True
        self.line3_decel_ramp_ms = 500
        self.line3_bottle_rate_ppm = 58.0
        self.line3_motor_current_a = 4.2
        self.line3_bearing_temp_c = 42.5
        self.line3_vibration_g = 1.2
        
        self.line4_running = True
        self.line4_cycle_time_ms = 820
        self.line4_pneumatic_pressure_kpa = 610
        self.line4_cartons_total = 14200
        
        # Injected faults & degradation parameters
        self.active_faults: List[str] = []
        self.total_avoided_downtime_dollars = 12450.0

    async def start_simulation_loop(self):
        """Runs the physics simulation clock at 5Hz (200ms ticks)."""
        self.running = True
        while self.running:
            now = time.time()
            
            # 1. Line 3: Kinematics, Bearing Harmonics, Motor Torque
            if self.line3_running:
                base_vib = 1.2 + max(0.0, (500.0 - self.line3_decel_ramp_ms)) * 0.0008
                if "BEARING_DEGRADATION_LINE3" in self.active_faults:
                    # Characteristic bearing defect vibration (BPFO/BPFI harmonic modulation)
                    fault_vib = 1.0 + 0.15 * math.sin(now * 24.17) + random.uniform(-0.08, 0.08)
                    self.line3_vibration_g = round(base_vib + fault_vib, 3)
                    self.line3_bearing_temp_c = min(78.0, self.line3_bearing_temp_c + 0.02)
                else:
                    self.line3_vibration_g = round(base_vib + random.uniform(-0.03, 0.03), 3)
                    self.line3_bearing_temp_c = max(42.5, self.line3_bearing_temp_c - 0.02)

                self.line3_bottle_rate_ppm = round(55.0 + (500.0 - self.line3_decel_ramp_ms) * 0.045 + random.uniform(-0.5, 0.5), 1)
                
                # Write to S7 memory via PAL
                await self.pal.write_normalized_tag("Line3.Infeed.BearingVibration_g", self.line3_vibration_g)
                await self.pal.write_normalized_tag("Line3.Infeed.Servo_Velocity_PPM", self.line3_bottle_rate_ppm)
                await self.pal.write_normalized_tag("Line3.Infeed.DecelRamp_ms", self.line3_decel_ramp_ms)

            # 2. Line 4: Pneumatics & Carton Folding
            if self.line4_running:
                if "PNEUMATIC_PRESSURE_DROP_LINE4" in self.active_faults:
                    self.line4_pneumatic_pressure_kpa = max(380, self.line4_pneumatic_pressure_kpa - 2)
                else:
                    self.line4_pneumatic_pressure_kpa = min(610, self.line4_pneumatic_pressure_kpa + 2)

                # Minor jitter on cycle time
                cycle_jitter = int(self.line4_cycle_time_ms + random.randint(-4, 4))
                self.line4_cartons_total += 1
                
                await self.pal.write_normalized_tag("Line4.Carton.PneumaticPressure_kPa", self.line4_pneumatic_pressure_kpa)
                await self.pal.write_normalized_tag("Line4.Carton.CycleTime_ms", cycle_jitter)
                await self.pal.write_normalized_tag("Line4.Carton.TotalCount", self.line4_cartons_total)

            await asyncio.sleep(0.2)

    def inject_fault(self, fault_type: str):
        if fault_type not in self.active_faults:
            self.active_faults.append(fault_type)

    def trigger_fault(self, fault_type: str):
        self.inject_fault(fault_type)

    def clear_faults(self):
        self.active_faults.clear()

    def apply_ai_patch(self, tag_id: str, new_value: Any) -> bool:
        """Applies hot-swapped PLC parameter update from verified AI engine."""
        if "DecelRamp" in tag_id:
            self.line3_decel_ramp_ms = int(new_value)
            if "BEARING_DEGRADATION_LINE3" in self.active_faults and self.line3_decel_ramp_ms <= 380:
                self.active_faults.remove("BEARING_DEGRADATION_LINE3")
                self.total_avoided_downtime_dollars += 42500.0
            return True
        elif "CycleTime" in tag_id:
            self.line4_cycle_time_ms = int(new_value)
            if "PNEUMATIC_PRESSURE_DROP_LINE4" in self.active_faults:
                self.active_faults.remove("PNEUMATIC_PRESSURE_DROP_LINE4")
                self.total_avoided_downtime_dollars += 18000.0
            return True
        return False

    def get_plant_telemetry_summary(self) -> Dict[str, Any]:
        """Returns structured plant telemetry summary for UI and benchmarking."""
        l3_status = "WARNING_VIBRATION_RESONANCE" if "BEARING_DEGRADATION_LINE3" in self.active_faults else "OPTIMAL"
        l4_status = "WARNING_PRESSURE_DROP" if "PNEUMATIC_PRESSURE_DROP_LINE4" in self.active_faults else "OPTIMAL"

        return {
            "overall_oee_percent": 90.2 if not self.active_faults else 78.4,
            "predicted_uptime_probability": 99.4 if not self.active_faults else 82.5,
            "total_avoided_downtime_dollars": self.total_avoided_downtime_dollars,
            "lines": [
                {
                    "machine_id": "Line3_Infeed",
                    "status": l3_status,
                    "vibration_rms_g": self.line3_vibration_g,
                    "throughput_ppm": self.line3_bottle_rate_ppm,
                    "decel_ramp_ms": self.line3_decel_ramp_ms,
                    "bearing_temp_c": self.line3_bearing_temp_c
                },
                {
                    "machine_id": "Line4_Carton",
                    "status": l4_status,
                    "pressure_kpa": self.line4_pneumatic_pressure_kpa,
                    "cycle_time_ms": self.line4_cycle_time_ms,
                    "total_cartons": self.line4_cartons_total
                }
            ]
        }
