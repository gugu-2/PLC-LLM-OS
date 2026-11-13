# biw_laser_brazing_builder/part8_phase5_alarms.py
"""
Part 8: Phase 5 - ISA-18.2 Process Alarms, SIL-3 Quench, 32-Bit Telemetry & Block End
Function Block: FB_Automotive_BIW_LaserBrazing_StructuralAdhesive
"""

def get_phase5_alarms():
    return """(* ============================================================================================== *)
(* PHASE 5: ISA-18.2 PROCESS ALARMS, WIRE MOTOR FAST QUENCH & 32-BIT BIT-PACKED TELEMETRY         *)
(* Sub-3ms SIL-3 Hardware Laser Quench Interlock, 4-Tier Process Alarm Matrix, DWORD Diagnostics   *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 5.1: FAST WIRE FEED MOTOR STALL / SLIP DETECTION (<3ms SIL-3 QUENCH INTERLOCK)            *)
(* ---------------------------------------------------------------------------------------------- *)
(* Over-Torque Instantaneous Motor Current Evaluation (Limit = 9.20 A) *)
IF (rWireFeedMotorCurrent > rWireStallCurrentLimit) AND bWireFeedForwardCmd THEN
    IF udiWireStallTripCounter < 2 THEN
        udiWireStallTripCounter := udiWireStallTripCounter + 1;
    ELSE
        bWireFeederStalled := TRUE;
        bFastQuenchTripped := TRUE;
        bFastLaserQuenchSIL3 := TRUE;
        bLaserEnable := FALSE;
        rLaserPowerCmd := 0.0;
    END_IF;
ELSE
    IF udiWireStallTripCounter > 0 THEN
        udiWireStallTripCounter := udiWireStallTripCounter - 1;
    END_IF;
END_IF;

(* Drive Roller Slippage / Wire Buckling Evaluation (Velocity Error > 18.5 mm/s) *)
IF (ABS(rWireFeedActualSpeed - rWireFeedSpeedCmd) > rWireSlipVelocityTolerance) 
   AND (rWireFeedSpeedCmd > 20.0) AND bWireFeedForwardCmd THEN
    IF udiWireSlipTripCounter < 2 THEN
        udiWireSlipTripCounter := udiWireSlipTripCounter + 1;
    ELSE
        bWireFeederSlipping := TRUE;
        bFastQuenchTripped := TRUE;
        bFastLaserQuenchSIL3 := TRUE;
        bLaserEnable := FALSE;
        rLaserPowerCmd := 0.0;
    END_IF;
ELSE
    IF udiWireSlipTripCounter > 0 THEN
        udiWireSlipTripCounter := udiWireSlipTripCounter - 1;
    END_IF;
END_IF;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 5.2: ISA-18.2 MULTI-TIER PROCESS ALARM MATRIX WITH DEADBAND HYSTERESIS                    *)
(* ---------------------------------------------------------------------------------------------- *)

(* 5.2.1: Melt Pool Temperature Alarms (x1) [deg C] *)
IF a_x[1] >= rAlarm_Pyro_HH THEN
    bAlarm_Pyro_HH_Latched := TRUE;
ELSIF a_x[1] <= (rAlarm_Pyro_HH - rAlarm_Pyro_Deadband) AND bReset THEN
    bAlarm_Pyro_HH_Latched := FALSE;
END_IF;

IF a_x[1] >= rAlarm_Pyro_H THEN
    bAlarm_Pyro_H_Latched := TRUE;
ELSIF a_x[1] <= (rAlarm_Pyro_H - rAlarm_Pyro_Deadband) THEN
    bAlarm_Pyro_H_Latched := FALSE;
END_IF;

IF a_x[1] <= rAlarm_Pyro_L THEN
    bAlarm_Pyro_L_Latched := TRUE;
ELSIF a_x[1] >= (rAlarm_Pyro_L + rAlarm_Pyro_Deadband) THEN
    bAlarm_Pyro_L_Latched := FALSE;
END_IF;

IF a_x[1] <= rAlarm_Pyro_LL THEN
    bAlarm_Pyro_LL_Latched := TRUE;
ELSIF a_x[1] >= (rAlarm_Pyro_LL + rAlarm_Pyro_Deadband) AND bReset THEN
    bAlarm_Pyro_LL_Latched := FALSE;
END_IF;

(* 5.2.2: CuSi3 Wire Feed Speed Alarms (x2) [mm/s] *)
IF a_x[2] >= rAlarm_WireV_HH THEN
    bAlarm_WireV_HH_Latched := TRUE;
ELSIF a_x[2] <= (rAlarm_WireV_HH - rAlarm_WireV_Deadband) AND bReset THEN
    bAlarm_WireV_HH_Latched := FALSE;
END_IF;

IF a_x[2] >= rAlarm_WireV_H THEN
    bAlarm_WireV_H_Latched := TRUE;
ELSIF a_x[2] <= (rAlarm_WireV_H - rAlarm_WireV_Deadband) THEN
    bAlarm_WireV_H_Latched := FALSE;
END_IF;

IF a_x[2] <= rAlarm_WireV_L THEN
    bAlarm_WireV_L_Latched := TRUE;
ELSIF a_x[2] >= (rAlarm_WireV_L + rAlarm_WireV_Deadband) THEN
    bAlarm_WireV_L_Latched := FALSE;
END_IF;

IF a_x[2] <= rAlarm_WireV_LL THEN
    bAlarm_WireV_LL_Latched := TRUE;
ELSIF a_x[2] >= (rAlarm_WireV_LL + rAlarm_WireV_Deadband) AND bReset THEN
    bAlarm_WireV_LL_Latched := FALSE;
END_IF;

(* 5.2.3: Seam Lateral Tracking Offset Alarms (x3) [um] *)
IF a_x[3] >= rAlarm_Seam_HH THEN
    bAlarm_Seam_HH_Latched := TRUE;
ELSIF a_x[3] <= (rAlarm_Seam_HH - rAlarm_Seam_Deadband) AND bReset THEN
    bAlarm_Seam_HH_Latched := FALSE;
END_IF;

IF a_x[3] >= rAlarm_Seam_H THEN
    bAlarm_Seam_H_Latched := TRUE;
ELSIF a_x[3] <= (rAlarm_Seam_H - rAlarm_Seam_Deadband) THEN
    bAlarm_Seam_H_Latched := FALSE;
END_IF;

IF a_x[3] <= rAlarm_Seam_L THEN
    bAlarm_Seam_L_Latched := TRUE;
ELSIF a_x[3] >= (rAlarm_Seam_L + rAlarm_Seam_Deadband) THEN
    bAlarm_Seam_L_Latched := FALSE;
END_IF;

IF a_x[3] <= rAlarm_Seam_LL THEN
    bAlarm_Seam_LL_Latched := TRUE;
ELSIF a_x[3] >= (rAlarm_Seam_LL + rAlarm_Seam_Deadband) AND bReset THEN
    bAlarm_Seam_LL_Latched := FALSE;
END_IF;

(* 5.2.4: Structural Adhesive Dynamic Line Pressure Alarms (x4) [bar] *)
IF a_x[4] >= rAlarm_AdhP_HH THEN
    bAlarm_AdhP_HH_Latched := TRUE;
ELSIF a_x[4] <= (rAlarm_AdhP_HH - rAlarm_AdhP_Deadband) AND bReset THEN
    bAlarm_AdhP_HH_Latched := FALSE;
END_IF;

IF a_x[4] >= rAlarm_AdhP_H THEN
    bAlarm_AdhP_H_Latched := TRUE;
ELSIF a_x[4] <= (rAlarm_AdhP_H - rAlarm_AdhP_Deadband) THEN
    bAlarm_AdhP_H_Latched := FALSE;
END_IF;

IF a_x[4] <= rAlarm_AdhP_L THEN
    bAlarm_AdhP_L_Latched := TRUE;
ELSIF a_x[4] >= (rAlarm_AdhP_L + rAlarm_AdhP_Deadband) THEN
    bAlarm_AdhP_L_Latched := FALSE;
END_IF;

IF a_x[4] <= rAlarm_AdhP_LL THEN
    bAlarm_AdhP_LL_Latched := TRUE;
ELSIF a_x[4] >= (rAlarm_AdhP_LL + rAlarm_AdhP_Deadband) AND bReset THEN
    bAlarm_AdhP_LL_Latched := FALSE;
END_IF;

(* 5.2.5: Structural Adhesive Volumetric Flux Alarms (x5) [mL/s] *)
IF a_x[5] >= rAlarm_AdhF_HH THEN
    bAlarm_AdhF_HH_Latched := TRUE;
ELSIF a_x[5] <= (rAlarm_AdhF_HH - rAlarm_AdhF_Deadband) AND bReset THEN
    bAlarm_AdhF_HH_Latched := FALSE;
END_IF;

IF a_x[5] >= rAlarm_AdhF_H THEN
    bAlarm_AdhF_H_Latched := TRUE;
ELSIF a_x[5] <= (rAlarm_AdhF_H - rAlarm_AdhF_Deadband) THEN
    bAlarm_AdhF_H_Latched := FALSE;
END_IF;

IF a_x[5] <= rAlarm_AdhF_L THEN
    bAlarm_AdhF_L_Latched := TRUE;
ELSIF a_x[5] >= (rAlarm_AdhF_L + rAlarm_AdhF_Deadband) THEN
    bAlarm_AdhF_L_Latched := FALSE;
END_IF;

IF a_x[5] <= rAlarm_AdhF_LL THEN
    bAlarm_AdhF_LL_Latched := TRUE;
ELSIF a_x[5] >= (rAlarm_AdhF_LL + rAlarm_AdhF_Deadband) AND bReset THEN
    bAlarm_AdhF_LL_Latched := FALSE;
END_IF;

(* 5.2.6: Dispensed Adhesive Bead Cross-Section Area Alarms (x6) [mm2] *)
IF a_x[6] >= rAlarm_BeadA_HH THEN
    bAlarm_BeadA_HH_Latched := TRUE;
ELSIF a_x[6] <= (rAlarm_BeadA_HH - rAlarm_BeadA_Deadband) AND bReset THEN
    bAlarm_BeadA_HH_Latched := FALSE;
END_IF;

IF a_x[6] >= rAlarm_BeadA_H THEN
    bAlarm_BeadA_H_Latched := TRUE;
ELSIF a_x[6] <= (rAlarm_BeadA_H - rAlarm_BeadA_Deadband) THEN
    bAlarm_BeadA_H_Latched := FALSE;
END_IF;

IF a_x[6] <= rAlarm_BeadA_L THEN
    bAlarm_BeadA_L_Latched := TRUE;
ELSIF a_x[6] >= (rAlarm_BeadA_L + rAlarm_BeadA_Deadband) THEN
    bAlarm_BeadA_L_Latched := FALSE;
END_IF;

IF a_x[6] <= rAlarm_BeadA_LL THEN
    bAlarm_BeadA_LL_Latched := TRUE;
ELSIF a_x[6] >= (rAlarm_BeadA_LL + rAlarm_BeadA_Deadband) AND bReset THEN
    bAlarm_BeadA_LL_Latched := FALSE;
END_IF;

(* 5.2.7: Roof Sheet Metal Thermal Buckling Alarms (x7) [um] *)
IF a_x[7] >= rAlarm_Buckle_HH THEN
    bAlarm_Buckle_HH_Latched := TRUE;
ELSIF a_x[7] <= (rAlarm_Buckle_HH - rAlarm_Buckle_Deadband) AND bReset THEN
    bAlarm_Buckle_HH_Latched := FALSE;
END_IF;

IF a_x[7] >= rAlarm_Buckle_H THEN
    bAlarm_Buckle_H_Latched := TRUE;
ELSIF a_x[7] <= (rAlarm_Buckle_H - rAlarm_Buckle_Deadband) THEN
    bAlarm_Buckle_H_Latched := FALSE;
END_IF;

(* 5.2.8: Framing Clamp Reaction Force Alarms (x8) [N] *)
IF a_x[8] >= rAlarm_ClampF_HH THEN
    bAlarm_ClampF_HH_Latched := TRUE;
ELSIF a_x[8] <= (rAlarm_ClampF_HH - rAlarm_ClampF_Deadband) AND bReset THEN
    bAlarm_ClampF_HH_Latched := FALSE;
END_IF;

IF a_x[8] >= rAlarm_ClampF_H THEN
    bAlarm_ClampF_H_Latched := TRUE;
ELSIF a_x[8] <= (rAlarm_ClampF_H - rAlarm_ClampF_Deadband) THEN
    bAlarm_ClampF_H_Latched := FALSE;
END_IF;

IF a_x[8] <= rAlarm_ClampF_L THEN
    bAlarm_ClampF_L_Latched := TRUE;
ELSIF a_x[8] >= (rAlarm_ClampF_L + rAlarm_ClampF_Deadband) THEN
    bAlarm_ClampF_L_Latched := FALSE;
END_IF;

IF a_x[8] <= rAlarm_ClampF_LL THEN
    bAlarm_ClampF_LL_Latched := TRUE;
ELSIF a_x[8] >= (rAlarm_ClampF_LL + rAlarm_ClampF_Deadband) AND bReset THEN
    bAlarm_ClampF_LL_Latched := FALSE;
END_IF;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 5.3: BIT-PACKED 32-BIT INDUSTRIAL TELEMETRY REGISTERS                                     *)
(* ---------------------------------------------------------------------------------------------- *)

(* 5.3.1: Primary Station Status Telemetry Word: dwStatusWord1 *)
dwStatusWord1 := 16#00000000;
IF bEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF;
IF bAutoMode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF;
IF bStationBusy THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF;
IF bStationComplete THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF;
IF bEgressReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF bLaserEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF bLaserShutterRelease THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bWireFeedForwardCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF bSeamTrackingActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF bAdhTipNeedleValveCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF bAdhRecircValveCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF bGeoClampsClosed THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
IF bDatumPinsLocked THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF;
IF bShieldGasValveCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF;
IF bCrossJetAirValveCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;
IF bWarningActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;
(* Pack eState [0..15] into bits 16..19 *)
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(eState AND 16#0F), 16);
(* Pack nSubState [0..99] into bits 20..27 *)
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(nSubState AND 16#FF), 20);
IF bSkidInStation THEN dwStatusWord1 := dwStatusWord1 OR 16#10000000; END_IF;
IF bSafetyFenceClosed THEN dwStatusWord1 := dwStatusWord1 OR 16#20000000; END_IF;
IF bEmergencyStopOk THEN dwStatusWord1 := dwStatusWord1 OR 16#40000000; END_IF;
IF bGeneralFaultTrip THEN dwStatusWord1 := dwStatusWord1 OR 16#80000000; END_IF;

(* 5.3.2: Secondary Robotic Subsystem Coordination Word: dwStatusWord2 *)
dwStatusWord2 := 16#00000000;
IF bPyro_ChannelDegraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF;
IF bSeam_ChannelDegraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF;
IF bAdhP_ChannelDegraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF;
IF bAdhF_ChannelDegraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF;
IF bClampW_ChannelDegraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF;
IF bPyro_A_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF;
IF bPyro_B_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF;
IF bPyro_C_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF;
IF bSeam_A_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bSeam_B_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;
IF bSeam_C_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;
IF bAdhP_A_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;
IF bAdhP_B_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF bAdhP_C_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;
IF bAdhF_A_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;
IF bAdhF_B_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF;
IF bAdhF_C_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00010000; END_IF;
IF bClampW_A_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF;
IF bClampW_B_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF;
IF bClampW_C_Healthy THEN dwStatusWord2 := dwStatusWord2 OR 16#00080000; END_IF;
IF bBarrel1LowLevel THEN dwStatusWord2 := dwStatusWord2 OR 16#00100000; END_IF;
IF bBarrel2LowLevel THEN dwStatusWord2 := dwStatusWord2 OR 16#00200000; END_IF;
IF bWireEndDetected THEN dwStatusWord2 := dwStatusWord2 OR 16#00400000; END_IF;
IF bWireJamDetected THEN dwStatusWord2 := dwStatusWord2 OR 16#00800000; END_IF;
IF rOpticsGlassTransmission < 92.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#01000000; END_IF;
IF NOT bLaserChillerTempOk THEN dwStatusWord2 := dwStatusWord2 OR 16#02000000; END_IF;
IF bRobotInContourZone THEN dwStatusWord2 := dwStatusWord2 OR 16#04000000; END_IF;
IF rBrazePorosityScore >= 92.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#08000000; END_IF;
IF rAdhBeadVolumeCompliance >= 90.0 THEN dwStatusWord2 := dwStatusWord2 OR 16#10000000; END_IF;
IF bCycleAborted THEN dwStatusWord2 := dwStatusWord2 OR 16#20000000; END_IF;
IF bFastQuenchTripped THEN dwStatusWord2 := dwStatusWord2 OR 16#40000000; END_IF;
IF bFastLaserQuenchSIL3 THEN dwStatusWord2 := dwStatusWord2 OR 16#80000000; END_IF;

(* 5.3.3: ISA-18.2 Process Alarms Word: dwAlarmWord1 *)
dwAlarmWord1 := 16#00000000;
IF bAlarm_Pyro_HH_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bAlarm_Pyro_H_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bAlarm_Pyro_L_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bAlarm_Pyro_LL_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bAlarm_WireV_HH_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bAlarm_WireV_H_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF bAlarm_WireV_L_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF bAlarm_WireV_LL_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;
IF bAlarm_Seam_HH_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;
IF bAlarm_Seam_H_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;
IF bAlarm_Seam_L_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF;
IF bAlarm_Seam_LL_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;
IF bAlarm_AdhP_HH_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF;
IF bAlarm_AdhP_H_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF;
IF bAlarm_AdhP_L_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; END_IF;
IF bAlarm_AdhP_LL_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00008000; END_IF;
IF bAlarm_AdhF_HH_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00010000; END_IF;
IF bAlarm_AdhF_H_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00020000; END_IF;
IF bAlarm_AdhF_L_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00040000; END_IF;
IF bAlarm_AdhF_LL_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00080000; END_IF;
IF bAlarm_BeadA_HH_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00100000; END_IF;
IF bAlarm_BeadA_H_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00200000; END_IF;
IF bAlarm_BeadA_L_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00400000; END_IF;
IF bAlarm_BeadA_LL_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00800000; END_IF;
IF bAlarm_Buckle_HH_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#01000000; END_IF;
IF bAlarm_Buckle_H_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#02000000; END_IF;
IF bAlarm_ClampF_HH_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#04000000; END_IF;
IF bAlarm_ClampF_H_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#08000000; END_IF;
IF bAlarm_ClampF_L_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#10000000; END_IF;
IF bAlarm_ClampF_LL_Latched THEN dwAlarmWord1 := dwAlarmWord1 OR 16#20000000; END_IF;
IF bWireFeederStalled THEN dwAlarmWord1 := dwAlarmWord1 OR 16#40000000; END_IF;
IF bWireFeederSlipping THEN dwAlarmWord1 := dwAlarmWord1 OR 16#80000000; END_IF;

(* 5.3.4: Hardware, Sensor & Environmental Alarm Word: dwAlarmWord2 *)
dwAlarmWord2 := 16#00000000;
IF bPyro_AllFaultTrip THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bSeam_AllFaultTrip THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bAdhP_AllFaultTrip THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bAdhF_AllFaultTrip THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bClampW_AllFaultTrip THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF rShieldGasPressure < 4.2 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF rShieldGasFlowRate < 15.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF rCrossJetAirPressure < 5.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;
IF rOpticsGlassTransmission < 88.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;
IF NOT bLaserSourceReady THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;
IF NOT bLaserChillerTempOk THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF;
IF NOT bLaserOpticsInterlockOk THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF;
IF bBarrel1LowLevel THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF;
IF bBarrel2LowLevel THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF;
IF bWireEndDetected THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF;
IF bWireJamDetected THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00008000; END_IF;
IF rWireReelRemaining < 50.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00010000; END_IF;
IF NOT bEmergencyStopOk THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00020000; END_IF;
IF NOT bSafetyFenceClosed THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00040000; END_IF;
IF bFastLaserQuenchSIL3 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#80000000; END_IF;

END_FUNCTION_BLOCK
"""
