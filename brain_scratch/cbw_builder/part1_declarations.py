# part1_declarations.py
# Generates the FB header, documentation, VAR_INPUT, VAR_OUTPUT, and VAR blocks

def get_part1():
    return '''FUNCTION_BLOCK FB_Laundry_ContinuousTunnel_WaterRecycle_Press
(* ==========================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - IEC 61131-3 HIGH-PERFORMANCE STRUCTURED TEXT
 * ARCHITECTURE: CONTINUOUS BATCH TUNNEL WASHER (CBW) & 50-BAR MEMBRANE DEWATERING PRESS
 * SYSTEM: 16-COMPARTMENT TOP-TRANSFER ARCHIMEDEAN SCREW WASHER (2,000 kg/h TEXTILE THROUGHPUT)
 * 
 * CORE SUBSYSTEMS INTEGRATED:
 *  1. Counter-Flow Water Reclamation & Heat Recovery Network with Plate Heat Exchanger (PHE)
 *     and Rotary Greywater Self-Cleaning Drum Filter with Dynamic Differential Pressure Monitoring.
 *  2. Compartment-Wise Direct Saturated Steam Injection (4.5 bar header) with Cavitation Suppression,
 *     Acoustic Noise Dampening, and Dynamic Multi-Zone Temperature Profiling (40°C -> 85°C -> 50°C).
 *  3. 12-Channel Micro-Peristaltic Precision Chemical Dosing Manifold (Caustic Alkali 50%, Surfactant,
 *     Peracetic Acid / Hydrogen Peroxide, Organic Acid Sour, Fabric Softener, Optical Brightener)
 *     with Inductive Toroidal Conductivity Closed-Loop Feedback & Temperature Compensation (25°C ref).
 *  4. 50-Bar High-Pressure Hydraulic Membrane Dewatering Press featuring Dual Proportional Axial Piston
 *     Pumps, Linear Position Transducer (LVDT 0-1500 mm), Dynamic Terzaghi Cake Consolidation Observer,
 *     Darcy Porous Media Drainage Mass Balance, and In-Situ Residual Textile Cake Moisture Estimator.
 *  5. Multi-Axis Automated Shuttle Conveyor Cake Transfer System with Optical Category 4 Light Curtain
 *     Muting Logic, Laser Distance Positioning, and Multi-Bay Industrial Tumbler Dryer Interlocks.
 *  6. Water Recycle Turbidity (Formazin Nephelometric Units [NTU]) & pH Spectrophotometric Quality
 *     Interlocks with Modulating Three-Way Proportional Diverter to Sewage Drain vs Rinse Recovery Tank.
 *  7. Full 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Architecture on 6 Critical Sensor Groups
 *     with Discrepancy Timers, Drift Compensation, and Bumpless Fallback to Dual/Single-Channel Modes.
 *  8. 8-State Discrete State-Space Cyber-Physical Plant Model (x[k+1] = A*x[k] + B*u[k]) with
 *     Receding-Horizon Model Predictive Control (MPC) Quadratic Cost Optimization (Q, R, P Matrices).
 *  9. 12-Stage Deterministic Finite State Machine (FSM) Covering Pre-Fill, Chemical Priming,
 *     Pre-Wash Heating, Counter-Flow Washing, 360-deg Top-Transfer Drum Indexing, Rinse Recovery,
 *     Press Loading, 50-Bar Consolidation, Cake Ejection, Shuttle Dispatch, Greywater CIP Backwash,
 *     and Emergency Press Hydraulic Dump & Saturated Steam Isolation.
 * 10. ISA-18.2 Multi-Tiered Alarm Hierarchy with Configurable Hysteresis Deadbands, Priority
 *     Escalation Timers, and Comprehensive 32-Bit Diagnostic Status Word Serialization.
 * ========================================================================================== *)

VAR_INPUT
    (* Master Operational Supervisory Controls *)
    bEnable                         : BOOL;     (* Master System Enable Supervisory Command [TRUE=Enable, FALSE=Safe Halt] *)
    bReset                          : BOOL;     (* Global System Fault Reset & Latched Alarm Clear Command [pulse] *)
    bAutoMode                       : BOOL;     (* Autonomous Recipe Automation Mode [TRUE=Auto, FALSE=Manual Jog] *)
    bEmergencyStop                  : BOOL;     (* Hardware E-Stop Safety Circuit [FALSE=Active Emergency Stop, TRUE=Healthy] *)
    bStartCycle                     : BOOL;     (* Batch Process Cycle Start Command [pulse] *)
    bTransferPermissive             : BOOL;     (* Downstream Shuttle & Dryer Transfer Permissive Interlock [TRUE=Permitted] *)
    bAckAlarms                      : BOOL;     (* ISA-18.2 Alarm Acknowledgment Command [pulse] *)

    (* Batch Recipe Parameters & Material Specification *)
    rBatchDryWeight_kg              : REAL;     (* Dry Textile Batch Mass Feed [kg] (Nominal 50.0 kg / compartment, range 20.0..75.0) *)
    iBatchRecipeID                  : INT;      (* Active Textile Wash Process Recipe ID [1=Cotton Towels, 2=PolyCotton, 3=Surgical, 4=Delicate] *)
    rTargetMoisture_pct             : REAL;     (* Final Target Residual Textile Moisture Post-Press [%] (Nominal 42.0..48.0) *)
    rTargetPreWashTemp_degC         : REAL;     (* Pre-Wash Zone Temperature Target Setpoint [deg C] (Nominal 38.0..42.0) *)
    rTargetWashTemp_degC            : REAL;     (* Main Wash Core Disinfection Temperature Setpoint [deg C] (Nominal 82.0..88.0) *)
    rTargetRinseTemp_degC           : REAL;     (* Counter-Flow Rinse Water Temperature Setpoint [deg C] (Nominal 48.0..55.0) *)
    rTargetConductivity_uS          : REAL;     (* Main Wash Bath Target Active Alkali Conductivity [uS/cm] (Nominal 11000..14000) *)
    rTargetRinsePH                  : REAL;     (* Final Neutralization Acid Sour Target pH [pH] (Nominal 5.8..6.5) *)

    (* 2oo3 TMR Group 1: Main Wash Core Direct Steam Injection Temperature Transmitters [deg C] *)
    rTemp_MainWash_TE101A           : REAL;     (* Main Wash Steam Zone Temperature Sensor A (RTD Pt100 Class A) [deg C] *)
    rTemp_MainWash_TE101B           : REAL;     (* Main Wash Steam Zone Temperature Sensor B (RTD Pt100 Class A) [deg C] *)
    rTemp_MainWash_TE101C           : REAL;     (* Main Wash Steam Zone Temperature Sensor C (RTD Pt100 Class A) [deg C] *)

    (* 2oo3 TMR Group 2: Greywater Heat Recovery Reclaim Tank Level Transmitters [%] *)
    rLevel_ReclaimTank_LT201A       : REAL;     (* Reclaim Tank Hydrostatic Pressure Level Transmitter A [%] (Range 0.0..100.0) *)
    rLevel_ReclaimTank_LT201B       : REAL;     (* Reclaim Tank Guided Wave Radar Level Transmitter B [%] (Range 0.0..100.0) *)
    rLevel_ReclaimTank_LT201C       : REAL;     (* Reclaim Tank Ultrasonic Pulse Level Transmitter C [%] (Range 0.0..100.0) *)

    (* 2oo3 TMR Group 3: Main Wash Compartment Inductive Toroidal Conductivity Sensors [uS/cm] *)
    rCond_MainWash_AT301A           : REAL;     (* Inductive Conductivity Probe A Main Wash Bath [uS/cm] (Range 0..30000) *)
    rCond_MainWash_AT301B           : REAL;     (* Inductive Conductivity Probe B Main Wash Bath [uS/cm] (Range 0..30000) *)
    rCond_MainWash_AT301C           : REAL;     (* Inductive Conductivity Probe C Main Wash Bath [uS/cm] (Range 0..30000) *)

    (* 2oo3 TMR Group 4: 50-Bar Hydraulic Membrane Dewatering Press Ram Pressure Transducers [bar] *)
    rPress_Hydraulic_PT401A         : REAL;     (* Hydraulic Main Ram Cylinder Pressure Piezo-Resistive Transducer A [bar] (0..60) *)
    rPress_Hydraulic_PT401B         : REAL;     (* Hydraulic Main Ram Cylinder Pressure Piezo-Resistive Transducer B [bar] (0..60) *)
    rPress_Hydraulic_PT401C         : REAL;     (* Hydraulic Main Ram Cylinder Pressure Piezo-Resistive Transducer C [bar] (0..60) *)

    (* 2oo3 TMR Group 5: Plate Heat Exchanger (PHE) Pre-Heated Fresh Water Exit Temperature [deg C] *)
    rTemp_HEX_PHE_TE501A            : REAL;     (* Plate Heat Exchanger Secondary Warm Outlet Temperature A [deg C] *)
    rTemp_HEX_PHE_TE501B            : REAL;     (* Plate Heat Exchanger Secondary Warm Outlet Temperature B [deg C] *)
    rTemp_HEX_PHE_TE501C            : REAL;     (* Plate Heat Exchanger Secondary Warm Outlet Temperature C [deg C] *)

    (* 2oo3 TMR Group 6: Reclaimed Greywater Optical Turbidity Spectrophotometer Probes [NTU] *)
    rTurbidity_Reclaim_AT601A       : REAL;     (* Optical Turbidity Sensor A Reclaimed Water Manifold [NTU] (Range 0..300) *)
    rTurbidity_Reclaim_AT601B       : REAL;     (* Optical Turbidity Sensor B Reclaimed Water Manifold [NTU] (Range 0..300) *)
    rTurbidity_Reclaim_AT601C       : REAL;     (* Optical Turbidity Sensor C Reclaimed Water Manifold [NTU] (Range 0..300) *)

    (* Auxiliary Process Analog Sensors *)
    rTemp_PreWash_degC              : REAL;     (* Pre-Wash Wetting-Out Compartment Temperature [deg C] (Range 15.0..60.0) *)
    rPH_RinseBath                   : REAL;     (* Final Neutralization Rinse Compartment Combination Glass Electrode [pH] (0..14) *)
    rPress_RamPosition_mm           : REAL;     (* Magnetostrictive Linear Position Transducer (Ram Stroke) [mm] (0.0..1500.0) *)
    rPress_Bladder_bar              : REAL;     (* Dewatering Press Rubber Membrane Cushion Internal Water Pressure [bar] (0.0..55.0) *)
    rFlow_PressFiltrate_Lmin        : REAL;     (* Magnetic Flowmeter Measuring Cake Drainage Rate [L/min] (Range 0.0..500.0) *)
    rFlow_FreshWater_m3h            : REAL;     (* Incoming Cold Fresh Water Supply Flowmeter [m3/h] (Range 0.0..30.0) *)
    rPress_SteamHeader_bar          : REAL;     (* Main Direct Steam Supply Header Pressure [bar] (Range 0.0..10.0, Nom 4.5) *)
    rDP_GreywaterFilter_mbar        : REAL;     (* Differential Pressure Across Rotary Drum Screen Filter [mbar] (0.0..800.0) *)
    rDrum_RockingAngle_deg          : REAL;     (* CBW Archimedean Arch Rocking Drum Angular Encoder [deg] (-180.0..+180.0) *)
    rShuttle_Position_mm            : REAL;     (* Laser Distance Meter Shuttle Conveyor Bay Travel Position [mm] (0.0..12000.0) *)

    (* Safety Interlock & Physical Limit Switches *)
    bLightCurtain_Clear             : BOOL;     (* Category 4 Optical Light Curtain Press Shuttle Zone [TRUE=Clear, FALSE=Obstructed] *)
    bPressGuard_Locked              : BOOL;     (* Press Safety Enclosure Solenoid Mechanical Interlock [TRUE=Locked, FALSE=Unlocked] *)
    bShuttleAligned_Dryer           : BOOL;     (* Inductive Proximity Switch Shuttle Docked at Target Dryer Bay [TRUE=Aligned] *)
    bDrumHome_Position              : BOOL;     (* Archimedean Screw Top-Transfer Drum Zero Home Sensor [TRUE=At Zero Index] *)
    bCakeDischarged_Detect          : BOOL;     (* Optical Through-Beam Cake Discharged to Shuttle Conveyor [TRUE=Cake Present] *)
    bMembraneBladder_RuptureSwitch  : BOOL;     (* Differential Pressure Membrane Rupture Safety Sensor [TRUE=Intact, FALSE=Ruptured] *)
    bHEX_HighDP_Switch              : BOOL;     (* Plate Heat Exchanger Severe Fouling High DP Switch [TRUE=Normal, FALSE=High DP] *)
    bEjectionLift_Retracted         : BOOL;     (* Hydraulic Press Cake Bottom Ejection Lifting Plate Home [TRUE=Fully Retracted] *)
    rDeltaTime_s                    : REAL;     (* PLC Task Scan Execution Time Delta [s] (Nominal 0.020 s, 20 ms task cycle) *)
END_VAR

VAR_OUTPUT
    (* Continuous Analog Actuator Command Outputs *)
    rValve_SteamDirect_pct          : REAL;     (* Modulating Saturated Steam Injection Globe Valve Position [%] (0.0..100.0) *)
    rValve_FreshWater_pct           : REAL;     (* Modulating Fresh Makeup Water Valve Position [%] (0.0..100.0) *)
    rPump_ReclaimRecirc_pct         : REAL;     (* Reclaimed Water Counter-Flow Recirculation Pump VFD Speed [%] (0.0..100.0) *)
    rDosing_Alkali_Lmin             : REAL;     (* Peristaltic Pump Command: Sodium Hydroxide 50% [L/min] (0.0..25.0) *)
    rDosing_Detergent_Lmin          : REAL;     (* Peristaltic Pump Command: Non-Ionic Surfactant [L/min] (0.0..15.0) *)
    rDosing_Bleach_Lmin             : REAL;     (* Peristaltic Pump Command: Hydrogen Peroxide / PAA [L/min] (0.0..10.0) *)
    rDosing_AcidSour_Lmin           : REAL;     (* Peristaltic Pump Command: Organic Neutralizing Acid [L/min] (0.0..10.0) *)
    rDosing_Softener_Lmin           : REAL;     (* Peristaltic Pump Command: Cationic Fabric Softener [L/min] (0.0..8.0) *)
    rPress_ProportionalPressure_bar : REAL;     (* 50-Bar Hydraulic Main Ram Proportional Pressure Relief Valve [bar] (0.0..55.0) *)
    rPress_RamSpeed_mms             : REAL;     (* Hydraulic Proportional Flow Valve Ram Advance/Retract Speed [mm/s] (0.0..150.0) *)
    rDrum_DriveSpeed_RPM            : REAL;     (* CBW Archimedean Drum Main Geared Motor VFD Speed [RPM] (0.0..12.0) *)
    rShuttle_Speed_mms              : REAL;     (* Shuttle Cake Traversing Car Servo Drive Speed [mm/s] (0.0..500.0) *)

    (* Discrete Digital Safety & Actuator Solenoids *)
    bValve_EmergencyDump_Open       : BOOL;     (* Hydraulic Press High-Speed Safety Depressurization Slam Valve [TRUE=Dump] *)
    bValve_SteamIsolation_Open      : BOOL;     (* Pneumatic Steam Supply Emergency Isolation Ball Valve [TRUE=Open, FALSE=Shut] *)
    bValve_ReclaimDivertToDrain     : BOOL;     (* 3-Way Reclaim Water Divert: FALSE=Rinse Reclaim Tank, TRUE=Sewer Drain *)
    bPump_GreywaterBackwash_Start   : BOOL;     (* High-Pressure Rotary Drum Screen Backwash Pump Contactor [TRUE=Running] *)
    bPress_BottomPlateLift_Up       : BOOL;     (* Hydraulic Press Cake Bottom Ejection Lifting Cylinder Solenoid [TRUE=Raise] *)
    bPress_PneumaticEjector_Active  : BOOL;     (* Pneumatic Pusher Ram Cake Release Solenoid [TRUE=Active] *)
    bShuttle_TraverseForward        : BOOL;     (* Shuttle Conveyor Traversing Drive Forward Permissive [TRUE=Run Forward] *)
    bShuttle_TraverseReverse        : BOOL;     (* Shuttle Conveyor Traversing Drive Reverse Permissive [TRUE=Run Reverse] *)
    bShuttle_DischargeRollers_Run   : BOOL;     (* Shuttle Conveyor Motorized Belt Discharge Rollers to Dryer [TRUE=Run] *)

    (* Cyber-Physical Observer Status & Key Process Variables *)
    iCurrentState                   : INT;      (* 12-Stage Operational FSM Active State Enumeration [1..12] *)
    sCurrentStateName               : STRING(32);(* Human-Readable Operational State Description *)
    rEstimatedCakeMoisture_pct      : REAL;     (* Dynamic Terzaghi In-Situ Observed Residual Textile Moisture [%] (0.0..100.0) *)
    rObserved_HeatRecovery_kW       : REAL;     (* Real-Time Plate Heat Exchanger Thermal Recovery Power [kW] (0.0..500.0) *)
    rObserved_AlkaliConcentration_pct:REAL;     (* Real-Time Temperature-Compensated Active NaOH Concentration [%] (0.0..15.0) *)
    rObserved_FiltrateTotalVolume_L : REAL;     (* Total Cumulative Expressed Water Volume During Current Press Cycle [L] *)
    rConsolidationRate_pct_s        : REAL;     (* Instantaneous Moisture Expression Rate Derivative [dM/dt, %/s] *)
    rCycleRemainingTime_s           : REAL;     (* Estimated Remaining Wash & Press Cycle Duration [s] *)

    (* ISA-18.2 Alarms & Serialized Status Words *)
    dwSystemStatusWord              : DWORD;    (* Overall Operational & Interlock Bitmask Status Word *)
    dwTMRStatusWord                 : DWORD;    (* 2oo3 Triple Modular Redundancy Channel Health Bitmask *)
    dwISAAlarmWord_Critical         : DWORD;    (* ISA-18.2 Priority 1 Unacknowledged Critical Safety Alarms *)
    dwISAAlarmWord_Warning          : DWORD;    (* ISA-18.2 Priority 2 Warning & Quality Deviation Alarms *)
    dwISAAlarmWord_Advisory         : DWORD;    (* ISA-18.2 Priority 3 Advisory Maintenance & Backwash Alarms *)
    dwActuatorStatusWord            : DWORD;    (* Solenoid & Actuator Output Echo Feedback Bitmask *)
    bAlarm_AnyCritical              : BOOL;     (* Global Critical Safety Alarm Active Flag [TRUE=Emergency Abort] *)
    bAlarm_AnyWarning               : BOOL;     (* Global Warning Alarm Active Flag [TRUE=Quality Degradation] *)
    bCycleComplete                  : BOOL;     (* Wash, Dewater & Cake Dispatch Cycle Successfully Finished [pulse] *)
    bReadyForNextBatch              : BOOL;     (* CBW & Press Empty, Normalized & Ready for Batch Infeed [TRUE=Ready] *)
END_VAR

VAR
    (* ======================================================================================
     * INTERNAL CYBER-PHYSICAL MODELING & DISCRETE STATE-SPACE MATRICES
     * State Vector x[k] (8x1):
     *  x[1] = T_pre   : Pre-Wash Zone Average Temperature [deg C] (Nominal 40.0)
     *  x[2] = T_main1 : Main Wash Zone 1 Temperature [deg C] (Nominal 85.0)
     *  x[3] = T_main2 : Main Wash Zone 2 Disinfection Temperature [deg C] (Nominal 85.0)
     *  x[4] = T_rinse : Counter-Flow Rinse Water Temperature [deg C] (Nominal 50.0)
     *  x[5] = L_rec   : Greywater Heat Recovery Reclaim Tank Level [%] (Nominal 65.0)
     *  x[6] = K_wash  : Wash Bath Active Inductive Conductivity [uS/cm] (Nominal 12500.0)
     *  x[7] = Z_ram   : Hydraulic Dewatering Press Ram Displacement [mm] (0.0..1500.0)
     *  x[8] = M_cake  : Textile Cake Moisture Percentage [%] (220.0% wet -> 42.0% pressed)
     *
     * Input Control Vector u[k] (6x1):
     *  u[1] = V_steam : Saturated Direct Steam Injection Valve Command [%] (0.0..100.0)
     *  u[2] = V_fresh : Fresh Water Make-Up Valve Command [%] (0.0..100.0)
     *  u[3] = N_rec   : Reclaimed Counterflow Recirculation Pump Speed [%] (0.0..100.0)
     *  u[4] = F_alk   : Caustic Alkali Dosing Pump Flow [L/min] (0.0..25.0)
     *  u[5] = F_sour  : Acid Sour Neutralizing Pump Flow [L/min] (0.0..10.0)
     *  u[6] = P_hyd   : Hydraulic Membrane Press Target Pressure [bar] (0.0..55.0)
     * ====================================================================================== *)
    matA : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Transition Matrix (Ts = 0.020 s) *)
    matB : ARRAY[1..8, 1..6] OF REAL; (* Discrete Control Input Matrix *)
    matC : ARRAY[1..8, 1..8] OF REAL; (* Output Measurement Matrix *)
    matD : ARRAY[1..8, 1..6] OF REAL; (* Direct Feedthrough Disturbance Matrix *)

    x_state         : ARRAY[1..8] OF REAL; (* Current State Vector x[k] *)
    x_prev          : ARRAY[1..8] OF REAL; (* Previous Step State Vector x[k-1] *)
    x_pred          : ARRAY[1..8] OF REAL; (* One-Step AHEAD Predicted State Vector x[k+1|k] *)
    y_meas          : ARRAY[1..8] OF REAL; (* Measured Output Vector from Voted Sensors *)
    y_est           : ARRAY[1..8] OF REAL; (* Model Estimated Output Vector *)
    x_err           : ARRAY[1..8] OF REAL; (* State Estimation / Tracking Error Vector *)
    u_ctrl          : ARRAY[1..6] OF REAL; (* Active Control Action Vector u[k] *)
    u_prev          : ARRAY[1..6] OF REAL; (* Previous Step Control Vector u[k-1] *)
    u_delta         : ARRAY[1..6] OF REAL; (* Slew Delta Vector du[k] = u[k] - u[k-1] *)
    rKalmanGain     : ARRAY[1..8] OF REAL; (* Diagonal Luenberger Observer / Kalman Gains *)

    (* Model Predictive Control (MPC) Cost Weight Matrices & Horizons *)
    matQ            : ARRAY[1..8, 1..8] OF REAL; (* State Error Penalty Matrix Q (Diagonal) *)
    matR            : ARRAY[1..6, 1..6] OF REAL; (* Control Actuation Effort Penalty Matrix R *)
    matP            : ARRAY[1..8, 1..8] OF REAL; (* Terminal State Cost Matrix P (Lyapunov Riccati Solution) *)
    rMpcGradient    : ARRAY[1..6] OF REAL;       (* Instantaneous Cost Function Gradient Vector dJ/du *)
    rMpcStepSize    : REAL;                      (* Projected Gradient Descent Learning Rate *)
    iMpcIter        : INT;                       (* Active Optimization Iteration Index *)

    (* 2oo3 Triple Modular Redundancy (TMR) Structures (6 Sensor Groups) *)
    (* TMR Group 1: Main Wash Zone Temperature Probes *)
    rTMR1_DiffAB            : REAL; (* |TE101A - TE101B| [deg C] *)
    rTMR1_DiffBC            : REAL; (* |TE101B - TE101C| [deg C] *)
    rTMR1_DiffCA            : REAL; (* |TE101C - TE101A| [deg C] *)
    tTMR1_TimerA            : REAL; (* Sensor A Discrepancy Persistence Timer [s] *)
    tTMR1_TimerB            : REAL; (* Sensor B Discrepancy Persistence Timer [s] *)
    tTMR1_TimerC            : REAL; (* Sensor C Discrepancy Persistence Timer [s] *)
    bTMR1_FaultA            : BOOL; (* Channel A Latched Discrepancy Fault *)
    bTMR1_FaultB            : BOOL; (* Channel B Latched Discrepancy Fault *)
    bTMR1_FaultC            : BOOL; (* Channel C Latched Discrepancy Fault *)
    rTMR1_VotedVal          : REAL; (* Synthesized 2oo3 Voted Temperature [deg C] *)
    iTMR1_HealthGrade       : INT;  (* Health: 3=Triple, 2=Dual Fallback, 1=Single Degraded, 0=Critical Fail *)

    (* TMR Group 2: Reclaim Tank Level Transmitters *)
    rTMR2_DiffAB            : REAL; (* |LT201A - LT201B| [%] *)
    rTMR2_DiffBC            : REAL; (* |LT201B - LT201C| [%] *)
    rTMR2_DiffCA            : REAL; (* |LT201C - LT201A| [%] *)
    tTMR2_TimerA            : REAL; (* Sensor A Discrepancy Timer [s] *)
    tTMR2_TimerB            : REAL; (* Sensor B Discrepancy Timer [s] *)
    tTMR2_TimerC            : REAL; (* Sensor C Discrepancy Timer [s] *)
    bTMR2_FaultA            : BOOL; (* Channel A Fault *)
    bTMR2_FaultB            : BOOL; (* Channel B Fault *)
    bTMR2_FaultC            : BOOL; (* Channel C Fault *)
    rTMR2_VotedVal          : REAL; (* Synthesized 2oo3 Voted Level [%] *)
    iTMR2_HealthGrade       : INT;

    (* TMR Group 3: Main Wash Bath Inductive Conductivity *)
    rTMR3_DiffAB            : REAL; (* |AT301A - AT301B| [uS/cm] *)
    rTMR3_DiffBC            : REAL; (* |AT301B - AT301C| [uS/cm] *)
    rTMR3_DiffCA            : REAL; (* |AT301C - AT301A| [uS/cm] *)
    tTMR3_TimerA            : REAL; (* Sensor A Discrepancy Timer [s] *)
    tTMR3_TimerB            : REAL; (* Sensor B Discrepancy Timer [s] *)
    tTMR3_TimerC            : REAL; (* Sensor C Discrepancy Timer [s] *)
    bTMR3_FaultA            : BOOL; (* Channel A Fault *)
    bTMR3_FaultB            : BOOL; (* Channel B Fault *)
    bTMR3_FaultC            : BOOL; (* Channel C Fault *)
    rTMR3_VotedVal          : REAL; (* Synthesized 2oo3 Voted Conductivity [uS/cm] *)
    iTMR3_HealthGrade       : INT;

    (* TMR Group 4: 50-Bar Hydraulic Press Pressure Transducers *)
    rTMR4_DiffAB            : REAL; (* |PT401A - PT401B| [bar] *)
    rTMR4_DiffBC            : REAL; (* |PT401B - PT401C| [bar] *)
    rTMR4_DiffCA            : REAL; (* |PT401C - PT401A| [bar] *)
    tTMR4_TimerA            : REAL; (* Sensor A Discrepancy Timer [s] *)
    tTMR4_TimerB            : REAL; (* Sensor B Discrepancy Timer [s] *)
    tTMR4_TimerC            : REAL; (* Sensor C Discrepancy Timer [s] *)
    bTMR4_FaultA            : BOOL; (* Channel A Fault *)
    bTMR4_FaultB            : BOOL; (* Channel B Fault *)
    bTMR4_FaultC            : BOOL; (* Channel C Fault *)
    rTMR4_VotedVal          : REAL; (* Synthesized 2oo3 Voted Hydraulic Pressure [bar] *)
    iTMR4_HealthGrade       : INT;

    (* TMR Group 5: Plate Heat Exchanger Outlet Temperature *)
    rTMR5_DiffAB            : REAL; (* |TE501A - TE501B| [deg C] *)
    rTMR5_DiffBC            : REAL; (* |TE501B - TE501C| [deg C] *)
    rTMR5_DiffCA            : REAL; (* |TE501C - TE501A| [deg C] *)
    tTMR5_TimerA            : REAL; (* Sensor A Discrepancy Timer [s] *)
    tTMR5_TimerB            : REAL; (* Sensor B Discrepancy Timer [s] *)
    tTMR5_TimerC            : REAL; (* Sensor C Discrepancy Timer [s] *)
    bTMR5_FaultA            : BOOL; (* Channel A Fault *)
    bTMR5_FaultB            : BOOL; (* Channel B Fault *)
    bTMR5_FaultC            : BOOL; (* Channel C Fault *)
    rTMR5_VotedVal          : REAL; (* Synthesized 2oo3 Voted Outlet Temp [deg C] *)
    iTMR5_HealthGrade       : INT;

    (* TMR Group 6: Reclaimed Water Turbidity Optical Analyzers *)
    rTMR6_DiffAB            : REAL; (* |AT601A - AT601B| [NTU] *)
    rTMR6_DiffBC            : REAL; (* |AT601B - AT601C| [NTU] *)
    rTMR6_DiffCA            : REAL; (* |AT601C - AT601A| [NTU] *)
    tTMR6_TimerA            : REAL; (* Sensor A Discrepancy Timer [s] *)
    tTMR6_TimerB            : REAL; (* Sensor B Discrepancy Timer [s] *)
    tTMR6_TimerC            : REAL; (* Sensor C Discrepancy Timer [s] *)
    bTMR6_FaultA            : BOOL; (* Channel A Fault *)
    bTMR6_FaultB            : BOOL; (* Channel B Fault *)
    bTMR6_FaultC            : BOOL; (* Channel C Fault *)
    rTMR6_VotedVal          : REAL; (* Synthesized 2oo3 Voted Turbidity [NTU] *)
    iTMR6_HealthGrade       : INT;

    (* Terzaghi Cake Consolidation & Darcy Porous Media Parameters *)
    rCake_InitialMoisture   : REAL; (* Starting Moisture Content Prior to Pressing [%] (Nom 220.0) *)
    rCake_CurrentMoisture   : REAL; (* Instantaneous In-Situ Observed Moisture [%] *)
    rCake_WaterMass_kg      : REAL; (* Current Residual Mass of Water Inside Cake [kg] *)
    rCake_FiltrateVol_L     : REAL; (* Cumulative Filtrate Runoff Volume [L] *)
    rCake_Permeability_m2   : REAL; (* Specific Dynamic Textile Permeability [m2] *)
    rCake_SpecificResistance: REAL; (* Specific Cake Resistance alpha [m/kg] *)
    rCake_ConsolidationCoeff: REAL; (* Terzaghi Consolidation Coefficient Cv [m2/s] *)
    rCake_CompressionStrain : REAL; (* Ram Displacement Strain Epsilon = (Z0 - Z) / Z0 *)
    rCake_InitialHeight_mm  : REAL; (* Uncompressed Wet Textile Cake Height in Basket [mm] (Nom 850.0) *)
    rCake_FiltrateFlow_Lps  : REAL; (* Expressed Pore Water Drainage Rate [L/s] *)

    (* Plate Heat Exchanger (PHE) Thermodynamic Heat Balance Variables *)
    rPHE_HotInletTemp_degC  : REAL; (* Effluent Greywater Entering Heat Exchanger [deg C] *)
    rPHE_HotOutletTemp_degC : REAL; (* Effluent Greywater Leaving Heat Exchanger [deg C] *)
    rPHE_ColdInletTemp_degC : REAL; (* Cold Fresh Water Entering Heat Exchanger [deg C] *)
    rPHE_ColdOutletTemp_degC: REAL; (* Pre-Heated Rinse Fresh Water Leaving [deg C] *)
    rPHE_DeltaT1            : REAL; (* Hot In - Cold Out Approach Temperature [deg C] *)
    rPHE_DeltaT2            : REAL; (* Hot Out - Cold In Approach Temperature [deg C] *)
    rPHE_LMTD               : REAL; (* Log Mean Temperature Difference [deg C] *)
    rPHE_HeatTransfer_kW    : REAL; (* Recovered Thermal Duty [kW] *)
    rPHE_HeatTransferCoeff_U: REAL; (* Dynamic Overall Heat Transfer Coefficient U [W/(m2*K)] *)
    rPHE_FoulingResistance  : REAL; (* Calculated Plate Scaling/Lint Fouling Factor Rf [(m2*K)/W] *)
    rPHE_CleanU_Benchmark   : REAL; (* Clean Baseline Plate Heat Transfer Coefficient [W/(m2*K)] *)

    (* Inductive Conductivity Temperature Compensation & Active Alkali Modeling *)
    rCond_RefTemp_degC      : REAL; (* Standard Reference Temperature (25.0 deg C) *)
    rCond_TempCoeff_pct_K   : REAL; (* Non-Linear Temperature Coefficient Alpha [%/K] (Nom 2.15) *)
    rCond_Normalized_uS     : REAL; (* Temperature-Compensated Conductivity at 25.0 deg C [uS/cm] *)
    rAlkali_Concentration_wt: REAL; (* Calculated Active Sodium Hydroxide Weight Percentage [wt%] *)

    (* 12-Channel Peristaltic Dosing Manifold Tube Wear & Fatigue Tracking *)
    rPeristaltic_TotalRev   : ARRAY[1..12] OF REAL; (* Cumulative Rotor Revolutions per Channel [rev] *)
    rPeristaltic_Volume_L   : ARRAY[1..12] OF REAL; (* Cumulative Chemical Pumped Volume [L] *)
    rPeristaltic_WearRatio  : ARRAY[1..12] OF REAL; (* Normalized Tube Elastomer Fatigue Index (0.0=New, 1.0=Exhausted) *)
    rPeristaltic_MaxRevLife : REAL;                 (* Rated Rotor Revolutions to Tube Rupture [rev] (Nom 5000000.0) *)

    (* 12-Stage Operational Finite State Machine Variables *)
    iState                  : INT;  (* Active FSM State Code [1..12] *)
    iPrevState              : INT;  (* Previous Step FSM State Code *)
    tStateTimer_s           : REAL; (* State Residence Time Elapsed [s] *)
    tCycleTotalTimer_s      : REAL; (* Total Batch Cycle Duration Timer [s] *)
    bStateFirstScan         : BOOL; (* First Scan Flag for State Entry Transition *)
    bStateTransitionPermit  : BOOL; (* Permissive Check Flag Prior to Indexing Next State *)
    iDrumOscillationCount   : INT;  (* Completed Rocking Cycles During Main Wash Phase *)
    bDrumRockingDirection   : BOOL; (* Active Rocking Direction: FALSE=Clockwise, TRUE=Counter-Clockwise *)
    rDrumTargetAngle_deg    : REAL; (* Instantaneous Commanded Rocking Angle Setpoint [deg] *)

    (* 50-Bar Hydraulic Membrane Press Profile & Shuttle Interlocks *)
    rPress_TargetPressure   : REAL; (* Dynamic Target Pressure Profile Command [bar] *)
    rPress_RampRate_bar_s   : REAL; (* Active Pressure Slew Ramp Rate [bar/s] *)
    rPress_Decompress_bar_s : REAL; (* Controlled Depressurization Rate [bar/s] *)
    iPressSubPhase          : INT;  (* Press Sub-Sequence: 1=Settle, 2=Bulk Consolidation, 3=Membrane 50-Bar, 4=Hold, 5=Vent *)
    tPressPhaseTimer_s      : REAL; (* Dwell Timer Inside Active Press Sub-Phase [s] *)
    bShuttleTargetBayOK     : BOOL; (* Interlock: Target Dryer Bay Door Open & Ready to Receive Cake *)
    rShuttle_TargetPos_mm   : REAL; (* Assigned Dryer Bay Target Traverse Coordinate [mm] *)

    (* ISA-18.2 Multi-Tiered Alarm Engine Structure *)
    (* Alarm Threshold Constants with Hysteresis Deadbands *)
    rHydraulicPress_HH_Trip : REAL; (* 53.0 bar : Safety Slam Dump Trip *)
    rHydraulicPress_H_Trip  : REAL; (* 48.0 bar : Hydraulic Warning High *)
    rHydraulicPress_Deadband: REAL; (*  1.5 bar : Hysteresis Clearance Deadband *)
    rWashTemp_HH_Trip       : REAL; (* 93.0 deg C: Severe Boiling & Cavitation Overheat *)
    rWashTemp_H_Trip        : REAL; (* 88.0 deg C: High Wash Temperature Warning *)
    rWashTemp_L_Trip        : REAL; (* 72.0 deg C: Disinfection Temperature Underheat *)
    rWashTemp_LL_Trip       : REAL; (* 45.0 deg C: Critical Steam Loss *)
    rWashTemp_Deadband      : REAL; (*  1.5 deg C: Temperature Deadband *)
    rReclaimLvl_HH_Trip     : REAL; (* 95.0 %: Tank Overflow Prevention *)
    rReclaimLvl_H_Trip      : REAL; (* 88.0 %: Tank High Warning *)
    rReclaimLvl_L_Trip      : REAL; (* 25.0 %: Recirculation Low Warning *)
    rReclaimLvl_LL_Trip     : REAL; (* 10.0 %: Pump Cavitation Low Cutoff *)
    rReclaimLvl_Deadband    : REAL; (*  2.0 %: Level Deadband *)
    rTurbidity_Severe_Trip  : REAL; (* 150.0 NTU: Quality Limit Auto Sewer Divert *)
    rTurbidity_High_Trip    : REAL; (*  80.0 NTU: Filter Backwash Warning *)
    rTurbidity_Deadband     : REAL; (*   5.0 NTU: Turbidity Deadband *)

    (* Alarm Debounce Timers & Escalation Tracking *)
    tAlarmTimer_PressHH     : REAL; (* Hydraulic Overpressure Trip Delay Accumulator [s] *)
    tAlarmTimer_TempHH      : REAL; (* Temperature Overheat Trip Delay Accumulator [s] *)
    tAlarmTimer_TempLL      : REAL; (* Disinfection Failure Delay Accumulator [s] *)
    tAlarmTimer_LvlHH       : REAL; (* Reclaim Tank Overflow Delay Accumulator [s] *)
    tAlarmTimer_LvlLL       : REAL; (* Reclaim Tank Low Delay Accumulator [s] *)
    tAlarmTimer_TurbidityHH : REAL; (* Severe Turbidity Delay Accumulator [s] *)
    tAlarmTimer_BladderDiff : REAL; (* Membrane Bladder Rupture Differential Delay [s] *)

    (* Actuator Slew-Rate Filters & Clamping Limits *)
    rValve_Steam_SlewLimit  : REAL; (* Saturated Steam Valve Maximum Slew Rate [%/s] (Nom 10.0) *)
    rPress_Hyd_SlewLimit    : REAL; (* Hydraulic Proportional Relief Maximum Slew Rate [bar/s] (Nom 15.0) *)
    rValve_Steam_Filtered   : REAL; (* First-Order Lag Filtered Steam Valve Command [%] *)
    rPress_Hyd_Filtered     : REAL; (* First-Order Lag Filtered Hydraulic Pressure Command [bar] *)
    rDosing_Alkali_Filtered : REAL; (* Slew-Rate Limited Alkali Command [L/min] *)
    rDosing_Acid_Filtered   : REAL; (* Slew-Rate Limited Sour Acid Command [L/min] *)
    iLoopIndexI             : INT;  (* Generic Inner Matrix Iteration Index *)
    iLoopIndexJ             : INT;  (* Generic Outer Matrix Iteration Index *)
    iLoopIndexK             : INT;  (* Generic Vector Iteration Index *)
    rTempSum                : REAL; (* Accumulator Float for Inner Product Math *)
    rTempMin                : REAL; (* Temporary Scalar for Bounding & Median Math *)
    rTempMax                : REAL; (* Temporary Scalar for Bounding & Median Math *)
    bInitialized            : BOOL; (* First Scan Cold Initialization Complete Flag *)
END_VAR
'''

if __name__ == "__main__":
    p1 = get_part1()
    print(f"Part 1 length: {len(p1)} characters")
