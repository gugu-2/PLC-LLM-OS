# Python generator to build Phase 6: ISA-18.2 Alarms & 32-Bit Telemetry

def build_phase6():
    st = []
    st.append("(* ==================================================================================================== *)\n")
    st.append("(* PHASE 6: ISA-18.2 MULTI-TIER PROCESS ALARM MATRIX & 32-BIT TELEMETRY WORDS                          *)\n")
    st.append("(* Deadband Clearance Hysteresis, First-Out Root Cause Diagnostic Latching & Bit Packing                 *)\n")
    st.append("(* ==================================================================================================== *)\n\n")

    st.append("(* ---------------------------------------------------------------------------------------------------- *)\n")
    st.append("(* Sub-Phase 6.1: ISA-18.2 Multi-Tier Process Alarm Evaluations with Hysteresis Deadband                 *)\n")
    st.append("(* ---------------------------------------------------------------------------------------------------- *)\n")

    # Alarm groups definitions
    alarms = [
        {
            "name": "Total Head Hydraulic Pressure",
            "val": "rHeadPress_Voted_kPa",
            "unit": "kPa",
            "prefix": "Head",
            "has_hh": True, "has_h": True, "has_l": True, "has_ll": True
        },
        {
            "name": "Stock Pond Liquid Level",
            "val": "rPondLevel_Voted_mm",
            "unit": "mm",
            "prefix": "Pond",
            "has_hh": True, "has_h": True, "has_l": True, "has_ll": True
        },
        {
            "name": "Air Cushion Compressed Pressure",
            "val": "rHeadPress_Voted_kPa",
            "unit": "kPa",
            "prefix": "AirPad",
            "has_hh": True, "has_h": True, "has_l": True, "has_ll": True
        },
        {
            "name": "Jet-to-Wire Velocity Ratio",
            "val": "rCalc_JetToWireRatio",
            "unit": "",
            "prefix": "JetWire",
            "has_hh": True, "has_h": True, "has_l": True, "has_ll": True
        },
        {
            "name": "Cross-Machine Mean Basis Weight",
            "val": "rCalc_MeanBasisWeight_gpm2",
            "unit": "gpm2",
            "prefix": "Weight",
            "has_hh": True, "has_h": True, "has_l": True, "has_ll": True
        }
    ]

    for alm in alarms:
        p = alm["prefix"]
        v = alm["val"]
        u = f"_{alm['unit']}" if alm["unit"] else ""
        db = f"r{p}_Deadband{u}"
        st.append(f"(* Alarms for {alm['name']} *)\n")
        # HH
        st.append(f"IF {v} >= r{p}_HH_Limit{u} THEN\n")
        st.append(f"    b{p}_HH_Active := TRUE;\n")
        st.append(f"ELSIF {v} < (r{p}_HH_Limit{u} - {db}) THEN\n")
        st.append(f"    IF bAlarmAck OR bFaultReset THEN\n")
        st.append(f"        b{p}_HH_Active := FALSE;\n")
        st.append(f"    END_IF;\n")
        st.append(f"END_IF;\n\n")

        # H
        st.append(f"IF {v} >= r{p}_H_Limit{u} THEN\n")
        st.append(f"    b{p}_H_Active := TRUE;\n")
        st.append(f"ELSIF {v} < (r{p}_H_Limit{u} - {db}) THEN\n")
        st.append(f"    IF bAlarmAck OR bFaultReset THEN\n")
        st.append(f"        b{p}_H_Active := FALSE;\n")
        st.append(f"    END_IF;\n")
        st.append(f"END_IF;\n\n")

        # L
        st.append(f"IF {v} <= r{p}_L_Limit{u} THEN\n")
        st.append(f"    b{p}_L_Active := TRUE;\n")
        st.append(f"ELSIF {v} > (r{p}_L_Limit{u} + {db}) THEN\n")
        st.append(f"    IF bAlarmAck OR bFaultReset THEN\n")
        st.append(f"        b{p}_L_Active := FALSE;\n")
        st.append(f"    END_IF;\n")
        st.append(f"END_IF;\n\n")

        # LL
        st.append(f"IF {v} <= r{p}_LL_Limit{u} THEN\n")
        st.append(f"    b{p}_LL_Active := TRUE;\n")
        st.append(f"ELSIF {v} > (r{p}_LL_Limit{u} + {db}) THEN\n")
        st.append(f"    IF bAlarmAck OR bFaultReset THEN\n")
        st.append(f"        b{p}_LL_Active := FALSE;\n")
        st.append(f"    END_IF;\n")
        st.append(f"END_IF;\n\n")

    # Additional profile alarms
    st.append("(* Basis Weight CD Profile 2-Sigma Variation Alarms *)\n")
    st.append("IF rCalc_TwoSigma_Pct >= 5.5 THEN\n")
    st.append("    bSigma_HH_Active := TRUE;\n")
    st.append("ELSIF rCalc_TwoSigma_Pct < 4.5 THEN\n")
    st.append("    IF bAlarmAck OR bFaultReset THEN\n")
    st.append("        bSigma_HH_Active := FALSE;\n")
    st.append("    END_IF;\n")
    st.append("END_IF;\n\n")

    st.append("IF rCalc_TwoSigma_Pct >= 3.5 THEN\n")
    st.append("    bSigma_H_Active := TRUE;\n")
    st.append("ELSIF rCalc_TwoSigma_Pct < 2.8 THEN\n")
    st.append("    IF bAlarmAck OR bFaultReset THEN\n")
    st.append("        bSigma_H_Active := FALSE;\n")
    st.append("    END_IF;\n")
    st.append("END_IF;\n\n")

    st.append("(* Slice Lip Curvature & Differential Mechanical Bending Alarms *)\n")
    st.append("IF rCalc_MaxSliceCurvature_um >= rMaxAllowedCurvature_um THEN\n")
    st.append("    bCurvature_HH_Active := TRUE;\n")
    st.append("ELSIF rCalc_MaxSliceCurvature_um < (rMaxAllowedCurvature_um - 3.0) THEN\n")
    st.append("    IF bAlarmAck OR bFaultReset THEN\n")
    st.append("        bCurvature_HH_Active := FALSE;\n")
    st.append("    END_IF;\n")
    st.append("END_IF;\n\n")

    st.append("IF rCalc_MaxAdjacentDelta_um >= rMaxAllowedAdjacentDelta_um THEN\n")
    st.append("    bAdjacentDelta_HH_Active := TRUE;\n")
    st.append("ELSIF rCalc_MaxAdjacentDelta_um < (rMaxAllowedAdjacentDelta_um - 4.0) THEN\n")
    st.append("    IF bAlarmAck OR bFaultReset THEN\n")
    st.append("        bAdjacentDelta_HH_Active := FALSE;\n")
    st.append("    END_IF;\n")
    st.append("END_IF;\n\n")

    st.append("(* ---------------------------------------------------------------------------------------------------- *)\n")
    st.append("(* Sub-Phase 6.2: First-Out Root Cause Diagnostic Latching                                              *)\n")
    st.append("(* ---------------------------------------------------------------------------------------------------- *)\n")
    st.append("IF NOT bFirstOutLatched THEN\n")
    st.append("    IF bEmergencyStop THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#00010001;\n")
    st.append("    ELSIF bHead_HH_Active THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#00010002;\n")
    st.append("    ELSIF bHead_LL_Active THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#00010003;\n")
    st.append("    ELSIF bPond_HH_Active THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#00010004;\n")
    st.append("    ELSIF bPond_LL_Active THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#00010005;\n")
    st.append("    ELSIF bAirPad_HH_Active THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#00010006;\n")
    st.append("    ELSIF bAirPad_LL_Active THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#00010007;\n")
    st.append("    ELSIF bJetWire_HH_Active THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#00010008;\n")
    st.append("    ELSIF bJetWire_LL_Active THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#00010009;\n")
    st.append("    ELSIF bHeadPress_Trip THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#0001000A;\n")
    st.append("    ELSIF bPondLevel_Trip THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#0001000B;\n")
    st.append("    ELSIF bSheetBreakDetected THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#0001000C;\n")
    st.append("    ELSIF bCurvature_HH_Active THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#0001000D;\n")
    st.append("    ELSIF bAdjacentDelta_HH_Active THEN\n")
    st.append("        bFirstOutLatched := TRUE;\n")
    st.append("        dwFirstOutCapturedCode := 16#0001000E;\n")
    st.append("    END_IF;\n")
    st.append("ELSE\n")
    st.append("    IF bFaultReset AND NOT bEmergencyStop AND NOT bHead_HH_Active AND NOT bHead_LL_Active AND NOT bPond_HH_Active AND NOT bPond_LL_Active AND NOT bHeadPress_Trip AND NOT bPondLevel_Trip THEN\n")
    st.append("        bFirstOutLatched := FALSE;\n")
    st.append("        dwFirstOutCapturedCode := 16#00000000;\n")
    st.append("    END_IF;\n")
    st.append("END_IF;\n")
    st.append("dwFirstOutWord := dwFirstOutCapturedCode;\n\n")

    st.append("(* ---------------------------------------------------------------------------------------------------- *)\n")
    st.append("(* Sub-Phase 6.3: 32-Bit Bit-Packed Telemetry & Diagnostic Status Words                                 *)\n")
    st.append("(* ---------------------------------------------------------------------------------------------------- *)\n")
    st.append("(* Status Word 1: Operational States, Permissives & Actuator Subsystems *)\n")
    st.append("dwStatusWord1 := INT_TO_DWORD(eState) AND 16#0000000F;\n")
    st.append("IF bEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;\n")
    st.append("IF bFanPumpReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;\n")
    st.append("IF bAirCompressorReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;\n")
    st.append("IF bWireDriveRunning THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;\n")
    st.append("IF bWhiteWaterFlushPermissive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;\n")
    st.append("IF bMpcEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;\n")
    st.append("IF bCdControlEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;\n")
    st.append("IF bScannerDataValid THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;\n")
    st.append("IF bGradeChangeCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF;\n")
    st.append("IF bSheetBreakDetected THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF;\n")
    st.append("IF bCleanInPlaceCmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;\n")
    st.append("IF bFirstScanDone THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;\n")
    st.append("IF rFanPump_SpeedCmd_pct > 0.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF;\n")
    st.append("IF rAirChargeValve_Cmd_pct > 0.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF;\n")
    st.append("IF rAirBleedValve_Cmd_pct > 0.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00040000; END_IF;\n")
    st.append("IF bEmergencySlurryDivertValve THEN dwStatusWord1 := dwStatusWord1 OR 16#00080000; END_IF;\n")
    st.append("IF bSliceLipProtectiveRetract THEN dwStatusWord1 := dwStatusWord1 OR 16#00100000; END_IF;\n")
    st.append("IF bFanPumpFastTrip THEN dwStatusWord1 := dwStatusWord1 OR 16#00200000; END_IF;\n")
    st.append("IF bAirPadFastDepressurize THEN dwStatusWord1 := dwStatusWord1 OR 16#00400000; END_IF;\n")
    st.append("IF bWhiteWaterBypassValve THEN dwStatusWord1 := dwStatusWord1 OR 16#00800000; END_IF;\n\n")

    st.append("(* Status Word 2: 2oo3 TMR Voting Health & System Convergence *)\n")
    st.append("dwStatusWord2 := 16#00000000;\n")
    st.append("IF bHeadPress_HealthA THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF;\n")
    st.append("IF bHeadPress_HealthB THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF;\n")
    st.append("IF bHeadPress_HealthC THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF;\n")
    st.append("IF bHeadPress_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF;\n")
    st.append("IF bPondLevel_HealthA THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF;\n")
    st.append("IF bPondLevel_HealthB THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF;\n")
    st.append("IF bPondLevel_HealthC THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF;\n")
    st.append("IF bPondLevel_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF;\n")
    st.append("IF bDilutionFlow_HealthA THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;\n")
    st.append("IF bDilutionFlow_HealthB THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;\n")
    st.append("IF bDilutionFlow_HealthC THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;\n")
    st.append("IF bDilutionFlow_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;\n")
    st.append("IF bWireSpeed_HealthA THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;\n")
    st.append("IF bWireSpeed_HealthB THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;\n")
    st.append("IF bWireSpeed_HealthC THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;\n")
    st.append("IF bWireSpeed_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF;\n")
    st.append("IF bHeadPress_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00010000; END_IF;\n")
    st.append("IF bPondLevel_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF;\n")
    st.append("IF bDilutionFlow_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF;\n")
    st.append("IF bWireSpeed_SingleFallback THEN dwStatusWord2 := dwStatusWord2 OR 16#00080000; END_IF;\n")
    st.append("IF bHeadPress_Trip THEN dwStatusWord2 := dwStatusWord2 OR 16#00100000; END_IF;\n")
    st.append("IF bPondLevel_Trip THEN dwStatusWord2 := dwStatusWord2 OR 16#00200000; END_IF;\n")
    st.append("IF bDilutionFlow_Trip THEN dwStatusWord2 := dwStatusWord2 OR 16#00400000; END_IF;\n")
    st.append("IF bWireSpeed_Trip THEN dwStatusWord2 := dwStatusWord2 OR 16#00800000; END_IF;\n\n")

    st.append("(* Alarm Word 1: Critical Process Trips & Safety Interlocks (HH/LL) *)\n")
    st.append("dwAlarmWord1 := 16#00000000;\n")
    st.append("IF bHead_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;\n")
    st.append("IF bHead_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;\n")
    st.append("IF bPond_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;\n")
    st.append("IF bPond_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;\n")
    st.append("IF bAirPad_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;\n")
    st.append("IF bAirPad_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;\n")
    st.append("IF bJetWire_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;\n")
    st.append("IF bJetWire_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;\n")
    st.append("IF bWeight_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;\n")
    st.append("IF bWeight_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;\n")
    st.append("IF bSigma_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF;\n")
    st.append("IF bCurvature_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;\n")
    st.append("IF bAdjacentDelta_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF;\n")
    st.append("IF bSheetBreakDetected THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF;\n")
    st.append("IF bEmergencyStop THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; END_IF;\n")
    st.append("IF bFanPumpFastTrip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00008000; END_IF;\n")
    st.append("IF bAirPadFastDepressurize THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00010000; END_IF;\n")
    st.append("IF bHeadPress_Trip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00020000; END_IF;\n")
    st.append("IF bPondLevel_Trip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00040000; END_IF;\n")
    st.append("IF bDilutionFlow_Trip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00080000; END_IF;\n")
    st.append("IF bWireSpeed_Trip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00100000; END_IF;\n\n")

    st.append("(* Alarm Word 2: Warning Process Deviations & Channel Discrepancies (H/L) *)\n")
    st.append("dwAlarmWord2 := 16#00000000;\n")
    st.append("IF bHead_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;\n")
    st.append("IF bHead_L_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;\n")
    st.append("IF bPond_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;\n")
    st.append("IF bPond_L_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;\n")
    st.append("IF bAirPad_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;\n")
    st.append("IF bAirPad_L_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;\n")
    st.append("IF bJetWire_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;\n")
    st.append("IF bJetWire_L_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;\n")
    st.append("IF bWeight_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;\n")
    st.append("IF bWeight_L_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;\n")
    st.append("IF bSigma_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF;\n")
    st.append("IF rHeadPress_Disc_AB_ms > 0.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF;\n")
    st.append("IF rHeadPress_Disc_BC_ms > 0.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF;\n")
    st.append("IF rHeadPress_Disc_CA_ms > 0.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF;\n")
    st.append("IF rPondLevel_Disc_AB_ms > 0.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF;\n")
    st.append("IF rPondLevel_Disc_BC_ms > 0.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00008000; END_IF;\n")
    st.append("IF rPondLevel_Disc_CA_ms > 0.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00010000; END_IF;\n")
    st.append("IF rDilutionFlow_Disc_AB_ms > 0.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00020000; END_IF;\n")
    st.append("IF rDilutionFlow_Disc_BC_ms > 0.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00040000; END_IF;\n")
    st.append("IF rDilutionFlow_Disc_CA_ms > 0.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00080000; END_IF;\n")
    st.append("IF rWireSpeed_Disc_AB_ms > 0.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00100000; END_IF;\n")
    st.append("IF rWireSpeed_Disc_BC_ms > 0.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00200000; END_IF;\n")
    st.append("IF rWireSpeed_Disc_CA_ms > 0.0 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00400000; END_IF;\n\n")

    st.append("(* Continuous Execution Loop Monotonic Counter Increment *)\n")
    st.append("iCycleCounter := iCycleCounter + 1;\n\n")

    st.append("END_FUNCTION_BLOCK\n")

    return "".join(st)

print("build_phase6 len:", len(build_phase6()))
