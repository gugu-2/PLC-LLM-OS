# -*- coding: utf-8 -*-
"""
vial_filler_header_io.py
Contains header comments, VAR_INPUT, VAR_OUTPUT, and VAR blocks for FB_Pharma_AsepticVialFilling_600VPM_Checkweigh.
"""

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Pharma_AsepticVialFilling_600VPM_Checkweigh
(* ========================================================================================= *)
(* LUMINA CYBER-PHYSICAL SYSTEMS PHARMACEUTICAL & STERILE INJECTABLES DIVISION               *)
(* V7 MAX-PERSONA ENGINEERING STANDARD: CGMP ANNEX 1 / FDA 21 CFR PART 211 / GAMP 5 CLASS 4  *)
(*                                                                                           *)
(* AUTONOMOUS HIGH-SPEED ASEPTIC ROTARY VIAL FILLING & STOPPERING MONOBLOCK (600 VPM)        *)
(* INTEGRATING:                                                                              *)
(*   1. CLOSED BARRIER ISOLATOR / RABS AERODYNAMICS & GRADE A UNIDIRECTIONAL AIRFLOW         *)
(*   2. 12-CHANNEL ROTARY VALVELESS CERAMIC PISTON / PERISTALTIC MULTI-NEEDLE DOSING        *)
(*   3. DYNAMIC 5TH-ORDER JERK-LIMITED BOTTOM-UP FILLING NEEDLE DIVE TRAJECTORY TRACKING     *)
(*   4. 100% IN-PROCESS CONTROL (IPC) TARE & GROSS DUAL-PAN EMFR DYNAMIC CHECKWEIGHING       *)
(*   5. CLOSED-LOOP INDIVIDUAL CHANNEL ADAPTIVE INTEGRAL MASS TRIM & CP/CPK SPC ENGINE       *)
(*   6. HIGH-PURITY NITROGEN (N2) PRE/IN/POST-GASSING HEADSPACE RESIDUAL OXYGEN CONTROL      *)
(*   7. CONTINUOUS ROTARY VACUUM STOPPERING WHEEL WITH 24-POCKET VACUUM SEAT VERIFICATION    *)
(*   8. CONTINUOUS 16-HEAD ROTARY ALUMINUM CRIMP CAPPER CONTAINER CLOSURE INTEGRITY (CCI)    *)
(*   9. HIGH-SPEED STARWHEEL DIVERTER GATE WITH PNEUMATIC AIR-PUFF POCKET REJECT DISPATCH    *)
(*  10. 16-STATE DISCRETE STATE-SPACE DYNAMICS (A, B, C, D) & RECEDING-HORIZON MPC SOLVER   *)
(*  11. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR FUSION ACROSS ALL CRITICAL CQA LOOPS    *)
(*  12. 12-STAGE DETERMINISTIC FINITE STATE MACHINE (FSM) WITH AUTOMATED CIP/SIP SEQUENCING  *)
(*  13. ISA-18.2 MULTI-TIERED ALARM MATRIX WITH BIT-PACKED REAL-TIME TELEMETRY DWORDS        *)
(*                                                                                           *)
(* GOVERNING FIRST-PRINCIPLES CYBER-PHYSICAL FORMULATIONS:                                   *)
(*   - Monoblock Kinematic Pitch: T_pitch = 60.0 / 600.0 = 0.100 s (100 ms index pitch)      *)
(*   - Turret Rotary Angular Speed: omega_turret = 2*PI * (600.0 / 60.0) / N_pockets [rad/s]*)
(*   - Bottom-Up Meniscus Tracking: z_needle(t) = z_bottom + (V_disp(t) / (PI*r_vial^2)) + dz*)
(*   - 5th-Order Polynomial Dive: S(tau) = Stroke * (10*tau^3 - 15*tau^4 + 6*tau^5)          *)
(*   - EMFR Electromagnetic Coil Equilibrium: F_em = B_mag * L_wire * I_coil = m_vial * g_acc*)
(*   - Lorentz Voice-Coil Dynamic Balance: m_meas = (B_mag * L_wire * I_coil) / g_acc - Tare *)
(*   - Tubing Maxwell-Kelvin Viscoelastic Pressure: dP/dt = E_eff/V * (Q_pump - Q_needle)    *)
(*   - Headspace Oxygen Inert Gas Diffusion: dC_O2/dt = - (Q_N2 / V_headspace) * C_O2        *)
(*   - Crimp Cap Residual Seal Force: F_rsf = k_stopper * delta_z + mu_elastomer * v_crimp   *)
(*   - State-Space Discretization: x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k]         *)
(*   - MPC Cost Functional: J = sum(x' Q x + u' R u + du' S du) + x_N' P x_N                 *)
(* ========================================================================================= *)

VAR_INPUT
    (* ===================================================================================== *)
    (* 1. PROCESS OPERATING SETPOINTS & RECIPE PARAMETERS                                    *)
    (* ===================================================================================== *)
    rTargetSpeed_VPM                : REAL := 600.0;    (* Monoblock target production rate [vials/min] *)
    rTargetDosingVol_ml             : REAL := 10.0;     (* Nominal recipe fill volume [ml] *)
    rLiquidDensity_g_cm3            : REAL := 1.025;    (* Liquid formulation density [g/cm3] *)
    rLiquidViscosity_mPas           : REAL := 3.25;     (* Liquid formulation dynamic viscosity [mPas] *)
    rTareWeightTolerance_mg         : REAL := 25.0;     (* Empty glass vial allowable tare tolerance [mg] *)
    rGrossWeightTolerance_mg        : REAL := 8.0;      (* Filled vial gross mass acceptance tolerance [mg] *)
    rHeadspaceO2_Max_Pct            : REAL := 0.80;     (* Maximum allowable residual headspace oxygen [%] *)
    rCrimpForce_Nominal_N           : REAL := 145.0;    (* Target container closure crimp sealing force [N] *)
    rCrimpForce_Tol_N               : REAL := 15.0;     (* Crimp sealing force allowable acceptance band [N] *)
    rIsolatorDiffPress_Set_Pa       : REAL := 45.0;     (* Grade A isolator positive differential pressure [Pa] *)
    rLaminarAirVelocity_Set_mps     : REAL := 0.45;     (* Vertical laminar airflow velocity setpoint [m/s] *)
    rN2SupplyPressure_bar           : REAL := 4.5;      (* High-purity nitrogen supply line pressure [bar] *)
    rN2PurgeFlow_Set_lnpm           : REAL := 18.5;     (* Nitrogen needle gassing flow setpoint [L/min] *)
    rDivingNeedleStroke_mm          : REAL := 65.0;     (* Vertical diving needle servo stroke length [mm] *)
    rVialNeckInternalDiam_mm        : REAL := 12.6;     (* ISO 8362-1 10R vial mouth inner diameter [mm] *)
    rVialBodyExternalDiam_mm        : REAL := 24.0;     (* ISO 8362-1 10R vial body outer diameter [mm] *)
    rVialHeight_mm                  : REAL := 45.0;     (* Total nominal glass vial height [mm] *)
    rMeniscusOffsetDist_mm          : REAL := 2.5;      (* Needle tip vertical clearance above liquid [mm] *)

    (* ===================================================================================== *)
    (* 2. TRIPLE MODULAR REDUNDANCY (2oo3) SENSOR INPUT BANKS                                *)
    (* ===================================================================================== *)
    (* --- Main Starwheel Master Optical Resolvers --- *)
    rStarwheelEncoder_ChA_deg       : REAL;             (* Master turret absolute resolver channel A [deg] *)
    rStarwheelEncoder_ChB_deg       : REAL;             (* Master turret absolute resolver channel B [deg] *)
    rStarwheelEncoder_ChC_deg       : REAL;             (* Master turret absolute resolver channel C [deg] *)

    (* --- In-Line Pre-Fill Dynamic EMFR Tare Load Cells --- *)
    rTareLoadCell_ChA_mg            : REAL;             (* Pre-fill EMFR Tare load cell channel A [mg] *)
    rTareLoadCell_ChB_mg            : REAL;             (* Pre-fill EMFR Tare load cell channel B [mg] *)
    rTareLoadCell_ChC_mg            : REAL;             (* Pre-fill EMFR Tare load cell channel C [mg] *)

    (* --- In-Line Post-Fill Dynamic EMFR Gross Load Cells --- *)
    rGrossLoadCell_ChA_mg           : REAL;             (* Post-fill EMFR Gross load cell channel A [mg] *)
    rGrossLoadCell_ChB_mg           : REAL;             (* Post-fill EMFR Gross load cell channel B [mg] *)
    rGrossLoadCell_ChC_mg           : REAL;             (* Post-fill EMFR Gross load cell channel C [mg] *)

    (* --- Grade A Isolator Differential Pressure Transmitters --- *)
    rIsolatorPress_ChA_Pa           : REAL;             (* Isolator differential pressure transmitter A [Pa] *)
    rIsolatorPress_ChB_Pa           : REAL;             (* Isolator differential pressure transmitter B [Pa] *)
    rIsolatorPress_ChC_Pa           : REAL;             (* Isolator differential pressure transmitter C [Pa] *)

    (* --- Nitrogen High-Purity Inerting Mass Flowmeters --- *)
    rN2Flow_ChA_lnpm                : REAL;             (* N2 mass flowmeter sensor channel A [L/min] *)
    rN2Flow_ChB_lnpm                : REAL;             (* N2 mass flowmeter sensor channel B [L/min] *)
    rN2Flow_ChC_lnpm                : REAL;             (* N2 mass flowmeter sensor channel C [L/min] *)

    (* ===================================================================================== *)
    (* 3. ANALYTICAL, PROCESS QUALITY & ENVIRONMENTAL INPUTS                                 *)
    (* ===================================================================================== *)
    rHeadspaceO2_Sensor_pct         : REAL;             (* TDLAS non-destructive headspace oxygen sensor [%] *)
    rCrimpForceSensor_N             : REAL;             (* Rotary capping spindle dynamic piezoelectric force [N] *)
    rCrimpDeflection_mm             : REAL;             (* Capping head calibrated spring deflection [mm] *)
    rStopperVacuumSense_bar         : REAL;             (* Rotary stoppering wheel vacuum manifold level [bar] *)
    rLaminarFlowAirVel_mps          : REAL;             (* Ultrasonic anemometer laminar air velocity [m/s] *)
    rVHP_Concentration_ppm          : REAL;             (* Vaporized Hydrogen Peroxide gassing level [ppm] *)
    rVHP_AerationLevel_ppm          : REAL;             (* Catalytic residual VHP aeration level [ppm] *)
    rIsolatorTemp_DegC              : REAL;             (* Grade A isolator chamber temperature [deg C] *)
    rIsolatorRH_pct                 : REAL;             (* Grade A isolator chamber relative humidity [%] *)
    rPeristalticInletPress_bar      : REAL;             (* Product feed manifold supply pressure [bar] *)

    (* ===================================================================================== *)
    (* 4. SAFETY, INTERLOCK & DISCRETE DIGITAL CONTROL SIGNALS                               *)
    (* ===================================================================================== *)
    bEmergencyStop                  : BOOL;             (* Hardwired SIL-3 emergency stop circuit healthy *)
    bIsolatorInterlockOk            : BOOL;             (* Glove ports, RTP, and door gaskets sealed *)
    bDepyrogenationTunnelReady      : BOOL;             (* Depyrogenation tunnel outfeed synchronized *)
    bStopperBowlLevelOk             : BOOL;             (* Elastomeric stopper vibratory bowl level ok *)
    bCapBowlLevelOk                 : BOOL;             (* Aluminum flip-off crimp cap bowl level ok *)
    bVialInfeedDetect               : BOOL;             (* Fiber-optic vial presence sensor at infeed star *)
    bRejectLaneClear                : BOOL;             (* Defect reject discharge chute sensor clear *)
    bCIP_SIP_Request                : BOOL;             (* Clean-In-Place / Steam-In-Place sequence request *)
    bReset                          : BOOL;             (* Master alarm and trip reset pushbutton *)
    bStepModeEnable                 : BOOL;             (* Maintenance single-index step mode enable *)
END_VAR

VAR_OUTPUT
    (* ===================================================================================== *)
    (* 1. PRIMARY ACTUATOR COMMANDS & SERVO SETPOINTS                                        *)
    (* ===================================================================================== *)
    rMainTurretSpeedCmd_RPM         : REAL;             (* Rotary starwheel indexing turret command [rpm] *)
    arNeedleDoseCmd_ml              : ARRAY[1..12] OF REAL; (* Multi-channel pump dose commands 1..12 [ml] *)
    rDivingNeedlePosCmd_mm          : REAL;             (* Bottom-up diving carriage servo position [mm] *)
    rDivingNeedleVelCmd_mms         : REAL;             (* Diving carriage instantaneous velocity [mm/s] *)
    rN2PurgeValveCmd_pct            : REAL;             (* Nitrogen purge gas proportional valve command [%] *)
    rStopperPickVacuumCmd_bar       : REAL;             (* Stoppering wheel vacuum transfer command [bar] *)
    rCrimpServoTorqueCmd_Nm         : REAL;             (* Rotary capping spindle dynamic torque command [Nm] *)
    rCrimpServoPosCmd_mm            : REAL;             (* Rotary capping spindle down-stroke position [mm] *)
    bRejectGateCmd                  : BOOL;             (* High-speed pneumatic reject diverter gate fire *)
    bRejectAirPuffCmd               : BOOL;             (* High-speed pocket pneumatic air-puff blast *)
    bRejectActive                   : BOOL;             (* Reject diverter currently executing discard *)

    (* ===================================================================================== *)
    (* 2. STATE TELEMETRY & DIGITAL SUPERVISION REGISTERS                                    *)
    (* ===================================================================================== *)
    dwMachineState                  : DWORD;            (* Current FSM operational state encoded *)
    dwSubState                      : DWORD;            (* Sub-routine phase identifier within active state *)
    dwAlarmsPriority1               : DWORD;            (* ISA-18.2 Critical Emergency Shutdown alarms *)
    dwAlarmsPriority2               : DWORD;            (* ISA-18.2 High Priority Quality/Reject alarms *)
    dwAlarmsPriority3               : DWORD;            (* ISA-18.2 Medium Advisory / Maintenance alarms *)
    dwDiagnosticWord                : DWORD;            (* Subsystem health and TMR channel degradation *)

    (* ===================================================================================== *)
    (* 3. PRODUCTION ACCOUNTABILITY & STATISTICAL PROCESS CONTROL (SPC)                      *)
    (* ===================================================================================== *)
    diTotalVialsProcessed           : DINT;             (* Total cumulative vials indexed into monoblock *)
    diTotalVialsAccepted            : DINT;             (* Conforming vials filled, stoppered, and capped *)
    diTotalVialsRejected            : DINT;             (* Defective vials diverted to reject bin *)
    diDosingRejectsCount            : DINT;             (* Rejects due to out-of-spec net liquid weight *)
    diStopperRejectsCount           : DINT;             (* Rejects due to missing or misaligned stopper *)
    diCrimpRejectsCount             : DINT;             (* Rejects due to abnormal crimp seal force *)
    rMeanGrossWeight_mg             : REAL;             (* Moving average of filled vial gross mass [mg] *)
    rStdDevGrossWeight_mg           : REAL;             (* Standard deviation of filled vial gross mass [mg] *)
    rProcessCapability_Cpk          : REAL;             (* Dynamic Cpk process capability index of dosing *)
    rMeanDosingVolume_ml            : REAL;             (* Real-time calculated mean fill volume [ml] *)
    bSystemRunning                  : BOOL;             (* Monoblock fully synchronized in production run *)
    bSystemReady                    : BOOL;             (* Monoblock sterilized, purged, and ready for infeed *)
    bCIP_SIP_Active                 : BOOL;             (* Automated CIP/SIP sanitization loop active *)
END_VAR

VAR
    (* ===================================================================================== *)
    (* 1. DISCRETE STATE-SPACE MODEL MATRICES & VECTORS (16 STATES, 8 CONTROLS, 8 OUTPUTS)    *)
    (* ===================================================================================== *)
    A_Matrix                        : ARRAY[1..16, 1..16] OF REAL; (* System dynamic transition matrix *)
    B_Matrix                        : ARRAY[1..16, 1..8] OF REAL;  (* Actuator input coupling matrix *)
    C_Matrix                        : ARRAY[1..8, 1..16] OF REAL;  (* Sensor measurement output matrix *)
    D_Matrix                        : ARRAY[1..8, 1..8] OF REAL;   (* Feedthrough direct transmission matrix *)

    (* MPC Quadratic Cost Optimization Weights *)
    Q_Weight                        : ARRAY[1..16, 1..16] OF REAL; (* State error penalty diagonal matrix *)
    R_Weight                        : ARRAY[1..8, 1..8] OF REAL;   (* Actuator slew rate penalty matrix *)
    P_Weight                        : ARRAY[1..16, 1..16] OF REAL; (* Terminal Riccati algebraic cost matrix *)

    (* Dynamic State and Control Vectors *)
    x_State                         : ARRAY[1..16] OF REAL;        (* Filtered true cyber-physical state *)
    x_Predict                       : ARRAY[1..16] OF REAL;        (* Forward 1-step predicted state *)
    x_Target                        : ARRAY[1..16] OF REAL;        (* Setpoint reference state trajectory *)
    x_Error                         : ARRAY[1..16] OF REAL;        (* Tracking deviation vector *)
    u_Control                       : ARRAY[1..8] OF REAL;         (* Instantaneous control vector *)
    u_Optimal                       : ARRAY[1..8] OF REAL;         (* MPC computed optimal control vector *)
    u_Prev                          : ARRAY[1..8] OF REAL;         (* Prior control vector for slew bounding *)
    du_Delta                        : ARRAY[1..8] OF REAL;         (* Control increment rate *)
    y_Measured                      : ARRAY[1..8] OF REAL;         (* Process output sensor vector *)
    y_Predict                       : ARRAY[1..8] OF REAL;         (* Predicted measurement vector *)
    y_Residual                      : ARRAY[1..8] OF REAL;         (* Innovation residual vector *)
    arObserverGain_L                : ARRAY[1..16, 1..8] OF REAL;  (* Steady-state Kalman observer gain *)

    (* Actuator Physical Saturation and Slew Limits *)
    arU_Min                         : ARRAY[1..8] OF REAL;         (* Lower saturation bound *)
    arU_Max                         : ARRAY[1..8] OF REAL;         (* Upper saturation bound *)
    arDeltaU_Max                    : ARRAY[1..8] OF REAL;         (* Maximum slew rate per execution step *)

    (* ===================================================================================== *)
    (* 2. MULTI-CHANNEL DOSING PUMP ARRAYS & ADAPTIVE TRIM (CHANNELS 1..12)                   *)
    (* ===================================================================================== *)
    arPumpOffsetTrim_ul             : ARRAY[1..12] OF REAL;        (* Adaptive micro-liter mass trim bias [ul] *)
    arNeedleTareWeight_mg           : ARRAY[1..12] OF REAL;        (* Tare weight registered per channel [mg] *)
    arNeedleGrossWeight_mg          : ARRAY[1..12] OF REAL;        (* Gross weight registered per channel [mg] *)
    arNeedleNetWeight_mg            : ARRAY[1..12] OF REAL;        (* Net filled mass registered per channel [mg] *)
    arNeedleDispenseCount           : ARRAY[1..12] OF DINT;        (* Total successful fills per needle *)
    arNeedleRejectCount             : ARRAY[1..12] OF DINT;        (* Reject count attributed per needle *)
    arChannelGain                   : ARRAY[1..12] OF REAL;        (* Closed-loop adaptive feedback gain *)
    arChannelIntegralError          : ARRAY[1..12] OF REAL;        (* Long-term cumulative bias integrator *)

    (* ===================================================================================== *)
    (* 3. IN-PROCESS CONTROL (IPC) STATISTICAL BUFFER (120 SAMPLES)                          *)
    (* ===================================================================================== *)
    arWeightBuffer_mg               : ARRAY[1..120] OF REAL;       (* Rolling circular FIFO buffer of net weight *)
    iBufferHead                     : INT := 1;                    (* Current write pointer in circular buffer *)
    iBufferCount                    : INT := 0;                    (* Current valid sample count in buffer *)
    rSumGrossWeight_mg              : REAL;                        (* Cumulative sum of buffer samples *)
    rSumSqGrossWeight_mg            : REAL;                        (* Cumulative sum of squares for variance *)
    rTargetNetWeight_mg             : REAL;                        (* Nominal mass: TargetVol * Density * 1000 *)
    rUpperSpecLimit_mg              : REAL;                        (* USL: TargetNetWeight + Tolerance *)
    rLowerSpecLimit_mg              : REAL;                        (* LSL: TargetNetWeight - Tolerance *)

    (* ===================================================================================== *)
    (* 4. TRIPLE MODULAR REDUNDANCY (2oo3) VOTING DATA STRUCTURES                            *)
    (* ===================================================================================== *)
    (* Starwheel Optical Resolvers *)
    rStarwheelVoted_deg             : REAL;
    bStarwheel_TMR_ChA_Valid        : BOOL := TRUE;
    bStarwheel_TMR_ChB_Valid        : BOOL := TRUE;
    bStarwheel_TMR_ChC_Valid        : BOOL := TRUE;
    tStarwheelDiscrepancyTimer      : TIME := T#0MS;
    bStarwheelDegraded              : BOOL;

    (* Tare EMFR Load Cell *)
    rTareVoted_mg                   : REAL;
    bTare_TMR_ChA_Valid             : BOOL := TRUE;
    bTare_TMR_ChB_Valid             : BOOL := TRUE;
    bTare_TMR_ChC_Valid             : BOOL := TRUE;
    tTareDiscrepancyTimer           : TIME := T#0MS;
    bTareDegraded                   : BOOL;

    (* Gross EMFR Load Cell *)
    rGrossVoted_mg                  : REAL;
    bGross_TMR_ChA_Valid            : BOOL := TRUE;
    bGross_TMR_ChB_Valid            : BOOL := TRUE;
    bGross_TMR_ChC_Valid            : BOOL := TRUE;
    tGrossDiscrepancyTimer          : TIME := T#0MS;
    bGrossDegraded                  : BOOL;

    (* Isolator Differential Pressure *)
    rIsolatorPressVoted_Pa          : REAL;
    bPress_TMR_ChA_Valid            : BOOL := TRUE;
    bPress_TMR_ChB_Valid            : BOOL := TRUE;
    bPress_TMR_ChC_Valid            : BOOL := TRUE;
    tPressDiscrepancyTimer          : TIME := T#0MS;
    bPressDegraded                  : BOOL;

    (* Nitrogen Mass Flowmeter *)
    rN2FlowVoted_lnpm               : REAL;
    bN2Flow_TMR_ChA_Valid           : BOOL := TRUE;
    bN2Flow_TMR_ChB_Valid           : BOOL := TRUE;
    bN2Flow_TMR_ChC_Valid           : BOOL := TRUE;
    tN2DiscrepancyTimer             : TIME := T#0MS;
    bN2FlowDegraded                 : BOOL;

    (* ===================================================================================== *)
    (* 5. POCKET TRACKING SHIFT REGISTERS ACROSS MONOBLOCK SECTORS                           *)
    (* ===================================================================================== *)
    (* Shift register length: 48 pockets covering Tare, Fill, Gross, N2, Stopper, Crimp, Reject *)
    arPocketVialPresent             : ARRAY[1..48] OF BOOL;        (* Vial presence bit per starwheel pocket *)
    arPocketTareWeight_mg           : ARRAY[1..48] OF REAL;        (* Registered tare weight per pocket *)
    arPocketGrossWeight_mg          : ARRAY[1..48] OF REAL;        (* Registered gross weight per pocket *)
    arPocketDispenseChannel         : ARRAY[1..48] OF INT;         (* Dispense needle ID (1..12) allocated *)
    arPocketRejectFlag              : ARRAY[1..48] OF BOOL;        (* True if pocket contains defective vial *)
    arPocketRejectReason            : ARRAY[1..48] OF DWORD;       (* Bit-encoded reason for reject *)

    (* Rotary Stoppering Wheel 24 Pockets *)
    arStopperWheelPocketVacuum_bar  : ARRAY[1..24] OF REAL;
    arStopperWheelPocketPresent     : ARRAY[1..24] OF BOOL;

    (* Rotary Crimp Capper 16 Spindles *)
    arCrimpSpindleSealForce_N       : ARRAY[1..16] OF REAL;
    arCrimpSpindleDeflection_mm     : ARRAY[1..16] OF REAL;

    (* ===================================================================================== *)
    (* 6. FINITE STATE MACHINE INTERNAL CONTROLS & TIMERS                                    *)
    (* ===================================================================================== *)
    iFsmState                       : INT := 1;                    (* Primary state machine step *)
    iFsmPrevState                   : INT := 0;                    (* State latch for edge triggers *)
    tStateTimer                     : TIME := T#0MS;               (* Elapsed dwell time in current state *)
    tCycleStepTimer                 : TIME := T#0MS;               (* Sub-cycle microsecond time accumulator *)
    tVHP_DwellTimer                 : TIME := T#0MS;               (* VHP gassing exposure timer *)
    tAerationTimer                  : TIME := T#0MS;               (* Isolator catalytic aeration timer *)
    tCIP_CleanTimer                 : TIME := T#0MS;               (* Clean-In-Place phase duration *)
    tSIP_SterilizeTimer             : TIME := T#0MS;               (* Steam-In-Place thermal kill timer *)
    rSIP_Temperature_DegC           : REAL;                        (* Steam manifold RTD temperature *)
    bStateFirstScan                 : BOOL := TRUE;                (* Edge pulse on entry to new state *)

    (* Bottom-Up Filling Trajectory Generator Variables *)
    rTurretIndexAngle_deg           : REAL;                        (* Current modular pocket position (0..30 deg) *)
    rDimensionlessPhase_tau         : REAL;                        (* Normalized time variable (0.0 to 1.0) *)
    rPolynomialS_tau                : REAL;                        (* Normalized 5th-order position value *)
    rPolynomialV_tau                : REAL;                        (* Normalized 5th-order velocity value *)
    rLiquidLevelRise_mm             : REAL;                        (* Meniscus height computed from volume *)
    rLiquidSurfaceVelocity_mms      : REAL;                        (* Instantaneous surface velocity *)

    (* Consecutive Quality Failure Counters *)
    iConsecutiveWeightRejects       : INT := 0;
    iConsecutiveStopperRejects      : INT := 0;
    iConsecutiveCrimpRejects        : INT := 0;

    (* Loop Counters & Scratch Variables *)
    idx_i                           : INT := 1;
    idx_j                           : INT := 1;
    idx_k                           : INT := 1;
    rScratchAccum                   : REAL := 0.0;
    rGradStep                       : REAL := 0.0015;              (* MPC gradient step size *)
    bMatricesInitialized            : BOOL := FALSE;               (* One-time initialization interlock *)
END_VAR
"""
