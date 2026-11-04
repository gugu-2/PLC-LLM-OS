# -*- coding: utf-8 -*-
"""
Module: phase1_tmr.py
Generates Phase 1: 2oo3 Triple Modular Redundancy (TMR) Sensor Voting logic.
Includes pairwise delta calculations, tolerance gates, debounce discrepancy timers,
bumpless degradation, median selection, and packed diagnostic health bitmasks.
"""

def generate_phase1_tmr():
    s = []
    s.append("(* ================================================================================================= *)")
    s.append("(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY DEBOUNCE               *)")
    s.append("(* ================================================================================================= *)")
    s.append("(* Increment scan execution counter *)")
    s.append("r_Scan_Counter := r_Scan_Counter + 1;")
    s.append("dw_TMR_Health_Bitmask_1 := 16#00000000;")
    s.append("dw_TMR_Health_Bitmask_2 := 16#00000000;")
    s.append("")

    # Helper function inside generator to create standardized 2oo3 analog voting block
    def make_analog_voter(tag, chA, chB, chC, voted_var, health_var, timer_var, fault_var, tol, bitmask_dword, bit_pos, comment):
        lines = []
        lines.append(f"(* --- TMR Channel Group: {comment} ({tag}) --- *)")
        lines.append(f"r_Temp_Val_1 := ABS({chA} - {chB}); (* Delta AB *)")
        lines.append(f"r_Temp_Val_2 := ABS({chB} - {chC}); (* Delta BC *)")
        lines.append(f"r_Temp_Val_3 := ABS({chC} - {chA}); (* Delta CA *)")
        lines.append(f"IF (r_Temp_Val_1 <= {tol}) AND (r_Temp_Val_2 <= {tol}) AND (r_Temp_Val_3 <= {tol}) THEN")
        lines.append(f"    (* All 3 channels congruent: Median selection *)")
        lines.append(f"    IF (({chA} >= {chB}) AND ({chA} <= {chC})) OR (({chA} <= {chB}) AND ({chA} >= {chC})) THEN")
        lines.append(f"        {voted_var} := {chA};")
        lines.append(f"    ELSIF (({chB} >= {chA}) AND ({chB} <= {chC})) OR (({chB} <= {chA}) AND ({chB} >= {chC})) THEN")
        lines.append(f"        {voted_var} := {chB};")
        lines.append(f"    ELSE")
        lines.append(f"        {voted_var} := {chC};")
        lines.append(f"    END_IF;")
        lines.append(f"    {health_var} := TRUE;")
        lines.append(f"    {timer_var} := 0.0;")
        lines.append(f"    {fault_var} := FALSE;")
        lines.append(f"    {bitmask_dword} := {bitmask_dword} OR SHL(16#00000001, {bit_pos});")
        lines.append(f"ELSIF (r_Temp_Val_1 <= {tol}) THEN")
        lines.append(f"    (* Channel C deviates: Degrade to 1oo2 average of A & B *)")
        lines.append(f"    {voted_var} := 0.5 * ({chA} + {chB});")
        lines.append(f"    {health_var} := TRUE;")
        lines.append(f"    {timer_var} := {timer_var} + T_SAMPLE_SEC;")
        lines.append(f"    IF {timer_var} > 0.050 THEN")
        lines.append(f"        {fault_var} := TRUE;")
        lines.append(f"    END_IF;")
        lines.append(f"    {bitmask_dword} := {bitmask_dword} OR SHL(16#00000001, {bit_pos});")
        lines.append(f"ELSIF (r_Temp_Val_2 <= {tol}) THEN")
        lines.append(f"    (* Channel A deviates: Degrade to 1oo2 average of B & C *)")
        lines.append(f"    {voted_var} := 0.5 * ({chB} + {chC});")
        lines.append(f"    {health_var} := TRUE;")
        lines.append(f"    {timer_var} := {timer_var} + T_SAMPLE_SEC;")
        lines.append(f"    IF {timer_var} > 0.050 THEN")
        lines.append(f"        {fault_var} := TRUE;")
        lines.append(f"    END_IF;")
        lines.append(f"    {bitmask_dword} := {bitmask_dword} OR SHL(16#00000001, {bit_pos});")
        lines.append(f"ELSIF (r_Temp_Val_3 <= {tol}) THEN")
        lines.append(f"    (* Channel B deviates: Degrade to 1oo2 average of C & A *)")
        lines.append(f"    {voted_var} := 0.5 * ({chC} + {chA});")
        lines.append(f"    {health_var} := TRUE;")
        lines.append(f"    {timer_var} := {timer_var} + T_SAMPLE_SEC;")
        lines.append(f"    IF {timer_var} > 0.050 THEN")
        lines.append(f"        {fault_var} := TRUE;")
        lines.append(f"    END_IF;")
        lines.append(f"    {bitmask_dword} := {bitmask_dword} OR SHL(16#00000001, {bit_pos});")
        lines.append(f"ELSE")
        lines.append(f"    (* Full triplicated discrepancy: Hold prior voted value and debounce fault *)")
        lines.append(f"    {timer_var} := {timer_var} + T_SAMPLE_SEC;")
        lines.append(f"    IF {timer_var} > 0.040 THEN")
        lines.append(f"        {health_var} := FALSE;")
        lines.append(f"        {fault_var} := TRUE;")
        lines.append(f"    END_IF;")
        lines.append(f"END_IF;")
        lines.append("")
        return "\n".join(lines)

    # 1. Virtual Master Speed
    s.append(make_analog_voter("ST_101", "ST_VIRTUAL_MASTER_ELS_SPEED_101A", "ST_VIRTUAL_MASTER_ELS_SPEED_101B", "ST_VIRTUAL_MASTER_ELS_SPEED_101C",
                               "r_ELS_Speed_Voted", "b_ELS_Speed_TMR_Healthy", "r_ELS_Speed_Discrep_Timer", "b_ELS_Speed_Discrep_Fault",
                               "0.15", "dw_TMR_Health_Bitmask_1", 0, "ELS Virtual Master Line Speed"))

    # 2. Infeed Dancer Position
    s.append(make_analog_voter("ZT_102", "ZT_WEB_INLET_TENSION_DANCER_102A", "ZT_WEB_INLET_TENSION_DANCER_102B", "ZT_WEB_INLET_TENSION_DANCER_102C",
                               "r_Infeed_Dancer_Voted", "b_Infeed_Dancer_TMR_Healthy", "r_Infeed_Dancer_Discrep_Timer", "b_Infeed_Dancer_Discrep_Fault",
                               "2.50", "dw_TMR_Health_Bitmask_1", 1, "Infeed Dancer Position"))

    # 3. Infeed Tension Load Cell
    s.append(make_analog_voter("WT_103", "WT_INFEED_TENSION_LOADCELL_103A", "WT_INFEED_TENSION_LOADCELL_103B", "WT_INFEED_TENSION_LOADCELL_103C",
                               "r_Infeed_Tension_Voted", "b_Infeed_Tension_TMR_Healthy", "r_Infeed_Tension_Discrep_Timer", "b_Infeed_Tension_Discrep_Fault",
                               "8.0", "dw_TMR_Health_Bitmask_1", 2, "Infeed Web Tension Load Cell"))

    # 4. Cyan Register Circumferential & Lateral
    s.append(make_analog_voter("OPT_201_CIRC", "OPT_REGISTER_CYAN_DEV_201A", "OPT_REGISTER_CYAN_DEV_201B", "OPT_REGISTER_CYAN_DEV_201C",
                               "r_Cyan_Circ_Dev_Voted", "b_Cyan_Reg_TMR_Healthy", "r_Cyan_Reg_Discrep_Timer", "b_Cyan_Reg_Discrep_Fault",
                               "0.015", "dw_TMR_Health_Bitmask_1", 3, "Cyan Circumferential Register Deviation"))
    s.append(make_analog_voter("OPT_201_LAT", "OPT_REGISTER_CYAN_LAT_201A", "OPT_REGISTER_CYAN_LAT_201B", "OPT_REGISTER_CYAN_LAT_201C",
                               "r_Cyan_Lat_Dev_Voted", "b_Cyan_Reg_TMR_Healthy", "r_Cyan_Reg_Discrep_Timer", "b_Cyan_Reg_Discrep_Fault",
                               "0.015", "dw_TMR_Health_Bitmask_1", 4, "Cyan Lateral Register Deviation"))

    # 5. Magenta Register Circumferential & Lateral
    s.append(make_analog_voter("OPT_202_CIRC", "OPT_REGISTER_MAGENTA_DEV_202A", "OPT_REGISTER_MAGENTA_DEV_202B", "OPT_REGISTER_MAGENTA_DEV_202C",
                               "r_Magenta_Circ_Dev_Voted", "b_Magenta_Reg_TMR_Healthy", "r_Magenta_Reg_Discrep_Timer", "b_Magenta_Reg_Discrep_Fault",
                               "0.015", "dw_TMR_Health_Bitmask_1", 5, "Magenta Circumferential Register Deviation"))
    s.append(make_analog_voter("OPT_202_LAT", "OPT_REGISTER_MAGENTA_LAT_202A", "OPT_REGISTER_MAGENTA_LAT_202B", "OPT_REGISTER_MAGENTA_LAT_202C",
                               "r_Magenta_Lat_Dev_Voted", "b_Magenta_Reg_TMR_Healthy", "r_Magenta_Reg_Discrep_Timer", "b_Magenta_Reg_Discrep_Fault",
                               "0.015", "dw_TMR_Health_Bitmask_1", 6, "Magenta Lateral Register Deviation"))

    # 6. Yellow Register Circumferential & Lateral
    s.append(make_analog_voter("OPT_203_CIRC", "OPT_REGISTER_YELLOW_DEV_203A", "OPT_REGISTER_YELLOW_DEV_203B", "OPT_REGISTER_YELLOW_DEV_203C",
                               "r_Yellow_Circ_Dev_Voted", "b_Yellow_Reg_TMR_Healthy", "r_Yellow_Reg_Discrep_Timer", "b_Yellow_Reg_Discrep_Fault",
                               "0.015", "dw_TMR_Health_Bitmask_1", 7, "Yellow Circumferential Register Deviation"))
    s.append(make_analog_voter("OPT_203_LAT", "OPT_REGISTER_YELLOW_LAT_203A", "OPT_REGISTER_YELLOW_LAT_203B", "OPT_REGISTER_YELLOW_LAT_203C",
                               "r_Yellow_Lat_Dev_Voted", "b_Yellow_Reg_TMR_Healthy", "r_Yellow_Reg_Discrep_Timer", "b_Yellow_Reg_Discrep_Fault",
                               "0.015", "dw_TMR_Health_Bitmask_1", 8, "Yellow Lateral Register Deviation"))

    # 7. Black Register Circumferential & Lateral
    s.append(make_analog_voter("OPT_204_CIRC", "OPT_REGISTER_BLACK_DEV_204A", "OPT_REGISTER_BLACK_DEV_204B", "OPT_REGISTER_BLACK_DEV_204C",
                               "r_Black_Circ_Dev_Voted", "b_Black_Reg_TMR_Healthy", "r_Black_Reg_Discrep_Timer", "b_Black_Reg_Discrep_Fault",
                               "0.015", "dw_TMR_Health_Bitmask_1", 9, "Black Circumferential Register Deviation"))
    s.append(make_analog_voter("OPT_204_LAT", "OPT_REGISTER_BLACK_LAT_204A", "OPT_REGISTER_BLACK_LAT_204B", "OPT_REGISTER_BLACK_LAT_204C",
                               "r_Black_Lat_Dev_Voted", "b_Black_Reg_TMR_Healthy", "r_Black_Reg_Discrep_Timer", "b_Black_Reg_Discrep_Fault",
                               "0.015", "dw_TMR_Health_Bitmask_1", 10, "Black Lateral Register Deviation"))

    # 8. Dampening Solution Conductivity
    s.append(make_analog_voter("AIT_301", "AIT_DAMPENING_CONDUCTIVITY_301A", "AIT_DAMPENING_CONDUCTIVITY_301B", "AIT_DAMPENING_CONDUCTIVITY_301C",
                               "r_Damp_Conductivity_Voted", "b_Damp_Cond_TMR_Healthy", "r_Damp_Cond_Discrep_Timer", "b_Damp_Cond_Discrep_Fault",
                               "35.0", "dw_TMR_Health_Bitmask_1", 11, "Dampening Fountain Conductivity"))

    # 9. Dampening Solution Temperature
    s.append(make_analog_voter("TT_302", "TT_DAMPENING_CHILL_TEMP_302A", "TT_DAMPENING_CHILL_TEMP_302B", "TT_DAMPENING_CHILL_TEMP_302C",
                               "r_Damp_Temp_Voted", "b_Damp_Temp_TMR_Healthy", "r_Damp_Temp_Discrep_Timer", "b_Damp_Temp_Discrep_Fault",
                               "1.0", "dw_TMR_Health_Bitmask_1", 12, "Dampening Fountain Chilled Temp"))

    # 10. Dryer Zone 1 Temperature
    s.append(make_analog_voter("TT_401", "TT_DRYER_ZONE1_TEMP_401A", "TT_DRYER_ZONE1_TEMP_401B", "TT_DRYER_ZONE1_TEMP_401C",
                               "r_Dryer_Z1_Temp_Voted", "b_Dryer_Z1_TMR_Healthy", "r_Dryer_Z1_Discrep_Timer", "b_Dryer_Z1_Discrep_Fault",
                               "4.0", "dw_TMR_Health_Bitmask_1", 13, "Dryer Zone 1 Temperature"))

    # 11. Dryer Zone 2 Temperature
    s.append(make_analog_voter("TT_402", "TT_DRYER_ZONE2_TEMP_402A", "TT_DRYER_ZONE2_TEMP_402B", "TT_DRYER_ZONE2_TEMP_402C",
                               "r_Dryer_Z2_Temp_Voted", "b_Dryer_Z2_TMR_Healthy", "r_Dryer_Z2_Discrep_Timer", "b_Dryer_Z2_Discrep_Fault",
                               "4.0", "dw_TMR_Health_Bitmask_1", 14, "Dryer Zone 2 Temperature"))

    # 12. Dryer Zone 3 Temperature
    s.append(make_analog_voter("TT_403", "TT_DRYER_ZONE3_TEMP_403A", "TT_DRYER_ZONE3_TEMP_403B", "TT_DRYER_ZONE3_TEMP_403C",
                               "r_Dryer_Z3_Temp_Voted", "b_Dryer_Z3_TMR_Healthy", "r_Dryer_Z3_Discrep_Timer", "b_Dryer_Z3_Discrep_Fault",
                               "4.0", "dw_TMR_Health_Bitmask_1", 15, "Dryer Zone 3 Temperature"))

    # 13. Dryer Zone 4 Temperature
    s.append(make_analog_voter("TT_404", "TT_DRYER_ZONE4_TEMP_404A", "TT_DRYER_ZONE4_TEMP_404B", "TT_DRYER_ZONE4_TEMP_404C",
                               "r_Dryer_Z4_Temp_Voted", "b_Dryer_Z4_TMR_Healthy", "r_Dryer_Z4_Discrep_Timer", "b_Dryer_Z4_Discrep_Fault",
                               "4.0", "dw_TMR_Health_Bitmask_2", 0, "Dryer Zone 4 Temperature"))

    # 14. Dryer Solvent LEL Concentration
    s.append(make_analog_voter("AIT_405", "AIT_DRYER_SOLVENT_LEL_405A", "AIT_DRYER_SOLVENT_LEL_405B", "AIT_DRYER_SOLVENT_LEL_405C",
                               "r_Dryer_LEL_Voted", "b_Dryer_LEL_TMR_Healthy", "r_Dryer_LEL_Discrep_Timer", "b_Dryer_LEL_Discrep_Fault",
                               "1.8", "dw_TMR_Health_Bitmask_2", 1, "Dryer Flue Solvent LEL %"))

    # 15. Chill Stand Surface Temp & Web Tension
    s.append(make_analog_voter("TT_501", "TT_CHILL_ROLL_SURFACE_TEMP_501A", "TT_CHILL_ROLL_SURFACE_TEMP_501B", "TT_CHILL_ROLL_SURFACE_TEMP_501C",
                               "r_Chill_Temp_Voted", "b_Chill_TMR_Healthy", "r_Chill_Discrep_Timer", "b_Chill_Discrep_Fault",
                               "1.2", "dw_TMR_Health_Bitmask_2", 2, "Chill Roll Surface Temp"))
    s.append(make_analog_voter("ZT_502", "ZT_CHILL_WEB_TENSION_502A", "ZT_CHILL_WEB_TENSION_502B", "ZT_CHILL_WEB_TENSION_502C",
                               "r_Chill_Tension_Voted", "b_Chill_TMR_Healthy", "r_Chill_Discrep_Timer", "b_Chill_Discrep_Fault",
                               "10.0", "dw_TMR_Health_Bitmask_2", 3, "Chill Stand Web Tension"))

    # 16. Flying Splicer RPM & Position
    s.append(make_analog_voter("ST_601", "ST_SPLICER_NEW_ROLL_RPM_601A", "ST_SPLICER_NEW_ROLL_RPM_601B", "ST_SPLICER_NEW_ROLL_RPM_601C",
                               "r_Splicer_RPM_Voted", "b_Splicer_TMR_Healthy", "r_Splicer_Discrep_Timer", "b_Splicer_Discrep_Fault",
                               "5.0", "dw_TMR_Health_Bitmask_2", 4, "Splicer New Roll Pre-Drive RPM"))
    s.append(make_analog_voter("ZT_602", "ZT_SPLICER_PASTER_KNIFE_POS_602A", "ZT_SPLICER_PASTER_KNIFE_POS_602B", "ZT_SPLICER_PASTER_KNIFE_POS_602C",
                               "r_Splicer_Pos_Voted", "b_Splicer_TMR_Healthy", "r_Splicer_Discrep_Timer", "b_Splicer_Discrep_Fault",
                               "1.0", "dw_TMR_Health_Bitmask_2", 5, "Splicer Paster Carriage Position"))

    # 17. High-Speed Web Break Boolean Voting (2oo3 Discrete Logic)
    s.append("(* --- Discrete 2oo3 High-Speed Web Break Detectors --- *)")
    s.append("IF (OPT_WEB_BREAK_ULTRASONIC_701A AND OPT_WEB_BREAK_ULTRASONIC_701B) OR")
    s.append("   (OPT_WEB_BREAK_ULTRASONIC_701B AND OPT_WEB_BREAK_ULTRASONIC_701C) OR")
    s.append("   (OPT_WEB_BREAK_ULTRASONIC_701C AND OPT_WEB_BREAK_ULTRASONIC_701A) THEN")
    s.append("    b_Web_Break_Tower_Voted := TRUE;")
    s.append("    dw_TMR_Health_Bitmask_2 := dw_TMR_Health_Bitmask_2 OR SHL(16#00000001, 6);")
    s.append("ELSE")
    s.append("    b_Web_Break_Tower_Voted := FALSE;")
    s.append("END_IF;")
    s.append("")
    s.append("IF (OPT_WEB_BREAK_DRYER_EXIT_702A AND OPT_WEB_BREAK_DRYER_EXIT_702B) OR")
    s.append("   (OPT_WEB_BREAK_DRYER_EXIT_702B AND OPT_WEB_BREAK_DRYER_EXIT_702C) OR")
    s.append("   (OPT_WEB_BREAK_DRYER_EXIT_702C AND OPT_WEB_BREAK_DRYER_EXIT_702A) THEN")
    s.append("    b_Web_Break_Dryer_Voted := TRUE;")
    s.append("    dw_TMR_Health_Bitmask_2 := dw_TMR_Health_Bitmask_2 OR SHL(16#00000001, 7);")
    s.append("ELSE")
    s.append("    b_Web_Break_Dryer_Voted := FALSE;")
    s.append("END_IF;")
    s.append("")

    return "\n".join(s)
