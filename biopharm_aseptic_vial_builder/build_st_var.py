# biopharm_aseptic_vial_builder/build_st_var.py

def get_var_declarations():
    return """VAR
    (* ===================================================================================== *)
    (* 1. DISCRETE STATE-SPACE CYBER-PHYSICAL MODEL MATRICES & VECTORS (Ts = 5 ms)           *)
    (* ===================================================================================== *)
    mA                              : ARRAY[1..12, 1..12] OF REAL;  (* System dynamic matrix A [12x12] *)
    mB                              : ARRAY[1..12, 1..8] OF REAL;   (* Control input matrix B [12x8] *)
    mEw                             : ARRAY[1..12, 1..4] OF REAL;   (* Disturbance coupling matrix Ew [12x4] *)
    mC                              : ARRAY[1..8, 1..12] OF REAL;   (* Measurement output matrix C [8x12] *)
    mD                              : ARRAY[1..8, 1..8] OF REAL;    (* Direct feedthrough matrix D [8x8] *)
    mK                              : ARRAY[1..12, 1..8] OF REAL;   (* Steady-state Kalman observer gain K [12x8] *)

    vecX                            : ARRAY[1..12] OF REAL;         (* True plant physical state vector *)
    vecX_hat                        : ARRAY[1..12] OF REAL;         (* Estimated Kalman state vector *)
    vecX_next                       : ARRAY[1..12] OF REAL;         (* Predicted next-step state vector *)
    vecU                            : ARRAY[1..8] OF REAL;          (* Plant manipulated input vector *)
    vecW                            : ARRAY[1..4] OF REAL;          (* Process disturbance vector *)
    vecY_meas                       : ARRAY[1..8] OF REAL;          (* Measured output vector from 2oo3 TMR *)
    vecY_hat                        : ARRAY[1..8] OF REAL;          (* Model predicted output vector *)
    vecY_ref                        : ARRAY[1..8] OF REAL;          (* Recipe setpoint tracking trajectory *)
    vecInnov                        : ARRAY[1..8] OF REAL;          (* Kalman observer innovation residual *)
    bMatricesInitialized            : BOOL := FALSE;                (* Cold start matrix initialization flag *)

    (* ===================================================================================== *)
    (* 2. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & PGD OPTIMIZATION VARIABLES        *)
    (* ===================================================================================== *)
    mQ                              : ARRAY[1..8, 1..8] OF REAL;    (* MPC output tracking error penalty [8x8] *)
    mR                              : ARRAY[1..8, 1..8] OF REAL;    (* MPC control effort penalty [8x8] *)
    mS                              : ARRAY[1..8, 1..8] OF REAL;    (* MPC slew rate / delta-u penalty [8x8] *)
    mP                              : ARRAY[1..12, 1..12] OF REAL;  (* MPC terminal state penalty [12x12] *)

    vecU_opt                        : ARRAY[1..8] OF REAL;          (* PGD optimized control vector *)
    vecU_prev                       : ARRAY[1..8] OF REAL;          (* Prior scan control input vector *)
    vecGrad                         : ARRAY[1..8] OF REAL;          (* Quadratic cost gradient vector *)
    vecPredX                        : ARRAY[1..6, 1..12] OF REAL;   (* 6-step prediction horizon states *)
    vecPredY                        : ARRAY[1..6, 1..8] OF REAL;    (* 6-step prediction horizon outputs *)
    rStepAlpha                      : REAL := 0.045;                (* PGD gradient descent step size *)
    rSlewLimit_PctPerScan           : REAL := 6.5;                  (* Actuator slew rate clamp [%/scan] *)
    rCostTotal                      : REAL := 0.0;                  (* Unrolled horizon quadratic cost *)

    (* ===================================================================================== *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES                      *)
    (* ===================================================================================== *)
    (* --- Bank 1: Tare Load Cells [mg] --- *)
    rTMR_Tare_Mid                   : REAL := 0.0;
    rTMR_Tare_Voted                 : REAL := 0.0;
    rTMR_Tare_DiffAB                : REAL := 0.0;
    rTMR_Tare_DiffBC                : REAL := 0.0;
    rTMR_Tare_DiffCA                : REAL := 0.0;
    rTMR_Tare_TimerA_ms             : REAL := 0.0;
    rTMR_Tare_TimerB_ms             : REAL := 0.0;
    rTMR_Tare_TimerC_ms             : REAL := 0.0;
    bTMR_Tare_FaultA                : BOOL := FALSE;
    bTMR_Tare_FaultB                : BOOL := FALSE;
    bTMR_Tare_FaultC                : BOOL := FALSE;
    bTMR_Tare_Degraded_1oo2         : BOOL := FALSE;
    bTMR_Tare_Degraded_1oo1         : BOOL := FALSE;
    bTMR_Tare_BankFailure           : BOOL := FALSE;

    (* --- Bank 2: Gross Load Cells [mg] --- *)
    rTMR_Gross_Mid                  : REAL := 0.0;
    rTMR_Gross_Voted                : REAL := 0.0;
    rTMR_Gross_DiffAB               : REAL := 0.0;
    rTMR_Gross_DiffBC               : REAL := 0.0;
    rTMR_Gross_DiffCA               : REAL := 0.0;
    rTMR_Gross_TimerA_ms            : REAL := 0.0;
    rTMR_Gross_TimerB_ms            : REAL := 0.0;
    rTMR_Gross_TimerC_ms            : REAL := 0.0;
    bTMR_Gross_FaultA               : BOOL := FALSE;
    bTMR_Gross_FaultB               : BOOL := FALSE;
    bTMR_Gross_FaultC               : BOOL := FALSE;
    bTMR_Gross_Degraded_1oo2        : BOOL := FALSE;
    bTMR_Gross_Degraded_1oo1        : BOOL := FALSE;
    bTMR_Gross_BankFailure          : BOOL := FALSE;

    (* --- Bank 3: Isolator Differential Pressure [Pa] --- *)
    rTMR_IsoPress_Mid               : REAL := 45.0;
    rTMR_IsoPress_Voted             : REAL := 45.0;
    rTMR_IsoPress_DiffAB            : REAL := 0.0;
    rTMR_IsoPress_DiffBC            : REAL := 0.0;
    rTMR_IsoPress_DiffCA            : REAL := 0.0;
    rTMR_IsoPress_TimerA_ms         : REAL := 0.0;
    rTMR_IsoPress_TimerB_ms         : REAL := 0.0;
    rTMR_IsoPress_TimerC_ms         : REAL := 0.0;
    bTMR_IsoPress_FaultA            : BOOL := FALSE;
    bTMR_IsoPress_FaultB            : BOOL := FALSE;
    bTMR_IsoPress_FaultC            : BOOL := FALSE;
    bTMR_IsoPress_Degraded_1oo2     : BOOL := FALSE;
    bTMR_IsoPress_Degraded_1oo1     : BOOL := FALSE;
    bTMR_IsoPress_BankFailure       : BOOL := FALSE;

    (* --- Bank 4: VHP H2O2 Vapor Concentration [ppm] --- *)
    rTMR_VHP_Mid                    : REAL := 0.0;
    rTMR_VHP_Voted                  : REAL := 0.0;
    rTMR_VHP_DiffAB                 : REAL := 0.0;
    rTMR_VHP_DiffBC                 : REAL := 0.0;
    rTMR_VHP_DiffCA                 : REAL := 0.0;
    rTMR_VHP_TimerA_ms              : REAL := 0.0;
    rTMR_VHP_TimerB_ms              : REAL := 0.0;
    rTMR_VHP_TimerC_ms              : REAL := 0.0;
    bTMR_VHP_FaultA                 : BOOL := FALSE;
    bTMR_VHP_FaultB                 : BOOL := FALSE;
    bTMR_VHP_FaultC                 : BOOL := FALSE;
    bTMR_VHP_Degraded_1oo2          : BOOL := FALSE;
    bTMR_VHP_Degraded_1oo1          : BOOL := FALSE;
    bTMR_VHP_BankFailure            : BOOL := FALSE;

    (* --- Bank 5: Glove Port Pressure Decay [Pa] --- *)
    rTMR_Glove_Mid                  : REAL := 500.0;
    rTMR_Glove_Voted                : REAL := 500.0;
    rTMR_Glove_DiffAB               : REAL := 0.0;
    rTMR_Glove_DiffBC               : REAL := 0.0;
    rTMR_Glove_DiffCA               : REAL := 0.0;
    rTMR_Glove_TimerA_ms            : REAL := 0.0;
    rTMR_Glove_TimerB_ms            : REAL := 0.0;
    rTMR_Glove_TimerC_ms            : REAL := 0.0;
    bTMR_Glove_FaultA               : BOOL := FALSE;
    bTMR_Glove_FaultB               : BOOL := FALSE;
    bTMR_Glove_FaultC               : BOOL := FALSE;
    bTMR_Glove_Degraded_1oo2        : BOOL := FALSE;
    bTMR_Glove_Degraded_1oo1        : BOOL := FALSE;
    bTMR_Glove_BankFailure          : BOOL := FALSE;

    (* --- Bank 6: Grade A Vertical Laminar Airflow [m/s] --- *)
    rTMR_Laminar_Mid                : REAL := 0.45;
    rTMR_Laminar_Voted              : REAL := 0.45;
    rTMR_Laminar_DiffAB             : REAL := 0.0;
    rTMR_Laminar_DiffBC             : REAL := 0.0;
    rTMR_Laminar_DiffCA             : REAL := 0.0;
    rTMR_Laminar_TimerA_ms          : REAL := 0.0;
    rTMR_Laminar_TimerB_ms          : REAL := 0.0;
    rTMR_Laminar_TimerC_ms          : REAL := 0.0;
    bTMR_Laminar_FaultA             : BOOL := FALSE;
    bTMR_Laminar_FaultB             : BOOL := FALSE;
    bTMR_Laminar_FaultC             : BOOL := FALSE;
    bTMR_Laminar_Degraded_1oo2      : BOOL := FALSE;
    bTMR_Laminar_Degraded_1oo1      : BOOL := FALSE;
    bTMR_Laminar_BankFailure        : BOOL := FALSE;

    (* --- Bank 7: Capper Dynamic Sealing Force [N] --- *)
    rTMR_Crimp_Mid                  : REAL := 145.0;
    rTMR_Crimp_Voted                : REAL := 145.0;
    rTMR_Crimp_DiffAB               : REAL := 0.0;
    rTMR_Crimp_DiffBC               : REAL := 0.0;
    rTMR_Crimp_DiffCA               : REAL := 0.0;
    rTMR_Crimp_TimerA_ms            : REAL := 0.0;
    rTMR_Crimp_TimerB_ms            : REAL := 0.0;
    rTMR_Crimp_TimerC_ms            : REAL := 0.0;
    bTMR_Crimp_FaultA               : BOOL := FALSE;
    bTMR_Crimp_FaultB               : BOOL := FALSE;
    bTMR_Crimp_FaultC               : BOOL := FALSE;
    bTMR_Crimp_Degraded_1oo2        : BOOL := FALSE;
    bTMR_Crimp_Degraded_1oo1        : BOOL := FALSE;
    bTMR_Crimp_BankFailure          : BOOL := FALSE;

    (* Discrepancy Threshold Constants *)
    rTMR_DiscrepancyLimit_ms        : REAL := 150.0;
    rTol_Tare_mg                    : REAL := 18.0;
    rTol_Gross_mg                   : REAL := 10.0;
    rTol_IsoDiffPress_Pa            : REAL := 4.5;
    rTol_VHP_ppm                    : REAL := 25.0;
    rTol_GlovePress_Pa              : REAL := 8.0;
    rTol_LaminarAir_mps             : REAL := 0.05;
    rTol_CrimpForce_N               : REAL := 8.0;

    (* ===================================================================================== *)
    (* 4. 10-HEAD CERAMIC ROTARY VALVELESS PISTON PUMPS & DIVING NEEDLE ACTUATORS            *)
    (* ===================================================================================== *)
    aPistonRotaryAngle_deg          : ARRAY[1..10] OF REAL;         (* Head rotary ceramic valve angle [0-360 deg] *)
    aPistonLinearStroke_mm          : ARRAY[1..10] OF REAL;         (* Head linear piston displacement [mm] *)
    aPistonVolumeDosed_ml           : ARRAY[1..10] OF REAL;         (* Head calculated delivered volume [mL] *)
    aTrimIntegral_ml                : ARRAY[1..10] OF REAL;         (* Head closed-loop micro-trim integrator [mL] *)
    aMicroTrimOutput_Pct            : ARRAY[1..10] OF REAL;         (* Head fine peristaltic trim stroke [%] *)
    aNeedleZ_mm                     : ARRAY[1..10] OF REAL;         (* Head diving needle vertical position [mm] *)
    aNeedleV_mps                    : ARRAY[1..10] OF REAL;         (* Head diving needle velocity [m/s] *)
    aNeedleClearance_mm             : ARRAY[1..10] OF REAL;         (* Head needle tip to liquid meniscus gap [mm] *)

    rCeramicPistonDiameter_mm       : REAL := 14.00;                (* Ceramic piston inner chamber diameter [mm] *)
    rPistonMaxStroke_mm             : REAL := 42.00;                (* Maximum linear stroke travel [mm] *)
    rSuckbackVolume_ml              : REAL := 0.050;                (* Anti-drip reverse aspiration volume [mL] *)
    rSuckbackStroke_mm              : REAL := 0.325;                (* Reverse suckback linear displacement [mm] *)
    rTrimKp                         : REAL := 0.750;                (* Micro-volume closed-loop proportional gain *)
    rTrimKi                         : REAL := 0.035;                (* Micro-volume closed-loop integral gain *)

    (* ===================================================================================== *)
    (* 5. DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM) VARIABLES                        *)
    (* ===================================================================================== *)
    nFSM_State                      : INT := 0;                     (* Active production FSM sequence index *)
    nFSM_PrevState                  : INT := -1;                    (* Prior scan FSM sequence index *)
    rFSM_StateTimer_s               : REAL := 0.0;                  (* State elapsed dwelling timer [s] *)
    bStateEntryTrigger              : BOOL := TRUE;                 (* One-shot state activation strobe *)

    (* FSM State Index Constants *)
    STATE_0_PRESSURE_DECAY_LEAK_TEST: INT := 0;                     (* Isolator chamber pressure decay leak test *)
    STATE_1_VHP_CONDITIONING        : INT := 1;                     (* Temperature/humidity conditioning *)
    STATE_2_H2O2_BIO_DECON_DWELL    : INT := 2;                     (* High concentration VHP gas dwell *)
    STATE_3_CATALYTIC_AERATION      : INT := 3;                     (* Fresh air purge through catalytic converter *)
    STATE_4_GRADE_A_LAMINAR_AIR_LOCK: INT := 4;                     (* Unidirectional laminar flow stabilization *)
    STATE_5_VIAL_INFEED_SYNC        : INT := 5;                     (* Depyrogenation tunnel scroll screw sync *)
    STATE_6_INLINE_100PCT_TARE_WEIGH: INT := 6;                     (* Dual-pan EMFR empty vial checkweighing *)
    STATE_7_SYNCHRONOUS_DOSE_NEEDLE : INT := 7;                     (* Rotary ceramic piston dosing & needle dive *)
    STATE_8_RETRACT_ANTI_DRIP_SUCK  : INT := 8;                     (* Anti-drip reverse aspiration & retraction *)
    STATE_9_INLINE_100PCT_GROSS_WEIGH:INT := 9;                     (* Filled vial checkweighing & trim feedback *)
    STATE_10_VACUUM_STOPPER_INSERT  : INT := 10;                    (* 24-pocket rotary vacuum stopper insertion *)
    STATE_11_SERVO_CRIMP_INTEGRITY  : INT := 11;                    (* 16-head rotary aluminum cap crimping *)
    STATE_12_OUTFEED_DEFECT_EJECT   : INT := 12;                    (* High-speed pneumatic 3-bin defect dispatch *)
    STATE_13_BARRIER_BREACH_LOCKDOWN: INT := 13;                    (* SIL 3 Grade A barrier emergency containment *)

    (* ===================================================================================== *)
    (* 6. VHP STERILIZATION & ISOLATOR AERODYNAMICS SUBSYSTEM                                *)
    (* ===================================================================================== *)
    rLeakTestStartPress_Pa          : REAL := 0.0;                  (* Starting chamber pressure for decay test [Pa] *)
    rLeakTestDecay_Pa_min           : REAL := 0.0;                  (* Derived pressure leak rate [Pa/min] *)
    bLeakTestPassed                 : BOOL := FALSE;                (* Chamber leak test acceptance verification *)
    bVHP_DeconCompleted             : BOOL := FALSE;                (* Bio-decontamination dwell validated *)
    bAerationCompleted              : BOOL := FALSE;                (* Aeration phase validated < threshold *)
    rVHP_InjPumpSpeed_Pct           : REAL := 0.0;                  (* Flash vaporizer liquid injection speed [%] *)
    rIsolatorTemp_degC              : REAL := 22.0;                 (* Current internal isolator temperature [deg C] *)
    rIsolatorRH_Pct                 : REAL := 45.0;                 (* Current internal isolator humidity [%] *)

    (* ===================================================================================== *)
    (* 7. EMFR CHECKWEIGHING DYNAMICS & STATISTICAL PROCESS CONTROL (SPC)                    *)
    (* ===================================================================================== *)
    rEMFR_FilterAlpha               : REAL := 0.30;                 (* First-order low-pass filter coefficient *)
    rFilteredTare_mg                : REAL := 0.0;                  (* Smoothed EMFR tare reading [mg] *)
    rFilteredGross_mg               : REAL := 0.0;                  (* Smoothed EMFR gross reading [mg] *)
    rDerivedNetDose_ml              : REAL := 0.0;                  (* Instantaneous measured dose [mL] *)

    aDosingHist_ml                  : ARRAY[1..30] OF REAL;         (* Circular buffer for last 30 vial doses [mL] *)
    aTareHist_mg                    : ARRAY[1..30] OF REAL;         (* Circular buffer for last 30 tare weights [mg] *)
    aGrossHist_mg                   : ARRAY[1..30] OF REAL;         (* Circular buffer for last 30 gross weights [mg] *)
    aCrimpHist_N                    : ARRAY[1..30] OF REAL;         (* Circular buffer for last 30 crimp forces [N] *)
    nHistIdx                        : INT := 1;                     (* Circular buffer ring pointer [1..30] *)
    nHistCount                      : INT := 0;                     (* Populated buffer entry counter [0..30] *)

    rMovingSum_ml                   : REAL := 0.0;                  (* Dosing volume accumulator sum [mL] *)
    rMovingSumSquares_ml            : REAL := 0.0;                  (* Dosing volume sum of squares accumulator *)
    rDosingVariance_ml2             : REAL := 0.0;                  (* Sample variance of fill volume [mL^2] *)
    rUSL_Dose_ml                    : REAL := 10.025;               (* Upper specification limit for volume [mL] *)
    rLSL_Dose_ml                    : REAL := 9.975;                (* Lower specification limit for volume [mL] *)

    (* ===================================================================================== *)
    (* 8. ISA-18.2 ALARM ENGINE TRIP POINTS, DEADBANDS & ACCUMULATORS                         *)
    (* ===================================================================================== *)
    rIsoPress_TripHH_Pa             : REAL := 65.0;                 (* Isolator over-pressure critical trip [Pa] *)
    rIsoPress_TripH_Pa              : REAL := 55.0;                 (* Isolator high pressure warning [Pa] *)
    rIsoPress_TripL_Pa              : REAL := 35.0;                 (* Isolator low pressure warning [Pa] *)
    rIsoPress_TripLL_Pa             : REAL := 20.0;                 (* Isolator loss of containment trip [Pa] *)
    rIsoPress_Deadband_Pa           : REAL := 2.5;                  (* Hysteresis deadband for pressure alarms [Pa] *)

    rLaminar_TripLL_mps             : REAL := 0.36;                 (* Unidirectional airflow LL breach [m/s] *)
    rLaminar_TripHH_mps             : REAL := 0.54;                 (* Unidirectional airflow turbulence HH [m/s] *)
    rLaminar_Deadband_mps           : REAL := 0.02;                 (* Hysteresis deadband for airflow [m/s] *)

    rVHP_TripLL_ppm                 : REAL := 1050.0;               (* Bio-decon dwell low concentration trip [ppm] *)
    rVHP_TripHH_ppm                 : REAL := 1500.0;               (* High concentration condensation trip [ppm] *)

    rCrimp_TripLL_N                 : REAL := 115.0;                (* Loose cap / low RSF crimp fault [N] *)
    rCrimp_TripHH_N                 : REAL := 185.0;                (* Crushed glass vial neck crimp fault [N] *)

    rAlarmTimer_IsoPressLL_ms       : REAL := 0.0;                  (* Delay timer for isolator LL trip [ms] *)
    rAlarmTimer_LaminarLL_ms        : REAL := 0.0;                  (* Delay timer for laminar airflow LL trip [ms] *)
    rAlarmTimer_CrimpFault_ms       : REAL := 0.0;                  (* Delay timer for crimper fault trip [ms] *)

    (* Internal Computation Loop Counters & Temporary Reals *)
    i                               : INT := 1;                     (* Primary row iterator *)
    j                               : INT := 1;                     (* Primary column iterator *)
    k                               : INT := 1;                     (* Prediction step iterator *)
    h                               : INT := 1;                     (* Dosing head index iterator [1..10] *)
    m                               : INT := 1;                     (* Sensor channel iterator *)
    iter                            : INT := 1;                     (* PGD solver iteration index *)

    rTemp1                          : REAL := 0.0;                  (* Scratch accumulator real 1 *)
    rTemp2                          : REAL := 0.0;                  (* Scratch accumulator real 2 *)
    rTemp3                          : REAL := 0.0;                  (* Scratch accumulator real 3 *)
    rTempDiff                       : REAL := 0.0;                  (* Scratch difference real *)
    rTempNorm                       : REAL := 0.0;                  (* Scratch vector Euclidean norm real *)
    rSum                            : REAL := 0.0;                  (* General scratch summation real *)
    rTau                            : REAL := 0.0;                  (* Normalized time variable [0.0 - 1.0] *)
    rTau2                           : REAL := 0.0;                  (* Tau squared *)
    rTau3                           : REAL := 0.0;                  (* Tau cubed *)
    rTau4                           : REAL := 0.0;                  (* Tau 4th power *)
    rTau5                           : REAL := 0.0;                  (* Tau 5th power *)
    rMeniscusRise_mm                : REAL := 0.0;                  (* Calculated liquid level elevation [mm] *)
END_VAR
"""
