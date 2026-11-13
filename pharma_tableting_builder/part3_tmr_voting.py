# pharma_tableting_builder/part3_tmr_voting.py

def get_part3():
    return """(* === PHASE 1: 2oo3 TMR SENSOR VOTING WITH DISCREPANCY TIMERS === *)

(* ============================================================================================== *)
(* CHANNEL 1: LOSS-IN-WEIGHT (LIW) GRAVIMETRIC FEEDER MASS FLOW RATE [kg/h]                       *)
(* ============================================================================================== *)
rFeeder_Delta_AB := ABS(rFeederFlow_ChA_kgh - rFeederFlow_ChB_kgh);
rFeeder_Delta_BC := ABS(rFeederFlow_ChB_kgh - rFeederFlow_ChC_kgh);
rFeeder_Delta_CA := ABS(rFeederFlow_ChC_kgh - rFeederFlow_ChA_kgh);

IF (rFeeder_Delta_AB > rFeeder_DiscrepancyLimit_kgh) OR 
   (rFeeder_Delta_BC > rFeeder_DiscrepancyLimit_kgh) OR 
   (rFeeder_Delta_CA > rFeeder_DiscrepancyLimit_kgh) THEN
    rFeeder_DiscrepancyTimer_s := rFeeder_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rFeeder_DiscrepancyTimer_s >= T_DISCREPANCY_MAX_SEC THEN
        (* Identify outlier channel via pairwise deviations *)
        IF (rFeeder_Delta_AB > rFeeder_DiscrepancyLimit_kgh) AND (rFeeder_Delta_CA > rFeeder_DiscrepancyLimit_kgh) THEN
            bFeeder_ChA_Valid := FALSE;
            nFeeder_VotingMode := 2; (* Degrade to ChB and ChC *)
        ELSIF (rFeeder_Delta_AB > rFeeder_DiscrepancyLimit_kgh) AND (rFeeder_Delta_BC > rFeeder_DiscrepancyLimit_kgh) THEN
            bFeeder_ChB_Valid := FALSE;
            nFeeder_VotingMode := 2; (* Degrade to ChA and ChC *)
        ELSIF (rFeeder_Delta_BC > rFeeder_DiscrepancyLimit_kgh) AND (rFeeder_Delta_CA > rFeeder_DiscrepancyLimit_kgh) THEN
            bFeeder_ChC_Valid := FALSE;
            nFeeder_VotingMode := 2; (* Degrade to ChA and ChB *)
        ELSE
            (* Multi-channel divergence - degrade to conservative single or hold *)
            bFeeder_ChA_Valid := FALSE;
            bFeeder_ChB_Valid := FALSE;
            nFeeder_VotingMode := 1;
        END_IF;
    END_IF;
ELSE
    rFeeder_DiscrepancyTimer_s := MAX(0.0, rFeeder_DiscrepancyTimer_s - (T_CYCLE_SEC * 0.5));
    bFeeder_ChA_Valid := TRUE;
    bFeeder_ChB_Valid := TRUE;
    bFeeder_ChC_Valid := TRUE;
    nFeeder_VotingMode := 3;
END_IF;

(* Compute Voted Feeder Mass Flow Value *)
IF nFeeder_VotingMode = 3 THEN
    (* 2oo3 Median Selection *)
    IF ((rFeederFlow_ChA_kgh >= rFeederFlow_ChB_kgh) AND (rFeederFlow_ChA_kgh <= rFeederFlow_ChC_kgh)) OR
       ((rFeederFlow_ChA_kgh <= rFeederFlow_ChB_kgh) AND (rFeederFlow_ChA_kgh >= rFeederFlow_ChC_kgh)) THEN
        rVotedFeederFlow_kgh := rFeederFlow_ChA_kgh;
    ELSIF ((rFeederFlow_ChB_kgh >= rFeederFlow_ChA_kgh) AND (rFeederFlow_ChB_kgh <= rFeederFlow_ChC_kgh)) OR
          ((rFeederFlow_ChB_kgh <= rFeederFlow_ChA_kgh) AND (rFeederFlow_ChB_kgh >= rFeederFlow_ChC_kgh)) THEN
        rVotedFeederFlow_kgh := rFeederFlow_ChB_kgh;
    ELSE
        rVotedFeederFlow_kgh := rFeederFlow_ChC_kgh;
    END_IF;
ELSIF nFeeder_VotingMode = 2 THEN
    (* 1oo2 Degraded Mean *)
    IF bFeeder_ChA_Valid AND bFeeder_ChB_Valid THEN
        rVotedFeederFlow_kgh := 0.5 * (rFeederFlow_ChA_kgh + rFeederFlow_ChB_kgh);
    ELSIF bFeeder_ChB_Valid AND bFeeder_ChC_Valid THEN
        rVotedFeederFlow_kgh := 0.5 * (rFeederFlow_ChB_kgh + rFeederFlow_ChC_kgh);
    ELSIF bFeeder_ChA_Valid AND bFeeder_ChC_Valid THEN
        rVotedFeederFlow_kgh := 0.5 * (rFeederFlow_ChA_kgh + rFeederFlow_ChC_kgh);
    ELSE
        rVotedFeederFlow_kgh := rFeederFlow_ChA_kgh;
    END_IF;
ELSIF nFeeder_VotingMode = 1 THEN
    IF bFeeder_ChA_Valid THEN
        rVotedFeederFlow_kgh := rFeederFlow_ChA_kgh;
    ELSIF bFeeder_ChB_Valid THEN
        rVotedFeederFlow_kgh := rFeederFlow_ChB_kgh;
    ELSE
        rVotedFeederFlow_kgh := rFeederFlow_ChC_kgh;
    END_IF;
ELSE
    (* Fail-Safe Fallback to Recipe Target *)
    rVotedFeederFlow_kgh := rRecipeTargetFeederFlow_kgh;
END_IF;


(* ============================================================================================== *)
(* CHANNEL 2: IN-LINE FLUID BED MICROWAVE RESONANCE MOISTURE CAVITY PROBES [% LOD]                 *)
(* ============================================================================================== *)
rMoist_Delta_AB := ABS(rMoistureLOD_ChA_pct - rMoistureLOD_ChB_pct);
rMoist_Delta_BC := ABS(rMoistureLOD_ChB_pct - rMoistureLOD_ChC_pct);
rMoist_Delta_CA := ABS(rMoistureLOD_ChC_pct - rMoistureLOD_ChA_pct);

IF (rMoist_Delta_AB > rMoist_DiscrepancyLimit_pct) OR 
   (rMoist_Delta_BC > rMoist_DiscrepancyLimit_pct) OR 
   (rMoist_Delta_CA > rMoist_DiscrepancyLimit_pct) THEN
    rMoist_DiscrepancyTimer_s := rMoist_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rMoist_DiscrepancyTimer_s >= T_DISCREPANCY_MAX_SEC THEN
        IF (rMoist_Delta_AB > rMoist_DiscrepancyLimit_pct) AND (rMoist_Delta_CA > rMoist_DiscrepancyLimit_pct) THEN
            bMoist_ChA_Valid := FALSE;
            nMoist_VotingMode := 2;
        ELSIF (rMoist_Delta_AB > rMoist_DiscrepancyLimit_pct) AND (rMoist_Delta_BC > rMoist_DiscrepancyLimit_pct) THEN
            bMoist_ChB_Valid := FALSE;
            nMoist_VotingMode := 2;
        ELSIF (rMoist_Delta_BC > rMoist_DiscrepancyLimit_pct) AND (rMoist_Delta_CA > rMoist_DiscrepancyLimit_pct) THEN
            bMoist_ChC_Valid := FALSE;
            nMoist_VotingMode := 2;
        ELSE
            bMoist_ChA_Valid := FALSE;
            bMoist_ChB_Valid := FALSE;
            nMoist_VotingMode := 1;
        END_IF;
    END_IF;
ELSE
    rMoist_DiscrepancyTimer_s := MAX(0.0, rMoist_DiscrepancyTimer_s - (T_CYCLE_SEC * 0.5));
    bMoist_ChA_Valid := TRUE;
    bMoist_ChB_Valid := TRUE;
    bMoist_ChC_Valid := TRUE;
    nMoist_VotingMode := 3;
END_IF;

IF nMoist_VotingMode = 3 THEN
    IF ((rMoistureLOD_ChA_pct >= rMoistureLOD_ChB_pct) AND (rMoistureLOD_ChA_pct <= rMoistureLOD_ChC_pct)) OR
       ((rMoistureLOD_ChA_pct <= rMoistureLOD_ChB_pct) AND (rMoistureLOD_ChA_pct >= rMoistureLOD_ChC_pct)) THEN
        rVotedMoistureLOD_pct := rMoistureLOD_ChA_pct;
    ELSIF ((rMoistureLOD_ChB_pct >= rMoistureLOD_ChA_pct) AND (rMoistureLOD_ChB_pct <= rMoistureLOD_ChC_pct)) OR
          ((rMoistureLOD_ChB_pct <= rMoistureLOD_ChA_pct) AND (rMoistureLOD_ChB_pct >= rMoistureLOD_ChC_pct)) THEN
        rVotedMoistureLOD_pct := rMoistureLOD_ChB_pct;
    ELSE
        rVotedMoistureLOD_pct := rMoistureLOD_ChC_pct;
    END_IF;
ELSIF nMoist_VotingMode = 2 THEN
    IF bMoist_ChA_Valid AND bMoist_ChB_Valid THEN
        rVotedMoistureLOD_pct := 0.5 * (rMoistureLOD_ChA_pct + rMoistureLOD_ChB_pct);
    ELSIF bMoist_ChB_Valid AND bMoist_ChC_Valid THEN
        rVotedMoistureLOD_pct := 0.5 * (rMoistureLOD_ChB_pct + rMoistureLOD_ChC_pct);
    ELSIF bMoist_ChA_Valid AND bMoist_ChC_Valid THEN
        rVotedMoistureLOD_pct := 0.5 * (rMoistureLOD_ChA_pct + rMoistureLOD_ChC_pct);
    ELSE
        rVotedMoistureLOD_pct := rMoistureLOD_ChA_pct;
    END_IF;
ELSIF nMoist_VotingMode = 1 THEN
    IF bMoist_ChA_Valid THEN
        rVotedMoistureLOD_pct := rMoistureLOD_ChA_pct;
    ELSIF bMoist_ChB_Valid THEN
        rVotedMoistureLOD_pct := rMoistureLOD_ChB_pct;
    ELSE
        rVotedMoistureLOD_pct := rMoistureLOD_ChC_pct;
    END_IF;
ELSE
    rVotedMoistureLOD_pct := rRecipeTargetMoistureLOD_pct;
END_IF;


(* ============================================================================================== *)
(* CHANNEL 3: ROTARY PRESS PRE-COMPRESSION PIEZOELECTRIC LOAD CELLS [kN]                          *)
(* ============================================================================================== *)
rPreComp_Delta_AB := ABS(rPreCompForce_ChA_kN - rPreCompForce_ChB_kN);
rPreComp_Delta_BC := ABS(rPreCompForce_ChB_kN - rPreCompForce_ChC_kN);
rPreComp_Delta_CA := ABS(rPreCompForce_ChC_kN - rPreCompForce_ChA_kN);

IF (rPreComp_Delta_AB > rPreComp_DiscrepancyLimit_kN) OR 
   (rPreComp_Delta_BC > rPreComp_DiscrepancyLimit_kN) OR 
   (rPreComp_Delta_CA > rPreComp_DiscrepancyLimit_kN) THEN
    rPreComp_DiscrepancyTimer_s := rPreComp_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rPreComp_DiscrepancyTimer_s >= T_DISCREPANCY_MAX_SEC THEN
        IF (rPreComp_Delta_AB > rPreComp_DiscrepancyLimit_kN) AND (rPreComp_Delta_CA > rPreComp_DiscrepancyLimit_kN) THEN
            bPreComp_ChA_Valid := FALSE;
            nPreComp_VotingMode := 2;
        ELSIF (rPreComp_Delta_AB > rPreComp_DiscrepancyLimit_kN) AND (rPreComp_Delta_BC > rPreComp_DiscrepancyLimit_kN) THEN
            bPreComp_ChB_Valid := FALSE;
            nPreComp_VotingMode := 2;
        ELSIF (rPreComp_Delta_BC > rPreComp_DiscrepancyLimit_kN) AND (rPreComp_Delta_CA > rPreComp_DiscrepancyLimit_kN) THEN
            bPreComp_ChC_Valid := FALSE;
            nPreComp_VotingMode := 2;
        ELSE
            bPreComp_ChA_Valid := FALSE;
            bPreComp_ChB_Valid := FALSE;
            nPreComp_VotingMode := 1;
        END_IF;
    END_IF;
ELSE
    rPreComp_DiscrepancyTimer_s := MAX(0.0, rPreComp_DiscrepancyTimer_s - (T_CYCLE_SEC * 0.5));
    bPreComp_ChA_Valid := TRUE;
    bPreComp_ChB_Valid := TRUE;
    bPreComp_ChC_Valid := TRUE;
    nPreComp_VotingMode := 3;
END_IF;

IF nPreComp_VotingMode = 3 THEN
    IF ((rPreCompForce_ChA_kN >= rPreCompForce_ChB_kN) AND (rPreCompForce_ChA_kN <= rPreCompForce_ChC_kN)) OR
       ((rPreCompForce_ChA_kN <= rPreCompForce_ChB_kN) AND (rPreCompForce_ChA_kN >= rPreCompForce_ChC_kN)) THEN
        rVotedPreCompForce_kN := rPreCompForce_ChA_kN;
    ELSIF ((rPreCompForce_ChB_kN >= rPreCompForce_ChA_kN) AND (rPreCompForce_ChB_kN <= rPreCompForce_ChC_kN)) OR
          ((rPreCompForce_ChB_kN <= rPreCompForce_ChA_kN) AND (rPreCompForce_ChB_kN >= rPreCompForce_ChC_kN)) THEN
        rVotedPreCompForce_kN := rPreCompForce_ChB_kN;
    ELSE
        rVotedPreCompForce_kN := rPreCompForce_ChC_kN;
    END_IF;
ELSIF nPreComp_VotingMode = 2 THEN
    IF bPreComp_ChA_Valid AND bPreComp_ChB_Valid THEN
        rVotedPreCompForce_kN := 0.5 * (rPreCompForce_ChA_kN + rPreCompForce_ChB_kN);
    ELSIF bPreComp_ChB_Valid AND bPreComp_ChC_Valid THEN
        rVotedPreCompForce_kN := 0.5 * (rPreCompForce_ChB_kN + rPreCompForce_ChC_kN);
    ELSIF bPreComp_ChA_Valid AND bPreComp_ChC_Valid THEN
        rVotedPreCompForce_kN := 0.5 * (rPreCompForce_ChA_kN + rPreCompForce_ChC_kN);
    ELSE
        rVotedPreCompForce_kN := rPreCompForce_ChA_kN;
    END_IF;
ELSIF nPreComp_VotingMode = 1 THEN
    IF bPreComp_ChA_Valid THEN
        rVotedPreCompForce_kN := rPreCompForce_ChA_kN;
    ELSIF bPreComp_ChB_Valid THEN
        rVotedPreCompForce_kN := rPreCompForce_ChB_kN;
    ELSE
        rVotedPreCompForce_kN := rPreCompForce_ChC_kN;
    END_IF;
ELSE
    rVotedPreCompForce_kN := rRecipeTargetPreCompForce_kN;
END_IF;


(* ============================================================================================== *)
(* CHANNEL 4: ROTARY PRESS MAIN COMPRESSION PIEZOELECTRIC LOAD CELLS [kN]                         *)
(* ============================================================================================== *)
rMainComp_Delta_AB := ABS(rMainCompForce_ChA_kN - rMainCompForce_ChB_kN);
rMainComp_Delta_BC := ABS(rMainCompForce_ChB_kN - rMainCompForce_ChC_kN);
rMainComp_Delta_CA := ABS(rMainCompForce_ChC_kN - rMainCompForce_ChA_kN);

IF (rMainComp_Delta_AB > rMainComp_DiscrepancyLimit_kN) OR 
   (rMainComp_Delta_BC > rMainComp_DiscrepancyLimit_kN) OR 
   (rMainComp_Delta_CA > rMainComp_DiscrepancyLimit_kN) THEN
    rMainComp_DiscrepancyTimer_s := rMainComp_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rMainComp_DiscrepancyTimer_s >= T_DISCREPANCY_MAX_SEC THEN
        IF (rMainComp_Delta_AB > rMainComp_DiscrepancyLimit_kN) AND (rMainComp_Delta_CA > rMainComp_DiscrepancyLimit_kN) THEN
            bMainComp_ChA_Valid := FALSE;
            nMainComp_VotingMode := 2;
        ELSIF (rMainComp_Delta_AB > rMainComp_DiscrepancyLimit_kN) AND (rMainComp_Delta_BC > rMainComp_DiscrepancyLimit_kN) THEN
            bMainComp_ChB_Valid := FALSE;
            nMainComp_VotingMode := 2;
        ELSIF (rMainComp_Delta_BC > rMainComp_DiscrepancyLimit_kN) AND (rMainComp_Delta_CA > rMainComp_DiscrepancyLimit_kN) THEN
            bMainComp_ChC_Valid := FALSE;
            nMainComp_VotingMode := 2;
        ELSE
            bMainComp_ChA_Valid := FALSE;
            bMainComp_ChB_Valid := FALSE;
            nMainComp_VotingMode := 1;
        END_IF;
    END_IF;
ELSE
    rMainComp_DiscrepancyTimer_s := MAX(0.0, rMainComp_DiscrepancyTimer_s - (T_CYCLE_SEC * 0.5));
    bMainComp_ChA_Valid := TRUE;
    bMainComp_ChB_Valid := TRUE;
    bMainComp_ChC_Valid := TRUE;
    nMainComp_VotingMode := 3;
END_IF;

IF nMainComp_VotingMode = 3 THEN
    IF ((rMainCompForce_ChA_kN >= rMainCompForce_ChB_kN) AND (rMainCompForce_ChA_kN <= rMainCompForce_ChC_kN)) OR
       ((rMainCompForce_ChA_kN <= rMainCompForce_ChB_kN) AND (rMainCompForce_ChA_kN >= rMainCompForce_ChC_kN)) THEN
        rVotedMainCompForce_kN := rMainCompForce_ChA_kN;
    ELSIF ((rMainCompForce_ChB_kN >= rMainCompForce_ChA_kN) AND (rMainCompForce_ChB_kN <= rMainCompForce_ChC_kN)) OR
          ((rMainCompForce_ChB_kN <= rMainCompForce_ChA_kN) AND (rMainCompForce_ChB_kN >= rMainCompForce_ChC_kN)) THEN
        rVotedMainCompForce_kN := rMainCompForce_ChB_kN;
    ELSE
        rVotedMainCompForce_kN := rMainCompForce_ChC_kN;
    END_IF;
ELSIF nMainComp_VotingMode = 2 THEN
    IF bMainComp_ChA_Valid AND bMainComp_ChB_Valid THEN
        rVotedMainCompForce_kN := 0.5 * (rMainCompForce_ChA_kN + rMainCompForce_ChB_kN);
    ELSIF bMainComp_ChB_Valid AND bMainComp_ChC_Valid THEN
        rVotedMainCompForce_kN := 0.5 * (rMainCompForce_ChB_kN + rMainCompForce_ChC_kN);
    ELSIF bMainComp_ChA_Valid AND bMainComp_ChC_Valid THEN
        rVotedMainCompForce_kN := 0.5 * (rMainCompForce_ChA_kN + rMainCompForce_ChC_kN);
    ELSE
        rVotedMainCompForce_kN := rMainCompForce_ChA_kN;
    END_IF;
ELSIF nMainComp_VotingMode = 1 THEN
    IF bMainComp_ChA_Valid THEN
        rVotedMainCompForce_kN := rMainCompForce_ChA_kN;
    ELSIF bMainComp_ChB_Valid THEN
        rVotedMainCompForce_kN := rMainCompForce_ChB_kN;
    ELSE
        rVotedMainCompForce_kN := rMainCompForce_ChC_kN;
    END_IF;
ELSE
    rVotedMainCompForce_kN := rRecipeTargetMainCompForce_kN;
END_IF;


(* ============================================================================================== *)
(* CHANNEL 5: ROTARY PRESS TURRET RESOLVER SHAFT ENCODERS [rpm]                                   *)
(* ============================================================================================== *)
rTurret_Delta_AB := ABS(rTurretSpeed_ChA_rpm - rTurretSpeed_ChB_rpm);
rTurret_Delta_BC := ABS(rTurretSpeed_ChB_rpm - rTurretSpeed_ChC_rpm);
rTurret_Delta_CA := ABS(rTurretSpeed_ChC_rpm - rTurretSpeed_ChA_rpm);

IF (rTurret_Delta_AB > rTurret_DiscrepancyLimit_rpm) OR 
   (rTurret_Delta_BC > rTurret_DiscrepancyLimit_rpm) OR 
   (rTurret_Delta_CA > rTurret_DiscrepancyLimit_rpm) THEN
    rTurret_DiscrepancyTimer_s := rTurret_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rTurret_DiscrepancyTimer_s >= T_DISCREPANCY_MAX_SEC THEN
        IF (rTurret_Delta_AB > rTurret_DiscrepancyLimit_rpm) AND (rTurret_Delta_CA > rTurret_DiscrepancyLimit_rpm) THEN
            bTurret_ChA_Valid := FALSE;
            nTurret_VotingMode := 2;
        ELSIF (rTurret_Delta_AB > rTurret_DiscrepancyLimit_rpm) AND (rTurret_Delta_BC > rTurret_DiscrepancyLimit_rpm) THEN
            bTurret_ChB_Valid := FALSE;
            nTurret_VotingMode := 2;
        ELSIF (rTurret_Delta_BC > rTurret_DiscrepancyLimit_rpm) AND (rTurret_Delta_CA > rTurret_DiscrepancyLimit_rpm) THEN
            bTurret_ChC_Valid := FALSE;
            nTurret_VotingMode := 2;
        ELSE
            bTurret_ChA_Valid := FALSE;
            bTurret_ChB_Valid := FALSE;
            nTurret_VotingMode := 1;
        END_IF;
    END_IF;
ELSE
    rTurret_DiscrepancyTimer_s := MAX(0.0, rTurret_DiscrepancyTimer_s - (T_CYCLE_SEC * 0.5));
    bTurret_ChA_Valid := TRUE;
    bTurret_ChB_Valid := TRUE;
    bTurret_ChC_Valid := TRUE;
    nTurret_VotingMode := 3;
END_IF;

IF nTurret_VotingMode = 3 THEN
    IF ((rTurretSpeed_ChA_rpm >= rTurretSpeed_ChB_rpm) AND (rTurretSpeed_ChA_rpm <= rTurretSpeed_ChC_rpm)) OR
       ((rTurretSpeed_ChA_rpm <= rTurretSpeed_ChB_rpm) AND (rTurretSpeed_ChA_rpm >= rTurretSpeed_ChC_rpm)) THEN
        rVotedTurretSpeed_rpm := rTurretSpeed_ChA_rpm;
    ELSIF ((rTurretSpeed_ChB_rpm >= rTurretSpeed_ChA_rpm) AND (rTurretSpeed_ChB_rpm <= rTurretSpeed_ChC_rpm)) OR
          ((rTurretSpeed_ChB_rpm <= rTurretSpeed_ChA_rpm) AND (rTurretSpeed_ChB_rpm >= rTurretSpeed_ChC_rpm)) THEN
        rVotedTurretSpeed_rpm := rTurretSpeed_ChB_rpm;
    ELSE
        rVotedTurretSpeed_rpm := rTurretSpeed_ChC_rpm;
    END_IF;
ELSIF nTurret_VotingMode = 2 THEN
    IF bTurret_ChA_Valid AND bTurret_ChB_Valid THEN
        rVotedTurretSpeed_rpm := 0.5 * (rTurretSpeed_ChA_rpm + rTurretSpeed_ChB_rpm);
    ELSIF bTurret_ChB_Valid AND bTurret_ChC_Valid THEN
        rVotedTurretSpeed_rpm := 0.5 * (rTurretSpeed_ChB_rpm + rTurretSpeed_ChC_rpm);
    ELSIF bTurret_ChA_Valid AND bTurret_ChC_Valid THEN
        rVotedTurretSpeed_rpm := 0.5 * (rTurretSpeed_ChA_rpm + rTurretSpeed_ChC_rpm);
    ELSE
        rVotedTurretSpeed_rpm := rTurretSpeed_ChA_rpm;
    END_IF;
ELSIF nTurret_VotingMode = 1 THEN
    IF bTurret_ChA_Valid THEN
        rVotedTurretSpeed_rpm := rTurretSpeed_ChA_rpm;
    ELSIF bTurret_ChB_Valid THEN
        rVotedTurretSpeed_rpm := rTurretSpeed_ChB_rpm;
    ELSE
        rVotedTurretSpeed_rpm := rTurretSpeed_ChC_rpm;
    END_IF;
ELSE
    rVotedTurretSpeed_rpm := rRecipeTargetTurretSpeed_rpm;
END_IF;


(* ============================================================================================== *)
(* CHANNEL 6: CONTINUOUS FLUID BED DRYER PLENUM DIFFERENTIAL PRESSURE [mbar]                       *)
(* ============================================================================================== *)
rFBDiff_Delta_AB := ABS(rFluidBedDiffPress_ChA_mbar - rFluidBedDiffPress_ChB_mbar);
rFBDiff_Delta_BC := ABS(rFluidBedDiffPress_ChB_mbar - rFluidBedDiffPress_ChC_mbar);
rFBDiff_Delta_CA := ABS(rFluidBedDiffPress_ChC_mbar - rFluidBedDiffPress_ChA_mbar);

IF (rFBDiff_Delta_AB > rFBDiff_DiscrepancyLimit_mbar) OR 
   (rFBDiff_Delta_BC > rFBDiff_DiscrepancyLimit_mbar) OR 
   (rFBDiff_Delta_CA > rFBDiff_DiscrepancyLimit_mbar) THEN
    rFBDiff_DiscrepancyTimer_s := rFBDiff_DiscrepancyTimer_s + T_CYCLE_SEC;
    IF rFBDiff_DiscrepancyTimer_s >= T_DISCREPANCY_MAX_SEC THEN
        IF (rFBDiff_Delta_AB > rFBDiff_DiscrepancyLimit_mbar) AND (rFBDiff_Delta_CA > rFBDiff_DiscrepancyLimit_mbar) THEN
            bFBDiff_ChA_Valid := FALSE;
            nFBDiff_VotingMode := 2;
        ELSIF (rFBDiff_Delta_AB > rFBDiff_DiscrepancyLimit_mbar) AND (rFBDiff_Delta_BC > rFBDiff_DiscrepancyLimit_mbar) THEN
            bFBDiff_ChB_Valid := FALSE;
            nFBDiff_VotingMode := 2;
        ELSIF (rFBDiff_Delta_BC > rFBDiff_DiscrepancyLimit_mbar) AND (rFBDiff_Delta_CA > rFBDiff_DiscrepancyLimit_mbar) THEN
            bFBDiff_ChC_Valid := FALSE;
            nFBDiff_VotingMode := 2;
        ELSE
            bFBDiff_ChA_Valid := FALSE;
            bFBDiff_ChB_Valid := FALSE;
            nFBDiff_VotingMode := 1;
        END_IF;
    END_IF;
ELSE
    rFBDiff_DiscrepancyTimer_s := MAX(0.0, rFBDiff_DiscrepancyTimer_s - (T_CYCLE_SEC * 0.5));
    bFBDiff_ChA_Valid := TRUE;
    bFBDiff_ChB_Valid := TRUE;
    bFBDiff_ChC_Valid := TRUE;
    nFBDiff_VotingMode := 3;
END_IF;

IF nFBDiff_VotingMode = 3 THEN
    IF ((rFluidBedDiffPress_ChA_mbar >= rFluidBedDiffPress_ChB_mbar) AND (rFluidBedDiffPress_ChA_mbar <= rFluidBedDiffPress_ChC_mbar)) OR
       ((rFluidBedDiffPress_ChA_mbar <= rFluidBedDiffPress_ChB_mbar) AND (rFluidBedDiffPress_ChA_mbar >= rFluidBedDiffPress_ChC_mbar)) THEN
        rVotedFluidBedDiffPress_mbar := rFluidBedDiffPress_ChA_mbar;
    ELSIF ((rFluidBedDiffPress_ChB_mbar >= rFluidBedDiffPress_ChA_mbar) AND (rFluidBedDiffPress_ChB_mbar <= rFluidBedDiffPress_ChC_mbar)) OR
          ((rFluidBedDiffPress_ChB_mbar <= rFluidBedDiffPress_ChA_mbar) AND (rFluidBedDiffPress_ChB_mbar >= rFluidBedDiffPress_ChC_mbar)) THEN
        rVotedFluidBedDiffPress_mbar := rFluidBedDiffPress_ChB_mbar;
    ELSE
        rVotedFluidBedDiffPress_mbar := rFluidBedDiffPress_ChC_mbar;
    END_IF;
ELSIF nFBDiff_VotingMode = 2 THEN
    IF bFBDiff_ChA_Valid AND bFBDiff_ChB_Valid THEN
        rVotedFluidBedDiffPress_mbar := 0.5 * (rFluidBedDiffPress_ChA_mbar + rFluidBedDiffPress_ChB_mbar);
    ELSIF bFBDiff_ChB_Valid AND bFBDiff_ChC_Valid THEN
        rVotedFluidBedDiffPress_mbar := 0.5 * (rFluidBedDiffPress_ChB_mbar + rFluidBedDiffPress_ChC_mbar);
    ELSIF bFBDiff_ChA_Valid AND bFBDiff_ChC_Valid THEN
        rVotedFluidBedDiffPress_mbar := 0.5 * (rFluidBedDiffPress_ChA_mbar + rFluidBedDiffPress_ChC_mbar);
    ELSE
        rVotedFluidBedDiffPress_mbar := rFluidBedDiffPress_ChA_mbar;
    END_IF;
ELSIF nFBDiff_VotingMode = 1 THEN
    IF bFBDiff_ChA_Valid THEN
        rVotedFluidBedDiffPress_mbar := rFluidBedDiffPress_ChA_mbar;
    ELSIF bFBDiff_ChB_Valid THEN
        rVotedFluidBedDiffPress_mbar := rFluidBedDiffPress_ChB_mbar;
    ELSE
        rVotedFluidBedDiffPress_mbar := rFluidBedDiffPress_ChC_mbar;
    END_IF;
ELSE
    rVotedFluidBedDiffPress_mbar := 12.5; (* Nominal bed fluidization Delta-P *)
END_IF;
"""
