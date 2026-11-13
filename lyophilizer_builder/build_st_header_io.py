# lyophilizer_builder/build_st_header_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Pharma_Lyophilization_FreezeDryer_VacuumSublimation_Thermal
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
COMMERCIAL PHARMACEUTICAL & BIOMANUFACTURING DIVISION - INDUSTRIAL FREEZE DRYING
========================================================================================================================
SYSTEM SPECIFICATION & ENGINEERING CONTEXT:
  Plant: Commercial Parenteral Biologics Bulk & Vial Lyophilization Facility
  Unit: Industrial Multi-Shelf Freeze Dryer (16 Hollow Shelves, Dual-Cascade Refrigeration -85 deg C, Silicone Oil HTF)
  Total Shelf Area: 42.5 m2 (Capacity: 85,000 x 10R DIN ISO 8362-1 Injection Vials)
  Thermal Fluid: Polydimethylsiloxane (Syltherm XLT) Heat Transfer Oil (-65 deg C to +125 deg C)
  Dual-Cascade Refrigeration:
    - Stage 1: R404A/R452A High-Stage Circuit (Evaporating at -40 deg C, Interstage Condenser Heat Exchanger)
    - Stage 2: R508B Low-Stage Circuit (Evaporating at -85 deg C on External Ice Condenser Coils)
    - Hot Gas Defrost Bypass Subsystem for Rapid Ice Melting and Condenser Sanitization
  Vacuum Subsystem: Dry Screw Backing Pump (650 m3/h) + Roots Vacuum Booster (2,500 m3/h) + Isolation Butterfly Valve
  Process Control Architecture:
    1. Triple Modular Redundant (2oo3) Sensor Voting Suite:
       - 3x Chamber Pirani Gauges (PT-101A/B/C) [mbar]
       - 3x Chamber Capacitance Manometers (PT-102A/B/C) [mbar] (True Absolute Gas Pressure)
       - 3x Shelf Silicone Supply Pt100 RTDs (TT-201A/B/C) [deg C] (Class 1/10 DIN A)
       - 3x Product Vial Core Thermocouples/RTDs (TT-301A/B/C) [deg C]
    2. First-Principles Ice Sublimation Kinetics:
       - Sublimation Mass Flux: dm_sub/dt = (P_ice(T_p) - P_chamber) / (R_p(L_cake) + R_s)
       - Saturation Vapor Pressure via Clausius-Clapeyron / Goff-Gratch Ice Curve:
         P_ice(T_p) = 6.1121 * EXP((22.587 * T_p) / (273.86 + T_p)) [mbar]
       - Dynamic Cake Dried Layer Resistance: R_p(L_cake) = R_0 + (A_cake * L_cake) / (1 + B_cake * L_cake)
       - Pikal Heat Transfer Coefficient: K_v = a_v + (b_v * P_chamber) / (1 + c_v * P_chamber)
    3. Cyber-Physical Discrete State-Space Model (6x6) with Luenberger Innovation Observer:
       x[k+1] = A * x[k] + B * u[k] + L * (y[k] - C * x_hat[k])
       States:
         x1: Shelf thermal fluid supply temperature [deg C]
         x2: Product vial average core temperature [deg C]
         x3: Product sublimation moving boundary interface temperature [deg C]
         x4: Freeze dryer chamber vacuum pressure [mbar]
         x5: Condenser coil ice surface temperature [deg C]
         x6: Product cake dry layer thickness [mm]
       Actuators:
         u1: Shelf electric thyristor heating power [%]
         u2: Shelf refrigeration plate-frame expansion valve [%]
         u3: Condenser cascade compressor stage 2 suction throttle [%]
         u4: Chamber vacuum throttle / fine sterile N2 bleed valve [%]
         u5: Shelf circulation pump VFD speed [%]
    4. Receding-Horizon Model Predictive Control (MPC) with 10 Unrolled PGD Iterations:
       - Explicit Quadratic Cost Penalties: Q (tracking error), R (actuator effort), S (slew rate damping), P (terminal cost)
       - Slew-rate limiting and hard constraints preventing Product Interface Temp > Cake Collapse Temp (-28.5 deg C)
    5. Dual Endpoint Detection:
       - Pirani / Capacitance Manometer Ratio: Convergence from ~1.60 toward 1.00 upon sublimation completion
       - Manometric Temperature Measurement (MTM) / Pressure Rise Test (PRT) dP/dt evaluation
    6. Deterministic 14-Stage Production Finite State Machine (FSM):
       - Full Life-Cycle: CIP -> SIP (121 deg C Hold) -> Drain/Vacuum Cool -> Leak Rate Test -> Loading ->
         Freezing Ramp -> Controlled Nucleation -> Primary Drying (MPC) -> PRT Endpoint -> Secondary Drying ->
         Hydraulic Vial Stoppering (4,000 kN) -> Sterile N2 Aeration -> Emergency Lockdown
    7. ISA-18.2 Multi-Tier Process Alarms, Deadband Hysteresis & 32-Bit Telemetry Bit-Packing
========================================================================================================================
*)
VAR_INPUT
    (* Master Operational Interlocks *)
    bEnable                         : BOOL;     (* Master automation block enable signal *)
    bAutoMode                       : BOOL;     (* True: Closed-loop MPC/FSM auto; False: Manual supervisory hold *)
    bEmergencyStop                  : BOOL;     (* Active Low fail-safe emergency stop circuit [SIL-3] *)
    bAcknowledgeAlarms              : BOOL;     (* Operator alarm reset & trip latch clearing command *)

    (* 2oo3 TMR Sensor Triplets: Chamber Pirani Gauges *)
    rChamberPirani_A                : REAL;     (* Chamber Pirani thermal conductivity vacuum gauge channel A [mbar] *)
    rChamberPirani_B                : REAL;     (* Chamber Pirani thermal conductivity vacuum gauge channel B [mbar] *)
    rChamberPirani_C                : REAL;     (* Chamber Pirani thermal conductivity vacuum gauge channel C [mbar] *)

    (* 2oo3 TMR Sensor Triplets: Chamber Capacitance Diaphragm Manometers *)
    rChamberCap_A                   : REAL;     (* Chamber capacitance diaphragm true pressure gauge channel A [mbar] *)
    rChamberCap_B                   : REAL;     (* Chamber capacitance diaphragm true pressure gauge channel B [mbar] *)
    rChamberCap_C                   : REAL;     (* Chamber capacitance diaphragm true pressure gauge channel C [mbar] *)

    (* 2oo3 TMR Sensor Triplets: Shelf Silicone Supply Pt100 RTDs *)
    rShelfFluidTemp_A               : REAL;     (* Shelf silicone heat transfer fluid supply RTD channel A [deg C] *)
    rShelfFluidTemp_B               : REAL;     (* Shelf silicone heat transfer fluid supply RTD channel B [deg C] *)
    rShelfFluidTemp_C               : REAL;     (* Shelf silicone heat transfer fluid supply RTD channel C [deg C] *)

    (* 2oo3 TMR Sensor Triplets: Product Vial Core RTDs *)
    rProductVialTemp_A              : REAL;     (* Core product vial Pt100 RTD thermocouple channel A [deg C] *)
    rProductVialTemp_B              : REAL;     (* Core product vial Pt100 RTD thermocouple channel B [deg C] *)
    rProductVialTemp_C              : REAL;     (* Core product vial Pt100 RTD thermocouple channel C [deg C] *)

    (* 16 Shelves Fluid Temperature Uniformity Profiles *)
    rShelfInletTemps                : ARRAY[1..16] OF REAL; (* Individual shelf silicone fluid inlet temperatures [deg C] *)
    rShelfOutletTemps               : ARRAY[1..16] OF REAL; (* Individual shelf silicone fluid outlet temperatures [deg C] *)

    (* Dual-Cascade Refrigeration Condenser Instrumentation *)
    rCondenserCoilTemp_A            : REAL;     (* Refrigeration condenser coil surface RTD channel A [deg C] *)
    rCondenserCoilTemp_B            : REAL;     (* Refrigeration condenser coil surface RTD channel B [deg C] *)
    rCascadeStage1_SuctionPress     : REAL;     (* Stage 1 R404A/R452A compressor suction pressure [bar] *)
    rCascadeStage1_DischPress       : REAL;     (* Stage 1 R404A/R452A compressor discharge pressure [bar] *)
    rCascadeStage2_SuctionPress     : REAL;     (* Stage 2 R508B compressor suction pressure [bar] *)
    rCascadeStage2_DischPress       : REAL;     (* Stage 2 R508B compressor discharge pressure [bar] *)

    (* Hydraulic Stoppering Ram Telemetry *)
    rStopperingPressure_bar         : REAL;     (* Hydraulic stoppering cylinder main line hydraulic pressure [bar] *)
    rStopperingRamPos_mm            : REAL;     (* Hydraulic vertical stoppering ram linear encoder position [mm] *)

    (* Utilities, CIP & SIP Instrumentation *)
    rSterileN2_SupplyPress_bar      : REAL;     (* Sterile filtered nitrogen gas aeration supply header pressure [bar] *)
    rCIP_WaterFlow_m3h              : REAL;     (* Clean-In-Place high-pressure water wash header volumetric flow [m3/h] *)
    rSIP_SteamTemp_degC             : REAL;     (* Steam-In-Place chamber core saturated steam temperature [deg C] *)
    rSIP_SteamPress_bar             : REAL;     (* Steam-In-Place chamber core saturated steam pressure [bar] *)

    (* Chamber Mechanical Interlocks & Physical Positions *)
    bDoorInterlockClosed            : BOOL;     (* Freeze dryer main autoclave front loading door seal interlock *)
    bIsolationValveOpen             : BOOL;     (* Chamber-to-condenser main vacuum isolation butterfly valve open limit *)

    (* Recipe Target Trajectory Setpoints *)
    rTargetShelfTemp_degC           : REAL;     (* Recipe active target shelf heat transfer fluid temperature [deg C] *)
    rTargetChamberPress_mbar        : REAL;     (* Recipe active target chamber vacuum operating pressure [mbar] *)
    rCollapseTempLimit_degC         : REAL;     (* Product critical cake collapse / glass transition threshold [deg C] *)
END_VAR
VAR_OUTPUT
    (* Modulating Actuator Commands *)
    rCmd_ShelfHeaterThyristor_pct   : REAL;     (* Modulating shelf electric thyristor heating power command [%] *)
    rCmd_ShelfRefrigExpValve_pct    : REAL;     (* Shelf refrigeration plate-frame heat exchanger expansion valve [%] *)
    rCmd_CascadeStage2Suction_pct   : REAL;     (* Cascade refrigeration stage 2 compressor suction throttle [%] *)
    rCmd_ChamberVacuumBleedValve_pct: REAL;     (* Chamber vacuum fine proportional sterile N2 bleed valve [%] *)
    rCmd_ShelfCircPumpSpeed_pct     : REAL;     (* Silicone heat transfer fluid primary circulation pump VFD speed [%] *)
    rCmd_HydraulicStopperingValve_pct: REAL;    (* Hydraulic stoppering ram proportional pressure modulating valve [%] *)

    (* Discrete Equipment Digital Commands *)
    bCmd_ChamberIsolationValve      : BOOL;     (* Chamber-to-condenser main vacuum butterfly isolation valve solenoid *)
    bCmd_VacuumBackingPump          : BOOL;     (* Vacuum system dry screw primary backing pump start contactor *)
    bCmd_VacuumRootsBlower          : BOOL;     (* Vacuum system Roots booster blower high-vacuum contactor *)
    bCmd_CascadeStage1Compressor    : BOOL;     (* Dual-cascade refrigeration Stage 1 (R404A) compressor motor run *)
    bCmd_CascadeStage2Compressor    : BOOL;     (* Dual-cascade refrigeration Stage 2 (R508B) compressor motor run *)
    bCmd_CondenserHotGasDefrost     : BOOL;     (* Ice condenser coil hot gas bypass de-icing solenoid valve *)
    bCmd_SterileN2AerationValve     : BOOL;     (* Sterile filtered nitrogen chamber aeration vacuum break valve *)
    bCmd_CIP_SupplyPump             : BOOL;     (* Clean-In-Place high-pressure rotary spray header pump contactor *)
    bCmd_SIP_PureSteamInletValve    : BOOL;     (* Pure steam sterilization 121.1 deg C chamber supply inlet valve *)
    bCmd_ChamberCondensateDrainValve: BOOL;     (* Chamber bottom sanitary steam trap / condensate drain valve *)

    (* Cyber-Physical Observer & Process Telemetry *)
    rEstimatedProductInterfaceTemp  : REAL;     (* Sublimation moving boundary ice interface temperature [deg C] *)
    rEstimatedCakeDryLayer_mm       : REAL;     (* Estimated dried product cake layer thickness [mm] *)
    rCalculatedSublimationRate_kgh  : REAL;     (* Instantaneous batch ice sublimation mass flow rate [kg/h] *)
    rCumulativeSublimedMass_kg      : REAL;     (* Total integrated water vapor ice mass captured on condenser [kg] *)
    rPiraniCapPressureRatio         : REAL;     (* Filtered Pirani-to-Capacitance manometer ratio [dimensionless] *)
    rShelfTempUniformityDelta_degC  : REAL;     (* Maximum temperature deviation across 16 shelves [deg C] *)
    rStopperingForce_kN             : REAL;     (* Total hydraulic compressive force on 16 collapsed shelves [kN] *)

    (* Cycle Phase Progress & Endpoint Flags *)
    bPrimaryDryingComplete          : BOOL;     (* Sublimation endpoint verified via Pirani/Cap convergence and PRT *)
    bSecondaryDryingComplete        : BOOL;     (* Desorption phase completed at target residual moisture limit *)
    bStopperingComplete             : BOOL;     (* 16 shelves compressed to vial seat height with verified force *)

    (* Finite State Machine Telemetry *)
    nFsmState                       : INT;      (* Active 14-stage deterministic finite state machine index [0..13] *)
    sFsmStateName                   : STRING[60];(* Human-readable designation of active lyophilizer state *)

    (* 32-Bit Bit-Packed Status & Alarm Telemetry Words *)
    dwStatusWord1                   : DWORD;    (* Primary system operational status word *)
    dwStatusWord2                   : DWORD;    (* Secondary auxiliary subsystems and vacuum status word *)
    dwAlarmWord1                    : DWORD;    (* Multi-tier critical process safety and product collapse alarms *)
    dwAlarmWord2                    : DWORD;    (* Instrumentation TMR discrepancies and equipment failure alarms *)
    dwFirstOutWord                  : DWORD;    (* Latched first-out safety shutdown trip diagnostic telemetry *)
END_VAR
"""
