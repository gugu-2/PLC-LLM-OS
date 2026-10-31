# -*- coding: utf-8 -*-
"""
Generator for Phase 1: 2oo3 Triple Modular Redundant (TMR) Sensor Voting
"""

def generate_tmr_st():
    lines = []
    lines.append("(* ==================================================================================================================== *)")
    lines.append("(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY ARBITRATION                              *)")
    lines.append("(* ==================================================================================================================== *)")
    lines.append("")
    
    # Triad 1: Cargo Tank Dome 1 Vapor Pressure
    lines.append("""(* 1.1 Cargo Tank Vapor Pressure Transmitters (PT101A, PT101B, PT101C) [950.0 to 1250.0 mbar abs] *)
IF rTank_VaporPress_PT101A_mbar < 950.0 OR rTank_VaporPress_PT101A_mbar > 1250.0 THEN
    bTankP_A_Healthy := FALSE;
END_IF;
IF rTank_VaporPress_PT101B_mbar < 950.0 OR rTank_VaporPress_PT101B_mbar > 1250.0 THEN
    bTankP_B_Healthy := FALSE;
END_IF;
IF rTank_VaporPress_PT101C_mbar < 950.0 OR rTank_VaporPress_PT101C_mbar > 1250.0 THEN
    bTankP_C_Healthy := FALSE;
END_IF;

rTankP_Diff_AB := ABS(rTank_VaporPress_PT101A_mbar - rTank_VaporPress_PT101B_mbar);
rTankP_Diff_BC := ABS(rTank_VaporPress_PT101B_mbar - rTank_VaporPress_PT101C_mbar);
rTankP_Diff_CA := ABS(rTank_VaporPress_PT101C_mbar - rTank_VaporPress_PT101A_mbar);

(* Channel A vs B Discrepancy Persistence *)
IF rTankP_Diff_AB > 8.0 THEN
    rTankP_DiscAccum_AB_s := rTankP_DiscAccum_AB_s + rScanCycleTime_s;
    IF rTankP_DiscAccum_AB_s >= 1.50 THEN
        bTankP_Disc_AB := TRUE;
    END_IF;
ELSE
    rTankP_DiscAccum_AB_s := 0.0;
    bTankP_Disc_AB := FALSE;
END_IF;

(* Channel B vs C Discrepancy Persistence *)
IF rTankP_Diff_BC > 8.0 THEN
    rTankP_DiscAccum_BC_s := rTankP_DiscAccum_BC_s + rScanCycleTime_s;
    IF rTankP_DiscAccum_BC_s >= 1.50 THEN
        bTankP_Disc_BC := TRUE;
    END_IF;
ELSE
    rTankP_DiscAccum_BC_s := 0.0;
    bTankP_Disc_BC := FALSE;
END_IF;

(* Channel C vs A Discrepancy Persistence *)
IF rTankP_Diff_CA > 8.0 THEN
    rTankP_DiscAccum_CA_s := rTankP_DiscAccum_CA_s + rScanCycleTime_s;
    IF rTankP_DiscAccum_CA_s >= 1.50 THEN
        bTankP_Disc_CA := TRUE;
    END_IF;
ELSE
    rTankP_DiscAccum_CA_s := 0.0;
    bTankP_Disc_CA := FALSE;
END_IF;

(* Pairwise Fault Isolation Engine for Tank Vapor Pressure *)
IF bTankP_Disc_AB AND bTankP_Disc_CA AND NOT bTankP_Disc_BC THEN
    bTankP_A_Healthy := FALSE;
    bTankP_B_Healthy := TRUE;
    bTankP_C_Healthy := TRUE;
ELSIF bTankP_Disc_AB AND bTankP_Disc_BC AND NOT bTankP_Disc_CA THEN
    bTankP_A_Healthy := TRUE;
    bTankP_B_Healthy := FALSE;
    bTankP_C_Healthy := TRUE;
ELSIF bTankP_Disc_BC AND bTankP_Disc_CA AND NOT bTankP_Disc_AB THEN
    bTankP_A_Healthy := TRUE;
    bTankP_B_Healthy := TRUE;
    bTankP_C_Healthy := FALSE;
ELSIF bTankP_Disc_AB AND bTankP_Disc_BC AND bTankP_Disc_CA THEN
    bTankP_A_Healthy := FALSE;
    bTankP_B_Healthy := FALSE;
    bTankP_C_Healthy := FALSE;
END_IF;

iTankP_HealthyCount := 0;
IF bTankP_A_Healthy THEN iTankP_HealthyCount := iTankP_HealthyCount + 1; END_IF;
IF bTankP_B_Healthy THEN iTankP_HealthyCount := iTankP_HealthyCount + 1; END_IF;
IF bTankP_C_Healthy THEN iTankP_HealthyCount := iTankP_HealthyCount + 1; END_IF;

IF iTankP_HealthyCount = 3 THEN
    (* 2oo3 Median Voting *)
    IF (rTank_VaporPress_PT101A_mbar >= rTank_VaporPress_PT101B_mbar AND rTank_VaporPress_PT101A_mbar <= rTank_VaporPress_PT101C_mbar) OR
       (rTank_VaporPress_PT101A_mbar >= rTank_VaporPress_PT101C_mbar AND rTank_VaporPress_PT101A_mbar <= rTank_VaporPress_PT101B_mbar) THEN
        rVoted_TankP_raw := rTank_VaporPress_PT101A_mbar;
    ELSIF (rTank_VaporPress_PT101B_mbar >= rTank_VaporPress_PT101A_mbar AND rTank_VaporPress_PT101B_mbar <= rTank_VaporPress_PT101C_mbar) OR
          (rTank_VaporPress_PT101B_mbar >= rTank_VaporPress_PT101C_mbar AND rTank_VaporPress_PT101B_mbar <= rTank_VaporPress_PT101A_mbar) THEN
        rVoted_TankP_raw := rTank_VaporPress_PT101B_mbar;
    ELSE
        rVoted_TankP_raw := rTank_VaporPress_PT101C_mbar;
    END_IF;
ELSIF iTankP_HealthyCount = 2 THEN
    (* Degraded 1oo2 Mid-Average Voting *)
    IF NOT bTankP_A_Healthy THEN
        rVoted_TankP_raw := (rTank_VaporPress_PT101B_mbar + rTank_VaporPress_PT101C_mbar) * 0.50;
    ELSIF NOT bTankP_B_Healthy THEN
        rVoted_TankP_raw := (rTank_VaporPress_PT101A_mbar + rTank_VaporPress_PT101C_mbar) * 0.50;
    ELSE
        rVoted_TankP_raw := (rTank_VaporPress_PT101A_mbar + rTank_VaporPress_PT101B_mbar) * 0.50;
    END_IF;
ELSIF iTankP_HealthyCount = 1 THEN
    IF bTankP_A_Healthy THEN
        rVoted_TankP_raw := rTank_VaporPress_PT101A_mbar;
    ELSIF bTankP_B_Healthy THEN
        rVoted_TankP_raw := rTank_VaporPress_PT101B_mbar;
    ELSE
        rVoted_TankP_raw := rTank_VaporPress_PT101C_mbar;
    END_IF;
ELSE
    rVoted_TankP_raw := rPrevVoted_TankP;
END_IF;

(* Rate of Change Clamping for Noise Immunity (Max 15 mbar/s) *)
IF rPrevVoted_TankP <> 0.0 THEN
    rVoted_CargoTankPress_mbar := rPrevVoted_TankP + LIMIT(-15.0 * rScanCycleTime_s, rVoted_TankP_raw - rPrevVoted_TankP, 15.0 * rScanCycleTime_s);
ELSE
    rVoted_CargoTankPress_mbar := rVoted_TankP_raw;
END_IF;
rPrevVoted_TankP := rVoted_CargoTankPress_mbar;
""")

    # Triad 2: Compressor Suction Temperature
    lines.append("""(* 1.2 Cryogenic Compressor Stage 1 Suction Temperature RTDs (TT201A, TT201B, TT201C) [-180.0 to 15.0 deg C] *)
IF rComp_SuctTemp_TT201A_degC < -180.0 OR rComp_SuctTemp_TT201A_degC > 15.0 THEN
    bSuctT_A_Healthy := FALSE;
END_IF;
IF rComp_SuctTemp_TT201B_degC < -180.0 OR rComp_SuctTemp_TT201B_degC > 15.0 THEN
    bSuctT_B_Healthy := FALSE;
END_IF;
IF rComp_SuctTemp_TT201C_degC < -180.0 OR rComp_SuctTemp_TT201C_degC > 15.0 THEN
    bSuctT_C_Healthy := FALSE;
END_IF;

rSuctT_Diff_AB := ABS(rComp_SuctTemp_TT201A_degC - rComp_SuctTemp_TT201B_degC);
rSuctT_Diff_BC := ABS(rComp_SuctTemp_TT201B_degC - rComp_SuctTemp_TT201C_degC);
rSuctT_Diff_CA := ABS(rComp_SuctTemp_TT201C_degC - rComp_SuctTemp_TT201A_degC);

IF rSuctT_Diff_AB > 4.0 THEN
    rSuctT_DiscAccum_AB_s := rSuctT_DiscAccum_AB_s + rScanCycleTime_s;
    IF rSuctT_DiscAccum_AB_s >= 2.00 THEN
        bSuctT_Disc_AB := TRUE;
    END_IF;
ELSE
    rSuctT_DiscAccum_AB_s := 0.0;
    bSuctT_Disc_AB := FALSE;
END_IF;

IF rSuctT_Diff_BC > 4.0 THEN
    rSuctT_DiscAccum_BC_s := rSuctT_DiscAccum_BC_s + rScanCycleTime_s;
    IF rSuctT_DiscAccum_BC_s >= 2.00 THEN
        bSuctT_Disc_BC := TRUE;
    END_IF;
ELSE
    rSuctT_DiscAccum_BC_s := 0.0;
    bSuctT_Disc_BC := FALSE;
END_IF;

IF rSuctT_Diff_CA > 4.0 THEN
    rSuctT_DiscAccum_CA_s := rSuctT_DiscAccum_CA_s + rScanCycleTime_s;
    IF rSuctT_DiscAccum_CA_s >= 2.00 THEN
        bSuctT_Disc_CA := TRUE;
    END_IF;
ELSE
    rSuctT_DiscAccum_CA_s := 0.0;
    bSuctT_Disc_CA := FALSE;
END_IF;

IF bSuctT_Disc_AB AND bSuctT_Disc_CA AND NOT bSuctT_Disc_BC THEN
    bSuctT_A_Healthy := FALSE;
    bSuctT_B_Healthy := TRUE;
    bSuctT_C_Healthy := TRUE;
ELSIF bSuctT_Disc_AB AND bSuctT_Disc_BC AND NOT bSuctT_Disc_CA THEN
    bSuctT_A_Healthy := TRUE;
    bSuctT_B_Healthy := FALSE;
    bSuctT_C_Healthy := TRUE;
ELSIF bSuctT_Disc_BC AND bSuctT_Disc_CA AND NOT bSuctT_Disc_AB THEN
    bSuctT_A_Healthy := TRUE;
    bSuctT_B_Healthy := TRUE;
    bSuctT_C_Healthy := FALSE;
ELSIF bSuctT_Disc_AB AND bSuctT_Disc_BC AND bSuctT_Disc_CA THEN
    bSuctT_A_Healthy := FALSE;
    bSuctT_B_Healthy := FALSE;
    bSuctT_C_Healthy := FALSE;
END_IF;

iSuctT_HealthyCount := 0;
IF bSuctT_A_Healthy THEN iSuctT_HealthyCount := iSuctT_HealthyCount + 1; END_IF;
IF bSuctT_B_Healthy THEN iSuctT_HealthyCount := iSuctT_HealthyCount + 1; END_IF;
IF bSuctT_C_Healthy THEN iSuctT_HealthyCount := iSuctT_HealthyCount + 1; END_IF;

IF iSuctT_HealthyCount = 3 THEN
    IF (rComp_SuctTemp_TT201A_degC >= rComp_SuctTemp_TT201B_degC AND rComp_SuctTemp_TT201A_degC <= rComp_SuctTemp_TT201C_degC) OR
       (rComp_SuctTemp_TT201A_degC >= rComp_SuctTemp_TT201C_degC AND rComp_SuctTemp_TT201A_degC <= rComp_SuctTemp_TT201B_degC) THEN
        rVoted_SuctT_raw := rComp_SuctTemp_TT201A_degC;
    ELSIF (rComp_SuctTemp_TT201B_degC >= rComp_SuctTemp_TT201A_degC AND rComp_SuctTemp_TT201B_degC <= rComp_SuctTemp_TT201C_degC) OR
          (rComp_SuctTemp_TT201B_degC >= rComp_SuctTemp_TT201C_degC AND rComp_SuctTemp_TT201B_degC <= rComp_SuctTemp_TT201A_degC) THEN
        rVoted_SuctT_raw := rComp_SuctTemp_TT201B_degC;
    ELSE
        rVoted_SuctT_raw := rComp_SuctTemp_TT201C_degC;
    END_IF;
ELSIF iSuctT_HealthyCount = 2 THEN
    IF NOT bSuctT_A_Healthy THEN
        rVoted_SuctT_raw := (rComp_SuctTemp_TT201B_degC + rComp_SuctTemp_TT201C_degC) * 0.50;
    ELSIF NOT bSuctT_B_Healthy THEN
        rVoted_SuctT_raw := (rComp_SuctTemp_TT201A_degC + rComp_SuctTemp_TT201C_degC) * 0.50;
    ELSE
        rVoted_SuctT_raw := (rComp_SuctTemp_TT201A_degC + rComp_SuctTemp_TT201B_degC) * 0.50;
    END_IF;
ELSIF iSuctT_HealthyCount = 1 THEN
    IF bSuctT_A_Healthy THEN
        rVoted_SuctT_raw := rComp_SuctTemp_TT201A_degC;
    ELSIF bSuctT_B_Healthy THEN
        rVoted_SuctT_raw := rComp_SuctTemp_TT201B_degC;
    ELSE
        rVoted_SuctT_raw := rComp_SuctTemp_TT201C_degC;
    END_IF;
ELSE
    rVoted_SuctT_raw := rPrevVoted_SuctT;
END_IF;

IF rPrevVoted_SuctT <> 0.0 THEN
    rVoted_CompSuctionTemp_degC := rPrevVoted_SuctT + LIMIT(-5.0 * rScanCycleTime_s, rVoted_SuctT_raw - rPrevVoted_SuctT, 5.0 * rScanCycleTime_s);
ELSE
    rVoted_CompSuctionTemp_degC := rVoted_SuctT_raw;
END_IF;
rPrevVoted_SuctT := rVoted_CompSuctionTemp_degC;
""")

    # Triad 3: ME-GI 300 Bar Fuel Gas Header Pressure
    lines.append("""(* 1.3 ME-GI 300 Bar Fuel Gas Header Pressure Transmitters (PT301A, PT301B, PT301C) [0.0 to 380.0 bar] *)
IF rMEGI_HeaderPress_PT301A_bar < 0.0 OR rMEGI_HeaderPress_PT301A_bar > 380.0 THEN
    bMEGI_P_A_Healthy := FALSE;
END_IF;
IF rMEGI_HeaderPress_PT301B_bar < 0.0 OR rMEGI_HeaderPress_PT301B_bar > 380.0 THEN
    bMEGI_P_B_Healthy := FALSE;
END_IF;
IF rMEGI_HeaderPress_PT301C_bar < 0.0 OR rMEGI_HeaderPress_PT301C_bar > 380.0 THEN
    bMEGI_P_C_Healthy := FALSE;
END_IF;

rMEGI_P_Diff_AB := ABS(rMEGI_HeaderPress_PT301A_bar - rMEGI_HeaderPress_PT301B_bar);
rMEGI_P_Diff_BC := ABS(rMEGI_HeaderPress_PT301B_bar - rMEGI_HeaderPress_PT301C_bar);
rMEGI_P_Diff_CA := ABS(rMEGI_HeaderPress_PT301C_bar - rMEGI_HeaderPress_PT301A_bar);

IF rMEGI_P_Diff_AB > 4.5 THEN
    rMEGI_P_DiscAccum_AB_s := rMEGI_P_DiscAccum_AB_s + rScanCycleTime_s;
    IF rMEGI_P_DiscAccum_AB_s >= 0.50 THEN
        bMEGI_P_Disc_AB := TRUE;
    END_IF;
ELSE
    rMEGI_P_DiscAccum_AB_s := 0.0;
    bMEGI_P_Disc_AB := FALSE;
END_IF;

IF rMEGI_P_Diff_BC > 4.5 THEN
    rMEGI_P_DiscAccum_BC_s := rMEGI_P_DiscAccum_BC_s + rScanCycleTime_s;
    IF rMEGI_P_DiscAccum_BC_s >= 0.50 THEN
        bMEGI_P_Disc_BC := TRUE;
    END_IF;
ELSE
    rMEGI_P_DiscAccum_BC_s := 0.0;
    bMEGI_P_Disc_BC := FALSE;
END_IF;

IF rMEGI_P_Diff_CA > 4.5 THEN
    rMEGI_P_DiscAccum_CA_s := rMEGI_P_DiscAccum_CA_s + rScanCycleTime_s;
    IF rMEGI_P_DiscAccum_CA_s >= 0.50 THEN
        bMEGI_P_Disc_CA := TRUE;
    END_IF;
ELSE
    rMEGI_P_DiscAccum_CA_s := 0.0;
    bMEGI_P_Disc_CA := FALSE;
END_IF;

IF bMEGI_P_Disc_AB AND bMEGI_P_Disc_CA AND NOT bMEGI_P_Disc_BC THEN
    bMEGI_P_A_Healthy := FALSE;
    bMEGI_P_B_Healthy := TRUE;
    bMEGI_P_C_Healthy := TRUE;
ELSIF bMEGI_P_Disc_AB AND bMEGI_P_Disc_BC AND NOT bMEGI_P_Disc_CA THEN
    bMEGI_P_A_Healthy := TRUE;
    bMEGI_P_B_Healthy := FALSE;
    bMEGI_P_C_Healthy := TRUE;
ELSIF bMEGI_P_Disc_BC AND bMEGI_P_Disc_CA AND NOT bMEGI_P_Disc_AB THEN
    bMEGI_P_A_Healthy := TRUE;
    bMEGI_P_B_Healthy := TRUE;
    bMEGI_P_C_Healthy := FALSE;
ELSIF bMEGI_P_Disc_AB AND bMEGI_P_Disc_BC AND bMEGI_P_Disc_CA THEN
    bMEGI_P_A_Healthy := FALSE;
    bMEGI_P_B_Healthy := FALSE;
    bMEGI_P_C_Healthy := FALSE;
END_IF;

iMEGI_P_HealthyCount := 0;
IF bMEGI_P_A_Healthy THEN iMEGI_P_HealthyCount := iMEGI_P_HealthyCount + 1; END_IF;
IF bMEGI_P_B_Healthy THEN iMEGI_P_HealthyCount := iMEGI_P_HealthyCount + 1; END_IF;
IF bMEGI_P_C_Healthy THEN iMEGI_P_HealthyCount := iMEGI_P_HealthyCount + 1; END_IF;

IF iMEGI_P_HealthyCount = 3 THEN
    IF (rMEGI_HeaderPress_PT301A_bar >= rMEGI_HeaderPress_PT301B_bar AND rMEGI_HeaderPress_PT301A_bar <= rMEGI_HeaderPress_PT301C_bar) OR
       (rMEGI_HeaderPress_PT301A_bar >= rMEGI_HeaderPress_PT301C_bar AND rMEGI_HeaderPress_PT301A_bar <= rMEGI_HeaderPress_PT301B_bar) THEN
        rVoted_MEGI_P_raw := rMEGI_HeaderPress_PT301A_bar;
    ELSIF (rMEGI_HeaderPress_PT301B_bar >= rMEGI_HeaderPress_PT301A_bar AND rMEGI_HeaderPress_PT301B_bar <= rMEGI_HeaderPress_PT301C_bar) OR
          (rMEGI_HeaderPress_PT301B_bar >= rMEGI_HeaderPress_PT301C_bar AND rMEGI_HeaderPress_PT301B_bar <= rMEGI_HeaderPress_PT301A_bar) THEN
        rVoted_MEGI_P_raw := rMEGI_HeaderPress_PT301B_bar;
    ELSE
        rVoted_MEGI_P_raw := rMEGI_HeaderPress_PT301C_bar;
    END_IF;
ELSIF iMEGI_P_HealthyCount = 2 THEN
    IF NOT bMEGI_P_A_Healthy THEN
        rVoted_MEGI_P_raw := (rMEGI_HeaderPress_PT301B_bar + rMEGI_HeaderPress_PT301C_bar) * 0.50;
    ELSIF NOT bMEGI_P_B_Healthy THEN
        rVoted_MEGI_P_raw := (rMEGI_HeaderPress_PT301A_bar + rMEGI_HeaderPress_PT301C_bar) * 0.50;
    ELSE
        rVoted_MEGI_P_raw := (rMEGI_HeaderPress_PT301A_bar + rMEGI_HeaderPress_PT301B_bar) * 0.50;
    END_IF;
ELSIF iMEGI_P_HealthyCount = 1 THEN
    IF bMEGI_P_A_Healthy THEN
        rVoted_MEGI_P_raw := rMEGI_HeaderPress_PT301A_bar;
    ELSIF bMEGI_P_B_Healthy THEN
        rVoted_MEGI_P_raw := rMEGI_HeaderPress_PT301B_bar;
    ELSE
        rVoted_MEGI_P_raw := rMEGI_HeaderPress_PT301C_bar;
    END_IF;
ELSE
    rVoted_MEGI_P_raw := rPrevVoted_MEGI_P;
END_IF;

IF rPrevVoted_MEGI_P <> 0.0 THEN
    rVoted_MEGI_HeaderPress_bar := rPrevVoted_MEGI_P + LIMIT(-20.0 * rScanCycleTime_s, rVoted_MEGI_P_raw - rPrevVoted_MEGI_P, 20.0 * rScanCycleTime_s);
ELSE
    rVoted_MEGI_HeaderPress_bar := rVoted_MEGI_P_raw;
END_IF;
rPrevVoted_MEGI_P := rVoted_MEGI_HeaderPress_bar;
""")

    # Triad 4: Compressor Machinery Room Methane Gas Concentration
    lines.append("""(* 1.4 Compressor Machinery Room Optical IR Methane Detectors (AT401A, AT401B, AT401C) [0.0 to 100.0 % LEL] *)
IF rCompRoom_GasLEL_AT401A_pct < 0.0 OR rCompRoom_GasLEL_AT401A_pct > 100.0 THEN
    bGasLEL_A_Healthy := FALSE;
END_IF;
IF rCompRoom_GasLEL_AT401B_pct < 0.0 OR rCompRoom_GasLEL_AT401B_pct > 100.0 THEN
    bGasLEL_B_Healthy := FALSE;
END_IF;
IF rCompRoom_GasLEL_AT401C_pct < 0.0 OR rCompRoom_GasLEL_AT401C_pct > 100.0 THEN
    bGasLEL_C_Healthy := FALSE;
END_IF;

rGasLEL_Diff_AB := ABS(rCompRoom_GasLEL_AT401A_pct - rCompRoom_GasLEL_AT401B_pct);
rGasLEL_Diff_BC := ABS(rCompRoom_GasLEL_AT401B_pct - rCompRoom_GasLEL_AT401C_pct);
rGasLEL_Diff_CA := ABS(rCompRoom_GasLEL_AT401C_pct - rCompRoom_GasLEL_AT401A_pct);

IF rGasLEL_Diff_AB > 5.0 THEN
    rGasLEL_DiscAccum_AB_s := rGasLEL_DiscAccum_AB_s + rScanCycleTime_s;
    IF rGasLEL_DiscAccum_AB_s >= 1.00 THEN
        bGasLEL_Disc_AB := TRUE;
    END_IF;
ELSE
    rGasLEL_DiscAccum_AB_s := 0.0;
    bGasLEL_Disc_AB := FALSE;
END_IF;

IF rGasLEL_Diff_BC > 5.0 THEN
    rGasLEL_DiscAccum_BC_s := rGasLEL_DiscAccum_BC_s + rScanCycleTime_s;
    IF rGasLEL_DiscAccum_BC_s >= 1.00 THEN
        bGasLEL_Disc_BC := TRUE;
    END_IF;
ELSE
    rGasLEL_DiscAccum_BC_s := 0.0;
    bGasLEL_Disc_BC := FALSE;
END_IF;

IF rGasLEL_Diff_CA > 5.0 THEN
    rGasLEL_DiscAccum_CA_s := rGasLEL_DiscAccum_CA_s + rScanCycleTime_s;
    IF rGasLEL_DiscAccum_CA_s >= 1.00 THEN
        bGasLEL_Disc_CA := TRUE;
    END_IF;
ELSE
    rGasLEL_DiscAccum_CA_s := 0.0;
    bGasLEL_Disc_CA := FALSE;
END_IF;

IF bGasLEL_Disc_AB AND bGasLEL_Disc_CA AND NOT bGasLEL_Disc_BC THEN
    bGasLEL_A_Healthy := FALSE;
    bGasLEL_B_Healthy := TRUE;
    bGasLEL_C_Healthy := TRUE;
ELSIF bGasLEL_Disc_AB AND bGasLEL_Disc_BC AND NOT bGasLEL_Disc_CA THEN
    bGasLEL_A_Healthy := TRUE;
    bGasLEL_B_Healthy := FALSE;
    bGasLEL_C_Healthy := TRUE;
ELSIF bGasLEL_Disc_BC AND bGasLEL_Disc_CA AND NOT bGasLEL_Disc_AB THEN
    bGasLEL_A_Healthy := TRUE;
    bGasLEL_B_Healthy := TRUE;
    bGasLEL_C_Healthy := FALSE;
ELSIF bGasLEL_Disc_AB AND bGasLEL_Disc_BC AND bGasLEL_Disc_CA THEN
    bGasLEL_A_Healthy := FALSE;
    bGasLEL_B_Healthy := FALSE;
    bGasLEL_C_Healthy := FALSE;
END_IF;

iGasLEL_HealthyCount := 0;
IF bGasLEL_A_Healthy THEN iGasLEL_HealthyCount := iGasLEL_HealthyCount + 1; END_IF;
IF bGasLEL_B_Healthy THEN iGasLEL_HealthyCount := iGasLEL_HealthyCount + 1; END_IF;
IF bGasLEL_C_Healthy THEN iGasLEL_HealthyCount := iGasLEL_HealthyCount + 1; END_IF;

IF iGasLEL_HealthyCount = 3 THEN
    (* Maximum safety selection: In gas detection, 2oo3 median or highest of voted *)
    IF (rCompRoom_GasLEL_AT401A_pct >= rCompRoom_GasLEL_AT401B_pct AND rCompRoom_GasLEL_AT401A_pct <= rCompRoom_GasLEL_AT401C_pct) OR
       (rCompRoom_GasLEL_AT401A_pct >= rCompRoom_GasLEL_AT401C_pct AND rCompRoom_GasLEL_AT401A_pct <= rCompRoom_GasLEL_AT401B_pct) THEN
        rVoted_GasLEL_raw := rCompRoom_GasLEL_AT401A_pct;
    ELSIF (rCompRoom_GasLEL_AT401B_pct >= rCompRoom_GasLEL_AT401A_pct AND rCompRoom_GasLEL_AT401B_pct <= rCompRoom_GasLEL_AT401C_pct) OR
          (rCompRoom_GasLEL_AT401B_pct >= rCompRoom_GasLEL_AT401C_pct AND rCompRoom_GasLEL_AT401B_pct <= rCompRoom_GasLEL_AT401A_pct) THEN
        rVoted_GasLEL_raw := rCompRoom_GasLEL_AT401B_pct;
    ELSE
        rVoted_GasLEL_raw := rCompRoom_GasLEL_AT401C_pct;
    END_IF;
ELSIF iGasLEL_HealthyCount = 2 THEN
    IF NOT bGasLEL_A_Healthy THEN
        IF rCompRoom_GasLEL_AT401B_pct > rCompRoom_GasLEL_AT401C_pct THEN
            rVoted_GasLEL_raw := rCompRoom_GasLEL_AT401B_pct;
        ELSE
            rVoted_GasLEL_raw := rCompRoom_GasLEL_AT401C_pct;
        END_IF;
    ELSIF NOT bGasLEL_B_Healthy THEN
        IF rCompRoom_GasLEL_AT401A_pct > rCompRoom_GasLEL_AT401C_pct THEN
            rVoted_GasLEL_raw := rCompRoom_GasLEL_AT401A_pct;
        ELSE
            rVoted_GasLEL_raw := rCompRoom_GasLEL_AT401C_pct;
        END_IF;
    ELSE
        IF rCompRoom_GasLEL_AT401A_pct > rCompRoom_GasLEL_AT401B_pct THEN
            rVoted_GasLEL_raw := rCompRoom_GasLEL_AT401A_pct;
        ELSE
            rVoted_GasLEL_raw := rCompRoom_GasLEL_AT401B_pct;
        END_IF;
    END_IF;
ELSIF iGasLEL_HealthyCount = 1 THEN
    IF bGasLEL_A_Healthy THEN
        rVoted_GasLEL_raw := rCompRoom_GasLEL_AT401A_pct;
    ELSIF bGasLEL_B_Healthy THEN
        rVoted_GasLEL_raw := rCompRoom_GasLEL_AT401B_pct;
    ELSE
        rVoted_GasLEL_raw := rCompRoom_GasLEL_AT401C_pct;
    END_IF;
ELSE
    rVoted_GasLEL_raw := 100.0; (* Fail-Safe: Trip on Total Gas Detector Loss *)
END_IF;

IF rPrevVoted_GasLEL <> 0.0 THEN
    rVoted_CompRoomGasLEL_pct := rPrevVoted_GasLEL + LIMIT(-10.0 * rScanCycleTime_s, rVoted_GasLEL_raw - rPrevVoted_GasLEL, 25.0 * rScanCycleTime_s);
ELSE
    rVoted_CompRoomGasLEL_pct := rVoted_GasLEL_raw;
END_IF;
rPrevVoted_GasLEL := rVoted_CompRoomGasLEL_pct;
""")
    return "\n".join(lines)

print("Part 3 TMR voting logic generator written.")
