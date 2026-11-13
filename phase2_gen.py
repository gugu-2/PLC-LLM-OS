# Phase 2 generator: State Space Model
import os

def generate_phase2_state_space():
    lines = []
    lines.append("(* ========================================================================= *)")
    lines.append("(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION           *)")
    lines.append("(* Discrete formulation at Ts = 0.050 s: x[k+1] = A*x[k] + B*u[k] + E*d[k]   *)")
    lines.append("(* ========================================================================= *)")
    lines.append("")
    lines.append("IF NOT bStateSpaceInitialized THEN")
    lines.append("    (* --- Matrix A (8x8) State Transition Matrix Coefficients --- *)")
    
    # Define A matrix elements with comments
    a_coeffs = [
        # row 1: x1 = SAG Total Charge Mass [t]
        [(1,1, "0.99972", "Ore charge mass retention per 50ms scan"),
         (1,2, "0.00145", "Internal slurry holdup mass coupling"),
         (1,3, "0.00010", "Toe angle shift effect on active charge retention"),
         (1,4, "-0.000008", "Mechanical power attrition breakage mass loss rate"),
         (1,5, "0.000000", "Decoupled from sump level"),
         (1,6, "0.000000", "Decoupled from overflow density"),
         (1,7, "0.000085", "Recycled pebble pebble load re-entry"),
         (1,8, "0.000000", "Decoupled from overflow P80")],
        # row 2: x2 = SAG Slurry Volumetric Holdup [m3]
        [(2,1, "0.00018", "Ore water content and fine slurry generation from charge"),
         (2,2, "0.99850", "Slurry volume retention vs pulp lifter discharge kinetics"),
         (2,3, "-0.00035", "Toe angle dilation altering pulp lifter submergence"),
         (2,4, "-0.000012", "Grinding energy slurry evaporation and slurry fluidization"),
         (2,5, "0.000000", "Decoupled from sump inventory"),
         (2,6, "0.000000", "Decoupled from overflow density"),
         (2,7, "0.000000", "Decoupled from circulating load"),
         (2,8, "0.000000", "Decoupled from product P80")],
        # row 3: x3 = Dynamic Charge Toe Impact Angle [deg]
        [(3,1, "0.00350", "Charge mass increment raising dynamic shoulder/toe angle"),
         (3,2, "-0.01250", "Slurry pool cushioning reducing charge friction and toe lift"),
         (3,3, "0.99200", "Charge rotational inertia angle relaxation damping"),
         (3,4, "0.00015", "Electromagnetic torque transmission to charge shoulder"),
         (3,5, "0.000000", "Decoupled from sump level"),
         (3,6, "0.000000", "Decoupled from overflow density"),
         (3,7, "0.000000", "Decoupled from circulating load"),
         (3,8, "0.000000", "Decoupled from product P80")],
        # row 4: x4 = 28 MW GMD Active Power Draw [kW]
        [(4,1, "4.25000", "Hogg-Fuerstenau power draw gradient per tonne of charge"),
         (4,2, "-18.5000", "Belly slurry pool cushioning effect lowering active power"),
         (4,3, "112.5000", "Charge center-of-gravity lift angle torque demand"),
         (4,4, "0.98500", "GMD stator field electrical time constant decay"),
         (4,5, "0.000000", "Decoupled from sump level"),
         (4,6, "0.000000", "Decoupled from overflow density"),
         (4,7, "0.000000", "Decoupled from circulating load"),
         (4,8, "0.000000", "Decoupled from product P80")],
        # row 5: x5 = Cyclone Feed Sump Slurry Level [%]
        [(5,1, "0.00025", "SAG mill rock discharge fraction into sump"),
         (5,2, "0.01520", "Pulp lifter volumetric slurry outflow entering sump"),
         (5,3, "0.000000", "Decoupled from toe angle"),
         (5,4, "0.000000", "Decoupled from GMD power"),
         (5,5, "0.99750", "Sump tank volumetric liquid holdup retention"),
         (5,6, "0.000000", "Decoupled from overflow density"),
         (5,7, "0.00065", "Ball mill discharge slurry entering sump closed circuit"),
         (5,8, "0.000000", "Decoupled from product P80")],
        # row 6: x6 = Cyclone Overflow Slurry Density [t/m3]
        [(6,1, "0.000000", "Decoupled from SAG charge"),
         (6,2, "0.000000", "Decoupled from SAG slurry"),
         (6,3, "0.000000", "Decoupled from toe angle"),
         (6,4, "0.000000", "Decoupled from GMD power"),
         (6,5, "0.00045", "Sump hydrostatic suction head effect on feed pump delivery"),
         (6,6, "0.99400", "Hydrocyclone manifold classification separation dynamics"),
         (6,7, "0.000015", "Ball mill fine grind slurry recirculating through cyclone"),
         (6,8, "-0.00030", "Product particle size correlation with overflow solids pct")],
        # row 7: x7 = Ball Mill Circulating Load [t/h]
        [(7,1, "0.000000", "Decoupled from SAG charge"),
         (7,2, "0.000000", "Decoupled from SAG slurry"),
         (7,3, "0.000000", "Decoupled from toe angle"),
         (7,4, "0.000000", "Decoupled from GMD power"),
         (7,5, "0.12500", "Sump discharge rate driving cyclone underflow coarse yield"),
         (7,6, "12.5000", "Slurry density effect on cyclone apex classification split"),
         (7,7, "0.99100", "Ball mill residence time dynamic inventory retention"),
         (7,8, "0.000000", "Decoupled from product P80")],
        # row 8: x8 = Final Product Particle Size P80 [um]
        [(8,1, "0.000000", "Decoupled from SAG charge"),
         (8,2, "0.000000", "Decoupled from SAG slurry"),
         (8,3, "0.000000", "Decoupled from toe angle"),
         (8,4, "0.000000", "Decoupled from GMD power"),
         (8,5, "0.00250", "Sump flow rate disturbance on hydrocyclone cut size d50c"),
         (8,6, "1.45000", "Overflow slurry viscosity hindering fine particle settling"),
         (8,7, "0.00380", "High circulating load coarser cyclone overflow carryover"),
         (8,8, "0.99600", "Austin comminution kinetics fine product retention")]
    ]
    for row in a_coeffs:
        for r, c, val, comment in row:
            lines.append(f"    aMatrix_A[{r},{c}] := {val}; (* {comment} *)")
    lines.append("")

    # Matrix B (8x8) Control Input Gain Matrix
    lines.append("    (* --- Matrix B (8x8) Control Input Gain Matrix Coefficients --- *)")
    b_coeffs = [
        # row 1: x1 = SAG Total Charge Mass [t]
        [(1,1, "0.000278", "Fresh ore feed addition: 1 t/h / 3600s * 0.05s"),
         (1,2, "0.000014", "Water mass addition to charge holdup"),
         (1,3, "-0.015000", "Mill speed centrifugal acceleration discharge enhancement"),
         (1,4, "0.000000", "Decoupled from cyclone pump"),
         (1,5, "0.000000", "Decoupled from sump water"),
         (1,6, "0.000000", "Decoupled from cyclone valve count"),
         (1,7, "0.000120", "Pebble crusher recycle returning to SAG feed chute"),
         (1,8, "0.000000", "Decoupled from ball mill water")],
        # row 2: x2 = SAG Slurry Volumetric Holdup [m3]
        [(2,1, "0.000028", "Ore interstitial moisture addition"),
         (2,2, "0.0000139", "SAG feed dilution water addition: 1 m3/h / 3600s * 0.05s"),
         (2,3, "-0.008500", "Mill speed increasing pulp lifter scooping frequency"),
         (2,4, "0.000000", "Decoupled from cyclone pump"),
         (2,5, "0.000000", "Decoupled from sump water"),
         (2,6, "0.000000", "Decoupled from cyclone valve count"),
         (2,7, "0.000000", "Decoupled from pebble recycle"),
         (2,8, "0.000000", "Decoupled from ball mill water")],
        # row 3: x3 = Dynamic Charge Toe Impact Angle [deg]
        [(3,1, "0.001200", "Fresh rock feed expanding kidney charge toe"),
         (3,2, "-0.002500", "Dilution water lowering internal charge dynamic friction"),
         (3,3, "0.450000", "Mill rotational speed lifting charge to higher cataracting angle"),
         (3,4, "0.000000", "Decoupled from cyclone pump"),
         (3,5, "0.000000", "Decoupled from sump water"),
         (3,6, "0.000000", "Decoupled from cyclone valve count"),
         (3,7, "0.000500", "Hard crushed pebble recycle elevating charge shoulder"),
         (3,8, "0.000000", "Decoupled from ball mill water")],
        # row 4: x4 = 28 MW GMD Active Power Draw [kW]
        [(4,1, "1.850000", "Fresh feed tonnage increasing gravity torque arm"),
         (4,2, "-0.850000", "Dilution water fluidizing charge and easing rotational torque"),
         (4,3, "245.0000", "GMD speed setpoint direct drive mechanical power scaling"),
         (4,4, "0.000000", "Decoupled from cyclone pump"),
         (4,5, "0.000000", "Decoupled from sump water"),
         (4,6, "0.000000", "Decoupled from cyclone valve count"),
         (4,7, "0.450000", "Recycled pebbles raising grinding media charge volume"),
         (4,8, "0.000000", "Decoupled from ball mill water")],
        # row 5: x5 = Cyclone Feed Sump Slurry Level [%]
        [(5,1, "0.000000", "Decoupled directly from fresh ore"),
         (5,2, "0.000150", "SAG mill dilution water flushing through grates into sump"),
         (5,3, "0.003500", "SAG speed pulp lifter discharge surge into sump"),
         (5,4, "-0.018500", "Cyclone feed slurry pump speed drawing sump inventory down"),
         (5,5, "0.000694", "Sump dilution water addition: 1 m3/h / 200m3 * 0.05s"),
         (5,6, "0.000000", "Decoupled directly from cyclone count"),
         (5,7, "0.000000", "Decoupled from pebble recycle"),
         (5,8, "0.000120", "Ball mill dilution water draining into sump closed circuit")],
        # row 6: x6 = Cyclone Overflow Slurry Density [t/m3]
        [(6,1, "0.000000", "Decoupled from fresh ore"),
         (6,2, "0.000000", "Decoupled from SAG water"),
         (6,3, "0.000000", "Decoupled from SAG speed"),
         (6,4, "0.000120", "Cyclone pump speed increasing inlet velocity and separation force"),
         (6,5, "-0.000045", "Sump dilution water thinning cyclone feed and overflow slurry"),
         (6,6, "-0.002800", "Opening cyclone knife gate lowering inlet velocity and pressure"),
         (6,7, "0.000000", "Decoupled from pebble recycle"),
         (6,8, "-0.000015", "Ball mill water dilution effect")],
        # row 7: x7 = Ball Mill Circulating Load [t/h]
        [(7,1, "0.000000", "Decoupled from fresh ore"),
         (7,2, "0.000000", "Decoupled from SAG water"),
         (7,3, "0.000000", "Decoupled from SAG speed"),
         (7,4, "0.450000", "Cyclone pump speed delivering more coarse mass to underflow"),
         (7,5, "-0.180000", "Sump dilution shifting cyclone split towards overflow"),
         (7,6, "-8.500000", "More active cyclones lowering underflow solids discharge"),
         (7,7, "0.000000", "Decoupled from pebble recycle"),
         (7,8, "-0.050000", "Ball mill water accelerating slurry flow through ball mill")],
        # row 8: x8 = Final Product Particle Size P80 [um]
        [(8,1, "0.000800", "Fresh ore throughput coarsening circuit grind size"),
         (8,2, "0.000000", "Decoupled from SAG water"),
         (8,3, "-0.050000", "SAG speed increasing impact breakage and fine generation"),
         (8,4, "0.025000", "High cyclone pump speed coarsening cut size d50c"),
         (8,5, "-0.015000", "Sump dilution improving hydrocyclone sharpness of separation"),
         (8,6, "0.850000", "More cyclones lowering header pressure and coarsening cut size"),
         (8,7, "0.005000", "Pebble recycle volume displacing fresh fine grinding"),
         (8,8, "-0.008000", "Ball mill water optimization improving Austin grinding kinetics")]
    ]
    for row in b_coeffs:
        for r, c, val, comment in row:
            lines.append(f"    aMatrix_B[{r},{c}] := {val}; (* {comment} *)")
    lines.append("")

    # Matrix C (8x8) Measurement Output Matrix
    lines.append("    (* --- Matrix C (8x8) Output Matrix Coefficients (Identity Mapping + Cross-Coupling) --- *)")
    for r in range(1, 9):
        for c in range(1, 9):
            if r == c:
                lines.append(f"    aMatrix_C[{r},{c}] := 1.000000; (* Direct unity state observation *)")
            else:
                lines.append(f"    aMatrix_C[{r},{c}] := 0.000000;")
    lines.append("")

    # Matrix D (8x8) Direct Feedthrough Matrix
    lines.append("    (* --- Matrix D (8x8) Direct Feedthrough Matrix (Zero Direct Feedthrough) --- *)")
    for r in range(1, 9):
        for c in range(1, 9):
            lines.append(f"    aMatrix_D[{r},{c}] := 0.000000;")
    lines.append("")

    # Matrix E (8x2) Disturbance Matrix
    lines.append("    (* --- Matrix E (8x2) Geological & Bulk Density Disturbance Matrix --- *)")
    e_coeffs = [
        (1, 1, "0.00450", "Ore hardness Bond Work Index increasing rock retention in charge"),
        (1, 2, "0.08500", "Bulk density fluctuation shifting charge mass reading"),
        (2, 1, "-0.00120", "Hard ore slower fine slurry creation rate"),
        (2, 2, "0.00000", "Decoupled from bulk density"),
        (3, 1, "0.00850", "Harder competency rocks rolling higher up liner lifters"),
        (3, 2, "0.00250", "Density shift moving dynamic center-of-gravity"),
        (4, 1, "48.5000", "High Bond Work Index requiring increased grinding torque and power"),
        (4, 2, "12.5000", "Higher bulk density demanding increased mechanical lift power"),
        (5, 1, "0.00000", "Decoupled from hardness"),
        (5, 2, "0.00000", "Decoupled from density"),
        (6, 1, "0.00050", "Hard ore fines altered rheology in cyclone overflow"),
        (6, 2, "0.00200", "Bulk density slurry specific gravity feed variation"),
        (7, 1, "1.25000", "Hard ore producing more pebbles and higher ball mill circulating load"),
        (7, 2, "0.00000", "Decoupled from density"),
        (8, 1, "0.15000", "High Bond Work Index directly coarsening final product P80"),
        (8, 2, "0.00000", "Decoupled from density")
    ]
    for r, c, val, comment in e_coeffs:
        lines.append(f"    aMatrix_E[{r},{c}] := {val}; (* {comment} *)")
    lines.append("")

    # Observer Gain Matrix L (8 elements)
    lines.append("    (* --- Luenberger Observer Innovation Gain Vector L --- *)")
    l_gains = [
        (1, "0.0450", "Charge mass estimator innovation gain"),
        (2, "0.0380", "Internal slurry holdup innovation gain"),
        (3, "0.0850", "Toe angle estimator innovation gain"),
        (4, "0.1250", "GMD power draw innovation gain"),
        (5, "0.0950", "Sump level filter innovation gain"),
        (6, "0.0650", "Cyclone overflow density innovation gain"),
        (7, "0.0550", "Circulating load innovation gain"),
        (8, "0.0420", "Product P80 analyzer innovation gain")
    ]
    for idx, val, comment in l_gains:
        lines.append(f"    aObserverGain_L[{idx}] := {val}; (* {comment} *)")
    lines.append("")

    # Initialize State Space Initial Conditions
    lines.append("    (* Initial state values at nominal comminution operating point *)")
    lines.append("    aState_x[1] := 1850.0; (* [t] SAG Total Dynamic Charge *)")
    lines.append("    aState_x[2] := 18.50;  (* [m3] SAG Slurry Volumetric Holdup *)")
    lines.append("    aState_x[3] := 52.00;  (* [deg] Dynamic Toe Angle *)")
    lines.append("    aState_x[4] := 23500.0;(* [kW] 28 MW GMD Active Power Draw *)")
    lines.append("    aState_x[5] := 55.00;  (* [%] Cyclone Feed Sump Slurry Level *)")
    lines.append("    aState_x[6] := 1.280;  (* [t/m3] Cyclone Overflow Slurry Density *)")
    lines.append("    aState_x[7] := 1650.0; (* [t/h] Ball Mill Circulating Load *)")
    lines.append("    aState_x[8] := 75.00;  (* [um] Product Particle Size P80 *)")
    lines.append("")
    lines.append("    bStateSpaceInitialized := TRUE;")
    lines.append("END_IF;")
    lines.append("")

    # Evaluate Disturbances
    lines.append("(* Evaluate Feedstock Geological Disturbances *)")
    lines.append("aDisturbance_d[1] := rBondWorkIndex_Estimated - 14.50; (* Deviation from baseline 14.5 kWh/t *)")
    lines.append("aDisturbance_d[2] := rOreFeedBulkDensity - 2.65;       (* Deviation from baseline 2.65 t/m3 *)")
    lines.append("")

    # Observer Innovation Calculation
    lines.append("(* Formulate Measured Output Vector from 2oo3 Voted & Process Transducers *)")
    lines.append("aOutput_y_meas[1] := (rFeedTrunnion_Voted + rDischTrunnion_Voted) * 14.25; (* Total charge estimate from trunnions [t] *)")
    lines.append("aOutput_y_meas[2] := rSlurryPoolVolume_Observed;                         (* Dynamic observer slurry pool [m3] *)")
    lines.append("aOutput_y_meas[3] := 38.0 + (rShellAcoustic_Voted * 0.32);               (* Toe angle mapped from acoustic profile [deg] *)")
    lines.append("aOutput_y_meas[4] := rGMDPower_Voted;                                    (* 28 MW GMD power [kW] *)")
    lines.append("aOutput_y_meas[5] := rSumpLevel_Voted;                                   (* Cyclone sump level [%] *)")
    lines.append("aOutput_y_meas[6] := 1.0 + (rCycloneDensity_Voted - 1.0) * 0.44;         (* Cyclone overflow density [t/m3] *)")
    lines.append("aOutput_y_meas[7] := rPebbleRecycleMassFlow * 3.85;                      (* Circulating load estimate [t/h] *)")
    lines.append("aOutput_y_meas[8] := rCycloneOverflowP80;                                (* On-line particle size P80 [um] *)")
    lines.append("")
    lines.append("(* Compute Innovation Residuals e = y_meas - C*x *)")
    for i in range(1, 9):
        lines.append(f"aInnovation_e[{i}] := aOutput_y_meas[{i}] - aOutput_y[{i}];")
    lines.append("")

    # Unrolled State Propagation
    lines.append("(* Explicit Term-by-Term Discrete State Propagation x[k+1] = A*x[k] + B*u[k] + E*d[k] + L*e[k] *)")
    for i in range(1, 9):
        terms_a = " + ".join([f"aMatrix_A[{i},{j}] * aState_x[{j}]" for j in range(1, 9)])
        terms_b = " + ".join([f"aMatrix_B[{i},{j}] * aControl_u[{j}]" for j in range(1, 9)])
        terms_e = f"aMatrix_E[{i},1] * aDisturbance_d[1] + aMatrix_E[{i},2] * aDisturbance_d[2]"
        terms_l = f"aObserverGain_L[{i}] * aInnovation_e[{i}]"
        lines.append(f"aState_x_next[{i}] := {terms_a} +")
        lines.append(f"                    {terms_b} +")
        lines.append(f"                    {terms_e} + {terms_l};")
        lines.append("")

    # State Bound Saturation Checks (Physical Constraints)
    lines.append("(* Apply First-Principles Physical Saturation Envelopes on Propagated States *)")
    lines.append("aState_x[1] := LIMIT(950.0, aState_x_next[1], 2550.0);   (* SAG charge [t]: 950 to 2550 *)")
    lines.append("aState_x[2] := LIMIT(2.0, aState_x_next[2], 55.0);       (* Slurry pool [m3]: 2 to 55 *)")
    lines.append("aState_x[3] := LIMIT(25.0, aState_x_next[3], 72.0);      (* Toe angle [deg]: 25 to 72 *)")
    lines.append("aState_x[4] := LIMIT(1500.0, aState_x_next[4], 28500.0); (* GMD power [kW]: 1.5MW to 28.5MW *)")
    lines.append("aState_x[5] := LIMIT(5.0, aState_x_next[5], 100.0);      (* Sump level [%]: 5 to 100 *)")
    lines.append("aState_x[6] := LIMIT(1.05, aState_x_next[6], 1.65);      (* Overflow density [t/m3]: 1.05 to 1.65 *)")
    lines.append("aState_x[7] := LIMIT(200.0, aState_x_next[7], 4000.0);   (* Circulating load [t/h]: 200 to 4000 *)")
    lines.append("aState_x[8] := LIMIT(35.0, aState_x_next[8], 140.0);     (* Overflow P80 [um]: 35 to 140 *)")
    lines.append("")

    # Output Vector Computation
    lines.append("(* Compute Measurement Output Vector y = C*x + D*u *)")
    for i in range(1, 9):
        terms_c = " + ".join([f"aMatrix_C[{i},{j}] * aState_x[{j}]" for j in range(1, 9)])
        lines.append(f"aOutput_y[{i}] := {terms_c};")
    lines.append("")

    return "\n".join(lines)

print("Phase 2 generator written.")
