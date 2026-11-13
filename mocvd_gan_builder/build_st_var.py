# mocvd_gan_builder/build_st_var.py

def get_var_declarations():
    return """VAR
    (* === SYSTEM ARCHITECTURE & TIMING REGISTERS === *)
    bInitialized                        : BOOL := FALSE;      (* Cold start initialization complete flag [bool] *)
    udiCycleCounter                     : UDINT := 0;         (* Scan execution cycle counter [counts] *)
    rCycleTime_sec                      : REAL := 0.010;      (* Nominal scan execution period Ts = 10ms [s] *)
    rTotalEpitaxyRunTime_sec            : REAL := 0.0;        (* Total cumulative growth run execution time [s] *)
    rStateTimer_sec                     : REAL := 0.0;        (* Elapsed time in active epitaxial FSM state [s] *)
    rSubStepTimer_sec                   : REAL := 0.0;        (* Elapsed time in active FSM internal sub-step [s] *)
    iCurrentState                       : INT := 0;           (* Internal copy of active 14-stage FSM state [int] *)
    iPreviousState                      : INT := -1;          (* Previous execution state for edge detection [int] *)
    uiSubStepIndex                      : UINT := 0;          (* Active sub-step index within current stage [uint] *)

    (* === GENERAL PURPOSE LOOP COUNTERS & MATHEMATICAL INDICES === *)
    idxRow                              : INT := 1;           (* Matrix row iteration index [int] *)
    idxCol                              : INT := 1;           (* Matrix column iteration index [int] *)
    idxK                                : INT := 1;           (* General purpose inner loop index [int] *)
    idxHorizon                          : INT := 1;           (* MPC receding prediction horizon step index [int] *)
    idxPGD                              : INT := 1;           (* Projected Gradient Descent iteration counter [int] *)
    idxMQW                              : INT := 1;           (* Multi-Quantum Well superlattice loop counter [int] *)

    (* === FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE MATRICES (Ts = 10 ms) === *)
    (* State Vector x: [x1..x8]
       x1: Susceptor Inner Zone Pyrometer Temp [deg C]
       x2: Susceptor Middle Zone Pyrometer Temp [deg C]
       x3: Susceptor Outer Zone Pyrometer Temp [deg C]
       x4: Reactor Chamber Total Static Pressure [mbar]
       x5: Gas-Foil Satellite Wafer Disk Speed [rpm]
       x6: Boundary Layer Ammonia Partial Pressure [mbar]
       x7: Integrated Optical Epilayer Thickness [nm]
       x8: GaN Crystal Growth Rate [um/h] *)
    x_hat                               : ARRAY[1..8] OF REAL; (* Filtered estimated state vector [mixed SI] *)
    x_pred                              : ARRAY[1..8] OF REAL; (* A priori one-step ahead state prediction [mixed SI] *)
    x_corr                              : ARRAY[1..8] OF REAL; (* A posteriori Kalman-corrected state vector [mixed SI] *)

    (* Actuator Vector u: [u1..u6]
       u1: Inner Zone RF Power [0..100 %]
       u2: Middle Zone RF Power [0..100 %]
       u3: Outer Zone RF Power [0..100 %]
       u4: Throttle Butterfly Pressure Valve Opening [0..100 %]
       u5: TMGa Organometallic Bubbler MFC Flow [0..500 sccm]
       u6: Ammonia Precursor MFC Flow [0..50 slm] *)
    u_vec                               : ARRAY[1..6] OF REAL; (* Current actuator control vector [mixed SI] *)
    u_prev                              : ARRAY[1..6] OF REAL; (* Previous cycle actuator vector for slew limiting [mixed SI] *)
    u_min_bound                         : ARRAY[1..6] OF REAL; (* Actuator lower box constraint bounds [mixed SI] *)
    u_max_bound                         : ARRAY[1..6] OF REAL; (* Actuator upper box constraint bounds [mixed SI] *)

    (* Measurement Vector y: [y1..y6]
       y1: Inner Pyrometer Temperature [deg C]
       y2: Middle Pyrometer Temperature [deg C]
       y3: Outer Pyrometer Temperature [deg C]
       y4: Chamber Total Static Pressure [mbar]
       y5: Satellite Wafer Rotation Speed [rpm]
       y6: GaN Growth Rate from Optical Reflectometer [um/h] *)
    y_meas                              : ARRAY[1..6] OF REAL; (* Measured voted process feedback vector [mixed SI] *)
    y_est                               : ARRAY[1..6] OF REAL; (* Observer estimated output vector [mixed SI] *)
    y_target                            : ARRAY[1..6] OF REAL; (* Desired setpoint tracking reference vector [mixed SI] *)
    y_innov                             : ARRAY[1..6] OF REAL; (* Innovation residual vector: (y_meas - y_est) [mixed SI] *)

    (* Explicit Non-Zero State-Space System Matrices *)
    matA                                : ARRAY[1..8, 1..8] OF REAL; (* Discrete state transition matrix (8x8) [dimensionless] *)
    matB                                : ARRAY[1..8, 1..6] OF REAL; (* Control input coupling matrix (8x6) [dimensionless] *)
    matC                                : ARRAY[1..6, 1..8] OF REAL; (* Measurement output matrix (6x8) [dimensionless] *)
    matD                                : ARRAY[1..6, 1..6] OF REAL; (* Direct feedthrough matrix (6x6) [dimensionless] *)
    matL                                : ARRAY[1..8, 1..6] OF REAL; (* Steady-state Kalman-Luenberger innovation gain (8x6) [dimensionless] *)

    (* === RADIATIVE COUPLING & DYNAMIC THERMAL DECOUPLING MATRICES === *)
    matF_rad                            : ARRAY[1..3, 1..3] OF REAL; (* Direct Stefan-Boltzmann view factor coupling matrix [dimensionless] *)
    matK_decouple                       : ARRAY[1..3, 1..3] OF REAL; (* Dynamic decoupling matrix (F_rad^-1) [dimensionless] *)
    rRaw_RF_Inner                       : REAL := 0.0;        (* Raw MPC Inner Zone RF Power Command [0..100 %] *)
    rRaw_RF_Mid                         : REAL := 0.0;        (* Raw MPC Middle Zone RF Power Command [0..100 %] *)
    rRaw_RF_Outer                       : REAL := 0.0;        (* Raw MPC Outer Zone RF Power Command [0..100 %] *)
    rDecoupled_RF_Inner                 : REAL := 0.0;        (* Dynamically decoupled Inner RF Power Command [0..100 %] *)
    rDecoupled_RF_Mid                   : REAL := 0.0;        (* Dynamically decoupled Middle RF Power Command [0..100 %] *)
    rDecoupled_RF_Outer                 : REAL := 0.0;        (* Dynamically decoupled Outer RF Power Command [0..100 %] *)
    rSlewLimit_RF_Per_Cycle             : REAL := 0.025;      (* Max allowed RF power step per 10ms cycle (2.5 %/s) [%] *)

    (* === MODEL PREDICTIVE CONTROL (MPC) HORIZON & COST MATRICES === *)
    (* Receding Prediction Horizon N = 5, 6 Unrolled Iterations of Projected Gradient Descent (PGD) *)
    matQ_cost                           : ARRAY[1..6] OF REAL; (* Quadratic state tracking error penalties [weights] *)
    matR_cost                           : ARRAY[1..6] OF REAL; (* Control effort expenditure penalties [weights] *)
    matS_slew_cost                      : ARRAY[1..6] OF REAL; (* Actuator slew-rate rate-of-change penalties [weights] *)
    matP_terminal                       : ARRAY[1..8] OF REAL; (* Terminal state penalty diagonal weights [weights] *)

    (* Trajectory Prediction Arrays over Horizon N = 5 *)
    x_traj                              : ARRAY[1..5, 1..8] OF REAL; (* Predicted state trajectory across horizon [mixed SI] *)
    u_traj                              : ARRAY[1..5, 1..6] OF REAL; (* Actuator control trajectory across horizon [mixed SI] *)
    grad_u                              : ARRAY[1..5, 1..6] OF REAL; (* Computed analytical gradient dJ/du [weights/SI] *)
    rAlpha_PGD                          : REAL := 0.0035;     (* Projected Gradient Descent optimization step size [dimensionless] *)
    rCost_J                             : REAL := 0.0;        (* Cumulative quadratic scalar cost functional J [dimensionless] *)
    rTerminal_Cost                      : REAL := 0.0;        (* Terminal cost component J_terminal [dimensionless] *)

    (* === 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) REGISTERS & DISCREPANCY TIMERS === *)
    (* Discrepancy accumulation timers (threshold 100 ms = 0.10 s) *)
    rTimer_TMR_TT101_Discrepancy        : REAL := 0.0;        (* Inner Pyrometer discrepancy accumulation timer [s] *)
    rTimer_TMR_TT201_Discrepancy        : REAL := 0.0;        (* Middle Pyrometer discrepancy accumulation timer [s] *)
    rTimer_TMR_TT301_Discrepancy        : REAL := 0.0;        (* Outer Pyrometer discrepancy accumulation timer [s] *)
    rTimer_TMR_PT401_Discrepancy        : REAL := 0.0;        (* Chamber Pressure discrepancy accumulation timer [s] *)
    rTimer_TMR_OPT501_Discrepancy       : REAL := 0.0;        (* Laser Reflectometer discrepancy accumulation timer [s] *)

    (* Discrepancy Threshold Constants *)
    rTol_TMR_Pyro_degC                  : REAL := 8.5;        (* Max allowed pyrometer inter-channel deviation [deg C] *)
    rTol_TMR_Press_mbar                 : REAL := 4.5;        (* Max allowed pressure inter-channel deviation [mbar] *)
    rTol_TMR_Refl_counts                : REAL := 65.0;       (* Max allowed reflectometer inter-channel deviation [counts] *)

    (* TMR Sensor Channel Fault Status Bits *)
    bFault_TT101A                       : BOOL := FALSE;      (* Pyrometer 101A out of tolerance or degraded [bool] *)
    bFault_TT101B                       : BOOL := FALSE;      (* Pyrometer 101B out of tolerance or degraded [bool] *)
    bFault_TT101C                       : BOOL := FALSE;      (* Pyrometer 101C out of tolerance or degraded [bool] *)
    bFault_TT201A                       : BOOL := FALSE;      (* Pyrometer 201A out of tolerance or degraded [bool] *)
    bFault_TT201B                       : BOOL := FALSE;      (* Pyrometer 201B out of tolerance or degraded [bool] *)
    bFault_TT201C                       : BOOL := FALSE;      (* Pyrometer 201C out of tolerance or degraded [bool] *)
    bFault_TT301A                       : BOOL := FALSE;      (* Pyrometer 301A out of tolerance or degraded [bool] *)
    bFault_TT301B                       : BOOL := FALSE;      (* Pyrometer 301B out of tolerance or degraded [bool] *)
    bFault_TT301C                       : BOOL := FALSE;      (* Pyrometer 301C out of tolerance or degraded [bool] *)
    bFault_PT401A                       : BOOL := FALSE;      (* Manometer 401A out of tolerance or degraded [bool] *)
    bFault_PT401B                       : BOOL := FALSE;      (* Manometer 401B out of tolerance or degraded [bool] *)
    bFault_PT401C                       : BOOL := FALSE;      (* Manometer 401C out of tolerance or degraded [bool] *)
    bFault_OPT501A                      : BOOL := FALSE;      (* Reflectometer 501A out of tolerance or degraded [bool] *)
    bFault_OPT501B                      : BOOL := FALSE;      (* Reflectometer 501B out of tolerance or degraded [bool] *)
    bFault_OPT501C                      : BOOL := FALSE;      (* Reflectometer 501C out of tolerance or degraded [bool] *)

    (* TMR Degraded Mode & Quorum Loss Flags *)
    bTMR_Degraded_TT101                 : BOOL := FALSE;      (* Inner Pyrometer triplet operating in degraded 2oo2/1oo1 [bool] *)
    bTMR_Degraded_TT201                 : BOOL := FALSE;      (* Middle Pyrometer triplet operating in degraded 2oo2/1oo1 [bool] *)
    bTMR_Degraded_TT301                 : BOOL := FALSE;      (* Outer Pyrometer triplet operating in degraded 2oo2/1oo1 [bool] *)
    bTMR_Degraded_PT401                 : BOOL := FALSE;      (* Chamber Manometer triplet operating in degraded 2oo2/1oo1 [bool] *)
    bTMR_Degraded_OPT501                : BOOL := FALSE;      (* Reflectometer triplet operating in degraded 2oo2/1oo1 [bool] *)
    bTMR_QuorumLoss_Trip                : BOOL := FALSE;      (* Critical loss of sensor voting quorum trip flag [bool] *)

    (* === CHEMICAL KINETICS & IN-SITU REFLECTOMETRY REGISTERS === *)
    rRefl_Peak_Counts                   : REAL := 1200.0;     (* Peak intensity of Fabry-Perot interference fringe [counts] *)
    rRefl_Valley_Counts                 : REAL := 800.0;      (* Valley intensity of Fabry-Perot interference fringe [counts] *)
    rRefl_Period_sec                    : REAL := 180.0;      (* Current oscillation period of Fabry-Perot fringe [s] *)
    rRefl_LastPeakTime_sec              : REAL := 0.0;        (* Timestamp of last observed interference peak [s] *)
    rRefl_LaserWavelength_nm            : REAL := 405.0;      (* Blue laser diode optical wavelength lambda [nm] *)
    rRefractiveIndex_GaN                : REAL := 2.52;       (* Optical refractive index of GaN crystal at 1050 deg C [dimensionless] *)
    rArrhenius_Ea_J_mol                 : REAL := 125000.0;   (* GaN pyrolysis activation energy Ea [J/mol] *)
    rUniversalGasConst_R                : REAL := 8.31446;    (* Universal gas constant R [J/(mol*K)] *)
    rArrhenius_K0                       : REAL := 1.85e5;     (* Pre-exponential rate coefficient [um*K/(h*mbar)] *)
    rGaN_MassTransport_DiffCoeff        : REAL := 2.45e-4;    (* Mass transport diffusion constant in H2 boundary layer [m^2/s] *)

    (* === SUB-25ms FAST PYROPHORIC GAS DOUBLE-BLOCK-AND-BLEED REGISTERS === *)
    rFastInterlockTripTimer_sec         : REAL := 0.0;        (* Elapsed time since fast safety trip trigger [s] *)
    bFastDoubleBlockBleed_Activated     : BOOL := FALSE;      (* High-speed double-block-and-bleed valve dump fired [bool] *)
    bPyrophoricLeakAlert                : BOOL := FALSE;      (* Toxic sniffer hydride/pyrophoric leak detected [bool] *)
    bScrubberExhaustInterlockOk         : BOOL := TRUE;       (* Thermal scrubber & water recirc interlock status [bool] *)
    bThyristorCrowbarFired              : BOOL := FALSE;      (* Sub-2ms thyristor crowbar gate trigger latched [bool] *)

    (* === ISA-18.2 MULTI-TIER PROCESS ALARM THRESHOLDS & HYSTERESIS === *)
    (* High-High, High, Low, Low-Low Trip Thresholds *)
    rTrip_Temp_HH_degC                  : REAL := 1220.0;     (* Susceptor Thermal Overheat Critical Trip (HH) [deg C] *)
    rTrip_Temp_H_degC                   : REAL := 1180.0;     (* Susceptor Thermal High Process Warning (H) [deg C] *)
    rTrip_Temp_L_degC                   : REAL := 350.0;      (* Susceptor Thermal Low Process Warning (L) [deg C] *)
    rTrip_Temp_LL_degC                  : REAL := 250.0;      (* Susceptor Thermal Underheat Critical Trip (LL) [deg C] *)
    rHyst_Temp_degC                     : REAL := 5.0;        (* Thermal Alarm Clearance Deadband Hysteresis [deg C] *)

    rTrip_Press_HH_mbar                 : REAL := 1025.0;     (* Chamber Overpressure Critical Blowout Trip (HH) [mbar] *)
    rTrip_Press_H_mbar                  : REAL := 950.0;      (* Chamber Pressure High Warning (H) [mbar] *)
    rTrip_Press_L_mbar                  : REAL := 25.0;       (* Chamber Pressure Low Warning (L) [mbar] *)
    rTrip_Press_LL_mbar                 : REAL := 8.0;        (* Chamber Vacuum Underpressure Critical Trip (LL) [mbar] *)
    rHyst_Press_mbar                    : REAL := 2.5;        (* Chamber Pressure Clearance Deadband Hysteresis [mbar] *)

    rTrip_Rotation_LL_rpm               : REAL := 15.0;       (* Minimum Wafer Planetary Rotation Stoppage Trip (LL) [rpm] *)
    rHyst_Rotation_rpm                  : REAL := 3.0;        (* Rotation Alarm Clearance Deadband Hysteresis [rpm] *)

    rTrip_ToxicLeak_HH_ppm              : REAL := 5.0;        (* Toxic Hydride / Pyrophoric Cabinet Leak Trip (HH) [ppm] *)
    rTrip_ToxicLeak_H_ppm               : REAL := 1.5;        (* Toxic Hydride / Pyrophoric Cabinet Warning (H) [ppm] *)
    rHyst_ToxicLeak_ppm                 : REAL := 0.4;        (* Toxic Sniffer Clearance Deadband Hysteresis [ppm] *)

    (* ISA-18.2 Latched Alarm Diagnostic Bits *)
    bAlarm_TempInner_HH                 : BOOL := FALSE;      (* Inner Susceptor Temperature High-High Trip [bool] *)
    bAlarm_TempInner_H                  : BOOL := FALSE;      (* Inner Susceptor Temperature High Warning [bool] *)
    bAlarm_TempInner_L                  : BOOL := FALSE;      (* Inner Susceptor Temperature Low Warning [bool] *)
    bAlarm_TempInner_LL                 : BOOL := FALSE;      (* Inner Susceptor Temperature Low-Low Trip [bool] *)
    bAlarm_TempMid_HH                   : BOOL := FALSE;      (* Middle Susceptor Temperature High-High Trip [bool] *)
    bAlarm_TempMid_H                    : BOOL := FALSE;      (* Middle Susceptor Temperature High Warning [bool] *)
    bAlarm_TempOuter_HH                 : BOOL := FALSE;      (* Outer Susceptor Temperature High-High Trip [bool] *)
    bAlarm_TempOuter_H                  : BOOL := FALSE;      (* Outer Susceptor Temperature High Warning [bool] *)
    bAlarm_ThermalGradient_High         : BOOL := FALSE;      (* Cross-zone thermal gradient exceeds 5.0 deg C warning [bool] *)
    bAlarm_ChamberPress_HH              : BOOL := FALSE;      (* Chamber Static Pressure High-High Trip [bool] *)
    bAlarm_ChamberPress_H               : BOOL := FALSE;      (* Chamber Static Pressure High Warning [bool] *)
    bAlarm_ChamberPress_L               : BOOL := FALSE;      (* Chamber Static Pressure Low Warning [bool] *)
    bAlarm_ChamberPress_LL              : BOOL := FALSE;      (* Chamber Static Pressure Low-Low Trip [bool] *)
    bAlarm_SusceptorRotation_LL         : BOOL := FALSE;      (* Susceptor Planetary Rotation Loss Trip [bool] *)
    bAlarm_GasFoilStagnation            : BOOL := FALSE;      (* Satellite Wafer Gas-Foil Levitating Stagnation Warning [bool] *)
    bAlarm_ScrubberFailure              : BOOL := FALSE;      (* Burn-Box Scrubber or Water Recirculation Trip [bool] *)
    bAlarm_ToxicGasLeak_HH              : BOOL := FALSE;      (* Gas Cabinet Pyrophoric / Hydride Leak Trip [bool] *)
    bAlarm_TMR_MajorDiscrepancy         : BOOL := FALSE;      (* TMR Multi-channel Discrepancy Failure Warning [bool] *)
    bAlarm_EStopAsserted                : BOOL := FALSE;      (* Emergency Stop Loop Interruption Trip [bool] *)

    (* ISA-18.2 Alarm Delay Timers *)
    rTimer_Alarm_TempInner_sec          : REAL := 0.0;        (* Temperature alarm qualification timer [s] *)
    rTimer_Alarm_ChamberPress_sec       : REAL := 0.0;        (* Pressure alarm qualification timer [s] *)
    rTimer_Alarm_Rotation_sec           : REAL := 0.0;        (* Rotation alarm qualification timer [s] *)
    rTimer_Alarm_ToxicLeak_sec          : REAL := 0.0;        (* Toxic gas qualification timer [s] *)

    (* First-Out Latching Register *)
    bFirstOutLatched                    : BOOL := FALSE;      (* First-out latch lock flag [bool] *)
END_VAR
"""
