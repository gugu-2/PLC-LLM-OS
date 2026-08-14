"""
Lumina Simulated Industrial Packaging Plant
===========================================
Simulates a multi-vendor manufacturing facility with realistic kinematics,
continuous sensor telemetry, and dynamic fault injection.
"""

import asyncio
import time
import math
import random
from typing import Dict, Any, List, Optional
from lumina_pal import PALManager, NormalizedTag, ProtocolType, DataType


class SimulatedPackagingPlant:
    def __init__(self, pal: PALManager):
        self.pal = pal
        self.running = False
        self.active_faults: List[str] = []
        self._step_counter = 0

        # Dynamic physical state variables
        self.line3_running = True
        self.line3_target_ppm = 60.0
        self.line3_actual_ppm = 58.4
        self.line3_decel_ramp_ms = 500
        self.line3_bearing_vibration_g = 1.35
        self.line3_motor_current_a = 4.2
        self.line3_bearing_temp_c = 44.5

        self.line4_running = True
        self.line4_pressure_kpa = 610
        self.line4_cycle_time_ms = 820
        self.line4_cartons_total = 14200

        self.total_avoided_downtime_dollars = 12450.0

    async def start_simulation_loop(self):
        """Runs the 100ms continuous simulation clock."""
        self.running = True
        while self.running:
            self._step_counter += 1
            now = time.time()

            # 1. Physics simulation for Line 3 Infeed & Capper
            if self.line3_running:
                # Vibration is an inverse function of decel ramp + small noise
                # If decel ramp is 500ms, baseline is ~1.4g. If fault injected, rises to ~2.6g
                base_vib = 1.2 + (500.0 - self.line3_decel_ramp_ms) * 0.0008
                if "BEARING_DEGRADATION_LINE3" in self.active_faults:
                    base_vib += 1.1 + 0.1 * math.sin(now * 2.0)
                    self.line3_bearing_temp_c = min(72.0, self.line3_bearing_temp_c + 0.02)
                else:
                    self.line3_bearing_temp_c = max(44.0, self.line3_bearing_temp_c - 0.01)

                self.line3_bearing_vibration_g = round(base_vib + random.uniform(-0.03, 0.03), 3)

                # Throughput calculation
                if self.line3_bearing_vibration_g > 2.2:
                    self.line3_actual_ppm = round(52.0 + random.uniform(-1.0, 1.0), 1)
                else:
                    # Optimized ramp gives closer to target 60 PPM
                    ramp_efficiency = (500.0 - self.line3_decel_ramp_ms) * 0.03
                    self.line3_actual_ppm = round(min(60.5, 58.0 + ramp_efficiency + random.uniform(-0.4, 0.4)), 1)
                
                # Motor current
                self.line3_motor_current_a = round(4.0 + (self.line3_bearing_vibration_g * 0.4) + random.uniform(-0.05, 0.05), 2)

                # Sync into PAL tags
                await self.pal.write_normalized_tag("Line3.Throughput.ActualPPM", self.line3_actual_ppm)
                await self.pal.write_normalized_tag("Line3.Throughput.TargetPPM", self.line3_target_ppm)
                await self.pal.write_normalized_tag("Line3.Health.BearingVibration_g", self.line3_bearing_vibration_g)
                await self.pal.write_normalized_tag("Line3.Servo.DecelRamp_ms", self.line3_decel_ramp_ms)
                await self.pal.write_normalized_tag("Line3.Infeed.Motor_ConveyorRun", self.line3_running)
                await self.pal.write_normalized_tag("Line3.Infeed.Sensor_BottlePresent", (self._step_counter % 6 != 0))

            # 2. Physics simulation for Line 4 Carton Erector & Pneumatics
            if "PNEUMATIC_PRESSURE_DROP_LINE4" in self.active_faults:
                self.line4_pressure_kpa = max(480, int(self.line4_pressure_kpa - 2))
                self.line4_cycle_time_ms = int(820 + (600 - self.line4_pressure_kpa) * 1.4 + random.randint(-10, 10))
            else:
                self.line4_pressure_kpa = min(615, int(self.line4_pressure_kpa + 1))
                self.line4_cycle_time_ms = int(820 + random.randint(-8, 8))

            await self.pal.write_normalized_tag("Utilities.Pneumatic.MainPressure_kPa", self.line4_pressure_kpa)
            await self.pal.write_normalized_tag("Line4.Carton.CycleTime_ms", self.line4_cycle_time_ms)
            await self.pal.write_normalized_tag("Line4.Carton.InfeedSensor", (self._step_counter % 10 != 0))
            await self.pal.write_normalized_tag("Line4.Carton.FlapCylinder", (self._step_counter % 8 == 0))

            # Accumulate avoided downtime savings
            self.total_avoided_downtime_dollars += 0.08

            await asyncio.sleep(0.2) # 200ms tick

    def trigger_fault(self, fault_name: str) -> Dict[str, Any]:
        """Injects dynamic physical anomaly into the plant floor."""
        if fault_name not in self.active_faults:
            self.active_faults.append(fault_name)
        return {
            "status": "FAULT_INJECTED",
            "active_faults": self.active_faults,
            "timestamp": time.time()
        }

    def clear_fault(self, fault_name: str) -> Dict[str, Any]:
        if fault_name in self.active_faults:
            self.active_faults.remove(fault_name)
        return {
            "status": "FAULT_CLEARED",
            "active_faults": self.active_faults,
            "timestamp": time.time()
        }

    def apply_ai_patch(self, tag_id: str, new_value: Any) -> bool:
        """Applies verified AI patch directly to physical simulator variables."""
        if tag_id == "Line3.Servo.DecelRamp_ms":
            self.line3_decel_ramp_ms = int(new_value)
            # Clearing fault since the patch dampens the vibration resonance!
            self.clear_fault("BEARING_DEGRADATION_LINE3")
            return True
        elif tag_id == "Line4.Carton.CycleTime_ms":
            self.line4_cycle_time_ms = int(new_value)
            self.clear_fault("PNEUMATIC_PRESSURE_DROP_LINE4")
            return True
        return False

    def get_plant_telemetry_summary(self) -> Dict[str, Any]:
        """Provides high-level dashboard metrics for all stakeholder personas."""
        uptime_prob = 96.4
        if "BEARING_DEGRADATION_LINE3" in self.active_faults:
            uptime_prob -= 18.2
        if "PNEUMATIC_PRESSURE_DROP_LINE4" in self.active_faults:
            uptime_prob -= 12.5

        overall_oee = round(min(98.5, max(65.0, (self.line3_actual_ppm / self.line3_target_ppm) * 94.0)), 1)

        return {
            "plant_name": "Lumina Apex Smart Manufacturing Facility (Site 01)",
            "timestamp": time.time(),
            "overall_oee_percent": overall_oee,
            "predicted_uptime_probability": round(max(40.0, uptime_prob), 1),
            "active_faults_count": len(self.active_faults),
            "active_faults": self.active_faults,
            "total_avoided_downtime_dollars": round(self.total_avoided_downtime_dollars, 2),
            "lines": [
                {
                    "line_id": "Line 3",
                    "machine_name": "Rotary Bottling & Capping Infeed",
                    "status": "DEGRADED_WARNING" if "BEARING_DEGRADATION_LINE3" in self.active_faults else "HEALTHY_OPTIMAL",
                    "throughput_ppm": self.line3_actual_ppm,
                    "target_ppm": self.line3_target_ppm,
                    "vibration_rms_g": self.line3_bearing_vibration_g,
                    "bearing_temp_c": round(self.line3_bearing_temp_c, 1),
                    "motor_current_a": self.line3_motor_current_a,
                    "decel_ramp_ms": self.line3_decel_ramp_ms
                },
                {
                    "line_id": "Line 4",
                    "machine_name": "Carton Erector & Glue Station",
                    "status": "PRESSURE_WARNING" if "PNEUMATIC_PRESSURE_DROP_LINE4" in self.active_faults else "HEALTHY_OPTIMAL",
                    "cycle_time_ms": self.line4_cycle_time_ms,
                    "pressure_kpa": self.line4_pressure_kpa,
                    "total_cartons": self.line4_cartons_total
                }
            ]
        }
