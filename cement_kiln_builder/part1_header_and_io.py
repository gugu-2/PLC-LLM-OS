# -*- coding: utf-8 -*-
"""
cement_kiln_builder/part1_header_and_io.py
Part 1: Function block declaration, engineering specification header,
VAR_INPUT, VAR_OUTPUT, and VAR variable declarations.
"""

def get_part1_header_and_io():
    return """FUNCTION_BLOCK FB_Cement_RotaryKiln_Precalciner_Pyroprocessing_Cooler
(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL PROCESS AUTOMATION ENGINE - SYNTHETIC DATASET ARCHITECTURE V7 MAX-PERSONA
  COMMERCIAL INDUSTRIAL SECTOR : Heavy Building Materials, Cement, Lime & Mineral Aggregates
  SYSTEM CLASSIFICATION        : 10,000 Ton/Day Industrial Precalciner Rotary Kiln & Multi-Stage Planetary Grate Clinker Cooler
  PROCESS TOPOLOGY             : 5-Stage Twin-String Suspension Cyclone Preheater Tower, Low-NOx In-Line Calciner (ILC),
                                 Counter-Current Rotary Sintering Kiln (5.6 m Dia x 88 m Length, 3.5% Slope),
                                 Tertiary Air Duct (TAD) Aerodynamic Combustion Decoupling,
                                 Reciprocating Hydraulic Cross-Bar Clinker Cooler with 4-Zone Under-Grate Aeration,
                                 Volatile Alkali/Chloride Bypass Gas Bleed Loop, and Shell Infrared Thermography Scanner.
  SAFETY INTEGRITY LEVEL       : SIL-3 Capable Architecture (IEC 61508 / IEC 61511 / NFPA 86 / NFPA 85)
  REGULATORY & EMISSIONS STD   : EN 196 / ASTM C150 / EPA NESHAP 40 CFR Part 63 Subpart LLL (Portland Cement Manufacturing)
  AUTHOR                       : Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Experience)
========================================================================================================================

CYBER-PHYSICAL PHENOMENOLOGY & THERMAL-CHEMICAL FOUNDATIONS:
------------------------------------------------------------------------------------------------------------------------
1. MULTI-STAGE SUSPENSION PREHEATING & IN-LINE PRECALCINER KINETICS:
   Raw cement meal (finely ground limestone CaCO3, clay/shale SiO2, Al2O3, Fe2O3, d90 < 90 um) enters the top cyclone
   string (Stage C1) at ~60 °C, cascading counter-currently against upward-flowing hot flue gases (1050 °C -> 330 °C).
   Inside the high-efficiency suspension cyclones, gas-solid heat transfer occurs in micro-seconds due to immense specific
   surface area (~4,000 cm2/g).
   The calcination reaction represents the most energy-intensive thermochemical step in the entire pyroprocessing loop:
       CaCO3 (solid) -> CaO (solid) + CO2 (gas)     Delta H_r = +1,782 kJ/kg CaCO3 (+178.2 kJ/mol endothermic)
   In the In-Line Calciner (ILC) furnace, fuel (pulverized coal, petcoke, and co-fired alternative fuels such as shredded
   tires and RDF) is combusted in preheated tertiary air (950 °C) ducted directly from the clinker cooler recuperation hood.
   The target apparent decarbonation degree exiting the lowest cyclone (Stage C5) into the kiln inlet is held rigidly
   between 92.0% and 95.5%. If decarbonation drops below 90%, thermal shock chills the kiln burning zone, collapsing
   the clinker coating and producing underburnt, high-free-lime clinker (fCaO > 2.5%). Conversely, if decarbonation reaches
   100% in the calciner, premature eutectic liquid formation causes severe cyclone clogging, calciner snow-man buildups,
   and refractory destruction.

2. ROTARY KILN SINTERING HYDRODYNAMICS & COATING THERMAL EQUILIBRIUM:
   The rotary kiln is an 88-meter inclined cylinder rotating at 1.0 to 5.0 RPM, driven by dual 1,200 kW VFD motors.
   Material residence time spans 25 to 45 minutes as the partially calcined meal travels down the incline toward the main
   flame. Within the transition and burning zones (material temperatures 1,350 °C to 1,480 °C, flame core 1,950 °C - 2,100 °C),
   liquid phase flux (24% - 28% molten aluminates and ferrites) facilitates the diffusion-controlled formation of alite
   (tricalcium silicate, C3S, 3CaO.SiO2) and belite (dicalcium silicate, C2S, 2CaO.SiO2):
       2 CaO + SiO2 -> C2S (exothermic, Delta H = -710 kJ/kg)
       C2S + CaO -> C3S    (exothermic clinkerization, Delta H = -420 kJ/kg)
   Stable operation requires the formation of a protective sacrificial clinker coating (150 mm - 250 mm thick) adhered
   to the basic spinel / magnesia-chromite refractory bricks. Kiln shell temperature is continuously mapped by a multi-track
   infrared scanner (360° rotational azimuthal resolution x 200 longitudinal segments). Shell temperatures exceeding
   350 °C indicate loss of coating or localized brick spalling, risking catastrophic shell ovality warping or burn-through.
   The kiln drive torque reflects internal clinker viscous coating drag, bed bed-lift, and liquid phase viscosity.

3. RECIPROCATING HYDRAULIC GRATE CLINKER COOLER RECUPERATION & AERATION DYNAMICS:
   Red-hot clinker discharged from the kiln nose ring at ~1,400 °C cascades onto the high-efficiency cross-bar reciprocating
   hydraulic cooler grate. The cooler must accomplish two critical thermodynamic objectives simultaneously:
   a) Rapid clinker crystal quenching: Dropping clinker temperature from 1,400 °C to < 100 °C at 1,500 °C/min freezes the
      hydraulic alite crystal structure (preventing slow-cooling conversion of alite into inactive belite and periclase),
      maximizing hydraulic reactivity for subsequent cement strength development.
   b) Maximum thermal energy recuperation: The first two cooler zones generate superheated secondary air (1,150 °C)
      channelled into the kiln hood for main burner coal combustion, and tertiary air (950 °C) channelled through the TAD
      for precalciner combustion, achieving overall cooler thermal efficiency exceeding 74%.
   Cooler under-grate aeration fans (multi-fan modular compartments) modulate static air pressures to prevent red-river
   short-circuiting and clinker blow-through fluidization.

4. CYBER-PHYSICAL MULTIVARIABLE RECEDING-HORIZON MPC & EMBEDDED ESTIMATION:
   Control involves a 6-state discrete-time linear time-invariant state-space model:
       x[k+1] = A * x[k] + B * u[k]
       y[k]   = C * x[k] + D * u[k]
   with a Luenberger observer updating states via innovation feedback:
       x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y_meas[k] - C * x_hat[k])
   A 10-step unrolled Projected Gradient Descent (PGD) optimizer computes optimal control actions:
       u1: Main burner pulverized coal pneumatic feed rate [t/h]
       u2: Precalciner fuel feed rate [t/h]
       u3: Kiln rotational drive VFD speed [RPM]
       u4: Preheater Induced Draft (ID) exhaust fan damper [%]
       u5: Grate cooler hydraulic cross-bar stroke speed [strokes/min]
   penalizing deviation from setpoints (burning zone temperature 1,450 °C, precalciner exit 890 °C, shell temp 280 °C,
   decarbonation degree 93.5%, drive torque 410 kNm, inlet CO 0.08%), while strictly enforcing slew rate limits and
   anti-ring thermal balancing constraints.

5. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE:
   Four mission-critical triplicated measurement channels with 300 ms persistence discrepancy timers:
     - Burning Zone Optical Pyrometers (Pyrometer_1, 2, 3) [deg C]
     - Precalciner Bottom Pt-Rh Thermocouples (TC_1, 2, 3) [deg C]
     - Kiln Inlet Laser Gas Analyzer CO Concentration (CO_1, 2, 3) [%]
     - Preheater Cyclone Stage 1 Draft Pressure Transmitters (P_1, 2, 3) [mbar]

6. 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM):
   From cold refractory brick curing and inching, auxiliary burner lightoff, coal ramp, meal introduction, steady-state
   clinker production, tire/RDF co-firing, volatile bypass bleed, clinker ring clearing, to emergency trips.
========================================================================================================================
*)
VAR_INPUT
    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 1: SYSTEM SUPERVISORY COMMANDS & PERMISSIVE INTERLOCKS                                            *)
    (* --------------------------------------------------------------------------------------------------------- *)
    bEnable                             : BOOL;     (* Master Pyroprocessing System Enable Supervisory Permissive [sys] *)
    bReset_Alarms                       : BOOL;     (* Master Alarm Latch Reset Command [cmd] *)
    bEmergencyStop                      : BOOL;     (* Hardwired SIL-3 Master Emergency Stop Pushbutton Contact [safety] *)
    bAutoMode_Permissive                : BOOL;     (* Plant Distributed Control System (DCS) Auto-Mode Permissive [status] *)
    rScanCycleTime_s                    : REAL;     (* PLC Deterministic Periodic Task Cycle Time (e.g. 0.050 s) [s] *)

    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANT SENSOR SUITE                                                     *)
    (* --------------------------------------------------------------------------------------------------------- *)
    (* Channel A: Burning Zone Optical Pyrometer Triplet [deg C] *)
    rPyrometer_BurnZone_Temp_S1_degC    : REAL;     (* Burning Zone Two-Color Optical Infrared Pyrometer Channel 1 [deg C] *)
    rPyrometer_BurnZone_Temp_S2_degC    : REAL;     (* Burning Zone Two-Color Optical Infrared Pyrometer Channel 2 [deg C] *)
    rPyrometer_BurnZone_Temp_S3_degC    : REAL;     (* Burning Zone Two-Color Optical Infrared Pyrometer Channel 3 [deg C] *)

    (* Channel B: Precalciner Bottom Combustion Thermocouple Triplet [deg C] *)
    rCalciner_Temp_TC_S1_degC           : REAL;     (* Precalciner Bottom Exit Gas Pt-Rh Type-S Thermocouple Channel 1 [deg C] *)
    rCalciner_Temp_TC_S2_degC           : REAL;     (* Precalciner Bottom Exit Gas Pt-Rh Type-S Thermocouple Channel 2 [deg C] *)
    rCalciner_Temp_TC_S3_degC           : REAL;     (* Precalciner Bottom Exit Gas Pt-Rh Type-S Thermocouple Channel 3 [deg C] *)

    (* Channel C: Kiln Inlet Laser Gas Analyzer Carbon Monoxide (CO) Triplet [%] *)
    rKilnInlet_CO_Sens1_pct             : REAL;     (* Kiln Inlet Laser Gas Analyzer CO Concentration Channel 1 [%] *)
    rKilnInlet_CO_Sens2_pct             : REAL;     (* Kiln Inlet Laser Gas Analyzer CO Concentration Channel 2 [%] *)
    rKilnInlet_CO_Sens3_pct             : REAL;     (* Kiln Inlet Laser Gas Analyzer CO Concentration Channel 3 [%] *)

    (* Channel D: Preheater Top Stage C1 Cyclone Draft Pressure Transmitter Triplet [mbar] *)
    rPreheater_TopDraft_P1_mbar         : REAL;     (* Preheater Top Stage C1 Cyclone Flue Gas Draft Pressure Channel 1 [mbar] *)
    rPreheater_TopDraft_P2_mbar         : REAL;     (* Preheater Top Stage C1 Cyclone Flue Gas Draft Pressure Channel 2 [mbar] *)
    rPreheater_TopDraft_P3_mbar         : REAL;     (* Preheater Top Stage C1 Cyclone Flue Gas Draft Pressure Channel 3 [mbar] *)

    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 3: KILN PROCESS TELEMETRY, COMBUSTION & MATERIAL FEED MEASUREMENTS                                *)
    (* --------------------------------------------------------------------------------------------------------- *)
    rKiln_RawMealFeed_Rate_tph          : REAL;     (* Mass Flow Rate of Raw Meal Introduced into Stage C1 Cyclone [t/h] *)
    rKilnInlet_O2_pct                   : REAL;     (* Kiln Inlet Flue Gas Excess Oxygen Concentration [%] *)
    rKilnInlet_NOx_ppm                  : REAL;     (* Kiln Inlet Nitric Oxide (NOx) Flue Gas Emissions [ppm] *)
    rKilnShell_MaxHotSpot_degC          : REAL;     (* Kiln Shell IR Thermal Scanner Peak Hot-Spot Temperature [deg C] *)
    rKilnShell_HotSpot_Position_m       : REAL;     (* Longitudinal Position of Peak Hot-Spot from Kiln Nose Ring [m] *)
    rKilnDrive_MotorCurrent_A           : REAL;     (* Kiln Main Drive Dual Induction Motors Current Draw [A] *)
    rKilnDrive_ActualTorque_kNm         : REAL;     (* Kiln Main Drive Output Mechanical Shaft Torque [kNm] *)
    rKilnDrive_TireSlip_mm_per_rev      : REAL;     (* Kiln Riding Ring (Tire #2) Relative Circumferential Creep/Slip [mm/rev] *)
    rPrecalciner_Calcination_Offline_pct: REAL;     (* Laboratory XRF / Titration Offline Hot Meal Decarbonation Degree [%] *)

    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 4: CLINKER COOLER, RECUPERATION & ALTERNATIVE FUELS TRANSDUCERS                                   *)
    (* --------------------------------------------------------------------------------------------------------- *)
    rCooler_SecondaryAir_Temp_degC      : REAL;     (* Recuperated High-Temperature Secondary Air to Main Burner [deg C] *)
    rCooler_TertiaryAir_Temp_degC       : REAL;     (* Recuperated High-Temperature Tertiary Air to Precalciner [deg C] *)
    rCooler_ClinkerDischarge_Temp_degC  : REAL;     (* Quenched Clinker Final Discharge Apron Pan Conveyor Temperature [deg C] *)
    rCooler_GrateChamber1_Pressure_mbar : REAL;     (* Hydraulic Cooler Under-Grate Aeration Chamber #1 Static Pressure [mbar] *)
    rAltFuel_TireRDF_Feed_tph           : REAL;     (* Whole/Shredded Scrap Tires & Refuse-Derived Fuel (RDF) Co-Firing Rate [t/h] *)
    rAlkaliBypass_Flow_Nm3h             : REAL;     (* Volatile Alkali & Chloride Bypass Exhaust Gas Bleed Flow Rate [Nm3/h] *)
END_VAR

VAR_OUTPUT
    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 1: CONTROLLER RUNTIME STATUS & CRITICAL SAFETY TRIP FLAGS                                         *)
    (* --------------------------------------------------------------------------------------------------------- *)
    bSystemActive                       : BOOL;     (* Pyroprocessing Autonomous Controller Running Status [status] *)
    bEmergencyTripActive                : BOOL;     (* SIL-3 Master Safety Shutdown Interlock Activated [trip] *)
    iFSM_State                          : INT;      (* Current 14-Stage Deterministic Production FSM Operational Index [state] *)

    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 2: PRIMARY MODULATED ACTUATOR ANALOG COMMAND SETPOINTS                                           *)
    (* --------------------------------------------------------------------------------------------------------- *)
    rCmd_MainBurner_CoalFeed_tph        : REAL;     (* Main Burner Pneumatic Pulverized Coal Feed Rate Setpoint [t/h] *)
    rCmd_Precalciner_FuelFeed_tph       : REAL;     (* Precalciner Fuel Dosing Feed Rate Actuator Command [t/h] *)
    rCmd_KilnDrive_Speed_RPM            : REAL;     (* Rotary Kiln Main Drive Dual VFD Rotational Speed Setpoint [RPM] *)
    rCmd_Preheater_IDFan_Damper_pct     : REAL;     (* Preheater Top Induced Draft (ID) Exhaust Fan Inlet Damper [%] *)
    rCmd_GrateCooler_StrokeSpeed_spm    : REAL;     (* Grate Cooler Hydraulic Cross-Bar Cylinder Stroke Rate [strokes/min] *)
    rCmd_TertiaryAir_Damper_pct         : REAL;     (* Tertiary Air Duct (TAD) Aerodynamic Balancing Damper [%] *)
    rCmd_Cooler_AerationFan1_Flow_Nm3h  : REAL;     (* Clinker Cooler Quench Zone High-Pressure Aeration Fan #1 Command [Nm3/h] *)
    rCmd_AlkaliBypass_Damper_pct        : REAL;     (* Volatile Alkali Bleed Quench Mixing Damper Position [%] *)
    rCmd_KilnShell_CoolingFan_pct       : REAL;     (* Kiln Shell Exterior Forced-Air Spot Cooling Fan Bank Speed [%] *)

    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 3: FIRST-PRINCIPLES OBSERVER STATE ESTIMATES & THERMAL PERFORMANCE METRICS                        *)
    (* --------------------------------------------------------------------------------------------------------- *)
    rEst_BurningZone_Temp_degC          : REAL;     (* Observer Estimated True Sintering Clinkering Temperature [deg C] *)
    rEst_Precalciner_Temp_degC          : REAL;     (* Observer Estimated Calciner Furnace Exit Gas Temperature [deg C] *)
    rEst_KilnShell_HotSpot_degC         : REAL;     (* Observer Estimated Kiln Shell Peak Outer Surface Temperature [deg C] *)
    rEst_DecarbonationDegree_pct        : REAL;     (* Observer Estimated Hot Meal CaCO3 Apparent Calcination [%] *)
    rEst_KilnDriveTorque_kNm            : REAL;     (* Observer Estimated Total Mechanical Drive Resistance Torque [kNm] *)
    rEst_KilnInletCO_pct                : REAL;     (* Observer Estimated Kiln Inlet Unburnt Carbon Monoxide Concentration [%] *)
    rCalculated_SpecificHeat_MJ_per_kg  : REAL;     (* Real-Time Estimated Specific Heat Consumption [MJ/kg clinker] *)

    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 4: BIT-PACKED STATUS, ALARM & FIRST-OUT TELEMETRY WORDS                                           *)
    (* --------------------------------------------------------------------------------------------------------- *)
    dwStatusWord1                       : DWORD;    (* 32-Bit Packed System Operational Status Register 1 [flags] *)
    dwStatusWord2                       : DWORD;    (* 32-Bit Packed System Subsystem Permissive Status Register 2 [flags] *)
    dwAlarmWord1                        : DWORD;    (* 32-Bit Packed ISA-18.2 Process Warning Alarm Register 1 [alarms] *)
    dwAlarmWord2                        : DWORD;    (* 32-Bit Packed ISA-18.2 Critical Trip Safety Alarm Register 2 [alarms] *)
    dwFirstOutWord                      : DWORD;    (* 32-Bit Bit-Latched First-Out Process Trip Event Register [code] *)
END_VAR

VAR
    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 1: DISCRETE CYBER-PHYSICAL STATE-SPACE MATRICES (6 STATES x 5 ACTUATORS)                          *)
    (* --------------------------------------------------------------------------------------------------------- *)
    bMatricesInitialized                : BOOL := FALSE;    (* Cold-start memory latch for state-space & MPC matrices *)
    
    (* Discrete State Transition Matrix A (6x6) *)
    A                                   : ARRAY[1..6, 1..6] OF REAL;
    (* Actuator Input Coupling Matrix B (6x5) *)
    B                                   : ARRAY[1..6, 1..5] OF REAL;
    (* Measurement Output Matrix C (6x6) *)
    C                                   : ARRAY[1..6, 1..6] OF REAL;
    (* Direct Feedthrough Matrix D (6x5) *)
    D                                   : ARRAY[1..6, 1..5] OF REAL;
    (* Luenberger Observer Innovation Gain Matrix L (6x6) *)
    L                                   : ARRAY[1..6, 1..6] OF REAL;

    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 2: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) PENALTY MATRICES                               *)
    (* --------------------------------------------------------------------------------------------------------- *)
    (* State Tracking Error Penalty Matrix Q (6x6 Diagonal) *)
    Q                                   : ARRAY[1..6, 1..6] OF REAL;
    (* Actuator Control Effort Penalty Matrix R (5x5 Diagonal) *)
    R                                   : ARRAY[1..5, 1..5] OF REAL;
    (* Slew Rate Suppression Penalty Matrix S (5x5 Diagonal) *)
    S                                   : ARRAY[1..5, 1..5] OF REAL;
    (* Terminal State Penalty Matrix P (6x6 Diagonal) *)
    P                                   : ARRAY[1..6, 1..6] OF REAL;

    (* State and Actuator Vectors *)
    rState_x                            : ARRAY[1..6] OF REAL; (* Physical plant states: [T_bz, T_calc, T_shell, Decarb, Torque, CO] *)
    rState_x_hat                        : ARRAY[1..6] OF REAL; (* Observer estimated state vector *)
    rState_x_pred                       : ARRAY[1..6] OF REAL; (* Open-loop one-step ahead state prediction *)
    rState_x_ref                        : ARRAY[1..6] OF REAL; (* State reference trajectories [1450, 890, 280, 93.5, 410, 0.08] *)
    rState_y_meas                       : ARRAY[1..6] OF REAL; (* Process measurement vector from voted sensors *)
    rState_y_innov                      : ARRAY[1..6] OF REAL; (* Output innovation residual: y_meas - C * x_pred *)
    rActuator_u                         : ARRAY[1..5] OF REAL; (* Current actuator outputs: [Coal_main, Fuel_calc, RPM, ID_Fan, Cooler_spm] *)
    rActuator_u_prev                    : ARRAY[1..5] OF REAL; (* Actuator outputs from previous execution cycle *)
    rActuator_u_opt                     : ARRAY[1..5] OF REAL; (* Optimal actuator commands calculated by MPC *)
    rActuator_u_min                     : ARRAY[1..5] OF REAL; (* Hard lower actuator saturation bounds *)
    rActuator_u_max                     : ARRAY[1..5] OF REAL; (* Hard upper actuator saturation bounds *)
    rActuator_du_max                    : ARRAY[1..5] OF REAL; (* Maximum permissible slew rates per scan cycle *)

    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 3: RECEDING-HORIZON MPC UNROLLED PGD OPTIMIZATION VARIABLES                                       *)
    (* --------------------------------------------------------------------------------------------------------- *)
    rPGD_Alpha                          : REAL := 0.00045;  (* Projected Gradient Descent line-search relaxation step size *)
    rCostate_lambda                     : ARRAY[1..6] OF REAL; (* Adjoint costate vector *)
    rGradient_grad_u                    : ARRAY[1..5] OF REAL; (* Unconstrained objective gradient w.r.t control inputs *)
    rPGD_Temp_u                         : ARRAY[1..5] OF REAL; (* Projected intermediate actuator command vector *)
    rState_Iter                         : ARRAY[1..6] OF REAL; (* Iteration state trajectory vector *)
    rMPC_ObjValue                       : REAL;             (* Calculated quadratic objective function value *)
    rMPC_BestObjValue                   : REAL;             (* Minimum objective value captured across PGD unrolls *)

    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 4: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE VARIABLES                             *)
    (* --------------------------------------------------------------------------------------------------------- *)
    (* Burning Zone Pyrometer Voted State *)
    rVoted_BurnZone_Temp                : REAL;             (* Voted Burning Zone Temperature [deg C] *)
    bTMR_Pyrometer_S1_Valid             : BOOL := TRUE;     (* Pyrometer Sensor 1 Health Flag *)
    bTMR_Pyrometer_S2_Valid             : BOOL := TRUE;     (* Pyrometer Sensor 2 Health Flag *)
    bTMR_Pyrometer_S3_Valid             : BOOL := TRUE;     (* Pyrometer Sensor 3 Health Flag *)
    bTMR_Pyrometer_Degraded             : BOOL := FALSE;    (* Pyrometer Triplet Degraded to 1oo2 or Single Mode *)
    tTMR_Pyrometer_T12_s                : REAL := 0.0;      (* Discrepancy Persistence Timer S1 vs S2 [s] *)
    tTMR_Pyrometer_T23_s                : REAL := 0.0;      (* Discrepancy Persistence Timer S2 vs S3 [s] *)
    tTMR_Pyrometer_T31_s                : REAL := 0.0;      (* Discrepancy Persistence Timer S3 vs S1 [s] *)
    rTMR_Pyrometer_Tolerance_degC       : REAL := 45.0;     (* Permissible Pairwise Pyrometer Deviation [deg C] *)

    (* Precalciner Thermocouple Voted State *)
    rVoted_Calciner_Temp                : REAL;             (* Voted Precalciner Exit Temperature [deg C] *)
    bTMR_Calciner_S1_Valid              : BOOL := TRUE;     (* Calciner TC Sensor 1 Health Flag *)
    bTMR_Calciner_S2_Valid              : BOOL := TRUE;     (* Calciner TC Sensor 2 Health Flag *)
    bTMR_Calciner_S3_Valid              : BOOL := TRUE;     (* Calciner TC Sensor 3 Health Flag *)
    bTMR_Calciner_Degraded              : BOOL := FALSE;    (* Calciner TC Degraded to 1oo2 or Single Mode *)
    tTMR_Calciner_T12_s                 : REAL := 0.0;      (* Discrepancy Persistence Timer S1 vs S2 [s] *)
    tTMR_Calciner_T23_s                 : REAL := 0.0;      (* Discrepancy Persistence Timer S2 vs S3 [s] *)
    tTMR_Calciner_T31_s                 : REAL := 0.0;      (* Discrepancy Persistence Timer S3 vs S1 [s] *)
    rTMR_Calciner_Tolerance_degC        : REAL := 25.0;     (* Permissible Pairwise Thermocouple Deviation [deg C] *)

    (* Kiln Inlet Carbon Monoxide (CO) Voted State *)
    rVoted_KilnInlet_CO                 : REAL;             (* Voted Kiln Inlet CO Concentration [%] *)
    bTMR_CO_S1_Valid                    : BOOL := TRUE;     (* CO Analyzer Sensor 1 Health Flag *)
    bTMR_CO_S2_Valid                    : BOOL := TRUE;     (* CO Analyzer Sensor 2 Health Flag *)
    bTMR_CO_S3_Valid                    : BOOL := TRUE;     (* CO Analyzer Sensor 3 Health Flag *)
    bTMR_CO_Degraded                    : BOOL := FALSE;    (* CO Analyzer Degraded to 1oo2 or Single Mode *)
    tTMR_CO_T12_s                       : REAL := 0.0;      (* Discrepancy Persistence Timer S1 vs S2 [s] *)
    tTMR_CO_T23_s                       : REAL := 0.0;      (* Discrepancy Persistence Timer S2 vs S3 [s] *)
    tTMR_CO_T31_s                       : REAL := 0.0;      (* Discrepancy Persistence Timer S3 vs S1 [s] *)
    rTMR_CO_Tolerance_pct               : REAL := 0.08;     (* Permissible Pairwise CO Deviation [%] *)

    (* Preheater Top Draft Pressure Voted State *)
    rVoted_Preheater_Draft              : REAL;             (* Voted Preheater Top Draft Pressure [mbar] *)
    bTMR_Draft_P1_Valid                 : BOOL := TRUE;     (* Draft Transmitter Sensor 1 Health Flag *)
    bTMR_Draft_P2_Valid                 : BOOL := TRUE;     (* Draft Transmitter Sensor 2 Health Flag *)
    bTMR_Draft_P3_Valid                 : BOOL := TRUE;     (* Draft Transmitter Sensor 3 Health Flag *)
    bTMR_Draft_Degraded                 : BOOL := FALSE;    (* Draft Transmitter Degraded to 1oo2 or Single Mode *)
    tTMR_Draft_T12_s                    : REAL := 0.0;      (* Discrepancy Persistence Timer P1 vs P2 [s] *)
    tTMR_Draft_T23_s                    : REAL := 0.0;      (* Discrepancy Persistence Timer P2 vs P3 [s] *)
    tTMR_Draft_T31_s                    : REAL := 0.0;      (* Discrepancy Persistence Timer P3 vs P1 [s] *)
    rTMR_Draft_Tolerance_mbar           : REAL := 6.0;      (* Permissible Pairwise Draft Pressure Deviation [mbar] *)

    (* Persistence and Common TMR Settings *)
    rTMR_Persistence_s                  : REAL := 0.300;    (* Discrepancy Fault Confirmation Time Limit [s] *)

    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 5: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM) VARIABLES                        *)
    (* --------------------------------------------------------------------------------------------------------- *)
    iFSM_CurrentState                   : INT := 0;         (* Current Operational State (0 = IDLE) *)
    iFSM_NextState                      : INT := 0;         (* Pending Next State Transition Target *)
    tFSM_StateTimer_s                   : REAL := 0.0;      (* Elapsed Dwell Time in Current State [s] *)
    tFSM_StepTimer_s                    : REAL := 0.0;      (* Sub-routine Sequence Progress Timer [s] *)
    bFSM_TransitionRequested            : BOOL := FALSE;    (* Internal State Step Command Trigger *)
    
    (* Specialized Process Regimes within FSM *)
    rCuring_CurrentTempRamp_degC_per_h  : REAL := 0.0;      (* Refractory Dryout Heating Rate [deg C/h] *)
    rCuring_TargetPlateau_degC          : REAL := 150.0;    (* Current Refractory Drying Temperature Plateau [deg C] *)
    tCuring_PlateauHoldTimer_s          : REAL := 0.0;      (* Refractory Moisture Soak Dwell Timer [s] *)
    bCuring_MoistureEvap_Complete       : BOOL := FALSE;    (* Primary Refractory Bound Water Outgassing Flag *)
    
    iRingClearing_CycleCounter          : INT := 0;         (* Clinker Coating Ring Thermal Shock Iteration Count *)
    tRingClearing_PhaseTimer_s          : REAL := 0.0;      (* Ring Thermal Expansion Disruption Timer [s] *)
    bRingClearing_Active                : BOOL := FALSE;    (* Clinker Ring Clearing Maneuver Active Flag *)
    rRingClearing_TempDelta_degC        : REAL := 0.0;      (* Deliberate Burning Zone Temperature Swing [deg C] *)

    rTireRDF_CoFiring_Target_TSR_pct    : REAL := 0.0;      (* Target Thermal Substitution Rate with Alternative Fuel [%] *)
    rTireRDF_Current_TSR_pct            : REAL := 0.0;      (* Actual Calculated Thermal Substitution Rate [%] *)
    rAlkaliBypass_TargetBleed_pct       : REAL := 0.0;      (* Kiln Inlet Gas Bleed Ratio to Bypass Quench [%] *)

    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 6: ISA-18.2 MULTI-TIERED ALARM SETPOINTS & HYSTERESIS DEADBANDS                                   *)
    (* --------------------------------------------------------------------------------------------------------- *)
    (* Burning Zone Pyrometer Alarm Trip Limits [deg C] *)
    rTrip_BurnZone_HH_degC              : REAL := 1520.0;   (* Burning Zone High-High Trip (Refractory Melt Hazard) [deg C] *)
    rTrip_BurnZone_H_degC               : REAL := 1485.0;   (* Burning Zone High Warning (Overburning / Heavy Clinker) [deg C] *)
    rTrip_BurnZone_L_degC               : REAL := 1415.0;   (* Burning Zone Low Warning (Coating Drop / Underburnt) [deg C] *)
    rTrip_BurnZone_LL_degC              : REAL := 1375.0;   (* Burning Zone Low-Low Trip (Severe Chilling / Uncalcined Meal) [deg C] *)
    rDeadband_BurnZone_degC             : REAL := 5.0;      (* Hysteresis Deadband for Pyrometer Alarms [deg C] *)

    (* Precalciner Exit Temperature Alarm Trip Limits [deg C] *)
    rTrip_Calciner_HH_degC              : REAL := 965.0;    (* Calciner Exit High-High Trip (Cyclone Clogging / Liquid Slag) [deg C] *)
    rTrip_Calciner_H_degC               : REAL := 925.0;    (* Calciner Exit High Warning (Fuel Wasted / Thermal Surge) [deg C] *)
    rTrip_Calciner_L_degC               : REAL := 855.0;    (* Calciner Exit Low Warning (Inadequate Decarbonation) [deg C] *)
    rTrip_Calciner_LL_degC              : REAL := 820.0;    (* Calciner Exit Low-Low Trip (Flameout / Calcination Collapse) [deg C] *)
    rDeadband_Calciner_degC             : REAL := 4.0;      (* Hysteresis Deadband for Calciner Alarms [deg C] *)

    (* Kiln Inlet Carbon Monoxide Alarm Trip Limits [%] *)
    rTrip_CO_HH_pct                     : REAL := 0.50;     (* Kiln Inlet CO High-High Trip (Deflagration / Preheater Explosion Hazard) [%] *)
    rTrip_CO_H_pct                      : REAL := 0.30;     (* Kiln Inlet CO High Warning (Incomplete Combustion / Reducing Flame) [%] *)
    rDeadband_CO_pct                    : REAL := 0.02;     (* Hysteresis Deadband for CO Alarms [%] *)

    (* Preheater Top Stage C1 Draft Pressure Alarm Trip Limits [mbar] *)
    rTrip_Draft_HH_mbar                 : REAL := -25.0;    (* Top Draft High-High Trip (Positive Pressure / Toxic Flue Blowback) [mbar] *)
    rTrip_Draft_H_mbar                  : REAL := -32.0;    (* Top Draft High Warning (Cyclone Blockage / Fan Capacity Limit) [mbar] *)
    rTrip_Draft_L_mbar                  : REAL := -55.0;    (* Top Draft Low Warning (False Air Inleakage / Draft Surge) [mbar] *)
    rTrip_Draft_LL_mbar                 : REAL := -65.0;    (* Top Draft Low-Low Trip (Severe ID Fan Overdraft / Duct Collapse Risk) [mbar] *)
    rDeadband_Draft_mbar                : REAL := 1.0;      (* Hysteresis Deadband for Draft Alarms [mbar] *)

    (* Kiln Shell Peak Hot-Spot Temperature Alarm Trip Limits [deg C] *)
    rTrip_ShellHotSpot_HH_degC          : REAL := 350.0;    (* Kiln Shell High-High Trip (Refractory Brick Lost / Shell Plastic Yield) [deg C] *)
    rTrip_ShellHotSpot_H_degC           : REAL := 320.0;    (* Kiln Shell High Warning (Coating Thinning / Activate Spot Fans) [deg C] *)
    rDeadband_ShellHotSpot_degC         : REAL := 5.0;      (* Hysteresis Deadband for Shell Temperature [deg C] *)

    (* Kiln Main Drive Mechanical Torque Alarm Trip Limits [kNm] *)
    rTrip_Torque_HH_kNm                 : REAL := 540.0;    (* Drive Torque High-High Trip (Severe Ring Jam / Mechanical Binding) [kNm] *)
    rTrip_Torque_H_kNm                  : REAL := 480.0;    (* Drive Torque High Warning (Heavy Internal Clinker Dam / Coating Ring) [kNm] *)
    rDeadband_Torque_kNm                : REAL := 10.0;     (* Hysteresis Deadband for Kiln Torque [kNm] *)

    (* Clinker Cooler Discharge Temperature Alarm Trip Limits [deg C] *)
    rTrip_ClinkerTemp_HH_degC           : REAL := 160.0;    (* Cooler Discharge High-High Trip (Pan Conveyor Belt Burn Hazard) [deg C] *)
    rTrip_ClinkerTemp_H_degC            : REAL := 125.0;    (* Cooler Discharge High Warning (Inefficient Quenching / Red-River) [deg C] *)
    rDeadband_ClinkerTemp_degC          : REAL := 5.0;      (* Hysteresis Deadband for Clinker Temperature [deg C] *)

    (* Active Alarm Condition Bit Latches *)
    bAlarm_BurnZone_HH                  : BOOL := FALSE;
    bAlarm_BurnZone_H                   : BOOL := FALSE;
    bAlarm_BurnZone_L                   : BOOL := FALSE;
    bAlarm_BurnZone_LL                  : BOOL := FALSE;
    bAlarm_Calciner_HH                  : BOOL := FALSE;
    bAlarm_Calciner_H                   : BOOL := FALSE;
    bAlarm_Calciner_L                   : BOOL := FALSE;
    bAlarm_Calciner_LL                  : BOOL := FALSE;
    bAlarm_CO_HH                        : BOOL := FALSE;
    bAlarm_CO_H                         : BOOL := FALSE;
    bAlarm_Draft_HH                     : BOOL := FALSE;
    bAlarm_Draft_H                      : BOOL := FALSE;
    bAlarm_Draft_L                      : BOOL := FALSE;
    bAlarm_Draft_LL                     : BOOL := FALSE;
    bAlarm_ShellHotSpot_HH              : BOOL := FALSE;
    bAlarm_ShellHotSpot_H               : BOOL := FALSE;
    bAlarm_Torque_HH                    : BOOL := FALSE;
    bAlarm_Torque_H                     : BOOL := FALSE;
    bAlarm_ClinkerTemp_HH               : BOOL := FALSE;
    bAlarm_ClinkerTemp_H                : BOOL := FALSE;
    bAlarm_TireSlip_High                : BOOL := FALSE;

    (* --------------------------------------------------------------------------------------------------------- *)
    (* SECTION 7: INTERMEDIATE CALCULATION, TIMERS & KINETIC VARIABLES                                          *)
    (* --------------------------------------------------------------------------------------------------------- *)
    rLoop_idx_i                         : INT;              (* General matrix row iteration index *)
    rLoop_idx_j                         : INT;              (* General matrix column iteration index *)
    rLoop_idx_m                         : INT;              (* General actuator iteration index *)
    rPGD_Iter                           : INT;              (* Unrolled PGD iteration index *)
    rEnthalpyDecarbonation_kW           : REAL;             (* Chemical endothermic calcination enthalpy absorption [kW] *)
    rEnthalpyClinkerExotherm_kW         : REAL;             (* Mineral clinkerization exothermic heat release rate [kW] *)
    rStefanBoltzmann_Radiation_kW       : REAL;             (* Burning zone radiative flux from flame to clinker bed [kW] *)
    rRecuperatedSecondaryAirEnthalpy_kW : REAL;             (* Clinker cooler secondary air recuperated thermal power [kW] *)
    rRecuperatedTertiaryAirEnthalpy_kW  : REAL;             (* Clinker cooler tertiary air recuperated thermal power [kW] *)
    rShellConvectiveLoss_kW             : REAL;             (* Kiln shell natural/forced convection thermal dissipation [kW] *)
    rTotalFuelHeatInput_GJ_per_h        : REAL;             (* Total primary and secondary fuel energy release rate [GJ/h] *)
    rHourlyClinkerProduction_tph        : REAL;             (* Real-time calculated clinker production rate [t/h] *)
    rCalculated_CO2_Emission_tph        : REAL;             (* Calculated mass flow rate of process & combustion CO2 [t/h] *)
    rCalculated_KilnFillDegree_pct      : REAL;             (* Volumetric loading percentage of meal inside kiln barrel [%] *)
    rTireSlip_Threshold_mm_per_rev      : REAL := 18.0;     (* Excessive riding ring migration limit [mm/rev] *)
    rAuxiliaryDrive_InchingSpeed_RPM    : REAL := 0.20;     (* Auxiliary diesel / electric inching barring speed [RPM] *)
END_VAR
"""
