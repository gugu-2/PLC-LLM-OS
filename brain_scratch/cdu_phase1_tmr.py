# -*- coding: utf-8 -*-
"""
Phase 1: 2oo3 Triple Modular Redundancy (TMR) Sensor Voting for 16 Critical CDU Triplets
"""

triplets = [
    {
        "id": "01", "name": "PT_101",
        "tagA": "PT_CDU_FEED_101A", "tagB": "PT_CDU_FEED_101B", "tagC": "PT_CDU_FEED_101C",
        "voted": "rVoted_PT_101",
        "desc": "Crude Feed Booster Pump Discharge Pressure [bar_g]",
        "tol": "1.50", "min": "0.0", "max": "60.0",
        "word": "1", "mask": "16#00000001", "fail_mask": "16#00010000"
    },
    {
        "id": "02", "name": "TT_102",
        "tagA": "TT_CDU_FURNACE_COT_102A", "tagB": "TT_CDU_FURNACE_COT_102B", "tagC": "TT_CDU_FURNACE_COT_102C",
        "voted": "rVoted_TT_102",
        "desc": "Fired Heater Combined Coil Outlet Temperature (COT) [deg C]",
        "tol": "2.50", "min": "100.0", "max": "450.0",
        "word": "1", "mask": "16#00000002", "fail_mask": "16#00020000"
    },
    {
        "id": "03", "name": "FT_103",
        "tagA": "FT_CRUDE_CHARGE_103A", "tagB": "FT_CRUDE_CHARGE_103B", "tagC": "FT_CRUDE_CHARGE_103C",
        "voted": "rVoted_FT_103",
        "desc": "Total Raw Crude Charge Flow Rate to Atmospheric Pipestill [m3/h]",
        "tol": "50.0", "min": "0.0", "max": "3500.0",
        "word": "1", "mask": "16#00000004", "fail_mask": "16#00040000"
    },
    {
        "id": "04", "name": "AT_201",
        "tagA": "AT_FLUE_GAS_O2_201A", "tagB": "AT_FLUE_GAS_O2_201B", "tagC": "AT_FLUE_GAS_O2_201C",
        "voted": "rVoted_AT_201",
        "desc": "Fired Heater Radiant Arch Flue Gas Excess Oxygen [vol%]",
        "tol": "0.35", "min": "0.0", "max": "21.0",
        "word": "1", "mask": "16#00000008", "fail_mask": "16#00080000"
    },
    {
        "id": "05", "name": "AT_202",
        "tagA": "AT_FLUE_GAS_CO_202A", "tagB": "AT_FLUE_GAS_CO_202B", "tagC": "AT_FLUE_GAS_CO_202C",
        "voted": "rVoted_AT_202",
        "desc": "Fired Heater Radiant Box Flue Gas Carbon Monoxide [ppm]",
        "tol": "25.0", "min": "0.0", "max": "2000.0",
        "word": "1", "mask": "16#00000010", "fail_mask": "16#00100000"
    },
    {
        "id": "06", "name": "PT_203",
        "tagA": "PT_FURNACE_DRAFT_203A", "tagB": "PT_FURNACE_DRAFT_203B", "tagC": "PT_FURNACE_DRAFT_203C",
        "voted": "rVoted_PT_203",
        "desc": "Fired Heater Radiant Arch Furnace Draft Vacuum Pressure [mbar]",
        "tol": "0.35", "min": "-10.0", "max": "5.0",
        "word": "1", "mask": "16#00000020", "fail_mask": "16#00200000"
    },
    {
        "id": "07", "name": "FT_204",
        "tagA": "FT_FUEL_GAS_SUPPLY_204A", "tagB": "FT_FUEL_GAS_SUPPLY_204B", "tagC": "FT_FUEL_GAS_SUPPLY_204C",
        "voted": "rVoted_FT_204",
        "desc": "Fired Heater Fuel Gas Main Supply Mass Flow Rate [kg/h]",
        "tol": "150.0", "min": "0.0", "max": "20000.0",
        "word": "1", "mask": "16#00000040", "fail_mask": "16#00400000"
    },
    {
        "id": "08", "name": "PT_301",
        "tagA": "PT_COLUMN_OVERHEAD_301A", "tagB": "PT_COLUMN_OVERHEAD_301B", "tagC": "PT_COLUMN_OVERHEAD_301C",
        "voted": "rVoted_PT_301",
        "desc": "Main Atmospheric Column Overhead Vapor Pressure [bar_g]",
        "tol": "0.15", "min": "0.0", "max": "6.0",
        "word": "1", "mask": "16#00000080", "fail_mask": "16#00800000"
    },
    {
        "id": "09", "name": "TT_302",
        "tagA": "TT_COLUMN_OVERHEAD_302A", "tagB": "TT_COLUMN_OVERHEAD_302B", "tagC": "TT_COLUMN_OVERHEAD_302C",
        "voted": "rVoted_TT_302",
        "desc": "Main Atmospheric Column Overhead Vapor Temperature [deg C]",
        "tol": "2.00", "min": "50.0", "max": "220.0",
        "word": "2", "mask": "16#00000001", "fail_mask": "16#00010000"
    },
    {
        "id": "10", "name": "LT_303",
        "tagA": "LT_REFLUX_DRUM_303A", "tagB": "LT_REFLUX_DRUM_303B", "tagC": "LT_REFLUX_DRUM_303C",
        "voted": "rVoted_LT_303",
        "desc": "Overhead Condensate Reflux Drum Liquid Level [%]",
        "tol": "3.50", "min": "0.0", "max": "100.0",
        "word": "2", "mask": "16#00000002", "fail_mask": "16#00020000"
    },
    {
        "id": "11", "name": "FT_304",
        "tagA": "FT_OVERHEAD_REFLUX_304A", "tagB": "FT_OVERHEAD_REFLUX_304B", "tagC": "FT_OVERHEAD_REFLUX_304C",
        "voted": "rVoted_FT_304",
        "desc": "Column Top External Liquid Reflux Return Flow [m3/h]",
        "tol": "20.0", "min": "0.0", "max": "1200.0",
        "word": "2", "mask": "16#00000004", "fail_mask": "16#00040000"
    },
    {
        "id": "12", "name": "TT_401",
        "tagA": "TT_DIESEL_STRIPPER_TRAY_401A", "tagB": "TT_DIESEL_STRIPPER_TRAY_401B", "tagC": "TT_DIESEL_STRIPPER_TRAY_401C",
        "voted": "rVoted_TT_401",
        "desc": "Diesel Side-Stream Draw Tray Liquid Temperature [deg C]",
        "tol": "2.50", "min": "150.0", "max": "350.0",
        "word": "2", "mask": "16#00000008", "fail_mask": "16#00080000"
    },
    {
        "id": "13", "name": "FT_501",
        "tagA": "FT_PUMPAROUND_PA1_501A", "tagB": "FT_PUMPAROUND_PA1_501B", "tagC": "FT_PUMPAROUND_PA1_501C",
        "voted": "rVoted_FT_501",
        "desc": "Pumparound PA-1 (Top/Kero) Circulation Liquid Flow [m3/h]",
        "tol": "30.0", "min": "0.0", "max": "1800.0",
        "word": "2", "mask": "16#00000010", "fail_mask": "16#00100000"
    },
    {
        "id": "14", "name": "TT_502",
        "tagA": "TT_PUMPAROUND_PA1_RET_502A", "tagB": "TT_PUMPAROUND_PA1_RET_502B", "tagC": "TT_PUMPAROUND_PA1_RET_502C",
        "voted": "rVoted_TT_502",
        "desc": "Pumparound PA-1 Cooled Return Temperature [deg C]",
        "tol": "2.50", "min": "80.0", "max": "260.0",
        "word": "2", "mask": "16#00000020", "fail_mask": "16#00200000"
    },
    {
        "id": "15", "name": "LT_601",
        "tagA": "LT_COLUMN_BOTTOMS_601A", "tagB": "LT_COLUMN_BOTTOMS_601B", "tagC": "LT_COLUMN_BOTTOMS_601C",
        "voted": "rVoted_LT_601",
        "desc": "Atmospheric Column Bottom Residue Sump Level [%]",
        "tol": "3.50", "min": "0.0", "max": "100.0",
        "word": "2", "mask": "16#00000040", "fail_mask": "16#00400000"
    },
    {
        "id": "16", "name": "FT_602",
        "tagA": "FT_RESID_BOTTOMS_602A", "tagB": "FT_RESID_BOTTOMS_602B", "tagC": "FT_RESID_BOTTOMS_602C",
        "voted": "rVoted_FT_602",
        "desc": "Atmospheric Residue Product Rundown Flow Rate [m3/h]",
        "tol": "30.0", "min": "0.0", "max": "1800.0",
        "word": "2", "mask": "16#00000080", "fail_mask": "16#00800000"
    }
]

def generate_phase1():
    lines = []
    lines.append("(* =================================================================================================== *)")
    lines.append("(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH PAIRWISE DEBOUNCE === *)")
    lines.append("(* =================================================================================================== *)")
    
    for t in triplets:
        idx = t["id"]
        tagA = t["tagA"]
        tagB = t["tagB"]
        tagC = t["tagC"]
        voted = t["voted"]
        desc = t["desc"]
        tol = t["tol"]
        min_val = t["min"]
        max_val = t["max"]
        w = t["word"]
        mask = t["mask"]
        fmask = t["fail_mask"]
        
        lines.append(f"(* --- Triplet {idx}: {desc} --- *)")
        lines.append(f"bHealthy_{tagA} := ({tagA} >= {min_val}) AND ({tagA} <= {max_val});")
        lines.append(f"bHealthy_{tagB} := ({tagB} >= {min_val}) AND ({tagB} <= {max_val});")
        lines.append(f"bHealthy_{tagC} := ({tagC} >= {min_val}) AND ({tagC} <= {max_val});")
        lines.append(f"rDelta_AB := ABS({tagA} - {tagB});")
        lines.append(f"rDelta_BC := ABS({tagB} - {tagC});")
        lines.append(f"rDelta_CA := ABS({tagC} - {tagA});")
        lines.append(f"IF (rDelta_AB > {tol}) OR (rDelta_BC > {tol}) OR (rDelta_CA > {tol}) THEN")
        lines.append(f"    rTimer_Disc_{idx} := rTimer_Disc_{idx} + rCycleTime_dt;")
        lines.append(f"    IF rTimer_Disc_{idx} >= 0.50 THEN")
        lines.append(f"        dwTMR_Diagnostic_Word{w} := dwTMR_Diagnostic_Word{w} OR {mask};")
        lines.append(f"    END_IF;")
        lines.append(f"ELSE")
        lines.append(f"    rTimer_Disc_{idx} := MAX(0.0, rTimer_Disc_{idx} - (rCycleTime_dt * 2.0));")
        lines.append(f"    IF rTimer_Disc_{idx} <= 0.05 THEN")
        lines.append(f"        dwTMR_Diagnostic_Word{w} := dwTMR_Diagnostic_Word{w} AND NOT {mask};")
        lines.append(f"    END_IF;")
        lines.append(f"END_IF;")
        lines.append(f"iHealthyCount := BOOL_TO_INT(bHealthy_{tagA}) + BOOL_TO_INT(bHealthy_{tagB}) + BOOL_TO_INT(bHealthy_{tagC});")
        lines.append(f"CASE iHealthyCount OF")
        lines.append(f"    3: (* Normal 3-Healthy Median Selection *)")
        lines.append(f"        IF ({tagA} >= {tagB} AND {tagA} <= {tagC}) OR ({tagA} >= {tagC} AND {tagA} <= {tagB}) THEN")
        lines.append(f"            {voted} := {tagA};")
        lines.append(f"        ELSIF ({tagB} >= {tagA} AND {tagB} <= {tagC}) OR ({tagB} >= {tagC} AND {tagB} <= {tagA}) THEN")
        lines.append(f"            {voted} := {tagB};")
        lines.append(f"        ELSE")
        lines.append(f"            {voted} := {tagC};")
        lines.append(f"        END_IF;")
        lines.append(f"        dwTMR_Diagnostic_Word{w} := dwTMR_Diagnostic_Word{w} AND NOT {fmask};")
        lines.append(f"    2: (* Degraded 2-Healthy: Arithmetic Mean of Surviving Pair *)")
        lines.append(f"        IF bHealthy_{tagA} AND bHealthy_{tagB} THEN")
        lines.append(f"            {voted} := 0.5 * ({tagA} + {tagB});")
        lines.append(f"        ELSIF bHealthy_{tagB} AND bHealthy_{tagC} THEN")
        lines.append(f"            {voted} := 0.5 * ({tagB} + {tagC});")
        lines.append(f"        ELSE")
        lines.append(f"            {voted} := 0.5 * ({tagA} + {tagC});")
        lines.append(f"        END_IF;")
        lines.append(f"        dwTMR_Diagnostic_Word{w} := dwTMR_Diagnostic_Word{w} AND NOT {fmask};")
        lines.append(f"    1: (* Degraded 1-Healthy: Single Fallback Surviving Channel *)")
        lines.append(f"        IF bHealthy_{tagA} THEN")
        lines.append(f"            {voted} := {tagA};")
        lines.append(f"        ELSIF bHealthy_{tagB} THEN")
        lines.append(f"            {voted} := {tagB};")
        lines.append(f"        ELSE")
        lines.append(f"            {voted} := {tagC};")
        lines.append(f"        END_IF;")
        lines.append(f"        dwTMR_Diagnostic_Word{w} := dwTMR_Diagnostic_Word{w} AND NOT {fmask};")
        lines.append(f"    0: (* Critical 0-Healthy: All Channels Discrepant or Out of Range *)")
        lines.append(f"        dwTMR_Diagnostic_Word{w} := dwTMR_Diagnostic_Word{w} OR {fmask};")
        lines.append(f"        (* Retain last good {voted} to prevent numerical discontinuity *)")
        lines.append(f"END_CASE;\n")
        
    return "\n".join(lines)

if __name__ == "__main__":
    code = generate_phase1()
    print(f"Phase 1 generated length: {len(code)} characters")
