# mega_casting_builder/build_phase2_tmr_voting.py

def get_phase2_tmr_voting():
    return """(* =====================================================================================================================
 * PHASE 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING WITH DISCREPANCY TIMERS & BUMPLESS DEGRADATION
 * Covers 4 mission-critical sensor trios + 4-column tie-bar extensometers and platen tilt parallelism
 * ===================================================================================================================== *)

(* Safe local copy of scan cycle time *)
IF rCycleTime_DeltaT > 0.00001 AND rCycleTime_DeltaT < 0.100 THEN
    rScanDeltaT := rCycleTime_DeltaT;
ELSE
    rScanDeltaT := 0.001; (* Default 1.0 ms fallback *)
END_IF;

rTotalRunTime_Sec := rTotalRunTime_Sec + rScanDeltaT;

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. PLUNGER MAGNETOSTRICTIVE LINEAR POSITION TRANSDUCERS (rPlungerPos_Sensor 1, 2, 3) [mm]
 * --------------------------------------------------------------------------------------------------------------------- *)
rPlunger_Diff_12 := ABS(rPlungerPos_Sensor1 - rPlungerPos_Sensor2);
rPlunger_Diff_23 := ABS(rPlungerPos_Sensor2 - rPlungerPos_Sensor3);
rPlunger_Diff_31 := ABS(rPlungerPos_Sensor3 - rPlungerPos_Sensor1);

(* Channel 1 Discrepancy Accumulation Timer *)
IF (rPlunger_Diff_12 > rTMR_Tol_Pos_mm) AND (rPlunger_Diff_31 > rTMR_Tol_Pos_mm) THEN
    rPlunger_Discrepancy_Timer1 := rPlunger_Discrepancy_Timer1 + rScanDeltaT;
    IF rPlunger_Discrepancy_Timer1 >= rTMR_Discrepancy_TripTime_Sec THEN
        bPlunger_Sensor1_Healthy := FALSE;
    END_IF;
ELSE
    IF rPlunger_Discrepancy_Timer1 > 0.0 THEN
        rPlunger_Discrepancy_Timer1 := rPlunger_Discrepancy_Timer1 - (rScanDeltaT * 2.0);
        IF rPlunger_Discrepancy_Timer1 < 0.0 THEN
            rPlunger_Discrepancy_Timer1 := 0.0;
        END_IF;
    END_IF;
    IF (rPlunger_Diff_12 < (rTMR_Tol_Pos_mm * 0.5)) AND (rPlunger_Diff_31 < (rTMR_Tol_Pos_mm * 0.5)) THEN
        bPlunger_Sensor1_Healthy := TRUE;
    END_IF;
END_IF;

(* Channel 2 Discrepancy Accumulation Timer *)
IF (rPlunger_Diff_12 > rTMR_Tol_Pos_mm) AND (rPlunger_Diff_23 > rTMR_Tol_Pos_mm) THEN
    rPlunger_Discrepancy_Timer2 := rPlunger_Discrepancy_Timer2 + rScanDeltaT;
    IF rPlunger_Discrepancy_Timer2 >= rTMR_Discrepancy_TripTime_Sec THEN
        bPlunger_Sensor2_Healthy := FALSE;
    END_IF;
ELSE
    IF rPlunger_Discrepancy_Timer2 > 0.0 THEN
        rPlunger_Discrepancy_Timer2 := rPlunger_Discrepancy_Timer2 - (rScanDeltaT * 2.0);
        IF rPlunger_Discrepancy_Timer2 < 0.0 THEN
            rPlunger_Discrepancy_Timer2 := 0.0;
        END_IF;
    END_IF;
    IF (rPlunger_Diff_12 < (rTMR_Tol_Pos_mm * 0.5)) AND (rPlunger_Diff_23 < (rTMR_Tol_Pos_mm * 0.5)) THEN
        bPlunger_Sensor2_Healthy := TRUE;
    END_IF;
END_IF;

(* Channel 3 Discrepancy Accumulation Timer *)
IF (rPlunger_Diff_31 > rTMR_Tol_Pos_mm) AND (rPlunger_Diff_23 > rTMR_Tol_Pos_mm) THEN
    rPlunger_Discrepancy_Timer3 := rPlunger_Discrepancy_Timer3 + rScanDeltaT;
    IF rPlunger_Discrepancy_Timer3 >= rTMR_Discrepancy_TripTime_Sec THEN
        bPlunger_Sensor3_Healthy := FALSE;
    END_IF;
ELSE
    IF rPlunger_Discrepancy_Timer3 > 0.0 THEN
        rPlunger_Discrepancy_Timer3 := rPlunger_Discrepancy_Timer3 - (rScanDeltaT * 2.0);
        IF rPlunger_Discrepancy_Timer3 < 0.0 THEN
            rPlunger_Discrepancy_Timer3 := 0.0;
        END_IF;
    END_IF;
    IF (rPlunger_Diff_31 < (rTMR_Tol_Pos_mm * 0.5)) AND (rPlunger_Diff_23 < (rTMR_Tol_Pos_mm * 0.5)) THEN
        bPlunger_Sensor3_Healthy := TRUE;
    END_IF;
END_IF;

(* Determine Plunger TMR Health Mode *)
IF bPlunger_Sensor1_Healthy AND bPlunger_Sensor2_Healthy AND bPlunger_Sensor3_Healthy THEN
    iPlunger_TMR_HealthMode := 3; (* Full 2oo3 Mode *)
    (* Median Selection Logic *)
    IF ((rPlungerPos_Sensor1 >= rPlungerPos_Sensor2) AND (rPlungerPos_Sensor1 <= rPlungerPos_Sensor3)) OR
       ((rPlungerPos_Sensor1 <= rPlungerPos_Sensor2) AND (rPlungerPos_Sensor1 >= rPlungerPos_Sensor3)) THEN
        rPlungerPos_Raw_Voted := rPlungerPos_Sensor1;
    ELSIF ((rPlungerPos_Sensor2 >= rPlungerPos_Sensor1) AND (rPlungerPos_Sensor2 <= rPlungerPos_Sensor3)) OR
          ((rPlungerPos_Sensor2 <= rPlungerPos_Sensor1) AND (rPlungerPos_Sensor2 >= rPlungerPos_Sensor3)) THEN
        rPlungerPos_Raw_Voted := rPlungerPos_Sensor2;
    ELSE
        rPlungerPos_Raw_Voted := rPlungerPos_Sensor3;
    END_IF;
ELSIF bPlunger_Sensor1_Healthy AND bPlunger_Sensor2_Healthy THEN
    iPlunger_TMR_HealthMode := 2; (* 2oo2 Dual Mode Ch1 & Ch2 *)
    rPlungerPos_Raw_Voted := (rPlungerPos_Sensor1 + rPlungerPos_Sensor2) * 0.5;
ELSIF bPlunger_Sensor2_Healthy AND bPlunger_Sensor3_Healthy THEN
    iPlunger_TMR_HealthMode := 2; (* 2oo2 Dual Mode Ch2 & Ch3 *)
    rPlungerPos_Raw_Voted := (rPlungerPos_Sensor2 + rPlungerPos_Sensor3) * 0.5;
ELSIF bPlunger_Sensor1_Healthy AND bPlunger_Sensor3_Healthy THEN
    iPlunger_TMR_HealthMode := 2; (* 2oo2 Dual Mode Ch1 & Ch3 *)
    rPlungerPos_Raw_Voted := (rPlungerPos_Sensor1 + rPlungerPos_Sensor3) * 0.5;
ELSIF bPlunger_Sensor1_Healthy THEN
    iPlunger_TMR_HealthMode := 1; (* 1oo1 Single Channel Degraded Ch1 *)
    rPlungerPos_Raw_Voted := rPlungerPos_Sensor1;
ELSIF bPlunger_Sensor2_Healthy THEN
    iPlunger_TMR_HealthMode := 1; (* 1oo1 Single Channel Degraded Ch2 *)
    rPlungerPos_Raw_Voted := rPlungerPos_Sensor2;
ELSIF bPlunger_Sensor3_Healthy THEN
    iPlunger_TMR_HealthMode := 1; (* 1oo1 Single Channel Degraded Ch3 *)
    rPlungerPos_Raw_Voted := rPlungerPos_Sensor3;
ELSE
    iPlunger_TMR_HealthMode := 0; (* Complete Sensor Failure *)
    bAlarm_Plunger_TMR_Fault := TRUE;
END_IF;

(* Bumpless Transfer Filter for Plunger Position *)
rPlungerPos_Voted := (rBumpless_Alpha_Pos * rPlungerPos_Voted) + ((1.0 - rBumpless_Alpha_Pos) * rPlungerPos_Raw_Voted);

(* High-Fidelity Differentiated Axial Velocity Calculation [m/s] *)
IF rScanDeltaT > 0.00001 THEN
    rPlungerVel_Filtered := (0.75 * rPlungerVel_Filtered) + (0.25 * (((rPlungerPos_Voted - rPlungerPos_Prev) / rScanDeltaT) / 1000.0));
END_IF;
rPlungerPos_Prev := rPlungerPos_Voted;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. HYDRAULIC INJECTION CYLINDER HEAD PRESSURE TRANSDUCERS (rHeadPress_Sensor 1, 2, 3) [bar]
 * --------------------------------------------------------------------------------------------------------------------- *)
rHeadPress_Diff_12 := ABS(rHeadPress_Sensor1 - rHeadPress_Sensor2);
rHeadPress_Diff_23 := ABS(rHeadPress_Sensor2 - rHeadPress_Sensor3);
rHeadPress_Diff_31 := ABS(rHeadPress_Sensor3 - rHeadPress_Sensor1);

(* Head Pressure Channel 1 Discrepancy Timer *)
IF (rHeadPress_Diff_12 > rTMR_Tol_HeadPress_bar) AND (rHeadPress_Diff_31 > rTMR_Tol_HeadPress_bar) THEN
    rHeadPress_Discrepancy_Timer1 := rHeadPress_Discrepancy_Timer1 + rScanDeltaT;
    IF rHeadPress_Discrepancy_Timer1 >= rTMR_Discrepancy_TripTime_Sec THEN
        bHeadPress_Sensor1_Healthy := FALSE;
    END_IF;
ELSE
    IF rHeadPress_Discrepancy_Timer1 > 0.0 THEN
        rHeadPress_Discrepancy_Timer1 := rHeadPress_Discrepancy_Timer1 - (rScanDeltaT * 2.0);
        IF rHeadPress_Discrepancy_Timer1 < 0.0 THEN
            rHeadPress_Discrepancy_Timer1 := 0.0;
        END_IF;
    END_IF;
    IF (rHeadPress_Diff_12 < (rTMR_Tol_HeadPress_bar * 0.5)) AND (rHeadPress_Diff_31 < (rTMR_Tol_HeadPress_bar * 0.5)) THEN
        bHeadPress_Sensor1_Healthy := TRUE;
    END_IF;
END_IF;

(* Head Pressure Channel 2 Discrepancy Timer *)
IF (rHeadPress_Diff_12 > rTMR_Tol_HeadPress_bar) AND (rHeadPress_Diff_23 > rTMR_Tol_HeadPress_bar) THEN
    rHeadPress_Discrepancy_Timer2 := rHeadPress_Discrepancy_Timer2 + rScanDeltaT;
    IF rHeadPress_Discrepancy_Timer2 >= rTMR_Discrepancy_TripTime_Sec THEN
        bHeadPress_Sensor2_Healthy := FALSE;
    END_IF;
ELSE
    IF rHeadPress_Discrepancy_Timer2 > 0.0 THEN
        rHeadPress_Discrepancy_Timer2 := rHeadPress_Discrepancy_Timer2 - (rScanDeltaT * 2.0);
        IF rHeadPress_Discrepancy_Timer2 < 0.0 THEN
            rHeadPress_Discrepancy_Timer2 := 0.0;
        END_IF;
    END_IF;
    IF (rHeadPress_Diff_12 < (rTMR_Tol_HeadPress_bar * 0.5)) AND (rHeadPress_Diff_23 < (rTMR_Tol_HeadPress_bar * 0.5)) THEN
        bHeadPress_Sensor2_Healthy := TRUE;
    END_IF;
END_IF;

(* Head Pressure Channel 3 Discrepancy Timer *)
IF (rHeadPress_Diff_31 > rTMR_Tol_HeadPress_bar) AND (rHeadPress_Diff_23 > rTMR_Tol_HeadPress_bar) THEN
    rHeadPress_Discrepancy_Timer3 := rHeadPress_Discrepancy_Timer3 + rScanDeltaT;
    IF rHeadPress_Discrepancy_Timer3 >= rTMR_Discrepancy_TripTime_Sec THEN
        bHeadPress_Sensor3_Healthy := FALSE;
    END_IF;
ELSE
    IF rHeadPress_Discrepancy_Timer3 > 0.0 THEN
        rHeadPress_Discrepancy_Timer3 := rHeadPress_Discrepancy_Timer3 - (rScanDeltaT * 2.0);
        IF rHeadPress_Discrepancy_Timer3 < 0.0 THEN
            rHeadPress_Discrepancy_Timer3 := 0.0;
        END_IF;
    END_IF;
    IF (rHeadPress_Diff_31 < (rTMR_Tol_HeadPress_bar * 0.5)) AND (rHeadPress_Diff_23 < (rTMR_Tol_HeadPress_bar * 0.5)) THEN
        bHeadPress_Sensor3_Healthy := TRUE;
    END_IF;
END_IF;

(* Head Pressure Voting Logic *)
IF bHeadPress_Sensor1_Healthy AND bHeadPress_Sensor2_Healthy AND bHeadPress_Sensor3_Healthy THEN
    iHeadPress_TMR_HealthMode := 3;
    IF ((rHeadPress_Sensor1 >= rHeadPress_Sensor2) AND (rHeadPress_Sensor1 <= rHeadPress_Sensor3)) OR
       ((rHeadPress_Sensor1 <= rHeadPress_Sensor2) AND (rHeadPress_Sensor1 >= rHeadPress_Sensor3)) THEN
        rHeadPress_Raw_Voted := rHeadPress_Sensor1;
    ELSIF ((rHeadPress_Sensor2 >= rHeadPress_Sensor1) AND (rHeadPress_Sensor2 <= rHeadPress_Sensor3)) OR
          ((rHeadPress_Sensor2 <= rHeadPress_Sensor1) AND (rHeadPress_Sensor2 >= rHeadPress_Sensor3)) THEN
        rHeadPress_Raw_Voted := rHeadPress_Sensor2;
    ELSE
        rHeadPress_Raw_Voted := rHeadPress_Sensor3;
    END_IF;
ELSIF bHeadPress_Sensor1_Healthy AND bHeadPress_Sensor2_Healthy THEN
    iHeadPress_TMR_HealthMode := 2;
    rHeadPress_Raw_Voted := (rHeadPress_Sensor1 + rHeadPress_Sensor2) * 0.5;
ELSIF bHeadPress_Sensor2_Healthy AND bHeadPress_Sensor3_Healthy THEN
    iHeadPress_TMR_HealthMode := 2;
    rHeadPress_Raw_Voted := (rHeadPress_Sensor2 + rHeadPress_Sensor3) * 0.5;
ELSIF bHeadPress_Sensor1_Healthy AND bHeadPress_Sensor3_Healthy THEN
    iHeadPress_TMR_HealthMode := 2;
    rHeadPress_Raw_Voted := (rHeadPress_Sensor1 + rHeadPress_Sensor3) * 0.5;
ELSIF bHeadPress_Sensor1_Healthy THEN
    iHeadPress_TMR_HealthMode := 1;
    rHeadPress_Raw_Voted := rHeadPress_Sensor1;
ELSIF bHeadPress_Sensor2_Healthy THEN
    iHeadPress_TMR_HealthMode := 1;
    rHeadPress_Raw_Voted := rHeadPress_Sensor2;
ELSIF bHeadPress_Sensor3_Healthy THEN
    iHeadPress_TMR_HealthMode := 1;
    rHeadPress_Raw_Voted := rHeadPress_Sensor3;
ELSE
    iHeadPress_TMR_HealthMode := 0;
    bAlarm_HeadPress_TMR_Fault := TRUE;
END_IF;

rHeadPress_Voted := (rBumpless_Alpha_Head * rHeadPress_Voted) + ((1.0 - rBumpless_Alpha_Head) * rHeadPress_Raw_Voted);

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. IN-CAVITY PIEZOELECTRIC QUARTZ PRESSURE TRANSDUCERS (rCavityPress_Sensor 1, 2, 3) [bar]
 * --------------------------------------------------------------------------------------------------------------------- *)
rCavityPress_Diff_12 := ABS(rCavityPress_Sensor1 - rCavityPress_Sensor2);
rCavityPress_Diff_23 := ABS(rCavityPress_Sensor2 - rCavityPress_Sensor3);
rCavityPress_Diff_31 := ABS(rCavityPress_Sensor3 - rCavityPress_Sensor1);

(* Cavity Piezo Channel 1 Discrepancy Timer *)
IF (rCavityPress_Diff_12 > rTMR_Tol_CavityPress_bar) AND (rCavityPress_Diff_31 > rTMR_Tol_CavityPress_bar) THEN
    rCavityPress_Discrepancy_Timer1 := rCavityPress_Discrepancy_Timer1 + rScanDeltaT;
    IF rCavityPress_Discrepancy_Timer1 >= rTMR_Discrepancy_TripTime_Sec THEN
        bCavityPress_Sensor1_Healthy := FALSE;
    END_IF;
ELSE
    IF rCavityPress_Discrepancy_Timer1 > 0.0 THEN
        rCavityPress_Discrepancy_Timer1 := rCavityPress_Discrepancy_Timer1 - (rScanDeltaT * 2.0);
        IF rCavityPress_Discrepancy_Timer1 < 0.0 THEN
            rCavityPress_Discrepancy_Timer1 := 0.0;
        END_IF;
    END_IF;
    IF (rCavityPress_Diff_12 < (rTMR_Tol_CavityPress_bar * 0.5)) AND (rCavityPress_Diff_31 < (rTMR_Tol_CavityPress_bar * 0.5)) THEN
        bCavityPress_Sensor1_Healthy := TRUE;
    END_IF;
END_IF;

(* Cavity Piezo Channel 2 Discrepancy Timer *)
IF (rCavityPress_Diff_12 > rTMR_Tol_CavityPress_bar) AND (rCavityPress_Diff_23 > rTMR_Tol_CavityPress_bar) THEN
    rCavityPress_Discrepancy_Timer2 := rCavityPress_Discrepancy_Timer2 + rScanDeltaT;
    IF rCavityPress_Discrepancy_Timer2 >= rTMR_Discrepancy_TripTime_Sec THEN
        bCavityPress_Sensor2_Healthy := FALSE;
    END_IF;
ELSE
    IF rCavityPress_Discrepancy_Timer2 > 0.0 THEN
        rCavityPress_Discrepancy_Timer2 := rCavityPress_Discrepancy_Timer2 - (rScanDeltaT * 2.0);
        IF rCavityPress_Discrepancy_Timer2 < 0.0 THEN
            rCavityPress_Discrepancy_Timer2 := 0.0;
        END_IF;
    END_IF;
    IF (rCavityPress_Diff_12 < (rTMR_Tol_CavityPress_bar * 0.5)) AND (rCavityPress_Diff_23 < (rTMR_Tol_CavityPress_bar * 0.5)) THEN
        bCavityPress_Sensor2_Healthy := TRUE;
    END_IF;
END_IF;

(* Cavity Piezo Channel 3 Discrepancy Timer *)
IF (rCavityPress_Diff_31 > rTMR_Tol_CavityPress_bar) AND (rCavityPress_Diff_23 > rTMR_Tol_CavityPress_bar) THEN
    rCavityPress_Discrepancy_Timer3 := rCavityPress_Discrepancy_Timer3 + rScanDeltaT;
    IF rCavityPress_Discrepancy_Timer3 >= rTMR_Discrepancy_TripTime_Sec THEN
        bCavityPress_Sensor3_Healthy := FALSE;
    END_IF;
ELSE
    IF rCavityPress_Discrepancy_Timer3 > 0.0 THEN
        rCavityPress_Discrepancy_Timer3 := rCavityPress_Discrepancy_Timer3 - (rScanDeltaT * 2.0);
        IF rCavityPress_Discrepancy_Timer3 < 0.0 THEN
            rCavityPress_Discrepancy_Timer3 := 0.0;
        END_IF;
    END_IF;
    IF (rCavityPress_Diff_31 < (rTMR_Tol_CavityPress_bar * 0.5)) AND (rCavityPress_Diff_23 < (rTMR_Tol_CavityPress_bar * 0.5)) THEN
        bCavityPress_Sensor3_Healthy := TRUE;
    END_IF;
END_IF;

(* Cavity Pressure Voting Logic *)
IF bCavityPress_Sensor1_Healthy AND bCavityPress_Sensor2_Healthy AND bCavityPress_Sensor3_Healthy THEN
    iCavityPress_TMR_HealthMode := 3;
    IF ((rCavityPress_Sensor1 >= rCavityPress_Sensor2) AND (rCavityPress_Sensor1 <= rCavityPress_Sensor3)) OR
       ((rCavityPress_Sensor1 <= rCavityPress_Sensor2) AND (rCavityPress_Sensor1 >= rCavityPress_Sensor3)) THEN
        rCavityPress_Raw_Voted := rCavityPress_Sensor1;
    ELSIF ((rCavityPress_Sensor2 >= rCavityPress_Sensor1) AND (rCavityPress_Sensor2 <= rCavityPress_Sensor3)) OR
          ((rCavityPress_Sensor2 <= rCavityPress_Sensor1) AND (rCavityPress_Sensor2 >= rCavityPress_Sensor3)) THEN
        rCavityPress_Raw_Voted := rCavityPress_Sensor2;
    ELSE
        rCavityPress_Raw_Voted := rCavityPress_Sensor3;
    END_IF;
ELSIF bCavityPress_Sensor1_Healthy AND bCavityPress_Sensor2_Healthy THEN
    iCavityPress_TMR_HealthMode := 2;
    rCavityPress_Raw_Voted := (rCavityPress_Sensor1 + rCavityPress_Sensor2) * 0.5;
ELSIF bCavityPress_Sensor2_Healthy AND bCavityPress_Sensor3_Healthy THEN
    iCavityPress_TMR_HealthMode := 2;
    rCavityPress_Raw_Voted := (rCavityPress_Sensor2 + rCavityPress_Sensor3) * 0.5;
ELSIF bCavityPress_Sensor1_Healthy AND bCavityPress_Sensor3_Healthy THEN
    iCavityPress_TMR_HealthMode := 2;
    rCavityPress_Raw_Voted := (rCavityPress_Sensor1 + rCavityPress_Sensor3) * 0.5;
ELSIF bCavityPress_Sensor1_Healthy THEN
    iCavityPress_TMR_HealthMode := 1;
    rCavityPress_Raw_Voted := rCavityPress_Sensor1;
ELSIF bCavityPress_Sensor2_Healthy THEN
    iCavityPress_TMR_HealthMode := 1;
    rCavityPress_Raw_Voted := rCavityPress_Sensor2;
ELSIF bCavityPress_Sensor3_Healthy THEN
    iCavityPress_TMR_HealthMode := 1;
    rCavityPress_Raw_Voted := rCavityPress_Sensor3;
ELSE
    iCavityPress_TMR_HealthMode := 0;
    bAlarm_CavityPress_TMR_Fault := TRUE;
END_IF;

rCavityPress_Voted := (rBumpless_Alpha_Cavity * rCavityPress_Voted) + ((1.0 - rBumpless_Alpha_Cavity) * rCavityPress_Raw_Voted);

(* Acoustic Fill Front Shockwave Derivation [bar/ms] *)
IF rScanDeltaT > 0.00001 THEN
    rAcousticFillShock_bar_ms := ((rCavityPress_Voted - rCavityPress_Prev) / (rScanDeltaT * 1000.0));
END_IF;
rCavityPress_Prev := rCavityPress_Voted;

(* ---------------------------------------------------------------------------------------------------------------------
 * 4. PARTING PLANE VACUUM EVACUATION CAPACITIVE TRANSDUCERS (rVacPressure_Sensor 1, 2, 3) [mbar]
 * --------------------------------------------------------------------------------------------------------------------- *)
rVac_Diff_12 := ABS(rVacPressure_Sensor1 - rVacPressure_Sensor2);
rVac_Diff_23 := ABS(rVacPressure_Sensor2 - rVacPressure_Sensor3);
rVac_Diff_31 := ABS(rVacPressure_Sensor3 - rVacPressure_Sensor1);

(* Vacuum Channel 1 Discrepancy Timer *)
IF (rVac_Diff_12 > rTMR_Tol_Vac_mbar) AND (rVac_Diff_31 > rTMR_Tol_Vac_mbar) THEN
    rVac_Discrepancy_Timer1 := rVac_Discrepancy_Timer1 + rScanDeltaT;
    IF rVac_Discrepancy_Timer1 >= rTMR_Discrepancy_TripTime_Sec THEN
        bVac_Sensor1_Healthy := FALSE;
    END_IF;
ELSE
    IF rVac_Discrepancy_Timer1 > 0.0 THEN
        rVac_Discrepancy_Timer1 := rVac_Discrepancy_Timer1 - (rScanDeltaT * 2.0);
        IF rVac_Discrepancy_Timer1 < 0.0 THEN
            rVac_Discrepancy_Timer1 := 0.0;
        END_IF;
    END_IF;
    IF (rVac_Diff_12 < (rTMR_Tol_Vac_mbar * 0.5)) AND (rVac_Diff_31 < (rTMR_Tol_Vac_mbar * 0.5)) THEN
        bVac_Sensor1_Healthy := TRUE;
    END_IF;
END_IF;

(* Vacuum Channel 2 Discrepancy Timer *)
IF (rVac_Diff_12 > rTMR_Tol_Vac_mbar) AND (rVac_Diff_23 > rTMR_Tol_Vac_mbar) THEN
    rVac_Discrepancy_Timer2 := rVac_Discrepancy_Timer2 + rScanDeltaT;
    IF rVac_Discrepancy_Timer2 >= rTMR_Discrepancy_TripTime_Sec THEN
        bVac_Sensor2_Healthy := FALSE;
    END_IF;
ELSE
    IF rVac_Discrepancy_Timer2 > 0.0 THEN
        rVac_Discrepancy_Timer2 := rVac_Discrepancy_Timer2 - (rScanDeltaT * 2.0);
        IF rVac_Discrepancy_Timer2 < 0.0 THEN
            rVac_Discrepancy_Timer2 := 0.0;
        END_IF;
    END_IF;
    IF (rVac_Diff_12 < (rTMR_Tol_Vac_mbar * 0.5)) AND (rVac_Diff_23 < (rTMR_Tol_Vac_mbar * 0.5)) THEN
        bVac_Sensor2_Healthy := TRUE;
    END_IF;
END_IF;

(* Vacuum Channel 3 Discrepancy Timer *)
IF (rVac_Diff_31 > rTMR_Tol_Vac_mbar) AND (rVac_Diff_23 > rTMR_Tol_Vac_mbar) THEN
    rVac_Discrepancy_Timer3 := rVac_Discrepancy_Timer3 + rScanDeltaT;
    IF rVac_Discrepancy_Timer3 >= rTMR_Discrepancy_TripTime_Sec THEN
        bVac_Sensor3_Healthy := FALSE;
    END_IF;
ELSE
    IF rVac_Discrepancy_Timer3 > 0.0 THEN
        rVac_Discrepancy_Timer3 := rVac_Discrepancy_Timer3 - (rScanDeltaT * 2.0);
        IF rVac_Discrepancy_Timer3 < 0.0 THEN
            rVac_Discrepancy_Timer3 := 0.0;
        END_IF;
    END_IF;
    IF (rVac_Diff_31 < (rTMR_Tol_Vac_mbar * 0.5)) AND (rVac_Diff_23 < (rTMR_Tol_Vac_mbar * 0.5)) THEN
        bVac_Sensor3_Healthy := TRUE;
    END_IF;
END_IF;

(* Vacuum Voting Logic *)
IF bVac_Sensor1_Healthy AND bVac_Sensor2_Healthy AND bVac_Sensor3_Healthy THEN
    iVac_TMR_HealthMode := 3;
    IF ((rVacPressure_Sensor1 >= rVacPressure_Sensor2) AND (rVacPressure_Sensor1 <= rVacPressure_Sensor3)) OR
       ((rVacPressure_Sensor1 <= rVacPressure_Sensor2) AND (rVacPressure_Sensor1 >= rVacPressure_Sensor3)) THEN
        rVac_Raw_Voted := rVacPressure_Sensor1;
    ELSIF ((rVacPressure_Sensor2 >= rVacPressure_Sensor1) AND (rVacPressure_Sensor2 <= rVacPressure_Sensor3)) OR
          ((rVacPressure_Sensor2 <= rVacPressure_Sensor1) AND (rVacPressure_Sensor2 >= rVacPressure_Sensor3)) THEN
        rVac_Raw_Voted := rVacPressure_Sensor2;
    ELSE
        rVac_Raw_Voted := rVacPressure_Sensor3;
    END_IF;
ELSIF bVac_Sensor1_Healthy AND bVac_Sensor2_Healthy THEN
    iVac_TMR_HealthMode := 2;
    rVac_Raw_Voted := (rVacPressure_Sensor1 + rVacPressure_Sensor2) * 0.5;
ELSIF bVac_Sensor2_Healthy AND bVac_Sensor3_Healthy THEN
    iVac_TMR_HealthMode := 2;
    rVac_Raw_Voted := (rVacPressure_Sensor2 + rVacPressure_Sensor3) * 0.5;
ELSIF bVac_Sensor1_Healthy AND bVac_Sensor3_Healthy THEN
    iVac_TMR_HealthMode := 2;
    rVac_Raw_Voted := (rVacPressure_Sensor1 + rVacPressure_Sensor3) * 0.5;
ELSIF bVac_Sensor1_Healthy THEN
    iVac_TMR_HealthMode := 1;
    rVac_Raw_Voted := rVacPressure_Sensor1;
ELSIF bVac_Sensor2_Healthy THEN
    iVac_TMR_HealthMode := 1;
    rVac_Raw_Voted := rVacPressure_Sensor2;
ELSIF bVac_Sensor3_Healthy THEN
    iVac_TMR_HealthMode := 1;
    rVac_Raw_Voted := rVacPressure_Sensor3;
ELSE
    iVac_TMR_HealthMode := 0;
    bAlarm_Vac_TMR_Fault := TRUE;
END_IF;

rVacPressure_Voted := (rBumpless_Alpha_Vac * rVacPressure_Voted) + ((1.0 - rBumpless_Alpha_Vac) * rVac_Raw_Voted);

(* Acoustic Vacuum Evacuation Rate / Parting Line Leak Rate [mbar/s] *)
IF rScanDeltaT > 0.00001 THEN
    rVac_LeakRate_Actual_mbar_s := (rVacPressure_Voted - rVac_Prev) / rScanDeltaT;
END_IF;
rVac_Prev := rVacPressure_Voted;

(* ---------------------------------------------------------------------------------------------------------------------
 * 5. 4-COLUMN TIE-BAR DYNAMIC STRAIN EXTENSOMETERS & 60,000 kN CLAMP FORCE MONITORING
 * Hooke's Law for 42CrMo4 Forged Steel: F = E * A * (Delta_L / L)
 * Extensometer strain is in micrometers [um], nominal length is 12.20 meters
 * Modulus E = 206 GPa = 206,000 N/mm2 = 206,000,000 kN/m2
 * --------------------------------------------------------------------------------------------------------------------- *)
IF rTieBar_Length_Nominal_m > 0.1 THEN
    (* Axial Force per Column in kN: F_i = (E * A * (strain_um * 1e-6) / L) * 1e3 *)
    rForce_Column1_kN := (rTieBar_Modulus_GPa * 1000000.0 * rTieBar_Area_m2 * (rTieBar_Strain_Ch1 * 0.000001)) / rTieBar_Length_Nominal_m;
    rForce_Column2_kN := (rTieBar_Modulus_GPa * 1000000.0 * rTieBar_Area_m2 * (rTieBar_Strain_Ch2 * 0.000001)) / rTieBar_Length_Nominal_m;
    rForce_Column3_kN := (rTieBar_Modulus_GPa * 1000000.0 * rTieBar_Area_m2 * (rTieBar_Strain_Ch3 * 0.000001)) / rTieBar_Length_Nominal_m;
    rForce_Column4_kN := (rTieBar_Modulus_GPa * 1000000.0 * rTieBar_Area_m2 * (rTieBar_Strain_Ch4 * 0.000001)) / rTieBar_Length_Nominal_m;
END_IF;

(* Total Hydraulic Toggle Clamping Force [kN] *)
rTotalClampingForce_kN := rForce_Column1_kN + rForce_Column2_kN + rForce_Column3_kN + rForce_Column4_kN;

(* Platen Deflection Parallelism & Angular Misalignment [um] *)
rPlaten_Delta_TopBottom_um := ABS((rTieBar_Strain_Ch1 + rTieBar_Strain_Ch2) * 0.5 - (rTieBar_Strain_Ch3 + rTieBar_Strain_Ch4) * 0.5);
rPlaten_Delta_LeftRight_um := ABS((rTieBar_Strain_Ch1 + rTieBar_Strain_Ch3) * 0.5 - (rTieBar_Strain_Ch2 + rTieBar_Strain_Ch4) * 0.5);

IF rPlaten_Delta_TopBottom_um > rPlaten_Delta_LeftRight_um THEN
    rPlatenTilt_Parallelism_um := rPlaten_Delta_TopBottom_um;
ELSE
    rPlatenTilt_Parallelism_um := rPlaten_Delta_LeftRight_um;
END_IF;

(* Maximum Eccentricity Percentage *)
IF rTotalClampingForce_kN > 1000.0 THEN
    rPlaten_MaxEccentricity_Pct := (rPlatenTilt_Parallelism_um / ((rTieBar_Strain_Ch1 + rTieBar_Strain_Ch2 + rTieBar_Strain_Ch3 + rTieBar_Strain_Ch4) * 0.25)) * 100.0;
ELSE
    rPlaten_MaxEccentricity_Pct := 0.0;
END_IF;
"""
