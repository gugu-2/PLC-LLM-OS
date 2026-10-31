# euv_builder/euv_phase2.py

def get_phase2():
    lines = []
    lines.append("(* === PHASE 2: STATE-SPACE PREDICTION (x[k+1] = A*x[k] + B*u[k]) === *)")
    lines.append("(* Multiphysics modeling of Rayleigh acoustic breakup, pre-pulse laser pancake hydrodynamics, *)")
    lines.append("(* atomic plasma ionization, Mo/Si collector mirror thermal conduction, and H2 chemical stannane etch. *)")
    lines.append("")

    # 2.1 Multiphysics calculations
    lines.append("(* 2.1 Droplet Generation Aerodynamics & Rayleigh-Plateau Capillary Breakup *)")
    lines.append("rRayleighWavelength_um := (rVotedDropletVel_mps * 1000.0) / (rTargetPiezoFreq_kHz * 1000.0) * 1000.0;")
    lines.append("rDropletMass_ug := (rConst_TinDensity_kgm3 * (4.0 / 3.0) * rConst_Pi * ((rVotedDropletDiam_um * 0.5 * 1.0E-6) * (rVotedDropletDiam_um * 0.5 * 1.0E-6) * (rVotedDropletDiam_um * 0.5 * 1.0E-6))) * 1.0E9;")
    lines.append("rDropletPosJitterCalc_um := SQRT((rVotedDropletX_um * rVotedDropletX_um) + (rVotedDropletY_um * rVotedDropletY_um));")
    lines.append("rDropletPosJitter_um := rDropletPosJitterCalc_um;")
    lines.append("")

    lines.append("(* 2.2 Pre-Pulse Droplet Ablation Shock & Pancake Disc Expansion *)")
    lines.append("rEstimatedPancakeDiam_um := rVotedDropletDiam_um * (1.0 + (8.5 * (rTargetPrePulse_mJ / 25.0) * (rTargetInterPulseDelay_us / 2.80)));")
    lines.append("IF rEstimatedPancakeDiam_um < 30.0 THEN rEstimatedPancakeDiam_um := 30.0; END_IF;")
    lines.append("IF rEstimatedPancakeDiam_um > 350.0 THEN rEstimatedPancakeDiam_um := 350.0; END_IF;")
    lines.append("rPancakeDiameter_um := rEstimatedPancakeDiam_um;")
    lines.append("")

    lines.append("(* 2.3 CO2 Main-Pulse Laser Plasma Ionization & Electron Temperature *)")
    lines.append("rCalculatedTe_eV := 32.0 + (5.5 * (rTargetMainPulse_J - 0.95)) - (0.8 * (rVotedVesselPressure_Pa - 3.5));")
    lines.append("IF rCalculatedTe_eV < 10.0 THEN rCalculatedTe_eV := 10.0; END_IF;")
    lines.append("IF rCalculatedTe_eV > 60.0 THEN rCalculatedTe_eV := 60.0; END_IF;")
    lines.append("rCalculatedNe_cm3 := rConst_CriticalDensityCO2_cm3 * (0.85 + (0.35 * (rEstimatedPancakeDiam_um / 200.0)));")
    lines.append("")

    lines.append("(* 2.4 In-Band 13.5 nm EUV Emission & Intermediate Focus (IF) Collection *)")
    lines.append("rCalculatedPlasmaEUV_W := 1420.0 * (rCalculatedTe_eV / 34.0) * (rTargetMainPulse_J / 0.95) * (rEstimatedPancakeDiam_um / 210.0);")
    lines.append("rCalculatedIFEUV_W := rCalculatedPlasmaEUV_W * 0.355 * (1.0 - (0.015 * (rVotedVesselPressure_Pa - 3.5)));")
    lines.append("IF (rTargetMainPulse_J > 0.1) THEN")
    lines.append("    rCalculatedCE_Pct := (rCalculatedPlasmaEUV_W / (rConst_NominalRepRate_Hz * (rTargetMainPulse_J + (rTargetPrePulse_mJ * 0.001)))) * 100.0;")
    lines.append("ELSE")
    lines.append("    rCalculatedCE_Pct := 0.0;")
    lines.append("END_IF;")
    lines.append("rConversionEfficiency_Pct := rCalculatedCE_Pct;")
    lines.append("rMeasuredEUVPower_IF_W := rVotedIFEUVPower_W;")
    lines.append("")

    lines.append("(* 2.5 Mo/Si Collector Mirror Thermal Diffusion & Stannane (SnH4) Chemical Debris Etching *)")
    lines.append("rCalculatedEtchRate_nms := 0.045 * (rTargetH2Flow_slpm / 150.0) * (rVotedVesselPressure_Pa / 3.5) * (1.0 + (0.01 * (rVotedMirrorCenterTemp_DegC - 60.0)));")
    lines.append("rStannaneEtchRate_nms := rCalculatedEtchRate_nms;")
    lines.append("rCollectorCenterTemp_DegC := rVotedMirrorCenterTemp_DegC;")
    lines.append("rCollectorMidTemp_DegC := rVotedMirrorMidTemp_DegC;")
    lines.append("rVesselVacuum_Pa := rVotedVesselPressure_Pa;")
    lines.append("rDropletFrequency_kHz := rTargetPiezoFreq_kHz;")
    lines.append("rDropletVelocity_mps := rVotedDropletVel_mps;")
    lines.append("rDropletDiameter_um := rVotedDropletDiam_um;")
    lines.append("")

    lines.append("(* 2.6 Explicit Assignment of Discrete 16x16 System State Matrix A (Ts = 0.010 s) *)")
    # Generate A matrix assignments
    # A is 16x16
    for i in range(1, 17):
        row_str = []
        for j in range(1, 17):
            if i == j:
                # Diagonal dominant stable discrete poles
                val = 0.9500 + ((i % 5) * 0.0080)
            elif (i == 1 and j == 6) or (i == 2 and j == 7):
                val = 0.0450
            elif (i == 4 and j == 3):
                val = 0.0120
            elif (i == 6 and j == 4):
                val = 0.0250
            elif (i == 7 and j == 6):
                val = 0.0180
            elif (i == 9 and j == 7):
                val = 0.0850
            elif (i == 10 and j == 9):
                val = 0.3550
            elif (i == 11 and j == 9):
                val = 0.0125
            elif (i == 12 and j == 11):
                val = 0.0350
            elif (i == 13 and j == 12):
                val = 0.0280
            elif (i == 15 and j == 9):
                val = 0.0650
            elif (i == 16 and j == 14):
                val = 0.0420
            elif (i == 15 and j == 14):
                val = -0.0520
            elif (i == 10 and j == 14):
                val = -0.0150
            else:
                val = 0.0000
            row_str.append(f"aMatrix_A[{i},{j}] := {val:.4f};")
        lines.append(" ".join(row_str))

    lines.append("")
    lines.append("(* 2.7 Explicit Assignment of Discrete 16x8 Input Coupling Matrix B *)")
    # Generate B matrix assignments
    # B is 16x8
    for i in range(1, 17):
        row_str = []
        for j in range(1, 8+1):
            val = 0.0000
            if i == 1 and j == 6:   # X pos vs Steer X
                val = 0.1250
            elif i == 2 and j == 7: # Y pos vs Steer Y
                val = 0.1250
            elif i == 4 and j == 3: # Velocity vs Reservoir Pressure
                val = 0.2850
            elif i == 4 and j == 1: # Velocity vs Piezo Freq
                val = 0.0450
            elif i == 5 and j == 2: # Diameter vs Piezo Voltage
                val = 0.0320
            elif i == 6 and j == 4: # Pancake vs PrePulse
                val = 4.8500
            elif i == 7 and j == 5: # Te vs MainPulse
                val = 8.5000
            elif i == 8 and j == 5: # Ne vs MainPulse
                val = 0.2200
            elif i == 9 and j == 5: # Plasma EUV vs MainPulse
                val = 450.0000
            elif i == 9 and j == 4: # Plasma EUV vs PrePulse
                val = 18.5000
            elif i == 10 and j == 5: # IF EUV vs MainPulse
                val = 160.0000
            elif i == 11 and j == 5: # Collector Center Temp vs MainPulse
                val = 0.0850
            elif i == 14 and j == 8: # Vessel Pressure vs H2 Flow
                val = 0.0350
            elif i == 15 and j == 8: # Sn Ion Flux vs H2 Flow
                val = -0.1450
            elif i == 16 and j == 8: # SnH4 Etch Rate vs H2 Flow
                val = 0.0085
            row_str.append(f"aMatrix_B[{i},{j}] := {val:.4f};")
        lines.append(" ".join(row_str))

    lines.append("")
    lines.append("(* 2.8 Discrete State Vector Propagation (x[k+1] = A * x[k] + B * u[k]) *)")
    for i in range(1, 17):
        a_terms = " + ".join([f"(aMatrix_A[{i},{j}] * aState_x[{j}])" for j in range(1, 17)])
        b_terms = " + ".join([f"(aMatrix_B[{i},{j}] * aControl_u[{j}])" for j in range(1, 8+1)])
        lines.append(f"aState_x_next[{i}] := ({a_terms}) + ({b_terms});")

    lines.append("")
    lines.append("(* Update state trajectory for next execution scan *)")
    for i in range(1, 17):
        lines.append(f"aState_x[{i}] := aState_x_next[{i}];")

    lines.append("")
    return "\n".join(lines)
