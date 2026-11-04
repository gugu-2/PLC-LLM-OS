# -*- coding: utf-8 -*-
"""
Builder script for the complete FB_Energy_Subsea_Wellhead_HIPPS_ChokeAntiSlug dataset.
"""

import os
import sys
import json
import uuid
import re

AGENT_UUID = "78709445"
TARGET_JSON = f"data/swarm_raw/agent_{AGENT_UUID}.json"

def build_section_matrices():
    lines = []
    lines.append("(* =========================================================================================== *)")
    lines.append("(* 1.0 CYBER-PHYSICAL DISCRETE STATE-SPACE MATRIX INITIALIZATION (8x8 DYNAMICS @ 5ms)         *)")
    lines.append("(* =========================================================================================== *)")
    lines.append("IF NOT bMatrixInitialized THEN")
    lines.append("    (* --- Matrix A (8x8): Multiphase Hydrodynamics, Hydrate Enthalpy & SCM Hydraulics --- *)")
    
    # State-Space Matrix A (8x8)
    # x1: Wellhead Tubing Pressure [bar]
    # x2: Downstream Manifold Pressure [bar]
    # x3: Liquid Slug Holdup Volume [m3]
    # x4: Multiphase Mixture Mass Flow [kg/s]
    # x5: Fluid Temperature [deg C]
    # x6: Aqueous MEG Concentration [wt%]
    # x7: Booster Pump Head [bar]
    # x8: Hydraulic Umbilical Pressure [bar]
    
    matrix_a_comments = {
        (1, 1): "Tubing acoustic capacitance and compressed reservoir fluid elasticity persistence",
        (1, 2): "Downstream flowline pressure back-coupling across choke orifice restriction",
        (1, 3): "Hydrostatic gravity head fluctuation from incoming dense liquid slug slugs",
        (1, 4): "Frictional pressure loss in wellhead production tubing strings (Darcy-Weisbach)",
        (1, 5): "Joule-Thomson thermal expansion pressure variance in high-pressure tubing gas",
        (1, 6): "Viscosity increase due to high-concentration chemical MEG injection",
        (1, 7): "Suction pressure drawdown from subsea multiphase booster pump impeller rotation",
        (1, 8): "Coupling from electro-hydraulic SCM valve actuator pilot movement",
        
        (2, 1): "Choke throat acoustic wave transmission from wellhead tubing pressure disturbances",
        (2, 2): "Downstream export flowline pipeline capacitance and compressibility persistence",
        (2, 3): "Momentum surge discharge during liquid slug passage into downstream manifold",
        (2, 4): "Multiphase mixture velocity expansion across choke vena contracta",
        (2, 5): "Thermal expansion of gas phase downstream of choke throat",
        (2, 6): "Density stabilization from aqueous glycol mixture fraction",
        (2, 7): "Direct head elevation across multiphase booster pump discharge plenum",
        (2, 8): "Actuator hydraulic transient damping across pilot choke trim",
        
        (3, 1): "Wellhead pressure differential driving liquid film accumulation in riser dip",
        (3, 2): "Manifold backpressure resistance against slug body discharge",
        (3, 3): "Hydrodynamic drift-flux liquid slug mass holdup persistence (Zuber-Findlay)",
        (3, 4): "Gas superficial velocity shear entrainment stripping liquid film into droplets",
        (3, 5): "Thermodynamic flash evaporation of volatile condensate fractions",
        (3, 6): "Interfacial surface tension alteration by injected glycol surfactant",
        (3, 7): "Multiphase pump suction volumetric ingestion clearing slug liquid holdup",
        (3, 8): "Choke stepping servo trim hydraulic transient disturbance",
        
        (4, 1): "Positive pressure gradient driving total multiphase mixture mass acceleration",
        (4, 2): "Opposing manifold pressure gradient retarding mixture mass acceleration",
        (4, 3): "Heavy liquid slug density acceleration inertia across choke restriction",
        (4, 4): "Mixture momentum conservation and wall frictional dissipation persistence",
        (4, 5): "Gas density variation with temperature modulating mass throughput",
        (4, 6): "Aqueous phase density elevation under concentrated MEG dosing",
        (4, 7): "Booster pump positive differential pressure driving mixture throughput",
        (4, 8): "Pilot valve hydraulic pressure jitter coupling into choke sleeve",
        
        (5, 1): "Upstream geothermal reservoir fluid thermal enthalpy advection flux",
        (5, 2): "Downstream pressure expansion modifying Joule-Thomson cooling coefficient",
        (5, 3): "Thermal inertia of dense liquid hydrocarbon and formation water slug slugs",
        (5, 4): "Advective convective heat transfer rate across titanium flowline walls",
        (5, 5): "Thermal dissipation and abyssal seawater heat loss persistence (U*A delta T)",
        (5, 6): "Enthalpy of dilution during dynamic concentrated MEG injection mixing",
        (5, 7): "Viscous dissipation and impeller hydraulic inefficiency thermal heating",
        (5, 8): "SCM hydraulic pilot oil thermal dissipation cross-conduction",
        
        (6, 1): "Wellhead pressure effect on water phase condensation and dilution equilibrium",
        (6, 2): "Manifold pressure feedback on aqueous phase thermodynamic equilibrium",
        (6, 3): "Slug water holdup influx diluting injected monoethylene glycol concentration",
        (6, 4): "Produced water mass flow rate dilution pacing requirement",
        (6, 5): "Hydrate equilibrium boundary shift with localized fluid temperature",
        (6, 6): "Aqueous chemical concentration mass balance retention persistence",
        (6, 7): "Booster pump shear mixing promoting homogenous aqueous phase dispersion",
        (6, 8): "CIMV hydraulic actuator line pressure stability coupling",
        
        (7, 1): "Upstream suction header pressure contribution to booster pump total head",
        (7, 2): "Discharge header backpressure resistance against booster pump stages",
        (7, 3): "Liquid slug ingestion shifting pump operating point along affinity curve",
        (7, 4): "Volumetric flow rate throughput across pump stage compression chambers",
        (7, 5): "Fluid viscosity and density thermal dependency modulating stage efficiency",
        (7, 6): "Aqueous glycol viscosity contribution to pump impeller disk friction",
        (7, 7): "Multiphase booster pump dynamic head generation persistence (Affinity Law)",
        (7, 8): "SCM hydraulic supply pressure stability to pump motor seal barrier system",
        
        (8, 1): "Wellhead vibration cross-talk into subsea umbilical hydraulic termination head",
        (8, 2): "Manifold pulsation feedback on subsea control module hydraulic manifold",
        (8, 3): "Severe slugging mechanical shock transmission through wellhead tree frame",
        (8, 4): "Production flow pulsation reaction forces on choke valve body",
        (8, 5): "Thermal expansion of subsea control module mineral hydraulic oil",
        (8, 6): "Chemical injection backpressure interaction across check valves",
        (8, 7): "Booster pump inverter electrical noise filter coupling to SCM telemetry",
        (8, 8): "Subsea electro-hydraulic multiplexed accumulator pressure persistence"
    }

    # Populate matA values
    a_values = [
        [0.9820, -0.0450,  0.1250, -0.0180,  0.0035, -0.0012, -0.0220,  0.0005],
        [0.0520,  0.9410,  0.2850,  0.0380,  0.0042, -0.0008,  0.0650,  0.0004],
        [0.0045, -0.0085,  0.8920, -0.0125, -0.0015, -0.0022, -0.0150,  0.0001],
        [0.0850, -0.0920,  0.1650,  0.9240,  0.0085,  0.0045,  0.0420,  0.0008],
        [0.0120, -0.0065,  0.0450,  0.0320,  0.9650,  0.0018,  0.0095,  0.0002],
        [-0.0015, 0.0008, -0.0850, -0.0420,  0.0055,  0.9120,  0.0035,  0.0001],
        [0.0180, -0.0320,  0.0650, -0.0450,  0.0025,  0.0015,  0.9520,  0.0006],
        [0.0002, -0.0001,  0.0012,  0.0008,  0.0001,  0.0000,  0.0004,  0.9850]
    ]

    for r in range(1, 9):
        for c in range(1, 9):
            val = a_values[r-1][c-1]
            comm = matrix_a_comments.get((r, c), "State transition cross-coupling")
            lines.append(f"    matA[{r}, {c}] := {val:10.4f}; (* {comm} *)")

    lines.append("")
    lines.append("    (* --- Matrix B (8x4): Actuator Coupling & Hydraulic Authority --- *)")
    # Actuators:
    # u1: Anti-Surge Choke Stroke Delta_z_choke [%]
    # u2: Multiphase Booster Pump RPM Delta_N_pump [rpm]
    # u3: CIMV MEG Flow Valve Stroke Delta_z_meg [%]
    # u4: Subsea MUX Hydraulic Pilot Supply Delta_u_hyd [%]
    
    matrix_b_comments = {
        (1, 1): "Choke opening decreases upstream wellhead tubing head backpressure",
        (1, 2): "Booster pump acceleration lowers wellhead pressure by drawing suction",
        (1, 3): "MEG injection pressure negligible effect on wellhead tubing head",
        (1, 4): "Hydraulic supply stabilization ensures precise choke positioning",
        
        (2, 1): "Choke opening increases downstream manifold pressure through mass inflow",
        (2, 2): "Booster pump speed directly pressurizes downstream manifold flowline",
        (2, 3): "Liquid glycol volume adds minor hydrostatic and flow displacement",
        (2, 4): "Pilot valve hydraulic pressure stability dampens manifold chatter",
        
        (3, 1): "Throttling choke holds back liquid slugs and mitigates riser flooding",
        (3, 2): "Booster pump speed sweeps slug liquid out of suction manifold spool",
        (3, 3): "Chemical glycol injection adds liquid phase volume at injection point",
        (3, 4): "Hydraulic actuator response time governing anti-surge choke damping",
        
        (4, 1): "Choke valve opening expands effective orifice area increasing mass rate",
        (4, 2): "Booster pump differential head increases total multiphase mass throughput",
        (4, 3): "Chemical injection mass flow directly adds to stream mass balance",
        (4, 4): "Hydraulic pilot valve dynamics enabling high-frequency flow trimming",
        
        (5, 1): "Joule-Thomson temperature drop across opening choke valve expansion",
        (5, 2): "Pump mechanical shear dissipation mildly elevates stream temperature",
        (5, 3): "Cold MEG chemical supply enthalpy mixes with hydrocarbon stream",
        (5, 4): "Hydraulic fluid conduction negligible thermal effect on flowline",
        
        (6, 1): "Choke flow rate variation scales dilution ratio of injected glycol",
        (6, 2): "Booster pump mixing efficiency promotes rapid hydrate inhibition",
        (6, 3): "CIMV valve opening directly injects concentrated Monoethylene Glycol",
        (6, 4): "Hydraulic actuator pressure governing chemical valve stem accuracy",
        
        (7, 1): "Choke throttling reduces suction header pressure delivered to pump",
        (7, 2): "Variable frequency drive RPM command directly scales affinity law head",
        (7, 3): "MEG chemical injection negligible direct effect on pump head",
        (7, 4): "Hydraulic supply pressure maintains pump mechanical seal barrier fluid",
        
        (8, 1): "Choke actuator movement consumes hydraulic accumulator volume",
        (8, 2): "Booster pump speed command decoupled from hydraulic SCM manifold",
        (8, 3): "CIMV stepping motor consumes minor hydraulic pilot power",
        (8, 4): "SCM umbilical high-pressure hydraulic supply regulator input authority"
    }

    b_values = [
        [-0.0850, -0.0015,  0.0000,  0.0010],
        [ 0.1150,  0.0045,  0.0005,  0.0015],
        [-0.0450, -0.0028,  0.0012, -0.0005],
        [ 0.2450,  0.0085,  0.0025,  0.0020],
        [-0.0350,  0.0012, -0.0150,  0.0000],
        [-0.0120,  0.0008,  0.0850,  0.0002],
        [-0.0250,  0.0350,  0.0000,  0.0018],
        [-0.0080,  0.0000, -0.0015,  0.1250]
    ]

    for r in range(1, 9):
        for c in range(1, 4):
            val = b_values[r-1][c-1]
            comm = matrix_b_comments.get((r, c), "Actuator authority coupling")
            lines.append(f"    matB[{r}, {c}] := {val:10.4f}; (* {comm} *)")
        val4 = b_values[r-1][3]
        comm4 = matrix_b_comments.get((r, 4), "Actuator authority coupling")
        lines.append(f"    matB[{r}, 4] := {val4:10.4f}; (* {comm4} *)")

    lines.append("")
    lines.append("    (* --- Matrix C (8x8): Output Observation Sensor Calibration --- *)")
    for r in range(1, 9):
        for c in range(1, 9):
            if r == c:
                lines.append(f"    matC[{r}, {c}] :=     1.0000; (* Direct state observation Channel {r} *)")
            else:
                lines.append(f"    matC[{r}, {c}] :=     0.0000; (* State observation decoupling *)")

    lines.append("")
    lines.append("    (* --- Matrix D (8x4): Direct Feedthrough Feedforward Matrix --- *)")
    for r in range(1, 9):
        for c in range(1, 5):
            lines.append(f"    matD[{r}, {c}] :=     0.0000; (* Strict physical causal decoupling *)")

    lines.append("")
    lines.append("    (* --- Matrix Q (8x8): Receding Horizon State Tracking Penalty Weights --- *)")
    q_weights = [45.0, 85.0, 120.0, 35.0, 25.0, 110.0, 50.0, 15.0]
    q_desc = [
        "Wellhead pressure fluctuation penalty (stabilize reservoir draw)",
        "Downstream manifold pressure penalty (prevent flowline overpressure)",
        "Liquid slug holdup surge penalty (aggressive damping of slug wave)",
        "Multiphase mass throughput deviation penalty (maintain production rate)",
        "Choke throat temperature penalty (prevent thermal fatigue cycling)",
        "Aqueous MEG chemical concentration error penalty (guarantee hydrate safety)",
        "Booster pump head stability penalty (prevent impeller hunting)",
        "SCM umbilical hydraulic pressure stability penalty"
    ]
    for r in range(1, 9):
        for c in range(1, 9):
            if r == c:
                lines.append(f"    matQ[{r}, {c}] := {q_weights[r-1]:10.2f}; (* {q_desc[r-1]} *)")
            else:
                lines.append(f"    matQ[{r}, {c}] :=       0.00; (* Cross-penalty decoupling *)")

    lines.append("")
    lines.append("    (* --- Matrix R (4x4): Control Actuation Effort & Slew Penalties --- *)")
    r_weights = [15.0, 8.5, 22.0, 5.0]
    r_desc = [
        "Choke stepping motor mechanical wear penalty",
        "Multiphase pump VFD electrical inverter stress penalty",
        "MEG chemical inhibitor consumption economic cost penalty",
        "SCM pilot hydraulic fluid consumption penalty"
    ]
    for r in range(1, 5):
        for c in range(1, 5):
            if r == c:
                lines.append(f"    matR[{r}, {c}] := {r_weights[r-1]:10.2f}; (* {r_desc[r-1]} *)")
            else:
                lines.append(f"    matR[{r}, {c}] :=       0.00; (* Actuator cross-effort decoupling *)")

    lines.append("")
    lines.append("    (* --- Matrix P (8x8): Terminal Horizon Lyapunov Stability Penalties --- *)")
    for r in range(1, 9):
        for c in range(1, 9):
            if r == c:
                term_val = q_weights[r-1] * 2.5
                lines.append(f"    matP[{r}, {c}] := {term_val:10.2f}; (* Terminal Lyapunov stability state {r} *)")
            else:
                lines.append(f"    matP[{r}, {c}] :=       0.00; (* Terminal decoupling *)")

    lines.append("")
    lines.append("    (* Hard Actuator Saturation & Rate Limits *)")
    lines.append("    uLowerLimit[1] :=   2.00; (* Minimum choke cracking position [%] *)")
    lines.append("    uUpperLimit[1] := 100.00; (* Maximum full open choke position [%] *)")
    lines.append("    deltaUMaxLimit[1] := 0.25; (* Maximum choke stroke change per 5ms scan [%] *)")
    lines.append("")
    lines.append("    uLowerLimit[2] := 800.00; (* Minimum booster pump speed [rpm] *)")
    lines.append("    uUpperLimit[2] := 3600.00; (* Maximum booster pump speed [rpm] *)")
    lines.append("    deltaUMaxLimit[2] := 5.00; (* Maximum booster pump RPM change per scan [rpm] *)")
    lines.append("")
    lines.append("    uLowerLimit[3] :=   0.00; (* Minimum MEG injection valve stroke [%] *)")
    lines.append("    uUpperLimit[3] := 100.00; (* Maximum MEG injection valve stroke [%] *)")
    lines.append("    deltaUMaxLimit[3] := 0.50; (* Maximum MEG valve stroke change per scan [%] *)")
    lines.append("")
    lines.append("    uLowerLimit[4] :=   0.00; (* Minimum hydraulic pilot modulation [%] *)")
    lines.append("    uUpperLimit[4] := 100.00; (* Maximum hydraulic pilot modulation [%] *)")
    lines.append("    deltaUMaxLimit[4] := 1.00; (* Maximum hydraulic pilot stroke change per scan [%] *)")
    lines.append("")
    lines.append("    bMatrixInitialized := TRUE;")
    lines.append("END_IF;")
    lines.append("")
    return "\n".join(lines)

def build_section_tmr():
    lines = []
    lines.append("(* =========================================================================================== *)")
    lines.append("(* 2.0 PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY TIMERS       *)")
    lines.append("(* =========================================================================================== *)")
    lines.append("(* Evaluates 8 critical instrument triplets with 2oo3 median selection, discrepancy timers,   *)")
    lines.append("(* and bumpless degradation from 2oo3 to 1oo2 to 1oo1 fail-safe before latching a fault.     *)")
    lines.append("")
    
    triplets = [
        ("PT101", "Wellhead Tubing Pressure [bar]", "PT_WELLHEAD_INLET_101A", "PT_WELLHEAD_INLET_101B", "PT_WELLHEAD_INLET_101C", "c_TmrTol_WellheadPress_bar", "rVotedWellheadPressure_bar", "bar"),
        ("PT102", "Choke Downstream Manifold Pressure [bar]", "PT_CHOKE_DOWNSTREAM_102A", "PT_CHOKE_DOWNSTREAM_102B", "PT_CHOKE_DOWNSTREAM_102C", "c_TmrTol_ManifoldPress_bar", "rVotedChokeDownstreamPressure_bar", "bar"),
        ("TT201", "Wellhead Fluid Bore Temperature [deg C]", "TT_WELLHEAD_FLUID_201A", "TT_WELLHEAD_FLUID_201B", "TT_WELLHEAD_FLUID_201C", "c_TmrTol_FluidTemp_degC", "rVotedWellheadTemp_degC", "deg C"),
        ("FT301", "Wet Gas Ultrasonic Mass Flow [kg/s]", "FT_WETGAS_ULTRASONIC_301A", "FT_WETGAS_ULTRASONIC_301B", "FT_WETGAS_ULTRASONIC_301C", "c_TmrTol_WetGasFlow_kgs", "rVotedWetGasFlow_kgs", "kg/s"),
        ("DT401", "Fast Gamma Slug Density [kg/m3]", "DT_SLUG_GAMMA_DENSITY_401A", "DT_SLUG_GAMMA_DENSITY_401B", "DT_SLUG_GAMMA_DENSITY_401C", "c_TmrTol_SlugDensity_kgm3", "rVotedSlugDensity_kgm3", "kg/m3"),
        ("PT501", "HIPPS Inter-Valve Cavity Pressure [bar]", "PT_HIPPS_INTERMEDIATE_501A", "PT_HIPPS_INTERMEDIATE_501B", "PT_HIPPS_INTERMEDIATE_501C", "c_TmrTol_HippsPress_bar", "rVotedHippsPressure_bar", "bar"),
        ("FT601", "MEG Chemical Injection Flow [L/h]", "FT_MEG_INHIBITOR_601A", "FT_MEG_INHIBITOR_601B", "FT_MEG_INHIBITOR_601C", "c_TmrTol_MegFlow_Lh", "rVotedMegFlow_Lh", "L/h"),
        ("ZT701", "Choke Actuator LVDT Stroke [%]", "ZT_CHOKE_ACTUATOR_POS_701A", "ZT_CHOKE_ACTUATOR_POS_701B", "ZT_CHOKE_ACTUATOR_POS_701C", "c_TmrTol_ChokePos_pct", "rVotedChokePosition_pct", "%")
    ]

    for tag, desc, chA, chB, chC, tol, votedVar, unit in triplets:
        lines.append(f"(* --- 2oo3 TMR Bank: {desc} --- *)")
        lines.append(f"rDev_{tag}_AB := ABS({chA} - {chB});")
        lines.append(f"rDev_{tag}_BC := ABS({chB} - {chC});")
        lines.append(f"rDev_{tag}_CA := ABS({chC} - {chA});")
        lines.append("")
        lines.append(f"tDiscrepancy_{tag}_AB(IN := (rDev_{tag}_AB > {tol}), PT := c_TmrPersistenceTime);")
        lines.append(f"tDiscrepancy_{tag}_BC(IN := (rDev_{tag}_BC > {tol}), PT := c_TmrPersistenceTime);")
        lines.append(f"tDiscrepancy_{tag}_CA(IN := (rDev_{tag}_CA > {tol}), PT := c_TmrPersistenceTime);")
        lines.append("")
        lines.append(f"IF tDiscrepancy_{tag}_AB.Q AND tDiscrepancy_{tag}_CA.Q THEN")
        lines.append(f"    bFault_{tag}_A := TRUE; (* Channel A persistent out-of-bounds deviation *)")
        lines.append(f"ELSIF NOT (rDev_{tag}_AB > {tol}) AND NOT (rDev_{tag}_CA > {tol}) THEN")
        lines.append(f"    bFault_{tag}_A := FALSE;")
        lines.append("END_IF;")
        lines.append("")
        lines.append(f"IF tDiscrepancy_{tag}_AB.Q AND tDiscrepancy_{tag}_BC.Q THEN")
        lines.append(f"    bFault_{tag}_B := TRUE; (* Channel B persistent out-of-bounds deviation *)")
        lines.append(f"ELSIF NOT (rDev_{tag}_AB > {tol}) AND NOT (rDev_{tag}_BC > {tol}) THEN")
        lines.append(f"    bFault_{tag}_B := FALSE;")
        lines.append("END_IF;")
        lines.append("")
        lines.append(f"IF tDiscrepancy_{tag}_BC.Q AND tDiscrepancy_{tag}_CA.Q THEN")
        lines.append(f"    bFault_{tag}_C := TRUE; (* Channel C persistent out-of-bounds deviation *)")
        lines.append(f"ELSIF NOT (rDev_{tag}_BC > {tol}) AND NOT (rDev_{tag}_CA > {tol}) THEN")
        lines.append(f"    bFault_{tag}_C := FALSE;")
        lines.append("END_IF;")
        lines.append("")
        lines.append(f"iHealthyCount_{tag} := 3;")
        lines.append(f"IF bFault_{tag}_A THEN iHealthyCount_{tag} := iHealthyCount_{tag} - 1; END_IF;")
        lines.append(f"IF bFault_{tag}_B THEN iHealthyCount_{tag} := iHealthyCount_{tag} - 1; END_IF;")
        lines.append(f"IF bFault_{tag}_C THEN iHealthyCount_{tag} := iHealthyCount_{tag} - 1; END_IF;")
        lines.append("")
        lines.append(f"(* Graceful TMR Voting Degradation Matrix for {tag} *)")
        lines.append(f"IF iHealthyCount_{tag} = 3 THEN")
        lines.append(f"    (* Nominal 2oo3 Mid-Value Selection *)")
        lines.append(f"    IF ({chA} >= {chB} AND {chA} <= {chC}) OR ({chA} <= {chB} AND {chA} >= {chC}) THEN")
        lines.append(f"        {votedVar} := {chA};")
        lines.append(f"    ELSIF ({chB} >= {chA} AND {chB} <= {chC}) OR ({chB} <= {chA} AND {chB} >= {chC}) THEN")
        lines.append(f"        {votedVar} := {chB};")
        lines.append("    ELSE")
        lines.append(f"        {votedVar} := {chC};")
        lines.append("    END_IF;")
        lines.append(f"ELSIF iHealthyCount_{tag} = 2 THEN")
        lines.append("    (* Degraded 1oo2 Mean Selection *)")
        lines.append(f"    IF bFault_{tag}_A THEN")
        lines.append(f"        {votedVar} := ({chB} + {chC}) * 0.50;")
        lines.append(f"    ELSIF bFault_{tag}_B THEN")
        lines.append(f"        {votedVar} := ({chA} + {chC}) * 0.50;")
        lines.append("    ELSE")
        lines.append(f"        {votedVar} := ({chA} + {chB}) * 0.50;")
        lines.append("    END_IF;")
        lines.append(f"ELSIF iHealthyCount_{tag} = 1 THEN")
        lines.append("    (* Degraded 1oo1 Single-Channel Operation *)")
        lines.append(f"    IF NOT bFault_{tag}_A THEN {votedVar} := {chA};")
        lines.append(f"    ELSIF NOT bFault_{tag}_B THEN {votedVar} := {chB};")
        lines.append(f"    ELSE {votedVar} := {chC};")
        lines.append("    END_IF;")
        lines.append("ELSE")
        lines.append("    (* Fail-Safe Hold Default Value on Complete Sensor Triplet Loss *)")
        lines.append(f"    {votedVar} := {votedVar};")
        lines.append("END_IF;")
        lines.append("")

    lines.append("(* Update Master TMR Degraded Mode Indicator *)")
    lines.append("bTMRSensorDegradedMode := (iHealthyCount_PT101 < 3) OR (iHealthyCount_PT102 < 3) OR ")
    lines.append("                          (iHealthyCount_TT201 < 3) OR (iHealthyCount_FT301 < 3) OR ")
    lines.append("                          (iHealthyCount_DT401 < 3) OR (iHealthyCount_PT501 < 3) OR ")
    lines.append("                          (iHealthyCount_FT601 < 3) OR (iHealthyCount_ZT701 < 3);")
    lines.append("")
    return "\n".join(lines)

def build_section_hydrodynamics():
    lines = []
    lines.append("(* =========================================================================================== *)")
    lines.append("(* 3.0 PHASE 2: HYDRODYNAMICS, DRIFT-FLUX SLUGGING OBSERVER, HYDRATE & CAVITATION METRICS    *)")
    lines.append("(* =========================================================================================== *)")
    lines.append("(* 3.1 Choke Differential Pressure Drop *)")
    lines.append("rChokePressureDrop_bar := rVotedWellheadPressure_bar - rVotedChokeDownstreamPressure_bar;")
    lines.append("IF rChokePressureDrop_bar < 0.0 THEN")
    lines.append("    rChokePressureDrop_bar := 0.0; (* Non-physical reverse pressure clamping *)")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* 3.2 In-Situ Mixture Bulk Density & Gas Volume Fraction (GVF) *)")
    lines.append("(* Derived from Fast Gamma-Ray Densitometer DT_401 *)")
    lines.append("IF rVotedSlugDensity_kgm3 > c_OilCondensateDensity_kgm3 THEN")
    lines.append("    rCalculatedGasVolumeFraction_GVF := 0.02; (* Pure heavy liquid slug body *)")
    lines.append("ELSIF rVotedSlugDensity_kgm3 < c_GasDensityStandard_kgm3 THEN")
    lines.append("    rCalculatedGasVolumeFraction_GVF := 0.98; (* Pure gas Taylor bubble pocket *)")
    lines.append("ELSE")
    lines.append("    rCalculatedGasVolumeFraction_GVF := (c_OilCondensateDensity_kgm3 - rVotedSlugDensity_kgm3) / ")
    lines.append("                                        (c_OilCondensateDensity_kgm3 - c_GasDensityStandard_kgm3);")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* Clamping GVF between physical limits 0.01 and 0.99 *)")
    lines.append("IF rCalculatedGasVolumeFraction_GVF < 0.01 THEN")
    lines.append("    rCalculatedGasVolumeFraction_GVF := 0.01;")
    lines.append("ELSIF rCalculatedGasVolumeFraction_GVF > 0.99 THEN")
    lines.append("    rCalculatedGasVolumeFraction_GVF := 0.99;")
    lines.append("END_IF;")
    lines.append("rEstimatedLiquidHoldup := 1.00 - rCalculatedGasVolumeFraction_GVF;")
    lines.append("")
    lines.append("(* 3.3 Hydrodynamic Drift-Flux Mixture Velocities (Zuber-Findlay Formulation) *)")
    lines.append("(* Superficial velocities: U_m = m_dot / (rho_mix * A_pipe) *)")
    lines.append("IF rVotedSlugDensity_kgm3 > 10.0 AND rPipeCrossSectionArea_m2 > 0.001 THEN")
    lines.append("    rMixtureVelocity_ms := rVotedWetGasFlow_kgs / (rVotedSlugDensity_kgm3 * rPipeCrossSectionArea_m2);")
    lines.append("ELSE")
    lines.append("    rMixtureVelocity_ms := 0.50;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("rGasSuperficialVelocity_ms := rMixtureVelocity_ms * rCalculatedGasVolumeFraction_GVF;")
    lines.append("rLiquidSuperficialVelocity_ms := rMixtureVelocity_ms * rEstimatedLiquidHoldup;")
    lines.append("rDriftVelocity_ms := 1.53 * 0.245; (* Constant bubble terminal rise drift velocity [m/s] *)")
    lines.append("")
    lines.append("(* 3.4 Slugging Severity Index (SSI) Calculation via Choke Delta-P Variance *)")
    lines.append("rSluggingPressureBuffer[iSlugBufferIndex] := rChokePressureDrop_bar;")
    lines.append("iSlugBufferIndex := iSlugBufferIndex + 1;")
    lines.append("IF iSlugBufferIndex > 10 THEN")
    lines.append("    iSlugBufferIndex := 1;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* Calculate Moving Average of Choke Delta-P *)")
    lines.append("rMeanChokeDeltaP_bar := (rSluggingPressureBuffer[1] + rSluggingPressureBuffer[2] + ")
    lines.append("                        rSluggingPressureBuffer[3] + rSluggingPressureBuffer[4] + ")
    lines.append("                        rSluggingPressureBuffer[5] + rSluggingPressureBuffer[6] + ")
    lines.append("                        rSluggingPressureBuffer[7] + rSluggingPressureBuffer[8] + ")
    lines.append("                        rSluggingPressureBuffer[9] + rSluggingPressureBuffer[10]) * 0.10;")
    lines.append("")
    lines.append("(* Calculate Variance & Standard Deviation *)")
    lines.append("rVarianceSumChokeDeltaP := ((rSluggingPressureBuffer[1] - rMeanChokeDeltaP_bar) * (rSluggingPressureBuffer[1] - rMeanChokeDeltaP_bar) +")
    lines.append("                           (rSluggingPressureBuffer[2] - rMeanChokeDeltaP_bar) * (rSluggingPressureBuffer[2] - rMeanChokeDeltaP_bar) +")
    lines.append("                           (rSluggingPressureBuffer[3] - rMeanChokeDeltaP_bar) * (rSluggingPressureBuffer[3] - rMeanChokeDeltaP_bar) +")
    lines.append("                           (rSluggingPressureBuffer[4] - rMeanChokeDeltaP_bar) * (rSluggingPressureBuffer[4] - rMeanChokeDeltaP_bar) +")
    lines.append("                           (rSluggingPressureBuffer[5] - rMeanChokeDeltaP_bar) * (rSluggingPressureBuffer[5] - rMeanChokeDeltaP_bar) +")
    lines.append("                           (rSluggingPressureBuffer[6] - rMeanChokeDeltaP_bar) * (rSluggingPressureBuffer[6] - rMeanChokeDeltaP_bar) +")
    lines.append("                           (rSluggingPressureBuffer[7] - rMeanChokeDeltaP_bar) * (rSluggingPressureBuffer[7] - rMeanChokeDeltaP_bar) +")
    lines.append("                           (rSluggingPressureBuffer[8] - rMeanChokeDeltaP_bar) * (rSluggingPressureBuffer[8] - rMeanChokeDeltaP_bar) +")
    lines.append("                           (rSluggingPressureBuffer[9] - rMeanChokeDeltaP_bar) * (rSluggingPressureBuffer[9] - rMeanChokeDeltaP_bar) +")
    lines.append("                           (rSluggingPressureBuffer[10] - rMeanChokeDeltaP_bar) * (rSluggingPressureBuffer[10] - rMeanChokeDeltaP_bar)) * 0.10;")
    lines.append("")
    lines.append("IF rVarianceSumChokeDeltaP > 0.0001 THEN")
    lines.append("    rStandardDeviationDeltaP := SQRT(rVarianceSumChokeDeltaP);")
    lines.append("ELSE")
    lines.append("    rStandardDeviationDeltaP := 0.0;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("IF rMeanChokeDeltaP_bar > 1.0 THEN")
    lines.append("    rSluggingSeverityIndex := (rStandardDeviationDeltaP / rMeanChokeDeltaP_bar) * 100.0;")
    lines.append("ELSE")
    lines.append("    rSluggingSeverityIndex := 0.0;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* 3.5 Thermodynamic Hydrate Equilibrium Boundary (Towler-Mokhatab Correlation) *)")
    lines.append("(* T_eq = 13.385 * ln(P_bar) - 43.125 [deg C] *)")
    lines.append("(* Natural logarithm Taylor approximation around nominal 100 bar *)")
    lines.append("IF rVotedChokeDownstreamPressure_bar > 10.0 THEN")
    lines.append("    rNormalizedPressureArg := (rVotedChokeDownstreamPressure_bar - 100.0) / 100.0;")
    lines.append("    rTaylorSeriesLogTerm := 4.60517 + rNormalizedPressureArg - ")
    lines.append("                            0.50 * rNormalizedPressureArg * rNormalizedPressureArg + ")
    lines.append("                            0.3333 * rNormalizedPressureArg * rNormalizedPressureArg * rNormalizedPressureArg;")
    lines.append("    rHydrateEquilibriumTemp_degC := 13.385 * rTaylorSeriesLogTerm - 43.125;")
    lines.append("ELSE")
    lines.append("    rHydrateEquilibriumTemp_degC := -15.0; (* Pressure too low for stable hydrate envelope *)")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* Subcooling Thermal Margin: Delta_T_sub = T_fluid - T_eq *)")
    lines.append("rHydrateSubcoolingMargin_degC := rVotedWellheadTemp_degC - rHydrateEquilibriumTemp_degC;")
    lines.append("")
    lines.append("(* Dynamic Monoethylene Glycol (MEG) Dosing Calculation (Nielsen-Hammerschmidt) *)")
    lines.append("IF rHydrateSubcoolingMargin_degC < rMinHydrateMargin_degC THEN")
    lines.append("    rRequiredHydrateDepression_degC := (rMinHydrateMargin_degC - rHydrateSubcoolingMargin_degC) + 3.0;")
    lines.append("    (* Target MEG wt% = (100 * M_meg * Delta_T) / (K_H + M_meg * Delta_T) *)")
    lines.append("    rTargetMegConcentration_wtPct := (100.0 * c_MegMolarMass_gmol * rRequiredHydrateDepression_degC) / ")
    lines.append("                                    (c_HammerschmidtConstant + c_MegMolarMass_gmol * rRequiredHydrateDepression_degC);")
    lines.append("    IF rTargetMegConcentration_wtPct > 80.0 THEN rTargetMegConcentration_wtPct := 80.0; END_IF;")
    lines.append("    IF rTargetMegConcentration_wtPct < 15.0 THEN rTargetMegConcentration_wtPct := 15.0; END_IF;")
    lines.append("    ")
    lines.append("    rWaterMassFlowRate_kgh := rVotedWetGasFlow_kgs * 3600.0 * rEstimatedWaterCutFraction;")
    lines.append("    rStoichiometricMegDemand_Lh := (rWaterMassFlowRate_kgh * (rTargetMegConcentration_wtPct / (100.0 - rTargetMegConcentration_wtPct))) / ")
    lines.append("                                   (c_PureMegDensity_kgm3 * 0.001);")
    lines.append("    IF rStoichiometricMegDemand_Lh > 850.0 THEN rStoichiometricMegDemand_Lh := 850.0; END_IF;")
    lines.append("    rMegInjectionRateDemand_Lh := rStoichiometricMegDemand_Lh;")
    lines.append("    rCalculatedMegConcentration_wtPct := rTargetMegConcentration_wtPct;")
    lines.append("ELSE")
    lines.append("    rMegInjectionRateDemand_Lh := 15.0; (* Baseline continuous trickle dose [L/h] *)")
    lines.append("    rCalculatedMegConcentration_wtPct := 5.0;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* 3.6 Subsea Multiphase Booster Pump NPSH & Cavitation Tracking *)")
    lines.append("IF rVotedSlugDensity_kgm3 > 50.0 THEN")
    lines.append("    rPumpSuctionSpecificHead_m := (rBoosterPumpSuctionPressure_bar * 100000.0) / (rVotedSlugDensity_kgm3 * c_GravitationalAccel_ms2);")
    lines.append("    rPumpVaporSpecificHead_m := (rFluidVaporPressure_bar * 100000.0) / (rVotedSlugDensity_kgm3 * c_GravitationalAccel_ms2);")
    lines.append("    rPumpSuctionDynamicVelocityHead_m := (rMixtureVelocity_ms * rMixtureVelocity_ms) / (2.0 * c_GravitationalAccel_ms2);")
    lines.append("    rCalculatedNpsha_m := rPumpSuctionSpecificHead_m - rPumpVaporSpecificHead_m + rPumpSuctionDynamicVelocityHead_m;")
    lines.append("ELSE")
    lines.append("    rCalculatedNpsha_m := 10.0;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* NPSHR increases with square of pump rotational speed *)")
    lines.append("rCalculatedNpshr_m := (rBoosterPumpMinNpshReq_bar * 100000.0) / (850.0 * c_GravitationalAccel_ms2) * ")
    lines.append("                      ((rBoosterPumpActualRPM / 2400.0) * (rBoosterPumpActualRPM / 2400.0));")
    lines.append("rNpshMarginHead_m := rCalculatedNpsha_m - rCalculatedNpshr_m;")
    lines.append("rBoosterPumpNPSHMargin_bar := (rNpshMarginHead_m * rVotedSlugDensity_kgm3 * c_GravitationalAccel_ms2) * 0.00001;")
    lines.append("")
    lines.append("(* Pump Speed De-Rating if Approaching Vapor Lock or Cavitation *)")
    lines.append("IF rBoosterPumpNPSHMargin_bar < 1.50 THEN")
    lines.append("    rPumpSpeedDerateFactor := rBoosterPumpNPSHMargin_bar / 1.50;")
    lines.append("    IF rPumpSpeedDerateFactor < 0.25 THEN rPumpSpeedDerateFactor := 0.25; END_IF;")
    lines.append("    bPumpCavitationMitigationActive := TRUE;")
    lines.append("ELSE")
    lines.append("    rPumpSpeedDerateFactor := 1.00;")
    lines.append("    bPumpCavitationMitigationActive := FALSE;")
    lines.append("END_IF;")
    lines.append("")
    return "\n".join(lines)

def build_section_mpc():
    lines = []
    lines.append("(* =========================================================================================== *)")
    lines.append("(* 4.0 PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) ANTI-SLUG SOLVER              *)")
    lines.append("(* =========================================================================================== *)")
    lines.append("(* 4.1 State Vector Assembly & Reference Setpoint Trajectory *)")
    lines.append("xState[1] := rVotedWellheadPressure_bar - 320.0;        (* State x1: Wellhead pressure deviation *)")
    lines.append("xState[2] := rVotedChokeDownstreamPressure_bar - rTargetManifoldPressure_bar; (* State x2: Downstream pressure deviation *)")
    lines.append("xState[3] := rEstimatedLiquidHoldup * 0.45;             (* State x3: Liquid slug holdup volume *)")
    lines.append("xState[4] := rVotedWetGasFlow_kgs - rTargetProductionRate_kgs; (* State x4: Mixture mass flow error *)")
    lines.append("xState[5] := rVotedWellheadTemp_degC - 45.0;            (* State x5: Temperature deviation *)")
    lines.append("xState[6] := rCalculatedMegConcentration_wtPct - rTargetMegConcentration_wtPct; (* State x6: Glycol concentration error *)")
    lines.append("xState[7] := (rBoosterPumpSuctionPressure_bar * 0.25);  (* State x7: Booster pump differential head *)")
    lines.append("xState[8] := PT_HYDRAULIC_HPU_HP_bar - 480.0;           (* State x8: SCM hydraulic pilot pressure *)")
    lines.append("")
    lines.append("FOR kState := 1 TO 8 DO")
    lines.append("    xSetpoint[kState] := 0.0; (* Regulate all deviations toward zero nominal equilibrium *)")
    lines.append("    xTrackingError[kState] := xState[kState] - xSetpoint[kState];")
    lines.append("END_FOR;")
    lines.append("")
    lines.append("(* 4.2 State-Space One-Step Prediction (x[k+1] = A*x[k] + B*u[k]) *)")
    lines.append("FOR iRow := 1 TO 8 DO")
    lines.append("    xNextState[iRow] := 0.0;")
    lines.append("    FOR jCol := 1 TO 8 DO")
    lines.append("        xNextState[iRow] := xNextState[iRow] + matA[iRow, jCol] * xState[jCol];")
    lines.append("    END_FOR;")
    lines.append("    FOR mInput := 1 TO 4 DO")
    lines.append("        xNextState[iRow] := xNextState[iRow] + matB[iRow, mInput] * uActuator[mInput];")
    lines.append("    END_FOR;")
    lines.append("END_FOR;")
    lines.append("")
    lines.append("(* 4.3 Receding Horizon Prediction Trajectory (Np = 4 Steps) *)")
    lines.append("FOR kState := 1 TO 8 DO")
    lines.append("    xPredictedHorizon[1, kState] := xNextState[kState];")
    lines.append("END_FOR;")
    lines.append("")
    lines.append("FOR iHorizonStep := 2 TO 4 DO")
    lines.append("    FOR iRow := 1 TO 8 DO")
    lines.append("        xPredictedHorizon[iHorizonStep, iRow] := 0.0;")
    lines.append("        FOR jCol := 1 TO 8 DO")
    lines.append("            xPredictedHorizon[iHorizonStep, iRow] := xPredictedHorizon[iHorizonStep, iRow] + ")
    lines.append("                                                    matA[iRow, jCol] * xPredictedHorizon[iHorizonStep - 1, jCol];")
    lines.append("        END_FOR;")
    lines.append("        FOR mInput := 1 TO 4 DO")
    lines.append("            xPredictedHorizon[iHorizonStep, iRow] := xPredictedHorizon[iHorizonStep, iRow] + ")
    lines.append("                                                    matB[iRow, mInput] * uActuator[mInput];")
    lines.append("        END_FOR;")
    lines.append("    END_FOR;")
    lines.append("END_FOR;")
    lines.append("")
    lines.append("(* 4.4 Quadratic Cost Function Evaluation (J = x' Q x + u' R u + x_N' P x_N) *)")
    lines.append("rStateCostAccumulator := 0.0;")
    lines.append("FOR iHorizonStep := 1 TO 3 DO")
    lines.append("    FOR kState := 1 TO 8 DO")
    lines.append("        rStateCostAccumulator := rStateCostAccumulator + ")
    lines.append("                                 xPredictedHorizon[iHorizonStep, kState] * matQ[kState, kState] * xPredictedHorizon[iHorizonStep, kState];")
    lines.append("    END_FOR;")
    lines.append("END_FOR;")
    lines.append("")
    lines.append("rActuatorCostAccumulator := 0.0;")
    lines.append("FOR mInput := 1 TO 4 DO")
    lines.append("    rActuatorCostAccumulator := rActuatorCostAccumulator + uActuator[mInput] * matR[mInput, mInput] * uActuator[mInput];")
    lines.append("END_FOR;")
    lines.append("")
    lines.append("(* Terminal Lyapunov Penalty *)")
    lines.append("FOR kState := 1 TO 8 DO")
    lines.append("    rStateCostAccumulator := rStateCostAccumulator + ")
    lines.append("                             xPredictedHorizon[4, kState] * matP[kState, kState] * xPredictedHorizon[4, kState];")
    lines.append("END_FOR;")
    lines.append("rMpcObjectiveCostJ := rStateCostAccumulator + rActuatorCostAccumulator;")
    lines.append("")
    lines.append("(* 4.5 Active-Set Projected Gradient Descent Optimization (3 Iterations) *)")
    lines.append("IF bMpcAntiSlugActive AND (eCurrentState = 70 OR eCurrentState = 80) THEN")
    lines.append("    FOR iMpcIteration := 1 TO 3 DO")
    lines.append("        (* Evaluate Cost Gradient w.r.t Controls: grad_J = 2 * B' Q (x_pred - r) + 2 * R u *)")
    lines.append("        FOR mInput := 1 TO 4 DO")
    lines.append("            rMpcGradient[mInput] := 2.0 * matR[mInput, mInput] * uActuator[mInput];")
    lines.append("            FOR kState := 1 TO 8 DO")
    lines.append("                rMpcGradient[mInput] := rMpcGradient[mInput] + ")
    lines.append("                                        2.0 * matB[kState, mInput] * matQ[kState, kState] * xPredictedHorizon[1, kState];")
    lines.append("            END_FOR;")
    lines.append("            ")
    lines.append("            (* Projected Gradient Step *)")
    lines.append("            uActuator[mInput] := uActuator[mInput] - rMpcStepSize * rMpcGradient[mInput];")
    lines.append("            ")
    lines.append("            (* Slew Rate Clamping *)")
    lines.append("            IF (uActuator[mInput] - uPrevious[mInput]) > deltaUMaxLimit[mInput] THEN")
    lines.append("                uActuator[mInput] := uPrevious[mInput] + deltaUMaxLimit[mInput];")
    lines.append("            ELSIF (uActuator[mInput] - uPrevious[mInput]) < -deltaUMaxLimit[mInput] THEN")
    lines.append("                uActuator[mInput] := uPrevious[mInput] - deltaUMaxLimit[mInput];")
    lines.append("            END_IF;")
    lines.append("            ")
    lines.append("            (* Box Actuator Bound Projection *)")
    lines.append("            IF uActuator[mInput] < uLowerLimit[mInput] THEN")
    lines.append("                uActuator[mInput] := uLowerLimit[mInput];")
    lines.append("            ELSIF uActuator[mInput] > uUpperLimit[mInput] THEN")
    lines.append("                uActuator[mInput] := uUpperLimit[mInput];")
    lines.append("            END_IF;")
    lines.append("        END_FOR;")
    lines.append("    END_FOR;")
    lines.append("    ")
    lines.append("    (* Store History *)")
    lines.append("    FOR mInput := 1 TO 4 DO")
    lines.append("        uPrevious[mInput] := uActuator[mInput];")
    lines.append("    END_FOR;")
    lines.append("    ")
    lines.append("    (* Actuator Mapping *)")
    lines.append("    rChokePositionDemand_pct := uActuator[1];")
    lines.append("    rBoosterPumpSpeedDemand_RPM := uActuator[2] * rPumpSpeedDerateFactor;")
    lines.append("    bActiveSluggingMitigationActive := TRUE;")
    lines.append("ELSE")
    lines.append("    (* Default Manual or Fixed Baseline Actuator Settings *)")
    lines.append("    IF NOT bMpcAntiSlugActive THEN")
    lines.append("        bActiveSluggingMitigationActive := FALSE;")
    lines.append("    END_IF;")
    lines.append("END_IF;")
    lines.append("")
    return "\n".join(lines)

def build_section_fsm():
    lines = []
    lines.append("(* =========================================================================================== *)")
    lines.append("(* 5.0 PHASE 4: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                               *)")
    lines.append("(* =========================================================================================== *)")
    lines.append("(* Execution of the 12 subsea production states with strict transition permissives:          *)")
    lines.append("(* 10: SYSTEM_COLD_HIBERNATION                                                                *)")
    lines.append("(* 20: HYDRAULIC_HPU_ACCUMULATOR_CHARGE                                                       *)")
    lines.append("(* 30: MEG_INJECTION_LINE_PRIME                                                               *)")
    lines.append("(* 40: WELLHEAD_MANDREL_UNLATCH_CHECK                                                         *)")
    lines.append("(* 50: CHOKE_CRACKING_WARMUP                                                                  *)")
    lines.append("(* 60: SLUG_OBSERVER_CALIBRATION                                                              *)")
    lines.append("(* 70: STEADY_STATE_MULTITANK_PRODUCTION                                                      *)")
    lines.append("(* 80: ACTIVE_SLUG_DAMPING_REGIME                                                             *)")
    lines.append("(* 90: HYDRATE_RISK_MEG_SURGE_BOOST                                                           *)")
    lines.append("(* 100: BOOSTER_PUMP_TRIP_DECOUPLING                                                          *)")
    lines.append("(* 110: HIPPS_OVERPRESSURE_EMERGENCY_SHUTDOWN                                                 *)")
    lines.append("(* 120: CONTROLLED_WELL_ISOLATION                                                             *)")
    lines.append("")
    lines.append("CASE eCurrentState OF")
    
    # State 10
    lines.append("    10: (* SYSTEM_COLD_HIBERNATION *)")
    lines.append("        bSystemReady := FALSE;")
    lines.append("        bSystemRunning := FALSE;")
    lines.append("        bHippsValve1_TripClose := TRUE; (* De-energized fail-safe closed *)")
    lines.append("        bHippsValve2_TripClose := TRUE; (* De-energized fail-safe closed *)")
    lines.append("        bSubseaHydraulicDumpValve_cmd := FALSE;")
    lines.append("        bWellheadMasterWingValve_Close := TRUE;")
    lines.append("        rChokePositionDemand_pct := 0.0;")
    lines.append("        rBoosterPumpSpeedDemand_RPM := 0.0;")
    lines.append("        rMegInjectionRateDemand_Lh := 0.0;")
    lines.append("        ")
    lines.append("        IF bEnableSystem AND bEmergencyShutdown_ESD AND (PT_HYDRAULIC_HPU_HP_bar > c_Limit_HpuSupplyPress_L_bar) THEN")
    lines.append("            eCurrentState := 20; (* Advance to Hydraulic Accumulator Charge *)")
    lines.append("        END_IF;")

    # State 20
    lines.append("    20: (* HYDRAULIC_HPU_ACCUMULATOR_CHARGE *)")
    lines.append("        bSystemReady := FALSE;")
    lines.append("        bSystemRunning := FALSE;")
    lines.append("        bHippsValve1_TripClose := TRUE;")
    lines.append("        bHippsValve2_TripClose := TRUE;")
    lines.append("        bWellheadMasterWingValve_Close := TRUE;")
    lines.append("        rChokePositionDemand_pct := 0.0;")
    lines.append("        ")
    lines.append("        tHydraulicAccumulatorTimer(IN := (PT_HYDRAULIC_HPU_HP_bar > 450.0), PT := T#5S);")
    lines.append("        IF tHydraulicAccumulatorTimer.Q THEN")
    lines.append("            tHydraulicAccumulatorTimer(IN := FALSE, PT := T#5S);")
    lines.append("            eCurrentState := 30; (* Advance to MEG Line Prime *)")
    lines.append("        END_IF;")
    lines.append("        IF NOT bEmergencyShutdown_ESD THEN eCurrentState := 110; END_IF;")

    # State 30
    lines.append("    30: (* MEG_INJECTION_LINE_PRIME *)")
    lines.append("        bSystemReady := FALSE;")
    lines.append("        bSystemRunning := FALSE;")
    lines.append("        rMegInjectionRateDemand_Lh := 120.0; (* Prime and flush umbilical CIMV header [L/h] *)")
    lines.append("        ")
    lines.append("        tMegLinePrimeTimer(IN := (rVotedMegFlow_Lh > 90.0), PT := T#4S);")
    lines.append("        IF tMegLinePrimeTimer.Q THEN")
    lines.append("            tMegLinePrimeTimer(IN := FALSE, PT := T#4S);")
    lines.append("            eCurrentState := 40; (* Advance to Wellhead Mandrel Check *)")
    lines.append("        END_IF;")
    lines.append("        IF NOT bEmergencyShutdown_ESD THEN eCurrentState := 110; END_IF;")

    # State 40
    lines.append("    40: (* WELLHEAD_MANDREL_UNLATCH_CHECK *)")
    lines.append("        bSystemReady := TRUE;")
    lines.append("        bSystemRunning := FALSE;")
    lines.append("        bHippsValve1_TripClose := FALSE; (* Energize open HIPPS-XV-101 *)")
    lines.append("        bHippsValve2_TripClose := FALSE; (* Energize open HIPPS-XV-102 *)")
    lines.append("        ")
    lines.append("        tWellheadUnlatchTimer(IN := (rVotedHippsPressure_bar < c_Limit_HippsTrip_HH_bar), PT := T#3S);")
    lines.append("        IF tWellheadUnlatchTimer.Q THEN")
    lines.append("            tWellheadUnlatchTimer(IN := FALSE, PT := T#3S);")
    lines.append("            bWellheadMasterWingValve_Close := FALSE; (* Open tree wing valve *)")
    lines.append("            eCurrentState := 50; (* Advance to Choke Cracking Warmup *)")
    lines.append("        END_IF;")
    lines.append("        IF NOT bEmergencyShutdown_ESD THEN eCurrentState := 110; END_IF;")

    # State 50
    lines.append("    50: (* CHOKE_CRACKING_WARMUP *)")
    lines.append("        bSystemReady := TRUE;")
    lines.append("        bSystemRunning := TRUE;")
    lines.append("        rChokeTargetPosition_pct := 8.0; (* Crack choke to 8% to induce gentle well warmup *)")
    lines.append("        rChokePositionDemand_pct := rChokeTargetPosition_pct;")
    lines.append("        rMegInjectionRateDemand_Lh := 85.0; (* High MEG rate during cold fluid startup *)")
    lines.append("        ")
    lines.append("        tChokeWarmupRampTimer(IN := (rVotedWellheadTemp_degC > 18.0), PT := T#6S);")
    lines.append("        IF tChokeWarmupRampTimer.Q THEN")
    lines.append("            tChokeWarmupRampTimer(IN := FALSE, PT := T#6S);")
    lines.append("            eCurrentState := 60; (* Advance to Slug Observer Calibration *)")
    lines.append("        END_IF;")
    lines.append("        IF rVotedChokeDownstreamPressure_bar > c_Limit_HippsTrip_HH_bar THEN eCurrentState := 110; END_IF;")
    lines.append("        IF NOT bEmergencyShutdown_ESD THEN eCurrentState := 110; END_IF;")

    # State 60
    lines.append("    60: (* SLUG_OBSERVER_CALIBRATION *)")
    lines.append("        bSystemReady := TRUE;")
    lines.append("        bSystemRunning := TRUE;")
    lines.append("        rChokePositionDemand_pct := 22.0;")
    lines.append("        IF bBoosterPumpEnable THEN rBoosterPumpSpeedDemand_RPM := 1200.0; END_IF;")
    lines.append("        ")
    lines.append("        tSlugStabilizationTimer(IN := (rSluggingSeverityIndex < 15.0), PT := T#5S);")
    lines.append("        IF tSlugStabilizationTimer.Q THEN")
    lines.append("            tSlugStabilizationTimer(IN := FALSE, PT := T#5S);")
    lines.append("            eCurrentState := 70; (* Advance to Steady State Production *)")
    lines.append("        END_IF;")
    lines.append("        IF rSluggingSeverityIndex > c_Limit_SlugSeverity_H_pct THEN eCurrentState := 80; END_IF;")
    lines.append("        IF rVotedChokeDownstreamPressure_bar > c_Limit_HippsTrip_HH_bar THEN eCurrentState := 110; END_IF;")
    lines.append("        IF NOT bEmergencyShutdown_ESD THEN eCurrentState := 110; END_IF;")

    # State 70
    lines.append("    70: (* STEADY_STATE_MULTITANK_PRODUCTION *)")
    lines.append("        bSystemReady := TRUE;")
    lines.append("        bSystemRunning := TRUE;")
    lines.append("        (* Baseline nominal production tracking commanded via MPC or fixed stroke *)")
    lines.append("        IF NOT bMpcAntiSlugActive THEN")
    lines.append("            rChokePositionDemand_pct := 45.0;")
    lines.append("            IF bBoosterPumpEnable THEN rBoosterPumpSpeedDemand_RPM := 2400.0 * rPumpSpeedDerateFactor; END_IF;")
    lines.append("        END_IF;")
    lines.append("        ")
    lines.append("        IF rSluggingSeverityIndex > c_Limit_SlugSeverity_H_pct THEN")
    lines.append("            eCurrentState := 80; (* Transition to Active Slug Damping *)")
    lines.append("        ELSIF rHydrateSubcoolingMargin_degC < 2.0 THEN")
    lines.append("            eCurrentState := 90; (* Transition to Hydrate Risk Surge Boost *)")
    lines.append("        ELSIF rBoosterPumpVibrationRMS_mms > c_Limit_PumpVibration_HH_mms THEN")
    lines.append("            eCurrentState := 100; (* Transition to Booster Pump Trip Decoupling *)")
    lines.append("        END_IF;")
    lines.append("        IF rVotedChokeDownstreamPressure_bar > c_Limit_HippsTrip_HH_bar THEN eCurrentState := 110; END_IF;")
    lines.append("        IF NOT bEmergencyShutdown_ESD THEN eCurrentState := 110; END_IF;")

    # State 80
    lines.append("    80: (* ACTIVE_SLUG_DAMPING_REGIME *)")
    lines.append("        bSystemReady := TRUE;")
    lines.append("        bSystemRunning := TRUE;")
    lines.append("        bActiveSluggingMitigationActive := TRUE;")
    lines.append("        (* Dynamic MPC actively modulates choke position and booster pump speed *)")
    lines.append("        (* When severe slug hits, throttle choke rapidly to build backpressure *)")
    lines.append("        IF rEstimatedLiquidHoldup > 0.65 THEN")
    lines.append("            rChokePositionDemand_pct := rChokePositionDemand_pct * 0.75; (* Fast choke cutback *)")
    lines.append("        END_IF;")
    lines.append("        ")
    lines.append("        IF rSluggingSeverityIndex < 12.0 THEN")
    lines.append("            eCurrentState := 70; (* Slugging successfully mitigated, return to Steady State *)")
    lines.append("        ELSIF rHydrateSubcoolingMargin_degC < 1.0 THEN")
    lines.append("            eCurrentState := 90; (* Hydrate risk escalated *)")
    lines.append("        END_IF;")
    lines.append("        IF rVotedChokeDownstreamPressure_bar > c_Limit_HippsTrip_HH_bar THEN eCurrentState := 110; END_IF;")
    lines.append("        IF NOT bEmergencyShutdown_ESD THEN eCurrentState := 110; END_IF;")

    # State 90
    lines.append("    90: (* HYDRATE_RISK_MEG_SURGE_BOOST *)")
    lines.append("        bSystemReady := TRUE;")
    lines.append("        bSystemRunning := TRUE;")
    lines.append("        bHydrateInhibitionWarning := TRUE;")
    lines.append("        rMegInjectionRateDemand_Lh := 450.0; (* Immediate maximum inhibitor surge dump *)")
    lines.append("        rChokePositionDemand_pct := rChokePositionDemand_pct * 0.85; (* Mild backpressure increase *)")
    lines.append("        ")
    lines.append("        IF rHydrateSubcoolingMargin_degC > rMinHydrateMargin_degC + 2.0 THEN")
    lines.append("            bHydrateInhibitionWarning := FALSE;")
    lines.append("            eCurrentState := 70; (* Hydrate envelope cleared *)")
    lines.append("        END_IF;")
    lines.append("        IF rVotedChokeDownstreamPressure_bar > c_Limit_HippsTrip_HH_bar THEN eCurrentState := 110; END_IF;")
    lines.append("        IF NOT bEmergencyShutdown_ESD THEN eCurrentState := 110; END_IF;")

    # State 100
    lines.append("    100: (* BOOSTER_PUMP_TRIP_DECOUPLING *)")
    lines.append("        bSystemReady := TRUE;")
    lines.append("        bSystemRunning := TRUE;")
    lines.append("        rBoosterPumpSpeedDemand_RPM := 0.0; (* Trip booster pump immediately *)")
    lines.append("        (* Open choke to compensate for loss of booster pump suction head *)")
    lines.append("        rChokePositionDemand_pct := rChokePositionDemand_pct * 1.15;")
    lines.append("        IF rChokePositionDemand_pct > 80.0 THEN rChokePositionDemand_pct := 80.0; END_IF;")
    lines.append("        ")
    lines.append("        IF rBoosterPumpVibrationRMS_mms < c_Limit_PumpVibration_H_mms AND bBoosterPumpEnable THEN")
    lines.append("            eCurrentState := 70;")
    lines.append("        END_IF;")
    lines.append("        IF rVotedChokeDownstreamPressure_bar > c_Limit_HippsTrip_HH_bar THEN eCurrentState := 110; END_IF;")
    lines.append("        IF NOT bEmergencyShutdown_ESD THEN eCurrentState := 110; END_IF;")

    # State 110
    lines.append("    110: (* HIPPS_OVERPRESSURE_EMERGENCY_SHUTDOWN *)")
    lines.append("        bSystemReady := FALSE;")
    lines.append("        bSystemRunning := FALSE;")
    lines.append("        bHippsTripped := TRUE;")
    lines.append("        bHippsValve1_TripClose := TRUE; (* De-energize SIL-3 primary ball valve solenoid *)")
    lines.append("        bHippsValve2_TripClose := TRUE; (* De-energize SIL-3 secondary ball valve solenoid *)")
    lines.append("        bSubseaHydraulicDumpValve_cmd := TRUE; (* Dump fast actuator hydraulic accumulator *)")
    lines.append("        bWellheadMasterWingValve_Close := TRUE; (* Close production wing valve *)")
    lines.append("        rChokePositionDemand_pct := 0.0; (* Full choke closure *)")
    lines.append("        rBoosterPumpSpeedDemand_RPM := 0.0; (* Trip booster pump *)")
    lines.append("        rMegInjectionRateDemand_Lh := 0.0;")
    lines.append("        ")
    lines.append("        IF bResetFaults AND bEmergencyShutdown_ESD AND (rVotedChokeDownstreamPressure_bar < c_Limit_ManifoldPress_H_bar) THEN")
    lines.append("            bHippsTripped := FALSE;")
    lines.append("            eCurrentState := 120; (* Proceed to Controlled Well Isolation *)")
    lines.append("        END_IF;")

    # State 120
    lines.append("    120: (* CONTROLLED_WELL_ISOLATION *)")
    lines.append("        bSystemReady := FALSE;")
    lines.append("        bSystemRunning := FALSE;")
    lines.append("        bHippsValve1_TripClose := TRUE;")
    lines.append("        bHippsValve2_TripClose := TRUE;")
    lines.append("        bWellheadMasterWingValve_Close := TRUE;")
    lines.append("        rChokePositionDemand_pct := 0.0;")
    lines.append("        rBoosterPumpSpeedDemand_RPM := 0.0;")
    lines.append("        rMegInjectionRateDemand_Lh := 0.0;")
    lines.append("        ")
    lines.append("        IF bResetFaults AND bEnableSystem THEN")
    lines.append("            eCurrentState := 10; (* Return to Hibernation for restart *)")
    lines.append("        END_IF;")

    lines.append("END_CASE;")
    lines.append("")
    lines.append("(* Update Active FSM State Code Output *)")
    lines.append("eActiveFsmStateCode := eCurrentState;")
    lines.append("")
    return "\n".join(lines)

def build_section_alarms_and_stepping():
    lines = []
    lines.append("(* =========================================================================================== *)")
    lines.append("(* 6.0 PHASE 5: ISA-18.2 ALARMS, HIPPS TRIP LOGIC & DIAGNOSTIC WORD BIT PACKING               *)")
    lines.append("(* =========================================================================================== *)")
    lines.append("(* Reset Word Registers *)")
    lines.append("dwAlarmWord1_Trips := 16#0000_0000;")
    lines.append("dwAlarmWord2_ProcessAlarms := 16#0000_0000;")
    lines.append("dwWarningWord := 16#0000_0000;")
    lines.append("dwTMR_DegradationWord := 16#0000_0000;")
    lines.append("dwSystemStatusWord := 16#0000_0000;")
    lines.append("")
    lines.append("(* 6.1 Critical SIL-3 Trips (Packed into dwAlarmWord1_Trips) *)")
    lines.append("tTimer_HippsOverpressure(IN := (rVotedChokeDownstreamPressure_bar >= c_Limit_HippsTrip_HH_bar), PT := T#200MS);")
    lines.append("IF tTimer_HippsOverpressure.Q THEN")
    lines.append("    dwAlarmWord1_Trips := dwAlarmWord1_Trips OR 16#0000_0001; (* Bit 0: HIPPS Downstream Overpressure Trip *)")
    lines.append("    IF NOT bHippsBypassKeySwitch THEN eCurrentState := 110; END_IF;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("IF NOT bEmergencyShutdown_ESD THEN")
    lines.append("    dwAlarmWord1_Trips := dwAlarmWord1_Trips OR 16#0000_0002; (* Bit 1: Hardwired ESD Loop Open Trip *)")
    lines.append("    eCurrentState := 110;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("tTimer_WellheadOverpressure(IN := (rVotedWellheadPressure_bar >= c_Limit_WellheadPress_HH_bar), PT := T#500MS);")
    lines.append("IF tTimer_WellheadOverpressure.Q THEN")
    lines.append("    dwAlarmWord1_Trips := dwAlarmWord1_Trips OR 16#0000_0004; (* Bit 2: Tubing Head Extreme Overpressure Trip *)")
    lines.append("    eCurrentState := 110;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("IF bHippsManualTripCmd THEN")
    lines.append("    dwAlarmWord1_Trips := dwAlarmWord1_Trips OR 16#0000_0008; (* Bit 3: Operator Manual HIPPS Pushbutton Trip *)")
    lines.append("    eCurrentState := 110;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("tTimer_HpuPressureLoss(IN := (PT_HYDRAULIC_HPU_HP_bar <= c_Limit_HpuSupplyPress_LL_bar), PT := T#1S);")
    lines.append("IF tTimer_HpuPressureLoss.Q THEN")
    lines.append("    dwAlarmWord1_Trips := dwAlarmWord1_Trips OR 16#0000_0010; (* Bit 4: Umbilical HPU Hydraulic Pressure Loss Trip *)")
    lines.append("    eCurrentState := 110;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("tTimer_PumpVibrationTrip(IN := (rBoosterPumpVibrationRMS_mms >= c_Limit_PumpVibration_HH_mms), PT := T#500MS);")
    lines.append("IF tTimer_PumpVibrationTrip.Q THEN")
    lines.append("    dwAlarmWord1_Trips := dwAlarmWord1_Trips OR 16#0000_0020; (* Bit 5: Booster Pump Destructive Vibration Trip *)")
    lines.append("    IF eCurrentState = 70 OR eCurrentState = 80 THEN eCurrentState := 100; END_IF;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("tTimer_WellheadColdHypothermia(IN := (rVotedWellheadTemp_degC <= c_Limit_WellheadTemp_LL_degC), PT := T#2S);")
    lines.append("IF tTimer_WellheadColdHypothermia.Q THEN")
    lines.append("    dwAlarmWord1_Trips := dwAlarmWord1_Trips OR 16#0000_0040; (* Bit 6: Severe Fluid Hypothermia Freeze Hazard Trip *)")
    lines.append("    eCurrentState := 110;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("IF rVotedWetGasFlow_kgs >= c_Limit_WetGasFlow_HH_kgs THEN")
    lines.append("    dwAlarmWord1_Trips := dwAlarmWord1_Trips OR 16#0000_0080; (* Bit 7: Production Flow Erosion Velocity Trip *)")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* 6.2 Secondary Process Alarms (Packed into dwAlarmWord2_ProcessAlarms) *)")
    lines.append("IF rVotedChokeDownstreamPressure_bar >= c_Limit_ManifoldPress_H_bar THEN")
    lines.append("    dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#0000_0001; (* Bit 0: Manifold Pressure High Warning *)")
    lines.append("END_IF;")
    lines.append("IF rVotedChokeDownstreamPressure_bar <= c_Limit_ManifoldPress_L_bar THEN")
    lines.append("    dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#0000_0002; (* Bit 1: Manifold Pressure Low Warning *)")
    lines.append("END_IF;")
    lines.append("IF rVotedChokeDownstreamPressure_bar <= c_Limit_ManifoldPress_LL_bar THEN")
    lines.append("    dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#0000_0004; (* Bit 2: Manifold Severe Depressurization LL *)")
    lines.append("END_IF;")
    lines.append("IF rVotedWellheadPressure_bar >= c_Limit_WellheadPress_H_bar THEN")
    lines.append("    dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#0000_0008; (* Bit 3: Wellhead Pressure High Warning *)")
    lines.append("END_IF;")
    lines.append("IF rVotedWellheadTemp_degC >= c_Limit_WellheadTemp_HH_degC THEN")
    lines.append("    dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#0000_0010; (* Bit 4: Wellhead Fluid High Temp Hazard *)")
    lines.append("END_IF;")
    lines.append("IF rVotedWellheadTemp_degC <= c_Limit_WellheadTemp_L_degC THEN")
    lines.append("    dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#0000_0020; (* Bit 5: Wellhead Fluid Low Temp Advisory *)")
    lines.append("END_IF;")
    lines.append("IF rVotedWetGasFlow_kgs >= c_Limit_WetGasFlow_H_kgs THEN")
    lines.append("    dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#0000_0040; (* Bit 6: Wet Gas Flow High Warning *)")
    lines.append("END_IF;")
    lines.append("IF PT_HYDRAULIC_HPU_HP_bar <= c_Limit_HpuSupplyPress_L_bar THEN")
    lines.append("    dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#0000_0080; (* Bit 7: SCM Hydraulic Pressure Low Advisory *)")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* 6.3 Process Warnings (Packed into dwWarningWord) *)")
    lines.append("IF rSluggingSeverityIndex >= c_Limit_SlugSeverity_H_pct THEN")
    lines.append("    dwWarningWord := dwWarningWord OR 16#0000_0001; (* Bit 0: Hydrodynamic Severe Slugging Inception *)")
    lines.append("END_IF;")
    lines.append("IF rSluggingSeverityIndex >= c_Limit_SlugSeverity_HH_pct THEN")
    lines.append("    dwWarningWord := dwWarningWord OR 16#0000_0002; (* Bit 1: Massive Liquid Slug Wave Impact Hazard *)")
    lines.append("END_IF;")
    lines.append("IF rHydrateSubcoolingMargin_degC <= rMinHydrateMargin_degC THEN")
    lines.append("    dwWarningWord := dwWarningWord OR 16#0000_0004; (* Bit 2: Operating Inside Hydrate Risk Envelope *)")
    lines.append("END_IF;")
    lines.append("IF rBoosterPumpNPSHMargin_bar <= 1.50 THEN")
    lines.append("    dwWarningWord := dwWarningWord OR 16#0000_0008; (* Bit 3: Booster Pump Low NPSH Cavitation Risk *)")
    lines.append("END_IF;")
    lines.append("IF rBoosterPumpVibrationRMS_mms >= c_Limit_PumpVibration_H_mms THEN")
    lines.append("    dwWarningWord := dwWarningWord OR 16#0000_0010; (* Bit 4: Booster Pump Elevated Vibration Advisory *)")
    lines.append("END_IF;")
    lines.append("IF bTMRSensorDegradedMode THEN")
    lines.append("    dwWarningWord := dwWarningWord OR 16#0000_0020; (* Bit 5: Instrument TMR Voting Operating in Degraded Mode *)")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* 6.4 TMR Sensor Channel Degradation Packing (dwTMR_DegradationWord) *)")
    lines.append("IF bFault_PT101_A THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_0001; END_IF;")
    lines.append("IF bFault_PT101_B THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_0002; END_IF;")
    lines.append("IF bFault_PT101_C THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_0004; END_IF;")
    lines.append("IF bFault_PT102_A THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_0008; END_IF;")
    lines.append("IF bFault_PT102_B THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_0010; END_IF;")
    lines.append("IF bFault_PT102_C THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_0020; END_IF;")
    lines.append("IF bFault_TT201_A THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_0040; END_IF;")
    lines.append("IF bFault_TT201_B THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_0080; END_IF;")
    lines.append("IF bFault_TT201_C THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_0100; END_IF;")
    lines.append("IF bFault_FT301_A THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_0200; END_IF;")
    lines.append("IF bFault_FT301_B THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_0400; END_IF;")
    lines.append("IF bFault_FT301_C THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_0800; END_IF;")
    lines.append("IF bFault_DT401_A THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_1000; END_IF;")
    lines.append("IF bFault_DT401_B THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_2000; END_IF;")
    lines.append("IF bFault_DT401_C THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_4000; END_IF;")
    lines.append("IF bFault_PT501_A THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0000_8000; END_IF;")
    lines.append("IF bFault_PT501_B THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0001_0000; END_IF;")
    lines.append("IF bFault_PT501_C THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0002_0000; END_IF;")
    lines.append("IF bFault_FT601_A THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0004_0000; END_IF;")
    lines.append("IF bFault_FT601_B THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0008_0000; END_IF;")
    lines.append("IF bFault_FT601_C THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0010_0000; END_IF;")
    lines.append("IF bFault_ZT701_A THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0020_0000; END_IF;")
    lines.append("IF bFault_ZT701_B THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0040_0000; END_IF;")
    lines.append("IF bFault_ZT701_C THEN dwTMR_DegradationWord := dwTMR_DegradationWord OR 16#0080_0000; END_IF;")
    lines.append("")
    lines.append("(* 6.5 Master Operational Status Word Packing (dwSystemStatusWord) *)")
    lines.append("IF bSystemReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0001; END_IF;")
    lines.append("IF bSystemRunning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0002; END_IF;")
    lines.append("IF bHippsTripped THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0004; END_IF;")
    lines.append("IF bActiveSluggingMitigationActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0008; END_IF;")
    lines.append("IF bHydrateInhibitionWarning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010; END_IF;")
    lines.append("IF bPumpCavitationMitigationActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020; END_IF;")
    lines.append("IF bTMRSensorDegradedMode THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0040; END_IF;")
    lines.append("IF bMpcAntiSlugActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0080; END_IF;")
    lines.append("IF bHippsBypassKeySwitch THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0100; END_IF;")
    lines.append("")
    lines.append("(* 6.6 Subsea Choke Hydraulic Linear Stepping Motor Actuator Logic *)")
    lines.append("rChokePositionError_pct := rChokePositionDemand_pct - rVotedChokePosition_pct;")
    lines.append("IF ABS(rChokePositionError_pct) > 0.35 THEN")
    lines.append("    bChokeSteppingMotorPulse := TRUE;")
    lines.append("    IF rChokePositionError_pct < 0.0 THEN")
    lines.append("        bChokeStepDirectionClose := TRUE; (* Command stepping motor close / throttle *)")
    lines.append("    ELSE")
    lines.append("        bChokeStepDirectionClose := FALSE; (* Command stepping motor open *)")
    lines.append("    END_IF;")
    lines.append("ELSE")
    lines.append("    bChokeSteppingMotorPulse := FALSE;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("(* Advance Scan Execution Counter *)")
    lines.append("iCycleCounter := iCycleCounter + 1;")
    lines.append("ePreviousState := eCurrentState;")
    lines.append("")
    lines.append("END_FUNCTION_BLOCK")
    return "\n".join(lines)

def build_entire_code():
    import test_gen
    decl = test_gen.generate_subsea_st_code()
    mat = build_section_matrices()
    tmr = build_section_tmr()
    hydro = build_section_hydrodynamics()
    mpc = build_section_mpc()
    fsm = build_section_fsm()
    alarms = build_section_alarms_and_stepping()
    
    code = f"{decl}\n{mat}\n{tmr}\n{hydro}\n{mpc}\n{fsm}\n{alarms}\n"
    return code

if __name__ == "__main__":
    code = build_entire_code()
    print("Total ST Code Length:", len(code))
    lines = code.splitlines()
    print("Total Line Count:", len(lines))
    print("First Line:", lines[0])
    print("Last Line:", lines[-1])
