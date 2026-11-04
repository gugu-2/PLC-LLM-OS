# Complete generator script for FB_Chemical_CryoASU_DoubleColumn_AntiSurge
import json, uuid, re, os, sys

def generate_full_st_code():
    from build_cryo_asu import get_header_and_vars
    parts = []
    
    # Header, inputs, outputs, and internal vars
    parts.append(get_header_and_vars())
    
    # PHASE 0: First Scan Initialization
    parts.append("""
(* ===================================================================================================================
 * PHASE 0: FIRST SCAN SYSTEM INITIALIZATION & DISCRETE STATE-SPACE MATRIX SEEDING
 * =================================================================================================================== *)
IF bFirstScan THEN
    (* 8x8 Multivariable Discrete Plant Dynamic Matrix matA (Discretized at Ts = 0.020 s) *)
    (* States x = [Delta_P_mac, Delta_Q_mac, Delta_P_hp, Delta_P_lp, Delta_L_lox, Delta_C_c2h2, Delta_y_o2, Delta_N_exp]^T *)
    (* Row 1: MAC Discharge Pressure Dynamics *)
    matA[1, 1] := 0.9845; matA[1, 2] :=-0.00012; matA[1, 3] := 0.0125; matA[1, 4] := 0.0000; matA[1, 5] := 0.0000; matA[1, 6] := 0.0000; matA[1, 7] := 0.0000; matA[1, 8] := 0.0000;
    (* Row 2: MAC Suction Volumetric Flow Dynamics *)
    matA[2, 1] :=-145.20; matA[2, 2] := 0.96200; matA[2, 3] :=-35.400; matA[2, 4] := 0.0000; matA[2, 5] := 0.0000; matA[2, 6] := 0.0000; matA[2, 7] := 0.0000; matA[2, 8] := 0.0000;
    (* Row 3: Medium Pressure (HP) Column Top Pressure *)
    matA[3, 1] := 0.0185; matA[3, 2] := 0.00008; matA[3, 3] := 0.9780; matA[3, 4] := 0.0042; matA[3, 5] :=-0.0015; matA[3, 6] := 0.0000; matA[3, 7] := 0.0000; matA[3, 8] :=-0.00005;
    (* Row 4: Low Pressure (LP) Column Top Pressure *)
    matA[4, 1] := 0.0000; matA[4, 2] := 0.00000; matA[4, 3] := 0.0085; matA[4, 4] := 0.9810; matA[4, 5] := 0.0025; matA[4, 6] := 0.0000; matA[4, 7] := 0.0012; matA[4, 8] := 0.00008;
    (* Row 5: Main Reboiler Liquid Oxygen (LOX) Bath Level *)
    matA[5, 1] := 0.0000; matA[5, 2] := 0.00025; matA[5, 3] := 0.0450; matA[5, 4] :=-0.0820; matA[5, 5] := 0.9925; matA[5, 6] := 0.0000; matA[5, 7] :=-0.0150; matA[5, 8] := 0.00035;
    (* Row 6: Reboiler Hydrocarbon Acetylene Accumulation Kinetics *)
    matA[6, 1] := 0.0000; matA[6, 2] := 0.00001; matA[6, 3] := 0.0000; matA[6, 4] := 0.0000; matA[6, 5] :=-0.0005; matA[6, 6] := 0.9985; matA[6, 7] := 0.0000; matA[6, 8] := 0.0000;
    (* Row 7: Crude Argon Column Side-Draw Oxygen Impurity *)
    matA[7, 1] := 0.0000; matA[7, 2] := 0.00005; matA[7, 3] := 0.0025; matA[7, 4] :=-0.0065; matA[7, 5] := 0.0080; matA[7, 6] := 0.0000; matA[7, 7] := 0.9740; matA[7, 8] := 0.0000;
    (* Row 8: Cryogenic Turbo-Expander Rotational Shaft Speed *)
    matA[8, 1] := 18.500; matA[8, 2] := 0.04500; matA[8, 3] := 25.200; matA[8, 4] :=-14.800; matA[8, 5] := 0.0000; matA[8, 6] := 0.0000; matA[8, 7] := 0.0000; matA[8, 8] := 0.9890;

    (* 8x5 Discrete Actuator Coupling Matrix matB *)
    (* Controls u = [u_asv, u_igv, u_exp, u_purge, u_ar]^T *)
    matB[1, 1] :=-0.0350; matB[1, 2] := 0.0240; matB[1, 3] :=-0.0025; matB[1, 4] := 0.0000; matB[1, 5] := 0.0000;
    matB[2, 1] := 185.00; matB[2, 2] := 320.00; matB[2, 3] := 12.500; matB[2, 4] := 0.0000; matB[2, 5] := 0.0000;
    matB[3, 1] :=-0.0125; matB[3, 2] := 0.0185; matB[3, 3] :=-0.0150; matB[3, 4] := 0.0000; matB[3, 5] := 0.0000;
    matB[4, 1] := 0.0000; matB[4, 2] := 0.0050; matB[4, 3] := 0.0085; matB[4, 4] :=-0.0015; matB[4, 5] :=-0.0042;
    matB[5, 1] := 0.0000; matB[5, 2] := 0.0080; matB[5, 3] := 0.0120; matB[5, 4] :=-0.0450; matB[5, 5] :=-0.0280;
    matB[6, 1] := 0.0000; matB[6, 2] := 0.0000; matB[6, 3] := 0.0000; matB[6, 4] :=-0.0035; matB[6, 5] := 0.0000;
    matB[7, 1] := 0.0000; matB[7, 2] := 0.0000; matB[7, 3] := 0.0000; matB[7, 4] := 0.0000; matB[7, 5] := 0.0185;
    matB[8, 1] :=-12.000; matB[8, 2] := 8.5000; matB[8, 3] := 145.00; matB[8, 4] := 0.0000; matB[8, 5] := 0.0000;

    (* 8x8 Identity Output Observation Matrix matC *)
    FOR iLoop := 1 TO 8 DO
        FOR jLoop := 1 TO 8 DO
            IF iLoop = jLoop THEN
                matC[iLoop, jLoop] := 1.0;
            ELSE
                matC[iLoop, jLoop] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* 8x5 Zero Direct Feedthrough Matrix matD *)
    FOR iLoop := 1 TO 8 DO
        FOR jLoop := 1 TO 5 DO
            matD[iLoop, jLoop] := 0.0;
        END_FOR;
    END_FOR;

    (* Initialize State Reference Vector x_ref to Zero Operating Setpoint Deviations *)
    FOR iLoop := 1 TO 8 DO
        vecX[iLoop] := 0.0;
        vecX_next[iLoop] := 0.0;
        vecX_ref[iLoop] := 0.0;
    END_FOR;

    (* Initialize Prior Actuator Commands to Bumpless Defaults *)
    vecU[1] := 0.0;     (* MAC Anti-Surge Recycle Valve (Nominally 0% in production) *)
    vecU[2] := 75.0;    (* MAC IGV Angle (Nominally 75% open at design flow) *)
    vecU[3] := 55.0;    (* Expander Variable Inlet Nozzle (55% open) *)
    vecU[4] := 2.5;     (* LOX Continuous Purge (2.5% continuous bleed) *)
    vecU[5] := 12.0;    (* Crude Argon Column Side-Draw Valve (12% flow) *)

    FOR jLoop := 1 TO 5 DO
        vecU_prev[jLoop] := vecU[jLoop];
        vecDeltaU[jLoop] := 0.0;
        vecGradU[jLoop] := 0.0;
    END_FOR;

    (* Quadratic MPC Tracking Penalty Weights Diag(Q) *)
    arrQ_Weight[1] := 15.0;     (* High penalty on MAC Discharge Pressure Deviation *)
    arrQ_Weight[2] := 22.0;     (* High penalty on MAC Inlet Flow / Surge Proximity *)
    arrQ_Weight[3] := 8.5;      (* Moderate penalty on HP Column Pressure *)
    arrQ_Weight[4] := 12.0;     (* High penalty on LP Column Pressure *)
    arrQ_Weight[5] := 18.0;     (* High penalty on Main Reboiler LOX Level *)
    arrQ_Weight[6] := 150.0;    (* Extreme penalty on Reboiler Acetylene Impurity *)
    arrQ_Weight[7] := 35.0;     (* High penalty on Crude Argon Purity *)
    arrQ_Weight[8] := 5.0;      (* Moderate penalty on Expander Speed Deviation *)

    (* Quadratic MPC Actuator Effort Penalty Weights Diag(R) *)
    arrR_Weight[1] := 1.20;     (* Anti-Surge Valve Recycle Penalty (Energy Loss) *)
    arrR_Weight[2] := 0.45;     (* IGV Actuator Position Effort *)
    arrR_Weight[3] := 0.35;     (* Expander Nozzle Position Effort *)
    arrR_Weight[4] := 2.50;     (* LOX Purge Loss of Liquid Oxygen Yield *)
    arrR_Weight[5] := 0.80;     (* Crude Argon Side-Draw Flow Penalty *)

    (* Quadratic MPC Actuator Slew Rate Penalties Diag(S) *)
    arrS_Weight[1] := 0.15;     (* Fast anti-surge valve rapid opening permitted *)
    arrS_Weight[2] := 1.50;     (* Slower IGV mechanical vane slew *)
    arrS_Weight[3] := 0.85;     (* Expander nozzle hydraulic slew *)
    arrS_Weight[4] := 0.50;     (* Purge valve slew *)
    arrS_Weight[5] := 1.20;     (* Argon draw slew rate to avoid distillation upset *)

    (* Terminal State Penalties Diag(P) *)
    FOR iLoop := 1 TO 8 DO
        arrP_TerminalWeight[iLoop] := arrQ_Weight[iLoop] * 1.85;
    END_FOR;

    (* Hard Actuator Authority Constraints *)
    arrU_Min[1] := 0.0;   arrU_Max[1] := 100.0; (* Anti-surge valve: 0 to 100% *)
    arrU_Min[2] := 15.0;  arrU_Max[2] := 95.0;  (* IGV: 15% minimum to 95% maximum *)
    arrU_Min[3] := 10.0;  arrU_Max[3] := 90.0;  (* Expander nozzle: 10% to 90% *)
    arrU_Min[4] := 0.5;   arrU_Max[4] := 25.0;  (* LOX purge: 0.5% continuous safety min *)
    arrU_Min[5] := 0.0;   arrU_Max[5] := 35.0;  (* Argon side draw: 0 to 35% *)

    (* Maximum Permissible Slew per 20 ms Cycle *)
    arrDeltaU_Max[1] := 5.00;   (* 250% per second opening speed for anti-surge *)
    arrDeltaU_Max[2] := 0.20;   (* 10% per second for IGV *)
    arrDeltaU_Max[3] := 0.35;   (* 17.5% per second for expander nozzle *)
    arrDeltaU_Max[4] := 0.50;   (* 25% per second for purge valve *)
    arrDeltaU_Max[5] := 0.15;   (* 7.5% per second for argon side draw *)

    bFirstScan := FALSE;
END_IF;
""")

    # PHASE 1: 2oo3 TMR Voting across all 16 triplets
    # Let's generate each triplet systematically
    triplets = [
        ("Press_MAC", "PT_MAC_DISCHARGE_101", "rVoted_MAC_DischargePress_bar", "c_rTol_Press_MAC_bar", "6.20"),
        ("Flow_MAC", "FT_MAC_INLET_AIR_102", "rVoted_MAC_Flow_m3h", "c_rTol_Flow_MAC_m3h", "185000.0"),
        ("Press_HP", "PT_HP_COLUMN_TOP_201", "rVoted_HP_Pressure_bar", "c_rTol_Press_HP_bar", "5.95"),
        ("Press_LP", "PT_LP_COLUMN_TOP_202", "rVoted_LP_Pressure_bar", "c_rTol_Press_LP_bar", "1.42"),
        ("Temp_Bath", "TT_CONDENSER_BATH_301", "rVoted_CondenserTemp_degC", "c_rTol_Temp_Bath_degC", "-181.8"),
        ("Level_LOX", "LT_REBOILER_LOX_LEVEL_302", "rVoted_LOX_Level_pct", "c_rTol_Level_LOX_pct", "65.0"),
        ("Acetylene", "AIT_LOX_ACETYLENE_PPM_401", "rVoted_Acetylene_ppm", "c_rTol_Acetylene_ppm", "0.024"),
        ("Argon_O2", "AIT_ARGON_PURITY_O2_402", "rVoted_Argon_O2_pct", "c_rTol_Argon_O2_pct", "1.50"),
        ("Expander_RPM", "ST_EXPANDER_RPM_501", "rVoted_Expander_RPM", "c_rTol_Expander_RPM", "82500.0"),
        ("Expander_Nozzle", "ZT_EXPANDER_NOZZLE_POS_502", "rVoted_Expander_Nozzle_pct", "c_rTol_Expander_Nozzle_pct", "55.0"),
        ("Flow_GOX", "FT_GOX_PRODUCT_601", "rVoted_GOX_Flow_Nm3h", "c_rTol_Flow_GOX_Nm3h", "65000.0"),
        ("Flow_GAN", "FT_GAN_PRODUCT_602", "rVoted_GAN_Flow_Nm3h", "c_rTol_Flow_GAN_Nm3h", "125000.0"),
        ("Venturi_DP", "DP_MAC_INLET_VENTURI_103", "rVoted_MAC_VenturiDP_mbar", "c_rTol_Venturi_DP_mbar", "48.4"),
        ("Temp_Discharge", "TT_MAC_DISCHARGE_104", "rVoted_MAC_DischargeTemp_degC", "c_rTol_Temp_Discharge_degC", "92.5"),
        ("Level_HPSump", "LT_HP_SUMP_LEVEL_203", "rVoted_HP_SumpLevel_pct", "c_rTol_Level_HPSump_pct", "52.0"),
        ("TotalHydrocarbon", "AIT_TOTAL_HYDROCARBON_403", "rVoted_TotalHydrocarbon_ppm", "c_rTol_TotalHydrocarbon_ppm", "0.43"),
    ]
    
    parts.append("""
(* ===================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS & BUMPLESS DEGRADATION
 * =================================================================================================================== *)
bDegradedSensorModeActive := FALSE;
""")
    for name, tag, voted_var, tol_var, fallback_val in triplets:
        triplet_st = f"""
(* --- 2oo3 TMR Voting: {tag} ({name}) --- *)
rDiffAB := ABS({tag}A - {tag}B);
rDiffBC := ABS({tag}B - {tag}C);
rDiffCA := ABS({tag}C - {tag}A);

(* Discrepancy Evaluation for Channel A *)
IF (rDiffAB > {tol_var}) AND (rDiffCA > {tol_var}) THEN
    rTimer_TMR_{name}_s := rTimer_TMR_{name}_s + c_rTs;
    IF rTimer_TMR_{name}_s >= c_rTMR_Timeout_s THEN
        bIso_{name}_A := TRUE;
    END_IF;
ELSE
    rTimer_TMR_{name}_s := MAX(0.0, rTimer_TMR_{name}_s - (0.25 * c_rTs));
END_IF;

(* Discrepancy Evaluation for Channel B *)
IF (rDiffAB > {tol_var}) AND (rDiffBC > {tol_var}) THEN
    rTimer_TMR_{name}_s := rTimer_TMR_{name}_s + c_rTs;
    IF rTimer_TMR_{name}_s >= c_rTMR_Timeout_s THEN
        bIso_{name}_B := TRUE;
    END_IF;
END_IF;

(* Discrepancy Evaluation for Channel C *)
IF (rDiffBC > {tol_var}) AND (rDiffCA > {tol_var}) THEN
    rTimer_TMR_{name}_s := rTimer_TMR_{name}_s + c_rTs;
    IF rTimer_TMR_{name}_s >= c_rTMR_Timeout_s THEN
        bIso_{name}_C := TRUE;
    END_IF;
END_IF;

(* Voted Selection & Fault Degradation *)
IF NOT bIso_{name}_A AND NOT bIso_{name}_B AND NOT bIso_{name}_C THEN
    (* All 3 Channels Healthy: Median Selection *)
    IF (({tag}A >= {tag}B AND {tag}A <= {tag}C) OR ({tag}A >= {tag}C AND {tag}A <= {tag}B)) THEN
        {voted_var} := {tag}A;
    ELSIF (({tag}B >= {tag}A AND {tag}B <= {tag}C) OR ({tag}B >= {tag}C AND {tag}B <= {tag}A)) THEN
        {voted_var} := {tag}B;
    ELSE
        {voted_var} := {tag}C;
    END_IF;
ELSIF NOT bIso_{name}_A AND NOT bIso_{name}_B THEN
    {voted_var} := ({tag}A + {tag}B) * 0.50;
    bDegradedSensorModeActive := TRUE;
ELSIF NOT bIso_{name}_B AND NOT bIso_{name}_C THEN
    {voted_var} := ({tag}B + {tag}C) * 0.50;
    bDegradedSensorModeActive := TRUE;
ELSIF NOT bIso_{name}_A AND NOT bIso_{name}_C THEN
    {voted_var} := ({tag}A + {tag}C) * 0.50;
    bDegradedSensorModeActive := TRUE;
ELSIF NOT bIso_{name}_A THEN
    {voted_var} := {tag}A;
    bDegradedSensorModeActive := TRUE;
ELSIF NOT bIso_{name}_B THEN
    {voted_var} := {tag}B;
    bDegradedSensorModeActive := TRUE;
ELSIF NOT bIso_{name}_C THEN
    {voted_var} := {tag}C;
    bDegradedSensorModeActive := TRUE;
ELSE
    {voted_var} := {fallback_val};
    bDegradedSensorModeActive := TRUE;
    bAlarm_TMR_ChannelDivergent := TRUE;
END_IF;
"""
        parts.append(triplet_st)
        
    return parts

print("Phase 0 and 1 ready.")
