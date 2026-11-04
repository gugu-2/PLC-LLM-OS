# gen_part2_tmr.py
def get_part2_tmr():
    return """
(* ==================================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY FAULT ISOLATION                          *)
(* Deterministic cycle: 250 microseconds. All 8 process sensor triplets evaluated for pairwise discrepancy tolerance.  *)
(* Healthy mode: 3-channel average/median. Degraded mode: 2-channel average with faulted channel isolation.              *)
(* Catastrophic failure: hold last valid state, trigger ISA-18.2 Priority 1 E-Stop or Reject Gate.                     *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.1: 2oo3 TMR VOTING: 1st Operation Roll Radial Reaction Force (WT_SEAM_ROLL_1ST_OP_FORCE_101A/B/C)                 *)
(* Discrepancy Tolerance: 35.0 N. Discrepancy Timeout: 50 ms (200 cycles @ 250 us). Target curling force: 320.0 N.      *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(WT_SEAM_ROLL_1ST_OP_FORCE_101A - WT_SEAM_ROLL_1ST_OP_FORCE_101B) <= 35.0) AND
   (ABS(WT_SEAM_ROLL_1ST_OP_FORCE_101B - WT_SEAM_ROLL_1ST_OP_FORCE_101C) <= 35.0) AND
   (ABS(WT_SEAM_ROLL_1ST_OP_FORCE_101C - WT_SEAM_ROLL_1ST_OP_FORCE_101A) <= 35.0) THEN
    (* All three load cell channels are mutually consistent within 35.0 N threshold *)
    rVoted_Force1stOp_N := (WT_SEAM_ROLL_1ST_OP_FORCE_101A + WT_SEAM_ROLL_1ST_OP_FORCE_101B + WT_SEAM_ROLL_1ST_OP_FORCE_101C) / 3.0;
    bTMR_Force1st_Fault_A := FALSE;
    bTMR_Force1st_Fault_B := FALSE;
    bTMR_Force1st_Fault_C := FALSE;
    rTimer_Force1stOp_Discrep_s := 0.0;
ELSIF (ABS(WT_SEAM_ROLL_1ST_OP_FORCE_101A - WT_SEAM_ROLL_1ST_OP_FORCE_101B) <= 35.0) THEN
    (* Channels A & B agree, Channel C has drifted or experienced strain gauge bridge fracture *)
    rVoted_Force1stOp_N := (WT_SEAM_ROLL_1ST_OP_FORCE_101A + WT_SEAM_ROLL_1ST_OP_FORCE_101B) * 0.5;
    bTMR_Force1st_Fault_A := FALSE;
    bTMR_Force1st_Fault_B := FALSE;
    bTMR_Force1st_Fault_C := TRUE;
    rTimer_Force1stOp_Discrep_s := rTimer_Force1stOp_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(WT_SEAM_ROLL_1ST_OP_FORCE_101A - WT_SEAM_ROLL_1ST_OP_FORCE_101C) <= 35.0) THEN
    (* Channels A & C agree, Channel B has drifted *)
    rVoted_Force1stOp_N := (WT_SEAM_ROLL_1ST_OP_FORCE_101A + WT_SEAM_ROLL_1ST_OP_FORCE_101C) * 0.5;
    bTMR_Force1st_Fault_A := FALSE;
    bTMR_Force1st_Fault_B := TRUE;
    bTMR_Force1st_Fault_C := FALSE;
    rTimer_Force1stOp_Discrep_s := rTimer_Force1stOp_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(WT_SEAM_ROLL_1ST_OP_FORCE_101B - WT_SEAM_ROLL_1ST_OP_FORCE_101C) <= 35.0) THEN
    (* Channels B & C agree, Channel A has drifted *)
    rVoted_Force1stOp_N := (WT_SEAM_ROLL_1ST_OP_FORCE_101B + WT_SEAM_ROLL_1ST_OP_FORCE_101C) * 0.5;
    bTMR_Force1st_Fault_A := TRUE;
    bTMR_Force1st_Fault_B := FALSE;
    bTMR_Force1st_Fault_C := FALSE;
    rTimer_Force1stOp_Discrep_s := rTimer_Force1stOp_Discrep_s + rCycleScanDeltaTime;
ELSE
    (* Catastrophic multi-channel sensor failure: All three channels disagree beyond 35.0 N *)
    bTMR_Force1st_Fault_A := TRUE;
    bTMR_Force1st_Fault_B := TRUE;
    bTMR_Force1st_Fault_C := TRUE;
    rTimer_Force1stOp_Discrep_s := rTimer_Force1stOp_Discrep_s + rCycleScanDeltaTime;
END_IF;

IF rTimer_Force1stOp_Discrep_s >= 0.050 THEN
    bDiscrepAlarm_Force1stOp := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.2: 2oo3 TMR VOTING: 2nd Operation Roll Radial Crimp Force (WT_SEAM_ROLL_2ND_OP_FORCE_102A/B/C)                     *)
(* Discrepancy Tolerance: 35.0 N. Discrepancy Timeout: 50 ms. Target hermetic crimping force: 680.0 N.                  *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(WT_SEAM_ROLL_2ND_OP_FORCE_102A - WT_SEAM_ROLL_2ND_OP_FORCE_102B) <= 35.0) AND
   (ABS(WT_SEAM_ROLL_2ND_OP_FORCE_102B - WT_SEAM_ROLL_2ND_OP_FORCE_102C) <= 35.0) AND
   (ABS(WT_SEAM_ROLL_2ND_OP_FORCE_102C - WT_SEAM_ROLL_2ND_OP_FORCE_102A) <= 35.0) THEN
    rVoted_Force2ndOp_N := (WT_SEAM_ROLL_2ND_OP_FORCE_102A + WT_SEAM_ROLL_2ND_OP_FORCE_102B + WT_SEAM_ROLL_2ND_OP_FORCE_102C) / 3.0;
    bTMR_Force2nd_Fault_A := FALSE;
    bTMR_Force2nd_Fault_B := FALSE;
    bTMR_Force2nd_Fault_C := FALSE;
    rTimer_Force2ndOp_Discrep_s := 0.0;
ELSIF (ABS(WT_SEAM_ROLL_2ND_OP_FORCE_102A - WT_SEAM_ROLL_2ND_OP_FORCE_102B) <= 35.0) THEN
    rVoted_Force2ndOp_N := (WT_SEAM_ROLL_2ND_OP_FORCE_102A + WT_SEAM_ROLL_2ND_OP_FORCE_102B) * 0.5;
    bTMR_Force2nd_Fault_A := FALSE;
    bTMR_Force2nd_Fault_B := FALSE;
    bTMR_Force2nd_Fault_C := TRUE;
    rTimer_Force2ndOp_Discrep_s := rTimer_Force2ndOp_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(WT_SEAM_ROLL_2ND_OP_FORCE_102A - WT_SEAM_ROLL_2ND_OP_FORCE_102C) <= 35.0) THEN
    rVoted_Force2ndOp_N := (WT_SEAM_ROLL_2ND_OP_FORCE_102A + WT_SEAM_ROLL_2ND_OP_FORCE_102C) * 0.5;
    bTMR_Force2nd_Fault_A := FALSE;
    bTMR_Force2nd_Fault_B := TRUE;
    bTMR_Force2nd_Fault_C := FALSE;
    rTimer_Force2ndOp_Discrep_s := rTimer_Force2ndOp_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(WT_SEAM_ROLL_2ND_OP_FORCE_102B - WT_SEAM_ROLL_2ND_OP_FORCE_102C) <= 35.0) THEN
    rVoted_Force2ndOp_N := (WT_SEAM_ROLL_2ND_OP_FORCE_102B + WT_SEAM_ROLL_2ND_OP_FORCE_102C) * 0.5;
    bTMR_Force2nd_Fault_A := TRUE;
    bTMR_Force2nd_Fault_B := FALSE;
    bTMR_Force2nd_Fault_C := FALSE;
    rTimer_Force2ndOp_Discrep_s := rTimer_Force2ndOp_Discrep_s + rCycleScanDeltaTime;
ELSE
    bTMR_Force2nd_Fault_A := TRUE;
    bTMR_Force2nd_Fault_B := TRUE;
    bTMR_Force2nd_Fault_C := TRUE;
    rTimer_Force2ndOp_Discrep_s := rTimer_Force2ndOp_Discrep_s + rCycleScanDeltaTime;
END_IF;

IF rTimer_Force2ndOp_Discrep_s >= 0.050 THEN
    bDiscrepAlarm_Force2ndOp := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.3: 2oo3 TMR VOTING: Rotary Turret Master Dual-Resolver Angular Position (ST_TURRET_RESOLVER_POS_201A/B/C)          *)
(* Discrepancy Tolerance: 0.150 deg (2.6 mrad). Discrepancy Timeout: 20 ms. Critical for Electronic Camming Sync.       *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(ST_TURRET_RESOLVER_POS_201A - ST_TURRET_RESOLVER_POS_201B) <= 0.150) AND
   (ABS(ST_TURRET_RESOLVER_POS_201B - ST_TURRET_RESOLVER_POS_201C) <= 0.150) AND
   (ABS(ST_TURRET_RESOLVER_POS_201C - ST_TURRET_RESOLVER_POS_201A) <= 0.150) THEN
    rVoted_TurretResolver_deg := (ST_TURRET_RESOLVER_POS_201A + ST_TURRET_RESOLVER_POS_201B + ST_TURRET_RESOLVER_POS_201C) / 3.0;
    bTMR_Resolver_Fault_A := FALSE;
    bTMR_Resolver_Fault_B := FALSE;
    bTMR_Resolver_Fault_C := FALSE;
    rTimer_Resolver_Discrep_s := 0.0;
ELSIF (ABS(ST_TURRET_RESOLVER_POS_201A - ST_TURRET_RESOLVER_POS_201B) <= 0.150) THEN
    rVoted_TurretResolver_deg := (ST_TURRET_RESOLVER_POS_201A + ST_TURRET_RESOLVER_POS_201B) * 0.5;
    bTMR_Resolver_Fault_A := FALSE;
    bTMR_Resolver_Fault_B := FALSE;
    bTMR_Resolver_Fault_C := TRUE;
    rTimer_Resolver_Discrep_s := rTimer_Resolver_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(ST_TURRET_RESOLVER_POS_201A - ST_TURRET_RESOLVER_POS_201C) <= 0.150) THEN
    rVoted_TurretResolver_deg := (ST_TURRET_RESOLVER_POS_201A + ST_TURRET_RESOLVER_POS_201C) * 0.5;
    bTMR_Resolver_Fault_A := FALSE;
    bTMR_Resolver_Fault_B := TRUE;
    bTMR_Resolver_Fault_C := FALSE;
    rTimer_Resolver_Discrep_s := rTimer_Resolver_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(ST_TURRET_RESOLVER_POS_201B - ST_TURRET_RESOLVER_POS_201C) <= 0.150) THEN
    rVoted_TurretResolver_deg := (ST_TURRET_RESOLVER_POS_201B + ST_TURRET_RESOLVER_POS_201C) * 0.5;
    bTMR_Resolver_Fault_A := TRUE;
    bTMR_Resolver_Fault_B := FALSE;
    bTMR_Resolver_Fault_C := FALSE;
    rTimer_Resolver_Discrep_s := rTimer_Resolver_Discrep_s + rCycleScanDeltaTime;
ELSE
    bTMR_Resolver_Fault_A := TRUE;
    bTMR_Resolver_Fault_B := TRUE;
    bTMR_Resolver_Fault_C := TRUE;
    rTimer_Resolver_Discrep_s := rTimer_Resolver_Discrep_s + rCycleScanDeltaTime;
END_IF;

IF rTimer_Resolver_Discrep_s >= 0.020 THEN
    bDiscrepAlarm_TurretResolver := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.4: 2oo3 TMR VOTING: Cryogenic Liquid Nitrogen (LN2) Micro-Dose Mass (FT_LN2_MICRODOSE_MASS_301A/B/C)               *)
(* Discrepancy Tolerance: 2.50 mg. Discrepancy Timeout: 50 ms. Target cryogenic mass: 45.0 mg per can container.       *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(FT_LN2_MICRODOSE_MASS_301A - FT_LN2_MICRODOSE_MASS_301B) <= 2.50) AND
   (ABS(FT_LN2_MICRODOSE_MASS_301B - FT_LN2_MICRODOSE_MASS_301C) <= 2.50) AND
   (ABS(FT_LN2_MICRODOSE_MASS_301C - FT_LN2_MICRODOSE_MASS_301A) <= 2.50) THEN
    rVoted_LN2DoseMass_mg := (FT_LN2_MICRODOSE_MASS_301A + FT_LN2_MICRODOSE_MASS_301B + FT_LN2_MICRODOSE_MASS_301C) / 3.0;
    bTMR_LN2Mass_Fault_A := FALSE;
    bTMR_LN2Mass_Fault_B := FALSE;
    bTMR_LN2Mass_Fault_C := FALSE;
    rTimer_LN2Mass_Discrep_s := 0.0;
ELSIF (ABS(FT_LN2_MICRODOSE_MASS_301A - FT_LN2_MICRODOSE_MASS_301B) <= 2.50) THEN
    rVoted_LN2DoseMass_mg := (FT_LN2_MICRODOSE_MASS_301A + FT_LN2_MICRODOSE_MASS_301B) * 0.5;
    bTMR_LN2Mass_Fault_A := FALSE;
    bTMR_LN2Mass_Fault_B := FALSE;
    bTMR_LN2Mass_Fault_C := TRUE;
    rTimer_LN2Mass_Discrep_s := rTimer_LN2Mass_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(FT_LN2_MICRODOSE_MASS_301A - FT_LN2_MICRODOSE_MASS_301C) <= 2.50) THEN
    rVoted_LN2DoseMass_mg := (FT_LN2_MICRODOSE_MASS_301A + FT_LN2_MICRODOSE_MASS_301C) * 0.5;
    bTMR_LN2Mass_Fault_A := FALSE;
    bTMR_LN2Mass_Fault_B := TRUE;
    bTMR_LN2Mass_Fault_C := FALSE;
    rTimer_LN2Mass_Discrep_s := rTimer_LN2Mass_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(FT_LN2_MICRODOSE_MASS_301B - FT_LN2_MICRODOSE_MASS_301C) <= 2.50) THEN
    rVoted_LN2DoseMass_mg := (FT_LN2_MICRODOSE_MASS_301B + FT_LN2_MICRODOSE_MASS_301C) * 0.5;
    bTMR_LN2Mass_Fault_A := TRUE;
    bTMR_LN2Mass_Fault_B := FALSE;
    bTMR_LN2Mass_Fault_C := FALSE;
    rTimer_LN2Mass_Discrep_s := rTimer_LN2Mass_Discrep_s + rCycleScanDeltaTime;
ELSE
    bTMR_LN2Mass_Fault_A := TRUE;
    bTMR_LN2Mass_Fault_B := TRUE;
    bTMR_LN2Mass_Fault_C := TRUE;
    rTimer_LN2Mass_Discrep_s := rTimer_LN2Mass_Discrep_s + rCycleScanDeltaTime;
END_IF;

IF rTimer_LN2Mass_Discrep_s >= 0.050 THEN
    bDiscrepAlarm_LN2DoseMass := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.5: 2oo3 TMR VOTING: Acoustic Tap Peak Resonance Frequency & Can Internal Pressure                                   *)
(* Discrepancy Tolerance: 120.0 Hz for Frequency, 0.150 bar for Pressure. Discrepancy Timeout: 30 ms.                  *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(rAcousticResonantFreq_ChA - rAcousticResonantFreq_ChB) <= 120.0) AND
   (ABS(rAcousticResonantFreq_ChB - rAcousticResonantFreq_ChC) <= 120.0) AND
   (ABS(rAcousticResonantFreq_ChC - rAcousticResonantFreq_ChA) <= 120.0) THEN
    rVoted_AcousticResonanceFreq_Hz := (rAcousticResonantFreq_ChA + rAcousticResonantFreq_ChB + rAcousticResonantFreq_ChC) / 3.0;
    rVoted_AcousticPressure_bar := (PT_CAN_ACOUSTIC_TAP_PRESSURE_401A + PT_CAN_ACOUSTIC_TAP_PRESSURE_401B + PT_CAN_ACOUSTIC_TAP_PRESSURE_401C) / 3.0;
    bTMR_Acoustic_Fault_A := FALSE;
    bTMR_Acoustic_Fault_B := FALSE;
    bTMR_Acoustic_Fault_C := FALSE;
    rTimer_Acoustic_Discrep_s := 0.0;
ELSIF (ABS(rAcousticResonantFreq_ChA - rAcousticResonantFreq_ChB) <= 120.0) THEN
    rVoted_AcousticResonanceFreq_Hz := (rAcousticResonantFreq_ChA + rAcousticResonantFreq_ChB) * 0.5;
    rVoted_AcousticPressure_bar := (PT_CAN_ACOUSTIC_TAP_PRESSURE_401A + PT_CAN_ACOUSTIC_TAP_PRESSURE_401B) * 0.5;
    bTMR_Acoustic_Fault_A := FALSE;
    bTMR_Acoustic_Fault_B := FALSE;
    bTMR_Acoustic_Fault_C := TRUE;
    rTimer_Acoustic_Discrep_s := rTimer_Acoustic_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(rAcousticResonantFreq_ChA - rAcousticResonantFreq_ChC) <= 120.0) THEN
    rVoted_AcousticResonanceFreq_Hz := (rAcousticResonantFreq_ChA + rAcousticResonantFreq_ChC) * 0.5;
    rVoted_AcousticPressure_bar := (PT_CAN_ACOUSTIC_TAP_PRESSURE_401A + PT_CAN_ACOUSTIC_TAP_PRESSURE_401C) * 0.5;
    bTMR_Acoustic_Fault_A := FALSE;
    bTMR_Acoustic_Fault_B := TRUE;
    bTMR_Acoustic_Fault_C := FALSE;
    rTimer_Acoustic_Discrep_s := rTimer_Acoustic_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(rAcousticResonantFreq_ChB - rAcousticResonantFreq_ChC) <= 120.0) THEN
    rVoted_AcousticResonanceFreq_Hz := (rAcousticResonantFreq_ChB + rAcousticResonantFreq_ChC) * 0.5;
    rVoted_AcousticPressure_bar := (PT_CAN_ACOUSTIC_TAP_PRESSURE_401B + PT_CAN_ACOUSTIC_TAP_PRESSURE_401C) * 0.5;
    bTMR_Acoustic_Fault_A := TRUE;
    bTMR_Acoustic_Fault_B := FALSE;
    bTMR_Acoustic_Fault_C := FALSE;
    rTimer_Acoustic_Discrep_s := rTimer_Acoustic_Discrep_s + rCycleScanDeltaTime;
ELSE
    bTMR_Acoustic_Fault_A := TRUE;
    bTMR_Acoustic_Fault_B := TRUE;
    bTMR_Acoustic_Fault_C := TRUE;
    rTimer_Acoustic_Discrep_s := rTimer_Acoustic_Discrep_s + rCycleScanDeltaTime;
END_IF;

IF rTimer_Acoustic_Discrep_s >= 0.030 THEN
    bDiscrepAlarm_AcousticResonance := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.6: 2oo3 TMR VOTING: Aseptic Isolator Vaporized Peracetic Acid (PAA) Concentration (ZT_CHAMBER_PAA_CONC_501A/B/C)   *)
(* Discrepancy Tolerance: 50.0 ppm. Discrepancy Timeout: 250 ms. Target sterilization concentration: 1500.0 ppm.         *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(ZT_CHAMBER_PAA_CONC_501A - ZT_CHAMBER_PAA_CONC_501B) <= 50.0) AND
   (ABS(ZT_CHAMBER_PAA_CONC_501B - ZT_CHAMBER_PAA_CONC_501C) <= 50.0) AND
   (ABS(ZT_CHAMBER_PAA_CONC_501C - ZT_CHAMBER_PAA_CONC_501A) <= 50.0) THEN
    rVoted_PAAConcentration_ppm := (ZT_CHAMBER_PAA_CONC_501A + ZT_CHAMBER_PAA_CONC_501B + ZT_CHAMBER_PAA_CONC_501C) / 3.0;
    bTMR_PAA_Fault_A := FALSE;
    bTMR_PAA_Fault_B := FALSE;
    bTMR_PAA_Fault_C := FALSE;
    rTimer_PAA_Discrep_s := 0.0;
ELSIF (ABS(ZT_CHAMBER_PAA_CONC_501A - ZT_CHAMBER_PAA_CONC_501B) <= 50.0) THEN
    rVoted_PAAConcentration_ppm := (ZT_CHAMBER_PAA_CONC_501A + ZT_CHAMBER_PAA_CONC_501B) * 0.5;
    bTMR_PAA_Fault_A := FALSE;
    bTMR_PAA_Fault_B := FALSE;
    bTMR_PAA_Fault_C := TRUE;
    rTimer_PAA_Discrep_s := rTimer_PAA_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(ZT_CHAMBER_PAA_CONC_501A - ZT_CHAMBER_PAA_CONC_501C) <= 50.0) THEN
    rVoted_PAAConcentration_ppm := (ZT_CHAMBER_PAA_CONC_501A + ZT_CHAMBER_PAA_CONC_501C) * 0.5;
    bTMR_PAA_Fault_A := FALSE;
    bTMR_PAA_Fault_B := TRUE;
    bTMR_PAA_Fault_C := FALSE;
    rTimer_PAA_Discrep_s := rTimer_PAA_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(ZT_CHAMBER_PAA_CONC_501B - ZT_CHAMBER_PAA_CONC_501C) <= 50.0) THEN
    rVoted_PAAConcentration_ppm := (ZT_CHAMBER_PAA_CONC_501B + ZT_CHAMBER_PAA_CONC_501C) * 0.5;
    bTMR_PAA_Fault_A := TRUE;
    bTMR_PAA_Fault_B := FALSE;
    bTMR_PAA_Fault_C := FALSE;
    rTimer_PAA_Discrep_s := rTimer_PAA_Discrep_s + rCycleScanDeltaTime;
ELSE
    bTMR_PAA_Fault_A := TRUE;
    bTMR_PAA_Fault_B := TRUE;
    bTMR_PAA_Fault_C := TRUE;
    rTimer_PAA_Discrep_s := rTimer_PAA_Discrep_s + rCycleScanDeltaTime;
END_IF;

IF rTimer_PAA_Discrep_s >= 0.250 THEN
    bDiscrepAlarm_PAAConcentration := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.7: 2oo3 TMR VOTING: Sterile Air Isolator Differential Overpressure (PT_STERILE_AIR_OVERPRESSURE_601A/B/C)          *)
(* Discrepancy Tolerance: 3.00 Pa. Discrepancy Timeout: 100 ms. Target positive pressure barrier: 45.0 Pa.             *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(PT_STERILE_AIR_OVERPRESSURE_601A - PT_STERILE_AIR_OVERPRESSURE_601B) <= 3.00) AND
   (ABS(PT_STERILE_AIR_OVERPRESSURE_601B - PT_STERILE_AIR_OVERPRESSURE_601C) <= 3.00) AND
   (ABS(PT_STERILE_AIR_OVERPRESSURE_601C - PT_STERILE_AIR_OVERPRESSURE_601A) <= 3.00) THEN
    rVoted_SterileAirPres_Pa := (PT_STERILE_AIR_OVERPRESSURE_601A + PT_STERILE_AIR_OVERPRESSURE_601B + PT_STERILE_AIR_OVERPRESSURE_601C) / 3.0;
    bTMR_SterileAir_Fault_A := FALSE;
    bTMR_SterileAir_Fault_B := FALSE;
    bTMR_SterileAir_Fault_C := FALSE;
    rTimer_SterileAir_Discrep_s := 0.0;
ELSIF (ABS(PT_STERILE_AIR_OVERPRESSURE_601A - PT_STERILE_AIR_OVERPRESSURE_601B) <= 3.00) THEN
    rVoted_SterileAirPres_Pa := (PT_STERILE_AIR_OVERPRESSURE_601A + PT_STERILE_AIR_OVERPRESSURE_601B) * 0.5;
    bTMR_SterileAir_Fault_A := FALSE;
    bTMR_SterileAir_Fault_B := FALSE;
    bTMR_SterileAir_Fault_C := TRUE;
    rTimer_SterileAir_Discrep_s := rTimer_SterileAir_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(PT_STERILE_AIR_OVERPRESSURE_601A - PT_STERILE_AIR_OVERPRESSURE_601C) <= 3.00) THEN
    rVoted_SterileAirPres_Pa := (PT_STERILE_AIR_OVERPRESSURE_601A + PT_STERILE_AIR_OVERPRESSURE_601C) * 0.5;
    bTMR_SterileAir_Fault_A := FALSE;
    bTMR_SterileAir_Fault_B := TRUE;
    bTMR_SterileAir_Fault_C := FALSE;
    rTimer_SterileAir_Discrep_s := rTimer_SterileAir_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(PT_STERILE_AIR_OVERPRESSURE_601B - PT_STERILE_AIR_OVERPRESSURE_601C) <= 3.00) THEN
    rVoted_SterileAirPres_Pa := (PT_STERILE_AIR_OVERPRESSURE_601B + PT_STERILE_AIR_OVERPRESSURE_601C) * 0.5;
    bTMR_SterileAir_Fault_A := TRUE;
    bTMR_SterileAir_Fault_B := FALSE;
    bTMR_SterileAir_Fault_C := FALSE;
    rTimer_SterileAir_Discrep_s := rTimer_SterileAir_Discrep_s + rCycleScanDeltaTime;
ELSE
    bTMR_SterileAir_Fault_A := TRUE;
    bTMR_SterileAir_Fault_B := TRUE;
    bTMR_SterileAir_Fault_C := TRUE;
    rTimer_SterileAir_Discrep_s := rTimer_SterileAir_Discrep_s + rCycleScanDeltaTime;
END_IF;

IF rTimer_SterileAir_Discrep_s >= 0.100 THEN
    bDiscrepAlarm_SterileAirPres := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.8: 2oo3 TMR VOTING: Seaming Chuck Ceramic Hybrid Bearings Temperature (TT_SEAM_CHUCK_BEARING_701A/B/C)             *)
(* Discrepancy Tolerance: 4.00 deg C. Discrepancy Timeout: 500 ms. Normal operating range: 35.0 - 45.0 deg C.           *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(TT_SEAM_CHUCK_BEARING_701A - TT_SEAM_CHUCK_BEARING_701B) <= 4.00) AND
   (ABS(TT_SEAM_CHUCK_BEARING_701B - TT_SEAM_CHUCK_BEARING_701C) <= 4.00) AND
   (ABS(TT_SEAM_CHUCK_BEARING_701C - TT_SEAM_CHUCK_BEARING_701A) <= 4.00) THEN
    rVoted_ChuckBearingTemp_C := (TT_SEAM_CHUCK_BEARING_701A + TT_SEAM_CHUCK_BEARING_701B + TT_SEAM_CHUCK_BEARING_701C) / 3.0;
    bTMR_BearingTemp_Fault_A := FALSE;
    bTMR_BearingTemp_Fault_B := FALSE;
    bTMR_BearingTemp_Fault_C := FALSE;
    rTimer_BearingTemp_Discrep_s := 0.0;
ELSIF (ABS(TT_SEAM_CHUCK_BEARING_701A - TT_SEAM_CHUCK_BEARING_701B) <= 4.00) THEN
    rVoted_ChuckBearingTemp_C := (TT_SEAM_CHUCK_BEARING_701A + TT_SEAM_CHUCK_BEARING_701B) * 0.5;
    bTMR_BearingTemp_Fault_A := FALSE;
    bTMR_BearingTemp_Fault_B := FALSE;
    bTMR_BearingTemp_Fault_C := TRUE;
    rTimer_BearingTemp_Discrep_s := rTimer_BearingTemp_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(TT_SEAM_CHUCK_BEARING_701A - TT_SEAM_CHUCK_BEARING_701C) <= 4.00) THEN
    rVoted_ChuckBearingTemp_C := (TT_SEAM_CHUCK_BEARING_701A + TT_SEAM_CHUCK_BEARING_701C) * 0.5;
    bTMR_BearingTemp_Fault_A := FALSE;
    bTMR_BearingTemp_Fault_B := TRUE;
    bTMR_BearingTemp_Fault_C := FALSE;
    rTimer_BearingTemp_Discrep_s := rTimer_BearingTemp_Discrep_s + rCycleScanDeltaTime;
ELSIF (ABS(TT_SEAM_CHUCK_BEARING_701B - TT_SEAM_CHUCK_BEARING_701C) <= 4.00) THEN
    rVoted_ChuckBearingTemp_C := (TT_SEAM_CHUCK_BEARING_701B + TT_SEAM_CHUCK_BEARING_701C) * 0.5;
    bTMR_BearingTemp_Fault_A := TRUE;
    bTMR_BearingTemp_Fault_B := FALSE;
    bTMR_BearingTemp_Fault_C := FALSE;
    rTimer_BearingTemp_Discrep_s := rTimer_BearingTemp_Discrep_s + rCycleScanDeltaTime;
ELSE
    bTMR_BearingTemp_Fault_A := TRUE;
    bTMR_BearingTemp_Fault_B := TRUE;
    bTMR_BearingTemp_Fault_C := TRUE;
    rTimer_BearingTemp_Discrep_s := rTimer_BearingTemp_Discrep_s + rCycleScanDeltaTime;
END_IF;

IF rTimer_BearingTemp_Discrep_s >= 0.500 THEN
    bDiscrepAlarm_ChuckBearingTemp := TRUE;
END_IF;
"""
