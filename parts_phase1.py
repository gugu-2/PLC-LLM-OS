# parts_phase1.py
# Generates Phase 1: 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Engine across 9 sensor channels

def get_channel_tmr(name, chA, chB, chC, voted_var, tol_var, timerA, timerB, timerC, healthA, healthB, healthC, fault_bit_A, fault_bit_B, fault_bit_C, fault_word_var):
    lines = []
    lines.append(f"    (* --- 2oo3 TMR VOTING: {name} --- *)")
    lines.append(f"    rDiffAB := ABS({chA} - {chB});")
    lines.append(f"    rDiffBC := ABS({chB} - {chC});")
    lines.append(f"    rDiffCA := ABS({chC} - {chA});")
    lines.append("")
    lines.append(f"    (* Discrepancy accumulation timers for Channel A, B, C *)")
    lines.append(f"    IF (rDiffAB > {tol_var}) AND (rDiffCA > {tol_var}) THEN")
    lines.append(f"        {timerA} := {timerA} + (tCycleTime_ms * 0.001);")
    lines.append(f"        IF {timerA} >= cTmrMaxTripTime_s THEN")
    lines.append(f"            {healthA} := FALSE;")
    lines.append(f"            {fault_word_var} := {fault_word_var} OR 16#{fault_bit_A:08X};")
    lines.append(f"        END_IF;")
    lines.append(f"    ELSE")
    lines.append(f"        IF {timerA} > 0.0 THEN")
    lines.append(f"            {timerA} := {timerA} - (tCycleTime_ms * 0.002);")
    lines.append(f"            IF {timerA} < 0.0 THEN {timerA} := 0.0; END_IF;")
    lines.append(f"        END_IF;")
    lines.append(f"    END_IF;")
    lines.append("")
    lines.append(f"    IF (rDiffAB > {tol_var}) AND (rDiffBC > {tol_var}) THEN")
    lines.append(f"        {timerB} := {timerB} + (tCycleTime_ms * 0.001);")
    lines.append(f"        IF {timerB} >= cTmrMaxTripTime_s THEN")
    lines.append(f"            {healthB} := FALSE;")
    lines.append(f"            {fault_word_var} := {fault_word_var} OR 16#{fault_bit_B:08X};")
    lines.append(f"        END_IF;")
    lines.append(f"    ELSE")
    lines.append(f"        IF {timerB} > 0.0 THEN")
    lines.append(f"            {timerB} := {timerB} - (tCycleTime_ms * 0.002);")
    lines.append(f"            IF {timerB} < 0.0 THEN {timerB} := 0.0; END_IF;")
    lines.append(f"        END_IF;")
    lines.append(f"    END_IF;")
    lines.append("")
    lines.append(f"    IF (rDiffBC > {tol_var}) AND (rDiffCA > {tol_var}) THEN")
    lines.append(f"        {timerC} := {timerC} + (tCycleTime_ms * 0.001);")
    lines.append(f"        IF {timerC} >= cTmrMaxTripTime_s THEN")
    lines.append(f"            {healthC} := FALSE;")
    lines.append(f"            {fault_word_var} := {fault_word_var} OR 16#{fault_bit_C:08X};")
    lines.append(f"        END_IF;")
    lines.append(f"    ELSE")
    lines.append(f"        IF {timerC} > 0.0 THEN")
    lines.append(f"            {timerC} := {timerC} - (tCycleTime_ms * 0.002);")
    lines.append(f"            IF {timerC} < 0.0 THEN {timerC} := 0.0; END_IF;")
    lines.append(f"        END_IF;")
    lines.append(f"    END_IF;")
    lines.append("")
    lines.append(f"    (* Multi-stage voter arbitration: 2oo3 -> 1oo2 -> Fail-safe degradation *)")
    lines.append(f"    IF {healthA} AND {healthB} AND {healthC} THEN")
    lines.append(f"        (* All 3 channels healthy: True median selection *)")
    lines.append(f"        IF (({chA} >= {chB}) AND ({chA} <= {chC})) OR (({chA} >= {chC}) AND ({chA} <= {chB})) THEN")
    lines.append(f"            {voted_var} := {chA};")
    lines.append(f"        ELSIF (({chB} >= {chA}) AND ({chB} <= {chC})) OR (({chB} >= {chC}) AND ({chB} <= {chA})) THEN")
    lines.append(f"            {voted_var} := {chB};")
    lines.append(f"        ELSE")
    lines.append(f"            {voted_var} := {chC};")
    lines.append(f"        END_IF;")
    lines.append(f"    ELSIF {healthA} AND {healthB} THEN")
    lines.append(f"        (* Degradation: Ch C failed, 1oo2 mean of A and B *)")
    lines.append(f"        {voted_var} := 0.5 * ({chA} + {chB});")
    lines.append(f"    ELSIF {healthB} AND {healthC} THEN")
    lines.append(f"        (* Degradation: Ch A failed, 1oo2 mean of B and C *)")
    lines.append(f"        {voted_var} := 0.5 * ({chB} + {chC});")
    lines.append(f"    ELSIF {healthA} AND {healthC} THEN")
    lines.append(f"        (* Degradation: Ch B failed, 1oo2 mean of A and C *)")
    lines.append(f"        {voted_var} := 0.5 * ({chA} + {chC});")
    lines.append(f"    ELSIF {healthA} THEN")
    lines.append(f"        (* Severe Degradation: Single remaining channel A *)")
    lines.append(f"        {voted_var} := {chA};")
    lines.append(f"    ELSIF {healthB} THEN")
    lines.append(f"        (* Severe Degradation: Single remaining channel B *)")
    lines.append(f"        {voted_var} := {chB};")
    lines.append(f"    ELSIF {healthC} THEN")
    lines.append(f"        (* Severe Degradation: Single remaining channel C *)")
    lines.append(f"        {voted_var} := {chC};")
    lines.append(f"    ELSE")
    lines.append(f"        (* Total sensor suite loss: Raise fatal trip flag *)")
    lines.append(f"        dwIsaAlarmTripHH := dwIsaAlarmTripHH OR 16#00000001;")
    lines.append(f"    END_IF;")
    lines.append("")
    return "\n".join(lines)

def get_phase1_code():
    lines = []
    lines.append("(* ====================================================================================================")
    lines.append("   PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT-TOLERANT DEGRADATION ENGINE")
    lines.append("   ==================================================================================================== *)")
    lines.append("")
    lines.append("    (* Reset transient TMR fault word before arbitration pass *)")
    lines.append("    dwSensorTmrFaultWord := 16#00000000;")
    lines.append("")

    # Channel 1: Laser X
    lines.append(get_channel_tmr(
        "Laser Interferometer X Position [nm]",
        "rLaserPosX_ChA", "rLaserPosX_ChB", "rLaserPosX_ChC",
        "rTmrVoted_LaserX", "rTmrTol_LaserPos",
        "tTmrTimer_LaserX_A", "tTmrTimer_LaserX_B", "tTmrTimer_LaserX_C",
        "bTmrHealthy_LaserX_A", "bTmrHealthy_LaserX_B", "bTmrHealthy_LaserX_C",
        0x00000001, 0x00000002, 0x00000004, "dwSensorTmrFaultWord"
    ))

    # Channel 2: Laser Y
    lines.append(get_channel_tmr(
        "Laser Interferometer Y Position [nm]",
        "rLaserPosY_ChA", "rLaserPosY_ChB", "rLaserPosY_ChC",
        "rTmrVoted_LaserY", "rTmrTol_LaserPos",
        "tTmrTimer_LaserY_A", "tTmrTimer_LaserY_B", "tTmrTimer_LaserY_C",
        "bTmrHealthy_LaserY_A", "bTmrHealthy_LaserY_B", "bTmrHealthy_LaserY_C",
        0x00000008, 0x00000010, 0x00000020, "dwSensorTmrFaultWord"
    ))

    # Channel 3: Laser Z
    lines.append(get_channel_tmr(
        "Laser Interferometer Z Position [nm]",
        "rLaserPosZ_ChA", "rLaserPosZ_ChB", "rLaserPosZ_ChC",
        "rTmrVoted_LaserZ", "rTmrTol_LaserPos",
        "tTmrTimer_LaserZ_A", "tTmrTimer_LaserZ_B", "tTmrTimer_LaserZ_C",
        "bTmrHealthy_LaserZ_A", "bTmrHealthy_LaserZ_B", "bTmrHealthy_LaserZ_C",
        0x00000040, 0x00000080, 0x00000100, "dwSensorTmrFaultWord"
    ))

    # Channel 4: Capacitive Gap Z1
    lines.append(get_channel_tmr(
        "Capacitive Gap Sensor Z1 [um]",
        "rCapacitiveGapZ1_ChA", "rCapacitiveGapZ1_ChB", "rCapacitiveGapZ1_ChC",
        "rTmrVoted_CapZ1", "rTmrTol_CapGap",
        "tTmrTimer_CapZ1_A", "tTmrTimer_CapZ1_B", "tTmrTimer_CapZ1_C",
        "bTmrHealthy_CapZ1_A", "bTmrHealthy_CapZ1_B", "bTmrHealthy_CapZ1_C",
        0x00000200, 0x00000400, 0x00000800, "dwSensorTmrFaultWord"
    ))

    # Channel 5: Capacitive Gap Z2
    lines.append(get_channel_tmr(
        "Capacitive Gap Sensor Z2 [um]",
        "rCapacitiveGapZ2_ChA", "rCapacitiveGapZ2_ChB", "rCapacitiveGapZ2_ChC",
        "rTmrVoted_CapZ2", "rTmrTol_CapGap",
        "tTmrTimer_CapZ2_A", "tTmrTimer_CapZ2_B", "tTmrTimer_CapZ2_C",
        "bTmrHealthy_CapZ2_A", "bTmrHealthy_CapZ2_B", "bTmrHealthy_CapZ2_C",
        0x00001000, 0x00002000, 0x00004000, "dwSensorTmrFaultWord"
    ))

    # Channel 6: Capacitive Gap Z3
    lines.append(get_channel_tmr(
        "Capacitive Gap Sensor Z3 [um]",
        "rCapacitiveGapZ3_ChA", "rCapacitiveGapZ3_ChB", "rCapacitiveGapZ3_ChC",
        "rTmrVoted_CapZ3", "rTmrTol_CapGap",
        "tTmrTimer_CapZ3_A", "tTmrTimer_CapZ3_B", "tTmrTimer_CapZ3_C",
        "bTmrHealthy_CapZ3_A", "bTmrHealthy_CapZ3_B", "bTmrHealthy_CapZ3_C",
        0x00008000, 0x00010000, 0x00020000, "dwSensorTmrFaultWord"
    ))

    # Channel 7: Optical Alignment Mark X
    lines.append(get_channel_tmr(
        "Optical Chuck Alignment Mark X [nm]",
        "rOpticalAlignMarkX_ChA", "rOpticalAlignMarkX_ChB", "rOpticalAlignMarkX_ChC",
        "rTmrVoted_OptAlignX", "rTmrTol_OptAlign",
        "tTmrTimer_OptX_A", "tTmrTimer_OptX_B", "tTmrTimer_OptX_C",
        "bTmrHealthy_OptX_A", "bTmrHealthy_OptX_B", "bTmrHealthy_OptX_C",
        0x00040000, 0x00080000, 0x00100000, "dwSensorTmrFaultWord"
    ))

    # Channel 8: Optical Alignment Mark Y
    lines.append(get_channel_tmr(
        "Optical Chuck Alignment Mark Y [nm]",
        "rOpticalAlignMarkY_ChA", "rOpticalAlignMarkY_ChB", "rOpticalAlignMarkY_ChC",
        "rTmrVoted_OptAlignY", "rTmrTol_OptAlign",
        "tTmrTimer_OptY_A", "tTmrTimer_OptY_B", "tTmrTimer_OptY_C",
        "bTmrHealthy_OptY_A", "bTmrHealthy_OptY_B", "bTmrHealthy_OptY_C",
        0x00200000, 0x00400000, 0x00800000, "dwSensorTmrFaultWord"
    ))

    # Channel 9: Backside Helium Pressure
    lines.append(get_channel_tmr(
        "Backside Helium Pressure Transducer [mbar]",
        "rHeBacksidePress_ChA", "rHeBacksidePress_ChB", "rHeBacksidePress_ChC",
        "rTmrVoted_HePress", "rTmrTol_HePress",
        "tTmrTimer_He_A", "tTmrTimer_He_B", "tTmrTimer_He_C",
        "bTmrHealthy_He_A", "bTmrHealthy_He_B", "bTmrHealthy_He_C",
        0x01000000, 0x02000000, 0x04000000, "dwSensorTmrFaultWord"
    ))

    return "\n".join(lines)

print("parts_phase1.py defined.")
