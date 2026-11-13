# steel_dri_builder/part3_phase0_init.py
"""
Part 3: Phase 0 - First-principles matrix initialization and nominal parameters
"""

def get_phase0_init():
    return """(* ==================================================================================================== *)
(* PHASE 0: SYSTEM INITIALIZATION & DISCRETE CYBER-PHYSICAL STATE-SPACE MATRIX INITIALIZATION           *)
(* ==================================================================================================== *)
IF NOT bInitialized THEN
    (* 1. Initialize Heartbeat, Timing and Execution Flags *)
    udiScanCounter := 0;
    udiHeartbeatCounter := 0;
    bHeartbeatBit := FALSE;
    rTs_Seconds := 0.025; (* Discrete sample period 25 ms *)

    (* 2. Discrete Cyber-Physical State Transition Matrix A (8x8) for Ts = 25 ms *)
    (* Gas-Solid Iron Ore Reduction Kinetics & Reactor Thermal Equilibrium Coupling *)
    matA[1, 1] := 0.98520; matA[1, 2] := -0.01250; matA[1, 3] := 0.00340; matA[1, 4] := -0.00820; matA[1, 5] := 0.00110; matA[1, 6] := -0.00150; matA[1, 7] := 0.00450; matA[1, 8] := -0.00620;
    matA[2, 1] := 0.00285; matA[2, 2] := 0.99340; matA[2, 3] := -0.00180; matA[2, 4] := 0.00760; matA[2, 5] := -0.00320; matA[2, 6] := 0.00120; matA[2, 7] := 0.00080; matA[2, 8] := -0.00480;
    matA[3, 1] := 0.00195; matA[3, 2] := 0.00240; matA[3, 3] := 0.96850; matA[3, 4] := -0.00150; matA[3, 5] := 0.00420; matA[3, 6] := 0.00090; matA[3, 7] := -0.00210; matA[3, 8] := 0.00840;
    matA[4, 1] := -0.00080; matA[4, 2] := -0.00310; matA[4, 3] := -0.00120; matA[4, 4] := 0.97650; matA[4, 5] := -0.00850; matA[4, 6] := -0.00240; matA[4, 7] := 0.00060; matA[4, 8] := 0.00150;
    matA[5, 1] := 0.00065; matA[5, 2] := 0.00420; matA[5, 3] := 0.00210; matA[5, 4] := -0.00640; matA[5, 5] := 0.97120; matA[5, 6] := 0.00380; matA[5, 7] := -0.00090; matA[5, 8] := -0.00180;
    matA[6, 1] := -0.00045; matA[6, 2] := 0.00160; matA[6, 3] := 0.00080; matA[6, 4] := -0.00250; matA[6, 5] := 0.00180; matA[6, 6] := 0.98850; matA[6, 7] := -0.00120; matA[6, 8] := -0.00350;
    matA[7, 1] := 0.00350; matA[7, 2] := 0.00120; matA[7, 3] := -0.00240; matA[7, 4] := 0.00080; matA[7, 5] := -0.00150; matA[7, 6] := -0.00060; matA[7, 7] := 0.96200; matA[7, 8] := 0.01250;
    matA[8, 1] := 0.00050; matA[8, 2] := -0.00080; matA[8, 3] := 0.00320; matA[8, 4] := 0.00040; matA[8, 5] := -0.00060; matA[8, 6] := 0.00020; matA[8, 7] := 0.00180; matA[8, 8] := 0.95200;

    (* 3. Input Actuator Control Coupling Matrix B (8x6) *)
    (* u1: Green H2, u2: Reformed Syngas, u3: Heater Fuel, u4: NatGas Carburize, u5: Cooling Blower, u6: Feeder Speed *)
    matB[1, 1] := -0.02450; matB[1, 2] := 0.01850;  matB[1, 3] := 0.08450;  matB[1, 4] := -0.00650; matB[1, 5] := -0.00210; matB[1, 6] := -0.00350;
    matB[2, 1] := 0.04850;  matB[2, 2] := 0.03200;  matB[2, 3] := 0.01250;  matB[2, 4] := 0.00420;  matB[2, 5] := -0.00150; matB[2, 6] := -0.02100;
    matB[3, 1] := 0.00850;  matB[3, 2] := 0.01240;  matB[3, 3] := 0.00450;  matB[3, 4] := 0.00180;  matB[3, 5] := 0.00620;  matB[3, 6] := 0.03500;
    matB[4, 1] := 0.06500;  matB[4, 2] := -0.03450; matB[4, 3] := 0.00120;  matB[4, 4] := -0.01850; matB[4, 5] := 0.00040;  matB[4, 6] := -0.00080;
    matB[5, 1] := -0.03800; matB[5, 2] := 0.02850;  matB[5, 3] := 0.00240;  matB[5, 4] := 0.01450;  matB[5, 5] := -0.00120; matB[5, 6] := 0.00150;
    matB[6, 1] := -0.01200; matB[6, 2] := 0.00850;  matB[6, 3] := -0.00150; matB[6, 4] := 0.05200;  matB[6, 5] := -0.00350; matB[6, 6] := -0.00850;
    matB[7, 1] := -0.00450; matB[7, 2] := 0.00250;  matB[7, 3] := 0.00850;  matB[7, 4] := -0.00550; matB[7, 5] := -0.06850; matB[7, 6] := 0.04500;
    matB[8, 1] := 0.00000;  matB[8, 2] := 0.00000;  matB[8, 3] := 0.00000;  matB[8, 4] := 0.00000;  matB[8, 5] := 0.00000;  matB[8, 6] := 0.07850;

    (* 4. Output Sensor Measurement Matrix C (6x8) *)
    (* y1: Bustle Temp, y2: Top Gas H2/CO, y3: Shaft DP, y4: Top Gas CO2, y5: DRI Temp, y6: Feeder Extraction Rate *)
    matC[1, 1] := 1.00000; matC[1, 2] := 0.00000; matC[1, 3] := 0.00000; matC[1, 4] := 0.00000; matC[1, 5] := 0.00000; matC[1, 6] := 0.00000; matC[1, 7] := 0.00000; matC[1, 8] := 0.00000;
    matC[2, 1] := 0.00000; matC[2, 2] := 0.00000; matC[2, 3] := 0.00000; matC[2, 4] := 1.00000; matC[2, 5] := 0.00000; matC[2, 6] := 0.00000; matC[2, 7] := 0.00000; matC[2, 8] := 0.00000;
    matC[3, 1] := 0.00000; matC[3, 2] := 0.00000; matC[3, 3] := 1.00000; matC[3, 4] := 0.00000; matC[3, 5] := 0.00000; matC[3, 6] := 0.00000; matC[3, 7] := 0.00000; matC[3, 8] := 0.00000;
    matC[4, 1] := 0.00000; matC[4, 2] := 0.00000; matC[4, 3] := 0.00000; matC[4, 4] := 0.00000; matC[4, 5] := 1.00000; matC[4, 6] := 0.00000; matC[4, 7] := 0.00000; matC[4, 8] := 0.00000;
    matC[5, 1] := 0.08500; matC[5, 2] := 0.04200; matC[5, 3] := 0.00000; matC[5, 4] := 0.00000; matC[5, 5] := 0.00000; matC[5, 6] := 0.00000; matC[5, 7] := 0.88500; matC[5, 8] := 0.00000;
    matC[6, 1] := 0.00000; matC[6, 2] := 0.00000; matC[6, 3] := 0.00000; matC[6, 4] := 0.00000; matC[6, 5] := 0.00000; matC[6, 6] := 0.00000; matC[6, 7] := 0.00000; matC[6, 8] := 1.00000;

    (* 5. Feedthrough Direct Transmission Matrix D (6x6) *)
    matD[1, 1] := 0.00000; matD[1, 2] := 0.00000; matD[1, 3] := 0.00120; matD[1, 4] := 0.00000; matD[1, 5] := 0.00000; matD[1, 6] := 0.00000;
    matD[2, 1] := 0.00250; matD[2, 2] := -0.00180; matD[2, 3] := 0.00000; matD[2, 4] := 0.00000; matD[2, 5] := 0.00000; matD[2, 6] := 0.00000;
    matD[3, 1] := 0.00080; matD[3, 2] := 0.00120; matD[3, 3] := 0.00000; matD[3, 4] := 0.00000; matD[3, 5] := 0.00050; matD[3, 6] := 0.00350;
    matD[4, 1] := -0.00150; matD[4, 2] := 0.00140; matD[4, 3] := 0.00000; matD[4, 4] := 0.00080; matD[4, 5] := 0.00000; matD[4, 6] := 0.00000;
    matD[5, 1] := 0.00000; matD[5, 2] := 0.00000; matD[5, 3] := 0.00000; matD[5, 4] := 0.00000; matD[5, 5] := -0.00420; matD[5, 6] := 0.00280;
    matD[6, 1] := 0.00000; matD[6, 2] := 0.00000; matD[6, 3] := 0.00000; matD[6, 4] := 0.00000; matD[6, 5] := 0.00000; matD[6, 6] := 0.00150;

    (* 6. Steady-State Luenberger Observer Innovation Gain Matrix L (8x6) *)
    matL[1, 1] := 0.18500; matL[1, 2] := -0.01200; matL[1, 3] := 0.00450; matL[1, 4] := 0.00280; matL[1, 5] := 0.02100; matL[1, 6] := -0.00180;
    matL[2, 1] := 0.01450; matL[2, 2] := 0.08200;  matL[2, 3] := -0.01500; matL[2, 4] := -0.04500; matL[2, 5] := 0.01800; matL[2, 6] := -0.02400;
    matL[3, 1] := 0.00620; matL[3, 2] := -0.00450; matL[3, 3] := 0.22500; matL[3, 4] := 0.01850; matL[3, 5] := -0.00850; matL[3, 6] := 0.04200;
    matL[4, 1] := -0.00350; matL[4, 2] := 0.21500; matL[4, 3] := -0.00850; matL[4, 4] := -0.06500; matL[4, 5] := 0.00120; matL[4, 6] := 0.00250;
    matL[5, 1] := 0.00280; matL[5, 2] := -0.07500; matL[5, 3] := 0.01450; matL[5, 4] := 0.19500; matL[5, 5] := -0.00250; matL[5, 6] := -0.00380;
    matL[6, 1] := -0.00150; matL[6, 2] := -0.02400; matL[6, 3] := 0.00550; matL[6, 4] := 0.03800; matL[6, 5] := -0.00450; matL[6, 6] := -0.01250;
    matL[7, 1] := 0.01850; matL[7, 2] := 0.00450;  matL[7, 3] := -0.01250; matL[7, 4] := -0.00650; matL[7, 5] := 0.28500; matL[7, 6] := 0.06500;
    matL[8, 1] := 0.00080; matL[8, 2] := 0.00150;  matL[8, 3] := 0.01850; matL[8, 4] := -0.00120; matL[8, 5] := 0.01450; matL[8, 6] := 0.32500;

    (* 7. Model Predictive Control State Penalty Weight Matrix Q (8x8) *)
    FOR idx_i := 1 TO 8 DO
        FOR idx_j := 1 TO 8 DO
            matQ[idx_i, idx_j] := 0.00000;
        END_FOR;
    END_FOR;
    matQ[1, 1] := 3.50000;  (* x1 Bustle Inlet Temperature Weight *)
    matQ[2, 2] := 45.00000; (* x2 Metallization Degree Primary Quality Penalty *)
    matQ[3, 3] := 18.50000; (* x3 Shaft Differential Pressure Fluidization Penalty *)
    matQ[4, 4] := 8.20000;  (* x4 Top Gas H2/CO Ratio Decoupling Weight *)
    matQ[5, 5] := 6.50000;  (* x5 Top Gas CO2 Oxidation Waste Weight *)
    matQ[6, 6] := 28.00000; (* x6 DRI Product Carburization Fe3C Weight *)
    matQ[7, 7] := 4.20000;  (* x7 Bottom Cooling Discharge Temp Penalty *)
    matQ[8, 8] := 12.00000; (* x8 Discharge Feeder Throughput Weight *)
    (* Off-diagonal cross-coupling penalties *)
    matQ[1, 2] := -0.45000; matQ[2, 1] := -0.45000;
    matQ[2, 4] := 0.65000;  matQ[4, 2] := 0.65000;
    matQ[3, 8] := 0.85000;  matQ[8, 3] := 0.85000;
    matQ[5, 6] := -0.35000; matQ[6, 5] := -0.35000;

    (* 8. Model Predictive Control Actuator Effort Penalty Matrix R (6x6) *)
    FOR idx_i := 1 TO 6 DO
        FOR idx_j := 1 TO 6 DO
            matR[idx_i, idx_j] := 0.00000;
        END_FOR;
    END_FOR;
    matR[1, 1] := 1.85000; (* u1 Green Hydrogen Modulation Cost *)
    matR[2, 2] := 1.15000; (* u2 Reformed Syngas Valve Cost *)
    matR[3, 3] := 2.45000; (* u3 Preheater Fuel Modulation Cost *)
    matR[4, 4] := 3.20000; (* u4 Natural Gas Carburization Trim Cost *)
    matR[5, 5] := 0.95000; (* u5 Cooling Gas Blower Inverter Rate Penalty *)
    matR[6, 6] := 1.65000; (* u6 Rotary Discharge Feeder Speed Slew Cost *)
    (* Coordinated gas mix cross-penalties *)
    matR[1, 2] := 0.38000; matR[2, 1] := 0.38000;
    matR[1, 3] := -0.22000; matR[3, 1] := -0.22000;

    (* 9. Terminal State Penalty Matrix P (8x8) ~ 2.4x Q *)
    FOR idx_i := 1 TO 8 DO
        FOR idx_j := 1 TO 8 DO
            matP[idx_i, idx_j] := matQ[idx_i, idx_j] * 2.40000;
        END_FOR;
    END_FOR;

    (* 10. Actuator Physical Constraints & Slew Boundaries *)
    u_Min[1] := 0.0;   u_Max[1] := 100.0; du_MaxSlew[1] := 1.50; (* Green H2 Valve *)
    u_Min[2] := 0.0;   u_Max[2] := 100.0; du_MaxSlew[2] := 1.80; (* Syngas Main Valve *)
    u_Min[3] := 0.0;   u_Max[3] := 100.0; du_MaxSlew[3] := 0.90; (* Preheater Fuel Valve *)
    u_Min[4] := 0.0;   u_Max[4] := 100.0; du_MaxSlew[4] := 0.75; (* NatGas Carburization Trim *)
    u_Min[5] := 0.0;   u_Max[5] := 100.0; du_MaxSlew[5] := 2.20; (* Cooling Gas Blower Inverter *)
    u_Min[6] := 0.0;   u_Max[6] := 100.0; du_MaxSlew[6] := 1.25; (* Rotary Discharge Feeder *)

    (* 11. Initial State Vector & Setpoint References *)
    x_State[1] := 950.0; (* Bustle Gas Temp [deg C] *)
    x_State[2] := 95.0;  (* Metallization Degree [% Fe] *)
    x_State[3] := 52.0;  (* Shaft DP [kPa] *)
    x_State[4] := 2.85;  (* Top Gas H2/CO Molar Ratio [ratio] *)
    x_State[5] := 15.2;  (* Top Gas CO2 [% vol] *)
    x_State[6] := 2.15;  (* DRI Product Carbon [wt% C] *)
    x_State[7] := 65.0;  (* Cooling Gas Bottom Discharge Temp [deg C] *)
    x_State[8] := 150.0; (* Discharge Feeder Rate [t/h] *)

    FOR idx_i := 1 TO 8 DO
        x_Hat[idx_i] := x_State[idx_i];
        x_Pred[idx_i] := x_State[idx_i];
        x_Ref[idx_i] := x_State[idx_i];
    END_FOR;

    FOR idx_i := 1 TO 6 DO
        u_Act[idx_i] := 0.0;
        u_Prev[idx_i] := 0.0;
        du_Act[idx_i] := 0.0;
        u_Ref[idx_i] := 0.0;
    END_FOR;
    u_Ref[1] := 45.0; (* Nominal Green H2 Injection *)
    u_Ref[2] := 55.0; (* Nominal Reformed Syngas Flow *)
    u_Ref[3] := 62.0; (* Nominal Preheater Duty *)
    u_Ref[4] := 18.0; (* Nominal Natural Gas Enrichment *)
    u_Ref[5] := 75.0; (* Nominal Cooling Loop Blower *)
    u_Ref[6] := 65.0; (* Nominal Feeder Rotation Speed *)

    FOR idx_n := 1 TO 5 DO
        FOR idx_j := 1 TO 6 DO
            u_MPC_Trajectory[idx_n, idx_j] := u_Ref[idx_j];
            grad_MPC[idx_n, idx_j] := 0.0;
        END_FOR;
        FOR idx_i := 1 TO 8 DO
            x_MPC_Predict[idx_n, idx_i] := x_State[idx_i];
        END_FOR;
    END_FOR;

    FOR idx_i := 1 TO 16 DO
        arrHist_Metallization[idx_i] := 95.0;
        arrHist_ShaftDP[idx_i] := 52.0;
    END_FOR;

    rTMR_Bustle_LastGood := 950.0;
    rTMR_ShaftDP_LastGood := 52.0;
    rTMR_GasH2CO_LastGood := 2.85;
    rTMR_GasCO2_LastGood := 15.2;
    rTMR_Burden_LastGood := 18.5;
    rTMR_DRITemp_LastGood := 680.0;

    iState := 0; (* Start in cold inert nitrogen standby *)
    iPrevState := -1;
    tCurrentStateDwell := T#0ms;

    bInitialized := TRUE;
END_IF;

(* Advance Discrete Scan Cycle Counter & Diagnostic Flasher *)
udiScanCounter := udiScanCounter + 1;
udiHeartbeatCounter := udiHeartbeatCounter + 1;
IF (udiHeartbeatCounter MOD 40) = 0 THEN
    bHeartbeatBit := NOT bHeartbeatBit;
END_IF;
"""
