(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS
 * Architecture: Median-select 2oo3 with pairwise divergence timers, bumpless degradation, and failsafe latching
 * Scan Period: Ts = 1.0 ms
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 1.1: IN-MOLD CAVITY PIEZOELECTRIC PRESSURE SENSORS (TMR BANK 1)
 * Channels: rCavityPres_TransA_In, rCavityPres_TransB_In, rCavityPres_TransC_In [bar]
 * Dynamic Range: 0.0 to 1,800.0 bar, Sub-millisecond Quartz Crystal Response
 * --------------------------------------------------------------------------------------------------------------------- *)
rCavPres_SensA_Val := rCavityPres_TransA_In;
rCavPres_SensB_Val := rCavityPres_TransB_In;
rCavPres_SensC_Val := rCavityPres_TransC_In;

(* Hardware Range Validity Check *)
IF (rCavPres_SensA_Val < -10.0) OR (rCavPres_SensA_Val > 2200.0) THEN
    bCavPres_SensA_Fault := TRUE;
END_IF;

IF (rCavPres_SensB_Val < -10.0) OR (rCavPres_SensB_Val > 2200.0) THEN
    bCavPres_SensB_Fault := TRUE;
END_IF;

IF (rCavPres_SensC_Val < -10.0) OR (rCavPres_SensC_Val > 2200.0) THEN
    bCavPres_SensC_Fault := TRUE;
END_IF;

(* Pairwise Discrepancy Divergence Integration *)
IF (NOT bCavPres_SensA_Fault) AND (NOT bCavPres_SensB_Fault) THEN
    rTemp_AbsDiff := ABS(rCavPres_SensA_Val - rCavPres_SensB_Val);
    IF rTemp_AbsDiff > rCavPres_DiscThresh THEN
        rCavPres_DiscTimer_AB := rCavPres_DiscTimer_AB + rScanTime_Ts;
        IF rCavPres_DiscTimer_AB >= rCavPres_DiscMaxTime THEN
            (* Compare with Channel C to identify culprit *)
            IF NOT bCavPres_SensC_Fault THEN
                IF ABS(rCavPres_SensA_Val - rCavPres_SensC_Val) > ABS(rCavPres_SensB_Val - rCavPres_SensC_Val) THEN
                    bCavPres_SensA_Fault := TRUE;
                ELSE
                    bCavPres_SensB_Fault := TRUE;
                END_IF;
            ELSE
                bCavPres_SensA_Fault := TRUE;
            END_IF;
        END_IF;
    ELSE
        rCavPres_DiscTimer_AB := MAX(0.0, rCavPres_DiscTimer_AB - (rScanTime_Ts * 2.0));
    END_IF;
END_IF;

IF (NOT bCavPres_SensB_Fault) AND (NOT bCavPres_SensC_Fault) THEN
    rTemp_AbsDiff := ABS(rCavPres_SensB_Val - rCavPres_SensC_Val);
    IF rTemp_AbsDiff > rCavPres_DiscThresh THEN
        rCavPres_DiscTimer_BC := rCavPres_DiscTimer_BC + rScanTime_Ts;
        IF rCavPres_DiscTimer_BC >= rCavPres_DiscMaxTime THEN
            IF NOT bCavPres_SensA_Fault THEN
                IF ABS(rCavPres_SensB_Val - rCavPres_SensA_Val) > ABS(rCavPres_SensC_Val - rCavPres_SensA_Val) THEN
                    bCavPres_SensB_Fault := TRUE;
                ELSE
                    bCavPres_SensC_Fault := TRUE;
                END_IF;
            ELSE
                bCavPres_SensB_Fault := TRUE;
            END_IF;
        END_IF;
    ELSE
        rCavPres_DiscTimer_BC := MAX(0.0, rCavPres_DiscTimer_BC - (rScanTime_Ts * 2.0));
    END_IF;
END_IF;

IF (NOT bCavPres_SensC_Fault) AND (NOT bCavPres_SensA_Fault) THEN
    rTemp_AbsDiff := ABS(rCavPres_SensC_Val - rCavPres_SensA_Val);
    IF rTemp_AbsDiff > rCavPres_DiscThresh THEN
        rCavPres_DiscTimer_CA := rCavPres_DiscTimer_CA + rScanTime_Ts;
        IF rCavPres_DiscTimer_CA >= rCavPres_DiscMaxTime THEN
            IF NOT bCavPres_SensB_Fault THEN
                IF ABS(rCavPres_SensC_Val - rCavPres_SensB_Val) > ABS(rCavPres_SensA_Val - rCavPres_SensB_Val) THEN
                    bCavPres_SensC_Fault := TRUE;
                ELSE
                    bCavPres_SensA_Fault := TRUE;
                END_IF;
            ELSE
                bCavPres_SensC_Fault := TRUE;
            END_IF;
        END_IF;
    ELSE
        rCavPres_DiscTimer_CA := MAX(0.0, rCavPres_DiscTimer_CA - (rScanTime_Ts * 2.0));
    END_IF;
END_IF;

(* 2oo3 Voting & Fault-Tolerant Median Determination *)
IF (NOT bCavPres_SensA_Fault) AND (NOT bCavPres_SensB_Fault) AND (NOT bCavPres_SensC_Fault) THEN
    (* All 3 Channels Healthy: Exact Mathematical Median *)
    iCavPres_TMR_HealthState := 3;
    IF ((rCavPres_SensA_Val >= rCavPres_SensB_Val) AND (rCavPres_SensA_Val <= rCavPres_SensC_Val)) OR
       ((rCavPres_SensA_Val >= rCavPres_SensC_Val) AND (rCavPres_SensA_Val <= rCavPres_SensB_Val)) THEN
        rTemp_A := rCavPres_SensA_Val;
    ELSIF ((rCavPres_SensB_Val >= rCavPres_SensA_Val) AND (rCavPres_SensB_Val <= rCavPres_SensC_Val)) OR
          ((rCavPres_SensB_Val >= rCavPres_SensC_Val) AND (rCavPres_SensB_Val <= rCavPres_SensA_Val)) THEN
        rTemp_A := rCavPres_SensB_Val;
    ELSE
        rTemp_A := rCavPres_SensC_Val;
    END_IF;
ELSIF (NOT bCavPres_SensA_Fault) AND (NOT bCavPres_SensB_Fault) AND bCavPres_SensC_Fault THEN
    iCavPres_TMR_HealthState := 2;
    rTemp_A := (rCavPres_SensA_Val + rCavPres_SensB_Val) * 0.5;
ELSIF (NOT bCavPres_SensB_Fault) AND (NOT bCavPres_SensC_Fault) AND bCavPres_SensA_Fault THEN
    iCavPres_TMR_HealthState := 2;
    rTemp_A := (rCavPres_SensB_Val + rCavPres_SensC_Val) * 0.5;
ELSIF (NOT bCavPres_SensC_Fault) AND (NOT bCavPres_SensA_Fault) AND bCavPres_SensB_Fault THEN
    iCavPres_TMR_HealthState := 2;
    rTemp_A := (rCavPres_SensC_Val + rCavPres_SensA_Val) * 0.5;
ELSIF (NOT bCavPres_SensA_Fault) AND bCavPres_SensB_Fault AND bCavPres_SensC_Fault THEN
    iCavPres_TMR_HealthState := 1;
    rTemp_A := rCavPres_SensA_Val;
ELSIF (NOT bCavPres_SensB_Fault) AND bCavPres_SensA_Fault AND bCavPres_SensC_Fault THEN
    iCavPres_TMR_HealthState := 1;
    rTemp_A := rCavPres_SensB_Val;
ELSIF (NOT bCavPres_SensC_Fault) AND bCavPres_SensA_Fault AND bCavPres_SensB_Fault THEN
    iCavPres_TMR_HealthState := 1;
    rTemp_A := rCavPres_SensC_Val;
ELSE
    iCavPres_TMR_HealthState := 0;
    rTemp_A := rCavPres_Prev_Voted;
    bTrip_TMR_SensorCollapse := TRUE;
END_IF;

(* Bumpless Rate-Limited Filter *)
rCavPres_Prev_Voted := rCavPres_Voted_Val;
rCavPres_Voted_Val := rCavPres_Prev_Voted + (0.35 * (rTemp_A - rCavPres_Prev_Voted));

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 1.2: NOZZLE MELT INJECTION PRESSURE SENSORS (TMR BANK 2)
 * Channels: rMeltPres_NozzleA_In, rMeltPres_NozzleB_In, rMeltPres_NozzleC_In [bar]
 * Dynamic Range: 0.0 to 2,500.0 bar, High-Temperature Melt Diaphragm Transducers
 * --------------------------------------------------------------------------------------------------------------------- *)
rMeltPres_SensA_Val := rMeltPres_NozzleA_In;
rMeltPres_SensB_Val := rMeltPres_NozzleB_In;
rMeltPres_SensC_Val := rMeltPres_NozzleC_In;

IF (rMeltPres_SensA_Val < -15.0) OR (rMeltPres_SensA_Val > 2800.0) THEN
    bMeltPres_SensA_Fault := TRUE;
END_IF;

IF (rMeltPres_SensB_Val < -15.0) OR (rMeltPres_SensB_Val > 2800.0) THEN
    bMeltPres_SensB_Fault := TRUE;
END_IF;

IF (rMeltPres_SensC_Val < -15.0) OR (rMeltPres_SensC_Val > 2800.0) THEN
    bMeltPres_SensC_Fault := TRUE;
END_IF;

(* Pairwise Discrepancy Evaluation *)
IF (NOT bMeltPres_SensA_Fault) AND (NOT bMeltPres_SensB_Fault) THEN
    rTemp_AbsDiff := ABS(rMeltPres_SensA_Val - rMeltPres_SensB_Val);
    IF rTemp_AbsDiff > rMeltPres_DiscThresh THEN
        rMeltPres_DiscTimer_AB := rMeltPres_DiscTimer_AB + rScanTime_Ts;
        IF rMeltPres_DiscTimer_AB >= rMeltPres_DiscMaxTime THEN
            IF NOT bMeltPres_SensC_Fault THEN
                IF ABS(rMeltPres_SensA_Val - rMeltPres_SensC_Val) > ABS(rMeltPres_SensB_Val - rMeltPres_SensC_Val) THEN
                    bMeltPres_SensA_Fault := TRUE;
                ELSE
                    bMeltPres_SensB_Fault := TRUE;
                END_IF;
            ELSE
                bMeltPres_SensA_Fault := TRUE;
            END_IF;
        END_IF;
    ELSE
        rMeltPres_DiscTimer_AB := MAX(0.0, rMeltPres_DiscTimer_AB - (rScanTime_Ts * 2.0));
    END_IF;
END_IF;

IF (NOT bMeltPres_SensB_Fault) AND (NOT bMeltPres_SensC_Fault) THEN
    rTemp_AbsDiff := ABS(rMeltPres_SensB_Val - rMeltPres_SensC_Val);
    IF rTemp_AbsDiff > rMeltPres_DiscThresh THEN
        rMeltPres_DiscTimer_BC := rMeltPres_DiscTimer_BC + rScanTime_Ts;
        IF rMeltPres_DiscTimer_BC >= rMeltPres_DiscMaxTime THEN
            IF NOT bMeltPres_SensA_Fault THEN
                IF ABS(rMeltPres_SensB_Val - rMeltPres_SensA_Val) > ABS(rMeltPres_SensC_Val - rMeltPres_SensA_Val) THEN
                    bMeltPres_SensB_Fault := TRUE;
                ELSE
                    bMeltPres_SensC_Fault := TRUE;
                END_IF;
            ELSE
                bMeltPres_SensB_Fault := TRUE;
            END_IF;
        END_IF;
    ELSE
        rMeltPres_DiscTimer_BC := MAX(0.0, rMeltPres_DiscTimer_BC - (rScanTime_Ts * 2.0));
    END_IF;
END_IF;

IF (NOT bMeltPres_SensC_Fault) AND (NOT bMeltPres_SensA_Fault) THEN
    rTemp_AbsDiff := ABS(rMeltPres_SensC_Val - rMeltPres_SensA_Val);
    IF rTemp_AbsDiff > rMeltPres_DiscThresh THEN
        rMeltPres_DiscTimer_CA := rMeltPres_DiscTimer_CA + rScanTime_Ts;
        IF rMeltPres_DiscTimer_CA >= rMeltPres_DiscMaxTime THEN
            IF NOT bMeltPres_SensB_Fault THEN
                IF ABS(rMeltPres_SensC_Val - rMeltPres_SensB_Val) > ABS(rMeltPres_SensA_Val - rMeltPres_SensB_Val) THEN
                    bMeltPres_SensC_Fault := TRUE;
                ELSE
                    bMeltPres_SensA_Fault := TRUE;
                END_IF;
            ELSE
                bMeltPres_SensC_Fault := TRUE;
            END_IF;
        END_IF;
    ELSE
        rMeltPres_DiscTimer_CA := MAX(0.0, rMeltPres_DiscTimer_CA - (rScanTime_Ts * 2.0));
    END_IF;
END_IF;

(* 2oo3 Voting Logic for Nozzle Melt Pressure *)
IF (NOT bMeltPres_SensA_Fault) AND (NOT bMeltPres_SensB_Fault) AND (NOT bMeltPres_SensC_Fault) THEN
    iMeltPres_TMR_HealthState := 3;
    IF ((rMeltPres_SensA_Val >= rMeltPres_SensB_Val) AND (rMeltPres_SensA_Val <= rMeltPres_SensC_Val)) OR
       ((rMeltPres_SensA_Val >= rMeltPres_SensC_Val) AND (rMeltPres_SensA_Val <= rMeltPres_SensB_Val)) THEN
        rTemp_B := rMeltPres_SensA_Val;
    ELSIF ((rMeltPres_SensB_Val >= rMeltPres_SensA_Val) AND (rMeltPres_SensB_Val <= rMeltPres_SensC_Val)) OR
          ((rMeltPres_SensB_Val >= rMeltPres_SensC_Val) AND (rMeltPres_SensB_Val <= rMeltPres_SensA_Val)) THEN
        rTemp_B := rMeltPres_SensB_Val;
    ELSE
        rTemp_B := rMeltPres_SensC_Val;
    END_IF;
ELSIF (NOT bMeltPres_SensA_Fault) AND (NOT bMeltPres_SensB_Fault) AND bMeltPres_SensC_Fault THEN
    iMeltPres_TMR_HealthState := 2;
    rTemp_B := (rMeltPres_SensA_Val + rMeltPres_SensB_Val) * 0.5;
ELSIF (NOT bMeltPres_SensB_Fault) AND (NOT bMeltPres_SensC_Fault) AND bMeltPres_SensA_Fault THEN
    iMeltPres_TMR_HealthState := 2;
    rTemp_B := (rMeltPres_SensB_Val + rMeltPres_SensC_Val) * 0.5;
ELSIF (NOT bMeltPres_SensC_Fault) AND (NOT bMeltPres_SensA_Fault) AND bMeltPres_SensB_Fault THEN
    iMeltPres_TMR_HealthState := 2;
    rTemp_B := (rMeltPres_SensC_Val + rMeltPres_SensA_Val) * 0.5;
ELSIF (NOT bMeltPres_SensA_Fault) AND bMeltPres_SensB_Fault AND bMeltPres_SensC_Fault THEN
    iMeltPres_TMR_HealthState := 1;
    rTemp_B := rMeltPres_SensA_Val;
ELSIF (NOT bMeltPres_SensB_Fault) AND bMeltPres_SensA_Fault AND bMeltPres_SensC_Fault THEN
    iMeltPres_TMR_HealthState := 1;
    rTemp_B := rMeltPres_SensB_Val;
ELSIF (NOT bMeltPres_SensC_Fault) AND bMeltPres_SensA_Fault AND bMeltPres_SensB_Fault THEN
    iMeltPres_TMR_HealthState := 1;
    rTemp_B := rMeltPres_SensC_Val;
ELSE
    iMeltPres_TMR_HealthState := 0;
    rTemp_B := rMeltPres_Prev_Voted;
    bTrip_TMR_SensorCollapse := TRUE;
END_IF;

rMeltPres_Prev_Voted := rMeltPres_Voted_Val;
rMeltPres_Voted_Val := rMeltPres_Prev_Voted + (0.40 * (rTemp_B - rMeltPres_Prev_Voted));

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 1.3: SCREW AXIAL POSITION ABSOLUTE SCALES (TMR BANK 3)
 * Channels: rScrewPos_LinearEncA_In, rScrewPos_LinearEncB_In, rScrewPos_LinearEncC_In [mm]
 * Dynamic Range: 0.0 to 450.0 mm, Sub-micron Optical Encoders
 * --------------------------------------------------------------------------------------------------------------------- *)
rScrewPos_SensA_Val := rScrewPos_LinearEncA_In;
rScrewPos_SensB_Val := rScrewPos_LinearEncB_In;
rScrewPos_SensC_Val := rScrewPos_LinearEncC_In;

IF (rScrewPos_SensA_Val < -5.0) OR (rScrewPos_SensA_Val > 480.0) THEN
    bScrewPos_SensA_Fault := TRUE;
END_IF;

IF (rScrewPos_SensB_Val < -5.0) OR (rScrewPos_SensB_Val > 480.0) THEN
    bScrewPos_SensB_Fault := TRUE;
END_IF;

IF (rScrewPos_SensC_Val < -5.0) OR (rScrewPos_SensC_Val > 480.0) THEN
    bScrewPos_SensC_Fault := TRUE;
END_IF;

(* Pairwise Scale Discrepancy *)
IF (NOT bScrewPos_SensA_Fault) AND (NOT bScrewPos_SensB_Fault) THEN
    rTemp_AbsDiff := ABS(rScrewPos_SensA_Val - rScrewPos_SensB_Val);
    IF rTemp_AbsDiff > rScrewPos_DiscThresh THEN
        rScrewPos_DiscTimer_AB := rScrewPos_DiscTimer_AB + rScanTime_Ts;
        IF rScrewPos_DiscTimer_AB >= rScrewPos_DiscMaxTime THEN
            IF NOT bScrewPos_SensC_Fault THEN
                IF ABS(rScrewPos_SensA_Val - rScrewPos_SensC_Val) > ABS(rScrewPos_SensB_Val - rScrewPos_SensC_Val) THEN
                    bScrewPos_SensA_Fault := TRUE;
                ELSE
                    bScrewPos_SensB_Fault := TRUE;
                END_IF;
            ELSE
                bScrewPos_SensA_Fault := TRUE;
            END_IF;
        END_IF;
    ELSE
        rScrewPos_DiscTimer_AB := MAX(0.0, rScrewPos_DiscTimer_AB - (rScanTime_Ts * 2.0));
    END_IF;
END_IF;

IF (NOT bScrewPos_SensB_Fault) AND (NOT bScrewPos_SensC_Fault) THEN
    rTemp_AbsDiff := ABS(rScrewPos_SensB_Val - rScrewPos_SensC_Val);
    IF rTemp_AbsDiff > rScrewPos_DiscThresh THEN
        rScrewPos_DiscTimer_BC := rScrewPos_DiscTimer_BC + rScanTime_Ts;
        IF rScrewPos_DiscTimer_BC >= rScrewPos_DiscMaxTime THEN
            IF NOT bScrewPos_SensA_Fault THEN
                IF ABS(rScrewPos_SensB_Val - rScrewPos_SensA_Val) > ABS(rScrewPos_SensC_Val - rScrewPos_SensA_Val) THEN
                    bScrewPos_SensB_Fault := TRUE;
                ELSE
                    bScrewPos_SensC_Fault := TRUE;
                END_IF;
            ELSE
                bScrewPos_SensB_Fault := TRUE;
            END_IF;
        END_IF;
    ELSE
        rScrewPos_DiscTimer_BC := MAX(0.0, rScrewPos_DiscTimer_BC - (rScanTime_Ts * 2.0));
    END_IF;
END_IF;

IF (NOT bScrewPos_SensC_Fault) AND (NOT bScrewPos_SensA_Fault) THEN
    rTemp_AbsDiff := ABS(rScrewPos_SensC_Val - rScrewPos_SensA_Val);
    IF rTemp_AbsDiff > rScrewPos_DiscThresh THEN
        rScrewPos_DiscTimer_CA := rScrewPos_DiscTimer_CA + rScanTime_Ts;
        IF rScrewPos_DiscTimer_CA >= rScrewPos_DiscMaxTime THEN
            IF NOT bScrewPos_SensB_Fault THEN
                IF ABS(rScrewPos_SensC_Val - rScrewPos_SensB_Val) > ABS(rScrewPos_SensA_Val - rScrewPos_SensB_Val) THEN
                    bScrewPos_SensC_Fault := TRUE;
                ELSE
                    bScrewPos_SensA_Fault := TRUE;
                END_IF;
            ELSE
                bScrewPos_SensC_Fault := TRUE;
            END_IF;
        END_IF;
    ELSE
        rScrewPos_DiscTimer_CA := MAX(0.0, rScrewPos_DiscTimer_CA - (rScanTime_Ts * 2.0));
    END_IF;
END_IF;

(* 2oo3 Voting for Screw Position *)
IF (NOT bScrewPos_SensA_Fault) AND (NOT bScrewPos_SensB_Fault) AND (NOT bScrewPos_SensC_Fault) THEN
    iScrewPos_TMR_HealthState := 3;
    IF ((rScrewPos_SensA_Val >= rScrewPos_SensB_Val) AND (rScrewPos_SensA_Val <= rScrewPos_SensC_Val)) OR
       ((rScrewPos_SensA_Val >= rScrewPos_SensC_Val) AND (rScrewPos_SensA_Val <= rScrewPos_SensB_Val)) THEN
        rTemp_C := rScrewPos_SensA_Val;
    ELSIF ((rScrewPos_SensB_Val >= rScrewPos_SensA_Val) AND (rScrewPos_SensB_Val <= rScrewPos_SensC_Val)) OR
          ((rScrewPos_SensB_Val >= rScrewPos_SensC_Val) AND (rScrewPos_SensB_Val <= rScrewPos_SensA_Val)) THEN
        rTemp_C := rScrewPos_SensB_Val;
    ELSE
        rTemp_C := rScrewPos_SensC_Val;
    END_IF;
ELSIF (NOT bScrewPos_SensA_Fault) AND (NOT bScrewPos_SensB_Fault) AND bScrewPos_SensC_Fault THEN
    iScrewPos_TMR_HealthState := 2;
    rTemp_C := (rScrewPos_SensA_Val + rScrewPos_SensB_Val) * 0.5;
ELSIF (NOT bScrewPos_SensB_Fault) AND (NOT bScrewPos_SensC_Fault) AND bScrewPos_SensA_Fault THEN
    iScrewPos_TMR_HealthState := 2;
    rTemp_C := (rScrewPos_SensB_Val + rScrewPos_SensC_Val) * 0.5;
ELSIF (NOT bScrewPos_SensC_Fault) AND (NOT bScrewPos_SensA_Fault) AND bScrewPos_SensB_Fault THEN
    iScrewPos_TMR_HealthState := 2;
    rTemp_C := (rScrewPos_SensC_Val + rScrewPos_SensA_Val) * 0.5;
ELSIF (NOT bScrewPos_SensA_Fault) AND bScrewPos_SensB_Fault AND bScrewPos_SensC_Fault THEN
    iScrewPos_TMR_HealthState := 1;
    rTemp_C := rScrewPos_SensA_Val;
ELSIF (NOT bScrewPos_SensB_Fault) AND bScrewPos_SensA_Fault AND bScrewPos_SensC_Fault THEN
    iScrewPos_TMR_HealthState := 1;
    rTemp_C := rScrewPos_SensB_Val;
ELSIF (NOT bScrewPos_SensC_Fault) AND bScrewPos_SensA_Fault AND bScrewPos_SensB_Fault THEN
    iScrewPos_TMR_HealthState := 1;
    rTemp_C := rScrewPos_SensC_Val;
ELSE
    iScrewPos_TMR_HealthState := 0;
    rTemp_C := rScrewPos_Prev_Voted;
    bTrip_TMR_SensorCollapse := TRUE;
END_IF;

rScrewPos_Prev_Voted := rScrewPos_Voted_Val;
rScrewPos_Voted_Val := rTemp_C;

(* Measured Injection Velocity via Backward Difference Filter *)
rScrewVelocity_Meas := (rScrewPos_Prev_Voted - rScrewPos_Voted_Val) / rScanTime_Ts;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 1.4: EXTRUDER BULK MELT THERMOCOUPLES (TMR BANK 4)
 * Channels: rMeltTemp_ThermocoupleA_In, rMeltTemp_ThermocoupleB_In, rMeltTemp_ThermocoupleC_In [deg C]
 * Dynamic Range: 50.0 to 420.0 deg C, Mineral Insulated Grounded Junction
 * --------------------------------------------------------------------------------------------------------------------- *)
rMeltTemp_SensA_Val := rMeltTemp_ThermocoupleA_In;
rMeltTemp_SensB_Val := rMeltTemp_ThermocoupleB_In;
rMeltTemp_SensC_Val := rMeltTemp_ThermocoupleC_In;

IF (rMeltTemp_SensA_Val < 10.0) OR (rMeltTemp_SensA_Val > 450.0) THEN
    bMeltTemp_SensA_Fault := TRUE;
END_IF;

IF (rMeltTemp_SensB_Val < 10.0) OR (rMeltTemp_SensB_Val > 450.0) THEN
    bMeltTemp_SensB_Fault := TRUE;
END_IF;

IF (rMeltTemp_SensC_Val < 10.0) OR (rMeltTemp_SensC_Val > 450.0) THEN
    bMeltTemp_SensC_Fault := TRUE;
END_IF;

(* Pairwise Thermal Discrepancy *)
IF (NOT bMeltTemp_SensA_Fault) AND (NOT bMeltTemp_SensB_Fault) THEN
    rTemp_AbsDiff := ABS(rMeltTemp_SensA_Val - rMeltTemp_SensB_Val);
    IF rTemp_AbsDiff > rMeltTemp_DiscThresh THEN
        rMeltTemp_DiscTimer_AB := rMeltTemp_DiscTimer_AB + rScanTime_Ts;
        IF rMeltTemp_DiscTimer_AB >= rMeltTemp_DiscMaxTime THEN
            IF NOT bMeltTemp_SensC_Fault THEN
                IF ABS(rMeltTemp_SensA_Val - rMeltTemp_SensC_Val) > ABS(rMeltTemp_SensB_Val - rMeltTemp_SensC_Val) THEN
                    bMeltTemp_SensA_Fault := TRUE;
                ELSE
                    bMeltTemp_SensB_Fault := TRUE;
                END_IF;
            ELSE
                bMeltTemp_SensA_Fault := TRUE;
            END_IF;
        END_IF;
    ELSE
        rMeltTemp_DiscTimer_AB := MAX(0.0, rMeltTemp_DiscTimer_AB - (rScanTime_Ts * 2.0));
    END_IF;
END_IF;

IF (NOT bMeltTemp_SensB_Fault) AND (NOT bMeltTemp_SensC_Fault) THEN
    rTemp_AbsDiff := ABS(rMeltTemp_SensB_Val - rMeltTemp_SensC_Val);
    IF rTemp_AbsDiff > rMeltTemp_DiscThresh THEN
        rMeltTemp_DiscTimer_BC := rMeltTemp_DiscTimer_BC + rScanTime_Ts;
        IF rMeltTemp_DiscTimer_BC >= rMeltTemp_DiscMaxTime THEN
            IF NOT bMeltTemp_SensA_Fault THEN
                IF ABS(rMeltTemp_SensB_Val - rMeltTemp_SensA_Val) > ABS(rMeltTemp_SensC_Val - rMeltTemp_SensA_Val) THEN
                    bMeltTemp_SensB_Fault := TRUE;
                ELSE
                    bMeltTemp_SensC_Fault := TRUE;
                END_IF;
            ELSE
                bMeltTemp_SensB_Fault := TRUE;
            END_IF;
        END_IF;
    ELSE
        rMeltTemp_DiscTimer_BC := MAX(0.0, rMeltTemp_DiscTimer_BC - (rScanTime_Ts * 2.0));
    END_IF;
END_IF;

IF (NOT bMeltTemp_SensC_Fault) AND (NOT bMeltTemp_SensA_Fault) THEN
    rTemp_AbsDiff := ABS(rMeltTemp_SensC_Val - rMeltTemp_SensA_Val);
    IF rTemp_AbsDiff > rMeltTemp_DiscThresh THEN
        rMeltTemp_DiscTimer_CA := rMeltTemp_DiscTimer_CA + rScanTime_Ts;
        IF rMeltTemp_DiscTimer_CA >= rMeltTemp_DiscMaxTime THEN
            IF NOT bMeltTemp_SensB_Fault THEN
                IF ABS(rMeltTemp_SensC_Val - rMeltTemp_SensB_Val) > ABS(rMeltTemp_SensA_Val - rMeltTemp_SensB_Val) THEN
                    bMeltTemp_SensC_Fault := TRUE;
                ELSE
                    bMeltTemp_SensA_Fault := TRUE;
                END_IF;
            ELSE
                bMeltTemp_SensC_Fault := TRUE;
            END_IF;
        END_IF;
    ELSE
        rMeltTemp_DiscTimer_CA := MAX(0.0, rMeltTemp_DiscTimer_CA - (rScanTime_Ts * 2.0));
    END_IF;
END_IF;

(* 2oo3 Voting for Bulk Melt Temperature *)
IF (NOT bMeltTemp_SensA_Fault) AND (NOT bMeltTemp_SensB_Fault) AND (NOT bMeltTemp_SensC_Fault) THEN
    iMeltTemp_TMR_HealthState := 3;
    IF ((rMeltTemp_SensA_Val >= rMeltTemp_SensB_Val) AND (rMeltTemp_SensA_Val <= rMeltTemp_SensC_Val)) OR
       ((rMeltTemp_SensA_Val >= rMeltTemp_SensC_Val) AND (rMeltTemp_SensA_Val <= rMeltTemp_SensB_Val)) THEN
        rMeltTemp_Voted_Val := rMeltTemp_SensA_Val;
    ELSIF ((rMeltTemp_SensB_Val >= rMeltTemp_SensA_Val) AND (rMeltTemp_SensB_Val <= rMeltTemp_SensC_Val)) OR
          ((rMeltTemp_SensB_Val >= rMeltTemp_SensC_Val) AND (rMeltTemp_SensB_Val <= rMeltTemp_SensA_Val)) THEN
        rMeltTemp_Voted_Val := rMeltTemp_SensB_Val;
    ELSE
        rMeltTemp_Voted_Val := rMeltTemp_SensC_Val;
    END_IF;
ELSIF (NOT bMeltTemp_SensA_Fault) AND (NOT bMeltTemp_SensB_Fault) AND bMeltTemp_SensC_Fault THEN
    iMeltTemp_TMR_HealthState := 2;
    rMeltTemp_Voted_Val := (rMeltTemp_SensA_Val + rMeltTemp_SensB_Val) * 0.5;
ELSIF (NOT bMeltTemp_SensB_Fault) AND (NOT bMeltTemp_SensC_Fault) AND bMeltTemp_SensA_Fault THEN
    iMeltTemp_TMR_HealthState := 2;
    rMeltTemp_Voted_Val := (rMeltTemp_SensB_Val + rMeltTemp_SensC_Val) * 0.5;
ELSIF (NOT bMeltTemp_SensC_Fault) AND (NOT bMeltTemp_SensA_Fault) AND bMeltTemp_SensB_Fault THEN
    iMeltTemp_TMR_HealthState := 2;
    rMeltTemp_Voted_Val := (rMeltTemp_SensC_Val + rMeltTemp_SensA_Val) * 0.5;
ELSIF (NOT bMeltTemp_SensA_Fault) AND bMeltTemp_SensB_Fault AND bMeltTemp_SensC_Fault THEN
    iMeltTemp_TMR_HealthState := 1;
    rMeltTemp_Voted_Val := rMeltTemp_SensA_Val;
ELSIF (NOT bMeltTemp_SensB_Fault) AND bMeltTemp_SensA_Fault AND bMeltTemp_SensC_Fault THEN
    iMeltTemp_TMR_HealthState := 1;
    rMeltTemp_Voted_Val := rMeltTemp_SensB_Val;
ELSIF (NOT bMeltTemp_SensC_Fault) AND bMeltTemp_SensA_Fault AND bMeltTemp_SensB_Fault THEN
    iMeltTemp_TMR_HealthState := 1;
    rMeltTemp_Voted_Val := rMeltTemp_SensC_Val;
ELSE
    iMeltTemp_TMR_HealthState := 0;
    bTrip_TMR_SensorCollapse := TRUE;
END_IF;
