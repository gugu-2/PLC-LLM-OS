# -*- coding: utf-8 -*-
"""
Generator module for Phase 1: 2oo3 TMR Sensor Voting Engines
"""

def generate_tmr_channel(name, tag, ch_a, ch_b, ch_c, tol, unit,
                         var_voted, var_degraded, disc_tmr_a, disc_tmr_b, disc_tmr_c,
                         hlth_a, hlth_b, hlth_c):
    return f"""    (* ------------------------------------------------------------------------------------------ *)
    (* TMR SENSOR CHANNEL: {name} [{unit}]                                                        *)
    (* Tag: {tag} | Redundancy: 2oo3 with Discrepancy Persistence Verification                  *)
    (* ------------------------------------------------------------------------------------------ *)
    val_temp := ABS({ch_a} - {ch_b});
    IF val_temp > {tol} THEN
        {disc_tmr_a} := {disc_tmr_a} + 1;
    ELSE
        IF {disc_tmr_a} > 0 THEN
            {disc_tmr_a} := {disc_tmr_a} - 1;
        END_IF;
    END_IF;

    val_temp := ABS({ch_b} - {ch_c});
    IF val_temp > {tol} THEN
        {disc_tmr_b} := {disc_tmr_b} + 1;
    ELSE
        IF {disc_tmr_b} > 0 THEN
            {disc_tmr_b} := {disc_tmr_b} - 1;
        END_IF;
    END_IF;

    val_temp := ABS({ch_c} - {ch_a});
    IF val_temp > {tol} THEN
        {disc_tmr_c} := {disc_tmr_c} + 1;
    ELSE
        IF {disc_tmr_c} > 0 THEN
            {disc_tmr_c} := {disc_tmr_c} - 1;
        END_IF;
    END_IF;

    (* Evaluate Individual Channel Health Criteria (Persistence Threshold = 25 scans / 50 ms) *)
    IF ({disc_tmr_a} > 25) AND ({disc_tmr_c} > 25) THEN
        {hlth_a} := FALSE;
    ELSE
        {hlth_a} := TRUE;
    END_IF;

    IF ({disc_tmr_a} > 25) AND ({disc_tmr_b} > 25) THEN
        {hlth_b} := FALSE;
    ELSE
        {hlth_b} := TRUE;
    END_IF;

    IF ({disc_tmr_b} > 25) AND ({disc_tmr_c} > 25) THEN
        {hlth_c} := FALSE;
    ELSE
        {hlth_c} := TRUE;
    END_IF;

    (* Redundant Voting Engine Matrix Execution *)
    IF {hlth_a} AND {hlth_b} AND {hlth_c} THEN
        (* Normal Triple Modular Redundancy: Median Value Selection *)
        IF (({ch_a} >= {ch_b}) AND ({ch_a} <= {ch_c})) OR (({ch_a} >= {ch_c}) AND ({ch_a} <= {ch_b})) THEN
            {var_voted} := {ch_a};
        ELSIF (({ch_b} >= {ch_a}) AND ({ch_b} <= {ch_c})) OR (({ch_b} >= {ch_c}) AND ({ch_b} <= {ch_a})) THEN
            {var_voted} := {ch_b};
        ELSE
            {var_voted} := {ch_c};
        END_IF;
        {var_degraded} := 0; (* Nominal 3-Channel 2oo3 Operation *)
    ELSIF {hlth_a} AND {hlth_b} THEN
        {var_voted} := ({ch_a} + {ch_b}) * 0.500000;
        {var_degraded} := 1; (* Degraded 1oo2 Operation (Channel C Discarded) *)
    ELSIF {hlth_b} AND {hlth_c} THEN
        {var_voted} := ({ch_b} + {ch_c}) * 0.500000;
        {var_degraded} := 1; (* Degraded 1oo2 Operation (Channel A Discarded) *)
    ELSIF {hlth_a} AND {hlth_c} THEN
        {var_voted} := ({ch_a} + {ch_c}) * 0.500000;
        {var_degraded} := 1; (* Degraded 1oo2 Operation (Channel B Discarded) *)
    ELSIF {hlth_a} THEN
        {var_voted} := {ch_a};
        {var_degraded} := 2; (* Severely Degraded Single Channel Hold (Channel A Only) *)
    ELSIF {hlth_b} THEN
        {var_voted} := {ch_b};
        {var_degraded} := 2; (* Severely Degraded Single Channel Hold (Channel B Only) *)
    ELSIF {hlth_c} THEN
        {var_voted} := {ch_c};
        {var_degraded} := 2; (* Severely Degraded Single Channel Hold (Channel C Only) *)
    ELSE
        {var_degraded} := 3; (* Total Sensor Channel Failure - Latched Fail-Safe Hold *)
    END_IF;
"""

def generate_phase_1():
    lines = []
    lines.append("""(* ============================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINES                           *)
(* Validates 19 Critical Process Instruments with Discrepancy Timers & Bumpless Failover          *)
(* ============================================================================================== *)
""")

    # 1. Crank Resolver
    lines.append(generate_tmr_channel(
        "Crankshaft Absolute Resolver Angle", "ST_CRANK_100",
        "ST_CRANK_RESOLVER_A", "ST_CRANK_RESOLVER_B", "ST_CRANK_RESOLVER_C",
        "1.250", "deg", "TMR_CRANK_VOTED_RESULT", "TMR_CRANK_DEGRADED_MODE",
        "TMR_CRANK_DISC_TMR_A", "TMR_CRANK_DISC_TMR_B", "TMR_CRANK_DISC_TMR_C",
        "TMR_CRANK_CH_A_HEALTHY", "TMR_CRANK_CH_B_HEALTHY", "TMR_CRANK_CH_C_HEALTHY"
    ))

    # 2. Slide Pos FL
    lines.append(generate_tmr_channel(
        "Slide Front-Left Optical Linear Scale", "ZT_SLIDE_FL_201",
        "ZT_SLIDE_POS_FL_A", "ZT_SLIDE_POS_FL_B", "ZT_SLIDE_POS_FL_C",
        "0.050", "mm", "TMR_SLIDE_FL_VOTED", "TMR_SLIDE_FL_DEGRADED",
        "TMR_SLIDE_FL_DISC_TMR_A", "TMR_SLIDE_FL_DISC_TMR_B", "TMR_SLIDE_FL_DISC_TMR_C",
        "TMR_SLIDE_FL_HEALTHY_A", "TMR_SLIDE_FL_HEALTHY_B", "TMR_SLIDE_FL_HEALTHY_C"
    ))

    # 3. Slide Pos FR
    lines.append(generate_tmr_channel(
        "Slide Front-Right Optical Linear Scale", "ZT_SLIDE_FR_202",
        "ZT_SLIDE_POS_FR_A", "ZT_SLIDE_POS_FR_B", "ZT_SLIDE_POS_FR_C",
        "0.050", "mm", "TMR_SLIDE_FR_VOTED", "TMR_SLIDE_FR_DEGRADED",
        "TMR_SLIDE_FR_DISC_TMR_A", "TMR_SLIDE_FR_DISC_TMR_B", "TMR_SLIDE_FR_DISC_TMR_C",
        "TMR_SLIDE_FR_HEALTHY_A", "TMR_SLIDE_FR_HEALTHY_B", "TMR_SLIDE_FR_HEALTHY_C"
    ))

    # 4. Slide Pos RL
    lines.append(generate_tmr_channel(
        "Slide Rear-Left Optical Linear Scale", "ZT_SLIDE_RL_203",
        "ZT_SLIDE_POS_RL_A", "ZT_SLIDE_POS_RL_B", "ZT_SLIDE_POS_RL_C",
        "0.050", "mm", "TMR_SLIDE_RL_VOTED", "TMR_SLIDE_RL_DEGRADED",
        "TMR_SLIDE_RL_DISC_TMR_A", "TMR_SLIDE_RL_DISC_TMR_B", "TMR_SLIDE_RL_DISC_TMR_C",
        "TMR_SLIDE_RL_HEALTHY_A", "TMR_SLIDE_RL_HEALTHY_B", "TMR_SLIDE_RL_HEALTHY_C"
    ))

    # 5. Slide Pos RR
    lines.append(generate_tmr_channel(
        "Slide Rear-Right Optical Linear Scale", "ZT_SLIDE_RR_204",
        "ZT_SLIDE_POS_RR_A", "ZT_SLIDE_POS_RR_B", "ZT_SLIDE_POS_RR_C",
        "0.050", "mm", "TMR_SLIDE_RR_VOTED", "TMR_SLIDE_RR_DEGRADED",
        "TMR_SLIDE_RR_DISC_TMR_A", "TMR_SLIDE_RR_DISC_TMR_B", "TMR_SLIDE_RR_DISC_TMR_C",
        "TMR_SLIDE_RR_HEALTHY_A", "TMR_SLIDE_RR_HEALTHY_B", "TMR_SLIDE_RR_HEALTHY_C"
    ))

    # 6. Tonnage FL
    lines.append(generate_tmr_channel(
        "Front-Left Press Frame Tonnage Strain Gauge", "WT_LOAD_FL_301",
        "WT_LOAD_FL_A", "WT_LOAD_FL_B", "WT_LOAD_FL_C",
        "250.00", "kN", "TMR_LOAD_FL_VOTED", "TMR_LOAD_FL_DEGRADED",
        "TMR_LOAD_FL_DISC_TMR_A", "TMR_LOAD_FL_DISC_TMR_B", "TMR_LOAD_FL_DISC_TMR_C",
        "TMR_LOAD_FL_HEALTHY_A", "TMR_LOAD_FL_HEALTHY_B", "TMR_LOAD_FL_HEALTHY_C"
    ))

    # 7. Tonnage FR
    lines.append(generate_tmr_channel(
        "Front-Right Press Frame Tonnage Strain Gauge", "WT_LOAD_FR_302",
        "WT_LOAD_FR_A", "WT_LOAD_FR_B", "WT_LOAD_FR_C",
        "250.00", "kN", "TMR_LOAD_FR_VOTED", "TMR_LOAD_FR_DEGRADED",
        "TMR_LOAD_FR_DISC_TMR_A", "TMR_LOAD_FR_DISC_TMR_B", "TMR_LOAD_FR_DISC_TMR_C",
        "TMR_LOAD_FR_HEALTHY_A", "TMR_LOAD_FR_HEALTHY_B", "TMR_LOAD_FR_HEALTHY_C"
    ))

    # 8. Tonnage RL
    lines.append(generate_tmr_channel(
        "Rear-Left Press Frame Tonnage Strain Gauge", "WT_LOAD_RL_303",
        "WT_LOAD_RL_A", "WT_LOAD_RL_B", "WT_LOAD_RL_C",
        "250.00", "kN", "TMR_LOAD_RL_VOTED", "TMR_LOAD_RL_DEGRADED",
        "TMR_LOAD_RL_DISC_TMR_A", "TMR_LOAD_RL_DISC_TMR_B", "TMR_LOAD_RL_DISC_TMR_C",
        "TMR_LOAD_RL_HEALTHY_A", "TMR_LOAD_RL_HEALTHY_B", "TMR_LOAD_RL_HEALTHY_C"
    ))

    # 9. Tonnage RR
    lines.append(generate_tmr_channel(
        "Rear-Right Press Frame Tonnage Strain Gauge", "WT_LOAD_RR_304",
        "WT_LOAD_RR_A", "WT_LOAD_RR_B", "WT_LOAD_RR_C",
        "250.00", "kN", "TMR_LOAD_RR_VOTED", "TMR_LOAD_RR_DEGRADED",
        "TMR_LOAD_RR_DISC_TMR_A", "TMR_LOAD_RR_DISC_TMR_B", "TMR_LOAD_RR_DISC_TMR_C",
        "TMR_LOAD_RR_HEALTHY_A", "TMR_LOAD_RR_HEALTHY_B", "TMR_LOAD_RR_HEALTHY_C"
    ))

    # 10 to 17: Cushion P1 to P8
    p_names = [
        "Die Cushion Cylinder 1 Chamber Pressure",
        "Die Cushion Cylinder 2 Chamber Pressure",
        "Die Cushion Cylinder 3 Chamber Pressure",
        "Die Cushion Cylinder 4 Chamber Pressure",
        "Die Cushion Cylinder 5 Chamber Pressure",
        "Die Cushion Cylinder 6 Chamber Pressure",
        "Die Cushion Cylinder 7 Chamber Pressure",
        "Die Cushion Cylinder 8 Chamber Pressure"
    ]
    for idx in range(1, 9):
        p_tag = f"PT_CUSH_P{idx}_40{idx}"
        ch_a = f"PT_CUSH_P{idx}_A"
        ch_b = f"PT_CUSH_P{idx}_B"
        ch_c = f"PT_CUSH_P{idx}_C"
        voted = f"TMR_PRESS_P{idx}_VOTED"
        deg = f"TMR_PRESS_P{idx}_DEGRADED"
        tmr_a = f"TMR_P_DISC_TMR_A[{idx}]"
        tmr_b = f"TMR_P_DISC_TMR_B[{idx}]"
        tmr_c = f"TMR_P_DISC_TMR_C[{idx}]"
        h_a = f"TMR_P_HEALTHY_A[{idx}]"
        h_b = f"TMR_P_HEALTHY_B[{idx}]"
        h_c = f"TMR_P_HEALTHY_C[{idx}]"
        lines.append(generate_tmr_channel(
            p_names[idx-1], p_tag, ch_a, ch_b, ch_c, "6.500", "bar",
            voted, deg, tmr_a, tmr_b, tmr_c, h_a, h_b, h_c
        ))

    # 18. Cushion Pos Left
    lines.append(generate_tmr_channel(
        "Die Cushion Left Bed Linear Displacement", "ZT_CUSH_L_501",
        "ZT_CUSH_POS_L_A", "ZT_CUSH_POS_L_B", "ZT_CUSH_POS_L_C",
        "0.150", "mm", "TMR_CUSH_POS_L_VOTED", "TMR_CUSH_POS_L_DEGRADED",
        "TMR_CUSH_DISC_TMR_L_A", "TMR_CUSH_DISC_TMR_L_B", "TMR_CUSH_DISC_TMR_L_C",
        "TMR_CUSH_HLTH_L_A", "TMR_CUSH_HLTH_L_B", "TMR_CUSH_HLTH_L_C"
    ))

    # 19. Cushion Pos Right
    lines.append(generate_tmr_channel(
        "Die Cushion Right Bed Linear Displacement", "ZT_CUSH_R_502",
        "ZT_CUSH_POS_R_A", "ZT_CUSH_POS_R_B", "ZT_CUSH_POS_R_C",
        "0.150", "mm", "TMR_CUSH_POS_R_VOTED", "TMR_CUSH_POS_R_DEGRADED",
        "TMR_CUSH_DISC_TMR_R_A", "TMR_CUSH_DISC_TMR_R_B", "TMR_CUSH_DISC_TMR_R_C",
        "TMR_CUSH_HLTH_R_A", "TMR_CUSH_HLTH_R_B", "TMR_CUSH_HLTH_R_C"
    ))

    return "".join(lines)

print("Phase 1 module loaded.")
