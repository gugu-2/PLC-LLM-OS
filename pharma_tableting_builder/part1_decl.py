# pharma_tableting_builder/part1_decl.py

def get_part1():
    return """FUNCTION_BLOCK FB_Pharma_ContinuousTableting_Granulation_TabletPress
(*
========================================================================================================================
  LUMINA AI CYBER-PHYSICAL SYSTEMS & ADVANCED INDUSTRIAL AUTOMATION ARCHITECTURE GROUP
  CONTINUOUS PHARMACEUTICAL ORAL SOLID DOSAGE (OSD) REFERENCE IMPLEMENTATION — SYNTHETIC DATASET ENGINE V7
  
  SYSTEM DESIGNATION : CONTINUOUS TWIN-SCREW WET GRANULATION, MULTI-CELL FLUID BED DRYING & ROTARY TABLETING LINE
  MANUFACTURING SCOPE: FULLY INTEGRATED SOLID DOSAGE CONTINUOUS DIRECT MANUFACTURING (CDM) PER FDA 21 CFR PART 11,
                       ICH Q8 (PHARMACEUTICAL DEVELOPMENT), ICH Q9 (QUALITY RISK MANAGEMENT), ICH Q10 (PHARMACEUTICAL
                       QUALITY SYSTEM), ICH Q13 (CONTINUOUS MANUFACTURING OF DRUG SUBSTANCES AND DRUG PRODUCTS).
  TABLETING PLATFORM : HIGH-SPEED ROTARY PRESS (250,000 TABLETS/HOUR NOMINAL, 48-STATION EU-B TOOLING) WITH
                       INSTRUMENTED PRE-COMPRESSION (0-20 kN) AND MAIN COMPRESSION (0-100 kN) PIEZOELECTRIC LOAD CELLS.
  PROCESS ANALYTICAL : IN-LINE PROCESS ANALYTICAL TECHNOLOGY (PAT): MICROWAVE RESONANCE & NIR SPECTROSCOPY CAVITY
                       PROBES FOR RESIDUAL LOSS-ON-DRYING (% LOD) MOISTURE MONITORING; CONTINUOUS LOSS-IN-WEIGHT (LIW)
                       ACTIVE PHARMACEUTICAL INGREDIENT (API) & EXCIPIENT GRAVIMETRIC FEEDING CASCADE.
  QUALITY CONTROL    : INDIVIDUAL TABLET DYNAMIC COMPACT HARDNESS, THICKNESS & POROSITY DE-COUPLING OBSERVER COUPLED
                       TO A HIGH-SPEED (< 10 ms) FAST-RESPONSE PNEUMATIC JET BLOW-OFF REJECT GATE MECHANISM.
  SAFETY INTEGRITY   : IEC 61508 / IEC 61511 SIL-2/SIL-3 REDUNDANT MACHINE PROTECTION & DUAL-CHANNEL OVERPRESSURE E-STOP.
  ALARM MANAGEMENT   : ANSI/ISA-18.2 / IEC 62682 INDUSTRIAL ALARM MANAGEMENT WITH ADVANCED DEAD-BAND HYSTERESIS.
  AUTHOR             : 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
========================================================================================================================

  THEORETICAL & CYBER-PHYSICAL SOLID-DOSAGE ENGINEERING FOUNDATIONS:
  ----------------------------------------------------------------------------------------------------------------------
  1. CONTINUOUS TWIN-SCREW WET GRANULATION (TSWG) MECHANICS:
     - The continuous wet granulator comprises co-rotating twin screws housed within a temperature-controlled split barrel.
       Powder blends consisting of micronized Active Pharmaceutical Ingredient (API), microcrystalline cellulose (MCC),
       lactose monohydrate, and disintegrants (croscarmellose sodium) enter through a gravimetric loss-in-weight twin-screw
       screw feeder at mass flow rate M_dot_powder [kg/h].
     - Liquid binder solution (aqueous hydroxypropyl cellulose, PVP K30, or pure demineralized water) is atomized or
       injected directly into the wetting zone via a high-precision multi-head peristaltic micro-pump cascade at volumetric
       or gravimetric rate M_dot_liquid [g/min].
     - The fundamental dimensionless Liquid-to-Solid Ratio (L/S) [% w/w] governs the nucleation, coalescence, and attrition
       regimes of wet granulation:
           L_S_ratio(t) = ( M_dot_liquid(t) / (M_dot_powder(t) * (1000.0 / 60.0)) ) * 100.0
       Deviation from target L/S ratio (< 8.0% w/w) produces dry friable powder with low granule density and excessive fines;
       excessive L/S ratio (> 14.5% w/w) causes uncontrolled wet massing, viscous dough formation, barrel clogging,
       and catastrophic torque spike on the screw drive servos.
     - Granule growth kinetics in the twin-screw mixing/kneading element sections are governed by the shear strain rate:
           gamma_dot = (pi * D_screw * N_screw) / h_clearance
       where D_screw = 16 mm, N_screw = 200 to 800 rpm, and h_clearance = 0.5 mm barrel-screw clearance.
     - Granule median diameter d50 [um] follows a dynamic population balance transition:
           tau_gran * (d(d50)/dt) = -d50(t) + d50_nominal * (1.0 + k_L_S * (L_S_ratio - L_S_target) + k_shear * (N_screw - N_nominal))

  2. MULTI-CELL CONTINUOUS FLUID BED DRYING & PAT MOISTURE REGULATION:
     - Wet granules discharged from the TSWG are pneumatically or gravitationally conveyed into a continuous multi-cell
       horizontal fluid bed dryer. The dryer consists of multiple sequential fluidization chambers separated by adjustable
       weirs, ensuring tight residence time distribution (RTD) and eliminating back-mixing.
     - Conditioned fluidization air is supplied through a perforated distributor plate at superficial air velocity
       u_air [m/s] governed by the two-phase fluidization balance:
           u_mf = (d_p^2 * (rho_p - rho_air) * g) / (150 * mu_air) * (epsilon_bed^3 / (1 - epsilon_bed))
     - Heat and mass transfer equations governing continuous moisture evaporation:
           m_bed * (dX_moisture / dt) = F_in * X_in - F_out * X_moisture - k_evap * A_surface * (P_sat(T_bed) - P_vapor_air)
           m_bed * Cp_bed * (dT_bed / dt) = F_in * Cp_bed * (T_in - T_bed) + Q_fluid_air - k_evap * A_surface * Delta_H_vap
     - Real-Time Moisture Measurement via In-Line Microwave Resonance & Near-Infrared (NIR) PAT Probes:
       Microwave resonance cavity probes measure the dielectric shift Delta_f and resonance curve broadening Delta_w
       induced by polar water molecules:
           LOD_pct = a_calib * (Delta_w / Delta_f) + b_calib
       Operating window: Target LOD = 1.8% to 2.2% loss-on-drying.
       If LOD > 3.0%: High risk of punch sticking, die wall binding, picking, and mold growth during storage.
       If LOD < 1.0%: Over-drying causes granule friability, excessive tablet capping, lamination, and micro-fissuring.

  3. HIGH-SPEED ROTARY TABLETING & INSTRUMENTED DUAL COMPACTION PHYSICS:
     - Dried and milled granules pass into the tablet press feed hopper, feeding a variable-speed force feeder with dual
       counter-rotating paddle wheels that fluidize and homogenize granule bed density inside the die cavity.
     - The rotary turret rotates at angular velocity omega_turret [rpm], producing up to 250,000 tablets/h across 48 punch
       stations arranged along the pitch circle diameter (PCD = 410 mm).
     - Compaction occurs in two distinct mechanical stages:
       * Pre-Compression Stage: Low punch force (2.0 to 10.0 kN) applied via pre-compression rollers to evacuate entrapped
         air from the loose granule column, consolidate the powder bed, and prevent capping/lamination at high speeds.
       * Main Compression Stage: High punch force (15.0 to 60.0 kN, max allowable 100 kN) applied via main pressure rollers,
         inducing plastic deformation and particle bonding.
     - Compaction Thermodynamics and Heckel / Kawakita Porosity Modeling:
       The classical Heckel equation describes tablet porosity reduction under compression pressure P_comp [MPa]:
           ln( 1.0 / (1.0 - D_rel) ) = K_heckel * P_comp + A_heckel
       where D_rel = rho_tablet / rho_true (relative density), K_heckel is a material plasticity parameter (reciprocal of
       mean yield pressure P_y), and A_heckel is related to initial die filling and die re-arrangement.
       The Kawakita equation characterizes powder consolidation:
           P_comp / C_comp = (1.0 / (a_kawa * b_kawa)) + (P_comp / a_kawa)
       where C_comp = (V_0 - V_p) / V_0 is degree of volume reduction.
     - Tablet Tensile Strength & Breaking Force (Hardness):
       For flat-faced cylindrical tablets with diameter D_tab [mm] and thickness t_tab [mm], breaking force F_break [N]
       is de-coupled from punch peak force F_main [kN] via the Fell and Newton tensile strength relationship:
           sigma_tensile = (2.0 * F_break) / (pi * D_tab * t_tab)
       Nominal target: Tablet hardness = 80.0 to 130.0 N, thickness = 4.20 mm +- 0.05 mm, weight = 250.0 mg +- 2.0 mg.

  4. HIGH-SPEED SINGLE-TABLET WEIGHT OBSERVER & FAST-RESPONSE REJECT JET (< 10 ms):
     - Each of the 48 punch stations is tracked dynamically via an optical turret absolute encoder. Instrumented
       piezoelectric load cells measure peak compression force for every individual tablet compaction cycle.
     - Under constant tooling geometry and die filling depth, compression peak force correlates with tablet weight:
           Delta_Weight = (dWeight / dForce) * (F_main_actual - F_main_target)
     - Individual punch tracking registers detect:
       * Punch-to-punch force variance (identifying damaged punch tips, worn cams, or sticky guide bushings).
       * Transient feeder starvation (inducing sudden low-force tablets).
     - When any tablet compression force falls outside upper/lower specification limits (+-5.0% warning, +-10.0% reject),
       a precision pneumatic air jet valve situated at the tablet discharge chute is triggered with exact angular micro-second
       timing (< 10 ms pulse), blowing the defective single tablet into a segregated reject bin without decelerating the press.

  5. 8-STATE DISCRETE CYBER-PHYSICAL STATE-SPACE FORMULATION & RECEDING-HORIZON MPC:
     - Continuous tableting process dynamics are discretized at Ts = 2 ms:
           x[k+1] = A * x[k] + B * u[k] + E * d[k]
           y[k]   = C * x[k] + D * u[k]
       State Vector x (8x1):
         x[1]: Granulator Dry Powder Mass Feed Rate                            [kg/h]
         x[2]: Granulator Liquid-to-Solid Ratio (L/S)                          [% w/w]
         x[3]: Granule Median Particle Size (d50)                              [um]
         x[4]: Fluid Bed Granule Residual Moisture Content (% LOD)             [%]
         x[5]: Fluid Bed Drying Plenum Supply Air Temperature                  [deg C]
         x[6]: Rotary Tablet Press Turret Rotational Speed                     [rpm]
         x[7]: Tablet Press Main Compression Peak Punch Force                  [kN]
         x[8]: Compressed Tablet Breaking Force / Hardness                     [N]
       Manipulated Control Input Vector u (8x1):
         u[1]: Loss-in-Weight Twin-Screw Feeder Motor Inverter Command         [Hz]
         u[2]: Liquid Binder Peristaltic Micro-Pump Dosing Flow Rate           [g/min]
         u[3]: Granulator Co-Rotating Twin-Screw Drive Speed Command           [rpm]
         u[4]: Fluid Bed Conditioned Supply Air Heater Thyristor Duty Cycle    [%]
         u[5]: Fluid Bed Fluidization Air Flow Inverter Velocity Damper        [%]
         u[6]: Tablet Press Turret Main Drive Servo Speed Command              [rpm]
         u[7]: Tablet Press Die Feed Shoe Dual Paddle Wheel Speed Command      [rpm]
         u[8]: Lower Punch Main Compression Dosing Cam Servo Vertical Position [mm]
       Disturbance Vector d (4x1):
         d[1]: Powder Bulk Density Infeed Variation                            [g/cm3]
         d[2]: Ambient Air Relative Humidity Ingress                           [% RH]
         d[3]: Liquid Binder Solution Reservoir Temperature Drift              [deg C]
         d[4]: Compression Punch Tooling Temperature Thermal Expansion         [deg C]
*)
VAR_INPUT
    (* ============================================================================================== *)
    (* MASTER PRODUCTION & SAFETY PERMISSIVE SIGNALS                                                 *)
    (* ============================================================================================== *)
    bSystemEnable                       : BOOL;     (* Master System Enable / Line Power Interlock Permissive *)
    bProductionRunCmd                   : BOOL;     (* Production Start Command from Batch Execution System (MES/SCADA) *)
    bEmergencyStop                      : BOOL;     (* Hardwired Dual-Channel SIL-3 Emergency Stop (1=Healthy, 0=Tripped) *)
    bBatchDrainModeCmd                  : BOOL;     (* Command to Initiate End-of-Batch Complete Granule Runout Drain *)
    bAlarmAcknowledge                   : BOOL;     (* Operator Alarm Acknowledge Pushbutton *)
    bAlarmReset                         : BOOL;     (* Master Alarm Reset Pushbutton *)
    bRejectGateManualTestCmd            : BOOL;     (* Maintenance Manual Test Pulse for High-Speed Reject Air Jet *)

    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) PRIMARY PROCESS INSTRUMENTATION                            *)
    (* ============================================================================================== *)
    (* 1. Twin-Screw Loss-In-Weight (LIW) Gravimetric Feeder Load Cells [kg/h] *)
    rFeederFlow_ChA_kgh                 : REAL;     (* Feeder Triplicate Load Cell Gravimetric Flow Channel A [kg/h] *)
    rFeederFlow_ChB_kgh                 : REAL;     (* Feeder Triplicate Load Cell Gravimetric Flow Channel B [kg/h] *)
    rFeederFlow_ChC_kgh                 : REAL;     (* Feeder Triplicate Load Cell Gravimetric Flow Channel C [kg/h] *)

    (* 2. In-Line Fluid Bed Microwave Resonance Moisture Cavity Probes [% LOD] *)
    rMoistureLOD_ChA_pct                : REAL;     (* Microwave Resonance Moisture Sensor Channel A [%] *)
    rMoistureLOD_ChB_pct                : REAL;     (* Microwave Resonance Moisture Sensor Channel B [%] *)
    rMoistureLOD_ChC_pct                : REAL;     (* Microwave Resonance Moisture Sensor Channel C [%] *)

    (* 3. Rotary Tablet Press Pre-Compression Piezoelectric Punch Load Cells [kN] *)
    rPreCompForce_ChA_kN                : REAL;     (* Pre-Compression Upper Roller Load Cell Channel A [kN] *)
    rPreCompForce_ChB_kN                : REAL;     (* Pre-Compression Upper Roller Load Cell Channel B [kN] *)
    rPreCompForce_ChC_kN                : REAL;     (* Pre-Compression Upper Roller Load Cell Channel C [kN] *)

    (* 4. Rotary Tablet Press Main Compression Piezoelectric Punch Load Cells [kN] *)
    rMainCompForce_ChA_kN               : REAL;     (* Main Compression Upper Roller Load Cell Channel A [kN] *)
    rMainCompForce_ChB_kN               : REAL;     (* Main Compression Upper Roller Load Cell Channel B [kN] *)
    rMainCompForce_ChC_kN               : REAL;     (* Main Compression Upper Roller Load Cell Channel C [kN] *)

    (* 5. Rotary Tablet Press Turret Resolver Shaft Encoders [rpm] *)
    rTurretSpeed_ChA_rpm                : REAL;     (* Rotary Turret High-Resolution Shaft Encoder Channel A [rpm] *)
    rTurretSpeed_ChB_rpm                : REAL;     (* Rotary Turret High-Resolution Shaft Encoder Channel B [rpm] *)
    rTurretSpeed_ChC_rpm                : REAL;     (* Rotary Turret High-Resolution Shaft Encoder Channel C [rpm] *)

    (* 6. Continuous Fluid Bed Dryer Plenum Differential Pressure Transmitters [mbar] *)
    rFluidBedDiffPress_ChA_mbar         : REAL;     (* Fluid Bed Distributor Plate Delta-P Transmitter Channel A [mbar] *)
    rFluidBedDiffPress_ChB_mbar         : REAL;     (* Fluid Bed Distributor Plate Delta-P Transmitter Channel B [mbar] *)
    rFluidBedDiffPress_ChC_mbar         : REAL;     (* Fluid Bed Distributor Plate Delta-P Transmitter Channel C [mbar] *)

    (* ============================================================================================== *)
    (* GRANULATION & DRYING PROCESS SENSORS WITH BRACKETED PHYSICAL UNITS                            *)
    (* ============================================================================================== *)
    rGranulatorBarrelTemp_degC          : REAL;     (* Twin-Screw Granulator Jacket Temperature Feedback [deg C] *)
    rGranulatorScrewTorque_Nm           : REAL;     (* Twin-Screw Drive Shaft Torque Feedback [Nm] *)
    rGranulatorScrewSpeed_rpm           : REAL;     (* Twin-Screw Drive Actual Rotational Speed [rpm] *)
    rBinderPumpActualFlow_gpmin         : REAL;     (* Liquid Binder Peristaltic Pump Actual Flow Rate [g/min] *)
    rBinderDeliveryPressure_bar         : REAL;     (* Liquid Binder Delivery Manifold Pressure [bar] *)
    rFluidBedInletAirTemp_degC          : REAL;     (* Conditioned Supply Air Inflow Temperature to Fluid Bed [deg C] *)
    rFluidBedExhaustAirTemp_degC        : REAL;     (* Fluid Bed Exhaust Air Relative Humidity / Temperature [deg C] *)
    rFluidBedAirVelocity_mps            : REAL;     (* Superficial Fluidization Air Velocity Feedback [m/s] *)
    rGranuleDischargeRate_kgh           : REAL;     (* Continuous Granule Dry Discharge Mass Flow Rate [kg/h] *)

    (* ============================================================================================== *)
    (* ROTARY TABLET PRESS SENSORS & MECHANICAL POSITION FEEDBACK                                    *)
    (* ============================================================================================== *)
    rFeederShoePaddleSpeed_rpm          : REAL;     (* Die Table Force Feeder Paddle Wheel Actual Speed [rpm] *)
    rLowerPunchDosingPos_mm             : REAL;     (* Lower Punch Fill Cam Vertical Position Feedback [mm] *)
    rUpperPunchEntryDepth_mm            : REAL;     (* Upper Punch Penetration Depth Inside Die Cavity [mm] *)
    rTabletEjectionForce_N              : REAL;     (* Ejection Cam Track Friction / Ejection Force [N] *)
    rPunchLubricationDosingFlow_mgps    : REAL;     (* Automated Magnesium Stearate Spray Dosing Flow [mg/s] *)
    rDieTableTemperature_degC           : REAL;     (* Rotary Turret Die Segment Surface Temperature [deg C] *)
    rTurretShaftResolverAngle_deg       : REAL;     (* Turret Absolute Mechanical Angular Position [deg] *)
    bTabletSensRejectChuteOptical       : BOOL;     (* High-Speed Optical Sensor at Reject Gate Chute Entrance *)
    bTabletSensGoodChuteOptical         : BOOL;     (* Optical Counter Sensor at Qualified Tablet Discharge Chute *)

    (* ============================================================================================== *)
    (* PRODUCTION RECIPE PARAMETER SETPOINTS (SP)                                                    *)
    (* ============================================================================================== *)
    rRecipeTargetFeederFlow_kgh         : REAL;     (* Recipe Setpoint Dry Powder Feed Rate [kg/h] *)
    rRecipeTargetLiquidSolidRatio_pct   : REAL;     (* Recipe Setpoint Granulation Liquid-to-Solid Ratio [%] *)
    rRecipeTargetScrewSpeed_rpm         : REAL;     (* Recipe Setpoint Twin-Screw Speed [rpm] *)
    rRecipeTargetFluidBedTemp_degC      : REAL;     (* Recipe Setpoint Fluid Bed Inflow Air Temperature [deg C] *)
    rRecipeTargetFluidBedAirVel_mps     : REAL;     (* Recipe Setpoint Superficial Air Velocity [m/s] *)
    rRecipeTargetMoistureLOD_pct        : REAL;     (* Recipe Setpoint Granule Residual Moisture LOD [%] *)
    rRecipeTargetTurretSpeed_rpm        : REAL;     (* Recipe Setpoint Rotary Press Turret Speed [rpm] *)
    rRecipeTargetMainCompForce_kN       : REAL;     (* Recipe Setpoint Main Compression Peak Punch Force [kN] *)
    rRecipeTargetPreCompForce_kN        : REAL;     (* Recipe Setpoint Pre-Compression De-Aeration Force [kN] *)
    rRecipeTargetTabletWeight_mg        : REAL;     (* Target Unit Tablet Weight [mg] *)
    rRecipeTargetTabletHardness_N       : REAL;     (* Target Unit Tablet Breaking Hardness [N] *)
    rRecipeTargetTabletThickness_mm     : REAL;     (* Target Unit Tablet Thickness [mm] *)
END_VAR
VAR_OUTPUT
    (* ============================================================================================== *)
    (* MASTER LINE STATUS, OPERATIONAL STATE & SAFETY FLAGS                                          *)
    (* ============================================================================================== *)
    bSystemReady                        : BOOL;     (* System Ready for Production Handshake *)
    bProductionActive                   : BOOL;     (* Fully Integrated Continuous Manufacturing Active *)
    bEmergencyTripped                   : BOOL;     (* Safety Circuit / Overpressure Trip Active *)
    bBatchDrainingActive                : BOOL;     (* Batch Drain & Granule Runout Sequence Active *)
    bBatchDrainComplete                 : BOOL;     (* Entire Line Granule Drain Successfully Completed *)
    nOperationalState                   : INT;      (* Active 14-Stage FSM State Index (0 to 14) *)
    
    (* ============================================================================================== *)
    (* 2oo3 TMR VOTED SENSOR SIGNALS & VALIDATED METRICS                                             *)
    (* ============================================================================================== *)
    rVotedFeederFlow_kgh                : REAL;     (* 2oo3 Voted Gravimetric Feeder Feed Rate [kg/h] *)
    rVotedMoistureLOD_pct               : REAL;     (* 2oo3 Voted Granule Residual Moisture LOD [%] *)
    rVotedPreCompForce_kN               : REAL;     (* 2oo3 Voted Pre-Compression Punch Force [kN] *)
    rVotedMainCompForce_kN              : REAL;     (* 2oo3 Voted Main Compression Peak Punch Force [kN] *)
    rVotedTurretSpeed_rpm               : REAL;     (* 2oo3 Voted Rotary Turret Speed [rpm] *)
    rVotedFluidBedDiffPress_mbar        : REAL;     (* 2oo3 Voted Fluid Bed Distributor Delta-P [mbar] *)

    (* ============================================================================================== *)
    (* FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE OBSERVER ESTIMATES                                *)
    (* ============================================================================================== *)
    rObservedLiquidSolidRatio_pct       : REAL;     (* In-Line Estimated Liquid-to-Solid Ratio [% w/w] *)
    rObservedGranuleMedianD50_um        : REAL;     (* In-Line Estimated Granule Median Particle Size [um] *)
    rObservedTabletPorosity_pct         : REAL;     (* Heckel Model Estimated Compact Porosity [%] *)
    rObservedTabletHardness_N           : REAL;     (* Estimated Tablet Breaking Tensile Hardness [N] *)
    rObservedTabletWeight_mg            : REAL;     (* In-Line De-Coupled Single-Tablet Mass Estimate [mg] *)
    rObservedTabletProductionRate_tph   : REAL;     (* Real-Time Net Tablet Throughput Rate [tablets/h] *)

    (* ============================================================================================== *)
    (* PRIMARY ACTUATOR CONTROL COMMAND OUTPUTS                                                      *)
    (* ============================================================================================== *)
    rFeederMotorSpeedCommand_Hz         : REAL;     (* Loss-In-Weight Feeder Screw Drive Inverter Command [Hz] *)
    rBinderPumpFlowCommand_gpmin        : REAL;     (* Peristaltic Liquid Binder Dosing Pump Setpoint [g/min] *)
    rGranulatorScrewSpeedCommand_rpm    : REAL;     (* Twin-Screw Granulator Drive Motor Speed Setpoint [rpm] *)
    rFluidBedHeaterDuty_pct             : REAL;     (* Fluid Bed Supply Air Heating Thyristor PWM Duty [%] *)
    rFluidBedAirFlowVelocity_pct        : REAL;     (* Fluid Bed Air Blower Damper Position Command [%] *)
    rTurretDriveSpeedCommand_rpm        : REAL;     (* Rotary Press Main Turret Drive Servo Speed [rpm] *)
    rFeederShoePaddleSpeedCommand_rpm   : REAL;     (* Die Table Force Feeder Paddle Wheel Speed [rpm] *)
    rLowerPunchDosingCamCommand_mm      : REAL;     (* Lower Punch Fill Cam Vertical Actuator Position [mm] *)

    (* ============================================================================================== *)
    (* HIGH-SPEED SINGLE-TABLET REJECT GATE ACTUATION                                                *)
    (* ============================================================================================== *)
    bHighSpeedRejectGateSolenoidCmd     : BOOL;     (* High-Speed (< 10 ms) Fast-Acting Pneumatic Reject Jet *)
    nActiveRejectPunchStation           : INT;      (* Station Number (1 to 48) Currently Under Reject Divert *)
    diTotalGoodTabletsProduced          : DINT;     (* Cumulative Good Tablet Batch Count Counter *)
    diTotalRejectedTabletsCount         : DINT;     (* Cumulative Out-of-Spec Rejected Tablet Counter *)

    (* ============================================================================================== *)
    (* ISA-18.2 MULTI-TIER ALARM TRIP FLAGS & BIT-PACKED WORDS                                       *)
    (* ============================================================================================== *)
    dwTabletingStatusWord               : DWORD;    (* 32-Bit System Operational State Bitmask *)
    dwTabletingDiagnosticWord           : DWORD;    (* 32-Bit Critical Fault & Interlock Diagnostic Bitmask *)
    bAlarmHighHighMainForce             : BOOL;     (* Priority 1 Critical Punch Overpressure HH Trip *)
    bAlarmLowLowMainForce               : BOOL;     (* Priority 2 Incomplete Compaction / Capping LL Trip *)
    bAlarmHighMoistureLOD               : BOOL;     (* Priority 2 Granule Moisture LOD High Warning *)
    bAlarmLowMoistureLOD                : BOOL;     (* Priority 2 Granule Moisture LOD Low Warning *)
    bAlarmHighGranulatorTorque          : BOOL;     (* Priority 1 Granulator Barrel Viscous Dough Torque Trip *)
    bAlarmFeederStarvation              : BOOL;     (* Priority 2 LIW Feeder Mass Flow Deviation Trip *)
    bAlarmTurretSpeedDeviation          : BOOL;     (* Priority 2 Turret Speed Servo Following Deviation *)
    bAlarmEjectionForceHigh             : BOOL;     (* Priority 2 Die Wall Sticking / Lubrication Deficit *)
END_VAR
VAR
    (* ============================================================================================== *)
    (* EXECUTION SCAN INTERVAL & SYSTEM CONSTANTS                                                     *)
    (* ============================================================================================== *)
    T_CYCLE_SEC                         : REAL := 0.002;    (* Discrete Cyclic Scan Period Ts = 2 ms [s] *)
    NUM_STATES                          : INT := 8;         (* Cyber-Physical State Dimension *)
    NUM_INPUTS                          : INT := 8;         (* Manipulated Actuator Input Dimension *)
    NUM_DISTURBANCES                    : INT := 4;         (* External Disturbance Input Dimension *)
    HORIZON_NP                          : INT := 5;         (* Receding-Horizon Prediction Step Count *)
    NUM_TURRET_STATIONS                 : INT := 48;        (* Total Number of Tooling Punch Stations EU-B *)
    PI_CONST                            : REAL := 3.14159265358979; (* Mathematical Constant Pi *)
    bMatricesInitialized                : BOOL := FALSE;    (* One-Shot State-Space Matrix Initialization Flag *)

    (* ============================================================================================== *)
    (* DISCRETE STATE-SPACE ARRAYS & VECTORS                                                          *)
    (* x[k+1] = A * x[k] + B * u[k] + E * d[k]                                                        *)
    (* y[k]   = C * x[k] + D * u[k]                                                                   *)
    (* ============================================================================================== *)
    a_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* State Transition Matrix A (8x8) *)
    b_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* Input Coupling Matrix B (8x8) *)
    c_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* Observation Output Matrix C (8x8) *)
    d_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* Feedthrough Matrix D (8x8) *)
    e_mat                               : ARRAY[1..8, 1..4] OF REAL;    (* Disturbance Coupling Matrix E (8x4) *)
    l_observer                          : ARRAY[1..8] OF REAL;          (* Luenberger Observer Correction Gains *)

    x_state                             : ARRAY[1..8] OF REAL;          (* Cyber-Physical Estimated State x[k] *)
    x_pred                              : ARRAY[1..8] OF REAL;          (* Model Propagated Predicted State x[k+1] *)
    y_meas                              : ARRAY[1..8] OF REAL;          (* Measured Sensor Feedback Vector y[k] *)
    u_ctrl                              : ARRAY[1..8] OF REAL;          (* Active Manipulated Actuator Vector u[k] *)
    u_prev                              : ARRAY[1..8] OF REAL;          (* Previous Step Actuator Vector u[k-1] *)
    d_dist                              : ARRAY[1..4] OF REAL;          (* In-Line Disturbance Vector d[k] *)
    x_ref                               : ARRAY[1..8] OF REAL;          (* Reference State Setpoint Vector *)
    u_ref                               : ARRAY[1..8] OF REAL;          (* Nominal Equilibrium Actuator Vector *)

    (* ============================================================================================== *)
    (* MODEL PREDICTIVE CONTROL (MPC) COST MATRICES & PROJECTION BOUNDS                               *)
    (* ============================================================================================== *)
    q_diag                              : ARRAY[1..8] OF REAL;          (* State Error Penalty Diagonal Q *)
    r_diag                              : ARRAY[1..8] OF REAL;          (* Actuator Effort Penalty Diagonal R *)
    s_diag                              : ARRAY[1..8] OF REAL;          (* Actuator Slew Rate Penalty Diagonal S *)
    p_diag                              : ARRAY[1..8] OF REAL;          (* Terminal State Penalty Diagonal P *)
    u_min                               : ARRAY[1..8] OF REAL;          (* Actuator Lower Box Saturation Bound *)
    u_max                               : ARRAY[1..8] OF REAL;          (* Actuator Upper Box Saturation Bound *)
    du_max                              : ARRAY[1..8] OF REAL;          (* Maximum Slew Rate Delta-U Limit *)
    grad_u                              : ARRAY[1..8] OF REAL;          (* MPC Projected Gradient Vector *)
    u_tentative                         : ARRAY[1..8] OF REAL;          (* Candidate Actuator Command *)
    rMpcStepSize                        : REAL := 0.052;                (* PGD Step Length Parameter Alpha *)
    rMpcAccumulatedCost                 : REAL;                         (* Value of Quadratic Cost Functional J *)

    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) STRUCTURES & TIMERS                                       *)
    (* ============================================================================================== *)
    (* Sensor 1: Gravimetric Feeder Load Cells [kg/h] *)
    rFeeder_Delta_AB                    : REAL;     (* |Feeder A - Feeder B| [kg/h] *)
    rFeeder_Delta_BC                    : REAL;     (* |Feeder B - Feeder C| [kg/h] *)
    rFeeder_Delta_CA                    : REAL;     (* |Feeder C - Feeder A| [kg/h] *)
    rFeeder_DiscrepancyLimit_kgh        : REAL := 1.25;     (* Max Allowed Load Cell Variance [kg/h] *)
    rFeeder_DiscrepancyTimer_s          : REAL := 0.0;      (* Feeder Discrepancy Fault Integrator [s] *)
    bFeeder_ChA_Valid                   : BOOL := TRUE;     (* Feeder Channel A Health Status *)
    bFeeder_ChB_Valid                   : BOOL := TRUE;     (* Feeder Channel B Health Status *)
    bFeeder_ChC_Valid                   : BOOL := TRUE;     (* Feeder Channel C Health Status *)
    nFeeder_VotingMode                  : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)

    (* Sensor 2: Microwave Resonance Moisture Probes [% LOD] *)
    rMoist_Delta_AB                     : REAL;     (* |Moist A - Moist B| [%] *)
    rMoist_Delta_BC                     : REAL;     (* |Moist B - Moist C| [%] *)
    rMoist_Delta_CA                     : REAL;     (* |Moist C - Moist A| [%] *)
    rMoist_DiscrepancyLimit_pct         : REAL := 0.35;     (* Max Allowed Moisture Sensor Discrepancy [%] *)
    rMoist_DiscrepancyTimer_s           : REAL := 0.0;      (* Moisture Sensor Discrepancy Integrator [s] *)
    bMoist_ChA_Valid                    : BOOL := TRUE;     (* Moisture Probe A Health Status *)
    bMoist_ChB_Valid                    : BOOL := TRUE;     (* Moisture Probe B Health Status *)
    bMoist_ChC_Valid                    : BOOL := TRUE;     (* Moisture Probe C Health Status *)
    nMoist_VotingMode                   : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)

    (* Sensor 3: Pre-Compression Piezoelectric Load Cells [kN] *)
    rPreComp_Delta_AB                   : REAL;     (* |PreComp A - PreComp B| [kN] *)
    rPreComp_Delta_BC                   : REAL;     (* |PreComp B - PreComp C| [kN] *)
    rPreComp_Delta_CA                   : REAL;     (* |PreComp C - PreComp A| [kN] *)
    rPreComp_DiscrepancyLimit_kN        : REAL := 0.85;     (* Max Pre-Compression Discrepancy [kN] *)
    rPreComp_DiscrepancyTimer_s         : REAL := 0.0;      (* Pre-Compression Discrepancy Integrator [s] *)
    bPreComp_ChA_Valid                  : BOOL := TRUE;     (* Pre-Compression Channel A Valid *)
    bPreComp_ChB_Valid                  : BOOL := TRUE;     (* Pre-Compression Channel B Valid *)
    bPreComp_ChC_Valid                  : BOOL := TRUE;     (* Pre-Compression Channel C Valid *)
    nPreComp_VotingMode                 : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)

    (* Sensor 4: Main Compression Piezoelectric Load Cells [kN] *)
    rMainComp_Delta_AB                  : REAL;     (* |MainComp A - MainComp B| [kN] *)
    rMainComp_Delta_BC                  : REAL;     (* |MainComp B - MainComp C| [kN] *)
    rMainComp_Delta_CA                  : REAL;     (* |MainComp C - MainComp A| [kN] *)
    rMainComp_DiscrepancyLimit_kN       : REAL := 2.50;     (* Max Main Compression Discrepancy [kN] *)
    rMainComp_DiscrepancyTimer_s        : REAL := 0.0;      (* Main Compression Discrepancy Integrator [s] *)
    bMainComp_ChA_Valid                 : BOOL := TRUE;     (* Main Compression Channel A Valid *)
    bMainComp_ChB_Valid                 : BOOL := TRUE;     (* Main Compression Channel B Valid *)
    bMainComp_ChC_Valid                 : BOOL := TRUE;     (* Main Compression Channel C Valid *)
    nMainComp_VotingMode                : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)

    (* Sensor 5: Rotary Press Turret Resolvers [rpm] *)
    rTurret_Delta_AB                    : REAL;     (* |Turret A - Turret B| [rpm] *)
    rTurret_Delta_BC                    : REAL;     (* |Turret B - Turret C| [rpm] *)
    rTurret_Delta_CA                    : REAL;     (* |Turret C - Turret A| [rpm] *)
    rTurret_DiscrepancyLimit_rpm        : REAL := 1.50;     (* Max Turret Resolver Discrepancy [rpm] *)
    rTurret_DiscrepancyTimer_s          : REAL := 0.0;      (* Turret Resolver Discrepancy Integrator [s] *)
    bTurret_ChA_Valid                   : BOOL := TRUE;     (* Turret Resolver A Valid *)
    bTurret_ChB_Valid                   : BOOL := TRUE;     (* Turret Resolver B Valid *)
    bTurret_ChC_Valid                   : BOOL := TRUE;     (* Turret Resolver C Valid *)
    nTurret_VotingMode                  : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)

    (* Sensor 6: Fluid Bed Differential Pressure Transmitters [mbar] *)
    rFBDiff_Delta_AB                    : REAL;     (* |DiffP A - DiffP B| [mbar] *)
    rFBDiff_Delta_BC                    : REAL;     (* |DiffP B - DiffP C| [mbar] *)
    rFBDiff_Delta_CA                    : REAL;     (* |DiffP C - DiffP A| [mbar] *)
    rFBDiff_DiscrepancyLimit_mbar       : REAL := 1.80;     (* Max Fluid Bed Delta-P Discrepancy [mbar] *)
    rFBDiff_DiscrepancyTimer_s          : REAL := 0.0;      (* Fluid Bed Delta-P Discrepancy Integrator [s] *)
    bFBDiff_ChA_Valid                   : BOOL := TRUE;     (* Fluid Bed Delta-P A Valid *)
    bFBDiff_ChB_Valid                   : BOOL := TRUE;     (* Fluid Bed Delta-P B Valid *)
    bFBDiff_ChC_Valid                   : BOOL := TRUE;     (* Fluid Bed Delta-P C Valid *)
    nFBDiff_VotingMode                  : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)

    (* Common TMR Discrepancy Trip Delay Parameter *)
    T_DISCREPANCY_MAX_SEC               : REAL := 0.500;    (* 500 ms Persistent Discrepancy Disqualifies Channel *)

    (* ============================================================================================== *)
    (* HECKEL / KAWAKITA DE-COUPLING MODEL CONSTANTS & PUNCH TRACKING                                 *)
    (* ============================================================================================== *)
    rHeckelYieldPressure_MPa            : REAL := 145.0;    (* Mean Yield Compaction Pressure Py [MPa] *)
    rHeckelIntercept_A                  : REAL := 0.620;    (* Heckel Packing Initial Intercept Parameter *)
    rTruePowderDensity_gpcm3            : REAL := 1.480;    (* True Solid Particle Density rho_true [g/cm3] *)
    rPunchDiameter_mm                   : REAL := 10.0;     (* Tooling Punch Tip Face Diameter [mm] *)
    rTabletNominalThickness_mm          : REAL := 4.25;     (* Target Tablet Cylindrical Height [mm] *)
    rPunchArea_mm2                      : REAL := 78.5398;  (* Punch Face Area: pi * (D/2)^2 [mm2] *)
    rMainCompPressure_MPa               : REAL;             (* In-Line Applied Compaction Stress [MPa] *)
    rRelativeDensity_D                  : REAL;             (* Calculated Compact Relative Density D *)

    (* Rotary Press Punch Station Tracking Arrays (Stations 1 to 48) *)
    arrStationPeakForce                 : ARRAY[1..48] OF REAL;     (* Recorded Peak Force for Punch i [kN] *)
    arrStationPreCompForce              : ARRAY[1..48] OF REAL;     (* Recorded Pre-Comp Force for Punch i [kN] *)
    arrStationRejectFlag                : ARRAY[1..48] OF BOOL;     (* Flagged Defect Status for Punch Station i *)
    arrStationConsecutiveRejects        : ARRAY[1..48] OF INT;      (* Cumulative Consecutive Fault Counter *)
    nCurrentTurretPunchIndex            : INT := 1;                 (* Active Punch Under Main Roller *)
    nRejectStationTargetIndex           : INT := 1;                 (* Predicted Punch Approaching Reject Gate *)
    rAngularStationStep_deg             : REAL := 7.50;             (* 360.0 / 48 Punch Spacing [deg] *)
    rRejectChuteOffsetAngle_deg         : REAL := 120.0;            (* Angular Distance Main Roller to Reject Jet *)
    rRejectPulseTimer_s                 : REAL := 0.0;              (* High-Speed Reject Air Jet Timer [s] *)
    bRejectValveActive                  : BOOL := FALSE;            (* Reject Air Solenoid Output State *)

    (* ============================================================================================== *)
    (* FINITE STATE MACHINE (FSM) STAGE CONTROL VARIABLES & TIMERS                                    *)
    (* ============================================================================================== *)
    rStateTimer_s                       : REAL := 0.0;      (* Operational State Dwell Integrator [s] *)
    nTargetState                        : INT := 0;         (* FSM Transition Destination State *)
    bStateTransitionTrigger             : BOOL := FALSE;    (* Transition Request Flag *)
    bWarmupComplete                     : BOOL := FALSE;    (* Fluid Bed Warmup Permissive Flag *)
    bDryBlendEquilibrated               : BOOL := FALSE;    (* Twin-Screw Granulator Dry Run Stabilized *)
    bNucleationEstablished              : BOOL := FALSE;    (* Liquid Binder Nucleation Established *)
    bMoistureStabilized                 : BOOL := FALSE;    (* Granule LOD Within Process Window *)
    bFeederShoeFilled                   : BOOL := FALSE;    (* Die Table Force Feeder Powder Bed Ready *)
    bTurretSpeedSynchronized            : BOOL := FALSE;    (* Turret Up to Production Operating Speed *)
    bContinuousTabletingSteady          : BOOL := FALSE;    (* Tablet Compression at Target Cpk *)
    bBatchDrainCompletedInternal        : BOOL := FALSE;    (* Runout Drain Finished Internally *)

    (* ============================================================================================== *)
    (* ISA-18.2 ALARM THRESHOLDS, DEADBANDS & RATE-OF-CHANGE (RoC) REGISTERS                          *)
    (* ============================================================================================== *)
    (* Main Compression Force Alarms [kN] *)
    rSP_MainForce_HH_kN                 : REAL := 55.0;     (* Overpressure Danger Trip Limit [kN] *)
    rSP_MainForce_H_kN                  : REAL := 42.0;     (* High Force Upper Spec Limit [kN] *)
    rSP_MainForce_L_kN                  : REAL := 18.0;     (* Low Force Lower Spec Limit [kN] *)
    rSP_MainForce_LL_kN                 : REAL := 10.0;     (* Underpressure / Capping Risk LL Trip [kN] *)
    rDB_MainForce_kN                    : REAL := 1.20;     (* Clearance Deadband Hysteresis [kN] *)

    (* Granule Residual Moisture LOD Alarms [%] *)
    rSP_MoistLOD_HH_pct                 : REAL := 3.40;     (* Wet Massing / Sticking Danger Trip [%] *)
    rSP_MoistLOD_H_pct                  : REAL := 2.60;     (* Moisture High Warning [%] *)
    rSP_MoistLOD_L_pct                  : REAL := 1.40;     (* Moisture Low Warning [%] *)
    rSP_MoistLOD_LL_pct                 : REAL := 0.90;     (* Over-Drying / Friability Trip [%] *)
    rDB_MoistLOD_pct                    : REAL := 0.15;     (* Clearance Deadband Hysteresis [%] *)

    (* Liquid-to-Solid Ratio Alarms [% w/w] *)
    rSP_LS_Ratio_HH_pct                 : REAL := 17.5;     (* Dough Formation Barrel Jam Trip [%] *)
    rSP_LS_Ratio_H_pct                  : REAL := 13.5;     (* Liquid Dosing High Warning [%] *)
    rSP_LS_Ratio_L_pct                  : REAL := 7.5;      (* Dry Blend Low Warning [%] *)
    rSP_LS_Ratio_LL_pct                 : REAL := 5.0;      (* Granulation Starvation Trip [%] *)
    rDB_LS_Ratio_pct                    : REAL := 0.8;      (* Clearance Deadband Hysteresis [%] *)

    (* Fluid Bed Plenum Supply Air Temperature Alarms [deg C] *)
    rSP_FBTemp_HH_degC                  : REAL := 75.0;     (* API Thermal Degradation Danger Trip [deg C] *)
    rSP_FBTemp_H_degC                   : REAL := 68.0;     (* High Air Temperature Warning [deg C] *)
    rSP_FBTemp_L_degC                   : REAL := 45.0;     (* Low Drying Capacity Warning [deg C] *)
    rSP_FBTemp_LL_degC                  : REAL := 35.0;     (* Insufficient Heat Trip [deg C] *)
    rDB_FBTemp_degC                     : REAL := 2.0;      (* Clearance Deadband Hysteresis [deg C] *)

    (* Rate-of-Change (RoC) Tracking Registers *)
    rPrevMainCompForce_kN               : REAL := 0.0;      (* Main Force from Previous PLC Cycle [kN] *)
    rMainCompForce_RoC_kNps             : REAL := 0.0;      (* Derivative dF/dt [kN/s] *)
    rSP_MainForce_RoC_Max_kNps          : REAL := 450.0;    (* Max Allowable Punch Shock Slope [kN/s] *)
    rPrevMoistLOD_pct                   : REAL := 2.0;      (* Moisture from Previous Scan [%] *)
    rMoistLOD_RoC_pctps                 : REAL := 0.0;      (* Derivative d(LOD)/dt [%/s] *)

    (* Alarm Latching Flags *)
    bTripLatched_MainForce_HH           : BOOL := FALSE;
    bTripLatched_MainForce_LL           : BOOL := FALSE;
    bTripLatched_Moist_HH               : BOOL := FALSE;
    bTripLatched_Moist_LL               : BOOL := FALSE;
    bTripLatched_LS_HH                  : BOOL := FALSE;
    bTripLatched_FBTemp_HH              : BOOL := FALSE;
    bTripLatched_GranulatorTorque       : BOOL := FALSE;
    bTripLatched_EmergencyStop          : BOOL := FALSE;

    (* Loop Index Iterators *)
    i                                   : INT;              (* General Purpose Outer Loop Iterator *)
    j                                   : INT;              (* General Purpose Inner Loop Iterator *)
    k                                   : INT;              (* Vector/Matrix Mathematical Iterator *)
    iter                                : INT;              (* Projected Gradient Descent Iteration Counter *)
END_VAR
"""
