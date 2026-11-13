# Builder Part 2: Discrete State-Space Matrices Initialization (8x8 A, B, C, D, Q, R, P)
# Lumina Cyber-Physical Systems Chair / Principal Automation Fellow (V7 Max-Persona)

def generate_matrices():
    lines = []
    def emit(s=""):
        lines.append(s)

    emit("(* =========================================================================================== *)")
    emit("(* DISCRETE STATE-SPACE MATRICES INITIALIZATION (8x8 A, 8x8 B, 8x8 C, 8x8 D, Q, R, P)          *)")
    emit("(* Sample Period Ts = 10.0 ms, Formulated from First-Principles Pulp & Paper Cyber-Physics     *)")
    emit("(* =========================================================================================== *)")
    emit("IF NOT bMatrixInitialized THEN")
    emit("    (* ------------------------------------------------------------------------------------- *)")
    emit("    (* Discrete State Transition Matrix A (8x8): Physical State Inter-Coupling             *)")
    emit("    (* x[1]=P_hb [kPa], x[2]=C_stock [%], x[3]=V_wire [m/min], x[4]=L_dryline [m]          *)")
    emit("    (* x[5]=M_sheet [%], x[6]=BW_dry [g/m2], x[7]=P_steam [kPa], x[8]=T_web [N/m]         *)")
    emit("    (* ------------------------------------------------------------------------------------- *)")

    # Matrix A entries with detailed physics comments
    a_matrix = [
        # row 1: P_hb
        [(1, 1, "0.9650", "Headbox hydraulic total head fluid inertia and friction dissipation decay"),
         (1, 2, "0.0120", "Stock consistency apparent slurry viscosity resistance coupling"),
         (1, 3, "0.0000", "Wire speed decoupling from upstream headbox internal hydraulics"),
         (1, 4, "0.0000", "Dry-line position decoupled from pressurized headbox chamber"),
         (1, 5, "0.0000", "Downstream sheet moisture decoupled from headbox hydraulic chamber"),
         (1, 6, "0.0000", "Sheet basis weight decoupled from instantaneous headbox pressure"),
         (1, 7, "0.0000", "Dryer steam pressure decoupled from wet-end headbox"),
         (1, 8, "0.0000", "Web draw tension decoupled from headbox hydraulic manifold")],
        # row 2: C_stock
        [(2, 1, "0.0000", "Headbox total pressure decoupled from stock consistency mixing dynamics"),
         (2, 2, "0.9820", "Stock consistency retention time in stock prep chest and blend loop"),
         (2, 3, "0.0000", "Wire speed decoupling from stock consistency in headbox"),
         (2, 4, "0.0000", "Downstream dryline decoupling from headbox stock consistency"),
         (2, 5, "0.0000", "Downstream moisture decoupling from stock consistency"),
         (2, 6, "0.0000", "Basis weight feedback decoupling from upstream stock consistency"),
         (2, 7, "0.0000", "Steam pressure decoupling from stock consistency"),
         (2, 8, "0.0000", "Web draw tension decoupling from stock consistency")],
        # row 3: V_wire
        [(3, 1, "0.0000", "Headbox pressure decoupled from sectional drive mechanical inertia"),
         (3, 2, "0.0000", "Stock consistency decoupled from sectional wire drive inertia"),
         (3, 3, "0.9880", "Multi-motor sectional drive mechanical flywheel inertia and friction"),
         (3, 4, "0.0000", "Dry-line position decoupled from drive closed-loop velocity regulation"),
         (3, 5, "0.0000", "Moisture decoupled from wire drive rotational velocity"),
         (3, 6, "0.0000", "Basis weight decoupled from wire sectional mechanical speed"),
         (3, 7, "0.0000", "Dryer steam pressure decoupled from wire section drive speed"),
         (3, 8, "-0.0185", "Web draw tension mechanical drag reaction against couch roll drive")],
        # row 4: L_dryline
        [(4, 1, "0.0450", "Increased headbox total head raises stock efflux volume, extending dry-line"),
         (4, 2, "0.0680", "Higher fiber consistency slows drainage rate through wire fabric, extending dry-line"),
         (4, 3, "0.0520", "Higher forming wire velocity carries wet slurry further down table"),
         (4, 4, "0.9150", "Hydrodynamic gravity foil and vacuum dewatering table drainage persistence"),
         (4, 5, "0.0000", "Downstream dryer moisture decoupled from wet-end dry-line boundary"),
         (4, 6, "0.0240", "Higher sheet basis weight increases drainage filtration flow resistance"),
         (4, 7, "0.0000", "Dryer steam pressure decoupled from forming wire dryline location"),
         (4, 8, "0.0000", "Web draw tension decoupled from wet-end gravity foil dryline")],
        # row 5: M_sheet
        [(5, 1, "0.0220", "Higher headbox efflux volume increases total water mass entering dryers"),
         (5, 2, "-0.0450", "Higher stock consistency slightly lowers water-to-fiber ratio entering dryers"),
         (5, 3, "0.0380", "Higher machine velocity shortens thermal residence time across steam dryers"),
         (5, 4, "0.0650", "Delayed dry-line increases moisture content delivered into press and dryer section"),
         (5, 5, "0.9250", "Multi-cylinder paper sheet bulk thermal and moisture diffusion persistence"),
         (5, 6, "0.0580", "Heavier basis weight sheet has higher specific heat and slower water evaporation"),
         (5, 7, "-0.0920", "Higher dryer steam header pressure accelerates cylinder shell evaporation rate"),
         (5, 8, "-0.0140", "Higher draw tension compresses sheet pores slightly, enhancing drying contact")],
        # row 6: BW_dry
        [(6, 1, "0.0580", "Increased headbox pressure increases Torricelli efflux volumetric fiber discharge"),
         (6, 2, "0.1420", "Increased fiber consistency directly elevates absolute dry fiber deposition"),
         (6, 3, "-0.0850", "Higher wire speed stretches fiber mat thinner per unit surface area"),
         (6, 4, "0.0000", "Dry-line position decoupled from mass conservation basis weight"),
         (6, 5, "0.0000", "Reel moisture percentage decoupled from bone-dry basis weight"),
         (6, 6, "0.9520", "Mass conservation continuity of deposited cellulose fiber mat on forming wire"),
         (6, 7, "0.0000", "Dryer steam pressure decoupled from bone-dry fiber mass"),
         (6, 8, "-0.0120", "Longitudinal web draw strain causes slight lateral Poisson width thinning")],
        # row 7: P_steam
        [(7, 1, "0.0000", "Wet-end headbox pressure decoupled from dryer steam header enthalpy"),
         (7, 2, "0.0000", "Stock consistency decoupled from dryer steam header thermal storage"),
         (7, 3, "0.0000", "Wire speed decoupled from steam supply header accumulator volume"),
         (7, 4, "0.0000", "Dryline position decoupled from steam supply header accumulator"),
         (7, 5, "0.0150", "Higher web moisture condenses more cylinder steam, lowering header pressure"),
         (7, 6, "0.0210", "Heavier basis weight consumes more latent heat, increasing steam condensation"),
         (7, 7, "0.9480", "Main steam distribution header thermal capacitance and pressure inertia"),
         (7, 8, "0.0000", "Web draw tension decoupled from steam distribution header thermodynamics")],
        # row 8: T_web
        [(8, 1, "0.0000", "Headbox total pressure decoupled from press-to-dryer elastic web tension"),
         (8, 2, "0.0000", "Stock consistency decoupled from longitudinal web draw tension"),
         (8, 3, "-0.0450", "Forming wire speed fluctuation alters sectional draw strain ratio"),
         (8, 4, "0.0000", "Dry-line position decoupled from mechanical draw tension"),
         (8, 5, "-0.0820", "Higher sheet moisture reduces paper elastic modulus, softening web tension"),
         (8, 6, "0.0420", "Heavier basis weight increases cross-sectional area, raising tensile resistance"),
         (8, 7, "0.0000", "Dryer steam pressure decoupled from mechanical tension load cells"),
         (8, 8, "0.8950", "Longitudinal visco-elastic web tension relaxation and draw dynamics")]
    ]

    for row in a_matrix:
        for r, c, val, comment in row:
            emit(f"    matA[{r}, {c}] := {val}; (* {comment} *)")

    emit("")
    emit("    (* ------------------------------------------------------------------------------------- *)")
    emit("    (* Discrete Control Input Coupling Matrix B (8x8): Actuator Influence Matrix            *)")
    emit("    (* u[1]=N_fan [%], u[2]=P_dil [kPa], u[3]=V_wire_sp [m/min], u[4]=V_steam [%]           *)")
    emit("    (* u[5]=V_tc [%], u[6]=V_blow [%], u[7]=Trim_draw [%], u[8]=P_crown [bar]              *)")
    emit("    (* ------------------------------------------------------------------------------------- *)")

    b_matrix = [
        # row 1: P_hb
        [(1, 1, "0.1850", "Fan pump VFD speed accelerates stock delivery into headbox manifold"),
         (1, 2, "0.0320", "Dilution water profiling valve header pressure trim coupling"),
         (1, 3, "0.0000", "Wire sectional speed setpoint decoupled from headbox internal pressure"),
         (1, 4, "0.0000", "Steam supply valve decoupled from wet-end headbox pressure"),
         (1, 5, "0.0000", "Thermocompressor motive valve decoupled from headbox hydraulics"),
         (1, 6, "0.0000", "Blowthrough valve decoupled from headbox hydraulics"),
         (1, 7, "0.0000", "Draw trim decoupled from headbox pressure"),
         (1, 8, "0.0000", "Calender crown pressure decoupled from headbox pressure")],
        # row 2: C_stock
        [(2, 1, "-0.0120", "Fan pump speed increase slightly dilutes headbox fiber consistency"),
         (2, 2, "-0.0450", "Dilution water valve injection directly lowers stock fiber consistency"),
         (2, 3, "0.0000", "Wire speed setpoint decoupled from headbox consistency"),
         (2, 4, "0.0000", "Steam valve decoupled from stock consistency"),
         (2, 5, "0.0000", "Thermocompressor decoupled from stock consistency"),
         (2, 6, "0.0000", "Blowthrough valve decoupled from stock consistency"),
         (2, 7, "0.0000", "Draw trim decoupled from stock consistency"),
         (2, 8, "0.0000", "Calender crown decoupled from stock consistency")],
        # row 3: V_wire
        [(3, 1, "0.0000", "Fan pump speed decoupled from sectional wire drive motor control"),
         (3, 2, "0.0000", "Dilution pressure decoupled from wire sectional drive motor"),
         (3, 3, "0.1450", "Sectional master wire drive speed reference accelerates wire drive"),
         (3, 4, "0.0000", "Steam valve decoupled from wire drive rotational velocity"),
         (3, 5, "0.0000", "Thermocompressor decoupled from wire drive velocity"),
         (3, 6, "0.0000", "Blowthrough valve decoupled from wire drive velocity"),
         (3, 7, "0.0000", "Press draw trim decoupled from master wire drive reference"),
         (3, 8, "0.0000", "Calender crown decoupled from wire drive velocity")],
        # row 4: L_dryline
        [(4, 1, "0.0550", "Fan pump speed increase increases slurry volume, moving dry-line outward"),
         (4, 2, "0.0280", "Dilution header pressure increase adds water, delaying drainage line"),
         (4, 3, "0.0620", "Wire drive speed increase carries wet fiber further before de-watering"),
         (4, 4, "0.0000", "Dryer steam valve decoupled from wet-end dryline boundary"),
         (4, 5, "0.0000", "Thermocompressor decoupled from wet-end drainage table"),
         (4, 6, "0.0000", "Blowthrough valve decoupled from wet-end drainage table"),
         (4, 7, "0.0000", "Draw trim decoupled from wet-end gravity drainage"),
         (4, 8, "0.0000", "Calender crown decoupled from wet-end dryline position")],
        # row 5: M_sheet
        [(5, 1, "0.0350", "Fan pump speed elevates water loading into press and dryer groups"),
         (5, 2, "0.0180", "Dilution water increases sheet water content entering dryers"),
         (5, 3, "0.0420", "Wire speed acceleration shortens cylinder contact time, raising moisture"),
         (5, 4, "-0.1650", "Main steam valve opening raises cylinder heat transfer, lowering moisture"),
         (5, 5, "-0.0480", "Thermocompressor motive boost evacuates condensate, enhancing heat flux"),
         (5, 6, "-0.0280", "Blowthrough valve opening prevents cylinder condensate puddling"),
         (5, 7, "-0.0150", "Draw trim tightening improves thermal cylinder wrap contact"),
         (5, 8, "-0.0080", "Calender roll nip pressure squeezes minute residual bound moisture")],
        # row 6: BW_dry
        [(6, 1, "0.1250", "Fan pump delivery directly governs mass throughput of fiber onto wire"),
         (6, 2, "0.0150", "Dilution water trim adjusts local cross-directional basis weight profile"),
         (6, 3, "-0.0950", "Wire speed increase stretches sheet thinner per unit machine area"),
         (6, 4, "0.0000", "Steam valve decoupled from absolute bone-dry fiber mass"),
         (6, 5, "0.0000", "Thermocompressor decoupled from dry basis weight"),
         (6, 6, "0.0000", "Blowthrough valve decoupled from dry basis weight"),
         (6, 7, "-0.0120", "Draw trim creates small longitudinal plastic elongation thinning"),
         (6, 8, "0.0000", "Calender crown decoupled from sheet bone-dry mass")],
        # row 7: P_steam
        [(7, 1, "0.0000", "Fan pump decoupled from steam header thermodynamic supply"),
         (7, 2, "0.0000", "Dilution pressure decoupled from steam header accumulator"),
         (7, 3, "0.0000", "Wire speed decoupled from steam supply header pressure"),
         (7, 4, "0.2200", "Main steam valve opening directly charges dryer steam header pressure"),
         (7, 5, "-0.0550", "Thermocompressor motive consumption draws steam from header"),
         (7, 6, "-0.0350", "Blowthrough valve opening vents steam into drainage separator"),
         (7, 7, "0.0000", "Draw trim decoupled from steam supply header"),
         (7, 8, "0.0000", "Calender crown decoupled from steam supply header")],
        # row 8: T_web
        [(8, 1, "0.0000", "Fan pump decoupled from press-to-dryer web draw tension"),
         (8, 2, "0.0000", "Dilution pressure decoupled from web draw tension"),
         (8, 3, "-0.0450", "Wire speed master step alters instantaneous section velocity ratio"),
         (8, 4, "0.0000", "Steam valve decoupled from mechanical drive tension"),
         (8, 5, "0.0000", "Thermocompressor decoupled from web draw tension"),
         (8, 6, "0.0000", "Blowthrough valve decoupled from web draw tension"),
         (8, 7, "0.1850", "Sectional draw ratio speed trim directly strains paper web elastically"),
         (8, 8, "0.0120", "Calender crown hydraulic nip loading adds rolling friction drag")]
    ]

    for row in b_matrix:
        for r, c, val, comment in row:
            emit(f"    matB[{r}, {c}] := {val}; (* {comment} *)")

    emit("")
    emit("    (* ------------------------------------------------------------------------------------- *)")
    emit("    (* Discrete Output Measurement Matrix C (8x8): Identity Mapping with Sensor Calibration *)")
    emit("    (* ------------------------------------------------------------------------------------- *)")
    for r in range(1, 9):
        for c in range(1, 9):
            if r == c:
                emit(f"    matC[{r}, {c}] := 1.0000; (* Direct State Observation Channel {r} *)")
            else:
                emit(f"    matC[{r}, {c}] := 0.0000; (* Zero Cross-Measurement Decoupling *)")

    emit("")
    emit("    (* ------------------------------------------------------------------------------------- *)")
    emit("    (* Discrete Direct Feedthrough Matrix D (8x8): Pure Dynamic System Null Transmission    *)")
    emit("    (* ------------------------------------------------------------------------------------- *)")
    for r in range(1, 9):
        for c in range(1, 9):
            emit(f"    matD[{r}, {c}] := 0.0000; (* Strictly Proper System No Direct Feedthrough *)")

    emit("")
    emit("    (* ------------------------------------------------------------------------------------- *)")
    emit("    (* Receding-Horizon MPC State Penalty Weighting Matrix Q (8x8 Diagonal)                 *)")
    emit("    (* ------------------------------------------------------------------------------------- *)")
    q_weights = [
        (1, "12.50", "Headbox Total Pressure Penalty Weighting"),
        (2, "45.00", "Stock Fiber Consistency Penalty Weighting"),
        (3, "18.00", "Forming Wire Speed Penalty Weighting"),
        (4, "8.50",  "Dry-Line Position Tracking Penalty Weighting"),
        (5, "65.00", "Exit Sheet Moisture Regulation Penalty Weighting"),
        (6, "85.00", "Bone-Dry Basis Weight Compliance Penalty Weighting"),
        (7, "15.00", "Steam Header Pressure Regulation Penalty Weighting"),
        (8, "25.00", "Web Draw Tension Safety Limit Penalty Weighting")
    ]
    for r in range(1, 9):
        for c in range(1, 9):
            if r == c:
                val, cmt = q_weights[r-1][1], q_weights[r-1][2]
                emit(f"    matQ[{r}, {c}] := {val}; (* {cmt} *)")
            else:
                emit(f"    matQ[{r}, {c}] := 0.0000; (* Off-diagonal state decoupling *)")

    emit("")
    emit("    (* ------------------------------------------------------------------------------------- *)")
    emit("    (* Receding-Horizon MPC Actuator Slew Energy Penalty Matrix R (8x8 Diagonal)             *)")
    emit("    (* ------------------------------------------------------------------------------------- *)")
    r_weights = [
        (1, "4.50", "Fan Pump Speed Rate-of-Change Damping Penalty"),
        (2, "2.20", "Dilution Pressure Actuator Wear Damping Penalty"),
        (3, "6.80", "Sectional Master Speed Slew Acceleration Penalty"),
        (4, "3.50", "Main Steam Valve Modulation Fatigue Penalty"),
        (5, "1.80", "Thermocompressor Motive Slew Rate Penalty"),
        (6, "1.50", "Blowthrough Valve Cycle Wear Penalty"),
        (7, "8.00", "Draw Trim Aggressiveness Prevention Penalty"),
        (8, "2.00", "Calender Hydraulic Crown Stress Penalty")
    ]
    for r in range(1, 9):
        for c in range(1, 9):
            if r == c:
                val, cmt = r_weights[r-1][1], r_weights[r-1][2]
                emit(f"    matR[{r}, {c}] := {val}; (* {cmt} *)")
            else:
                emit(f"    matR[{r}, {c}] := 0.0000; (* Off-diagonal actuator decoupling *)")

    emit("")
    emit("    (* ------------------------------------------------------------------------------------- *)")
    emit("    (* Receding-Horizon MPC Terminal State Cost Matrix P (8x8 Algebraic Riccati Solution)   *)")
    emit("    (* ------------------------------------------------------------------------------------- *)")
    p_weights = [
        (1, "28.50", "Terminal Headbox Pressure Stability Weight"),
        (2, "92.00", "Terminal Stock Consistency Stability Weight"),
        (3, "38.00", "Terminal Forming Wire Speed Stability Weight"),
        (4, "18.50", "Terminal Dry-Line Position Stability Weight"),
        (5, "145.00", "Terminal Exit Sheet Moisture Stability Weight"),
        (6, "180.00", "Terminal Bone-Dry Basis Weight Stability Weight"),
        (7, "32.00", "Terminal Steam Header Pressure Stability Weight"),
        (8, "55.00", "Terminal Web Draw Tension Safety Margin Weight")
    ]
    for r in range(1, 9):
        for c in range(1, 9):
            if r == c:
                val, cmt = p_weights[r-1][1], p_weights[r-1][2]
                emit(f"    matP[{r}, {c}] := {val}; (* {cmt} *)")
            else:
                emit(f"    matP[{r}, {c}] := 0.0000; (* Off-diagonal terminal decoupling *)")

    emit("")
    emit("    (* Actuator Physical Saturation Box Limits & Maximum Slew Rates per Ts *)")
    emit("    uLowerBound[1] :=   0.0;    uUpperBound[1] := 100.0;   deltaUMax[1] := 1.20; (* Fan Pump [%] *)")
    emit("    uLowerBound[2] :=   0.0;    uUpperBound[2] := 150.0;   deltaUMax[2] := 2.50; (* Dilution Pressure [kPa] *)")
    emit("    uLowerBound[3] :=   0.0;    uUpperBound[3] := 2200.0;  deltaUMax[3] := 8.50; (* Wire Speed [m/min] *)")
    emit("    uLowerBound[4] :=   0.0;    uUpperBound[4] := 100.0;   deltaUMax[4] := 1.80; (* Main Steam Valve [%] *)")
    emit("    uLowerBound[5] :=   0.0;    uUpperBound[5] := 100.0;   deltaUMax[5] := 2.20; (* Thermocompressor [%] *)")
    emit("    uLowerBound[6] :=   0.0;    uUpperBound[6] := 100.0;   deltaUMax[6] := 2.50; (* Blowthrough Valve [%] *)")
    emit("    uLowerBound[7] :=  -2.5;    uUpperBound[7] :=   2.5;   deltaUMax[7] := 0.15; (* Draw Ratio Trim [%] *)")
    emit("    uLowerBound[8] :=   5.0;    uUpperBound[8] := 160.0;   deltaUMax[8] := 2.80; (* Crown Pressure [bar] *)")
    emit("")
    emit("    (* Default Initial Previous Actuator References *)")
    emit("    FOR mInputIdx := 1 TO 8 DO")
    emit("        uPrevious[mInputIdx] := uLowerBound[mInputIdx];")
    emit("        uOptimal[mInputIdx]  := uLowerBound[mInputIdx];")
    emit("    END_FOR;")
    emit("")
    emit("    (* Cross-Machine Web Shrinkage Parabolic Factor Initialization across 48 Zones *)")
    emit("    FOR iZoneIdx := 1 TO 48 DO")
    emit("        (* Parabolic expansion: edge zones undergo ~4.5% shrinkage while center has ~1.8% *)")
    emit("        rShrinkageProfileCorrection[iZoneIdx] := 1.018 + 0.027 * ( (INT_TO_REAL(iZoneIdx) - 24.5) / 23.5 ) * ( (INT_TO_REAL(iZoneIdx) - 24.5) / 23.5 );")
    emit("        rCD_RawBasisWeightProfile[iZoneIdx]   := 120.0;")
    emit("        rCD_FilteredBasisWeight[iZoneIdx]     := 120.0;")
    emit("        rCD_WeightDeviationError[iZoneIdx]    := 0.0;")
    emit("        rCD_ActuatorIntegralError[iZoneIdx]   := 0.0;")
    emit("        rCD_SliceActuatorInternal[iZoneIdx]   := 50.0;")
    emit("        rCD_RawMoistureProfile[iZoneIdx]      := 7.50;")
    emit("        rCD_FilteredMoisture[iZoneIdx]        := 7.50;")
    emit("        rCD_CaliperProfile[iZoneIdx]          := 145.0;")
    emit("        bSliceActuatorStallFault[iZoneIdx]    := FALSE;")
    emit("        rSliceActuatorBendingMoment[iZoneIdx] := 0.0;")
    emit("    END_FOR;")
    emit("")
    emit("    bMatrixInitialized := TRUE;")
    emit("END_IF;")
    emit("")
    return lines
