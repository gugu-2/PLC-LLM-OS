# cz_builder/cz_phase2.py

def get_phase2():
    lines = []
    lines.append("(* === PHASE 2: STATE-SPACE PREDICTION (x[k+1] = A*x[k] + B*u[k]) === *)")
    lines.append("(* Executes multiphysics modeling of Stefan phase boundary, capillary meniscus optics, *)")
    lines.append("(* Voronkov point defect incorporation, and discrete 12-state system propagation.        *)")
    lines.append("")
    lines.append("(* 2.1 Meniscus Capillary Optics & Laplace-Young Equation *)")
    lines.append("rCalculatedMeniscusHeight_mm := 4.50 + (0.015 * (rVotedMeniscusDiam_mm - 300.0)) - (0.008 * (rActualPullSpeed_mmpm - 1.10));")
    lines.append("IF rCalculatedMeniscusHeight_mm < 1.0 THEN rCalculatedMeniscusHeight_mm := 1.0; END_IF;")
    lines.append("IF rCalculatedMeniscusHeight_mm > 8.0 THEN rCalculatedMeniscusHeight_mm := 8.0; END_IF;")
    lines.append("rMeniscusHeight_mm := rCalculatedMeniscusHeight_mm;")
    lines.append("")
    lines.append("(* Dynamic growth contact angle derivation *)")
    lines.append("rCalculatedGrowthAngle_deg := 11.0 + ((180.0 / rConst_Pi) * (rCalculatedMeniscusHeight_mm - 4.50) / rConst_CapillaryConst_mm);")
    lines.append("IF rCalculatedGrowthAngle_deg < 0.0 THEN rCalculatedGrowthAngle_deg := 0.0; END_IF;")
    lines.append("IF rCalculatedGrowthAngle_deg > 85.0 THEN rCalculatedGrowthAngle_deg := 85.0; END_IF;")
    lines.append("rMeniscusGrowthAngle_deg := rCalculatedGrowthAngle_deg;")
    lines.append("")
    lines.append("(* Radial growth velocity based on contact angle mismatch *)")
    lines.append("rRadialGrowthRate_mmpm := rActualPullSpeed_mmpm * TAN((rCalculatedGrowthAngle_deg - 11.0) * rConst_Pi / 180.0);")
    lines.append("")
    lines.append("(* Filtered solid crystal diameter estimate *)")
    lines.append("rEstimatedCrystalDiameter_mm := rVotedMeniscusDiam_mm - (2.0 * rCalculatedMeniscusHeight_mm * COS(rCalculatedGrowthAngle_deg * rConst_Pi / 180.0));")
    lines.append("IF rEstimatedCrystalDiameter_mm < 0.0 THEN rEstimatedCrystalDiameter_mm := 0.0; END_IF;")
    lines.append("")
    lines.append("(* 2.2 Stefan Solidification Phase Boundary Latent Heat *)")
    lines.append("rSolidificationRate_kgs := (rConst_RhoSolid_kgm3 * (0.25 * rConst_Pi * rEstimatedCrystalDiameter_mm * rEstimatedCrystalDiameter_mm * 1.0E-6) * (rActualPullSpeed_mmpm / 60000.0));")
    lines.append("rLatentHeatRelease_kW := (rSolidificationRate_kgs * rConst_LatentHeat_Jkg) / 1000.0;")
    lines.append("")
    lines.append("(* Axial thermal gradient G0 at interface *)")
    lines.append("rAxialGradient_Kcm := 35.0 - (0.045 * (rEstimatedCrystalDiameter_mm - 300.0)) - (0.025 * (rVotedMeltTemp_DegC - 1414.0));")
    lines.append("IF rAxialGradient_Kcm < 10.0 THEN rAxialGradient_Kcm := 10.0; END_IF;")
    lines.append("rAxialThermalGradient_Kcm := rAxialGradient_Kcm;")
    lines.append("")
    lines.append("(* 2.3 Voronkov Ratio Calculation: xi = v_pull / G0 *)")
    lines.append("IF rAxialGradient_Kcm > 1.0 THEN")
    lines.append("    rVoronkovRatio_vG := (rActualPullSpeed_mmpm / 10.0) / (rAxialGradient_Kcm * 0.1); (* [mm2/(min*K)] *)")
    lines.append("ELSE")
    lines.append("    rVoronkovRatio_vG := 0.220;")
    lines.append("END_IF;")
    lines.append("")
    lines.append("bVoronkovRatioOutOfBounds := (rVoronkovRatio_vG < rConst_VoronkovMin_mm2minK) OR (rVoronkovRatio_vG > rConst_VoronkovMax_mm2minK);")
    lines.append("")
    lines.append("(* 2.4 Mass Continuity & Crucible Level Kinematics *)")
    lines.append("rCumulativeMass_kg := rCumulativeMass_kg + (rSolidificationRate_kgs * rCycleTime_sec);")
    lines.append("rCrystalMass_kg := rCumulativeMass_kg;")
    lines.append("rRemainingMeltMass_kg := rInitialPolyCharge_kg - rCumulativeMass_kg;")
    lines.append("IF rRemainingMeltMass_kg < 0.0 THEN rRemainingMeltMass_kg := 0.0; END_IF;")
    lines.append("rMeltRemaining_kg := rRemainingMeltMass_kg;")
    lines.append("")
    lines.append("(* Melt level drop velocity due to silicon mass extraction *)")
    lines.append("rMeltLevelDropVelocity_mmpm := rActualPullSpeed_mmpm * (rConst_RhoSolid_kgm3 / rConst_RhoLiquid_kgm3) *")
    lines.append("                              ((rEstimatedCrystalDiameter_mm * rEstimatedCrystalDiameter_mm) /")
    lines.append("                               ((rConst_CrucibleRadius_mm * 2.0 * rConst_CrucibleRadius_mm * 2.0) - (rEstimatedCrystalDiameter_mm * rEstimatedCrystalDiameter_mm) + 1.0));")
    lines.append("rCrucibleLiftError_mm := 0.0 - rVotedMeltLevel_mm;")
    lines.append("rEstimatedMeltLevel_mm := rVotedMeltLevel_mm;")
    lines.append("")
    lines.append("(* 2.5 Explicit Population of Discrete 12x12 System Matrix A (Ts = 0.10 s) *)")

    # Generate A matrix (12x12)
    A = [[0.0 for _ in range(12)] for _ in range(12)]
    # Default diagonal
    for i in range(12):
        A[i][i] = 0.9900
    A[0][0] = 0.9850; A[0][1] = 0.0420; A[0][2] = 0.1250; A[0][3] = -0.0150; A[0][9] = -0.0080
    A[1][0] = 0.0025; A[1][1] = 0.9780; A[1][2] = 0.0350; A[1][3] = -0.0045; A[1][9] = 0.0120
    A[2][0] = 0.0120; A[2][1] = 0.0850; A[2][2] = 0.9620; A[2][3] = -0.0220; A[2][9] = 0.0150
    A[3][0] = -0.0005; A[3][3] = 0.9820; A[3][4] = 0.0120; A[3][5] = 0.0040; A[3][8] = 0.0018
    A[4][3] = 0.0085; A[4][4] = 0.9750; A[4][5] = 0.0065; A[4][6] = 0.0055; A[4][7] = 0.0045; A[4][8] = 0.0040
    A[5][5] = 0.9680; A[5][8] = 0.0120
    A[6][6] = 0.9650; A[6][8] = 0.0150
    A[7][7] = 0.9720; A[7][8] = 0.0180
    A[8][4] = 0.0020; A[8][5] = 0.0050; A[8][6] = 0.0060; A[8][7] = 0.0040; A[8][8] = 0.9830
    A[9][0] = -0.0015; A[9][9] = 0.9950
    A[10][0] = -0.0045; A[10][3] = -0.0025; A[10][10] = 0.9880
    A[11][0] = 0.0085; A[11][11] = 1.0000

    for i in range(12):
        row_str = " ".join([f"aMatrix_A[{i+1},{j+1}] := {A[i][j]:.4f};" for j in range(12)])
        lines.append(row_str)

    lines.append("")
    lines.append("(* 2.6 Explicit Population of Discrete 12x8 Input Matrix B *)")
    B = [[0.0 for _ in range(8)] for _ in range(12)]
    B[0][0] = -0.0450; B[0][1] = 0.0000; B[0][2] = -0.0085; B[0][3] = -0.0065; B[0][4] = -0.0035; B[0][5] = 0.0012; B[0][6] = -0.0008; B[0][7] = 0.0005
    B[1][0] = -0.0120; B[1][1] = 0.0050; B[1][2] = -0.0025; B[1][3] = -0.0018; B[1][4] = -0.0008; B[1][5] = 0.0004; B[1][6] = -0.0002; B[1][7] = 0.0002
    B[2][0] = -0.0280; B[2][1] = 0.0080; B[2][2] = -0.0055; B[2][3] = -0.0040; B[2][4] = -0.0015; B[2][5] = 0.0008; B[2][6] = -0.0005; B[2][7] = 0.0004
    B[3][0] = 0.0150;  B[3][1] = 0.0000; B[3][2] = 0.0220;  B[3][3] = 0.0180;  B[3][4] = 0.0095;  B[3][5] = -0.0015; B[3][6] = 0.0010;  B[3][7] = -0.0012
    B[4][0] = 0.0050;  B[4][1] = 0.0000; B[4][2] = 0.0350;  B[4][3] = 0.0420;  B[4][4] = 0.0280;  B[4][5] = -0.0025; B[4][6] = 0.0020;  B[4][7] = -0.0008
    B[5][0] = 0.0000;  B[5][1] = 0.0000; B[5][2] = 0.0850;  B[5][3] = 0.0150;  B[5][4] = 0.0050;  B[5][5] = 0.0000;  B[5][6] = 0.0000;  B[5][7] = -0.0025
    B[6][0] = 0.0000;  B[6][1] = 0.0000; B[6][2] = 0.0180;  B[6][3] = 0.0920;  B[6][4] = 0.0120;  B[6][5] = 0.0000;  B[6][6] = 0.0000;  B[6][7] = -0.0018
    B[7][0] = 0.0000;  B[7][1] = 0.0000; B[7][2] = 0.0050;  B[7][3] = 0.0150;  B[7][4] = 0.1150;  B[7][5] = 0.0000;  B[7][6] = 0.0000;  B[7][7] = -0.0005
    B[8][0] = 0.0000;  B[8][1] = 0.0000; B[8][2] = 0.0250;  B[8][3] = 0.0320;  B[8][4] = 0.0280;  B[8][5] = -0.0010; B[8][6] = 0.0015;  B[8][7] = -0.0010
    B[9][0] = -0.0035; B[9][1] = 0.0095; B[9][2] = 0.0000;  B[9][3] = 0.0000;  B[9][4] = 0.0000;  B[9][5] = 0.0000;  B[9][6] = 0.0000;  B[9][7] = 0.0000
    B[10][0] = -0.0120; B[10][1] = 0.0000; B[10][2] = -0.0150; B[10][3] = -0.0120; B[10][4] = -0.0060; B[10][5] = 0.0015; B[10][6] = -0.0010; B[10][7] = 0.0008
    B[11][0] = 0.0450; B[11][1] = 0.0000; B[11][2] = 0.0000;  B[11][3] = 0.0000;  B[11][4] = 0.0000;  B[11][5] = 0.0000;  B[11][6] = 0.0000;  B[11][7] = 0.0000

    for i in range(12):
        row_str = " ".join([f"aMatrix_B[{i+1},{j+1}] := {B[i][j]:.4f};" for j in range(8)])
        lines.append(row_str)

    lines.append("")
    lines.append("(* 2.7 Load Current State Vector x[k] *)")
    lines.append("aState_x[1] := rEstimatedCrystalDiameter_mm - 300.0;")
    lines.append("aState_x[2] := rCalculatedMeniscusHeight_mm - 4.50;")
    lines.append("aState_x[3] := rCalculatedGrowthAngle_deg - 11.0;")
    lines.append("aState_x[4] := rVotedMeltTemp_DegC - 1414.0;")
    lines.append("aState_x[5] := rVotedMeltTemp_DegC + 15.0; (* Bulk melt estimate *)")
    lines.append("aState_x[6] := 1485.0; (* Upper heater core temp *)")
    lines.append("aState_x[7] := 1495.0; (* Lower heater core temp *)")
    lines.append("aState_x[8] := 1460.0; (* Bottom heater core temp *)")
    lines.append("aState_x[9] := rVotedCrucibleTemp_DegC;")
    lines.append("aState_x[10] := rVotedMeltLevel_mm;")
    lines.append("aState_x[11] := rAxialGradient_Kcm;")
    lines.append("aState_x[12] := rCumulativeMass_kg;")
    lines.append("")
    lines.append("(* Load Actuator Control Vector u[k] *)")
    lines.append("aControl_u[1] := rActualPullSpeed_mmpm;")
    lines.append("aControl_u[2] := rActualCrucibleLift_mmpm;")
    lines.append("aControl_u[3] := rUpperHeaterPowerDemand_kW;")
    lines.append("aControl_u[4] := rLowerHeaterPowerDemand_kW;")
    lines.append("aControl_u[5] := rBottomHeaterPowerDemand_kW;")
    lines.append("aControl_u[6] := rActualSeedRotation_rpm;")
    lines.append("aControl_u[7] := rActualCrucibleRotation_rpm;")
    lines.append("aControl_u[8] := rActualArgonInletFlow_slpm;")
    lines.append("")
    lines.append("(* 2.8 Explicit Unrolled State Propagation: x[k+1] = A * x[k] + B * u[k] *)")

    for i in range(12):
        term_A = " + ".join([f"(aMatrix_A[{i+1},{j+1}] * aState_x[{j+1}])" for j in range(12)])
        term_B = " + ".join([f"(aMatrix_B[{i+1},{j+1}] * aControl_u[{j+1}])" for j in range(8)])
        lines.append(f"aState_x_next[{i+1}] := ({term_A}) +")
        lines.append(f"                      ({term_B});")

    return "\n".join(lines) + "\n"
