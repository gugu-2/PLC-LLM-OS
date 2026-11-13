# Part 3: 2oo3 Triple Modular Redundancy (TMR) Voting Architecture
import sys

def get_channel_tmr_code(
    chan_num, chan_tag, chan_desc, unit,
    input_a, input_b, input_c,
    timer_ab, timer_bc, timer_ca,
    fault_a, fault_b, fault_c,
    discrepancy_active, prev_voted, voted_filtered,
    out_voted_var,
    tol_val, debounce_time, min_val, max_val, max_rate, default_safe
):
    code = []
    code.append(f"    (* ------------------------------------------------------------------------------------------ *)")
    code.append(f"    (* CHANNEL {chan_num}: {chan_tag} — {chan_desc} [{unit}] *)")
    code.append(f"    (* ------------------------------------------------------------------------------------------ *)")
    code.append(f"    (* Step {chan_num}.1: Out-of-Range Sensor Hardware Boundary Checks *)")
    code.append(f"    IF ({input_a} < {min_val:.2f}) OR ({input_a} > {max_val:.2f}) THEN")
    code.append(f"        {fault_a} := TRUE;")
    code.append(f"    ELSE")
    code.append(f"        {fault_a} := FALSE;")
    code.append(f"    END_IF;")
    code.append(f"")
    code.append(f"    IF ({input_b} < {min_val:.2f}) OR ({input_b} > {max_val:.2f}) THEN")
    code.append(f"        {fault_b} := TRUE;")
    code.append(f"    ELSE")
    code.append(f"        {fault_b} := FALSE;")
    code.append(f"    END_IF;")
    code.append(f"")
    code.append(f"    IF ({input_c} < {min_val:.2f}) OR ({input_c} > {max_val:.2f}) THEN")
    code.append(f"        {fault_c} := TRUE;")
    code.append(f"    ELSE")
    code.append(f"        {fault_c} := FALSE;")
    code.append(f"    END_IF;")
    code.append(f"")
    code.append(f"    (* Step {chan_num}.2: Pairwise Sensor Deviation & Debounce Timers *)")
    code.append(f"    IF ABS({input_a} - {input_b}) > {tol_val:.2f} THEN")
    code.append(f"        {timer_ab} := {timer_ab} + tScanTime;")
    code.append(f"    ELSE")
    code.append(f"        IF {timer_ab} > 0.0 THEN")
    code.append(f"            {timer_ab} := {timer_ab} - (tScanTime * 2.0);")
    code.append(f"            IF {timer_ab} < 0.0 THEN {timer_ab} := 0.0; END_IF;")
    code.append(f"        END_IF;")
    code.append(f"    END_IF;")
    code.append(f"")
    code.append(f"    IF ABS({input_b} - {input_c}) > {tol_val:.2f} THEN")
    code.append(f"        {timer_bc} := {timer_bc} + tScanTime;")
    code.append(f"    ELSE")
    code.append(f"        IF {timer_bc} > 0.0 THEN")
    code.append(f"            {timer_bc} := {timer_bc} - (tScanTime * 2.0);")
    code.append(f"            IF {timer_bc} < 0.0 THEN {timer_bc} := 0.0; END_IF;")
    code.append(f"        END_IF;")
    code.append(f"    END_IF;")
    code.append(f"")
    code.append(f"    IF ABS({input_c} - {input_a}) > {tol_val:.2f} THEN")
    code.append(f"        {timer_ca} := {timer_ca} + tScanTime;")
    code.append(f"    ELSE")
    code.append(f"        IF {timer_ca} > 0.0 THEN")
    code.append(f"            {timer_ca} := {timer_ca} - (tScanTime * 2.0);")
    code.append(f"            IF {timer_ca} < 0.0 THEN {timer_ca} := 0.0; END_IF;")
    code.append(f"        END_IF;")
    code.append(f"    END_IF;")
    code.append(f"")
    code.append(f"    (* Step {chan_num}.3: Discrepancy Flagging & Channel Isolation *)")
    code.append(f"    IF ({timer_ab} >= {debounce_time:.2f}) OR ({timer_bc} >= {debounce_time:.2f}) OR ({timer_ca} >= {debounce_time:.2f}) THEN")
    code.append(f"        {discrepancy_active} := TRUE;")
    code.append(f"        (* Identify individual discordant channel *)")
    code.append(f"        IF ({timer_ab} >= {debounce_time:.2f}) AND ({timer_ca} >= {debounce_time:.2f}) THEN")
    code.append(f"            {fault_a} := TRUE;")
    code.append(f"        END_IF;")
    code.append(f"        IF ({timer_ab} >= {debounce_time:.2f}) AND ({timer_bc} >= {debounce_time:.2f}) THEN")
    code.append(f"            {fault_b} := TRUE;")
    code.append(f"        END_IF;")
    code.append(f"        IF ({timer_bc} >= {debounce_time:.2f}) AND ({timer_ca} >= {debounce_time:.2f}) THEN")
    code.append(f"            {fault_c} := TRUE;")
    code.append(f"        END_IF;")
    code.append(f"    ELSE")
    code.append(f"        {discrepancy_active} := FALSE;")
    code.append(f"    END_IF;")
    code.append(f"")
    code.append(f"    (* Step {chan_num}.4: 2oo3 Degraded Majority Voting Evaluation *)")
    code.append(f"    IF (NOT {fault_a}) AND (NOT {fault_b}) AND (NOT {fault_c}) THEN")
    code.append(f"        (* Triple healthy: True Median Selection *)")
    code.append(f"        IF (({input_a} >= {input_b}) AND ({input_a} <= {input_c})) OR (({input_a} <= {input_b}) AND ({input_a} >= {input_c})) THEN")
    code.append(f"            rTemp := {input_a};")
    code.append(f"        ELSIF (({input_b} >= {input_a}) AND ({input_b} <= {input_c})) OR (({input_b} <= {input_a}) AND ({input_b} >= {input_c})) THEN")
    code.append(f"            rTemp := {input_b};")
    code.append(f"        ELSE")
    code.append(f"            rTemp := {input_c};")
    code.append(f"        END_IF;")
    code.append(f"    ELSIF (NOT {fault_a}) AND (NOT {fault_b}) THEN")
    code.append(f"        (* Channel C degraded: 1oo2 Average of A and B *)")
    code.append(f"        rTemp := ({input_a} + {input_b}) * 0.5;")
    code.append(f"    ELSIF (NOT {fault_b}) AND (NOT {fault_c}) THEN")
    code.append(f"        (* Channel A degraded: 1oo2 Average of B and C *)")
    code.append(f"        rTemp := ({input_b} + {input_c}) * 0.5;")
    code.append(f"    ELSIF (NOT {fault_c}) AND (NOT {fault_a}) THEN")
    code.append(f"        (* Channel B degraded: 1oo2 Average of C and A *)")
    code.append(f"        rTemp := ({input_c} + {input_a}) * 0.5;")
    code.append(f"    ELSIF (NOT {fault_a}) THEN")
    code.append(f"        (* Two channels degraded: Single Channel A fallback *)")
    code.append(f"        rTemp := {input_a};")
    code.append(f"    ELSIF (NOT {fault_b}) THEN")
    code.append(f"        (* Two channels degraded: Single Channel B fallback *)")
    code.append(f"        rTemp := {input_b};")
    code.append(f"    ELSIF (NOT {fault_c}) THEN")
    code.append(f"        (* Two channels degraded: Single Channel C fallback *)")
    code.append(f"        rTemp := {input_c};")
    code.append(f"    ELSE")
    code.append(f"        (* All channels failed: Catastrophic Failsafe Default *)")
    code.append(f"        rTemp := {default_safe:.2f};")
    code.append(f"    END_IF;")
    code.append(f"")
    code.append(f"    (* Step {chan_num}.5: Bumpless Rate-of-Change Smoothing Filter *)")
    code.append(f"    rSum := rTemp - {prev_voted};")
    code.append(f"    IF rSum > {max_rate:.2f} THEN")
    code.append(f"        rSum := {max_rate:.2f};")
    code.append(f"    ELSIF rSum < -{max_rate:.2f} THEN")
    code.append(f"        rSum := -{max_rate:.2f};")
    code.append(f"    END_IF;")
    code.append(f"    {voted_filtered} := {prev_voted} + rSum;")
    code.append(f"    {prev_voted} := {voted_filtered};")
    code.append(f"    {out_voted_var} := {voted_filtered};")
    code.append("")
    return "\n".join(code)

def get_part3_tmr_voting():
    code = []
    code.append("(* ============================================================================================== *)")
    code.append("(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & SENSOR HEALTH ARCHITECTURE            *)")
    code.append("(* ============================================================================================== *)")
    
    # Channel 1: PT-101 Permeate Suction Pressure [mbar]
    # Range: -600.0 to +100.0 mbar, Tol: 15.0 mbar, Debounce: 2.5s, Rate: 10.0 mbar/scan, Default: -150.0 mbar
    code.append(get_channel_tmr_code(
        1, "PT-101", "Permeate Header Suction Pressure Transducers", "mbar",
        "rPermSuctionPress_PT101A", "rPermSuctionPress_PT101B", "rPermSuctionPress_PT101C",
        "rPT101_DiscrepancyTimerAB", "rPT101_DiscrepancyTimerBC", "rPT101_DiscrepancyTimerCA",
        "bPT101_FaultA", "bPT101_FaultB", "bPT101_FaultC",
        "bPT101_DiscrepancyActive", "rPT101_PrevVoted", "rPT101_VotedFiltered",
        "rVotedPermSuctionPress",
        15.0, 2.5, -600.0, 150.0, 10.0, -150.0
    ))

    # Channel 2: AT-102 Bioreactor MLSS Optical Turbidity [mg/L]
    # Range: 2000.0 to 25000.0 mg/L, Tol: 600.0 mg/L, Debounce: 3.0s, Rate: 50.0 mg/L/scan, Default: 10000.0 mg/L
    code.append(get_channel_tmr_code(
        2, "AT-102", "Mixed Liquor Suspended Solids Optical Turbidity Probes", "mg/L",
        "rBioreactorMLSS_AT102A", "rBioreactorMLSS_AT102B", "rBioreactorMLSS_AT102C",
        "rAT102_DiscrepancyTimerAB", "rAT102_DiscrepancyTimerBC", "rAT102_DiscrepancyTimerCA",
        "bAT102_FaultA", "bAT102_FaultB", "bAT102_FaultC",
        "bAT102_DiscrepancyActive", "rAT102_PrevVoted", "rAT102_VotedFiltered",
        "rVotedBioreactorMLSS",
        600.0, 3.0, 2000.0, 25000.0, 50.0, 10000.0
    ))

    # Channel 3: AT-103 Bioreactor DO Luminescent Probes [mg/L]
    # Range: 0.0 to 15.0 mg/L, Tol: 0.35 mg/L, Debounce: 2.0s, Rate: 0.15 mg/L/scan, Default: 2.0 mg/L
    code.append(get_channel_tmr_code(
        3, "AT-103", "Membrane Aerobic Basin Luminescent Dissolved Oxygen Probes", "mg/L",
        "rBioreactorDO_AT103A", "rBioreactorDO_AT103B", "rBioreactorDO_AT103C",
        "rAT103_DiscrepancyTimerAB", "rAT103_DiscrepancyTimerBC", "rAT103_DiscrepancyTimerCA",
        "bAT103_FaultA", "bAT103_FaultB", "bAT103_FaultC",
        "bAT103_DiscrepancyActive", "rAT103_PrevVoted", "rAT103_VotedFiltered",
        "rVotedBioreactorDO",
        0.35, 2.0, 0.0, 15.0, 0.15, 2.0
    ))

    # Channel 4: AT-104 Pre-Anoxic ORP Probes [mV]
    # Range: -500.0 to +300.0 mV, Tol: 25.0 mV, Debounce: 3.0s, Rate: 5.0 mV/scan, Default: -120.0 mV
    code.append(get_channel_tmr_code(
        4, "AT-104", "Pre-Anoxic Denitrification Zone ORP Potentiometric Sensors", "mV",
        "rPreAnoxicORP_AT104A", "rPreAnoxicORP_AT104B", "rPreAnoxicORP_AT104C",
        "rAT104_DiscrepancyTimerAB", "rAT104_DiscrepancyTimerBC", "rAT104_DiscrepancyTimerCA",
        "bAT104_FaultA", "bAT104_FaultB", "bAT104_FaultC",
        "bAT104_DiscrepancyActive", "rAT104_PrevVoted", "rAT104_VotedFiltered",
        "rVotedPreAnoxicORP",
        25.0, 3.0, -500.0, 300.0, 5.0, -120.0
    ))

    # Channel 5: FT-105 Permeate Electromagnetic Flowmeters [m3/h]
    # Range: 0.0 to 600.0 m3/h, Tol: 12.0 m3/h, Debounce: 2.0s, Rate: 5.0 m3/h/scan, Default: 260.0 m3/h
    code.append(get_channel_tmr_code(
        5, "FT-105", "Permeate Header Electromagnetic Discharge Flowmeters", "m3/h",
        "rPermeateFlow_FT105A", "rPermeateFlow_FT105B", "rPermeateFlow_FT105C",
        "rFT105_DiscrepancyTimerAB", "rFT105_DiscrepancyTimerBC", "rFT105_DiscrepancyTimerCA",
        "bFT105_FaultA", "bFT105_FaultB", "bFT105_FaultC",
        "bFT105_DiscrepancyActive", "rFT105_PrevVoted", "rFT105_VotedFiltered",
        "rVotedPermeateFlow",
        12.0, 2.0, 0.0, 600.0, 5.0, 260.0
    ))

    # Channel 6: PT-106 Membrane Air Scour Pressure Transducers [mbar]
    # Range: 0.0 to 1000.0 mbar, Tol: 25.0 mbar, Debounce: 2.5s, Rate: 15.0 mbar/scan, Default: 380.0 mbar
    code.append(get_channel_tmr_code(
        6, "PT-106", "Coarse-Bubble Air Scour Distribution Manifold Pressure", "mbar",
        "rScourAirPress_PT106A", "rScourAirPress_PT106B", "rScourAirPress_PT106C",
        "rPT106_DiscrepancyTimerAB", "rPT106_DiscrepancyTimerBC", "rPT106_DiscrepancyTimerCA",
        "bPT106_FaultA", "bPT106_FaultB", "bPT106_FaultC",
        "bPT106_DiscrepancyActive", "rPT106_PrevVoted", "rPT106_VotedFiltered",
        "rVotedScourAirPress",
        25.0, 2.5, 0.0, 1000.0, 15.0, 380.0
    ))

    return "\n".join(code)
