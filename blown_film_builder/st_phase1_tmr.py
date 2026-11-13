# blown_film_builder/st_phase1_tmr.py

def get_phase1_tmr():
    return """(* ==================================================================================================== *)
(* PHASE 0: SYSTEM INITIALIZATION & DISCRETE CYBER-PHYSICAL STATE-SPACE MATRIX INITIALIZATION           *)
(* Sample Time Ts = 20 [ms], 6x6 Full Coupled System Dynamics, Decoupling Kernels & MPC Weight Vectors  *)
(* ==================================================================================================== *)
IF NOT bFirstScanDone THEN
    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0A: Discrete State Transition Matrix A (6x6) Initialization                                  *)
    (* Physics: Thickness thermal relaxation, IBC volume dynamics, FLH thermal conduction, melt flow    *)
    (* ------------------------------------------------------------------------------------------------ *)
    matA[0, 0] := 0.9820; matA[0, 1] := -0.0145; matA[0, 2] := 0.0032; matA[0, 3] := -0.0210; matA[0, 4] := 0.0185; matA[0, 5] := -0.0065;
    matA[1, 0] := -0.0085; matA[1, 1] := 0.9740; matA[1, 2] := 0.0480; matA[1, 3] := 0.0320; matA[1, 4] := -0.0120; matA[1, 5] := -0.0150;
    matA[2, 0] := 0.0015; matA[2, 1] := -0.0650; matA[2, 2] := 0.9350; matA[2, 3] := -0.0180; matA[2, 4] := 0.0085; matA[2, 5] := 0.0040;
    matA[3, 0] := 0.0120; matA[3, 1] := 0.0280; matA[3, 2] := -0.0110; matA[3, 3] := 0.9650; matA[3, 4] := 0.0540; matA[3, 5] := -0.0220;
    matA[4, 0] := 0.0000; matA[4, 1] := 0.0000; matA[4, 2] := 0.0000; matA[4, 3] := 0.0000; matA[4, 4] := 0.9920; matA[4, 5] := 0.0000;
    matA[5, 0] := -0.0180; matA[5, 1] := -0.0350; matA[5, 2] := 0.0080; matA[5, 3] := 0.0420; matA[5, 4] := -0.0280; matA[5, 5] := 0.9580;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0B: Discrete Control Input Matrix B (6x6) Initialization                                     *)
    (* Actuators: Thermal bolts, IBC supply, IBC exhaust, Air ring valve, Extruder speed, Haul-off speed*)
    (* ------------------------------------------------------------------------------------------------ *)
    matB[0, 0] := -0.0420; matB[0, 1] := 0.0035; matB[0, 2] := -0.0030; matB[0, 3] := -0.0185; matB[0, 4] := 0.0250; matB[0, 5] := -0.0380;
    matB[1, 0] := 0.0020; matB[1, 1] := 0.0620; matB[1, 2] := -0.0580; matB[1, 3] := -0.0140; matB[1, 4] := 0.0180; matB[1, 5] := -0.0210;
    matB[2, 0] := 0.0000; matB[2, 1] := 0.0850; matB[2, 2] := -0.0920; matB[2, 3] := 0.0050; matB[2, 4] := 0.0020; matB[2, 5] := 0.0000;
    matB[3, 0] := 0.0080; matB[3, 1] := -0.0220; matB[3, 2] := 0.0190; matB[3, 3] := -0.0750; matB[3, 4] := 0.0480; matB[3, 5] := 0.0650;
    matB[4, 0] := 0.0000; matB[4, 1] := 0.0000; matB[4, 2] := 0.0000; matB[4, 3] := 0.0000; matB[4, 4] := 0.0380; matB[4, 5] := 0.0000;
    matB[5, 0] := -0.0050; matB[5, 1] := -0.0180; matB[5, 2] := 0.0150; matB[5, 3] := 0.0280; matB[5, 4] := -0.0350; matB[5, 5] := 0.0820;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0C: Discrete Output Measurement Matrix C (6x6) Initialization                               *)
    (* Direct Observation with Calibration Scaling Coefficients                                          *)
    (* ------------------------------------------------------------------------------------------------ *)
    matC[0, 0] := 1.0000; matC[0, 1] := 0.0000; matC[0, 2] := 0.0000; matC[0, 3] := 0.0000; matC[0, 4] := 0.0000; matC[0, 5] := 0.0000;
    matC[1, 0] := 0.0000; matC[1, 1] := 1.0000; matC[1, 2] := 0.0000; matC[1, 3] := 0.0000; matC[1, 4] := 0.0000; matC[1, 5] := 0.0000;
    matC[2, 0] := 0.0000; matC[2, 1] := 0.0000; matC[2, 2] := 1.0000; matC[2, 3] := 0.0000; matC[2, 4] := 0.0000; matC[2, 5] := 0.0000;
    matC[3, 0] := 0.0000; matC[3, 1] := 0.0000; matC[3, 2] := 0.0000; matC[3, 3] := 1.0000; matC[3, 4] := 0.0000; matC[3, 5] := 0.0000;
    matC[4, 0] := 0.0000; matC[4, 1] := 0.0000; matC[4, 2] := 0.0000; matC[4, 3] := 0.0000; matC[4, 4] := 1.0000; matC[4, 5] := 0.0000;
    matC[5, 0] := 0.0000; matC[5, 1] := 0.0000; matC[5, 2] := 0.0000; matC[5, 3] := 0.0000; matC[5, 4] := 0.0000; matC[5, 5] := 1.0000;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0D: Discrete Feedthrough Matrix D (6x6) Initialization (Strictly Proper Dynamics)           *)
    (* ------------------------------------------------------------------------------------------------ *)
    matD[0, 0] := 0.0; matD[0, 1] := 0.0; matD[0, 2] := 0.0; matD[0, 3] := 0.0; matD[0, 4] := 0.0; matD[0, 5] := 0.0;
    matD[1, 0] := 0.0; matD[1, 1] := 0.0; matD[1, 2] := 0.0; matD[1, 3] := 0.0; matD[1, 4] := 0.0; matD[1, 5] := 0.0;
    matD[2, 0] := 0.0; matD[2, 1] := 0.0; matD[2, 2] := 0.0; matD[2, 3] := 0.0; matD[2, 4] := 0.0; matD[2, 5] := 0.0;
    matD[3, 0] := 0.0; matD[3, 1] := 0.0; matD[3, 2] := 0.0; matD[3, 3] := 0.0; matD[3, 4] := 0.0; matD[3, 5] := 0.0;
    matD[4, 0] := 0.0; matD[4, 1] := 0.0; matD[4, 2] := 0.0; matD[4, 3] := 0.0; matD[4, 4] := 0.0; matD[4, 5] := 0.0;
    matD[5, 0] := 0.0; matD[5, 1] := 0.0; matD[5, 2] := 0.0; matD[5, 3] := 0.0; matD[5, 4] := 0.0; matD[5, 5] := 0.0;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0E: Luenberger State Observer Innovation Gain Matrix L (6x6)                                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    matL[0, 0] := 0.2450; matL[0, 1] := -0.0120; matL[0, 2] := 0.0045; matL[0, 3] := -0.0150; matL[0, 4] := 0.0080; matL[0, 5] := -0.0050;
    matL[1, 0] := -0.0090; matL[1, 1] := 0.2850; matL[1, 2] := 0.0380; matL[1, 3] := 0.0210; matL[1, 4] := -0.0065; matL[1, 5] := -0.0120;
    matL[2, 0] := 0.0020; matL[2, 1] := -0.0420; matL[2, 2] := 0.3150; matL[2, 3] := -0.0140; matL[2, 4] := 0.0050; matL[2, 5] := 0.0035;
    matL[3, 0] := 0.0110; matL[3, 1] := 0.0190; matL[3, 2] := -0.0085; matL[3, 3] := 0.2650; matL[3, 4] := 0.0320; matL[3, 5] := -0.0180;
    matL[4, 0] := 0.0000; matL[4, 1] := 0.0000; matL[4, 2] := 0.0000; matL[4, 3] := 0.0000; matL[4, 4] := 0.2100; matL[4, 5] := 0.0000;
    matL[5, 0] := -0.0120; matL[5, 1] := -0.0220; matL[5, 2] := 0.0060; matL[5, 3] := 0.0280; matL[5, 4] := -0.0150; matL[5, 5] := 0.2950;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0F: Model Predictive Control (MPC) Cost Functional Weighting Vectors                        *)
    (* ------------------------------------------------------------------------------------------------ *)
    vecQ_weight[0] := 8.50;  (* Film Thickness 2-Sigma Penalty Q[0] *)
    vecQ_weight[1] := 12.00; (* Bubble Diameter Deviation Penalty Q[1] *)
    vecQ_weight[2] := 4.50;  (* IBC Differential Pressure Penalty Q[2] *)
    vecQ_weight[3] := 6.20;  (* Frost-Line Height Stability Penalty Q[3] *)
    vecQ_weight[4] := 3.80;  (* Tooling Melt Temperature Penalty Q[4] *)
    vecQ_weight[5] := 5.10;  (* Oscillating Haul-Off Web Tension Penalty Q[5] *)

    vecR_weight[0] := 0.45;  (* Air Ring Global Bolt Power Action Penalty R[0] *)
    vecR_weight[1] := 0.25;  (* IBC Supply Blower VFD Action Penalty R[1] *)
    vecR_weight[2] := 0.25;  (* IBC Exhaust Blower VFD Action Penalty R[2] *)
    vecR_weight[3] := 0.35;  (* Air Ring Flow Valve Action Penalty R[3] *)
    vecR_weight[4] := 0.60;  (* Extruder Master Screw Speed Penalty R[4] *)
    vecR_weight[5] := 0.50;  (* Haul-Off Line Speed Action Penalty R[5] *)

    vecR_rate_weight[0] := 1.20; (* Air Ring Global Power Slew Penalty R_rate[0] *)
    vecR_rate_weight[1] := 0.85; (* IBC Supply Blower Slew Penalty R_rate[1] *)
    vecR_rate_weight[2] := 0.85; (* IBC Exhaust Blower Slew Penalty R_rate[2] *)
    vecR_rate_weight[3] := 1.10; (* Air Ring Valve Slew Penalty R_rate[3] *)
    vecR_rate_weight[4] := 1.50; (* Extruder Screw Slew Penalty R_rate[4] *)
    vecR_rate_weight[5] := 1.30; (* Haul-Off Line Speed Slew Penalty R_rate[5] *)

    vecP_terminal[0] := 25.00; (* Terminal State Stability Matrix Diagonal P[0] *)
    vecP_terminal[1] := 35.00; (* Terminal State Stability Matrix Diagonal P[1] *)
    vecP_terminal[2] := 15.00; (* Terminal State Stability Matrix Diagonal P[2] *)
    vecP_terminal[3] := 20.00; (* Terminal State Stability Matrix Diagonal P[3] *)
    vecP_terminal[4] := 12.00; (* Terminal State Stability Matrix Diagonal P[4] *)
    vecP_terminal[5] := 18.00; (* Terminal State Stability Matrix Diagonal P[5] *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0G: Physical Actuator Box Saturation Limits & Maximum Allowable Slew Rates                  *)
    (* ------------------------------------------------------------------------------------------------ *)
    vecU_min[0] := 10.0; vecU_max[0] := 90.0; vecU_slew_max[0] := 1.5;   (* Air Ring Global Bolt Power [%] *)
    vecU_min[1] := 500.0; vecU_max[1] := 2850.0; vecU_slew_max[1] := 60.0; (* IBC Supply Blower [RPM] *)
    vecU_min[2] := 500.0; vecU_max[2] := 2850.0; vecU_slew_max[2] := 60.0; (* IBC Exhaust Blower [RPM] *)
    vecU_min[3] := 15.0; vecU_max[3] := 98.0; vecU_slew_max[3] := 2.5;   (* Air Ring Flow Valve [%] *)
    vecU_min[4] := 10.0; vecU_max[4] := 115.0; vecU_slew_max[4] := 1.2;  (* Master Extruder Speed [RPM] *)
    vecU_min[5] := 15.0; vecU_max[5] := 165.0; vecU_slew_max[5] := 2.5;  (* Haul-Off Line Speed [m/min] *)

    (* Seed Nominal Operating Vector Targets *)
    vecU_target[0] := 50.0;
    vecU_target[1] := 1850.0;
    vecU_target[2] := 1820.0;
    vecU_target[3] := 65.0;
    vecU_target[4] := 68.0;
    vecU_target[5] := 150.0;

    FOR mIdx := 0 TO 5 DO
        vecU[mIdx] := vecU_target[mIdx];
        vecU_prev[mIdx] := vecU_target[mIdx];
        vecU_rate[mIdx] := 0.0;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0H: Gaussian Spatial Influence Expansion Kernel for 128 Thermal Expansion Bolts             *)
    (* Sigma = 1.8 Zones: Models Lateral Heat Conduction Across Adjacent Segmented Orifice Slots        *)
    (* ------------------------------------------------------------------------------------------------ *)
    arrGaussianKernel[0] := 1.0000; (* Center Zone Peak Expansion Coefficient *)
    arrGaussianKernel[1] := 0.8570; (* Neighbor Zone +/- 1 Expansion Coefficient *)
    arrGaussianKernel[2] := 0.5380; (* Neighbor Zone +/- 2 Expansion Coefficient *)
    arrGaussianKernel[3] := 0.2480; (* Neighbor Zone +/- 3 Expansion Coefficient *)
    arrGaussianKernel[4] := 0.0830; (* Neighbor Zone +/- 4 Expansion Coefficient *)
    arrGaussianKernel[5] := 0.0200; (* Neighbor Zone +/- 5 Expansion Coefficient *)
    arrGaussianKernel[6] := 0.0035; (* Neighbor Zone +/- 6 Expansion Coefficient *)
    arrGaussianKernel[7] := 0.0004; (* Neighbor Zone +/- 7 Expansion Coefficient *)
    FOR kKernel := 8 TO 16 DO
        arrGaussianKernel[kKernel] := 0.0000;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Step 0I: Initialize 128-Zone Segmented Dual-Lip Air Ring Thermal Expansion Heaters              *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR zIdx := 0 TO 127 DO
        arrAirRing_ThermalBoltPower_pct[zIdx] := 50.0;
        arrBoltThermalPower_Target[zIdx] := 50.0;
        arrBoltThermalPower_Prev[zIdx] := 50.0;
        arrBoltHeaterCurrent_A[zIdx] := 2.15;
        arrBoltZoneHealthy[zIdx] := TRUE;
        arrFilteredProfile_um[zIdx] := 60.0;
        arrThicknessError_um[zIdx] := 0.0;
        arrMappedBoltError_um[zIdx] := 0.0;
    END_FOR;

    bFirstScanDone := TRUE;
END_IF;

(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE WITH DISCREPANCY TIMERS           *)
(* Fail-Operational / Bumpless Degradation Across Critical Co-Extrusion Measurement Transducers         *)
(* ==================================================================================================== *)

    (* -------------------------------------------------------------------------------------------- *)
    (* Channel Group 1: IBC Ultrasonic Bubble Diameter Transducers (IBC_Transducer_1A/B/C) [mm]    *)
    (* Persistence Discrepancy Threshold = 35.0 [mm], Persistence Trip Window = 350.0 [ms]          *)
    (* -------------------------------------------------------------------------------------------- *)
    IF ABS(rIBC_Transducer_1A_mm - rIBC_Transducer_1B_mm) > 35.0 THEN
        rIBC_Disc_AB_ms := rIBC_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
    ELSE
        rIBC_Disc_AB_ms := MAX(0.0, rIBC_Disc_AB_ms - (tScanCycleTime_s * 500.0));
    END_IF;

    IF ABS(rIBC_Transducer_1B_mm - rIBC_Transducer_1C_mm) > 35.0 THEN
        rIBC_Disc_BC_ms := rIBC_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
    ELSE
        rIBC_Disc_BC_ms := MAX(0.0, rIBC_Disc_BC_ms - (tScanCycleTime_s * 500.0));
    END_IF;

    IF ABS(rIBC_Transducer_1C_mm - rIBC_Transducer_1A_mm) > 35.0 THEN
        rIBC_Disc_CA_ms := rIBC_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
    ELSE
        rIBC_Disc_CA_ms := MAX(0.0, rIBC_Disc_CA_ms - (tScanCycleTime_s * 500.0));
    END_IF;

    (* Determine Channel Group 1 Individual Health Statuses *)
    bIBC_HealthA := (rIBC_Disc_AB_ms < 350.0) OR (rIBC_Disc_CA_ms < 350.0);
    bIBC_HealthB := (rIBC_Disc_AB_ms < 350.0) OR (rIBC_Disc_BC_ms < 350.0);
    bIBC_HealthC := (rIBC_Disc_BC_ms < 350.0) OR (rIBC_Disc_CA_ms < 350.0);

    (* Execute Bumpless Voting Hierarchy: 3-Healthy Median -> 2-Healthy Average -> 1-Healthy Fallback *)
    IF bIBC_HealthA AND bIBC_HealthB AND bIBC_HealthC THEN
        (* Full 3-Channel Triple Modular Redundancy Median Voting *)
        IF (rIBC_Transducer_1A_mm >= rIBC_Transducer_1B_mm AND rIBC_Transducer_1A_mm <= rIBC_Transducer_1C_mm) OR
           (rIBC_Transducer_1A_mm >= rIBC_Transducer_1C_mm AND rIBC_Transducer_1A_mm <= rIBC_Transducer_1B_mm) THEN
            rIBC_Diameter_Voted := rIBC_Transducer_1A_mm;
        ELSIF (rIBC_Transducer_1B_mm >= rIBC_Transducer_1A_mm AND rIBC_Transducer_1B_mm <= rIBC_Transducer_1C_mm) OR
              (rIBC_Transducer_1B_mm >= rIBC_Transducer_1C_mm AND rIBC_Transducer_1B_mm <= rIBC_Transducer_1A_mm) THEN
            rIBC_Diameter_Voted := rIBC_Transducer_1B_mm;
        ELSE
            rIBC_Diameter_Voted := rIBC_Transducer_1C_mm;
        END_IF;
        bIBC_Degraded := FALSE;
        bIBC_SingleFallback := FALSE;
        bIBC_Trip := FALSE;
    ELSIF bIBC_HealthA AND bIBC_HealthB THEN
        (* Dual-Channel Average Degradation *)
        rIBC_Diameter_Voted := 0.5 * (rIBC_Transducer_1A_mm + rIBC_Transducer_1B_mm);
        bIBC_Degraded := TRUE;
        bIBC_SingleFallback := FALSE;
        bIBC_Trip := FALSE;
    ELSIF bIBC_HealthB AND bIBC_HealthC THEN
        rIBC_Diameter_Voted := 0.5 * (rIBC_Transducer_1B_mm + rIBC_Transducer_1C_mm);
        bIBC_Degraded := TRUE;
        bIBC_SingleFallback := FALSE;
        bIBC_Trip := FALSE;
    ELSIF bIBC_HealthC AND bIBC_HealthA THEN
        rIBC_Diameter_Voted := 0.5 * (rIBC_Transducer_1C_mm + rIBC_Transducer_1A_mm);
        bIBC_Degraded := TRUE;
        bIBC_SingleFallback := FALSE;
        bIBC_Trip := FALSE;
    ELSIF bIBC_HealthA THEN
        (* Single Channel Fallback *)
        rIBC_Diameter_Voted := rIBC_Transducer_1A_mm;
        bIBC_Degraded := TRUE;
        bIBC_SingleFallback := TRUE;
        bIBC_Trip := FALSE;
    ELSIF bIBC_HealthB THEN
        rIBC_Diameter_Voted := rIBC_Transducer_1B_mm;
        bIBC_Degraded := TRUE;
        bIBC_SingleFallback := TRUE;
        bIBC_Trip := FALSE;
    ELSIF bIBC_HealthC THEN
        rIBC_Diameter_Voted := rIBC_Transducer_1C_mm;
        bIBC_Degraded := TRUE;
        bIBC_SingleFallback := TRUE;
        bIBC_Trip := FALSE;
    ELSE
        (* Total Channel Group 1 Failure Trip *)
        bIBC_Degraded := TRUE;
        bIBC_SingleFallback := FALSE;
        bIBC_Trip := TRUE;
    END_IF;

    (* -------------------------------------------------------------------------------------------- *)
    (* Channel Group 2: Frost-Line Optical Infrared Camera Height Sensors (FLH_Camera_2A/B/C) [mm]  *)
    (* Persistence Discrepancy Threshold = 60.0 [mm], Persistence Trip Window = 350.0 [ms]          *)
    (* -------------------------------------------------------------------------------------------- *)
    IF ABS(rFLH_Camera_2A_mm - rFLH_Camera_2B_mm) > 60.0 THEN
        rFLH_Disc_AB_ms := rFLH_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
    ELSE
        rFLH_Disc_AB_ms := MAX(0.0, rFLH_Disc_AB_ms - (tScanCycleTime_s * 500.0));
    END_IF;

    IF ABS(rFLH_Camera_2B_mm - rFLH_Camera_2C_mm) > 60.0 THEN
        rFLH_Disc_BC_ms := rFLH_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
    ELSE
        rFLH_Disc_BC_ms := MAX(0.0, rFLH_Disc_BC_ms - (tScanCycleTime_s * 500.0));
    END_IF;

    IF ABS(rFLH_Camera_2C_mm - rFLH_Camera_2A_mm) > 60.0 THEN
        rFLH_Disc_CA_ms := rFLH_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
    ELSE
        rFLH_Disc_CA_ms := MAX(0.0, rFLH_Disc_CA_ms - (tScanCycleTime_s * 500.0));
    END_IF;

    (* Determine Channel Group 2 Individual Health Statuses *)
    bFLH_HealthA := (rFLH_Disc_AB_ms < 350.0) OR (rFLH_Disc_CA_ms < 350.0);
    bFLH_HealthB := (rFLH_Disc_AB_ms < 350.0) OR (rFLH_Disc_BC_ms < 350.0);
    bFLH_HealthC := (rFLH_Disc_BC_ms < 350.0) OR (rFLH_Disc_CA_ms < 350.0);

    IF bFLH_HealthA AND bFLH_HealthB AND bFLH_HealthC THEN
        IF (rFLH_Camera_2A_mm >= rFLH_Camera_2B_mm AND rFLH_Camera_2A_mm <= rFLH_Camera_2C_mm) OR
           (rFLH_Camera_2A_mm >= rFLH_Camera_2C_mm AND rFLH_Camera_2A_mm <= rFLH_Camera_2B_mm) THEN
            rFLH_Height_Voted := rFLH_Camera_2A_mm;
        ELSIF (rFLH_Camera_2B_mm >= rFLH_Camera_2A_mm AND rFLH_Camera_2B_mm <= rFLH_Camera_2C_mm) OR
              (rFLH_Camera_2B_mm >= rFLH_Camera_2C_mm AND rFLH_Camera_2B_mm <= rFLH_Camera_2A_mm) THEN
            rFLH_Height_Voted := rFLH_Camera_2B_mm;
        ELSE
            rFLH_Height_Voted := rFLH_Camera_2C_mm;
        END_IF;
        bFLH_Degraded := FALSE;
        bFLH_SingleFallback := FALSE;
        bFLH_Trip := FALSE;
    ELSIF bFLH_HealthA AND bFLH_HealthB THEN
        rFLH_Height_Voted := 0.5 * (rFLH_Camera_2A_mm + rFLH_Camera_2B_mm);
        bFLH_Degraded := TRUE;
        bFLH_SingleFallback := FALSE;
        bFLH_Trip := FALSE;
    ELSIF bFLH_HealthB AND bFLH_HealthC THEN
        rFLH_Height_Voted := 0.5 * (rFLH_Camera_2B_mm + rFLH_Camera_2C_mm);
        bFLH_Degraded := TRUE;
        bFLH_SingleFallback := FALSE;
        bFLH_Trip := FALSE;
    ELSIF bFLH_HealthC AND bFLH_HealthA THEN
        rFLH_Height_Voted := 0.5 * (rFLH_Camera_2C_mm + rFLH_Camera_2A_mm);
        bFLH_Degraded := TRUE;
        bFLH_SingleFallback := FALSE;
        bFLH_Trip := FALSE;
    ELSIF bFLH_HealthA THEN
        rFLH_Height_Voted := rFLH_Camera_2A_mm;
        bFLH_Degraded := TRUE;
        bFLH_SingleFallback := TRUE;
        bFLH_Trip := FALSE;
    ELSIF bFLH_HealthB THEN
        rFLH_Height_Voted := rFLH_Camera_2B_mm;
        bFLH_Degraded := TRUE;
        bFLH_SingleFallback := TRUE;
        bFLH_Trip := FALSE;
    ELSIF bFLH_HealthC THEN
        rFLH_Height_Voted := rFLH_Camera_2C_mm;
        bFLH_Degraded := TRUE;
        bFLH_SingleFallback := TRUE;
        bFLH_Trip := FALSE;
    ELSE
        bFLH_Degraded := TRUE;
        bFLH_SingleFallback := FALSE;
        bFLH_Trip := TRUE;
    END_IF;

    (* -------------------------------------------------------------------------------------------- *)
    (* Channel Group 3: Co-Extrusion Die Exit Total Melt Pressure (MeltPress_Die_3A/B/C) [bar]     *)
    (* Persistence Discrepancy Threshold = 18.0 [bar], Persistence Trip Window = 300.0 [ms]         *)
    (* -------------------------------------------------------------------------------------------- *)
    IF ABS(rMeltPress_Die_3A_bar - rMeltPress_Die_3B_bar) > 18.0 THEN
        rMeltPress_Disc_AB_ms := rMeltPress_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
    ELSE
        rMeltPress_Disc_AB_ms := MAX(0.0, rMeltPress_Disc_AB_ms - (tScanCycleTime_s * 500.0));
    END_IF;

    IF ABS(rMeltPress_Die_3B_bar - rMeltPress_Die_3C_bar) > 18.0 THEN
        rMeltPress_Disc_BC_ms := rMeltPress_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
    ELSE
        rMeltPress_Disc_BC_ms := MAX(0.0, rMeltPress_Disc_BC_ms - (tScanCycleTime_s * 500.0));
    END_IF;

    IF ABS(rMeltPress_Die_3C_bar - rMeltPress_Die_3A_bar) > 18.0 THEN
        rMeltPress_Disc_CA_ms := rMeltPress_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
    ELSE
        rMeltPress_Disc_CA_ms := MAX(0.0, rMeltPress_Disc_CA_ms - (tScanCycleTime_s * 500.0));
    END_IF;

    bMeltPress_HealthA := (rMeltPress_Disc_AB_ms < 300.0) OR (rMeltPress_Disc_CA_ms < 300.0);
    bMeltPress_HealthB := (rMeltPress_Disc_AB_ms < 300.0) OR (rMeltPress_Disc_BC_ms < 300.0);
    bMeltPress_HealthC := (rMeltPress_Disc_BC_ms < 300.0) OR (rMeltPress_Disc_CA_ms < 300.0);

    IF bMeltPress_HealthA AND bMeltPress_HealthB AND bMeltPress_HealthC THEN
        IF (rMeltPress_Die_3A_bar >= rMeltPress_Die_3B_bar AND rMeltPress_Die_3A_bar <= rMeltPress_Die_3C_bar) OR
           (rMeltPress_Die_3A_bar >= rMeltPress_Die_3C_bar AND rMeltPress_Die_3A_bar <= rMeltPress_Die_3B_bar) THEN
            rMeltPress_Die_Voted := rMeltPress_Die_3A_bar;
        ELSIF (rMeltPress_Die_3B_bar >= rMeltPress_Die_3A_bar AND rMeltPress_Die_3B_bar <= rMeltPress_Die_3C_bar) OR
              (rMeltPress_Die_3B_bar >= rMeltPress_Die_3C_bar AND rMeltPress_Die_3B_bar <= rMeltPress_Die_3A_bar) THEN
            rMeltPress_Die_Voted := rMeltPress_Die_3B_bar;
        ELSE
            rMeltPress_Die_Voted := rMeltPress_Die_3C_bar;
        END_IF;
        bMeltPress_Degraded := FALSE;
        bMeltPress_SingleFallback := FALSE;
        bMeltPress_Trip := FALSE;
    ELSIF bMeltPress_HealthA AND bMeltPress_HealthB THEN
        rMeltPress_Die_Voted := 0.5 * (rMeltPress_Die_3A_bar + rMeltPress_Die_3B_bar);
        bMeltPress_Degraded := TRUE;
        bMeltPress_SingleFallback := FALSE;
        bMeltPress_Trip := FALSE;
    ELSIF bMeltPress_HealthB AND bMeltPress_HealthC THEN
        rMeltPress_Die_Voted := 0.5 * (rMeltPress_Die_3B_bar + rMeltPress_Die_3C_bar);
        bMeltPress_Degraded := TRUE;
        bMeltPress_SingleFallback := FALSE;
        bMeltPress_Trip := FALSE;
    ELSIF bMeltPress_HealthC AND bMeltPress_HealthA THEN
        rMeltPress_Die_Voted := 0.5 * (rMeltPress_Die_3C_bar + rMeltPress_Die_3A_bar);
        bMeltPress_Degraded := TRUE;
        bMeltPress_SingleFallback := FALSE;
        bMeltPress_Trip := FALSE;
    ELSIF bMeltPress_HealthA THEN
        rMeltPress_Die_Voted := rMeltPress_Die_3A_bar;
        bMeltPress_Degraded := TRUE;
        bMeltPress_SingleFallback := TRUE;
        bMeltPress_Trip := FALSE;
    ELSIF bMeltPress_HealthB THEN
        rMeltPress_Die_Voted := rMeltPress_Die_3B_bar;
        bMeltPress_Degraded := TRUE;
        bMeltPress_SingleFallback := TRUE;
        bMeltPress_Trip := FALSE;
    ELSIF bMeltPress_HealthC THEN
        rMeltPress_Die_Voted := rMeltPress_Die_3C_bar;
        bMeltPress_Degraded := TRUE;
        bMeltPress_SingleFallback := TRUE;
        bMeltPress_Trip := FALSE;
    ELSE
        bMeltPress_Degraded := TRUE;
        bMeltPress_SingleFallback := FALSE;
        bMeltPress_Trip := TRUE;
    END_IF;

    (* -------------------------------------------------------------------------------------------- *)
    (* Channel Group 4: Oscillating Haul-Off Web Tension Load Cells (WebTension_4A/B/C) [N]        *)
    (* Persistence Discrepancy Threshold = 35.0 [N], Persistence Trip Window = 400.0 [ms]          *)
    (* -------------------------------------------------------------------------------------------- *)
    IF ABS(rWebTension_HaulOff_4A_N - rWebTension_HaulOff_4B_N) > 35.0 THEN
        rWebTension_Disc_AB_ms := rWebTension_Disc_AB_ms + (tScanCycleTime_s * 1000.0);
    ELSE
        rWebTension_Disc_AB_ms := MAX(0.0, rWebTension_Disc_AB_ms - (tScanCycleTime_s * 500.0));
    END_IF;

    IF ABS(rWebTension_HaulOff_4B_N - rWebTension_HaulOff_4C_N) > 35.0 THEN
        rWebTension_Disc_BC_ms := rWebTension_Disc_BC_ms + (tScanCycleTime_s * 1000.0);
    ELSE
        rWebTension_Disc_BC_ms := MAX(0.0, rWebTension_Disc_BC_ms - (tScanCycleTime_s * 500.0));
    END_IF;

    IF ABS(rWebTension_HaulOff_4C_N - rWebTension_HaulOff_4A_N) > 35.0 THEN
        rWebTension_Disc_CA_ms := rWebTension_Disc_CA_ms + (tScanCycleTime_s * 1000.0);
    ELSE
        rWebTension_Disc_CA_ms := MAX(0.0, rWebTension_Disc_CA_ms - (tScanCycleTime_s * 500.0));
    END_IF;

    bWebTension_HealthA := (rWebTension_Disc_AB_ms < 400.0) OR (rWebTension_Disc_CA_ms < 400.0);
    bWebTension_HealthB := (rWebTension_Disc_AB_ms < 400.0) OR (rWebTension_Disc_BC_ms < 400.0);
    bWebTension_HealthC := (rWebTension_Disc_BC_ms < 400.0) OR (rWebTension_Disc_CA_ms < 400.0);

    IF bWebTension_HealthA AND bWebTension_HealthB AND bWebTension_HealthC THEN
        IF (rWebTension_HaulOff_4A_N >= rWebTension_HaulOff_4B_N AND rWebTension_HaulOff_4A_N <= rWebTension_HaulOff_4C_N) OR
           (rWebTension_HaulOff_4A_N >= rWebTension_HaulOff_4C_N AND rWebTension_HaulOff_4A_N <= rWebTension_HaulOff_4B_N) THEN
            rWebTension_HaulOff_Voted := rWebTension_HaulOff_4A_N;
        ELSIF (rWebTension_HaulOff_4B_N >= rWebTension_HaulOff_4A_N AND rWebTension_HaulOff_4B_N <= rWebTension_HaulOff_4C_N) OR
              (rWebTension_HaulOff_4B_N >= rWebTension_HaulOff_4C_N AND rWebTension_HaulOff_4B_N <= rWebTension_HaulOff_4A_N) THEN
            rWebTension_HaulOff_Voted := rWebTension_HaulOff_4B_N;
        ELSE
            rWebTension_HaulOff_Voted := rWebTension_HaulOff_4C_N;
        END_IF;
        bWebTension_Degraded := FALSE;
        bWebTension_SingleFallback := FALSE;
        bWebTension_Trip := FALSE;
    ELSIF bWebTension_HealthA AND bWebTension_HealthB THEN
        rWebTension_HaulOff_Voted := 0.5 * (rWebTension_HaulOff_4A_N + rWebTension_HaulOff_4B_N);
        bWebTension_Degraded := TRUE;
        bWebTension_SingleFallback := FALSE;
        bWebTension_Trip := FALSE;
    ELSIF bWebTension_HealthB AND bWebTension_HealthC THEN
        rWebTension_HaulOff_Voted := 0.5 * (rWebTension_HaulOff_4B_N + rWebTension_HaulOff_4C_N);
        bWebTension_Degraded := TRUE;
        bWebTension_SingleFallback := FALSE;
        bWebTension_Trip := FALSE;
    ELSIF bWebTension_HealthC AND bWebTension_HealthA THEN
        rWebTension_HaulOff_Voted := 0.5 * (rWebTension_HaulOff_4C_N + rWebTension_HaulOff_4A_N);
        bWebTension_Degraded := TRUE;
        bWebTension_SingleFallback := FALSE;
        bWebTension_Trip := FALSE;
    ELSIF bWebTension_HealthA THEN
        rWebTension_HaulOff_Voted := rWebTension_HaulOff_4A_N;
        bWebTension_Degraded := TRUE;
        bWebTension_SingleFallback := TRUE;
        bWebTension_Trip := FALSE;
    ELSIF bWebTension_HealthB THEN
        rWebTension_HaulOff_Voted := rWebTension_HaulOff_4B_N;
        bWebTension_Degraded := TRUE;
        bWebTension_SingleFallback := TRUE;
        bWebTension_Trip := FALSE;
    ELSIF bWebTension_HealthC THEN
        rWebTension_HaulOff_Voted := rWebTension_HaulOff_4C_N;
        bWebTension_Degraded := TRUE;
        bWebTension_SingleFallback := TRUE;
        bWebTension_Trip := FALSE;
    ELSE
        bWebTension_Degraded := TRUE;
        bWebTension_SingleFallback := FALSE;
        bWebTension_Trip := TRUE;
    END_IF;

    (* Aggregated TMR Sensor Channel Supervisory Diagnostics *)
    bDegradedSensorMode := bIBC_Degraded OR bFLH_Degraded OR bMeltPress_Degraded OR bWebTension_Degraded;
    bCriticalTrip := bIBC_Trip OR bFLH_Trip OR bMeltPress_Trip OR bWebTension_Trip;
"""
