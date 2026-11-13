# ccgt_builder/st_matrices.py

def get_matrices_init():
    return """(* =====================================================================================================================
 * PHASE 0: ONE-SHOT FIRST-SCAN HARD REAL-TIME DETERMINISTIC MATRIX ALLOCATION & SYSTEM INITIALIZATION
 * Discretized at Ts = 0.020 s (20.0 ms / 50.0 Hz) from Coupled Thermo-Fluid Dynamics & Rotor Mechanical Equations:
 *   Continuous State-Space:  dx/dt = A_c * x(t) + B_c * u(t)
 *   Discrete Equivalence:    x[k+1] = A * x[k] + B * u[k]
 *   Measurement Vector:      y[k]   = C * x[k] + D * u[k]
 *   Luenberger Observer:     x_hat[k+1] = A * x_corr[k] + B * u[k], where x_corr = x_hat + L * (y_meas - C * x_hat)
 * ===================================================================================================================== *)
IF NOT bInitialized THEN
    (* -----------------------------------------------------------------------------------------------------------------
     * SYSTEM DYNAMICS MATRIX A (8x8):
     * x1: GT Power [MW], x2: EGT [deg C], x3: VGV Position [deg], x4: Drum Level [mm],
     * x5: Steam Flow [kg/s], x6: Main Steam Temp [deg C], x7: Inter-Stage Temp [deg C], x8: FW Valve Effective [%]
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Row 1: Gas Turbine Active Electrical Power Dynamics (x1) [MW] *)
    A_mat[1, 1] := 0.988250; (* Gas turbine shaft inertia and aerodynamic damping at 3000 rpm *)
    A_mat[1, 2] := 0.000450; (* Thermodynamic Brayton cycle expansion efficiency variation with exhaust enthalpy *)
    A_mat[1, 3] := 0.012500; (* Compressor guide vane opening increases air mass flow and gas generator torque *)
    A_mat[1, 4] := 0.000000; (* Decoupled from downstream HRSG steam drum level *)
    A_mat[1, 5] := 0.000000; (* Decoupled from downstream steam header flow *)
    A_mat[1, 6] := 0.000000; (* Decoupled from steam turbine superheater temperature *)
    A_mat[1, 7] := 0.000000; (* Decoupled from attemperator spray *)
    A_mat[1, 8] := 0.000000; (* Decoupled from feedwater valve *)

    (* Row 2: Combustor Exhaust Gas Temperature (EGT) Dynamics (x2) [deg C] *)
    A_mat[2, 1] := -0.002100; (* Turbine power extraction reduces gas total temperature through expansion stages *)
    A_mat[2, 2] := 0.991200; (* Thermal inertia of transition pieces, turbine nozzle guide vanes and exhaust diffuser casing *)
    A_mat[2, 3] := -0.015400; (* VGV opening introduces excess compressor airflow, diluting combustor and lowering EGT *)
    A_mat[2, 4] := 0.000000; (* Decoupled from drum water level *)
    A_mat[2, 5] := 0.000000; (* Decoupled from steam header flow *)
    A_mat[2, 6] := 0.000000; (* Decoupled from superheater metal temperature *)
    A_mat[2, 7] := 0.000000; (* Decoupled from attemperator *)
    A_mat[2, 8] := 0.000000; (* Decoupled from feedwater *)

    (* Row 3: Compressor Variable Guide Vane (VGV) Position Dynamics (x3) [deg] *)
    A_mat[3, 1] := 0.000000; (* Electro-hydraulic uni-torque actuator feedback isolation *)
    A_mat[3, 2] := 0.000000; (* Electro-hydraulic actuator temperature isolation *)
    A_mat[3, 3] := 0.962000; (* Hydraulic ring servo actuator closed-loop position lag (tau ~ 0.52 s) *)
    A_mat[3, 4] := 0.000000; (* Decoupled from drum *)
    A_mat[3, 5] := 0.000000; (* Decoupled from steam flow *)
    A_mat[3, 6] := 0.000000; (* Decoupled from superheater *)
    A_mat[3, 7] := 0.000000; (* Decoupled from attemperator *)
    A_mat[3, 8] := 0.000000; (* Decoupled from feedwater *)

    (* Row 4: HRSG High-Pressure Drum Narrow-Range Water Level Dynamics (x4) [mm] *)
    A_mat[4, 1] := 0.000000; (* Decoupled from electrical load direct induction *)
    A_mat[4, 2] := 0.008450; (* Exhaust gas enthalpy flux driving boiling void swell in evaporator riser tubes *)
    A_mat[4, 3] := 0.000000; (* Decoupled from direct guide vane position *)
    A_mat[4, 4] := 0.997200; (* Drum liquid mass storage retention and hydrostatic surface area geometry *)
    A_mat[4, 5] := -0.025400; (* Steam outflow drawing mass inventory out of drum *)
    A_mat[4, 6] := 0.000000; (* Decoupled from final superheater exit temp *)
    A_mat[4, 7] := 0.000000; (* Decoupled from attemperator spray *)
    A_mat[4, 8] := 0.034800; (* Feedwater valve liquid inflow replenishing water inventory *)

    (* Row 5: High-Pressure Steam Header Generated Mass Flow Rate (x5) [kg/s] *)
    A_mat[5, 1] := 0.000000; (* Electrical load boundary condition *)
    A_mat[5, 2] := 0.015200; (* Flue gas heat transfer across evaporator finned tube bundles generating steam *)
    A_mat[5, 3] := 0.000000; (* Decoupled from VGV *)
    A_mat[5, 4] := 0.000120; (* Hydrostatic liquid head driving natural circulation through downcomers *)
    A_mat[5, 5] := 0.991800; (* Evaporation momentum and steam vapor header capacitance *)
    A_mat[5, 6] := 0.000000; (* Decoupled from superheater metal *)
    A_mat[5, 7] := 0.000000; (* Decoupled from spray *)
    A_mat[5, 8] := 0.002100; (* Subcooled feedwater inflow displacing saturated steam in drum *)

    (* Row 6: Final Superheater Main Steam Exit Temperature (x6) [deg C] *)
    A_mat[6, 1] := 0.000000; (* Decoupled from electrical power *)
    A_mat[6, 2] := 0.008500; (* Convective heat transfer from hot exhaust gas stream into superheater tubes *)
    A_mat[6, 3] := 0.000000; (* Decoupled from VGV *)
    A_mat[6, 4] := 0.000000; (* Decoupled from drum level *)
    A_mat[6, 5] := -0.006200; (* Steam mass flow cooling effect (higher velocity decreases steam residence time) *)
    A_mat[6, 6] := 0.994200; (* Superheater thick-walled Cr-Mo alloy tube metal thermal storage inertia *)
    A_mat[6, 7] := 0.005100; (* Convective steam enthalpy inflow from intermediate desuperheater station *)
    A_mat[6, 8] := 0.000000; (* Decoupled from boiler feedwater valve *)

    (* Row 7: Attemperator Desuperheater Inter-Stage Steam Temperature (x7) [deg C] *)
    A_mat[7, 1] := 0.000000; (* Decoupled from electrical power *)
    A_mat[7, 2] := 0.006200; (* Primary superheater convective thermal absorption from exhaust gas *)
    A_mat[7, 3] := 0.000000; (* Decoupled from VGV *)
    A_mat[7, 4] := 0.000000; (* Decoupled from drum level *)
    A_mat[7, 5] := -0.004800; (* Steam velocity cooling effect in primary superheater *)
    A_mat[7, 6] := 0.000000; (* Downstream temperature does not back-propagate into attemperator *)
    A_mat[7, 7] := 0.985000; (* Attemperator mixing chamber thermal residence time and turbulent dispersion *)
    A_mat[7, 8] := 0.000000; (* Decoupled from feedwater valve *)

    (* Row 8: Boiler Feedwater Regulating Valve Effective Hydrodynamic Position (x8) [%] *)
    A_mat[8, 1] := 0.000000; (* Actuator internal dynamics *)
    A_mat[8, 2] := 0.000000; (* Actuator internal dynamics *)
    A_mat[8, 3] := 0.000000; (* Actuator internal dynamics *)
    A_mat[8, 4] := 0.000000; (* Actuator internal dynamics *)
    A_mat[8, 5] := 0.000000; (* Actuator internal dynamics *)
    A_mat[8, 6] := 0.000000; (* Actuator internal dynamics *)
    A_mat[8, 7] := 0.000000; (* Actuator internal dynamics *)
    A_mat[8, 8] := 0.955000; (* Electro-hydraulic positioner response lag (tau ~ 0.44 s) *)

    (* -----------------------------------------------------------------------------------------------------------------
     * ACTUATOR / DISTURBANCE INPUT MATRIX B (8x6):
     * u1: Fuel Gas [%], u2: VGV [deg], u3: FW Valve [%], u4: Attemp Spray [%], u5: Steam Bypass [%], u6: Duct Burner [%]
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Row 1: GT Power [MW] *)
    B_mat[1, 1] := 0.045200; (* Fuel gas control valve directly meters heat release to increase shaft power *)
    B_mat[1, 2] := 0.001850; (* Guide vane slewing modulates compressor airflow and pressure ratio *)
    B_mat[1, 3] := 0.000000; (* Feedwater valve has no direct power influence *)
    B_mat[1, 4] := 0.000000; (* Spray valve has no direct power influence *)
    B_mat[1, 5] := 0.000000; (* Bypass valve has no direct power influence *)
    B_mat[1, 6] := 0.000000; (* Duct burner fires downstream in HRSG, zero gas turbine power influence *)

    (* Row 2: Combustor Exhaust Gas Temperature (EGT) [deg C] *)
    B_mat[2, 1] := 0.082500; (* Fuel gas enrichment directly increases stoichiometric flame temperature *)
    B_mat[2, 2] := -0.028400; (* VGV opening increases excess air ratio, quenching turbine exhaust temperature *)
    B_mat[2, 3] := 0.000000; (* Feedwater valve *)
    B_mat[2, 4] := 0.000000; (* Spray valve *)
    B_mat[2, 5] := 0.000000; (* Bypass valve *)
    B_mat[2, 6] := 0.035500; (* Supplemental duct burner firing elevates HRSG entry exhaust temperature *)

    (* Row 3: Variable Guide Vane (VGV) Position [deg] *)
    B_mat[3, 1] := 0.000000; (* Fuel gas *)
    B_mat[3, 2] := 0.038000; (* VGV position command slews actuator ring (38.0 deg/s normalized gain) *)
    B_mat[3, 3] := 0.000000; (* Feedwater valve *)
    B_mat[3, 4] := 0.000000; (* Spray valve *)
    B_mat[3, 5] := 0.000000; (* Bypass valve *)
    B_mat[3, 6] := 0.000000; (* Duct burner *)

    (* Row 4: HP Drum Water Level [mm] *)
    B_mat[4, 1] := 0.000000; (* Fuel gas (coupled through EGT state x2) *)
    B_mat[4, 2] := 0.000000; (* VGV *)
    B_mat[4, 3] := 0.012400; (* Feedwater valve command dynamic displacement *)
    B_mat[4, 4] := 0.000000; (* Attemperator spray *)
    B_mat[4, 5] := 0.004200; (* Rapid steam bypass opening creates drum depressurization flash swell *)
    B_mat[4, 6] := 0.006500; (* Duct burner ignition creates sudden heat flux swell in evaporator *)

    (* Row 5: HP Steam Generated Mass Flow Rate [kg/s] *)
    B_mat[5, 1] := 0.000000; (* Fuel gas (coupled through EGT state x2) *)
    B_mat[5, 2] := 0.000000; (* VGV *)
    B_mat[5, 3] := 0.000000; (* Feedwater valve *)
    B_mat[5, 4] := 0.000000; (* Spray valve *)
    B_mat[5, 5] := 0.042000; (* Steam bypass valve to condenser draws steam mass flow out of HRSG header *)
    B_mat[5, 6] := 0.028500; (* Duct burner fuel heat input directly generates incremental steam evaporation *)

    (* Row 6: Final Superheater Main Steam Exit Temperature [deg C] *)
    B_mat[6, 1] := 0.000000; (* Fuel gas *)
    B_mat[6, 2] := 0.000000; (* VGV *)
    B_mat[6, 3] := 0.000000; (* Feedwater valve *)
    B_mat[6, 4] := -0.048500; (* Attemperator spray desuperheater water injection cools steam stream *)
    B_mat[6, 5] := 0.000000; (* Steam bypass *)
    B_mat[6, 6] := 0.014200; (* Duct burner flue gas radiant and convective heating onto superheater *)

    (* Row 7: Attemperator Desuperheater Inter-Stage Temperature [deg C] *)
    B_mat[7, 1] := 0.000000; (* Fuel gas *)
    B_mat[7, 2] := 0.000000; (* VGV *)
    B_mat[7, 3] := 0.000000; (* Feedwater valve *)
    B_mat[7, 4] := -0.095000; (* Attemperator spray nozzle atomization directly quenches inter-stage steam *)
    B_mat[7, 5] := 0.000000; (* Steam bypass *)
    B_mat[7, 6] := 0.010500; (* Duct burner flue gas temperature elevation *)

    (* Row 8: Boiler Feedwater Regulating Valve Position [%] *)
    B_mat[8, 1] := 0.000000; (* Fuel gas *)
    B_mat[8, 2] := 0.000000; (* VGV *)
    B_mat[8, 3] := 0.045000; (* Feedwater demand command directly slews electro-hydraulic valve actuator *)
    B_mat[8, 4] := 0.000000; (* Spray valve *)
    B_mat[8, 5] := 0.000000; (* Bypass valve *)
    B_mat[8, 6] := 0.000000; (* Duct burner *)

    (* -----------------------------------------------------------------------------------------------------------------
     * OBSERVATION MATRIX C (6x8):
     * Maps State Vector to Measured Physical Process Outputs:
     *   y1: Active Power, y2: EGT, y3: VGV Position, y4: Drum Level, y5: Steam Flow, y6: Main Steam Temp
     * ----------------------------------------------------------------------------------------------------------------- *)
    FOR i_idx := 1 TO 6 DO
        FOR j_idx := 1 TO 8 DO
            IF i_idx = j_idx THEN
                C_mat[i_idx, j_idx] := 1.000000; (* Direct unity observation of state variables *)
            ELSE
                C_mat[i_idx, j_idx] := 0.000000;
            END_IF;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------------------
     * DIRECT FEEDTHROUGH MATRIX D (6x6): Zero direct feedthrough for physical strictly-proper plants
     * ----------------------------------------------------------------------------------------------------------------- *)
    FOR i_idx := 1 TO 6 DO
        FOR j_idx := 1 TO 6 DO
            D_mat[i_idx, j_idx] := 0.000000;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------------------
     * LUENBERGER / KALMAN OBSERVER INNOVATION GAIN MATRIX L (8x6):
     * Calibrated for closed-loop estimator stability and rapid innovation convergence under sensor noise
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* State 1 (Power) Observer Gains across measurements y1..y6 *)
    L_mat[1, 1] := 0.285000; (* Power innovation gain *)
    L_mat[1, 2] := 0.001200;
    L_mat[1, 3] := 0.004500;
    L_mat[1, 4] := 0.000000;
    L_mat[1, 5] := 0.000000;
    L_mat[1, 6] := 0.000000;

    (* State 2 (EGT) Observer Gains *)
    L_mat[2, 1] := 0.002500;
    L_mat[2, 2] := 0.312000; (* EGT pyrometer innovation gain *)
    L_mat[2, 3] := 0.008400;
    L_mat[2, 4] := 0.000000;
    L_mat[2, 5] := 0.000000;
    L_mat[2, 6] := 0.001500;

    (* State 3 (VGV) Observer Gains *)
    L_mat[3, 1] := 0.000000;
    L_mat[3, 2] := 0.000000;
    L_mat[3, 3] := 0.350000; (* VGV LVDT feedback gain *)
    L_mat[3, 4] := 0.000000;
    L_mat[3, 5] := 0.000000;
    L_mat[3, 6] := 0.000000;

    (* State 4 (Drum Level) Observer Gains *)
    L_mat[4, 1] := 0.000000;
    L_mat[4, 2] := 0.004500;
    L_mat[4, 3] := 0.000000;
    L_mat[4, 4] := 0.380000; (* Drum narrow-range level innovation gain *)
    L_mat[4, 5] := 0.012500;
    L_mat[4, 6] := 0.000000;

    (* State 5 (Steam Flow) Observer Gains *)
    L_mat[5, 1] := 0.000000;
    L_mat[5, 2] := 0.008500;
    L_mat[5, 3] := 0.000000;
    L_mat[5, 4] := 0.001500;
    L_mat[5, 5] := 0.320000; (* Coriolis mass flowmeter innovation gain *)
    L_mat[5, 6] := 0.000000;

    (* State 6 (Main Steam Temp) Observer Gains *)
    L_mat[6, 1] := 0.000000;
    L_mat[6, 2] := 0.006200;
    L_mat[6, 3] := 0.000000;
    L_mat[6, 4] := 0.000000;
    L_mat[6, 5] := 0.002800;
    L_mat[6, 6] := 0.340000; (* Main steam exit RTD innovation gain *)

    (* State 7 (Inter-Stage Temp) Observer Gains *)
    L_mat[7, 1] := 0.000000;
    L_mat[7, 2] := 0.005500;
    L_mat[7, 3] := 0.000000;
    L_mat[7, 4] := 0.000000;
    L_mat[7, 5] := 0.002100;
    L_mat[7, 6] := 0.085000; (* Attemperator inter-stage temperature coupling from main steam *)

    (* State 8 (FW Valve Effective) Observer Gains *)
    L_mat[8, 1] := 0.000000;
    L_mat[8, 2] := 0.000000;
    L_mat[8, 3] := 0.000000;
    L_mat[8, 4] := 0.015000; (* Feedwater position inferred from drum level mass imbalance *)
    L_mat[8, 5] := 0.008500;
    L_mat[8, 6] := 0.000000;

    (* -----------------------------------------------------------------------------------------------------------------
     * MPC QUADRATIC COST PENALTY MATRICES: Q (8x8), R (6x6), R_delta (6x6), P (8x8)
     * ----------------------------------------------------------------------------------------------------------------- *)
    FOR i_idx := 1 TO 8 DO
        FOR j_idx := 1 TO 8 DO
            Q_mat[i_idx, j_idx] := 0.000000;
            P_mat[i_idx, j_idx] := 0.000000;
        END_FOR;
    END_FOR;

    (* Diagonal State Error Penalties Q: Emphasis on Drum Level (Q4) and Steam Temp (Q6) *)
    Q_mat[1, 1] := 1.500000; (* Active electrical power tracking penalty *)
    Q_mat[2, 2] := 0.800000; (* EGT operating envelope penalty *)
    Q_mat[3, 3] := 0.200000; (* VGV guide vane position variation penalty *)
    Q_mat[4, 4] := 5.000000; (* HP Drum Level strict deviation penalty (shrink/swell suppression) *)
    Q_mat[5, 5] := 1.200000; (* Steam mass flow rate stabilization penalty *)
    Q_mat[6, 6] := 8.000000; (* Main steam temperature precision penalty (prevent turbine creep) *)
    Q_mat[7, 7] := 1.000000; (* Attemperator inter-stage temperature stability *)
    Q_mat[8, 8] := 0.100000; (* Feedwater valve movement damping *)

    (* Terminal State Penalty Matrix P = 1.8 * Q *)
    FOR i_idx := 1 TO 8 DO
        P_mat[i_idx, i_idx] := 1.800000 * Q_mat[i_idx, i_idx];
    END_FOR;

    (* Diagonal Control Effort Penalties R (6x6) & Slew Variation Penalties R_delta (6x6) *)
    FOR i_idx := 1 TO 6 DO
        FOR j_idx := 1 TO 6 DO
            R_mat[i_idx, j_idx] := 0.000000;
            R_delta[i_idx, j_idx] := 0.000000;
        END_FOR;
    END_FOR;

    R_mat[1, 1] := 0.500000;   (* Fuel gas valve effort *)
    R_mat[2, 2] := 0.250000;   (* VGV actuator effort *)
    R_mat[3, 3] := 0.800000;   (* Boiler feedwater valve effort *)
    R_mat[4, 4] := 0.600000;   (* Attemperator spray valve effort *)
    R_mat[5, 5] := 0.350000;   (* Steam bypass valve effort *)
    R_mat[6, 6] := 0.400000;   (* Peaking duct burner valve effort *)

    R_delta[1, 1] := 2.500000; (* Fuel gas valve slew penalty *)
    R_delta[2, 2] := 1.800000; (* VGV slew penalty *)
    R_delta[3, 3] := 3.500000; (* Feedwater valve slew penalty *)
    R_delta[4, 4] := 2.000000; (* Spray valve slew penalty *)
    R_delta[5, 5] := 1.500000; (* Bypass valve slew penalty *)
    R_delta[6, 6] := 2.000000; (* Duct burner slew penalty *)

    (* -----------------------------------------------------------------------------------------------------------------
     * ACTUATOR PHYSICAL BOX BOUNDS & SCAN SLEW RATE LIMITS (Ts = 20 ms)
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Lower Bounds u_min *)
    u_min[1] := 0.0;   (* Fuel valve min [%] *)
    u_min[2] := 0.0;   (* VGV min angle [deg] *)
    u_min[3] := 0.0;   (* Feedwater valve min [%] *)
    u_min[4] := 0.0;   (* Spray valve min [%] *)
    u_min[5] := 0.0;   (* Steam bypass min [%] *)
    u_min[6] := 0.0;   (* Duct burner min [%] *)

    (* Upper Bounds u_max *)
    u_max[1] := 100.0; (* Fuel valve max [%] *)
    u_max[2] := 85.0;  (* VGV max angle [deg] *)
    u_max[3] := 100.0; (* Feedwater valve max [%] *)
    u_max[4] := 100.0; (* Spray valve max [%] *)
    u_max[5] := 100.0; (* Steam bypass max [%] *)
    u_max[6] := 100.0; (* Duct burner max [%] *)

    (* Slew Limits du_max per 20 ms scan cycle *)
    du_max[1] := 0.10;  (* Fuel valve: 5.0 %/s -> 0.10 % per 20 ms *)
    du_max[2] := 0.08;  (* VGV: 4.0 deg/s -> 0.08 deg per 20 ms *)
    du_max[3] := 0.20;  (* Feedwater valve: 10.0 %/s -> 0.20 % per 20 ms *)
    du_max[4] := 0.40;  (* Attemperator spray: 20.0 %/s -> 0.40 % per 20 ms *)
    du_max[5] := 0.50;  (* Steam bypass: 25.0 %/s -> 0.50 % per 20 ms *)
    du_max[6] := 0.10;  (* Duct burner: 5.0 %/s -> 0.10 % per 20 ms *)

    (* Initialize State Vectors to Safe Cold Standby Baseline *)
    FOR i_idx := 1 TO 8 DO
        x_hat[i_idx] := 0.0;
        x_pred[i_idx] := 0.0;
        x_ref[i_idx] := 0.0;
        x_corr[i_idx] := 0.0;
    END_FOR;
    x_ref[2] := 620.0; (* Nominal EGT baseline *)
    x_ref[6] := 565.0; (* Nominal main steam temp *)
    x_ref[7] := 490.0; (* Nominal inter-stage temp *)

    FOR j_idx := 1 TO 6 DO
        u_vec[j_idx] := 0.0;
        u_prev[j_idx] := 0.0;
        u_ref[j_idx] := 0.0;
        y_meas[j_idx] := 0.0;
        y_est[j_idx] := 0.0;
        innov_err[j_idx] := 0.0;
    END_FOR;

    bInitialized := TRUE;
END_IF;
"""
