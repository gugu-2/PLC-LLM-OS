# semiconductor_tcb_builder/build_st_header_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Semiconductor_AdvancedPackaging_TCB_ThermalCompression_Bonding
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 HIGH-INTEGRITY STRUCTURED TEXT
DOMAIN: SEMICONDUCTOR ADVANCED PACKAGING / 3D HETEROGENEOUS CHIPLET INTEGRATION
PROCESS: HIGH-BANDWIDTH MEMORY (HBM3E/HBM4) & CoWoS THERMO-COMPRESSION BONDING (TCB)
EQUIPMENT: ULTRA-PRECISION SUB-MICRON THERMO-COMPRESSION CHIPLET DIE ATTACH SYSTEM
====================================================================================================

SYSTEM OPERATIONAL ARCHITECTURE:
This industrial cyber-physical automation block provides complete closed-loop supervisory,
multi-variable Model Predictive Control (MPC), Triple Modular Redundant (TMR 2oo3) sensor fusion,
and deterministic 14-stage finite state machine sequencing for sub-micron Thermo-Compression
Bonding (TCB) in 2.5D/3D semiconductor packaging.

KEY SUBSYSTEMS INTEGRATED:
1. VOICE COIL LINEAR MOTOR & PIEZO DUAL-STAGE FORCE/POSITION HEAD:
   - Coarse/fine vertical actuation providing soft landing (5.0 N +/- 0.5 N) and precision
     eutectic bonding force regulation (5.0 N to 450.0 N +/- 1.0 N).
   - High-bandwidth sub-millisecond voice-coil current regulation coupled with dynamic
     piezoelectric micro-actuator displacement trim (+/-10.0 um).
2. ULTRA-FAST PULSE CERAMIC HEATER & CHILLED NITROGEN QUENCH:
   - Low thermal mass silicon nitride / aluminum nitride ceramic heater delivering ultra-fast
     thermal ramps (>280 deg C/s) up to 420.0 deg C peak reflow temperature.
   - High-flow cryogenic/chilled nitrogen gas blast quench cooling (>120 deg C/s) for controlled
     intermetallic compound (IMC) crystallization (Cu6Sn5, Cu3Sn) without thermal voids.
3. 6-AXIS ACTIVE PIEZOELECTRIC CHUCK LEVELING (HEXAPOD KINEMATICS):
   - Dynamic real-time planarization and co-planarity tilt correction (<1.5 urad) compensating
     for substrate warpage, thermal expansion gradients, and non-uniform micro-bump arrays.
4. CONTROLLED-ATMOSPHERE FORMIC ACID (HCOOH) DEOXIDATION SHROUD:
   - Closed vapor injection shroud maintaining residual O2 < 30 ppm and 1.5% - 3.5% vol HCOOH
     vapor concentration for fluxless native oxide reduction of copper pillar micro-bumps.
5. ADVANCED CYBER-PHYSICAL ESTIMATION & MODEL PREDICTIVE CONTROL:
   - 6-state discrete-time Kalman filter tracking dynamic force error, thermal expansion,
     micro-bump solder squeeze-out viscoplastic collapse, heater temperature, chuck vacuum,
     and co-planarity tilt error.
   - Receding-horizon MPC with unrolled Projected Gradient Descent (PGD) over a 10-step horizon.
6. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING:
   - Dual-fault tolerant voting with dynamic discrepancy accumulators across bond force load cells,
     ceramic thin-film thermocouples, linear glass scale encoders, and vacuum diaphragm gauges.

AUTHOR: LUMINA SYNTHETIC DATA ARCHITECT (V7 MAX-PERSONA / CYBER-PHYSICAL SYSTEMS CHAIR)
====================================================================================================
*)

VAR_INPUT
    (* Master System Commands & Safety Interlocks *)
    bEnable                         : BOOL;     (* Master function block execution enable [-] *)
    bStartCycle                     : BOOL;     (* Trigger rising-edge single chiplet bond cycle [-] *)
    bAcknowledgeAlarms              : BOOL;     (* Reset and acknowledge ISA-18.2 active latches [-] *)
    bEmergencyStopOk                : BOOL;     (* Hardware E-Stop safety circuit healthy active-high [-] *)
    bSafetyShieldInterlock          : BOOL;     (* Enclosure physical safety interlock locked [-] *)
    bExhaustAbatementReady          : BOOL;     (* Toxic gas abatement scrubber system ready [-] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Bank 1: Piezo Quartz Bond Force Load Cells [N] *)
    rForceSensor_Ch1                : REAL;     (* Piezo load cell Channel 1 calibrated force [N] *)
    rForceSensor_Ch2                : REAL;     (* Piezo load cell Channel 2 calibrated force [N] *)
    rForceSensor_Ch3                : REAL;     (* Piezo load cell Channel 3 calibrated force [N] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Bank 2: Ceramic Heater Thin-Film Thermocouples [deg C] *)
    rTempSensor_Ch1                 : REAL;     (* Ultra-fast thin-film thermocouple Channel 1 [deg C] *)
    rTempSensor_Ch2                 : REAL;     (* Ultra-fast thin-film thermocouple Channel 2 [deg C] *)
    rTempSensor_Ch3                 : REAL;     (* Ultra-fast thin-film thermocouple Channel 3 [deg C] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Bank 3: Bond Head Linear Optical Glass Encoders [um] *)
    rZPosSensor_Ch1                 : REAL;     (* Bond head linear glass scale encoder Channel 1 [um] *)
    rZPosSensor_Ch2                 : REAL;     (* Bond head linear glass scale encoder Channel 2 [um] *)
    rZPosSensor_Ch3                 : REAL;     (* Bond head linear glass scale encoder Channel 3 [um] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Bank 4: Chuck Vacuum Capacitance Diaphragm Gauges [kPa] *)
    rChuckVacSensor_Ch1             : REAL;     (* Substrate chuck vacuum diaphragm gauge Channel 1 [kPa] *)
    rChuckVacSensor_Ch2             : REAL;     (* Substrate chuck vacuum diaphragm gauge Channel 2 [kPa] *)
    rChuckVacSensor_Ch3             : REAL;     (* Substrate chuck vacuum diaphragm gauge Channel 3 [kPa] *)

    (* Multi-Axis Chuck Optical Alignment & Dynamic Autocollimator Ingest *)
    rChuckTilt_Rx                   : REAL;     (* Optical autocollimator substrate pitch tilt error [urad] *)
    rChuckTilt_Ry                   : REAL;     (* Optical autocollimator substrate roll tilt error [urad] *)
    rVisionAlign_X_um               : REAL;     (* Dual-vision chiplet fiducial placement error X [um] *)
    rVisionAlign_Y_um               : REAL;     (* Dual-vision chiplet fiducial placement error Y [um] *)
    rVisionAlign_Theta_urad         : REAL;     (* Dual-vision chiplet rotational orientation error [urad] *)
    bVisionFiducialLocked           : BOOL;     (* Machine vision target recognition lock valid [-] *)

    (* Process Atmosphere & Chemical Gas Delivery Ingest *)
    rChamber_O2_PPM                 : REAL;     (* Formic shroud residual oxygen gas concentration [ppm] *)
    rFormicAcid_Conc_Pct            : REAL;     (* Formic acid vapor concentration in N2 shroud [%] *)
    rFormicBubblerTemp_degC         : REAL;     (* Liquid formic acid bubbler temperature [deg C] *)
    rCarrierGasPressure_bar         : REAL;     (* N2 carrier gas manifold header pressure [bar] *)
    rExhaustVentFlow_slpm           : REAL;     (* Chamber exhaust ventilation flow rate [slpm] *)

    (* Recipe Target Parameters for Active Bond Profile *)
    rRecipeTargetForce_N            : REAL;     (* Recipe peak thermo-compression bond force [N] *)
    rRecipeSoftTouchForce_N         : REAL;     (* Recipe initial soft landing touch force [N] *)
    rRecipePeakTemp_degC            : REAL;     (* Recipe target peak solder reflow temperature [deg C] *)
    rRecipeSoakTemp_degC            : REAL;     (* Recipe pre-heat thermal soak temperature [deg C] *)
    rRecipeTargetCollapse_um        : REAL;     (* Recipe target micro-bump solder collapse depth [um] *)
    rRecipeThermalRampRate_degC_s   : REAL;     (* Recipe ceramic heater thermal ramp rate [deg C/s] *)
    rRecipeQuenchCoolRate_degC_s    : REAL;     (* Recipe chilled N2 blast cooling quench rate [deg C/s] *)
    rRecipeEutecticHoldTime_ms      : REAL;     (* Recipe duration at peak reflow temperature [ms] *)
    rRecipeDeoxDwellTime_ms         : REAL;     (* Recipe formic acid reduction dwell duration [ms] *)
    rRecipeMicroBumpCount           : REAL;     (* Total quantity of micro-bumps on active die [-] *)
    rRecipeMicroBumpDiameter_um     : REAL;     (* Nominal micro-bump copper pillar diameter [um] *)

    (* Post-Bond Acoustic Inspection Transducer Ingest *)
    rAcousticEchoAmplitude_mV       : REAL;     (* Ultrasonic transducer pulse-echo amplitude [mV] *)
    rAcousticTimeOfFlight_ns        : REAL;     (* Ultrasonic pulse-echo time-of-flight return [ns] *)

    (* PLC Execution Timing Ingest *)
    tCycleScanTime                  : TIME;     (* Deterministic PLC task cyclic scan time interval [s] *)
END_VAR

VAR_OUTPUT
    (* Primary Sequence Operational Status *)
    bCycleBusy                      : BOOL;     (* TCB automated sequence actively executing [-] *)
    bCycleComplete                  : BOOL;     (* Single chiplet bond sequence completed successfully [-] *)
    bCycleAborted                   : BOOL;     (* Active bond cycle terminated prematurely [-] *)
    bSystemHealthy                  : BOOL;     (* All safety circuits, TMR sensors and interlocks healthy [-] *)
    iCurrentFsmState                : INT;      (* Active finite state machine execution state index (0..13) [-] *)
    sCurrentFsmStateName            : STRING[64];(* Human-readable state description string [-] *)
    rStepElapsedTime_ms             : REAL;     (* Active state stage elapsed timer [ms] *)
    rTotalCycleTime_ms              : REAL;     (* Total cumulative bonding sequence duration [ms] *)

    (* Actuator Command Signals (Dual-Stage Head & Thermal Engine) *)
    rVoiceCoilCurrent_Cmd_A         : REAL;     (* Bond head voice-coil motor drive current command [A] *)
    rPiezoZ_Trim_Cmd_um             : REAL;     (* Z-axis piezo fine positioner displacement trim [um] *)
    rCeramicHeaterDuty_Cmd_Pct      : REAL;     (* Pulse ceramic heater PWM firing duty cycle [%] *)
    rN2QuenchValve_Cmd_Pct          : REAL;     (* Chilled N2 cooling quench blast proportional valve [%] *)
    rFormicPurgeValve_Cmd_Pct       : REAL;     (* Formic acid vapor shroud mass flow control [%] *)
    bHeadVacuumSolenoid             : BOOL;     (* Bond collet chiplet holding vacuum valve [-] *)
    bHeadPurgePuffSolenoid          : BOOL;     (* Bond collet micro-puff positive pressure release [-] *)
    bChuckVacuumSolenoid            : BOOL;     (* Substrate holding vacuum chuck lock valve [-] *)
    bExhaustDiverterValve           : BOOL;     (* Chamber exhaust diverter to catalytic scrubber [-] *)

    (* 6-Axis Chuck Dynamic Leveling Hexapod Piezo Actuators *)
    rChuckPiezoLevel_Tx_um          : REAL;     (* Active chuck leveling translation trim X [um] *)
    rChuckPiezoLevel_Ty_um          : REAL;     (* Active chuck leveling translation trim Y [um] *)
    rChuckPiezoLevel_Tz_um          : REAL;     (* Active chuck leveling translation trim Z [um] *)
    rChuckPiezoLevel_Rx_urad        : REAL;     (* Active chuck leveling angular tilt pitch Rx [urad] *)
    rChuckPiezoLevel_Ry_urad        : REAL;     (* Active chuck leveling angular tilt roll Ry [urad] *)
    rChuckPiezoLevel_Rz_urad        : REAL;     (* Active chuck leveling rotational theta Rz [urad] *)

    (* 2oo3 TMR Validated Process Variables *)
    rVotedBondForce_N               : REAL;     (* TMR voted real-time bond force measurement [N] *)
    rVotedInterfaceTemp_degC        : REAL;     (* TMR voted pulse ceramic heater temperature [deg C] *)
    rVotedZPosition_um              : REAL;     (* TMR voted bond head Z linear scale position [um] *)
    rVotedChuckVacuum_kPa           : REAL;     (* TMR voted substrate chuck differential pressure [kPa] *)

    (* Cyber-Physical Estimated States & Quality Metrics *)
    rEstimatedSolderCollapse_um     : REAL;     (* Real-time tracked micro-bump solder collapse depth [um] *)
    rEstimatedHeadElongation_um     : REAL;     (* Bond head collet Z-axis thermal expansion elongation [um] *)
    rDynamicContactStiffness_N_um   : REAL;     (* Online calculated micro-bump contact stiffness [N/um] *)
    rAcousticVoidFraction_Pct       : REAL;     (* Post-bond acoustic pulse-echo detected joint void [%] *)
    bBondQualityPass                : BOOL;     (* Post-bond multi-parameter quality acceptance flag [-] *)

    (* ISA-18.2 Bit-Packed Diagnostic and Alarm Telemetry *)
    dwAlarmWord1_SafetyTrips        : DWORD;    (* Bit-packed critical safety trips and process trips [-] *)
    dwAlarmWord2_Discrepancies      : DWORD;    (* Bit-packed TMR sensor discrepancy and drift warnings [-] *)
    dwStatusWord1_Operational       : DWORD;    (* Bit-packed system operational modes and health flags [-] *)
    dwStatusWord2_Subsystems        : DWORD;    (* Bit-packed sub-actuator status and interlock states [-] *)
END_VAR
"""
