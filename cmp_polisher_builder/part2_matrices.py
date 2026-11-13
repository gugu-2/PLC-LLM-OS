# cmp_polisher_builder/part2_matrices.py

def get_part2():
    return """(*
========================================================================================================================
  PHASE 0: CYBER-PHYSICAL DISCRETE STATE-SPACE & MPC MATRIX COEFFICIENT INITIALIZATION
  SAMPLE INTERVAL: Ts = 0.005 s (5 ms scan time)
========================================================================================================================
*)
IF bStateFirstScan THEN
    (* -------------------------------------------------------------------------------------------------------------- *)
    (* DISCRETE STATE TRANSITION MATRIX A (8x8)                                                                       *)
    (* Derived via zero-order hold discretization of linearized CMP tribo-thermo-kinetics at nominal operating point  *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    (* Row 1: Platen Spindle Angular Velocity Dynamics [rpm] *)
    a_mat[1, 1] := 0.98520;     (* Platen mechanical rotational inertia decay (tau = 0.334 s) *)
    a_mat[1, 2] := 0.00142;     (* Interfacial hydrodynamic shear coupling from carrier rotation *)
    a_mat[1, 3] := -0.01250;    (* Increased membrane downforce exerts frictional drag deceleration *)
    a_mat[1, 4] := 0.00000;     (* Film thickness has negligible direct inertia coupling *)
    a_mat[1, 5] := 0.00085;     (* Thermal expansion of pad increases contact area slightly *)
    a_mat[1, 6] := -0.04500;    (* Direct platen friction torque back-reaction *)
    a_mat[1, 7] := 0.00210;     (* Slurry film lubrication reduces interfacial traction drag *)
    a_mat[1, 8] := -0.00050;    (* Conditioning disc contact drag on platen *)

    (* Row 2: Wafer Carrier Head Angular Velocity Dynamics [rpm] *)
    a_mat[2, 1] := 0.00185;     (* Platen pad traction hydrodynamic entrainment *)
    a_mat[2, 2] := 0.98100;     (* Carrier head spindle mechanical inertia decay (tau = 0.260 s) *)
    a_mat[2, 3] := -0.01840;    (* Retaining ring and membrane normal downforce friction drag *)
    a_mat[2, 4] := 0.00000;     (* Interconnect thickness has negligible direct inertial effect *)
    a_mat[2, 5] := 0.00062;     (* Temperature effect on carrier gimbal bearing lubrication *)
    a_mat[2, 6] := -0.02200;    (* Friction torque reaction on carrier spindle *)
    a_mat[2, 7] := 0.00340;     (* Slurry fluid layer hydrodynamic coupling *)
    a_mat[2, 8] := 0.00000;     (* Conditioner disc is radially isolated from carrier head *)

    (* Row 3: Weighted Multi-Zone Membrane Downforce Pressure [psi] *)
    a_mat[3, 1] := 0.00010;     (* Platen speed hydrodynamic uplift effect *)
    a_mat[3, 2] := 0.00012;     (* Carrier speed hydrodynamic uplift effect *)
    a_mat[3, 3] := 0.94200;     (* Pneumatic membrane chamber pressure compliance (tau = 0.084 s) *)
    a_mat[3, 4] := 0.00000;     (* Film thickness does not alter pneumatic pressure *)
    a_mat[3, 5] := 0.00150;     (* Pad thermal expansion increases contact normal reaction *)
    a_mat[3, 6] := 0.00000;     (* Friction torque does not alter normal pneumatic pressure *)
    a_mat[3, 7] := 0.00080;     (* Slurry hydrodynamic squeeze-film lubrication pressure *)
    a_mat[3, 8] := 0.00000;     (* Conditioner does not directly load carrier membrane *)

    (* Row 4: Remaining Copper/Barrier Film Thickness [Angstrom] *)
    a_mat[4, 1] := -0.02450;    (* Preston MRR: Platen speed component of relative sliding velocity *)
    a_mat[4, 2] := -0.02180;    (* Preston MRR: Carrier speed component of relative sliding velocity *)
    a_mat[4, 3] := -0.38500;    (* Preston MRR: Direct normal downforce abrasion sensitivity *)
    a_mat[4, 4] := 1.00000;     (* Pure discrete integrator of Prestonian material removal *)
    a_mat[4, 5] := -0.01420;    (* Arrhenius thermal activation of chemical complexing etching *)
    a_mat[4, 6] := -0.00850;    (* Friction energy dissipation accelerating surface reaction *)
    a_mat[4, 7] := -0.03500;    (* Slurry chemical oxidizer and abrasive replenishment rate *)
    a_mat[4, 8] := -0.00500;    (* Asperity texturing refreshing active abrasive contact sites *)

    (* Row 5: Polyurethane Polishing Pad Surface Bulk Temperature [deg C] *)
    a_mat[5, 1] := 0.00420;     (* Platen rotation shear heating in pad grooves *)
    a_mat[5, 2] := 0.00380;     (* Carrier rotation interfacial frictional heat generation *)
    a_mat[5, 3] := 0.02850;     (* Normal downforce friction heating (q_f = mu * P * V) *)
    a_mat[5, 4] := 0.00000;     (* Film thickness has negligible thermal capacitance effect *)
    a_mat[5, 5] := 0.96800;     (* Pad bulk thermal dissipation to platen cooling channels (tau = 0.153 s) *)
    a_mat[5, 6] := 0.04200;     (* Direct frictional dissipation heat source *)
    a_mat[5, 7] := -0.01850;    (* Fresh chilled chemical slurry convective cooling effect *)
    a_mat[5, 8] := 0.00180;     (* Diamond conditioning disc frictional work input *)

    (* Row 6: Interfacial CMP Friction Torque at Platen Spindle [Nm] *)
    a_mat[6, 1] := -0.01500;    (* Hydrodynamic lubrication transition at higher platen speeds *)
    a_mat[6, 2] := -0.01200;    (* Hydrodynamic lift at higher carrier rotational velocities *)
    a_mat[6, 3] := 0.64500;     (* Direct Coulomb normal force to friction torque coupling *)
    a_mat[6, 4] := 0.00085;     (* Barrier layer (TaN) transition increases friction coefficient *)
    a_mat[6, 5] := -0.02400;    (* Temperature softening of polyurethane pad surface asperities *)
    a_mat[6, 6] := 0.88500;     (* Platen mechanical torque transducer compliance (tau = 0.041 s) *)
    a_mat[6, 7] := -0.04200;    (* Slurry hydrodynamic lubrication boundary layer reducing COF *)
    a_mat[6, 8] := 0.03200;     (* Conditioning disc friction load on platen *)

    (* Row 7: Active Slurry Chemical Volumetric Delivery Flow Rate [mL/min] *)
    a_mat[7, 1] := 0.00000;     (* Platen speed does not alter peristaltic pump discharge *)
    a_mat[7, 2] := 0.00000;     (* Carrier speed does not alter peristaltic pump discharge *)
    a_mat[7, 3] := 0.00000;     (* Membrane pressure does not alter slurry delivery line *)
    a_mat[7, 4] := 0.00000;     (* Film thickness does not alter delivery flow *)
    a_mat[7, 5] := 0.00000;     (* Pad temp does not alter peristaltic pumping rate *)
    a_mat[7, 6] := 0.00000;     (* Friction torque does not alter delivery flow *)
    a_mat[7, 7] := 0.92500;     (* Peristaltic delivery hydraulic line impedance decay (tau = 0.064 s) *)
    a_mat[7, 8] := 0.00000;     (* Conditioner does not alter pump flow *)

    (* Row 8: Pad Diamond Conditioning Cut Rate (PCR) [um/h] *)
    a_mat[8, 1] := 0.00850;     (* Platen speed increases diamond abrasive linear cutting speed *)
    a_mat[8, 2] := 0.00000;     (* Carrier rotation is decoupled from conditioner station *)
    a_mat[8, 3] := 0.00000;     (* Wafer membrane downforce is decoupled from conditioner head *)
    a_mat[8, 4] := 0.00000;     (* Wafer thickness does not alter pad cutting rate *)
    a_mat[8, 5] := 0.01200;     (* Pad polymer softness at elevated temperatures increases wear *)
    a_mat[8, 6] := 0.00000;     (* Friction torque has negligible direct effect on cut rate *)
    a_mat[8, 7] := 0.00550;     (* Slurry flushing removes abraded pad debris from diamond grits *)
    a_mat[8, 8] := 0.95200;     (* Conditioning process steady-state wear persistence (tau = 0.102 s) *)

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* DISCRETE INPUT COUPLING MATRIX B (8x8)                                                                         *)
    (* Relates 8 manipulated actuator commands [%] to state derivative increments over Ts = 5 ms                    *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    (* Row 1: Platen Spindle Speed Response *)
    b_mat[1, 1] := 0.28500;     (* u1: Platen Direct-Drive Motor Torque Command [%] *)
    b_mat[1, 2] := 0.00000;     (* u2: Carrier Motor Torque *)
    b_mat[1, 3] := -0.00850;    (* u3: Membrane Downforce Command *)
    b_mat[1, 4] := -0.01450;    (* u4: Retaining Ring Downforce Command *)
    b_mat[1, 5] := 0.00000;     (* u5: Slurry Pump Speed *)
    b_mat[1, 6] := -0.00620;    (* u6: Conditioner Downforce *)
    b_mat[1, 7] := 0.00000;     (* u7: Conditioner Sweep Servo *)
    b_mat[1, 8] := 0.00000;     (* u8: DIW Flush Valve *)

    (* Row 2: Carrier Head Spindle Speed Response *)
    b_mat[2, 1] := 0.00000;     (* u1: Platen Motor Torque *)
    b_mat[2, 2] := 0.32000;     (* u2: Carrier Direct-Drive Motor Torque Command [%] *)
    b_mat[2, 3] := -0.01250;    (* u3: Membrane Downforce Command *)
    b_mat[2, 4] := -0.02100;    (* u4: Retaining Ring Downforce Command *)
    b_mat[2, 5] := 0.00000;     (* u5: Slurry Pump Speed *)
    b_mat[2, 6] := 0.00000;     (* u6: Conditioner Downforce *)
    b_mat[2, 7] := 0.00000;     (* u7: Conditioner Sweep Servo *)
    b_mat[2, 8] := 0.00000;     (* u8: DIW Flush Valve *)

    (* Row 3: Weighted Membrane Downforce Pressure Response *)
    b_mat[3, 1] := 0.00000;     (* u1: Platen Motor Torque *)
    b_mat[3, 2] := 0.00000;     (* u2: Carrier Motor Torque *)
    b_mat[3, 3] := 0.05800;     (* u3: Membrane Master Pressure Regulator Command [%] *)
    b_mat[3, 4] := 0.00950;     (* u4: Retaining Ring Cross-Coupling into Edge Membrane *)
    b_mat[3, 5] := 0.00000;     (* u5: Slurry Pump Speed *)
    b_mat[3, 6] := 0.00000;     (* u6: Conditioner Downforce *)
    b_mat[3, 7] := 0.00000;     (* u7: Conditioner Sweep Servo *)
    b_mat[3, 8] := 0.00000;     (* u8: DIW Flush Valve *)

    (* Row 4: Remaining Film Thickness Response *)
    b_mat[4, 1] := -0.01850;    (* u1: Platen drive acceleration increases instantaneous MRR *)
    b_mat[4, 2] := -0.01620;    (* u2: Carrier drive acceleration increases instantaneous MRR *)
    b_mat[4, 3] := -0.42000;    (* u3: Direct membrane downforce increases Preston MRR *)
    b_mat[4, 4] := -0.08500;    (* u4: Retaining ring downforce pre-compressing pad asperities *)
    b_mat[4, 5] := -0.06500;    (* u5: Slurry supply providing fresh abrasive nanoparticles *)
    b_mat[4, 6] := -0.00210;    (* u6: Conditioner maintaining pad roughness Ra *)
    b_mat[4, 7] := 0.00000;     (* u7: Conditioner Sweep Servo *)
    b_mat[4, 8] := 0.04500;     (* u8: DIW rinse dilutes slurry, suppressing chemical MRR *)

    (* Row 5: Pad Surface Bulk Temperature Response *)
    b_mat[5, 1] := 0.00550;     (* u1: Platen torque creates shear viscous dissipation *)
    b_mat[5, 2] := 0.00480;     (* u2: Carrier torque creates interfacial frictional heating *)
    b_mat[5, 3] := 0.03800;     (* u3: Membrane pressure increases frictional heat flux *)
    b_mat[5, 4] := 0.01500;     (* u4: Retaining ring friction on outer pad track *)
    b_mat[5, 5] := -0.02200;    (* u5: Slurry chemical cooling enthalpy transport *)
    b_mat[5, 6] := 0.01100;     (* u6: Conditioner disc diamond friction heating *)
    b_mat[5, 7] := 0.00000;     (* u7: Conditioner Sweep Servo *)
    b_mat[5, 8] := -0.06500;    (* u8: DIW high-pressure rinse actively chills pad surface *)

    (* Row 6: Platen Spindle Friction Torque Response *)
    b_mat[6, 1] := -0.02800;    (* u1: Platen torque dynamic damping *)
    b_mat[6, 2] := -0.01800;    (* u2: Carrier torque dynamic damping *)
    b_mat[6, 3] := 0.48500;     (* u3: Membrane normal downforce generates friction torque *)
    b_mat[6, 4] := 0.16500;     (* u4: Retaining ring normal downforce generates friction torque *)
    b_mat[6, 5] := -0.05500;    (* u5: Slurry pump delivery reduces boundary friction *)
    b_mat[6, 6] := 0.08200;     (* u6: Conditioner downforce adds direct friction load on platen *)
    b_mat[6, 7] := 0.00000;     (* u7: Conditioner Sweep Servo *)
    b_mat[6, 8] := -0.09500;    (* u8: DIW flood provides liquid boundary layer lubrication *)

    (* Row 7: Slurry Volumetric Delivery Flow Response *)
    b_mat[7, 1] := 0.00000;     (* u1: Platen Motor Torque *)
    b_mat[7, 2] := 0.00000;     (* u2: Carrier Motor Torque *)
    b_mat[7, 3] := 0.00000;     (* u3: Membrane Downforce *)
    b_mat[7, 4] := 0.00000;     (* u4: Retaining Ring *)
    b_mat[7, 5] := 0.35000;     (* u5: Slurry Metering Pump Speed Command [%] *)
    b_mat[7, 6] := 0.00000;     (* u6: Conditioner Downforce *)
    b_mat[7, 7] := 0.00000;     (* u7: Conditioner Sweep Servo *)
    b_mat[7, 8] := 0.00000;     (* u8: DIW Flush Valve *)

    (* Row 8: Conditioner Pad Cut Rate (PCR) Response *)
    b_mat[8, 1] := 0.01100;     (* u1: Platen speed increases linear cutting velocity *)
    b_mat[8, 2] := 0.00000;     (* u2: Carrier Motor Torque *)
    b_mat[8, 3] := 0.00000;     (* u3: Membrane Downforce *)
    b_mat[8, 4] := 0.00000;     (* u4: Retaining Ring *)
    b_mat[8, 5] := 0.00000;     (* u5: Slurry Pump Speed *)
    b_mat[8, 6] := 0.14500;     (* u6: Conditioner Disc Downforce Cylinder Command [%] *)
    b_mat[8, 7] := 0.04800;     (* u7: Conditioner Sweep Velocity increases pad coverage rate *)
    b_mat[8, 8] := 0.00000;     (* u8: DIW Flush Valve *)

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* STATE OUTPUT MATRIX C (8x8)                                                                                    *)
    (* Direct measurement of physical process variables from state vector                                             *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    c_mat[1, 1] := 1.0; c_mat[1, 2] := 0.0; c_mat[1, 3] := 0.0; c_mat[1, 4] := 0.0;
    c_mat[1, 5] := 0.0; c_mat[1, 6] := 0.0; c_mat[1, 7] := 0.0; c_mat[1, 8] := 0.0;

    c_mat[2, 1] := 0.0; c_mat[2, 2] := 1.0; c_mat[2, 3] := 0.0; c_mat[2, 4] := 0.0;
    c_mat[2, 5] := 0.0; c_mat[2, 6] := 0.0; c_mat[2, 7] := 0.0; c_mat[2, 8] := 0.0;

    c_mat[3, 1] := 0.0; c_mat[3, 2] := 0.0; c_mat[3, 3] := 1.0; c_mat[3, 4] := 0.0;
    c_mat[3, 5] := 0.0; c_mat[3, 6] := 0.0; c_mat[3, 7] := 0.0; c_mat[3, 8] := 0.0;

    c_mat[4, 1] := 0.0; c_mat[4, 2] := 0.0; c_mat[4, 3] := 0.0; c_mat[4, 4] := 1.0;
    c_mat[4, 5] := 0.0; c_mat[4, 6] := 0.0; c_mat[4, 7] := 0.0; c_mat[4, 8] := 0.0;

    c_mat[5, 1] := 0.0; c_mat[5, 2] := 0.0; c_mat[5, 3] := 0.0; c_mat[4, 4] := 0.0;
    c_mat[5, 5] := 1.0; c_mat[5, 6] := 0.0; c_mat[5, 7] := 0.0; c_mat[5, 8] := 0.0;

    c_mat[6, 1] := 0.0; c_mat[6, 2] := 0.0; c_mat[6, 3] := 0.0; c_mat[6, 4] := 0.0;
    c_mat[6, 5] := 0.0; c_mat[6, 6] := 1.0; c_mat[6, 7] := 0.0; c_mat[6, 8] := 0.0;

    c_mat[7, 1] := 0.0; c_mat[7, 2] := 0.0; c_mat[7, 3] := 0.0; c_mat[7, 4] := 0.0;
    c_mat[7, 5] := 0.0; c_mat[7, 6] := 0.0; c_mat[7, 7] := 1.0; c_mat[7, 8] := 0.0;

    c_mat[8, 1] := 0.0; c_mat[8, 2] := 0.0; c_mat[8, 3] := 0.0; c_mat[8, 4] := 0.0;
    c_mat[8, 5] := 0.0; c_mat[8, 6] := 0.0; c_mat[8, 7] := 0.0; c_mat[8, 8] := 1.0;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* DIRECT FEEDTHROUGH MATRIX D (8x8)                                                                              *)
    (* Strictly zero for strictly proper cyber-physical mechanical-fluid system                                       *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    FOR i_idx := 1 TO 8 DO
        FOR j_idx := 1 TO 8 DO
            d_mat[i_idx, j_idx] := 0.0;
        END_FOR;
    END_FOR;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* DISTURBANCE COUPLING MATRIX E (8x4)                                                                            *)
    (* d1: Incoming Wafer Thickness Drift [A]                                                                         *)
    (* d2: Slurry Header Temp Variance [deg C]                                                                        *)
    (* d3: Slurry Chemical pH Deviation [pH units]                                                                    *)
    (* d4: Pad Glaze / Diamond Grit Wear State Index [0..1]                                                           *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    e_mat[1, 1] := 0.0;      e_mat[1, 2] := 0.0;      e_mat[1, 3] := 0.0;      e_mat[1, 4] := -0.0120;
    e_mat[2, 1] := 0.0;      e_mat[2, 2] := 0.0;      e_mat[2, 3] := 0.0;      e_mat[2, 4] := -0.0150;
    e_mat[3, 1] := 0.0;      e_mat[3, 2] := 0.0;      e_mat[3, 3] := 0.0;      e_mat[3, 4] := 0.0;
    e_mat[4, 1] := 1.0000;   e_mat[4, 2] := -0.0240;  e_mat[4, 3] := -0.0850;  e_mat[4, 4] := 0.2500;
    e_mat[5, 1] := 0.0;      e_mat[5, 2] := 0.0850;   e_mat[5, 3] := 0.0;      e_mat[5, 4] := -0.0350;
    e_mat[6, 1] := 0.0;      e_mat[6, 2] := -0.0150;  e_mat[6, 3] := 0.0;      e_mat[6, 4] := -0.4500;
    e_mat[7, 1] := 0.0;      e_mat[7, 2] := 0.0;      e_mat[7, 3] := 0.0;      e_mat[7, 4] := 0.0;
    e_mat[8, 1] := 0.0;      e_mat[8, 2] := 0.0;      e_mat[8, 3] := 0.0;      e_mat[8, 4] := -0.8500;

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* LUENBERGER OBSERVER GAIN VECTOR (8x1)                                                                          *)
    (* Pole-placed innovation gains ensuring asymptotic state convergence with 50 ms settling time                    *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    l_observer_gain[1] := 0.285;    (* Platen Angular Velocity Observer Gain *)
    l_observer_gain[2] := 0.310;    (* Carrier Angular Velocity Observer Gain *)
    l_observer_gain[3] := 0.420;    (* Membrane Pressure Observer Gain *)
    l_observer_gain[4] := 0.540;    (* Film Thickness Observer Gain (Eddy Current Fusion) *)
    l_observer_gain[5] := 0.220;    (* Pad Surface Temperature Observer Gain *)
    l_observer_gain[6] := 0.380;    (* Platen Spindle Torque Observer Gain *)
    l_observer_gain[7] := 0.450;    (* Slurry Delivery Flow Observer Gain *)
    l_observer_gain[8] := 0.190;    (* Diamond Conditioner Cut Rate Observer Gain *)

    (* -------------------------------------------------------------------------------------------------------------- *)
    (* MODEL PREDICTIVE CONTROL (MPC) PENALTY WEIGHTS & SATURATION LIMITS                                             *)
    (* -------------------------------------------------------------------------------------------------------------- *)
    (* State Tracking Penalty Diagonal Q (8x8) *)
    q_diag[1] := 4.5;       (* Platen speed error penalty *)
    q_diag[2] := 4.8;       (* Carrier speed error penalty *)
    q_diag[3] := 85.0;      (* Membrane downforce pressure precision penalty *)
    q_diag[4] := 250.0;     (* Copper film thickness tracking penalty (highest priority) *)
    q_diag[5] := 12.0;      (* Pad surface temperature limit penalty *)
    q_diag[6] := 6.5;       (* Platen friction torque stabilization penalty *)
    q_diag[7] := 18.0;      (* Slurry flow rate tracking penalty *)
    q_diag[8] := 15.0;      (* Conditioner cut rate tracking penalty *)

    (* Actuator Effort Penalty Diagonal R (8x8) *)
    r_diag[1] := 0.85;      (* Platen motor torque effort *)
    r_diag[2] := 0.95;      (* Carrier motor torque effort *)
    r_diag[3] := 2.50;      (* Membrane pressure regulator effort *)
    r_diag[4] := 3.20;      (* Retaining ring regulator effort *)
    r_diag[5] := 1.10;      (* Slurry pump speed effort *)
    r_diag[6] := 1.80;      (* Conditioner downforce cylinder effort *)
    r_diag[7] := 0.65;      (* Conditioner sweep servo effort *)
    r_diag[8] := 0.40;      (* DIW rinse valve effort *)

    (* Actuator Slew Rate Penalty Diagonal S (8x8) *)
    s_diag[1] := 2.4;       (* Platen torque slew penalty *)
    s_diag[2] := 2.8;       (* Carrier torque slew penalty *)
    s_diag[3] := 12.0;      (* Membrane pressure slew penalty (prevent wafer damage) *)
    s_diag[4] := 14.5;      (* Retaining ring pressure slew penalty *)
    s_diag[5] := 1.8;       (* Slurry pump speed slew penalty *)
    s_diag[6] := 3.5;       (* Conditioner cylinder slew penalty *)
    s_diag[7] := 1.2;       (* Conditioner sweep acceleration penalty *)
    s_diag[8] := 0.8;       (* DIW rinse valve transition penalty *)

    (* Terminal State Penalty Diagonal P (8x8) (Solution of Discrete Algebraic Riccati Equation) *)
    p_diag[1] := 8.2;
    p_diag[2] := 9.1;
    p_diag[3] := 165.0;
    p_diag[4] := 620.0;
    p_diag[5] := 28.0;
    p_diag[6] := 14.5;
    p_diag[7] := 34.0;
    p_diag[8] := 29.5;

    (* Physical Box Actuator Saturation Constraints [0.0 to 100.0 %] *)
    FOR i_idx := 1 TO 8 DO
        u_box_min[i_idx] := 0.0;
        u_box_max[i_idx] := 100.0;
    END_FOR;

    (* Dynamic Actuator Slew Rate Limits [% per 5ms scan] *)
    du_slew_max[1] := 1.85;   (* Platen drive max torque rate: 370 %/s *)
    du_slew_max[2] := 2.20;   (* Carrier drive max torque rate: 440 %/s *)
    du_slew_max[3] := 0.95;   (* Membrane pressure regulator max rate: 190 %/s *)
    du_slew_max[4] := 1.10;   (* Retaining ring regulator max rate: 220 %/s *)
    du_slew_max[5] := 3.50;   (* Slurry pump speed max rate: 700 %/s *)
    du_slew_max[6] := 1.45;   (* Conditioner cylinder max rate: 290 %/s *)
    du_slew_max[7] := 4.00;   (* Conditioner sweep servo max rate: 800 %/s *)
    du_slew_max[8] := 10.00;  (* DIW flush valve fast solenoid: 2000 %/s *)

    (* Initialize Reference Trajectory Vectors *)
    x_ref[1] := 93.0;       (* Nominal Platen Speed Setpoint [rpm] *)
    x_ref[2] := 87.0;       (* Nominal Carrier Speed Setpoint [rpm] *)
    x_ref[3] := 2.90;       (* Nominal Wafer Downforce Pressure [psi] *)
    x_ref[4] := 0.0;        (* Nominal Target Copper Interconnect Residual [Angstrom] *)
    x_ref[5] := 38.5;       (* Nominal Steady-State Pad Surface Temp [deg C] *)
    x_ref[6] := 115.0;      (* Nominal Platen Friction Torque [Nm] *)
    x_ref[7] := 250.0;      (* Nominal Slurry Delivery Flow [mL/min] *)
    x_ref[8] := 18.5;       (* Nominal Conditioner Pad Cut Rate [um/h] *)

    (* Nominal Equilibrium Actuator Commands *)
    u_ref[1] := 52.0;       (* Platen motor torque nominal *)
    u_ref[2] := 48.0;       (* Carrier motor torque nominal *)
    u_ref[3] := 42.0;       (* Membrane pressure regulator nominal *)
    u_ref[4] := 55.0;       (* Retaining ring regulator nominal *)
    u_ref[5] := 62.5;       (* Slurry pump speed nominal *)
    u_ref[6] := 38.0;       (* Conditioner cylinder pressure nominal *)
    u_ref[7] := 50.0;       (* Conditioner sweep servo nominal *)
    u_ref[8] := 0.0;        (* DIW rinse valve closed during polish *)

    (* Initial State Vector Estimates *)
    x_state[1] := 0.0;
    x_state[2] := 0.0;
    x_state[3] := 0.0;
    x_state[4] := 8500.0;   (* Incoming standard bulk copper overburden [Angstrom] *)
    x_state[5] := 22.0;     (* Cleanroom ambient pad temperature [deg C] *)
    x_state[6] := 0.0;
    x_state[7] := 0.0;
    x_state[8] := 0.0;

    FOR i_idx := 1 TO 8 DO
        u_ctrl[i_idx] := 0.0;
        u_prev[i_idx] := 0.0;
        FOR j_idx := 1 TO 5 DO
            u_mpc_traj[j_idx, i_idx] := 0.0;
        END_FOR;
    END_FOR;
END_IF;
"""
