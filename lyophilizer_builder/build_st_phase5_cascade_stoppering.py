# lyophilizer_builder/build_st_phase5_cascade_stoppering.py

def get_phase5_cascade_stoppering():
    return """(* === PHASE 5: DUAL-CASCADE REFRIGERATION & HYDRAULIC STOPPERING SUBSYSTEMS === *)
(* ---------------------------------------------------------------------------------------------------- *)
(* DUAL-CASCADE REFRIGERATION CYCLE DIAGNOSTICS & CONDENSER TEMPERATURE MANAGEMENT                      *)
(* Stage 1: R404A/R452A High-Stage (-40 deg C interstage), Stage 2: R508B Low-Stage (-85 deg C coil)    *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Stage 1 Saturated Vapor Temperature Approximation [deg C] from Pressure [bar] *)
IF rCascadeStage1_SuctionPress > 0.10 THEN
    rCascadeStage1_EvapTemp := -45.0 + (12.50 * LN(rCascadeStage1_SuctionPress));
ELSE
    rCascadeStage1_EvapTemp := -55.0;
END_IF;

IF rCascadeStage1_DischPress > 1.00 THEN
    rCascadeStage1_CondTemp := 25.0 + (8.250 * LN(rCascadeStage1_DischPress));
ELSE
    rCascadeStage1_CondTemp := 30.0;
END_IF;

(* Stage 2 Saturated Vapor Temperature Approximation [deg C] from Pressure [bar] *)
IF rCascadeStage2_SuctionPress > 0.05 THEN
    rCascadeStage2_EvapTemp := -88.0 + (9.850 * LN(rCascadeStage2_SuctionPress));
ELSE
    rCascadeStage2_EvapTemp := -95.0;
END_IF;

IF rCascadeStage2_DischPress > 0.50 THEN
    rCascadeStage2_CondTemp := -38.0 + (7.450 * LN(rCascadeStage2_DischPress));
ELSE
    rCascadeStage2_CondTemp := -40.0;
END_IF;

(* Interstage Plate Heat Exchanger Thermal Approach [deg C] *)
rCascadeInterstageApproach := rCascadeStage2_CondTemp - rCascadeStage1_EvapTemp;

(* Condenser Dual Sensor Synthesis & Health Check *)
IF ABS(rCondenserCoilTemp_A - rCondenserCoilTemp_B) < 4.50 THEN
    rCondenserVotedTemp := (rCondenserCoilTemp_A + rCondenserCoilTemp_B) * 0.50;
    bCondenserTempFault := FALSE;
ELSE
    rCondenserVotedTemp := MIN(rCondenserCoilTemp_A, rCondenserCoilTemp_B); (* Failsafe cold pick *)
    bCondenserTempFault := TRUE;
END_IF;

(* Refrigeration Capacity Modulation & Hot Gas Defrost Logic *)
IF bDefrostActive THEN
    bCmd_CondenserHotGasDefrost := TRUE;
    rCmd_CascadeStage2Suction_pct := 0.0;
    tDefrostTimer_s := tDefrostTimer_s + tScanInterval_s;
    IF (tDefrostTimer_s >= 2400.0) OR (rCondenserVotedTemp >= 25.0) THEN
        bDefrostActive := FALSE;
        bCmd_CondenserHotGasDefrost := FALSE;
        tDefrostTimer_s := 0.0;
    END_IF;
ELSE
    bCmd_CondenserHotGasDefrost := FALSE;
    tDefrostTimer_s := 0.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* HYDRAULIC VIAL STOPPERING RAM PRESS SUBSYSTEM                                                        *)
(* Compresses 16 shelves together to seat elastomeric lyophilization stoppers into 85,000 vials        *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Compressive Force Calculation: F = P * A [kN] *)
rStopperingForce_kN := rStopperingPressure_bar * (rHydraulicCylinderArea_cm2 / 100.00) * 0.100;

IF nFsmState = 11 THEN
    (* STATE_HYDRAULIC_VIAL_STOPPERING_RAM_PRESS Active *)
    IF rStopperingRamPos_mm < rStopperingTargetPos_mm THEN
        (* Ram advancing down to compress shelves *)
        rCmd_HydraulicStopperingValve_pct := 45.00;
        tStopperingHoldTimer_s := 0.0;
        bStopperingHoldComplete := FALSE;
        bStopperingComplete := FALSE;
    ELSIF rStopperingForce_kN < (rStopperingTargetForce_kN * 0.95) THEN
        (* Pressure build-up to final compaction setpoint (3,400 kN) *)
        rCmd_HydraulicStopperingValve_pct := MIN(100.0, rCmd_HydraulicStopperingValve_pct + 0.50);
        tStopperingHoldTimer_s := 0.0;
        bStopperingHoldComplete := FALSE;
        bStopperingComplete := FALSE;
    ELSE
        (* Target compressive force sustained: Hold soak timer for 300 s (5 min) *)
        rCmd_HydraulicStopperingValve_pct := 75.00; (* Pressure holding regulation *)
        tStopperingHoldTimer_s := tStopperingHoldTimer_s + tScanInterval_s;
        IF tStopperingHoldTimer_s >= 300.0 THEN
            bStopperingHoldComplete := TRUE;
            bStopperingComplete := TRUE;
        END_IF;
    END_IF;
ELSE
    (* Retracted Home Position *)
    rCmd_HydraulicStopperingValve_pct := 0.0;
    tStopperingHoldTimer_s := 0.0;
    bStopperingHoldComplete := FALSE;
END_IF;
"""
