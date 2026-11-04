# -*- coding: utf-8 -*-
"""
Module 3: Phase 0 State-Space Matrix & MPC Weight Initialization
"""

def get_phase0_matrices():
    lines = []
    lines.append("(* =========================================================================================== *)")
    lines.append("(* PHASE 0: MODEL MATRICES & CONTROL COEFFICIENT INITIALIZATION                                *)")
    lines.append("(* =========================================================================================== *)")
    lines.append("IF NOT bMatricesInitialized THEN")
    lines.append("    (* --------------------------------------------------------------------------------------- *)")
    lines.append("    (* 1.0 DISCRETE STATE TRANSITION MATRIX A (8x8) @ Ts = 10 ms                               *)")
    lines.append("    (* States:                                                                                 *)")
    lines.append("    (* x1: Delta Cargo Tank Ullage Vapor Pressure [mbar] (Nominal: 1060.0 mbar abs)            *)")
    lines.append("    (* x2: Delta Bulk Liquid LNG Temperature [deg C] (Nominal: -161.5 deg C)                   *)")
    lines.append("    (* x3: Instantaneous BOG Mass Generation Rate [kg/h] (Nominal: 1570.0 kg/h)                *)")
    lines.append("    (* x4: Delta 4-Stage Compressor Discharge Pressure [bar] (Nominal: 300.0 bar)              *)")
    lines.append("    (* x5: Delta Compressor Final Stage Discharge Gas Temp [deg C] (Nominal: 42.0 deg C)       *)")
    lines.append("    (* x6: Delta Reverse-Brayton Subcooled Exit Temp [deg C] (Nominal: -162.0 deg C)           *)")
    lines.append("    (* x7: Delta FGSS Main Engine Fuel Rail Header Pressure [bar] (Nominal: 300.0 bar)         *)")
    lines.append("    (* x8: Cryogenic NO96 Invar Membrane Hydro-Thermal Stress [MPa] (Nominal: 18.5 MPa)        *)")
    lines.append("    (* --------------------------------------------------------------------------------------- *)")
    
    # State-Space Matrix A (8x8)
    a_descriptions = {
        (1, 1): (0.9942, "Tank ullage vapor acoustic capacitance and pressure self-regulation persistence"),
        (1, 2): (0.0145, "Thermodynamic saturation vapor pressure coupling from liquid surface temperature rise"),
        (1, 3): (0.0038, "Vapor pressure rate surge driven by net incoming boil-off gas mass accumulation"),
        (1, 4): (-0.0012, "Vapor extraction backpressure relief from 4-stage compressor suction intake"),
        (1, 5): (0.0004, "Hot gas blowback thermal expansion coupling across compressor suction bypass"),
        (1, 6): (-0.0028, "Cryogenic vapor contraction and condensing collapse from subcooler liquid return"),
        (1, 7): (-0.0009, "Fuel gas manifold transient draw coupling back to cargo suction header"),
        (1, 8): (0.0001, "Membrane corrugation micro-flexure volumetric volume perturbation on ullage"),

        (2, 1): (0.0008, "Hydrostatic head compression thermal dissipation into bulk cryogenic liquid"),
        (2, 2): (0.9985, "Massive cryogenic thermal inertia of 174,000 m3 subcooled liquid methane bulk"),
        (2, 3): (-0.0002, "Evaporative cooling latent heat extraction from liquid surface during boil-off"),
        (2, 4): (0.0000, "Decoupled downstream compressor discharge pressure isolated from liquid bulk"),
        (2, 5): (0.0001, "Thermal conduction along submerged pump discharge column piping"),
        (2, 6): (0.0032, "Subcooled liquid droplet return from reliquefier directly chilling cargo bulk"),
        (2, 7): (0.0000, "High-pressure fuel rail decoupled from cargo liquid bulk thermal dynamics"),
        (2, 8): (-0.0005, "Membrane boundary heat transfer enhancement during hull thermal contraction"),

        (3, 1): (0.0120, "Tank pressure accumulation suppressing superficial bubble flash boiling rate"),
        (3, 2): (0.0450, "Arrhenius vapor-liquid interfacial kinetic evaporation acceleration with temperature"),
        (3, 3): (0.9820, "Boil-off gas momentum and turbulent vapor plume transport persistence"),
        (3, 4): (-0.0040, "Compressor suction suction depression accelerating boundary gas evacuation"),
        (3, 5): (0.0015, "Thermal recirculation vapor plume warming enhancing localized boil-off rate"),
        (3, 6): (-0.0180, "Vapor suppression by continuous subcooled cryogenic condensate spray re-injection"),
        (3, 7): (-0.0010, "Engine manifold pressure transient modulating suction gas displacement"),
        (3, 8): (0.0085, "Hull sloshing mechanical shear wave agitation generating aerosol flash vapor"),

        (4, 1): (0.0015, "Suction header pressure feedforward into 4th-stage compression cylinder displacement"),
        (4, 2): (0.0000, "Liquid bulk temperature decoupled from reciprocating cylinder gas compression"),
        (4, 3): (0.0062, "Gas mass intake density variation directly altering reciprocating stage mass flow"),
        (4, 4): (0.9850, "4-Stage reciprocating compressor pulsation dampener volume capacitance"),
        (4, 5): (-0.0024, "Gas density reduction at elevated discharge temperature reducing mass pressure"),
        (4, 6): (0.0000, "Reliquefaction cold-box isolated from compressor 4th-stage high-pressure delivery"),
        (4, 7): (-0.0140, "Hydraulic backpressure wave coupling from dual-fuel engine injection rail"),
        (4, 8): (0.0000, "Membrane mechanical stress decoupled from reciprocating compressor discharge"),

        (5, 1): (0.0005, "Suction pressure fluctuation altering overall 4-stage polytropic pressure ratio"),
        (5, 2): (0.0000, "Liquid cargo bulk temperature isolated from intercooled reciprocating stages"),
        (5, 3): (0.0018, "Compressor mass throughput modulating interstage gas velocity and heat transfer"),
        (5, 4): (0.0150, "Polytropic compression thermodynamic temperature rise across stage 4 cylinders"),
        (5, 5): (0.9780, "Intercooler shell-and-tube thermal dissipation and jacket cooling persistence"),
        (5, 6): (0.0000, "Reliquefaction cold loop decoupled from compressor interstage cooling circuit"),
        (5, 7): (0.0035, "Downstream hydraulic resistance causing localized gas stagnation heating"),
        (5, 8): (0.0000, "Hull membrane stress isolated from compressor cylinder head heat transfer"),

        (6, 1): (0.0010, "BOG inlet vapor pressure modulating cold-box plate-fin heat exchanger density"),
        (6, 2): (0.0045, "Inlet gas enthalpy shift driven by bulk cargo evaporation temperature variation"),
        (6, 3): (0.0110, "BOG mass flow throughput increasing thermal load on Nitrogen Brayton expander"),
        (6, 4): (0.0000, "High-pressure compressor discharge isolated from low-pressure reliquefier loop"),
        (6, 5): (0.0000, "Compressor discharge heat isolated from cryogenic subcooler cold-box core"),
        (6, 6): (0.9880, "Reverse-Brayton plate-fin matrix cryogenic thermal inertia and subcooling persistence"),
        (6, 7): (0.0000, "FGSS engine rail pressure isolated from Nitrogen Brayton subcooler loop"),
        (6, 8): (0.0000, "Membrane stress decoupled from plate-fin vacuum cold-box heat transfer"),

        (7, 1): (0.0008, "Suction gas supply pressure stability propagating through 4 compression stages"),
        (7, 2): (0.0000, "Liquid bulk temperature isolated from engine fuel injection rail dynamics"),
        (7, 3): (0.0042, "BOG mass flow availability stabilizing high-pressure fuel rail accumulation"),
        (7, 4): (0.0380, "Direct mass inflow from 4-stage reciprocating compressor discharge line"),
        (7, 5): (-0.0018, "Fuel gas thermal expansion/contraction modifying dense phase compressibility"),
        (7, 6): (0.0000, "Subcooler condensate return loop decoupled from engine high-pressure fuel rail"),
        (7, 7): (0.9910, "Main engine fuel gas rail hydraulic accumulator capacitance (300 bar dense phase)"),
        (7, 8): (0.0000, "Containment membrane stress decoupled from engine fuel gas supply manifold"),

        (8, 1): (0.0045, "Tank internal vapor pressure expansion exerting outward normal stress on Invar"),
        (8, 2): (-0.0180, "Cryogenic temperature contraction thermal gradient across 0.7 mm Invar membrane"),
        (8, 3): (0.0000, "Vapor mass generation rate decoupled from solid membrane structural mechanics"),
        (8, 4): (0.0000, "Compressor discharge pressure isolated from cargo tank boundary bulkhead"),
        (8, 5): (0.0000, "Compressor gas temperature isolated from cryogenic cargo tank membrane walls"),
        (8, 6): (0.0022, "Localized subcooled condensate droplet impingement creating localized thermal stress"),
        (8, 7): (0.0000, "Engine manifold pressure isolated from cargo tank structural containment"),
        (8, 8): (0.9960, "NO96 Invar alloy and reinforced perlite insulation box viscoelastic stress retention")
    }

    for (row, col), (val, desc) in a_descriptions.items():
        lines.append(f"    matA[{row}, {col}] := {val:.4f}; (* {desc} *)")
    lines.append("")
    
    lines.append("    (* --------------------------------------------------------------------------------------- *)")
    lines.append("    (* 2.0 ACTUATOR COUPLING MATRIX B (8x4) @ Ts = 10 ms                                       *)")
    lines.append("    (* Inputs:                                                                                 *)")
    lines.append("    (* u1: BOG Reciprocating Compressor VFD Speed [RPM] (0.0 to 1800.0 RPM)                     *)")
    lines.append("    (* u2: Nitrogen Reverse-Brayton Expander JT Bypass Valve [%] (0.0 to 100.0 %)               *)")
    lines.append("    (* u3: Gas Combustion Unit (GCU) Burner Firing Rate [%] (0.0 to 100.0 %)                   *)")
    lines.append("    (* u4: FGSS Engine Fuel Gas Supply Trim Valve [%] (0.0 to 100.0 %)                         *)")
    lines.append("    (* --------------------------------------------------------------------------------------- *)")

    b_descriptions = {
        (1, 1): (-0.0185, "Compressor speed increase accelerates suction evacuation, depressing tank ullage"),
        (1, 2): (-0.0082, "JT valve opening deepens subcooling, accelerating vapor collapse in ullage space"),
        (1, 3): (-0.0140, "GCU burner firing evacuates excess BOG, directly relieving tank ullage pressure"),
        (1, 4): (0.0000, "Engine fuel gas trim valve operates on high-pressure rail, zero direct ullage effect"),

        (2, 1): (-0.0004, "Enhanced evaporation evaporatively cools LNG liquid surface under compressor draw"),
        (2, 2): (-0.0025, "Subcooled condensate return cools bulk liquid cargo inventory"),
        (2, 3): (-0.0002, "GCU gas consumption slightly accelerates surface latent heat evaporative cooling"),
        (2, 4): (0.0000, "Engine fuel rail trim valve decoupled from bulk liquid cargo temperature"),

        (3, 1): (-0.0250, "Compressor suction depression suppresses interfacial thermal vapor blanket"),
        (3, 2): (-0.0160, "Subcooler condensate return suppresses localized vapor plume generation"),
        (3, 3): (-0.0320, "GCU draw directly consumes available BOG mass from collection manifold"),
        (3, 4): (0.0000, "Engine rail trim valve decoupled from raw cargo boil-off generation rate"),

        (4, 1): (0.0520, "Compressor VFD RPM ramp directly elevates 4th-stage discharge mass throughput"),
        (4, 2): (0.0000, "JT valve bypass isolated from reciprocating compressor discharge manifold"),
        (4, 3): (0.0000, "GCU atmospheric burner isolated from high-pressure compressor discharge line"),
        (4, 4): (-0.0210, "Opening engine fuel rail trim valve discharges high-pressure gas, lowering P4"),

        (5, 1): (0.0180, "Higher reciprocating compressor RPM increases polytropic frictional heat"),
        (5, 2): (0.0000, "Reliquefaction JT bypass valve decoupled from compressor stage 4 gas temperature"),
        (5, 3): (0.0000, "GCU burner modulation decoupled from compressor interstage gas temperature"),
        (5, 4): (-0.0035, "Increased gas velocity through trim valve enhances convective cylinder scavenge"),

        (6, 1): (0.0000, "BOG compressor speed decoupled from Reverse-Brayton Nitrogen cold-box core"),
        (6, 2): (-0.0450, "JT valve opening expands high-pressure N2, deepening cryogenic refrigeration"),
        (6, 3): (0.0000, "GCU flaring decoupled from Nitrogen Reverse-Brayton subcooler return loop"),
        (6, 4): (0.0000, "Engine fuel trim valve decoupled from reliquefier condensate return loop"),

        (7, 1): (0.0480, "Compressor displacement directly supplies high-pressure gas to FGSS rail"),
        (7, 2): (0.0000, "Nitrogen reliquefaction loop decoupled from dual-fuel engine FGSS fuel rail"),
        (7, 3): (0.0000, "GCU low-pressure combustion isolated from 300 bar engine fuel supply header"),
        (7, 4): (-0.0560, "Engine fuel trim valve throttling directly controls high-pressure rail pressure"),

        (8, 1): (0.0010, "Pressure suction transients create minor membrane micro-deflection stress"),
        (8, 2): (-0.0015, "Subcooler return temperature moderates thermal gradient on tank bottom Invar"),
        (8, 3): (0.0005, "GCU flaring minimizes ullage overpressurization, protecting membrane integrity"),
        (8, 4): (0.0000, "Engine fuel trim valve completely decoupled from cargo containment membrane")
    }

    for (row, col), (val, desc) in b_descriptions.items():
        lines.append(f"    matB[{row}, {col}] := {val:.4f}; (* {desc} *)")
    lines.append("")
    
    lines.append("    (* --------------------------------------------------------------------------------------- *)")
    lines.append("    (* 3.0 STATE OBSERVATION MATRIX C (8x8) & DIRECT FEEDTHROUGH D (8x4)                        *)")
    lines.append("    (* --------------------------------------------------------------------------------------- *)")
    lines.append("    FOR idx_i := 1 TO 8 DO")
    lines.append("        FOR idx_j := 1 TO 8 DO")
    lines.append("            IF idx_i = idx_j THEN")
    lines.append("                matC[idx_i, idx_j] := 1.0; (* Direct 1:1 State Observation *)")
    lines.append("            ELSE")
    lines.append("                matC[idx_i, idx_j] := 0.0;")
    lines.append("            END_IF;")
    lines.append("        END_FOR;")
    lines.append("        FOR idx_m := 1 TO 4 DO")
    lines.append("            matD[idx_i, idx_m] := 0.0; (* Pure Strictly Proper Dynamic Plant *)")
    lines.append("        END_FOR;")
    lines.append("    END_FOR;")
    lines.append("")

    lines.append("    (* --------------------------------------------------------------------------------------- *)")
    lines.append("    (* 4.0 RECEDING-HORIZON MPC WEIGHT MATRICES & ACTUATOR CONSTRAINTS                          *)")
    lines.append("    (* --------------------------------------------------------------------------------------- *)")
    lines.append("    (* Q Diagonal Penalties: State Tracking Performance Weights *)")
    lines.append("    matQ_Weight[1] := 15.0;  (* x1: Cargo Tank Ullage Pressure - Critical Primary Target *)")
    lines.append("    matQ_Weight[2] := 2.5;   (* x2: Cargo Liquid Temperature - High Thermal Inertia *)")
    lines.append("    matQ_Weight[3] := 4.0;   (* x3: BOG Mass Generation Rate - Mass Balance Target *)")
    lines.append("    matQ_Weight[4] := 10.0;  (* x4: Compressor Discharge Pressure - Machine Integrity *)")
    lines.append("    matQ_Weight[5] := 5.0;   (* x5: Compressor Discharge Gas Temp - Intercooler Protection *)")
    lines.append("    matQ_Weight[6] := 8.0;   (* x6: Reliquefier Exit Temp - Subcooling Quality *)")
    lines.append("    matQ_Weight[7] := 18.0;  (* x7: FGSS Engine Fuel Rail - Ultra-Tight 300.0 +/- 1.5 bar *)")
    lines.append("    matQ_Weight[8] := 6.0;   (* x8: Membrane Thermal-Mechanical Stress - Fatigue Prevention *)")
    lines.append("")
    lines.append("    (* R Diagonal Penalties: Actuator Effort Minimization *)")
    lines.append("    matR_Weight[1] := 0.08;  (* u1: Compressor VFD RPM - Electrical Power Economy *)")
    lines.append("    matR_Weight[2] := 0.05;  (* u2: Reliquefier JT Valve - Nitrogen Refrigeration Power *)")
    lines.append("    matR_Weight[3] := 0.25;  (* u3: GCU Firing Rate - High Penalty: Minimize Cargo Loss *)")
    lines.append("    matR_Weight[4] := 0.04;  (* u4: FGSS Trim Valve - Engine Responsiveness Priority *)")
    lines.append("")
    lines.append("    (* S Diagonal Penalties: Slew Rate Smoothing Penalties *)")
    lines.append("    matS_Weight[1] := 0.45;  (* u1: Slew penalty to protect compressor crankshaft *)")
    lines.append("    matS_Weight[2] := 0.20;  (* u2: Slew penalty to protect JT valve seat cavitation *)")
    lines.append("    matS_Weight[3] := 0.60;  (* u3: Slew penalty to stabilize GCU burner combustion *)")
    lines.append("    matS_Weight[4] := 0.15;  (* u4: Slew penalty for fuel rail acoustic dampening *)")
    lines.append("")
    lines.append("    (* Physical Saturation Bounds *)")
    lines.append("    vecU_Min[1] := 0.0;      vecU_Max[1] := 1800.0;   (* Compressor VFD RPM Range *)")
    lines.append("    vecU_Min[2] := 0.0;      vecU_Max[2] := 100.0;    (* Reliquefier JT Valve Range [%] *)")
    lines.append("    vecU_Min[3] := 0.0;      vecU_Max[3] := 100.0;    (* GCU Burner Firing Range [%] *)")
    lines.append("    vecU_Min[4] := 0.0;      vecU_Max[4] := 100.0;    (* FGSS Fuel Rail Trim Range [%] *)")
    lines.append("")
    lines.append("    (* Maximum Allowable Slew Rates Per 10 ms Cycle *)")
    lines.append("    vecDeltaU_Max[1] := 1.5; (* 150 RPM/sec Max Acceleration Limit *)")
    lines.append("    vecDeltaU_Max[2] := 0.5; (* 50.0 %/sec Max Stroke Velocity *)")
    lines.append("    vecDeltaU_Max[3] := 0.8; (* 80.0 %/sec Max Burner Ramp Rate *)")
    lines.append("    vecDeltaU_Max[4] := 1.2; (* 120.0 %/sec Fast Trim Actuation *)")
    lines.append("")
    lines.append("    (* Nominal Reference Target State Vector r[k] *)")
    lines.append("    vecRef[1] := 0.0;        (* Delta Ullage Pressure target = 0 mbar (1060 mbar abs) *)")
    lines.append("    vecRef[2] := 0.0;        (* Delta Liquid Temp target = 0 deg C (-161.5 deg C) *)")
    lines.append("    vecRef[3] := 0.0;        (* Delta BOG Rate target = 0 kg/h balance *)")
    lines.append("    vecRef[4] := 0.0;        (* Delta Comp Discharge target = 0 bar (300.0 bar) *)")
    lines.append("    vecRef[5] := 0.0;        (* Delta Stage 4 Temp target = 0 deg C (42.0 deg C) *)")
    lines.append("    vecRef[6] := 0.0;        (* Delta Reliq Return target = 0 deg C (-162.0 deg C) *)")
    lines.append("    vecRef[7] := 0.0;        (* Delta FGSS Rail target = 0 bar (300.0 bar) *)")
    lines.append("    vecRef[8] := 0.0;        (* Delta Membrane Stress target = 0 MPa balance *)")
    lines.append("")
    lines.append("    bMatricesInitialized := TRUE;")
    lines.append("END_IF;")
    return "\n".join(lines)

print("Module 3 (Phase 0 Matrices) ready.")
