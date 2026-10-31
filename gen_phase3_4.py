# gen_phase3_4.py - Generates Phase 3 (State Space) & Phase 4 (MPC)

def generate_phase3_4():
    return """(* ==================================================================================================================== *)
(* PHASE 3: DISCRETE STATE-SPACE MODEL PROPAGATION (x[k+1] = A * x[k] + B * u[k])                                       *)
(* ==================================================================================================================== *)

(* Map Real-Time Sensor Feedbacks & Observers into State Vector x[k] *)
ax_LyoState[1]  := rShelfTempInlet_ChA;
ax_LyoState[2]  := rShelfTempOutlet_ChA;
ax_LyoState[3]  := rVotedShelfTemperatureActual;
ax_LyoState[4]  := rVialBaseTemperatureEstimate;
ax_LyoState[5]  := rVotedProductTemperatureActual;
ax_LyoState[6]  := rVotedProductTemperatureActual + 2.5; (* Upper cake layer estimate *)
ax_LyoState[7]  := rVotedChamberPressure_CM_Actual * (1.0 - (rVotedChamberPressure_CM_Actual / (rVotedChamberPressure_Pirani_Actual + 0.0001)));
ax_LyoState[8]  := rVotedChamberPressure_CM_Actual - ax_LyoState[7];
IF ax_LyoState[8] < 0.0 THEN ax_LyoState[8] := 0.0; END_IF;
ax_LyoState[9]  := rVotedChamberPressure_CM_Actual;
ax_LyoState[10] := rVotedChamberPressure_Pirani_Actual;
ax_LyoState[11] := rVotedCondenserCoilTempActual;
ax_LyoState[12] := rCondenserFrostThickness_mm;
ax_LyoState[13] := rSublimationRateInstantaneous;
ax_LyoState[14] := rDesorptionMoistureEstimate_Pct;
ax_LyoState[15] := rHydraulicRamLinearPosition_mm;
ax_LyoState[16] := rVotedHydraulicRamForceActual;

(* Execute 16x16 State Prediction Matrix Multiply *)
FOR nRowIdx := 1 TO 16 DO
    ax_LyoPredicted[nRowIdx] := 0.0;
    FOR nColIdx := 1 TO 16 DO
        ax_LyoPredicted[nRowIdx] := ax_LyoPredicted[nRowIdx] + (aA_Lyo[nRowIdx, nColIdx] * ax_LyoState[nColIdx]);
    END_FOR;
    FOR nColIdx := 1 TO 8 DO
        ax_LyoPredicted[nRowIdx] := ax_LyoPredicted[nRowIdx] + (aB_Lyo[nRowIdx, nColIdx] * au_LyoPrevious[nColIdx]);
    END_FOR;
END_FOR;

(* ==================================================================================================================== *)
(* PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) COST MINIMIZATION & ACTUATOR PACING                         *)
(* ==================================================================================================================== *)

(* Dynamic State Trajectory Target Mapping Based on Current Recipe Steps *)
aStateTrajectoryTarget[1]  := rShelfRampSetpointActual;
aStateTrajectoryTarget[2]  := rShelfRampSetpointActual - 0.50;
aStateTrajectoryTarget[3]  := rShelfRampSetpointActual;
aStateTrajectoryTarget[4]  := rShelfRampSetpointActual - 1.20;
aStateTrajectoryTarget[5]  := rSet_ProductCollapseTemp_Tc - 3.00; (* Tight safety margin *)
aStateTrajectoryTarget[6]  := rShelfRampSetpointActual - 2.00;
aStateTrajectoryTarget[7]  := rChamberPresSetpointActual * 0.70;
aStateTrajectoryTarget[8]  := rChamberPresSetpointActual * 0.30;
aStateTrajectoryTarget[9]  := rChamberPresSetpointActual;
aStateTrajectoryTarget[10] := rChamberPresSetpointActual;
aStateTrajectoryTarget[11] := -80.0; (* Condenser setpoint *)
aStateTrajectoryTarget[12] := 0.0;
aStateTrajectoryTarget[13] := 15.0;  (* Target sublimation flux *)
aStateTrajectoryTarget[14] := 0.80;  (* Desorption moisture target < 1% *)
aStateTrajectoryTarget[15] := 350.0; (* Stoppering stroke *)
aStateTrajectoryTarget[16] := rSet_StopperingHoldForceTarget;

(* Compute State Tracking Errors: e = Target - Predicted *)
FOR nRowIdx := 1 TO 16 DO
    aStateTrackingError[nRowIdx] := aStateTrajectoryTarget[nRowIdx] - ax_LyoPredicted[nRowIdx];
END_FOR;

(* --- Unrolled MPC Optimization: Gradient Descent with Quadratic Cost Weights --- *)
IF bMasterBatchRunPermissive AND (NOT bEmergencySafetyInterlockTripped) THEN

    (* Actuator 1: SCR Electric Heater Duty [%] (Controls Shelf Fluid Inlet Temp) *)
    rMPC_GradientAcc := (aB_Lyo[1, 1] * aQ_LyoDiag[1] * aStateTrackingError[1])
                      + (aB_Lyo[3, 1] * aQ_LyoDiag[3] * aStateTrackingError[3])
                      + (aB_Lyo[5, 1] * aQ_LyoDiag[5] * aStateTrackingError[5]);
    rMPC_HessianTerm := aR_LyoDiag[1] + (aB_Lyo[1, 1] * aP_LyoDiag[1] * aB_Lyo[1, 1]) + (aB_Lyo[3, 1] * aP_LyoDiag[3] * aB_Lyo[3, 1]);
    IF rMPC_HessianTerm > 0.001 THEN
        aDelta_u_Lyo[1] := 0.35 * (rMPC_GradientAcc / rMPC_HessianTerm);
    ELSE
        aDelta_u_Lyo[1] := 0.0;
    END_IF;

    (* Actuator 2: Screw Compressor Slide Valve [%] (Primary Mechanical Chilling) *)
    rMPC_GradientAcc := (-aB_Lyo[1, 2] * aQ_LyoDiag[1] * aStateTrackingError[1])
                      + (-aB_Lyo[3, 2] * aQ_LyoDiag[3] * aStateTrackingError[3]);
    rMPC_HessianTerm := aR_LyoDiag[2] + (aB_Lyo[1, 2] * aP_LyoDiag[1] * aB_Lyo[1, 2]);
    IF rMPC_HessianTerm > 0.001 THEN
        aDelta_u_Lyo[2] := 0.28 * (rMPC_GradientAcc / rMPC_HessianTerm);
    ELSE
        aDelta_u_Lyo[2] := 0.0;
    END_IF;

    (* Actuator 3: Cryogenic LN2 Booster Injection Valve [%] (Deep Freeze Ramp Rate Boost) *)
    IF (eCurrentState = 30) AND (rShelfRampSetpointActual < -30.0) THEN
        rMPC_GradientAcc := (-aB_Lyo[1, 3] * aQ_LyoDiag[1] * aStateTrackingError[1]);
        rMPC_HessianTerm := aR_LyoDiag[3] + (aB_Lyo[1, 3] * aP_LyoDiag[1] * aB_Lyo[1, 3]);
        IF rMPC_HessianTerm > 0.001 THEN
            aDelta_u_Lyo[3] := 0.40 * (rMPC_GradientAcc / rMPC_HessianTerm);
        ELSE
            aDelta_u_Lyo[3] := 0.0;
        END_IF;
    ELSE
        aDelta_u_Lyo[3] := -5.0 * rCycleScanDeltaTime; (* Bleed down LN2 valve when not active *)
    END_IF;

    (* Actuator 4: High-Vacuum Roots Blower VFD Speed [%] (Chamber Pressure Coarse Control) *)
    rMPC_GradientAcc := (-aB_Lyo[9, 4] * aQ_LyoDiag[9] * aStateTrackingError[9]);
    rMPC_HessianTerm := aR_LyoDiag[4] + (aB_Lyo[9, 4] * aP_LyoDiag[9] * aB_Lyo[9, 4]);
    IF rMPC_HessianTerm > 0.001 THEN
        aDelta_u_Lyo[4] := 0.32 * (rMPC_GradientAcc / rMPC_HessianTerm);
    ELSE
        aDelta_u_Lyo[4] := 0.0;
    END_IF;

    (* Actuator 5: Sterile N2 Micro-Bleed Proportional Dosing Valve [%] (Precision Chamber Pressure Trim) *)
    IF (eCurrentState = 60) OR (eCurrentState = 70) THEN
        rMPC_GradientAcc := (aB_Lyo[9, 5] * aQ_LyoDiag[9] * aStateTrackingError[9]);
        rMPC_HessianTerm := aR_LyoDiag[5] + (aB_Lyo[9, 5] * aP_LyoDiag[9] * aB_Lyo[9, 5]);
        IF rMPC_HessianTerm > 0.001 THEN
            aDelta_u_Lyo[5] := 0.45 * (rMPC_GradientAcc / rMPC_HessianTerm);
        ELSE
            aDelta_u_Lyo[5] := 0.0;
        END_IF;
    ELSE
        aDelta_u_Lyo[5] := -10.0 * rCycleScanDeltaTime;
    END_IF;

    (* Actuator 6: Condenser Refrigeration Direct Expansion TXV [%] *)
    rMPC_GradientAcc := (-aB_Lyo[11, 6] * aQ_LyoDiag[11] * aStateTrackingError[11]);
    rMPC_HessianTerm := aR_LyoDiag[6] + (aB_Lyo[11, 6] * aP_LyoDiag[11] * aB_Lyo[11, 6]);
    IF rMPC_HessianTerm > 0.001 THEN
        aDelta_u_Lyo[6] := 0.30 * (rMPC_GradientAcc / rMPC_HessianTerm);
    ELSE
        aDelta_u_Lyo[6] := 0.0;
    END_IF;

    (* Actuator 7: Hydraulic Directional Servo Valve [%] (Shelf Stoppering Force Compaction) *)
    IF eCurrentState = 100 THEN
        rMPC_GradientAcc := (aB_Lyo[16, 7] * aQ_LyoDiag[16] * aStateTrackingError[16]);
        rMPC_HessianTerm := aR_LyoDiag[7] + (aB_Lyo[16, 7] * aP_LyoDiag[16] * aB_Lyo[16, 7]);
        IF rMPC_HessianTerm > 0.001 THEN
            aDelta_u_Lyo[7] := 0.25 * (rMPC_GradientAcc / rMPC_HessianTerm);
        ELSE
            aDelta_u_Lyo[7] := 0.0;
        END_IF;
    ELSE
        aDelta_u_Lyo[7] := -10.0 * rCycleScanDeltaTime;
    END_IF;

    (* Actuator 8: Nucleation Depressurization Pulse Valve [%] *)
    IF eCurrentState = 40 THEN
        aDelta_u_Lyo[8] := 50.0; (* Rapid pulse *)
    ELSE
        aDelta_u_Lyo[8] := -100.0; (* Fully closed *)
    END_IF;

    (* Critical Product Cake Collapse Safety Interlock Override *)
    IF (ax_LyoPredicted[5] >= (rSet_ProductCollapseTemp_Tc - 1.50)) AND ((eCurrentState = 60) OR (eCurrentState = 70)) THEN
        (* Product temperature dangerously approaching collapse: immediately kill heater SCR duty *)
        aDelta_u_Lyo[1] := -25.0;
        (* Boost refrigeration capacity to prevent meltback *)
        aDelta_u_Lyo[2] := 15.0;
    END_IF;

    (* Actuator Slew Rate Limiting & Integration *)
    FOR nInputIdx := 1 TO 8 DO
        IF aDelta_u_Lyo[nInputIdx] > (aActuatorSlewRateLimit[nInputIdx] * rCycleScanDeltaTime) THEN
            aDelta_u_Lyo[nInputIdx] := aActuatorSlewRateLimit[nInputIdx] * rCycleScanDeltaTime;
        ELSIF aDelta_u_Lyo[nInputIdx] < (-aActuatorSlewRateLimit[nInputIdx] * rCycleScanDeltaTime) THEN
            aDelta_u_Lyo[nInputIdx] := -aActuatorSlewRateLimit[nInputIdx] * rCycleScanDeltaTime;
        END_IF;

        au_LyoInput[nInputIdx] := au_LyoPrevious[nInputIdx] + aDelta_u_Lyo[nInputIdx];

        (* Actuator Physical Saturation Limiting *)
        IF au_LyoInput[nInputIdx] > aActuatorUpperLimit[nInputIdx] THEN
            au_LyoInput[nInputIdx] := aActuatorUpperLimit[nInputIdx];
        ELSIF au_LyoInput[nInputIdx] < aActuatorLowerLimit[nInputIdx] THEN
            au_LyoInput[nInputIdx] := aActuatorLowerLimit[nInputIdx];
        END_IF;

        au_LyoPrevious[nInputIdx] := au_LyoInput[nInputIdx];
    END_FOR;

    (* Map Optimized MPC Commands to Physical Outputs *)
    rCmd_ShelfHeaterSCR_DutyPct            := au_LyoInput[1];
    rCmd_ScrewCompressorSlideValvePct      := au_LyoInput[2];
    rCmd_LN2_BoosterCoolingValvePct        := au_LyoInput[3];
    rCmd_RootsVacuumBlowerSpeedPct         := au_LyoInput[4];
    rCmd_SterileN2_MicroBleedDosingPct     := au_LyoInput[5];
    rCmd_CondenserRefrigExpansionValvePct  := au_LyoInput[6];
    rCmd_HydraulicStopperingServoPct       := au_LyoInput[7];
    rCmd_NucleationDepressPulseValvePct    := au_LyoInput[8];

ELSE
    (* Emergency Safe State / Batch Inactive: Actuators to Fail-Safe Low Power *)
    rCmd_ShelfHeaterSCR_DutyPct            := 0.0;
    rCmd_ScrewCompressorSlideValvePct      := 0.0;
    rCmd_LN2_BoosterCoolingValvePct        := 0.0;
    rCmd_RootsVacuumBlowerSpeedPct         := 0.0;
    rCmd_SterileN2_MicroBleedDosingPct     := 0.0;
    rCmd_CondenserRefrigExpansionValvePct  := 0.0;
    rCmd_HydraulicStopperingServoPct       := 0.0;
    rCmd_NucleationDepressPulseValvePct    := 0.0;

    FOR nInputIdx := 1 TO 8 DO
        au_LyoInput[nInputIdx] := 0.0;
        au_LyoPrevious[nInputIdx] := 0.0;
    END_FOR;
END_IF;
"""

print("generate_phase3_4 loaded.")
