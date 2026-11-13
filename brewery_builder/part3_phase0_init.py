# brewery_builder/part3_phase0_init.py

def get_part3():
    return """(* ============================================================================================== *)
(* PHASE 0: CYBER-PHYSICAL KERNEL INITIALIZATION & STATE-SPACE MATRIX CONFIGURATION               *)
(* ============================================================================================== *)
IF NOT bInitialized OR bReset THEN
    (* Reset Executive Timers and Counters *)
    fMasterBatchTimeSeconds := 0.0;
    udiCycleCounter := 0;
    fCycleDeltaTimeSec := fScanCycleTime;
    IF fCycleDeltaTimeSec < 0.010 THEN
        fCycleDeltaTimeSec := 0.100; (* Enforce Minimum Scan Step Guard [s] *)
    END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* DISCRETE STATE-SPACE SYSTEM MATRIX A (6x6) - Ts = 100 ms                                   *)
    (* States: 1=Lauter DP [mbar], 2=Turbidity [EBC], 3=Runoff [hL/h], 4=Temp [deg C], 5=Evap [%/h], 6=DMS [ppb] *)
    (* ------------------------------------------------------------------------------------------ *)
    (* Row 1: Grain Bed Differential Pressure Dynamics *)
    matA[1, 1] := 0.985000; (* Viscous compaction retention and Darcy pressure dissipation *)
    matA[1, 2] := 0.001200; (* Minor pressure increase due to fines pore blinding *)
    matA[1, 3] := 0.042500; (* Dynamic head loss gradient from runoff flow velocity *)
    matA[1, 4] := -0.000850; (* Viscosity thinning effect at elevated temperature *)
    matA[1, 5] := 0.000000; (* Kettle evaporation decoupled from lauter bed *)
    matA[1, 6] := 0.000000; (* Chemical DMS decoupled from mechanical bed pressure *)

    (* Row 2: Vorlauf Wort Clarity & Turbidity Dynamics *)
    matA[2, 1] := 0.003500; (* Bed channeling turbidity breakthrough under extreme DP *)
    matA[2, 2] := 0.962000; (* Natural particle entrapment decay in grain filter matrix *)
    matA[2, 3] := 0.018000; (* Shearing of husk fines at excessive superficial velocity *)
    matA[2, 4] := -0.001500; (* Enhanced particle agglomeration at optimal sparge temp *)
    matA[2, 5] := 0.000000; (* Kettle evaporation decoupled from Vorlauf clarity *)
    matA[2, 6] := 0.000000; (* DMS decoupled from optical turbidity *)

    (* Row 3: Lauter Runoff Volumetric Flow Rate Dynamics *)
    matA[3, 1] := -0.085000; (* Flow retardation due to bed hydraulic compaction resistance *)
    matA[3, 2] := -0.002000; (* Flow resistance increase from suspended micro-fines *)
    matA[3, 3] := 0.945000; (* Fluid momentum conservation in runoff piping manifold *)
    matA[3, 4] := 0.004200; (* Darcy permeability increase from reduced wort dynamic viscosity *)
    matA[3, 5] := 0.000000; (* Kettle evaporation decoupled from lauter outflow *)
    matA[3, 6] := 0.000000; (* DMS decoupled from fluid flow momentum *)

    (* Row 4: Wort Kettle Calandria Boiling Temperature Dynamics *)
    matA[4, 1] := 0.000000; (* Lauter DP decoupled from kettle thermodynamics *)
    matA[4, 2] := 0.000000; (* Wort turbidity decoupled from kettle thermal mass *)
    matA[4, 3] := -0.012500; (* Thermal dilution from incoming cooler first wort / sparge *)
    matA[4, 4] := 0.991000; (* Lumped thermal capacitance heat retention of 600 hL wort *)
    matA[4, 5] := -0.038000; (* Latent heat enthalpy loss due to vapor boil-off *)
    matA[4, 6] := 0.000000; (* DMS trace mass decoupled from thermal bulk energy *)

    (* Row 5: Wort Kettle Continuous Evaporation Rate Dynamics *)
    matA[5, 1] := 0.000000; (* Lauter DP decoupled from kettle evaporation *)
    matA[5, 2] := 0.000000; (* Wort turbidity decoupled from vapor flash kinetics *)
    matA[5, 3] := -0.005500; (* Evaporation rate depression during cold wort influx *)
    matA[5, 4] := 0.065000; (* Vapor pressure driving force above saturation temperature *)
    matA[5, 5] := 0.925000; (* Evaporative boiling thermal equilibrium stabilization *)
    matA[5, 6] := 0.000000; (* Trace DMS concentration decoupled from vapor mass flux *)

    (* Row 6: Volatile Dimethyl Sulfide (DMS) Residual Concentration Dynamics *)
    matA[6, 1] := 0.000000; (* Lauter DP decoupled from DMS chemical degradation *)
    matA[6, 2] := 0.000000; (* Wort turbidity decoupled from DMS volatile desorption *)
    matA[6, 3] := 0.025000; (* Incoming SMM precursor mass addition from unboiled runoff *)
    matA[6, 4] := 0.085000; (* Thermal cleavage rate of SMM to DMS at boiling temp *)
    matA[6, 5] := -0.145000; (* Vapor-liquid stripping efficiency as function of boil rate *)
    matA[6, 6] := 0.938000; (* Logarithmic decay of residual volatile sulfur compounds *)

    (* ------------------------------------------------------------------------------------------ *)
    (* DISCRETE CONTROL INPUT COUPLING MATRIX B (6x5) - Ts = 100 ms                                *)
    (* Controls: 1=Rake Height [mm], 2=Rake Speed [RPM], 3=Runoff Valve [%], 4=Steam [bar], 5=Recirc [%] *)
    (* ------------------------------------------------------------------------------------------ *)
    (* Row 1: Lauter Bed DP *)
    matB[1, 1] := -0.048000; (* Rake elevation: lowering cuts deep, relieving bottom bed DP *)
    matB[1, 2] := -0.125000; (* Rake rotation: knives loosen packed malt bed compaction *)
    matB[1, 3] := 0.082000;  (* Opening runoff valve increases suction, compacting bed *)
    matB[1, 4] := 0.000000;  (* Calandria steam has zero coupling to lauter bed *)
    matB[1, 5] := -0.015000; (* Vorlauf recirculation relieves suction vacuum on bed *)

    (* Row 2: Vorlauf Clarity / Turbidity *)
    matB[2, 1] := 0.035000;  (* Disturbance of bed by low rakes temporarily raises turbidity *)
    matB[2, 2] := 0.062000;  (* Fast rake rotation agitates sediment, increasing turbidity *)
    matB[2, 3] := 0.045000;  (* Rapid valve opening pulls fines through false bottom slots *)
    matB[2, 4] := 0.000000;  (* Calandria steam has zero coupling to lauter clarity *)
    matB[2, 5] := -0.085000; (* Vorlauf recirculation filters wort through grain cake *)

    (* Row 3: Lauter Runoff Flow Rate *)
    matB[3, 1] := 0.028000;  (* Rake cutting restores Darcy permeability, boosting flow *)
    matB[3, 2] := 0.045000;  (* Rake rotation clears blinded false bottom screen slots *)
    matB[3, 3] := 0.285000;  (* Direct throttling of runoff control valve *)
    matB[3, 4] := 0.000000;  (* Calandria steam decoupled from lauter runoff hydraulics *)
    matB[3, 5] := -0.220000; (* Diverting to recirculation reduces forward kettle runoff *)

    (* Row 4: Wort Kettle Calandria Temperature *)
    matB[4, 1] := 0.000000;  (* Rake mechanics decoupled from kettle heat transfer *)
    matB[4, 2] := 0.000000;  (* Rake speed decoupled from kettle heat transfer *)
    matB[4, 3] := -0.018000; (* Incoming cooler wort throttles kettle thermal ramp *)
    matB[4, 4] := 0.350000;  (* Calandria steam pressure increases condensing delta-T *)
    matB[4, 5] := 0.000000;  (* Recirculation valve decoupled from kettle temperature *)

    (* Row 5: Wort Kettle Evaporation Rate *)
    matB[5, 1] := 0.000000;  (* Rake decoupled from boiling evaporation *)
    matB[5, 2] := 0.000000;  (* Rake decoupled from boiling evaporation *)
    matB[5, 3] := -0.008000; (* Cold inflow reduces boiling intensity *)
    matB[5, 4] := 0.420000;  (* Calandria steam supply directly drives flash evaporation *)
    matB[5, 5] := 0.000000;  (* Vorlauf recirc decoupled from boiling evaporation *)

    (* Row 6: Volatile DMS Residual Concentration *)
    matB[6, 1] := 0.000000;  (* Rake decoupled from DMS chemistry *)
    matB[6, 2] := 0.000000;  (* Rake decoupled from DMS chemistry *)
    matB[6, 3] := 0.035000;  (* Fresh unboiled wort inflow introduces unstripped precursor *)
    matB[6, 4] := -0.210000; (* Steam boiling rate enhances DMS vapor stripping stripping *)
    matB[6, 5] := 0.000000;  (* Vorlauf recirc decoupled from DMS stripping *)

    (* ------------------------------------------------------------------------------------------ *)
    (* DISCRETE MEASUREMENT OUTPUT MATRIX C (6x6)                                                 *)
    (* Direct state observation through voted physical sensors                                    *)
    (* ------------------------------------------------------------------------------------------ *)
    FOR idxRow := 1 TO 6 DO
        FOR idxCol := 1 TO 6 DO
            IF idxRow = idxCol THEN
                matC[idxRow, idxCol] := 1.000000; (* Direct unity measurement scaling *)
            ELSE
                matC[idxRow, idxCol] := 0.000000;
            END_IF;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------ *)
    (* DISCRETE DIRECT FEEDTHROUGH MATRIX D (6x5)                                                 *)
    (* Zero direct feedthrough in strictly proper thermodynamic/hydraulic plants                  *)
    (* ------------------------------------------------------------------------------------------ *)
    FOR idxRow := 1 TO 6 DO
        FOR idxCol := 1 TO 5 DO
            matD[idxRow, idxCol] := 0.000000;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------ *)
    (* LUENBERGER OBSERVER INNOVATION GAIN MATRIX L (6x6)                                         *)
    (* Synthesized via discrete Kalman filter algebraic Riccati equation                         *)
    (* ------------------------------------------------------------------------------------------ *)
    matL[1, 1] := 0.285000; matL[1, 2] := 0.000500; matL[1, 3] := 0.015000; matL[1, 4] := 0.000000; matL[1, 5] := 0.000000; matL[1, 6] := 0.000000;
    matL[2, 1] := 0.001200; matL[2, 2] := 0.320000; matL[2, 3] := 0.008000; matL[2, 4] := 0.000000; matL[2, 5] := 0.000000; matL[2, 6] := 0.000000;
    matL[3, 1] := -0.02500; matL[3, 2] := 0.002000; matL[3, 3] := 0.310000; matL[3, 4] := 0.001500; matL[3, 5] := 0.000000; matL[3, 6] := 0.000000;
    matL[4, 1] := 0.000000; matL[4, 2] := 0.000000; matL[4, 3] := -0.00400; matL[4, 4] := 0.295000; matL[4, 5] := 0.012000; matL[4, 6] := 0.000000;
    matL[5, 1] := 0.000000; matL[5, 2] := 0.000000; matL[5, 3] := -0.00200; matL[5, 4] := 0.018000; matL[5, 5] := 0.265000; matL[5, 6] := 0.000000;
    matL[6, 1] := 0.000000; matL[6, 2] := 0.000000; matL[6, 3] := 0.005000; matL[6, 4] := 0.022000; matL[6, 5] := -0.03500; matL[6, 6] := 0.340000;

    (* ------------------------------------------------------------------------------------------ *)
    (* MPC QUADRATIC COST WEIGHTING MATRICES (Q, R, R_slew, P)                                    *)
    (* ------------------------------------------------------------------------------------------ *)
    (* Diagonal State Penalty Q: Prioritizing Lauter DP avoidance and DMS stripping *)
    diagQ_StateCost[1] := 8.500;  (* High penalty on grain bed differential pressure [mbar] *)
    diagQ_StateCost[2] := 4.200;  (* Penalty on wort turbidity / suspended particulates [EBC] *)
    diagQ_StateCost[3] := 3.800;  (* Penalty on runoff volumetric throughput deviation [hL/h] *)
    diagQ_StateCost[4] := 6.000;  (* Strict tracking of boiling temperature profile [deg C] *)
    diagQ_StateCost[5] := 7.500;  (* Rigorous penalty on continuous evaporation rate [%/h] *)
    diagQ_StateCost[6] := 9.000;  (* Heavy penalty on lingering residual DMS concentration [ppb] *)

    (* Diagonal Control Effort Penalty R *)
    diagR_ControlCost[1] := 0.120; (* Rake hydraulic vertical elevation movement penalty *)
    diagR_ControlCost[2] := 0.250; (* Rake rotational speed wear and power penalty *)
    diagR_ControlCost[3] := 0.180; (* Lauter runoff control valve throttling penalty *)
    diagR_ControlCost[4] := 0.450; (* Calandria high-pressure steam consumption penalty *)
    diagR_ControlCost[5] := 0.150; (* Vorlauf recirculation diverter movement penalty *)

    (* Diagonal Control Slew Rate Penalty R_slew (Prevents Actuator Hunting & Water Hammer) *)
    diagR_SlewCost[1] := 1.500;   (* Damp rake vertical hunting *)
    diagR_SlewCost[2] := 2.800;   (* Damp rake VFD mechanical shock *)
    diagR_SlewCost[3] := 3.200;   (* Prevent hydraulic water hammer in runoff headers *)
    diagR_SlewCost[4] := 4.500;   (* Thermal stress dampening on calandria tube sheets *)
    diagR_SlewCost[5] := 2.000;   (* Prevent surge during Vorlauf-to-Kettle switchover *)

    (* Diagonal Terminal State Penalty Matrix P (Lyapunov Stability Terminal Weight) *)
    diagP_TerminalCost[1] := 18.500;
    diagP_TerminalCost[2] := 9.800;
    diagP_TerminalCost[3] := 8.400;
    diagP_TerminalCost[4] := 14.200;
    diagP_TerminalCost[5] := 16.500;
    diagP_TerminalCost[6] := 22.000;

    (* ------------------------------------------------------------------------------------------ *)
    (* ACTUATOR HARD BOX CONSTRAINTS & MAXIMUM SLEW LIMITS                                        *)
    (* ------------------------------------------------------------------------------------------ *)
    (* Control 1: Wort Rake Height [mm] - False bottom clearance safety limit >= 15 mm *)
    vecU_MinBox[1] := 15.0;
    vecU_MaxBox[1] := 420.0;
    vecU_SlewLimit[1] := 6.0;   (* Maximum 6.0 mm per scan cycle *)

    (* Control 2: Wort Rake Rotational Speed [RPM] *)
    vecU_MinBox[2] := 0.0;
    vecU_MaxBox[2] := 4.8;
    vecU_SlewLimit[2] := 0.25;  (* Maximum 0.25 RPM per scan cycle *)

    (* Control 3: Lauter Runoff Valve Position [%] *)
    vecU_MinBox[3] := 0.0;
    vecU_MaxBox[3] := 100.0;
    vecU_SlewLimit[3] := 2.5;   (* Maximum 2.5% stroke per scan cycle *)

    (* Control 4: Calandria Steam Supply Pressure [bar] *)
    vecU_MinBox[4] := 0.0;
    vecU_MaxBox[4] := 4.2;
    vecU_SlewLimit[4] := 0.15;  (* Maximum 0.15 bar per scan cycle *)

    (* Control 5: Vorlauf Recirculation Valve Position [%] *)
    vecU_MinBox[5] := 0.0;
    vecU_MaxBox[5] := 100.0;
    vecU_SlewLimit[5] := 5.0;   (* Maximum 5.0% stroke per scan cycle *)

    (* Initialize Initial Estimated State Vector *)
    vecX_hat[1] := 8.5;         (* Initial DP [mbar] *)
    vecX_hat[2] := 85.0;        (* Initial Turbidity [EBC] *)
    vecX_hat[3] := 0.0;         (* Initial Flow [hL/h] *)
    vecX_hat[4] := 20.0;        (* Initial Kettle Temp [deg C] *)
    vecX_hat[5] := 0.0;         (* Initial Evaporation Rate [%/h] *)
    vecX_hat[6] := 125.0;       (* Initial DMS concentration [ppb] *)

    FOR idxRow := 1 TO 6 DO
        vecX_hat_prev[idxRow] := vecX_hat[idxRow];
        vecX_hat_next[idxRow] := vecX_hat[idxRow];
        vecY_meas[idxRow] := vecX_hat[idxRow];
        vecY_est[idxRow] := vecX_hat[idxRow];
        vecY_innov[idxRow] := 0.0;
        vecX_Setpoint[idxRow] := vecX_hat[idxRow];
    END_FOR;

    FOR idxInput := 1 TO 5 DO
        vecU_active[idxInput] := vecU_MinBox[idxInput];
        vecU_active_prev[idxInput] := vecU_MinBox[idxInput];
        vecU_Target[idxInput] := vecU_MinBox[idxInput];
    END_FOR;

    (* Initialize Trajectory Prediction Rollout Arrays *)
    FOR idxHorizon := 0 TO 5 DO
        FOR idxRow := 1 TO 6 DO
            arrX_Trajectory[idxHorizon, idxRow] := vecX_hat[idxRow];
            arrLambda_Costate[idxHorizon, idxRow] := 0.0;
        END_FOR;
    END_FOR;

    FOR idxHorizon := 0 TO 4 DO
        FOR idxInput := 1 TO 5 DO
            arrU_Trajectory[idxHorizon, idxInput] := vecU_MinBox[idxInput];
            arrU_Trajectory_Best[idxHorizon, idxInput] := vecU_MinBox[idxInput];
            arrGrad_J[idxHorizon, idxInput] := 0.0;
        END_FOR;
    END_FOR;

    (* Mark Initialization Complete *)
    bInitialized := TRUE;
    bWarmRestart := FALSE;
    bReady := TRUE;
    bError := FALSE;
END_IF;
"""
