def get_matrices_code():
    lines = []
    lines.append("(* ============================================================================================= *)")
    lines.append("(* SECTION 1: FIRST-SCAN INITIALIZATION & DISCRETE STATE-SPACE / MPC ARRAYS                     *)")
    lines.append("(* ============================================================================================= *)")
    lines.append("IF NOT bFirstScanDone THEN")
    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    lines.append("    (* 1.1 Discrete State-Space Transition Matrix A (16x16) Discretized at Ts = 2.0 ms            *)")
    lines.append("    (* States: x[1..4]=Angle Errors, x[5..8]=Vel Errors, x[9..12]=Torque Currents, x[13..16]=Vac *)")
    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    
    # Generate A matrix (16x16)
    for i in range(1, 17):
        for j in range(1, 17):
            val = 0.0
            # Diagonals
            if i == j:
                if 1 <= i <= 4:
                    val = 0.998240
                elif 5 <= i <= 8:
                    val = 0.985420
                elif 9 <= i <= 12:
                    val = 0.912500
                elif 13 <= i <= 16:
                    val = 0.894200
            # Kinematic integration x_dot = v
            elif (1 <= i <= 4) and (j == i + 4):
                val = 0.001980
            # Acceleration from motor current
            elif (5 <= i <= 8) and (j == i + 4):
                val = 0.012450
            # Back-EMF dampening on current
            elif (9 <= i <= 12) and (j == i - 4):
                val = -0.004210
            # Cross-coupling between adjacent delta robots (gantry flex & DC bus)
            elif (i == 5 and j == 6) or (i == 6 and j == 5):
                val = 0.000350
            elif (i == 6 and j == 7) or (i == 7 and j == 6):
                val = 0.000350
            elif (i == 7 and j == 8) or (i == 8 and j == 7):
                val = 0.000350
            elif (i == 9 and j == 10) or (i == 10 and j == 9):
                val = 0.000180
            elif (i == 10 and j == 11) or (i == 11 and j == 10):
                val = 0.000180
            elif (i == 11 and j == 12) or (i == 12 and j == 11):
                val = 0.000180
            
            lines.append(f"    arrA[{i}, {j}] := {val:.6f};")

    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    lines.append("    (* 1.2 Discrete Input Coupling Matrix B (16x8)                                              *)")
    lines.append("    (* Inputs: u[1..4]=Motor Torques [Nm], u[5..8]=Vacuum Ejector Valve Duty [0.0..1.0]         *)")
    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    for i in range(1, 17):
        for j in range(1, 9):
            val = 0.0
            if (9 <= i <= 12) and (j == i - 8):
                val = 0.084500 # Current drive gain
            elif (13 <= i <= 16) and (j == i - 8):
                val = -9.542000 # Negative gauge pressure buildup gain
            lines.append(f"    arrB[{i}, {j}] := {val:.6f};")

    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    lines.append("    (* 1.3 Discrete Output Measurement Matrix C (16x16)                                         *)")
    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    for i in range(1, 17):
        for j in range(1, 17):
            val = 1.000000 if i == j else 0.000000
            lines.append(f"    arrC[{i}, {j}] := {val:.6f};")

    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    lines.append("    (* 1.4 Direct Feedthrough Matrix D (16x8)                                                   *)")
    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    for i in range(1, 17):
        for j in range(1, 9):
            val = 0.000000
            lines.append(f"    arrD[{i}, {j}] := {val:.6f};")

    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    lines.append("    (* 1.5 MPC State Penalty Weighting Matrix Q (16x16)                                         *)")
    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    for i in range(1, 17):
        for j in range(1, 17):
            val = 0.0
            if i == j:
                if 1 <= i <= 4:
                    val = 250.000000 # Joint position error penalty
                elif 5 <= i <= 8:
                    val = 45.000000  # Velocity overshoot penalty
                elif 9 <= i <= 12:
                    val = 2.500000   # Motor current penalty
                elif 13 <= i <= 16:
                    val = 85.000000  # Vacuum pressure deviation penalty
            lines.append(f"    arrQ[{i}, {j}] := {val:.6f};")

    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    lines.append("    (* 1.6 MPC Actuator Effort Penalty Weighting Matrix R (8x8)                                 *)")
    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    for i in range(1, 9):
        for j in range(1, 9):
            val = 0.0
            if i == j:
                if 1 <= i <= 4:
                    val = 0.150000 # Motor torque smoothness penalty
                elif 5 <= i <= 8:
                    val = 0.085000 # Vacuum valve switching life penalty
            lines.append(f"    arrR[{i}, {j}] := {val:.6f};")

    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    lines.append("    (* 1.7 MPC Terminal State Riccati Penalty Matrix P (16x16)                                  *)")
    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    for i in range(1, 17):
        for j in range(1, 17):
            val = 0.0
            if i == j:
                if 1 <= i <= 4:
                    val = 520.000000 # Terminal position error penalty
                elif 5 <= i <= 8:
                    val = 95.000000  # Terminal velocity penalty
                elif 9 <= i <= 12:
                    val = 5.000000
                elif 13 <= i <= 16:
                    val = 140.000000
            lines.append(f"    arrP[{i}, {j}] := {val:.6f};")

    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    lines.append("    (* 1.8 Initialize In-Line Optical Line-Scan 64-Package Circular Tracking Buffer             *)")
    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    lines.append("    FOR iIdx := 1 TO 64 DO")
    lines.append("        arrPkg_ID[iIdx] := 0;")
    lines.append("        arrPkg_X_Entry[iIdx] := 0.0;")
    lines.append("        arrPkg_Y_Entry[iIdx] := 0.0;")
    lines.append("        arrPkg_Theta_Entry[iIdx] := 0.0;")
    lines.append("        arrPkg_EncSnapshot[iIdx] := 0;")
    lines.append("        arrPkg_State[iIdx] := 0; (* 0 = Empty slot *)")
    lines.append("        arrPkg_Defect[iIdx] := FALSE;")
    lines.append("        arrPkg_AssignedRobot[iIdx] := 0;")
    lines.append("    END_FOR;")
    lines.append("    iQueueHead := 1;")
    lines.append("    iQueueTail := 1;")
    lines.append("    iQueueCount := 0;")
    lines.append("")
    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    lines.append("    (* 1.9 Initialize Secondary RSC Corrugated Case 4x6 Collation Pocket Grid                   *)")
    lines.append("    (* ----------------------------------------------------------------------------------------- *)")
    lines.append("    FOR iIdx := 1 TO 4 DO")
    lines.append("        FOR jIdx := 1 TO 6 DO")
    lines.append("            arrCaseGrid_Occupied[iIdx, jIdx] := FALSE;")
    lines.append("        END_FOR;")
    lines.append("    END_FOR;")
    lines.append("    iCaseCurrentUnits := 0;")
    lines.append("    iCaseTargetUnits := 24;")
    lines.append("    bCartonFullReadyToDischarge := FALSE;")
    lines.append("")
    lines.append("    (* Initial Home Coordinates for Delta Robots *)")
    lines.append("    lrR1_TCP_X := 0.0; lrR1_TCP_Y := 0.0; lrR1_TCP_Z := -520.0; lrR1_TCP_Theta := 0.0;")
    lines.append("    lrR2_TCP_X := 0.0; lrR2_TCP_Y := 0.0; lrR2_TCP_Z := -520.0; lrR2_TCP_Theta := 0.0;")
    lines.append("    lrR3_TCP_X := 0.0; lrR3_TCP_Y := 0.0; lrR3_TCP_Z := -520.0; lrR3_TCP_Theta := 0.0;")
    lines.append("    lrR4_TCP_X := 0.0; lrR4_TCP_Y := 0.0; lrR4_TCP_Z := -520.0; lrR4_TCP_Theta := 0.0;")
    lines.append("")
    lines.append("    bFirstScanDone := TRUE;")
    lines.append("END_IF;")
    lines.append("")
    return "\n".join(lines)

