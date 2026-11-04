# -*- coding: utf-8 -*-
"""
Module 4: Phase 1 2oo3 TMR Sensor Voting Engines for all 12 Transducer Triplets
"""

def generate_tmr_triplet(idx, tag, chA, chB, chC, tol, unit, out_var, timer_var, isoA, isoB, isoC):
    lines = []
    lines.append(f"    (* --------------------------------------------------------------------------------------- *)")
    lines.append(f"    (* 1.{idx} 2oo3 TMR VOTING: {tag} [{unit}] (Discrepancy Limit: {tol} {unit}) *)")
    lines.append(f"    (* --------------------------------------------------------------------------------------- *)")
    lines.append(f"    IF bResetAlarms THEN")
    lines.append(f"        {isoA} := FALSE;")
    lines.append(f"        {isoB} := FALSE;")
    lines.append(f"        {isoC} := FALSE;")
    lines.append(f"        {timer_var} := 0;")
    lines.append(f"    END_IF;")
    lines.append("")
    lines.append(f"    (* Calculate Absolute Channel Discrepancies *)")
    lines.append(f"    IF ABS({chA} - {chB}) > {tol} OR ABS({chB} - {chC}) > {tol} OR ABS({chC} - {chA}) > {tol} THEN")
    lines.append(f"        IF {timer_var} < 5000 THEN")
    lines.append(f"            {timer_var} := {timer_var} + 10; (* Discrepancy integration @ 10ms *)")
    lines.append(f"        END_IF;")
    lines.append(f"    ELSE")
    lines.append(f"        IF {timer_var} > 0 THEN")
    lines.append(f"            {timer_var} := {timer_var} - 10;")
    lines.append(f"        END_IF;")
    lines.append(f"    END_IF;")
    lines.append("")
    lines.append(f"    (* Channel Health Isolation Logic (500 ms Discrepancy Debounce) *)")
    lines.append(f"    IF {timer_var} >= 500 THEN")
    lines.append(f"        IF (ABS({chA} - {chB}) > {tol}) AND (ABS({chC} - {chA}) > {tol}) AND (ABS({chB} - {chC}) <= {tol}) THEN")
    lines.append(f"            {isoA} := TRUE; (* Channel A Deviated & Isolated *)")
    lines.append(f"        ELSIF (ABS({chA} - {chB}) > {tol}) AND (ABS({chB} - {chC}) > {tol}) AND (ABS({chC} - {chA}) <= {tol}) THEN")
    lines.append(f"            {isoB} := TRUE; (* Channel B Deviated & Isolated *)")
    lines.append(f"        ELSIF (ABS({chB} - {chC}) > {tol}) AND (ABS({chC} - {chA}) > {tol}) AND (ABS({chA} - {chB}) <= {tol}) THEN")
    lines.append(f"            {isoC} := TRUE; (* Channel C Deviated & Isolated *)")
    lines.append(f"        ELSE")
    lines.append(f"            (* Symmetric Divergence: Isolate Channel with Largest Deviation from Mean *)")
    lines.append(f"            IF ABS({chA} - (({chA} + {chB} + {chC}) / 3.0)) >= ABS({chB} - (({chA} + {chB} + {chC}) / 3.0)) AND ABS({chA} - (({chA} + {chB} + {chC}) / 3.0)) >= ABS({chC} - (({chA} + {chB} + {chC}) / 3.0)) THEN")
    lines.append(f"                {isoA} := TRUE;")
    lines.append(f"            ELSIF ABS({chB} - (({chA} + {chB} + {chC}) / 3.0)) >= ABS({chA} - (({chA} + {chB} + {chC}) / 3.0)) AND ABS({chB} - (({chA} + {chB} + {chC}) / 3.0)) >= ABS({chC} - (({chA} + {chB} + {chC}) / 3.0)) THEN")
    lines.append(f"                {isoB} := TRUE;")
    lines.append(f"            ELSE")
    lines.append(f"                {isoC} := TRUE;")
    lines.append(f"            END_IF;")
    lines.append(f"        END_IF;")
    lines.append(f"    END_IF;")
    lines.append("")
    lines.append(f"    (* Fault-Tolerant Voting Engine & Bumpless Degradation *)")
    lines.append(f"    IF NOT {isoA} AND NOT {isoB} AND NOT {isoC} THEN")
    lines.append(f"        (* All 3 Channels Healthy: Exact Median Selection *)")
    lines.append(f"        IF ({chA} >= {chB} AND {chA} <= {chC}) OR ({chA} >= {chC} AND {chA} <= {chB}) THEN")
    lines.append(f"            {out_var} := {chA};")
    lines.append(f"        ELSIF ({chB} >= {chA} AND {chB} <= {chC}) OR ({chB} >= {chC} AND {chB} <= {chA}) THEN")
    lines.append(f"            {out_var} := {chB};")
    lines.append(f"        ELSE")
    lines.append(f"            {out_var} := {chC};")
    lines.append(f"        END_IF;")
    lines.append(f"    ELSIF {isoA} AND NOT {isoB} AND NOT {isoC} THEN")
    lines.append(f"        (* Ch A Isolated: Degraded 1oo2 Average of B and C *)")
    lines.append(f"        {out_var} := ({chB} + {chC}) * 0.5;")
    lines.append(f"        bTMR_AnySensorDegraded := TRUE;")
    lines.append(f"    ELSIF {isoB} AND NOT {isoA} AND NOT {isoC} THEN")
    lines.append(f"        (* Ch B Isolated: Degraded 1oo2 Average of A and C *)")
    lines.append(f"        {out_var} := ({chA} + {chC}) * 0.5;")
    lines.append(f"        bTMR_AnySensorDegraded := TRUE;")
    lines.append(f"    ELSIF {isoC} AND NOT {isoA} AND NOT {isoB} THEN")
    lines.append(f"        (* Ch C Isolated: Degraded 1oo2 Average of A and B *)")
    lines.append(f"        {out_var} := ({chA} + {chB}) * 0.5;")
    lines.append(f"        bTMR_AnySensorDegraded := TRUE;")
    lines.append(f"    ELSIF {isoA} AND {isoB} AND NOT {isoC} THEN")
    lines.append(f"        (* Dual Failure: 1oo1 Last Healthy Fallback on Ch C *)")
    lines.append(f"        {out_var} := {chC};")
    lines.append(f"        bTMR_AnySensorDegraded := TRUE;")
    lines.append(f"    ELSIF {isoB} AND {isoC} AND NOT {isoA} THEN")
    lines.append(f"        (* Dual Failure: 1oo1 Last Healthy Fallback on Ch A *)")
    lines.append(f"        {out_var} := {chA};")
    lines.append(f"        bTMR_AnySensorDegraded := TRUE;")
    lines.append(f"    ELSIF {isoA} AND {isoC} AND NOT {isoB} THEN")
    lines.append(f"        (* Dual Failure: 1oo1 Last Healthy Fallback on Ch B *)")
    lines.append(f"        {out_var} := {chB};")
    lines.append(f"        bTMR_AnySensorDegraded := TRUE;")
    lines.append(f"    ELSE")
    lines.append(f"        (* Triple Failure: All 3 Channels Isolated - Critical Transducer Fault *)")
    lines.append(f"        {out_var} := {chA}; (* Fail-Safe Static Freeze *)")
    lines.append(f"        bTMR_CriticalSensorFailure := TRUE;")
    lines.append(f"    END_IF;")
    lines.append("")
    return "\n".join(lines)

def get_phase1_tmr():
    lines = []
    lines.append("(* =========================================================================================== *)")
    lines.append("(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINES                         *)")
    lines.append("(* =========================================================================================== *)")
    lines.append("bTMR_AnySensorDegraded := FALSE;")
    lines.append("bTMR_CriticalSensorFailure := FALSE;")
    lines.append("")

    triplets = [
        (1, "PT_CARGO_TANK_ULLAGE_101", "PT_CARGO_TANK_ULLAGE_101A", "PT_CARGO_TANK_ULLAGE_101B", "PT_CARGO_TANK_ULLAGE_101C",
         "8.0", "mbar", "rVoted_CargoTankUllage_mbar", "nDiscTimer_1_Ullage", "bIso_1A_Ullage", "bIso_1B_Ullage", "bIso_1C_Ullage"),

        (2, "TT_CARGO_LIQUID_TEMP_102", "TT_CARGO_LIQUID_TEMP_102A", "TT_CARGO_LIQUID_TEMP_102B", "TT_CARGO_LIQUID_TEMP_102C",
         "0.5", "deg C", "rVoted_CargoLiquidTemp_degC", "nDiscTimer_2_LiquidTemp", "bIso_2A_LiquidTemp", "bIso_2B_LiquidTemp", "bIso_2C_LiquidTemp"),

        (3, "PT_BOG_COMP_SUCTION_201", "PT_BOG_COMP_SUCTION_201A", "PT_BOG_COMP_SUCTION_201B", "PT_BOG_COMP_SUCTION_201C",
         "0.05", "bar", "rVoted_BOGCompSuction_bar", "nDiscTimer_3_Suction", "bIso_3A_Suction", "bIso_3B_Suction", "bIso_3C_Suction"),

        (4, "PT_BOG_COMP_DISCHARGE_202", "PT_BOG_COMP_DISCHARGE_202A", "PT_BOG_COMP_DISCHARGE_202B", "PT_BOG_COMP_DISCHARGE_202C",
         "3.5", "bar", "rVoted_BOGCompDischarge_bar", "nDiscTimer_4_Discharge", "bIso_4A_Discharge", "bIso_4B_Discharge", "bIso_4C_Discharge"),

        (5, "TT_BOG_COMP_STAGE4_203", "TT_BOG_COMP_STAGE4_203A", "TT_BOG_COMP_STAGE4_203B", "TT_BOG_COMP_STAGE4_203C",
         "2.0", "deg C", "rVoted_BOGStage4Temp_degC", "nDiscTimer_5_Stage4Temp", "bIso_5A_Stage4Temp", "bIso_5B_Stage4Temp", "bIso_5C_Stage4Temp"),

        (6, "PT_FGSS_MANIFOLD_301", "PT_FGSS_MANIFOLD_301A", "PT_FGSS_MANIFOLD_301B", "PT_FGSS_MANIFOLD_301C",
         "3.5", "bar", "rVoted_FGSSManifold_bar", "nDiscTimer_6_FGSS", "bIso_6A_FGSS", "bIso_6B_FGSS", "bIso_6C_FGSS"),

        (7, "FT_FUEL_GAS_MASS_FLOW_302", "FT_FUEL_GAS_MASS_FLOW_302A", "FT_FUEL_GAS_MASS_FLOW_302B", "FT_FUEL_GAS_MASS_FLOW_302C",
         "45.0", "kg/h", "rVoted_FuelGasMassFlow_kgh", "nDiscTimer_7_MassFlow", "bIso_7A_MassFlow", "bIso_7B_MassFlow", "bIso_7C_MassFlow"),

        (8, "TT_N2_RELIQUEFIER_RETURN_401", "TT_N2_RELIQUEFIER_RETURN_401A", "TT_N2_RELIQUEFIER_RETURN_401B", "TT_N2_RELIQUEFIER_RETURN_401C",
         "1.0", "deg C", "rVoted_N2ReliquefierReturn_degC", "nDiscTimer_8_ReliqReturn", "bIso_8A_ReliqReturn", "bIso_8B_ReliqReturn", "bIso_8C_ReliqReturn"),

        (9, "PT_GCU_COMBUSTION_CHAMBER_501", "PT_GCU_COMBUSTION_CHAMBER_501A", "PT_GCU_COMBUSTION_CHAMBER_501B", "PT_GCU_COMBUSTION_CHAMBER_501C",
         "1.5", "mbar", "rVoted_GCUChamberPress_mbar", "nDiscTimer_9_GCUDraft", "bIso_9A_GCUDraft", "bIso_9B_GCUDraft", "bIso_9C_GCUDraft"),

        (10, "AIT_ENCLOSED_SPACE_CH4_PPM_601", "AIT_ENCLOSED_SPACE_CH4_PPM_601A", "AIT_ENCLOSED_SPACE_CH4_PPM_601B", "AIT_ENCLOSED_SPACE_CH4_PPM_601C",
         "250.0", "ppm", "rVoted_EnclosedCH4_ppm", "nDiscTimer_10_CH4Ppm", "bIso_10A_CH4Ppm", "bIso_10B_CH4Ppm", "bIso_10C_CH4Ppm"),

        (11, "ZT_ESD_DOUBLE_BLOCK_VENT_701", "ZT_ESD_DOUBLE_BLOCK_VENT_701A", "ZT_ESD_DOUBLE_BLOCK_VENT_701B", "ZT_ESD_DOUBLE_BLOCK_VENT_701C",
         "2.0", "%", "rVoted_ESDValvePos_pct", "nDiscTimer_11_ESDPos", "bIso_11A_ESDPos", "bIso_11B_ESDPos", "bIso_11C_ESDPos"),

        (12, "WT_TANK_SLOSHING_PRESSURE_801", "WT_TANK_SLOSHING_PRESSURE_801A", "WT_TANK_SLOSHING_PRESSURE_801B", "WT_TANK_SLOSHING_PRESSURE_801C",
         "12.0", "kPa", "rVoted_SloshingPressure_kPa", "nDiscTimer_12_Slosh", "bIso_12A_Slosh", "bIso_12B_Slosh", "bIso_12C_Slosh")
    ]

    for item in triplets:
        lines.append(generate_tmr_triplet(*item))

    return "\n".join(lines)

print("Module 4 (Phase 1 TMR) ready.")
