# -*- coding: utf-8 -*-
"""
Module: mod_phase1_tmr.py
Generates PHASE 1: 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite & Discrepancy Timers
for FB_Tunneling_SlurryTBM_Cutterhead_BentoniteBalance.
Covers all 10 analog sensor triplets with pairwise error checking, discrepancy accumulation timers,
channel isolation, bumpless degradation (2oo3 -> 1oo2 -> 1oo1), and health diagnostic word bit packing.
"""

def generate_triplet_st(
    idx: int,
    name: str,
    tag: str,
    unit: str,
    sigA: str,
    sigB: str,
    sigC: str,
    tol: str,
    timerAB: str,
    timerBC: str,
    timerCA: str,
    faultA: str,
    faultB: str,
    faultC: str,
    votedVar: str,
    defaultVal: str,
    bitOffset: int
) -> str:
    return f"""
(* ------------------------------------------------------------------------------------------- *)
(* 1.{idx} {name.upper()} ({tag}) [2oo3 VOTING]                                             *)
(* ------------------------------------------------------------------------------------------- *)
(* Pairwise Discrepancy Evaluation *)
IF ABS({sigA} - {sigB}) > {tol} THEN
    {timerAB} := {timerAB} + rCycleTime_s;
ELSE
    {timerAB} := MAX(0.0, {timerAB} - (rCycleTime_s * 2.0));
END_IF;

IF ABS({sigB} - {sigC}) > {tol} THEN
    {timerBC} := {timerBC} + rCycleTime_s;
ELSE
    {timerBC} := MAX(0.0, {timerBC} - (rCycleTime_s * 2.0));
END_IF;

IF ABS({sigC} - {sigA}) > {tol} THEN
    {timerCA} := {timerCA} + rCycleTime_s;
ELSE
    {timerCA} := MAX(0.0, {timerCA} - (rCycleTime_s * 2.0));
END_IF;

(* Channel Fault Quarantine Latching *)
IF ({timerAB} >= c_rDiscrepancyLimit_s) AND ({timerCA} >= c_rDiscrepancyLimit_s) THEN
    {faultA} := TRUE;
END_IF;

IF ({timerAB} >= c_rDiscrepancyLimit_s) AND ({timerBC} >= c_rDiscrepancyLimit_s) THEN
    {faultB} := TRUE;
END_IF;

IF ({timerBC} >= c_rDiscrepancyLimit_s) AND ({timerCA} >= c_rDiscrepancyLimit_s) THEN
    {faultC} := TRUE;
END_IF;

(* Automatic Channel Fault Self-Healing Reset *)
IF ({faultA}) AND ({timerAB} = 0.0) AND ({timerCA} = 0.0) THEN
    {faultA} := FALSE;
END_IF;

IF ({faultB}) AND ({timerAB} = 0.0) AND ({timerBC} = 0.0) THEN
    {faultB} := FALSE;
END_IF;

IF ({faultC}) AND ({timerBC} = 0.0) AND ({timerCA} = 0.0) THEN
    {faultC} := FALSE;
END_IF;

(* Bumpless Voted Value Selection Logic *)
IF (NOT {faultA}) AND (NOT {faultB}) AND (NOT {faultC}) THEN
    (* 3 Channels Healthy: Standard Mid-Value / Median Selector *)
    IF (({sigA} >= {sigB}) AND ({sigA} <= {sigC})) OR (({sigA} >= {sigC}) AND ({sigA} <= {sigB})) THEN
        {votedVar} := {sigA};
    ELSIF (({sigB} >= {sigA}) AND ({sigB} <= {sigC})) OR (({sigB} >= {sigC}) AND ({sigB} <= {sigA})) THEN
        {votedVar} := {sigB};
    ELSE
        {votedVar} := {sigC};
    END_IF;
ELSIF (NOT {faultA}) AND (NOT {faultB}) AND ({faultC}) THEN
    (* Channel C Faulty: 2-Channel Average (A + B) / 2 *)
    {votedVar} := ({sigA} + {sigB}) * 0.50;
ELSIF (NOT {faultA}) AND ({faultB}) AND (NOT {faultC}) THEN
    (* Channel B Faulty: 2-Channel Average (A + C) / 2 *)
    {votedVar} := ({sigA} + {sigC}) * 0.50;
ELSIF ({faultA}) AND (NOT {faultB}) AND (NOT {faultC}) THEN
    (* Channel A Faulty: 2-Channel Average (B + C) / 2 *)
    {votedVar} := ({sigB} + {sigC}) * 0.50;
ELSIF (NOT {faultA}) AND ({faultB}) AND ({faultC}) THEN
    (* Only Channel A Healthy: Degraded Single Channel Hold *)
    {votedVar} := {sigA};
ELSIF ({faultA}) AND (NOT {faultB}) AND ({faultC}) THEN
    (* Only Channel B Healthy: Degraded Single Channel Hold *)
    {votedVar} := {sigB};
ELSIF ({faultA}) AND ({faultB}) AND (NOT {faultC}) THEN
    (* Only Channel C Healthy: Degraded Single Channel Hold *)
    {votedVar} := {sigC};
ELSE
    (* All Channels Tripped: Fail-Safe Safe Default State *)
    {votedVar} := {defaultVal};
END_IF;

(* Diagnostic Status Word Packing for Triplet {idx} *)
IF {faultA} THEN
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR SHL(DWORD#1, {bitOffset});
END_IF;
IF {faultB} THEN
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR SHL(DWORD#1, {bitOffset + 1});
END_IF;
IF {faultC} THEN
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR SHL(DWORD#1, {bitOffset + 2});
END_IF;
"""

def get_phase1_tmr() -> str:
    header = [
        "(* =========================================================================================== *)",
        "(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE                   === *)",
        "(* =========================================================================================== *)",
        "(* Clear Diagnostic Status Register at Scan Start *)",
        "dwTMR_DiagnosticWord := 16#00000000;",
        ""
    ]
    
    triplets = [
        (1, "Chamber Crown Hydrostatic Pressure", "PT-101A/B/C", "[bar]",
         "rChamberPress_PT101A_bar", "rChamberPress_PT101B_bar", "rChamberPress_PT101C_bar",
         "c_rChamberPress_Tol_bar", "rChamberPress_DiscTimer_AB", "rChamberPress_DiscTimer_BC", "rChamberPress_DiscTimer_CA",
         "bChamberPress_Fault_A", "bChamberPress_Fault_B", "bChamberPress_Fault_C",
         "rVotedChamberPress_bar", "rHydroOverburdenTarget_bar", 0),
         
        (2, "Compressed Air Bubble Cushion Pressure", "PT-201A/B/C", "[bar]",
         "rAirBubblePress_PT201A_bar", "rAirBubblePress_PT201B_bar", "rAirBubblePress_PT201C_bar",
         "c_rAirBubblePress_Tol_bar", "rAirBubblePress_DiscTimer_AB", "rAirBubblePress_DiscTimer_BC", "rAirBubblePress_DiscTimer_CA",
         "bAirBubblePress_Fault_A", "bAirBubblePress_Fault_B", "bAirBubblePress_Fault_C",
         "rVotedAirBubblePress_bar", "rHydroOverburdenTarget_bar", 3),

        (3, "Air Bubble Working Chamber Bentonite Level", "LT-202A/B/C", "[m]",
         "rAirBubbleLevel_LT202A_m", "rAirBubbleLevel_LT202B_m", "rAirBubbleLevel_LT202C_m",
         "c_rAirBubbleLevel_Tol_m", "rAirBubbleLevel_DiscTimer_AB", "rAirBubbleLevel_DiscTimer_BC", "rAirBubbleLevel_DiscTimer_CA",
         "bAirBubbleLevel_Fault_A", "bAirBubbleLevel_Fault_B", "bAirBubbleLevel_Fault_C",
         "rVotedAirBubbleLevel_m", "6.50", 6),

        (4, "Fresh Bentonite Feed Volumetric Flow Rate", "FT-301A/B/C", "[m3/h]",
         "rSlurryFeedFlow_FT301A_m3h", "rSlurryFeedFlow_FT301B_m3h", "rSlurryFeedFlow_FT301C_m3h",
         "c_rFeedFlow_Tol_m3h", "rFeedFlow_DiscTimer_AB", "rFeedFlow_DiscTimer_BC", "rFeedFlow_DiscTimer_CA",
         "bFeedFlow_Fault_A", "bFeedFlow_Fault_B", "bFeedFlow_Fault_C",
         "rVotedFeedFlow_m3h", "1200.0", 9),

        (5, "Excavated Muck Slurry Discharge Flow Rate", "FT-302A/B/C", "[m3/h]",
         "rSlurryDischFlow_FT302A_m3h", "rSlurryDischFlow_FT302B_m3h", "rSlurryDischFlow_FT302C_m3h",
         "c_rDischFlow_Tol_m3h", "rDischFlow_DiscTimer_AB", "rDischFlow_DiscTimer_BC", "rDischFlow_DiscTimer_CA",
         "bDischFlow_Fault_A", "bDischFlow_Fault_B", "bDischFlow_Fault_C",
         "rVotedDischFlow_m3h", "1350.0", 12),

        (6, "Fresh Bentonite Feed Slurry Density", "DT-401A/B/C", "[t/m3]",
         "rFeedDensity_DT401A_tm3", "rFeedDensity_DT401B_tm3", "rFeedDensity_DT401C_tm3",
         "c_rFeedDensity_Tol_tm3", "rFeedDensity_DiscTimer_AB", "rFeedDensity_DiscTimer_BC", "rFeedDensity_DiscTimer_CA",
         "bFeedDensity_Fault_A", "bFeedDensity_Fault_B", "bFeedDensity_Fault_C",
         "rVotedFeedDensity_tm3", "1.080", 15),

        (7, "Excavated Muck Slurry Discharge Density", "DT-402A/B/C", "[t/m3]",
         "rDischDensity_DT402A_tm3", "rDischDensity_DT402B_tm3", "rDischDensity_DT402C_tm3",
         "c_rDischDensity_Tol_tm3", "rDischDensity_DiscTimer_AB", "rDischDensity_DiscTimer_BC", "rDischDensity_DiscTimer_CA",
         "bDischDensity_Fault_A", "bDischDensity_Fault_B", "bDischDensity_Fault_C",
         "rVotedDischDensity_tm3", "1.320", 18),

        (8, "Total Shield Advance Thrust Load Cells", "LC-601A/B/C", "[kN]",
         "rTotalThrustForce_LC601A_kN", "rTotalThrustForce_LC601B_kN", "rTotalThrustForce_LC601C_kN",
         "c_rTotalThrust_Tol_kN", "rTotalThrust_DiscTimer_AB", "rTotalThrust_DiscTimer_BC", "rTotalThrust_DiscTimer_CA",
         "bTotalThrust_Fault_A", "bTotalThrust_Fault_B", "bTotalThrust_Fault_C",
         "rVotedTotalThrust_kN", "85000.0", 21),

        (9, "Cutterhead Drive Torque Transducers", "TT-501A/B/C", "[kNm]",
         "rCutterheadTorque_TT501A_kNm", "rCutterheadTorque_TT501B_kNm", "rCutterheadTorque_TT501C_kNm",
         "c_rCutterheadTorque_Tol_kNm", "rCutterTorque_DiscTimer_AB", "rCutterTorque_DiscTimer_BC", "rCutterTorque_DiscTimer_CA",
         "bCutterTorque_Fault_A", "bCutterTorque_Fault_B", "bCutterTorque_Fault_C",
         "rVotedCutterheadTorque_kNm", "18500.0", 24),

        (10, "Annular Tail Void Grout Injection Pressure", "PT-701A/B/C", "[bar]",
         "rTailGroutPress_PT701A_bar", "rTailGroutPress_PT701B_bar", "rTailGroutPress_PT701C_bar",
         "c_rTailGroutPress_Tol_bar", "rTailGrout_DiscTimer_AB", "rTailGrout_DiscTimer_BC", "rTailGrout_DiscTimer_CA",
         "bTailGrout_Fault_A", "bTailGrout_Fault_B", "bTailGrout_Fault_C",
         "rVotedTailGroutPress_bar", "3.80", 27)
    ]
    
    body = [generate_triplet_st(*t) for t in triplets]
    return "\n".join(header) + "\n".join(body)
