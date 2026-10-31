# gen_phase1.py - Generates Phase 1: 2oo3 TMR Sensor Voting

def generate_phase1():
    return """(* ==================================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY ARBITRATION                              *)
(* ==================================================================================================================== *)

(* --- 1.1: Shelf Silicone Oil Average Temperature 2oo3 TMR Voting --- *)
(* Combine Inlet and Outlet for each channel to evaluate overall shelf heat transfer performance *)
rTMR_Shelf_Diff_AB := ABS((0.5 * (rShelfTempInlet_ChA + rShelfTempOutlet_ChA)) - (0.5 * (rShelfTempInlet_ChB + rShelfTempOutlet_ChB)));
rTMR_Shelf_Diff_BC := ABS((0.5 * (rShelfTempInlet_ChB + rShelfTempOutlet_ChB)) - (0.5 * (rShelfTempInlet_ChC + rShelfTempOutlet_ChC)));
rTMR_Shelf_Diff_CA := ABS((0.5 * (rShelfTempInlet_ChC + rShelfTempOutlet_ChC)) - (0.5 * (rShelfTempInlet_ChA + rShelfTempOutlet_ChA)));

(* Channel A Discrepancy Persistence Evaluation (Tolerance > 1.2 deg C for 2.5 seconds) *)
IF (rTMR_Shelf_Diff_AB > 1.20) AND (rTMR_Shelf_Diff_CA > 1.20) THEN
    rTMR_Shelf_Timer_A := rTMR_Shelf_Timer_A + rCycleScanDeltaTime;
    IF rTMR_Shelf_Timer_A >= 2.50 THEN
        bTMR_Shelf_Fault_A := TRUE;
    END_IF;
ELSE
    rTMR_Shelf_Timer_A := 0.0;
END_IF;

(* Channel B Discrepancy Persistence Evaluation *)
IF (rTMR_Shelf_Diff_AB > 1.20) AND (rTMR_Shelf_Diff_BC > 1.20) THEN
    rTMR_Shelf_Timer_B := rTMR_Shelf_Timer_B + rCycleScanDeltaTime;
    IF rTMR_Shelf_Timer_B >= 2.50 THEN
        bTMR_Shelf_Fault_B := TRUE;
    END_IF;
ELSE
    rTMR_Shelf_Timer_B := 0.0;
END_IF;

(* Channel C Discrepancy Persistence Evaluation *)
IF (rTMR_Shelf_Diff_BC > 1.20) AND (rTMR_Shelf_Diff_CA > 1.20) THEN
    rTMR_Shelf_Timer_C := rTMR_Shelf_Timer_C + rCycleScanDeltaTime;
    IF rTMR_Shelf_Timer_C >= 2.50 THEN
        bTMR_Shelf_Fault_C := TRUE;
    END_IF;
ELSE
    rTMR_Shelf_Timer_C := 0.0;
END_IF;

(* Shelf Temperature Voting Synthesis *)
IF (NOT bTMR_Shelf_Fault_A) AND (NOT bTMR_Shelf_Fault_B) AND (NOT bTMR_Shelf_Fault_C) THEN
    (* All 3 channels healthy: Median selection *)
    IF (((0.5 * (rShelfTempInlet_ChA + rShelfTempOutlet_ChA)) >= (0.5 * (rShelfTempInlet_ChB + rShelfTempOutlet_ChB))) AND
        ((0.5 * (rShelfTempInlet_ChA + rShelfTempOutlet_ChA)) <= (0.5 * (rShelfTempInlet_ChC + rShelfTempOutlet_ChC)))) OR
       (((0.5 * (rShelfTempInlet_ChA + rShelfTempOutlet_ChA)) <= (0.5 * (rShelfTempInlet_ChB + rShelfTempOutlet_ChB))) AND
        ((0.5 * (rShelfTempInlet_ChA + rShelfTempOutlet_ChA)) >= (0.5 * (rShelfTempInlet_ChC + rShelfTempOutlet_ChC)))) THEN
        rVotedShelfTemperatureActual := 0.5 * (rShelfTempInlet_ChA + rShelfTempOutlet_ChA);
    ELSIF (((0.5 * (rShelfTempInlet_ChB + rShelfTempOutlet_ChB)) >= (0.5 * (rShelfTempInlet_ChA + rShelfTempOutlet_ChA))) AND
           ((0.5 * (rShelfTempInlet_ChB + rShelfTempOutlet_ChB)) <= (0.5 * (rShelfTempInlet_ChC + rShelfTempOutlet_ChC)))) OR
          (((0.5 * (rShelfTempInlet_ChB + rShelfTempOutlet_ChB)) <= (0.5 * (rShelfTempInlet_ChA + rShelfTempOutlet_ChA))) AND
           ((0.5 * (rShelfTempInlet_ChB + rShelfTempOutlet_ChB)) >= (0.5 * (rShelfTempInlet_ChC + rShelfTempOutlet_ChC)))) THEN
        rVotedShelfTemperatureActual := 0.5 * (rShelfTempInlet_ChB + rShelfTempOutlet_ChB);
    ELSE
        rVotedShelfTemperatureActual := 0.5 * (rShelfTempInlet_ChC + rShelfTempOutlet_ChC);
    END_IF;
ELSIF bTMR_Shelf_Fault_A AND (NOT bTMR_Shelf_Fault_B) AND (NOT bTMR_Shelf_Fault_C) THEN
    rVotedShelfTemperatureActual := 0.25 * (rShelfTempInlet_ChB + rShelfTempOutlet_ChB + rShelfTempInlet_ChC + rShelfTempOutlet_ChC);
ELSIF bTMR_Shelf_Fault_B AND (NOT bTMR_Shelf_Fault_A) AND (NOT bTMR_Shelf_Fault_C) THEN
    rVotedShelfTemperatureActual := 0.25 * (rShelfTempInlet_ChA + rShelfTempOutlet_ChA + rShelfTempInlet_ChC + rShelfTempOutlet_ChC);
ELSIF bTMR_Shelf_Fault_C AND (NOT bTMR_Shelf_Fault_A) AND (NOT bTMR_Shelf_Fault_B) THEN
    rVotedShelfTemperatureActual := 0.25 * (rShelfTempInlet_ChA + rShelfTempOutlet_ChA + rShelfTempInlet_ChB + rShelfTempOutlet_ChB);
ELSE
    bAlarm_SensorTMR_Discrepancy_H := TRUE;
    rVotedShelfTemperatureActual := 0.5 * (rShelfTempInlet_ChA + rShelfTempOutlet_ChA);
END_IF;

(* --- 1.2: Product Vial Thermocouple Clusters 2oo3 TMR Voting --- *)
rTMR_Prod_Diff_AB := ABS(rProductVialTemp_ChA - rProductVialTemp_ChB);
rTMR_Prod_Diff_BC := ABS(rProductVialTemp_ChB - rProductVialTemp_ChC);
rTMR_Prod_Diff_CA := ABS(rProductVialTemp_ChC - rProductVialTemp_ChA);

IF (rTMR_Prod_Diff_AB > 2.00) AND (rTMR_Prod_Diff_CA > 2.00) THEN
    rTMR_Prod_Timer_A := rTMR_Prod_Timer_A + rCycleScanDeltaTime;
    IF rTMR_Prod_Timer_A >= 3.00 THEN
        bTMR_Prod_Fault_A := TRUE;
    END_IF;
ELSE
    rTMR_Prod_Timer_A := 0.0;
END_IF;

IF (rTMR_Prod_Diff_AB > 2.00) AND (rTMR_Prod_Diff_BC > 2.00) THEN
    rTMR_Prod_Timer_B := rTMR_Prod_Timer_B + rCycleScanDeltaTime;
    IF rTMR_Prod_Timer_B >= 3.00 THEN
        bTMR_Prod_Fault_B := TRUE;
    END_IF;
ELSE
    rTMR_Prod_Timer_B := 0.0;
END_IF;

IF (rTMR_Prod_Diff_BC > 2.00) AND (rTMR_Prod_Diff_CA > 2.00) THEN
    rTMR_Prod_Timer_C := rTMR_Prod_Timer_C + rCycleScanDeltaTime;
    IF rTMR_Prod_Timer_C >= 3.00 THEN
        bTMR_Prod_Fault_C := TRUE;
    END_IF;
ELSE
    rTMR_Prod_Timer_C := 0.0;
END_IF;

IF (NOT bTMR_Prod_Fault_A) AND (NOT bTMR_Prod_Fault_B) AND (NOT bTMR_Prod_Fault_C) THEN
    (* Robust Maximum Selection during Sublimation: Always select highest reading to guarantee cake collapse protection *)
    IF (rProductVialTemp_ChA >= rProductVialTemp_ChB) AND (rProductVialTemp_ChA >= rProductVialTemp_ChC) THEN
        rVotedProductTemperatureActual := rProductVialTemp_ChA;
    ELSIF (rProductVialTemp_ChB >= rProductVialTemp_ChA) AND (rProductVialTemp_ChB >= rProductVialTemp_ChC) THEN
        rVotedProductTemperatureActual := rProductVialTemp_ChB;
    ELSE
        rVotedProductTemperatureActual := rProductVialTemp_ChC;
    END_IF;
ELSIF bTMR_Prod_Fault_A AND (NOT bTMR_Prod_Fault_B) AND (NOT bTMR_Prod_Fault_C) THEN
    IF rProductVialTemp_ChB >= rProductVialTemp_ChC THEN
        rVotedProductTemperatureActual := rProductVialTemp_ChB;
    ELSE
        rVotedProductTemperatureActual := rProductVialTemp_ChC;
    END_IF;
ELSIF bTMR_Prod_Fault_B AND (NOT bTMR_Prod_Fault_A) AND (NOT bTMR_Prod_Fault_C) THEN
    IF rProductVialTemp_ChA >= rProductVialTemp_ChC THEN
        rVotedProductTemperatureActual := rProductVialTemp_ChA;
    ELSE
        rVotedProductTemperatureActual := rProductVialTemp_ChC;
    END_IF;
ELSIF bTMR_Prod_Fault_C AND (NOT bTMR_Prod_Fault_A) AND (NOT bTMR_Prod_Fault_B) THEN
    IF rProductVialTemp_ChA >= rProductVialTemp_ChB THEN
        rVotedProductTemperatureActual := rProductVialTemp_ChA;
    ELSE
        rVotedProductTemperatureActual := rProductVialTemp_ChB;
    END_IF;
ELSE
    bAlarm_SensorTMR_Discrepancy_H := TRUE;
    rVotedProductTemperatureActual := rProductVialTemp_ChA;
END_IF;

(* --- 1.3: Heated Capacitance Manometer Absolute Vacuum Gauges 2oo3 TMR Voting --- *)
rTMR_CM_Diff_AB := ABS(rChamberPressure_CM_ChA - rChamberPressure_CM_ChB);
rTMR_CM_Diff_BC := ABS(rChamberPressure_CM_ChB - rChamberPressure_CM_ChC);
rTMR_CM_Diff_CA := ABS(rChamberPressure_CM_ChC - rChamberPressure_CM_ChA);

IF (rTMR_CM_Diff_AB > 0.015) AND (rTMR_CM_Diff_CA > 0.015) THEN
    rTMR_CM_Timer_A := rTMR_CM_Timer_A + rCycleScanDeltaTime;
    IF rTMR_CM_Timer_A >= 1.00 THEN
        bTMR_CM_Fault_A := TRUE;
    END_IF;
ELSE
    rTMR_CM_Timer_A := 0.0;
END_IF;

IF (rTMR_CM_Diff_AB > 0.015) AND (rTMR_CM_Diff_BC > 0.015) THEN
    rTMR_CM_Timer_B := rTMR_CM_Timer_B + rCycleScanDeltaTime;
    IF rTMR_CM_Timer_B >= 1.00 THEN
        bTMR_CM_Fault_B := TRUE;
    END_IF;
ELSE
    rTMR_CM_Timer_B := 0.0;
END_IF;

IF (rTMR_CM_Diff_BC > 0.015) AND (rTMR_CM_Diff_CA > 0.015) THEN
    rTMR_CM_Timer_C := rTMR_CM_Timer_C + rCycleScanDeltaTime;
    IF rTMR_CM_Timer_C >= 1.00 THEN
        bTMR_CM_Fault_C := TRUE;
    END_IF;
ELSE
    rTMR_CM_Timer_C := 0.0;
END_IF;

IF (NOT bTMR_CM_Fault_A) AND (NOT bTMR_CM_Fault_B) AND (NOT bTMR_CM_Fault_C) THEN
    IF ((rChamberPressure_CM_ChA >= rChamberPressure_CM_ChB) AND (rChamberPressure_CM_ChA <= rChamberPressure_CM_ChC)) OR
       ((rChamberPressure_CM_ChA <= rChamberPressure_CM_ChB) AND (rChamberPressure_CM_ChA >= rChamberPressure_CM_ChC)) THEN
        rVotedChamberPressure_CM_Actual := rChamberPressure_CM_ChA;
    ELSIF ((rChamberPressure_CM_ChB >= rChamberPressure_CM_ChA) AND (rChamberPressure_CM_ChB <= rChamberPressure_CM_ChC)) OR
          ((rChamberPressure_CM_ChB <= rChamberPressure_CM_ChA) AND (rChamberPressure_CM_ChB >= rChamberPressure_CM_ChC)) THEN
        rVotedChamberPressure_CM_Actual := rChamberPressure_CM_ChB;
    ELSE
        rVotedChamberPressure_CM_Actual := rChamberPressure_CM_ChC;
    END_IF;
ELSIF bTMR_CM_Fault_A AND (NOT bTMR_CM_Fault_B) AND (NOT bTMR_CM_Fault_C) THEN
    rVotedChamberPressure_CM_Actual := 0.5 * (rChamberPressure_CM_ChB + rChamberPressure_CM_ChC);
ELSIF bTMR_CM_Fault_B AND (NOT bTMR_CM_Fault_A) AND (NOT bTMR_CM_Fault_C) THEN
    rVotedChamberPressure_CM_Actual := 0.5 * (rChamberPressure_CM_ChA + rChamberPressure_CM_ChC);
ELSIF bTMR_CM_Fault_C AND (NOT bTMR_CM_Fault_A) AND (NOT bTMR_CM_Fault_B) THEN
    rVotedChamberPressure_CM_Actual := 0.5 * (rChamberPressure_CM_ChA + rChamberPressure_CM_ChB);
ELSE
    bAlarm_SensorTMR_Discrepancy_H := TRUE;
    rVotedChamberPressure_CM_Actual := rChamberPressure_CM_ChA;
END_IF;

(* --- 1.4: Pirani Thermal Conductivity Vacuum Gauges 2oo3 TMR Voting --- *)
rTMR_Pirani_Diff_AB := ABS(rChamberPressure_Pirani_ChA - rChamberPressure_Pirani_ChB);
rTMR_Pirani_Diff_BC := ABS(rChamberPressure_Pirani_ChB - rChamberPressure_Pirani_ChC);
rTMR_Pirani_Diff_CA := ABS(rChamberPressure_Pirani_ChC - rChamberPressure_Pirani_ChA);

IF (rTMR_Pirani_Diff_AB > 0.025) AND (rTMR_Pirani_Diff_CA > 0.025) THEN
    rTMR_Pirani_Timer_A := rTMR_Pirani_Timer_A + rCycleScanDeltaTime;
    IF rTMR_Pirani_Timer_A >= 1.50 THEN
        bTMR_Pirani_Fault_A := TRUE;
    END_IF;
ELSE
    rTMR_Pirani_Timer_A := 0.0;
END_IF;

IF (rTMR_Pirani_Diff_AB > 0.025) AND (rTMR_Pirani_Diff_BC > 0.025) THEN
    rTMR_Pirani_Timer_B := rTMR_Pirani_Timer_B + rCycleScanDeltaTime;
    IF rTMR_Pirani_Timer_B >= 1.50 THEN
        bTMR_Pirani_Fault_B := TRUE;
    END_IF;
ELSE
    rTMR_Pirani_Timer_B := 0.0;
END_IF;

IF (rTMR_Pirani_Diff_BC > 0.025) AND (rTMR_Pirani_Diff_CA > 0.025) THEN
    rTMR_Pirani_Timer_C := rTMR_Pirani_Timer_C + rCycleScanDeltaTime;
    IF rTMR_Pirani_Timer_C >= 1.50 THEN
        bTMR_Pirani_Fault_C := TRUE;
    END_IF;
ELSE
    rTMR_Pirani_Timer_C := 0.0;
END_IF;

IF (NOT bTMR_Pirani_Fault_A) AND (NOT bTMR_Pirani_Fault_B) AND (NOT bTMR_Pirani_Fault_C) THEN
    IF ((rChamberPressure_Pirani_ChA >= rChamberPressure_Pirani_ChB) AND (rChamberPressure_Pirani_ChA <= rChamberPressure_Pirani_ChC)) OR
       ((rChamberPressure_Pirani_ChA <= rChamberPressure_Pirani_ChB) AND (rChamberPressure_Pirani_ChA >= rChamberPressure_Pirani_ChC)) THEN
        rVotedChamberPressure_Pirani_Actual := rChamberPressure_Pirani_ChA;
    ELSIF ((rChamberPressure_Pirani_ChB >= rChamberPressure_Pirani_ChA) AND (rChamberPressure_Pirani_ChB <= rChamberPressure_Pirani_ChC)) OR
          ((rChamberPressure_Pirani_ChB <= rChamberPressure_Pirani_ChA) AND (rChamberPressure_Pirani_ChB >= rChamberPressure_Pirani_ChC)) THEN
        rVotedChamberPressure_Pirani_Actual := rChamberPressure_Pirani_ChB;
    ELSE
        rVotedChamberPressure_Pirani_Actual := rChamberPressure_Pirani_ChC;
    END_IF;
ELSIF bTMR_Pirani_Fault_A AND (NOT bTMR_Pirani_Fault_B) AND (NOT bTMR_Pirani_Fault_C) THEN
    rVotedChamberPressure_Pirani_Actual := 0.5 * (rChamberPressure_Pirani_ChB + rChamberPressure_Pirani_ChC);
ELSIF bTMR_Pirani_Fault_B AND (NOT bTMR_Pirani_Fault_A) AND (NOT bTMR_Pirani_Fault_C) THEN
    rVotedChamberPressure_Pirani_Actual := 0.5 * (rChamberPressure_Pirani_ChA + rChamberPressure_Pirani_ChC);
ELSIF bTMR_Pirani_Fault_C AND (NOT bTMR_Pirani_Fault_A) AND (NOT bTMR_Pirani_Fault_B) THEN
    rVotedChamberPressure_Pirani_Actual := 0.5 * (rChamberPressure_Pirani_ChA + rChamberPressure_Pirani_ChB);
ELSE
    bAlarm_SensorTMR_Discrepancy_H := TRUE;
    rVotedChamberPressure_Pirani_Actual := rChamberPressure_Pirani_ChA;
END_IF;

(* --- 1.5: Ice Condenser Refrigeration Surface RTDs 2oo3 TMR Voting --- *)
rTMR_Cond_Diff_AB := ABS(rCondenserCoilTemp_ChA - rCondenserCoilTemp_ChB);
rTMR_Cond_Diff_BC := ABS(rCondenserCoilTemp_ChB - rCondenserCoilTemp_ChC);
rTMR_Cond_Diff_CA := ABS(rCondenserCoilTemp_ChC - rCondenserCoilTemp_ChA);

IF (rTMR_Cond_Diff_AB > 3.00) AND (rTMR_Cond_Diff_CA > 3.00) THEN
    rTMR_Cond_Timer_A := rTMR_Cond_Timer_A + rCycleScanDeltaTime;
    IF rTMR_Cond_Timer_A >= 2.00 THEN
        bTMR_Cond_Fault_A := TRUE;
    END_IF;
ELSE
    rTMR_Cond_Timer_A := 0.0;
END_IF;

IF (rTMR_Cond_Diff_AB > 3.00) AND (rTMR_Cond_Diff_BC > 3.00) THEN
    rTMR_Cond_Timer_B := rTMR_Cond_Timer_B + rCycleScanDeltaTime;
    IF rTMR_Cond_Timer_B >= 2.00 THEN
        bTMR_Cond_Fault_B := TRUE;
    END_IF;
ELSE
    rTMR_Cond_Timer_B := 0.0;
END_IF;

IF (rTMR_Cond_Diff_BC > 3.00) AND (rTMR_Cond_Diff_CA > 3.00) THEN
    rTMR_Cond_Timer_C := rTMR_Cond_Timer_C + rCycleScanDeltaTime;
    IF rTMR_Cond_Timer_C >= 2.00 THEN
        bTMR_Cond_Fault_C := TRUE;
    END_IF;
ELSE
    rTMR_Cond_Timer_C := 0.0;
END_IF;

IF (NOT bTMR_Cond_Fault_A) AND (NOT bTMR_Cond_Fault_B) AND (NOT bTMR_Cond_Fault_C) THEN
    IF ((rCondenserCoilTemp_ChA >= rCondenserCoilTemp_ChB) AND (rCondenserCoilTemp_ChA <= rCondenserCoilTemp_ChC)) OR
       ((rCondenserCoilTemp_ChA <= rCondenserCoilTemp_ChB) AND (rCondenserCoilTemp_ChA >= rCondenserCoilTemp_ChC)) THEN
        rVotedCondenserCoilTempActual := rCondenserCoilTemp_ChA;
    ELSIF ((rCondenserCoilTemp_ChB >= rCondenserCoilTemp_ChA) AND (rCondenserCoilTemp_ChB <= rCondenserCoilTemp_ChC)) OR
          ((rCondenserCoilTemp_ChB <= rCondenserCoilTemp_ChA) AND (rCondenserCoilTemp_ChB >= rCondenserCoilTemp_ChC)) THEN
        rVotedCondenserCoilTempActual := rCondenserCoilTemp_ChB;
    ELSE
        rVotedCondenserCoilTempActual := rCondenserCoilTemp_ChC;
    END_IF;
ELSIF bTMR_Cond_Fault_A AND (NOT bTMR_Cond_Fault_B) AND (NOT bTMR_Cond_Fault_C) THEN
    rVotedCondenserCoilTempActual := 0.5 * (rCondenserCoilTemp_ChB + rCondenserCoilTemp_ChC);
ELSIF bTMR_Cond_Fault_B AND (NOT bTMR_Cond_Fault_A) AND (NOT bTMR_Cond_Fault_C) THEN
    rVotedCondenserCoilTempActual := 0.5 * (rCondenserCoilTemp_ChA + rCondenserCoilTemp_ChC);
ELSIF bTMR_Cond_Fault_C AND (NOT bTMR_Cond_Fault_A) AND (NOT bTMR_Cond_Fault_B) THEN
    rVotedCondenserCoilTempActual := 0.5 * (rCondenserCoilTemp_ChA + rCondenserCoilTemp_ChB);
ELSE
    bAlarm_SensorTMR_Discrepancy_H := TRUE;
    rVotedCondenserCoilTempActual := rCondenserCoilTemp_ChA;
END_IF;

(* --- 1.6: Hydraulic Shelf Stoppering Compaction Load Cells 2oo3 TMR Voting --- *)
rTMR_Ram_Diff_AB := ABS(rHydraulicRamForce_ChA - rHydraulicRamForce_ChB);
rTMR_Ram_Diff_BC := ABS(rHydraulicRamForce_ChB - rHydraulicRamForce_ChC);
rTMR_Ram_Diff_CA := ABS(rHydraulicRamForce_ChC - rHydraulicRamForce_ChA);

IF (rTMR_Ram_Diff_AB > 25.0) AND (rTMR_Ram_Diff_CA > 25.0) THEN
    rTMR_Ram_Timer_A := rTMR_Ram_Timer_A + rCycleScanDeltaTime;
    IF rTMR_Ram_Timer_A >= 0.50 THEN
        bTMR_Ram_Fault_A := TRUE;
    END_IF;
ELSE
    rTMR_Ram_Timer_A := 0.0;
END_IF;

IF (rTMR_Ram_Diff_AB > 25.0) AND (rTMR_Ram_Diff_BC > 25.0) THEN
    rTMR_Ram_Timer_B := rTMR_Ram_Timer_B + rCycleScanDeltaTime;
    IF rTMR_Ram_Timer_B >= 0.50 THEN
        bTMR_Ram_Fault_B := TRUE;
    END_IF;
ELSE
    rTMR_Ram_Timer_B := 0.0;
END_IF;

IF (rTMR_Ram_Diff_BC > 25.0) AND (rTMR_Ram_Diff_CA > 25.0) THEN
    rTMR_Ram_Timer_C := rTMR_Ram_Timer_C + rCycleScanDeltaTime;
    IF rTMR_Ram_Timer_C >= 0.50 THEN
        bTMR_Ram_Fault_C := TRUE;
    END_IF;
ELSE
    rTMR_Ram_Timer_C := 0.0;
END_IF;

IF (NOT bTMR_Ram_Fault_A) AND (NOT bTMR_Ram_Fault_B) AND (NOT bTMR_Ram_Fault_C) THEN
    (* All 3 load cells healthy: evaluate average force across 3-point load distribution *)
    rVotedHydraulicRamForceActual := (rHydraulicRamForce_ChA + rHydraulicRamForce_ChB + rHydraulicRamForce_ChC) / 3.0;
ELSIF bTMR_Ram_Fault_A AND (NOT bTMR_Ram_Fault_B) AND (NOT bTMR_Ram_Fault_C) THEN
    rVotedHydraulicRamForceActual := 0.5 * (rHydraulicRamForce_ChB + rHydraulicRamForce_ChC);
ELSIF bTMR_Ram_Fault_B AND (NOT bTMR_Ram_Fault_A) AND (NOT bTMR_Ram_Fault_C) THEN
    rVotedHydraulicRamForceActual := 0.5 * (rHydraulicRamForce_ChA + rHydraulicRamForce_ChC);
ELSIF bTMR_Ram_Fault_C AND (NOT bTMR_Ram_Fault_A) AND (NOT bTMR_Ram_Fault_B) THEN
    rVotedHydraulicRamForceActual := 0.5 * (rHydraulicRamForce_ChA + rHydraulicRamForce_ChB);
ELSE
    bAlarm_SensorTMR_Discrepancy_H := TRUE;
    rVotedHydraulicRamForceActual := rHydraulicRamForce_ChA;
END_IF;
"""

print("generate_phase1 loaded.")
