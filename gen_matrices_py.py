# -*- coding: utf-8 -*-
"""
gen_matrices_py.py
Generates the vial_filler_matrices.py file with completely unrolled 16x16 A, 16x8 B, 8x16 C, 8x8 D,
16x16 Q, 8x8 R, 16x16 P, and 16x8 L matrices with detailed cyber-physical commentary.
"""

def generate():
    lines = []
    lines.append('# -*- coding: utf-8 -*-')
    lines.append('"""')
    lines.append('vial_filler_matrices.py')
    lines.append('Contains unrolled cyber-physical state-space matrices initialization for FB_Pharma_AsepticVialFilling_600VPM_Checkweigh.')
    lines.append('"""')
    lines.append('')
    lines.append('def get_matrices_code():')
    lines.append('    return """(* ========================================================================================= *)')
    lines.append('(* SECTION 0: DISCRETE STATE-SPACE MATRICES INITIALIZATION (16x16 A, 16x8 B, 8x16 C, 8x8 D) *)')
    lines.append('(* ========================================================================================= *)')
    lines.append('IF NOT bMatricesInitialized THEN')
    lines.append('    (* --- 16x16 Dynamic State Matrix A (Continuous-to-Discrete ZOH at Ts = 0.001 s) --- *)')

    # State names for physical commentary
    state_names = [
        "Starwheel angular position error [deg]",
        "Starwheel angular velocity error [deg/s]",
        "Diving needle carriage vertical position [mm]",
        "Diving needle carriage vertical velocity [mm/s]",
        "Peristaltic tubing manifold fluid pressure [bar]",
        "Liquid meniscus column velocity inside needle [mm/s]",
        "Dispensed liquid volume accumulated in active vial [ml]",
        "Vial liquid surface rising velocity [mm/s]",
        "Tare EMFR load cell restoring beam deflection [um]",
        "Tare EMFR load cell voice-coil feedback current [mA]",
        "Gross EMFR load cell restoring beam deflection [um]",
        "Gross EMFR load cell voice-coil feedback current [mA]",
        "Grade A isolator differential pressure [Pa]",
        "Nitrogen headspace purge gas manifold pressure [bar]",
        "Rotary stoppering wheel vacuum manifold level [bar]",
        "Rotary crimper spindle dynamic compliance force [N]"
    ]

    input_names = [
        "Starwheel servo torque command [Nm]",
        "Diving needle linear motor force command [N]",
        "Peristaltic pump servo angle rate [rpm]",
        "Tare EMFR dynamic compensation current [mA]",
        "Gross EMFR dynamic compensation current [mA]",
        "Isolator supply blower VFD speed trim [%]",
        "Nitrogen purge valve proportional command [%]",
        "Crimp capper servo down-stroke preload command [mm]"
    ]

    output_names = [
        "Starwheel resolver position [deg]",
        "Diving needle linear encoder position [mm]",
        "Peristaltic fluid pressure [bar]",
        "Tare EMFR load cell dynamic reading [mg]",
        "Gross EMFR load cell dynamic reading [mg]",
        "Isolator differential pressure [Pa]",
        "Nitrogen headspace purge flow [L/min]",
        "Crimp capper dynamic sealing force [N]"
    ]

    # Generate A_Matrix (16x16)
    # Realistic diagonal and off-diagonal couplings
    for i in range(1, 17):
        for j in range(1, 17):
            val = 0.0
            comment = f"A[{i},{j}]: Coupling from state {j} to state {i}"
            if i == j:
                # Diagonal terms
                diag_vals = [
                    0.9982, 0.9850, 0.9990, 0.9820,
                    0.9450, 0.9620, 1.0000, 0.9540,
                    0.9200, 0.9150, 0.9200, 0.9150,
                    0.9880, 0.9650, 0.9720, 0.9400
                ]
                val = diag_vals[i-1]
                comment = f"A[{i},{j}]: Self-decay / inertia of {state_names[i-1]}"
            elif i == 1 and j == 2:
                val = 0.0010  # Ts * velocity -> position
                comment = "A[1,2]: Starwheel velocity integration into angle error"
            elif i == 2 and j == 1:
                val = -0.0045 # Torsional spring restoring
                comment = "A[2,1]: Turret drive mechanical torsional compliance restoring"
            elif i == 3 and j == 4:
                val = 0.0010  # Ts * velocity -> position
                comment = "A[3,4]: Diving needle servo velocity integration into vertical stroke"
            elif i == 4 and j == 3:
                val = -0.0082 # Guidance rail mechanical restoring
                comment = "A[4,3]: Needle linear carriage magnetic spring stiffness"
            elif i == 5 and j == 6:
                val = -0.0028 # Fluid outflow pressure drop
                comment = "A[5,6]: Meniscus fluid outflow pressure drop in peristaltic line"
            elif i == 6 and j == 5:
                val = 0.0345  # Pressure gradient driving fluid acceleration
                comment = "A[6,5]: Navier-Stokes hydraulic pressure gradient acceleration"
            elif i == 7 and j == 6:
                val = 0.00045 # Needle flow rate to vial volume
                comment = "A[7,6]: Needle fluid column velocity to dispensed vial volume"
            elif i == 8 and j == 6:
                val = 0.1250  # Ratio of needle bore area to vial inner cross section
                comment = "A[8,6]: Needle-to-vial hydraulic area continuity ratio"
            elif i == 9 and j == 10:
                val = -0.0065 # Tare voice-coil Lorentz restoring force
                comment = "A[9,10]: Tare EMFR voice-coil electromagnetic Lorentz counter-force"
            elif i == 10 and j == 9:
                val = 0.0450  # Tare position detector feedback current
                comment = "A[10,9]: Tare optical beam position photo-sensor feedback gain"
            elif i == 11 and j == 12:
                val = -0.0065 # Gross voice-coil Lorentz restoring force
                comment = "A[11,12]: Gross EMFR voice-coil electromagnetic Lorentz counter-force"
            elif i == 12 and j == 11:
                val = 0.0450  # Gross position detector feedback current
                comment = "A[12,11]: Gross optical beam position photo-sensor feedback gain"
            elif i == 13 and j == 14:
                val = 0.0015  # Nitrogen purge gas leakage into isolator volume
                comment = "A[13,14]: High-purity N2 purge gas bleeding into Grade A chamber"
            elif i == 15 and j == 1:
                val = 0.0002  # Starwheel indexing vibration to vacuum seal
                comment = "A[15,1]: Rotary starwheel kinematic jitter effect on vacuum seal"
            elif i == 16 and j == 3:
                val = 0.0055  # Needle carriage position thermal coupling to capping head
                comment = "A[16,3]: Monoblock baseplate thermal expansion dynamic coupling"

            lines.append(f"    A_Matrix[{i:2d}, {j:2d}] := {val:10.6f}; (* {comment} *)")

    lines.append('')
    lines.append('    (* --- 16x8 Input Coupling Matrix B --- *)')
    for i in range(1, 17):
        for j in range(1, 9):
            val = 0.0
            comment = f"B[{i},{j}]: Coupling from input {j} to state {i}"
            if i == 2 and j == 1:
                val = 0.0125
                comment = "B[2,1]: Starwheel servo torque to angular acceleration"
            elif i == 4 and j == 2:
                val = 0.0180
                comment = "B[4,2]: Diving carriage linear motor force to vertical acceleration"
            elif i == 5 and j == 3:
                val = 0.0420
                comment = "B[5,3]: Peristaltic pump RPM to tubing fluid manifold pressure"
            elif i == 6 and j == 3:
                val = 0.0850
                comment = "B[6,3]: Peristaltic pump displacement rate to needle liquid velocity"
            elif i == 10 and j == 4:
                val = 0.0550
                comment = "B[10,4]: Dynamic tare voice-coil current command coupling"
            elif i == 12 and j == 5:
                val = 0.0550
                comment = "B[12,5]: Dynamic gross voice-coil current command coupling"
            elif i == 13 and j == 6:
                val = 0.0380
                comment = "B[13,6]: Isolator blower VFD speed trim to chamber differential pressure"
            elif i == 14 and j == 7:
                val = 0.0620
                comment = "B[14,7]: Nitrogen proportional regulator valve to manifold pressure"
            elif i == 15 and j == 1:
                val = -0.0010
                comment = "B[15,1]: Rotary turret acceleration vacuum manifold transient"
            elif i == 16 and j == 8:
                val = 0.0780
                comment = "B[16,8]: Rotary capping servo down-stroke preload to crimp seal force"

            lines.append(f"    B_Matrix[{i:2d}, {j:2d}] := {val:10.6f}; (* {comment} *)")

    lines.append('')
    lines.append('    (* --- 8x16 Output Measurement Matrix C --- *)')
    for i in range(1, 9):
        for j in range(1, 17):
            val = 0.0
            comment = f"C[{i},{j}]: Output {i} projection from state {j}"
            if i == 1 and j == 1:
                val = 1.0000
                comment = "C[1,1]: Measured starwheel resolver angle from state 1"
            elif i == 2 and j == 3:
                val = 1.0000
                comment = "C[2,3]: Measured diving needle linear encoder from state 3"
            elif i == 3 and j == 5:
                val = 1.0000
                comment = "C[3,5]: Measured peristaltic manifold pressure from state 5"
            elif i == 4 and j == 10:
                val = 125.0000
                comment = "C[4,10]: Tare EMFR load cell dynamic reading from voice-coil mA"
            elif i == 5 and j == 12:
                val = 125.0000
                comment = "C[5,12]: Gross EMFR load cell dynamic reading from voice-coil mA"
            elif i == 6 and j == 13:
                val = 1.0000
                comment = "C[6,13]: Isolator differential pressure reading from state 13"
            elif i == 7 and j == 14:
                val = 4.1100
                comment = "C[7,14]: Nitrogen purge flow from manifold pressure state 14"
            elif i == 8 and j == 16:
                val = 1.0000
                comment = "C[8,16]: Rotary crimp capper dynamic sealing force from state 16"

            lines.append(f"    C_Matrix[{i:2d}, {j:2d}] := {val:10.6f}; (* {comment} *)")

    lines.append('')
    lines.append('    (* --- 8x8 Direct Feedthrough Transmission Matrix D --- *)')
    for i in range(1, 9):
        for j in range(1, 9):
            val = 0.0
            comment = f"D[{i},{j}]: Feedthrough from input {j} to output {i}"
            if i == 7 and j == 7:
                val = 0.0150
                comment = "D[7,7]: Direct acoustic orifice feedthrough on N2 regulator step"
            elif i == 8 and j == 8:
                val = 0.0250
                comment = "D[8,8]: Direct piezoelectric impact compliance feedthrough"

            lines.append(f"    D_Matrix[{i:2d}, {j:2d}] := {val:10.6f}; (* {comment} *)")

    lines.append('')
    lines.append('    (* --- 16x16 State Error Penalty Matrix Q (Diagonal) --- *)')
    for i in range(1, 17):
        for j in range(1, 17):
            val = 0.0
            comment = f"Q[{i},{j}]: Off-diagonal cross-state penalty"
            if i == j:
                diag_q = [
                    50.0, 10.0, 80.0, 15.0,
                    25.0, 30.0, 150.0, 40.0,
                    20.0, 60.0, 20.0, 60.0,
                    100.0, 45.0, 35.0, 75.0
                ]
                val = diag_q[i-1]
                comment = f"Q[{i},{j}]: Penalty weight for {state_names[i-1]}"
            lines.append(f"    Q_Weight[{i:2d}, {j:2d}] := {val:10.6f}; (* {comment} *)")

    lines.append('')
    lines.append('    (* --- 8x8 Actuator Slew Rate Penalty Matrix R (Diagonal) --- *)')
    for i in range(1, 9):
        for j in range(1, 9):
            val = 0.0
            comment = f"R[{i},{j}]: Actuator cross-coupling penalty"
            if i == j:
                diag_r = [
                    5.0, 8.0, 12.0, 2.5,
                    2.5, 4.0, 3.0, 6.0
                ]
                val = diag_r[i-1]
                comment = f"R[{i},{j}]: Actuator energy/slew penalty for {input_names[i-1]}"
            lines.append(f"    R_Weight[{i:2d}, {j:2d}] := {val:10.6f}; (* {comment} *)")

    lines.append('')
    lines.append('    (* --- 16x16 Terminal Riccati Algebraic Cost Matrix P --- *)')
    for i in range(1, 17):
        for j in range(1, 17):
            val = 0.0
            comment = f"P[{i},{j}]: Terminal cross-cost"
            if i == j:
                diag_p = [
                    120.0, 25.0, 180.0, 35.0,
                    55.0, 65.0, 350.0, 90.0,
                    45.0, 140.0, 45.0, 140.0,
                    220.0, 95.0, 80.0, 160.0
                ]
                val = diag_p[i-1]
                comment = f"P[{i},{j}]: Terminal Riccati weight for {state_names[i-1]}"
            elif abs(i - j) == 1:
                val = 2.5000
                comment = f"P[{i},{j}]: Terminal Lyapunov coupling between states {i} and {j}"
            lines.append(f"    P_Weight[{i:2d}, {j:2d}] := {val:10.6f}; (* {comment} *)")

    lines.append('')
    lines.append('    (* --- 16x8 Steady-State Kalman Observer Gain Matrix L --- *)')
    for i in range(1, 17):
        for j in range(1, 9):
            val = 0.0
            comment = f"L[{i},{j}]: Kalman observer innovation gain"
            if i == 1 and j == 1:
                val = 0.2850
                comment = "L[1,1]: Angular position error innovation correction"
            elif i == 2 and j == 1:
                val = 0.1420
                comment = "L[2,1]: Angular velocity innovation from resolver"
            elif i == 3 and j == 2:
                val = 0.3100
                comment = "L[3,2]: Diving carriage position innovation"
            elif i == 4 and j == 2:
                val = 0.1650
                comment = "L[4,2]: Diving carriage velocity innovation"
            elif i == 5 and j == 3:
                val = 0.2450
                comment = "L[5,3]: Peristaltic manifold pressure innovation"
            elif i == 9 and j == 4:
                val = 0.1850
                comment = "L[9,4]: Tare beam deflection innovation"
            elif i == 10 and j == 4:
                val = 0.0085
                comment = "L[10,4]: Tare voice-coil current innovation"
            elif i == 11 and j == 5:
                val = 0.1850
                comment = "L[11,5]: Gross beam deflection innovation"
            elif i == 12 and j == 5:
                val = 0.0085
                comment = "L[12,5]: Gross voice-coil current innovation"
            elif i == 13 and j == 6:
                val = 0.2950
                comment = "L[13,6]: Isolator differential pressure innovation"
            elif i == 14 and j == 7:
                val = 0.2200
                comment = "L[14,7]: Nitrogen headspace manifold pressure innovation"
            elif i == 16 and j == 8:
                val = 0.2750
                comment = "L[16,8]: Crimp capper dynamic sealing force innovation"

            lines.append(f"    arObserverGain_L[{i:2d}, {j:2d}] := {val:10.6f}; (* {comment} *)")

    lines.append('')
    lines.append('    (* --- Actuator Saturation and Slew Limits --- *)')
    u_mins = [-25.0, -80.0, 0.0, -50.0, -50.0, 0.0, 0.0, 0.0]
    u_maxs = [25.0, 80.0, 650.0, 50.0, 50.0, 100.0, 100.0, 35.0]
    du_maxs = [2.5, 8.0, 50.0, 5.0, 5.0, 5.0, 10.0, 3.5]
    for j in range(1, 9):
        lines.append(f"    arU_Min[{j}] := {u_mins[j-1]:8.2f}; (* Minimum bound for {input_names[j-1]} *)")
        lines.append(f"    arU_Max[{j}] := {u_maxs[j-1]:8.2f}; (* Maximum bound for {input_names[j-1]} *)")
        lines.append(f"    arDeltaU_Max[{j}] := {du_maxs[j-1]:8.2f}; (* Slew limit for {input_names[j-1]} *)")

    lines.append('')
    lines.append('    (* --- Dosing Channels Initial Calibration & Trim --- *)')
    for k in range(1, 13):
        lines.append(f"    arPumpOffsetTrim_ul[{k}] := 0.0; (* Needle {k} zero initial trim [ul] *)")
        lines.append(f"    arChannelGain[{k}] := 0.085; (* Adaptive feedback gain channel {k} *)")
        lines.append(f"    arChannelIntegralError[{k}] := 0.0; (* Channel {k} integral bias *)")
        lines.append(f"    arNeedleTareWeight_mg[{k}] := 0.0;")
        lines.append(f"    arNeedleGrossWeight_mg[{k}] := 0.0;")
        lines.append(f"    arNeedleNetWeight_mg[{k}] := 0.0;")
        lines.append(f"    arNeedleDispenseCount[{k}] := 0;")
        lines.append(f"    arNeedleRejectCount[{k}] := 0;")

    lines.append('')
    lines.append('    (* --- Setpoint Target Mass Limits --- *)')
    lines.append('    rTargetNetWeight_mg := rTargetDosingVol_ml * rLiquidDensity_g_cm3 * 1000.0;')
    lines.append('    rUpperSpecLimit_mg := rTargetNetWeight_mg + rGrossWeightTolerance_mg;')
    lines.append('    rLowerSpecLimit_mg := rTargetNetWeight_mg - rGrossWeightTolerance_mg;')
    lines.append('')
    lines.append('    bMatricesInitialized := TRUE;')
    lines.append('END_IF;')
    lines.append('"""')
    return '\n'.join(lines)

if __name__ == "__main__":
    code = generate()
    with open("vial_filler_matrices.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("vial_filler_matrices.py generated successfully!")
