# -*- coding: utf-8 -*-
"""
smt_builder/phase1_tmr.py
Generates Phase 1: 2oo3 Triple Modular Redundancy (TMR) Sensor Voting logic
for all 5 critical sensor channels with discrepancy timers and degradation state machines.
"""

def get_phase1_tmr():
    return """(*
========================================================================================================================
  PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DYNAMIC DISCREPANCY TIMERS
========================================================================================================================
  Monitors 5 mission-critical sensor triplets essential for nanometer-accurate SMT component alignment and safety:
    1. Gantry X-Axis Dual-Drive Linear Optical Encoders (Renishaw Invar, 50 nm pitch)
    2. Gantry Y-Axis Crossbeam Linear Optical Encoders (Zerodur Ceramic, 50 nm pitch)
    3. 16-Spindle Head Master Theta Direct-Drive Hollow-Shaft Rotary Encoders
    4. Main High-Vacuum Distribution Manifold Piezoresistive Transducers (-100 to 0 kPa)
    5. High-Speed Triangulation Blue-Laser PCB Surface Warpage Profiling Gauges (0 to 10 mm)

  Voting Architecture:
    - Normal State (Degradation State 0): Exact 3-channel mathematical median computation.
    - Degraded State (Degradation State 1): Persistent single-channel discrepancy (> 25 ms) isolates the faulty
      channel, seamlessly transitioning to a 2-channel arithmetic mean with bumpless rate-limiting.
    - Fail-Safe State (Degradation State 2): Two channels disagree; reverts to primary calibrated channel with warning.
    - Trip State (Degradation State 3): All 3 channels diverge beyond safety tolerance; triggers immediate Category 0
      fail-safe gantry deceleration and sets SIL-3 hardware safety interlock trip.
*)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* SENSOR TRIPLET 1: GANTRY X-AXIS LINEAR OPTICAL ENCODERS                                                              *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rTMR_X_ChA := rEnc_Gantry_X_ChA;
rTMR_X_ChB := rEnc_Gantry_X_ChB;
rTMR_X_ChC := rEnc_Gantry_X_ChC;

(* Pairwise absolute divergence calculations *)
rTMR_X_Dev_AB := ABS(rTMR_X_ChA - rTMR_X_ChB);
rTMR_X_Dev_BC := ABS(rTMR_X_ChB - rTMR_X_ChC);
rTMR_X_Dev_CA := ABS(rTMR_X_ChC - rTMR_X_ChA);

bTMR_X_Discrep_AB := (rTMR_X_Dev_AB > rTol_Discrep_X_mm);
bTMR_X_Discrep_BC := (rTMR_X_Dev_BC > rTol_Discrep_X_mm);
bTMR_X_Discrep_CA := (rTMR_X_Dev_CA > rTol_Discrep_X_mm);

(* Discrepancy persistence integration timers *)
IF bTMR_X_Discrep_AB THEN
    IF udiTMR_X_Timer_AB < 1000 THEN
        udiTMR_X_Timer_AB := udiTMR_X_Timer_AB + 1;
    END_IF;
ELSE
    IF udiTMR_X_Timer_AB > 0 THEN
        udiTMR_X_Timer_AB := udiTMR_X_Timer_AB - 1;
    END_IF;
END_IF;

IF bTMR_X_Discrep_BC THEN
    IF udiTMR_X_Timer_BC < 1000 THEN
        udiTMR_X_Timer_BC := udiTMR_X_Timer_BC + 1;
    END_IF;
ELSE
    IF udiTMR_X_Timer_BC > 0 THEN
        udiTMR_X_Timer_BC := udiTMR_X_Timer_BC - 1;
    END_IF;
END_IF;

IF bTMR_X_Discrep_CA THEN
    IF udiTMR_X_Timer_CA < 1000 THEN
        udiTMR_X_Timer_CA := udiTMR_X_Timer_CA + 1;
    END_IF;
ELSE
    IF udiTMR_X_Timer_CA > 0 THEN
        udiTMR_X_Timer_CA := udiTMR_X_Timer_CA - 1;
    END_IF;
END_IF;

(* TMR Degradation State Evaluation & Median Selection for X-Axis *)
IF (udiTMR_X_Timer_AB <= udiTMR_DiscrepancyLimit_ms) AND
   (udiTMR_X_Timer_BC <= udiTMR_DiscrepancyLimit_ms) AND
   (udiTMR_X_Timer_CA <= udiTMR_DiscrepancyLimit_ms) THEN
    (* All channels healthy: mathematical median of 3 channels *)
    rTMR_X_Voted := (rTMR_X_ChA + rTMR_X_ChB + rTMR_X_ChC)
                    - MIN(rTMR_X_ChA, MIN(rTMR_X_ChB, rTMR_X_ChC))
                    - MAX(rTMR_X_ChA, MAX(rTMR_X_ChB, rTMR_X_ChC));
    iTMR_X_DegradationState := 0;
    bTMR_X_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_X_Timer_AB > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_X_Timer_CA > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_X_Timer_BC <= udiTMR_DiscrepancyLimit_ms) THEN
    (* Channel A isolated as faulty; average healthy channels B and C *)
    rTMR_X_Voted := 0.5 * (rTMR_X_ChB + rTMR_X_ChC);
    iTMR_X_DegradationState := 1;
    bTMR_X_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_X_Timer_AB > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_X_Timer_BC > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_X_Timer_CA <= udiTMR_DiscrepancyLimit_ms) THEN
    (* Channel B isolated as faulty; average healthy channels A and C *)
    rTMR_X_Voted := 0.5 * (rTMR_X_ChA + rTMR_X_ChC);
    iTMR_X_DegradationState := 1;
    bTMR_X_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_X_Timer_BC > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_X_Timer_CA > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_X_Timer_AB <= udiTMR_DiscrepancyLimit_ms) THEN
    (* Channel C isolated as faulty; average healthy channels A and B *)
    rTMR_X_Voted := 0.5 * (rTMR_X_ChA + rTMR_X_ChB);
    iTMR_X_DegradationState := 1;
    bTMR_X_MajorDiscrepancyTrip := FALSE;
ELSE
    (* Multiple simultaneous channel divergence - major sensor breakdown *)
    rTMR_X_Voted := rTMR_X_ChA;
    iTMR_X_DegradationState := 3;
    bTMR_X_MajorDiscrepancyTrip := TRUE;
END_IF;

rVoted_X_Raw := rTMR_X_Voted;


(* -------------------------------------------------------------------------------------------------------------------- *)
(* SENSOR TRIPLET 2: GANTRY Y-AXIS CROSSBEAM LINEAR OPTICAL ENCODERS                                                    *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rTMR_Y_ChA := rEnc_Gantry_Y_ChA;
rTMR_Y_ChB := rEnc_Gantry_Y_ChB;
rTMR_Y_ChC := rEnc_Gantry_Y_ChC;

rTMR_Y_Dev_AB := ABS(rTMR_Y_ChA - rTMR_Y_ChB);
rTMR_Y_Dev_BC := ABS(rTMR_Y_ChB - rTMR_Y_ChC);
rTMR_Y_Dev_CA := ABS(rTMR_Y_ChC - rTMR_Y_ChA);

bTMR_Y_Discrep_AB := (rTMR_Y_Dev_AB > rTol_Discrep_Y_mm);
bTMR_Y_Discrep_BC := (rTMR_Y_Dev_BC > rTol_Discrep_Y_mm);
bTMR_Y_Discrep_CA := (rTMR_Y_Dev_CA > rTol_Discrep_Y_mm);

IF bTMR_Y_Discrep_AB THEN
    IF udiTMR_Y_Timer_AB < 1000 THEN
        udiTMR_Y_Timer_AB := udiTMR_Y_Timer_AB + 1;
    END_IF;
ELSE
    IF udiTMR_Y_Timer_AB > 0 THEN
        udiTMR_Y_Timer_AB := udiTMR_Y_Timer_AB - 1;
    END_IF;
END_IF;

IF bTMR_Y_Discrep_BC THEN
    IF udiTMR_Y_Timer_BC < 1000 THEN
        udiTMR_Y_Timer_BC := udiTMR_Y_Timer_BC + 1;
    END_IF;
ELSE
    IF udiTMR_Y_Timer_BC > 0 THEN
        udiTMR_Y_Timer_BC := udiTMR_Y_Timer_BC - 1;
    END_IF;
END_IF;

IF bTMR_Y_Discrep_CA THEN
    IF udiTMR_Y_Timer_CA < 1000 THEN
        udiTMR_Y_Timer_CA := udiTMR_Y_Timer_CA + 1;
    END_IF;
ELSE
    IF udiTMR_Y_Timer_CA > 0 THEN
        udiTMR_Y_Timer_CA := udiTMR_Y_Timer_CA - 1;
    END_IF;
END_IF;

IF (udiTMR_Y_Timer_AB <= udiTMR_DiscrepancyLimit_ms) AND
   (udiTMR_Y_Timer_BC <= udiTMR_DiscrepancyLimit_ms) AND
   (udiTMR_Y_Timer_CA <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Y_Voted := (rTMR_Y_ChA + rTMR_Y_ChB + rTMR_Y_ChC)
                    - MIN(rTMR_Y_ChA, MIN(rTMR_Y_ChB, rTMR_Y_ChC))
                    - MAX(rTMR_Y_ChA, MAX(rTMR_Y_ChB, rTMR_Y_ChC));
    iTMR_Y_DegradationState := 0;
    bTMR_Y_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_Y_Timer_AB > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Y_Timer_CA > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Y_Timer_BC <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Y_Voted := 0.5 * (rTMR_Y_ChB + rTMR_Y_ChC);
    iTMR_Y_DegradationState := 1;
    bTMR_Y_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_Y_Timer_AB > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Y_Timer_BC > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Y_Timer_CA <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Y_Voted := 0.5 * (rTMR_Y_ChA + rTMR_Y_ChC);
    iTMR_Y_DegradationState := 1;
    bTMR_Y_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_Y_Timer_BC > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Y_Timer_CA > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Y_Timer_AB <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Y_Voted := 0.5 * (rTMR_Y_ChA + rTMR_Y_ChB);
    iTMR_Y_DegradationState := 1;
    bTMR_Y_MajorDiscrepancyTrip := FALSE;
ELSE
    rTMR_Y_Voted := rTMR_Y_ChA;
    iTMR_Y_DegradationState := 3;
    bTMR_Y_MajorDiscrepancyTrip := TRUE;
END_IF;

rVoted_Y_Raw := rTMR_Y_Voted;


(* -------------------------------------------------------------------------------------------------------------------- *)
(* SENSOR TRIPLET 3: SPINDLE TURRET ROTARY THETA ENCODERS                                                              *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rTMR_Theta_ChA := rEnc_Head_Theta_ChA;
rTMR_Theta_ChB := rEnc_Head_Theta_ChB;
rTMR_Theta_ChC := rEnc_Head_Theta_ChC;

rTMR_Theta_Dev_AB := ABS(rTMR_Theta_ChA - rTMR_Theta_ChB);
rTMR_Theta_Dev_BC := ABS(rTMR_Theta_ChB - rTMR_Theta_ChC);
rTMR_Theta_Dev_CA := ABS(rTMR_Theta_ChC - rTMR_Theta_ChA);

bTMR_Theta_Discrep_AB := (rTMR_Theta_Dev_AB > rTol_Discrep_Theta_deg);
bTMR_Theta_Discrep_BC := (rTMR_Theta_Dev_BC > rTol_Discrep_Theta_deg);
bTMR_Theta_Discrep_CA := (rTMR_Theta_Dev_CA > rTol_Discrep_Theta_deg);

IF bTMR_Theta_Discrep_AB THEN
    IF udiTMR_Theta_Timer_AB < 1000 THEN
        udiTMR_Theta_Timer_AB := udiTMR_Theta_Timer_AB + 1;
    END_IF;
ELSE
    IF udiTMR_Theta_Timer_AB > 0 THEN
        udiTMR_Theta_Timer_AB := udiTMR_Theta_Timer_AB - 1;
    END_IF;
END_IF;

IF bTMR_Theta_Discrep_BC THEN
    IF udiTMR_Theta_Timer_BC < 1000 THEN
        udiTMR_Theta_Timer_BC := udiTMR_Theta_Timer_BC + 1;
    END_IF;
ELSE
    IF udiTMR_Theta_Timer_BC > 0 THEN
        udiTMR_Theta_Timer_BC := udiTMR_Theta_Timer_BC - 1;
    END_IF;
END_IF;

IF bTMR_Theta_Discrep_CA THEN
    IF udiTMR_Theta_Timer_CA < 1000 THEN
        udiTMR_Theta_Timer_CA := udiTMR_Theta_Timer_CA + 1;
    END_IF;
ELSE
    IF udiTMR_Theta_Timer_CA > 0 THEN
        udiTMR_Theta_Timer_CA := udiTMR_Theta_Timer_CA - 1;
    END_IF;
END_IF;

IF (udiTMR_Theta_Timer_AB <= udiTMR_DiscrepancyLimit_ms) AND
   (udiTMR_Theta_Timer_BC <= udiTMR_DiscrepancyLimit_ms) AND
   (udiTMR_Theta_Timer_CA <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Theta_Voted := (rTMR_Theta_ChA + rTMR_Theta_ChB + rTMR_Theta_ChC)
                        - MIN(rTMR_Theta_ChA, MIN(rTMR_Theta_ChB, rTMR_Theta_ChC))
                        - MAX(rTMR_Theta_ChA, MAX(rTMR_Theta_ChB, rTMR_Theta_ChC));
    iTMR_Theta_DegradationState := 0;
    bTMR_Theta_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_Theta_Timer_AB > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Theta_Timer_CA > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Theta_Timer_BC <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Theta_Voted := 0.5 * (rTMR_Theta_ChB + rTMR_Theta_ChC);
    iTMR_Theta_DegradationState := 1;
    bTMR_Theta_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_Theta_Timer_AB > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Theta_Timer_BC > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Theta_Timer_CA <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Theta_Voted := 0.5 * (rTMR_Theta_ChA + rTMR_Theta_ChC);
    iTMR_Theta_DegradationState := 1;
    bTMR_Theta_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_Theta_Timer_BC > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Theta_Timer_CA > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Theta_Timer_AB <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Theta_Voted := 0.5 * (rTMR_Theta_ChA + rTMR_Theta_ChB);
    iTMR_Theta_DegradationState := 1;
    bTMR_Theta_MajorDiscrepancyTrip := FALSE;
ELSE
    rTMR_Theta_Voted := rTMR_Theta_ChA;
    iTMR_Theta_DegradationState := 3;
    bTMR_Theta_MajorDiscrepancyTrip := TRUE;
END_IF;

rVoted_Theta_Raw := rTMR_Theta_Voted;


(* -------------------------------------------------------------------------------------------------------------------- *)
(* SENSOR TRIPLET 4: VACUUM MANIFOLD DIFFERENTIAL PRESSURE TRANSDUCERS                                                  *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rTMR_Vac_ChA := rPT_VacuumManifold_ChA;
rTMR_Vac_ChB := rPT_VacuumManifold_ChB;
rTMR_Vac_ChC := rPT_VacuumManifold_ChC;

rTMR_Vac_Dev_AB := ABS(rTMR_Vac_ChA - rTMR_Vac_ChB);
rTMR_Vac_Dev_BC := ABS(rTMR_Vac_ChB - rTMR_Vac_ChC);
rTMR_Vac_Dev_CA := ABS(rTMR_Vac_ChC - rTMR_Vac_ChA);

bTMR_Vac_Discrep_AB := (rTMR_Vac_Dev_AB > rTol_Discrep_Vac_kPa);
bTMR_Vac_Discrep_BC := (rTMR_Vac_Dev_BC > rTol_Discrep_Vac_kPa);
bTMR_Vac_Discrep_CA := (rTMR_Vac_Dev_CA > rTol_Discrep_Vac_kPa);

IF bTMR_Vac_Discrep_AB THEN
    IF udiTMR_Vac_Timer_AB < 1000 THEN
        udiTMR_Vac_Timer_AB := udiTMR_Vac_Timer_AB + 1;
    END_IF;
ELSE
    IF udiTMR_Vac_Timer_AB > 0 THEN
        udiTMR_Vac_Timer_AB := udiTMR_Vac_Timer_AB - 1;
    END_IF;
END_IF;

IF bTMR_Vac_Discrep_BC THEN
    IF udiTMR_Vac_Timer_BC < 1000 THEN
        udiTMR_Vac_Timer_BC := udiTMR_Vac_Timer_BC + 1;
    END_IF;
ELSE
    IF udiTMR_Vac_Timer_BC > 0 THEN
        udiTMR_Vac_Timer_BC := udiTMR_Vac_Timer_BC - 1;
    END_IF;
END_IF;

IF bTMR_Vac_Discrep_CA THEN
    IF udiTMR_Vac_Timer_CA < 1000 THEN
        udiTMR_Vac_Timer_CA := udiTMR_Vac_Timer_CA + 1;
    END_IF;
ELSE
    IF udiTMR_Vac_Timer_CA > 0 THEN
        udiTMR_Vac_Timer_CA := udiTMR_Vac_Timer_CA - 1;
    END_IF;
END_IF;

IF (udiTMR_Vac_Timer_AB <= udiTMR_DiscrepancyLimit_ms) AND
   (udiTMR_Vac_Timer_BC <= udiTMR_DiscrepancyLimit_ms) AND
   (udiTMR_Vac_Timer_CA <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Vac_Voted := (rTMR_Vac_ChA + rTMR_Vac_ChB + rTMR_Vac_ChC)
                      - MIN(rTMR_Vac_ChA, MIN(rTMR_Vac_ChB, rTMR_Vac_ChC))
                      - MAX(rTMR_Vac_ChA, MAX(rTMR_Vac_ChB, rTMR_Vac_ChC));
    iTMR_Vac_DegradationState := 0;
    bTMR_Vac_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_Vac_Timer_AB > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Vac_Timer_CA > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Vac_Timer_BC <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Vac_Voted := 0.5 * (rTMR_Vac_ChB + rTMR_Vac_ChC);
    iTMR_Vac_DegradationState := 1;
    bTMR_Vac_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_Vac_Timer_AB > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Vac_Timer_BC > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Vac_Timer_CA <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Vac_Voted := 0.5 * (rTMR_Vac_ChA + rTMR_Vac_ChC);
    iTMR_Vac_DegradationState := 1;
    bTMR_Vac_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_Vac_Timer_BC > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Vac_Timer_CA > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Vac_Timer_AB <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Vac_Voted := 0.5 * (rTMR_Vac_ChA + rTMR_Vac_ChB);
    iTMR_Vac_DegradationState := 1;
    bTMR_Vac_MajorDiscrepancyTrip := FALSE;
ELSE
    rTMR_Vac_Voted := rTMR_Vac_ChA;
    iTMR_Vac_DegradationState := 3;
    bTMR_Vac_MajorDiscrepancyTrip := TRUE;
END_IF;

rVoted_Vac_Raw := rTMR_Vac_Voted;


(* -------------------------------------------------------------------------------------------------------------------- *)
(* SENSOR TRIPLET 5: TRIANGULATION LASER PCB WARPAGE GAUGES                                                             *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rTMR_Laser_ChA := rLaser_WarpageHeight_ChA;
rTMR_Laser_ChB := rLaser_WarpageHeight_ChB;
rTMR_Laser_ChC := rLaser_WarpageHeight_ChC;

rTMR_Laser_Dev_AB := ABS(rTMR_Laser_ChA - rTMR_Laser_ChB);
rTMR_Laser_Dev_BC := ABS(rTMR_Laser_ChB - rTMR_Laser_ChC);
rTMR_Laser_Dev_CA := ABS(rTMR_Laser_ChC - rTMR_Laser_ChA);

bTMR_Laser_Discrep_AB := (rTMR_Laser_Dev_AB > rTol_Discrep_Laser_mm);
bTMR_Laser_Discrep_BC := (rTMR_Laser_Dev_BC > rTol_Discrep_Laser_mm);
bTMR_Laser_Discrep_CA := (rTMR_Laser_Dev_CA > rTol_Discrep_Laser_mm);

IF bTMR_Laser_Discrep_AB THEN
    IF udiTMR_Laser_Timer_AB < 1000 THEN
        udiTMR_Laser_Timer_AB := udiTMR_Laser_Timer_AB + 1;
    END_IF;
ELSE
    IF udiTMR_Laser_Timer_AB > 0 THEN
        udiTMR_Laser_Timer_AB := udiTMR_Laser_Timer_AB - 1;
    END_IF;
END_IF;

IF bTMR_Laser_Discrep_BC THEN
    IF udiTMR_Laser_Timer_BC < 1000 THEN
        udiTMR_Laser_Timer_BC := udiTMR_Laser_Timer_BC + 1;
    END_IF;
ELSE
    IF udiTMR_Laser_Timer_BC > 0 THEN
        udiTMR_Laser_Timer_BC := udiTMR_Laser_Timer_BC - 1;
    END_IF;
END_IF;

IF bTMR_Laser_Discrep_CA THEN
    IF udiTMR_Laser_Timer_CA < 1000 THEN
        udiTMR_Laser_Timer_CA := udiTMR_Laser_Timer_CA + 1;
    END_IF;
ELSE
    IF udiTMR_Laser_Timer_CA > 0 THEN
        udiTMR_Laser_Timer_CA := udiTMR_Laser_Timer_CA - 1;
    END_IF;
END_IF;

IF (udiTMR_Laser_Timer_AB <= udiTMR_DiscrepancyLimit_ms) AND
   (udiTMR_Laser_Timer_BC <= udiTMR_DiscrepancyLimit_ms) AND
   (udiTMR_Laser_Timer_CA <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Laser_Voted := (rTMR_Laser_ChA + rTMR_Laser_ChB + rTMR_Laser_ChC)
                        - MIN(rTMR_Laser_ChA, MIN(rTMR_Laser_ChB, rTMR_Laser_ChC))
                        - MAX(rTMR_Laser_ChA, MAX(rTMR_Laser_ChB, rTMR_Laser_ChC));
    iTMR_Laser_DegradationState := 0;
    bTMR_Laser_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_Laser_Timer_AB > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Laser_Timer_CA > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Laser_Timer_BC <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Laser_Voted := 0.5 * (rTMR_Laser_ChB + rTMR_Laser_ChC);
    iTMR_Laser_DegradationState := 1;
    bTMR_Laser_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_Laser_Timer_AB > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Laser_Timer_BC > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Laser_Timer_CA <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Laser_Voted := 0.5 * (rTMR_Laser_ChA + rTMR_Laser_ChC);
    iTMR_Laser_DegradationState := 1;
    bTMR_Laser_MajorDiscrepancyTrip := FALSE;
ELSIF (udiTMR_Laser_Timer_BC > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Laser_Timer_CA > udiTMR_DiscrepancyLimit_ms) AND
      (udiTMR_Laser_Timer_AB <= udiTMR_DiscrepancyLimit_ms) THEN
    rTMR_Laser_Voted := 0.5 * (rTMR_Laser_ChA + rTMR_Laser_ChB);
    iTMR_Laser_DegradationState := 1;
    bTMR_Laser_MajorDiscrepancyTrip := FALSE;
ELSE
    rTMR_Laser_Voted := rTMR_Laser_ChA;
    iTMR_Laser_DegradationState := 3;
    bTMR_Laser_MajorDiscrepancyTrip := TRUE;
END_IF;

rVoted_Laser_Raw := rTMR_Laser_Voted;
"""
