# mining_flotation_builder/section_phase1_tmr.py
"""
Section: Phase 1 - 2oo3 Triple Modular Redundant (TMR) Sensor Voting Suite
Function Block: FB_Mining_Flotation_RougherScavenger_FrothDepth_ReagentDosing
"""

def get_phase1_tmr():
    return """(* ========================================================================= *)
(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANT SENSOR VOTING & HEALTH     === *)
(* ========================================================================= *)

(* ------------------------------------------------------------------------- *)
(* SUITE 1: PULP SLURRY LEVEL TRANSMITTERS (LT-101A / B / C) [mm]            *)
(* Triplicated Hydrostatic Bubbler & Piezoresistive Diaphragms               *)
(* ------------------------------------------------------------------------- *)
(* Step 1.1: Clamp inputs to allowable physical range *)
IF rPulpLevel_ChA < 0.0 THEN rPulpLevel_ChA_Clamped := 0.0;
ELSIF rPulpLevel_ChA > 4500.0 THEN rPulpLevel_ChA_Clamped := 4500.0;
ELSE rPulpLevel_ChA_Clamped := rPulpLevel_ChA; END_IF;

IF rPulpLevel_ChB < 0.0 THEN rPulpLevel_ChB_Clamped := 0.0;
ELSIF rPulpLevel_ChB > 4500.0 THEN rPulpLevel_ChB_Clamped := 4500.0;
ELSE rPulpLevel_ChB_Clamped := rPulpLevel_ChB; END_IF;

IF rPulpLevel_ChC < 0.0 THEN rPulpLevel_ChC_Clamped := 0.0;
ELSIF rPulpLevel_ChC > 4500.0 THEN rPulpLevel_ChC_Clamped := 4500.0;
ELSE rPulpLevel_ChC_Clamped := rPulpLevel_ChC; END_IF;

(* Step 1.2: Pairwise difference & persistence discrepancy accumulation *)
IF ABS(rPulpLevel_ChA_Clamped - rPulpLevel_ChB_Clamped) > rPulpLevel_DevLimit THEN
    tPulpLevel_Timer_AB := tPulpLevel_Timer_AB + rCycleTimeSec;
ELSE
    tPulpLevel_Timer_AB := MAX(0.0, tPulpLevel_Timer_AB - (rCycleTimeSec * 2.0));
END_IF;

IF ABS(rPulpLevel_ChB_Clamped - rPulpLevel_ChC_Clamped) > rPulpLevel_DevLimit THEN
    tPulpLevel_Timer_BC := tPulpLevel_Timer_BC + rCycleTimeSec;
ELSE
    tPulpLevel_Timer_BC := MAX(0.0, tPulpLevel_Timer_BC - (rCycleTimeSec * 2.0));
END_IF;

IF ABS(rPulpLevel_ChC_Clamped - rPulpLevel_ChA_Clamped) > rPulpLevel_DevLimit THEN
    tPulpLevel_Timer_CA := tPulpLevel_Timer_CA + rCycleTimeSec;
ELSE
    tPulpLevel_Timer_CA := MAX(0.0, tPulpLevel_Timer_CA - (rCycleTimeSec * 2.0));
END_IF;

(* Step 1.3: Channel disqualification logic with 250 ms threshold *)
IF (tPulpLevel_Timer_AB >= rDiscrepancyTripTime) AND (tPulpLevel_Timer_CA >= rDiscrepancyTripTime) THEN
    bFail_PulpLevel_A := TRUE;
END_IF;
IF (tPulpLevel_Timer_AB >= rDiscrepancyTripTime) AND (tPulpLevel_Timer_BC >= rDiscrepancyTripTime) THEN
    bFail_PulpLevel_B := TRUE;
END_IF;
IF (tPulpLevel_Timer_BC >= rDiscrepancyTripTime) AND (tPulpLevel_Timer_CA >= rDiscrepancyTripTime) THEN
    bFail_PulpLevel_C := TRUE;
END_IF;

(* Auto-recovery reset if healthy for 2.0 seconds continuously *)
IF (tPulpLevel_Timer_AB = 0.0) AND (tPulpLevel_Timer_CA = 0.0) AND bReset THEN
    bFail_PulpLevel_A := FALSE;
END_IF;
IF (tPulpLevel_Timer_AB = 0.0) AND (tPulpLevel_Timer_BC = 0.0) AND bReset THEN
    bFail_PulpLevel_B := FALSE;
END_IF;
IF (tPulpLevel_Timer_BC = 0.0) AND (tPulpLevel_Timer_CA = 0.0) AND bReset THEN
    bFail_PulpLevel_C := FALSE;
END_IF;

(* Step 1.4: Multi-mode voting execution *)
IF (NOT bFail_PulpLevel_A) AND (NOT bFail_PulpLevel_B) AND (NOT bFail_PulpLevel_C) THEN
    (* 2oo3 Median Voting *)
    bTMR_PulpLevelDegraded := FALSE;
    IF ((rPulpLevel_ChA_Clamped >= rPulpLevel_ChB_Clamped) AND (rPulpLevel_ChA_Clamped <= rPulpLevel_ChC_Clamped)) OR
       ((rPulpLevel_ChA_Clamped >= rPulpLevel_ChC_Clamped) AND (rPulpLevel_ChA_Clamped <= rPulpLevel_ChB_Clamped)) THEN
        rVoted_PulpLevel := rPulpLevel_ChA_Clamped;
    ELSIF ((rPulpLevel_ChB_Clamped >= rPulpLevel_ChA_Clamped) AND (rPulpLevel_ChB_Clamped <= rPulpLevel_ChC_Clamped)) OR
          ((rPulpLevel_ChB_Clamped >= rPulpLevel_ChC_Clamped) AND (rPulpLevel_ChB_Clamped <= rPulpLevel_ChA_Clamped)) THEN
        rVoted_PulpLevel := rPulpLevel_ChB_Clamped;
    ELSE
        rVoted_PulpLevel := rPulpLevel_ChC_Clamped;
    END_IF;
    rPulpLevel_LastValid := rVoted_PulpLevel;
ELSIF bFail_PulpLevel_A AND (NOT bFail_PulpLevel_B) AND (NOT bFail_PulpLevel_C) THEN
    (* Degraded to 1oo2 Average of B and C *)
    bTMR_PulpLevelDegraded := TRUE;
    rVoted_PulpLevel := (rPulpLevel_ChB_Clamped + rPulpLevel_ChC_Clamped) * 0.5;
    rPulpLevel_LastValid := rVoted_PulpLevel;
ELSIF bFail_PulpLevel_B AND (NOT bFail_PulpLevel_A) AND (NOT bFail_PulpLevel_C) THEN
    (* Degraded to 1oo2 Average of A and C *)
    bTMR_PulpLevelDegraded := TRUE;
    rVoted_PulpLevel := (rPulpLevel_ChA_Clamped + rPulpLevel_ChC_Clamped) * 0.5;
    rPulpLevel_LastValid := rVoted_PulpLevel;
ELSIF bFail_PulpLevel_C AND (NOT bFail_PulpLevel_A) AND (NOT bFail_PulpLevel_B) THEN
    (* Degraded to 1oo2 Average of A and B *)
    bTMR_PulpLevelDegraded := TRUE;
    rVoted_PulpLevel := (rPulpLevel_ChA_Clamped + rPulpLevel_ChB_Clamped) * 0.5;
    rPulpLevel_LastValid := rVoted_PulpLevel;
ELSE
    (* Critical Failure: More than 1 channel failed -> Hold Last Valid *)
    bTMR_PulpLevelDegraded := TRUE;
    rVoted_PulpLevel := rPulpLevel_LastValid;
END_IF;


(* ------------------------------------------------------------------------- *)
(* SUITE 2: FROTH BED THICKNESS / LIP HEIGHT (LT-201A / B / C) [mm]          *)
(* Triplicated Ultrasonic & High-Resolution Non-Contact Laser Sensors        *)
(* ------------------------------------------------------------------------- *)
IF rFrothHeight_ChA < 0.0 THEN rFrothHeight_ChA_Clamped := 0.0;
ELSIF rFrothHeight_ChA > 1000.0 THEN rFrothHeight_ChA_Clamped := 1000.0;
ELSE rFrothHeight_ChA_Clamped := rFrothHeight_ChA; END_IF;

IF rFrothHeight_ChB < 0.0 THEN rFrothHeight_ChB_Clamped := 0.0;
ELSIF rFrothHeight_ChB > 1000.0 THEN rFrothHeight_ChB_Clamped := 1000.0;
ELSE rFrothHeight_ChB_Clamped := rFrothHeight_ChB; END_IF;

IF rFrothHeight_ChC < 0.0 THEN rFrothHeight_ChC_Clamped := 0.0;
ELSIF rFrothHeight_ChC > 1000.0 THEN rFrothHeight_ChC_Clamped := 1000.0;
ELSE rFrothHeight_ChC_Clamped := rFrothHeight_ChC; END_IF;

(* Pairwise differences & timers *)
IF ABS(rFrothHeight_ChA_Clamped - rFrothHeight_ChB_Clamped) > rFrothHeight_DevLimit THEN
    tFrothHeight_Timer_AB := tFrothHeight_Timer_AB + rCycleTimeSec;
ELSE
    tFrothHeight_Timer_AB := MAX(0.0, tFrothHeight_Timer_AB - (rCycleTimeSec * 2.0));
END_IF;

IF ABS(rFrothHeight_ChB_Clamped - rFrothHeight_ChC_Clamped) > rFrothHeight_DevLimit THEN
    tFrothHeight_Timer_BC := tFrothHeight_Timer_BC + rCycleTimeSec;
ELSE
    tFrothHeight_Timer_BC := MAX(0.0, tFrothHeight_Timer_BC - (rCycleTimeSec * 2.0));
END_IF;

IF ABS(rFrothHeight_ChC_Clamped - rFrothHeight_ChA_Clamped) > rFrothHeight_DevLimit THEN
    tFrothHeight_Timer_CA := tFrothHeight_Timer_CA + rCycleTimeSec;
ELSE
    tFrothHeight_Timer_CA := MAX(0.0, tFrothHeight_Timer_CA - (rCycleTimeSec * 2.0));
END_IF;

IF (tFrothHeight_Timer_AB >= rDiscrepancyTripTime) AND (tFrothHeight_Timer_CA >= rDiscrepancyTripTime) THEN
    bFail_FrothHeight_A := TRUE;
END_IF;
IF (tFrothHeight_Timer_AB >= rDiscrepancyTripTime) AND (tFrothHeight_Timer_BC >= rDiscrepancyTripTime) THEN
    bFail_FrothHeight_B := TRUE;
END_IF;
IF (tFrothHeight_Timer_BC >= rDiscrepancyTripTime) AND (tFrothHeight_Timer_CA >= rDiscrepancyTripTime) THEN
    bFail_FrothHeight_C := TRUE;
END_IF;

IF (tFrothHeight_Timer_AB = 0.0) AND (tFrothHeight_Timer_CA = 0.0) AND bReset THEN
    bFail_FrothHeight_A := FALSE;
END_IF;
IF (tFrothHeight_Timer_AB = 0.0) AND (tFrothHeight_Timer_BC = 0.0) AND bReset THEN
    bFail_FrothHeight_B := FALSE;
END_IF;
IF (tFrothHeight_Timer_BC = 0.0) AND (tFrothHeight_Timer_CA = 0.0) AND bReset THEN
    bFail_FrothHeight_C := FALSE;
END_IF;

IF (NOT bFail_FrothHeight_A) AND (NOT bFail_FrothHeight_B) AND (NOT bFail_FrothHeight_C) THEN
    bTMR_FrothHeightDegraded := FALSE;
    IF ((rFrothHeight_ChA_Clamped >= rFrothHeight_ChB_Clamped) AND (rFrothHeight_ChA_Clamped <= rFrothHeight_ChC_Clamped)) OR
       ((rFrothHeight_ChA_Clamped >= rFrothHeight_ChC_Clamped) AND (rFrothHeight_ChA_Clamped <= rFrothHeight_ChB_Clamped)) THEN
        rVoted_FrothThickness := rFrothHeight_ChA_Clamped;
    ELSIF ((rFrothHeight_ChB_Clamped >= rFrothHeight_ChA_Clamped) AND (rFrothHeight_ChB_Clamped <= rFrothHeight_ChC_Clamped)) OR
          ((rFrothHeight_ChB_Clamped >= rFrothHeight_ChC_Clamped) AND (rFrothHeight_ChB_Clamped <= rFrothHeight_ChA_Clamped)) THEN
        rVoted_FrothThickness := rFrothHeight_ChB_Clamped;
    ELSE
        rVoted_FrothThickness := rFrothHeight_ChC_Clamped;
    END_IF;
    rFrothHeight_LastValid := rVoted_FrothThickness;
ELSIF bFail_FrothHeight_A AND (NOT bFail_FrothHeight_B) AND (NOT bFail_FrothHeight_C) THEN
    bTMR_FrothHeightDegraded := TRUE;
    rVoted_FrothThickness := (rFrothHeight_ChB_Clamped + rFrothHeight_ChC_Clamped) * 0.5;
    rFrothHeight_LastValid := rVoted_FrothThickness;
ELSIF bFail_FrothHeight_B AND (NOT bFail_FrothHeight_A) AND (NOT bFail_FrothHeight_C) THEN
    bTMR_FrothHeightDegraded := TRUE;
    rVoted_FrothThickness := (rFrothHeight_ChA_Clamped + rFrothHeight_ChC_Clamped) * 0.5;
    rFrothHeight_LastValid := rVoted_FrothThickness;
ELSIF bFail_FrothHeight_C AND (NOT bFail_FrothHeight_A) AND (NOT bFail_FrothHeight_B) THEN
    bTMR_FrothHeightDegraded := TRUE;
    rVoted_FrothThickness := (rFrothHeight_ChA_Clamped + rFrothHeight_ChB_Clamped) * 0.5;
    rFrothHeight_LastValid := rVoted_FrothThickness;
ELSE
    bTMR_FrothHeightDegraded := TRUE;
    rVoted_FrothThickness := rFrothHeight_LastValid;
END_IF;


(* ------------------------------------------------------------------------- *)
(* SUITE 3: PULP CONDITIONING SLURRY pH ANALYZERS (AT-301A / B / C) [pH]     *)
(* Triplicated Differential Glass / Antimony Industrial Electrodes           *)
(* ------------------------------------------------------------------------- *)
IF rPulpPH_ChA < 2.0 THEN rPulpPH_ChA_Clamped := 2.0;
ELSIF rPulpPH_ChA > 14.0 THEN rPulpPH_ChA_Clamped := 14.0;
ELSE rPulpPH_ChA_Clamped := rPulpPH_ChA; END_IF;

IF rPulpPH_ChB < 2.0 THEN rPulpPH_ChB_Clamped := 2.0;
ELSIF rPulpPH_ChB > 14.0 THEN rPulpPH_ChB_Clamped := 14.0;
ELSE rPulpPH_ChB_Clamped := rPulpPH_ChB; END_IF;

IF rPulpPH_ChC < 2.0 THEN rPulpPH_ChC_Clamped := 2.0;
ELSIF rPulpPH_ChC > 14.0 THEN rPulpPH_ChC_Clamped := 14.0;
ELSE rPulpPH_ChC_Clamped := rPulpPH_ChC; END_IF;

IF ABS(rPulpPH_ChA_Clamped - rPulpPH_ChB_Clamped) > rPH_DevLimit THEN
    tPH_Timer_AB := tPH_Timer_AB + rCycleTimeSec;
ELSE
    tPH_Timer_AB := MAX(0.0, tPH_Timer_AB - (rCycleTimeSec * 2.0));
END_IF;

IF ABS(rPulpPH_ChB_Clamped - rPulpPH_ChC_Clamped) > rPH_DevLimit THEN
    tPH_Timer_BC := tPH_Timer_BC + rCycleTimeSec;
ELSE
    tPH_Timer_BC := MAX(0.0, tPH_Timer_BC - (rCycleTimeSec * 2.0));
END_IF;

IF ABS(rPulpPH_ChC_Clamped - rPulpPH_ChA_Clamped) > rPH_DevLimit THEN
    tPH_Timer_CA := tPH_Timer_CA + rCycleTimeSec;
ELSE
    tPH_Timer_CA := MAX(0.0, tPH_Timer_CA - (rCycleTimeSec * 2.0));
END_IF;

IF (tPH_Timer_AB >= rDiscrepancyTripTime) AND (tPH_Timer_CA >= rDiscrepancyTripTime) THEN
    bFail_PH_A := TRUE;
END_IF;
IF (tPH_Timer_AB >= rDiscrepancyTripTime) AND (tPH_Timer_BC >= rDiscrepancyTripTime) THEN
    bFail_PH_B := TRUE;
END_IF;
IF (tPH_Timer_BC >= rDiscrepancyTripTime) AND (tPH_Timer_CA >= rDiscrepancyTripTime) THEN
    bFail_PH_C := TRUE;
END_IF;

IF (tPH_Timer_AB = 0.0) AND (tPH_Timer_CA = 0.0) AND bReset THEN
    bFail_PH_A := FALSE;
END_IF;
IF (tPH_Timer_AB = 0.0) AND (tPH_Timer_BC = 0.0) AND bReset THEN
    bFail_PH_B := FALSE;
END_IF;
IF (tPH_Timer_BC = 0.0) AND (tPH_Timer_CA = 0.0) AND bReset THEN
    bFail_PH_C := FALSE;
END_IF;

IF (NOT bFail_PH_A) AND (NOT bFail_PH_B) AND (NOT bFail_PH_C) THEN
    bTMR_PH_Degraded := FALSE;
    IF ((rPulpPH_ChA_Clamped >= rPulpPH_ChB_Clamped) AND (rPulpPH_ChA_Clamped <= rPulpPH_ChC_Clamped)) OR
       ((rPulpPH_ChA_Clamped >= rPulpPH_ChC_Clamped) AND (rPulpPH_ChA_Clamped <= rPulpPH_ChB_Clamped)) THEN
        rVoted_PulpPH := rPulpPH_ChA_Clamped;
    ELSIF ((rPulpPH_ChB_Clamped >= rPulpPH_ChA_Clamped) AND (rPulpPH_ChB_Clamped <= rPulpPH_ChC_Clamped)) OR
          ((rPulpPH_ChB_Clamped >= rPulpPH_ChC_Clamped) AND (rPulpPH_ChB_Clamped <= rPulpPH_ChA_Clamped)) THEN
        rVoted_PulpPH := rPulpPH_ChB_Clamped;
    ELSE
        rVoted_PulpPH := rPulpPH_ChC_Clamped;
    END_IF;
    rPH_LastValid := rVoted_PulpPH;
ELSIF bFail_PH_A AND (NOT bFail_PH_B) AND (NOT bFail_PH_C) THEN
    bTMR_PH_Degraded := TRUE;
    rVoted_PulpPH := (rPulpPH_ChB_Clamped + rPulpPH_ChC_Clamped) * 0.5;
    rPH_LastValid := rVoted_PulpPH;
ELSIF bFail_PH_B AND (NOT bFail_PH_A) AND (NOT bFail_PH_C) THEN
    bTMR_PH_Degraded := TRUE;
    rVoted_PulpPH := (rPulpPH_ChA_Clamped + rPulpPH_ChC_Clamped) * 0.5;
    rPH_LastValid := rVoted_PulpPH;
ELSIF bFail_PH_C AND (NOT bFail_PH_A) AND (NOT bFail_PH_B) THEN
    bTMR_PH_Degraded := TRUE;
    rVoted_PulpPH := (rPulpPH_ChA_Clamped + rPulpPH_ChB_Clamped) * 0.5;
    rPH_LastValid := rVoted_PulpPH;
ELSE
    bTMR_PH_Degraded := TRUE;
    rVoted_PulpPH := rPH_LastValid;
END_IF;


(* ------------------------------------------------------------------------- *)
(* SUITE 4: NUCLEAR SLURRY DENSITY GAUGES (DT-401A / B / C) [kg/m3]          *)
(* Triplicated Non-Contact Cesium-137 Gamma Density Transmitters              *)
(* ------------------------------------------------------------------------- *)
IF rSlurryDensity_ChA < 1000.0 THEN rSlurryDensity_ChA_Clamped := 1000.0;
ELSIF rSlurryDensity_ChA > 2400.0 THEN rSlurryDensity_ChA_Clamped := 2400.0;
ELSE rSlurryDensity_ChA_Clamped := rSlurryDensity_ChA; END_IF;

IF rSlurryDensity_ChB < 1000.0 THEN rSlurryDensity_ChB_Clamped := 1000.0;
ELSIF rSlurryDensity_ChB > 2400.0 THEN rSlurryDensity_ChB_Clamped := 2400.0;
ELSE rSlurryDensity_ChB_Clamped := rSlurryDensity_ChB; END_IF;

IF rSlurryDensity_ChC < 1000.0 THEN rSlurryDensity_ChC_Clamped := 1000.0;
ELSIF rSlurryDensity_ChC > 2400.0 THEN rSlurryDensity_ChC_Clamped := 2400.0;
ELSE rSlurryDensity_ChC_Clamped := rSlurryDensity_ChC; END_IF;

IF ABS(rSlurryDensity_ChA_Clamped - rSlurryDensity_ChB_Clamped) > rDensity_DevLimit THEN
    tDensity_Timer_AB := tDensity_Timer_AB + rCycleTimeSec;
ELSE
    tDensity_Timer_AB := MAX(0.0, tDensity_Timer_AB - (rCycleTimeSec * 2.0));
END_IF;

IF ABS(rSlurryDensity_ChB_Clamped - rSlurryDensity_ChC_Clamped) > rDensity_DevLimit THEN
    tDensity_Timer_BC := tDensity_Timer_BC + rCycleTimeSec;
ELSE
    tDensity_Timer_BC := MAX(0.0, tDensity_Timer_BC - (rCycleTimeSec * 2.0));
END_IF;

IF ABS(rSlurryDensity_ChC_Clamped - rSlurryDensity_ChA_Clamped) > rDensity_DevLimit THEN
    tDensity_Timer_CA := tDensity_Timer_CA + rCycleTimeSec;
ELSE
    tDensity_Timer_CA := MAX(0.0, tDensity_Timer_CA - (rCycleTimeSec * 2.0));
END_IF;

IF (tDensity_Timer_AB >= rDiscrepancyTripTime) AND (tDensity_Timer_CA >= rDiscrepancyTripTime) THEN
    bFail_Density_A := TRUE;
END_IF;
IF (tDensity_Timer_AB >= rDiscrepancyTripTime) AND (tDensity_Timer_BC >= rDiscrepancyTripTime) THEN
    bFail_Density_B := TRUE;
END_IF;
IF (tDensity_Timer_BC >= rDiscrepancyTripTime) AND (tDensity_Timer_CA >= rDiscrepancyTripTime) THEN
    bFail_Density_C := TRUE;
END_IF;

IF (tDensity_Timer_AB = 0.0) AND (tDensity_Timer_CA = 0.0) AND bReset THEN
    bFail_Density_A := FALSE;
END_IF;
IF (tDensity_Timer_AB = 0.0) AND (tDensity_Timer_BC = 0.0) AND bReset THEN
    bFail_Density_B := FALSE;
END_IF;
IF (tDensity_Timer_BC = 0.0) AND (tDensity_Timer_CA = 0.0) AND bReset THEN
    bFail_Density_C := FALSE;
END_IF;

IF (NOT bFail_Density_A) AND (NOT bFail_Density_B) AND (NOT bFail_Density_C) THEN
    bTMR_DensityDegraded := FALSE;
    IF ((rSlurryDensity_ChA_Clamped >= rSlurryDensity_ChB_Clamped) AND (rSlurryDensity_ChA_Clamped <= rSlurryDensity_ChC_Clamped)) OR
       ((rSlurryDensity_ChA_Clamped >= rSlurryDensity_ChC_Clamped) AND (rSlurryDensity_ChA_Clamped <= rSlurryDensity_ChB_Clamped)) THEN
        rVoted_SlurryDensity := rSlurryDensity_ChA_Clamped;
    ELSIF ((rSlurryDensity_ChB_Clamped >= rSlurryDensity_ChA_Clamped) AND (rSlurryDensity_ChB_Clamped <= rSlurryDensity_ChC_Clamped)) OR
          ((rSlurryDensity_ChB_Clamped >= rSlurryDensity_ChC_Clamped) AND (rSlurryDensity_ChB_Clamped <= rSlurryDensity_ChA_Clamped)) THEN
        rVoted_SlurryDensity := rSlurryDensity_ChB_Clamped;
    ELSE
        rVoted_SlurryDensity := rSlurryDensity_ChC_Clamped;
    END_IF;
    rDensity_LastValid := rVoted_SlurryDensity;
ELSIF bFail_Density_A AND (NOT bFail_Density_B) AND (NOT bFail_Density_C) THEN
    bTMR_DensityDegraded := TRUE;
    rVoted_SlurryDensity := (rSlurryDensity_ChB_Clamped + rSlurryDensity_ChC_Clamped) * 0.5;
    rDensity_LastValid := rVoted_SlurryDensity;
ELSIF bFail_Density_B AND (NOT bFail_Density_A) AND (NOT bFail_Density_C) THEN
    bTMR_DensityDegraded := TRUE;
    rVoted_SlurryDensity := (rSlurryDensity_ChA_Clamped + rSlurryDensity_ChC_Clamped) * 0.5;
    rDensity_LastValid := rVoted_SlurryDensity;
ELSIF bFail_Density_C AND (NOT bFail_Density_A) AND (NOT bFail_Density_B) THEN
    bTMR_DensityDegraded := TRUE;
    rVoted_SlurryDensity := (rSlurryDensity_ChA_Clamped + rSlurryDensity_ChB_Clamped) * 0.5;
    rDensity_LastValid := rVoted_SlurryDensity;
ELSE
    bTMR_DensityDegraded := TRUE;
    rVoted_SlurryDensity := rDensity_LastValid;
END_IF;

(* Reconcile Total Pulp + Froth Head *)
rCalculated_TotalPulpFrothHead := rVoted_PulpLevel + rVoted_FrothThickness;
"""
