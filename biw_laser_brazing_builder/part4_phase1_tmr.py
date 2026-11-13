# biw_laser_brazing_builder/part4_phase1_tmr.py
"""
Part 4: Phase 1 - 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Engine
Function Block: FB_Automotive_BIW_LaserBrazing_StructuralAdhesive
"""

def get_phase1_tmr():
    return """(* ============================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY ACCUMULATION     *)
(* Discrepancy Persistence Threshold = 100 ms (50 Consecutive PLC Execution Scans @ Ts = 2.0 ms)  *)
(* Channels: Pyrometers [deg C], Seam Trackers [um], Pressure [bar], Mass Flow [g/s], Clamps [N]  *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* CHANNEL 1: COAXIAL OPTICAL PYROMETERS (TT_PYRO_101A/B/C) [deg C]                               *)
(* ---------------------------------------------------------------------------------------------- *)
(* Step 1.1: First-Order Low-Pass Digital Filtering (tau = 10 ms) *)
rPyro_FiltA := rPyro_FiltA + rFilterAlpha * (rTT_Pyro_101A - rPyro_FiltA);
rPyro_FiltB := rPyro_FiltB + rFilterAlpha * (rTT_Pyro_101B - rPyro_FiltB);
rPyro_FiltC := rPyro_FiltC + rFilterAlpha * (rTT_Pyro_101C - rPyro_FiltC);

(* Step 1.2: Pairwise Absolute Deviation Computation *)
rPyro_DiffAB := ABS(rPyro_FiltA - rPyro_FiltB);
rPyro_DiffBC := ABS(rPyro_FiltB - rPyro_FiltC);
rPyro_DiffCA := ABS(rPyro_FiltC - rPyro_FiltA);

(* Step 1.3: Pairwise Discrepancy Debounce Timers (100 ms Persistence) *)
IF rPyro_DiffAB > rPyro_Tol THEN
    IF udiPyro_DiscAB_Count < udiDiscrepancyLimit THEN
        udiPyro_DiscAB_Count := udiPyro_DiscAB_Count + 1;
    END_IF;
ELSE
    IF udiPyro_DiscAB_Count > 0 THEN
        udiPyro_DiscAB_Count := udiPyro_DiscAB_Count - 1;
    END_IF;
END_IF;

IF rPyro_DiffBC > rPyro_Tol THEN
    IF udiPyro_DiscBC_Count < udiDiscrepancyLimit THEN
        udiPyro_DiscBC_Count := udiPyro_DiscBC_Count + 1;
    END_IF;
ELSE
    IF udiPyro_DiscBC_Count > 0 THEN
        udiPyro_DiscBC_Count := udiPyro_DiscBC_Count - 1;
    END_IF;
END_IF;

IF rPyro_DiffCA > rPyro_Tol THEN
    IF udiPyro_DiscCA_Count < udiDiscrepancyLimit THEN
        udiPyro_DiscCA_Count := udiPyro_DiscCA_Count + 1;
    END_IF;
ELSE
    IF udiPyro_DiscCA_Count > 0 THEN
        udiPyro_DiscCA_Count := udiPyro_DiscCA_Count - 1;
    END_IF;
END_IF;

(* Step 1.4: Cross-Channel Health Isolation Logic *)
IF (udiPyro_DiscAB_Count >= udiDiscrepancyLimit) AND (udiPyro_DiscCA_Count >= udiDiscrepancyLimit) THEN
    bPyro_A_Healthy := FALSE; (* Channel A diverged from both B and C *)
ELSE
    IF (udiPyro_DiscAB_Count = 0) AND (udiPyro_DiscCA_Count = 0) THEN
        bPyro_A_Healthy := TRUE;
    END_IF;
END_IF;

IF (udiPyro_DiscAB_Count >= udiDiscrepancyLimit) AND (udiPyro_DiscBC_Count >= udiDiscrepancyLimit) THEN
    bPyro_B_Healthy := FALSE; (* Channel B diverged from both A and C *)
ELSE
    IF (udiPyro_DiscAB_Count = 0) AND (udiPyro_DiscBC_Count = 0) THEN
        bPyro_B_Healthy := TRUE;
    END_IF;
END_IF;

IF (udiPyro_DiscBC_Count >= udiDiscrepancyLimit) AND (udiPyro_DiscCA_Count >= udiDiscrepancyLimit) THEN
    bPyro_C_Healthy := FALSE; (* Channel C diverged from both A and B *)
ELSE
    IF (udiPyro_DiscBC_Count = 0) AND (udiPyro_DiscCA_Count = 0) THEN
        bPyro_C_Healthy := TRUE;
    END_IF;
END_IF;

nPyro_HealthyTotal := BOOL_TO_INT(bPyro_A_Healthy) + BOOL_TO_INT(bPyro_B_Healthy) + BOOL_TO_INT(bPyro_C_Healthy);

(* Step 1.5: Multi-Tier Bumpless Voting Arbitration *)
IF nPyro_HealthyTotal = 3 THEN
    (* 2oo3 Median Voting: Sort A, B, C *)
    rSortA := rPyro_FiltA;
    rSortB := rPyro_FiltB;
    rSortC := rPyro_FiltC;
    IF rSortA > rSortB THEN
        rSortTemp := rSortA; rSortA := rSortB; rSortB := rSortTemp;
    END_IF;
    IF rSortB > rSortC THEN
        rSortTemp := rSortB; rSortB := rSortC; rSortC := rSortTemp;
    END_IF;
    IF rSortA > rSortB THEN
        rSortTemp := rSortA; rSortA := rSortB; rSortB := rSortTemp;
    END_IF;
    rPyro_VotedVal := rSortB; (* Median channel selected *)
    bPyro_ChannelDegraded := FALSE;
    bPyro_AllFaultTrip := FALSE;
ELSIF nPyro_HealthyTotal = 2 THEN
    (* 1oo2 Degraded Dual-Averaging *)
    IF NOT bPyro_A_Healthy THEN
        rPyro_VotedVal := (rPyro_FiltB + rPyro_FiltC) * 0.50;
    ELSIF NOT bPyro_B_Healthy THEN
        rPyro_VotedVal := (rPyro_FiltA + rPyro_FiltC) * 0.50;
    ELSE
        rPyro_VotedVal := (rPyro_FiltA + rPyro_FiltB) * 0.50;
    END_IF;
    bPyro_ChannelDegraded := TRUE;
    bPyro_AllFaultTrip := FALSE;
ELSIF nPyro_HealthyTotal = 1 THEN
    (* Single Surviving Channel Fallback *)
    IF bPyro_A_Healthy THEN
        rPyro_VotedVal := rPyro_FiltA;
    ELSIF bPyro_B_Healthy THEN
        rPyro_VotedVal := rPyro_FiltB;
    ELSE
        rPyro_VotedVal := rPyro_FiltC;
    END_IF;
    bPyro_ChannelDegraded := TRUE;
    bPyro_AllFaultTrip := FALSE;
ELSE
    (* Total TMR Sensor Loss: Safe Hold and Trip *)
    bPyro_ChannelDegraded := TRUE;
    bPyro_AllFaultTrip := TRUE;
END_IF;


(* ---------------------------------------------------------------------------------------------- *)
(* CHANNEL 2: 3D LASER SEAM TRIANGULATION PROFILOMETERS (LT_SEAM_201A/B/C) [um]                   *)
(* ---------------------------------------------------------------------------------------------- *)
(* Step 2.1: First-Order Low-Pass Filtering *)
rSeam_FiltA := rSeam_FiltA + rFilterAlpha * (rLT_Seam_201A - rSeam_FiltA);
rSeam_FiltB := rSeam_FiltB + rFilterAlpha * (rLT_Seam_201B - rSeam_FiltB);
rSeam_FiltC := rSeam_FiltC + rFilterAlpha * (rLT_Seam_201C - rSeam_FiltC);

(* Step 2.2: Pairwise Differences *)
rSeam_DiffAB := ABS(rSeam_FiltA - rSeam_FiltB);
rSeam_DiffBC := ABS(rSeam_FiltB - rSeam_FiltC);
rSeam_DiffCA := ABS(rSeam_FiltC - rSeam_FiltA);

(* Step 2.3: Discrepancy Debounce Timers *)
IF rSeam_DiffAB > rSeam_Tol THEN
    IF udiSeam_DiscAB_Count < udiDiscrepancyLimit THEN
        udiSeam_DiscAB_Count := udiSeam_DiscAB_Count + 1;
    END_IF;
ELSE
    IF udiSeam_DiscAB_Count > 0 THEN
        udiSeam_DiscAB_Count := udiSeam_DiscAB_Count - 1;
    END_IF;
END_IF;

IF rSeam_DiffBC > rSeam_Tol THEN
    IF udiSeam_DiscBC_Count < udiDiscrepancyLimit THEN
        udiSeam_DiscBC_Count := udiSeam_DiscBC_Count + 1;
    END_IF;
ELSE
    IF udiSeam_DiscBC_Count > 0 THEN
        udiSeam_DiscBC_Count := udiSeam_DiscBC_Count - 1;
    END_IF;
END_IF;

IF rSeam_DiffCA > rSeam_Tol THEN
    IF udiSeam_DiscCA_Count < udiDiscrepancyLimit THEN
        udiSeam_DiscCA_Count := udiSeam_DiscCA_Count + 1;
    END_IF;
ELSE
    IF udiSeam_DiscCA_Count > 0 THEN
        udiSeam_DiscCA_Count := udiSeam_DiscCA_Count - 1;
    END_IF;
END_IF;

(* Step 2.4: Cross-Channel Health Isolation *)
IF (udiSeam_DiscAB_Count >= udiDiscrepancyLimit) AND (udiSeam_DiscCA_Count >= udiDiscrepancyLimit) THEN
    bSeam_A_Healthy := FALSE;
ELSE
    IF (udiSeam_DiscAB_Count = 0) AND (udiSeam_DiscCA_Count = 0) THEN
        bSeam_A_Healthy := TRUE;
    END_IF;
END_IF;

IF (udiSeam_DiscAB_Count >= udiDiscrepancyLimit) AND (udiSeam_DiscBC_Count >= udiDiscrepancyLimit) THEN
    bSeam_B_Healthy := FALSE;
ELSE
    IF (udiSeam_DiscAB_Count = 0) AND (udiSeam_DiscBC_Count = 0) THEN
        bSeam_B_Healthy := TRUE;
    END_IF;
END_IF;

IF (udiSeam_DiscBC_Count >= udiDiscrepancyLimit) AND (udiSeam_DiscCA_Count >= udiDiscrepancyLimit) THEN
    bSeam_C_Healthy := FALSE;
ELSE
    IF (udiSeam_DiscBC_Count = 0) AND (udiSeam_DiscCA_Count = 0) THEN
        bSeam_C_Healthy := TRUE;
    END_IF;
END_IF;

nSeam_HealthyTotal := BOOL_TO_INT(bSeam_A_Healthy) + BOOL_TO_INT(bSeam_B_Healthy) + BOOL_TO_INT(bSeam_C_Healthy);

(* Step 2.5: Multi-Tier Voting Arbitration *)
IF nSeam_HealthyTotal = 3 THEN
    rSortA := rSeam_FiltA;
    rSortB := rSeam_FiltB;
    rSortC := rSeam_FiltC;
    IF rSortA > rSortB THEN
        rSortTemp := rSortA; rSortA := rSortB; rSortB := rSortTemp;
    END_IF;
    IF rSortB > rSortC THEN
        rSortTemp := rSortB; rSortB := rSortC; rSortC := rSortTemp;
    END_IF;
    IF rSortA > rSortB THEN
        rSortTemp := rSortA; rSortA := rSortB; rSortB := rSortTemp;
    END_IF;
    rSeam_VotedVal := rSortB;
    bSeam_ChannelDegraded := FALSE;
    bSeam_AllFaultTrip := FALSE;
ELSIF nSeam_HealthyTotal = 2 THEN
    IF NOT bSeam_A_Healthy THEN
        rSeam_VotedVal := (rSeam_FiltB + rSeam_FiltC) * 0.50;
    ELSIF NOT bSeam_B_Healthy THEN
        rSeam_VotedVal := (rSeam_FiltA + rSeam_FiltC) * 0.50;
    ELSE
        rSeam_VotedVal := (rSeam_FiltA + rSeam_FiltB) * 0.50;
    END_IF;
    bSeam_ChannelDegraded := TRUE;
    bSeam_AllFaultTrip := FALSE;
ELSIF nSeam_HealthyTotal = 1 THEN
    IF bSeam_A_Healthy THEN
        rSeam_VotedVal := rSeam_FiltA;
    ELSIF bSeam_B_Healthy THEN
        rSeam_VotedVal := rSeam_FiltB;
    ELSE
        rSeam_VotedVal := rSeam_FiltC;
    END_IF;
    bSeam_ChannelDegraded := TRUE;
    bSeam_AllFaultTrip := FALSE;
ELSE
    bSeam_ChannelDegraded := TRUE;
    bSeam_AllFaultTrip := TRUE;
END_IF;


(* ---------------------------------------------------------------------------------------------- *)
(* CHANNEL 3: ADHESIVE HIGH-PRESSURE TRANSDUCERS (PT_ADH_301A/B/C) [bar]                          *)
(* ---------------------------------------------------------------------------------------------- *)
(* Step 3.1: First-Order Low-Pass Filtering *)
rAdhP_FiltA := rAdhP_FiltA + rFilterAlpha * (rPT_Adh_301A - rAdhP_FiltA);
rAdhP_FiltB := rAdhP_FiltB + rFilterAlpha * (rPT_Adh_301B - rAdhP_FiltB);
rAdhP_FiltC := rAdhP_FiltC + rFilterAlpha * (rPT_Adh_301C - rAdhP_FiltC);

(* Step 3.2: Pairwise Differences *)
rAdhP_DiffAB := ABS(rAdhP_FiltA - rAdhP_FiltB);
rAdhP_DiffBC := ABS(rAdhP_FiltB - rAdhP_FiltC);
rAdhP_DiffCA := ABS(rAdhP_FiltC - rAdhP_FiltA);

(* Step 3.3: Discrepancy Debounce Timers *)
IF rAdhP_DiffAB > rAdhP_Tol THEN
    IF udiAdhP_DiscAB_Count < udiDiscrepancyLimit THEN
        udiAdhP_DiscAB_Count := udiAdhP_DiscAB_Count + 1;
    END_IF;
ELSE
    IF udiAdhP_DiscAB_Count > 0 THEN
        udiAdhP_DiscAB_Count := udiAdhP_DiscAB_Count - 1;
    END_IF;
END_IF;

IF rAdhP_DiffBC > rAdhP_Tol THEN
    IF udiAdhP_DiscBC_Count < udiDiscrepancyLimit THEN
        udiAdhP_DiscBC_Count := udiAdhP_DiscBC_Count + 1;
    END_IF;
ELSE
    IF udiAdhP_DiscBC_Count > 0 THEN
        udiAdhP_DiscBC_Count := udiAdhP_DiscBC_Count - 1;
    END_IF;
END_IF;

IF rAdhP_DiffCA > rAdhP_Tol THEN
    IF udiAdhP_DiscCA_Count < udiDiscrepancyLimit THEN
        udiAdhP_DiscCA_Count := udiAdhP_DiscCA_Count + 1;
    END_IF;
ELSE
    IF udiAdhP_DiscCA_Count > 0 THEN
        udiAdhP_DiscCA_Count := udiAdhP_DiscCA_Count - 1;
    END_IF;
END_IF;

(* Step 3.4: Cross-Channel Health Isolation *)
IF (udiAdhP_DiscAB_Count >= udiDiscrepancyLimit) AND (udiAdhP_DiscCA_Count >= udiDiscrepancyLimit) THEN
    bAdhP_A_Healthy := FALSE;
ELSE
    IF (udiAdhP_DiscAB_Count = 0) AND (udiAdhP_DiscCA_Count = 0) THEN
        bAdhP_A_Healthy := TRUE;
    END_IF;
END_IF;

IF (udiAdhP_DiscAB_Count >= udiDiscrepancyLimit) AND (udiAdhP_DiscBC_Count >= udiDiscrepancyLimit) THEN
    bAdhP_B_Healthy := FALSE;
ELSE
    IF (udiAdhP_DiscAB_Count = 0) AND (udiAdhP_DiscBC_Count = 0) THEN
        bAdhP_B_Healthy := TRUE;
    END_IF;
END_IF;

IF (udiAdhP_DiscBC_Count >= udiDiscrepancyLimit) AND (udiAdhP_DiscCA_Count >= udiDiscrepancyLimit) THEN
    bAdhP_C_Healthy := FALSE;
ELSE
    IF (udiAdhP_DiscBC_Count = 0) AND (udiAdhP_DiscCA_Count = 0) THEN
        bAdhP_C_Healthy := TRUE;
    END_IF;
END_IF;

nAdhP_HealthyTotal := BOOL_TO_INT(bAdhP_A_Healthy) + BOOL_TO_INT(bAdhP_B_Healthy) + BOOL_TO_INT(bAdhP_C_Healthy);

(* Step 3.5: Multi-Tier Voting Arbitration *)
IF nAdhP_HealthyTotal = 3 THEN
    rSortA := rAdhP_FiltA;
    rSortB := rAdhP_FiltB;
    rSortC := rAdhP_FiltC;
    IF rSortA > rSortB THEN
        rSortTemp := rSortA; rSortA := rSortB; rSortB := rSortTemp;
    END_IF;
    IF rSortB > rSortC THEN
        rSortTemp := rSortB; rSortB := rSortC; rSortC := rSortTemp;
    END_IF;
    IF rSortA > rSortB THEN
        rSortTemp := rSortA; rSortA := rSortB; rSortB := rSortTemp;
    END_IF;
    rAdhP_VotedVal := rSortB;
    bAdhP_ChannelDegraded := FALSE;
    bAdhP_AllFaultTrip := FALSE;
ELSIF nAdhP_HealthyTotal = 2 THEN
    IF NOT bAdhP_A_Healthy THEN
        rAdhP_VotedVal := (rAdhP_FiltB + rAdhP_FiltC) * 0.50;
    ELSIF NOT bAdhP_B_Healthy THEN
        rAdhP_VotedVal := (rAdhP_FiltA + rAdhP_FiltC) * 0.50;
    ELSE
        rAdhP_VotedVal := (rAdhP_FiltA + rAdhP_FiltB) * 0.50;
    END_IF;
    bAdhP_ChannelDegraded := TRUE;
    bAdhP_AllFaultTrip := FALSE;
ELSIF nAdhP_HealthyTotal = 1 THEN
    IF bAdhP_A_Healthy THEN
        rAdhP_VotedVal := rAdhP_FiltA;
    ELSIF bAdhP_B_Healthy THEN
        rAdhP_VotedVal := rAdhP_FiltB;
    ELSE
        rAdhP_VotedVal := rAdhP_FiltC;
    END_IF;
    bAdhP_ChannelDegraded := TRUE;
    bAdhP_AllFaultTrip := FALSE;
ELSE
    bAdhP_ChannelDegraded := TRUE;
    bAdhP_AllFaultTrip := TRUE;
END_IF;


(* ---------------------------------------------------------------------------------------------- *)
(* CHANNEL 4: IN-LINE CORIOLIS MASS FLOWMETERS (FT_ADH_401A/B/C) [g/s]                             *)
(* ---------------------------------------------------------------------------------------------- *)
(* Step 4.1: First-Order Low-Pass Filtering *)
rAdhF_FiltA := rAdhF_FiltA + rFilterAlpha * (rFT_Adh_401A - rAdhF_FiltA);
rAdhF_FiltB := rAdhF_FiltB + rFilterAlpha * (rFT_Adh_401B - rAdhF_FiltB);
rAdhF_FiltC := rAdhF_FiltC + rFilterAlpha * (rFT_Adh_401C - rAdhF_FiltC);

(* Step 4.2: Pairwise Differences *)
rAdhF_DiffAB := ABS(rAdhF_FiltA - rAdhF_FiltB);
rAdhF_DiffBC := ABS(rAdhF_FiltB - rAdhF_FiltC);
rAdhF_DiffCA := ABS(rAdhF_FiltC - rAdhF_FiltA);

(* Step 4.3: Discrepancy Debounce Timers *)
IF rAdhF_DiffAB > rAdhF_Tol THEN
    IF udiAdhF_DiscAB_Count < udiDiscrepancyLimit THEN
        udiAdhF_DiscAB_Count := udiAdhF_DiscAB_Count + 1;
    END_IF;
ELSE
    IF udiAdhF_DiscAB_Count > 0 THEN
        udiAdhF_DiscAB_Count := udiAdhF_DiscAB_Count - 1;
    END_IF;
END_IF;

IF rAdhF_DiffBC > rAdhF_Tol THEN
    IF udiAdhF_DiscBC_Count < udiDiscrepancyLimit THEN
        udiAdhF_DiscBC_Count := udiAdhF_DiscBC_Count + 1;
    END_IF;
ELSE
    IF udiAdhF_DiscBC_Count > 0 THEN
        udiAdhF_DiscBC_Count := udiAdhF_DiscBC_Count - 1;
    END_IF;
END_IF;

IF rAdhF_DiffCA > rAdhF_Tol THEN
    IF udiAdhF_DiscCA_Count < udiDiscrepancyLimit THEN
        udiAdhF_DiscCA_Count := udiAdhF_DiscCA_Count + 1;
    END_IF;
ELSE
    IF udiAdhF_DiscCA_Count > 0 THEN
        udiAdhF_DiscCA_Count := udiAdhF_DiscCA_Count - 1;
    END_IF;
END_IF;

(* Step 4.4: Cross-Channel Health Isolation *)
IF (udiAdhF_DiscAB_Count >= udiDiscrepancyLimit) AND (udiAdhF_DiscCA_Count >= udiDiscrepancyLimit) THEN
    bAdhF_A_Healthy := FALSE;
ELSE
    IF (udiAdhF_DiscAB_Count = 0) AND (udiAdhF_DiscCA_Count = 0) THEN
        bAdhF_A_Healthy := TRUE;
    END_IF;
END_IF;

IF (udiAdhF_DiscAB_Count >= udiDiscrepancyLimit) AND (udiAdhF_DiscBC_Count >= udiDiscrepancyLimit) THEN
    bAdhF_B_Healthy := FALSE;
ELSE
    IF (udiAdhF_DiscAB_Count = 0) AND (udiAdhF_DiscBC_Count = 0) THEN
        bAdhF_B_Healthy := TRUE;
    END_IF;
END_IF;

IF (udiAdhF_DiscBC_Count >= udiDiscrepancyLimit) AND (udiAdhF_DiscCA_Count >= udiDiscrepancyLimit) THEN
    bAdhF_C_Healthy := FALSE;
ELSE
    IF (udiAdhF_DiscBC_Count = 0) AND (udiAdhF_DiscCA_Count = 0) THEN
        bAdhF_C_Healthy := TRUE;
    END_IF;
END_IF;

nAdhF_HealthyTotal := BOOL_TO_INT(bAdhF_A_Healthy) + BOOL_TO_INT(bAdhF_B_Healthy) + BOOL_TO_INT(bAdhF_C_Healthy);

(* Step 4.5: Multi-Tier Voting Arbitration *)
IF nAdhF_HealthyTotal = 3 THEN
    rSortA := rAdhF_FiltA;
    rSortB := rAdhF_FiltB;
    rSortC := rAdhF_FiltC;
    IF rSortA > rSortB THEN
        rSortTemp := rSortA; rSortA := rSortB; rSortB := rSortTemp;
    END_IF;
    IF rSortB > rSortC THEN
        rSortTemp := rSortB; rSortB := rSortC; rSortC := rSortTemp;
    END_IF;
    IF rSortA > rSortB THEN
        rSortTemp := rSortA; rSortA := rSortB; rSortB := rSortTemp;
    END_IF;
    rAdhF_VotedVal := rSortB;
    bAdhF_ChannelDegraded := FALSE;
    bAdhF_AllFaultTrip := FALSE;
ELSIF nAdhF_HealthyTotal = 2 THEN
    IF NOT bAdhF_A_Healthy THEN
        rAdhF_VotedVal := (rAdhF_FiltB + rAdhF_FiltC) * 0.50;
    ELSIF NOT bAdhF_B_Healthy THEN
        rAdhF_VotedVal := (rAdhF_FiltA + rAdhF_FiltC) * 0.50;
    ELSE
        rAdhF_VotedVal := (rAdhF_FiltA + rAdhF_FiltB) * 0.50;
    END_IF;
    bAdhF_ChannelDegraded := TRUE;
    bAdhF_AllFaultTrip := FALSE;
ELSIF nAdhF_HealthyTotal = 1 THEN
    IF bAdhF_A_Healthy THEN
        rAdhF_VotedVal := rAdhF_FiltA;
    ELSIF bAdhF_B_Healthy THEN
        rAdhF_VotedVal := rAdhF_FiltB;
    ELSE
        rAdhF_VotedVal := rAdhF_FiltC;
    END_IF;
    bAdhF_ChannelDegraded := TRUE;
    bAdhF_AllFaultTrip := FALSE;
ELSE
    bAdhF_ChannelDegraded := TRUE;
    bAdhF_AllFaultTrip := TRUE;
END_IF;


(* ---------------------------------------------------------------------------------------------- *)
(* CHANNEL 5: FRAMING GEO-CLAMP PNEUMATIC LOAD CELLS (WT_CLAMP_501A/B/C) [N]                      *)
(* ---------------------------------------------------------------------------------------------- *)
(* Step 5.1: First-Order Low-Pass Filtering *)
rClampW_FiltA := rClampW_FiltA + rFilterAlpha * (rWT_Clamp_501A - rClampW_FiltA);
rClampW_FiltB := rClampW_FiltB + rFilterAlpha * (rWT_Clamp_501B - rClampW_FiltB);
rClampW_FiltC := rClampW_FiltC + rFilterAlpha * (rWT_Clamp_501C - rClampW_FiltC);

(* Step 5.2: Pairwise Differences *)
rClampW_DiffAB := ABS(rClampW_FiltA - rClampW_FiltB);
rClampW_DiffBC := ABS(rClampW_FiltB - rClampW_FiltC);
rClampW_DiffCA := ABS(rClampW_FiltC - rClampW_FiltA);

(* Step 5.3: Discrepancy Debounce Timers *)
IF rClampW_DiffAB > rClampW_Tol THEN
    IF udiClampW_DiscAB_Count < udiDiscrepancyLimit THEN
        udiClampW_DiscAB_Count := udiClampW_DiscAB_Count + 1;
    END_IF;
ELSE
    IF udiClampW_DiscAB_Count > 0 THEN
        udiClampW_DiscAB_Count := udiClampW_DiscAB_Count - 1;
    END_IF;
END_IF;

IF rClampW_DiffBC > rClampW_Tol THEN
    IF udiClampW_DiscBC_Count < udiDiscrepancyLimit THEN
        udiClampW_DiscBC_Count := udiClampW_DiscBC_Count + 1;
    END_IF;
ELSE
    IF udiClampW_DiscBC_Count > 0 THEN
        udiClampW_DiscBC_Count := udiClampW_DiscBC_Count - 1;
    END_IF;
END_IF;

IF rClampW_DiffCA > rClampW_Tol THEN
    IF udiClampW_DiscCA_Count < udiDiscrepancyLimit THEN
        udiClampW_DiscCA_Count := udiClampW_DiscCA_Count + 1;
    END_IF;
ELSE
    IF udiClampW_DiscCA_Count > 0 THEN
        udiClampW_DiscCA_Count := udiClampW_DiscCA_Count - 1;
    END_IF;
END_IF;

(* Step 5.4: Cross-Channel Health Isolation *)
IF (udiClampW_DiscAB_Count >= udiDiscrepancyLimit) AND (udiClampW_DiscCA_Count >= udiDiscrepancyLimit) THEN
    bClampW_A_Healthy := FALSE;
ELSE
    IF (udiClampW_DiscAB_Count = 0) AND (udiClampW_DiscCA_Count = 0) THEN
        bClampW_A_Healthy := TRUE;
    END_IF;
END_IF;

IF (udiClampW_DiscAB_Count >= udiDiscrepancyLimit) AND (udiClampW_DiscBC_Count >= udiDiscrepancyLimit) THEN
    bClampW_B_Healthy := FALSE;
ELSE
    IF (udiClampW_DiscAB_Count = 0) AND (udiClampW_DiscBC_Count = 0) THEN
        bClampW_B_Healthy := TRUE;
    END_IF;
END_IF;

IF (udiClampW_DiscBC_Count >= udiDiscrepancyLimit) AND (udiClampW_DiscCA_Count >= udiDiscrepancyLimit) THEN
    bClampW_C_Healthy := FALSE;
ELSE
    IF (udiClampW_DiscBC_Count = 0) AND (udiClampW_DiscCA_Count = 0) THEN
        bClampW_C_Healthy := TRUE;
    END_IF;
END_IF;

nClampW_HealthyTotal := BOOL_TO_INT(bClampW_A_Healthy) + BOOL_TO_INT(bClampW_B_Healthy) + BOOL_TO_INT(bClampW_C_Healthy);

(* Step 5.5: Multi-Tier Voting Arbitration *)
IF nClampW_HealthyTotal = 3 THEN
    rSortA := rClampW_FiltA;
    rSortB := rClampW_FiltB;
    rSortC := rClampW_FiltC;
    IF rSortA > rSortB THEN
        rSortTemp := rSortA; rSortA := rSortB; rSortB := rSortTemp;
    END_IF;
    IF rSortB > rSortC THEN
        rSortTemp := rSortB; rSortB := rSortC; rSortC := rSortTemp;
    END_IF;
    IF rSortA > rSortB THEN
        rSortTemp := rSortA; rSortA := rSortB; rSortB := rSortTemp;
    END_IF;
    rClampW_VotedVal := rSortB;
    bClampW_ChannelDegraded := FALSE;
    bClampW_AllFaultTrip := FALSE;
ELSIF nClampW_HealthyTotal = 2 THEN
    IF NOT bClampW_A_Healthy THEN
        rClampW_VotedVal := (rClampW_FiltB + rClampW_FiltC) * 0.50;
    ELSIF NOT bClampW_B_Healthy THEN
        rClampW_VotedVal := (rClampW_FiltA + rClampW_FiltC) * 0.50;
    ELSE
        rClampW_VotedVal := (rClampW_FiltA + rClampW_FiltB) * 0.50;
    END_IF;
    bClampW_ChannelDegraded := TRUE;
    bClampW_AllFaultTrip := FALSE;
ELSIF nClampW_HealthyTotal = 1 THEN
    IF bClampW_A_Healthy THEN
        rClampW_VotedVal := rClampW_FiltA;
    ELSIF bClampW_B_Healthy THEN
        rClampW_VotedVal := rClampW_FiltB;
    ELSE
        rClampW_VotedVal := rClampW_FiltC;
    END_IF;
    bClampW_ChannelDegraded := TRUE;
    bClampW_AllFaultTrip := FALSE;
ELSE
    bClampW_ChannelDegraded := TRUE;
    bClampW_AllFaultTrip := TRUE;
END_IF;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 1.6: ASSEMBLE 6-DIMENSIONAL VOTED MEASUREMENT VECTOR a_y_meas [1..6]                      *)
(* ---------------------------------------------------------------------------------------------- *)
a_y_meas[1] := rPyro_VotedVal;                  (* Voted Melt Pool Temperature [deg C] *)
a_y_meas[2] := rWireFeedActualSpeed;            (* Measured Wire Feed Velocity [mm/s] *)
a_y_meas[3] := rSeam_VotedVal;                  (* Voted Lateral Seam Deviation [um] *)
a_y_meas[4] := rAdhP_VotedVal;                  (* Voted Adhesive Line Pressure [bar] *)
a_y_meas[5] := rAdhF_VotedVal * 0.78125;        (* Voted Adhesive Flux [mL/s] (from g/s / 1.28) *)
a_y_meas[6] := rClampW_VotedVal;                (* Voted Framing Clamp Reaction Force [N] *)
"""
