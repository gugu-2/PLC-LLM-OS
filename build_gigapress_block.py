# Modular generator for FB_Automotive_MegaCasting_9000Ton_RealTimeShot_Vacuum

import json
import uuid
import re
import sys
import os

def generate_full_st_code():
    parts = []
    
    # -------------------------------------------------------------------------
    # 0. HEADER & COMMENTS
    # -------------------------------------------------------------------------
    header = """FUNCTION_BLOCK FB_Automotive_MegaCasting_9000Ton_RealTimeShot_Vacuum
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
COMMERCIAL AUTOMOTIVE FOUNDRY & STRUCTURAL MEGA-CASTING DIVISION
========================================================================================================================
SYSTEM SPECIFICATION:
  - Machine Type:        9,000-Ton Ultra-Large High-Pressure Die Casting Machine (Giga-Press / Mega-Casting Cell)
  - Target Component:    Single-Piece Integrated Automotive Rear Underbody Structural Casting
  - Alloy Specification: Hypoeutectic Aluminum-Silicon Die Casting Alloy (AlSi10MnMg / A380 High-Ductility Structural)
  - Shot Dose Weight:    110.0 kg Liquid Aluminum per Machine Cycle (Net casting mass: 82.5 kg, Runners/Biscuits: 27.5 kg)
  - Plunger Dimensions:  Diameter = 180.0 mm (Cross-sectional Area = 0.025447 m^2), Shot Sleeve Length = 1,400.0 mm
  - Nominal Clamp Force: 90,000.0 kN (9,177 Metric Tons) across Four 750.0 mm Diameter High-Tensile 4340 Alloy Tie-Bars
  - Hydraulic Injection: 3-Stage Closed-Loop Hydraulic Servo System with 400 L Piston Nitrogen Accumulator (320 bar precharge)
  - Intensification:     Differential Booster Cylinder (Ratio 4.2:1) capable of peak static squeeze pressure up to 1,400.0 bar
  - High-Vacuum System:  Tri-Stage Roots Blower Station with Evacuated Surge Tank (4,000 L) pulling cavity < 25.0 mbar
  - Vacuum Chill Vent:   Acoustic/Hydraulic High-Speed Chill-Block Shutoff Valve with < 8.0 ms Dynamic Seat Closure
  - Control Execution:   Deterministic 1.0 ms Task Interrupt Cycle (IEC 61131-3 3rd Edition Structured Text)

CYBER-PHYSICAL SYSTEM ARCHITECTURE & GOVERNING PRINCIPLES:
  1. Multi-Phase Closed-Loop Shot Dynamics:
     - Phase 1 (Slow Shot): Plunger advances at nominal velocity v1 = 0.25 m/s. The free surface profile of molten aluminum
       is governed by open-channel shallow water wave dynamics. Plunger acceleration is actively sculpted using critical
       Froude number criteria (Fr = v / sqrt(g * h_eff) < 0.95) to prevent wave rollover, surface turbulence, and air
       entrapment within the shot sleeve before the pour hole is sealed and the sleeve is compacted.
     - Phase 2 (Fast Shot): Plunger accelerates dynamically (a_shot >= 45.0 m/s^2) up to v2 = 8.5 m/s in < 35.0 ms,
       discharging the molten metal front through multiple fanned tangential runners at gate velocities exceeding 65.0 m/s.
       The complete 0.038 m^3 rear underbody thin-walled cavity (mean wall thickness 2.5 mm) is filled in under 40.0 ms
       to eliminate cold shuts and premature laminar freezing.
     - Phase 3 (Intensification Squeeze): Upon instantaneous cavity fill impact (detected by multi-channel gate pressure
       transducers and cavity arrival optical sensors), the servo pilot switches to the 4.2:1 differential intensifier booster.
       Hydraulic head pressure spikes to 1,400.0 bar with a 10%-90% rise time of < 15.0 ms, delivering dynamic squeeze
       pressure into the mushy metal zone to collapse dendritic shrinkage micro-porosity before gate freeze-off occurs.

  2. 4-Tie-Bar Dynamic Clamping Tonnage & Eccentricity Balancing:
     - The movable platen (mass 140 metric tons) is clamped against the fixed cover die by four massive 750 mm diameter
       tie-bars under 90,000 kN nominal pre-stress. Due to asymmetric die cavity geometry, non-uniform thermal expansion,
       and heavy bottom-biased runner layouts, unbalanced thermal and mechanical forces can induce severe platen tilting,
       causing molten aluminum die flash blowouts (catastrophic safety hazard) and permanent tie-bar fatigue cracking.
     - Dynamic strain gauge extensometers continuously measure tension on Tie-Bars 1 (Top-Left), 2 (Top-Right), 3 (Bottom-Left),
       and 4 (Bottom-Right). The block computes horizontal, vertical, and diagonal bending moments and dynamically commands
       individual high-pressure hydraulic pre-stress nuts to maintain total load balance within +/- 2.0% of nominal setpoint.

  3. High-Vacuum Evacuation & Acoustic Chill-Block Fast Shutoff:
     - To achieve structural ductility (> 10% elongation at break for automotive crash safety), dissolved gas and trapped
       air must be extracted prior to metal arrival. A tri-stage Roots vacuum package evacuates the sealed die cavity to
       below 25.0 mbar within 250.0 ms during Phase 1.
     - When the molten metal front reaches the chill-block venting channels at the end of cavity fill, an ultra-fast
       hydraulic chill-block valve must snap shut in < 8.0 ms. If closure is sluggish (> 8.0 ms), molten aluminum penetrates
       the vacuum line, destroying expensive vacuum instrumentation and disabling the entire foundry production cell.

  4. Multivariable Discrete State-Space Model & Receding-Horizon MPC:
     - Continuous-time dynamics linearized around operating trajectory:
         x[k+1] = A * x[k] + B * u[k] + w[k]
         y[k]   = C * x[k] + D * u[k] + v[k]
     - States (6x1):
         x1: Plunger Injection Velocity [m/s]
         x2: Hydraulic Shot Cylinder Head Pressure [bar]
         x3: Mold Cavity Vacuum Level [mbar]
         x4: Total 4-Tie-Bar Clamping Force [kN]
         x5: Mold Cavity Face Surface Temperature [deg C]
         x6: Cast Part Shell Solidification Thickness [mm]
     - Actuators (5x1):
         u1: High-Response Servo Shot Proportional Pilot Valve [%] (0 - 100%)
         u2: High-Speed Accumulator Discharge Poppet Valve [%] (0 - 100%)
         u3: Intensifier Multiplier Booster Pilot Valve [%] (0 - 100%)
         u4: High-Vacuum Cavity Extraction Throttle Valve [%] (0 - 100%)
         u5: Die Tempering Thermal Oil Circulating Pump Speed [%] (0 - 100%)
     - Receding-Horizon MPC executes 10 unrolled Projected Gradient Descent (PGD) iterations solving:
         min J = sum_{k=0}^{N-1} [ (x[k]-x_ref)^T * Q * (x[k]-x_ref) + (u[k]-u_ref)^T * R * (u[k]-u_ref) + delta_u^T * S * delta_u ]
                 + (x[N]-x_ref)^T * P * (x[N]-x_ref)
         subject to actuator velocity limits, hydraulic flow saturation, and tie-bar anti-flash safety bounds.
========================================================================================================================
*)
"""
    parts.append(header)
    return "".join(parts)

if __name__ == "__main__":
    c = generate_full_st_code()
    print("Header len:", len(c))
