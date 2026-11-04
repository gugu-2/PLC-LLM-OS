# parts_water_rec_4.py - PHASE 1: 2oo3 TMR SENSOR VOTING

def get_phase1_tmr():
    groups = [
        ("MABR_DO", "rAIT_MABR_DO_101A", "rAIT_MABR_DO_101B", "rAIT_MABR_DO_101C", "rVoted_MABR_DO", "rTol_MABR_DO", "0.00", "12.00", "0.20", 0, 0),
        ("MABR_NH4", "rAIT_MABR_NH4_102A", "rAIT_MABR_NH4_102B", "rAIT_MABR_NH4_102C", "rVoted_MABR_NH4", "rTol_MABR_NH4", "0.00", "60.00", "1.50", 1, 3),
        ("MABR_NO3", "rAIT_MABR_NO3_103A", "rAIT_MABR_NO3_103B", "rAIT_MABR_NO3_103C", "rVoted_MABR_NO3", "rTol_MABR_NO3", "0.00", "60.00", "6.80", 2, 6),
        ("UF_TMP", "rPDT_UF_TMP_201A", "rPDT_UF_TMP_201B", "rPDT_UF_TMP_201C", "rVoted_UF_TMP", "rTol_UF_TMP", "-0.80", "3.00", "0.25", 3, 9),
        ("UF_Turb", "rAIT_UF_TURB_202A", "rAIT_UF_TURB_202B", "rAIT_UF_TURB_202C", "rVoted_UF_Turb", "rTol_UF_Turb", "0.00", "5.00", "0.05", 4, 12),
        ("RO_HP_Feed", "rPT_RO_HP_FEED_301A", "rPT_RO_HP_FEED_301B", "rPT_RO_HP_FEED_301C", "rVoted_RO_HP_Feed", "rTol_RO_HP_Feed", "0.00", "95.00", "65.00", 5, 15),
        ("RO_Conc_Press", "rPT_RO_CONC_PRESS_302A", "rPT_RO_CONC_PRESS_302B", "rPT_RO_CONC_PRESS_302C", "rVoted_RO_Conc_Press", "rTol_RO_Conc_Press", "0.00", "95.00", "62.50", 6, 18),
        ("RO_Cond", "rAIT_RO_COND_401A", "rAIT_RO_COND_401B", "rAIT_RO_COND_401C", "rVoted_RO_Cond", "rTol_RO_Cond", "0.00", "1500.00", "20.00", 7, 21),
        ("ERD_HP_In", "rPT_ERD_HP_IN_501A", "rPT_ERD_HP_IN_501B", "rPT_ERD_HP_IN_501C", "rVoted_ERD_HP_In", "rTol_ERD_HP_In", "0.00", "95.00", "62.00", 8, 24),
        ("UV_Trans", "rAIT_UV_TRANS_601A", "rAIT_UV_TRANS_601B", "rAIT_UV_TRANS_601C", "rVoted_UV_Trans", "rTol_UV_Trans", "10.00", "105.00", "95.00", 9, 27),
    ]

    code = []
    code.append("(* =====================================================================================================================\n")
    code.append(" * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY TIMERS\n")
    code.append(" * Executes deterministic median voting across 10 mission-critical triplicated sensor banks with bumpless\n")
    code.append(" * degradation (3 healthy -> 2oo3 median; 2 healthy -> 1oo2 mean; 1 healthy -> 1oo1 fallback; 0 -> safe clamp).\n")
    code.append(" * ===================================================================================================================== *)\n")
    code.append("dwSensorHealthMask := 16#0000_0000;\n")
    code.append("dwAlarmWord_Sensor_Discrepancy := 16#0000_0000;\n\n")

    for tag, chA, chB, chC, voted, tol, rmin, rmax, safe, disc_bit, health_base_bit in groups:
        code.append(f"(* --- TMR Sensor Bank: {tag} --- *)\n")
        code.append(f"rDelta_{tag}_AB := ABS({chA} - {chB});\n")
        code.append(f"rDelta_{tag}_BC := ABS({chB} - {chC});\n")
        code.append(f"rDelta_{tag}_CA := ABS({chC} - {chA});\n\n")

        # Discrepancy timers
        code.append(f"IF rDelta_{tag}_AB > {tol} THEN\n")
        code.append(f"    tTimer_{tag}_AB := tTimer_{tag}_AB + rPar_SampleTime_Sec;\n")
        code.append("ELSE\n")
        code.append(f"    tTimer_{tag}_AB := MAX(0.0, tTimer_{tag}_AB - (rPar_SampleTime_Sec * 0.5));\n")
        code.append("END_IF;\n\n")

        code.append(f"IF rDelta_{tag}_BC > {tol} THEN\n")
        code.append(f"    tTimer_{tag}_BC := tTimer_{tag}_BC + rPar_SampleTime_Sec;\n")
        code.append("ELSE\n")
        code.append(f"    tTimer_{tag}_BC := MAX(0.0, tTimer_{tag}_BC - (rPar_SampleTime_Sec * 0.5));\n")
        code.append("END_IF;\n\n")

        code.append(f"IF rDelta_{tag}_CA > {tol} THEN\n")
        code.append(f"    tTimer_{tag}_CA := tTimer_{tag}_CA + rPar_SampleTime_Sec;\n")
        code.append("ELSE\n")
        code.append(f"    tTimer_{tag}_CA := MAX(0.0, tTimer_{tag}_CA - (rPar_SampleTime_Sec * 0.5));\n")
        code.append("END_IF;\n\n")

        # Channel health flags
        code.append(f"bHealth_{tag}_A := ({chA} >= {rmin}) AND ({chA} <= {rmax}) AND ((tTimer_{tag}_AB < tDebounce_Limit_Sec) OR (tTimer_{tag}_CA < tDebounce_Limit_Sec));\n")
        code.append(f"bHealth_{tag}_B := ({chB} >= {rmin}) AND ({chB} <= {rmax}) AND ((tTimer_{tag}_AB < tDebounce_Limit_Sec) OR (tTimer_{tag}_BC < tDebounce_Limit_Sec));\n")
        code.append(f"bHealth_{tag}_C := ({chC} >= {rmin}) AND ({chC} <= {rmax}) AND ((tTimer_{tag}_BC < tDebounce_Limit_Sec) OR (tTimer_{tag}_CA < tDebounce_Limit_Sec));\n\n")

        # Health mask packing
        code.append(f"IF bHealth_{tag}_A THEN dwSensorHealthMask := dwSensorHealthMask OR SHL(DWORD#1, {health_base_bit}); END_IF;\n")
        code.append(f"IF bHealth_{tag}_B THEN dwSensorHealthMask := dwSensorHealthMask OR SHL(DWORD#1, {health_base_bit + 1}); END_IF;\n")
        code.append(f"IF bHealth_{tag}_C THEN dwSensorHealthMask := dwSensorHealthMask OR SHL(DWORD#1, {health_base_bit + 2}); END_IF;\n\n")

        # Voting branches
        code.append(f"IF bHealth_{tag}_A AND bHealth_{tag}_B AND bHealth_{tag}_C THEN\n")
        code.append(f"    (* 3 Channels Healthy: Exact 2oo3 Median Selection *)\n")
        code.append(f"    IF (({chA} >= {chB}) AND ({chA} <= {chC})) OR (({chA} >= {chC}) AND ({chA} <= {chB})) THEN\n")
        code.append(f"        {voted} := {chA};\n")
        code.append(f"    ELSIF (({chB} >= {chA}) AND ({chB} <= {chC})) OR (({chB} >= {chC}) AND ({chB} <= {chA})) THEN\n")
        code.append(f"        {voted} := {chB};\n")
        code.append("    ELSE\n")
        code.append(f"        {voted} := {chC};\n")
        code.append("    END_IF;\n")
        code.append(f"ELSIF bHealth_{tag}_A AND bHealth_{tag}_B THEN\n")
        code.append(f"    (* 1 Channel Faulty: Bumpless Degraded 1oo2 Mean A+B *)\n")
        code.append(f"    {voted} := 0.5 * ({chA} + {chB});\n")
        code.append(f"    dwAlarmWord_Sensor_Discrepancy := dwAlarmWord_Sensor_Discrepancy OR SHL(DWORD#1, {disc_bit});\n")
        code.append(f"ELSIF bHealth_{tag}_B AND bHealth_{tag}_C THEN\n")
        code.append(f"    (* 1 Channel Faulty: Bumpless Degraded 1oo2 Mean B+C *)\n")
        code.append(f"    {voted} := 0.5 * ({chB} + {chC});\n")
        code.append(f"    dwAlarmWord_Sensor_Discrepancy := dwAlarmWord_Sensor_Discrepancy OR SHL(DWORD#1, {disc_bit});\n")
        code.append(f"ELSIF bHealth_{tag}_A AND bHealth_{tag}_C THEN\n")
        code.append(f"    (* 1 Channel Faulty: Bumpless Degraded 1oo2 Mean A+C *)\n")
        code.append(f"    {voted} := 0.5 * ({chA} + {chC});\n")
        code.append(f"    dwAlarmWord_Sensor_Discrepancy := dwAlarmWord_Sensor_Discrepancy OR SHL(DWORD#1, {disc_bit});\n")
        code.append(f"ELSIF bHealth_{tag}_A THEN\n")
        code.append(f"    (* 2 Channels Faulty: Degraded 1oo1 Single Channel A *)\n")
        code.append(f"    {voted} := {chA};\n")
        code.append(f"    dwAlarmWord_Sensor_Discrepancy := dwAlarmWord_Sensor_Discrepancy OR SHL(DWORD#1, {disc_bit});\n")
        code.append(f"ELSIF bHealth_{tag}_B THEN\n")
        code.append(f"    (* 2 Channels Faulty: Degraded 1oo1 Single Channel B *)\n")
        code.append(f"    {voted} := {chB};\n")
        code.append(f"    dwAlarmWord_Sensor_Discrepancy := dwAlarmWord_Sensor_Discrepancy OR SHL(DWORD#1, {disc_bit});\n")
        code.append(f"ELSIF bHealth_{tag}_C THEN\n")
        code.append(f"    (* 2 Channels Faulty: Degraded 1oo1 Single Channel C *)\n")
        code.append(f"    {voted} := {chC};\n")
        code.append(f"    dwAlarmWord_Sensor_Discrepancy := dwAlarmWord_Sensor_Discrepancy OR SHL(DWORD#1, {disc_bit});\n")
        code.append("ELSE\n")
        code.append(f"    (* All 3 Channels Faulty: Fail-Safe Default Holding Clamp *)\n")
        code.append(f"    {voted} := {safe};\n")
        code.append(f"    dwAlarmWord_Sensor_Discrepancy := dwAlarmWord_Sensor_Discrepancy OR SHL(DWORD#1, {disc_bit});\n")
        code.append(f"    dwAlarmWord_Critical_Trip := dwAlarmWord_Critical_Trip OR SHL(DWORD#1, {disc_bit});\n")
        code.append("END_IF;\n\n")

    return "".join(code)
