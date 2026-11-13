# pharma_tableting_builder/part2_init_matrices.py

def get_part2():
    return """(* === PHASE 0: ONE-SHOT FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE INITIALIZATION === *)
IF NOT bMatricesInitialized THEN
    (* ----------------------------------------------------------------------------------------- *)
    (* Discrete State Transition Matrix A (8x8) at Ts = 2 ms                                     *)
    (* Models cross-coupled granulator powder transport, moisture evaporation, turret dynamics  *)
    (* and tablet compaction mechanics.                                                         *)
    (* ----------------------------------------------------------------------------------------- *)
    a_mat[1,1] := 0.985200;  a_mat[1,2] := 0.000000;  a_mat[1,3] := 0.000000;  a_mat[1,4] := 0.000000;  a_mat[1,5] := 0.000000;  a_mat[1,6] := 0.000000;  a_mat[1,7] := 0.000000;  a_mat[1,8] := 0.000000;
    a_mat[2,1] := -0.012400; a_mat[2,2] := 0.978500;  a_mat[2,3] := 0.000000;  a_mat[2,4] := 0.000000;  a_mat[2,5] := 0.000000;  a_mat[2,6] := 0.000000;  a_mat[2,7] := 0.000000;  a_mat[2,8] := 0.000000;
    a_mat[3,1] := 0.045000;  a_mat[3,2] := 0.185000;  a_mat[3,3] := 0.962000;  a_mat[3,4] := 0.000000;  a_mat[3,5] := 0.000000;  a_mat[3,6] := 0.000000;  a_mat[3,7] := 0.000000;  a_mat[3,8] := 0.000000;
    a_mat[4,1] := 0.008500;  a_mat[4,2] := 0.062000;  a_mat[4,3] := -0.001200; a_mat[4,4] := 0.982000;  a_mat[4,5] := -0.015400; a_mat[4,6] := 0.000000;  a_mat[4,7] := 0.000000;  a_mat[4,8] := 0.000000;
    a_mat[5,1] := 0.000000;  a_mat[5,2] := 0.000000;  a_mat[5,3] := 0.000000;  a_mat[5,4] := 0.000000;  a_mat[5,5] := 0.991500;  a_mat[5,6] := 0.000000;  a_mat[5,7] := 0.000000;  a_mat[5,8] := 0.000000;
    a_mat[6,1] := 0.000000;  a_mat[6,2] := 0.000000;  a_mat[6,3] := 0.000000;  a_mat[6,4] := 0.000000;  a_mat[6,5] := 0.000000;  a_mat[6,6] := 0.994000;  a_mat[6,7] := 0.000000;  a_mat[6,8] := 0.000000;
    a_mat[7,1] := 0.015000;  a_mat[7,2] := 0.008000;  a_mat[7,3] := 0.004200;  a_mat[7,4] := 0.085000;  a_mat[7,5] := 0.000000;  a_mat[7,6] := -0.018500; a_mat[7,7] := 0.965000;  a_mat[7,8] := 0.000000;
    a_mat[8,1] := 0.022000;  a_mat[8,2] := 0.014000;  a_mat[8,3] := 0.018000;  a_mat[8,4] := -0.042000; a_mat[8,5] := 0.000000;  a_mat[8,6] := -0.009000; a_mat[8,7] := 0.245000;  a_mat[8,8] := 0.958000;

    (* ----------------------------------------------------------------------------------------- *)
    (* Input Coupling Matrix B (8x8) at Ts = 2 ms                                                *)
    (* Direct response to LIW screw, micro-pump, barrel speed, heater, damper, press servos      *)
    (* ----------------------------------------------------------------------------------------- *)
    b_mat[1,1] := 0.038500;  b_mat[1,2] := 0.000000;  b_mat[1,3] := 0.000000;  b_mat[1,4] := 0.000000;  b_mat[1,5] := 0.000000;  b_mat[1,6] := 0.000000;  b_mat[1,7] := 0.000000;  b_mat[1,8] := 0.000000;
    b_mat[2,1] := -0.004200; b_mat[2,2] := 0.024500;  b_mat[2,3] := 0.000000;  b_mat[2,4] := 0.000000;  b_mat[2,5] := 0.000000;  b_mat[2,6] := 0.000000;  b_mat[2,7] := 0.000000;  b_mat[2,8] := 0.000000;
    b_mat[3,1] := 0.001800;  b_mat[3,2] := 0.008500;  b_mat[3,3] := 0.012500;  b_mat[3,4] := 0.000000;  b_mat[3,5] := 0.000000;  b_mat[3,6] := 0.000000;  b_mat[3,7] := 0.000000;  b_mat[3,8] := 0.000000;
    b_mat[4,1] := 0.000000;  b_mat[4,2] := 0.001200;  b_mat[4,3] := 0.000000;  b_mat[4,4] := -0.016500; b_mat[4,5] := -0.008500; b_mat[4,6] := 0.000000;  b_mat[4,7] := 0.000000;  b_mat[4,8] := 0.000000;
    b_mat[5,1] := 0.000000;  b_mat[5,2] := 0.000000;  b_mat[5,3] := 0.000000;  b_mat[5,4] := 0.042000;  b_mat[5,5] := -0.011000; b_mat[5,6] := 0.000000;  b_mat[5,7] := 0.000000;  b_mat[5,8] := 0.000000;
    b_mat[6,1] := 0.000000;  b_mat[6,2] := 0.000000;  b_mat[6,3] := 0.000000;  b_mat[6,4] := 0.000000;  b_mat[6,5] := 0.000000;  b_mat[6,6] := 0.058000;  b_mat[6,7] := 0.000000;  b_mat[6,8] := 0.000000;
    b_mat[7,1] := 0.000000;  b_mat[7,2] := 0.000000;  b_mat[7,3] := 0.000000;  b_mat[7,4] := 0.000000;  b_mat[7,5] := 0.000000;  b_mat[7,6] := 0.008200;  b_mat[7,7] := 0.016500;  b_mat[7,8] := 0.125000;
    b_mat[8,1] := 0.000000;  b_mat[8,2] := 0.000000;  b_mat[8,3] := 0.000000;  b_mat[8,4] := 0.000000;  b_mat[8,5] := 0.000000;  b_mat[8,6] := 0.003500;  b_mat[8,7] := 0.009400;  b_mat[8,8] := 0.082000;

    (* ----------------------------------------------------------------------------------------- *)
    (* Observation Output Matrix C (8x8)                                                         *)
    (* Direct mapping of states to sensor process measurements                                   *)
    (* ----------------------------------------------------------------------------------------- *)
    c_mat[1,1] := 1.000000;  c_mat[1,2] := 0.000000;  c_mat[1,3] := 0.000000;  c_mat[1,4] := 0.000000;  c_mat[1,5] := 0.000000;  c_mat[1,6] := 0.000000;  c_mat[1,7] := 0.000000;  c_mat[1,8] := 0.000000;
    c_mat[2,1] := 0.000000;  c_mat[2,2] := 1.000000;  c_mat[2,3] := 0.000000;  c_mat[2,4] := 0.000000;  c_mat[2,5] := 0.000000;  c_mat[2,6] := 0.000000;  c_mat[2,7] := 0.000000;  c_mat[2,8] := 0.000000;
    c_mat[3,1] := 0.000000;  c_mat[3,2] := 0.000000;  c_mat[3,3] := 1.000000;  c_mat[3,4] := 0.000000;  c_mat[3,5] := 0.000000;  c_mat[3,6] := 0.000000;  c_mat[3,7] := 0.000000;  c_mat[3,8] := 0.000000;
    c_mat[4,1] := 0.000000;  c_mat[4,2] := 0.000000;  c_mat[4,3] := 0.000000;  c_mat[4,4] := 1.000000;  c_mat[4,5] := 0.000000;  c_mat[4,6] := 0.000000;  c_mat[4,7] := 0.000000;  c_mat[4,8] := 0.000000;
    c_mat[5,1] := 0.000000;  c_mat[5,2] := 0.000000;  c_mat[5,3] := 0.000000;  c_mat[5,4] := 0.000000;  c_mat[5,5] := 1.000000;  c_mat[5,6] := 0.000000;  c_mat[5,7] := 0.000000;  c_mat[5,8] := 0.000000;
    c_mat[6,1] := 0.000000;  c_mat[6,2] := 0.000000;  c_mat[6,3] := 0.000000;  c_mat[6,4] := 0.000000;  c_mat[6,5] := 0.000000;  c_mat[6,6] := 1.000000;  c_mat[6,7] := 0.000000;  c_mat[6,8] := 0.000000;
    c_mat[7,1] := 0.000000;  c_mat[7,2] := 0.000000;  c_mat[7,3] := 0.000000;  c_mat[7,4] := 0.000000;  c_mat[7,5] := 0.000000;  c_mat[7,6] := 0.000000;  c_mat[7,7] := 1.000000;  c_mat[7,8] := 0.000000;
    c_mat[8,1] := 0.000000;  c_mat[8,2] := 0.000000;  c_mat[8,3] := 0.000000;  c_mat[8,4] := 0.000000;  c_mat[8,5] := 0.000000;  c_mat[8,6] := 0.000000;  c_mat[8,7] := 0.000000;  c_mat[8,8] := 1.000000;

    (* ----------------------------------------------------------------------------------------- *)
    (* Feedthrough Matrix D (8x8) - Strictly strictly causal                                     *)
    (* ----------------------------------------------------------------------------------------- *)
    d_mat[1,1] := 0.000000;  d_mat[1,2] := 0.000000;  d_mat[1,3] := 0.000000;  d_mat[1,4] := 0.000000;  d_mat[1,5] := 0.000000;  d_mat[1,6] := 0.000000;  d_mat[1,7] := 0.000000;  d_mat[1,8] := 0.000000;
    d_mat[2,1] := 0.000000;  d_mat[2,2] := 0.000000;  d_mat[2,3] := 0.000000;  d_mat[2,4] := 0.000000;  d_mat[2,5] := 0.000000;  d_mat[2,6] := 0.000000;  d_mat[2,7] := 0.000000;  d_mat[2,8] := 0.000000;
    d_mat[3,1] := 0.000000;  d_mat[3,2] := 0.000000;  d_mat[3,3] := 0.000000;  d_mat[3,4] := 0.000000;  d_mat[3,5] := 0.000000;  d_mat[3,6] := 0.000000;  d_mat[3,7] := 0.000000;  d_mat[3,8] := 0.000000;
    d_mat[4,1] := 0.000000;  d_mat[4,2] := 0.000000;  d_mat[4,3] := 0.000000;  d_mat[4,4] := 0.000000;  d_mat[4,5] := 0.000000;  d_mat[4,6] := 0.000000;  d_mat[4,7] := 0.000000;  d_mat[4,8] := 0.000000;
    d_mat[5,1] := 0.000000;  d_mat[5,2] := 0.000000;  d_mat[5,3] := 0.000000;  d_mat[5,4] := 0.000000;  d_mat[5,5] := 0.000000;  d_mat[5,6] := 0.000000;  d_mat[5,7] := 0.000000;  d_mat[5,8] := 0.000000;
    d_mat[6,1] := 0.000000;  d_mat[6,2] := 0.000000;  d_mat[6,3] := 0.000000;  d_mat[6,4] := 0.000000;  d_mat[6,5] := 0.000000;  d_mat[6,6] := 0.000000;  d_mat[6,7] := 0.000000;  d_mat[6,8] := 0.000000;
    d_mat[7,1] := 0.000000;  d_mat[7,2] := 0.000000;  d_mat[7,3] := 0.000000;  d_mat[7,4] := 0.000000;  d_mat[7,5] := 0.000000;  d_mat[7,6] := 0.000000;  d_mat[7,7] := 0.000000;  d_mat[7,8] := 0.000000;
    d_mat[8,1] := 0.000000;  d_mat[8,2] := 0.000000;  d_mat[8,3] := 0.000000;  d_mat[8,4] := 0.000000;  d_mat[8,5] := 0.000000;  d_mat[8,6] := 0.000000;  d_mat[8,7] := 0.000000;  d_mat[8,8] := 0.000000;

    (* ----------------------------------------------------------------------------------------- *)
    (* Disturbance Coupling Matrix E (8x4)                                                       *)
    (* External impacts: bulk density, humidity ingress, binder temp, punch tooling wear        *)
    (* ----------------------------------------------------------------------------------------- *)
    e_mat[1,1] := 0.018500;  e_mat[1,2] := 0.000000;  e_mat[1,3] := 0.000000;  e_mat[1,4] := 0.000000;
    e_mat[2,1] := -0.006500; e_mat[2,2] := 0.002200;  e_mat[2,3] := 0.001400;  e_mat[2,4] := 0.000000;
    e_mat[3,1] := 0.012000;  e_mat[3,2] := 0.004500;  e_mat[3,3] := 0.003000;  e_mat[3,4] := 0.000000;
    e_mat[4,1] := 0.000000;  e_mat[4,2] := 0.009200;  e_mat[4,3] := -0.001500; e_mat[4,4] := 0.000000;
    e_mat[5,1] := 0.000000;  e_mat[5,2] := -0.004000; e_mat[5,3] := 0.000000;  e_mat[5,4] := 0.000000;
    e_mat[6,1] := 0.000000;  e_mat[6,2] := 0.000000;  e_mat[6,3] := 0.000000;  e_mat[6,4] := -0.002500;
    e_mat[7,1] := 0.045000;  e_mat[7,2] := 0.008000;  e_mat[7,3] := 0.000000;  e_mat[7,4] := 0.038000;
    e_mat[8,1] := 0.032000;  e_mat[8,2] := -0.011000; e_mat[8,3] := 0.000000;  e_mat[8,4] := 0.021000;

    (* ----------------------------------------------------------------------------------------- *)
    (* Luenberger Observer Correction Gains L (8x1)                                              *)
    (* Designed via pole placement for asymptotic zero steady-state error                        *)
    (* ----------------------------------------------------------------------------------------- *)
    l_observer[1] := 0.220000;
    l_observer[2] := 0.185000;
    l_observer[3] := 0.150000;
    l_observer[4] := 0.245000;
    l_observer[5] := 0.165000;
    l_observer[6] := 0.280000;
    l_observer[7] := 0.310000;
    l_observer[8] := 0.195000;

    (* ----------------------------------------------------------------------------------------- *)
    (* MPC Quadratic Penalty Diagonal Weights: Q, R, S, P                                        *)
    (* Q: State error, R: Actuator effort, S: Slew rate, P: Terminal state                       *)
    (* ----------------------------------------------------------------------------------------- *)
    q_diag[1] := 12.50;  (* Feeder Flow rate error penalty *)
    q_diag[2] := 45.00;  (* Liquid-to-Solid ratio error penalty *)
    q_diag[3] := 8.50;   (* Granule D50 particle size error penalty *)
    q_diag[4] := 85.00;  (* Granule LOD moisture error penalty *)
    q_diag[5] := 18.00;  (* Fluid bed air temp error penalty *)
    q_diag[6] := 35.00;  (* Turret rotational speed error penalty *)
    q_diag[7] := 120.00; (* Main compression peak force penalty *)
    q_diag[8] := 65.00;  (* Tablet tensile hardness error penalty *)

    r_diag[1] := 0.150;  (* LIW Feeder screw motor effort *)
    r_diag[2] := 0.350;  (* Liquid binder micro-pump effort *)
    r_diag[3] := 0.080;  (* Granulator drive motor effort *)
    r_diag[4] := 0.120;  (* Fluid bed air heater duty effort *)
    r_diag[5] := 0.110;  (* Fluid bed velocity damper effort *)
    r_diag[6] := 0.250;  (* Tablet press turret drive effort *)
    r_diag[7] := 0.090;  (* Feeder paddle wheel drive effort *)
    r_diag[8] := 0.450;  (* Dosing cam servo positioning effort *)

    s_diag[1] := 2.50;   (* Slew rate penalty Feeder motor *)
    s_diag[2] := 5.80;   (* Slew rate penalty Binder pump *)
    s_diag[3] := 1.20;   (* Slew rate penalty Granulator drive *)
    s_diag[4] := 3.40;   (* Slew rate penalty Air heater *)
    s_diag[5] := 2.80;   (* Slew rate penalty Blower damper *)
    s_diag[6] := 6.50;   (* Slew rate penalty Turret drive *)
    s_diag[7] := 1.80;   (* Slew rate penalty Paddle wheel *)
    s_diag[8] := 8.50;   (* Slew rate penalty Dosing cam servo *)

    p_diag[1] := 18.50;  (* Terminal penalty State 1 *)
    p_diag[2] := 65.00;  (* Terminal penalty State 2 *)
    p_diag[3] := 12.00;  (* Terminal penalty State 3 *)
    p_diag[4] := 125.00; (* Terminal penalty State 4 *)
    p_diag[5] := 26.00;  (* Terminal penalty State 5 *)
    p_diag[6] := 55.00;  (* Terminal penalty State 6 *)
    p_diag[7] := 185.00; (* Terminal penalty State 7 *)
    p_diag[8] := 95.00;  (* Terminal penalty State 8 *)

    (* ----------------------------------------------------------------------------------------- *)
    (* Actuator Physical Box Saturation Bounds [u_min, u_max] and Slew Limits du_max             *)
    (* ----------------------------------------------------------------------------------------- *)
    u_min[1] := 0.0;    u_max[1] := 60.0;    du_max[1] := 1.20;   (* LIW Feeder Inverter [Hz] *)
    u_min[2] := 0.0;    u_max[2] := 150.0;   du_max[2] := 3.50;   (* Binder Pump Flow [g/min] *)
    u_min[3] := 0.0;    u_max[3] := 800.0;   du_max[3] := 15.0;   (* Granulator Screw [rpm] *)
    u_min[4] := 0.0;    u_max[4] := 100.0;   du_max[4] := 2.50;   (* Air Heater Duty [%] *)
    u_min[5] := 0.0;    u_max[5] := 100.0;   du_max[5] := 2.00;   (* Air Damper Velocity [%] *)
    u_min[6] := 0.0;    u_max[6] := 110.0;   du_max[6] := 2.20;   (* Turret Drive Speed [rpm] *)
    u_min[7] := 0.0;    u_max[7] := 160.0;   du_max[7] := 4.00;   (* Feed Paddle Speed [rpm] *)
    u_min[8] := 0.50;   u_max[8] := 15.0;    du_max[8] := 0.15;   (* Dosing Cam Position [mm] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* Station Punch Arrays Initial Reset (Punch 1 to 48)                                        *)
    (* ----------------------------------------------------------------------------------------- *)
    arrStationPeakForce[1] := 32.50; arrStationPreCompForce[1] := 4.50; arrStationRejectFlag[1] := FALSE; arrStationConsecutiveRejects[1] := 0;
    arrStationPeakForce[2] := 32.50; arrStationPreCompForce[2] := 4.50; arrStationRejectFlag[2] := FALSE; arrStationConsecutiveRejects[2] := 0;
    arrStationPeakForce[3] := 32.50; arrStationPreCompForce[3] := 4.50; arrStationRejectFlag[3] := FALSE; arrStationConsecutiveRejects[3] := 0;
    arrStationPeakForce[4] := 32.50; arrStationPreCompForce[4] := 4.50; arrStationRejectFlag[4] := FALSE; arrStationConsecutiveRejects[4] := 0;
    arrStationPeakForce[5] := 32.50; arrStationPreCompForce[5] := 4.50; arrStationRejectFlag[5] := FALSE; arrStationConsecutiveRejects[5] := 0;
    arrStationPeakForce[6] := 32.50; arrStationPreCompForce[6] := 4.50; arrStationRejectFlag[6] := FALSE; arrStationConsecutiveRejects[6] := 0;
    arrStationPeakForce[7] := 32.50; arrStationPreCompForce[7] := 4.50; arrStationRejectFlag[7] := FALSE; arrStationConsecutiveRejects[7] := 0;
    arrStationPeakForce[8] := 32.50; arrStationPreCompForce[8] := 4.50; arrStationRejectFlag[8] := FALSE; arrStationConsecutiveRejects[8] := 0;
    arrStationPeakForce[9] := 32.50; arrStationPreCompForce[9] := 4.50; arrStationRejectFlag[9] := FALSE; arrStationConsecutiveRejects[9] := 0;
    arrStationPeakForce[10] := 32.50; arrStationPreCompForce[10] := 4.50; arrStationRejectFlag[10] := FALSE; arrStationConsecutiveRejects[10] := 0;
    arrStationPeakForce[11] := 32.50; arrStationPreCompForce[11] := 4.50; arrStationRejectFlag[11] := FALSE; arrStationConsecutiveRejects[11] := 0;
    arrStationPeakForce[12] := 32.50; arrStationPreCompForce[12] := 4.50; arrStationRejectFlag[12] := FALSE; arrStationConsecutiveRejects[12] := 0;
    arrStationPeakForce[13] := 32.50; arrStationPreCompForce[13] := 4.50; arrStationRejectFlag[13] := FALSE; arrStationConsecutiveRejects[13] := 0;
    arrStationPeakForce[14] := 32.50; arrStationPreCompForce[14] := 4.50; arrStationRejectFlag[14] := FALSE; arrStationConsecutiveRejects[14] := 0;
    arrStationPeakForce[15] := 32.50; arrStationPreCompForce[15] := 4.50; arrStationRejectFlag[15] := FALSE; arrStationConsecutiveRejects[15] := 0;
    arrStationPeakForce[16] := 32.50; arrStationPreCompForce[16] := 4.50; arrStationRejectFlag[16] := FALSE; arrStationConsecutiveRejects[16] := 0;
    arrStationPeakForce[17] := 32.50; arrStationPreCompForce[17] := 4.50; arrStationRejectFlag[17] := FALSE; arrStationConsecutiveRejects[17] := 0;
    arrStationPeakForce[18] := 32.50; arrStationPreCompForce[18] := 4.50; arrStationRejectFlag[18] := FALSE; arrStationConsecutiveRejects[18] := 0;
    arrStationPeakForce[19] := 32.50; arrStationPreCompForce[19] := 4.50; arrStationRejectFlag[19] := FALSE; arrStationConsecutiveRejects[19] := 0;
    arrStationPeakForce[20] := 32.50; arrStationPreCompForce[20] := 4.50; arrStationRejectFlag[20] := FALSE; arrStationConsecutiveRejects[20] := 0;
    arrStationPeakForce[21] := 32.50; arrStationPreCompForce[21] := 4.50; arrStationRejectFlag[21] := FALSE; arrStationConsecutiveRejects[21] := 0;
    arrStationPeakForce[22] := 32.50; arrStationPreCompForce[22] := 4.50; arrStationRejectFlag[22] := FALSE; arrStationConsecutiveRejects[22] := 0;
    arrStationPeakForce[23] := 32.50; arrStationPreCompForce[23] := 4.50; arrStationRejectFlag[23] := FALSE; arrStationConsecutiveRejects[23] := 0;
    arrStationPeakForce[24] := 32.50; arrStationPreCompForce[24] := 4.50; arrStationRejectFlag[24] := FALSE; arrStationConsecutiveRejects[24] := 0;
    arrStationPeakForce[25] := 32.50; arrStationPreCompForce[25] := 4.50; arrStationRejectFlag[25] := FALSE; arrStationConsecutiveRejects[25] := 0;
    arrStationPeakForce[26] := 32.50; arrStationPreCompForce[26] := 4.50; arrStationRejectFlag[26] := FALSE; arrStationConsecutiveRejects[26] := 0;
    arrStationPeakForce[27] := 32.50; arrStationPreCompForce[27] := 4.50; arrStationRejectFlag[27] := FALSE; arrStationConsecutiveRejects[27] := 0;
    arrStationPeakForce[28] := 32.50; arrStationPreCompForce[28] := 4.50; arrStationRejectFlag[28] := FALSE; arrStationConsecutiveRejects[28] := 0;
    arrStationPeakForce[29] := 32.50; arrStationPreCompForce[29] := 4.50; arrStationRejectFlag[29] := FALSE; arrStationConsecutiveRejects[29] := 0;
    arrStationPeakForce[30] := 32.50; arrStationPreCompForce[30] := 4.50; arrStationRejectFlag[30] := FALSE; arrStationConsecutiveRejects[30] := 0;
    arrStationPeakForce[31] := 32.50; arrStationPreCompForce[31] := 4.50; arrStationRejectFlag[31] := FALSE; arrStationConsecutiveRejects[31] := 0;
    arrStationPeakForce[32] := 32.50; arrStationPreCompForce[32] := 4.50; arrStationRejectFlag[32] := FALSE; arrStationConsecutiveRejects[32] := 0;
    arrStationPeakForce[33] := 32.50; arrStationPreCompForce[33] := 4.50; arrStationRejectFlag[33] := FALSE; arrStationConsecutiveRejects[33] := 0;
    arrStationPeakForce[34] := 32.50; arrStationPreCompForce[34] := 4.50; arrStationRejectFlag[34] := FALSE; arrStationConsecutiveRejects[34] := 0;
    arrStationPeakForce[35] := 32.50; arrStationPreCompForce[35] := 4.50; arrStationRejectFlag[35] := FALSE; arrStationConsecutiveRejects[35] := 0;
    arrStationPeakForce[36] := 32.50; arrStationPreCompForce[36] := 4.50; arrStationRejectFlag[36] := FALSE; arrStationConsecutiveRejects[36] := 0;
    arrStationPeakForce[37] := 32.50; arrStationPreCompForce[37] := 4.50; arrStationRejectFlag[37] := FALSE; arrStationConsecutiveRejects[37] := 0;
    arrStationPeakForce[38] := 32.50; arrStationPreCompForce[38] := 4.50; arrStationRejectFlag[38] := FALSE; arrStationConsecutiveRejects[38] := 0;
    arrStationPeakForce[39] := 32.50; arrStationPreCompForce[39] := 4.50; arrStationRejectFlag[39] := FALSE; arrStationConsecutiveRejects[39] := 0;
    arrStationPeakForce[40] := 32.50; arrStationPreCompForce[40] := 4.50; arrStationRejectFlag[40] := FALSE; arrStationConsecutiveRejects[40] := 0;
    arrStationPeakForce[41] := 32.50; arrStationPreCompForce[41] := 4.50; arrStationRejectFlag[41] := FALSE; arrStationConsecutiveRejects[41] := 0;
    arrStationPeakForce[42] := 32.50; arrStationPreCompForce[42] := 4.50; arrStationRejectFlag[42] := FALSE; arrStationConsecutiveRejects[42] := 0;
    arrStationPeakForce[43] := 32.50; arrStationPreCompForce[43] := 4.50; arrStationRejectFlag[43] := FALSE; arrStationConsecutiveRejects[43] := 0;
    arrStationPeakForce[44] := 32.50; arrStationPreCompForce[44] := 4.50; arrStationRejectFlag[44] := FALSE; arrStationConsecutiveRejects[44] := 0;
    arrStationPeakForce[45] := 32.50; arrStationPreCompForce[45] := 4.50; arrStationRejectFlag[45] := FALSE; arrStationConsecutiveRejects[45] := 0;
    arrStationPeakForce[46] := 32.50; arrStationPreCompForce[46] := 4.50; arrStationRejectFlag[46] := FALSE; arrStationConsecutiveRejects[46] := 0;
    arrStationPeakForce[47] := 32.50; arrStationPreCompForce[47] := 4.50; arrStationRejectFlag[47] := FALSE; arrStationConsecutiveRejects[47] := 0;
    arrStationPeakForce[48] := 32.50; arrStationPreCompForce[48] := 4.50; arrStationRejectFlag[48] := FALSE; arrStationConsecutiveRejects[48] := 0;

    (* Initial Equilibrium State Vector Estimation *)
    x_state[1] := 25.00; (* Feeder mass flow rate 25 kg/h *)
    x_state[2] := 10.50; (* Liquid-to-solid ratio 10.5% *)
    x_state[3] := 285.0; (* Granule median diameter 285 um *)
    x_state[4] := 1.95;  (* Fluid bed moisture 1.95% LOD *)
    x_state[5] := 58.00; (* Fluid bed supply air temp 58 deg C *)
    x_state[6] := 86.80; (* Turret speed 86.8 rpm (approx 250,000 tph) *)
    x_state[7] := 32.50; (* Main compression peak force 32.5 kN *)
    x_state[8] := 105.0; (* Tablet breaking hardness 105 N *)

    (* Initial Nominal Actuator Baseline *)
    u_prev[1] := 32.50;  (* LIW screw frequency [Hz] *)
    u_prev[2] := 43.75;  (* Liquid binder pump flow [g/min] *)
    u_prev[3] := 450.0;  (* Granulator screw speed [rpm] *)
    u_prev[4] := 48.50;  (* Air heater duty [%] *)
    u_prev[5] := 62.00;  (* Air flow damper position [%] *)
    u_prev[6] := 86.80;  (* Turret drive speed command [rpm] *)
    u_prev[7] := 65.00;  (* Feeder paddle speed [rpm] *)
    u_prev[8] := 5.20;   (* Lower punch dosing position [mm] *)

    bMatricesInitialized := TRUE;
END_IF;
"""
