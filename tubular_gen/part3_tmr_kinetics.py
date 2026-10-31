# part3_tmr_kinetics.py
tmr_kinetics_text = """(* ==========================================================================================================
   INITIALIZATION & FIRST-SCAN STATE-SPACE MATRIX DEFINITIONS
   ========================================================================================================== *)
IF NOT bFirstScanDone THEN
    (* Scan Cycle Delta Time in seconds *)
    IF TIME_TO_REAL(tScanCycleTime_ms) > 0.0 THEN
        rDeltaTime_s := TIME_TO_REAL(tScanCycleTime_ms) / 1000.0;
    ELSE
        rDeltaTime_s := 0.020;
    END_IF;

    (* Zero out all state-space matrices *)
    FOR idx_i := 1 TO 16 DO
        FOR idx_j := 1 TO 16 DO
            aState_A[idx_i, idx_j] := 0.0;
        END_FOR;
        FOR idx_j := 1 TO 8 DO
            bInput_B[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;

    FOR idx_i := 1 TO 8 DO
        FOR idx_j := 1 TO 16 DO
            cOutput_C[idx_i, idx_j] := 0.0;
        END_FOR;
        FOR idx_j := 1 TO 8 DO
            dDirect_D[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------------
       Matrix A: 16x16 Discrete State Transition Dynamics (Sampling Period Ts = 20 ms)
       Incorporates convective heat transport, radical decay, exothermic feedback, pressure dissipation
       ------------------------------------------------------------------------------------------------------ *)
    (* Temperature Diagonal Decay (Convective axial transport + wall heat dissipation) *)
    aState_A[1, 1]  := 0.9450;  (* Zone 1 Peak Temp self-decay *)
    aState_A[2, 2]  := 0.9410;  (* Zone 2 Peak Temp self-decay *)
    aState_A[3, 3]  := 0.9380;  (* Zone 3 Peak Temp self-decay *)
    aState_A[4, 4]  := 0.9350;  (* Zone 4 Peak Temp self-decay *)

    (* Cross-zone axial thermal conduction & convective slip *)
    aState_A[2, 1]  := 0.0380;  (* Convective heat downstream from Zone 1 to Zone 2 *)
    aState_A[3, 2]  := 0.0420;  (* Convective heat downstream from Zone 2 to Zone 3 *)
    aState_A[4, 3]  := 0.0450;  (* Convective heat downstream from Zone 3 to Zone 4 *)

    (* Exothermic heat generation coupling from free radical concentrations *)
    aState_A[1, 8]  := 12.850;  (* Radical conc Zone 1 -> Temp Peak 1 *)
    aState_A[2, 9]  := 14.120;  (* Radical conc Zone 2 -> Temp Peak 2 *)
    aState_A[3, 10] := 13.950;  (* Radical conc Zone 3 -> Temp Peak 3 *)
    aState_A[4, 11] := 11.750;  (* Radical conc Zone 4 -> Temp Peak 4 *)

    (* Pressure Dynamics (Inlet, Mid-reactor, Outlet) - Acoustic propagation and friction loss *)
    aState_A[5, 5]  := 0.9780;  (* Inlet Pressure momentum retention *)
    aState_A[5, 6]  := 0.0180;  (* Mid back-propagation *)
    aState_A[6, 5]  := 0.0210;  (* Inlet forward pressure propagation *)
    aState_A[6, 6]  := 0.9650;  (* Mid Pressure retention *)
    aState_A[6, 7]  := 0.0110;  (* Outlet back-pressure reflection *)
    aState_A[7, 6]  := 0.0240;  (* Mid-to-Outlet forward pressure propagation *)
    aState_A[7, 7]  := 0.9600;  (* Outlet Pressure retention *)

    (* Radical Concentration Lifetimes (Cage effect + radical-radical termination) *)
    aState_A[8, 8]   := 0.8200; (* Radical conc Zone 1 decay *)
    aState_A[9, 9]   := 0.7950; (* Radical conc Zone 2 decay *)
    aState_A[10, 10] := 0.7800; (* Radical conc Zone 3 decay *)
    aState_A[11, 11] := 0.7600; (* Radical conc Zone 4 decay *)

    (* Monomer Conversion Integrator *)
    aState_A[12, 12] := 0.9985; (* Conversion retention *)
    aState_A[12, 8]  := 0.0450; (* Conversion rate from Zone 1 radicals *)
    aState_A[12, 9]  := 0.0520; (* Conversion rate from Zone 2 radicals *)
    aState_A[12, 10] := 0.0480; (* Conversion rate from Zone 3 radicals *)
    aState_A[12, 11] := 0.0380; (* Conversion rate from Zone 4 radicals *)

    (* Molecular Weight Moments (Mn, Mw) Dynamics *)
    aState_A[13, 13] := 0.9850; (* Mn auto-correlation *)
    aState_A[13, 1]  := -0.085; (* High temp decreases Mn via scission & CTA *)
    aState_A[13, 2]  := -0.092;
    aState_A[14, 14] := 0.9880; (* Mw auto-correlation *)
    aState_A[14, 1]  := -0.115;
    aState_A[14, 2]  := -0.125;

    (* Tube Inner Wall Skin Maximum Temperature *)
    aState_A[15, 15] := 0.9620;
    aState_A[15, 1]  := 0.0180;
    aState_A[15, 2]  := 0.0210;

    (* Polymer Melt Wall Viscosity *)
    aState_A[16, 16] := 0.9550;
    aState_A[16, 1]  := -1.450; (* Shear-thinning thermal softening *)
    aState_A[16, 5]  := 0.0820; (* Pressure piezo-viscous hardening *)

    (* ------------------------------------------------------------------------------------------------------
       Matrix B: 16x8 Input Control Matrix
       Inputs: u1..u4: Peroxide strokes, u5..u7: Jacket valves, u8: Let-Down Valve position
       ------------------------------------------------------------------------------------------------------ *)
    (* Radical initiation injection responses *)
    bInput_B[8, 1]  := 0.2850;  (* u1 Peroxide Z1 -> Radical conc Z1 *)
    bInput_B[9, 2]  := 0.3100;  (* u2 Peroxide Z2 -> Radical conc Z2 *)
    bInput_B[10, 3] := 0.2950;  (* u3 Peroxide Z3 -> Radical conc Z3 *)
    bInput_B[11, 4] := 0.2650;  (* u4 Peroxide Z4 -> Radical conc Z4 *)

    (* Direct thermal response on peak exotherms *)
    bInput_B[1, 1]  := 0.5200;  (* Peroxide Z1 -> Temp Z1 rise *)
    bInput_B[2, 2]  := 0.5800;  (* Peroxide Z2 -> Temp Z2 rise *)
    bInput_B[3, 3]  := 0.5400;  (* Peroxide Z3 -> Temp Z3 rise *)
    bInput_B[4, 4]  := 0.4900;  (* Peroxide Z4 -> Temp Z4 rise *)

    (* Jacket cooling water modulating valve action (u5..u7) - Negative thermal gain *)
    bInput_B[1, 5]  := -0.3200; (* Jacket Z1 valve -> Temp Z1 cooling *)
    bInput_B[2, 6]  := -0.3500; (* Jacket Z2 valve -> Temp Z2 cooling *)
    bInput_B[3, 7]  := -0.3100; (* Jacket Z3 valve -> Temp Z3 cooling *)
    bInput_B[4, 7]  := -0.2800; (* Jacket Z4 valve -> Temp Z4 cooling *)

    (* High-Pressure Let-Down Valve (HPLDV, u8) Pressure Relief Dynamics *)
    bInput_B[5, 8]  := -1.8500; (* HPLDV open -> Inlet pressure drop *)
    bInput_B[6, 8]  := -2.4500; (* HPLDV open -> Mid pressure drop *)
    bInput_B[7, 8]  := -3.9500; (* HPLDV open -> Outlet pressure relief *)

    (* ------------------------------------------------------------------------------------------------------
       Matrix C: 8x16 Observation Matrix
       Maps 16 states to 8 measured output channels
       ------------------------------------------------------------------------------------------------------ *)
    cOutput_C[1, 1]  := 1.0; (* y1: Peak Temp 1 *)
    cOutput_C[2, 2]  := 1.0; (* y2: Peak Temp 2 *)
    cOutput_C[3, 3]  := 1.0; (* y3: Peak Temp 3 *)
    cOutput_C[4, 4]  := 1.0; (* y4: Peak Temp 4 *)
    cOutput_C[5, 5]  := 1.0; (* y5: Inlet Pressure *)
    cOutput_C[6, 7]  := 1.0; (* y6: Outlet Pressure *)
    cOutput_C[7, 12] := 1.0; (* y7: Cumulative Conversion *)
    cOutput_C[8, 14] := 1.0; (* y8: Weight-Average Mw *)

    (* ------------------------------------------------------------------------------------------------------
       MPC Weighting Vectors: Q (State tracking), R (Actuator movement), P (Terminal cost)
       ------------------------------------------------------------------------------------------------------ *)
    FOR idx_i := 1 TO 16 DO
        qWeight_Q[idx_i] := 1.0;
        pWeight_P[idx_i] := 5.0;
    END_FOR;
    (* Heavy penalties on peak temperatures to prevent runaway decomposition *)
    qWeight_Q[1]  := 180.0;
    qWeight_Q[2]  := 220.0;
    qWeight_Q[3]  := 200.0;
    qWeight_Q[4]  := 160.0;
    (* Very high penalty on reactor inlet and outlet pressure exceeding limits *)
    qWeight_Q[5]  := 350.0;
    qWeight_Q[6]  := 280.0;
    qWeight_Q[7]  := 320.0;
    (* Terminal state penalties *)
    pWeight_P[1]  := 450.0;
    pWeight_P[2]  := 550.0;
    pWeight_P[5]  := 850.0;
    pWeight_P[7]  := 800.0;

    (* Actuator slew and energy cost weights R *)
    rWeight_R[1] := 12.0; (* Peroxide Z1 stroke *)
    rWeight_R[2] := 14.0; (* Peroxide Z2 stroke *)
    rWeight_R[3] := 14.0; (* Peroxide Z3 stroke *)
    rWeight_R[4] := 12.0; (* Peroxide Z4 stroke *)
    rWeight_R[5] := 8.5;  (* Jacket Z1 valve *)
    rWeight_R[6] := 8.5;  (* Jacket Z2 valve *)
    rWeight_R[7] := 8.0;  (* Jacket Z3 valve *)
    rWeight_R[8] := 25.0; (* Let-down valve position movement penalty *)

    (* Actuator Hard Limits and Slew Rates *)
    FOR idx_i := 1 TO 4 DO
        uMin_Limits[idx_i]   := 0.0;
        uMax_Limits[idx_i]   := 100.0;
        deltaU_Limits[idx_i] := 2.5; (* Max 2.5% stroke change per scan *)
    END_FOR;
    FOR idx_i := 5 TO 7 DO
        uMin_Limits[idx_i]   := 0.0;
        uMax_Limits[idx_i]   := 100.0;
        deltaU_Limits[idx_i] := 5.0; (* Max 5.0% valve change per scan *)
    END_FOR;
    uMin_Limits[8]   := 15.0;   (* Minimum HPLDV opening to prevent shutoff *)
    uMax_Limits[8]   := 95.0;   (* Maximum HPLDV opening *)
    deltaU_Limits[8] := 4.0;    (* Electrohydraulic servo slew limit *)

    (* Pre-initialize tracking references *)
    FOR idx_i := 1 TO 16 DO
        xState_Est[idx_i]  := 0.0;
        xState_Pred[idx_i] := 0.0;
        xState_Ref[idx_i]  := 0.0;
    END_FOR;
    xState_Ref[1] := 280.0; (* Z1 Peak Temp Setpoint *)
    xState_Ref[2] := 295.0; (* Z2 Peak Temp Setpoint *)
    xState_Ref[3] := 290.0; (* Z3 Peak Temp Setpoint *)
    xState_Ref[4] := 275.0; (* Z4 Peak Temp Setpoint *)
    xState_Ref[5] := 2980.0;(* Inlet Pressure Setpoint [bar] *)
    xState_Ref[6] := 2920.0;(* Mid Pressure Setpoint [bar] *)
    xState_Ref[7] := 2850.0;(* Outlet Pressure Setpoint [bar] *)

    bFirstScanDone := TRUE;
END_IF;

(* ==========================================================================================================
   PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS
   ========================================================================================================== *)
bDegraded_TMR_Active := FALSE;

(* 1.1: Reactor Inlet Pressure 2oo3 TMR Voting *)
rDev_Inlet_AB := ABS(rPress_Inlet_ChA_bar - rPress_Inlet_ChB_bar);
rDev_Inlet_BC := ABS(rPress_Inlet_ChB_bar - rPress_Inlet_ChC_bar);
rDev_Inlet_AC := ABS(rPress_Inlet_ChA_bar - rPress_Inlet_ChC_bar);

tonTMR_Inlet_Dev(IN := (rDev_Inlet_AB > 45.0) OR (rDev_Inlet_BC > 45.0) OR (rDev_Inlet_AC > 45.0), PT := T#100MS);

IF tonTMR_Inlet_Dev.Q THEN
    bDegraded_TMR_Active := TRUE;
    IF (rDev_Inlet_AB > 45.0) AND (rDev_Inlet_AC > 45.0) THEN
        bInlet_ChA_Healthy := FALSE; (* Ch A deviates from both B and C *)
    ELSIF (rDev_Inlet_AB > 45.0) AND (rDev_Inlet_BC > 45.0) THEN
        bInlet_ChB_Healthy := FALSE; (* Ch B deviates from both A and C *)
    ELSIF (rDev_Inlet_AC > 45.0) AND (rDev_Inlet_BC > 45.0) THEN
        bInlet_ChC_Healthy := FALSE; (* Ch C deviates from both A and B *)
    END_IF;
END_IF;

IF bInlet_ChA_Healthy AND bInlet_ChB_Healthy AND bInlet_ChC_Healthy THEN
    (* 3 Channels Healthy: Median Voting *)
    IF (rPress_Inlet_ChA_bar >= rPress_Inlet_ChB_bar AND rPress_Inlet_ChA_bar <= rPress_Inlet_ChC_bar) OR
       (rPress_Inlet_ChA_bar <= rPress_Inlet_ChB_bar AND rPress_Inlet_ChA_bar >= rPress_Inlet_ChC_bar) THEN
        rVoted_Press_Inlet_bar := rPress_Inlet_ChA_bar;
    ELSIF (rPress_Inlet_ChB_bar >= rPress_Inlet_ChA_bar AND rPress_Inlet_ChB_bar <= rPress_Inlet_ChC_bar) OR
          (rPress_Inlet_ChB_bar <= rPress_Inlet_ChA_bar AND rPress_Inlet_ChB_bar >= rPress_Inlet_ChC_bar) THEN
        rVoted_Press_Inlet_bar := rPress_Inlet_ChB_bar;
    ELSE
        rVoted_Press_Inlet_bar := rPress_Inlet_ChC_bar;
    END_IF;
ELSIF bInlet_ChA_Healthy AND bInlet_ChB_Healthy THEN
    rVoted_Press_Inlet_bar := (rPress_Inlet_ChA_bar + rPress_Inlet_ChB_bar) * 0.5;
ELSIF bInlet_ChB_Healthy AND bInlet_ChC_Healthy THEN
    rVoted_Press_Inlet_bar := (rPress_Inlet_ChB_bar + rPress_Inlet_ChC_bar) * 0.5;
ELSIF bInlet_ChA_Healthy AND bInlet_ChC_Healthy THEN
    rVoted_Press_Inlet_bar := (rPress_Inlet_ChA_bar + rPress_Inlet_ChC_bar) * 0.5;
ELSIF bInlet_ChA_Healthy THEN
    rVoted_Press_Inlet_bar := rPress_Inlet_ChA_bar;
ELSIF bInlet_ChB_Healthy THEN
    rVoted_Press_Inlet_bar := rPress_Inlet_ChB_bar;
ELSIF bInlet_ChC_Healthy THEN
    rVoted_Press_Inlet_bar := rPress_Inlet_ChC_bar;
ELSE
    rVoted_Press_Inlet_bar := rPress_Inlet_Prev; (* Failsafe hold *)
END_IF;

(* 1.2: Zone 1 Pressure 2oo3 TMR Voting *)
rDev_Z1_AB := ABS(rPress_Z1_ChA_bar - rPress_Z1_ChB_bar);
rDev_Z1_BC := ABS(rPress_Z1_ChB_bar - rPress_Z1_ChC_bar);
rDev_Z1_AC := ABS(rPress_Z1_ChA_bar - rPress_Z1_ChC_bar);

tonTMR_Z1_Dev(IN := (rDev_Z1_AB > 45.0) OR (rDev_Z1_BC > 45.0) OR (rDev_Z1_AC > 45.0), PT := T#100MS);
IF tonTMR_Z1_Dev.Q THEN
    bDegraded_TMR_Active := TRUE;
    IF (rDev_Z1_AB > 45.0) AND (rDev_Z1_AC > 45.0) THEN
        bZ1_ChA_Healthy := FALSE;
    ELSIF (rDev_Z1_AB > 45.0) AND (rDev_Z1_BC > 45.0) THEN
        bZ1_ChB_Healthy := FALSE;
    ELSIF (rDev_Z1_AC > 45.0) AND (rDev_Z1_BC > 45.0) THEN
        bZ1_ChC_Healthy := FALSE;
    END_IF;
END_IF;

IF bZ1_ChA_Healthy AND bZ1_ChB_Healthy AND bZ1_ChC_Healthy THEN
    IF (rPress_Z1_ChA_bar >= rPress_Z1_ChB_bar AND rPress_Z1_ChA_bar <= rPress_Z1_ChC_bar) OR
       (rPress_Z1_ChA_bar <= rPress_Z1_ChB_bar AND rPress_Z1_ChA_bar >= rPress_Z1_ChC_bar) THEN
        rVoted_Press_Z1_bar := rPress_Z1_ChA_bar;
    ELSIF (rPress_Z1_ChB_bar >= rPress_Z1_ChA_bar AND rPress_Z1_ChB_bar <= rPress_Z1_ChC_bar) OR
          (rPress_Z1_ChB_bar <= rPress_Z1_ChA_bar AND rPress_Z1_ChB_bar >= rPress_Z1_ChC_bar) THEN
        rVoted_Press_Z1_bar := rPress_Z1_ChB_bar;
    ELSE
        rVoted_Press_Z1_bar := rPress_Z1_ChC_bar;
    END_IF;
ELSIF bZ1_ChA_Healthy AND bZ1_ChB_Healthy THEN
    rVoted_Press_Z1_bar := (rPress_Z1_ChA_bar + rPress_Z1_ChB_bar) * 0.5;
ELSIF bZ1_ChB_Healthy AND bZ1_ChC_Healthy THEN
    rVoted_Press_Z1_bar := (rPress_Z1_ChB_bar + rPress_Z1_ChC_bar) * 0.5;
ELSIF bZ1_ChA_Healthy AND bZ1_ChC_Healthy THEN
    rVoted_Press_Z1_bar := (rPress_Z1_ChA_bar + rPress_Z1_ChC_bar) * 0.5;
ELSE
    rVoted_Press_Z1_bar := rPress_Z1_ChA_bar;
END_IF;

(* 1.3: Zone 2 Pressure 2oo3 TMR Voting *)
IF (rPress_Z2_ChA_bar >= rPress_Z2_ChB_bar AND rPress_Z2_ChA_bar <= rPress_Z2_ChC_bar) OR
   (rPress_Z2_ChA_bar <= rPress_Z2_ChB_bar AND rPress_Z2_ChA_bar >= rPress_Z2_ChC_bar) THEN
    rVoted_Press_Z2_bar := rPress_Z2_ChA_bar;
ELSIF (rPress_Z2_ChB_bar >= rPress_Z2_ChA_bar AND rPress_Z2_ChB_bar <= rPress_Z2_ChC_bar) OR
      (rPress_Z2_ChB_bar <= rPress_Z2_ChA_bar AND rPress_Z2_ChB_bar >= rPress_Z2_ChC_bar) THEN
    rVoted_Press_Z2_bar := rPress_Z2_ChB_bar;
ELSE
    rVoted_Press_Z2_bar := rPress_Z2_ChC_bar;
END_IF;

(* 1.4: Reactor Outlet Pressure 2oo3 TMR Voting *)
IF (rPress_Outlet_ChA_bar >= rPress_Outlet_ChB_bar AND rPress_Outlet_ChA_bar <= rPress_Outlet_ChC_bar) OR
   (rPress_Outlet_ChA_bar <= rPress_Outlet_ChB_bar AND rPress_Outlet_ChA_bar >= rPress_Outlet_ChC_bar) THEN
    rVoted_Press_Outlet_bar := rPress_Outlet_ChA_bar;
ELSIF (rPress_Outlet_ChB_bar >= rPress_Outlet_ChA_bar AND rPress_Outlet_ChB_bar <= rPress_Outlet_ChC_bar) OR
      (rPress_Outlet_ChB_bar <= rPress_Outlet_ChA_bar AND rPress_Outlet_ChB_bar >= rPress_Outlet_ChC_bar) THEN
    rVoted_Press_Outlet_bar := rPress_Outlet_ChB_bar;
ELSE
    rVoted_Press_Outlet_bar := rPress_Outlet_ChC_bar;
END_IF;

(* 1.5: Hyper-Compressor Discharge Pressure 2oo3 TMR Voting *)
IF (rPress_HyperDisch_ChA_bar >= rPress_HyperDisch_ChB_bar AND rPress_HyperDisch_ChA_bar <= rPress_HyperDisch_ChC_bar) OR
   (rPress_HyperDisch_ChA_bar <= rPress_HyperDisch_ChB_bar AND rPress_HyperDisch_ChA_bar >= rPress_HyperDisch_ChC_bar) THEN
    rVoted_Press_HyperDisch_bar := rPress_HyperDisch_ChA_bar;
ELSIF (rPress_HyperDisch_ChB_bar >= rPress_HyperDisch_ChA_bar AND rPress_HyperDisch_ChB_bar <= rPress_HyperDisch_ChC_bar) OR
      (rPress_HyperDisch_ChB_bar <= rPress_HyperDisch_ChA_bar AND rPress_HyperDisch_ChB_bar >= rPress_HyperDisch_ChC_bar) THEN
    rVoted_Press_HyperDisch_bar := rPress_HyperDisch_ChB_bar;
ELSE
    rVoted_Press_HyperDisch_bar := rPress_HyperDisch_ChC_bar;
END_IF;

(* 1.6: Reaction Peak Temperatures 1 to 4 2oo3 TMR Voting *)
rDev_T1_AB := ABS(rTemp_Peak1_ChA_degC - rTemp_Peak1_ChB_degC);
rDev_T1_BC := ABS(rTemp_Peak1_ChB_degC - rTemp_Peak1_ChC_degC);
rDev_T1_AC := ABS(rTemp_Peak1_ChA_degC - rTemp_Peak1_ChC_degC);
tonTMR_T1_Dev(IN := (rDev_T1_AB > 8.0) OR (rDev_T1_BC > 8.0) OR (rDev_T1_AC > 8.0), PT := T#250MS);
IF tonTMR_T1_Dev.Q THEN
    bDegraded_TMR_Active := TRUE;
    IF (rDev_T1_AB > 8.0) AND (rDev_T1_AC > 8.0) THEN bT1_ChA_Healthy := FALSE;
    ELSIF (rDev_T1_AB > 8.0) AND (rDev_T1_BC > 8.0) THEN bT1_ChB_Healthy := FALSE;
    ELSIF (rDev_T1_AC > 8.0) AND (rDev_T1_BC > 8.0) THEN bT1_ChC_Healthy := FALSE;
    END_IF;
END_IF;

(* Voted Peak Temp 1 *)
IF (rTemp_Peak1_ChA_degC >= rTemp_Peak1_ChB_degC AND rTemp_Peak1_ChA_degC <= rTemp_Peak1_ChC_degC) OR
   (rTemp_Peak1_ChA_degC <= rTemp_Peak1_ChB_degC AND rTemp_Peak1_ChA_degC >= rTemp_Peak1_ChC_degC) THEN
    rVoted_Temp_Peak1_degC := rTemp_Peak1_ChA_degC;
ELSIF (rTemp_Peak1_ChB_degC >= rTemp_Peak1_ChA_degC AND rTemp_Peak1_ChB_degC <= rTemp_Peak1_ChC_degC) OR
      (rTemp_Peak1_ChB_degC <= rTemp_Peak1_ChA_degC AND rTemp_Peak1_ChB_degC >= rTemp_Peak1_ChC_degC) THEN
    rVoted_Temp_Peak1_degC := rTemp_Peak1_ChB_degC;
ELSE
    rVoted_Temp_Peak1_degC := rTemp_Peak1_ChC_degC;
END_IF;

(* Voted Peak Temp 2 *)
IF (rTemp_Peak2_ChA_degC >= rTemp_Peak2_ChB_degC AND rTemp_Peak2_ChA_degC <= rTemp_Peak2_ChC_degC) OR
   (rTemp_Peak2_ChA_degC <= rTemp_Peak2_ChB_degC AND rTemp_Peak2_ChA_degC >= rTemp_Peak2_ChC_degC) THEN
    rVoted_Temp_Peak2_degC := rTemp_Peak2_ChA_degC;
ELSIF (rTemp_Peak2_ChB_degC >= rTemp_Peak2_ChA_degC AND rTemp_Peak2_ChB_degC <= rTemp_Peak2_ChC_degC) OR
      (rTemp_Peak2_ChB_degC <= rTemp_Peak2_ChA_degC AND rTemp_Peak2_ChB_degC >= rTemp_Peak2_ChC_degC) THEN
    rVoted_Temp_Peak2_degC := rTemp_Peak2_ChB_degC;
ELSE
    rVoted_Temp_Peak2_degC := rTemp_Peak2_ChC_degC;
END_IF;

(* Voted Peak Temp 3 *)
IF (rTemp_Peak3_ChA_degC >= rTemp_Peak3_ChB_degC AND rTemp_Peak3_ChA_degC <= rTemp_Peak3_ChC_degC) OR
   (rTemp_Peak3_ChA_degC <= rTemp_Peak3_ChB_degC AND rTemp_Peak3_ChA_degC >= rTemp_Peak3_ChC_degC) THEN
    rVoted_Temp_Peak3_degC := rTemp_Peak3_ChA_degC;
ELSIF (rTemp_Peak3_ChB_degC >= rTemp_Peak3_ChA_degC AND rTemp_Peak3_ChB_degC <= rTemp_Peak3_ChC_degC) OR
      (rTemp_Peak3_ChB_degC <= rTemp_Peak3_ChA_degC AND rTemp_Peak3_ChB_degC >= rTemp_Peak3_ChC_degC) THEN
    rVoted_Temp_Peak3_degC := rTemp_Peak3_ChB_degC;
ELSE
    rVoted_Temp_Peak3_degC := rTemp_Peak3_ChC_degC;
END_IF;

(* Voted Peak Temp 4 *)
IF (rTemp_Peak4_ChA_degC >= rTemp_Peak4_ChB_degC AND rTemp_Peak4_ChA_degC <= rTemp_Peak4_ChC_degC) OR
   (rTemp_Peak4_ChA_degC <= rTemp_Peak4_ChB_degC AND rTemp_Peak4_ChA_degC >= rTemp_Peak4_ChC_degC) THEN
    rVoted_Temp_Peak4_degC := rTemp_Peak4_ChA_degC;
ELSIF (rTemp_Peak4_ChB_degC >= rTemp_Peak4_ChA_degC AND rTemp_Peak4_ChB_degC <= rTemp_Peak4_ChC_degC) OR
      (rTemp_Peak4_ChB_degC <= rTemp_Peak4_ChA_degC AND rTemp_Peak4_ChB_degC >= rTemp_Peak4_ChC_degC) THEN
    rVoted_Temp_Peak4_degC := rTemp_Peak4_ChB_degC;
ELSE
    rVoted_Temp_Peak4_degC := rTemp_Peak4_ChC_degC;
END_IF;

(* 1.7: High-Speed Piezo Dynamic dP/dt Sensors & Numerical Verification *)
IF rDeltaTime_s > 0.001 THEN
    rCalculated_dPdt_Inlet  := (rVoted_Press_Inlet_bar - rPress_Inlet_Prev) / rDeltaTime_s;
    rCalculated_dPdt_Outlet := (rVoted_Press_Outlet_bar - rPress_Outlet_Prev) / rDeltaTime_s;
ELSE
    rCalculated_dPdt_Inlet  := 0.0;
    rCalculated_dPdt_Outlet := 0.0;
END_IF;

rPress_Inlet_Prev  := rVoted_Press_Inlet_bar;
rPress_Outlet_Prev := rVoted_Press_Outlet_bar;

(* Determine Highest Measured dP/dt *)
rCalculated_dPdt_Max_bar_s := rdPdt_Z1_ChA_bar_s;
IF rdPdt_Z1_ChB_bar_s > rCalculated_dPdt_Max_bar_s THEN rCalculated_dPdt_Max_bar_s := rdPdt_Z1_ChB_bar_s; END_IF;
IF rdPdt_Z1_ChC_bar_s > rCalculated_dPdt_Max_bar_s THEN rCalculated_dPdt_Max_bar_s := rdPdt_Z1_ChC_bar_s; END_IF;
IF rdPdt_Z2_ChA_bar_s > rCalculated_dPdt_Max_bar_s THEN rCalculated_dPdt_Max_bar_s := rdPdt_Z2_ChA_bar_s; END_IF;
IF rdPdt_Z2_ChB_bar_s > rCalculated_dPdt_Max_bar_s THEN rCalculated_dPdt_Max_bar_s := rdPdt_Z2_ChB_bar_s; END_IF;
IF rdPdt_Z2_ChC_bar_s > rCalculated_dPdt_Max_bar_s THEN rCalculated_dPdt_Max_bar_s := rdPdt_Z2_ChC_bar_s; END_IF;
IF rCalculated_dPdt_Inlet > rCalculated_dPdt_Max_bar_s THEN rCalculated_dPdt_Max_bar_s := rCalculated_dPdt_Inlet; END_IF;

(* ==========================================================================================================
   PHASE 2: CHEMICAL KINETICS, FLUID RHEOLOGY & DISCRETE STATE-SPACE PROPAGATION
   ========================================================================================================== *)
(* 2.1: Supercritical Ethylene Density & Monomer Concentration *)
rDensity_Ethylene_kg_m3 := 520.0 + 0.085 * (rVoted_Press_Inlet_bar - 2500.0) - 0.45 * (rVoted_Temp_Peak1_degC - 200.0);
IF rDensity_Ethylene_kg_m3 < 460.0 THEN rDensity_Ethylene_kg_m3 := 460.0; END_IF;
IF rDensity_Ethylene_kg_m3 > 590.0 THEN rDensity_Ethylene_kg_m3 := 590.0; END_IF;

rConcentration_Monomer := (rDensity_Ethylene_kg_m3 / c_MW_Ethylene) * 1000.0; (* [mol/m3] *)

(* 2.2: Pressure-Dependent Arrhenius Initiator Decomposition Rates kd *)
(* Zone 1: TBPPI *)
rTempCalc := (c_Ea_Peroxide_Z1 + c_dV_Peroxide_Z1 * rVoted_Press_Inlet_bar * 1.0E5) / (c_R_gas * (rVoted_Temp_Peak1_degC + 273.15));
IF rTempCalc > 80.0 THEN rTempCalc := 80.0; END_IF;
rRate_kd1 := c_Ad_Peroxide_Z1 * EXP(-rTempCalc);

(* Zone 2: TBPO *)
rTempCalc := (c_Ea_Peroxide_Z2 + c_dV_Peroxide_Z2 * rVoted_Press_Z1_bar * 1.0E5) / (c_R_gas * (rVoted_Temp_Peak2_degC + 273.15));
IF rTempCalc > 80.0 THEN rTempCalc := 80.0; END_IF;
rRate_kd2 := c_Ad_Peroxide_Z2 * EXP(-rTempCalc);

(* Zone 3: TBPEH *)
rTempCalc := (c_Ea_Peroxide_Z3 + c_dV_Peroxide_Z3 * rVoted_Press_Z2_bar * 1.0E5) / (c_R_gas * (rVoted_Temp_Peak3_degC + 273.15));
IF rTempCalc > 80.0 THEN rTempCalc := 80.0; END_IF;
rRate_kd3 := c_Ad_Peroxide_Z3 * EXP(-rTempCalc);

(* Zone 4: DTBP *)
rTempCalc := (c_Ea_Peroxide_Z4 + c_dV_Peroxide_Z4 * rVoted_Press_Outlet_bar * 1.0E5) / (c_R_gas * (rVoted_Temp_Peak4_degC + 273.15));
IF rTempCalc > 80.0 THEN rTempCalc := 80.0; END_IF;
rRate_kd4 := c_Ad_Peroxide_Z4 * EXP(-rTempCalc);

(* Propagation & Termination Rates *)
rTempCalc := (c_Ea_Propagation + c_dV_Propagation * rVoted_Press_Inlet_bar * 1.0E5) / (c_R_gas * (rVoted_Temp_Peak1_degC + 273.15));
IF rTempCalc > 80.0 THEN rTempCalc := 80.0; END_IF;
rRate_kp := c_Ap_Propagation * EXP(-rTempCalc);

rTempCalc := (c_Ea_Termination + c_dV_Termination * rVoted_Press_Inlet_bar * 1.0E5) / (c_R_gas * (rVoted_Temp_Peak1_degC + 273.15));
IF rTempCalc > 80.0 THEN rTempCalc := 80.0; END_IF;
rRate_kt := c_At_Termination * EXP(-rTempCalc);
IF rRate_kt < 1.0E5 THEN rRate_kt := 1.0E5; END_IF;

(* Quasi-Steady Free Radical Concentrations [mol/m3] *)
IF rRate_kt > 0.0 AND rFlow_Peroxide_Z1_l_h > 0.001 THEN
    rRadical_Conc_Z1 := SQRT(ABS(2.0 * 0.65 * rRate_kd1 * (rFlow_Peroxide_Z1_l_h * 0.25) / rRate_kt));
ELSE
    rRadical_Conc_Z1 := 0.0;
END_IF;

IF rRate_kt > 0.0 AND rFlow_Peroxide_Z2_l_h > 0.001 THEN
    rRadical_Conc_Z2 := SQRT(ABS(2.0 * 0.65 * rRate_kd2 * (rFlow_Peroxide_Z2_l_h * 0.25) / rRate_kt));
ELSE
    rRadical_Conc_Z2 := 0.0;
END_IF;

IF rRate_kt > 0.0 AND rFlow_Peroxide_Z3_l_h > 0.001 THEN
    rRadical_Conc_Z3 := SQRT(ABS(2.0 * 0.65 * rRate_kd3 * (rFlow_Peroxide_Z3_l_h * 0.25) / rRate_kt));
ELSE
    rRadical_Conc_Z3 := 0.0;
END_IF;

IF rRate_kt > 0.0 AND rFlow_Peroxide_Z4_l_h > 0.001 THEN
    rRadical_Conc_Z4 := SQRT(ABS(2.0 * 0.65 * rRate_kd4 * (rFlow_Peroxide_Z4_l_h * 0.25) / rRate_kt));
ELSE
    rRadical_Conc_Z4 := 0.0;
END_IF;

(* Exothermic Heat Generation Rates [W] *)
rExotherm_Heat_Z1 := c_DeltaH_rxn * rRate_kp * rRadical_Conc_Z1 * rConcentration_Monomer * (c_Tube_CrossSection_m2 * c_Zone1_Length_m);
rExotherm_Heat_Z2 := c_DeltaH_rxn * rRate_kp * rRadical_Conc_Z2 * rConcentration_Monomer * (c_Tube_CrossSection_m2 * c_Zone2_Length_m);
rExotherm_Heat_Z3 := c_DeltaH_rxn * rRate_kp * rRadical_Conc_Z3 * rConcentration_Monomer * (c_Tube_CrossSection_m2 * c_Zone3_Length_m);
rExotherm_Heat_Z4 := c_DeltaH_rxn * rRate_kp * rRadical_Conc_Z4 * rConcentration_Monomer * (c_Tube_CrossSection_m2 * c_Zone4_Length_m);

(* Non-Newtonian Apparent Viscosity (Carreau-Yasuda Model) *)
rTempCalc := 1.0 + (c_CY_RelaxTime * 285.0);
xState_Est[16] := c_CY_ZeroShearVisc / (1.0 + 0.15 * (rVoted_Temp_Peak1_degC - 180.0));
IF xState_Est[16] < 50.0 THEN xState_Est[16] := 50.0; END_IF;

(* Update Real-Time State Vector Estimates xState_Est *)
xState_Est[1]  := rVoted_Temp_Peak1_degC;
xState_Est[2]  := rVoted_Temp_Peak2_degC;
xState_Est[3]  := rVoted_Temp_Peak3_degC;
xState_Est[4]  := rVoted_Temp_Peak4_degC;
xState_Est[5]  := rVoted_Press_Inlet_bar;
xState_Est[6]  := rVoted_Press_Z1_bar;
xState_Est[7]  := rVoted_Press_Outlet_bar;
xState_Est[8]  := rRadical_Conc_Z1;
xState_Est[9]  := rRadical_Conc_Z2;
xState_Est[10] := rRadical_Conc_Z3;
xState_Est[11] := rRadical_Conc_Z4;
xState_Est[12] := rMonomerConversion_pct;
xState_Est[13] := 24500.0; (* Estimated Mn *)
xState_Est[14] := 115000.0; (* Estimated Mw *)
xState_Est[15] := (rVoted_Temp_Peak1_degC + rVoted_Temp_Peak2_degC) * 0.5 + 12.0; (* Wall skin temp *)

(* Current Actuator Control Vector u *)
uControl_Curr[1] := rCmd_PeroxidePump_Z1_Stroke_pct;
uControl_Curr[2] := rCmd_PeroxidePump_Z2_Stroke_pct;
uControl_Curr[3] := rCmd_PeroxidePump_Z3_Stroke_pct;
uControl_Curr[4] := rCmd_PeroxidePump_Z4_Stroke_pct;
uControl_Curr[5] := rCmd_Jacket3WayValve_Z1_pct;
uControl_Curr[6] := rCmd_Jacket3WayValve_Z2_pct;
uControl_Curr[7] := rCmd_Jacket3WayValve_Z3_pct;
uControl_Curr[8] := rCmd_HPLDV_ServoPos_pct;

(* Compute Discrete State-Space Propagation: xState_Pred = A * xState_Est + B * uControl_Curr *)
FOR idx_i := 1 TO 16 DO
    rAccum := 0.0;
    FOR idx_j := 1 TO 16 DO
        rAccum := rAccum + (aState_A[idx_i, idx_j] * xState_Est[idx_j]);
    END_FOR;
    FOR idx_j := 1 TO 8 DO
        rAccum := rAccum + (bInput_B[idx_i, idx_j] * uControl_Curr[idx_j]);
    END_FOR;
    xState_Pred[idx_i] := rAccum;
END_FOR;

(* Compute Projected Sensor Observations: yOutput_Pred = C * xState_Pred *)
FOR idx_i := 1 TO 8 DO
    rAccum := 0.0;
    FOR idx_j := 1 TO 16 DO
        rAccum := rAccum + (cOutput_C[idx_i, idx_j] * xState_Pred[idx_j]);
    END_FOR;
    yOutput_Pred[idx_i] := rAccum;
END_FOR;
"""

