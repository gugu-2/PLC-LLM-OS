# Part 2: Matrix and Parameter Initialization (Phase 0)
import sys

def get_part2_matrix_init():
    code = []
    code.append("(* ============================================================================================== *)")
    code.append("(* PHASE 0: FIRST-CYCLE CYBER-PHYSICAL SYSTEM MATRICES & COEFFICIENTS INITIALIZATION             *)")
    code.append("(* ============================================================================================== *)")
    code.append("IF NOT bInitialized THEN")
    code.append("    (* --- Discrete State-Space System Matrix A (8x8) at Ts = 0.025 s --- *)")
    
    # Define A matrix values
    # x1: Flux J
    # x2: P_perm
    # x3: TMP
    # x4: R_cake
    # x5: DO
    # x6: MLSS
    # x7: NO3-N
    # x8: Q_air
    matA_vals = [
        # x1: J (decays slightly with cake resistance and TMP rise)
        [0.9880, -0.0015, -0.0028, -0.0045,  0.0000, -0.0008,  0.0000,  0.0005],
        # x2: P_perm (suction pressure tracking)
        [0.0050,  0.9820, -0.0120, -0.0018,  0.0000,  0.0000,  0.0000,  0.0000],
        # x3: TMP (inversely coupled to suction pressure and cake build-up)
        [0.0085, -0.0150,  0.9860,  0.0075,  0.0000,  0.0012,  0.0000, -0.0008],
        # x4: R_cake (accumulates with flux and MLSS, sheared by air scour)
        [0.0042,  0.0000,  0.0015,  0.9920,  0.0000,  0.0035,  0.0000, -0.0065],
        # x5: DO (aerobic consumption OUR, fine bubble oxygen transfer)
        [0.0000,  0.0000,  0.0000,  0.0000,  0.9750, -0.0022,  0.0000,  0.0012],
        # x6: MLSS (biological growth and solids yield)
        [0.0000,  0.0000,  0.0000,  0.0000,  0.0015,  0.9995,  0.0000,  0.0000],
        # x7: NO3-N (nitrification rate dependent on DO, denitrification by MLR)
        [0.0000,  0.0000,  0.0000,  0.0000,  0.0065,  0.0008,  0.9820,  0.0000],
        # x8: Q_air (blower manifold pneumatic dynamics)
        [0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.9650]
    ]

    matA_comments = [
        "J flux auto-decay, suction coupling, TMP resistance, cake throttling, null, MLSS viscosity drag, null, air scour shear lift",
        "P_perm forward permeation coupling, hydraulic relaxation, TMP pressure drop, cake drop, null, null, null, null",
        "TMP cross-flux rise, suction manifold delta, TMP damping, cake resistance penalty, null, MLSS solids impact, null, scour reduction",
        "Cake accumulation wrt flux, null, TMP compression, cake retention, null, MLSS deposition rate, null, air bubble scouring detachment",
        "Null, null, null, null, DO oxygen auto-consumption decay, MLSS endogenous respiration, null, coarse-bubble surface transfer",
        "Null, null, null, null, DO biomass synthesis yield, MLSS sludge inventory retention, null, null",
        "Null, null, null, null, Nitrification DO conversion, autotrophic biomass fraction, Nitrate retention, null",
        "Null, null, null, null, null, null, null, Blower distribution manifold pneumatic lag"
    ]

    for r in range(8):
        code.append(f"    (* Row {r+1}: {matA_comments[r]} *)")
        for c in range(8):
            val = matA_vals[r][c]
            code.append(f"    matA[{r+1}, {c+1}] := {val:.4f};")

    code.append("")
    code.append("    (* --- Discrete Input Control Matrix B (8x8) at Ts = 0.025 s --- *)")
    # Inputs:
    # u1: Permeate Suction Pump [%]
    # u2: Backpulse Pump [%]
    # u3: Scour Blower [%]
    # u4: Aeration Valve [%]
    # u5: MLR Pump [%]
    # u6: WAS Pump [%]
    # u7: NaOCl Metering [%]
    # u8: Citric Acid Metering [%]
    matB_vals = [
        # x1: J
        [ 0.0450, -0.0650,  0.0025,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        # x2: P_perm
        [-0.0820,  0.1150,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000],
        # x3: TMP
        [ 0.0750, -0.1200, -0.0150,  0.0000,  0.0000,  0.0000, -0.0080, -0.0065],
        # x4: R_cake
        [ 0.0120, -0.0850, -0.0450,  0.0000,  0.0000,  0.0000, -0.0250, -0.0180],
        # x5: DO
        [ 0.0000,  0.0000,  0.0045,  0.0520, -0.0015,  0.0000,  0.0000,  0.0000],
        # x6: MLSS
        [ 0.0000,  0.0000,  0.0000,  0.0000,  0.0025, -0.0380,  0.0000,  0.0000],
        # x7: NO3-N
        [ 0.0000,  0.0000,  0.0000,  0.0085, -0.0420, -0.0012,  0.0000,  0.0000],
        # x8: Q_air
        [ 0.0000,  0.0000,  0.3500,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000]
    ]

    matB_comments = [
        "Flux response: Suction pump gain (+), backpulse reverse (-), scour shear assist (+), zero, zero, zero, zero, zero",
        "Suction pressure: Suction pump vacuum (-), backpulse positive pressure (+), zero, zero, zero, zero, zero, zero",
        "TMP response: Suction pump TMP elevation (+), backpulse relief (-), air scour scouring relief (-), null, null, null, NaOCl bio-clean (-), Citric acid scale-clean (-)",
        "Cake resistance: Suction deposition (+), backpulse cake lift (-), coarse-bubble shear detachment (-), null, null, null, NaOCl oxidation (-), Citric solubilization (-)",
        "DO response: null, null, coarse-bubble surface reaeration (+), fine-bubble diffuser oxygenation (+), MLR recycle drag (-), null, null, null",
        "MLSS response: null, null, null, null, internal recycle yield (+), WAS sludge wasting discharge (-), null, null",
        "Nitrate response: null, null, null, nitrification DO boost (+), MLR anoxic denitrification dilution (-), WAS loss (-), null, null",
        "Scour air flow: null, null, Scour blower speed drive authority (+), null, null, null, null, null"
    ]

    for r in range(8):
        code.append(f"    (* Row {r+1}: {matB_comments[r]} *)")
        for c in range(8):
            val = matB_vals[r][c]
            code.append(f"    matB[{r+1}, {c+1}] := {val:.4f};")

    code.append("")
    code.append("    (* --- Discrete Disturbance Feedforward Matrix E (8x8) at Ts = 0.025 s --- *)")
    # Disturbances:
    # d1: Mixed Liquor Temp [deg C]
    # d2: Basin Liquid Level [m]
    # d3: Influent COD [mg/L]
    # d4: Influent TKN [mg/L]
    # d5: Influent Flow Rate [m3/h]
    # d6: SVI [mL/g]
    # d7: EPS [mg/L]
    # d8: Barometric Press [mbar]
    matE_vals = [
        # x1: J (temperature viscosity boost, hydrostatic head assist)
        [ 0.0150,  0.0085,  0.0000,  0.0000,  0.0005, -0.0012, -0.0025,  0.0000],
        # x2: P_perm (hydrostatic head adds positive base pressure)
        [ 0.0000,  0.0981,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0010],
        # x3: TMP (viscosity temperature reduction, SVI fouling, EPS gel resistance)
        [-0.0180,  0.0000,  0.0008,  0.0005,  0.0015,  0.0045,  0.0085,  0.0000],
        # x4: R_cake (SVI sludge compressibility, EPS extracellular polymer fouling)
        [-0.0080,  0.0000,  0.0012,  0.0000,  0.0020,  0.0065,  0.0125,  0.0000],
        # x5: DO (temperature saturation solubility reduction, COD aeration demand)
        [-0.0120,  0.0015, -0.0035, -0.0018, -0.0008,  0.0000,  0.0000,  0.0005],
        # x6: MLSS (influent solids loading and substrate growth)
        [ 0.0000,  0.0000,  0.0085,  0.0015,  0.0120,  0.0000,  0.0000,  0.0000],
        # x7: NO3-N (TKN nitrogen load converted to nitrate)
        [ 0.0025,  0.0000, -0.0015,  0.0095,  0.0035,  0.0000,  0.0000,  0.0000],
        # x8: Q_air (atmospheric pressure density variation)
        [-0.0050,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0025]
    ]

    matE_comments = [
        "Flux disturbance: Water temp viscosity (+), liquid level (+), null, null, influent surge (+), SVI (-), EPS (-), null",
        "Suction pressure: null, hydrostatic level column (+), null, null, null, null, null, barometric shift (+)",
        "TMP disturbance: Water temp viscosity relief (-), null, COD foulants (+), TKN (+), flow surge (+), SVI (+), EPS (+), null",
        "Cake resistance: Temp mobility (-), null, COD organic load (+), null, hydraulic flux surge (+), SVI cake (+), EPS gel (+), null",
        "DO disturbance: Temp solubility loss (-), head depth (+), COD oxygen demand (-), TKN nitrification demand (-), flow load (-), null, null, barometric (+)",
        "MLSS disturbance: null, null, COD organic synthesis (+), TKN synthesis (+), influent hydraulic solids load (+), null, null, null",
        "Nitrate disturbance: Biological temperature rate (+), null, COD carbonaceous denitrification (-), TKN nitrification feed (+), flow (+), null, null, null",
        "Scour air disturbance: Air temp expansion (-), null, null, null, null, null, null, ambient barometric intake density (+)"
    ]

    for r in range(8):
        code.append(f"    (* Row {r+1}: {matE_comments[r]} *)")
        for c in range(8):
            val = matE_vals[r][c]
            code.append(f"    matE[{r+1}, {c+1}] := {val:.4f};")

    code.append("")
    code.append("    (* --- Discrete Measurement Matrix C (8x8) --- *)")
    # State mapping: direct observation of J, P_perm, TMP, R_cake (observer), DO, MLSS, NO3-N, Q_air
    for r in range(8):
        code.append(f"    (* Row {r+1}: State observation output y[{r+1}] *)")
        for c in range(8):
            val = 1.0000 if r == c else 0.0000
            code.append(f"    matC[{r+1}, {c+1}] := {val:.4f};")

    code.append("")
    code.append("    (* --- Discrete Direct Transmission Matrix D (8x8) --- *)")
    for r in range(8):
        code.append(f"    (* Row {r+1}: Direct feedthrough D[{r+1}] *)")
        for c in range(8):
            code.append(f"    matD[{r+1}, {c+1}] := 0.0000;")

    code.append("")
    code.append("    (* --- Luenberger State Observer Gain Matrix L (8x8) --- *)")
    # Innovation filter gains
    matL_vals = [
        [0.1850, 0.0025, 0.0050, 0.0015, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0035, 0.2200, 0.0150, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0065, 0.0180, 0.2450, 0.0085, 0.0000, 0.0010, 0.0000, 0.0000],
        [0.0025, 0.0000, 0.0125, 0.1650, 0.0000, 0.0045, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.2100, 0.0015, 0.0000, 0.0025],
        [0.0000, 0.0000, 0.0000, 0.0025, 0.0010, 0.1950, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0035, 0.0015, 0.1750, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.2800]
    ]
    for r in range(8):
        code.append(f"    (* Observer gain Row {r+1} *)")
        for c in range(8):
            val = matL_vals[r][c]
            code.append(f"    matL[{r+1}, {c+1}] := {val:.4f};")

    code.append("")
    code.append("    (* --- MPC State Tracking Penalty Matrix Q (8x8) --- *)")
    # Weights on states:
    # x1 (Flux): high penalty (45.0)
    # x2 (Suction P): moderate (15.0)
    # x3 (TMP): critical penalty (85.0)
    # x4 (Cake R): high penalty (35.0)
    # x5 (DO): high penalty (55.0)
    # x6 (MLSS): moderate penalty (20.0)
    # x7 (NO3-N): moderate penalty (25.0)
    # x8 (Q_air): moderate penalty (18.0)
    q_diag = [45.0, 15.0, 85.0, 35.0, 55.0, 20.0, 25.0, 18.0]
    for r in range(8):
        code.append(f"    (* Q Row {r+1} *)")
        for c in range(8):
            val = q_diag[r] if r == c else 0.0
            code.append(f"    matQ[{r+1}, {c+1}] := {val:.4f};")

    code.append("")
    code.append("    (* --- MPC Actuator Effort Penalty Matrix R (8x8) --- *)")
    # Penalty on control effort:
    # u1 (Permeate VFD): 2.5
    # u2 (Backpulse VFD): 4.0
    # u3 (Scour Blower): 3.5
    # u4 (Aeration Valve): 1.8
    # u5 (MLR Pump): 2.0
    # u6 (WAS Pump): 3.0
    # u7 (NaOCl Pump): 8.5
    # u8 (Citric Acid Pump): 8.5
    r_diag = [2.5, 4.0, 3.5, 1.8, 2.0, 3.0, 8.5, 8.5]
    for r in range(8):
        code.append(f"    (* R Row {r+1} *)")
        for c in range(8):
            val = r_diag[r] if r == c else 0.0
            code.append(f"    matR[{r+1}, {c+1}] := {val:.4f};")

    code.append("")
    code.append("    (* --- MPC Actuator Slew Rate Penalty Matrix S (8x8) --- *)")
    # Penalty on rate of change Du:
    s_diag = [12.0, 15.0, 18.0, 8.0, 10.0, 14.0, 25.0, 25.0]
    for r in range(8):
        code.append(f"    (* S Row {r+1} *)")
        for c in range(8):
            val = s_diag[r] if r == c else 0.0
            code.append(f"    matS[{r+1}, {c+1}] := {val:.4f};")

    code.append("")
    code.append("    (* --- MPC Terminal State Penalty Matrix P (8x8) --- *)")
    # Riccati terminal cost approximation
    p_diag = [65.0, 22.0, 140.0, 55.0, 85.0, 32.0, 40.0, 28.0]
    for r in range(8):
        code.append(f"    (* P Row {r+1} *)")
        for c in range(8):
            val = p_diag[r] if r == c else 0.0
            code.append(f"    matP[{r+1}, {c+1}] := {val:.4f};")

    code.append("")
    code.append("    (* --- Actuator Physical Saturation Box Bounds & Dynamic Slew Limits --- *)")
    # u1: Permeate Suction Pump [0..100 %], max slew 2.0 % / scan
    code.append("    vecU_Min[1] := 0.0;     vecU_Max[1] := 100.0;   vecDeltaU_Max[1] := 2.00;")
    # u2: Backpulse Pump [0..100 %], max slew 5.0 % / scan
    code.append("    vecU_Min[2] := 0.0;     vecU_Max[2] := 100.0;   vecDeltaU_Max[2] := 5.00;")
    # u3: Scour Blower VFD [20..100 %], max slew 1.5 % / scan
    code.append("    vecU_Min[3] := 20.0;    vecU_Max[3] := 100.0;   vecDeltaU_Max[3] := 1.50;")
    # u4: Aeration Valve [0..100 %], max slew 3.0 % / scan
    code.append("    vecU_Min[4] := 0.0;     vecU_Max[4] := 100.0;   vecDeltaU_Max[4] := 3.00;")
    # u5: MLR Pump [15..100 %], max slew 2.5 % / scan
    code.append("    vecU_Min[5] := 15.0;    vecU_Max[5] := 100.0;   vecDeltaU_Max[5] := 2.50;")
    # u6: WAS Pump [0..100 %], max slew 2.0 % / scan
    code.append("    vecU_Min[6] := 0.0;     vecU_Max[6] := 100.0;   vecDeltaU_Max[6] := 2.00;")
    # u7: NaOCl Dosing Pump [0..100 %], max slew 4.0 % / scan
    code.append("    vecU_Min[7] := 0.0;     vecU_Max[7] := 100.0;   vecDeltaU_Max[7] := 4.00;")
    # u8: Citric Acid Pump [0..100 %], max slew 4.0 % / scan
    code.append("    vecU_Min[8] := 0.0;     vecU_Max[8] := 100.0;   vecDeltaU_Max[8] := 4.00;")

    code.append("")
    code.append("    (* --- Initial State Estimates & Vectors Reset --- *)")
    code.append("    FOR i := 1 TO 8 DO")
    code.append("        vecX_Est[i] := 0.0;")
    code.append("        vecX_Pred[i] := 0.0;")
    code.append("        vecX_Ref[i] := 0.0;")
    code.append("        vecY_Meas[i] := 0.0;")
    code.append("        vecY_Est[i] := 0.0;")
    code.append("        vecY_Residual[i] := 0.0;")
    code.append("        vecU_Current[i] := 0.0;")
    code.append("        vecU_Optimal[i] := 0.0;")
    code.append("        vecU_Prev[i] := 0.0;")
    code.append("        vecDisturbance[i] := 0.0;")
    code.append("    END_FOR;")

    code.append("")
    code.append("    (* Baseline State Reference Setpoints *)")
    code.append("    vecX_Ref[1] := 22.5;    (* Target Permeate Flux J = 22.5 LMH *)")
    code.append("    vecX_Ref[2] := -180.0;  (* Target Permeate Suction Pressure = -180 mbar *)")
    code.append("    vecX_Ref[3] := 150.0;   (* Target Baseline TMP = 150 mbar *)")
    code.append("    vecX_Ref[4] := 12.0;    (* Target Dynamic Cake Resistance = 12.0 * 10^11 m^-1 *)")
    code.append("    vecX_Ref[5] := 2.0;     (* Target Aeration Basin DO = 2.0 mg/L *)")
    code.append("    vecX_Ref[6] := 10000.0; (* Target Basin MLSS = 10,000 mg/L *)")
    code.append("    vecX_Ref[7] := 4.5;     (* Target Nitrate NO3-N = 4.5 mg/L *)")
    code.append("    vecX_Ref[8] := 3200.0;  (* Target Scour Air Flow = 3,200 Nm3/h *)")

    code.append("")
    code.append("    bInitialized := TRUE;")
    code.append("END_IF;")
    return "\n".join(code)
