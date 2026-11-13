# rail_emu_builder/part2_matrices.py

def get_part2():
    return '''(* ============================================================================================== *)
(* PHASE 0: FIRST-SCAN INITIALIZATION OF DISCRETE STATE-SPACE MATRICES & MPC PARAMETERS           *)
(* Sampling Period Ts = 0.005 s (5 ms). Discretized via Zero-Order Hold (ZOH)                      *)
(* ============================================================================================== *)
IF NOT bInitDone THEN
    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize State Transition Matrix A (8x8)                                                 *)
    (* States: 1:v_train, 2:v_axle1, 3:v_axle2, 4:F_panto, 5:U_dclink, 6:T_em, 7:P_bc, 8:mu_adh     *)
    (* ------------------------------------------------------------------------------------------ *)
    a_mat[1, 1] := 0.999820;  (* v_train self-decay (Davis aerodynamic/rolling friction) *)
    a_mat[1, 2] := 0.000045;  (* Axle 1 tractive creep coupling *)
    a_mat[1, 3] := 0.000045;  (* Axle 2 tractive creep coupling *)
    a_mat[1, 4] := 0.000000;  (* Pantograph contact force does not affect longitudinal motion *)
    a_mat[1, 5] := 0.000000;  (* DC bus voltage coupling negligible on vehicle mass *)
    a_mat[1, 6] := 0.000185;  (* Electromagnetic traction torque acceleration *)
    a_mat[1, 7] := -0.000240; (* Bogie brake cylinder pressure deceleration *)
    a_mat[1, 8] := 0.000050;  (* Available rail adhesion transmission factor *)

    a_mat[2, 1] := 0.014200;  (* Axle 1 mechanical coupling to rail ground velocity *)
    a_mat[2, 2] := 0.985000;  (* Axle 1 rotational inertia self-dynamics *)
    a_mat[2, 3] := 0.000000;  (* Bogie axle-to-axle mechanical isolation *)
    a_mat[2, 4] := 0.000000;  (* No direct pantograph coupling *)
    a_mat[2, 5] := 0.000000;  (* Inverter bus voltage indirect *)
    a_mat[2, 6] := 0.003150;  (* Traction motor torque acceleration on axle 1 inertia *)
    a_mat[2, 7] := -0.004250; (* Brake caliper friction deceleration on axle 1 *)
    a_mat[2, 8] := 0.001800;  (* Adhesion grip coefficient resisting wheel slip *)

    a_mat[3, 1] := 0.014200;  (* Axle 2 mechanical coupling to rail ground velocity *)
    a_mat[3, 2] := 0.000000;  (* Axle 1 to Axle 2 mechanical isolation *)
    a_mat[3, 3] := 0.985000;  (* Axle 2 rotational inertia self-dynamics *)
    a_mat[3, 4] := 0.000000;  (* No direct pantograph coupling *)
    a_mat[3, 5] := 0.000000;  (* Inverter bus voltage indirect *)
    a_mat[3, 6] := 0.003150;  (* Traction motor torque acceleration on axle 2 inertia *)
    a_mat[3, 7] := -0.004250; (* Brake caliper friction deceleration on axle 2 *)
    a_mat[3, 8] := 0.001800;  (* Adhesion grip coefficient resisting wheel slip *)

    a_mat[4, 1] := 0.000850;  (* High-speed train aerodynamic uplift on collector head *)
    a_mat[4, 2] := 0.000000;  (* Axle dynamics independent of catenary *)
    a_mat[4, 3] := 0.000000;  (* Axle dynamics independent of catenary *)
    a_mat[4, 4] := 0.942000;  (* Pantograph frame mechanical resonance & damper dissipation *)
    a_mat[4, 5] := 0.000000;  (* Electrical DC link independent *)
    a_mat[4, 6] := 0.000000;  (* Traction motor independent *)
    a_mat[4, 7] := 0.000000;  (* Pneumatic brake independent *)
    a_mat[4, 8] := 0.000000;  (* Rail adhesion independent *)

    a_mat[5, 1] := 0.000000;  (* Vehicle speed independent *)
    a_mat[5, 2] := 0.000000;  (* Axle speed independent *)
    a_mat[5, 3] := 0.000000;  (* Axle speed independent *)
    a_mat[5, 4] := 0.000000;  (* Pantograph contact independent *)
    a_mat[5, 5] := 0.995000;  (* DC link capacitor bank leakage / bleeding resistor discharge *)
    a_mat[5, 6] := -0.024000; (* Motoring electrical power extraction depletes bus voltage *)
    a_mat[5, 7] := 0.000000;  (* Brake cylinder independent *)
    a_mat[5, 8] := 0.000000;  (* Rail adhesion independent *)

    a_mat[6, 1] := 0.000000;  (* Train speed independent *)
    a_mat[6, 2] := -0.001200; (* Rotor back-EMF opposing torque at rising angular speed *)
    a_mat[6, 3] := -0.001200; (* Rotor back-EMF opposing torque *)
    a_mat[6, 4] := 0.000000;  (* Pantograph independent *)
    a_mat[6, 5] := 0.000550;  (* DC bus voltage stiffens electromagnetic torque capability *)
    a_mat[6, 6] := 0.885000;  (* Asynchronous motor electromagnetic lag (rotor time constant) *)
    a_mat[6, 7] := 0.000000;  (* Brake cylinder independent *)
    a_mat[6, 8] := 0.000000;  (* Rail adhesion independent *)

    a_mat[7, 1] := 0.000000;  (* Speed independent *)
    a_mat[7, 2] := 0.000000;  (* Axle independent *)
    a_mat[7, 3] := 0.000000;  (* Axle independent *)
    a_mat[7, 4] := 0.000000;  (* Pantograph independent *)
    a_mat[7, 5] := 0.000000;  (* DC link independent *)
    a_mat[7, 6] := 0.000000;  (* Motor torque independent *)
    a_mat[7, 7] := 0.925000;  (* Pneumatic brake cylinder filling/exhaust volume time constant *)
    a_mat[7, 8] := 0.000000;  (* Adhesion independent *)

    a_mat[8, 1] := -0.000015; (* Curtius-Kniffler high-speed adhesion degradation slope *)
    a_mat[8, 2] := -0.000085; (* High axle 1 slip speed induces microscopic thermal degradation *)
    a_mat[8, 3] := -0.000085; (* High axle 2 slip speed degrades railhead contact film *)
    a_mat[8, 4] := 0.000000;  (* Pantograph independent *)
    a_mat[8, 5] := 0.000000;  (* DC link independent *)
    a_mat[8, 6] := 0.000000;  (* Motor torque indirect *)
    a_mat[8, 7] := 0.000000;  (* Brake pressure indirect *)
    a_mat[8, 8] := 0.992000;  (* Railhead surface physical condition persistence *)

    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize Input Coupling Matrix B (8x8)                                                   *)
    (* Inputs: 1:Isd*, 2:Isq*, 3:Mod_4QC, 4:Panto_valv, 5:T_ed*, 6:EP_pilot, 7:WSSP_dmp, 8:WSSP_app*)
    (* ------------------------------------------------------------------------------------------ *)
    b_mat[1, 1] := 0.000000;  b_mat[1, 2] := 0.000000;  b_mat[1, 3] := 0.000000;  b_mat[1, 4] := 0.000000;
    b_mat[1, 5] := -0.000120; b_mat[1, 6] := -0.000180; b_mat[1, 7] := 0.000050;  b_mat[1, 8] := -0.000040;

    b_mat[2, 1] := 0.000000;  b_mat[2, 2] := 0.000000;  b_mat[2, 3] := 0.000000;  b_mat[2, 4] := 0.000000;
    b_mat[2, 5] := -0.002800; b_mat[2, 6] := -0.003500; b_mat[2, 7] := 0.004800;  b_mat[2, 8] := -0.003800;

    b_mat[3, 1] := 0.000000;  b_mat[3, 2] := 0.000000;  b_mat[3, 3] := 0.000000;  b_mat[3, 4] := 0.000000;
    b_mat[3, 5] := -0.002800; b_mat[3, 6] := -0.003500; b_mat[3, 7] := 0.004800;  b_mat[3, 8] := -0.003800;

    b_mat[4, 1] := 0.000000;  b_mat[4, 2] := 0.000000;  b_mat[4, 3] := 0.000000;  b_mat[4, 4] := 0.585000;
    b_mat[4, 5] := 0.000000;  b_mat[4, 6] := 0.000000;  b_mat[4, 7] := 0.000000;  b_mat[4, 8] := 0.000000;

    b_mat[5, 1] := 0.000000;  b_mat[5, 2] := 0.000000;  b_mat[5, 3] := 0.420000;  b_mat[5, 4] := 0.000000;
    b_mat[5, 5] := 0.018000;  b_mat[5, 6] := 0.000000;  b_mat[5, 7] := 0.000000;  b_mat[5, 8] := 0.000000;

    b_mat[6, 1] := 0.000450;  b_mat[6, 2] := 0.012500;  b_mat[6, 3] := 0.000000;  b_mat[6, 4] := 0.000000;
    b_mat[6, 5] := -0.115000; b_mat[6, 6] := 0.000000;  b_mat[6, 7] := 0.000000;  b_mat[6, 8] := 0.000000;

    b_mat[7, 1] := 0.000000;  b_mat[7, 2] := 0.000000;  b_mat[7, 3] := 0.000000;  b_mat[7, 4] := 0.000000;
    b_mat[7, 5] := 0.000000;  b_mat[7, 6] := 0.075000;  b_mat[7, 7] := -0.125000; b_mat[7, 8] := 0.085000;

    b_mat[8, 1] := 0.000000;  b_mat[8, 2] := 0.000000;  b_mat[8, 3] := 0.000000;  b_mat[8, 4] := 0.000000;
    b_mat[8, 5] := 0.000000;  b_mat[8, 6] := 0.000000;  b_mat[8, 7] := 0.000150;  b_mat[8, 8] := -0.000100;

    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize Disturbance Coupling Matrix E (8x4)                                             *)
    (* Disturbances: 1:F_grade, 2:v_wind, 3:U_catenary_fluct, 4:K_rail_contam                      *)
    (* ------------------------------------------------------------------------------------------ *)
    e_mat[1, 1] := -0.000115; (* Upward grade decelerates train longitudinal motion *)
    e_mat[1, 2] := -0.000085; (* Headwind increases aerodynamic drag resistance *)
    e_mat[1, 3] := 0.000000;  (* Voltage fluctuation negligible on mass *)
    e_mat[1, 4] := 0.000000;  (* Contamination indirect *)

    e_mat[2, 1] := -0.000095; (* Axle 1 grade load *)
    e_mat[2, 2] := 0.000000;  (* Headwind indirect *)
    e_mat[2, 3] := 0.000000;  (* Voltage fluctuation indirect *)
    e_mat[2, 4] := -0.001250; (* Rail contamination promotes wheel slip on axle 1 *)

    e_mat[3, 1] := -0.000095; (* Axle 2 grade load *)
    e_mat[3, 2] := 0.000000;  (* Headwind indirect *)
    e_mat[3, 3] := 0.000000;  (* Voltage fluctuation indirect *)
    e_mat[3, 4] := -0.001250; (* Rail contamination promotes wheel slip on axle 2 *)

    e_mat[4, 1] := 0.000000;  (* Grade independent *)
    e_mat[4, 2] := 0.012500;  (* Direct headwind aerodynamic uplift on pantograph *)
    e_mat[4, 3] := 0.000000;  (* Catenary voltage independent *)
    e_mat[4, 4] := 0.000000;  (* Rail contamination independent *)

    e_mat[5, 1] := 0.000000;  (* Grade independent *)
    e_mat[5, 2] := 0.000000;  (* Headwind independent *)
    e_mat[5, 3] := 0.185000;  (* Catenary line voltage drop causes DC link sag *)
    e_mat[5, 4] := 0.000000;  (* Contamination independent *)

    e_mat[6, 1] := 0.000000;  (* Grade handled via feedback *)
    e_mat[6, 2] := 0.000000;  (* Headwind handled via feedback *)
    e_mat[6, 3] := 0.008500;  (* Line voltage fluctuation ripples electromagnetic torque *)
    e_mat[6, 4] := 0.000000;  (* Contamination indirect *)

    e_mat[7, 1] := 0.000000;  (* Brake cylinder isolated from external disturbances *)
    e_mat[7, 2] := 0.000000;  
    e_mat[7, 3] := 0.000000;  
    e_mat[7, 4] := 0.000000;  

    e_mat[8, 1] := 0.000000;  (* Grade independent *)
    e_mat[8, 2] := 0.000000;  (* Headwind independent *)
    e_mat[8, 3] := 0.000000;  (* Voltage independent *)
    e_mat[8, 4] := -0.085000; (* Rail surface water/leaves severely degrades adhesion *)

    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize State Output Matrix C (8x8) and Direct Feedthrough D (8x8)                      *)
    (* ------------------------------------------------------------------------------------------ *)
    FOR i := 1 TO 8 DO
        FOR j := 1 TO 8 DO
            IF i = j THEN
                c_mat[i, j] := 1.0;
            ELSE
                c_mat[i, j] := 0.0;
            END_IF;
            d_mat[i, j] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize Luenberger Observer Correction Gains L (8x1)                                    *)
    (* ------------------------------------------------------------------------------------------ *)
    l_observer_gain[1] := 0.185; (* Train speed observer gain *)
    l_observer_gain[2] := 0.245; (* Axle 1 speed observer gain *)
    l_observer_gain[3] := 0.245; (* Axle 2 speed observer gain *)
    l_observer_gain[4] := 0.195; (* Pantograph force observer gain *)
    l_observer_gain[5] := 0.280; (* DC link bus voltage observer gain *)
    l_observer_gain[6] := 0.320; (* Traction torque observer gain *)
    l_observer_gain[7] := 0.260; (* Brake cylinder pressure observer gain *)
    l_observer_gain[8] := 0.145; (* Rail adhesion observer gain *)

    (* ------------------------------------------------------------------------------------------ *)
    (* Initialize MPC Quadratic Cost Penalty Matrices Q, R, S, P (Diagonal Elements)             *)
    (* ------------------------------------------------------------------------------------------ *)
    q_diag[1] := 18.50;  (* High priority: Train speed trajectory tracking *)
    q_diag[2] := 12.00;  (* Axle 1 speed synchronism with train velocity *)
    q_diag[3] := 12.00;  (* Axle 2 speed synchronism with train velocity *)
    q_diag[4] := 6.50;   (* Pantograph contact force tight regulation *)
    q_diag[5] := 3.20;   (* DC link voltage regulation *)
    q_diag[6] := 5.80;   (* Traction torque tracking *)
    q_diag[7] := 8.40;   (* Brake cylinder pressure tracking *)
    q_diag[8] := 25.00;  (* Highest penalty: Adhesion preservation & anti-slip *)

    r_diag[1] := 0.45;   (* Actuator effort penalty: Isd* *)
    r_diag[2] := 0.35;   (* Actuator effort penalty: Isq* *)
    r_diag[3] := 0.25;   (* Actuator effort penalty: 4QC modulation *)
    r_diag[4] := 0.60;   (* Actuator effort penalty: Pantograph valve *)
    r_diag[5] := 0.40;   (* Actuator effort penalty: ED brake *)
    r_diag[6] := 0.50;   (* Actuator effort penalty: EP brake *)
    r_diag[7] := 0.85;   (* Actuator effort penalty: WSSP dump valve duty *)
    r_diag[8] := 0.85;   (* Actuator effort penalty: WSSP apply valve duty *)

    s_diag[1] := 1.20;   (* Slew rate penalty: d(Isd)/dt *)
    s_diag[2] := 0.95;   (* Slew rate penalty: d(Isq)/dt *)
    s_diag[3] := 0.80;   (* Slew rate penalty: d(Mod_4QC)/dt *)
    s_diag[4] := 1.50;   (* Slew rate penalty: d(Panto_valve)/dt *)
    s_diag[5] := 1.10;   (* Slew rate penalty: d(T_ed)/dt *)
    s_diag[6] := 1.30;   (* Slew rate penalty: d(EP_valve)/dt *)
    s_diag[7] := 2.20;   (* Slew rate penalty: d(WSSP_dump)/dt *)
    s_diag[8] := 2.20;   (* Slew rate penalty: d(WSSP_apply)/dt *)

    p_diag[1] := 28.00;  (* Terminal state penalty: Train speed *)
    p_diag[2] := 18.00;  (* Terminal state penalty: Axle 1 *)
    p_diag[3] := 18.00;  (* Terminal state penalty: Axle 2 *)
    p_diag[4] := 9.80;   (* Terminal state penalty: Pantograph *)
    p_diag[5] := 4.80;   (* Terminal state penalty: DC link *)
    p_diag[6] := 8.70;   (* Terminal state penalty: Torque *)
    p_diag[7] := 12.60;  (* Terminal state penalty: Brake *)
    p_diag[8] := 38.00;  (* Terminal state penalty: Adhesion *)

    (* Actuator Box Saturation Constraints *)
    u_box_min[1] := 50.0;    u_box_max[1] := 450.0;   (* Isd*: 50 A to 450 A *)
    u_box_min[2] := -600.0;  u_box_max[2] := 600.0;   (* Isq*: -600 A to +600 A *)
    u_box_min[3] := 0.0;     u_box_max[3] := 100.0;   (* 4QC Modulation: 0% to 100% *)
    u_box_min[4] := 0.0;     u_box_max[4] := 100.0;   (* Pantograph valve: 0% to 100% *)
    u_box_min[5] := 0.0;     u_box_max[5] := 13.60;   (* ED brake torque: 0 to 13.6 kNm *)
    u_box_min[6] := 0.0;     u_box_max[6] := 100.0;   (* EP pilot valve: 0% to 100% *)
    u_box_min[7] := 0.0;     u_box_max[7] := 100.0;   (* WSSP dump PWM: 0% to 100% *)
    u_box_min[8] := 0.0;     u_box_max[8] := 100.0;   (* WSSP apply PWM: 0% to 100% *)

    (* Actuator Maximum Dynamic Slew Rate per 5 ms Cycle *)
    du_slew_max[1] := 15.0;  (* Isd max slew: 15 A/cycle *)
    du_slew_max[2] := 25.0;  (* Isq max slew: 25 A/cycle *)
    du_slew_max[3] := 5.0;   (* 4QC modulation max slew: 5%/cycle *)
    du_slew_max[4] := 4.0;   (* Pantograph valve max slew: 4%/cycle *)
    du_slew_max[5] := 0.50;  (* ED brake torque max slew: 0.5 kNm/cycle *)
    du_slew_max[6] := 6.0;   (* EP pilot valve max slew: 6%/cycle *)
    du_slew_max[7] := 20.0;  (* WSSP dump valve fast slew: 20%/cycle *)
    du_slew_max[8] := 20.0;  (* WSSP apply valve fast slew: 20%/cycle *)

    (* Initialize State and Trajectory Vectors *)
    FOR i := 1 TO 8 DO
        x_state[i] := 0.0;
        x_next[i] := 0.0;
        y_meas[i] := 0.0;
        u_ctrl[i] := 0.0;
        x_ref[i] := 0.0;
        u_ref[i] := 0.0;
        u_prev[i] := 0.0;
        FOR k := 1 TO 5 DO
            u_mpc_traj[k, i] := 0.0;
        END_FOR;
    END_FOR;

    x_state[5] := 3000.0; (* DC link pre-charged initial state *)
    x_state[8] := 0.280;  (* Initial clean dry rail adhesion *)

    bInitDone := TRUE;
END_IF;
'''
