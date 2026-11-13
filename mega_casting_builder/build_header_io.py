# mega_casting_builder/build_header_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Machining_DieCasting_ColdChamber_RealTimeInjection_PorosityControl
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - IEC 61131-3 SYNTHETIC DATASET ARCHITECTURE
 * PERSONA         : 75+ Years Principal Automation Fellow & Cyber-Physical Systems Chair
 * SECTOR          : Heavy Machinery & Automotive Mega-Casting / High-Pressure Die Casting (HPDC)
 * MACHINE CLASS   : Commercial 6,000-Ton (60,000 kN) Cold Chamber Giga-Casting Press Cell
 * TARGET PRODUCT  : Single-Piece Aluminum Structural Rear Underbody Subframe (AlSi10MnMg Alloy, ~75 kg Shot Weight)
 * INJECTION CORE  : Dynamic 4-Stage Closed-Loop Real-Time Hydraulic Injection Profile:
 *                   - Phase 1: Slow shot wave-free plunger motion (wave crest suppression, air entrapment prevention)
 *                   - Phase 2: Ultra-fast cavity fill up to 9.5 m/s (critical cavity fill time 30 - 45 ms)
 *                   - Phase 3: Instant intensification spike up to 1,200 bar within 15 ms (solidification feeding)
 *                   - Phase 4: Biscuit deceleration cushion, crystallization holding pressure & freeze-off
 * VACUUM SYSTEM   : Dual vacuum evacuation channel (< 25 mbar absolute) with acoustic leak rate evaluation
 * CLAMP LOCKUP    : 60,000 kN toggle clamping mechanism with 4 tie-bar dynamic strain stretch & platen tilt balancing
 * THERMAL CONTROL : Multi-circuit mold thermal oil balancing for fixed die, moving die, gating, and biscuit regions
 * CONTROL REGIME  : Discrete State-Space (A, B, C, D) 6x6 with Luenberger/Kalman Observer + Receding-Horizon MPC
 *                   with 10-Iteration Unrolled Projected Gradient Descent (PGD) and Slew Rate Constraints
 * REDUNDANCY      : 2oo3 Triple Modular Redundant (TMR) voting across 4 critical sensor trios with discrepancy timers
 * SAFETY & ALARMS : ISA-18.2 multi-tiered alarm matrix (HH/H/L/LL with deadbands) & 32-bit bit-packed DWORD telemetry
 * ===================================================================================================================== *)
VAR_INPUT
    (* --- Master Cell Automation & Safety Controls --- *)
    bEnable                                : BOOL;        (* System Master Automation Function Block Enable [bool] *)
    bResetAlarms                           : BOOL;        (* Master Alarm Reset and First-Out Latch Acknowledge [bool] *)
    bAutoCycleStart                        : BOOL;        (* Automatic Casting Cycle Start Command [bool] *)
    bEmergencyStop                         : BOOL;        (* Hardwired Emergency Stop Dual-Channel Relay Status [bool] *)
    rCycleTime_DeltaT                      : REAL;        (* Controller Deterministic Scan Period Ts [s] (nominal 0.001 s) *)

    (* --- 2oo3 TMR Triple Channel Plunger Magnetostrictive Linear Transducers --- *)
    rPlungerPos_Sensor1                    : REAL;        (* Plunger Stroke Position Sensor 1 Magnetostrictive [mm] *)
    rPlungerPos_Sensor2                    : REAL;        (* Plunger Stroke Position Sensor 2 Magnetostrictive [mm] *)
    rPlungerPos_Sensor3                    : REAL;        (* Plunger Stroke Position Sensor 3 Magnetostrictive [mm] *)

    (* --- 2oo3 TMR Triple Channel Hydraulic Shot Cylinder Head Pressure Transducers --- *)
    rHeadPress_Sensor1                     : REAL;        (* Injection Cylinder Head Hydraulic Pressure Transducer 1 [bar] *)
    rHeadPress_Sensor2                     : REAL;        (* Injection Cylinder Head Hydraulic Pressure Transducer 2 [bar] *)
    rHeadPress_Sensor3                     : REAL;        (* Injection Cylinder Head Hydraulic Pressure Transducer 3 [bar] *)

    (* --- Hydraulic Injection Cylinder Rod Chamber Pressure Transducer --- *)
    rRodPress_Sensor                       : REAL;        (* Injection Cylinder Rod Backpressure Transducer [bar] *)

    (* --- 2oo3 TMR Triple Channel In-Cavity Piezoelectric Quartz Pressure Transducers --- *)
    rCavityPress_Sensor1                   : REAL;        (* In-Cavity Piezoelectric Pressure Sensor 1 (Gate Inflow) [bar] *)
    rCavityPress_Sensor2                   : REAL;        (* In-Cavity Piezoelectric Pressure Sensor 2 (Center Web) [bar] *)
    rCavityPress_Sensor3                   : REAL;        (* In-Cavity Piezoelectric Pressure Sensor 3 (End of Fill) [bar] *)

    (* --- 2oo3 TMR Triple Channel Parting Plane Vacuum Capacitive Transducers --- *)
    rVacPressure_Sensor1                   : REAL;        (* Parting Plane Vacuum Evacuation Capacitive Gauge 1 [mbar] *)
    rVacPressure_Sensor2                   : REAL;        (* Parting Plane Vacuum Evacuation Capacitive Gauge 2 [mbar] *)
    rVacPressure_Sensor3                   : REAL;        (* Parting Plane Vacuum Evacuation Capacitive Gauge 3 [mbar] *)

    (* --- 4-Column Tie-Bar Dynamic Strain Extensometer Transducers --- *)
    rTieBar_Strain_Ch1                     : REAL;        (* Column 1 (Top-Left) Tie-Bar Elastic Extensometer Strain [um] *)
    rTieBar_Strain_Ch2                     : REAL;        (* Column 2 (Top-Right) Tie-Bar Elastic Extensometer Strain [um] *)
    rTieBar_Strain_Ch3                     : REAL;        (* Column 3 (Bottom-Left) Tie-Bar Elastic Extensometer Strain [um] *)
    rTieBar_Strain_Ch4                     : REAL;        (* Column 4 (Bottom-Right) Tie-Bar Elastic Extensometer Strain [um] *)

    (* --- Mold Steel & Thermal Oil Circulation Temperatures --- *)
    rFixedDie_Temp_Actual                  : REAL;        (* Fixed Die Insert Bulk Core Temperature Thermocouple [deg C] *)
    rMovingDie_Temp_Actual                 : REAL;        (* Moving Die Insert Bulk Core Temperature Thermocouple [deg C] *)
    rOil_Supply_Temp_Actual                : REAL;        (* Mold Thermal Regulation Unit Oil Supply Manifold [deg C] *)
    rOil_Return_Temp_Actual                : REAL;        (* Mold Thermal Regulation Unit Oil Return Manifold [deg C] *)

    (* --- Molten Aluminum Ladle & Sleeve Pouring Interface --- *)
    rLadle_Melt_Temp_Actual                : REAL;        (* Molten Aluminum Temperature in Robotic Dosing Ladle [deg C] *)
    rLadle_Dosed_Weight_kg                 : REAL;        (* Gravimetric Load Cell Poured Shot Weight [kg] *)
    bLadle_Pour_Completed                  : BOOL;        (* Robotic Ladle Pouring Sequence Completed Permissive [bool] *)

    (* --- Giga-Press Mechanical & Safety Interlocks --- *)
    bSafetyGate_Closed                     : BOOL;        (* Die Enclosure Acoustic Safety Sliding Doors Interlock [bool] *)
    bRobot_Extractor_Home                  : BOOL;        (* Heavy Giga-Part Unloader Robot in Safe Standby Position [bool] *)
    bRobot_Spray_Home                      : BOOL;        (* Multi-Axis Die Lubricant Spray Tooling Safe Standby [bool] *)
    bCorePins_Advanced_Permissive          : BOOL;        (* Hydraulic Side Slide Cores Advanced Limit Switches [bool] *)
    bCorePins_Retracted_Permissive         : BOOL;        (* Hydraulic Side Slide Cores Retracted Limit Switches [bool] *)
    bEjector_Retracted_Permissive          : BOOL;        (* Servo Ejector Plate Fully Retracted Home Limit [bool] *)
    bAccumulator_Charged_Permissive        : BOOL;        (* High-Speed Hydraulic Accumulator Nitrogen Charge OK [bool] *)

    (* --- Production Casting Recipe Setpoints --- *)
    rRecipe_Phase1_Velocity                : REAL;        (* Target Phase 1 Wave-Free Plunger Velocity [m/s] *)
    rRecipe_Phase1_SwitchPos               : REAL;        (* Plunger Stroke Switchpoint Position from Phase 1 to 2 [mm] *)
    rRecipe_Phase2_Velocity                : REAL;        (* Target Phase 2 High-Speed Cavity Fill Plunger Velocity [m/s] *)
    rRecipe_Intensification_Press          : REAL;        (* Target Phase 3 Intensification Final Specific Pressure [bar] *)
    rRecipe_Intensification_RiseTime_ms    : REAL;        (* Target Phase 3 Pressure Rise Response Time [ms] (<= 15 ms) *)
    rRecipe_Biscuit_Nominal_mm             : REAL;        (* Nominal Target Casting Biscuit Thickness [mm] *)
    rRecipe_Vacuum_Threshold_mbar          : REAL;        (* Maximum Allowable Evacuation Pressure for Fast Shot [mbar] *)
    rRecipe_ClampTonnage_kN                : REAL;        (* Target Toggle Clamping Lockup Force [kN] (nominal 60000 kN) *)
    rRecipe_Hold_Solidification_Time_s     : REAL;        (* In-Die Solidification Cooling Dwell Time [s] *)
    rRecipe_DieTemp_Target_degC            : REAL;        (* Desired Die Equilibrium Working Temperature [deg C] *)
END_VAR
VAR_OUTPUT
    (* --- 2oo3 TMR Voted Process Variables --- *)
    rPlungerPos_Voted                      : REAL;        (* 2oo3 TMR Voted Plunger Stroke Position [mm] *)
    rPlungerVel_Filtered                   : REAL;        (* Low-Pass Filtered Plunger Instantaneous Axial Velocity [m/s] *)
    rHeadPress_Voted                       : REAL;        (* 2oo3 TMR Voted Shot Cylinder Head Pressure [bar] *)
    rCavityPress_Voted                     : REAL;        (* 2oo3 TMR Voted In-Cavity Dynamic Piezo Pressure [bar] *)
    rVacPressure_Voted                     : REAL;        (* 2oo3 TMR Voted Parting Plane Absolute Vacuum Level [mbar] *)
    rTotalClampingForce_kN                 : REAL;        (* Calculated Total Dynamic Tie-Bar Clamping Force [kN] *)
    rPlatenTilt_Parallelism_um             : REAL;        (* Differential Platen Tilt Deflection Misalignment [um] *)

    (* --- Metallurgical Quality & Process Verification Outputs --- *)
    rBiscuitThickness_Actual_mm            : REAL;        (* Final Measured Casting Biscuit Thickness [mm] *)
    rIntensification_RiseTime_Actual_ms    : REAL;        (* Actual Intensification Pressure Rise Response Time [ms] *)
    rAcousticFillShock_bar_ms              : REAL;        (* Cavity Fill Acoustic Shock Wave Gradient [bar/ms] *)
    rPorosity_Risk_Index                   : REAL;        (* Calculated Porosity Risk Metric [0.0..1.0] (< 0.20 optimal) *)
    iCasting_Quality_Grade                 : INT;         (* Quality Tier: 1=Class A Structural, 2=Class B, 3=Scrap *)
    rCycleTime_Elapsed_s                   : REAL;        (* Total Elapsed Cycle Time for Current Casting Shot [s] *)

    (* --- Hydraulic Actuator Servo & Proportional Control Outputs --- *)
    rServoInjectionValve_Cmd               : REAL;        (* Ultra-Fast Moog Proportional Injection Valve Spool Cmd [%] *)
    rAccumulatorPilotTrim_Cmd              : REAL;        (* High-Speed Hydraulic Accumulator Discharge Pilot Trim [%] *)
    rIntensificationValve_Cmd              : REAL;        (* Phase 3 Intensification Booster Cartridge Fast Spool [%] *)
    rVacuumThrottle_Cmd                    : REAL;        (* Parting Plane Vacuum Evacuation Throttle Valve Cmd [%] *)
    rThermalOil_Valve_Cmd                  : REAL;        (* Mold Multi-Circuit Thermal Oil Heating/Cooling Trim [%] *)
    rToggleClampPilot_Cmd                  : REAL;        (* Toggle Hydraulic Locking Cylinder Proportional Trim [%] *)

    (* --- Discrete Actuator Sequence & Motion Interlocks --- *)
    bVacuumValve_Open_Cmd                  : BOOL;        (* Chill-Block Parting Plane Vacuum Evacuation Valve Open [bool] *)
    bVacuumPurge_N2_Cmd                    : BOOL;        (* High-Pressure Nitrogen Vacuum Channel Blowback Purge [bool] *)
    bCorePull_Advance_Cmd                  : BOOL;        (* Hydraulic Side Core Slides Advance Command [bool] *)
    bCorePull_Retract_Cmd                  : BOOL;        (* Hydraulic Side Core Slides Retract Command [bool] *)
    bClampLockup_Cmd                       : BOOL;        (* 6,000-Ton Hydraulic Toggle Lockup Advance Command [bool] *)
    bClampOpen_Cmd                         : BOOL;        (* Die Opening Decompression and Retraction Command [bool] *)
    bServoEjector_Fire_Cmd                 : BOOL;        (* Multi-Stage Servo Ejector Demold Pulse Command [bool] *)
    bRobotExtractor_Start_Cmd              : BOOL;        (* Trigger Giga-Casting Part Extraction Robot Cycle [bool] *)
    bRobotSpray_Start_Cmd                  : BOOL;        (* Trigger Automated Die Face Lubricant Spray Cycle [bool] *)

    (* --- Deterministic State Machine & Diagnostic Telemetry --- *)
    iFSM_CurrentState                      : INT;         (* Current Deterministic FSM Operational Step Index (0..13) *)
    dwStatusWord1                          : DWORD;       (* 32-Bit Bit-Packed Machine Status & Sequence Permissives *)
    dwStatusWord2                          : DWORD;       (* 32-Bit Bit-Packed Sensor TMR Health & Subsystem Readiness *)
    dwAlarmWord1                           : DWORD;       (* 32-Bit Bit-Packed ISA-18.2 Process Trips & Metal Flash Alarms *)
    dwAlarmWord2                           : DWORD;       (* 32-Bit Bit-Packed Sensor Discrepancy & Hardware Faults *)
    dwFirstOutWord                         : DWORD;       (* 32-Bit Bit-Packed Latching First-Out Forensic Trip Word *)
    bGeneralFault                          : BOOL;        (* Master Cell Latched Emergency Trip Status [bool] *)
    bGeneralWarning                        : BOOL;        (* Master Cell Preventative Maintenance Warning [bool] *)
    bCycleComplete_Pulse                   : BOOL;        (* One-Shot Pulse Signal Indicating Casting Cycle Success [bool] *)
END_VAR
"""
