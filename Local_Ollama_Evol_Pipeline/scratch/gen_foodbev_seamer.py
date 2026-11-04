# Full generator script for FB_FoodBev_AsepticCanning_DoubleSeamer_LeakInspect
import os
import sys
import re
import uuid
import json

# Ensure Local_Ollama_Evol_Pipeline/scripts is in sys.path for linter
sys.path.insert(0, os.path.abspath("Local_Ollama_Evol_Pipeline/scripts"))
try:
    from linter import ST_Linter
    print("Successfully imported ST_Linter")
except Exception as e:
    print(f"Linter import note: {e}")

code_blocks = []

# --- PART 1: HEADER & VAR DECLARATIONS ---
part1 = """FUNCTION_BLOCK FB_FoodBev_AsepticCanning_DoubleSeamer_LeakInspect
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
COMMERCIAL FOOD & BEVERAGE DIVISION - ASEPTIC ROTARY BEVERAGE CANNING SYSTEM
========================================================================================================================
SYSTEM SPECIFICATION:
  - Machine Architecture: Ultra-High-Speed (90,000 CPH / 1,500 cans/min) Continuous Rotary Aseptic Beverage Canning Line.
  - Seamer Kinematics: 18-Station Twin-Turret Electronic Camming Hermetic Double-Seamer with independent servomotor
    actuation for 1st Operation Roll radial positioning and 2nd Operation Roll hermetic crimping.
  - Cryogenic Dosing: In-Seam Liquid Nitrogen (LN2) Inert Micro-Dosing System injecting sub-cooled cryogenic liquid
    nitrogen (-196 deg C) into the can headspace immediately prior to end seam positioning (generating internal
    pressurization of 1.5 to 2.5 bar for container wall hoop stress rigidity and O2 displacement < 0.05 ppm).
  - Quality & Leak Inspection: In-Line 360-Degree Acoustic Tap Resonance Impulse Analysis and High-Speed Eddy-Current
    Hermetic Leak Detection with sub-2-millisecond electro-pneumatic reject gate actuation.
  - Microbiological Barrier: Closed Isolator Chamber with Vaporized Peracetic Acid (PAA, 1,500 ppm) sterilization
    and ISO Class 5 laminar sterile air barrier overpressure (+45 Pa).
  - Regulatory Standards: FDA 21 CFR Part 113 (Thermally Processed Low-Acid Foods Packaged in Hermetically Sealed
    Containers), EHEDG Type EL Class I Aseptic Standards, ISO 13849-1 Safety Integrity Level SIL 3 / PL e.
  - Cyber-Physical Core:
    * Full 8x8 discrete state-space formulation at 250 microsecond execution cycle: x[k+1] = A*x[k] + B*u[k].
    * Receding-Horizon Model Predictive Control (MPC) quadratic cost optimization with Q, R, S, P weighting matrices.
    * 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) on all critical sensor trios with discrepancy timers.
    * ISA-18.2 Multi-Tiered Alarm Hierarchy with deadband hysteresis, rate-of-change, and packed diagnostic words.
    * 12-State Finite State Machine (FSM) governing full aseptic lifecycle from PAA SIP to synchronous production.
========================================================================================================================
*)
VAR_INPUT
    (* Master Automation Supervisory Permissives & Safety Interlocks *)
    bMasterLineRunPermissive          : BOOL := FALSE;    (* Global Canning Line Master Run Permissive [BOOL] *)
    bEmergencyStopCircuit_NC          : BOOL := TRUE;     (* Dual-Channel Safety E-Stop Circuit Normally Closed [BOOL] *)
    bAsepticIsolatorDoorInterlock_NC  : BOOL := TRUE;     (* Isolator Access Door Safety Interlock NC [BOOL] *)
    bResetFaultLatches                : BOOL := FALSE;    (* Master Fault Reset and Latched Alarm Acknowledge [BOOL] *)
    bCIP_SIP_ModePermissive           : BOOL := FALSE;    (* Clean-in-Place / Sterilization Mode Permissive [BOOL] *)
    bDryCycleMotionCheckMode          : BOOL := FALSE;    (* Mechanical Dry-Cycle Test Permissive (No Cans/LN2) [BOOL] *)
    bCanPresenceInfeedStarwheel       : BOOL := FALSE;    (* High-Speed Optical Proximity Sensor Can Infeed [BOOL] *)
    bLidPresenceCapChute              : BOOL := FALSE;    (* Fiber-Optic Lid/Cap Detection at Seaming Chuck [BOOL] *)

    (* 2oo3 Triple Modular Redundancy (TMR): 1st Operation Seaming Roll Load Cells [N] *)
    WT_SEAM_ROLL_1ST_OP_FORCE_101A    : REAL := 320.0;    (* 1st Operation Roll Radial Force Channel A [N] *)
    WT_SEAM_ROLL_1ST_OP_FORCE_101B    : REAL := 320.0;    (* 1st Operation Roll Radial Force Channel B [N] *)
    WT_SEAM_ROLL_1ST_OP_FORCE_101C    : REAL := 320.0;    (* 1st Operation Roll Radial Force Channel C [N] *)

    (* 2oo3 Triple Modular Redundancy (TMR): 2nd Operation Seaming Roll Load Cells [N] *)
    WT_SEAM_ROLL_2ND_OP_FORCE_102A    : REAL := 680.0;    (* 2nd Operation Roll Radial Force Channel A [N] *)
    WT_SEAM_ROLL_2ND_OP_FORCE_102B    : REAL := 680.0;    (* 2nd Operation Roll Radial Force Channel B [N] *)
    WT_SEAM_ROLL_2ND_OP_FORCE_102C    : REAL := 680.0;    (* 2nd Operation Roll Radial Force Channel C [N] *)

    (* 2oo3 Triple Modular Redundancy (TMR): Rotary Turret Dual-Resolver Angular Pos [deg] *)
    ST_TURRET_RESOLVER_POS_201A       : REAL := 0.0;      (* Turret Master Resolver Angular Position Ch A [deg] *)
    ST_TURRET_RESOLVER_POS_201B       : REAL := 0.0;      (* Turret Master Resolver Angular Position Ch B [deg] *)
    ST_TURRET_RESOLVER_POS_201C       : REAL := 0.0;      (* Turret Master Resolver Angular Position Ch C [deg] *)

    (* 2oo3 Triple Modular Redundancy (TMR): Cryogenic Liquid Nitrogen (LN2) Micro-Dose Mass [mg] *)
    FT_LN2_MICRODOSE_MASS_301A        : REAL := 45.0;     (* LN2 Cryogenic Mass Dosed Per Can Channel A [mg] *)
    FT_LN2_MICRODOSE_MASS_301B        : REAL := 45.0;     (* LN2 Cryogenic Mass Dosed Per Can Channel B [mg] *)
    FT_LN2_MICRODOSE_MASS_301C        : REAL := 45.0;     (* LN2 Cryogenic Mass Dosed Per Can Channel C [mg] *)

    (* 2oo3 Triple Modular Redundancy (TMR): Can Acoustic Tap Resonance Sensor [bar / Hz] *)
    PT_CAN_ACOUSTIC_TAP_PRESSURE_401A : REAL := 1.85;     (* Tap Peak Resonant Pressure Estimation Ch A [bar] *)
    PT_CAN_ACOUSTIC_TAP_PRESSURE_401B : REAL := 1.85;     (* Tap Peak Resonant Pressure Estimation Ch B [bar] *)
    PT_CAN_ACOUSTIC_TAP_PRESSURE_401C : REAL := 1.85;     (* Tap Peak Resonant Pressure Estimation Ch C [bar] *)
    rAcousticResonantFreq_ChA         : REAL := 3250.0;   (* Acoustic FFT Peak Natural Frequency Ch A [Hz] *)
    rAcousticResonantFreq_ChB         : REAL := 3250.0;   (* Acoustic FFT Peak Natural Frequency Ch B [Hz] *)
    rAcousticResonantFreq_ChC         : REAL := 3250.0;   (* Acoustic FFT Peak Natural Frequency Ch C [Hz] *)

    (* 2oo3 Triple Modular Redundancy (TMR): Vaporized PAA Isolator Concentration [ppm] *)
    ZT_CHAMBER_PAA_CONC_501A          : REAL := 1500.0;   (* Peracetic Acid Vapor Concentration Ch A [ppm] *)
    ZT_CHAMBER_PAA_CONC_501B          : REAL := 1500.0;   (* Peracetic Acid Vapor Concentration Ch B [ppm] *)
    ZT_CHAMBER_PAA_CONC_501C          : REAL := 1500.0;   (* Peracetic Acid Vapor Concentration Ch C [ppm] *)

    (* 2oo3 Triple Modular Redundancy (TMR): Sterile Air Isolator Differential Overpressure [Pa] *)
    PT_STERILE_AIR_OVERPRESSURE_601A  : REAL := 45.0;     (* Sterile Isolator Positive Pressure Ch A [Pa] *)
    PT_STERILE_AIR_OVERPRESSURE_601B  : REAL := 45.0;     (* Sterile Isolator Positive Pressure Ch B [Pa] *)
    PT_STERILE_AIR_OVERPRESSURE_601C  : REAL := 45.0;     (* Sterile Isolator Positive Pressure Ch C [Pa] *)

    (* 2oo3 Triple Modular Redundancy (TMR): Seaming Chuck Ceramic Hybrid Bearings Temp [deg C] *)
    TT_SEAM_CHUCK_BEARING_701A        : REAL := 38.5;     (* Seaming Chuck High-Speed Bearing Temp Ch A [deg C] *)
    TT_SEAM_CHUCK_BEARING_701B        : REAL := 38.5;     (* Seaming Chuck High-Speed Bearing Temp Ch B [deg C] *)
    TT_SEAM_CHUCK_BEARING_701C        : REAL := 38.5;     (* Seaming Chuck High-Speed Bearing Temp Ch C [deg C] *)

    (* Dynamic Machine Kinematics & Line Telemetry *)
    rTurretMasterVelocity_RPM         : REAL := 83.33;    (* Turret Rotary Angular Velocity (83.33 RPM = 1,500 CPM) [RPM] *)
    rCanInfeedPitchRate_CPH           : REAL := 90000.0;  (* Continuous Infeed Production Rate [cans/h] *)
    rLifterTableActualBaseForce_N     : REAL := 1150.0;   (* Can Elevator Lifter Spring/Pneumatic Base Force [N] *)
    rInfeedScrewServoVelocity_RPM     : REAL := 250.0;    (* Progressive Infeed Metering Screw Speed [RPM] *)
    rLN2SupplyHeaderPressure_bar      : REAL := 3.20;     (* Cryogenic Manifold Header Liquid Pressure [bar] *)
    rLN2SupplyHeaderTemp_Kelvin       : REAL := 77.36;    (* Cryogenic Sub-Cooler Temperature [K] *)

    (* Engineering Recipe Parameters & Critical Quality Attributes (CQA) *)
    rSet_CanNominalDiameter_mm        : REAL := 52.00;    (* Can Body External Flange Diameter [mm] *)
    rSet_SeamNominalThickness_mm      : REAL := 1.020;    (* Target Completed Double-Seam Thickness [mm] *)
    rSet_SeamNominalLength_mm         : REAL := 2.850;    (* Target Completed Double-Seam Length (Height) [mm] *)
    rSet_Target1stOpPeakForce_N       : REAL := 320.0;    (* Commanded 1st Operation Roll Curling Force [N] *)
    rSet_Target2ndOpPeakForce_N       : REAL := 680.0;    (* Commanded 2nd Operation Roll Crimp Force [N] *)
    rSet_TargetLN2DoseMass_mg         : REAL := 45.0;     (* Target Cryogenic LN2 Dose Mass [mg] *)
    rSet_TargetInternalPressure_bar   : REAL := 1.85;     (* Target Post-Seam Container Internal Pressure [bar] *)
    rSet_AcousticResonanceTarget_Hz   : REAL := 3250.0;   (* Nominal End Dome Resonant Vibration Frequency [Hz] *)
    rSet_ChamberPAAConcentration_ppm  : REAL := 1500.0;   (* Aseptic Isolator Target PAA Concentration [ppm] *)
    rSet_SterileAirPressure_Pa        : REAL := 45.0;     (* Aseptic Isolator Target Overpressure [Pa] *)
    rCycleScanDeltaTime               : REAL := 0.00025;  (* Deterministic Industrial PLC Scan Cycle (250 us) [s] *)
END_VAR
VAR_OUTPUT
    (* High-Speed Actuator Command Vectors & Servo Setpoints *)
    rCmd_1stOpServoRadialPosition_mm  : REAL := 1.450;    (* 1st Op Roll Dynamic Servo Radial Infeed Position [mm] *)
    rCmd_2ndOpServoRadialPosition_mm  : REAL := 1.020;    (* 2nd Op Roll Dynamic Servo Radial Infeed Position [mm] *)
    rCmd_SpindleElectronicCamTorque_Nm: REAL := 0.0;      (* Electronic Cam Direct-Drive Spindle Torque [Nm] *)
    rCmd_LN2InjectorPulseDuration_ms  : REAL := 3.85;     (* High-Speed Cryogenic Solenoid Injection Pulse [ms] *)
    rCmd_LifterPneumaticCushion_bar   : REAL := 4.20;     (* Lifter Cushion Dynamic Pneumatic Compensation [bar] *)
    bCmd_PneumaticRejectSolenoid_Fast : BOOL := FALSE;    (* Sub-2ms Solenoid Valve Pulse for Defective Can Divert [BOOL] *)
    rCmd_InfeedPacingScrewSpeed_RPM   : REAL := 250.0;    (* Infeed Pacing Screw Servo Velocity Reference [RPM] *)
    rCmd_DischargeTurretSync_RPM      : REAL := 83.33;    (* Outfeed Transfer Starwheel Servo Reference [RPM] *)
    rCmd_PAAVaporizerDosingPump_Pct   : REAL := 0.0;      (* PAA Liquid Injection Peristaltic Pump Command [%] *)
    rCmd_SterileAirSupplyDamper_Pct   : REAL := 85.0;     (* ISO 5 HEPA Laminar Air Flow Blower Damper [%] *)

    (* Online Quality Attributes, Hermeticity & Metrology Telemetry *)
    rEstimatedSeamOverlap_Pct         : REAL := 88.5;     (* Online Seam Overlap Percentage (CQA > 85.0%) [%] *)
    rEstimatedSeamThickness_mm        : REAL := 1.020;    (* Online Calculated Seam Thickness Gauge [mm] *)
    rCalculatedBodyHookLength_mm      : REAL := 1.420;    (* Calculated Body Hook Fold Length [mm] *)
    rCalculatedCoverHookLength_mm     : REAL := 1.410;    (* Calculated Cover Hook Curl Length [mm] *)
    rEstimatedInternalCanPressure_bar : REAL := 1.85;     (* Acoustic / Physical Headspace Pressure [bar] *)
    rFilteredResonantFrequency_Hz     : REAL := 3250.0;   (* 2oo3 Voted Acoustic Impulse Peak Resonance [Hz] *)
    rAcousticDampingDecayRate         : REAL := 42.5;     (* Resonance Amplitude Logarithmic Decrement [1/s] *)
    rCamElectronicTrackingError_mrad  : REAL := 0.0;      (* Electronic Camming Dynamic Tracking Deviation [mrad] *)

    (* ISA-18.2 Diagnostic Alarm Words, System Health & Statistics *)
    wAlarmWord_ISA18_Critical         : WORD := 16#0000;  (* Priority 1 Emergency Shutdown Trip Mask [WORD] *)
    wAlarmWord_ISA18_Warning          : WORD := 16#0000;  (* Priority 2 Quality Rejection & Warning Mask [WORD] *)
    wSensorHealthStatusWord           : WORD := 16#0000;  (* 2oo3 TMR Sensor Health & Fault Channel Bitmask [WORD] *)
    wAutomationStatusWord             : WORD := 16#0000;  (* Machine Operational State & Subsystem Word [WORD] *)
    wCanRejectionBitmask              : WORD := 16#0000;  (* Reject Reason Coded Bitfield (Leak, Force, LN2, PAA) [WORD] *)
    diTotalCansProcessedCount         : DINT := 0;        (* Total Running Processed Container Counter [DINT] *)
    diTotalCansRejectedCount          : DINT := 0;        (* Total Defective Diverted Container Counter [DINT] *)
    rDefectPPM_CurrentRun             : REAL := 0.0;      (* Running Production Defect Rate [Parts Per Million] *)
    eCurrentFSMState                  : INT := 10;        (* Current Finite State Machine Phase Identifier [INT] *)
    bMachineSynchronized              : BOOL := FALSE;    (* Twin-Turret Electronic Camming Locked & Phase Aligned [BOOL] *)
    bAsepticBarrierIntegrityOK        : BOOL := FALSE;    (* Isolator PAA & Positive Pressure Validated [BOOL] *)
    tCurrentProductionDuration        : TIME := T#0s;     (* Accumulated Active Production Runtime [TIME] *)
END_VAR
VAR
    (* ================================================================================================================ *)
    (* DISCRETE STATE-SPACE MATRICES & VECTORS (8x8 State-Space Formulation at 250 microsecond Cycle)                   *)
    (* States x = [x1: BodyHook (mm), x2: CoverHook (mm), x3: SeamThickness (mm), x4: CamAngleErr (rad),              *)
    (*             x5: CamVelErr (rad/s), x6: HeadspacePres (bar), x7: AcousticResonance (Hz), x8: OscEnvelope (V)]   *)
    (* Inputs u = [u1: 1stOpRadialOffset (mm), u2: 2ndOpRadialOffset (mm), u3: SpindleTorqueCorr (Nm),                 *)
    (*             u4: LN2InjectorDuration (ms), u5: LifterCushionPres (bar)]                                          *)
    (* Outputs y = [y1: OverlapPct (%), y2: SeamThick (mm), y3: CamErr (mrad), y4: Pressure (bar),                      *)
    (*              y5: ResFreq (Hz), y6: DecayRate (1/s), y7: 1stOpForce (N), y8: 2ndOpForce (N)]                      *)
    (* ================================================================================================================ *)
    matA                              : ARRAY[1..8, 1..8] OF REAL;  (* Discrete System Transition Matrix (8x8) *)
    matB                              : ARRAY[1..8, 1..5] OF REAL;  (* Discrete Input Distribution Matrix (8x5) *)
    matC                              : ARRAY[1..8, 1..8] OF REAL;  (* Discrete Measurement Observation Matrix (8x8) *)
    matD                              : ARRAY[1..8, 1..5] OF REAL;  (* Discrete Direct Feedthrough Matrix (8x5) *)
    vecX                              : ARRAY[1..8] OF REAL;        (* Current Dynamic State Vector x[k] *)
    vecX_Next                         : ARRAY[1..8] OF REAL;        (* Predicted Next Dynamic State Vector x[k+1] *)
    vecU                              : ARRAY[1..5] OF REAL;        (* Optimal Control Input Vector u[k] *)
    vecU_Prev                         : ARRAY[1..5] OF REAL;        (* Previous Control Input Vector u[k-1] *)
    vecDeltaU                         : ARRAY[1..5] OF REAL;        (* Slew Rate Increment Vector Delta_u[k] *)
    vecY                              : ARRAY[1..8] OF REAL;        (* Output Measurement Vector y[k] *)
    vecR                              : ARRAY[1..8] OF REAL;        (* Dynamic Recipe Reference Vector r[k] *)
    vecStateError                     : ARRAY[1..8] OF REAL;        (* State Tracking Deviation e[k] = x[k] - r[k] *)

    (* Model Predictive Control (MPC) Quadratic Weighting Matrices & Gradient Optimization *)
    matQ                              : ARRAY[1..8, 1..8] OF REAL;  (* State Tracking Penalty Diagonal Matrix (8x8) *)
    matR                              : ARRAY[1..5, 1..5] OF REAL;  (* Actuator Effort Penalty Diagonal Matrix (5x5) *)
    matS                              : ARRAY[1..5, 1..5] OF REAL;  (* Actuator Slew Rate Rate-of-Change Penalty (5x5) *)
    matP                              : ARRAY[1..8, 1..8] OF REAL;  (* Terminal State Riccati Cost Matrix (8x8) *)
    vecCostGradient                   : ARRAY[1..5] OF REAL;        (* Unconstrained MPC Cost Function Gradient *)
    matHessianApprox                  : ARRAY[1..5, 1..5] OF REAL;  (* Quadratic Hessian Approximation Matrix *)
    rMPC_OptimizationLearningRate     : REAL := 0.045;              (* Projected Gradient Descent Step Size Alpha *)
    rMPC_TotalCalculatedCost          : REAL := 0.0;                (* Instantaneous Quadratic Cost J[k] *)
    rMPC_StatePenaltyCost             : REAL := 0.0;                (* Tracking Deviation Penalty Term *)
    rMPC_ActuatorEffortCost           : REAL := 0.0;                (* Control Magnitude Penalty Term *)
    rMPC_ActuatorSlewCost             : REAL := 0.0;                (* Control Slew Delta Penalty Term *)
    iMPC_IterationCounter             : INT := 0;                   (* Solver Iteration Index *)

    (* 2oo3 Triple Modular Redundancy (TMR) Operational Channels, Discrepancies & Timers *)
    rVoted_Force1stOp_N               : REAL := 320.0;  (* 2oo3 Selected 1st Operation Roll Reaction Force [N] *)
    bDiscrepAlarm_Force1stOp          : BOOL := FALSE;  (* 1st Operation Force Discrepancy Active (> 35.0 N) *)
    rTimer_Force1stOp_Discrep_s       : REAL := 0.0;    (* Discrepancy Latch Delay Accumulator [s] *)
    bTMR_Force1st_Fault_A             : BOOL := FALSE;  (* 1st Op Force Channel A Hardware Diagnostic Fault *)
    bTMR_Force1st_Fault_B             : BOOL := FALSE;  (* 1st Op Force Channel B Hardware Diagnostic Fault *)
    bTMR_Force1st_Fault_C             : BOOL := FALSE;  (* 1st Op Force Channel C Hardware Diagnostic Fault *)

    rVoted_Force2ndOp_N               : REAL := 680.0;  (* 2oo3 Selected 2nd Operation Roll Crimp Force [N] *)
    bDiscrepAlarm_Force2ndOp          : BOOL := FALSE;  (* 2nd Operation Force Discrepancy Active (> 35.0 N) *)
    rTimer_Force2ndOp_Discrep_s       : REAL := 0.0;    (* Discrepancy Latch Delay Accumulator [s] *)
    bTMR_Force2nd_Fault_A             : BOOL := FALSE;  (* 2nd Op Force Channel A Hardware Diagnostic Fault *)
    bTMR_Force2nd_Fault_B             : BOOL := FALSE;  (* 2nd Op Force Channel B Hardware Diagnostic Fault *)
    bTMR_Force2nd_Fault_C             : BOOL := FALSE;  (* 2nd Op Force Channel C Hardware Diagnostic Fault *)

    rVoted_TurretResolver_deg         : REAL := 0.0;    (* 2oo3 Selected Turret Resolver Angle [deg] *)
    bDiscrepAlarm_TurretResolver      : BOOL := FALSE;  (* Resolver Discrepancy Active (> 0.150 deg) *)
    rTimer_Resolver_Discrep_s         : REAL := 0.0;    (* Discrepancy Latch Delay Accumulator [s] *)
    bTMR_Resolver_Fault_A             : BOOL := FALSE;  (* Resolver Channel A Hardware Diagnostic Fault *)
    bTMR_Resolver_Fault_B             : BOOL := FALSE;  (* Resolver Channel B Hardware Diagnostic Fault *)
    bTMR_Resolver_Fault_C             : BOOL := FALSE;  (* Resolver Channel C Hardware Diagnostic Fault *)

    rVoted_LN2DoseMass_mg             : REAL := 45.0;   (* 2oo3 Selected Cryogenic LN2 Dose Mass [mg] *)
    bDiscrepAlarm_LN2DoseMass         : BOOL := FALSE;  (* LN2 Mass Flow Discrepancy Active (> 2.50 mg) *)
    rTimer_LN2Mass_Discrep_s          : REAL := 0.0;    (* Discrepancy Latch Delay Accumulator [s] *)
    bTMR_LN2Mass_Fault_A              : BOOL := FALSE;  (* Cryogenic Mass Flow Channel A Diagnostic Fault *)
    bTMR_LN2Mass_Fault_B              : BOOL := FALSE;  (* Cryogenic Mass Flow Channel B Diagnostic Fault *)
    bTMR_LN2Mass_Fault_C              : BOOL := FALSE;  (* Cryogenic Mass Flow Channel C Diagnostic Fault *)

    rVoted_AcousticPressure_bar       : REAL := 1.85;   (* 2oo3 Selected Can Resonant Internal Pressure [bar] *)
    rVoted_AcousticResonanceFreq_Hz   : REAL := 3250.0; (* 2oo3 Selected Acoustic Peak Resonance Frequency [Hz] *)
    bDiscrepAlarm_AcousticResonance   : BOOL := FALSE;  (* Resonance Discrepancy Active (> 120.0 Hz) *)
    rTimer_Acoustic_Discrep_s         : REAL := 0.0;    (* Discrepancy Latch Delay Accumulator [s] *)
    bTMR_Acoustic_Fault_A             : BOOL := FALSE;  (* Acoustic Sensor Channel A Diagnostic Fault *)
    bTMR_Acoustic_Fault_B             : BOOL := FALSE;  (* Acoustic Sensor Channel B Diagnostic Fault *)
    bTMR_Acoustic_Fault_C             : BOOL := FALSE;  (* Acoustic Sensor Channel C Diagnostic Fault *)

    rVoted_PAAConcentration_ppm       : REAL := 1500.0; (* 2oo3 Selected Isolator PAA Concentration [ppm] *)
    bDiscrepAlarm_PAAConcentration    : BOOL := FALSE;  (* PAA Concentration Discrepancy Active (> 50.0 ppm) *)
    rTimer_PAA_Discrep_s              : REAL := 0.0;    (* Discrepancy Latch Delay Accumulator [s] *)
    bTMR_PAA_Fault_A                  : BOOL := FALSE;  (* PAA Transmitter Channel A Diagnostic Fault *)
    bTMR_PAA_Fault_B                  : BOOL := FALSE;  (* PAA Transmitter Channel B Diagnostic Fault *)
    bTMR_PAA_Fault_C                  : BOOL := FALSE;  (* PAA Transmitter Channel C Diagnostic Fault *)

    rVoted_SterileAirPres_Pa          : REAL := 45.0;   (* 2oo3 Selected Sterile Air Overpressure [Pa] *)
    bDiscrepAlarm_SterileAirPres      : BOOL := FALSE;  (* Isolator Pressure Discrepancy Active (> 3.00 Pa) *)
    rTimer_SterileAir_Discrep_s       : REAL := 0.0;    (* Discrepancy Latch Delay Accumulator [s] *)
    bTMR_SterileAir_Fault_A           : BOOL := FALSE;  (* Sterile Air Transducer Channel A Fault *)
    bTMR_SterileAir_Fault_B           : BOOL := FALSE;  (* Sterile Air Transducer Channel B Fault *)
    bTMR_SterileAir_Fault_C           : BOOL := FALSE;  (* Sterile Air Transducer Channel C Fault *)

    rVoted_ChuckBearingTemp_C         : REAL := 38.5;   (* 2oo3 Selected Seaming Chuck Bearing Temp [deg C] *)
    bDiscrepAlarm_ChuckBearingTemp    : BOOL := FALSE;  (* Bearing Temp Discrepancy Active (> 4.00 deg C) *)
    rTimer_BearingTemp_Discrep_s      : REAL := 0.0;    (* Discrepancy Latch Delay Accumulator [s] *)
    bTMR_BearingTemp_Fault_A          : BOOL := FALSE;  (* Thermocouple Channel A Diagnostic Fault *)
    bTMR_BearingTemp_Fault_B          : BOOL := FALSE;  (* Thermocouple Channel B Diagnostic Fault *)
    bTMR_BearingTemp_Fault_C          : BOOL := FALSE;  (* Thermocouple Channel C Diagnostic Fault *)

    (* Double-Seam Elastic-Plastic Micro-Mechanics & Geometry Constants *)
    rSheetThickness_Body_mm           : REAL := 0.165;  (* Body Cylinder Sheet Metal Nominal Thickness [mm] *)
    rSheetThickness_End_mm            : REAL := 0.205;  (* End Can Lid Sheet Metal Nominal Thickness [mm] *)
    rSeamingCompoundDryFilmThick_mm   : REAL := 0.038;  (* Elastomeric Gasket Sealing Compound Thickness [mm] *)
    rCompoundCompressionModulus_MPa   : REAL := 82.50;  (* Elastic Bulk Modulus of Water-Based Compound [MPa] *)
    rSeamLengthCalculated_mm          : REAL := 2.850;  (* Geometric Double Seam Length (Flange Height) [mm] *)
    rTheoreticalMinimumSeamThick_mm   : REAL := 0.943;  (* 3*End + 2*Body = 3(0.205) + 2(0.165) = 0.945 mm *)

    (* Electronic Camming Polynomial Profile Synthesis (5th-Order Quintic Cam Curves) *)
    rCamAngle_Normalized_deg          : REAL := 0.0;    (* Turret Station Master Phase Angle [0.0 - 360.0 deg] *)
    rCam1stOp_BaseRadius_mm           : REAL := 42.50;  (* 1st Operation Roll Cam Profile Base Pitch Radius [mm] *)
    rCam1stOp_MaxStroke_mm            : REAL := 6.200;  (* 1st Operation Roll Radial Servo Total Stroke [mm] *)
    rCam2ndOp_BaseRadius_mm           : REAL := 42.50;  (* 2nd Operation Roll Cam Profile Base Pitch Radius [mm] *)
    rCam2ndOp_MaxStroke_mm            : REAL := 4.800;  (* 2nd Operation Roll Radial Servo Total Stroke [mm] *)
    rProfile1stOp_PosFeedforward_mm   : REAL := 0.0;    (* Cam Analytical Position Feedforward Profile [mm] *)
    rProfile2ndOp_PosFeedforward_mm   : REAL := 0.0;    (* Cam Analytical Position Feedforward Profile [mm] *)
    rCamPoly_A0, rCamPoly_A1, rCamPoly_A2 : REAL := 0.0;(* Quintic Cam Polynomial Coefficients 1st Op *)
    rCamPoly_A3, rCamPoly_A4, rCamPoly_A5 : REAL := 0.0;
    rCamPoly_B0, rCamPoly_B1, rCamPoly_B2 : REAL := 0.0;(* Quintic Cam Polynomial Coefficients 2nd Op *)
    rCamPoly_B3, rCamPoly_B4, rCamPoly_B5 : REAL := 0.0;

    (* Liquid Nitrogen Sub-Cooled Cryogenic Micro-Dosing Thermodynamics *)
    rLN2_LatentHeatVap_kJ_per_kg      : REAL := 199.1;  (* Latent Heat of Vaporization of Liquid Nitrogen [kJ/kg] *)
    rLN2_DensityLiquid_kg_per_m3      : REAL := 808.4;  (* Liquid Nitrogen Density at Atmospheric Boiling [kg/m3] *)
    rN2_GasConstant_J_per_mol_K       : REAL := 8.31446;(* Universal Gas Constant R [J/(mol*K)] *)
    rN2_MolarMass_kg_per_mol          : REAL := 0.02801;(* Nitrogen Molecular Weight [kg/mol] *)
    rHeadspaceNominalVolume_m3        : REAL := 0.0000185; (* Nominal Headspace Volume 18.5 ml [m3] *)
    rBeverageFillTemperature_K        : REAL := 277.15; (* Product Cold-Fill Temperature (4 deg C) [K] *)
    rLN2_FlashFractionInstantaneous   : REAL := 0.420;  (* Primary Vaporization Fraction During Drop Fall *)
    rLN2_InjectedDoseMass_Current_mg  : REAL := 45.0;   (* Dynamic Mass Injected into Target Can [mg] *)

    (* Acoustic Tap Resonance Bandpass Filter & Peak Envelope Observer *)
    rAcousticSampleRaw_V              : REAL := 0.0;    (* Analog Input Voltage from Microphone/Sensor [V] *)
    rIIR_FilterState_x1               : REAL := 0.0;    (* Direct-Form II Biquad Delay Variable x[k-1] *)
    rIIR_FilterState_x2               : REAL := 0.0;    (* Direct-Form II Biquad Delay Variable x[k-2] *)
    rIIR_Coeff_b0                     : REAL := 0.0825; (* Biquad Resonator Feedforward Coeff b0 *)
    rIIR_Coeff_b1                     : REAL := 0.0000; (* Biquad Resonator Feedforward Coeff b1 *)
    rIIR_Coeff_b2                     : REAL := -0.0825;(* Biquad Resonator Feedforward Coeff b2 *)
    rIIR_Coeff_a1                     : REAL := -1.7245;(* Biquad Resonator Feedback Pole Coeff a1 *)
    rIIR_Coeff_a2                     : REAL := 0.8350; (* Biquad Resonator Feedback Pole Coeff a2 *)
    rAcousticSignalFiltered           : REAL := 0.0;    (* Bandpass Filtered Acoustic Pressure Signal [V] *)
    rAcousticEnvelopeAmplitude        : REAL := 0.0;    (* Dynamic Vibration Amplitude Envelope [V] *)
    rAcousticPeakTrackingFrequency_Hz : REAL := 3250.0; (* Fast Peak Extracted Resonant Frequency [Hz] *)
    rAcousticLogarithmicDecrement     : REAL := 0.085;  (* Vibration Log Decrement Delta = ln(y1/y2) *)

    (* ISA-18.2 Multi-Tiered Alarm Thresholds & Hysteresis Deadbands *)
    rLim_1stOpForce_HH_N              : REAL := 480.0;  (* Seam Roll 1st Op Force Extreme Overload [N] *)
    rLim_1stOpForce_H_N               : REAL := 420.0;  (* Seam Roll 1st Op Force High Process Limit [N] *)
    rLim_1stOpForce_L_N               : REAL := 220.0;  (* Seam Roll 1st Op Force Under-Curl Limit [N] *)
    rLim_1stOpForce_LL_N              : REAL := 150.0;  (* Seam Roll 1st Op Missing End / Slip Trip [N] *)
    rLim_2ndOpForce_HH_N              : REAL := 950.0;  (* Seam Roll 2nd Op Force Chuck Fracture Trip [N] *)
    rLim_2ndOpForce_H_N               : REAL := 820.0;  (* Seam Roll 2nd Op Force High Crimp Limit [N] *)
    rLim_2ndOpForce_L_N               : REAL := 540.0;  (* Seam Roll 2nd Op Force Loose Seam Warning [N] *)
    rLim_2ndOpForce_LL_N              : REAL := 400.0;  (* Seam Roll 2nd Op Inadequate Hermetic Seal [N] *)
    rLim_InternalPres_HH_bar          : REAL := 3.20;   (* Can Internal Pressure Hydro-Burst Hazard [bar] *)
    rLim_InternalPres_H_bar           : REAL := 2.60;   (* Can Internal Pressure Over-Dose Limit [bar] *)
    rLim_InternalPres_L_bar           : REAL := 1.35;   (* Can Internal Pressure Panel Buckle Warning [bar] *)
    rLim_InternalPres_LL_bar          : REAL := 0.80;   (* Can Internal Pressure Flat / Micro-Leak Reject [bar] *)
    rLim_AcousticResonance_HH_Hz      : REAL := 3900.0; (* Acoustic Dome Resonance Over-Stress [Hz] *)
    rLim_AcousticResonance_H_Hz       : REAL := 3650.0; (* Acoustic Dome Resonance Upper Tolerance [Hz] *)
    rLim_AcousticResonance_L_Hz       : REAL := 2850.0; (* Acoustic Dome Resonance Lower Tolerance [Hz] *)
    rLim_AcousticResonance_LL_Hz      : REAL := 2400.0; (* Acoustic Dome Resonance Flat Can / Puncture [Hz] *)
    rLim_PAAConc_HH_ppm               : REAL := 2200.0; (* Isolator PAA Chemical Vapor Surge [ppm] *)
    rLim_PAAConc_H_ppm                : REAL := 1800.0; (* Isolator PAA Upper Target Band [ppm] *)
    rLim_PAAConc_L_ppm                : REAL := 1200.0; (* Isolator PAA Sub-Sterile Warning [ppm] *)
    rLim_PAAConc_LL_ppm               : REAL := 800.0;  (* Isolator PAA Critical De-Sterilization Trip [ppm] *)
    rLim_SterileAir_HH_Pa             : REAL := 85.0;   (* Isolator Air Overpressure Overload [Pa] *)
    rLim_SterileAir_H_Pa              : REAL := 65.0;   (* Isolator Air Upper Target Band [Pa] *)
    rLim_SterileAir_L_Pa              : REAL := 30.0;   (* Isolator Air Low Pressure Barrier Warning [Pa] *)
    rLim_SterileAir_LL_Pa             : REAL := 15.0;   (* Isolator Air Loss of Aseptic Barrier Trip [Pa] *)
    rLim_ChuckBearingTemp_HH_C        : REAL := 65.0;   (* Chuck Bearing Thermal Runaway E-Stop [deg C] *)
    rLim_ChuckBearingTemp_H_C         : REAL := 52.0;   (* Chuck Bearing Elevated Friction Warning [deg C] *)
    rDeadband_Force_N                 : REAL := 6.0;    (* Analog Deadband Hysteresis for Force [N] *)
    rDeadband_Pressure_bar            : REAL := 0.04;   (* Analog Deadband Hysteresis for Pressure [bar] *)
    rDeadband_Acoustic_Hz             : REAL := 25.0;   (* Analog Deadband Hysteresis for Acoustic Freq [Hz] *)
    rDeadband_PAA_ppm                 : REAL := 30.0;   (* Analog Deadband Hysteresis for PAA [ppm] *)
    rDeadband_SterileAir_Pa           : REAL := 2.5;    (* Analog Deadband Hysteresis for Isolator Pres [Pa] *)
    rDeadband_BearingTemp_C           : REAL := 1.5;    (* Analog Deadband Hysteresis for Temp [deg C] *)

    (* Rate-of-Change (ROC) Signal Differentiators *)
    rPrevPressureSample_bar           : REAL := 1.85;   (* Prior Execution Scan Pressure Sample [bar] *)
    rRateOfChange_Pressure_bar_per_s  : REAL := 0.0;    (* Computed Derivative dP/dt [bar/s] *)
    rPrevForce1stOpSample_N           : REAL := 320.0;  (* Prior Scan 1st Op Force Sample [N] *)
    rRateOfChange_Force1stOp_N_per_s  : REAL := 0.0;    (* Computed Derivative dF1/dt [N/s] *)

    (* Latched Alarm Flags *)
    bAlarm_Force1stOp_HH              : BOOL := FALSE;  (* Critical Seaming Roll 1st Op Force HH Trip *)
    bAlarm_Force1stOp_H               : BOOL := FALSE;  (* Warning Seaming Roll 1st Op Force H *)
    bAlarm_Force1stOp_L               : BOOL := FALSE;  (* Warning Seaming Roll 1st Op Force L *)
    bAlarm_Force1stOp_LL              : BOOL := FALSE;  (* Critical Seaming Roll 1st Op Force LL Trip *)
    bAlarm_Force2ndOp_HH              : BOOL := FALSE;  (* Critical Seaming Roll 2nd Op Force HH Trip *)
    bAlarm_Force2ndOp_H               : BOOL := FALSE;  (* Warning Seaming Roll 2nd Op Force H *)
    bAlarm_Force2ndOp_L               : BOOL := FALSE;  (* Warning Seaming Roll 2nd Op Force L *)
    bAlarm_Force2ndOp_LL              : BOOL := FALSE;  (* Critical Seaming Roll 2nd Op Force LL Trip *)
    bAlarm_InternalPres_HH            : BOOL := FALSE;  (* Critical Can Internal Pressure HH Trip *)
    bAlarm_InternalPres_H             : BOOL := FALSE;  (* Warning Can Internal Pressure H *)
    bAlarm_InternalPres_L             : BOOL := FALSE;  (* Warning Can Internal Pressure L *)
    bAlarm_InternalPres_LL            : BOOL := FALSE;  (* Critical Can Internal Pressure LL Trip *)
    bAlarm_AcousticResonance_HH       : BOOL := FALSE;  (* Critical Acoustic Resonance HH Trip *)
    bAlarm_AcousticResonance_H        : BOOL := FALSE;  (* Warning Acoustic Resonance H *)
    bAlarm_AcousticResonance_L        : BOOL := FALSE;  (* Warning Acoustic Resonance L *)
    bAlarm_AcousticResonance_LL       : BOOL := FALSE;  (* Critical Acoustic Resonance LL (Leak) Trip *)
    bAlarm_PressureLeakRateOfChange   : BOOL := FALSE;  (* Fast Pressure Puncture Defect dP/dt Alarm *)
    bAlarm_PAAConc_HH                 : BOOL := FALSE;  (* Critical Isolator PAA Surge Trip *)
    bAlarm_PAAConc_H                  : BOOL := FALSE;  (* Warning Isolator PAA High *)
    bAlarm_PAAConc_L                  : BOOL := FALSE;  (* Warning Isolator PAA Low *)
    bAlarm_PAAConc_LL                 : BOOL := FALSE;  (* Critical Isolator PAA Loss of Sterility Trip *)
    bAlarm_SterileAir_HH              : BOOL := FALSE;  (* Critical Isolator Air Overpressure HH Trip *)
    bAlarm_SterileAir_H               : BOOL := FALSE;  (* Warning Isolator Air Overpressure H *)
    bAlarm_SterileAir_L               : BOOL := FALSE;  (* Warning Isolator Air Barrier Low *)
    bAlarm_SterileAir_LL              : BOOL := FALSE;  (* Critical Isolator Air Breach LL Trip *)
    bAlarm_ChuckBearingTemp_HH        : BOOL := FALSE;  (* Critical Spindle Chuck Bearing HH Trip *)
    bAlarm_ChuckBearingTemp_H         : BOOL := FALSE;  (* Warning Spindle Chuck Bearing H *)
    bAlarm_SeamOverlapDeficiency      : BOOL := FALSE;  (* Hermetic Seam Overlap < 85.0% Reject Alarm *)
    bAlarm_CanJamInfeedLifter         : BOOL := FALSE;  (* Infeed Pacing Screw / Lifter Starwheel Jam Alarm *)
    bAlarm_EStopDepressurized         : BOOL := FALSE;  (* Emergency Stop Activated Alarm *)

    (* Finite State Machine Internal Sequencers & Timers *)
    eState                            : INT := 10;      (* Active Primary FSM Step Index *)
    ePrevState                        : INT := 10;      (* Historical Step Index for Transition Detection *)
    rStateTimer_s                     : REAL := 0.0;    (* In-State Monotonic Real-Time Timer [s] *)
    rStateTimeoutLimit_s              : REAL := 600.0;  (* Watchdog Safety Timeout for FSM States [s] *)
    iCanPocketIndex                   : INT := 1;       (* Active Rotary Seamer Station Chuck Index (1 to 18) *)
    rProductionAccumulator_s          : REAL := 0.0;    (* Continuous Running Line Master Timer [s] *)
    bRejectTriggerActive              : BOOL := FALSE;  (* Pneumatic High-Speed Reject Solenoid Gate Request *)
    rRejectPulseTimer_s               : REAL := 0.0;    (* Sub-2ms Pneumatic Air Blow-Off Gate Timer [s] *)

    (* Matrix Math Internal Iteration Indices & Scratch Variables *)
    iRow                              : INT := 1;       (* General Loop Row Index *)
    iCol                              : INT := 1;       (* General Loop Column Index *)
    iSub                              : INT := 1;       (* General Loop Inner Index *)
    rSumAccumulator                   : REAL := 0.0;    (* Real Matrix Multiplication Product Accumulator *)
    rDiffAbs                          : REAL := 0.0;    (* Real Absolute Value Temporary Variable *)
    rIntermediateVal                  : REAL := 0.0;    (* Real Math Intermediate Scratch Storage *)
    bMatricesInitialized             : BOOL := FALSE;  (* One-Time State-Space & MPC Matrix Initialization *)
END_VAR
"""

code_blocks.append(part1)
print(f"Part 1 appended, length: {len(part1)}")

# Write to test file to inspect
with open("Local_Ollama_Evol_Pipeline/scratch/test_part1.st", "w", encoding="utf-8") as f:
    f.write(part1)
