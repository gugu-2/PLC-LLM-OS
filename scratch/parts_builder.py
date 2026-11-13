# scratch/parts_builder.py
import sys

def get_header():
    return """FUNCTION_BLOCK FB_Nuclear_PWR_SteamGenerator_NarrowRangeLevel_ShrinkSwell
(*
 ==============================================================================
 LUMINA ADVANCED INDUSTRIAL CYBER-PHYSICAL AUTOMATION ENGINE
 SAFETY-CRITICAL NUCLEAR POWER GENERATION ARCHITECTURE: CLASS 1E / IEEE 603 / IEEE 7-4.3.2
 DOMAIN: Pressurized Water Reactor (PWR) Steam Generator Level Thermo-Hydraulics
 SYSTEM: Model 51F / EPR-Class U-Tube Steam Generator (UTSG) Recirculating Loop
 COMPONENT: Dynamic Narrow-Range Level Regulation with Shrink & Swell Compensation
 TARGET RUNTIME: Safety-Certified IEC 61131-3 Programmable Logic Controller
 SCAN DISCRETE TIME INTERVAL (Ts): 25.000 milliseconds (40 Hz Execution Rate)
 ==============================================================================
 SYSTEM FUNCTIONAL & MATHEMATICAL OVERVIEW:
 The Steam Generator in a Pressurized Water Reactor (PWR) nuclear power plant is 
 a high-inertia, highly non-linear, non-minimum phase two-phase thermo-hydraulic
 heat exchanger transferring ~900 MWth to 1350 MWth per loop from the primary 
 Reactor Coolant System (RCS) at ~15.5 MPa (155 bar) and ~325 deg C to the secondary 
 steam power conversion cycle at ~6.9 MPa (69 bar) saturated steam (~285 deg C).

 CORE PHENOMENOLOGICAL CHALLENGES SOLVED IN THIS IMPLEMENTATION:
 1. Non-Minimum Phase Dynamic Inversion (Shrink and Swell):
    - Thermal Swell: Rapid opening of the main steam governor valve causes an 
      immediate drop in secondary drum pressure. The lower saturation temperature 
      triggers flashing boiling throughout the boiling riser tube bundle, 
      causing an immediate surge in average void fraction (alpha). The volumetric 
      expansion of steam bubbles forces water upwards into the steam drum, creating 
      a false initial level increase ("swell") even though secondary water mass 
      inventory is rapidly depleting. A naive PI controller responds by reducing 
      feedwater flow, catastrophically accelerating tube bundle uncovery!
    - Thermal Shrink: Sudden injection of subcooled cold feedwater (~220 deg C) 
      into the upper downcomer feedring condenses steam in the upper bundle and 
      collapses steam voids in the riser. The collapse of void volume causes 
      the measured liquid level in the downcomer annulus to plunge downwards 
      ("shrink") prior to the positive mass accumulation taking effect. A naive 
      controller responds by driving the feedwater valve further open, collapsing 
      even more voids in a dangerous positive feedback instability!
 2. Internal Recirculation Dynamics:
    - Natural circulation is driven by the density differential between the 
      subcooled liquid downcomer column (~740 kg/m3) and the two-phase boiling 
      riser mixture (~320 to 500 kg/m3). The recirculation ratio (Riser Mass Flow /
      Steam Mass Flow) varies non-linearly from ~3.2 at 100% full power to > 8.0 
      at low power (< 15% FP), shifting system poles and zeros across operating regimes.
 3. Advanced 5-Phase Cyber-Physical Architecture:
    - Phase 1: 2oo3 Triple Modular Redundancy (TMR) Voting on all Class 1E process 
      channels (Narrow Range Level, Wide Range Level, Steam Drum Pressure, Steam 
      Mass Flow, Feedwater Mass Flow, RCS Cold Leg Temp, Secondary SGTR Radiation) 
      with dynamic deviation monitoring, 500 ms discrepancy accumulation timers, 
      and bumpless degradation (2oo3 -> 1oo2 -> 1oo1 -> Fail-Safe Trip).
    - Phase 2: First-Principles 8-State Cyber-Physical Discrete State-Space Model 
      (Ts = 25 ms) with Kalman Filter State Observer:
        x1: SG Narrow-Range Water Level Deviation [mm]
        x2: Downcomer Recirculation Mass Flow Rate [kg/s]
        x3: Boiling Riser Mean Void Fraction [ratio 0.0..1.0]
        x4: Primary-to-Secondary U-Tube Heat Transfer Rate [MW]
        x5: Steam Drum Saturated Vapor Pressure [bar]
        x6: Primary Coolant Cold Leg Return Temperature [deg C]
        x7: Main Feedwater Regulating Valve Trim Effective Position [%]
        x8: Dynamic Non-Minimum Phase (NMP) Lead/Lag Shrink/Swell State [mm]
    - Phase 3: Receding Horizon Model Predictive Control (MPC) with Projected 
      Gradient Descent (PGD) unrolled across horizon N = 5 steps and 6 iterations, 
      with dynamic inverse response feedforward compensation and actuator slew limits (5%/s).
    - Phase 4: Deterministic 14-Stage Nuclear State Machine (FSM) governing plant 
      evolution from cold shutdown, low-power bypass control, bumpless transfer, 
      full-power MPC, rapid turbine runback, MSIV trip containment, SGTR diagnostic, 
      auxiliary feedwater initiation, dry-out protection, to post-scram decay heat removal.
    - Phase 5: ISA-18.2 Process Alarm Matrix with hysteresis deadbands, first-out 
      root cause latching, and dual 32-bit bit-packed telemetry words.
 ==============================================================================
*)
"""

print("parts_builder header ready.")
