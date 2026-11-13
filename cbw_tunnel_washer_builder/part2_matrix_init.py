# cbw_tunnel_washer_builder/part2_matrix_init.py
# Discrete State-Space Matrices & MPC Weighting Matrix Initialization

def get_part2_matrix_init():
    code = """(* ==================================================================================================== *)
(* PHASE 0: ONE-TIME COLD-START INITIALIZATION OF MATRICES & CONTROL VECTORS                            *)
(* ==================================================================================================== *)
IF NOT bInitialized THEN
    (* ---------------------------------------------------------------------------------------------- *)
    (* DISCRETE STATE-SPACE SYSTEM DYNAMICS MATRIX A (10 x 10) [Ts = 100 ms]                          *)
    (* States:                                                                                        *)
    (*   x[1]  = Pre-Wash Zone Average Bath Temperature T_pre [deg C]                                 *)
    (*   x[2]  = Main Wash Core Zone Bath Temperature T_main [deg C]                                  *)
    (*   x[3]  = Bleach Disinfection Zone Bath Temperature T_blc [deg C]                              *)
    (*   x[4]  = Counter-Flow Rinse Water Conductivity C_rns [mS/cm]                                  *)
    (*   x[5]  = Main Wash Active Alkali Chemical Titration C_alk [g/L]                               *)
    (*   x[6]  = Heat Exchanger Effluent Clean Water Preheat Temp T_rec [deg C]                       *)
    (*   x[7]  = Extractor Hydraulic Ram Extraction Pressure P_prs [bar]                              *)
    (*   x[8]  = Extracted Linen Cake Residual Moisture Retention M_cake [%]                         *)
    (*   x[9]  = Drum Geared Drive Motor Shaft Dynamic Load Torque Tau_drum [N*m]                     *)
    (*   x[10] = Press Water Recovery Storage Buffer Tank Level L_rec [%]                             *)
    (* ---------------------------------------------------------------------------------------------- *)
"""
    # Generate A matrix (10x10)
    # Physically derived values
    a_vals = [
        # Row 1: T_pre
        [0.9965, 0.0008, 0.0000, 0.0000, 0.0000, 0.0018, 0.0000, 0.0000, 0.0000, 0.0002],
        # Row 2: T_main
        [0.0012, 0.9942, 0.0010, 0.0000, 0.0000, 0.0008, 0.0000, 0.0000, 0.0000, 0.0000],
        # Row 3: T_blc
        [0.0000, 0.0020, 0.9935, 0.0000, 0.0000, 0.0005, 0.0000, 0.0000, 0.0000, 0.0000],
        # Row 4: C_rns
        [0.0000, 0.0000, 0.0005, 0.9880, 0.0008, 0.0000, 0.0000, 0.0000, 0.0000, 0.0002],
        # Row 5: C_alk
        [0.0000, 0.0002, 0.0000, 0.0000, 0.9950, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        # Row 6: T_rec
        [0.0005, 0.0150, 0.0025, 0.0000, 0.0000, 0.9820, 0.0000, 0.0000, 0.0000, 0.0000],
        # Row 7: P_prs
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.9200, 0.0000, 0.0000, 0.0000],
        # Row 8: M_cake
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, -0.0450, 0.9910, 0.0000, 0.0000],
        # Row 9: Tau_drum
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0250, 0.9500, 0.0000],
        # Row 10: L_rec
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0120, 0.0000, 0.0000, 0.9980]
    ]

    for r in range(10):
        for c in range(10):
            val = a_vals[r][c]
            code += f"    matA[{r+1},{c+1}] := {val:0.4f};\n"

    code += "\n    (* ---------------------------------------------------------------------------------------------- *)\n"
    code += "    (* CONTROL INPUT COUPLING MATRIX B (10 x 6)                                                      *)\n"
    code += "    (* Inputs:                                                                                       *)\n"
    code += "    (*   u[1] = Main Wash Steam Valve Cmd [%]                                                        *)\n"
    code += "    (*   u[2] = Bleach Direct Steam Valve Cmd [%]                                                    *)\n"
    code += "    (*   u[3] = Freshwater Intake Makeup Valve Cmd [%]                                               *)\n"
    code += "    (*   u[4] = Counter-Flow Recirculation Pump VFD Cmd [%]                                         *)\n"
    code += "    (*   u[5] = Hydraulic Press Proportional Pressure Servo [bar]                                  *)\n"
    code += "    (*   u[6] = Chemical Dosing Manifold Master Injection Rate [%]                                   *)\n"
    code += "    (* ---------------------------------------------------------------------------------------------- *)\n"

    b_vals = [
        # Row 1: T_pre
        [0.0000, 0.0000, -0.0008, 0.0015, 0.0000, 0.0000],
        # Row 2: T_main
        [0.0125, 0.0000, -0.0005, -0.0008, 0.0000, 0.0000],
        # Row 3: T_blc
        [0.0000, 0.0140, -0.0004, -0.0010, 0.0000, 0.0000],
        # Row 4: C_rns
        [0.0000, 0.0000, -0.0025, -0.0018, 0.0000, 0.0005],
        # Row 5: C_alk
        [0.0000, 0.0000, -0.0002, -0.0012, 0.0000, 0.0085],
        # Row 6: T_rec
        [0.0000, 0.0000, -0.0015, 0.0020, 0.0000, 0.0000],
        # Row 7: P_prs
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0800, 0.0000],
        # Row 8: M_cake
        [0.0000, 0.0000, 0.0000, 0.0000, -0.0020, 0.0000],
        # Row 9: Tau_drum
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.1500],
        # Row 10: L_rec
        [0.0000, 0.0000, 0.0000, -0.0080, 0.0000, 0.0000]
    ]

    for r in range(10):
        for c in range(6):
            val = b_vals[r][c]
            code += f"    matB[{r+1},{c+1}] := {val:0.4f};\n"

    code += "\n    (* ---------------------------------------------------------------------------------------------- *)\n"
    code += "    (* OUTPUT OBSERVATION MATRIX C (8 x 10)                                                          *)\n"
    code += "    (* Outputs:                                                                                      *)\n"
    code += "    (*   y[1] = TT-101 Main Wash Bath Temp [deg C]                                                   *)\n"
    code += "    (*   y[2] = AT-201 Rinse Zone Conductivity [mS/cm]                                               *)\n"
    code += "    (*   y[3] = PT-301 Hydraulic Extraction Pressure [bar]                                           *)\n"
    code += "    (*   y[4] = FT-401 Cold Freshwater Intake Flow [m3/h]                                            *)\n"
    code += "    (*   y[5] = ST-501 Drum Geared Drive Motor Torque [N*m]                                          *)\n"
    code += "    (*   y[6] = TT-701 Heat Exchanger Effluent Temp [deg C]                                          *)\n"
    code += "    (*   y[7] = Estimated Residual Linen Cake Moisture [%]                                           *)\n"
    code += "    (*   y[8] = LT-901 Press Water Recovery Tank Level [%]                                           *)\n"
    code += "    (* ---------------------------------------------------------------------------------------------- *)\n"

    c_vals = [
        # y1: T_main (x2)
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        # y2: C_rns (x4)
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        # y3: P_prs (x7)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
        # y4: Flow FT-401 (proportional to u3)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        # y5: Drum Torque (x9)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        # y6: Exchanger Temp (x6)
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        # y7: Cake Moisture (x8)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
        # y8: Tank Level (x10)
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    ]

    for r in range(8):
        for c in range(10):
            val = c_vals[r][c]
            code += f"    matC[{r+1},{c+1}] := {val:0.4f};\n"

    code += "\n    (* ---------------------------------------------------------------------------------------------- *)\n"
    code += "    (* DIRECT FEEDTHROUGH MATRIX D (8 x 6)                                                           *)\n"
    code += "    (* ---------------------------------------------------------------------------------------------- *)\n"

    for r in range(8):
        for c in range(6):
            if r == 3 and c == 2:  # FT-401 flow directly coupled to u3
                val = 0.1200
            else:
                val = 0.0000
            code += f"    matD[{r+1},{c+1}] := {val:0.4f};\n"

    code += "\n    (* ---------------------------------------------------------------------------------------------- *)\n"
    code += "    (* LUENBERGER OBSERVER INNOVATION GAIN MATRIX L (10 x 8)                                         *)\n"
    code += "    (* ---------------------------------------------------------------------------------------------- *)\n"

    l_vals = [
        # Row 1: x1 (T_pre)
        [0.0150, 0.0000, 0.0000, 0.0010, 0.0000, 0.0200, 0.0000, 0.0020],
        # Row 2: x2 (T_main)
        [0.0850, 0.0000, 0.0000, 0.0000, 0.0000, 0.0100, 0.0000, 0.0000],
        # Row 3: x3 (T_blc)
        [0.0250, 0.0000, 0.0000, 0.0000, 0.0000, 0.0050, 0.0000, 0.0000],
        # Row 4: x4 (C_rns)
        [0.0000, 0.1200, 0.0000, 0.0020, 0.0000, 0.0000, 0.0000, 0.0050],
        # Row 5: x5 (C_alk)
        [0.0000, 0.0450, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        # Row 6: x6 (T_rec)
        [0.0050, 0.0000, 0.0000, 0.0010, 0.0000, 0.0950, 0.0000, 0.0000],
        # Row 7: x7 (P_prs)
        [0.0000, 0.0000, 0.1500, 0.0000, 0.0000, 0.0000, 0.0000, 0.0010],
        # Row 8: x8 (M_cake)
        [0.0000, 0.0000, -0.0120, 0.0000, 0.0000, 0.0000, 0.0750, 0.0000],
        # Row 9: x9 (Tau_drum)
        [0.0000, 0.0000, 0.0000, 0.0000, 0.1100, 0.0000, 0.0050, 0.0000],
        # Row 10: x10 (L_rec)
        [0.0000, 0.0000, 0.0020, 0.0000, 0.0000, 0.0000, 0.0000, 0.0800]
    ]

    for r in range(10):
        for c in range(8):
            val = l_vals[r][c]
            code += f"    matL[{r+1},{c+1}] := {val:0.4f};\n"

    code += "\n    (* ---------------------------------------------------------------------------------------------- *)\n"
    code += "    (* MPC STATE DEVIATION PENALTY WEIGHT MATRIX Q (10 x 10)                                         *)\n"
    code += "    (* ---------------------------------------------------------------------------------------------- *)\n"

    for r in range(10):
        for c in range(10):
            if r == c:
                if r == 0:   # x1 T_pre
                    val = 2.50
                elif r == 1: # x2 T_main (high priority tracking of 85 deg C)
                    val = 18.00
                elif r == 2: # x3 T_blc (high priority tracking of 70 deg C)
                    val = 12.00
                elif r == 3: # x4 C_rns (low conductivity rinse penalty)
                    val = 15.00
                elif r == 4: # x5 C_alk (alkali concentration)
                    val = 5.00
                elif r == 5: # x6 T_rec (heat recovery maximization)
                    val = 6.00
                elif r == 6: # x7 P_prs (press extraction pressure)
                    val = 8.00
                elif r == 7: # x8 M_cake (moisture reduction penalty)
                    val = 25.00
                elif r == 8: # x9 Tau_drum (torque surge penalty)
                    val = 1.50
                elif r == 9: # x10 L_rec (tank level penalty)
                    val = 3.00
            else:
                val = 0.00
            code += f"    matQ[{r+1},{c+1}] := {val:0.4f};\n"

    code += "\n    (* ---------------------------------------------------------------------------------------------- *)\n"
    code += "    (* MPC CONTROL EFFORT ENERGY PENALTY MATRIX R (6 x 6)                                            *)\n"
    code += "    (* ---------------------------------------------------------------------------------------------- *)\n"

    for r in range(6):
        for c in range(6):
            if r == c:
                if r == 0:   # u1 Steam main
                    val = 3.20
                elif r == 1: # u2 Steam bleach
                    val = 3.00
                elif r == 2: # u3 Fresh water makeup
                    val = 4.50
                elif r == 3: # u4 Recirculation pump
                    val = 1.20
                elif r == 4: # u5 Hydraulic press
                    val = 0.80
                elif r == 5: # u6 Chemical dosing
                    val = 5.00
            else:
                val = 0.00
            code += f"    matR[{r+1},{c+1}] := {val:0.4f};\n"

    code += "\n    (* ---------------------------------------------------------------------------------------------- *)\n"
    code += "    (* MPC ACTUATOR SLEW-RATE PENALTY MATRIX S (6 x 6)                                               *)\n"
    code += "    (* ---------------------------------------------------------------------------------------------- *)\n"

    for r in range(6):
        for c in range(6):
            if r == c:
                if r == 0:   # u1 Steam main slew
                    val = 8.50
                elif r == 1: # u2 Steam bleach slew
                    val = 8.00
                elif r == 2: # u3 Fresh water slew
                    val = 5.00
                elif r == 3: # u4 Recirculation pump slew
                    val = 2.50
                elif r == 4: # u5 Press ram pressure slew
                    val = 12.00
                elif r == 5: # u6 Chemical rate slew
                    val = 6.00
            else:
                val = 0.00
            code += f"    matS[{r+1},{c+1}] := {val:0.4f};\n"

    code += "\n    (* ---------------------------------------------------------------------------------------------- *)\n"
    code += "    (* MPC TERMINAL RICCATI PENALTY MATRIX P (10 x 10)                                               *)\n"
    code += "    (* ---------------------------------------------------------------------------------------------- *)\n"

    for r in range(10):
        for c in range(10):
            if r == c:
                if r == 0:
                    val = 4.50
                elif r == 1:
                    val = 32.00
                elif r == 2:
                    val = 22.00
                elif r == 3:
                    val = 26.00
                elif r == 4:
                    val = 8.50
                elif r == 5:
                    val = 10.00
                elif r == 6:
                    val = 14.00
                elif r == 7:
                    val = 45.00
                elif r == 8:
                    val = 2.50
                elif r == 9:
                    val = 5.00
            else:
                val = 0.00
            code += f"    matP[{r+1},{c+1}] := {val:0.4f};\n"

    code += "\n    (* ---------------------------------------------------------------------------------------------- *)\n"
    code += "    (* ACTUATOR BOUNDS & SLEW LIMIT CONSTRAINTS                                                      *)\n"
    code += "    (* ---------------------------------------------------------------------------------------------- *)\n"
    code += "    vecU_min[1] := 0.0;    vecU_max[1] := 100.0;   vecDeltaU_max[1] := 2.5;  (* Steam Main [%] *)\n"
    code += "    vecU_min[2] := 0.0;    vecU_max[2] := 100.0;   vecDeltaU_max[2] := 2.5;  (* Steam Bleach [%] *)\n"
    code += "    vecU_min[3] := 0.0;    vecU_max[3] := 100.0;   vecDeltaU_max[3] := 5.0;  (* Freshwater Intake [%] *)\n"
    code += "    vecU_min[4] := 10.0;   vecU_max[4] := 100.0;   vecDeltaU_max[4] := 4.0;  (* Recirc Pump VFD [%] *)\n"
    code += "    vecU_min[5] := 0.0;    vecU_max[5] := 50.0;    vecDeltaU_max[5] := 1.5;  (* Press Pressure [bar] *)\n"
    code += "    vecU_min[6] := 0.0;    vecU_max[6] := 100.0;   vecDeltaU_max[6] := 10.0; (* Chemical Pulse Rate [%] *)\n\n"

    code += "    (* ---------------------------------------------------------------------------------------------- *)\n"
    code += "    (* BASELINE CYBER-PHYSICAL STATE REFERENCE SETPOINT TRAJECTORY                                   *)\n"
    code += "    (* ---------------------------------------------------------------------------------------------- *)\n"
    code += "    vecX_ref[1]  := 40.0;   (* Pre-Wash Zone Target Temp [deg C] *)\n"
    code += "    vecX_ref[2]  := 85.0;   (* Main Wash Disinfection Core Target Temp [deg C] *)\n"
    code += "    vecX_ref[3]  := 70.0;   (* Bleach Activation Zone Target Temp [deg C] *)\n"
    code += "    vecX_ref[4]  := 0.18;   (* Rinse Soil Conductivity Target [mS/cm] *)\n"
    code += "    vecX_ref[5]  := 1.25;   (* Main Wash Active Alkali Target [g/L] *)\n"
    code += "    vecX_ref[6]  := 48.0;   (* Heat Exchanger Preheated Water Effluent Temp [deg C] *)\n"
    code += "    vecX_ref[7]  := 48.0;   (* Dewatering Hydraulic Ram Peak Pressure [bar] *)\n"
    code += "    vecX_ref[8]  := 46.5;   (* Target Residual Linen Cake Moisture [%] *)\n"
    code += "    vecX_ref[9]  := 1850.0; (* Nominal Drum Drive Torque Load [N*m] *)\n"
    code += "    vecX_ref[10] := 65.0;   (* Press Water Recovery Buffer Level [%] *)\n\n"

    code += "    (* Initial State Vector Cold Estimates *)\n"
    code += "    vecX[1]  := 22.0;\n"
    code += "    vecX[2]  := 22.0;\n"
    code += "    vecX[3]  := 22.0;\n"
    code += "    vecX[4]  := 0.05;\n"
    code += "    vecX[5]  := 0.00;\n"
    code += "    vecX[6]  := 20.0;\n"
    code += "    vecX[7]  := 0.0;\n"
    code += "    vecX[8]  := 220.0;\n"
    code += "    vecX[9]  := 500.0;\n"
    code += "    vecX[10] := 50.0;\n\n"

    code += "    FOR i := 1 TO 6 DO\n"
    code += "        vecU[i] := 0.0;\n"
    code += "        vecU_prev[i] := 0.0;\n"
    code += "        vecU_target[i] := 0.0;\n"
    code += "    END_FOR;\n\n"

    code += "    bInitialized := TRUE;\n"
    code += "END_IF;\n\n"

    return code
