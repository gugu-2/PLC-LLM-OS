# scratch/gen_phase2.py

def get_phase2():
    lines = []
    lines.append("""
(* ============================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION (8-STATE KALMAN)*)
(* ============================================================================== *)
(* Model formulation sampled at Ts = 25 ms (0.025 s).                             *)
(* States:                                                                        *)
(*   x1: SG Narrow-Range Level deviation [mm]                                     *)
(*   x2: Downcomer Recirculation Flow Rate [kg/s]                                 *)
(*   x3: Boiling Riser Mean Void Fraction [ratio 0.0..1.0]                        *)
(*   x4: Primary-to-Secondary U-Tube Heat Transfer Rate [MW]                      *)
(*   x5: Saturated Steam Drum Pressure [bar]                                      *)
(*   x6: RCS Cold Leg Return Temperature [deg C]                                  *)
(*   x7: Main Feedwater Regulating Valve Trim Effective Position [%]              *)
(*   x8: Non-Minimum Phase (NMP) Dynamic Lead/Lag Shrink/Swell State [mm]         *)
(* ------------------------------------------------------------------------------ *)

IF NOT bInitialized THEN
    (* ------------------------------------------------------------------------- *)
    (* SYSTEM DYNAMICS MATRIX A (8x8) INITIALIZATION                             *)
    (* Derived from linearized conservation equations for mass, momentum, energy *)
    (* ------------------------------------------------------------------------- *)
    (* Row 1: Narrow Range Level Dynamics (Integrator + Recirculation + Swell) *)
    A_Matrix[1, 1] := 1.00000000; (* Mass inventory pure integrator *)
    A_Matrix[1, 2] := 0.00342500; (* Downcomer liquid influx momentum coupling *)
    A_Matrix[1, 3] := 485.62000000; (* Riser void fraction volumetric expansion swell *)
    A_Matrix[1, 4] := 0.00185000; (* Thermal expansion boundary swell *)
    A_Matrix[1, 5] := -0.04215000; (* Vapor compressibility density effect on level *)
    A_Matrix[1, 6] := -0.01560000; (* Cold leg subcooling condensation feedback *)
    A_Matrix[1, 7] := 0.00045000; (* Valve trim direct mechanical coupling *)
    A_Matrix[1, 8] := 0.98500000; (* Dynamic non-minimum phase lead-lag state transfer *)

    (* Row 2: Downcomer Recirculation Mass Flow Rate Dynamics *)
    A_Matrix[2, 1] := 0.00012000; (* Static hydrostatic head feedback *)
    A_Matrix[2, 2] := 0.97850000; (* Fluid momentum inertia decay (tau_dc = 1.15 s) *)
    A_Matrix[2, 3] := 42.15000000; (* Natural circulation driving head from riser voids *)
    A_Matrix[2, 4] := 0.00840000; (* Heat addition buoyancy acceleration *)
    A_Matrix[2, 5] := -0.01250000; (* Pressure gradient across separator deck *)
    A_Matrix[2, 6] := 0.03540000; (* Subcooled fluid density head variation *)
    A_Matrix[2, 7] := 0.12500000; (* Feedwater ring jet induction momentum *)
    A_Matrix[2, 8] := 0.00000000;

    (* Row 3: Boiling Riser Mean Void Fraction Dynamics *)
    A_Matrix[3, 1] := 0.00000500;
    A_Matrix[3, 2] := -0.00008500; (* Liquid velocity sweeping vapor bubbles out *)
    A_Matrix[3, 3] := 0.96200000; (* Bubble residence time constant (tau_void = 0.65 s) *)
    A_Matrix[3, 4] := 0.00021500; (* Primary heat flux vapor generation rate *)
    A_Matrix[3, 5] := -0.00145000; (* Pressure suppression of boiling bubble growth *)
    A_Matrix[3, 6] := 0.00018500; (* Coolant temperature driving Delta-T *)
    A_Matrix[3, 7] := -0.00004500; (* Cold feedwater void collapse (Thermal Shrink) *)
    A_Matrix[3, 8] := 0.00000000;

    (* Row 4: Primary-to-Secondary U-Tube Heat Transfer Rate Dynamics *)
    A_Matrix[4, 1] := 0.00000000;
    A_Matrix[4, 2] := 0.00125000; (* Riser mass velocity convective heat transfer boost *)
    A_Matrix[4, 3] := -0.02450000; (* Two-phase boiling heat transfer coefficient shift *)
    A_Matrix[4, 4] := 0.98100000; (* Inconel 690 tube metal thermal lag (tau_m = 1.30 s) *)
    A_Matrix[4, 5] := -0.15800000; (* Saturation temperature change reduces Log Mean Delta T *)
    A_Matrix[4, 6] := -0.08450000; (* Cold leg boundary temperature shift *)
    A_Matrix[4, 7] := 0.00560000; (* Feedwater subcooling heat extraction *)
    A_Matrix[4, 8] := 0.00000000;

    (* Row 5: Steam Drum Saturated Vapor Pressure Dynamics *)
    A_Matrix[5, 1] := 0.00001500;
    A_Matrix[5, 2] := 0.00005500;
    A_Matrix[5, 3] := 0.24500000; (* Vapor release rate into steam space *)
    A_Matrix[5, 4] := 0.00062000; (* Net energy addition vapor pressurization *)
    A_Matrix[5, 5] := 0.99350000; (* Steam drum compressibility capacity (tau_p = 3.82 s) *)
    A_Matrix[5, 6] := 0.00015000;
    A_Matrix[5, 7] := -0.00002500;
    A_Matrix[5, 8] := -0.00008500;

    (* Row 6: RCS Cold Leg Return Temperature Dynamics *)
    A_Matrix[6, 1] := 0.00000000;
    A_Matrix[6, 2] := -0.00004500;
    A_Matrix[6, 3] := 0.00120000;
    A_Matrix[6, 4] := -0.00285000; (* Heat extracted cools primary coolant stream *)
    A_Matrix[6, 5] := 0.02150000; (* Secondary saturation pressure equilibrium coupling *)
    A_Matrix[6, 6] := 0.98800000; (* Lower plenum mixing volume time constant (tau = 2.08 s) *)
    A_Matrix[6, 7] := -0.00015000;
    A_Matrix[6, 8] := 0.00000000;

    (* Row 7: Main Feedwater Regulating Valve Trim Position Dynamics *)
    A_Matrix[7, 1] := 0.00000000;
    A_Matrix[7, 2] := 0.00000000;
    A_Matrix[7, 3] := 0.00000000;
    A_Matrix[7, 4] := 0.00000000;
    A_Matrix[7, 5] := 0.00000000;
    A_Matrix[7, 6] := 0.00000000;
    A_Matrix[7, 7] := 0.94500000; (* Electro-hydraulic actuator lag (tau_act = 0.45 s) *)
    A_Matrix[7, 8] := 0.00000000;

    (* Row 8: Non-Minimum Phase Dynamic Lead/Lag State Dynamics *)
    A_Matrix[8, 1] := 0.00000000;
    A_Matrix[8, 2] := -0.00150000;
    A_Matrix[8, 3] := 0.08500000; (* Internal void redistribution excitation *)
    A_Matrix[8, 4] := 0.00045000;
    A_Matrix[8, 5] := -0.01200000; (* Sudden pressure transient excitation *)
    A_Matrix[8, 6] := 0.00000000;
    A_Matrix[8, 7] := 0.00000000;
    A_Matrix[8, 8] := 0.93500000; (* NMP transient decay time constant (tau_nmp = 0.38 s) *)

    (* ------------------------------------------------------------------------- *)
    (* CONTROL INPUT MATRIX B (8x5) INITIALIZATION                               *)
    (* Inputs: u1=MFRV [%], u2=BPV [%], u3=AFW [%], u4=Blowdown [kg/s], u5=Steam [kg/s] *)
    (* ------------------------------------------------------------------------- *)
    (* Row 1: Level State x1 *)
    B_Matrix[1, 1] := -0.01250000; (* Cold feedwater initial shrink reverse response *)
    B_Matrix[1, 2] := -0.00450000; (* Bypass feedwater cold shrink *)
    B_Matrix[1, 3] := -0.00850000; (* Auxiliary feedwater subcooled shrink *)
    B_Matrix[1, 4] := -0.00025000; (* Continuous blowdown mass drain *)
    B_Matrix[1, 5] := 0.04850000; (* Steam demand sudden increase flash swell *)

    (* Row 2: Downcomer Flow x2 *)
    B_Matrix[2, 1] := 0.85400000; (* MFRV valve opening drives downcomer inflow *)
    B_Matrix[2, 2] := 0.31200000; (* BPV valve opening drives downcomer inflow *)
    B_Matrix[2, 3] := 0.45000000; (* AFW pump flow enters upper downcomer *)
    B_Matrix[2, 4] := -0.05000000; (* Blowdown extraction at tubesheet level *)
    B_Matrix[2, 5] := 0.01200000;

    (* Row 3: Void Fraction x3 *)
    B_Matrix[3, 1] := -0.00085000; (* Cold subcooled water collapses voids *)
    B_Matrix[3, 2] := -0.00028000;
    B_Matrix[3, 3] := -0.00065000;
    B_Matrix[3, 4] := -0.00001000;
    B_Matrix[3, 5] := 0.00195000; (* Depressurization induces flashing void expansion *)

    (* Row 4: Heat Transfer Rate x4 *)
    B_Matrix[4, 1] := 0.00420000; (* Subcooling increases Delta-T across tubesheet *)
    B_Matrix[4, 2] := 0.00140000;
    B_Matrix[4, 3] := 0.00310000;
    B_Matrix[4, 4] := 0.00010000;
    B_Matrix[4, 5] := 0.01850000; (* Increased steaming rate draws more heat flux *)

    (* Row 5: Steam Drum Pressure x5 *)
    B_Matrix[5, 1] := -0.00045000;
    B_Matrix[5, 2] := -0.00015000;
    B_Matrix[5, 3] := -0.00035000;
    B_Matrix[5, 4] := -0.00120000;
    B_Matrix[5, 5] := -0.01650000; (* Steam extraction directly depletes vapor pressure *)

    (* Row 6: Cold Leg Temp x6 *)
    B_Matrix[6, 1] := -0.00185000; (* Subcooled secondary side cools primary return *)
    B_Matrix[6, 2] := -0.00062000;
    B_Matrix[6, 3] := -0.00145000;
    B_Matrix[6, 4] := -0.00005000;
    B_Matrix[6, 5] := -0.00450000; (* Steam load increase pulls primary temperature down *)

    (* Row 7: Valve Trim x7 *)
    B_Matrix[7, 1] := 0.05500000; (* Actuator demand driving trim position *)
    B_Matrix[7, 2] := 0.00000000;
    B_Matrix[7, 3] := 0.00000000;
    B_Matrix[7, 4] := 0.00000000;
    B_Matrix[7, 5] := 0.00000000;

    (* Row 8: NMP Lead/Lag State x8 *)
    B_Matrix[8, 1] := -0.08500000; (* Feedwater injection shrink excitation *)
    B_Matrix[8, 2] := -0.03200000;
    B_Matrix[8, 3] := -0.05500000;
    B_Matrix[8, 4] := 0.00000000;
    B_Matrix[8, 5] := 0.14500000; (* Steam extraction flash swell excitation *)

    (* ------------------------------------------------------------------------- *)
    (* OUTPUT MEASUREMENT MATRIX C (5x8) INITIALIZATION                          *)
    (* Outputs: y1=NR Level, y2=Feedwater Flow, y3=Pressure, y4=Cold Leg, y5=Steam Flow *)
    (* ------------------------------------------------------------------------- *)
    C_Matrix[1, 1] := 1.00000000; (* Measured level observes physical water level *)
    C_Matrix[1, 2] := 0.00000000;
    C_Matrix[1, 3] := 0.00000000;
    C_Matrix[1, 4] := 0.00000000;
    C_Matrix[1, 5] := 0.00000000;
    C_Matrix[1, 6] := 0.00000000;
    C_Matrix[1, 7] := 0.00000000;
    C_Matrix[1, 8] := 1.00000000; (* Measured level observes prompt NMP reverse state *)

    C_Matrix[2, 1] := 0.00000000;
    C_Matrix[2, 2] := 0.98500000; (* Feedwater flow observes downcomer mass inflow *)
    C_Matrix[2, 3] := 0.00000000;
    C_Matrix[2, 4] := 0.00000000;
    C_Matrix[2, 5] := 0.00000000;
    C_Matrix[2, 6] := 0.00000000;
    C_Matrix[2, 7] := 0.15000000; (* Valve trim position coupling *)
    C_Matrix[2, 8] := 0.00000000;

    C_Matrix[3, 1] := 0.00000000;
    C_Matrix[3, 2] := 0.00000000;
    C_Matrix[3, 3] := 0.00000000;
    C_Matrix[3, 4] := 0.00000000;
    C_Matrix[3, 5] := 1.00000000; (* Pressure transmitter observes drum pressure *)
    C_Matrix[3, 6] := 0.00000000;
    C_Matrix[3, 7] := 0.00000000;
    C_Matrix[3, 8] := 0.00000000;

    C_Matrix[4, 1] := 0.00000000;
    C_Matrix[4, 2] := 0.00000000;
    C_Matrix[4, 3] := 0.00000000;
    C_Matrix[4, 4] := 0.00000000;
    C_Matrix[4, 5] := 0.00000000;
    C_Matrix[4, 6] := 1.00000000; (* RTD observes cold leg return temperature *)
    C_Matrix[4, 7] := 0.00000000;
    C_Matrix[4, 8] := 0.00000000;

    C_Matrix[5, 1] := 0.00000000;
    C_Matrix[5, 2] := 0.00000000;
    C_Matrix[5, 3] := 0.05000000; (* Boiling void formation feeds steaming rate *)
    C_Matrix[5, 4] := 0.01500000; (* Heat transfer rate creates steam *)
    C_Matrix[5, 5] := 0.02500000; (* Choked sonic velocity through turbine valves *)
    C_Matrix[5, 6] := 0.00000000;
    C_Matrix[5, 7] := 0.00000000;
    C_Matrix[5, 8] := 0.00000000;

    (* ------------------------------------------------------------------------- *)
    (* DIRECT TRANSMISSION MATRIX D (5x5) INITIALIZATION                         *)
    (* ------------------------------------------------------------------------- *)
    D_Matrix[1, 1] := 0.00000000;
    D_Matrix[1, 2] := 0.00000000;
    D_Matrix[1, 3] := 0.00000000;
    D_Matrix[1, 4] := 0.00000000;
    D_Matrix[1, 5] := 0.00000000;

    D_Matrix[2, 1] := 0.08500000; (* Direct feedthrough of MFRV actuator demand *)
    D_Matrix[2, 2] := 0.03500000; (* Direct feedthrough of BPV demand *)
    D_Matrix[2, 3] := 0.05000000; (* Direct feedthrough of AFW demand *)
    D_Matrix[2, 4] := 0.00000000;
    D_Matrix[2, 5] := 0.00000000;

    D_Matrix[3, 1] := 0.00000000;
    D_Matrix[3, 2] := 0.00000000;
    D_Matrix[3, 3] := 0.00000000;
    D_Matrix[3, 4] := 0.00000000;
    D_Matrix[3, 5] := -0.00250000; (* Prompt pressure acoustic response to steam flow *)

    D_Matrix[4, 1] := 0.00000000;
    D_Matrix[4, 2] := 0.00000000;
    D_Matrix[4, 3] := 0.00000000;
    D_Matrix[4, 4] := 0.00000000;
    D_Matrix[4, 5] := 0.00000000;

    D_Matrix[5, 1] := 0.00000000;
    D_Matrix[5, 2] := 0.00000000;
    D_Matrix[5, 3] := 0.00000000;
    D_Matrix[5, 4] := 0.00000000;
    D_Matrix[5, 5] := 0.98500000; (* Measured steam flow tracks turbine flow directly *)

    (* ------------------------------------------------------------------------- *)
    (* KALMAN FILTER OBSERVER GAIN MATRIX L (8x5) INITIALIZATION                 *)
    (* Synthesized via discrete Algebraic Riccati Equation (DARE) solution       *)
    (* ------------------------------------------------------------------------- *)
    L_Matrix[1, 1] := 0.18500000; (* Level correction from level innovation *)
    L_Matrix[1, 2] := 0.01250000;
    L_Matrix[1, 3] := -0.00850000;
    L_Matrix[1, 4] := 0.00045000;
    L_Matrix[1, 5] := -0.01450000;

    L_Matrix[2, 1] := 0.04500000;
    L_Matrix[2, 2] := 0.24500000; (* Downcomer flow correction from FW flow innovation *)
    L_Matrix[2, 3] := 0.01850000;
    L_Matrix[2, 4] := 0.00250000;
    L_Matrix[2, 5] := 0.03500000;

    L_Matrix[3, 1] := 0.00125000;
    L_Matrix[3, 2] := -0.00085000;
    L_Matrix[3, 3] := -0.00245000; (* Void fraction corrected from pressure innovation *)
    L_Matrix[3, 4] := 0.00015000;
    L_Matrix[3, 5] := 0.00450000; (* Void fraction corrected from steam flow innovation *)

    L_Matrix[4, 1] := 0.00850000;
    L_Matrix[4, 2] := 0.01500000;
    L_Matrix[4, 3] := 0.04500000;
    L_Matrix[4, 4] := 0.18500000; (* Heat transfer corrected from cold leg temp *)
    L_Matrix[4, 5] := 0.09500000; (* Heat transfer corrected from steam flow *)

    L_Matrix[5, 1] := 0.00250000;
    L_Matrix[5, 2] := 0.00120000;
    L_Matrix[5, 3] := 0.28500000; (* Pressure state correction from pressure innovation *)
    L_Matrix[5, 4] := 0.00150000;
    L_Matrix[5, 5] := -0.01850000;

    L_Matrix[6, 1] := 0.00045000;
    L_Matrix[6, 2] := 0.00085000;
    L_Matrix[6, 3] := 0.01200000;
    L_Matrix[6, 4] := 0.21500000; (* Cold leg temp correction from cold leg innovation *)
    L_Matrix[6, 5] := -0.00550000;

    L_Matrix[7, 1] := 0.00150000;
    L_Matrix[7, 2] := 0.12500000; (* Valve trim corrected from feedwater flow *)
    L_Matrix[7, 3] := 0.00050000;
    L_Matrix[7, 4] := 0.00000000;
    L_Matrix[7, 5] := 0.00000000;

    L_Matrix[8, 1] := 0.14500000; (* NMP state corrected from level innovation *)
    L_Matrix[8, 2] := -0.02500000;
    L_Matrix[8, 3] := 0.01500000;
    L_Matrix[8, 4] := 0.00000000;
    L_Matrix[8, 5] := 0.08500000; (* NMP state corrected from steam flow innovation *)

    (* ------------------------------------------------------------------------- *)
    (* MPC WEIGHTING MATRICES Q, R, S, P INITIALIZATION                          *)
    (* ------------------------------------------------------------------------- *)
    Q_diag[1] := 18.50000000; (* Level tracking penalty *)
    Q_diag[2] := 2.50000000; (* Downcomer flow regulation penalty *)
    Q_diag[3] := 8.50000000; (* Void fraction stability penalty *)
    Q_diag[4] := 1.20000000; (* Thermal stress minimization penalty *)
    Q_diag[5] := 12.00000000; (* Steam drum pressure deviation penalty *)
    Q_diag[6] := 3.50000000; (* Cold leg temperature return penalty *)
    Q_diag[7] := 0.50000000; (* Valve trim position deviation penalty *)
    Q_diag[8] := 15.00000000; (* NMP reverse dynamic state suppression penalty *)

    R_diag[1] := 0.85000000; (* MFRV control effort penalty *)
    R_diag[2] := 1.25000000; (* BPV control effort penalty *)

    S_diag[1] := 3.50000000; (* MFRV rate-of-change slew penalty *)
    S_diag[2] := 4.20000000; (* BPV rate-of-change slew penalty *)

    P_diag[1] := 46.25000000; (* Terminal level penalty: 2.5 * Q1 *)
    P_diag[2] := 6.25000000;
    P_diag[3] := 21.25000000;
    P_diag[4] := 3.00000000;
    P_diag[5] := 30.00000000;
    P_diag[6] := 8.75000000;
    P_diag[7] := 1.25000000;
    P_diag[8] := 37.50000000;

    (* Initial State Vector Estimates *)
    x_hat[1] := 0.0;
    x_hat[2] := 513.8;
    x_hat[3] := 0.425;
    x_hat[4] := 950.0;
    x_hat[5] := 68.5;
    x_hat[6] := 292.0;
    x_hat[7] := 75.0;
    x_hat[8] := 0.0;

    bInitialized := TRUE;
END_IF;

(* ----------------------------------------------------------------------------- *)
(* FORMULATE PROCESS INPUT VECTOR u[1..5] & MEASUREMENT VECTOR y[1..5]           *)
(* ----------------------------------------------------------------------------- *)
u_vector[1] := fMFRV_PositionDemand;
u_vector[2] := fBPV_PositionDemand;
u_vector[3] := (fAFW_MotorPump1_SpeedDemand + fAFW_MotorPump2_SpeedDemand + fAFW_TurbinePump_GovernorDemand) * 0.33333333;
u_vector[4] := 15.00000000; (* Continuous blowdown base rate: 15.0 kg/s *)
u_vector[5] := fVotedSteamFlow_t_h / 3.60000000; (* Main steam flow in kg/s *)

y_meas[1] := fVotedNarrowRangeLevel_mm;
y_meas[2] := fVotedFeedwaterFlow_t_h / 3.60000000; (* Feedwater flow in kg/s *)
y_meas[3] := fVotedDrumPressure_bar;
y_meas[4] := fVotedColdLegTemp_degC;
y_meas[5] := fVotedSteamFlow_t_h / 3.60000000; (* Steam flow in kg/s *)

(* ----------------------------------------------------------------------------- *)
(* STEP 1: ONE-STEP AHEAD A-PRIORI STATE PROPAGATION: x_pred = A*x_hat + B*u     *)
(* ----------------------------------------------------------------------------- *)
x_pred[1] := (A_Matrix[1, 1] * x_hat[1]) + (A_Matrix[1, 2] * x_hat[2]) + 
             (A_Matrix[1, 3] * x_hat[3]) + (A_Matrix[1, 4] * x_hat[4]) + 
             (A_Matrix[1, 5] * x_hat[5]) + (A_Matrix[1, 6] * x_hat[6]) + 
             (A_Matrix[1, 7] * x_hat[7]) + (A_Matrix[1, 8] * x_hat[8]) + 
             (B_Matrix[1, 1] * u_vector[1]) + (B_Matrix[1, 2] * u_vector[2]) + 
             (B_Matrix[1, 3] * u_vector[3]) + (B_Matrix[1, 4] * u_vector[4]) + 
             (B_Matrix[1, 5] * u_vector[5]);

x_pred[2] := (A_Matrix[2, 1] * x_hat[1]) + (A_Matrix[2, 2] * x_hat[2]) + 
             (A_Matrix[2, 3] * x_hat[3]) + (A_Matrix[2, 4] * x_hat[4]) + 
             (A_Matrix[2, 5] * x_hat[5]) + (A_Matrix[2, 6] * x_hat[6]) + 
             (A_Matrix[2, 7] * x_hat[7]) + (A_Matrix[2, 8] * x_hat[8]) + 
             (B_Matrix[2, 1] * u_vector[1]) + (B_Matrix[2, 2] * u_vector[2]) + 
             (B_Matrix[2, 3] * u_vector[3]) + (B_Matrix[2, 4] * u_vector[4]) + 
             (B_Matrix[2, 5] * u_vector[5]);

x_pred[3] := (A_Matrix[3, 1] * x_hat[1]) + (A_Matrix[3, 2] * x_hat[2]) + 
             (A_Matrix[3, 3] * x_hat[3]) + (A_Matrix[3, 4] * x_hat[4]) + 
             (A_Matrix[3, 5] * x_hat[5]) + (A_Matrix[3, 6] * x_hat[6]) + 
             (A_Matrix[3, 7] * x_hat[7]) + (A_Matrix[3, 8] * x_hat[8]) + 
             (B_Matrix[3, 1] * u_vector[1]) + (B_Matrix[3, 2] * u_vector[2]) + 
             (B_Matrix[3, 3] * u_vector[3]) + (B_Matrix[3, 4] * u_vector[4]) + 
             (B_Matrix[3, 5] * u_vector[5]);

x_pred[4] := (A_Matrix[4, 1] * x_hat[1]) + (A_Matrix[4, 2] * x_hat[2]) + 
             (A_Matrix[4, 3] * x_hat[3]) + (A_Matrix[4, 4] * x_hat[4]) + 
             (A_Matrix[4, 5] * x_hat[5]) + (A_Matrix[4, 6] * x_hat[6]) + 
             (A_Matrix[4, 7] * x_hat[7]) + (A_Matrix[4, 8] * x_hat[8]) + 
             (B_Matrix[4, 1] * u_vector[1]) + (B_Matrix[4, 2] * u_vector[2]) + 
             (B_Matrix[4, 3] * u_vector[3]) + (B_Matrix[4, 4] * u_vector[4]) + 
             (B_Matrix[4, 5] * u_vector[5]);

x_pred[5] := (A_Matrix[5, 1] * x_hat[1]) + (A_Matrix[5, 2] * x_hat[2]) + 
             (A_Matrix[5, 3] * x_hat[3]) + (A_Matrix[5, 4] * x_hat[4]) + 
             (A_Matrix[5, 5] * x_hat[5]) + (A_Matrix[5, 6] * x_hat[6]) + 
             (A_Matrix[5, 7] * x_hat[7]) + (A_Matrix[5, 8] * x_hat[8]) + 
             (B_Matrix[5, 1] * u_vector[1]) + (B_Matrix[5, 2] * u_vector[2]) + 
             (B_Matrix[5, 3] * u_vector[3]) + (B_Matrix[5, 4] * u_vector[4]) + 
             (B_Matrix[5, 5] * u_vector[5]);

x_pred[6] := (A_Matrix[6, 1] * x_hat[1]) + (A_Matrix[6, 2] * x_hat[2]) + 
             (A_Matrix[6, 3] * x_hat[3]) + (A_Matrix[6, 4] * x_hat[4]) + 
             (A_Matrix[6, 5] * x_hat[5]) + (A_Matrix[6, 6] * x_hat[6]) + 
             (A_Matrix[6, 7] * x_hat[7]) + (A_Matrix[6, 8] * x_hat[8]) + 
             (B_Matrix[6, 1] * u_vector[1]) + (B_Matrix[6, 2] * u_vector[2]) + 
             (B_Matrix[6, 3] * u_vector[3]) + (B_Matrix[6, 4] * u_vector[4]) + 
             (B_Matrix[6, 5] * u_vector[5]);

x_pred[7] := (A_Matrix[7, 1] * x_hat[1]) + (A_Matrix[7, 2] * x_hat[2]) + 
             (A_Matrix[7, 3] * x_hat[3]) + (A_Matrix[7, 4] * x_hat[4]) + 
             (A_Matrix[7, 5] * x_hat[5]) + (A_Matrix[7, 6] * x_hat[6]) + 
             (A_Matrix[7, 7] * x_hat[7]) + (A_Matrix[7, 8] * x_hat[8]) + 
             (B_Matrix[7, 1] * u_vector[1]) + (B_Matrix[7, 2] * u_vector[2]) + 
             (B_Matrix[7, 3] * u_vector[3]) + (B_Matrix[7, 4] * u_vector[4]) + 
             (B_Matrix[7, 5] * u_vector[5]);

x_pred[8] := (A_Matrix[8, 1] * x_hat[1]) + (A_Matrix[8, 2] * x_hat[2]) + 
             (A_Matrix[8, 3] * x_hat[3]) + (A_Matrix[8, 4] * x_hat[4]) + 
             (A_Matrix[8, 5] * x_hat[5]) + (A_Matrix[8, 6] * x_hat[6]) + 
             (A_Matrix[8, 7] * x_hat[7]) + (A_Matrix[8, 8] * x_hat[8]) + 
             (B_Matrix[8, 1] * u_vector[1]) + (B_Matrix[8, 2] * u_vector[2]) + 
             (B_Matrix[8, 3] * u_vector[3]) + (B_Matrix[8, 4] * u_vector[4]) + 
             (B_Matrix[8, 5] * u_vector[5]);

(* ----------------------------------------------------------------------------- *)
(* STEP 2: MEASURED OUTPUT PREDICTION: y_pred = C*x_pred + D*u                   *)
(* ----------------------------------------------------------------------------- *)
y_pred[1] := (C_Matrix[1, 1] * x_pred[1]) + (C_Matrix[1, 2] * x_pred[2]) + 
             (C_Matrix[1, 3] * x_pred[3]) + (C_Matrix[1, 4] * x_pred[4]) + 
             (C_Matrix[1, 5] * x_pred[5]) + (C_Matrix[1, 6] * x_pred[6]) + 
             (C_Matrix[1, 7] * x_pred[7]) + (C_Matrix[1, 8] * x_pred[8]) + 
             (D_Matrix[1, 1] * u_vector[1]) + (D_Matrix[1, 2] * u_vector[2]) + 
             (D_Matrix[1, 3] * u_vector[3]) + (D_Matrix[1, 4] * u_vector[4]) + 
             (D_Matrix[1, 5] * u_vector[5]);

y_pred[2] := (C_Matrix[2, 1] * x_pred[1]) + (C_Matrix[2, 2] * x_pred[2]) + 
             (C_Matrix[2, 3] * x_pred[3]) + (C_Matrix[2, 4] * x_pred[4]) + 
             (C_Matrix[2, 5] * x_pred[5]) + (C_Matrix[2, 6] * x_pred[6]) + 
             (C_Matrix[2, 7] * x_pred[7]) + (C_Matrix[2, 8] * x_pred[8]) + 
             (D_Matrix[2, 1] * u_vector[1]) + (D_Matrix[2, 2] * u_vector[2]) + 
             (D_Matrix[2, 3] * u_vector[3]) + (D_Matrix[2, 4] * u_vector[4]) + 
             (D_Matrix[2, 5] * u_vector[5]);

y_pred[3] := (C_Matrix[3, 1] * x_pred[1]) + (C_Matrix[3, 2] * x_pred[2]) + 
             (C_Matrix[3, 3] * x_pred[3]) + (C_Matrix[3, 4] * x_pred[4]) + 
             (C_Matrix[3, 5] * x_pred[5]) + (C_Matrix[3, 6] * x_pred[6]) + 
             (C_Matrix[3, 7] * x_pred[7]) + (C_Matrix[3, 8] * x_pred[8]) + 
             (D_Matrix[3, 1] * u_vector[1]) + (D_Matrix[3, 2] * u_vector[2]) + 
             (D_Matrix[3, 3] * u_vector[3]) + (D_Matrix[3, 4] * u_vector[4]) + 
             (D_Matrix[3, 5] * u_vector[5]);

y_pred[4] := (C_Matrix[4, 1] * x_pred[1]) + (C_Matrix[4, 2] * x_pred[2]) + 
             (C_Matrix[4, 3] * x_pred[3]) + (C_Matrix[4, 4] * x_pred[4]) + 
             (C_Matrix[4, 5] * x_pred[5]) + (C_Matrix[4, 6] * x_pred[6]) + 
             (C_Matrix[4, 7] * x_pred[7]) + (C_Matrix[4, 8] * x_pred[8]) + 
             (D_Matrix[4, 1] * u_vector[1]) + (D_Matrix[4, 2] * u_vector[2]) + 
             (D_Matrix[4, 3] * u_vector[3]) + (D_Matrix[4, 4] * u_vector[4]) + 
             (D_Matrix[4, 5] * u_vector[5]);

y_pred[5] := (C_Matrix[5, 1] * x_pred[1]) + (C_Matrix[5, 2] * x_pred[2]) + 
             (C_Matrix[5, 3] * x_pred[3]) + (C_Matrix[5, 4] * x_pred[4]) + 
             (C_Matrix[5, 5] * x_pred[5]) + (C_Matrix[5, 6] * x_pred[6]) + 
             (C_Matrix[5, 7] * x_pred[7]) + (C_Matrix[5, 8] * x_pred[8]) + 
             (D_Matrix[5, 1] * u_vector[1]) + (D_Matrix[5, 2] * u_vector[2]) + 
             (D_Matrix[5, 3] * u_vector[3]) + (D_Matrix[5, 4] * u_vector[4]) + 
             (D_Matrix[5, 5] * u_vector[5]);

(* ----------------------------------------------------------------------------- *)
(* STEP 3: INNOVATION CALCULATION WITH SPIKE CLAMPING PROTECTIONS                *)
(* ----------------------------------------------------------------------------- *)
innov[1] := y_meas[1] - y_pred[1];
IF innov[1] > 250.0 THEN
    innov[1] := 250.0;
ELSIF innov[1] < -250.0 THEN
    innov[1] := -250.0;
END_IF;

innov[2] := y_meas[2] - y_pred[2];
IF innov[2] > 150.0 THEN
    innov[2] := 150.0;
ELSIF innov[2] < -150.0 THEN
    innov[2] := -150.0;
END_IF;

innov[3] := y_meas[3] - y_pred[3];
IF innov[3] > 8.0 THEN
    innov[3] := 8.0;
ELSIF innov[3] < -8.0 THEN
    innov[3] := -8.0;
END_IF;

innov[4] := y_meas[4] - y_pred[4];
IF innov[4] > 10.0 THEN
    innov[4] := 10.0;
ELSIF innov[4] < -10.0 THEN
    innov[4] := -10.0;
END_IF;

innov[5] := y_meas[5] - y_pred[5];
IF innov[5] > 150.0 THEN
    innov[5] := 150.0;
ELSIF innov[5] < -150.0 THEN
    innov[5] := -150.0;
END_IF;

(* ----------------------------------------------------------------------------- *)
(* STEP 4: KALMAN OBSERVER STATE UPDATE: x_hat = x_pred + L*innov                *)
(* ----------------------------------------------------------------------------- *)
x_hat[1] := x_pred[1] + (L_Matrix[1, 1] * innov[1]) + (L_Matrix[1, 2] * innov[2]) + 
            (L_Matrix[1, 3] * innov[3]) + (L_Matrix[1, 4] * innov[4]) + 
            (L_Matrix[1, 5] * innov[5]);

x_hat[2] := x_pred[2] + (L_Matrix[2, 1] * innov[1]) + (L_Matrix[2, 2] * innov[2]) + 
            (L_Matrix[2, 3] * innov[3]) + (L_Matrix[2, 4] * innov[4]) + 
            (L_Matrix[2, 5] * innov[5]);

x_hat[3] := x_pred[3] + (L_Matrix[3, 1] * innov[1]) + (L_Matrix[3, 2] * innov[2]) + 
            (L_Matrix[3, 3] * innov[3]) + (L_Matrix[3, 4] * innov[4]) + 
            (L_Matrix[3, 5] * innov[5]);

x_hat[4] := x_pred[4] + (L_Matrix[4, 1] * innov[1]) + (L_Matrix[4, 2] * innov[2]) + 
            (L_Matrix[4, 3] * innov[3]) + (L_Matrix[4, 4] * innov[4]) + 
            (L_Matrix[4, 5] * innov[5]);

x_hat[5] := x_pred[5] + (L_Matrix[5, 1] * innov[1]) + (L_Matrix[5, 2] * innov[2]) + 
            (L_Matrix[5, 3] * innov[3]) + (L_Matrix[5, 4] * innov[4]) + 
            (L_Matrix[5, 5] * innov[5]);

x_hat[6] := x_pred[6] + (L_Matrix[6, 1] * innov[1]) + (L_Matrix[6, 2] * innov[2]) + 
            (L_Matrix[6, 3] * innov[3]) + (L_Matrix[6, 4] * innov[4]) + 
            (L_Matrix[6, 5] * innov[5]);

x_hat[7] := x_pred[7] + (L_Matrix[7, 1] * innov[1]) + (L_Matrix[7, 2] * innov[2]) + 
            (L_Matrix[7, 3] * innov[3]) + (L_Matrix[7, 4] * innov[4]) + 
            (L_Matrix[7, 5] * innov[5]);

x_hat[8] := x_pred[8] + (L_Matrix[8, 1] * innov[1]) + (L_Matrix[8, 2] * innov[2]) + 
            (L_Matrix[8, 3] * innov[3]) + (L_Matrix[8, 4] * innov[4]) + 
            (L_Matrix[8, 5] * innov[5]);

(* ----------------------------------------------------------------------------- *)
(* STEP 5: THERMO-HYDRAULIC PHYSICAL CONSTRAINT BOUNDING                         *)
(* ----------------------------------------------------------------------------- *)
(* Void fraction bounded strictly between 0.0 (pure liquid) and 0.85 (annular mist) *)
IF x_hat[3] < 0.00000000 THEN
    x_hat[3] := 0.00000000;
ELSIF x_hat[3] > 0.85000000 THEN
    x_hat[3] := 0.85000000;
END_IF;

(* Downcomer recirculation flow must remain non-negative in normal operation *)
IF x_hat[2] < 0.00000000 THEN
    x_hat[2] := 0.00000000;
END_IF;

(* Valve trim physically constrained [0..100%] *)
IF x_hat[7] < 0.00000000 THEN
    x_hat[7] := 0.00000000;
ELSIF x_hat[7] > 100.00000000 THEN
    x_hat[7] := 100.00000000;
END_IF;

(* Steam drum pressure physically bounded [0..120 bar] *)
IF x_hat[5] < 0.00000000 THEN
    x_hat[5] := 0.00000000;
ELSIF x_hat[5] > 120.00000000 THEN
    x_hat[5] := 120.00000000;
END_IF;

(* RCS cold leg return temperature bounded [150..350 deg C] *)
IF x_hat[6] < 150.00000000 THEN
    x_hat[6] := 150.00000000;
ELSIF x_hat[6] > 350.00000000 THEN
    x_hat[6] := 350.00000000;
END_IF;

(* Assign Cyber-Physical Corrected State Outputs *)
fStateSpaceEstimatedLevel_mm := x_hat[1];
fStateSpaceEstimatedDowncomerFlow_kg_s := x_hat[2];
fStateSpaceEstimatedVoidFraction := x_hat[3];
fStateSpaceEstimatedHeatTransfer_MW := x_hat[4];
fStateSpaceEstimatedPressure_bar := x_hat[5];
fStateSpaceEstimatedColdLegTemp_degC := x_hat[6];
fStateSpaceEstimatedValveTrim_pct := x_hat[7];
fStateSpaceEstimatedNMP_LeadLag_mm := x_hat[8];
""")
    return "".join(lines)

if __name__ == "__main__":
    p2 = get_phase2()
    print(f"Phase 2 generated. Length: {len(p2)} characters.")
