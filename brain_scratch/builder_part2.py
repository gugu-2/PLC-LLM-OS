# -*- coding: utf-8 -*-
"""
Builder module for FB_Fertilizer_AmmoniumNitrate_Granulation_Scrubber
Part 2: Phase 1 - 2oo3 TMR Sensor Voting across all 16 field channels
"""

def get_tmr_channel_logic(channel_name, tag_prefix, val_a, val_b, val_c, tol_const, voted_output, timer_var, iso_a, iso_b, iso_c):
    return f"""(* -------------------------------------------------------------------------------------------------- *)
(* TMR CHANNEL: {channel_name} (TAG: {tag_prefix}) *)
(* -------------------------------------------------------------------------------------------------- *)
rValA := {val_a};
rValB := {val_b};
rValC := {val_c};

rDiffAB := ABS(rValA - rValB);
rDiffBC := ABS(rValB - rValC);
rDiffCA := ABS(rValC - rValA);

bAgreeAB := (rDiffAB <= {tol_const});
bAgreeBC := (rDiffBC <= {tol_const});
bAgreeCA := (rDiffCA <= {tol_const});

IF bAgreeAB AND bAgreeBC AND bAgreeCA THEN
    (* All three channels concordant: optimal mid-value median selection *)
    IF (rValA >= rValB AND rValA <= rValC) OR (rValA <= rValB AND rValA >= rValC) THEN
        rVotedVal := rValA;
    ELSIF (rValB >= rValA AND rValB <= rValC) OR (rValB <= rValA AND rValB >= rValC) THEN
        rVotedVal := rValB;
    ELSE
        rVotedVal := rValC;
    END_IF;
    {timer_var} := 0.0;
    {iso_a} := FALSE;
    {iso_b} := FALSE;
    {iso_c} := FALSE;

ELSIF bAgreeAB AND NOT bAgreeBC AND NOT bAgreeCA THEN
    (* Channel C deviating from A & B consensus *)
    rVotedVal := (rValA + rValB) * 0.5;
    {timer_var} := {timer_var} + c_rTs;
    IF {timer_var} >= c_rTMR_PersistencyLimit_s THEN
        {iso_c} := TRUE;
    END_IF;

ELSIF bAgreeBC AND NOT bAgreeAB AND NOT bAgreeCA THEN
    (* Channel A deviating from B & C consensus *)
    rVotedVal := (rValB + rValC) * 0.5;
    {timer_var} := {timer_var} + c_rTs;
    IF {timer_var} >= c_rTMR_PersistencyLimit_s THEN
        {iso_a} := TRUE;
    END_IF;

ELSIF bAgreeCA AND NOT bAgreeAB AND NOT bAgreeBC THEN
    (* Channel B deviating from C & A consensus *)
    rVotedVal := (rValC + rValA) * 0.5;
    {timer_var} := {timer_var} + c_rTs;
    IF {timer_var} >= c_rTMR_PersistencyLimit_s THEN
        {iso_b} := TRUE;
    END_IF;

ELSE
    (* Total Triplet Discrepancy: Hold prior valid telemetry, flag degradation *)
    rVotedVal := {voted_output};
    {timer_var} := {timer_var} + c_rTs;
    IF {timer_var} >= c_rTMR_PersistencyLimit_s THEN
        bAlarm_TMR_MajorDegraded_Warn := TRUE;
    END_IF;
END_IF;

{voted_output} := rVotedVal;
"""

def get_phase1_tmr():
    channels = [
        ("Drum Granule Bed Internal Temperature", "TT_DRUM_BED_TEMP_101",
         "TT_DRUM_BED_TEMP_101A", "TT_DRUM_BED_TEMP_101B", "TT_DRUM_BED_TEMP_101C",
         "c_rTol_DrumBedTemp_degC", "rVoted_DrumBedTemp_degC", "rTimer_BedTemp_Disc_s",
         "bIso_BedTemp_ChA", "bIso_BedTemp_ChB", "bIso_BedTemp_ChC"),

        ("Molten Slurry Spray Header Pressure", "PT_SLURRY_FEED_102",
         "PT_SLURRY_FEED_102A", "PT_SLURRY_FEED_102B", "PT_SLURRY_FEED_102C",
         "c_rTol_SlurryPress_bar", "rVoted_SlurryFeedPress_bar", "rTimer_SlurryPress_Disc_s",
         "bIso_SlurryPress_ChA", "bIso_SlurryPress_ChB", "bIso_SlurryPress_ChC"),

        ("Molten Slurry Spray Header Temperature", "TT_SLURRY_FEED_103",
         "TT_SLURRY_FEED_103A", "TT_SLURRY_FEED_103B", "TT_SLURRY_FEED_103C",
         "c_rTol_SlurryTemp_degC", "rVoted_SlurryFeedTemp_degC", "rTimer_SlurryTemp_Disc_s",
         "bIso_SlurryTemp_ChA", "bIso_SlurryTemp_ChB", "bIso_SlurryTemp_ChC"),

        ("Drum Outer Shell Hotspot Pyrometer", "TT_DRUM_SHELL_HOTSPOT_104",
         "TT_DRUM_SHELL_HOTSPOT_104A", "TT_DRUM_SHELL_HOTSPOT_104B", "TT_DRUM_SHELL_HOTSPOT_104C",
         "c_rTol_DrumShellHotspot_degC", "rVoted_DrumShellHotspot_degC", "rTimer_ShellHotspot_Disc_s",
         "bIso_ShellHotspot_ChA", "bIso_ShellHotspot_ChB", "bIso_ShellHotspot_ChC"),

        ("Dryer Flue Gas Inlet Temperature", "TT_DRYER_INLET_TEMP_201",
         "TT_DRYER_INLET_TEMP_201A", "TT_DRYER_INLET_TEMP_201B", "TT_DRYER_INLET_TEMP_201C",
         "c_rTol_DryerInletTemp_degC", "rVoted_DryerInletTemp_degC", "rTimer_DryerInletTemp_Disc_s",
         "bIso_DryerInletTemp_ChA", "bIso_DryerInletTemp_ChB", "bIso_DryerInletTemp_ChC"),

        ("Burner Natural Gas Fuel Flow", "FT_BURNER_FUEL_GAS_202",
         "FT_BURNER_FUEL_GAS_202A", "FT_BURNER_FUEL_GAS_202B", "FT_BURNER_FUEL_GAS_202C",
         "c_rTol_BurnerGasFlow_Nm3h", "rVoted_BurnerGasFlow_Nm3h", "rTimer_BurnerGasFlow_Disc_s",
         "bIso_BurnerGasFlow_ChA", "bIso_BurnerGasFlow_ChB", "bIso_BurnerGasFlow_ChC"),

        ("Forced Draft Combustion Air Flow", "FT_BURNER_AIR_FLOW_203",
         "FT_BURNER_AIR_FLOW_203A", "FT_BURNER_AIR_FLOW_203B", "FT_BURNER_AIR_FLOW_203C",
         "c_rTol_BurnerAirFlow_Nm3h", "rVoted_BurnerAirFlow_Nm3h", "rTimer_BurnerAirFlow_Disc_s",
         "bIso_BurnerAirFlow_ChA", "bIso_BurnerAirFlow_ChB", "bIso_BurnerAirFlow_ChC"),

        ("Burner Optical Flame Intensity Scanner", "BE_BURNER_FLAME_SCAN_204",
         "BE_BURNER_FLAME_SCAN_204A", "BE_BURNER_FLAME_SCAN_204B", "BE_BURNER_FLAME_SCAN_204C",
         "c_rTol_BurnerFlameScan_pct", "rVoted_BurnerFlameIntensity_pct", "rTimer_BurnerFlame_Disc_s",
         "bIso_BurnerFlame_ChA", "bIso_BurnerFlame_ChB", "bIso_BurnerFlame_ChC"),

        ("Fluid Bed Cooler Exit Granule Temperature", "TT_COOLER_ZONE4_TEMP_301",
         "TT_COOLER_ZONE4_TEMP_301A", "TT_COOLER_ZONE4_TEMP_301B", "TT_COOLER_ZONE4_TEMP_301C",
         "c_rTol_CoolerZone4Temp_degC", "rVoted_CoolerZone4Temp_degC", "rTimer_CoolerTemp_Disc_s",
         "bIso_CoolerTemp_ChA", "bIso_CoolerTemp_ChB", "bIso_CoolerTemp_ChC"),

        ("Cooler Air Plenum Differential Pressure", "PT_COOLER_PLENUM_302",
         "PT_COOLER_PLENUM_302A", "PT_COOLER_PLENUM_302B", "PT_COOLER_PLENUM_302C",
         "c_rTol_CoolerPlenumPress_mbar", "rVoted_CoolerPlenumPress_mbar", "rTimer_CoolerPlenum_Disc_s",
         "bIso_CoolerPlenum_ChA", "bIso_CoolerPlenum_ChB", "bIso_CoolerPlenum_ChC"),

        ("Solid Recycle Seed Mass Flow Rate", "WT_RECYCLE_MASS_FLOW_401",
         "WT_RECYCLE_MASS_FLOW_401A", "WT_RECYCLE_MASS_FLOW_401B", "WT_RECYCLE_MASS_FLOW_401C",
         "c_rTol_RecycleMassFlow_tph", "rVoted_RecycleMassFlow_tph", "rTimer_RecycleFlow_Disc_s",
         "bIso_RecycleFlow_ChA", "bIso_RecycleFlow_ChB", "bIso_RecycleFlow_ChC"),

        ("Finished On-Spec Product Mass Flow Rate", "WT_PRODUCT_MASS_FLOW_402",
         "WT_PRODUCT_MASS_FLOW_402A", "WT_PRODUCT_MASS_FLOW_402B", "WT_PRODUCT_MASS_FLOW_402C",
         "c_rTol_ProductMassFlow_tph", "rVoted_ProductMassFlow_tph", "rTimer_ProductFlow_Disc_s",
         "bIso_ProductFlow_ChA", "bIso_ProductFlow_ChB", "bIso_ProductFlow_ChC"),

        ("Venturi Scrubber Aerodynamic Delta P", "PDT_SCRUBBER_VENTURI_501",
         "PDT_SCRUBBER_VENTURI_501A", "PDT_SCRUBBER_VENTURI_501B", "PDT_SCRUBBER_VENTURI_501C",
         "c_rTol_VenturiDeltaP_mbar", "rVoted_VenturiDeltaP_mbar", "rTimer_VenturiDeltaP_Disc_s",
         "bIso_VenturiDeltaP_ChA", "bIso_VenturiDeltaP_ChB", "bIso_VenturiDeltaP_ChC"),

        ("Scrubber Recirculating Liquor pH Probe", "AT_SCRUBBER_SUMP_PH_502",
         "AT_SCRUBBER_SUMP_PH_502A", "AT_SCRUBBER_SUMP_PH_502B", "AT_SCRUBBER_SUMP_PH_502C",
         "c_rTol_Scrubber_pH", "rVoted_Scrubber_pH", "rTimer_Scrubber_pH_Disc_s",
         "bIso_Scrubber_pH_ChA", "bIso_Scrubber_pH_ChB", "bIso_Scrubber_pH_ChC"),

        ("Tail-Gas Stack Optical Dust Concentration", "AT_STACK_PARTICULATE_503",
         "AT_STACK_PARTICULATE_503A", "AT_STACK_PARTICULATE_503B", "AT_STACK_PARTICULATE_503C",
         "c_rTol_StackDust_mgNm3", "rVoted_StackDust_mgNm3", "rTimer_StackDust_Disc_s",
         "bIso_StackDust_ChA", "bIso_StackDust_ChB", "bIso_StackDust_ChC"),

        ("Tail-Gas Stack Ammonia Slip Analyzer", "AT_STACK_AMMONIA_SLIP_504",
         "AT_STACK_AMMONIA_SLIP_504A", "AT_STACK_AMMONIA_SLIP_504B", "AT_STACK_AMMONIA_SLIP_504C",
         "c_rTol_StackAmmoniaSlip_ppmv", "rVoted_StackAmmoniaSlip_ppmv", "rTimer_AmmoniaSlip_Disc_s",
         "bIso_AmmoniaSlip_ChA", "bIso_AmmoniaSlip_ChB", "bIso_AmmoniaSlip_ChC")
    ]

    lines = [
        "(* ============================================================================================================== *)",
        "(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING WITH BUMPLESS DEGRADATION (16 CHANNELS)                   *)",
        "(* ============================================================================================================== *)"
    ]
    for ch in channels:
        lines.append(get_tmr_channel_logic(*ch))

    return "\n".join(lines)
