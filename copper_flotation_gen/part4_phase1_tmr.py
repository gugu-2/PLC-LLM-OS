# copper_flotation_gen/part4_phase1_tmr.py

def get_phase1_tmr():
    lines = []
    lines.append("(* ==================================================================================================== *)")
    lines.append("(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE WITH DISCREPANCY TIMERS           *)")
    lines.append("(* Fail-Operational / Bumpless Degradation Architecture Across Critical Mineral Slurry Sensors          *)")
    lines.append("(* ==================================================================================================== *)")
    lines.append("")
    
    channels = [
        {
            "name": "Rougher Cell 1 Slurry Pulp Level (LT_PULP_101)",
            "pfx": "rPulpLevel_Cell1",
            "inA": "rPulpLevel_Cell1_1A_mm",
            "inB": "rPulpLevel_Cell1_1B_mm",
            "inC": "rPulpLevel_Cell1_1C_mm",
            "tol": "45.0", # mm
            "unit": "mm"
        },
        {
            "name": "Cleaner Cell 6 Slurry Pulp Level (LT_PULP_106)",
            "pfx": "rPulpLevel_Cell6",
            "inA": "rPulpLevel_Cell6_1A_mm",
            "inB": "rPulpLevel_Cell6_1B_mm",
            "inC": "rPulpLevel_Cell6_1C_mm",
            "tol": "45.0", # mm
            "unit": "mm"
        },
        {
            "name": "Scavenger Cell 12 Slurry Pulp Level (LT_PULP_112)",
            "pfx": "rPulpLevel_Cell12",
            "inA": "rPulpLevel_Cell12_1A_mm",
            "inB": "rPulpLevel_Cell12_1B_mm",
            "inC": "rPulpLevel_Cell12_1C_mm",
            "tol": "45.0", # mm
            "unit": "mm"
        },
        {
            "name": "Froth Bed Overflow Lip Thickness (LT_FROTH_201)",
            "pfx": "rFrothHeight",
            "inA": "rFrothHeight_2A_mm",
            "inB": "rFrothHeight_2B_mm",
            "inC": "rFrothHeight_2C_mm",
            "tol": "20.0", # mm
            "unit": "mm"
        },
        {
            "name": "Aeration Manifold Differential Air Pressure (PDT_AIR_301)",
            "pfx": "rAirPress",
            "inA": "rAirPress_Manifold_3A_kPa",
            "inB": "rAirPress_Manifold_3B_kPa",
            "inC": "rAirPress_Manifold_3C_kPa",
            "tol": "3.5", # kPa
            "unit": "kPa"
        },
        {
            "name": "In-Stream XRF Concentrate Copper Grade (AT_CU_401)",
            "pfx": "rXRF_ConcCu",
            "inA": "rXRF_ConcCu_4A_pct",
            "inB": "rXRF_ConcCu_4B_pct",
            "inC": "rXRF_ConcCu_4C_pct",
            "tol": "1.25", # % Cu
            "unit": "% Cu"
        },
        {
            "name": "Tailings Slurry Nuclear Specific Gravity Gauge (DT_TAIL_501)",
            "pfx": "rTailings_Density",
            "inA": "rTailings_Density_5A_gcc",
            "inB": "rTailings_Density_5B_gcc",
            "inC": "rTailings_Density_5C_gcc",
            "tol": "0.075", # g/cm3
            "unit": "g/cm3"
        }
    ]

    for ch in channels:
        pfx = ch["pfx"]
        name = ch["name"]
        inA = ch["inA"]
        inB = ch["inB"]
        inC = ch["inC"]
        tol = ch["tol"]
        unit = ch["unit"]

        lines.append(f"    (* -------------------------------------------------------------------------------------------- *)")
        lines.append(f"    (* 2oo3 TMR Channel: {name} [{unit}] *)")
        lines.append(f"    (* -------------------------------------------------------------------------------------------- *)")
        lines.append(f"    (* Step 1: Discrepancy Accumulation Timers with 400.0 [ms] Persistence Trip Threshold *)")
        lines.append(f"    IF ABS({inA} - {inB}) > {tol} THEN")
        lines.append(f"        {pfx}_Disc_AB_ms := {pfx}_Disc_AB_ms + (tScanCycleTime_s * 1000.0);")
        lines.append(f"    ELSE")
        lines.append(f"        {pfx}_Disc_AB_ms := MAX(0.0, {pfx}_Disc_AB_ms - (tScanCycleTime_s * 500.0));")
        lines.append(f"    END_IF;")
        lines.append("")
        lines.append(f"    IF ABS({inB} - {inC}) > {tol} THEN")
        lines.append(f"        {pfx}_Disc_BC_ms := {pfx}_Disc_BC_ms + (tScanCycleTime_s * 1000.0);")
        lines.append(f"    ELSE")
        lines.append(f"        {pfx}_Disc_BC_ms := MAX(0.0, {pfx}_Disc_BC_ms - (tScanCycleTime_s * 500.0));")
        lines.append(f"    END_IF;")
        lines.append("")
        lines.append(f"    IF ABS({inC} - {inA}) > {tol} THEN")
        lines.append(f"        {pfx}_Disc_CA_ms := {pfx}_Disc_CA_ms + (tScanCycleTime_s * 1000.0);")
        lines.append(f"    ELSE")
        lines.append(f"        {pfx}_Disc_CA_ms := MAX(0.0, {pfx}_Disc_CA_ms - (tScanCycleTime_s * 500.0));")
        lines.append(f"    END_IF;")
        lines.append("")
        lines.append(f"    (* Step 2: Channel Integrity Determination Based on Cross-Channel Timers *)")
        lines.append(f"    {pfx}_HealthA := ({pfx}_Disc_AB_ms < 400.0) OR ({pfx}_Disc_CA_ms < 400.0);")
        lines.append(f"    {pfx}_HealthB := ({pfx}_Disc_AB_ms < 400.0) OR ({pfx}_Disc_BC_ms < 400.0);")
        lines.append(f"    {pfx}_HealthC := ({pfx}_Disc_BC_ms < 400.0) OR ({pfx}_Disc_CA_ms < 400.0);")
        lines.append("")
        lines.append(f"    (* Step 3: Fault-Tolerant Voting: 3-Healthy Median, 2-Healthy Average, 1-Healthy Fallback *)")
        lines.append(f"    IF {pfx}_HealthA AND {pfx}_HealthB AND {pfx}_HealthC THEN")
        lines.append(f"        (* Full 3-Channel Triple Modular Redundant Median Voting *)")
        lines.append(f"        IF ({inA} >= {inB} AND {inA} <= {inC}) OR ({inA} >= {inC} AND {inA} <= {inB}) THEN")
        lines.append(f"            {pfx}_Voted := {inA};")
        lines.append(f"        ELSIF ({inB} >= {inA} AND {inB} <= {inC}) OR ({inB} >= {inC} AND {inB} <= {inA}) THEN")
        lines.append(f"            {pfx}_Voted := {inB};")
        lines.append(f"        ELSE")
        lines.append(f"            {pfx}_Voted := {inC};")
        lines.append(f"        END_IF;")
        lines.append(f"        {pfx}_Degraded := FALSE;")
        lines.append(f"        {pfx}_SingleFallback := FALSE;")
        lines.append(f"        {pfx}_Trip := FALSE;")
        lines.append(f"    ELSIF {pfx}_HealthA AND {pfx}_HealthB THEN")
        lines.append(f"        (* Channel C Failed: Bumpless Failover to 2oo2 Mean of Channels A and B *)")
        lines.append(f"        {pfx}_Voted := 0.5 * ({inA} + {inB});")
        lines.append(f"        {pfx}_Degraded := TRUE;")
        lines.append(f"        {pfx}_SingleFallback := FALSE;")
        lines.append(f"        {pfx}_Trip := FALSE;")
        lines.append(f"    ELSIF {pfx}_HealthB AND {pfx}_HealthC THEN")
        lines.append(f"        (* Channel A Failed: Bumpless Failover to 2oo2 Mean of Channels B and C *)")
        lines.append(f"        {pfx}_Voted := 0.5 * ({inB} + {inC});")
        lines.append(f"        {pfx}_Degraded := TRUE;")
        lines.append(f"        {pfx}_SingleFallback := FALSE;")
        lines.append(f"        {pfx}_Trip := FALSE;")
        lines.append(f"    ELSIF {pfx}_HealthC AND {pfx}_HealthA THEN")
        lines.append(f"        (* Channel B Failed: Bumpless Failover to 2oo2 Mean of Channels C and A *)")
        lines.append(f"        {pfx}_Voted := 0.5 * ({inC} + {inA});")
        lines.append(f"        {pfx}_Degraded := TRUE;")
        lines.append(f"        {pfx}_SingleFallback := FALSE;")
        lines.append(f"        {pfx}_Trip := FALSE;")
        lines.append(f"    ELSIF {pfx}_HealthA THEN")
        lines.append(f"        (* Two Channels Failed: Degraded Operation on Channel A with Safety Advisory *)")
        lines.append(f"        {pfx}_Voted := {inA};")
        lines.append(f"        {pfx}_Degraded := TRUE;")
        lines.append(f"        {pfx}_SingleFallback := TRUE;")
        lines.append(f"        {pfx}_Trip := FALSE;")
        lines.append(f"    ELSIF {pfx}_HealthB THEN")
        lines.append(f"        (* Two Channels Failed: Degraded Operation on Channel B with Safety Advisory *)")
        lines.append(f"        {pfx}_Voted := {inB};")
        lines.append(f"        {pfx}_Degraded := TRUE;")
        lines.append(f"        {pfx}_SingleFallback := TRUE;")
        lines.append(f"        {pfx}_Trip := FALSE;")
        lines.append(f"    ELSIF {pfx}_HealthC THEN")
        lines.append(f"        (* Two Channels Failed: Degraded Operation on Channel C with Safety Advisory *)")
        lines.append(f"        {pfx}_Voted := {inC};")
        lines.append(f"        {pfx}_Degraded := TRUE;")
        lines.append(f"        {pfx}_SingleFallback := TRUE;")
        lines.append(f"        {pfx}_Trip := FALSE;")
        lines.append(f"    ELSE")
        lines.append(f"        (* Complete Sensory Failure: Freeze Last Valid Reading & Latch Fail-Safe Trip *)")
        lines.append(f"        {pfx}_Degraded := TRUE;")
        lines.append(f"        {pfx}_SingleFallback := TRUE;")
        lines.append(f"        {pfx}_Trip := TRUE;")
        lines.append(f"    END_IF;")
        lines.append("")

    return "\n".join(lines)
