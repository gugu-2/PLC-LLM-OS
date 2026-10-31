# Python script to generate FB_HydraulicDieForging_MultiCylinderRam_Leveling
import json
import os
import re
import sys

def build_code():
    parts = []

    # 1. Header
    parts.append("""FUNCTION_BLOCK FB_HydraulicDieForging_MultiCylinderRam_Leveling
(*
 ==========================================================================================
  PROJECT:       HEAVY COMMERCIAL AEROSPACE & DEFENSE CLOSED-DIE FORGING AUTOMATION
  SUBSYSTEM:     50,000-TON MULTI-CYLINDER HYDRAULIC FORGING PRESS RAM LEVELING & EJECTOR
  DISCIPLINE:    HIGH-PRESSURE HYDRAULICS / FINITE TILT RECEDING-HORIZON MPC / TMR 2oo3
  IEC STANDARD:  IEC 61131-3 3RD EDITION (DETERMINISTIC EMBEDDED AUTOMATION)
  PLATFORM:      SAFETY PLC / HIGH-PERFORMANCE INDUSTRIAL MOTION CONTROLLER
 ==========================================================================================
  ARCHITECTURAL SPECIFICATION:
  This Function Block executes deterministically on real-time industrial PLC controllers
  (1.0 ms nominal execution cycle) governing a 50,000-metric-ton closed-die hydraulic
  forging press. Such presses are heavily deployed in aerospace manufacturing for forging
  heavy titanium (Ti-6Al-4V) bulkheads, large nickel-based superalloy (Inconel 718) turbine
  discs, and commercial widebody aircraft landing gear main outer cylinders.

  PHYSICAL ACTUATION & SENSORY STRUCTURE:
  1. Main Hydraulic Cylinder Ram Array:
     - 4 Main Corner Pressing Cylinders:
       * Cyl 1: Front-Left  (FL), Piston Area A_cyl1 = 1.6513 m2 (Bore = 1450 mm, Rod = 1200 mm)
       * Cyl 2: Front-Right (FR), Piston Area A_cyl2 = 1.6513 m2
       * Cyl 3: Rear-Right  (RR), Piston Area A_cyl3 = 1.6513 m2
       * Cyl 4: Rear-Left   (RL), Piston Area A_cyl4 = 1.6513 m2
     - Press Column Structural Geometry: Width (Roll axis, L_x) = 3800 mm, Depth (Pitch axis, L_y) = 5200 mm.
     - Maximum Moving Ram Mass: M_ram = 2,450 metric tons (2,450,000 kg).

  2. High-Pressure Fluid Dynamics & Bulk Modulus:
     - Hydraulic Fluid: ISO VG 46 synthetic water-glycol / polyol ester fire-resistant fluid.
     - Operating Supply Pressure: P_supply = 350.0 bar nominal (420.0 bar mechanical proof rating).
     - Non-linear secant fluid bulk modulus beta(p, T) modeled dynamically across 20.0 to 70.0 deg C
       and 1.0 to 400.0 bar: beta = beta_0 + m_bulk * p - k_T * (T - T_0).
     - Trapped High-Pressure Fluid Volume: V_total ~ 38,500 L, storing > 42 MJ of elastic energy.
     - Controlled multi-stage decompression ramp limits dp/dt <= 650.0 bar/s to prevent hydraulic
       water-hammer cavitation, catastrophic pipe-flange rupture, and pre-fill valve chatter.

  3. Cyber-Physical Receding-Horizon MPC Tilt Leveling:
     - Asymmetric forging deformation and flash gutter resistance create eccentric tipping moments
       (M_pitch, M_roll) exceeding 15,000 kNm, inducing severe ram tilt.
     - MPC algorithm evaluates discrete state-space predictions (x[k+1] = A*x[k] + B*u[k]) over an
       8-state x 6-input formulation to modulate 4 high-speed servo proportional valves (frequency
       response -3 dB at 85 Hz), achieving sub-millimeter ram tilt (< 0.10 mm/m) under 40,000 Ton.

  4. Triple Modular Redundancy (2oo3) Sensor Voting:
     - Ram Corner Displacements: 4 corners x 3 redundant magnetostrictive SSI linear transducers.
     - Cylinder Hydraulic Pressures: 4 corners x 3 redundant 600-bar piezoresistive transmitters.
     - Tie-Rod Column Forging Tonnage: 4 corners x 3 redundant semiconductor strain gauge bridges.
     - Accumulator Station Pressure: 3 redundant ceramic diaphragm sensors.
     - Accumulator N2 Pre-Charge Bottles: 3 redundant piezoresistive transmitters.
     - Lower Die Ejector Pin Displacements: 3 redundant linear LVDTs.
     - Full discrepancy timing, bumpless degradation to 1oo2, and fail-safe latching.

  5. Dynamic Forging Cycle FSM:
     - States: 0 (IDLE), 10 (PERMISSIVE CHECK), 20 (RAPID GRAVITY APPROACH PREFILL),
       30 (PRE-CONTACT DECEL & ACCUMULATOR PRIMING), 40 (HIGH-PRESSURE FORGING PENETRATION),
       50 (TONNAGE DWELL & RECRYSTALLIZATION HOLD), 60 (CONTROLLED S-CURVE DECOMPRESSION),
       70 (DECOMPRESSION CONFIRMATION & PRE-FILL OPEN), 80 (RAPID RAM RETRACTION),
       90 (TDC CUSHION & MECHANICAL WEDGE LOCK), 100 (PULSED EJECTOR PIN CYCLE),
       110 (SCALE BLOWOFF & DIE LUBE), 999 (EMERGENCY SAFETY DUMP).

  6. ISA-18.2 Multi-Tiered Alarm Matrix:
     - HH, H, L, LL alarms with deadband hysteresis, bit-packed into status and diagnostic words.
 ==========================================================================================
*)
VAR_INPUT
    (* ===================================================================================== *)
    (* 1. 2oo3 TMR RAM POSITION SENSORS (MAGNETOSTRICTIVE SSI ENCODERS)                     *)
    (* ===================================================================================== *)
    rPos_Corner1_SensorA_mm         : REAL;     (* Ram Corner 1 (FL) Displacement Ch A [mm] *)
    rPos_Corner1_SensorB_mm         : REAL;     (* Ram Corner 1 (FL) Displacement Ch B [mm] *)
    rPos_Corner1_SensorC_mm         : REAL;     (* Ram Corner 1 (FL) Displacement Ch C [mm] *)
    rPos_Corner2_SensorA_mm         : REAL;     (* Ram Corner 2 (FR) Displacement Ch A [mm] *)
    rPos_Corner2_SensorB_mm         : REAL;     (* Ram Corner 2 (FR) Displacement Ch B [mm] *)
    rPos_Corner2_SensorC_mm         : REAL;     (* Ram Corner 2 (FR) Displacement Ch C [mm] *)
    rPos_Corner3_SensorA_mm         : REAL;     (* Ram Corner 3 (RR) Displacement Ch A [mm] *)
    rPos_Corner3_SensorB_mm         : REAL;     (* Ram Corner 3 (RR) Displacement Ch B [mm] *)
    rPos_Corner3_SensorC_mm         : REAL;     (* Ram Corner 3 (RR) Displacement Ch C [mm] *)
    rPos_Corner4_SensorA_mm         : REAL;     (* Ram Corner 4 (RL) Displacement Ch A [mm] *)
    rPos_Corner4_SensorB_mm         : REAL;     (* Ram Corner 4 (RL) Displacement Ch B [mm] *)
    rPos_Corner4_SensorC_mm         : REAL;     (* Ram Corner 4 (RL) Displacement Ch C [mm] *)

    (* ===================================================================================== *)
    (* 2. 2oo3 TMR HYDRAULIC CYLINDER PRESSURES (HIGH-FREQUENCY PIEZORESISTIVE)              *)
    (* ===================================================================================== *)
    rPress_Cyl1_SensorA_bar         : REAL;     (* Main Cylinder 1 Chamber Pressure Ch A [bar] *)
    rPress_Cyl1_SensorB_bar         : REAL;     (* Main Cylinder 1 Chamber Pressure Ch B [bar] *)
    rPress_Cyl1_SensorC_bar         : REAL;     (* Main Cylinder 1 Chamber Pressure Ch C [bar] *)
    rPress_Cyl2_SensorA_bar         : REAL;     (* Main Cylinder 2 Chamber Pressure Ch A [bar] *)
    rPress_Cyl2_SensorB_bar         : REAL;     (* Main Cylinder 2 Chamber Pressure Ch B [bar] *)
    rPress_Cyl2_SensorC_bar         : REAL;     (* Main Cylinder 2 Chamber Pressure Ch C [bar] *)
    rPress_Cyl3_SensorA_bar         : REAL;     (* Main Cylinder 3 Chamber Pressure Ch A [bar] *)
    rPress_Cyl3_SensorB_bar         : REAL;     (* Main Cylinder 3 Chamber Pressure Ch B [bar] *)
    rPress_Cyl3_SensorC_bar         : REAL;     (* Main Cylinder 3 Chamber Pressure Ch C [bar] *)
    rPress_Cyl4_SensorA_bar         : REAL;     (* Main Cylinder 4 Chamber Pressure Ch A [bar] *)
    rPress_Cyl4_SensorB_bar         : REAL;     (* Main Cylinder 4 Chamber Pressure Ch B [bar] *)
    rPress_Cyl4_SensorC_bar         : REAL;     (* Main Cylinder 4 Chamber Pressure Ch C [bar] *)

    (* ===================================================================================== *)
    (* 3. 2oo3 TMR TIE-ROD COLUMN LOAD CELLS (DUAL-BRIDGE FOIL STRAIN GAUGES)               *)
    (* ===================================================================================== *)
    rLoad_Corner1_SensorA_kN        : REAL;     (* Tie-Rod 1 Tensile Force Ch A [kN] *)
    rLoad_Corner1_SensorB_kN        : REAL;     (* Tie-Rod 1 Tensile Force Ch B [kN] *)
    rLoad_Corner1_SensorC_kN        : REAL;     (* Tie-Rod 1 Tensile Force Ch C [kN] *)
    rLoad_Corner2_SensorA_kN        : REAL;     (* Tie-Rod 2 Tensile Force Ch A [kN] *)
    rLoad_Corner2_SensorB_kN        : REAL;     (* Tie-Rod 2 Tensile Force Ch B [kN] *)
    rLoad_Corner2_SensorC_kN        : REAL;     (* Tie-Rod 2 Tensile Force Ch C [kN] *)
    rLoad_Corner3_SensorA_kN        : REAL;     (* Tie-Rod 3 Tensile Force Ch A [kN] *)
    rLoad_Corner3_SensorB_kN        : REAL;     (* Tie-Rod 3 Tensile Force Ch B [kN] *)
    rLoad_Corner3_SensorC_kN        : REAL;     (* Tie-Rod 3 Tensile Force Ch C [kN] *)
    rLoad_Corner4_SensorA_kN        : REAL;     (* Tie-Rod 4 Tensile Force Ch A [kN] *)
    rLoad_Corner4_SensorB_kN        : REAL;     (* Tie-Rod 4 Tensile Force Ch B [kN] *)
    rLoad_Corner4_SensorC_kN        : REAL;     (* Tie-Rod 4 Tensile Force Ch C [kN] *)

    (* ===================================================================================== *)
    (* 4. 2oo3 TMR ACCUMULATOR & AUXILIARY HYDRAULIC PRESSURE TRANSMITTERS                 *)
    (* ===================================================================================== *)
    rPress_AccSupply_SensorA_bar    : REAL;     (* High-Pressure Accumulator Bank Header Ch A [bar] *)
    rPress_AccSupply_SensorB_bar    : REAL;     (* High-Pressure Accumulator Bank Header Ch B [bar] *)
    rPress_AccSupply_SensorC_bar    : REAL;     (* High-Pressure Accumulator Bank Header Ch C [bar] *)
    rPress_N2Precharge_SensorA_bar  : REAL;     (* Accumulator Nitrogen Bottle Precharge Ch A [bar] *)
    rPress_N2Precharge_SensorB_bar  : REAL;     (* Accumulator Nitrogen Bottle Precharge Ch B [bar] *)
    rPress_N2Precharge_SensorC_bar  : REAL;     (* Accumulator Nitrogen Bottle Precharge Ch C [bar] *)
    rPress_DecompHeader_SensorA_bar : REAL;     (* Decompression Return Line Pressure Ch A [bar] *)
    rPress_DecompHeader_SensorB_bar : REAL;     (* Decompression Return Line Pressure Ch B [bar] *)
    rPress_DecompHeader_SensorC_bar : REAL;     (* Decompression Return Line Pressure Ch C [bar] *)

    (* ===================================================================================== *)
    (* 5. 2oo3 TMR LOWER DIE HYDRAULIC EJECTOR PIN SENSORS                                  *)
    (* ===================================================================================== *)
    rPos_EjectorPin_SensorA_mm      : REAL;     (* Ejector Pin Hydraulic Stroke Ch A [mm] *)
    rPos_EjectorPin_SensorB_mm      : REAL;     (* Ejector Pin Hydraulic Stroke Ch B [mm] *)
    rPos_EjectorPin_SensorC_mm      : REAL;     (* Ejector Pin Hydraulic Stroke Ch C [mm] *)
    rPress_EjectorHyd_SensorA_bar   : REAL;     (* Ejector Cylinder Push Pressure Ch A [bar] *)
    rPress_EjectorHyd_SensorB_bar   : REAL;     (* Ejector Cylinder Push Pressure Ch B [bar] *)
    rPress_EjectorHyd_SensorC_bar   : REAL;     (* Ejector Cylinder Push Pressure Ch C [bar] *)

    (* ===================================================================================== *)
    (* 6. HYDRAULIC SYSTEM TELEMETRY & VALVE SPOOL FEEDBACK                                 *)
    (* ===================================================================================== *)
    rTemp_HydraulicFluid_degC       : REAL;     (* Main Hydraulic Fluid Reservoir Temperature [deg C] *)
    rPress_FilterDeltaP_bar         : REAL;     (* High-Pressure Fluid Filter Differential Pressure [bar] *)
    rSpool_ServoValve1_Feedback_pct : REAL;     (* Corner 1 Proportional Servo Spool LVDT Feedback [%] *)
    rSpool_ServoValve2_Feedback_pct : REAL;     (* Corner 2 Proportional Servo Spool LVDT Feedback [%] *)
    rSpool_ServoValve3_Feedback_pct : REAL;     (* Corner 3 Proportional Servo Spool LVDT Feedback [%] *)
    rSpool_ServoValve4_Feedback_pct : REAL;     (* Corner 4 Proportional Servo Spool LVDT Feedback [%] *)
    rStroke_PrefillValve_Feedback_pct:REAL;     (* Overhead Tank Pilot Pre-fill Poppet Stroke Feedback [%] *)
    rSpool_DecompValve_Feedback_pct : REAL;     (* Active Decompression Proportional Valve Spool [%] *)

    (* ===================================================================================== *)
    (* 7. OPERATOR RECIPE SETPOINTS & KINEMATIC TARGETS                                     *)
    (* ===================================================================================== *)
    rTargetPressTonnage_Ton         : REAL;     (* Final Forging Clamping Tonnage Target [Ton] *)
    rTargetBottomDeadCenter_mm      : REAL;     (* Target Bottom Dead Center Penetration Depth [mm] *)
    rTargetApproachSpeed_mms        : REAL;     (* Rapid Gravity Descent Speed Setpoint [mm/s] *)
    rTargetForgingSpeed_mms         : REAL;     (* High-Pressure Forging Penetration Speed [mm/s] *)
    rTargetRetractSpeed_mms         : REAL;     (* Ram Upward Return Retract Speed [mm/s] *)
    rTargetDwellDuration_s          : REAL;     (* Isothermal Forging Tonnage Dwell Duration [s] *)
    rTargetDecompDuration_s         : REAL;     (* Active S-Curve Decompression Ramp Time [s] *)
    rMaxPermissibleTilt_Pitch_mmm   : REAL;     (* Maximum Allowable Pitch Tilt Threshold [mm/m] *)
    rMaxPermissibleTilt_Roll_mmm    : REAL;     (* Maximum Allowable Roll Tilt Threshold [mm/m] *)
    rTargetEjectorStroke_mm         : REAL;     (* Lower Die Ejector Part Extraction Stroke [mm] *)
    nTargetEjectorPulses            : INT;      (* Number of Hydraulic Ejection Vibration Pulses [-] *)
    rEjectorPulseFrequency_Hz       : REAL;     (* Ejector Hydraulic Pulsing Frequency [Hz] *)
    rBilletPyrometerTemp_degC       : REAL;     (* Infrared Pyrometer Heated Billet Surface Temp [deg C] *)
    rBilletMinForgingTemp_degC      : REAL;     (* Minimum Allowable Billet Forging Temp [deg C] *)

    (* ===================================================================================== *)
    (* 8. DISCRETE PERMISSIVES & SAFETY INTERLOCKS                                          *)
    (* ===================================================================================== *)
    bEnablePressCycle               : BOOL;     (* Master Press Enable Permissive Flag *)
    bAutoCycleStart                 : BOOL;     (* Automatic Single-Cycle Start Pushbutton *)
    bEmergencyStop_NC               : BOOL;     (* Hardwired Fail-Safe E-Stop PB (Normally Closed: 1=OK, 0=Trip) *)
    bSafetyLightCurtainClear        : BOOL;     (* Perimeter Optical Safety Light Curtain Muted/Clear *)
    bDieSafetyShieldClosed          : BOOL;     (* Hydraulic Ballistic Shrapnel Protective Shield Closed *)
    bBilletLoadedConfirmed          : BOOL;     (* Vision / Laser In-Die Billet Seating Confirmation *)
    bDieLubricationCycleDone        : BOOL;     (* Graphite Die Lubricant Robot Cycle Finished *)
    bHydraulicPumpsRunning          : BOOL;     (* Main Variable-Displacement High-Pressure Pumps On *)
    bAccumulatorChargePermissive    : BOOL;     (* Accumulator Charging Manifold Ready *)
    bResetFaults                    : BOOL;     (* Operator Alarm Reset and Latched Fault Clear PB *)
    bManualJogRamUp                 : BOOL;     (* Manual Maintenance Jog Ram Retract *)
    bManualJogRamDown               : BOOL;     (* Manual Maintenance Jog Ram Advance *)
END_VAR

VAR_OUTPUT
    (* ===================================================================================== *)
    (* 1. ANALOG & MODULATING VALVE COMMANDS                                                *)
    (* ===================================================================================== *)
    rCmdServoValve1_pct             : REAL;     (* Corner 1 Proportional Servo Spool Command [%] *)
    rCmdServoValve2_pct             : REAL;     (* Corner 2 Proportional Servo Spool Command [%] *)
    rCmdServoValve3_pct             : REAL;     (* Corner 3 Proportional Servo Spool Command [%] *)
    rCmdServoValve4_pct             : REAL;     (* Corner 4 Proportional Servo Spool Command [%] *)
    rCmdPrefillValvePilot_pct       : REAL;     (* Pilot-Operated Pre-Fill Poppet Opening Command [%] *)
    rCmdDecompressionValve_pct      : REAL;     (* Multi-Stage S-Curve Decompression Valve Command [%] *)
    rCmdRetractCylinders_pct        : REAL;     (* High-Speed Ram Pullback Retract Cylinders [%] *)
    rCmdEjectorPinValve_pct         : REAL;     (* Lower Die Ejector Proportional Valve Command [%] *)
    rCmdGraphiteSprayAir_pct        : REAL;     (* Atomized Graphite Die Lubrication Proportional Air [%] *)
    rCmdDescalingBlast_pct          : REAL;     (* High-Pressure Billet Water/Air Descaling Blast [%] *)

    (* ===================================================================================== *)
    (* 2. DISCRETE SAFETY & DIRECTIONAL SOLENOID ACTUATION                                  *)
    (* ===================================================================================== *)
    bCmdMechanicalWedgeLocksRetract : BOOL;     (* Top Dead Center Hydraulic Safety Wedge Retract Solenoid *)
    bCmdMainAccumulatorIsolationOpen: BOOL;     (* High-Pressure Accumulator Bank Isolation Gate Solenoid *)
    bCmdEmergencyDecompressionDump  : BOOL;     (* Fail-Safe Emergency Hydraulic Fast Dump Valve *)
    bCmdPumpUnloadCirculation       : BOOL;     (* Main Hydraulic Pump High-Pressure Unload Bypass Solenoid *)
    bCmdCoolingRecirculationValve   : BOOL;     (* Oil Cooler Recirculation Heat Exchanger Pump *)

    (* ===================================================================================== *)
    (* 3. SYSTEM TELEMETRY, OBSERVERS & CYBER-PHYSICAL ESTIMATIONS                          *)
    (* ===================================================================================== *)
    rActualAverageRamPos_mm         : REAL;     (* Real-time Center-of-Ram Vertical Position [mm] *)
    rActualRamVelocity_mms          : REAL;     (* Filtered Numerical Derivative Ram Velocity [mm/s] *)
    rActualRamTilt_Pitch_mmm        : REAL;     (* Dynamic Ram Pitch Tilt Angle Differential [mm/m] *)
    rActualRamTilt_Roll_mmm         : REAL;     (* Dynamic Ram Roll Tilt Angle Differential [mm/m] *)
    rActualTotalPressTonnage_Ton    : REAL;     (* Summed 4-Corner Tie-Rod Press Tonnage [Ton] *)
    rActualEccentricMoment_Pitch_kNm: REAL;     (* Off-Center Forging Load Tipping Moment Pitch Axis [kNm] *)
    rActualEccentricMoment_Roll_kNm : REAL;     (* Off-Center Forging Load Tipping Moment Roll Axis [kNm] *)
    rActualFluidBulkModulus_bar     : REAL;     (* Dynamic Real-Time Fluid Bulk Modulus beta(p, T) [bar] *)
    rActualDecompressionRate_bars   : REAL;     (* High-Frequency Pressure Decay Gradient dp/dt [bar/s] *)
    rMPC_ObjectiveCost_J            : REAL;     (* Receding-Horizon Leveling Quadratic Cost Metric [-] *)
    rCycleDurationTimer_s           : REAL;     (* Total Forging Cycle Execution Timer [s] *)

    (* ===================================================================================== *)
    (* 4. OPERATIONAL STATUS WORDS & ISA-18.2 ALARM PACKING                                 *)
    (* ===================================================================================== *)
    bSystemOperationalReady         : BOOL;     (* All Interlocks Satisfied, Accumulator Primed, Ready *)
    bPressCycleRunning              : BOOL;     (* Automated Forging Sequence In Active Execution *)
    bRamInTonnageDwell              : BOOL;     (* Pressing Holding Full Setpoint Tonnage at BDC *)
    bDecompressionCompleted         : BOOL;     (* Controlled Multi-Stage Decompression Completed *)
    bRamAtTopDeadCenter             : BOOL;     (* Ram Locked at Top Dead Center Home *)
    bEjectorSequenceComplete        : BOOL;     (* Lower Die Ejection Sequence Completed *)
    bSystemSafetyTripActive         : BOOL;     (* Critical Safety Trip Active, Hydraulics Dumped *)
    nActiveFSMState                 : INT;      (* Current Numeric State of Forging Finite State Machine *)
    dwOperationalStatusWord         : DWORD;    (* Bit-Packed Press Telemetry & Subsystem State *)
    dwAlarmStatusWord_1             : DWORD;    (* ISA-18.2 Critical Emergency Safety Trips [Bit-Packed] *)
    dwAlarmStatusWord_2             : DWORD;    (* ISA-18.2 Process Warnings & Leveling Tolerances [Bit-Packed] *)
    dwDegradationWord               : DWORD;    (* 2oo3 TMR Sensor Degradation & Channel Fallback Status *)
END_VAR

VAR
    (* ===================================================================================== *)
    (* 1. DISCRETE STATE-SPACE MODEL MATRICES & VECTORS (8 STATES x 6 INPUTS)               *)
    (* ===================================================================================== *)
    (* State Vector x[k]:
       x[1] = rActualAverageRamPos_mm        (Ram Vertical Position, [mm])
       x[2] = rActualRamVelocity_mms         (Ram Vertical Velocity, [mm/s])
       x[3] = rActualRamTilt_Pitch_mmm       (Ram Pitch Angle Differential, [mm/m])
       x[4] = rActualRamTilt_Roll_mmm        (Ram Roll Angle Differential, [mm/m])
       x[5] = rVotedPress_Cyl1_bar           (Corner 1 Chamber Pressure, [bar])
       x[6] = rVotedPress_Cyl2_bar           (Corner 2 Chamber Pressure, [bar])
       x[7] = rVotedPress_Cyl3_bar           (Corner 3 Chamber Pressure, [bar])
       x[8] = rVotedPress_Cyl4_bar           (Corner 4 Chamber Pressure, [bar])
       Control Vector u[k]:
       u[1] = rCmdServoValve1_pct            (Corner 1 Servo Valve Command, [%])
       u[2] = rCmdServoValve2_pct            (Corner 2 Servo Valve Command, [%])
       u[3] = rCmdServoValve3_pct            (Corner 3 Servo Valve Command, [%])
       u[4] = rCmdServoValve4_pct            (Corner 4 Servo Valve Command, [%])
       u[5] = rCmdPrefillValvePilot_pct      (Pilot Pre-Fill Poppet Opening, [%])
       u[6] = rCmdDecompressionValve_pct     (Active Decompression Valve, [%])
    *)
    rA_Matrix                       : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Transition Matrix *)
    rB_Matrix                       : ARRAY[1..8, 1..6] OF REAL; (* Discrete Input Coupling Matrix *)
    rC_Matrix                       : ARRAY[1..8, 1..8] OF REAL; (* Output Observation Matrix *)
    rD_Matrix                       : ARRAY[1..8, 1..6] OF REAL; (* Direct Feedthrough Matrix *)

    rStateVector_x                  : ARRAY[1..8] OF REAL;       (* Current Discrete System State Vector *)
    rStateTarget_r                  : ARRAY[1..8] OF REAL;       (* Reference Setpoint State Vector *)
    rStateError_e                   : ARRAY[1..8] OF REAL;       (* State Tracking Error e[k] = x[k] - r[k] *)
    rStateVector_xNext              : ARRAY[1..8] OF REAL;       (* Forward Predicted State x[k+1] *)

    (* MPC Cost Weightings & Optimization Tuning *)
    rQ_DiagWeights                  : ARRAY[1..8] OF REAL;       (* State Error Quadratic Penalty Weights *)
    rR_DiagWeights                  : ARRAY[1..6] OF REAL;       (* Actuator Effort Quadratic Penalty Weights *)
    rP_TerminalWeights              : ARRAY[1..8] OF REAL;       (* Terminal State Error Quadratic Penalty *)
    rS_SlewWeights                  : ARRAY[1..6] OF REAL;       (* Control Rate of Change (Slew) Penalty *)

    rControlVector_u                : ARRAY[1..6] OF REAL;       (* Current Optimization Control Vector *)
    rControlVector_uPrev            : ARRAY[1..6] OF REAL;       (* Previous Cycle Control Vector u[k-1] *)
    rGradient_J                     : ARRAY[1..6] OF REAL;       (* Cost Gradient Vector del_J / del_u *)
    rDeltaU_SlewLimit               : ARRAY[1..6] OF REAL;       (* Maximum Permissible Slew Step per ms *)
    rU_UpperBound                   : ARRAY[1..6] OF REAL;       (* Actuator Hard Saturation Maximum *)
    rU_LowerBound                   : ARRAY[1..6] OF REAL;       (* Actuator Hard Saturation Minimum *)

    rMPC_StepGain                   : REAL;                      (* Gradient Descent Optimization Step Size *)
    rSumTempMatrix                  : REAL;                      (* Scratch Accumulator for Matrix Multiply *)
    rCostStatePenalty               : REAL;                      (* State Error Cost Component *)
    rCostActuatorPenalty            : REAL;                      (* Actuator Effort Cost Component *)
    rCostSlewPenalty                : REAL;                      (* Actuator Slew Rate Cost Component *)

    (* Active Leveling Trim Computations *)
    rTrimPitch_P                    : REAL;                      (* Pitch Proportional Tilt Trim *)
    rTrimPitch_D                    : REAL;                      (* Pitch Derivative Tilt Trim *)
    rTrimRoll_P                     : REAL;                      (* Roll Proportional Tilt Trim *)
    rTrimRoll_D                     : REAL;                      (* Roll Derivative Tilt Trim *)
    rPrevTiltPitch                  : REAL;                      (* Prior Cycle Pitch Tilt for Derivative *)
    rPrevTiltRoll                   : REAL;                      (* Prior Cycle Roll Tilt for Derivative *)
    rDeltaTiltPitch_dt              : REAL;                      (* Tilt Rate of Change Pitch [mm/(m*s)] *)
    rDeltaTiltRoll_dt               : REAL;                      (* Tilt Rate of Change Roll [mm/(m*s)] *)
    rBaseAdvanceCmd_pct             : REAL;                      (* Base Synchronous Advance Command [%] *)

    (* ===================================================================================== *)
    (* 2. 2oo3 TMR SENSOR VOTING STRUCTURES, DISCREPANCY TIMERS & HEALTH FLAGS              *)
    (* ===================================================================================== *)
    (* Voted Sensor Signal Registers *)
    rVotedPos_Corner1_mm            : REAL;
    rVotedPos_Corner2_mm            : REAL;
    rVotedPos_Corner3_mm            : REAL;
    rVotedPos_Corner4_mm            : REAL;

    rVotedPress_Cyl1_bar            : REAL;
    rVotedPress_Cyl2_bar            : REAL;
    rVotedPress_Cyl3_bar            : REAL;
    rVotedPress_Cyl4_bar            : REAL;

    rVotedLoad_Corner1_kN           : REAL;
    rVotedLoad_Corner2_kN           : REAL;
    rVotedLoad_Corner3_kN           : REAL;
    rVotedLoad_Corner4_kN           : REAL;

    rVotedPress_AccSupply_bar       : REAL;
    rVotedPress_N2Precharge_bar     : REAL;
    rVotedPress_DecompHeader_bar    : REAL;
    rVotedPos_EjectorPin_mm         : REAL;
    rVotedPress_EjectorHyd_bar      : REAL;

    (* Discrepancy Thresholds & Timers [ms] *)
    rDiscrepancyThresholdPos_mm     : REAL;
    rDiscrepancyThresholdPress_bar  : REAL;
    rDiscrepancyThresholdLoad_kN    : REAL;
    rDiscrepancyThresholdAcc_bar    : REAL;

    nTimerDiscrepancy_PosC1         : INT;
    nTimerDiscrepancy_PosC2         : INT;
    nTimerDiscrepancy_PosC3         : INT;
    nTimerDiscrepancy_PosC4         : INT;

    nTimerDiscrepancy_PressC1       : INT;
    nTimerDiscrepancy_PressC2       : INT;
    nTimerDiscrepancy_PressC3       : INT;
    nTimerDiscrepancy_PressC4       : INT;

    nTimerDiscrepancy_LoadC1        : INT;
    nTimerDiscrepancy_LoadC2        : INT;
    nTimerDiscrepancy_LoadC3        : INT;
    nTimerDiscrepancy_LoadC4        : INT;

    nTimerDiscrepancy_AccSupply     : INT;
    nTimerDiscrepancy_N2Precharge   : INT;
    nTimerDiscrepancy_Decomp        : INT;
    nTimerDiscrepancy_Ejector       : INT;

    (* Health & Degradation Status Flags *)
    bHealthy_PosC1                  : BOOL;
    bHealthy_PosC2                  : BOOL;
    bHealthy_PosC3                  : BOOL;
    bHealthy_PosC4                  : BOOL;

    bHealthy_PressC1                : BOOL;
    bHealthy_PressC2                : BOOL;
    bHealthy_PressC3                : BOOL;
    bHealthy_PressC4                : BOOL;

    bHealthy_LoadC1                 : BOOL;
    bHealthy_LoadC2                 : BOOL;
    bHealthy_LoadC3                 : BOOL;
    bHealthy_LoadC4                 : BOOL;

    bHealthy_AccSupply              : BOOL;
    bHealthy_N2Precharge            : BOOL;
    bHealthy_Decomp                 : BOOL;
    bHealthy_Ejector                : BOOL;

    bDegraded_PosAny                : BOOL;
    bDegraded_PressAny              : BOOL;
    bDegraded_LoadAny               : BOOL;
    bDegraded_AccAny                : BOOL;

    (* TMR Scratch Variables for Sorting and Median Selection *)
    rTMR_A                          : REAL;
    rTMR_B                          : REAL;
    rTMR_C                          : REAL;
    rTMR_DiffAB                     : REAL;
    rTMR_DiffBC                     : REAL;
    rTMR_DiffCA                     : REAL;
    rTMR_MedianResult               : REAL;

    (* ===================================================================================== *)
    (* 3. FLUID BULK MODULUS & THERMODYNAMIC COMPRESSIBILITY PROPERTIES                     *)
    (* ===================================================================================== *)
    rFluidBulkModulus_0_bar         : REAL;     (* Base Bulk Modulus at 1 bar, 20 deg C [bar] *)
    rBulkPressureSlope_m            : REAL;     (* Pressure Stiffening Coefficient m [-] *)
    rBulkTempSlope_kT               : REAL;     (* Thermal Softening Coefficient k_T [bar/deg C] *)
    rTrappedFluidVolume_L           : REAL;     (* Total Volume of High-Pressure Hydraulic Fluid [L] *)
    rCompressedElasticStrainDeltaV_L: REAL;     (* Elastic Compressed Fluid Volume Delta V [L] *)
    rStoredElasticEnergy_MJ         : REAL;     (* Trapped Stored Elastic Strain Energy [MJ] *)

    (* Numerical Filtering Registers for Velocity & Decompression Rate *)
    rPrevAverageRamPos_mm           : REAL;     (* Position at Cycle k-1 [mm] *)
    rPrevAverageCylPress_bar        : REAL;     (* Chamber Pressure at Cycle k-1 [bar] *)
    rRawRamVelocity_mms             : REAL;     (* Unfiltered Velocity [mm/s] *)
    rRawDecompressionRate_bars      : REAL;     (* Unfiltered dp/dt [bar/s] *)

    (* ===================================================================================== *)
    (* 4. DYNAMIC FORGING FINITE STATE MACHINE (FSM) TIMERS & SEQUENCING                    *)
    (* ===================================================================================== *)
    nFSMState                       : INT;      (* Internal State Code *)
    nNextFSMState                   : INT;      (* Next State Pending Transition *)
    nFSMStateTimer_ms               : DINT;     (* Dwell/State Elapsed Milliseconds [ms] *)
    nDwellTimer_ms                  : DINT;     (* High-Pressure Tonnage Dwell Timer [ms] *)
    nDecompTimer_ms                 : DINT;     (* Decompression S-Curve Timer [ms] *)
    nEjectorPulseCounter            : INT;      (* Active Pulse Count for Ejector Pins [-] *)
    nEjectorPeriodTimer_ms          : INT;      (* Ejector Frequency Sub-Timer [ms] *)
    bEjectorStrokeExtend            : BOOL;     (* Ejector Pulse Direction Flip-Flop *)
    nScaleBlastTimer_ms             : INT;      (* Scale Blowoff Air Solenoid Timer [ms] *)
    nDieLubeTimer_ms                : INT;      (* Graphite Spray Atomizer Timer [ms] *)
    bCycleCompletedLatch            : BOOL;     (* Single-Cycle Done Memory Bit *)

    (* S-Curve Decompression Mathematical Profile *)
    rDecompNormTime_tau             : REAL;     (* Normalized Time tau = t / t_decomp [0.0..1.0] *)
    rDecompPressureTarget_bar       : REAL;     (* Analytical Target Pressure Curve p(t) [bar] *)
    rDecompStartPressure_bar        : REAL;     (* Cylinder Pressure at Inception of Decompression [bar] *)

    (* ===================================================================================== *)
    (* 5. ISA-18.2 ALARM THRESHOLDS, DEADBANDS, TIMERS & LATCHES                            *)
    (* ===================================================================================== *)
    (* Threshold Definitions *)
    rLimit_PressSupply_HH_bar       : REAL;
    rLimit_PressSupply_H_bar        : REAL;
    rLimit_PressSupply_L_bar        : REAL;
    rLimit_PressSupply_LL_bar       : REAL;

    rLimit_TiltPitch_HH_mmm         : REAL;
    rLimit_TiltPitch_H_mmm          : REAL;
    rLimit_TiltRoll_HH_mmm          : REAL;
    rLimit_TiltRoll_H_mmm           : REAL;

    rLimit_EccentricMoment_HH_kNm   : REAL;
    rLimit_N2Precharge_LL_bar       : REAL;
    rLimit_N2Precharge_L_bar        : REAL;

    rLimit_FluidTemp_HH_degC        : REAL;
    rLimit_FluidTemp_H_degC         : REAL;
    rLimit_FilterDeltaP_HH_bar      : REAL;
    rLimit_FilterDeltaP_H_bar       : REAL;

    rLimit_DecompShock_HH_bars      : REAL;

    (* Deadbands *)
    rAlarmDeadband_Press_bar        : REAL;
    rAlarmDeadband_Tilt_mmm         : REAL;
    rAlarmDeadband_Temp_degC        : REAL;

    (* Latched Alarm Bits *)
    bAlarm_PressSupply_HH           : BOOL;
    bAlarm_PressSupply_H            : BOOL;
    bAlarm_PressSupply_L            : BOOL;
    bAlarm_PressSupply_LL           : BOOL;

    bAlarm_TiltPitch_HH             : BOOL;
    bAlarm_TiltPitch_H              : BOOL;
    bAlarm_TiltRoll_HH              : BOOL;
    bAlarm_TiltRoll_H               : BOOL;

    bAlarm_EccentricMoment_HH       : BOOL;
    bAlarm_N2Precharge_LL           : BOOL;
    bAlarm_N2Precharge_L            : BOOL;

    bAlarm_FluidTemp_HH             : BOOL;
    bAlarm_FluidTemp_H              : BOOL;
    bAlarm_FilterDeltaP_HH          : BOOL;
    bAlarm_FilterDeltaP_H           : BOOL;

    bAlarm_DecompShock_HH           : BOOL;
    bAlarm_EStop_Trip               : BOOL;
    bAlarm_LightCurtain_Breach      : BOOL;
    bAlarm_BilletUnderTemp_Trip     : BOOL;
    bAlarm_EjectorStall_Trip        : BOOL;

    (* General Purpose Loop Counters *)
    i                               : INT;
    j                               : INT;
    bFirstScanDone                  : BOOL;
END_VAR
""")
    return "".join(parts)

print("Part 1 builder compiled successfully.")
