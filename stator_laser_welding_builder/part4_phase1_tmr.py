# stator_laser_welding_builder/part4_phase1_tmr.py

def get_phase1_tmr():
    return """(*
====================================================================================================
PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANT (TMR) SENSOR VOTING SUITE WITH DISCREPANCY TIMERS
Channels:
  1. 3D Profilometer Pin Gap Transducers (Tol = 0.020 [mm], Timeout = 0.040 [s])
  2. 3D Profilometer Pin Height Delta (Tol = 0.035 [mm], Timeout = 0.040 [s])
  3. Coaxial Melt Pool High-Speed Pyrometer (Tol = 75.0 [deg C], Timeout = 0.010 [s])
  4. Fiber Laser Delivered Optical Power Monitor (Tol = 0.25 [kW], Timeout = 0.020 [s])
  5. Shielding Nitrogen Mass Flowmeters (Tol = 3.5 [L/min], Timeout = 0.050 [s])
  6. Hydraulic Collet Clamping Pressure Transducers (Tol = 8.0 [bar], Timeout = 0.040 [s])
====================================================================================================
*)

(* -------------------------------------------------------------------------------------------------
   CHANNEL GROUP 1: 3D PROFILOMETER PIN GAP GAUGES (1A, 1B, 1C)
   ------------------------------------------------------------------------------------------------- *)
(* Step 1.1: Calculate Pairwise Absolute Differences *)
rTemp_Scalar1 := ABS(rGap_Sensor_1A_mm - rGap_Sensor_1B_mm);
rTemp_Scalar2 := ABS(rGap_Sensor_1B_mm - rGap_Sensor_1C_mm);
rTemp_SumReal1 := ABS(rGap_Sensor_1C_mm - rGap_Sensor_1A_mm);

(* Step 1.2: Discrepancy Debounce Timers *)
IF rTemp_Scalar1 > 0.020 THEN
    rGap_DiscrepTimer_AB_s := rGap_DiscrepTimer_AB_s + rScanTime_s;
ELSE
    rGap_DiscrepTimer_AB_s := MAX(0.0, rGap_DiscrepTimer_AB_s - (2.0 * rScanTime_s));
END_IF;

IF rTemp_Scalar2 > 0.020 THEN
    rGap_DiscrepTimer_BC_s := rGap_DiscrepTimer_BC_s + rScanTime_s;
ELSE
    rGap_DiscrepTimer_BC_s := MAX(0.0, rGap_DiscrepTimer_BC_s - (2.0 * rScanTime_s));
END_IF;

IF rTemp_SumReal1 > 0.020 THEN
    rGap_DiscrepTimer_CA_s := rGap_DiscrepTimer_CA_s + rScanTime_s;
ELSE
    rGap_DiscrepTimer_CA_s := MAX(0.0, rGap_DiscrepTimer_CA_s - (2.0 * rScanTime_s));
END_IF;

(* Step 1.3: Channel Health Isolation *)
bTemp_Condition1 := (rGap_DiscrepTimer_AB_s >= 0.040);
bTemp_Condition2 := (rGap_DiscrepTimer_BC_s >= 0.040);
bGap_ChA_Healthy := NOT (bTemp_Condition1 AND (rGap_DiscrepTimer_CA_s >= 0.040));
bGap_ChB_Healthy := NOT (bTemp_Condition1 AND bTemp_Condition2);
bGap_ChC_Healthy := NOT (bTemp_Condition2 AND (rGap_DiscrepTimer_CA_s >= 0.040));

(* Step 1.4: 2oo3 Voting & Degradation Matrix *)
IF bGap_ChA_Healthy AND bGap_ChB_Healthy AND bGap_ChC_Healthy THEN
    (* 3 Channels Healthy: Exact Median Selection *)
    IF (rGap_Sensor_1A_mm >= rGap_Sensor_1B_mm) THEN
        IF (rGap_Sensor_1B_mm >= rGap_Sensor_1C_mm) THEN
            rGap_Voted_mm := rGap_Sensor_1B_mm;
        ELSIF (rGap_Sensor_1A_mm <= rGap_Sensor_1C_mm) THEN
            rGap_Voted_mm := rGap_Sensor_1A_mm;
        ELSE
            rGap_Voted_mm := rGap_Sensor_1C_mm;
        END_IF;
    ELSE
        IF (rGap_Sensor_1A_mm >= rGap_Sensor_1C_mm) THEN
            rGap_Voted_mm := rGap_Sensor_1A_mm;
        ELSIF (rGap_Sensor_1B_mm <= rGap_Sensor_1C_mm) THEN
            rGap_Voted_mm := rGap_Sensor_1B_mm;
        ELSE
            rGap_Voted_mm := rGap_Sensor_1C_mm;
        END_IF;
    END_IF;
    bGap_DegradedMode := FALSE;
    bGap_SensorVotingFailure := FALSE;
ELSIF bGap_ChA_Healthy AND bGap_ChB_Healthy THEN
    rGap_Voted_mm := (rGap_Sensor_1A_mm + rGap_Sensor_1B_mm) * 0.50;
    bGap_DegradedMode := TRUE;
    bGap_SensorVotingFailure := FALSE;
ELSIF bGap_ChB_Healthy AND bGap_ChC_Healthy THEN
    rGap_Voted_mm := (rGap_Sensor_1B_mm + rGap_Sensor_1C_mm) * 0.50;
    bGap_DegradedMode := TRUE;
    bGap_SensorVotingFailure := FALSE;
ELSIF bGap_ChA_Healthy AND bGap_ChC_Healthy THEN
    rGap_Voted_mm := (rGap_Sensor_1A_mm + rGap_Sensor_1C_mm) * 0.50;
    bGap_DegradedMode := TRUE;
    bGap_SensorVotingFailure := FALSE;
ELSIF bGap_ChA_Healthy THEN
    rGap_Voted_mm := rGap_Sensor_1A_mm;
    bGap_DegradedMode := TRUE;
    bGap_SensorVotingFailure := FALSE;
ELSIF bGap_ChB_Healthy THEN
    rGap_Voted_mm := rGap_Sensor_1B_mm;
    bGap_DegradedMode := TRUE;
    bGap_SensorVotingFailure := FALSE;
ELSIF bGap_ChC_Healthy THEN
    rGap_Voted_mm := rGap_Sensor_1C_mm;
    bGap_DegradedMode := TRUE;
    bGap_SensorVotingFailure := FALSE;
ELSE
    (* All Channels Tripped: Latch Critical Fault *)
    bGap_SensorVotingFailure := TRUE;
    bGap_DegradedMode := TRUE;
END_IF;


(* -------------------------------------------------------------------------------------------------
   CHANNEL GROUP 1 EXT: PIN HEIGHT MISMATCH TRANSDUCERS (1A, 1B, 1C)
   ------------------------------------------------------------------------------------------------- *)
rTemp_Scalar1 := ABS(rHeight_Diff_1A_mm - rHeight_Diff_1B_mm);
rTemp_Scalar2 := ABS(rHeight_Diff_1B_mm - rHeight_Diff_1C_mm);
rTemp_SumReal1 := ABS(rHeight_Diff_1C_mm - rHeight_Diff_1A_mm);

IF rTemp_Scalar1 > 0.035 THEN
    rHeight_DiscrepTimer_AB_s := rHeight_DiscrepTimer_AB_s + rScanTime_s;
ELSE
    rHeight_DiscrepTimer_AB_s := MAX(0.0, rHeight_DiscrepTimer_AB_s - (2.0 * rScanTime_s));
END_IF;

IF rTemp_Scalar2 > 0.035 THEN
    rHeight_DiscrepTimer_BC_s := rHeight_DiscrepTimer_BC_s + rScanTime_s;
ELSE
    rHeight_DiscrepTimer_BC_s := MAX(0.0, rHeight_DiscrepTimer_BC_s - (2.0 * rScanTime_s));
END_IF;

IF rTemp_SumReal1 > 0.035 THEN
    rHeight_DiscrepTimer_CA_s := rHeight_DiscrepTimer_CA_s + rScanTime_s;
ELSE
    rHeight_DiscrepTimer_CA_s := MAX(0.0, rHeight_DiscrepTimer_CA_s - (2.0 * rScanTime_s));
END_IF;

bTemp_Condition1 := (rHeight_DiscrepTimer_AB_s >= 0.040);
bTemp_Condition2 := (rHeight_DiscrepTimer_BC_s >= 0.040);
bHeight_ChA_Healthy := NOT (bTemp_Condition1 AND (rHeight_DiscrepTimer_CA_s >= 0.040));
bHeight_ChB_Healthy := NOT (bTemp_Condition1 AND bTemp_Condition2);
bHeight_ChC_Healthy := NOT (bTemp_Condition2 AND (rHeight_DiscrepTimer_CA_s >= 0.040));

IF bHeight_ChA_Healthy AND bHeight_ChB_Healthy AND bHeight_ChC_Healthy THEN
    IF (rHeight_Diff_1A_mm >= rHeight_Diff_1B_mm) THEN
        IF (rHeight_Diff_1B_mm >= rHeight_Diff_1C_mm) THEN
            rHeight_Voted_mm := rHeight_Diff_1B_mm;
        ELSIF (rHeight_Diff_1A_mm <= rHeight_Diff_1C_mm) THEN
            rHeight_Voted_mm := rHeight_Diff_1A_mm;
        ELSE
            rHeight_Voted_mm := rHeight_Diff_1C_mm;
        END_IF;
    ELSE
        IF (rHeight_Diff_1A_mm >= rHeight_Diff_1C_mm) THEN
            rHeight_Voted_mm := rHeight_Diff_1A_mm;
        ELSIF (rHeight_Diff_1B_mm <= rHeight_Diff_1C_mm) THEN
            rHeight_Voted_mm := rHeight_Diff_1B_mm;
        ELSE
            rHeight_Voted_mm := rHeight_Diff_1C_mm;
        END_IF;
    END_IF;
    bHeight_DegradedMode := FALSE;
    bHeight_SensorVotingFailure := FALSE;
ELSIF bHeight_ChA_Healthy AND bHeight_ChB_Healthy THEN
    rHeight_Voted_mm := (rHeight_Diff_1A_mm + rHeight_Diff_1B_mm) * 0.50;
    bHeight_DegradedMode := TRUE;
    bHeight_SensorVotingFailure := FALSE;
ELSIF bHeight_ChB_Healthy AND bHeight_ChC_Healthy THEN
    rHeight_Voted_mm := (rHeight_Diff_1B_mm + rHeight_Diff_1C_mm) * 0.50;
    bHeight_DegradedMode := TRUE;
    bHeight_SensorVotingFailure := FALSE;
ELSIF bHeight_ChA_Healthy AND bHeight_ChC_Healthy THEN
    rHeight_Voted_mm := (rHeight_Diff_1A_mm + rHeight_Diff_1C_mm) * 0.50;
    bHeight_DegradedMode := TRUE;
    bHeight_SensorVotingFailure := FALSE;
ELSE
    bHeight_SensorVotingFailure := TRUE;
    bHeight_DegradedMode := TRUE;
END_IF;


(* -------------------------------------------------------------------------------------------------
   CHANNEL GROUP 2: COAXIAL MELT POOL FAST PYROMETER PHOTODIODES (2A, 2B, 2C)
   ------------------------------------------------------------------------------------------------- *)
rTemp_Scalar1 := ABS(rMeltPool_Temp_2A_degC - rMeltPool_Temp_2B_degC);
rTemp_Scalar2 := ABS(rMeltPool_Temp_2B_degC - rMeltPool_Temp_2C_degC);
rTemp_SumReal1 := ABS(rMeltPool_Temp_2C_degC - rMeltPool_Temp_2A_degC);

(* High-Speed Thermal Discrepancy Debounce (10 ms) *)
IF rTemp_Scalar1 > 75.0 THEN
    rMeltPool_DiscrepTimer_AB_s := rMeltPool_DiscrepTimer_AB_s + rScanTime_s;
ELSE
    rMeltPool_DiscrepTimer_AB_s := MAX(0.0, rMeltPool_DiscrepTimer_AB_s - (2.0 * rScanTime_s));
END_IF;

IF rTemp_Scalar2 > 75.0 THEN
    rMeltPool_DiscrepTimer_BC_s := rMeltPool_DiscrepTimer_BC_s + rScanTime_s;
ELSE
    rMeltPool_DiscrepTimer_BC_s := MAX(0.0, rMeltPool_DiscrepTimer_BC_s - (2.0 * rScanTime_s));
END_IF;

IF rTemp_SumReal1 > 75.0 THEN
    rMeltPool_DiscrepTimer_CA_s := rMeltPool_DiscrepTimer_CA_s + rScanTime_s;
ELSE
    rMeltPool_DiscrepTimer_CA_s := MAX(0.0, rMeltPool_DiscrepTimer_CA_s - (2.0 * rScanTime_s));
END_IF;

bTemp_Condition1 := (rMeltPool_DiscrepTimer_AB_s >= 0.010);
bTemp_Condition2 := (rMeltPool_DiscrepTimer_BC_s >= 0.010);
bMeltPool_ChA_Healthy := NOT (bTemp_Condition1 AND (rMeltPool_DiscrepTimer_CA_s >= 0.010));
bMeltPool_ChB_Healthy := NOT (bTemp_Condition1 AND bTemp_Condition2);
bMeltPool_ChC_Healthy := NOT (bTemp_Condition2 AND (rMeltPool_DiscrepTimer_CA_s >= 0.010));

IF bMeltPool_ChA_Healthy AND bMeltPool_ChB_Healthy AND bMeltPool_ChC_Healthy THEN
    IF (rMeltPool_Temp_2A_degC >= rMeltPool_Temp_2B_degC) THEN
        IF (rMeltPool_Temp_2B_degC >= rMeltPool_Temp_2C_degC) THEN
            rMeltPool_Voted_degC := rMeltPool_Temp_2B_degC;
        ELSIF (rMeltPool_Temp_2A_degC <= rMeltPool_Temp_2C_degC) THEN
            rMeltPool_Voted_degC := rMeltPool_Temp_2A_degC;
        ELSE
            rMeltPool_Voted_degC := rMeltPool_Temp_2C_degC;
        END_IF;
    ELSE
        IF (rMeltPool_Temp_2A_degC >= rMeltPool_Temp_2C_degC) THEN
            rMeltPool_Voted_degC := rMeltPool_Temp_2A_degC;
        ELSIF (rMeltPool_Temp_2B_degC <= rMeltPool_Temp_2C_degC) THEN
            rMeltPool_Voted_degC := rMeltPool_Temp_2B_degC;
        ELSE
            rMeltPool_Voted_degC := rMeltPool_Temp_2C_degC;
        END_IF;
    END_IF;
    bMeltPool_DegradedMode := FALSE;
    bMeltPool_SensorVotingFailure := FALSE;
ELSIF bMeltPool_ChA_Healthy AND bMeltPool_ChB_Healthy THEN
    rMeltPool_Voted_degC := (rMeltPool_Temp_2A_degC + rMeltPool_Temp_2B_degC) * 0.50;
    bMeltPool_DegradedMode := TRUE;
    bMeltPool_SensorVotingFailure := FALSE;
ELSIF bMeltPool_ChB_Healthy AND bMeltPool_ChC_Healthy THEN
    rMeltPool_Voted_degC := (rMeltPool_Temp_2B_degC + rMeltPool_Temp_2C_degC) * 0.50;
    bMeltPool_DegradedMode := TRUE;
    bMeltPool_SensorVotingFailure := FALSE;
ELSIF bMeltPool_ChA_Healthy AND bMeltPool_ChC_Healthy THEN
    rMeltPool_Voted_degC := (rMeltPool_Temp_2A_degC + rMeltPool_Temp_2C_degC) * 0.50;
    bMeltPool_DegradedMode := TRUE;
    bMeltPool_SensorVotingFailure := FALSE;
ELSE
    bMeltPool_SensorVotingFailure := TRUE;
    bMeltPool_DegradedMode := TRUE;
END_IF;


(* -------------------------------------------------------------------------------------------------
   CHANNEL GROUP 3: FIBER LASER DELIVERED OPTICAL POWER MONITORS (3A, 3B, 3C)
   ------------------------------------------------------------------------------------------------- *)
rTemp_Scalar1 := ABS(rLaserPower_Mon_3A_kW - rLaserPower_Mon_3B_kW);
rTemp_Scalar2 := ABS(rLaserPower_Mon_3B_kW - rLaserPower_Mon_3C_kW);
rTemp_SumReal1 := ABS(rLaserPower_Mon_3C_kW - rLaserPower_Mon_3A_kW);

IF rTemp_Scalar1 > 0.25 THEN
    rLaserPwr_DiscrepTimer_AB_s := rLaserPwr_DiscrepTimer_AB_s + rScanTime_s;
ELSE
    rLaserPwr_DiscrepTimer_AB_s := MAX(0.0, rLaserPwr_DiscrepTimer_AB_s - (2.0 * rScanTime_s));
END_IF;

IF rTemp_Scalar2 > 0.25 THEN
    rLaserPwr_DiscrepTimer_BC_s := rLaserPwr_DiscrepTimer_BC_s + rScanTime_s;
ELSE
    rLaserPwr_DiscrepTimer_BC_s := MAX(0.0, rLaserPwr_DiscrepTimer_BC_s - (2.0 * rScanTime_s));
END_IF;

IF rTemp_SumReal1 > 0.25 THEN
    rLaserPwr_DiscrepTimer_CA_s := rLaserPwr_DiscrepTimer_CA_s + rScanTime_s;
ELSE
    rLaserPwr_DiscrepTimer_CA_s := MAX(0.0, rLaserPwr_DiscrepTimer_CA_s - (2.0 * rScanTime_s));
END_IF;

bTemp_Condition1 := (rLaserPwr_DiscrepTimer_AB_s >= 0.020);
bTemp_Condition2 := (rLaserPwr_DiscrepTimer_BC_s >= 0.020);
bLaserPwr_ChA_Healthy := NOT (bTemp_Condition1 AND (rLaserPwr_DiscrepTimer_CA_s >= 0.020));
bLaserPwr_ChB_Healthy := NOT (bTemp_Condition1 AND bTemp_Condition2);
bLaserPwr_ChC_Healthy := NOT (bTemp_Condition2 AND (rLaserPwr_DiscrepTimer_CA_s >= 0.020));

IF bLaserPwr_ChA_Healthy AND bLaserPwr_ChB_Healthy AND bLaserPwr_ChC_Healthy THEN
    IF (rLaserPower_Mon_3A_kW >= rLaserPower_Mon_3B_kW) THEN
        IF (rLaserPower_Mon_3B_kW >= rLaserPower_Mon_3C_kW) THEN
            rLaserPwr_Voted_kW := rLaserPower_Mon_3B_kW;
        ELSIF (rLaserPower_Mon_3A_kW <= rLaserPower_Mon_3C_kW) THEN
            rLaserPwr_Voted_kW := rLaserPower_Mon_3A_kW;
        ELSE
            rLaserPwr_Voted_kW := rLaserPower_Mon_3C_kW;
        END_IF;
    ELSE
        IF (rLaserPower_Mon_3A_kW >= rLaserPower_Mon_3C_kW) THEN
            rLaserPwr_Voted_kW := rLaserPower_Mon_3A_kW;
        ELSIF (rLaserPower_Mon_3B_kW <= rLaserPower_Mon_3C_kW) THEN
            rLaserPwr_Voted_kW := rLaserPower_Mon_3B_kW;
        ELSE
            rLaserPwr_Voted_kW := rLaserPower_Mon_3C_kW;
        END_IF;
    END_IF;
    bLaserPwr_DegradedMode := FALSE;
    bLaserPwr_SensorVotingFailure := FALSE;
ELSIF bLaserPwr_ChA_Healthy AND bLaserPwr_ChB_Healthy THEN
    rLaserPwr_Voted_kW := (rLaserPower_Mon_3A_kW + rLaserPower_Mon_3B_kW) * 0.50;
    bLaserPwr_DegradedMode := TRUE;
    bLaserPwr_SensorVotingFailure := FALSE;
ELSIF bLaserPwr_ChB_Healthy AND bLaserPwr_ChC_Healthy THEN
    rLaserPwr_Voted_kW := (rLaserPower_Mon_3B_kW + rLaserPower_Mon_3C_kW) * 0.50;
    bLaserPwr_DegradedMode := TRUE;
    bLaserPwr_SensorVotingFailure := FALSE;
ELSIF bLaserPwr_ChA_Healthy AND bLaserPwr_ChC_Healthy THEN
    rLaserPwr_Voted_kW := (rLaserPower_Mon_3A_kW + rLaserPower_Mon_3C_kW) * 0.50;
    bLaserPwr_DegradedMode := TRUE;
    bLaserPwr_SensorVotingFailure := FALSE;
ELSE
    bLaserPwr_SensorVotingFailure := TRUE;
    bLaserPwr_DegradedMode := TRUE;
END_IF;


(* -------------------------------------------------------------------------------------------------
   CHANNEL GROUP 4: SHIELDING NITROGEN GAS MASS FLOWMETERS (4A, 4B, 4C)
   ------------------------------------------------------------------------------------------------- *)
rTemp_Scalar1 := ABS(rShieldGas_Flow_4A_Lmin - rShieldGas_Flow_4B_Lmin);
rTemp_Scalar2 := ABS(rShieldGas_Flow_4B_Lmin - rShieldGas_Flow_4C_Lmin);
rTemp_SumReal1 := ABS(rShieldGas_Flow_4C_Lmin - rShieldGas_Flow_4A_Lmin);

IF rTemp_Scalar1 > 3.5 THEN
    rShieldGas_DiscrepTimer_AB_s := rShieldGas_DiscrepTimer_AB_s + rScanTime_s;
ELSE
    rShieldGas_DiscrepTimer_AB_s := MAX(0.0, rShieldGas_DiscrepTimer_AB_s - (2.0 * rScanTime_s));
END_IF;

IF rTemp_Scalar2 > 3.5 THEN
    rShieldGas_DiscrepTimer_BC_s := rShieldGas_DiscrepTimer_BC_s + rScanTime_s;
ELSE
    rShieldGas_DiscrepTimer_BC_s := MAX(0.0, rShieldGas_DiscrepTimer_BC_s - (2.0 * rScanTime_s));
END_IF;

IF rTemp_SumReal1 > 3.5 THEN
    rShieldGas_DiscrepTimer_CA_s := rShieldGas_DiscrepTimer_CA_s + rScanTime_s;
ELSE
    rShieldGas_DiscrepTimer_CA_s := MAX(0.0, rShieldGas_DiscrepTimer_CA_s - (2.0 * rScanTime_s));
END_IF;

bTemp_Condition1 := (rShieldGas_DiscrepTimer_AB_s >= 0.050);
bTemp_Condition2 := (rShieldGas_DiscrepTimer_BC_s >= 0.050);
bShieldGas_ChA_Healthy := NOT (bTemp_Condition1 AND (rShieldGas_DiscrepTimer_CA_s >= 0.050));
bShieldGas_ChB_Healthy := NOT (bTemp_Condition1 AND bTemp_Condition2);
bShieldGas_ChC_Healthy := NOT (bTemp_Condition2 AND (rShieldGas_DiscrepTimer_CA_s >= 0.050));

IF bShieldGas_ChA_Healthy AND bShieldGas_ChB_Healthy AND bShieldGas_ChC_Healthy THEN
    IF (rShieldGas_Flow_4A_Lmin >= rShieldGas_Flow_4B_Lmin) THEN
        IF (rShieldGas_Flow_4B_Lmin >= rShieldGas_Flow_4C_Lmin) THEN
            rShieldGas_Voted_Lmin := rShieldGas_Flow_4B_Lmin;
        ELSIF (rShieldGas_Flow_4A_Lmin <= rShieldGas_Flow_4C_Lmin) THEN
            rShieldGas_Voted_Lmin := rShieldGas_Flow_4A_Lmin;
        ELSE
            rShieldGas_Voted_Lmin := rShieldGas_Flow_4C_Lmin;
        END_IF;
    ELSE
        IF (rShieldGas_Flow_4A_Lmin >= rShieldGas_Flow_4C_Lmin) THEN
            rShieldGas_Voted_Lmin := rShieldGas_Flow_4A_Lmin;
        ELSIF (rShieldGas_Flow_4B_Lmin <= rShieldGas_Flow_4C_Lmin) THEN
            rShieldGas_Voted_Lmin := rShieldGas_Flow_4B_Lmin;
        ELSE
            rShieldGas_Voted_Lmin := rShieldGas_Flow_4C_Lmin;
        END_IF;
    END_IF;
    bShieldGas_DegradedMode := FALSE;
    bShieldGas_SensorVotingFailure := FALSE;
ELSIF bShieldGas_ChA_Healthy AND bShieldGas_ChB_Healthy THEN
    rShieldGas_Voted_Lmin := (rShieldGas_Flow_4A_Lmin + rShieldGas_Flow_4B_Lmin) * 0.50;
    bShieldGas_DegradedMode := TRUE;
    bShieldGas_SensorVotingFailure := FALSE;
ELSIF bShieldGas_ChB_Healthy AND bShieldGas_ChC_Healthy THEN
    rShieldGas_Voted_Lmin := (rShieldGas_Flow_4B_Lmin + rShieldGas_Flow_4C_Lmin) * 0.50;
    bShieldGas_DegradedMode := TRUE;
    bShieldGas_SensorVotingFailure := FALSE;
ELSIF bShieldGas_ChA_Healthy AND bShieldGas_ChC_Healthy THEN
    rShieldGas_Voted_Lmin := (rShieldGas_Flow_4A_Lmin + rShieldGas_Flow_4C_Lmin) * 0.50;
    bShieldGas_DegradedMode := TRUE;
    bShieldGas_SensorVotingFailure := FALSE;
ELSE
    bShieldGas_SensorVotingFailure := TRUE;
    bShieldGas_DegradedMode := TRUE;
END_IF;


(* -------------------------------------------------------------------------------------------------
   CHANNEL GROUP 5: ROTARY CHUCK HYDRAULIC CLAMPING PRESSURE (5A, 5B, 5C)
   ------------------------------------------------------------------------------------------------- *)
rTemp_Scalar1 := ABS(rHyd_ClampPress_5A_bar - rHyd_ClampPress_5B_bar);
rTemp_Scalar2 := ABS(rHyd_ClampPress_5B_bar - rHyd_ClampPress_5C_bar);
rTemp_SumReal1 := ABS(rHyd_ClampPress_5C_bar - rHyd_ClampPress_5A_bar);

IF rTemp_Scalar1 > 8.0 THEN
    rHydClamp_DiscrepTimer_AB_s := rHydClamp_DiscrepTimer_AB_s + rScanTime_s;
ELSE
    rHydClamp_DiscrepTimer_AB_s := MAX(0.0, rHydClamp_DiscrepTimer_AB_s - (2.0 * rScanTime_s));
END_IF;

IF rTemp_Scalar2 > 8.0 THEN
    rHydClamp_DiscrepTimer_BC_s := rHydClamp_DiscrepTimer_BC_s + rScanTime_s;
ELSE
    rHydClamp_DiscrepTimer_BC_s := MAX(0.0, rHydClamp_DiscrepTimer_BC_s - (2.0 * rScanTime_s));
END_IF;

IF rTemp_SumReal1 > 8.0 THEN
    rHydClamp_DiscrepTimer_CA_s := rHydClamp_DiscrepTimer_CA_s + rScanTime_s;
ELSE
    rHydClamp_DiscrepTimer_CA_s := MAX(0.0, rHydClamp_DiscrepTimer_CA_s - (2.0 * rScanTime_s));
END_IF;

bTemp_Condition1 := (rHydClamp_DiscrepTimer_AB_s >= 0.040);
bTemp_Condition2 := (rHydClamp_DiscrepTimer_BC_s >= 0.040);
bHydClamp_ChA_Healthy := NOT (bTemp_Condition1 AND (rHydClamp_DiscrepTimer_CA_s >= 0.040));
bHydClamp_ChB_Healthy := NOT (bTemp_Condition1 AND bTemp_Condition2);
bHydClamp_ChC_Healthy := NOT (bTemp_Condition2 AND (rHydClamp_DiscrepTimer_CA_s >= 0.040));

IF bHydClamp_ChA_Healthy AND bHydClamp_ChB_Healthy AND bHydClamp_ChC_Healthy THEN
    IF (rHyd_ClampPress_5A_bar >= rHyd_ClampPress_5B_bar) THEN
        IF (rHyd_ClampPress_5B_bar >= rHyd_ClampPress_5C_bar) THEN
            rHydClamp_Voted_bar := rHyd_ClampPress_5B_bar;
        ELSIF (rHyd_ClampPress_5A_bar <= rHyd_ClampPress_5C_bar) THEN
            rHydClamp_Voted_bar := rHyd_ClampPress_5A_bar;
        ELSE
            rHydClamp_Voted_bar := rHyd_ClampPress_5C_bar;
        END_IF;
    ELSE
        IF (rHyd_ClampPress_5A_bar >= rHyd_ClampPress_5C_bar) THEN
            rHydClamp_Voted_bar := rHyd_ClampPress_5A_bar;
        ELSIF (rHyd_ClampPress_5B_bar <= rHyd_ClampPress_5C_bar) THEN
            rHydClamp_Voted_bar := rHyd_ClampPress_5B_bar;
        ELSE
            rHydClamp_Voted_bar := rHyd_ClampPress_5C_bar;
        END_IF;
    END_IF;
    bHydClamp_DegradedMode := FALSE;
    bHydClamp_SensorVotingFailure := FALSE;
ELSIF bHydClamp_ChA_Healthy AND bHydClamp_ChB_Healthy THEN
    rHydClamp_Voted_bar := (rHyd_ClampPress_5A_bar + rHyd_ClampPress_5B_bar) * 0.50;
    bHydClamp_DegradedMode := TRUE;
    bHydClamp_SensorVotingFailure := FALSE;
ELSIF bHydClamp_ChB_Healthy AND bHydClamp_ChC_Healthy THEN
    rHydClamp_Voted_bar := (rHyd_ClampPress_5B_bar + rHyd_ClampPress_5C_bar) * 0.50;
    bHydClamp_DegradedMode := TRUE;
    bHydClamp_SensorVotingFailure := FALSE;
ELSIF bHydClamp_ChA_Healthy AND bHydClamp_ChC_Healthy THEN
    rHydClamp_Voted_bar := (rHyd_ClampPress_5A_bar + rHyd_ClampPress_5C_bar) * 0.50;
    bHydClamp_DegradedMode := TRUE;
    bHydClamp_SensorVotingFailure := FALSE;
ELSE
    bHydClamp_SensorVotingFailure := TRUE;
    bHydClamp_DegradedMode := TRUE;
END_IF;
"""
