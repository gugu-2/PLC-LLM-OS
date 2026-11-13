VAR
    (* =================================================================================================================
     * SECTION 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) INTERNAL STRUCTURES & DISCREPANCY TIMERS
     * ================================================================================================================= *)
    (* --- TMR Channel 1: In-Mold Cavity Piezoelectric Pressure Sensors --- *)
    rCavPres_SensA_Val           : REAL := 0.0;     (* Filtered Sensor A Value [bar] *)
    rCavPres_SensB_Val           : REAL := 0.0;     (* Filtered Sensor B Value [bar] *)
    rCavPres_SensC_Val           : REAL := 0.0;     (* Filtered Sensor C Value [bar] *)
    rCavPres_Voted_Val           : REAL := 0.0;     (* 2oo3 Voted Output Cavity Pressure [bar] *)
    rCavPres_Prev_Voted          : REAL := 0.0;     (* Previous Cycle Voted Cavity Pressure [bar] *)
    rCavPres_DiscTimer_AB        : REAL := 0.0;     (* Discrepancy Timer Channel A vs B [s] *)
    rCavPres_DiscTimer_BC        : REAL := 0.0;     (* Discrepancy Timer Channel B vs C [s] *)
    rCavPres_DiscTimer_CA        : REAL := 0.0;     (* Discrepancy Timer Channel C vs A [s] *)
    rCavPres_DiscThresh          : REAL := 45.0;    (* Maximum Allowable Discrepancy Threshold [bar] *)
    rCavPres_DiscMaxTime         : REAL := 0.015;   (* Maximum Discrepancy Persistence Limit [s] (15 ms) *)
    bCavPres_SensA_Fault         : BOOL := FALSE;   (* Sensor A Latching Hardware Fault Flag *)
    bCavPres_SensB_Fault         : BOOL := FALSE;   (* Sensor B Latching Hardware Fault Flag *)
    bCavPres_SensC_Fault         : BOOL := FALSE;   (* Sensor C Latching Hardware Fault Flag *)
    iCavPres_TMR_HealthState     : INT  := 3;       (* 3=2oo3 Normal, 2=1oo2 Degraded, 1=1oo1 Failsafe, 0=Trip *)

    (* --- TMR Channel 2: Nozzle Melt Injection Pressure Sensors --- *)
    rMeltPres_SensA_Val          : REAL := 0.0;     (* Filtered Sensor A Value [bar] *)
    rMeltPres_SensB_Val          : REAL := 0.0;     (* Filtered Sensor B Value [bar] *)
    rMeltPres_SensC_Val          : REAL := 0.0;     (* Filtered Sensor C Value [bar] *)
    rMeltPres_Voted_Val          : REAL := 0.0;     (* 2oo3 Voted Output Nozzle Melt Pressure [bar] *)
    rMeltPres_Prev_Voted         : REAL := 0.0;     (* Previous Cycle Voted Melt Pressure [bar] *)
    rMeltPres_DiscTimer_AB       : REAL := 0.0;     (* Discrepancy Timer Channel A vs B [s] *)
    rMeltPres_DiscTimer_BC       : REAL := 0.0;     (* Discrepancy Timer Channel B vs C [s] *)
    rMeltPres_DiscTimer_CA       : REAL := 0.0;     (* Discrepancy Timer Channel C vs A [s] *)
    rMeltPres_DiscThresh         : REAL := 60.0;    (* Discrepancy Threshold [bar] *)
    rMeltPres_DiscMaxTime        : REAL := 0.010;   (* Discrepancy Persistence Limit [s] (10 ms) *)
    bMeltPres_SensA_Fault        : BOOL := FALSE;   (* Sensor A Fault Flag *)
    bMeltPres_SensB_Fault        : BOOL := FALSE;   (* Sensor B Fault Flag *)
    bMeltPres_SensC_Fault        : BOOL := FALSE;   (* Sensor C Fault Flag *)
    iMeltPres_TMR_HealthState    : INT  := 3;       (* 3=2oo3 Normal, 2=1oo2 Degraded, 1=1oo1 Failsafe, 0=Trip *)

    (* --- TMR Channel 3: Screw Axial Position Absolute Scales --- *)
    rScrewPos_SensA_Val          : REAL := 0.0;     (* Filtered Scale A Position [mm] *)
    rScrewPos_SensB_Val          : REAL := 0.0;     (* Filtered Scale B Position [mm] *)
    rScrewPos_SensC_Val          : REAL := 0.0;     (* Filtered Scale C Position [mm] *)
    rScrewPos_Voted_Val          : REAL := 0.0;     (* 2oo3 Voted Output Screw Position [mm] *)
    rScrewPos_Prev_Voted         : REAL := 0.0;     (* Previous Cycle Screw Position [mm] *)
    rScrewPos_DiscTimer_AB       : REAL := 0.0;     (* Discrepancy Timer Channel A vs B [s] *)
    rScrewPos_DiscTimer_BC       : REAL := 0.0;     (* Discrepancy Timer Channel B vs C [s] *)
    rScrewPos_DiscTimer_CA       : REAL := 0.0;     (* Discrepancy Timer Channel C vs A [s] *)
    rScrewPos_DiscThresh         : REAL := 0.75;    (* Linear Scale Discrepancy Threshold [mm] *)
    rScrewPos_DiscMaxTime        : REAL := 0.005;   (* Discrepancy Persistence Limit [s] (5 ms) *)
    bScrewPos_SensA_Fault        : BOOL := FALSE;   (* Scale A Fault Flag *)
    bScrewPos_SensB_Fault        : BOOL := FALSE;   (* Scale B Fault Flag *)
    bScrewPos_SensC_Fault        : BOOL := FALSE;   (* Scale C Fault Flag *)
    iScrewPos_TMR_HealthState    : INT  := 3;       (* 3=2oo3 Normal, 2=1oo2 Degraded, 1=1oo1 Failsafe, 0=Trip *)

    (* --- TMR Channel 4: Extruder Bulk Melt Thermocouples --- *)
    rMeltTemp_SensA_Val          : REAL := 0.0;     (* Filtered TC A Value [deg C] *)
    rMeltTemp_SensB_Val          : REAL := 0.0;     (* Filtered TC B Value [deg C] *)
    rMeltTemp_SensC_Val          : REAL := 0.0;     (* Filtered TC C Value [deg C] *)
    rMeltTemp_Voted_Val          : REAL := 0.0;     (* 2oo3 Voted Output Bulk Melt Temp [deg C] *)
    rMeltTemp_DiscTimer_AB       : REAL := 0.0;     (* Discrepancy Timer A vs B [s] *)
    rMeltTemp_DiscTimer_BC       : REAL := 0.0;     (* Discrepancy Timer B vs C [s] *)
    rMeltTemp_DiscTimer_CA       : REAL := 0.0;     (* Discrepancy Timer C vs A [s] *)
    rMeltTemp_DiscThresh         : REAL := 6.5;     (* Thermal Discrepancy Threshold [deg C] *)
    rMeltTemp_DiscMaxTime        : REAL := 0.050;   (* Discrepancy Persistence Limit [s] (50 ms) *)
    bMeltTemp_SensA_Fault        : BOOL := FALSE;   (* Thermocouple A Fault Flag *)
    bMeltTemp_SensB_Fault        : BOOL := FALSE;   (* Thermocouple B Fault Flag *)
    bMeltTemp_SensC_Fault        : BOOL := FALSE;   (* Thermocouple C Fault Flag *)
    iMeltTemp_TMR_HealthState    : INT  := 3;       (* 3=2oo3 Normal, 2=1oo2 Degraded, 1=1oo1 Failsafe, 0=Trip *)

    (* =================================================================================================================
     * SECTION 2: 4 TIE-BAR EXTENSOMETERS, PLATEN BALANCING & THERMAL COMPENSATION OBSERVER
     * ================================================================================================================= *)
    rTB_Strain_CH1               : REAL := 0.0;     (* Filtered Tie-Bar 1 Extensometer Strain [um] *)
    rTB_Strain_CH2               : REAL := 0.0;     (* Filtered Tie-Bar 2 Extensometer Strain [um] *)
    rTB_Strain_CH3               : REAL := 0.0;     (* Filtered Tie-Bar 3 Extensometer Strain [um] *)
    rTB_Strain_CH4               : REAL := 0.0;     (* Filtered Tie-Bar 4 Extensometer Strain [um] *)
    rTB_MeanStrain               : REAL := 0.0;     (* Mean Elongation Across All 4 Tie-Bars [um] *)
    rTB_Force_CH1                : REAL := 0.0;     (* Individual Tensile Force Tie-Bar 1 [kN] *)
    rTB_Force_CH2                : REAL := 0.0;     (* Individual Tensile Force Tie-Bar 2 [kN] *)
    rTB_Force_CH3                : REAL := 0.0;     (* Individual Tensile Force Tie-Bar 3 [kN] *)
    rTB_Force_CH4                : REAL := 0.0;     (* Individual Tensile Force Tie-Bar 4 [kN] *)
    rTB_TotalClampForce          : REAL := 0.0;     (* Summed Clamp Tonnage from Tie-Bars [kN] *)
    rTB_YoungsModulus            : REAL := 210000.0;(* Chrome-Molybdenum Steel Elastic Modulus E [N/mm2] *)
    rTB_Diameter                 : REAL := 220.0;   (* Tie-Bar Solid Cylindrical Diameter [mm] *)
    rTB_CrossSectionArea         : REAL := 38013.27;(* Tie-Bar Cross Sectional Area A = pi*(d/2)^2 [mm2] *)
    rTB_GaugeLength              : REAL := 3500.0;  (* Effective Tension Measurement Length L [mm] *)
    rPlaten_Tilt_Horizontal      : REAL := 0.0;     (* Left vs Right Platen Strain Delta [um] *)
    rPlaten_Tilt_Vertical        : REAL := 0.0;     (* Top vs Bottom Platen Strain Delta [um] *)
    rPlaten_Tilt_Diagonal        : REAL := 0.0;     (* Torsional Platen Diagonal Asymmetry [um] *)
    rPlaten_MaxDeviation         : REAL := 0.0;     (* Peak-to-Peak Platen Elongation Spread [um] *)
    rTB_ThermalExpansionCoeff    : REAL := 0.000012;(* Structural Alloy Thermal Expansion Alpha [1/K] *)
    rPlaten_RefTemp              : REAL := 25.0;    (* Reference Calibration Metal Temperature [deg C] *)
    rMold_ThermalElongation_Delta: REAL := 0.0;     (* Calculated Tie-Bar Thermal Growth [mm] *)
    rMoldHeight_TrimAccumulator  : REAL := 0.0;     (* Servo Mold Height Correction Accumulator [mm] *)

    (* =================================================================================================================
     * SECTION 3: 8-ZONE BARREL CERAMIC HEATING & NON-LINEAR CROSS-WLF VISCOSITY OBSERVER
     * ================================================================================================================= *)
    (* --- 8-Zone Temperature Setpoints [deg C] --- *)
    rBarrel_SP_Z1                : REAL := 55.0;    (* Zone 1 Water-Cooled Feed Throat Setpoint [deg C] *)
    rBarrel_SP_Z2                : REAL := 245.0;   (* Zone 2 Rear Compression Zone Setpoint [deg C] *)
    rBarrel_SP_Z3                : REAL := 275.0;   (* Zone 3 Middle-Rear Plasticizing Setpoint [deg C] *)
    rBarrel_SP_Z4                : REAL := 295.0;   (* Zone 4 Middle Plasticizing Setpoint [deg C] *)
    rBarrel_SP_Z5                : REAL := 305.0;   (* Zone 5 Middle-Front Homogenizing Setpoint [deg C] *)
    rBarrel_SP_Z6                : REAL := 315.0;   (* Zone 6 Front Metering Setpoint [deg C] *)
    rBarrel_SP_Z7                : REAL := 320.0;   (* Zone 7 Nozzle Adapter Body Setpoint [deg C] *)
    rBarrel_SP_Z8                : REAL := 325.0;   (* Zone 8 High-Speed Injection Nozzle Tip [deg C] *)

    (* --- 8-Zone Temperature Process Values [deg C] --- *)
    rBarrel_PV_Z1                : REAL := 55.0;
    rBarrel_PV_Z2                : REAL := 245.0;
    rBarrel_PV_Z3                : REAL := 275.0;
    rBarrel_PV_Z4                : REAL := 295.0;
    rBarrel_PV_Z5                : REAL := 305.0;
    rBarrel_PV_Z6                : REAL := 315.0;
    rBarrel_PV_Z7                : REAL := 320.0;
    rBarrel_PV_Z8                : REAL := 325.0;

    (* --- 8-Zone PID Controller Registers --- *)
    rPID_Err_Z1, rPID_Err_Z2, rPID_Err_Z3, rPID_Err_Z4 : REAL := 0.0;
    rPID_Err_Z5, rPID_Err_Z6, rPID_Err_Z7, rPID_Err_Z8 : REAL := 0.0;
    rPID_ErrPrev_Z1, rPID_ErrPrev_Z2, rPID_ErrPrev_Z3, rPID_ErrPrev_Z4 : REAL := 0.0;
    rPID_ErrPrev_Z5, rPID_ErrPrev_Z6, rPID_ErrPrev_Z7, rPID_ErrPrev_Z8 : REAL := 0.0;
    rPID_Integ_Z1, rPID_Integ_Z2, rPID_Integ_Z3, rPID_Integ_Z4 : REAL := 0.0;
    rPID_Integ_Z5, rPID_Integ_Z6, rPID_Integ_Z7, rPID_Integ_Z8 : REAL := 0.0;
    rPID_Deriv_Z1, rPID_Deriv_Z2, rPID_Deriv_Z3, rPID_Deriv_Z4 : REAL := 0.0;
    rPID_Deriv_Z5, rPID_Deriv_Z6, rPID_Deriv_Z7, rPID_Deriv_Z8 : REAL := 0.0;
    rPID_Out_Z1, rPID_Out_Z2, rPID_Out_Z3, rPID_Out_Z4 : REAL := 0.0;
    rPID_Out_Z5, rPID_Out_Z6, rPID_Out_Z7, rPID_Out_Z8 : REAL := 0.0;

    (* --- Barrel Zone PID Tuning Parameters --- *)
    rPID_Kp_Zones                : REAL := 4.20;    (* Proportional Gain [ % / deg C ] *)
    rPID_Ti_Zones                : REAL := 120.0;   (* Integral Reset Time Ti [s] *)
    rPID_Td_Zones                : REAL := 18.5;    (* Derivative Rate Time Td [s] *)
    rPID_DerivFilter_Tau         : REAL := 1.25;    (* Derivative Low-Pass Filter Constant [s] *)
    rPID_Integ_Limit             : REAL := 85.0;    (* Anti-Windup Integral Saturation Clamp [%] *)

    (* --- Cross-WLF Rheological Viscosity Model Parameters --- *)
    rWLF_Eta0_Ref                : REAL := 4250.0;  (* Zero-Shear Viscosity Reference Eta0 [Pa.s] *)
    rWLF_TauStar                 : REAL := 38500.0; (* Critical Shear Stress Parameter Tau* [Pa] *)
    rWLF_PowerLawIndex           : REAL := 0.315;   (* Non-Newtonian Pseudoplastic Exponent n [-] *)
    rWLF_TStar                   : REAL := 423.15;  (* Reference Glass Transition Temperature T* [K] (150 C) *)
    rWLF_C1                      : REAL := 20.45;   (* WLF Universal Shift Factor C1 [-] *)
    rWLF_C2                      : REAL := 51.60;   (* WLF Universal Shift Factor C2 [K] *)
    rWLF_D3_PresCoeff            : REAL := 0.00018; (* Pressure Dependence Viscosity Factor D3 [1/bar] *)
    rScrew_Diameter              : REAL := 90.0;    (* Extruder Screw Outer Flight Diameter [mm] *)
    rScrew_ChannelDepth          : REAL := 4.80;    (* Metering Flight Channel Depth [mm] *)
    rScrew_ChannelVolume         : REAL := 0.00165; (* Metering Zone Active Polymer Volume [m3] *)
    rPolymer_ShearRate           : REAL := 0.0;     (* Calculated Apparent Shear Rate Gamma_Dot [1/s] *)
    rPolymer_DynamicViscosity    : REAL := 280.0;   (* Calculated Dynamic Shear Melt Viscosity [Pa.s] *)
    rShear_DissipationPower      : REAL := 0.0;     (* Viscous Shear Heating Generation Q_visc [W] *)
    rFeedforward_ThermalPower    : REAL := 0.0;     (* Viscous Dissipation Feedforward Heat Subtraction [%] *)

    (* =================================================================================================================
     * SECTION 4: DISCRETE 8x8 CYBER-PHYSICAL STATE-SPACE MATRICES & REGISTERS (Ts = 1.0 ms)
     * ================================================================================================================= *)
    (* State Vector x:
     *   x[1] = Screw Injection Axial Position [mm]
     *   x[2] = Screw Injection Velocity [mm/s]
     *   x[3] = Extruder Nozzle Melt Pressure [bar]
     *   x[4] = In-Mold Cavity Quartz Pressure [bar]
     *   x[5] = Barrel Bulk Polymer Temperature [deg C]
     *   x[6] = Clamping Toggle Lockup Force [kN]
     *   x[7] = Tie-Bar Mean Strain Elongation [um]
     *   x[8] = Proportional Hydraulic/Servo Back Pressure [bar]
     *)
    x_State                      : ARRAY[1..8] OF REAL := [0.0, 0.0, 0.0, 0.0, 280.0, 0.0, 0.0, 15.0];
    x_Ref                        : ARRAY[1..8] OF REAL := [0.0, 0.0, 0.0, 0.0, 310.0, 16000.0, 680.0, 15.0];
    x_Pred                       : ARRAY[1..8] OF REAL := [0.0, 0.0, 0.0, 0.0, 280.0, 0.0, 0.0, 15.0];
    x_Error                      : ARRAY[1..8] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

    (* Control Input Vector u:
     *   u[1] = Injection Servo Velocity Command [mm/s]
     *   u[2] = Holding / Packing Pressure Command [bar]
     *   u[3] = Toggle Clamping Servo Command [kN]
     *   u[4] = Ceramic Heater Master Thermal Command [%]
     *   u[5] = Extruder Screw Plasticizing RPM Command [RPM]
     *)
    u_Cmd                        : ARRAY[1..5] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0];
    u_Prev                       : ARRAY[1..5] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0];
    u_Candidate                  : ARRAY[1..5] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0];
    u_Grad                       : ARRAY[1..5] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0];
    u_Min                        : ARRAY[1..5] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0];
    u_Max                        : ARRAY[1..5] OF REAL := [320.0, 2200.0, 18000.0, 100.0, 220.0];
    u_MaxSlew                    : ARRAY[1..5] OF REAL := [15.0, 80.0, 500.0, 2.5, 8.0]; (* Max Delta u per ms *)

    (* Discrete State Transition Matrix A (8x8) at Ts = 1.0 ms *)
    matA                         : ARRAY[1..8, 1..8] OF REAL;
    (* Input Matrix B (8x5) at Ts = 1.0 ms *)
    matB                         : ARRAY[1..8, 1..5] OF REAL;
    (* Output Matrix C (8x8) *)
    matC                         : ARRAY[1..8, 1..8] OF REAL;
    (* Direct Feedthrough Matrix D (8x5) *)
    matD                         : ARRAY[1..8, 1..5] OF REAL;

    (* =================================================================================================================
     * SECTION 5: RECEDING-HORIZON MPC OPTIMIZER WITH PROJECTED GRADIENT DESCENT (PGD)
     * ================================================================================================================= *)
    rMPC_WeightQ                 : ARRAY[1..8] OF REAL := [1.80, 0.95, 0.65, 3.40, 0.40, 1.25, 0.85, 0.50];
    rMPC_WeightR                 : ARRAY[1..5] OF REAL := [0.12, 0.08, 0.05, 0.25, 0.15];
    rMPC_WeightS                 : ARRAY[1..5] OF REAL := [0.35, 0.22, 0.18, 0.45, 0.30]; (* Slew rate penalty *)
    rMPC_WeightP_Term            : ARRAY[1..8] OF REAL := [4.50, 2.20, 1.80, 8.50, 1.00, 3.20, 2.10, 1.20];
    rMPC_StepSize_Alpha          : REAL := 0.0028;  (* PGD Convergence Gradient Step Size *)
    rMPC_CostObjective           : REAL := 0.0;     (* Computed Quadratic Cost Functional Value J *)
    iMPC_IterCounter             : INT  := 0;       (* PGD Iteration Loop Index *)
    bMPC_Converged               : BOOL := FALSE;   (* PGD Convergence Gradient Tolerance Met *)
    rMPC_GradNorm                : REAL := 0.0;     (* Euclidean 2-Norm of Control Input Gradient *)
    rMPC_GradTolerance           : REAL := 0.050;   (* Gradient Stopping Criterion Norm *)

    (* Multi-Step Forward Prediction Registers (Horizon Np = 5) *)
    x_Horizon                    : ARRAY[1..5, 1..8] OF REAL;
    u_Horizon                    : ARRAY[1..5, 1..5] OF REAL;

    (* =================================================================================================================
     * SECTION 6: IN-MOLD CAVITY PIEZOELECTRIC V/P CASCADE & ANTI-OVERSHOOT FILTER
     * ================================================================================================================= *)
    rVP_CavityThreshold          : REAL := 650.0;   (* Target Mold Cavity V/P Transfer Pressure [bar] *)
    rVP_RateThreshold            : REAL := 42000.0; (* Dynamic Pressure Rate-of-Rise Trigger dP/dt [bar/s] *)
    rVP_IntegralThreshold        : REAL := 85.0;    (* Cavity Pressure Impulse Integral Trigger [bar.s] *)
    rVP_ScrewPosFallback         : REAL := 18.5;    (* Safety Machine Position Switchover Fallback [mm] *)
    rVP_MeltPresFallback         : REAL := 1850.0;  (* Hydraulic/Nozzle Safety Overpressure Fallback [bar] *)
    rCavPres_Derivative          : REAL := 0.0;     (* Filtered In-Mold Pressure Rate of Change [bar/s] *)
    rCavPres_Integral            : REAL := 0.0;     (* Numerical Time-Integral of Cavity Pressure [bar.s] *)
    rCavPres_DampenedVelocity    : REAL := 0.0;     (* Deceleration Compensated Servo Injection Velocity [mm/s] *)
    rVP_DampingGain_Kd           : REAL := 0.185;   (* Pressure Overshoot Mitigation Deceleration Factor *)
    rVP_RateDampingGain_Kr       : REAL := 0.0012;  (* Pressure Spike Rate Mitigation Deceleration Factor *)
    bVP_SwitchoverLatched        : BOOL := FALSE;   (* V/P Transfer Transition Completed Latch *)
    bVP_TriggeredByCavity        : BOOL := FALSE;   (* V/P Triggered by Piezoelectric Quartz Sensor *)
    bVP_TriggeredByRate          : BOOL := FALSE;   (* V/P Triggered by Dynamic Pressure Inflection *)
    bVP_TriggeredByPosition      : BOOL := FALSE;   (* V/P Triggered by Stroke Position Fallback *)
    bVP_TriggeredByMeltPres      : BOOL := FALSE;   (* V/P Triggered by Nozzle Overpressure Limit *)
    rVP_TransferCavityPressure   : REAL := 0.0;     (* Snapshot Cavity Pressure at Instant of Switchover [bar] *)
    rVP_TransferScrewPosition    : REAL := 0.0;     (* Snapshot Screw Position at Instant of Switchover [mm] *)
    rVP_TransferTimeStamp        : REAL := 0.0;     (* Elapsed Cycle Time at Transfer [s] *)
    rCavity_PeakObservedPressure : REAL := 0.0;     (* Peak In-Mold Pressure Detected During Cycle [bar] *)

    (* =================================================================================================================
     * SECTION 7: DETERMINISTIC 14-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
     * ================================================================================================================= *)
    (* FSM State Enumeration:
     *   0: STATE_00_IDLE_STANDBY
     *   1: STATE_01_MOLD_CLOSE_RAPID
     *   2: STATE_02_LOW_PRESSURE_MOLD_PROTECT
     *   3: STATE_03_CLAMP_LOCKUP_TONNAGE
     *   4: STATE_04_CARRIAGE_FORWARD_TOUCH
     *   5: STATE_05_INJECTION_FILLING_PROFILE
     *   6: STATE_06_VP_SWITCHOVER_TRANSFER
     *   7: STATE_07_HOLDING_PRESSURE_PROFILE
     *   8: STATE_08_SCREW_PLASTICIZING_DOSING
     *   9: STATE_09_SUCKBACK_DECOMPRESSION
     *  10: STATE_10_IN_MOLD_COOLING_CYCLE
     *  11: STATE_11_MOLD_OPEN_DECEL_PROFILE
     *  12: STATE_12_PARTS_EJECTION_ROBOT_HANDSHAKE
     *  13: STATE_13_SAFE_ABORT_PURGE_RECOVERY
     *)
    iFSM_State                   : INT  := 0;       (* Active Operating Stage Index *)
    iFSM_StatePrev               : INT  := 0;       (* Previous Operating Stage Index *)
    rFSM_StateTimer              : REAL := 0.0;     (* Elapsed Time within Active State [s] *)
    bFSM_FirstScan               : BOOL := TRUE;    (* First Scan Flag upon State Entry *)
    rCycle_TotalTimer            : REAL := 0.0;     (* Running Cumulative Total Cycle Time [s] *)
    iCycle_ShotCounter           : DINT := 0;       (* Continuous Production Shot Counter *)

    (* Multi-Stage Injection Filling Profile Parameters *)
    rInjProfile_Pos1             : REAL := 180.0;   (* Injection Velocity Step 1 Boundary [mm] *)
    rInjProfile_Pos2             : REAL := 120.0;   (* Injection Velocity Step 2 Boundary [mm] *)
    rInjProfile_Pos3             : REAL := 60.0;    (* Injection Velocity Step 3 Boundary [mm] *)
    rInjProfile_Pos4             : REAL := 30.0;    (* Injection Velocity Step 4 Boundary [mm] *)
    rInjProfile_Pos5             : REAL := 18.5;    (* Injection Velocity Step 5 Boundary (V/P zone) [mm] *)
    rInjProfile_Vel1             : REAL := 140.0;   (* High-Speed Volumetric Filling Velocity 1 [mm/s] *)
    rInjProfile_Vel2             : REAL := 125.0;   (* Progressive Cavity Filling Velocity 2 [mm/s] *)
    rInjProfile_Vel3             : REAL := 95.0;    (* Runner/Gate Entry Controlled Velocity 3 [mm/s] *)
    rInjProfile_Vel4             : REAL := 60.0;    (* Cavity End-Pack Controlled Velocity 4 [mm/s] *)
    rInjProfile_Vel5             : REAL := 32.0;    (* Final Deceleration Anti-Spike Velocity 5 [mm/s] *)

    (* Multi-Stage Holding Packing Pressure Profile Parameters *)
    rHoldProfile_Time1           : REAL := 1.25;    (* Stage 1 High Packing Duration [s] *)
    rHoldProfile_Time2           : REAL := 2.50;    (* Stage 2 Gate Solidification Duration [s] *)
    rHoldProfile_Time3           : REAL := 1.75;    (* Stage 3 Residual Sinking Hold Duration [s] *)
    rHoldProfile_Pres1           : REAL := 1050.0;  (* Stage 1 Initial Cavity Packing Pressure [bar] *)
    rHoldProfile_Pres2           : REAL := 780.0;   (* Stage 2 Sustained Gate Freeze Pressure [bar] *)
    rHoldProfile_Pres3           : REAL := 480.0;   (* Stage 3 Residual Packing Pressure [bar] *)

    (* Plasticizing, Suck-Back & Toggle Kinematics *)
    rDose_TargetStroke           : REAL := 210.0;   (* Metered Polymer Shot Size Target [mm] *)
    rDose_ScrewSpeedRPM          : REAL := 75.0;    (* Plasticizing Extruder Rotational Velocity [RPM] *)
    rDose_BackPresSetpoint       : REAL := 18.5;    (* Constant Back-Pressure Resistance [bar] *)
    rSuckBack_Stroke             : REAL := 7.5;     (* Axial Screw Decompression Distance [mm] *)
    rSuckBack_Velocity           : REAL := 25.0;    (* Axial Screw Decompression Velocity [mm/s] *)
    rCooling_Duration            : REAL := 9.5;     (* Mold In-Cavity Solidification Time [s] *)
    rMoldClose_StrokeTarget      : REAL := 0.0;     (* Fully Closed Toggle Platen Datum [mm] *)
    rMoldOpen_StrokeTarget       : REAL := 680.0;   (* Fully Open Moving Platen Target [mm] *)
    rMoldOpen_DecelPosition      : REAL := 610.0;   (* Deceleration Braking Point During Opening [mm] *)
    rLPMP_StartPosition          : REAL := 65.0;    (* Mold Protection Sensitive Zone Start [mm] *)
    rLPMP_ForceLimit             : REAL := 12.0;    (* Mold Protection Max Clamp Force Limit [kN] *)
    rLPMP_TimeLimit              : REAL := 1.40;    (* Mold Protection Max Allowed Transit Time [s] *)
    rEjector_StrokeTarget        : REAL := 145.0;   (* Parts Stripping Forward Ejector Stroke [mm] *)
    rEjector_PulseCount          : INT  := 0;       (* Ejector Multi-Stroke Pulsing Counter *)
    rEjector_MaxPulses           : INT  := 3;       (* Maximum Ejector Retract/Forward Cycles *)

    (* =================================================================================================================
     * SECTION 8: ISA-18.2 MULTI-TIERED ALARM THRESHOLDS, HYSTERESIS & DWORD REGISTERS
     * ================================================================================================================= *)
    (* Cavity Pressure Alarm Thresholds *)
    rAlarm_CavPres_HH_Trip       : REAL := 1350.0;  (* Critical Cavity Overpressure Tooling Trip [bar] *)
    rAlarm_CavPres_H_Warn        : REAL := 1150.0;  (* High Cavity Packing Pressure Warning [bar] *)
    rAlarm_CavPres_L_Warn        : REAL := 280.0;   (* Low Cavity Pressure Short-Shot Warning [bar] *)
    rAlarm_CavPres_LL_Trip       : REAL := 45.0;    (* Zero Cavity Pressure Blocked Gate Trip [bar] *)
    rAlarm_CavPres_ROC_Trip      : REAL := 85000.0; (* Dangerous Cavity Pressure Rate Spike [bar/s] *)
    rAlarm_CavPres_Hyst          : REAL := 25.0;    (* Clearance Deadband Hysteresis [bar] *)

    (* Melt Nozzle Pressure Alarm Thresholds *)
    rAlarm_MeltPres_HH_Trip      : REAL := 2250.0;  (* Maximum Hydraulic/Extruder Servo Trip [bar] *)
    rAlarm_MeltPres_H_Warn       : REAL := 1950.0;  (* High Extruder Head Pressure Warning [bar] *)
    rAlarm_MeltPres_L_Warn       : REAL := 120.0;   (* Low Melt Feed Pressure Warning [bar] *)
    rAlarm_MeltPres_LL_Trip      : REAL := 15.0;    (* Empty Barrel Injection Trip [bar] *)
    rAlarm_MeltPres_Hyst         : REAL := 40.0;    (* Clearance Deadband Hysteresis [bar] *)

    (* Clamp Tonnage Alarm Thresholds *)
    rAlarm_Clamp_HH_Trip         : REAL := 17600.0; (* Over-Tonnage Tie-Bar Yield Protection Trip [kN] *)
    rAlarm_Clamp_H_Warn          : REAL := 16800.0; (* High Clamping Tonnage Warning [kN] *)
    rAlarm_Clamp_L_Warn          : REAL := 14800.0; (* Low Tonnage Mold Flash Risk Warning [kN] *)
    rAlarm_Clamp_LL_Trip         : REAL := 12000.0; (* Unlocked Toggle Clamp Under-Tonnage Trip [kN] *)
    rAlarm_Clamp_Hyst            : REAL := 150.0;   (* Clamping Force Hysteresis [kN] *)

    (* Tie-Bar Strain Imbalance Alarm Thresholds *)
    rAlarm_TB_Tilt_HH_Trip       : REAL := 75.0;    (* Platen Tilt Angular Deflection Critical Trip [um] *)
    rAlarm_TB_Tilt_H_Warn        : REAL := 45.0;    (* Platen Parallelism Deviation Warning [um] *)
    rAlarm_TB_Tilt_Hyst          : REAL := 8.0;     (* Platen Tilt Clear Hysteresis [um] *)

    (* Barrel Zone Temperature Deviation Bands *)
    rAlarm_Barrel_Dev_HH_Trip    : REAL := 30.0;    (* Critical Polymer Thermal Degradation Trip [deg C] *)
    rAlarm_Barrel_Dev_H_Warn     : REAL := 12.0;    (* High Barrel Temperature Excursion Warning [deg C] *)
    rAlarm_Barrel_Dev_L_Warn     : REAL := 12.0;    (* Low Barrel Temperature Viscosity Warning [deg C] *)
    rAlarm_Barrel_Dev_LL_Trip    : REAL := 25.0;    (* Cold Screw Solid Plastic Jam Interlock Trip [deg C] *)
    rAlarm_Barrel_Dev_Hyst       : REAL := 3.0;     (* Thermal Alarm Clearance Hysteresis [deg C] *)

    (* Low Pressure Mold Protection Alarm *)
    bAlarm_LPMP_ObstructionTrip  : BOOL := FALSE;   (* Mold Clamping Obstruction Detected (Part Jam) *)

    (* Alarm Status Latching Bits *)
    bTrip_CavPres_HH             : BOOL := FALSE;
    bWarn_CavPres_H              : BOOL := FALSE;
    bWarn_CavPres_L              : BOOL := FALSE;
    bTrip_CavPres_LL             : BOOL := FALSE;
    bTrip_CavPres_ROC            : BOOL := FALSE;

    bTrip_MeltPres_HH            : BOOL := FALSE;
    bWarn_MeltPres_H             : BOOL := FALSE;
    bWarn_MeltPres_L             : BOOL := FALSE;
    bTrip_MeltPres_LL            : BOOL := FALSE;

    bTrip_Clamp_HH               : BOOL := FALSE;
    bWarn_Clamp_H                : BOOL := FALSE;
    bWarn_Clamp_L                : BOOL := FALSE;
    bTrip_Clamp_LL               : BOOL := FALSE;

    bTrip_TB_Tilt_HH             : BOOL := FALSE;
    bWarn_TB_Tilt_H              : BOOL := FALSE;

    bTrip_Barrel_Thermal_HH      : BOOL := FALSE;
    bWarn_Barrel_Thermal_H       : BOOL := FALSE;
    bWarn_Barrel_Thermal_L       : BOOL := FALSE;
    bTrip_Barrel_Thermal_LL      : BOOL := FALSE;

    bTrip_SafetyGate_Violation   : BOOL := FALSE;
    bTrip_EmergencyStop_Active   : BOOL := FALSE;
    bTrip_TMR_SensorCollapse     : BOOL := FALSE;

    (* Rate-of-Change Numerical Derivative Registers *)
    rMeltPres_ROC                : REAL := 0.0;     (* Melt Pressure Rate of Change [bar/s] *)
    rClampForce_ROC              : REAL := 0.0;     (* Clamp Force Rate of Change [kN/s] *)
    rScrewVelocity_Meas          : REAL := 0.0;     (* Measured Screw Injection Velocity [mm/s] *)

    (* 32-Bit Internal Mask Registers *)
    dwStatus_FSM                 : DWORD := 16#0000_0000;
    dwStatus_TMR                 : DWORD := 16#0000_0000;
    dwTrip_Alarms                : DWORD := 16#0000_0000;
    dwWarn_Alarms                : DWORD := 16#0000_0000;
    dwDiag_MPC                   : DWORD := 16#0000_0000;

    (* Auxiliary Iteration & Temporary Registers *)
    iLoop_i                      : INT  := 0;
    iLoop_j                      : INT  := 0;
    iLoop_k                      : INT  := 0;
    rTemp_A                      : REAL := 0.0;
    rTemp_B                      : REAL := 0.0;
    rTemp_C                      : REAL := 0.0;
    rTemp_Delta                  : REAL := 0.0;
    rTemp_Sum                    : REAL := 0.0;
    rTemp_Diff                   : REAL := 0.0;
    rTemp_AbsDiff                : REAL := 0.0;
    rScanTime_Ts                 : REAL := 0.001;   (* Servo Scan Period: 1.0 ms (0.001 s) *)
    bInitializedMatrices         : BOOL := FALSE;   (* One-Shot Matrix Initialization Flag *)
END_VAR
