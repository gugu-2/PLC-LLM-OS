# gen_thermoform.py - Comprehensive generator for FB_Plastics_RotaryThermoforming_MultiStation

import os
import json
import re

def generate_matrices_init():
    lines = []
    lines.append("    (* ================================================================================= *)")
    lines.append("    (* INITIALIZATION OF 16x16 SYSTEM MATRIX A (CONTINUOUS-TO-DISCRETE DYNAMICS)        *)")
    lines.append("    (* Sampling Interval Ts = 5.0 [ms]. Coefficients derived from polymer rheology,     *)")
    lines.append("    (* Stefan-Boltzmann radiant flux, catenary viscoelastic creep, and orifice vacuum.  *)")
    lines.append("    (* ================================================================================= *)")
    
    a_coeffs = {
        (1, 1): (0.9652, "Top surface temperature thermal inertia"),
        (1, 3): (0.0284, "Internal conduction flux from sheet core to top surface"),
        (2, 2): (0.9618, "Bottom surface temperature thermal inertia"),
        (2, 3): (0.0312, "Internal conduction flux from sheet core to bottom surface"),
        (3, 1): (0.0195, "Thermal diffusion from top irradiated surface into core"),
        (3, 2): (0.0215, "Thermal diffusion from bottom irradiated surface into core"),
        (3, 3): (0.9576, "Core mid-plane thermal capacitance and retention"),
        (4, 4): (0.9845, "Catenary sag geometric memory and tension retention"),
        (4, 5): (0.0050, "Sag velocity integration into vertical displacement [mm]"),
        (5, 3): (0.0162, "Thermal softening creep acceleration driven by core temperature"),
        (5, 4): (-0.0092, "Biaxial membrane restoring tension stiffness counteracting sag"),
        (5, 5): (0.9320, "Viscoelastic damping ratio of sagging thermoplastic membrane"),
        (6, 6): (0.9412, "Bubble apex height geometric retention"),
        (6, 7): (0.0485, "Pre-blow chamber differential pressure driving upward bubble expansion"),
        (7, 6): (-0.0142, "Spherical cap volume expansion adiabatic pressure decompression"),
        (7, 7): (0.8925, "Pre-blow pneumatic chamber acoustic damping and decay"),
        (8, 8): (0.9240, "Mold cavity vacuum holding retention"),
        (8, 9): (-0.0785, "Evacuation flow rate drawing vacuum down towards surge tank"),
        (9, 8): (0.0392, "Cavity-to-tank pressure gradient driving volumetric airflow"),
        (9, 9): (0.8460, "Vacuum manifold fluid dynamic momentum and port resistance"),
        (10, 10): (1.0000, "Servo plug assist linear position integrator"),
        (10, 11): (0.0050, "Servo plug linear velocity integration into position [mm]"),
        (11, 11): (0.9080, "Servo linear motor mechanical and electromagnetic velocity damping"),
        (11, 12): (-0.0038, "Viscoelastic drawing resistance retarding plug penetration speed"),
        (12, 10): (0.0245, "Penetration depth increasing contact area and frictional drag force"),
        (12, 11): (0.0560, "Viscous shear drag rate between syntactic foam and hot polymer"),
        (12, 12): (0.8780, "Maxwell-Weichert viscoelastic stress relaxation of drawn sheet"),
        (13, 13): (0.9865, "Aluminum mold tool cavity surface thermal capacitance"),
        (13, 14): (-0.0195, "Polymer heat flux absorption cooling the mold tool"),
        (14, 3): (0.0268, "Polymer core temperature gradient driving mold contact heat transfer"),
        (14, 13): (-0.0345, "Chilled aluminum surface temperature driving part quenching"),
        (14, 14): (0.9180, "Thermal boundary layer solidification decay rate"),
        (15, 15): (0.9985, "Rotary carousel turntable angular position retention"),
        (16, 10): (0.0492, "Plug penetration elongation inducing membrane biaxial stress"),
        (16, 16): (0.8720, "Non-linear Maxwell relaxation: exp(-Ts / tau_relax)")
    }
    
    for r in range(1, 17):
        for c in range(1, 17):
            if (r, c) in a_coeffs:
                val, desc = a_coeffs[(r, c)]
                lines.append(f"    aMatrix_A[{r:2d}, {c:2d}] := {val:0.4f};  (* A[{r},{c}]: {desc} *)")
            else:
                lines.append(f"    aMatrix_A[{r:2d}, {c:2d}] := 0.0000;  (* A[{r},{c}]: Uncoupled state dynamic *)")
                
    lines.append("\n    (* ================================================================================= *)")
    lines.append("    (* INITIALIZATION OF 16x8 ACTUATOR INPUT MATRIX B                                    *)")
    lines.append("    (* Input Coupling: Top/Bot Power, Pre-Blow, Vacuum, Plug Torque, MTC, Carousel, Jet *)")
    lines.append("    (* ================================================================================= *)")
    
    b_coeffs = {
        (1, 1): (0.0465, "u[1] Top Quartz Power [%] -> Top Sheet Surface Temp [deg C]"),
        (2, 2): (0.0482, "u[2] Bot Quartz Power [%] -> Bottom Sheet Surface Temp [deg C]"),
        (4, 3): (-0.0280, "u[3] Pre-Blow Air Pulse [%] -> Sheet Sag Counteraction [mm]"),
        (6, 3): (0.0685, "u[3] Pre-Blow Valve [%] -> Bubble Apex Expansion [mm]"),
        (7, 3): (0.1320, "u[3] Pre-Blow Valve [%] -> Bubble Chamber Pressure [mbar]"),
        (8, 4): (-0.1950, "u[4] Vacuum Proportional Valve [%] -> Mold Cavity Absolute Vacuum [mbar]"),
        (9, 4): (0.2350, "u[4] Vacuum Proportional Valve [%] -> Evacuation Flow Rate [m3/h]"),
        (10, 5): (0.0018, "u[5] Plug Assist Drive Torque [Nm] -> Plug Position [mm]"),
        (11, 5): (0.0295, "u[5] Plug Assist Drive Torque [Nm] -> Plug Linear Velocity [m/s]"),
        (13, 6): (-0.0380, "u[6] MTC Coolant Flow Valve [%] -> Aluminum Mold Surface Temp [deg C]"),
        (14, 8): (0.0920, "u[8] Chilled Air Cooling Jet [%] -> Polymer Solidification Rate [deg C/s]"),
        (15, 7): (0.0460, "u[7] Carousel Indexing Torque [Nm] -> Turntable Rotation Angle [deg]")
    }
    
    for r in range(1, 17):
        for c in range(1, 9):
            if (r, c) in b_coeffs:
                val, desc = b_coeffs[(r, c)]
                lines.append(f"    aMatrix_B[{r:2d}, {c:2d}] := {val:0.4f};  (* B[{r},{c}]: {desc} *)")
            else:
                lines.append(f"    aMatrix_B[{r:2d}, {c:2d}] := 0.0000;  (* B[{r},{c}]: Zero input coupling *)")

    lines.append("\n    (* ================================================================================= *)")
    lines.append("    (* INITIALIZATION OF 16x16 OUTPUT MATRIX C & 16x8 FEEDTHROUGH MATRIX D               *)")
    lines.append("    (* ================================================================================= *)")
    for r in range(1, 17):
        for c in range(1, 17):
            if r == c:
                lines.append(f"    aMatrix_C[{r:2d}, {c:2d}] := 1.0000;  (* Direct full-state observation C[{r},{c}] *)")
            else:
                lines.append(f"    aMatrix_C[{r:2d}, {c:2d}] := 0.0000;")
                
    for r in range(1, 17):
        for c in range(1, 9):
            lines.append(f"    aMatrix_D[{r:2d}, {c:2d}] := 0.0000;  (* D[{r},{c}]: Zero direct feedthrough *)")

    lines.append("\n    (* ================================================================================= *)")
    lines.append("    (* INITIALIZATION OF MPC QUADRATIC COST WEIGHTING MATRICES (Q, R, P)                 *)")
    lines.append("    (* Q: State error penalties, R: Actuator effort penalties, P: Riccati terminal cost  *)")
    lines.append("    (* ================================================================================= *)")
    
    q_weights = [
        12.5,  # x1: Top Temp
        12.5,  # x2: Bot Temp
        15.0,  # x3: Core Temp
        25.0,  # x4: Sag (High priority to avoid heater contact)
        8.0,   # x5: Sag Rate
        18.0,  # x6: Bubble Apex
        10.0,  # x7: Bubble Pressure
        30.0,  # x8: Mold Vacuum (Critical for part definition)
        5.0,   # x9: Evacuation Flow
        22.0,  # x10: Plug Position
        8.0,   # x11: Plug Velocity
        14.0,  # x12: Plug Force
        16.0,  # x13: Mold Temp
        18.0,  # x14: Cooling Rate
        20.0,  # x15: Carousel Angle
        10.0   # x16: Relaxation Stress
    ]
    
    r_weights = [
        1.20,  # u1: Top Power
        1.20,  # u2: Bot Power
        2.50,  # u3: Pre-blow valve
        2.00,  # u4: Vacuum valve
        0.80,  # u5: Plug torque
        1.50,  # u6: MTC valve
        3.00,  # u7: Carousel torque
        1.00   # u8: Chilled air
    ]
    
    for r in range(1, 17):
        for c in range(1, 17):
            if r == c:
                qw = q_weights[r-1]
                pw = qw * 2.85
                lines.append(f"    aMatrix_Q[{r:2d}, {c:2d}] := {qw:0.2f};  (* Q[{r},{r}]: State x[{r}] error tracking weight *)")
                lines.append(f"    aMatrix_P[{r:2d}, {c:2d}] := {pw:0.2f};  (* P[{r},{r}]: Terminal Riccati weight for x[{r}] *)")
            else:
                lines.append(f"    aMatrix_Q[{r:2d}, {c:2d}] := 0.00;")
                lines.append(f"    aMatrix_P[{r:2d}, {c:2d}] := 0.00;")

    for r in range(1, 9):
        for c in range(1, 9):
            if r == c:
                rw = r_weights[r-1]
                lines.append(f"    aMatrix_R[{r:2d}, {c:2d}] := {rw:0.2f};  (* R[{r},{r}]: Actuator u[{r}] rate penalty *)")
            else:
                lines.append(f"    aMatrix_R[{r:2d}, {c:2d}] := 0.00;")

    return "\n".join(lines)

print("Matrices generator defined.")
