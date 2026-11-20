(* ==================================================================================================== *)
(* PHASE 1: 4-CHANNEL 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH 50ms DISCREPANCY WATCHDOGS *)
(* ==================================================================================================== *)
(* ARCHITECTURAL OVERVIEW & PRINCIPLES OF 2oo3 SENSOR TRIPLE MODULAR REDUNDANCY:                         *)
(* To guarantee SIL 3 / PL e machine safety and deterministic cyber-physical accuracy during high-tonnage*)
(* superplastic forging at 100 MN (10,000 metric tons) and 950 deg C die temperatures, four critical     *)
(* process measurement feedback loops are instrumented with triply redundant independent transducers:   *)
(*   1. Channel 1: Total Ram Axial Forging Tonnage [kN] (3x calibrated load cell strain columns)          *)
(*   2. Channel 2: Main Cylinder High-Pressure Hydraulic Header [bar] (3x piezoresistive transmitters)    *)
(*   3. Channel 3: Upper Die Induction Core Temperature [deg C] (3x Type-B thermocouples & pyrometers)    *)
(*   4. Channel 4: 4-Corner Dynamic Ram Leveling Tilt Skew [um] (3x absolute optical/magnetic encoders)   *)
(*                                                                                                      *)
(* For each channel, the algorithm executes five deterministic real-time operations per scan cycle:      *)
(*   1. Hardware Health Verification: Verifies transducer electrical loop integrity (b_ValidA/B/C).      *)
(*   2. Pairwise Divergence Analysis: Computes absolute sensor discrepancies |A-B|, |B-C|, |C-A|.        *)
(*   3. 50ms Persistent Discrepancy Integration: Real-time accumulator timer filters transient noise while*)
(*      latching sustained sensor calibration drift or catastrophic signal failure.                     *)
(*   4. Tri-State Fault Isolation & Bumpless Degradation Management:                                     *)
(*      - Full 3-Sensor Healthy: Exact Median selection (Voted = Median(A, B, C)) with zero drift.       *)
(*      - Single Sensor Faulted: Seamless transition to 2-sensor arithmetic mean (Voted = 0.5*(Y+Z)).   *)
(*      - Dual Sensors Faulted: Emergency degraded operation on surviving sensor with safety warning.    *)
(*      - Triple Sensors Faulted: Total channel failure lock, emergency decompression abort triggered.    *)
(*   5. First-Order Bumpless Slew Rate Limiter: Suppresses derivative impulses during sensor transition  *)
(*      to safeguard downstream Kalman state estimation and Model Predictive Control (MPC) solvers.      *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* CHANNEL 1: MAIN RAM AXIAL FORGING TONNAGE 2oo3 VOTING ENGINE [kN]                                    *)
(* Transducers: Sensor A (Tie-Rod Column FL), Sensor B (Tie-Rod Column FR), Sensor C (Piezo Dynamometer)*)
(* Nominal Rating: 100,000 kN (10,000 metric tons). Discrepancy Tolerance: 2,500.0 kN (2.5% Full Scale).  *)
(* Discrepancy Persistence Watchdog: 50.0 ms. Slew Limit: 50,000 kN/s.                                  *)
(* ---------------------------------------------------------------------------------------------------- *)
r_TMR_Tonnage_DiffAB_kN := ABS(r_Tonnage_SensorA_kN - r_Tonnage_SensorB_kN);
r_TMR_Tonnage_DiffBC_kN := ABS(r_Tonnage_SensorB_kN - r_Tonnage_SensorC_kN);
r_TMR_Tonnage_DiffCA_kN := ABS(r_Tonnage_SensorC_kN - r_Tonnage_SensorA_kN);

(* Pair AB Discrepancy Persistence Integration *)
IF (r_TMR_Tonnage_DiffAB_kN > r_Tonnage_TMR_TolMax_kN) OR (NOT b_Tonnage_ValidA) OR (NOT b_Tonnage_ValidB) THEN
    r_TMR_Tonnage_TimerAB_ms := r_TMR_Tonnage_TimerAB_ms + r_CycleScanPeriod_ms;
ELSE
    IF r_TMR_Tonnage_TimerAB_ms > 0.0 THEN
        r_TMR_Tonnage_TimerAB_ms := r_TMR_Tonnage_TimerAB_ms - (r_CycleScanPeriod_ms * 2.0);
        IF r_TMR_Tonnage_TimerAB_ms < 0.0 THEN
            r_TMR_Tonnage_TimerAB_ms := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Pair BC Discrepancy Persistence Integration *)
IF (r_TMR_Tonnage_DiffBC_kN > r_Tonnage_TMR_TolMax_kN) OR (NOT b_Tonnage_ValidB) OR (NOT b_Tonnage_ValidC) THEN
    r_TMR_Tonnage_TimerBC_ms := r_TMR_Tonnage_TimerBC_ms + r_CycleScanPeriod_ms;
ELSE
    IF r_TMR_Tonnage_TimerBC_ms > 0.0 THEN
        r_TMR_Tonnage_TimerBC_ms := r_TMR_Tonnage_TimerBC_ms - (r_CycleScanPeriod_ms * 2.0);
        IF r_TMR_Tonnage_TimerBC_ms < 0.0 THEN
            r_TMR_Tonnage_TimerBC_ms := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Pair CA Discrepancy Persistence Integration *)
IF (r_TMR_Tonnage_DiffCA_kN > r_Tonnage_TMR_TolMax_kN) OR (NOT b_Tonnage_ValidC) OR (NOT b_Tonnage_ValidA) THEN
    r_TMR_Tonnage_TimerCA_ms := r_TMR_Tonnage_TimerCA_ms + r_CycleScanPeriod_ms;
ELSE
    IF r_TMR_Tonnage_TimerCA_ms > 0.0 THEN
        r_TMR_Tonnage_TimerCA_ms := r_TMR_Tonnage_TimerCA_ms - (r_CycleScanPeriod_ms * 2.0);
        IF r_TMR_Tonnage_TimerCA_ms < 0.0 THEN
            r_TMR_Tonnage_TimerCA_ms := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Sensor Fault Isolation Matrix for Tonnage Channel *)
IF (r_TMR_Tonnage_TimerAB_ms >= 50.0) AND (r_TMR_Tonnage_TimerCA_ms >= 50.0) AND (r_TMR_Tonnage_TimerBC_ms < 50.0) THEN
    b_TMR_Tonnage_FaultA := TRUE;
END_IF;
IF (r_TMR_Tonnage_TimerAB_ms >= 50.0) AND (r_TMR_Tonnage_TimerBC_ms >= 50.0) AND (r_TMR_Tonnage_TimerCA_ms < 50.0) THEN
    b_TMR_Tonnage_FaultB := TRUE;
END_IF;
IF (r_TMR_Tonnage_TimerBC_ms >= 50.0) AND (r_TMR_Tonnage_TimerCA_ms >= 50.0) AND (r_TMR_Tonnage_TimerAB_ms < 50.0) THEN
    b_TMR_Tonnage_FaultC := TRUE;
END_IF;
IF NOT b_Tonnage_ValidA THEN
    b_TMR_Tonnage_FaultA := TRUE;
END_IF;
IF NOT b_Tonnage_ValidB THEN
    b_TMR_Tonnage_FaultB := TRUE;
END_IF;
IF NOT b_Tonnage_ValidC THEN
    b_TMR_Tonnage_FaultC := TRUE;
END_IF;
IF b_ResetAllFaults THEN
    b_TMR_Tonnage_FaultA := FALSE;
    b_TMR_Tonnage_FaultB := FALSE;
    b_TMR_Tonnage_FaultC := FALSE;
    b_TMR_Tonnage_TotalFailure := FALSE;
    r_TMR_Tonnage_TimerAB_ms := 0.0;
    r_TMR_Tonnage_TimerBC_ms := 0.0;
    r_TMR_Tonnage_TimerCA_ms := 0.0;
END_IF;

(* Degradation Voting Selection for Tonnage Channel *)
IF (NOT b_TMR_Tonnage_FaultA) AND (NOT b_TMR_Tonnage_FaultB) AND (NOT b_TMR_Tonnage_FaultC) THEN
    (* All 3 Channels Healthy: Exact Median Voting *)
    IF ((r_Tonnage_SensorA_kN >= r_Tonnage_SensorB_kN) AND (r_Tonnage_SensorA_kN <= r_Tonnage_SensorC_kN)) OR
       ((r_Tonnage_SensorA_kN >= r_Tonnage_SensorC_kN) AND (r_Tonnage_SensorA_kN <= r_Tonnage_SensorB_kN)) THEN
        r_TMR_VotedTonnage_kN := r_Tonnage_SensorA_kN;
    ELSIF ((r_Tonnage_SensorB_kN >= r_Tonnage_SensorA_kN) AND (r_Tonnage_SensorB_kN <= r_Tonnage_SensorC_kN)) OR
          ((r_Tonnage_SensorB_kN >= r_Tonnage_SensorC_kN) AND (r_Tonnage_SensorB_kN <= r_Tonnage_SensorA_kN)) THEN
        r_TMR_VotedTonnage_kN := r_Tonnage_SensorB_kN;
    ELSE
        r_TMR_VotedTonnage_kN := r_Tonnage_SensorC_kN;
    END_IF;
    b_TMR_Tonnage_DegradedMode := FALSE;
    b_TMR_Tonnage_TotalFailure := FALSE;
ELSIF b_TMR_Tonnage_FaultA AND (NOT b_TMR_Tonnage_FaultB) AND (NOT b_TMR_Tonnage_FaultC) THEN
    (* Sensor A Faulted: Dual Redundant Mean of B and C *)
    r_TMR_VotedTonnage_kN := 0.5 * (r_Tonnage_SensorB_kN + r_Tonnage_SensorC_kN);
    b_TMR_Tonnage_DegradedMode := TRUE;
ELSIF b_TMR_Tonnage_FaultB AND (NOT b_TMR_Tonnage_FaultA) AND (NOT b_TMR_Tonnage_FaultC) THEN
    (* Sensor B Faulted: Dual Redundant Mean of A and C *)
    r_TMR_VotedTonnage_kN := 0.5 * (r_Tonnage_SensorA_kN + r_Tonnage_SensorC_kN);
    b_TMR_Tonnage_DegradedMode := TRUE;
ELSIF b_TMR_Tonnage_FaultC AND (NOT b_TMR_Tonnage_FaultA) AND (NOT b_TMR_Tonnage_FaultB) THEN
    (* Sensor C Faulted: Dual Redundant Mean of A and B *)
    r_TMR_VotedTonnage_kN := 0.5 * (r_Tonnage_SensorA_kN + r_Tonnage_SensorB_kN);
    b_TMR_Tonnage_DegradedMode := TRUE;
ELSIF (NOT b_TMR_Tonnage_FaultA) AND b_TMR_Tonnage_FaultB AND b_TMR_Tonnage_FaultC THEN
    (* Only Sensor A Healthy: Fallback Single Channel *)
    r_TMR_VotedTonnage_kN := r_Tonnage_SensorA_kN;
    b_TMR_Tonnage_DegradedMode := TRUE;
ELSIF (NOT b_TMR_Tonnage_FaultB) AND b_TMR_Tonnage_FaultA AND b_TMR_Tonnage_FaultC THEN
    (* Only Sensor B Healthy: Fallback Single Channel *)
    r_TMR_VotedTonnage_kN := r_Tonnage_SensorB_kN;
    b_TMR_Tonnage_DegradedMode := TRUE;
ELSIF (NOT b_TMR_Tonnage_FaultC) AND b_TMR_Tonnage_FaultA AND b_TMR_Tonnage_FaultB THEN
    (* Only Sensor C Healthy: Fallback Single Channel *)
    r_TMR_VotedTonnage_kN := r_Tonnage_SensorC_kN;
    b_TMR_Tonnage_DegradedMode := TRUE;
ELSE
    (* All 3 Sensors Faulted: Total Channel Failure Lockout *)
    b_TMR_Tonnage_TotalFailure := TRUE;
    b_TMR_Tonnage_DegradedMode := TRUE;
END_IF;

(* Bumpless Slew Rate Filter for Tonnage (Max 50,000 kN/s = 50.0 kN/ms) *)
r_TmpDeltaU := r_TMR_VotedTonnage_kN - r_TMR_Tonnage_SlewFilt_kN;
IF r_TmpDeltaU > (50.0 * r_CycleScanPeriod_ms) THEN
    r_TMR_Tonnage_SlewFilt_kN := r_TMR_Tonnage_SlewFilt_kN + (50.0 * r_CycleScanPeriod_ms);
ELSIF r_TmpDeltaU < -(50.0 * r_CycleScanPeriod_ms) THEN
    r_TMR_Tonnage_SlewFilt_kN := r_TMR_Tonnage_SlewFilt_kN - (50.0 * r_CycleScanPeriod_ms);
ELSE
    r_TMR_Tonnage_SlewFilt_kN := r_TMR_VotedTonnage_kN;
END_IF;
r_TMR_VotedTonnage_kN := r_TMR_Tonnage_SlewFilt_kN;

(* ---------------------------------------------------------------------------------------------------- *)
(* CHANNEL 2: MAIN CYLINDER HIGH-PRESSURE HYDRAULIC HEADER 2oo3 VOTING ENGINE [bar]                     *)
(* Transducers: Sensor A (Manifold Piezoresistive Transducer 1), Sensor B (Manifold Transducer 2),     *)
(*              Sensor C (Pre-Fill Intensifier Transducer 3). Nominal: 350.0 bar (Max: 400.0 bar).       *)
(* Discrepancy Tolerance: 12.0 bar. Persistence Watchdog: 50.0 ms. Slew Limit: 250.0 bar/s.             *)
(* ---------------------------------------------------------------------------------------------------- *)
r_TMR_HydPress_DiffAB_bar := ABS(r_HydPressure_SensorA_bar - r_HydPressure_SensorB_bar);
r_TMR_HydPress_DiffBC_bar := ABS(r_HydPressure_SensorB_bar - r_HydPressure_SensorC_bar);
r_TMR_HydPress_DiffCA_bar := ABS(r_HydPressure_SensorC_bar - r_HydPressure_SensorA_bar);

(* Pair AB Discrepancy Persistence Integration *)
IF (r_TMR_HydPress_DiffAB_bar > r_HydPressure_TMR_TolMax_bar) OR (NOT b_HydPressure_ValidA) OR (NOT b_HydPressure_ValidB) THEN
    r_TMR_HydPress_TimerAB_ms := r_TMR_HydPress_TimerAB_ms + r_CycleScanPeriod_ms;
ELSE
    IF r_TMR_HydPress_TimerAB_ms > 0.0 THEN
        r_TMR_HydPress_TimerAB_ms := r_TMR_HydPress_TimerAB_ms - (r_CycleScanPeriod_ms * 2.0);
        IF r_TMR_HydPress_TimerAB_ms < 0.0 THEN
            r_TMR_HydPress_TimerAB_ms := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Pair BC Discrepancy Persistence Integration *)
IF (r_TMR_HydPress_DiffBC_bar > r_HydPressure_TMR_TolMax_bar) OR (NOT b_HydPressure_ValidB) OR (NOT b_HydPressure_ValidC) THEN
    r_TMR_HydPress_TimerBC_ms := r_TMR_HydPress_TimerBC_ms + r_CycleScanPeriod_ms;
ELSE
    IF r_TMR_HydPress_TimerBC_ms > 0.0 THEN
        r_TMR_HydPress_TimerBC_ms := r_TMR_HydPress_TimerBC_ms - (r_CycleScanPeriod_ms * 2.0);
        IF r_TMR_HydPress_TimerBC_ms < 0.0 THEN
            r_TMR_HydPress_TimerBC_ms := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Pair CA Discrepancy Persistence Integration *)
IF (r_TMR_HydPress_DiffCA_bar > r_HydPressure_TMR_TolMax_bar) OR (NOT b_HydPressure_ValidC) OR (NOT b_HydPressure_ValidA) THEN
    r_TMR_HydPress_TimerCA_ms := r_TMR_HydPress_TimerCA_ms + r_CycleScanPeriod_ms;
ELSE
    IF r_TMR_HydPress_TimerCA_ms > 0.0 THEN
        r_TMR_HydPress_TimerCA_ms := r_TMR_HydPress_TimerCA_ms - (r_CycleScanPeriod_ms * 2.0);
        IF r_TMR_HydPress_TimerCA_ms < 0.0 THEN
            r_TMR_HydPress_TimerCA_ms := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Sensor Fault Isolation Matrix for Pressure Channel *)
IF (r_TMR_HydPress_TimerAB_ms >= 50.0) AND (r_TMR_HydPress_TimerCA_ms >= 50.0) AND (r_TMR_HydPress_TimerBC_ms < 50.0) THEN
    b_TMR_HydPress_FaultA := TRUE;
END_IF;
IF (r_TMR_HydPress_TimerAB_ms >= 50.0) AND (r_TMR_HydPress_TimerBC_ms >= 50.0) AND (r_TMR_HydPress_TimerCA_ms < 50.0) THEN
    b_TMR_HydPress_FaultB := TRUE;
END_IF;
IF (r_TMR_HydPress_TimerBC_ms >= 50.0) AND (r_TMR_HydPress_TimerCA_ms >= 50.0) AND (r_TMR_HydPress_TimerAB_ms < 50.0) THEN
    b_TMR_HydPress_FaultC := TRUE;
END_IF;
IF NOT b_HydPressure_ValidA THEN
    b_TMR_HydPress_FaultA := TRUE;
END_IF;
IF NOT b_HydPressure_ValidB THEN
    b_TMR_HydPress_FaultB := TRUE;
END_IF;
IF NOT b_HydPressure_ValidC THEN
    b_TMR_HydPress_FaultC := TRUE;
END_IF;
IF b_ResetAllFaults THEN
    b_TMR_HydPress_FaultA := FALSE;
    b_TMR_HydPress_FaultB := FALSE;
    b_TMR_HydPress_FaultC := FALSE;
    b_TMR_HydPress_TotalFailure := FALSE;
    r_TMR_HydPress_TimerAB_ms := 0.0;
    r_TMR_HydPress_TimerBC_ms := 0.0;
    r_TMR_HydPress_TimerCA_ms := 0.0;
END_IF;

(* Degradation Voting Selection for Pressure Channel *)
IF (NOT b_TMR_HydPress_FaultA) AND (NOT b_TMR_HydPress_FaultB) AND (NOT b_TMR_HydPress_FaultC) THEN
    (* All 3 Channels Healthy: Exact Median Voting *)
    IF ((r_HydPressure_SensorA_bar >= r_HydPressure_SensorB_bar) AND (r_HydPressure_SensorA_bar <= r_HydPressure_SensorC_bar)) OR
       ((r_HydPressure_SensorA_bar >= r_HydPressure_SensorC_bar) AND (r_HydPressure_SensorA_bar <= r_HydPressure_SensorB_bar)) THEN
        r_TMR_VotedHydPressure_bar := r_HydPressure_SensorA_bar;
    ELSIF ((r_HydPressure_SensorB_bar >= r_HydPressure_SensorA_bar) AND (r_HydPressure_SensorB_bar <= r_HydPressure_SensorC_bar)) OR
          ((r_HydPressure_SensorB_bar >= r_HydPressure_SensorC_bar) AND (r_HydPressure_SensorB_bar <= r_HydPressure_SensorA_bar)) THEN
        r_TMR_VotedHydPressure_bar := r_HydPressure_SensorB_bar;
    ELSE
        r_TMR_VotedHydPressure_bar := r_HydPressure_SensorC_bar;
    END_IF;
    b_TMR_HydPressure_DegradedMode := FALSE;
    b_TMR_HydPress_TotalFailure := FALSE;
ELSIF b_TMR_HydPress_FaultA AND (NOT b_TMR_HydPress_FaultB) AND (NOT b_TMR_HydPress_FaultC) THEN
    (* Sensor A Faulted: Dual Redundant Mean of B and C *)
    r_TMR_VotedHydPressure_bar := 0.5 * (r_HydPressure_SensorB_bar + r_HydPressure_SensorC_bar);
    b_TMR_HydPressure_DegradedMode := TRUE;
ELSIF b_TMR_HydPress_FaultB AND (NOT b_TMR_HydPress_FaultA) AND (NOT b_TMR_HydPress_FaultC) THEN
    (* Sensor B Faulted: Dual Redundant Mean of A and C *)
    r_TMR_VotedHydPressure_bar := 0.5 * (r_HydPressure_SensorA_bar + r_HydPressure_SensorC_bar);
    b_TMR_HydPressure_DegradedMode := TRUE;
ELSIF b_TMR_HydPress_FaultC AND (NOT b_TMR_HydPress_FaultA) AND (NOT b_TMR_HydPress_FaultB) THEN
    (* Sensor C Faulted: Dual Redundant Mean of A and B *)
    r_TMR_VotedHydPressure_bar := 0.5 * (r_HydPressure_SensorA_bar + r_HydPressure_SensorB_bar);
    b_TMR_HydPressure_DegradedMode := TRUE;
ELSIF (NOT b_TMR_HydPress_FaultA) AND b_TMR_HydPress_FaultB AND b_TMR_HydPress_FaultC THEN
    (* Only Sensor A Healthy: Fallback Single Channel *)
    r_TMR_VotedHydPressure_bar := r_HydPressure_SensorA_bar;
    b_TMR_HydPressure_DegradedMode := TRUE;
ELSIF (NOT b_TMR_HydPress_FaultB) AND b_TMR_HydPress_FaultA AND b_TMR_HydPress_FaultC THEN
    (* Only Sensor B Healthy: Fallback Single Channel *)
    r_TMR_VotedHydPressure_bar := r_HydPressure_SensorB_bar;
    b_TMR_HydPressure_DegradedMode := TRUE;
ELSIF (NOT b_TMR_HydPress_FaultC) AND b_TMR_HydPress_FaultA AND b_TMR_HydPress_FaultB THEN
    (* Only Sensor C Healthy: Fallback Single Channel *)
    r_TMR_VotedHydPressure_bar := r_HydPressure_SensorC_bar;
    b_TMR_HydPressure_DegradedMode := TRUE;
ELSE
    (* All 3 Sensors Faulted: Total Channel Failure Lockout *)
    b_TMR_HydPress_TotalFailure := TRUE;
    b_TMR_HydPressure_DegradedMode := TRUE;
END_IF;

(* Bumpless Slew Rate Filter for Pressure (Max 250.0 bar/s = 0.25 bar/ms) *)
r_TmpDeltaU := r_TMR_VotedHydPressure_bar - r_TMR_HydPress_SlewFilt_bar;
IF r_TmpDeltaU > (0.25 * r_CycleScanPeriod_ms) THEN
    r_TMR_HydPress_SlewFilt_bar := r_TMR_HydPress_SlewFilt_bar + (0.25 * r_CycleScanPeriod_ms);
ELSIF r_TmpDeltaU < -(0.25 * r_CycleScanPeriod_ms) THEN
    r_TMR_HydPress_SlewFilt_bar := r_TMR_HydPress_SlewFilt_bar - (0.25 * r_CycleScanPeriod_ms);
ELSE
    r_TMR_HydPress_SlewFilt_bar := r_TMR_VotedHydPressure_bar;
END_IF;
r_TMR_VotedHydPressure_bar := r_TMR_HydPress_SlewFilt_bar;

(* ---------------------------------------------------------------------------------------------------- *)
(* CHANNEL 3: UPPER DIE INDUCTION CORE TEMPERATURE 2oo3 VOTING ENGINE [deg C]                           *)
(* Transducers: Sensor A (Type-B Thermocouple Core 1), Sensor B (Type-B Thermocouple Core 2),           *)
(*              Sensor C (Two-Color Optical Infrared Ratio Pyrometer 3). Nominal: 950.0 deg C.          *)
(* Discrepancy Tolerance: 15.0 deg C. Persistence Watchdog: 50.0 ms. Slew Limit: 20.0 deg C/s.          *)
(* ---------------------------------------------------------------------------------------------------- *)
r_TMR_DieTemp_DiffAB_DegC := ABS(r_DieTemp_SensorA_DegC - r_DieTemp_SensorB_DegC);
r_TMR_DieTemp_DiffBC_DegC := ABS(r_DieTemp_SensorB_DegC - r_DieTemp_SensorC_DegC);
r_TMR_DieTemp_DiffCA_DegC := ABS(r_DieTemp_SensorC_DegC - r_DieTemp_SensorA_DegC);

(* Pair AB Discrepancy Persistence Integration *)
IF (r_TMR_DieTemp_DiffAB_DegC > r_DieTemp_TMR_TolMax_DegC) OR (NOT b_DieTemp_ValidA) OR (NOT b_DieTemp_ValidB) THEN
    r_TMR_DieTemp_TimerAB_ms := r_TMR_DieTemp_TimerAB_ms + r_CycleScanPeriod_ms;
ELSE
    IF r_TMR_DieTemp_TimerAB_ms > 0.0 THEN
        r_TMR_DieTemp_TimerAB_ms := r_TMR_DieTemp_TimerAB_ms - (r_CycleScanPeriod_ms * 2.0);
        IF r_TMR_DieTemp_TimerAB_ms < 0.0 THEN
            r_TMR_DieTemp_TimerAB_ms := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Pair BC Discrepancy Persistence Integration *)
IF (r_TMR_DieTemp_DiffBC_DegC > r_DieTemp_TMR_TolMax_DegC) OR (NOT b_DieTemp_ValidB) OR (NOT b_DieTemp_ValidC) THEN
    r_TMR_DieTemp_TimerBC_ms := r_TMR_DieTemp_TimerBC_ms + r_CycleScanPeriod_ms;
ELSE
    IF r_TMR_DieTemp_TimerBC_ms > 0.0 THEN
        r_TMR_DieTemp_TimerBC_ms := r_TMR_DieTemp_TimerBC_ms - (r_CycleScanPeriod_ms * 2.0);
        IF r_TMR_DieTemp_TimerBC_ms < 0.0 THEN
            r_TMR_DieTemp_TimerBC_ms := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Pair CA Discrepancy Persistence Integration *)
IF (r_TMR_DieTemp_DiffCA_DegC > r_DieTemp_TMR_TolMax_DegC) OR (NOT b_DieTemp_ValidC) OR (NOT b_DieTemp_ValidA) THEN
    r_TMR_DieTemp_TimerCA_ms := r_TMR_DieTemp_TimerCA_ms + r_CycleScanPeriod_ms;
ELSE
    IF r_TMR_DieTemp_TimerCA_ms > 0.0 THEN
        r_TMR_DieTemp_TimerCA_ms := r_TMR_DieTemp_TimerCA_ms - (r_CycleScanPeriod_ms * 2.0);
        IF r_TMR_DieTemp_TimerCA_ms < 0.0 THEN
            r_TMR_DieTemp_TimerCA_ms := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Sensor Fault Isolation Matrix for Die Temperature Channel *)
IF (r_TMR_DieTemp_TimerAB_ms >= 50.0) AND (r_TMR_DieTemp_TimerCA_ms >= 50.0) AND (r_TMR_DieTemp_TimerBC_ms < 50.0) THEN
    b_TMR_DieTemp_FaultA := TRUE;
END_IF;
IF (r_TMR_DieTemp_TimerAB_ms >= 50.0) AND (r_TMR_DieTemp_TimerBC_ms >= 50.0) AND (r_TMR_DieTemp_TimerCA_ms < 50.0) THEN
    b_TMR_DieTemp_FaultB := TRUE;
END_IF;
IF (r_TMR_DieTemp_TimerBC_ms >= 50.0) AND (r_TMR_DieTemp_TimerCA_ms >= 50.0) AND (r_TMR_DieTemp_TimerAB_ms < 50.0) THEN
    b_TMR_DieTemp_FaultC := TRUE;
END_IF;
IF NOT b_DieTemp_ValidA THEN
    b_TMR_DieTemp_FaultA := TRUE;
END_IF;
IF NOT b_DieTemp_ValidB THEN
    b_TMR_DieTemp_FaultB := TRUE;
END_IF;
IF NOT b_DieTemp_ValidC THEN
    b_TMR_DieTemp_FaultC := TRUE;
END_IF;
IF b_ResetAllFaults THEN
    b_TMR_DieTemp_FaultA := FALSE;
    b_TMR_DieTemp_FaultB := FALSE;
    b_TMR_DieTemp_FaultC := FALSE;
    b_TMR_DieTemp_TotalFailure := FALSE;
    r_TMR_DieTemp_TimerAB_ms := 0.0;
    r_TMR_DieTemp_TimerBC_ms := 0.0;
    r_TMR_DieTemp_TimerCA_ms := 0.0;
END_IF;

(* Degradation Voting Selection for Die Temperature Channel *)
IF (NOT b_TMR_DieTemp_FaultA) AND (NOT b_TMR_DieTemp_FaultB) AND (NOT b_TMR_DieTemp_FaultC) THEN
    (* All 3 Channels Healthy: Exact Median Voting *)
    IF ((r_DieTemp_SensorA_DegC >= r_DieTemp_SensorB_DegC) AND (r_DieTemp_SensorA_DegC <= r_DieTemp_SensorC_DegC)) OR
       ((r_DieTemp_SensorA_DegC >= r_DieTemp_SensorC_DegC) AND (r_DieTemp_SensorA_DegC <= r_DieTemp_SensorB_DegC)) THEN
        r_TMR_VotedDieTemp_DegC := r_DieTemp_SensorA_DegC;
    ELSIF ((r_DieTemp_SensorB_DegC >= r_DieTemp_SensorA_DegC) AND (r_DieTemp_SensorB_DegC <= r_DieTemp_SensorC_DegC)) OR
          ((r_DieTemp_SensorB_DegC >= r_DieTemp_SensorC_DegC) AND (r_DieTemp_SensorB_DegC <= r_DieTemp_SensorA_DegC)) THEN
        r_TMR_VotedDieTemp_DegC := r_DieTemp_SensorB_DegC;
    ELSE
        r_TMR_VotedDieTemp_DegC := r_DieTemp_SensorC_DegC;
    END_IF;
    b_TMR_DieTemp_DegradedMode := FALSE;
    b_TMR_DieTemp_TotalFailure := FALSE;
ELSIF b_TMR_DieTemp_FaultA AND (NOT b_TMR_DieTemp_FaultB) AND (NOT b_TMR_DieTemp_FaultC) THEN
    (* Sensor A Faulted: Dual Redundant Mean of B and C *)
    r_TMR_VotedDieTemp_DegC := 0.5 * (r_DieTemp_SensorB_DegC + r_DieTemp_SensorC_DegC);
    b_TMR_DieTemp_DegradedMode := TRUE;
ELSIF b_TMR_DieTemp_FaultB AND (NOT b_TMR_DieTemp_FaultA) AND (NOT b_TMR_DieTemp_FaultC) THEN
    (* Sensor B Faulted: Dual Redundant Mean of A and C *)
    r_TMR_VotedDieTemp_DegC := 0.5 * (r_DieTemp_SensorA_DegC + r_DieTemp_SensorC_DegC);
    b_TMR_DieTemp_DegradedMode := TRUE;
ELSIF b_TMR_DieTemp_FaultC AND (NOT b_TMR_DieTemp_FaultA) AND (NOT b_TMR_DieTemp_FaultB) THEN
    (* Sensor C Faulted: Dual Redundant Mean of A and B *)
    r_TMR_VotedDieTemp_DegC := 0.5 * (r_DieTemp_SensorA_DegC + r_DieTemp_SensorB_DegC);
    b_TMR_DieTemp_DegradedMode := TRUE;
ELSIF (NOT b_TMR_DieTemp_FaultA) AND b_TMR_DieTemp_FaultB AND b_TMR_DieTemp_FaultC THEN
    (* Only Sensor A Healthy: Fallback Single Channel *)
    r_TMR_VotedDieTemp_DegC := r_DieTemp_SensorA_DegC;
    b_TMR_DieTemp_DegradedMode := TRUE;
ELSIF (NOT b_TMR_DieTemp_FaultB) AND b_TMR_DieTemp_FaultA AND b_TMR_DieTemp_FaultC THEN
    (* Only Sensor B Healthy: Fallback Single Channel *)
    r_TMR_VotedDieTemp_DegC := r_DieTemp_SensorB_DegC;
    b_TMR_DieTemp_DegradedMode := TRUE;
ELSIF (NOT b_TMR_DieTemp_FaultC) AND b_TMR_DieTemp_FaultA AND b_TMR_DieTemp_FaultB THEN
    (* Only Sensor C Healthy: Fallback Single Channel *)
    r_TMR_VotedDieTemp_DegC := r_DieTemp_SensorC_DegC;
    b_TMR_DieTemp_DegradedMode := TRUE;
ELSE
    (* All 3 Sensors Faulted: Total Channel Failure Lockout *)
    b_TMR_DieTemp_TotalFailure := TRUE;
    b_TMR_DieTemp_DegradedMode := TRUE;
END_IF;

(* Bumpless Slew Rate Filter for Die Temp (Max 20.0 deg C/s = 0.02 deg C/ms) *)
r_TmpDeltaU := r_TMR_VotedDieTemp_DegC - r_TMR_DieTemp_SlewFilt_DegC;
IF r_TmpDeltaU > (0.02 * r_CycleScanPeriod_ms) THEN
    r_TMR_DieTemp_SlewFilt_DegC := r_TMR_DieTemp_SlewFilt_DegC + (0.02 * r_CycleScanPeriod_ms);
ELSIF r_TmpDeltaU < -(0.02 * r_CycleScanPeriod_ms) THEN
    r_TMR_DieTemp_SlewFilt_DegC := r_TMR_DieTemp_SlewFilt_DegC - (0.02 * r_CycleScanPeriod_ms);
ELSE
    r_TMR_DieTemp_SlewFilt_DegC := r_TMR_VotedDieTemp_DegC;
END_IF;
r_TMR_VotedDieTemp_DegC := r_TMR_DieTemp_SlewFilt_DegC;

(* ---------------------------------------------------------------------------------------------------- *)
(* CHANNEL 4: 4-CORNER RAM LEVELING TILT SKEW DEVIATION 2oo3 VOTING ENGINE [um]                          *)
(* Transducers: Sensor A (Optical Glass Scale Network A), Sensor B (Optical Glass Scale Network B),      *)
(*              Sensor C (Absolute Magnetostrictive Network C). Nominal: 0.0 um. Limit: +/- 20.0 um.     *)
(* Discrepancy Tolerance: 8.0 um. Persistence Watchdog: 50.0 ms. Slew Limit: 500.0 um/s.                *)
(* ---------------------------------------------------------------------------------------------------- *)
r_TMR_TiltSkew_DiffAB_um := ABS(r_TiltSkew_SensorA_um - r_TiltSkew_SensorB_um);
r_TMR_TiltSkew_DiffBC_um := ABS(r_TiltSkew_SensorB_um - r_TiltSkew_SensorC_um);
r_TMR_TiltSkew_DiffCA_um := ABS(r_TiltSkew_SensorC_um - r_TiltSkew_SensorA_um);

(* Pair AB Discrepancy Persistence Integration *)
IF (r_TMR_TiltSkew_DiffAB_um > r_TiltSkew_TMR_TolMax_um) OR (NOT b_TiltSkew_ValidA) OR (NOT b_TiltSkew_ValidB) THEN
    r_TMR_TiltSkew_TimerAB_ms := r_TMR_TiltSkew_TimerAB_ms + r_CycleScanPeriod_ms;
ELSE
    IF r_TMR_TiltSkew_TimerAB_ms > 0.0 THEN
        r_TMR_TiltSkew_TimerAB_ms := r_TMR_TiltSkew_TimerAB_ms - (r_CycleScanPeriod_ms * 2.0);
        IF r_TMR_TiltSkew_TimerAB_ms < 0.0 THEN
            r_TMR_TiltSkew_TimerAB_ms := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Pair BC Discrepancy Persistence Integration *)
IF (r_TMR_TiltSkew_DiffBC_um > r_TiltSkew_TMR_TolMax_um) OR (NOT b_TiltSkew_ValidB) OR (NOT b_TiltSkew_ValidC) THEN
    r_TMR_TiltSkew_TimerBC_ms := r_TMR_TiltSkew_TimerBC_ms + r_CycleScanPeriod_ms;
ELSE
    IF r_TMR_TiltSkew_TimerBC_ms > 0.0 THEN
        r_TMR_TiltSkew_TimerBC_ms := r_TMR_TiltSkew_TimerBC_ms - (r_CycleScanPeriod_ms * 2.0);
        IF r_TMR_TiltSkew_TimerBC_ms < 0.0 THEN
            r_TMR_TiltSkew_TimerBC_ms := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Pair CA Discrepancy Persistence Integration *)
IF (r_TMR_TiltSkew_DiffCA_um > r_TiltSkew_TMR_TolMax_um) OR (NOT b_TiltSkew_ValidC) OR (NOT b_TiltSkew_ValidA) THEN
    r_TMR_TiltSkew_TimerCA_ms := r_TMR_TiltSkew_TimerCA_ms + r_CycleScanPeriod_ms;
ELSE
    IF r_TMR_TiltSkew_TimerCA_ms > 0.0 THEN
        r_TMR_TiltSkew_TimerCA_ms := r_TMR_TiltSkew_TimerCA_ms - (r_CycleScanPeriod_ms * 2.0);
        IF r_TMR_TiltSkew_TimerCA_ms < 0.0 THEN
            r_TMR_TiltSkew_TimerCA_ms := 0.0;
        END_IF;
    END_IF;
END_IF;

(* Sensor Fault Isolation Matrix for Tilt Skew Channel *)
IF (r_TMR_TiltSkew_TimerAB_ms >= 50.0) AND (r_TMR_TiltSkew_TimerCA_ms >= 50.0) AND (r_TMR_TiltSkew_TimerBC_ms < 50.0) THEN
    b_TMR_TiltSkew_FaultA := TRUE;
END_IF;
IF (r_TMR_TiltSkew_TimerAB_ms >= 50.0) AND (r_TMR_TiltSkew_TimerBC_ms >= 50.0) AND (r_TMR_TiltSkew_TimerCA_ms < 50.0) THEN
    b_TMR_TiltSkew_FaultB := TRUE;
END_IF;
IF (r_TMR_TiltSkew_TimerBC_ms >= 50.0) AND (r_TMR_TiltSkew_TimerCA_ms >= 50.0) AND (r_TMR_TiltSkew_TimerAB_ms < 50.0) THEN
    b_TMR_TiltSkew_FaultC := TRUE;
END_IF;
IF NOT b_TiltSkew_ValidA THEN
    b_TMR_TiltSkew_FaultA := TRUE;
END_IF;
IF NOT b_TiltSkew_ValidB THEN
    b_TMR_TiltSkew_FaultB := TRUE;
END_IF;
IF NOT b_TiltSkew_ValidC THEN
    b_TMR_TiltSkew_FaultC := TRUE;
END_IF;
IF b_ResetAllFaults THEN
    b_TMR_TiltSkew_FaultA := FALSE;
    b_TMR_TiltSkew_FaultB := FALSE;
    b_TMR_TiltSkew_FaultC := FALSE;
    b_TMR_TiltSkew_TotalFailure := FALSE;
    r_TMR_TiltSkew_TimerAB_ms := 0.0;
    r_TMR_TiltSkew_TimerBC_ms := 0.0;
    r_TMR_TiltSkew_TimerCA_ms := 0.0;
END_IF;

(* Degradation Voting Selection for Tilt Skew Channel *)
IF (NOT b_TMR_TiltSkew_FaultA) AND (NOT b_TMR_TiltSkew_FaultB) AND (NOT b_TMR_TiltSkew_FaultC) THEN
    (* All 3 Channels Healthy: Exact Median Voting *)
    IF ((r_TiltSkew_SensorA_um >= r_TiltSkew_SensorB_um) AND (r_TiltSkew_SensorA_um <= r_TiltSkew_SensorC_um)) OR
       ((r_TiltSkew_SensorA_um >= r_TiltSkew_SensorC_um) AND (r_TiltSkew_SensorA_um <= r_TiltSkew_SensorB_um)) THEN
        r_TMR_VotedTiltSkew_um := r_TiltSkew_SensorA_um;
    ELSIF ((r_TiltSkew_SensorB_um >= r_TiltSkew_SensorA_um) AND (r_TiltSkew_SensorB_um <= r_TiltSkew_SensorC_um)) OR
          ((r_TiltSkew_SensorB_um >= r_TiltSkew_SensorC_um) AND (r_TiltSkew_SensorB_um <= r_TiltSkew_SensorA_um)) THEN
        r_TMR_VotedTiltSkew_um := r_TiltSkew_SensorB_um;
    ELSE
        r_TMR_VotedTiltSkew_um := r_TiltSkew_SensorC_um;
    END_IF;
    b_TMR_TiltSkew_DegradedMode := FALSE;
    b_TMR_TiltSkew_TotalFailure := FALSE;
ELSIF b_TMR_TiltSkew_FaultA AND (NOT b_TMR_TiltSkew_FaultB) AND (NOT b_TMR_TiltSkew_FaultC) THEN
    (* Sensor A Faulted: Dual Redundant Mean of B and C *)
    r_TMR_VotedTiltSkew_um := 0.5 * (r_TiltSkew_SensorB_um + r_TiltSkew_SensorC_um);
    b_TMR_TiltSkew_DegradedMode := TRUE;
ELSIF b_TMR_TiltSkew_FaultB AND (NOT b_TMR_TiltSkew_FaultA) AND (NOT b_TMR_TiltSkew_FaultC) THEN
    (* Sensor B Faulted: Dual Redundant Mean of A and C *)
    r_TMR_VotedTiltSkew_um := 0.5 * (r_TiltSkew_SensorA_um + r_TiltSkew_SensorC_um);
    b_TMR_TiltSkew_DegradedMode := TRUE;
ELSIF b_TMR_TiltSkew_FaultC AND (NOT b_TMR_TiltSkew_FaultA) AND (NOT b_TMR_TiltSkew_FaultB) THEN
    (* Sensor C Faulted: Dual Redundant Mean of A and B *)
    r_TMR_VotedTiltSkew_um := 0.5 * (r_TiltSkew_SensorA_um + r_TiltSkew_SensorB_um);
    b_TMR_TiltSkew_DegradedMode := TRUE;
ELSIF (NOT b_TMR_TiltSkew_FaultA) AND b_TMR_TiltSkew_FaultB AND b_TMR_TiltSkew_FaultC THEN
    (* Only Sensor A Healthy: Fallback Single Channel *)
    r_TMR_VotedTiltSkew_um := r_TiltSkew_SensorA_um;
    b_TMR_TiltSkew_DegradedMode := TRUE;
ELSIF (NOT b_TMR_TiltSkew_FaultB) AND b_TMR_TiltSkew_FaultA AND b_TMR_TiltSkew_FaultC THEN
    (* Only Sensor B Healthy: Fallback Single Channel *)
    r_TMR_VotedTiltSkew_um := r_TiltSkew_SensorB_um;
    b_TMR_TiltSkew_DegradedMode := TRUE;
ELSIF (NOT b_TMR_TiltSkew_FaultC) AND b_TMR_TiltSkew_FaultA AND b_TMR_TiltSkew_FaultB THEN
    (* Only Sensor C Healthy: Fallback Single Channel *)
    r_TMR_VotedTiltSkew_um := r_TiltSkew_SensorC_um;
    b_TMR_TiltSkew_DegradedMode := TRUE;
ELSE
    (* All 3 Sensors Faulted: Total Channel Failure Lockout *)
    b_TMR_TiltSkew_TotalFailure := TRUE;
    b_TMR_TiltSkew_DegradedMode := TRUE;
END_IF;

(* Bumpless Slew Rate Filter for Tilt Skew (Max 500.0 um/s = 0.5 um/ms) *)
r_TmpDeltaU := r_TMR_VotedTiltSkew_um - r_TMR_TiltSkew_SlewFilt_um;
IF r_TmpDeltaU > (0.5 * r_CycleScanPeriod_ms) THEN
    r_TMR_TiltSkew_SlewFilt_um := r_TMR_TiltSkew_SlewFilt_um + (0.5 * r_CycleScanPeriod_ms);
ELSIF r_TmpDeltaU < -(0.5 * r_CycleScanPeriod_ms) THEN
    r_TMR_TiltSkew_SlewFilt_um := r_TMR_TiltSkew_SlewFilt_um - (0.5 * r_CycleScanPeriod_ms);
ELSE
    r_TMR_TiltSkew_SlewFilt_um := r_TMR_VotedTiltSkew_um;
END_IF;
r_TMR_VotedTiltSkew_um := r_TMR_TiltSkew_SlewFilt_um;

(* ---------------------------------------------------------------------------------------------------- *)
(* 4-CORNER HYDRAULIC FORCE SYNCHRONIZATION, MOMENT RESOLUTION & GEOMETRIC TILT CALCULATION             *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Convert Cylinder Chamber Pressures [bar] to Dynamic Actuator Axial Forces [kN]:                     *)
(* Force F [kN] = Pressure P [bar] * 100.0 [kPa/bar] * Area A [m2] = P * A * 100.0                      *)
r_CylForce_FL_kN := r_CylPressure_FL_bar * C_CYL_BORE_AREA_M2 * 100.0;
r_CylForce_FR_kN := r_CylPressure_FR_bar * C_CYL_BORE_AREA_M2 * 100.0;
r_CylForce_RL_kN := r_CylPressure_RL_bar * C_CYL_BORE_AREA_M2 * 100.0;
r_CylForce_RR_kN := r_CylPressure_RR_bar * C_CYL_BORE_AREA_M2 * 100.0;
r_TotalCylForce_kN := r_CylForce_FL_kN + r_CylForce_FR_kN + r_CylForce_RL_kN + r_CylForce_RR_kN;

(* Calculate Dynamic Eccentric Tilting Moments [kNm] about the Press Platen Geometric Neutral Axes:     *)
(* Mx = [(F_FL + F_FR) - (F_RL + F_RR)] * (Platen_Span / 2)                                              *)
(* My = [(F_FL + F_RL) - (F_FR + F_RR)] * (Platen_Span / 2)                                              *)
r_EccentricMomentX_kNm := ((r_CylForce_FL_kN + r_CylForce_FR_kN) - (r_CylForce_RL_kN + r_CylForce_RR_kN)) * C_PLATEN_HALF_SPAN_M;
r_EccentricMomentY_kNm := ((r_CylForce_FL_kN + r_CylForce_RL_kN) - (r_CylForce_FR_kN + r_CylForce_RR_kN)) * C_PLATEN_HALF_SPAN_M;

(* Corner Deflection Deviations [um] Relative to Mean Stroke Plane *)
r_CornerTilt_FL_um := (r_CylPosition_FL_mm - ((r_CylPosition_FL_mm + r_CylPosition_FR_mm + r_CylPosition_RL_mm + r_CylPosition_RR_mm) * 0.25)) * 1000.0;
r_CornerTilt_FR_um := (r_CylPosition_FR_mm - ((r_CylPosition_FL_mm + r_CylPosition_FR_mm + r_CylPosition_RL_mm + r_CylPosition_RR_mm) * 0.25)) * 1000.0;
r_CornerTilt_RL_um := (r_CylPosition_RL_mm - ((r_CylPosition_FL_mm + r_CylPosition_FR_mm + r_CylPosition_RL_mm + r_CylPosition_RR_mm) * 0.25)) * 1000.0;
r_CornerTilt_RR_um := (r_CylPosition_RR_mm - ((r_CylPosition_FL_mm + r_CylPosition_FR_mm + r_CylPosition_RL_mm + r_CylPosition_RR_mm) * 0.25)) * 1000.0;

(* Determine Maximum Geometric Platen Skew Deviation [um] across Diagonal Cylinder Pairs *)
r_MaxCornerTiltDev_um := MAX(ABS(r_CornerTilt_FL_um - r_CornerTilt_RR_um), ABS(r_CornerTilt_FR_um - r_CornerTilt_RL_um));
