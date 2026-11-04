# scripts/feedmill_builder/part3_phase0_init.py
# -*- coding: utf-8 -*-

def get_phase0_block():
    return """(* ====================================================================================================
   PHASE 0: MODEL MATRICES, CONTROL COEFFICIENTS & COLD-START NUMERICAL EMBEDDING
   ==================================================================================================== *)
IF NOT bModelInitialized THEN
    (* ------------------------------------------------------------------------------------------------
       A-MATRIX (8x8): DISCRETE PLANT DYNAMICS (Sampling Period Ts = 50 ms = 0.050 s)
       States:
         x1: Conditioned Mash Exit Temperature T_mash [deg C]
         x2: Conditioned Mash Exit Moisture w_mash [% w/w]
         x3: Starch Gelatinization Extent Index alpha_gel [0.0..1.0]
         x4: Pellet Mill 400 kW Main Drive Current I_mill [A]
         x5: Ring Die Surface Pyrometer Temperature T_die [deg C]
         x6: Dynamic Roller Hydraulic Extrusion Gap g_roller [mm]
         x7: Counterflow Cooler Pellet Bed Depth h_bed [mm]
         x8: Cooled Pellet Discharge Equilibrium Moisture w_pellet [% w/w]
       ------------------------------------------------------------------------------------------------ *)
    (* Row 1: Mash Temperature Dynamics d(T_mash)/dt *)
    A_mat[1,1] := 0.982500;  (* Thermal inertia decay: tau_th = 2.85 s *)
    A_mat[1,2] := 0.004200;  (* Moisture latent heat buffering *)
    A_mat[1,3] := 0.000000;  (* Gelatinization enthalpy coupling (negligible endothermic heat) *)
    A_mat[1,4] := 0.000000;  (* No upstream feedback from mill current *)
    A_mat[1,5] := 0.000000;  (* Upstream decoupled from die temp *)
    A_mat[1,6] := 0.000000;  (* Decoupled from roller gap *)
    A_mat[1,7] := 0.000000;  (* Decoupled from cooler bed *)
    A_mat[1,8] := 0.000000;  (* Decoupled from final pellet moisture *)

    (* Row 2: Mash Moisture Dynamics d(w_mash)/dt *)
    A_mat[2,1] := 0.000150;  (* Vaporization equilibrium shift with temperature *)
    A_mat[2,2] := 0.978000;  (* Moisture holdup retention dynamics: tau_w = 2.25 s *)
    A_mat[2,3] :=-0.000850;  (* Bound water uptake consumed in starch crystal hydration *)
    A_mat[2,4] := 0.000000;  (* Upstream decoupled from mill current *)
    A_mat[2,5] := 0.000000;  (* Upstream decoupled from die temp *)
    A_mat[2,6] := 0.000000;  (* Decoupled from roller gap *)
    A_mat[2,7] := 0.000000;  (* Decoupled from cooler bed *)
    A_mat[2,8] := 0.000000;  (* Decoupled from cooler moisture *)

    (* Row 3: Starch Gelatinization Extent d(alpha_gel)/dt *)
    A_mat[3,1] := 0.001850;  (* Arrhenius thermal reaction rate acceleration *)
    A_mat[3,2] := 0.004200;  (* Hydrothermal plasticization moisture sensitivity *)
    A_mat[3,3] := 0.994000;  (* Irreversible crystal lamellae melting accumulation *)
    A_mat[3,4] := 0.000000;  (* Decoupled upstream *)
    A_mat[3,5] := 0.000000;  (* Decoupled upstream *)
    A_mat[3,6] := 0.000000;  (* Decoupled upstream *)
    A_mat[3,7] := 0.000000;  (* Decoupled upstream *)
    A_mat[3,8] := 0.000000;  (* Decoupled upstream *)

    (* Row 4: Pellet Mill 400 kW Motor Current d(I_mill)/dt *)
    A_mat[4,1] :=-0.850000;  (* Mash temperature softening: hotter mash reduces extrusion viscosity [A/deg C] *)
    A_mat[4,2] :=-1.420000;  (* Mash moisture lubrication: higher water content lowers extrusion friction [A/%] *)
    A_mat[4,3] :=-35.50000;  (* Gelatinized starch acts as natural binder, drastically reducing extrusion torque [A/unit] *)
    A_mat[4,4] := 0.915000;  (* Motor electromagnetic torque and rotational inertia lag: tau_em = 0.55 s *)
    A_mat[4,5] := 0.220000;  (* Die hole wall friction thermal drag increase [A/deg C] *)
    A_mat[4,6] :=-45.80000;  (* Roller gap sensitivity: tighter gap increases mash compaction resistance [A/mm] *)
    A_mat[4,7] := 0.000000;  (* Downstream decoupled from cooler bed *)
    A_mat[4,8] := 0.000000;  (* Downstream decoupled from cooler moisture *)

    (* Row 5: Ring Die Surface Temperature d(T_die)/dt *)
    A_mat[5,1] := 0.035000;  (* Incoming conditioned mash convective heat transfer *)
    A_mat[5,2] :=-0.015000;  (* Moisture evaporative heat loss on die surface *)
    A_mat[5,3] :=-0.080000;  (* Better lubricated starch reduces frictional heat dissipation *)
    A_mat[5,4] := 0.012500;  (* Mechanical friction conversion of electrical motor power to thermal heat *)
    A_mat[5,5] := 0.988000;  (* Heavy steel die thermal mass retention: tau_die = 4.15 s *)
    A_mat[5,6] :=-0.055000;  (* Roller pinch mechanical shearing heat generation *)
    A_mat[5,7] := 0.000000;  (* Downstream decoupled *)
    A_mat[5,8] := 0.000000;  (* Downstream decoupled *)

    (* Row 6: Twin Roller Hydraulic Extrusion Gap d(g_roller)/dt *)
    A_mat[6,1] := 0.000000;  (* No direct fluidic coupling *)
    A_mat[6,2] := 0.000000;  (* No direct fluidic coupling *)
    A_mat[6,3] := 0.000000;  (* No direct fluidic coupling *)
    A_mat[6,4] := 0.000120;  (* High mash compaction back-pressure forces hydraulic ram back *)
    A_mat[6,5] :=-0.000350;  (* Die thermal expansion narrows effective clearance *)
    A_mat[6,6] := 0.945000;  (* Electro-hydraulic proportional valve position loop response *)
    A_mat[6,7] := 0.000000;  (* Downstream decoupled *)
    A_mat[6,8] := 0.000000;  (* Downstream decoupled *)

    (* Row 7: Counterflow Cooler Pellet Bed Depth d(h_bed)/dt *)
    A_mat[7,1] := 0.000000;  (* Temperature independent *)
    A_mat[7,2] := 0.000000;  (* Moisture independent *)
    A_mat[7,3] := 0.000000;  (* Gelatinization independent *)
    A_mat[7,4] := 0.085000;  (* Higher mill motor power correlates with pellet volumetric output into cooler *)
    A_mat[7,5] := 0.000000;  (* Die temp independent *)
    A_mat[7,6] := 0.000000;  (* Roller gap independent *)
    A_mat[7,7] := 0.996500;  (* Cooler volumetric mass accumulation retention *)
    A_mat[7,8] := 0.000000;  (* Decoupled from moisture *)

    (* Row 8: Cooled Pellet Discharge Equilibrium Moisture d(w_pellet)/dt *)
    A_mat[8,1] := 0.002500;  (* Hotter pellets possess higher vapor pressure, accelerating drying *)
    A_mat[8,2] := 0.045000;  (* Incoming pellet moisture directly drives core moisture *)
    A_mat[8,3] :=-0.012000;  (* Strongly gelatinized pellets retain hygroscopic bound water *)
    A_mat[8,4] := 0.000000;  (* Mill current decoupled *)
    A_mat[8,5] := 0.000000;  (* Die temp decoupled *)
    A_mat[8,6] := 0.000000;  (* Roller gap decoupled *)
    A_mat[8,7] :=-0.000180;  (* Higher bed depth increases retention time, yielding deeper moisture removal *)
    A_mat[8,8] := 0.975000;  (* Core pellet diffusion mass transfer lag *)

    (* ------------------------------------------------------------------------------------------------
       B-MATRIX (8x6): CONTROL ACTUATOR COUPLING MATRIX (Ts = 50 ms)
       Actuators:
         u1: Feeder Screw Speed Command N_feeder [RPM] (0..180 RPM -> 0..30 t/h)
         u2: Saturated Steam Modulating Globe Valve Position Y_steam [%] (0..100%)
         u3: Conditioner Dual-Shaft Agitator Speed N_shaft [RPM] (150..450 RPM)
         u4: Dynamic Hydraulic Roller Gap Servo Position Y_gap_hyd [%] (0..100%)
         u5: Counterflow Cooler Reciprocating Discharge Grid Speed Y_grid [%] (0..100%)
         u6: Cooler Centrifugal Exhaust Fan VFD Speed N_fan [%] (30..100%)
       ------------------------------------------------------------------------------------------------ *)
    (* Row 1: Mash Temp *)
    B_mat[1,1] :=-0.025000;  (* Higher throughput cold meal reduces conditioner temperature *)
    B_mat[1,2] := 0.075000;  (* Steam injection directly heats mash via latent heat condensation [deg C/%] *)
    B_mat[1,3] := 0.004500;  (* Mechanical paddle shear dissipation converts to thermal energy *)
    B_mat[1,4] := 0.000000;  (* Decoupled *)
    B_mat[1,5] := 0.000000;  (* Decoupled *)
    B_mat[1,6] := 0.000000;  (* Decoupled *)

    (* Row 2: Mash Moisture *)
    B_mat[2,1] :=-0.008000;  (* Cold meal mass dilution reduces steam condensation fraction *)
    B_mat[2,2] := 0.032000;  (* Direct culinary steam condensation adds moisture [%/% valve] *)
    B_mat[2,3] :=-0.000500;  (* Higher shaft speed vents slight flash vapor *)
    B_mat[2,4] := 0.000000;  (* Decoupled *)
    B_mat[2,5] := 0.000000;  (* Decoupled *)
    B_mat[2,6] := 0.000000;  (* Decoupled *)

    (* Row 3: Starch Gelatinization Extent *)
    B_mat[3,1] :=-0.000450;  (* Shorter residence time at higher feed rate reduces reaction extent *)
    B_mat[3,2] := 0.001250;  (* Steam enthalpy accelerates Arrhenius reaction *)
    B_mat[3,3] := 0.000650;  (* Intense hydrodynamic paddle shear shatters starch granules *)
    B_mat[3,4] := 0.000000;  (* Decoupled *)
    B_mat[3,5] := 0.000000;  (* Decoupled *)
    B_mat[3,6] := 0.000000;  (* Decoupled *)

    (* Row 4: Pellet Mill 400 kW Motor Current *)
    B_mat[4,1] := 1.850000;  (* Feed mass flow rate directly increases die extrusion resistance [A/RPM] *)
    B_mat[4,2] :=-0.650000;  (* Steam softening reduces extrusion torque load *)
    B_mat[4,3] :=-0.085000;  (* Better pre-conditioning lowers die compaction friction *)
    B_mat[4,4] :=-1.250000;  (* Opening hydraulic gap relieves extrusion compaction pressure [A/% servo] *)
    B_mat[4,5] := 0.000000;  (* Decoupled *)
    B_mat[4,6] := 0.000000;  (* Decoupled *)

    (* Row 5: Ring Die Surface Temperature *)
    B_mat[5,1] := 0.045000;  (* Higher throughput pushes more warm mash into die face *)
    B_mat[5,2] := 0.015000;  (* Steam thermal transfer *)
    B_mat[5,3] := 0.000000;  (* Decoupled *)
    B_mat[5,4] :=-0.035000;  (* Wider roller gap reduces metal-to-mash friction heating *)
    B_mat[5,5] := 0.000000;  (* Decoupled *)
    B_mat[5,6] := 0.000000;  (* Decoupled *)

    (* Row 6: Twin Roller Hydraulic Gap *)
    B_mat[6,1] :=-0.000250;  (* Heavy feed rate forces rollers slightly against hydraulics *)
    B_mat[6,2] := 0.000000;  (* Decoupled *)
    B_mat[6,3] := 0.000000;  (* Decoupled *)
    B_mat[6,4] := 0.022500;  (* Hydraulic servo proportional positioning gain [mm/% servo] *)
    B_mat[6,5] := 0.000000;  (* Decoupled *)
    B_mat[6,6] := 0.000000;  (* Decoupled *)

    (* Row 7: Counterflow Cooler Bed Depth *)
    B_mat[7,1] := 0.125000;  (* Feeder screw mass flow feeds hot pellets directly into cooler bed [mm/RPM] *)
    B_mat[7,2] := 0.000000;  (* Decoupled *)
    B_mat[7,3] := 0.000000;  (* Decoupled *)
    B_mat[7,4] := 0.000000;  (* Decoupled *)
    B_mat[7,5] :=-0.345000;  (* Cooler discharge grid reciprocating speed evacuates pellets [mm/% grid] *)
    B_mat[7,6] := 0.000000;  (* Fan speed does not affect volumetric depth directly *)

    (* Row 8: Cooled Pellet Discharge Equilibrium Moisture *)
    B_mat[8,1] := 0.004500;  (* Higher feed rate shortens cooler retention time, raising exit moisture *)
    B_mat[8,2] := 0.008500;  (* Higher steam conditioning requires greater evaporative duty *)
    B_mat[8,3] := 0.000000;  (* Decoupled *)
    B_mat[8,4] := 0.000000;  (* Decoupled *)
    B_mat[8,5] := 0.003500;  (* Faster discharge grid reduces drying residence time *)
    B_mat[8,6] :=-0.016500;  (* Cooler exhaust fan increases counterflow air velocity and moisture pickup *)

    (* ------------------------------------------------------------------------------------------------
       E-MATRIX (8x3): DISTURBANCE COUPLING MATRIX (Ts = 50 ms)
       Disturbances:
         d1: Incoming Raw Meal Ambient Temperature T_inlet [deg C] (5..35 deg C)
         d2: Incoming Raw Meal Moisture Content w_inlet [% w/w] (10.5..13.5%)
         d3: Saturated Steam Supply Header Pressure P_steam_hdr [bar] (2.2..2.8 bar)
       ------------------------------------------------------------------------------------------------ *)
    E_mat[1,1] := 0.017500;  (* Ambient grain meal temperature enters conditioner directly *)
    E_mat[1,2] := 0.000000;
    E_mat[1,3] := 0.042000;  (* Steam supply pressure fluctuation alters nozzle mass injection *)

    E_mat[2,1] := 0.000000;
    E_mat[2,2] := 0.022000;  (* Inlet moisture directly shifts conditioned mash moisture content *)
    E_mat[2,3] := 0.018500;  (* Steam pressure shifts injected steam flow rate *)

    E_mat[3,1] := 0.000350;  (* Warmer raw meal slightly promotes gelatinization onset *)
    E_mat[3,2] := 0.000850;  (* Higher natural grain moisture plasticizes starch *)
    E_mat[3,3] := 0.000450;  (* Steam header pressure stability *)

    E_mat[4,1] :=-0.150000;  (* Cold grain enters harder, slightly raising mill current *)
    E_mat[4,2] :=-0.850000;  (* Dry inlet grain meal causes severe die friction surges *)
    E_mat[4,3] :=-0.250000;  (* Steam pressure drop causes sudden mash drying and motor torque spikes *)

    E_mat[5,1] := 0.005000;
    E_mat[5,2] :=-0.012000;
    E_mat[5,3] := 0.008000;

    E_mat[6,1] := 0.000000;
    E_mat[6,2] := 0.000000;
    E_mat[6,3] := 0.000000;

    E_mat[7,1] := 0.000000;
    E_mat[7,2] := 0.000000;
    E_mat[7,3] := 0.000000;

    E_mat[8,1] := 0.001500;
    E_mat[8,2] := 0.015000;  (* Raw meal moisture variation carries forward into cooled pellet moisture *)
    E_mat[8,3] := 0.002000;

    (* ------------------------------------------------------------------------------------------------
       C-MATRIX (8x8) & D-MATRIX (8x6): OUTPUT & DIRECT FEEDTHROUGH
       Direct state observation (C = Identity) and zero direct algebraic feedthrough (D = Zero)
       ------------------------------------------------------------------------------------------------ *)
    FOR i := 1 TO 8 DO
        FOR j := 1 TO 8 DO
            IF i = j THEN
                C_mat[i,j] := 1.0;
            ELSE
                C_mat[i,j] := 0.0;
            END_IF;
        END_FOR;
        FOR m := 1 TO 6 DO
            D_mat[i,m] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------
       MPC QUADRATIC COST WEIGHTING VECTORS (Q, R, P_term)
       Penalizing starch gelatinization error, motor overcurrent spikes, and actuator wear
       ------------------------------------------------------------------------------------------------ *)
    (* State Tracking Error Penalties Q *)
    Q_diag[1] := 4.50;      (* Conditioner Mash Temperature Tracking Weight *)
    Q_diag[2] := 8.00;      (* Conditioned Mash Moisture Tracking Weight *)
    Q_diag[3] := 25.00;     (* Starch Gelatinization Extent Weight (Crucial for PDI & Sanitation) *)
    Q_diag[4] := 18.00;     (* Pellet Mill 400 kW Motor Amperage Balance Weight *)
    Q_diag[5] := 2.00;      (* Ring Die Face Temperature Moderation Weight *)
    Q_diag[6] := 12.00;     (* Dynamic Hydraulic Roller Gap Regulation Weight *)
    Q_diag[7] := 5.00;      (* Counterflow Cooler Bed Level Tracking Weight *)
    Q_diag[8] := 15.00;     (* Final Pellet Storage Equilibrium Moisture Weight *)

    (* Actuator Rate-of-Change Slew Penalties R *)
    R_diag[1] := 3.00;      (* Feeder Screw Slew Rate Penalty (Damps throughput surges) *)
    R_diag[2] := 6.00;      (* Saturated Steam Modulating Valve Throttle Wear Penalty *)
    R_diag[3] := 1.50;      (* Conditioner Agitator VFD Slew Penalty *)
    R_diag[4] := 8.00;      (* Dynamic Hydraulic Gap Servo Valve Wear Penalty (Prevents hunting) *)
    R_diag[5] := 2.50;      (* Cooler Discharge Grid Frequency Slew Penalty *)
    R_diag[6] := 2.00;      (* Cooler Exhaust Fan VFD Slew Penalty *)

    (* Terminal State Horizon Weights P_term (Aggressive Terminal Cost on Np = 3) *)
    P_diag[1] := 9.00;
    P_diag[2] := 16.00;
    P_diag[3] := 50.00;     (* High terminal focus on achieving targeted gelatinization index *)
    P_diag[4] := 75.00;     (* Critical penalty on terminal motor current to prevent die plugging *)
    P_diag[5] := 4.00;
    P_diag[6] := 24.00;
    P_diag[7] := 10.00;
    P_diag[8] := 30.00;

    (* ------------------------------------------------------------------------------------------------
       ACTUATOR PHYSICAL SATURATION BOUNDS & MAXIMUM SLEW RATES
       ------------------------------------------------------------------------------------------------ *)
    (* u1: Feeder Screw Speed [RPM] *)
    u_min[1]  := 0.0;       u_max[1]  := 180.0;     du_max[1] := 2.50;  (* Max 2.5 RPM/scan *)
    (* u2: Steam Modulating Valve [%] *)
    u_min[2]  := 0.0;       u_max[2]  := 100.0;     du_max[2] := 1.80;  (* Max 1.8 %/scan *)
    (* u3: Conditioner Shaft Agitator Speed [RPM] *)
    u_min[3]  := 150.0;     u_max[3]  := 450.0;     du_max[3] := 5.00;  (* Max 5.0 RPM/scan *)
    (* u4: Dynamic Hydraulic Gap Servo Position [%] *)
    u_min[4]  := 0.0;       u_max[4]  := 100.0;     du_max[4] := 1.20;  (* Max 1.2 %/scan *)
    (* u5: Cooler Discharge Grid Speed [%] *)
    u_min[5]  := 0.0;       u_max[5]  := 100.0;     du_max[5] := 2.00;  (* Max 2.0 %/scan *)
    (* u6: Cooler Exhaust Fan Speed [%] *)
    u_min[6]  := 30.0;      u_max[6]  := 100.0;     du_max[6] := 1.50;  (* Max 1.5 %/scan *)

    (* Initialize State Vector to Cold Standby Ambient Equilibrium *)
    x_state[1] := 22.0;     (* Ambient Mash Temp: 22 deg C *)
    x_state[2] := 12.0;     (* Ambient Mash Moisture: 12.0% *)
    x_state[3] := 0.05;     (* Raw Starch Gelatinization: 5% *)
    x_state[4] := 0.0;      (* Motor Current Idle: 0 A *)
    x_state[5] := 25.0;     (* Die Surface Temp: 25 deg C *)
    x_state[6] := 2.00;     (* Retracted Standby Roller Gap: 2.00 mm *)
    x_state[7] := 0.0;      (* Empty Cooler Bed: 0 mm *)
    x_state[8] := 12.0;     (* Pellet Moisture: 12.0% *)

    FOR i := 1 TO 8 DO
        x_prev[i]   := x_state[i];
        x_next[i]   := x_state[i];
        x_target[i] := x_state[i];
        x_error[i]  := 0.0;
    END_FOR;

    FOR m := 1 TO 6 DO
        u_ctrl[m]     := u_min[m];
        u_prev[m]     := u_min[m];
        u_delta[m]    := 0.0;
        u_gradient[m] := 0.0;
    END_FOR;

    bModelInitialized := TRUE;
END_IF;
"""
