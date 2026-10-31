# Generator script for FB_Mining_SAGMill_BallMill_GrindingCircuit
# Target: data/swarm_raw/agent_4b8109d1.json

import json
import os
import sys

def get_user_prompt():
    return """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Heavy Mining & Mineral Processing: 40-Foot Semi-Autogenous Grinding (SAG) Mill & Closed-Circuit Ball Mill with Dual-Pinion Synchronous Drives, Hydrocyclone Battery & Acoustic Toe-Angle Tracking**

Technical Cyber-Physical Depth:
- 40-ft SAG Mill (28 MW dual-pinion synchronous drive) + 26-ft Ball Mill in closed circuit with a 14-pack hydrocyclone battery.
- Dual-pinion load-sharing closed loop regulating torque balance between Master and Slave pinions (< 0.5% differential torque) to prevent gear tooth pitting and fatigue fracture.
- Mill charge dynamic volume & density estimation using acoustic impact microphone arrays and bearing hydrostatic trunnion lift oil pressure transmitters to locate the charge "toe" and "shoulder" angles in real time (preventing liner ball damage during underload and slurry pooling during overload).
- Slurry rheology & water addition control: Variable-frequency sump pump, nuclear density gauge, and magnetic flowmeters feeding the hydrocyclone battery with automated cyclopac knife-gate valve staging to maintain overflow particle size distribution (P80 = 75 microns).
- Discrete State-Space Model (14x14 state matrix A, 14x8 B, C, D) incorporating Austin comminution breakage kinetics, slurry hydrodynamic transport, hydrostatic bearing film stiffness, and motor winding thermal dynamics.
- Receding-horizon MPC for SAG mill feed ore rate pacing (apron feeder speed), water ratio regulation, and cyclone feed pump pressure optimization.
- 2oo3 Triple Modular Redundancy (TMR) voting across trunnion bearing hydrostatic pressures, vibration accelerometers, mill acoustic microphones, and nuclear slurry density gauges.
- 12-Stage Operational FSM (Hydrostatic Bearing Lubrication High-Pressure Jacking Verification, Mill Inching & Creep Rotation, Drive Synchronization & Soft Start Ramp, Slurry Sump Pre-Fill, SAG Feed Ore Introduction, Hydrocyclone Battery Staging, Closed-Loop MPC Grinding Steady State, Pebble Crusher Diverter Routing, Mill Washout & Grind-Out, Controlled Stop & Park on Brakes, Frozen Charge Detection Interlock, Emergency E-Stop Trip).
- ISA-18.2 multi-tiered alarm matrix (Trunnion bearing loss-of-lift HH, drive torque imbalance, frozen charge breakaway trip, cyclone roping warning, sump overflow risk) with bit-packed telemetry DWORDs.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named FB_Mining_SAGMill_BallMill_GrindingCircuit with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

def build_iec_code():
    parts = []

    # 1. Header
    parts.append("""FUNCTION_BLOCK FB_Mining_SAGMill_BallMill_GrindingCircuit
(*
 ==========================================================================================
  PROJECT:       COMMERCIAL HEAVY COMMINUTION & MINERAL PROCESSING CIRCUIT
  SUBSYSTEM:     40-FT SAG MILL (28 MW DUAL-PINION) & 26-FT BALL MILL CLOSED CIRCUIT
  EQUIPMENT:     14-PACK CYCLOPAC HYDROCYCLONE BATTERY, ACOUSTIC CHARGE TOE TRACKING
  DISCIPLINE:    CYBER-PHYSICAL MODEL PREDICTIVE CONTROL / AUSTIN KINETICS / 2oo3 TMR
  IEC STANDARD:  IEC 61131-3 3RD EDITION COMPLIANT (STRICT DETERMINISTIC STRUCTURED TEXT)
 ==========================================================================================
  CYBER-PHYSICAL PROCESS DESCRIPTION & ARCHITECTURAL FOUNDATION:
  This Function Block executes comprehensive, real-time deterministic cyber-physical control
  for a world-scale mineral processing comminution plant treating 4,000 t/h of porphyry copper-gold ore.
  The circuit incorporates:
   1. 40-ft x 24-ft Semi-Autogenous Grinding (SAG) Mill driven by dual 14 MW wound rotor induction
      motors (28 MW combined nameplate) equipped with variable frequency drives and high-precision
      dual-pinion load sharing to prevent mechanical gear fatigue, pitting, and backlash impact.
   2. 26-ft x 40-ft Closed-Circuit Secondary Ball Mill (16 MW drive power) processing SAG trommel
      undersize and hydrocyclone underflow to liberate fine target minerals.
   3. 14-Pack Hydrocyclone Battery (Cyclopac) fed by a common slurry discharge sump with variable-speed
      slurry pumps, nuclear density profiling, and automated knife-gate valve staging maintaining
      an overflow product grind of P80 = 75 microns.
   4. Austin Comminution Breakage Kinetics coupled with hydrodynamic slurry transport modeling
      and non-Newtonian Krieger-Dougherty rheological apparent viscosity behavior.
   5. Dynamic Mill Charge Acoustic & Trunnion Monitoring: Multi-microphone acoustic impact telemetry
      tracking the cascading charge "toe" angle and cataracting "shoulder" angle in real time to
      prevent catastrophic steel ball-on-liner impact during underload and slurry pooling during overload.
   6. Hydrostatic Trunnion Bearing Protection: Multi-channel high-pressure jacking oil verification,
      continuous oil film stiffness calculation, and hydrodynamic wedge thermal monitoring.
   7. 2oo3 Triple Modular Redundant (TMR) voting across trunnion lift oil pressures, vibration
      accelerometers, shell acoustic microphones, and nuclear slurry density transmitters.
   8. 12-Stage Operational Finite State Machine governing jacking permissive, frozen charge keying
      detection, soft-start synchronization, steady-state MPC grinding, pebble crusher routing,
      controlled slurry grind-out washout, and precision park-on-caliper-brakes.
   9. ISA-18.2 Compliant Multi-Tiered Alarm Matrix with deadband hysteresis, priority escalation,
      and bit-packed 32-bit DWORD telemetry registers.
 ==========================================================================================
*)
VAR_INPUT
    (* ================================================================================= *)
    (* SYSTEM SUPERVISORY COMMANDS & OPERATIONAL PERMISSIVES                             *)
    (* ================================================================================= *)
    bMasterEnable                   : BOOL;     (* Plant supervisory auto sequence enable [-] *)
    bEmergencyStop                  : BOOL;     (* Redundant hardwired SIL-3 emergency stop circuit healthy [-] *)
    bAckFaults                      : BOOL;     (* Alarm acknowledge and fault reset command pulse [-] *)
    bAutoModeSelect                 : BOOL;     (* Supervisory automatic MPC closed-loop control enable [-] *)
    bInchingModeSelect              : BOOL;     (* Low speed inching/creeping drive mode selector [-] *)
    bCrusherPermissive              : BOOL;     (* Downstream pebble crusher ready permissive [-] *)
    bPebbleBypassCommand            : BOOL;     (* Operator manual pebble diverter bypass command [-] *)
    bWashoutPermissive              : BOOL;     (* Circuit slurry washout sequence authorized [-] *)

    (* ================================================================================= *)
    (* PROCESS SETPOINTS WITH PHYSICAL ENGINEERING UNITS                                 *)
    (* ================================================================================= *)
    rOreFeedRateSp_t_h              : REAL;     (* Apron feeder total fresh ore mass flow setpoint [t/h] *)
    rSAGWaterRatioSp_m3_t           : REAL;     (* SAG mill feed water-to-ore volumetric ratio setpoint [m3/t] *)
    rBallMillWaterRatioSp_m3_t      : REAL;     (* Ball mill feed dilution water ratio setpoint [m3/t] *)
    rCycloneFeedDensitySp_t_m3      : REAL;     (* Hydrocyclone feed slurry target density setpoint [t/m3] *)
    rCycloneFeedPressSp_kPa         : REAL;     (* Hydrocyclone distributor header pressure setpoint [kPa] *)
    rSumpLevelSp_pct                : REAL;     (* Common mill discharge collection sump target level [%] *)
    rTargetP80_microns              : REAL;     (* Hydrocyclone overflow target 80% passing grind size [um] *)
    rSAGSpeedSp_PctCrit             : REAL;     (* SAG mill target rotational speed fraction of critical [% Nc] *)
    rBallMillSpeedSp_PctCrit        : REAL;     (* Ball mill target rotational speed fraction of critical [% Nc] *)
    rTargetToeAngleSp_deg           : REAL;     (* Desired SAG mill dynamic charge toe position setpoint [deg] *)
    rTargetShoulderAngleSp_deg      : REAL;     (* Desired SAG mill dynamic charge shoulder position [deg] *)

    (* ================================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) CRITICAL SAFETY SENSOR CHANNELS               *)
    (* ================================================================================= *)
    rSAG_TrunnionFeedPress_ChA_bar  : REAL;     (* SAG feed trunnion hydrostatic lift oil press Ch A [bar] *)
    rSAG_TrunnionFeedPress_ChB_bar  : REAL;     (* SAG feed trunnion hydrostatic lift oil press Ch B [bar] *)
    rSAG_TrunnionFeedPress_ChC_bar  : REAL;     (* SAG feed trunnion hydrostatic lift oil press Ch C [bar] *)
    rSAG_TrunnionDischPress_ChA_bar : REAL;     (* SAG disch trunnion hydrostatic lift press Ch A [bar] *)
    rSAG_TrunnionDischPress_ChB_bar : REAL;     (* SAG disch trunnion hydrostatic lift press Ch B [bar] *)
    rSAG_TrunnionDischPress_ChC_bar : REAL;     (* SAG disch trunnion hydrostatic lift press Ch C [bar] *)
    rBM_TrunnionFeedPress_ChA_bar   : REAL;     (* Ball mill feed trunnion lift press Ch A [bar] *)
    rBM_TrunnionFeedPress_ChB_bar   : REAL;     (* Ball mill feed trunnion lift press Ch B [bar] *)
    rBM_TrunnionFeedPress_ChC_bar   : REAL;     (* Ball mill feed trunnion lift press Ch C [bar] *)
    rBM_TrunnionDischPress_ChA_bar  : REAL;     (* Ball mill disch trunnion lift press Ch A [bar] *)
    rBM_TrunnionDischPress_ChB_bar  : REAL;     (* Ball mill disch trunnion lift press Ch B [bar] *)
    rBM_TrunnionDischPress_ChC_bar  : REAL;     (* Ball mill disch trunnion lift press Ch C [bar] *)
    rSAG_AcousticImpact_ChA_dB      : REAL;     (* SAG shell acoustic impact sound intensity Ch A [dB] *)
    rSAG_AcousticImpact_ChB_dB      : REAL;     (* SAG shell acoustic impact sound intensity Ch B [dB] *)
    rSAG_AcousticImpact_ChC_dB      : REAL;     (* SAG shell acoustic impact sound intensity Ch C [dB] *)
    rSump_SlurryDensity_ChA_t_m3    : REAL;     (* Common discharge sump nuclear density gauge Ch A [t/m3] *)
    rSump_SlurryDensity_ChB_t_m3    : REAL;     (* Common discharge sump nuclear density gauge Ch B [t/m3] *)
    rSump_SlurryDensity_ChC_t_m3    : REAL;     (* Common discharge sump nuclear density gauge Ch C [t/m3] *)
    rCyclone_FeedFlow_ChA_m3_h      : REAL;     (* Hydrocyclone feed slurry magnetic flowmeter Ch A [m3/h] *)
    rCyclone_FeedFlow_ChB_m3_h      : REAL;     (* Hydrocyclone feed slurry magnetic flowmeter Ch B [m3/h] *)
    rCyclone_FeedFlow_ChC_m3_h      : REAL;     (* Hydrocyclone feed slurry magnetic flowmeter Ch C [m3/h] *)
    rSump_Level_ChA_pct             : REAL;     (* Discharge collection sump radar level transmitter Ch A [%] *)
    rSump_Level_ChB_pct             : REAL;     (* Discharge collection sump radar level transmitter Ch B [%] *)
    rSump_Level_ChC_pct             : REAL;     (* Discharge collection sump ultrasonic level transmitter Ch C [%] *)

    (* ================================================================================= *)
    (* DUAL-PINION SYNCHRONOUS DRIVE FEEDBACK SIGNALS                                    *)
    (* ================================================================================= *)
    rSAG_MasterDriveTorque_kNm      : REAL;     (* SAG Master pinion shaft drive torque transducer [kN m] *)
    rSAG_SlaveDriveTorque_kNm       : REAL;     (* SAG Slave pinion shaft drive torque transducer [kN m] *)
    rSAG_MasterDriveSpeed_RPM       : REAL;     (* SAG Master drive motor tachometer speed feedback [rpm] *)
    rSAG_SlaveDriveSpeed_RPM        : REAL;     (* SAG Slave drive motor tachometer speed feedback [rpm] *)
    rSAG_MasterDriveCurrent_A       : REAL;     (* SAG Master synchronous drive stator current draw [A] *)
    rSAG_SlaveDriveCurrent_A        : REAL;     (* SAG Slave synchronous drive stator current draw [A] *)
    rSAG_MasterWindingTemp_degC     : REAL;     (* SAG Master drive stator winding hot spot temp [deg C] *)
    rSAG_SlaveWindingTemp_degC      : REAL;     (* SAG Slave drive stator winding hot spot temp [deg C] *)
    rBM_MasterDriveTorque_kNm       : REAL;     (* Ball mill Master pinion shaft drive torque [kN m] *)
    rBM_SlaveDriveTorque_kNm        : REAL;     (* Ball mill Slave pinion shaft drive torque [kN m] *)
    rBM_MasterDriveSpeed_RPM        : REAL;     (* Ball mill Master drive motor tachometer speed [rpm] *)
    rBM_SlaveDriveSpeed_RPM         : REAL;     (* Ball mill Slave drive motor tachometer speed [rpm] *)
    rBM_MasterDriveCurrent_A        : REAL;     (* Ball mill Master drive stator current draw [A] *)
    rBM_SlaveDriveCurrent_A         : REAL;     (* Ball mill Slave drive stator current draw [A] *)
    rBM_MasterWindingTemp_degC      : REAL;     (* Ball mill Master drive stator winding hot spot temp [deg C] *)
    rBM_SlaveWindingTemp_degC       : REAL;     (* Ball mill Slave drive stator winding hot spot temp [deg C] *)

    (* ================================================================================= *)
    (* AUXILIARY FIELD SENSORS & MECHANICAL STATUS CONTACTS                              *)
    (* ================================================================================= *)
    rApronFeeder1ActualRate_t_h     : REAL;     (* Apron feeder 1 weightometer mass flow rate [t/h] *)
    rApronFeeder2ActualRate_t_h     : REAL;     (* Apron feeder 2 weightometer mass flow rate [t/h] *)
    rPebbleRecycleFlow_t_h          : REAL;     (* SAG trommel scats pebble recycle conveyor rate [t/h] *)
    rPebbleCrusherPower_kW          : REAL;     (* Secondary pebble crusher motor power draw [kW] *)
    rPebbleCrusherCSS_mm            : REAL;     (* Pebble crusher closed side setting hydraulic position [mm] *)
    rCycloneManifoldPress_kPa       : REAL;     (* Hydrocyclone distributor header pressure transmitter [kPa] *)
    rSAGFeedWaterFlow_m3_h          : REAL;     (* SAG mill feed chute process water flowmeter [m3/h] *)
    rBallMillWaterFlow_m3_h         : REAL;     (* Ball mill feed trunnion dilution water flowmeter [m3/h] *)
    rSumpDilutionWaterFlow_m3_h     : REAL;     (* Mill discharge sump dilution trim water flowmeter [m3/h] *)
    rCycloneFeedPumpSpeed_RPM       : REAL;     (* Cyclone feed centrifugal slurry pump VFD speed [rpm] *)
    wCycloneValvesOpenFeedback      : WORD;     (* 14-pack hydrocyclone knife-gate open limit switches bitmask [-] *)
    rSAG_LubeOilSupplyTemp_degC     : REAL;     (* SAG trunnion bearing lubrication oil supply temp [deg C] *)
    rSAG_LubeOilReturnTemp_degC     : REAL;     (* SAG trunnion bearing lubrication oil return temp [deg C] *)
    bSAG_JackingPump1Running        : BOOL;     (* SAG feed HP jacking oil pump auxiliary contact [-] *)
    bSAG_JackingPump2Running        : BOOL;     (* SAG disch HP jacking oil pump auxiliary contact [-] *)
    bBM_JackingPump1Running         : BOOL;     (* Ball mill feed HP jacking oil pump auxiliary contact [-] *)
    bBM_JackingPump2Running         : BOOL;     (* Ball mill disch HP jacking oil pump auxiliary contact [-] *)
    bInchingDriveClutchEngaged      : BOOL;     (* Inching auxiliary gearbox mechanical clutch proximity switch [-] *)
    bInchingDriveMotorRunning       : BOOL;     (* Inching drive auxiliary motor running feedback [-] *)
    bMechanicalCaliperBrakeReleased : BOOL;     (* Mill disc park caliper brake released pressure switch [-] *)
    rMillRotationalAngle_deg        : REAL;     (* SAG mill absolute shell resolver rotational angle [deg] *)
    bMillFrozenChargeBypass         : BOOL;     (* Maintenance supervisor key-switch bypass for frozen charge [-] *)
END_VAR

VAR_OUTPUT
    (* ================================================================================= *)
    (* SEQUENCE SUPERVISORY STATUS & BIT-PACKED DIAGNOSTIC WORDS                         *)
    (* ================================================================================= *)
    bSystemReady                    : BOOL;     (* Circuit permissive ready for auto sequence initiation [-] *)
    bSystemRunning                  : BOOL;     (* SAG and Ball mills operating in steady-state production [-] *)
    bCircuitInWashout               : BOOL;     (* Circuit slurry washout / grind-out sequence in progress [-] *)
    iCurrentFsmState                : INT;      (* Active 12-stage operational state index [-] *)
    wSystemStatusWord               : DWORD;    (* Bit-packed 32-bit machine diagnostic status telemetry [-] *)
    wAlarmWord_Priority1            : DWORD;    (* ISA-18.2 Critical Emergency Stop alarm bitfield [-] *)
    wAlarmWord_Priority2            : DWORD;    (* ISA-18.2 Process Interlock & Hold alarm bitfield [-] *)
    wAlarmWord_Priority3            : DWORD;    (* ISA-18.2 Advisory & Preventive Maintenance bitfield [-] *)

    (* ================================================================================= *)
    (* PRIMARY ACTUATOR COMMAND SETPOINTS & SPEED REFERENCES                             *)
    (* ================================================================================= *)
    rApronFeeder1SpeedCmd_pct       : REAL;     (* Apron feeder 1 VFD drive speed command [%] *)
    rApronFeeder2SpeedCmd_pct       : REAL;     (* Apron feeder 2 VFD drive speed command [%] *)
    rSAGFeedWaterValveCmd_pct       : REAL;     (* SAG mill feed water control valve position demand [%] *)
    rBallMillWaterValveCmd_pct      : REAL;     (* Ball mill feed dilution water valve position demand [%] *)
    rSumpWaterValveCmd_pct          : REAL;     (* Mill discharge sump dilution trim valve position [%] *)
    rCycloneFeedPumpSpeedCmd_RPM    : REAL;     (* Cyclone feed variable-speed slurry pump demand [rpm] *)
    rSAGMasterDriveSpeedCmd_RPM     : REAL;     (* SAG mill master synchronous drive speed reference [rpm] *)
    rSAGSlaveDriveTorqueBias_pct    : REAL;     (* SAG slave drive torque balance closed-loop bias trim [%] *)
    rBallMillMasterDriveSpeedCmd_RPM: REAL;     (* Ball mill master drive speed reference [rpm] *)
    rBallMillSlaveDriveTorqueBias_pct:REAL;     (* Ball mill slave drive torque balance closed-loop bias trim [%] *)
    wCycloneValveSelectCmd          : WORD;     (* 14-pack hydrocyclone knife-gate open demand bitmask [-] *)
    bPebbleCrusherDiverterCmd       : BOOL;     (* Pebble diverter gate: TRUE=Crusher, FALSE=SAG bypass [-] *)
    bSAGJackingPump1Cmd             : BOOL;     (* SAG feed end HP jacking oil pump 1 start command [-] *)
    bSAGJackingPump2Cmd             : BOOL;     (* SAG disch end HP jacking oil pump 2 start command [-] *)
    bSAGLowPressureLubeCmd          : BOOL;     (* SAG mill low-pressure hydrodynamic lube pump command [-] *)
    bBMJackingPump1Cmd              : BOOL;     (* Ball mill feed end HP jacking oil pump 1 start command [-] *)
    bBMJackingPump2Cmd              : BOOL;     (* Ball mill disch end HP jacking oil pump 2 start command [-] *)
    bBMLowPressureLubeCmd           : BOOL;     (* Ball mill low-pressure lube pump command [-] *)
    bInchingDriveClutchCmd          : BOOL;     (* Mill inching auxiliary gearbox clutch engage demand [-] *)
    bInchingDriveMotorCmd           : BOOL;     (* Mill inching auxiliary motor run demand [-] *)
    bMechanicalCaliperBrakeCmd      : BOOL;     (* Hydraulic disc caliper park brake release demand [-] *)

    (* ================================================================================= *)
    (* 2oo3 VOTED SIGNALS & CYBER-PHYSICAL PROCESS ESTIMATES                             *)
    (* ================================================================================= *)
    rVoted_SAGFeedTrunnionPress_bar : REAL;     (* 2oo3 validated SAG feed trunnion oil pressure [bar] *)
    rVoted_SAGDischTrunnionPress_bar: REAL;     (* 2oo3 validated SAG disch trunnion oil pressure [bar] *)
    rVoted_BMFeedTrunnionPress_bar  : REAL;     (* 2oo3 validated Ball mill feed trunnion oil pressure [bar] *)
    rVoted_BMDischTrunnionPress_bar : REAL;     (* 2oo3 validated Ball mill disch trunnion oil press [bar] *)
    rVoted_SAGAcousticImpact_dB     : REAL;     (* 2oo3 validated SAG shell acoustic impact sound level [dB] *)
    rVoted_SumpDensity_t_m3         : REAL;     (* 2oo3 validated common sump slurry density [t/m3] *)
    rVoted_CycloneFlow_m3_h         : REAL;     (* 2oo3 validated cyclone feed slurry volumetric flow [m3/h] *)
    rVoted_SumpLevel_pct            : REAL;     (* 2oo3 validated common mill discharge sump level [%] *)
    rEstimatedDynamicToeAngle_deg   : REAL;     (* Cyber-physical estimated dynamic charge toe angle [deg] *)
    rEstimatedDynamicShoulderAngle_deg:REAL;    (* Cyber-physical estimated dynamic charge shoulder angle [deg] *)
    rEstimatedSAGTotalChargeFilling_pct:REAL;   (* Dynamic volumetric mill charge filling degree J [%] *)
    rEstimatedSAGBallFilling_pct    : REAL;     (* Estimated grinding ball volumetric filling degree Jb [%] *)
    rSAGDriveTorqueImbalance_pct    : REAL;     (* SAG dual-pinion torque differential error [%] *)
    rBMDriveTorqueImbalance_pct     : REAL;     (* Ball mill dual-pinion torque differential error [%] *)
    rSpecificEnergyConsumption_kWh_t: REAL;     (* Overall grinding circuit specific energy consumption [kWh/t] *)
    rPredictedOverflowP80_um        : REAL;     (* Plitt model predicted hydrocyclone overflow P80 grind size [um] *)
    rPredictedCutSize_d50c_um       : REAL;     (* Plitt corrected hydrocyclone cut size d50c [um] *)
    rSlurryApparentViscosity_mPas   : REAL;     (* Non-Newtonian Krieger-Dougherty apparent viscosity [mPa s] *)
    rCycloneRopingRiskIndex         : REAL;     (* Hydrocyclone underflow discharge roping index [0..1] *)
    rFrozenChargeRiskIndex          : REAL;     (* Breakaway frozen keyed ore risk probability index [0..1] *)
END_VAR
""")
    return "".join(parts)

print("build_iec_code header & IO defined.")
