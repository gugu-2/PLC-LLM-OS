# Python generator to build Phase 1: 2oo3 TMR Voting

def build_phase1():
    st = []
    st.append("(* ==================================================================================================== *)\n")
    st.append("(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE                                   *)\n")
    st.append("(* 4 Independent Sensor Triplets, 150 [ms] Discrepancy Timers & Bumpless Degradation                   *)\n")
    st.append("(* ==================================================================================================== *)\n\n")

    channels = [
        {
            "num": "1",
            "name": "Total Head Hydraulic Pressure",
            "tag": "PT_HEAD_101",
            "unit": "kPa",
            "var_prefix": "HeadPress",
            "in_prefix": "rHeadPress_1",
            "min_val": "10.0",
            "max_val": "300.0",
            "tol": "3.5",
            "default_val": "158.5"
        },
        {
            "num": "2",
            "name": "Stock Pond Liquid Level",
            "tag": "LT_POND_201",
            "unit": "mm",
            "var_prefix": "PondLevel",
            "in_prefix": "rPondLevel_2",
            "min_val": "50.0",
            "max_val": "600.0",
            "tol": "6.0",
            "default_val": "320.0"
        },
        {
            "num": "3",
            "name": "Dilution Profiling Header Flow",
            "tag": "FT_DIL_301",
            "unit": "m3/h",
            "var_prefix": "DilutionFlow",
            "in_prefix": "rDilutionFlow_3",
            "min_val": "10.0",
            "max_val": "350.0",
            "tol": "4.5",
            "default_val": "145.0"
        },
        {
            "num": "4",
            "name": "Forming Wire Section Speed",
            "tag": "ST_WIRE_401",
            "unit": "m/min",
            "var_prefix": "WireSpeed",
            "in_prefix": "rWireSpeed_4",
            "min_val": "10.0",
            "max_val": "2200.0",
            "tol": "8.0",
            "default_val": "1800.0"
        }
    ]

    for ch in channels:
        vp = ch["var_prefix"]
        inp = ch["in_prefix"]
        unit = ch["unit"]
        st.append(f"(* ---------------------------------------------------------------------------------------------------- *)\n")
        st.append(f"(* Channel Group {ch['num']}: {ch['name']} ({ch['tag']}A/B/C) [{unit}] *)\n")
        st.append(f"(* ---------------------------------------------------------------------------------------------------- *)\n")
        
        # Range checks
        st.append(f"(* Range & Plausibility Validation checks for Channel {ch['num']} *)\n")
        st.append(f"IF ({inp}A_{unit} < {ch['min_val']}) OR ({inp}A_{unit} > {ch['max_val']}) THEN\n")
        st.append(f"    b{vp}_HealthA := FALSE;\n")
        st.append(f"ELSE\n")
        st.append(f"    IF bFaultReset AND NOT b{vp}_Trip THEN\n")
        st.append(f"        b{vp}_HealthA := TRUE;\n")
        st.append(f"    END_IF;\n")
        st.append(f"END_IF;\n\n")

        st.append(f"IF ({inp}B_{unit} < {ch['min_val']}) OR ({inp}B_{unit} > {ch['max_val']}) THEN\n")
        st.append(f"    b{vp}_HealthB := FALSE;\n")
        st.append(f"ELSE\n")
        st.append(f"    IF bFaultReset AND NOT b{vp}_Trip THEN\n")
        st.append(f"        b{vp}_HealthB := TRUE;\n")
        st.append(f"    END_IF;\n")
        st.append(f"END_IF;\n\n")

        st.append(f"IF ({inp}C_{unit} < {ch['min_val']}) OR ({inp}C_{unit} > {ch['max_val']}) THEN\n")
        st.append(f"    b{vp}_HealthC := FALSE;\n")
        st.append(f"ELSE\n")
        st.append(f"    IF bFaultReset AND NOT b{vp}_Trip THEN\n")
        st.append(f"        b{vp}_HealthC := TRUE;\n")
        st.append(f"    END_IF;\n")
        st.append(f"END_IF;\n\n")

        # Discrepancy checks & timers
        st.append(f"(* Pairwise Deviation Timers with 150 [ms] Persistence Filter *)\n")
        st.append(f"IF b{vp}_HealthA AND b{vp}_HealthB THEN\n")
        st.append(f"    IF ABS({inp}A_{unit} - {inp}B_{unit}) > {ch['tol']} THEN\n")
        st.append(f"        r{vp}_Disc_AB_ms := r{vp}_Disc_AB_ms + (tScanCycleTime_s * 1000.0);\n")
        st.append(f"    ELSE\n")
        st.append(f"        r{vp}_Disc_AB_ms := MAX(0.0, r{vp}_Disc_AB_ms - (tScanCycleTime_s * 1000.0 * 2.0));\n")
        st.append(f"    END_IF;\n")
        st.append(f"ELSE\n")
        st.append(f"    r{vp}_Disc_AB_ms := 0.0;\n")
        st.append(f"END_IF;\n\n")

        st.append(f"IF b{vp}_HealthB AND b{vp}_HealthC THEN\n")
        st.append(f"    IF ABS({inp}B_{unit} - {inp}C_{unit}) > {ch['tol']} THEN\n")
        st.append(f"        r{vp}_Disc_BC_ms := r{vp}_Disc_BC_ms + (tScanCycleTime_s * 1000.0);\n")
        st.append(f"    ELSE\n")
        st.append(f"        r{vp}_Disc_BC_ms := MAX(0.0, r{vp}_Disc_BC_ms - (tScanCycleTime_s * 1000.0 * 2.0));\n")
        st.append(f"    END_IF;\n")
        st.append(f"ELSE\n")
        st.append(f"    r{vp}_Disc_BC_ms := 0.0;\n")
        st.append(f"END_IF;\n\n")

        st.append(f"IF b{vp}_HealthC AND b{vp}_HealthA THEN\n")
        st.append(f"    IF ABS({inp}C_{unit} - {inp}A_{unit}) > {ch['tol']} THEN\n")
        st.append(f"        r{vp}_Disc_CA_ms := r{vp}_Disc_CA_ms + (tScanCycleTime_s * 1000.0);\n")
        st.append(f"    ELSE\n")
        st.append(f"        r{vp}_Disc_CA_ms := MAX(0.0, r{vp}_Disc_CA_ms - (tScanCycleTime_s * 1000.0 * 2.0));\n")
        st.append(f"    END_IF;\n")
        st.append(f"ELSE\n")
        st.append(f"    r{vp}_Disc_CA_ms := 0.0;\n")
        st.append(f"END_IF;\n\n")

        # Isolation of Outlier Channel
        st.append(f"(* Outlier Channel Fault Isolation *)\n")
        st.append(f"IF (r{vp}_Disc_AB_ms >= 150.0) AND (r{vp}_Disc_CA_ms >= 150.0) THEN\n")
        st.append(f"    b{vp}_HealthA := FALSE;\n")
        st.append(f"ELSIF (r{vp}_Disc_AB_ms >= 150.0) AND (r{vp}_Disc_BC_ms >= 150.0) THEN\n")
        st.append(f"    b{vp}_HealthB := FALSE;\n")
        st.append(f"ELSIF (r{vp}_Disc_BC_ms >= 150.0) AND (r{vp}_Disc_CA_ms >= 150.0) THEN\n")
        st.append(f"    b{vp}_HealthC := FALSE;\n")
        st.append(f"END_IF;\n\n")

        # Voting execution: 2oo3 Median, 2oo2 Average, 1oo1 Single Fallback, or Trip
        st.append(f"(* 2oo3 TMR Voting Logic with Bumpless Degradation *)\n")
        st.append(f"IF b{vp}_HealthA AND b{vp}_HealthB AND b{vp}_HealthC THEN\n")
        st.append(f"    (* Nominal 2oo3 Triple Modular Redundancy - Median Select *)\n")
        st.append(f"    IF (({inp}A_{unit} >= {inp}B_{unit}) AND ({inp}A_{unit} <= {inp}C_{unit})) OR (({inp}A_{unit} >= {inp}C_{unit}) AND ({inp}A_{unit} <= {inp}B_{unit})) THEN\n")
        st.append(f"        r{vp}_Voted_{unit} := {inp}A_{unit};\n")
        st.append(f"    ELSIF (({inp}B_{unit} >= {inp}A_{unit}) AND ({inp}B_{unit} <= {inp}C_{unit})) OR (({inp}B_{unit} >= {inp}C_{unit}) AND ({inp}B_{unit} <= {inp}A_{unit})) THEN\n")
        st.append(f"        r{vp}_Voted_{unit} := {inp}B_{unit};\n")
        st.append(f"    ELSE\n")
        st.append(f"        r{vp}_Voted_{unit} := {inp}C_{unit};\n")
        st.append(f"    END_IF;\n")
        st.append(f"    b{vp}_Degraded := FALSE;\n")
        st.append(f"    b{vp}_SingleFallback := FALSE;\n")
        st.append(f"    b{vp}_Trip := FALSE;\n")
        st.append(f"ELSIF b{vp}_HealthA AND b{vp}_HealthB THEN\n")
        st.append(f"    (* Degraded 2oo2 Dual Sensor Voting - Mean Average *)\n")
        st.append(f"    r{vp}_Voted_{unit} := ({inp}A_{unit} + {inp}B_{unit}) * 0.5;\n")
        st.append(f"    b{vp}_Degraded := TRUE;\n")
        st.append(f"    b{vp}_SingleFallback := FALSE;\n")
        st.append(f"    b{vp}_Trip := FALSE;\n")
        st.append(f"ELSIF b{vp}_HealthB AND b{vp}_HealthC THEN\n")
        st.append(f"    (* Degraded 2oo2 Dual Sensor Voting - Mean Average *)\n")
        st.append(f"    r{vp}_Voted_{unit} := ({inp}B_{unit} + {inp}C_{unit}) * 0.5;\n")
        st.append(f"    b{vp}_Degraded := TRUE;\n")
        st.append(f"    b{vp}_SingleFallback := FALSE;\n")
        st.append(f"    b{vp}_Trip := FALSE;\n")
        st.append(f"ELSIF b{vp}_HealthC AND b{vp}_HealthA THEN\n")
        st.append(f"    (* Degraded 2oo2 Dual Sensor Voting - Mean Average *)\n")
        st.append(f"    r{vp}_Voted_{unit} := ({inp}C_{unit} + {inp}A_{unit}) * 0.5;\n")
        st.append(f"    b{vp}_Degraded := TRUE;\n")
        st.append(f"    b{vp}_SingleFallback := FALSE;\n")
        st.append(f"    b{vp}_Trip := FALSE;\n")
        st.append(f"ELSIF b{vp}_HealthA THEN\n")
        st.append(f"    (* Degraded 1oo1 Single Channel Fallback *)\n")
        st.append(f"    r{vp}_Voted_{unit} := {inp}A_{unit};\n")
        st.append(f"    b{vp}_Degraded := TRUE;\n")
        st.append(f"    b{vp}_SingleFallback := TRUE;\n")
        st.append(f"    b{vp}_Trip := FALSE;\n")
        st.append(f"ELSIF b{vp}_HealthB THEN\n")
        st.append(f"    (* Degraded 1oo1 Single Channel Fallback *)\n")
        st.append(f"    r{vp}_Voted_{unit} := {inp}B_{unit};\n")
        st.append(f"    b{vp}_Degraded := TRUE;\n")
        st.append(f"    b{vp}_SingleFallback := TRUE;\n")
        st.append(f"    b{vp}_Trip := FALSE;\n")
        st.append(f"ELSIF b{vp}_HealthC THEN\n")
        st.append(f"    (* Degraded 1oo1 Single Channel Fallback *)\n")
        st.append(f"    r{vp}_Voted_{unit} := {inp}C_{unit};\n")
        st.append(f"    b{vp}_Degraded := TRUE;\n")
        st.append(f"    b{vp}_SingleFallback := TRUE;\n")
        st.append(f"    b{vp}_Trip := FALSE;\n")
        st.append(f"ELSE\n")
        st.append(f"    (* Complete Sensor Suite Failure - Freeze Last Good & Assert Critical Trip *)\n")
        st.append(f"    b{vp}_Trip := TRUE;\n")
        st.append(f"    b{vp}_Degraded := TRUE;\n")
        st.append(f"    b{vp}_SingleFallback := TRUE;\n")
        st.append(f"END_IF;\n\n")

    return "".join(st)

print("build_phase1 len:", len(build_phase1()))
