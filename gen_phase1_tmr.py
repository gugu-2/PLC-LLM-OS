# -*- coding: utf-8 -*-
"""
Generator module: Phase 1 2oo3 TMR Voting Suite
"""

def get_phase1_tmr():
    return """(* =========================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & FAULT-TOLERANT ESTIMATION    *)
(* =========================================================================================== *)
(* ------------------------------------------------------------------------------------------- *)
(* GROUP 1: OPTICAL FLUORESCENCE DISSOLVED OXYGEN (dO2 A, B, C)                                *)
(* ------------------------------------------------------------------------------------------- *)
arrDO_Sensors[1] := AI_DissolvedOxygen_ChA_pct;
arrDO_Sensors[2] := AI_DissolvedOxygen_ChB_pct;
arrDO_Sensors[3] := AI_DissolvedOxygen_ChC_pct;

arrDO_Diff[1] := ABS(arrDO_Sensors[1] - arrDO_Sensors[2]);
arrDO_Diff[2] := ABS(arrDO_Sensors[2] - arrDO_Sensors[3]);
arrDO_Diff[3] := ABS(arrDO_Sensors[3] - arrDO_Sensors[1]);

(* Channel A Health Evaluation *)
IF (arrDO_Diff[1] > rDO_Tolerance_pct) AND (arrDO_Diff[3] > rDO_Tolerance_pct) THEN
    arrDO_DiscrepTimer_s[1] := arrDO_DiscrepTimer_s[1] + AI_ControllerCycleTime_s;
    IF arrDO_DiscrepTimer_s[1] >= rDO_DiscrepLimit_s THEN
        arrDO_Healthy[1] := FALSE;
    END_IF;
ELSE
    arrDO_DiscrepTimer_s[1] := 0.0;
    arrDO_Healthy[1] := TRUE;
END_IF;

(* Channel B Health Evaluation *)
IF (arrDO_Diff[1] > rDO_Tolerance_pct) AND (arrDO_Diff[2] > rDO_Tolerance_pct) THEN
    arrDO_DiscrepTimer_s[2] := arrDO_DiscrepTimer_s[2] + AI_ControllerCycleTime_s;
    IF arrDO_DiscrepTimer_s[2] >= rDO_DiscrepLimit_s THEN
        arrDO_Healthy[2] := FALSE;
    END_IF;
ELSE
    arrDO_DiscrepTimer_s[2] := 0.0;
    arrDO_Healthy[2] := TRUE;
END_IF;

(* Channel C Health Evaluation *)
IF (arrDO_Diff[2] > rDO_Tolerance_pct) AND (arrDO_Diff[3] > rDO_Tolerance_pct) THEN
    arrDO_DiscrepTimer_s[3] := arrDO_DiscrepTimer_s[3] + AI_ControllerCycleTime_s;
    IF arrDO_DiscrepTimer_s[3] >= rDO_DiscrepLimit_s THEN
        arrDO_Healthy[3] := FALSE;
    END_IF;
ELSE
    arrDO_DiscrepTimer_s[3] := 0.0;
    arrDO_Healthy[3] := TRUE;
END_IF;

(* Group 1 Voting Execution *)
IF arrDO_Healthy[1] AND arrDO_Healthy[2] AND arrDO_Healthy[3] THEN
    bDO_Degraded := FALSE;
    bDO_CriticalFault := FALSE;
    IF ((arrDO_Sensors[1] >= arrDO_Sensors[2]) AND (arrDO_Sensors[1] <= arrDO_Sensors[3])) OR
       ((arrDO_Sensors[1] >= arrDO_Sensors[3]) AND (arrDO_Sensors[1] <= arrDO_Sensors[2])) THEN
        rVoted_DissolvedOxygen_pct := arrDO_Sensors[1];
    ELSIF ((arrDO_Sensors[2] >= arrDO_Sensors[1]) AND (arrDO_Sensors[2] <= arrDO_Sensors[3])) OR
          ((arrDO_Sensors[2] >= arrDO_Sensors[3]) AND (arrDO_Sensors[2] <= arrDO_Sensors[1])) THEN
        rVoted_DissolvedOxygen_pct := arrDO_Sensors[2];
    ELSE
        rVoted_DissolvedOxygen_pct := arrDO_Sensors[3];
    END_IF;
ELSIF arrDO_Healthy[1] AND arrDO_Healthy[2] THEN
    bDO_Degraded := TRUE;
    bDO_CriticalFault := FALSE;
    rVoted_DissolvedOxygen_pct := (arrDO_Sensors[1] + arrDO_Sensors[2]) * 0.50;
ELSIF arrDO_Healthy[2] AND arrDO_Healthy[3] THEN
    bDO_Degraded := TRUE;
    bDO_CriticalFault := FALSE;
    rVoted_DissolvedOxygen_pct := (arrDO_Sensors[2] + arrDO_Sensors[3]) * 0.50;
ELSIF arrDO_Healthy[1] AND arrDO_Healthy[3] THEN
    bDO_Degraded := TRUE;
    bDO_CriticalFault := FALSE;
    rVoted_DissolvedOxygen_pct := (arrDO_Sensors[1] + arrDO_Sensors[3]) * 0.50;
ELSIF arrDO_Healthy[1] THEN
    bDO_Degraded := TRUE;
    bDO_CriticalFault := FALSE;
    rVoted_DissolvedOxygen_pct := arrDO_Sensors[1];
ELSIF arrDO_Healthy[2] THEN
    bDO_Degraded := TRUE;
    bDO_CriticalFault := FALSE;
    rVoted_DissolvedOxygen_pct := arrDO_Sensors[2];
ELSIF arrDO_Healthy[3] THEN
    bDO_Degraded := TRUE;
    bDO_CriticalFault := FALSE;
    rVoted_DissolvedOxygen_pct := arrDO_Sensors[3];
ELSE
    bDO_Degraded := TRUE;
    bDO_CriticalFault := TRUE;
    (* Hold last valid voted reading *)
END_IF;

(* dO2 Rate of Change Monitoring [% / min] *)
IF AI_ControllerCycleTime_s > 0.001 THEN
    rDO_RoC_pct_per_min := (rVoted_DissolvedOxygen_pct - rDO_Prev_pct) / (AI_ControllerCycleTime_s / 60.0);
    rDO_Prev_pct := rVoted_DissolvedOxygen_pct;
END_IF;

(* ------------------------------------------------------------------------------------------- *)
(* GROUP 2: PRESSURIZED GEL GLASS pH ELECTRODES (pH A, B, C)                                   *)
(* ------------------------------------------------------------------------------------------- *)
arrPH_Sensors[1] := AI_LiquidBroth_pH_ChA;
arrPH_Sensors[2] := AI_LiquidBroth_pH_ChB;
arrPH_Sensors[3] := AI_LiquidBroth_pH_ChC;

arrPH_Diff[1] := ABS(arrPH_Sensors[1] - arrPH_Sensors[2]);
arrPH_Diff[2] := ABS(arrPH_Sensors[2] - arrPH_Sensors[3]);
arrPH_Diff[3] := ABS(arrPH_Sensors[3] - arrPH_Sensors[1]);

(* Channel A Health Evaluation *)
IF (arrPH_Diff[1] > rPH_Tolerance) AND (arrPH_Diff[3] > rPH_Tolerance) THEN
    arrPH_DiscrepTimer_s[1] := arrPH_DiscrepTimer_s[1] + AI_ControllerCycleTime_s;
    IF arrPH_DiscrepTimer_s[1] >= rPH_DiscrepLimit_s THEN
        arrPH_Healthy[1] := FALSE;
    END_IF;
ELSE
    arrPH_DiscrepTimer_s[1] := 0.0;
    arrPH_Healthy[1] := TRUE;
END_IF;

(* Channel B Health Evaluation *)
IF (arrPH_Diff[1] > rPH_Tolerance) AND (arrPH_Diff[2] > rPH_Tolerance) THEN
    arrPH_DiscrepTimer_s[2] := arrPH_DiscrepTimer_s[2] + AI_ControllerCycleTime_s;
    IF arrPH_DiscrepTimer_s[2] >= rPH_DiscrepLimit_s THEN
        arrPH_Healthy[2] := FALSE;
    END_IF;
ELSE
    arrPH_DiscrepTimer_s[2] := 0.0;
    arrPH_Healthy[2] := TRUE;
END_IF;

(* Channel C Health Evaluation *)
IF (arrPH_Diff[2] > rPH_Tolerance) AND (arrPH_Diff[3] > rPH_Tolerance) THEN
    arrPH_DiscrepTimer_s[3] := arrPH_DiscrepTimer_s[3] + AI_ControllerCycleTime_s;
    IF arrPH_DiscrepTimer_s[3] >= rPH_DiscrepLimit_s THEN
        arrPH_Healthy[3] := FALSE;
    END_IF;
ELSE
    arrPH_DiscrepTimer_s[3] := 0.0;
    arrPH_Healthy[3] := TRUE;
END_IF;

(* Group 2 Voting Execution *)
IF arrPH_Healthy[1] AND arrPH_Healthy[2] AND arrPH_Healthy[3] THEN
    bPH_Degraded := FALSE;
    bPH_CriticalFault := FALSE;
    IF ((arrPH_Sensors[1] >= arrPH_Sensors[2]) AND (arrPH_Sensors[1] <= arrPH_Sensors[3])) OR
       ((arrPH_Sensors[1] >= arrPH_Sensors[3]) AND (arrPH_Sensors[1] <= arrPH_Sensors[2])) THEN
        rVoted_LiquidBroth_pH := arrPH_Sensors[1];
    ELSIF ((arrPH_Sensors[2] >= arrPH_Sensors[1]) AND (arrPH_Sensors[2] <= arrPH_Sensors[3])) OR
          ((arrPH_Sensors[2] >= arrPH_Sensors[3]) AND (arrPH_Sensors[2] <= arrPH_Sensors[1])) THEN
        rVoted_LiquidBroth_pH := arrPH_Sensors[2];
    ELSE
        rVoted_LiquidBroth_pH := arrPH_Sensors[3];
    END_IF;
ELSIF arrPH_Healthy[1] AND arrPH_Healthy[2] THEN
    bPH_Degraded := TRUE;
    bPH_CriticalFault := FALSE;
    rVoted_LiquidBroth_pH := (arrPH_Sensors[1] + arrPH_Sensors[2]) * 0.50;
ELSIF arrPH_Healthy[2] AND arrPH_Healthy[3] THEN
    bPH_Degraded := TRUE;
    bPH_CriticalFault := FALSE;
    rVoted_LiquidBroth_pH := (arrPH_Sensors[2] + arrPH_Sensors[3]) * 0.50;
ELSIF arrPH_Healthy[1] AND arrPH_Healthy[3] THEN
    bPH_Degraded := TRUE;
    bPH_CriticalFault := FALSE;
    rVoted_LiquidBroth_pH := (arrPH_Sensors[1] + arrPH_Sensors[3]) * 0.50;
ELSIF arrPH_Healthy[1] THEN
    bPH_Degraded := TRUE;
    bPH_CriticalFault := FALSE;
    rVoted_LiquidBroth_pH := arrPH_Sensors[1];
ELSIF arrPH_Healthy[2] THEN
    bPH_Degraded := TRUE;
    bPH_CriticalFault := FALSE;
    rVoted_LiquidBroth_pH := arrPH_Sensors[2];
ELSIF arrPH_Healthy[3] THEN
    bPH_Degraded := TRUE;
    bPH_CriticalFault := FALSE;
    rVoted_LiquidBroth_pH := arrPH_Sensors[3];
ELSE
    bPH_Degraded := TRUE;
    bPH_CriticalFault := TRUE;
END_IF;

(* pH Rate of Change Monitoring [pH / min] *)
IF AI_ControllerCycleTime_s > 0.001 THEN
    rPH_RoC_per_min := (rVoted_LiquidBroth_pH - rPH_Prev) / (AI_ControllerCycleTime_s / 60.0);
    rPH_Prev := rVoted_LiquidBroth_pH;
END_IF;

(* ------------------------------------------------------------------------------------------- *)
(* GROUP 3: 4-WIRE Pt100 RTD BROTH TEMPERATURE (Temp A, B, C)                                  *)
(* ------------------------------------------------------------------------------------------- *)
arrTemp_Sensors[1] := AI_BrothTemp_ChA_degC;
arrTemp_Sensors[2] := AI_BrothTemp_ChB_degC;
arrTemp_Sensors[3] := AI_BrothTemp_ChC_degC;

arrTemp_Diff[1] := ABS(arrTemp_Sensors[1] - arrTemp_Sensors[2]);
arrTemp_Diff[2] := ABS(arrTemp_Sensors[2] - arrTemp_Sensors[3]);
arrTemp_Diff[3] := ABS(arrTemp_Sensors[3] - arrTemp_Sensors[1]);

(* Channel A Health Evaluation *)
IF (arrTemp_Diff[1] > rTemp_Tolerance_degC) AND (arrTemp_Diff[3] > rTemp_Tolerance_degC) THEN
    arrTemp_DiscrepTimer_s[1] := arrTemp_DiscrepTimer_s[1] + AI_ControllerCycleTime_s;
    IF arrTemp_DiscrepTimer_s[1] >= rTemp_DiscrepLimit_s THEN
        arrTemp_Healthy[1] := FALSE;
    END_IF;
ELSE
    arrTemp_DiscrepTimer_s[1] := 0.0;
    arrTemp_Healthy[1] := TRUE;
END_IF;

(* Channel B Health Evaluation *)
IF (arrTemp_Diff[1] > rTemp_Tolerance_degC) AND (arrTemp_Diff[2] > rTemp_Tolerance_degC) THEN
    arrTemp_DiscrepTimer_s[2] := arrTemp_DiscrepTimer_s[2] + AI_ControllerCycleTime_s;
    IF arrTemp_DiscrepTimer_s[2] >= rTemp_DiscrepLimit_s THEN
        arrTemp_Healthy[2] := FALSE;
    END_IF;
ELSE
    arrTemp_DiscrepTimer_s[2] := 0.0;
    arrTemp_Healthy[2] := TRUE;
END_IF;

(* Channel C Health Evaluation *)
IF (arrTemp_Diff[2] > rTemp_Tolerance_degC) AND (arrTemp_Diff[3] > rTemp_Tolerance_degC) THEN
    arrTemp_DiscrepTimer_s[3] := arrTemp_DiscrepTimer_s[3] + AI_ControllerCycleTime_s;
    IF arrTemp_DiscrepTimer_s[3] >= rTemp_DiscrepLimit_s THEN
        arrTemp_Healthy[3] := FALSE;
    END_IF;
ELSE
    arrTemp_DiscrepTimer_s[3] := 0.0;
    arrTemp_Healthy[3] := TRUE;
END_IF;

(* Group 3 Voting Execution *)
IF arrTemp_Healthy[1] AND arrTemp_Healthy[2] AND arrTemp_Healthy[3] THEN
    bTemp_Degraded := FALSE;
    bTemp_CriticalFault := FALSE;
    IF ((arrTemp_Sensors[1] >= arrTemp_Sensors[2]) AND (arrTemp_Sensors[1] <= arrTemp_Sensors[3])) OR
       ((arrTemp_Sensors[1] >= arrTemp_Sensors[3]) AND (arrTemp_Sensors[1] <= arrTemp_Sensors[2])) THEN
        rVoted_BrothTemp_degC := arrTemp_Sensors[1];
    ELSIF ((arrTemp_Sensors[2] >= arrTemp_Sensors[1]) AND (arrTemp_Sensors[2] <= arrTemp_Sensors[3])) OR
          ((arrTemp_Sensors[2] >= arrTemp_Sensors[3]) AND (arrTemp_Sensors[2] <= arrTemp_Sensors[1])) THEN
        rVoted_BrothTemp_degC := arrTemp_Sensors[2];
    ELSE
        rVoted_BrothTemp_degC := arrTemp_Sensors[3];
    END_IF;
ELSIF arrTemp_Healthy[1] AND arrTemp_Healthy[2] THEN
    bTemp_Degraded := TRUE;
    bTemp_CriticalFault := FALSE;
    rVoted_BrothTemp_degC := (arrTemp_Sensors[1] + arrTemp_Sensors[2]) * 0.50;
ELSIF arrTemp_Healthy[2] AND arrTemp_Healthy[3] THEN
    bTemp_Degraded := TRUE;
    bTemp_CriticalFault := FALSE;
    rVoted_BrothTemp_degC := (arrTemp_Sensors[2] + arrTemp_Sensors[3]) * 0.50;
ELSIF arrTemp_Healthy[1] AND arrTemp_Healthy[3] THEN
    bTemp_Degraded := TRUE;
    bTemp_CriticalFault := FALSE;
    rVoted_BrothTemp_degC := (arrTemp_Sensors[1] + arrTemp_Sensors[3]) * 0.50;
ELSIF arrTemp_Healthy[1] THEN
    bTemp_Degraded := TRUE;
    bTemp_CriticalFault := FALSE;
    rVoted_BrothTemp_degC := arrTemp_Sensors[1];
ELSIF arrTemp_Healthy[2] THEN
    bTemp_Degraded := TRUE;
    bTemp_CriticalFault := FALSE;
    rVoted_BrothTemp_degC := arrTemp_Sensors[2];
ELSIF arrTemp_Healthy[3] THEN
    bTemp_Degraded := TRUE;
    bTemp_CriticalFault := FALSE;
    rVoted_BrothTemp_degC := arrTemp_Sensors[3];
ELSE
    bTemp_Degraded := TRUE;
    bTemp_CriticalFault := TRUE;
END_IF;

(* Temperature Rate of Change Monitoring [deg C / min] *)
IF AI_ControllerCycleTime_s > 0.001 THEN
    rTemp_RoC_degC_per_min := (rVoted_BrothTemp_degC - rTemp_Prev_degC) / (AI_ControllerCycleTime_s / 60.0);
    rTemp_Prev_degC := rVoted_BrothTemp_degC;
END_IF;

(* ------------------------------------------------------------------------------------------- *)
(* GROUP 4: ATF HOLLOW-FIBER RETENTATE PRESSURE (RetPress A, B, C)                             *)
(* ------------------------------------------------------------------------------------------- *)
arrRetP_Sensors[1] := AI_ATF_RetentatePress_ChA_bar;
arrRetP_Sensors[2] := AI_ATF_RetentatePress_ChB_bar;
arrRetP_Sensors[3] := AI_ATF_RetentatePress_ChC_bar;

arrRetP_Diff[1] := ABS(arrRetP_Sensors[1] - arrRetP_Sensors[2]);
arrRetP_Diff[2] := ABS(arrRetP_Sensors[2] - arrRetP_Sensors[3]);
arrRetP_Diff[3] := ABS(arrRetP_Sensors[3] - arrRetP_Sensors[1]);

IF (arrRetP_Diff[1] > rRetP_Tolerance_bar) AND (arrRetP_Diff[3] > rRetP_Tolerance_bar) THEN
    arrRetP_DiscrepTimer_s[1] := arrRetP_DiscrepTimer_s[1] + AI_ControllerCycleTime_s;
    IF arrRetP_DiscrepTimer_s[1] >= rRetP_DiscrepLimit_s THEN
        arrRetP_Healthy[1] := FALSE;
    END_IF;
ELSE
    arrRetP_DiscrepTimer_s[1] := 0.0;
    arrRetP_Healthy[1] := TRUE;
END_IF;

IF (arrRetP_Diff[1] > rRetP_Tolerance_bar) AND (arrRetP_Diff[2] > rRetP_Tolerance_bar) THEN
    arrRetP_DiscrepTimer_s[2] := arrRetP_DiscrepTimer_s[2] + AI_ControllerCycleTime_s;
    IF arrRetP_DiscrepTimer_s[2] >= rRetP_DiscrepLimit_s THEN
        arrRetP_Healthy[2] := FALSE;
    END_IF;
ELSE
    arrRetP_DiscrepTimer_s[2] := 0.0;
    arrRetP_Healthy[2] := TRUE;
END_IF;

IF (arrRetP_Diff[2] > rRetP_Tolerance_bar) AND (arrRetP_Diff[3] > rRetP_Tolerance_bar) THEN
    arrRetP_DiscrepTimer_s[3] := arrRetP_DiscrepTimer_s[3] + AI_ControllerCycleTime_s;
    IF arrRetP_DiscrepTimer_s[3] >= rRetP_DiscrepLimit_s THEN
        arrRetP_Healthy[3] := FALSE;
    END_IF;
ELSE
    arrRetP_DiscrepTimer_s[3] := 0.0;
    arrRetP_Healthy[3] := TRUE;
END_IF;

IF arrRetP_Healthy[1] AND arrRetP_Healthy[2] AND arrRetP_Healthy[3] THEN
    bRetP_Degraded := FALSE;
    bRetP_CriticalFault := FALSE;
    IF ((arrRetP_Sensors[1] >= arrRetP_Sensors[2]) AND (arrRetP_Sensors[1] <= arrRetP_Sensors[3])) OR
       ((arrRetP_Sensors[1] >= arrRetP_Sensors[3]) AND (arrRetP_Sensors[1] <= arrRetP_Sensors[2])) THEN
        rVoted_ATF_RetentatePress_bar := arrRetP_Sensors[1];
    ELSIF ((arrRetP_Sensors[2] >= arrRetP_Sensors[1]) AND (arrRetP_Sensors[2] <= arrRetP_Sensors[3])) OR
          ((arrRetP_Sensors[2] >= arrRetP_Sensors[3]) AND (arrRetP_Sensors[2] <= arrRetP_Sensors[1])) THEN
        rVoted_ATF_RetentatePress_bar := arrRetP_Sensors[2];
    ELSE
        rVoted_ATF_RetentatePress_bar := arrRetP_Sensors[3];
    END_IF;
ELSIF arrRetP_Healthy[1] AND arrRetP_Healthy[2] THEN
    bRetP_Degraded := TRUE;
    bRetP_CriticalFault := FALSE;
    rVoted_ATF_RetentatePress_bar := (arrRetP_Sensors[1] + arrRetP_Sensors[2]) * 0.50;
ELSIF arrRetP_Healthy[2] AND arrRetP_Healthy[3] THEN
    bRetP_Degraded := TRUE;
    bRetP_CriticalFault := FALSE;
    rVoted_ATF_RetentatePress_bar := (arrRetP_Sensors[2] + arrRetP_Sensors[3]) * 0.50;
ELSIF arrRetP_Healthy[1] AND arrRetP_Healthy[3] THEN
    bRetP_Degraded := TRUE;
    bRetP_CriticalFault := FALSE;
    rVoted_ATF_RetentatePress_bar := (arrRetP_Sensors[1] + arrRetP_Sensors[3]) * 0.50;
ELSIF arrRetP_Healthy[1] THEN
    bRetP_Degraded := TRUE;
    bRetP_CriticalFault := FALSE;
    rVoted_ATF_RetentatePress_bar := arrRetP_Sensors[1];
ELSIF arrRetP_Healthy[2] THEN
    bRetP_Degraded := TRUE;
    bRetP_CriticalFault := FALSE;
    rVoted_ATF_RetentatePress_bar := arrRetP_Sensors[2];
ELSIF arrRetP_Healthy[3] THEN
    bRetP_Degraded := TRUE;
    bRetP_CriticalFault := FALSE;
    rVoted_ATF_RetentatePress_bar := arrRetP_Sensors[3];
ELSE
    bRetP_Degraded := TRUE;
    bRetP_CriticalFault := TRUE;
END_IF;

(* ------------------------------------------------------------------------------------------- *)
(* GROUP 5: ATF HOLLOW-FIBER PERMEATE PRESSURE (PermPress A, B, C)                             *)
(* ------------------------------------------------------------------------------------------- *)
arrPermP_Sensors[1] := AI_ATF_PermeatePress_ChA_bar;
arrPermP_Sensors[2] := AI_ATF_PermeatePress_ChB_bar;
arrPermP_Sensors[3] := AI_ATF_PermeatePress_ChC_bar;

arrPermP_Diff[1] := ABS(arrPermP_Sensors[1] - arrPermP_Sensors[2]);
arrPermP_Diff[2] := ABS(arrPermP_Sensors[2] - arrPermP_Sensors[3]);
arrPermP_Diff[3] := ABS(arrPermP_Sensors[3] - arrPermP_Sensors[1]);

IF (arrPermP_Diff[1] > rPermP_Tolerance_bar) AND (arrPermP_Diff[3] > rPermP_Tolerance_bar) THEN
    arrPermP_DiscrepTimer_s[1] := arrPermP_DiscrepTimer_s[1] + AI_ControllerCycleTime_s;
    IF arrPermP_DiscrepTimer_s[1] >= rPermP_DiscrepLimit_s THEN
        arrPermP_Healthy[1] := FALSE;
    END_IF;
ELSE
    arrPermP_DiscrepTimer_s[1] := 0.0;
    arrPermP_Healthy[1] := TRUE;
END_IF;

IF (arrPermP_Diff[1] > rPermP_Tolerance_bar) AND (arrPermP_Diff[2] > rPermP_Tolerance_bar) THEN
    arrPermP_DiscrepTimer_s[2] := arrPermP_DiscrepTimer_s[2] + AI_ControllerCycleTime_s;
    IF arrPermP_DiscrepTimer_s[2] >= rPermP_DiscrepLimit_s THEN
        arrPermP_Healthy[2] := FALSE;
    END_IF;
ELSE
    arrPermP_DiscrepTimer_s[2] := 0.0;
    arrPermP_Healthy[2] := TRUE;
END_IF;

IF (arrPermP_Diff[2] > rPermP_Tolerance_bar) AND (arrPermP_Diff[3] > rPermP_Tolerance_bar) THEN
    arrPermP_DiscrepTimer_s[3] := arrPermP_DiscrepTimer_s[3] + AI_ControllerCycleTime_s;
    IF arrPermP_DiscrepTimer_s[3] >= rPermP_DiscrepLimit_s THEN
        arrPermP_Healthy[3] := FALSE;
    END_IF;
ELSE
    arrPermP_DiscrepTimer_s[3] := 0.0;
    arrPermP_Healthy[3] := TRUE;
END_IF;

IF arrPermP_Healthy[1] AND arrPermP_Healthy[2] AND arrPermP_Healthy[3] THEN
    bPermP_Degraded := FALSE;
    bPermP_CriticalFault := FALSE;
    IF ((arrPermP_Sensors[1] >= arrPermP_Sensors[2]) AND (arrPermP_Sensors[1] <= arrPermP_Sensors[3])) OR
       ((arrPermP_Sensors[1] >= arrPermP_Sensors[3]) AND (arrPermP_Sensors[1] <= arrPermP_Sensors[2])) THEN
        rVoted_ATF_PermeatePress_bar := arrPermP_Sensors[1];
    ELSIF ((arrPermP_Sensors[2] >= arrPermP_Sensors[1]) AND (arrPermP_Sensors[2] <= arrPermP_Sensors[3])) OR
          ((arrPermP_Sensors[2] >= arrPermP_Sensors[3]) AND (arrPermP_Sensors[2] <= arrPermP_Sensors[1])) THEN
        rVoted_ATF_PermeatePress_bar := arrPermP_Sensors[2];
    ELSE
        rVoted_ATF_PermeatePress_bar := arrPermP_Sensors[3];
    END_IF;
ELSIF arrPermP_Healthy[1] AND arrPermP_Healthy[2] THEN
    bPermP_Degraded := TRUE;
    bPermP_CriticalFault := FALSE;
    rVoted_ATF_PermeatePress_bar := (arrPermP_Sensors[1] + arrPermP_Sensors[2]) * 0.50;
ELSIF arrPermP_Healthy[2] AND arrPermP_Healthy[3] THEN
    bPermP_Degraded := TRUE;
    bPermP_CriticalFault := FALSE;
    rVoted_ATF_PermeatePress_bar := (arrPermP_Sensors[2] + arrPermP_Sensors[3]) * 0.50;
ELSIF arrPermP_Healthy[1] AND arrPermP_Healthy[3] THEN
    bPermP_Degraded := TRUE;
    bPermP_CriticalFault := FALSE;
    rVoted_ATF_PermeatePress_bar := (arrPermP_Sensors[1] + arrPermP_Sensors[3]) * 0.50;
ELSIF arrPermP_Healthy[1] THEN
    bPermP_Degraded := TRUE;
    bPermP_CriticalFault := FALSE;
    rVoted_ATF_PermeatePress_bar := arrPermP_Sensors[1];
ELSIF arrPermP_Healthy[2] THEN
    bPermP_Degraded := TRUE;
    bPermP_CriticalFault := FALSE;
    rVoted_ATF_PermeatePress_bar := arrPermP_Sensors[2];
ELSIF arrPermP_Healthy[3] THEN
    bPermP_Degraded := TRUE;
    bPermP_CriticalFault := FALSE;
    rVoted_ATF_PermeatePress_bar := arrPermP_Sensors[3];
ELSE
    bPermP_Degraded := TRUE;
    bPermP_CriticalFault := TRUE;
END_IF;
"""

print("get_phase1_tmr ready.")
