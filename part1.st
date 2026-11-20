FUNCTION_BLOCK FB_Mechanical_10000Ton_IsothermalForging_Sync
(* ================================================================================================================
   LUMINA CYBER-PHYSICAL AUTOMATION SYSTEMS ARCHITECTURE - HEAVY FORGING & AEROSPACE TURBINE SERIES
   COMPONENT: FB_Mechanical_10000Ton_IsothermalForging_Sync
   EQUIPMENT: 10,000-Ton (100 MN) High-Precision Isothermal Hydraulic Die Forging Press
   APPLICATION: Titanium Alloy Ti-6Al-4V Aerospace High-Pressure Compressor Discs & Turbine Blisks
   STANDARDS: IEC 61131-3 3rd Ed., ANSI/ISA-88.01 (Batch Control), ANSI/ISA-18.2-2016 (Alarm Management),
              DIN EN 693 / EN ISO 16092-3 (Machine Tools - Hydraulic Presses Safety), ISO 13849-1 Cat 4 / PL e,
              AS9100D Aerospace Quality Management, AMS 4928 / AMS-T-9046 Titanium Forging Specifications.
   ================================================================================================================
   CYBER-PHYSICAL MATHEMATICAL SYSTEM ARCHITECTURE:
   This Function Block executes real-time cyber-physical closed-loop control for a massive 10,000-metric-ton
   (100 MN nominal axial forging force) isothermal hydraulic press cell. The system manufactures near-net-shape
   aerospace turbine engine discs and integrally bladed discs (blisks) from Ti-6Al-4V titanium preforms.
   
   1. 4-CYLINDER DYNAMIC HYDRAULIC SERVO LEVELING DYNAMICS:
      - Ram Platen Dimensions: 3,500 mm x 3,500 mm; Moving Ram Mass: M_ram = 450,000 kg (450 metric tons).
      - 4 Corner Main Hydraulic Rams: Front-Left (FL), Front-Right (FR), Rear-Left (RL), Rear-Right (RR).
      - Bore Diameter: D_bore = 900 mm (Piston Area A_cyl = 0.63617 m2 per cylinder; Total Area = 2.54469 m2).
      - Hydraulic Supply Pressure: P_supply = 350.0 bar (35.0 MPa); Total Hydraulic Force = 89.06 MN nominal,
        with intensifier boost achieving 100.0 MN (10,197 metric tons) at 393.0 bar.
      - Fluid Compressibility: Bulk modulus Beta_oil = 16,500 bar (1.65 GPa); Hydraulic fluid stiffness
        governed by continuity equation: (V_i / Beta_oil) * dP_i/dt = Q_valve_i - A_cyl_i * v_i - C_leak * P_i.
      - Dynamic Eccentric Tilting Moment Rejection: Off-center billet upsetting creates dynamic moments Mx and My.
        Ram angular tilt Theta_x and Theta_y are held within +/- 20.0 micrometers (< 0.0057 mrad) across the 3.5 m span
        via 4 independent high-frequency Moog dynamic servo valves (response bandwidth 85 Hz).
   
   2. SUPERPLASTIC CONSTITUTIVE FLOW STRESS & SELLARS-TEGART HYPERBOLIC SINE KINETICS:
      - Workpiece Material: Extra Low Interstitial (ELI) Titanium Alloy Ti-6Al-4V (AMS 4928).
      - Isothermal Forging Temperature: T = 950.0 deg C (1,223.15 K) in fine equiaxed (alpha + beta) microstructure.
      - Superplastic Strain Rate Sensitivity: True strain rate dEpsilon/dt maintained strictly at 1.0e-3 s^-1.
      - Sellars-Tegart Hyperbolic Sine Constitutive Equation:
        dEpsilon/dt = A_st * [sinh(alpha_st * Sigma)]^n_st * exp(-Q_def / (R_gas * T))
        where Activation Energy Q_def = 641,000 J/mol, Gas Constant R_gas = 8.31446 J/(mol*K),
        Stress Multiplier alpha_st = 0.015 MPa^-1, Stress Exponent n_st = 4.12, Pre-exponential A_st = 2.85e12 s^-1.
      - Zener-Hollomon Temperature-Compensated Strain Rate Parameter: Z = (dEpsilon/dt) * exp(Q_def / (R_gas * T)).
      - Explicit Flow Stress Formulation: Sigma = (1.0 / alpha_st) * asinh( (Z / A_st)^(1.0 / n_st) ).
      - Dynamic Recrystallization (DRX) Kinetics & Grain Size Evolution:
        Critical Strain for DRX: Epsilon_c = 0.8 * Epsilon_peak = 0.0012 * Z^0.125;
        DRX Volume Fraction: X_drx = 1.0 - exp( -beta_drx * ((Epsilon - Epsilon_c) / Epsilon_0.5)^m_drx );
        Steady-State Dynamically Recrystallized Grain Size: d_ss = 350.0 * Z^(-0.18) [micrometers].
   
   3. 950 DEG C MULTI-ZONE INDUCTION DIE HEATING & VACUUM ATMOSPHERE CONTROL:
      - Upper and Lower Die Blocks: High-temperature nickel superalloy IN-100 / TZM Molybdenum (Mass = 28,000 kg).
      - Multi-Zone Medium-Frequency Induction Heating System: 4 independent 375 kW IGBT resonant inverter zones (1.5 MW total).
      - Temperature Uniformity: Held to +/- 2.0 deg C across entire 3,200 mm die diameter.
      - Vacuum Transfer Chamber: Prevents atmospheric oxygen and nitrogen pickup (titanium alpha-case formation);
        Roots blower + turbomolecular vacuum train maintains chamber pressure P_vac < 5.0e-2 mbar.
   
   4. 2oo3 TMR SENSOR VOTING WITH 50ms DISCREPANCY TIMERS:
      - Channel 1: Total Ram Forging Tonnage [kN] (3x strain-gauge load cell columns).
      - Channel 2: Main Cylinder High-Pressure Header [bar] (3x piezoresistive pressure transmitters).
      - Channel 3: Upper Die Induction Core Temperature [deg C] (3x Type-B thermocouple / ratio pyrometers).
      - Channel 4: 4-Corner Ram Leveling Tilt Deviation [um] (3x optical absolute glass scale networks).
   
   5. 6TH-ORDER DISCRETE STATE-SPACE OBSERVER & RECEDING-HORIZON MPC (PGD):
      - 6 Dynamic States: Ram Position x1 [mm], Velocity x2 [mm/s], Flow Stress x3 [MPa], DRX Grain Size x4 [um],
        Die Temperature x5 [deg C], Corner Tilt Angle x6 [um].
      - 5 Control Inputs: Servo Pump Swashplate u1 [%], Leveling Valve Flow u2 [L/min], Induction Power u3 [kW],
        Vacuum Bleed u4 [mbar], Counterbalance Pressure Valve u5 [%].
      - MPC Objective: 10 unrolled iterations of Accelerated Projected Gradient Descent (PGD) with state constraints,
        slew rate limits, true strain rate tracking, and dynamic moment leveling rejection.
   
   6. 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE & ISA-18.2 ALARMS:
      - Fully coordinated sequence from 950 deg C furnace transfer, vacuum lock, superplastic squeeze to blisk laser metrology.
   ================================================================================================================ *)

VAR_INPUT
    (* =========================================================================================================== *)
    (* 1. SYSTEM SUPERVISION, SAFETY INTERLOCKS & MASTER CYCLE COMMANDS                                            *)
    (* =========================================================================================================== *)
    b_EnableMasterSys               : BOOL := FALSE; (* Master Cyber-Physical Executive System Enable Command [bool] *)
    b_ResetAllFaults                : BOOL := FALSE; (* Global Safety and Operational Fault Latches Reset Strobe [bool] *)
    b_AutoCycleStartReq             : BOOL := FALSE; (* Request to Initiate 14-Stage Isothermal Forging Automatic Sequence [bool] *)
    b_EmergencyStopDualCh_PL_e      : BOOL := TRUE;  (* Dual-Channel Cat 4 / PL e Hardwired Safety Gate & Emergency Loop Tripped [bool] *)
    b_SafetyShieldInterlockClosed   : BOOL := TRUE;  (* Hydraulic Safety Enclosure & Vacuum Protective Gate Closed Confirmation [bool] *)
    b_HydraulicPowerUnitRunning     : BOOL := FALSE; (* 6x 450 kW Variable Frequency Main Hydraulic Servo Pump Status [bool] *)
    b_FurnaceTransferClearance      : BOOL := FALSE; (* 950 deg C Rotary Hearth Furnace Robotic Discharge Rail Clear [bool] *)
    b_AcknowledgeAlarms_Strobe      : BOOL := FALSE; (* ISA-18.2 Manual Operator Alarm Acknowledgment Pushbutton [bool] *)
    r_CycleScanPeriod_ms            : REAL := 1.0;   (* Dynamic Discrete Controller Scan Time Period [ms] *)

    (* =========================================================================================================== *)
    (* 2. AEROSPACE TURBINE DISC RECIPE SETPOINTS & KINEMATICS                                                     *)
    (* =========================================================================================================== *)
    r_TargetForgingTonnage_kN       : REAL := 100000.0; (* [kN] Nominal Target Coining Tonnage (100,000 kN = 10,000 metric tons) *)
    r_TargetIsothermalDieTemp_DegC  : REAL := 950.0;    (* [deg C] Target Isothermal Die Block Surface Temperature *)
    r_SuperplasticStrainRate_s_inv  : REAL := 0.0010;   (* [s^-1] Commanded Workpiece True Plastic Strain Rate (1.0e-3 s^-1) *)
    r_InitialBilletHeight_mm        : REAL := 420.0;    (* [mm] Pre-form Raw Titanium Billet Starting Axial Height *)
    r_FinalForgedWebThickness_mm    : REAL := 65.0;     (* [mm] Target Forged Turbine Disc Center Web Residual Thickness *)
    r_RapidApproachVelocity_mm_s    : REAL := 180.0;    (* [mm/s] Ram Free-Fall Rapid Approach Stroke Velocity Target *)
    r_DecompressionRampTime_s       : REAL := 8.5;      (* [s] Hydraulic Active Controlled Decompression Duration *)
    r_VacuumChamberTarget_mbar      : REAL := 0.045;    (* [mbar] High-Vacuum Chamber Base Pressure Limit for Alpha-Case Avoidance *)
    r_MaxAllowableRamTilt_um        : REAL := 20.0;     (* [um] Maximum Dynamic 4-Corner Ram Leveling Tilt Deviation Limit *)

    (* =========================================================================================================== *)
    (* 3. 2oo3 TMR CHANNEL 1: MAIN RAM FORGING TONNAGE [kN]                                                        *)
    (* =========================================================================================================== *)
    r_Tonnage_SensorA_kN            : REAL := 0.0; (* Load Cell Column A (Front-Left Tie Rod Strain Transducer) [kN] *)
    r_Tonnage_SensorB_kN            : REAL := 0.0; (* Load Cell Column B (Front-Right Tie Rod Strain Transducer) [kN] *)
    r_Tonnage_SensorC_kN            : REAL := 0.0; (* Load Cell Column C (Rear Center Piezoelectric Dynamometer) [kN] *)
    b_Tonnage_ValidA                : BOOL := TRUE;(* Hardware Electrical Health Status - Tonnage Sensor A [bool] *)
    b_Tonnage_ValidB                : BOOL := TRUE;(* Hardware Electrical Health Status - Tonnage Sensor B [bool] *)
    b_Tonnage_ValidC                : BOOL := TRUE;(* Hardware Electrical Health Status - Tonnage Sensor C [bool] *)
    r_Tonnage_TMR_TolMax_kN         : REAL := 2500.0; (* [kN] Pairwise Sensor Discrepancy Tolerance (2.5% of Full Scale) *)

    (* =========================================================================================================== *)
    (* 4. 2oo3 TMR CHANNEL 2: MAIN CYLINDER HIGH-PRESSURE HEADER [bar]                                             *)
    (* =========================================================================================================== *)
    r_HydPressure_SensorA_bar       : REAL := 0.0; (* Piezoresistive Pressure Transmitter A (Main Cylinder Manifold) [bar] *)
    r_HydPressure_SensorB_bar       : REAL := 0.0; (* Piezoresistive Pressure Transmitter B (Main Cylinder Manifold) [bar] *)
    r_HydPressure_SensorC_bar       : REAL := 0.0; (* Piezoresistive Pressure Transmitter C (Main Cylinder Manifold) [bar] *)
    b_HydPressure_ValidA            : BOOL := TRUE;(* Hardware Electrical Health Status - Hydraulic Pressure Sensor A [bool] *)
    b_HydPressure_ValidB            : BOOL := TRUE;(* Hardware Electrical Health Status - Hydraulic Pressure Sensor B [bool] *)
    b_HydPressure_ValidC            : BOOL := TRUE;(* Hardware Electrical Health Status - Hydraulic Pressure Sensor C [bool] *)
    r_HydPressure_TMR_TolMax_bar    : REAL := 12.0; (* [bar] Pairwise Pressure Sensor Discrepancy Tolerance *)

    (* =========================================================================================================== *)
    (* 5. 2oo3 TMR CHANNEL 3: UPPER DIE INDUCTION HEATING TEMPERATURE [deg C]                                      *)
    (* =========================================================================================================== *)
    r_DieTemp_SensorA_DegC          : REAL := 950.0; (* Type-B Dual-Sheathed Thermocouple Probe 1 Upper Die Core [deg C] *)
    r_DieTemp_SensorB_DegC          : REAL := 950.0; (* Type-B Dual-Sheathed Thermocouple Probe 2 Upper Die Core [deg C] *)
    r_DieTemp_SensorC_DegC          : REAL := 950.0; (* Infrared Dual-Wavelength Ratio Optical Pyrometer Ch C [deg C] *)
    b_DieTemp_ValidA                : BOOL := TRUE;  (* Hardware Electrical Health Status - Die Temp Sensor A [bool] *)
    b_DieTemp_ValidB                : BOOL := TRUE;  (* Hardware Electrical Health Status - Die Temp Sensor B [bool] *)
    b_DieTemp_ValidC                : BOOL := TRUE;  (* Hardware Electrical Health Status - Die Temp Sensor C [bool] *)
    r_DieTemp_TMR_TolMax_DegC       : REAL := 15.0;  (* [deg C] Pairwise Die Temperature Discrepancy Tolerance *)

    (* =========================================================================================================== *)
    (* 6. 2oo3 TMR CHANNEL 4: 4-CORNER RAM LEVELING TILT SKEW DEVIATION [um]                                       *)
    (* =========================================================================================================== *)
    r_TiltSkew_SensorA_um           : REAL := 0.0; (* Optical Linear Glass Scale Network A Differential Skew [um] *)
    r_TiltSkew_SensorB_um           : REAL := 0.0; (* Optical Linear Glass Scale Network B Differential Skew [um] *)
    r_TiltSkew_SensorC_um           : REAL := 0.0; (* Magnetostrictive Absolute Corner Sensor Network C Skew [um] *)
    b_TiltSkew_ValidA               : BOOL := TRUE;(* Hardware Electrical Health Status - Tilt Skew Sensor A [bool] *)
    b_TiltSkew_ValidB               : BOOL := TRUE;(* Hardware Electrical Health Status - Tilt Skew Sensor B [bool] *)
    b_TiltSkew_ValidC               : BOOL := TRUE;(* Hardware Electrical Health Status - Tilt Skew Sensor C [bool] *)
    r_TiltSkew_TMR_TolMax_um        : REAL := 8.0; (* [um] Pairwise Corner Tilt Discrepancy Tolerance *)

    (* =========================================================================================================== *)
    (* 7. 4 INDIVIDUAL HYDRAULIC CYLINDER PRESSURE & POSITION SENSORS                                              *)
    (* =========================================================================================================== *)
    r_CylPressure_FL_bar            : REAL := 0.0; (* Front-Left Hydraulic Ram Chamber Pressure [bar] *)
    r_CylPressure_FR_bar            : REAL := 0.0; (* Front-Right Hydraulic Ram Chamber Pressure [bar] *)
    r_CylPressure_RL_bar            : REAL := 0.0; (* Rear-Left Hydraulic Ram Chamber Pressure [bar] *)
    r_CylPressure_RR_bar            : REAL := 0.0; (* Rear-Right Hydraulic Ram Chamber Pressure [bar] *)
    r_CylPosition_FL_mm             : REAL := 420.0; (* Front-Left Ram Cylinder Absolute Linear Position [mm] *)
    r_CylPosition_FR_mm             : REAL := 420.0; (* Front-Right Ram Cylinder Absolute Linear Position [mm] *)
    r_CylPosition_RL_mm             : REAL := 420.0; (* Rear-Left Ram Cylinder Absolute Linear Position [mm] *)
    r_CylPosition_RR_mm             : REAL := 420.0; (* Rear-Right Ram Cylinder Absolute Linear Position [mm] *)

    (* =========================================================================================================== *)
    (* 8. DIE INDUCTION POWER & LOWER DIE / BILLET THERMAL TELEMETRY                                               *)
    (* =========================================================================================================== *)
    r_InductionPowerActual_kW       : REAL := 0.0;   (* Combined 4-Zone Induction Generator Active Power Feedback [kW] *)
    r_InductionCurrentActual_A      : REAL := 0.0;   (* Resonant Tank Circuit Primary AC Current [A] *)
    r_LowerDieTemp_DegC             : REAL := 950.0; (* Lower Die Surface Core Multi-Zone Thermocouple [deg C] *)
    r_BilletSurfacePyrometer_DegC   : REAL := 950.0; (* In-Situ Optical Fiber Pyrometer Measuring Titanium Disc Surface [deg C] *)
    r_HydraulicOilSumpTemp_DegC     : REAL := 42.0;  (* 12,000-Liter Hydraulic Power Sump Fluid Reservoir Temp [deg C] *)
    r_HydCoolingWaterFlow_L_min     : REAL := 450.0; (* Heat Exchanger Closed-Loop Cooling Water Volumetric Flow [L/min] *)

    (* =========================================================================================================== *)
    (* 9. VACUUM CHAMBER & ROBOTIC MANIPULATOR INTERFACE SIGNALS                                                   *)
    (* =========================================================================================================== *)
    r_VacuumChamberPressure_mbar    : REAL := 0.035; (* Penning / Pirani Wide-Range Vacuum Chamber Sensor [mbar] *)
    b_VacuumRoughingPumpRunning     : BOOL := TRUE;  (* Roots Mechanical Blower Vacuum Pump Auxiliary Status [bool] *)
    b_TurbomolecularPumpAtSpeed     : BOOL := TRUE;  (* High-Vacuum Turbomolecular Pump Nominal Speed Reached [bool] *)
    b_RoboticLoaderAtForgingPos     : BOOL := FALSE; (* In-Line Titanium Pre-form Gripper In Vacuum Chamber Center [bool] *)
    b_RoboticLoaderRetractedClear   : BOOL := TRUE;  (* In-Line Titanium Pre-form Gripper Parked Outside Die Envelope [bool] *)
    b_LowerDieEjectorRetractedLS    : BOOL := TRUE;  (* Lower Die 4-Pin Hydraulic Ejector Fully Retracted Limit Switch [bool] *)
    b_LowerDieEjectorExtendedLS     : BOOL := FALSE; (* Lower Die 4-Pin Hydraulic Ejector Top Ejection Limit Switch [bool] *)
    r_LowerDieEjectorStroke_mm      : REAL := 0.0;   (* Lower Die Hydraulic Part Lifter Stroke Position [mm] *)
    r_ArgonBackfillPressure_bar     : REAL := 6.0;   (* High-Purity (99.999%) Gaseous Argon Backfill Supply Pressure [bar] *)
    b_LaserMetrologyScanComplete    : BOOL := FALSE; (* Post-Forge 3D Laser Profilometry Dimensional Check Passed [bool] *)
    r_LaserMeasuredWebThick_mm      : REAL := 65.0;  (* Laser Profilometer Scanned Disc Web Thickness Dimension [mm] *)
END_VAR

VAR_OUTPUT
    (* =========================================================================================================== *)
    (* 1. SYSTEM GENERAL STATUS & SUPERVISORY FLAGS                                                                *)
    (* =========================================================================================================== *)
    b_SystemReady                   : BOOL := FALSE; (* Forging Cell Normal Operational Readiness Interlock Confirmed [bool] *)
    b_AutoCycleActive               : BOOL := FALSE; (* 14-Stage Automatic Isothermal Forging Sequence Executing [bool] *)
    b_CycleCompleteStrobe           : BOOL := FALSE; (* Disc Forging Cycle Successfully Finished Pulse Strobe [bool] *)
    b_EmergencyStopTripped          : BOOL := FALSE; (* Safety Relay Tripped - Hydraulic Decompression Immediate Safe Stop [bool] *)
    b_GlobalFaultActive             : BOOL := FALSE; (* Severe Process or Hardware Malfunction Latched [bool] *)
    n_ActiveFSMStage                : INT := 0;      (* Current Active Deterministic Production FSM Stage Index (1 to 14) *)
    r_CurrentStageElapsed_s         : REAL := 0.0;   (* Active FSM State Execution Timer [s] *)

    (* =========================================================================================================== *)
    (* 2. HYDRAULIC SERVO ACTUATOR & PROPORTIONAL PUMP COMMANDS                                                    *)
    (* =========================================================================================================== *)
    r_MainPumpSwashplateCmd_Pct     : REAL := 0.0; (* Variable Displacement Hydraulic Main Pump Swashplate Command [%] *)
    r_RamLevelingValve_FL_Cmd_L_min : REAL := 0.0; (* Dynamic Servo Valve Flow Command - Front-Left Cylinder [L/min] *)
    r_RamLevelingValve_FR_Cmd_L_min : REAL := 0.0; (* Dynamic Servo Valve Flow Command - Front-Right Cylinder [L/min] *)
    r_RamLevelingValve_RL_Cmd_L_min : REAL := 0.0; (* Dynamic Servo Valve Flow Command - Rear-Left Cylinder [L/min] *)
    r_RamLevelingValve_RR_Cmd_L_min : REAL := 0.0; (* Dynamic Servo Valve Flow Command - Rear-Right Cylinder [L/min] *)
    b_PreFillValvesEnergized        : BOOL := FALSE;(* Main Tank Gravity Pre-Fill Pilot Poppet Valves Open Command [bool] *)
    r_ActiveDecompressValveCmd_Pct  : REAL := 0.0; (* Controlled Proportional Hydraulic Decompression Valve [%] *)
    r_CounterbalanceValveCmd_Pct    : REAL := 0.0; (* Dynamic Hydraulic Ram Counterbalance Backpressure Valve [%] *)
    r_LowerDieEjectorHydCmd_Pct     : REAL := 0.0; (* Lower Die 4-Pin Synchronized Hydraulic Ejector Lifter Valve [%] *)

    (* =========================================================================================================== *)
    (* 3. INDUCTION HEATING & VACUUM ATMOSPHERE COMMANDS                                                           *)
    (* =========================================================================================================== *)
    r_InductionPowerCmd_kW          : REAL := 0.0;   (* 4-Zone Induction Inverter Master Power Setpoint Command [kW] *)
    b_InductionInverterRunEnable    : BOOL := FALSE; (* IGBT Medium-Frequency Inverter Gate Driver Run Permissive [bool] *)
    b_VacuumRoughingValveOpen       : BOOL := FALSE; (* Vacuum Foreline Roughing Pumping Isolation Valve Solenoid [bool] *)
    b_VacuumHighVacGateValveOpen    : BOOL := FALSE; (* Turbomolecular High-Vacuum Isolation Gate Valve Solenoid [bool] *)
    b_ArgonBackfillVentValveOpen    : BOOL := FALSE; (* High-Purity Gaseous Argon Chamber Equalization Vent Valve [bool] *)
    b_VacuumChamberDoorOpenCmd      : BOOL := FALSE; (* Vacuum Lock Hydraulic Access Door Actuator Open Command [bool] *)

    (* =========================================================================================================== *)
    (* 4. 2oo3 TMR SENSOR VOTED HEALTH STATUS & CONSOLIDATED VALUES                                                *)
    (* =========================================================================================================== *)
    r_TMR_VotedTonnage_kN           : REAL := 0.0;   (* 2oo3 Triply Voted Main Ram Forging Tonnage [kN] *)
    r_TMR_VotedHydPressure_bar      : REAL := 0.0;   (* 2oo3 Triply Voted Cylinder Manifold Hydraulic Pressure [bar] *)
    r_TMR_VotedDieTemp_DegC         : REAL := 950.0; (* 2oo3 Triply Voted Upper Die Block Core Temperature [deg C] *)
    r_TMR_VotedTiltSkew_um          : REAL := 0.0;   (* 2oo3 Triply Voted 4-Corner Ram Dynamic Leveling Tilt [um] *)
    b_TMR_Tonnage_DegradedMode      : BOOL := FALSE; (* Tonnage Loop Operating in Degraded 2-Sensor Average Mode [bool] *)
    b_TMR_HydPressure_DegradedMode  : BOOL := FALSE; (* Pressure Loop Operating in Degraded 2-Sensor Average Mode [bool] *)
    b_TMR_DieTemp_DegradedMode      : BOOL := FALSE; (* Die Temp Loop Operating in Degraded 2-Sensor Average Mode [bool] *)
    b_TMR_TiltSkew_DegradedMode     : BOOL := FALSE; (* Tilt Skew Loop Operating in Degraded 2-Sensor Average Mode [bool] *)

    (* =========================================================================================================== *)
    (* 5. CYBER-PHYSICAL OBSERVER & CONSTITUTIVE KINETICS ESTIMATES                                                *)
    (* =========================================================================================================== *)
    r_Obs_RamPosition_mm            : REAL := 420.0; (* Observer State x1: Ram Instantaneous Billet Height [mm] *)
    r_Obs_RamVelocity_mm_s          : REAL := 0.0;   (* Observer State x2: Ram Downward Forging Velocity [mm/s] *)
    r_Obs_FlowStress_MPa            : REAL := 0.0;   (* Observer State x3: Ti-6Al-4V True Constitutive Flow Stress [MPa] *)
    r_Obs_DRX_GrainSize_um          : REAL := 12.0;  (* Observer State x4: Dynamically Recrystallized Grain Size [um] *)
    r_Obs_DieInterfaceTemp_DegC     : REAL := 950.0; (* Observer State x5: Workpiece-Die Contact Interface Temp [deg C] *)
    r_Obs_CornerTiltDeviation_um    : REAL := 0.0;   (* Observer State x6: Estimated Corner Angular Skew Deflection [um] *)
    r_InstantaneousTrueStrain       : REAL := 0.0;   (* True Logarithmic Axial Compression Strain: Epsilon = -ln(h/h0) *)
    r_InstantaneousStrainRate_s_inv : REAL := 0.0;   (* True Axial Deformation Strain Rate: dEpsilon/dt = v / h [s^-1] *)
    r_DRX_RecrystallizedFraction    : REAL := 0.0;   (* Fraction of Dynamically Recrystallized Microstructure X_drx (0.0 to 1.0) *)
    r_ZenerHollomonParameter_Z      : REAL := 0.0;   (* Zener-Hollomon Temperature-Compensated Strain Rate Parameter [s^-1] *)

    (* =========================================================================================================== *)
    (* 6. ROBOTIC VACUUM MANIPULATOR HANDSHAKE & METROLOGY INTERFACE                                               *)
    (* =========================================================================================================== *)
    b_FurnaceUnloadRequest          : BOOL := FALSE; (* Request Rotary Hearth Furnace to Dispatch Heated Pre-form [bool] *)
    b_RobotLoadSequenceStartCmd     : BOOL := FALSE; (* Command Vacuum Gripper Robot to Load Pre-form into Press Die [bool] *)
    b_RobotExtractForgedPartCmd     : BOOL := FALSE; (* Command Vacuum Gripper Robot to Extract Finished Blisk [bool] *)
    b_LaserMetrologyScanTriggerCmd  : BOOL := FALSE; (* Trigger 3D Optical Laser Profilometry Inspection Scan [bool] *)
    b_DiscDimensionQualityPassed    : BOOL := FALSE; (* Forged Turbine Disc Final Geometry Within Aerodynamic Spec [bool] *)

    (* =========================================================================================================== *)
    (* 7. FIELDBUS TELEMETRY PACKED WORDS (ISO 13849, DIN EN 693, ISA-18.2, OPC UA)                                *)
    (* =========================================================================================================== *)
    dw_Telemetry_Safety_ISO13849_PLe: DWORD := 16#00000000; (* 32-Bit Bit-Packed Machine Safety & Guard Interlocks *)
    dw_Telemetry_Hydraulic_DIN_EN_693: DWORD := 16#00000000;(* 32-Bit Bit-Packed Hydraulic Press DIN EN 693 Compliance *)
    dw_Telemetry_Process_Isothermal : DWORD := 16#00000000; (* 32-Bit Bit-Packed Titanium Isothermal Process Telemetry *)
    dw_Telemetry_Alarms_ISA18_2     : DWORD := 16#00000000; (* 32-Bit Bit-Packed ISA-18.2 Trip and Warning Status *)
    dw_Telemetry_FSM_Robotics_OPCUA : DWORD := 16#00000000; (* 32-Bit Bit-Packed FSM Sequence & Vacuum Cell Automation *)
END_VAR

VAR
    (* =========================================================================================================== *)
    (* INTERNAL CONSTANTS & PHYSICAL MODEL COEFFICIENTS                                                            *)
    (* =========================================================================================================== *)
    (* Sellars-Tegart & Ti-6Al-4V Dynamic Recrystallization Parameters *)
    C_R_GAS_CONST_J_MOL_K           : REAL := 8.31446;  (* Universal Molar Gas Constant [J/(mol*K)] *)
    C_Q_ACTIVATION_ENERGY_J_MOL     : REAL := 641000.0; (* Deformation Apparent Activation Energy Ti-6Al-4V [J/mol] *)
    C_ST_ALPHA_INV_MPA              : REAL := 0.0150;   (* Sellars-Tegart Stress Multiplier [MPa^-1] *)
    C_ST_EXPONENT_N                 : REAL := 4.120;    (* Sellars-Tegart Stress Exponent n [-] *)
    C_ST_PRE_EXP_A_S_INV            : REAL := 2.85e12;  (* Sellars-Tegart Kinetic Pre-exponential Factor [s^-1] *)
    C_DRX_BETA                      : REAL := 1.850;    (* Dynamic Recrystallization Avrami Shape Factor [-] *)
    C_DRX_EXPONENT_M                : REAL := 1.450;    (* Dynamic Recrystallization Avrami Growth Exponent [-] *)
    C_INITIAL_GRAIN_SIZE_UM         : REAL := 15.0;     (* Pre-form Initial Equiaxed Alpha Grain Size [um] *)
    C_RAM_MOVING_MASS_KG            : REAL := 450000.0; (* Total Moving Ram & Upper Die Mass (450 metric tons) [kg] *)
    C_OIL_BULK_MODULUS_BAR          : REAL := 16500.0;  (* ISO VG 46 Mineral Hydraulic Oil Bulk Modulus [bar] *)
    C_CYL_BORE_AREA_M2              : REAL := 0.63617;  (* Single Corner Cylinder Piston Cross-Section Area [m2] *)
    C_CYL_TOTAL_AREA_M2             : REAL := 2.54469;  (* 4 Cylinder Combined Piston Cross-Section Area [m2] *)
    C_PLATEN_HALF_SPAN_M            : REAL := 1.750;    (* Half-Span Distance from Press Center to Cylinder Axis [m] *)

    (* =========================================================================================================== *)
    (* 2oo3 TMR VOTING ENGINE INTERNAL PERSISTENCE TIMERS & STATUS                                                 *)
    (* =========================================================================================================== *)
    (* Channel 1: Tonnage [kN] *)
    r_TMR_Tonnage_DiffAB_kN         : REAL := 0.0;
    r_TMR_Tonnage_DiffBC_kN         : REAL := 0.0;
    r_TMR_Tonnage_DiffCA_kN         : REAL := 0.0;
    r_TMR_Tonnage_TimerAB_ms        : REAL := 0.0;
    r_TMR_Tonnage_TimerBC_ms        : REAL := 0.0;
    r_TMR_Tonnage_TimerCA_ms        : REAL := 0.0;
    b_TMR_Tonnage_FaultA            : BOOL := FALSE;
    b_TMR_Tonnage_FaultB            : BOOL := FALSE;
    b_TMR_Tonnage_FaultC            : BOOL := FALSE;
    b_TMR_Tonnage_TotalFailure      : BOOL := FALSE;
    r_TMR_Tonnage_SlewFilt_kN       : REAL := 0.0;

    (* Channel 2: Hydraulic Pressure [bar] *)
    r_TMR_HydPress_DiffAB_bar       : REAL := 0.0;
    r_TMR_HydPress_DiffBC_bar       : REAL := 0.0;
    r_TMR_HydPress_DiffCA_bar       : REAL := 0.0;
    r_TMR_HydPress_TimerAB_ms       : REAL := 0.0;
    r_TMR_HydPress_TimerBC_ms       : REAL := 0.0;
    r_TMR_HydPress_TimerCA_ms       : REAL := 0.0;
    b_TMR_HydPress_FaultA           : BOOL := FALSE;
    b_TMR_HydPress_FaultB           : BOOL := FALSE;
    b_TMR_HydPress_FaultC           : BOOL := FALSE;
    b_TMR_HydPress_TotalFailure     : BOOL := FALSE;
    r_TMR_HydPress_SlewFilt_bar     : REAL := 0.0;

    (* Channel 3: Die Temperature [deg C] *)
    r_TMR_DieTemp_DiffAB_DegC       : REAL := 0.0;
    r_TMR_DieTemp_DiffBC_DegC       : REAL := 0.0;
    r_TMR_DieTemp_DiffCA_DegC       : REAL := 0.0;
    r_TMR_DieTemp_TimerAB_ms        : REAL := 0.0;
    r_TMR_DieTemp_TimerBC_ms        : REAL := 0.0;
    r_TMR_DieTemp_TimerCA_ms        : REAL := 0.0;
    b_TMR_DieTemp_FaultA            : BOOL := FALSE;
    b_TMR_DieTemp_FaultB            : BOOL := FALSE;
    b_TMR_DieTemp_FaultC            : BOOL := FALSE;
    b_TMR_DieTemp_TotalFailure      : BOOL := FALSE;
    r_TMR_DieTemp_SlewFilt_DegC     : REAL := 950.0;

    (* Channel 4: 4-Corner Tilt Skew [um] *)
    r_TMR_TiltSkew_DiffAB_um        : REAL := 0.0;
    r_TMR_TiltSkew_DiffBC_um        : REAL := 0.0;
    r_TMR_TiltSkew_DiffCA_um        : REAL := 0.0;
    r_TMR_TiltSkew_TimerAB_ms       : REAL := 0.0;
    r_TMR_TiltSkew_TimerBC_ms       : REAL := 0.0;
    r_TMR_TiltSkew_TimerCA_ms       : REAL := 0.0;
    b_TMR_TiltSkew_FaultA           : BOOL := FALSE;
    b_TMR_TiltSkew_FaultB           : BOOL := FALSE;
    b_TMR_TiltSkew_FaultC           : BOOL := FALSE;
    b_TMR_TiltSkew_TotalFailure     : BOOL := FALSE;
    r_TMR_TiltSkew_SlewFilt_um      : REAL := 0.0;

    (* =========================================================================================================== *)
    (* DISCRETE 6TH-ORDER STATE-SPACE MODEL & KALMAN INNOVATION FILTER (6x6 A, 6x5 B, 4x6 C, 4x5 D)                 *)
    (* =========================================================================================================== *)
    (* State Vector: x1=Pos [mm], x2=Vel [mm/s], x3=Stress [MPa], x4=GrainSize [um], x5=DieTemp [deg C], x6=Tilt [um] *)
    x_est                           : ARRAY[1..6] OF REAL := [420.0, 0.0, 0.0, 15.0, 950.0, 0.0];
    x_pred                          : ARRAY[1..6] OF REAL := [420.0, 0.0, 0.0, 15.0, 950.0, 0.0];
    x_ref                           : ARRAY[1..6] OF REAL := [65.0, -0.42, 68.0, 8.5, 950.0, 0.0];
    
    (* Control Vector: u1=Pump [%], u2=LevelingFlow [L/min], u3=InductionPower [kW], u4=VacArgon [mbar], u5=Counterbalance [%] *)
    u_cmd                           : ARRAY[1..5] OF REAL := [0.0, 0.0, 0.0, 0.045, 100.0];
    u_prev                          : ARRAY[1..5] OF REAL := [0.0, 0.0, 0.0, 0.045, 100.0];
    
    (* Output Vector: y1=Tonnage [kN], y2=Pressure [bar], y3=DieTemp [deg C], y4=Tilt [um] *)
    y_meas                          : ARRAY[1..4] OF REAL := [0.0, 0.0, 950.0, 0.0];
    y_est                           : ARRAY[1..4] OF REAL := [0.0, 0.0, 950.0, 0.0];
    y_innov                         : ARRAY[1..4] OF REAL := [0.0, 0.0, 0.0, 0.0];
    
    (* Discrete State Transition Matrix A (6x6) *)
    A_mat                           : ARRAY[1..6, 1..6] OF REAL := [
        [ 1.000000,  0.001000,  0.000000,  0.000000,  0.000000,  0.000000 ],
        [ 0.000000,  0.994200, -0.001850,  0.000000,  0.000450, -0.000120 ],
        [ 0.000000,  0.082500,  0.965000, -0.015000, -0.045000,  0.000000 ],
        [ 0.000000, -0.003500, -0.001200,  0.988000,  0.002200,  0.000000 ],
        [ 0.000000,  0.000000,  0.001500,  0.000000,  0.997500,  0.000000 ],
        [ 0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.985000 ]
    ];
    
    (* Discrete Input Matrix B (6x5) *)
    B_mat                           : ARRAY[1..6, 1..5] OF REAL := [
        [  0.000000,  0.000000,  0.000000,  0.000000,  0.000000 ],
        [ -0.008500,  0.000000,  0.000000,  0.000000,  0.004200 ],
        [  0.012500,  0.000000, -0.000850,  0.000000,  0.000000 ],
        [  0.000000,  0.000000,  0.000450,  0.000000,  0.000000 ],
        [  0.000000,  0.000000,  0.003500, -0.012000,  0.000000 ],
        [  0.000000, -0.045000,  0.000000,  0.000000,  0.000000 ]
    ];
    
    (* Discrete Measurement Matrix C (4x6) *)
    C_mat                           : ARRAY[1..4, 1..6] OF REAL := [
        [  0.000000,  0.000000, 1470.588,  0.000000,  0.000000,  0.000000 ],
        [  0.000000,  0.000000,    3.922,  0.000000,  0.000000,  0.000000 ],
        [  0.000000,  0.000000,    0.000,  0.000000,  1.000000,  0.000000 ],
        [  0.000000,  0.000000,    0.000,  0.000000,  0.000000,  1.000000 ]
    ];
    
    (* Discrete Feedthrough Matrix D (4x5) *)
    D_mat                           : ARRAY[1..4, 1..5] OF REAL := [
        [  0.000000,  0.000000,  0.000000,  0.000000,  0.000000 ],
        [  0.000000,  0.000000,  0.000000,  0.000000,  0.000000 ],
        [  0.000000,  0.000000,  0.000000,  0.000000,  0.000000 ],
        [  0.000000,  0.000000,  0.000000,  0.000000,  0.000000 ]
    ];
    
    (* Stationary Kalman Innovation Gain Matrix L (6x4) *)
    L_mat                           : ARRAY[1..6, 1..4] OF REAL := [
        [ 0.0000025,  0.000850,  0.000000,  0.000000 ],
        [ 0.0000150,  0.005200,  0.000000, -0.000045 ],
        [ 0.0005500,  0.185000, -0.002500,  0.000000 ],
        [-0.0000120, -0.004200,  0.000850,  0.000000 ],
        [ 0.0000000,  0.000000,  0.085000,  0.000000 ],
        [ 0.0000000,  0.000000,  0.000000,  0.125000 ]
    ];
    
    (* Kalman Estimation Error Covariance Matrix P_cov (6x6) *)
    P_cov                           : ARRAY[1..6, 1..6] OF REAL := [
        [ 0.025, 0.000, 0.000, 0.000, 0.000, 0.000 ],
        [ 0.000, 0.085, 0.000, 0.000, 0.000, 0.000 ],
        [ 0.000, 0.000, 1.250, 0.000, 0.000, 0.000 ],
        [ 0.000, 0.000, 0.000, 0.045, 0.000, 0.000 ],
        [ 0.000, 0.000, 0.000, 0.000, 0.180, 0.000 ],
        [ 0.000, 0.000, 0.000, 0.000, 0.000, 0.350 ]
    ];
    
    (* Process Noise Covariance Diagonal Q_obs (6x6) *)
    Q_obs_diag                      : ARRAY[1..6] OF REAL := [ 0.0010, 0.0050, 0.2500, 0.0100, 0.0500, 0.0800 ];
    
    (* Measurement Noise Covariance Diagonal R_obs (4x4) *)
    R_obs_diag                      : ARRAY[1..4] OF REAL := [ 25.000, 0.8500, 0.4500, 0.1500 ];

    (* =========================================================================================================== *)
    (* RECEDING-HORIZON MPC OPTIMIZER (N=5 HORIZON, 10 UNROLLED PGD ITERATIONS)                                    *)
    (* =========================================================================================================== *)
    (* Quadratic Penalty Diagonal Matrices Q, R, P, S *)
    Q_diag                          : ARRAY[1..6] OF REAL := [ 0.0050, 150.000, 0.0250, 0.8500, 1.2500, 45.000 ];
    R_diag                          : ARRAY[1..5] OF REAL := [ 0.0080, 0.0150, 0.0025, 5.0000, 0.0120 ];
    P_term                          : ARRAY[1..6] OF REAL := [ 0.0125, 375.000, 0.0625, 2.1250, 3.1250, 112.50 ];
    S_diag                          : ARRAY[1..5] OF REAL := [ 0.0500, 0.1200, 0.0150, 15.000, 0.0800 ];
    
    (* PGD Step Size Alpha and Actuator Box / Slew Bounds *)
    r_PGD_StepSize_Alpha            : REAL := 0.00045;
    u_min                           : ARRAY[1..5] OF REAL := [   0.0, -120.0,    0.0, 0.001,   0.0 ];
    u_max                           : ARRAY[1..5] OF REAL := [ 100.0,  120.0, 1500.0, 1.000, 100.0 ];
    delta_u_max                     : ARRAY[1..5] OF REAL := [   5.0,   15.0,   50.0, 0.050,   8.0 ];
    
    (* MPC Trajectory Arrays over Prediction Horizon k = 0 to 5 *)
    x_traj                          : ARRAY[0..5, 1..6] OF REAL;
    u_traj                          : ARRAY[0..4, 1..5] OF REAL;
    lambda_costate                  : ARRAY[0..5, 1..6] OF REAL;
    grad_u                          : ARRAY[0..4, 1..5] OF REAL;
    u_opt_next                      : ARRAY[1..5] OF REAL := [0.0, 0.0, 0.0, 0.045, 100.0];

    (* =========================================================================================================== *)
    (* 4-CORNER HYDRAULIC LEVELING & CYLINDER GEOMETRIC PARAMETERS                                                 *)
    (* =========================================================================================================== *)
    r_CylForce_FL_kN                : REAL := 0.0;
    r_CylForce_FR_kN                : REAL := 0.0;
    r_CylForce_RL_kN                : REAL := 0.0;
    r_CylForce_RR_kN                : REAL := 0.0;
    r_TotalCylForce_kN              : REAL := 0.0;
    r_EccentricMomentX_kNm          : REAL := 0.0;
    r_EccentricMomentY_kNm          : REAL := 0.0;
    r_CornerTilt_FL_um              : REAL := 0.0;
    r_CornerTilt_FR_um              : REAL := 0.0;
    r_CornerTilt_RL_um              : REAL := 0.0;
    r_CornerTilt_RR_um              : REAL := 0.0;
    r_MaxCornerTiltDev_um           : REAL := 0.0;

    (* =========================================================================================================== *)
    (* 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE VARIABLES                                            *)
    (* =========================================================================================================== *)
    n_FSM_State                     : INT := 1;      (* Active FSM State (1=Furnace Load to 14=Metrology Laser Scan) *)
    n_FSM_StatePrev                 : INT := 0;      (* Previous FSM State for Transition Edge Detection *)
    t_FSM_StateTimer_ms             : REAL := 0.0;   (* Active FSM State Resettable Millisecond Elapsed Timer *)
    b_FSM_StageComplete             : BOOL := FALSE; (* Handshake Flag: Active Step Conditions Fulfilled *)
    b_FSM_StageFault                : BOOL := FALSE; (* Handshake Flag: Step Timeout or Physical Guard Fault *)
    b_FirstScanInit                 : BOOL := TRUE;  (* Cold Boot First Execution Cycle Initialization Latch *)
    r_DecompressStartPress_bar      : REAL := 0.0;   (* Latched Pressure at Start of Active Decompression Ramp *)
    r_ForgingStrokeStartPos_mm      : REAL := 420.0; (* Latched Touch-Down Position for Logarithmic Strain Calc *)

    (* =========================================================================================================== *)
    (* ISA-18.2 MULTI-TIER PROCESS ALARM ENGINES (8 INDEPENDENT CYBER-PHYSICAL MONITORING LOOPS)                  *)
    (* =========================================================================================================== *)
    (* Alarm Loop 1: Main Ram Forging Tonnage Overload [kN] *)
    r_Alm1_Trip_HH_kN               : REAL := 105000.0; (* Emergency Hydraulic Relief Trip Point [kN] *)
    r_Alm1_Trip_H_kN                : REAL := 98000.0;  (* High Warning Tonnage Limit [kN] *)
    r_Alm1_Trip_L_kN                : REAL := 500.0;    (* Low Contact Detection Limit [kN] *)
    r_Alm1_Trip_LL_kN               : REAL := 50.0;     (* Underload Loss of Contact Limit [kN] *)
    r_Alm1_Deadband_kN              : REAL := 500.0;    (* Hysteresis Deadband [kN] *)
    r_Alm1_Timer_HH_ms              : REAL := 0.0;
    r_Alm1_Timer_H_ms               : REAL := 0.0;
    r_Alm1_Timer_L_ms               : REAL := 0.0;
    r_Alm1_Timer_LL_ms              : REAL := 0.0;
    b_Alm1_Active_HH                : BOOL := FALSE;
    b_Alm1_Active_H                 : BOOL := FALSE;
    b_Alm1_Active_L                 : BOOL := FALSE;
    b_Alm1_Active_LL                : BOOL := FALSE;
    b_Alm1_Ack_HH                   : BOOL := FALSE;
    b_Alm1_Ack_H                    : BOOL := FALSE;
    b_Alm1_Ack_L                    : BOOL := FALSE;
    b_Alm1_Ack_LL                   : BOOL := FALSE;

    (* Alarm Loop 2: Hydraulic Main Header Pressure [bar] *)
    r_Alm2_Trip_HH_bar              : REAL := 380.0;    (* High-Pressure Overpressure Relief [bar] *)
    r_Alm2_Trip_H_bar               : REAL := 355.0;    (* High Operating Pressure Warning [bar] *)
    r_Alm2_Trip_L_bar               : REAL := 40.0;     (* Low Hydraulic Standby Pressure [bar] *)
    r_Alm2_Trip_LL_bar              : REAL := 15.0;     (* Severe Loss of Hydraulic Pressure [bar] *)
    r_Alm2_Deadband_bar             : REAL := 3.0;      (* Hysteresis Deadband [bar] *)
    r_Alm2_Timer_HH_ms              : REAL := 0.0;
    r_Alm2_Timer_H_ms               : REAL := 0.0;
    r_Alm2_Timer_L_ms               : REAL := 0.0;
    r_Alm2_Timer_LL_ms              : REAL := 0.0;
    b_Alm2_Active_HH                : BOOL := FALSE;
    b_Alm2_Active_H                 : BOOL := FALSE;
    b_Alm2_Active_L                 : BOOL := FALSE;
    b_Alm2_Active_LL                : BOOL := FALSE;
    b_Alm2_Ack_HH                   : BOOL := FALSE;
    b_Alm2_Ack_H                    : BOOL := FALSE;
    b_Alm2_Ack_L                    : BOOL := FALSE;
    b_Alm2_Ack_LL                   : BOOL := FALSE;

    (* Alarm Loop 3: Upper Die Induction Temperature [deg C] *)
    r_Alm3_Trip_HH_DegC             : REAL := 985.0;    (* Over-Temperature Superalloy Die Anneal Trip [deg C] *)
    r_Alm3_Trip_H_DegC              : REAL := 965.0;    (* High Isothermal Die Temperature Warning [deg C] *)
    r_Alm3_Trip_L_DegC              : REAL := 935.0;    (* Low Isothermal Die Temperature Warning [deg C] *)
    r_Alm3_Trip_LL_DegC             : REAL := 900.0;    (* Under-Temperature Quenching Brittle Trip [deg C] *)
    r_Alm3_Deadband_DegC            : REAL := 2.0;      (* Hysteresis Deadband [deg C] *)
    r_Alm3_Timer_HH_ms              : REAL := 0.0;
    r_Alm3_Timer_H_ms               : REAL := 0.0;
    r_Alm3_Timer_L_ms               : REAL := 0.0;
    r_Alm3_Timer_LL_ms              : REAL := 0.0;
    b_Alm3_Active_HH                : BOOL := FALSE;
    b_Alm3_Active_H                 : BOOL := FALSE;
    b_Alm3_Active_L                 : BOOL := FALSE;
    b_Alm3_Active_LL                : BOOL := FALSE;
    b_Alm3_Ack_HH                   : BOOL := FALSE;
    b_Alm3_Ack_H                    : BOOL := FALSE;
    b_Alm3_Ack_L                    : BOOL := FALSE;
    b_Alm3_Ack_LL                   : BOOL := FALSE;

    (* Alarm Loop 4: 4-Corner Ram Dynamic Leveling Tilt Skew [um] *)
    r_Alm4_Trip_HH_um               : REAL := 45.0;     (* Severe Die Binding / Column Jamming Limit [um] *)
    r_Alm4_Trip_H_um                : REAL := 25.0;     (* High Asymmetric Flash / Skew Warning [um] *)
    r_Alm4_Trip_L_um                : REAL := -25.0;    (* Negative High Asymmetric Skew Warning [um] *)
    r_Alm4_Trip_LL_um               : REAL := -45.0;    (* Severe Negative Jamming Limit [um] *)
    r_Alm4_Deadband_um              : REAL := 2.5;      (* Hysteresis Deadband [um] *)
    r_Alm4_Timer_HH_ms              : REAL := 0.0;
    r_Alm4_Timer_H_ms               : REAL := 0.0;
    r_Alm4_Timer_L_ms               : REAL := 0.0;
    r_Alm4_Timer_LL_ms              : REAL := 0.0;
    b_Alm4_Active_HH                : BOOL := FALSE;
    b_Alm4_Active_H                 : BOOL := FALSE;
    b_Alm4_Active_L                 : BOOL := FALSE;
    b_Alm4_Active_LL                : BOOL := FALSE;
    b_Alm4_Ack_HH                   : BOOL := FALSE;
    b_Alm4_Ack_H                    : BOOL := FALSE;
    b_Alm4_Ack_L                    : BOOL := FALSE;
    b_Alm4_Ack_LL                   : BOOL := FALSE;

    (* Alarm Loop 5: Vacuum Chamber Pressure [mbar] *)
    r_Alm5_Trip_HH_mbar             : REAL := 1.000;    (* Severe Loss of Vacuum - Alpha-Case Oxidation Threat [mbar] *)
    r_Alm5_Trip_H_mbar              : REAL := 0.085;    (* High Vacuum Warning Limit [mbar] *)
    r_Alm5_Trip_L_mbar              : REAL := 0.0001;   (* Ultra-High Vacuum Gauge Lower Sens [mbar] *)
    r_Alm5_Trip_LL_mbar             : REAL := 0.00001;  (* Gauge Sensor Fault [mbar] *)
    r_Alm5_Deadband_mbar            : REAL := 0.005;    (* Hysteresis Deadband [mbar] *)
    r_Alm5_Timer_HH_ms              : REAL := 0.0;
    r_Alm5_Timer_H_ms               : REAL := 0.0;
    r_Alm5_Timer_L_ms               : REAL := 0.0;
    r_Alm5_Timer_LL_ms              : REAL := 0.0;
    b_Alm5_Active_HH                : BOOL := FALSE;
    b_Alm5_Active_H                 : BOOL := FALSE;
    b_Alm5_Active_L                 : BOOL := FALSE;
    b_Alm5_Active_LL                : BOOL := FALSE;
    b_Alm5_Ack_HH                   : BOOL := FALSE;
    b_Alm5_Ack_H                    : BOOL := FALSE;
    b_Alm5_Ack_L                    : BOOL := FALSE;
    b_Alm5_Ack_LL                   : BOOL := FALSE;

    (* Alarm Loop 6: Constitutive Sellars-Tegart Flow Stress [MPa] *)
    r_Alm6_Trip_HH_MPa              : REAL := 180.0;    (* Flow Stress High-High Rupture / Die Cracking [MPa] *)
    r_Alm6_Trip_H_MPa               : REAL := 140.0;    (* High Flow Stress Strain-Rate Too High Warning [MPa] *)
    r_Alm6_Trip_L_MPa               : REAL := 15.0;     (* Low Flow Stress Under-Resistance [MPa] *)
    r_Alm6_Trip_LL_MPa              : REAL := 5.0;      (* Billet Missing or Melted Limit [MPa] *)
    r_Alm6_Deadband_MPa             : REAL := 3.0;      (* Hysteresis Deadband [MPa] *)
    r_Alm6_Timer_HH_ms              : REAL := 0.0;
    r_Alm6_Timer_H_ms               : REAL := 0.0;
    r_Alm6_Timer_L_ms               : REAL := 0.0;
    r_Alm6_Timer_LL_ms              : REAL := 0.0;
    b_Alm6_Active_HH                : BOOL := FALSE;
    b_Alm6_Active_H                 : BOOL := FALSE;
    b_Alm6_Active_L                 : BOOL := FALSE;
    b_Alm6_Active_LL                : BOOL := FALSE;
    b_Alm6_Ack_HH                   : BOOL := FALSE;
    b_Alm6_Ack_H                    : BOOL := FALSE;
    b_Alm6_Ack_L                    : BOOL := FALSE;
    b_Alm6_Ack_LL                   : BOOL := FALSE;

    (* Alarm Loop 7: Titanium Billet Surface Pyrometer [deg C] *)
    r_Alm7_Trip_HH_DegC             : REAL := 980.0;    (* Beta-Transus Microstructure Destruction Trip [deg C] *)
    r_Alm7_Trip_H_DegC              : REAL := 965.0;    (* High Billet Surface Temperature Warning [deg C] *)
    r_Alm7_Trip_L_DegC              : REAL := 930.0;    (* Low Billet Surface Superplastic Loss Warning [deg C] *)
    r_Alm7_Trip_LL_DegC             : REAL := 880.0;    (* Severe Billet Chilling Brittle Forging Abort [deg C] *)
    r_Alm7_Deadband_DegC            : REAL := 2.5;      (* Hysteresis Deadband [deg C] *)
    r_Alm7_Timer_HH_ms              : REAL := 0.0;
    r_Alm7_Timer_H_ms               : REAL := 0.0;
    r_Alm7_Timer_L_ms               : REAL := 0.0;
    r_Alm7_Timer_LL_ms              : REAL := 0.0;
    b_Alm7_Active_HH                : BOOL := FALSE;
    b_Alm7_Active_H                 : BOOL := FALSE;
    b_Alm7_Active_L                 : BOOL := FALSE;
    b_Alm7_Active_LL                : BOOL := FALSE;
    b_Alm7_Ack_HH                   : BOOL := FALSE;
    b_Alm7_Ack_H                    : BOOL := FALSE;
    b_Alm7_Ack_L                    : BOOL := FALSE;
    b_Alm7_Ack_LL                   : BOOL := FALSE;

    (* Alarm Loop 8: Hydraulic Sump Oil Fluid Temperature [deg C] *)
    r_Alm8_Trip_HH_DegC             : REAL := 65.0;     (* Fluid Thermal Breakdown / Pump Cavitation Trip [deg C] *)
    r_Alm8_Trip_H_DegC              : REAL := 55.0;     (* Oil Over-Temperature Chiller Booster Required [deg C] *)
    r_Alm8_Trip_L_DegC              : REAL := 25.0;     (* Cold Viscous Oil Standby Circulation [deg C] *)
    r_Alm8_Trip_LL_DegC             : REAL := 15.0;     (* Cold Oil Start Inhibit Interlock [deg C] *)
    r_Alm8_Deadband_DegC            : REAL := 2.0;      (* Hysteresis Deadband [deg C] *)
    r_Alm8_Timer_HH_ms              : REAL := 0.0;
    r_Alm8_Timer_H_ms               : REAL := 0.0;
    r_Alm8_Timer_L_ms               : REAL := 0.0;
    r_Alm8_Timer_LL_ms              : REAL := 0.0;
    b_Alm8_Active_HH                : BOOL := FALSE;
    b_Alm8_Active_H                 : BOOL := FALSE;
    b_Alm8_Active_L                 : BOOL := FALSE;
    b_Alm8_Active_LL                : BOOL := FALSE;
    b_Alm8_Ack_HH                   : BOOL := FALSE;
    b_Alm8_Ack_H                    : BOOL := FALSE;
    b_Alm8_Ack_L                    : BOOL := FALSE;
    b_Alm8_Ack_LL                   : BOOL := FALSE;

    (* Loop and Matrix Temporary Variables *)
    idx_i                           : INT := 1;
    idx_j                           : INT := 1;
    idx_k                           : INT := 1;
    idx_iter                        : INT := 1;
    r_TmpSum                        : REAL := 0.0;
    r_TmpZ                          : REAL := 0.0;
    r_TmpArg                        : REAL := 0.0;
    r_TmpExp                        : REAL := 0.0;
    r_TmpSqrt                       : REAL := 0.0;
    r_TmpASinh                      : REAL := 0.0;
    r_TmpDeltaU                     : REAL := 0.0;
END_VAR
