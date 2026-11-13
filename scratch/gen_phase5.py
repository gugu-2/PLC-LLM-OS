# scratch/gen_phase5.py

def get_phase5():
    lines = []
    lines.append("""
(* ============================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED STATUS TELEMETRY       *)
(* ============================================================================== *)
(* Nuclear Class 1E Process Protection, First-Out Root-Cause Latching, and        *)
(* Complete 32-Bit Telemetry Packaging for Distributed Control System (DCS).      *)
(* ------------------------------------------------------------------------------ *)

(* ----------------------------------------------------------------------------- *)
(* STEP 1: ISA-18.2 TRIP AND ALERT COMPARISONS WITH DEADBAND HYSTERESIS         *)
(* ----------------------------------------------------------------------------- *)
(* Level High-High Trip (HH: +450.0 mm, Hysteresis: 25.0 mm) *)
IF fVotedNarrowRangeLevel_mm >= 450.00000000 THEN
    bTrip_Level_HH := TRUE;
ELSIF fVotedNarrowRangeLevel_mm <= 425.00000000 THEN
    bTrip_Level_HH := FALSE;
END_IF;

(* Level High Alert (H: +200.0 mm, Hysteresis: 15.0 mm) *)
IF fVotedNarrowRangeLevel_mm >= 200.00000000 THEN
    bAlert_Level_H := TRUE;
ELSIF fVotedNarrowRangeLevel_mm <= 185.00000000 THEN
    bAlert_Level_H := FALSE;
END_IF;

(* Level Low Warning (L: -200.0 mm, Hysteresis: 15.0 mm) *)
IF fVotedNarrowRangeLevel_mm <= -200.00000000 THEN
    bWarning_Level_L := TRUE;
ELSIF fVotedNarrowRangeLevel_mm >= -185.00000000 THEN
    bWarning_Level_L := FALSE;
END_IF;

(* Level Low-Low Trip (LL: -450.0 mm, Hysteresis: 25.0 mm) *)
IF fVotedNarrowRangeLevel_mm <= -450.00000000 THEN
    bTrip_Level_LL := TRUE;
ELSIF fVotedNarrowRangeLevel_mm >= -425.00000000 THEN
    bTrip_Level_LL := FALSE;
END_IF;

(* Steam Drum Pressure High-High Trip (HH: 78.5 bar, Hysteresis: 1.5 bar) *)
IF fVotedDrumPressure_bar >= 78.50000000 THEN
    bTrip_Pressure_HH := TRUE;
ELSIF fVotedDrumPressure_bar <= 77.00000000 THEN
    bTrip_Pressure_HH := FALSE;
END_IF;

(* Steam Drum Pressure High Alert (H: 74.0 bar, Hysteresis: 1.0 bar) *)
IF fVotedDrumPressure_bar >= 74.00000000 THEN
    bAlert_Pressure_H := TRUE;
ELSIF fVotedDrumPressure_bar <= 73.00000000 THEN
    bAlert_Pressure_H := FALSE;
END_IF;

(* Steam Drum Pressure Low Warning (L: 58.0 bar, Hysteresis: 1.0 bar) *)
IF fVotedDrumPressure_bar <= 58.00000000 THEN
    bWarning_Pressure_L := TRUE;
ELSIF fVotedDrumPressure_bar >= 59.00000000 THEN
    bWarning_Pressure_L := FALSE;
END_IF;

(* Steam Drum Pressure Low-Low Trip (LL: 45.0 bar, Hysteresis: 2.0 bar) *)
IF fVotedDrumPressure_bar <= 45.00000000 THEN
    bTrip_Pressure_LL := TRUE;
ELSIF fVotedDrumPressure_bar >= 47.00000000 THEN
    bTrip_Pressure_LL := FALSE;
END_IF;

(* Feedwater / Steam Mass Flow Mismatch Alert (150.0 t/h, Hysteresis: 15.0 t/h) *)
IF ABS(fVotedSteamFlow_t_h - fVotedFeedwaterFlow_t_h) >= 150.00000000 THEN
    bAlert_FlowMismatch_H := TRUE;
ELSIF ABS(fVotedSteamFlow_t_h - fVotedFeedwaterFlow_t_h) <= 135.00000000 THEN
    bAlert_FlowMismatch_H := FALSE;
END_IF;

(* Steam Line SGTR Radiation High-High Trip (1.85E6 Bq/m3, Hysteresis: 5.0E4 Bq/m3) *)
IF fVotedSGTR_Rad_Bq_m3 >= 1850000.00000000 THEN
    bTrip_SGTR_Rad_HH := TRUE;
ELSIF fVotedSGTR_Rad_Bq_m3 <= 1800000.00000000 THEN
    bTrip_SGTR_Rad_HH := FALSE;
END_IF;

(* Economizer Feedwater Inlet Temperature Low Alert (140.0 deg C) *)
IF fTE_FW_503 <= 140.00000000 THEN
    bAlert_FeedwaterTemp_L := TRUE;
ELSIF fTE_FW_503 >= 145.00000000 THEN
    bAlert_FeedwaterTemp_L := FALSE;
END_IF;

(* Boiling Riser Void Fraction Surge Alert (Rate > 0.15 / s) *)
IF ABS(x_hat[3] - x_pred[3]) / fCycleTime_Ts >= 0.15000000 THEN
    bAlert_VoidFractionSurge := TRUE;
ELSE
    bAlert_VoidFractionSurge := FALSE;
END_IF;

(* ----------------------------------------------------------------------------- *)
(* STEP 2: FIRST-OUT CAUSE ANNUNCIATOR LATCHING LOGIC (IEEE 603 CLASS 1E)        *)
(* Captures the exact initial trip cause and latches until operator reset        *)
(* ----------------------------------------------------------------------------- *)
IF NOT bFirstOutLocked THEN
    IF bTrip_Level_HH THEN
        dwFirstOutWord := 16#00000001; (* Bit 0: Narrow Range Level High-High *)
        bFirstOutLocked := TRUE;
    ELSIF bTrip_Level_LL THEN
        dwFirstOutWord := 16#00000002; (* Bit 1: Narrow Range Level Low-Low *)
        bFirstOutLocked := TRUE;
    ELSIF bTrip_Pressure_HH THEN
        dwFirstOutWord := 16#00000004; (* Bit 2: Steam Drum Pressure High-High *)
        bFirstOutLocked := TRUE;
    ELSIF bTrip_Pressure_LL THEN
        dwFirstOutWord := 16#00000008; (* Bit 3: Steam Drum Pressure Low-Low *)
        bFirstOutLocked := TRUE;
    ELSIF bTrip_SGTR_Rad_HH THEN
        dwFirstOutWord := 16#00000010; (* Bit 4: SGTR Secondary Radiation Trip *)
        bFirstOutLocked := TRUE;
    ELSIF bTrip_DryoutRisk THEN
        dwFirstOutWord := 16#00000020; (* Bit 5: Steam Generator Dry-Out Risk *)
        bFirstOutLocked := TRUE;
    ELSIF bTrip_SensorLoss_Fatal THEN
        dwFirstOutWord := 16#00000040; (* Bit 6: Total 2oo3 Sensor Loss Failure *)
        bFirstOutLocked := TRUE;
    END_IF;
END_IF;

(* Master Safety Reset Pushbutton clears latched trips when conditions clear *)
IF bMasterResetTrip THEN
    IF (NOT bTrip_Level_HH) AND (NOT bTrip_Level_LL) AND 
       (NOT bTrip_Pressure_HH) AND (NOT bTrip_Pressure_LL) AND 
       (NOT bTrip_SGTR_Rad_HH) AND (NOT bTrip_SensorLoss_Fatal) THEN
        bFirstOutLocked := FALSE;
        dwFirstOutWord := 16#00000000;
        bTripLockoutActive := FALSE;
    END_IF;
END_IF;

IF bFirstOutLocked THEN
    bTripLockoutActive := TRUE;
END_IF;

(* ----------------------------------------------------------------------------- *)
(* STEP 3: DEDICATED CLASS 1E SAFETY-CRITICAL ACTUATION SIGNALS                  *)
(* ----------------------------------------------------------------------------- *)
bReactorScramSG_TripReq := bTrip_Level_HH OR bTrip_Level_LL OR bTrip_Pressure_HH OR 
                           bTrip_SGTR_Rad_HH OR bTrip_DryoutRisk OR bTrip_SensorLoss_Fatal;

bTurbineTripSG_Req := bTrip_Level_HH OR bReactorScramSG_TripReq;

bMFRV_FastTripClosureCmd := bTrip_Level_HH OR bTrip_SGTR_Rad_HH OR 
                            (eCurrentState = 6) OR (eCurrentState = 11);

bBPV_FastTripClosureCmd := bTrip_Level_HH OR bTrip_SGTR_Rad_HH OR 
                           (eCurrentState = 6) OR (eCurrentState = 11);

bAFW_MotorPump1_AutoStartCmd := bTrip_Level_LL OR bLossOfMainFeedwater OR 
                                (eCurrentState = 8) OR (eCurrentState = 10);

bAFW_MotorPump2_AutoStartCmd := bTrip_Level_LL OR bLossOfMainFeedwater OR 
                                (eCurrentState = 8) OR (eCurrentState = 10);

bAFW_TurbinePump_AutoStartCmd := (fVotedNarrowRangeLevel_mm <= -650.00000000) OR 
                                 bStationBlackoutSignal OR (eCurrentState = 9) OR (eCurrentState = 10);

bMSIV_SG_IsolationReq := bTrip_Pressure_LL OR bTrip_SGTR_Rad_HH OR (eCurrentState = 6);

bBlowdownIsolationCmd := bTrip_Level_LL OR bTrip_SGTR_Rad_HH OR 
                         (eCurrentState = 6) OR (eCurrentState = 7);

(* Overall System Health Evaluation *)
bSystemHealthy := (NOT bTripLockoutActive) AND (NOT bTrip_SensorLoss_Fatal) AND 
                  (NOT bDegradedTMR) AND bEnableControlBlock;

(* ----------------------------------------------------------------------------- *)
(* STEP 4: OPERATOR MANUAL CONTROL OVERRIDE STATION                              *)
(* ----------------------------------------------------------------------------- *)
IF bManualControlSelect AND (NOT bTrip_Level_HH) AND (NOT bTrip_SGTR_Rad_HH) AND 
   (NOT bTripLockoutActive) THEN
    fMFRV_PositionDemand := fManualDemand_MFRV;
    fBPV_PositionDemand := fManualDemand_BPV;
    fAFW_MotorPump1_SpeedDemand := fManualDemand_AFW;
    fAFW_MotorPump2_SpeedDemand := fManualDemand_AFW;
END_IF;

(* ----------------------------------------------------------------------------- *)
(* STEP 5: FINAL ACTUATOR POSITION CLAMPING [0.0..100.0 %]                      *)
(* ----------------------------------------------------------------------------- *)
IF bMFRV_FastTripClosureCmd THEN
    fMFRV_PositionDemand := 0.00000000;
ELSE
    IF fMFRV_PositionDemand < 0.00000000 THEN
        fMFRV_PositionDemand := 0.00000000;
    ELSIF fMFRV_PositionDemand > 100.00000000 THEN
        fMFRV_PositionDemand := 100.00000000;
    END_IF;
END_IF;

IF bBPV_FastTripClosureCmd THEN
    fBPV_PositionDemand := 0.00000000;
ELSE
    IF fBPV_PositionDemand < 0.00000000 THEN
        fBPV_PositionDemand := 0.00000000;
    ELSIF fBPV_PositionDemand > 100.00000000 THEN
        fBPV_PositionDemand := 100.00000000;
    END_IF;
END_IF;

IF fAFW_MotorPump1_SpeedDemand < 0.00000000 THEN
    fAFW_MotorPump1_SpeedDemand := 0.00000000;
ELSIF fAFW_MotorPump1_SpeedDemand > 100.00000000 THEN
    fAFW_MotorPump1_SpeedDemand := 100.00000000;
END_IF;

IF fAFW_MotorPump2_SpeedDemand < 0.00000000 THEN
    fAFW_MotorPump2_SpeedDemand := 0.00000000;
ELSIF fAFW_MotorPump2_SpeedDemand > 100.00000000 THEN
    fAFW_MotorPump2_SpeedDemand := 100.00000000;
END_IF;

IF fAFW_TurbinePump_GovernorDemand < 0.00000000 THEN
    fAFW_TurbinePump_GovernorDemand := 0.00000000;
ELSIF fAFW_TurbinePump_GovernorDemand > 100.00000000 THEN
    fAFW_TurbinePump_GovernorDemand := 100.00000000;
END_IF;

(* ----------------------------------------------------------------------------- *)
(* STEP 6: BIT-PACKED 32-BIT TELEMETRY REGISTERS FOR DCS / SCADA INTERFACE       *)
(* ----------------------------------------------------------------------------- *)
(* Telemetry Status Word 1 *)
dwStatusWord1 := 16#00000000;
dwStatusWord1 := dwStatusWord1 OR DINT_TO_DWORD(eCurrentState AND 16#0F); (* Bits 0-3: FSM State *)
IF bEnableControlBlock THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00000010; (* Bit 4: Enable *)
END_IF;
IF bManualControlSelect THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00000020; (* Bit 5: Manual Mode *)
END_IF;
IF eCurrentState = 4 THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00000040; (* Bit 6: Full MPC Active *)
END_IF;
IF eCurrentState = 3 THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00000080; (* Bit 7: 3-Element Cascade *)
END_IF;
IF eCurrentState = 1 THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00000100; (* Bit 8: Low-Power Bypass *)
END_IF;
IF eCurrentState = 2 THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00000200; (* Bit 9: Bumpless Transfer *)
END_IF;
IF bDegradedTMR THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00000400; (* Bit 10: TMR Degraded *)
END_IF;
IF bTrip_SensorLoss_Fatal THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00000800; (* Bit 11: Sensor Loss Fatal *)
END_IF;
IF bMFRV_FastTripClosureCmd THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00001000; (* Bit 12: MFRV Solenoid Closed *)
END_IF;
IF bBPV_FastTripClosureCmd THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00002000; (* Bit 13: BPV Solenoid Closed *)
END_IF;
IF bAFW_MotorPump1_AutoStartCmd THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00004000; (* Bit 14: MDAFW 1 Auto-Start *)
END_IF;
IF bAFW_MotorPump2_AutoStartCmd THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00008000; (* Bit 15: MDAFW 2 Auto-Start *)
END_IF;
IF bAFW_TurbinePump_AutoStartCmd THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00010000; (* Bit 16: TDAFW Auto-Start *)
END_IF;
IF bMSIV_SG_IsolationReq THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00020000; (* Bit 17: MSIV Isolated *)
END_IF;
IF bBlowdownIsolationCmd THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00040000; (* Bit 18: Blowdown Isolated *)
END_IF;
IF bReactorScramSG_TripReq THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00080000; (* Bit 19: RPS Scram Req *)
END_IF;
IF bTurbineTripSG_Req THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00100000; (* Bit 20: Turbine Trip Req *)
END_IF;
IF ABS(fAntiSwellBias) > 0.50000000 THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00200000; (* Bit 21: Anti-Swell Active *)
END_IF;
IF eCurrentState = 13 THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00400000; (* Bit 22: Decay Heat Mode *)
END_IF;
IF eCurrentState = 10 THEN
    dwStatusWord1 := dwStatusWord1 OR 16#00800000; (* Bit 23: Dryout Cooldown *)
END_IF;
IF bTrip_OverfillRisk THEN
    dwStatusWord1 := dwStatusWord1 OR 16#01000000; (* Bit 24: Overfill Risk *)
END_IF;
IF bTrip_DryoutRisk THEN
    dwStatusWord1 := dwStatusWord1 OR 16#02000000; (* Bit 25: Dryout Risk *)
END_IF;
IF eCurrentState = 7 THEN
    dwStatusWord1 := dwStatusWord1 OR 16#04000000; (* Bit 26: SGTR Active *)
END_IF;
IF bTripLockoutActive THEN
    dwStatusWord1 := dwStatusWord1 OR 16#08000000; (* Bit 27: Trip Lockout *)
END_IF;
IF bSystemHealthy THEN
    dwStatusWord1 := dwStatusWord1 OR 16#10000000; (* Bit 28: System Healthy *)
END_IF;
IF (nExecutionCycleCounter AND 16#01) = 16#01 THEN
    dwStatusWord1 := dwStatusWord1 OR 16#80000000; (* Bit 31: Heartbeat Toggle *)
END_IF;

(* Telemetry Status Word 2: Sensor Channel Health Flags *)
dwStatusWord2 := 16#00000000;
IF bChA_Healthy_LT_NR THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF;
IF bChB_Healthy_LT_NR THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF;
IF bChC_Healthy_LT_NR THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF;
IF bChA_Healthy_LT_WR THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF;
IF bChB_Healthy_LT_WR THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF;
IF bChC_Healthy_LT_WR THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF;
IF bChA_Healthy_PT_MS THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF;
IF bChB_Healthy_PT_MS THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF;
IF bChC_Healthy_PT_MS THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bChA_Healthy_FT_MS THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;
IF bChB_Healthy_FT_MS THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;
IF bChC_Healthy_FT_MS THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;
IF bChA_Healthy_FT_FW THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF bChB_Healthy_FT_FW THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;
IF bChC_Healthy_FT_FW THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;
IF bChA_Healthy_TE_CL THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF;
IF bChB_Healthy_TE_CL THEN dwStatusWord2 := dwStatusWord2 OR 16#00010000; END_IF;
IF bChC_Healthy_TE_CL THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF;
IF bChA_Healthy_RE_SGTR THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF;
IF bChB_Healthy_RE_SGTR THEN dwStatusWord2 := dwStatusWord2 OR 16#00080000; END_IF;
IF bChC_Healthy_RE_SGTR THEN dwStatusWord2 := dwStatusWord2 OR 16#00100000; END_IF;

(* Telemetry Alarm Word 1: ISA-18.2 Process Trips & Warnings *)
dwAlarmWord1 := 16#00000000;
IF bTrip_Level_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bAlert_Level_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bWarning_Level_L THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bTrip_Level_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bTrip_Pressure_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bAlert_Pressure_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF bWarning_Pressure_L THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF bTrip_Pressure_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;
IF bAlert_FlowMismatch_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;
IF bTrip_SGTR_Rad_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;
IF bAlert_FeedwaterTemp_L THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF;
IF bAlert_VoidFractionSurge THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;
IF bTrip_OverfillRisk THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF;
IF bTrip_DryoutRisk THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF;
IF bTrip_SensorLoss_Fatal THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; END_IF;
IF bTripLockoutActive THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00008000; END_IF;

(* Telemetry Alarm Word 2: TMR Hardware Discrepancies *)
dwAlarmWord2 := 16#00000000;
IF bDiscrep_LT_NR_AB THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bDiscrep_LT_NR_BC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bDiscrep_LT_NR_CA THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bDiscrep_LT_WR_AB THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bDiscrep_LT_WR_BC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF bDiscrep_LT_WR_CA THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF bDiscrep_PT_MS_AB THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF bDiscrep_PT_MS_BC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;
IF bDiscrep_PT_MS_CA THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;
IF bDiscrep_FT_MS_AB THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;
IF bDiscrep_FT_MS_BC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF;
IF bDiscrep_FT_MS_CA THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF;
IF bDiscrep_FT_FW_AB THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF;
IF bDiscrep_FT_FW_BC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF;
IF bDiscrep_FT_FW_CA THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF;
IF bDiscrep_TE_CL_AB THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00008000; END_IF;
IF bDiscrep_TE_CL_BC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00010000; END_IF;
IF bDiscrep_TE_CL_CA THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00020000; END_IF;
IF bDiscrep_RE_SGTR_AB THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00040000; END_IF;
IF bDiscrep_RE_SGTR_BC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00080000; END_IF;
IF bDiscrep_RE_SGTR_CA THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00100000; END_IF;

(* Increment Execution Cycle Counter *)
nExecutionCycleCounter := nExecutionCycleCounter + 1;

END_FUNCTION_BLOCK
""")
    return "".join(lines)

if __name__ == "__main__":
    p5 = get_phase5()
    print(f"Phase 5 generated. Length: {len(p5)} characters.")
