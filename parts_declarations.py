# parts_declarations.py
# VAR_INPUT, VAR_OUTPUT, VAR declarations for FB_Semiconductor_Lithography_WaferStage_NanometerPositioning

def get_var_input():
    return """VAR_INPUT
    (* ====================================================================================================
       MASTER SUPERVISORY COMMANDS & REAL-TIME INTERLOCK SIGNALS
       ==================================================================================================== *)
    bEnable : BOOL; (* [bool] Master stage servo enable command *)
    bResetAlarms : BOOL; (* [bool] Alarm acknowledge and trip reset command *)
    bStartAutoCycle : BOOL; (* [bool] Automated step-and-scan lithography cycle start command *)
    bEmergencyStop : BOOL; (* [bool] Hardwired failsafe emergency drop command *)
    bTwinScanSwapAck : BOOL; (* [bool] TwinScan dual stage exchange trajectory clearance acknowledge *)
    bChuckVacuumPermissive : BOOL; (* [bool] Lithography main chamber high vacuum permissive (< 1e-6 mbar) *)
    bEuvInterlockClear : BOOL; (* [bool] EUV illumination source safety shutter interlock permissive *)
    bWaferRobotPresent : BOOL; (* [bool] Wafer transfer robot end-effector presence sensor at handoff station *)

    (* ====================================================================================================
       MULTI-AXIS HETERODYNE LASER INTERFEROMETER 2oo3 POSITION CHANNELS (SUB-0.1 nm RESOLUTION)
       ==================================================================================================== *)
    rLaserPosX_ChA : LREAL; (* [nm] Multi-axis heterodyne laser interferometer Ch A X position *)
    rLaserPosX_ChB : LREAL; (* [nm] Multi-axis heterodyne laser interferometer Ch B X position *)
    rLaserPosX_ChC : LREAL; (* [nm] Multi-axis heterodyne laser interferometer Ch C X position *)
    rLaserPosY_ChA : LREAL; (* [nm] Multi-axis heterodyne laser interferometer Ch A Y position *)
    rLaserPosY_ChB : LREAL; (* [nm] Multi-axis heterodyne laser interferometer Ch B Y position *)
    rLaserPosY_ChC : LREAL; (* [nm] Multi-axis heterodyne laser interferometer Ch C Y position *)
    rLaserPosZ_ChA : LREAL; (* [nm] Multi-axis heterodyne laser interferometer Ch A Z position *)
    rLaserPosZ_ChB : LREAL; (* [nm] Multi-axis heterodyne laser interferometer Ch B Z position *)
    rLaserPosZ_ChC : LREAL; (* [nm] Multi-axis heterodyne laser interferometer Ch C Z position *)

    (* ====================================================================================================
       CAPACITIVE FINE GAP SENSOR 2oo3 CHANNELS (LEVITATION & CHUCK TILT)
       ==================================================================================================== *)
    rCapacitiveGapZ1_ChA : REAL; (* [um] Capacitive gap sensor 1 Ch A vertical levitation gap *)
    rCapacitiveGapZ1_ChB : REAL; (* [um] Capacitive gap sensor 1 Ch B vertical levitation gap *)
    rCapacitiveGapZ1_ChC : REAL; (* [um] Capacitive gap sensor 1 Ch C vertical levitation gap *)
    rCapacitiveGapZ2_ChA : REAL; (* [um] Capacitive gap sensor 2 Ch A vertical levitation gap *)
    rCapacitiveGapZ2_ChB : REAL; (* [um] Capacitive gap sensor 2 Ch B vertical levitation gap *)
    rCapacitiveGapZ2_ChC : REAL; (* [um] Capacitive gap sensor 2 Ch C vertical levitation gap *)
    rCapacitiveGapZ3_ChA : REAL; (* [um] Capacitive gap sensor 3 Ch A vertical levitation gap *)
    rCapacitiveGapZ3_ChB : REAL; (* [um] Capacitive gap sensor 3 Ch B vertical levitation gap *)
    rCapacitiveGapZ3_ChC : REAL; (* [um] Capacitive gap sensor 3 Ch C vertical levitation gap *)

    (* ====================================================================================================
       OPTICAL CHUCK WAFER GLOBAL ALIGNMENT MARK 2oo3 SENSOR CHANNELS
       ==================================================================================================== *)
    rOpticalAlignMarkX_ChA : REAL; (* [nm] Optical mark sensor Ch A wafer global alignment error X *)
    rOpticalAlignMarkX_ChB : REAL; (* [nm] Optical mark sensor Ch B wafer global alignment error X *)
    rOpticalAlignMarkX_ChC : REAL; (* [nm] Optical mark sensor Ch C wafer global alignment error X *)
    rOpticalAlignMarkY_ChA : REAL; (* [nm] Optical mark sensor Ch A wafer global alignment error Y *)
    rOpticalAlignMarkY_ChB : REAL; (* [nm] Optical mark sensor Ch B wafer global alignment error Y *)
    rOpticalAlignMarkY_ChC : REAL; (* [nm] Optical mark sensor Ch C wafer global alignment error Y *)

    (* ====================================================================================================
       WAFER BACKSIDE HELIUM PRESSURE TRANSDUCER 2oo3 SENSOR CHANNELS
       ==================================================================================================== *)
    rHeBacksidePress_ChA : REAL; (* [mbar] Wafer chuck backside helium pressure transducer Ch A *)
    rHeBacksidePress_ChB : REAL; (* [mbar] Wafer chuck backside helium pressure transducer Ch B *)
    rHeBacksidePress_ChC : REAL; (* [mbar] Wafer chuck backside helium pressure transducer Ch C *)

    (* ====================================================================================================
       ELECTROSTATIC CHUCK (ESC), THERMAL METROLOGY & REACTION COUNTER-MASS FEEDBACK
       ==================================================================================================== *)
    rChuckTempActual_mK : REAL; (* [mK] Wafer electrostatic chuck temperature deviation from 22.000 deg C *)
    rEscClampVoltagePos_V : REAL; (* [V] Bipolar electrostatic chuck positive electrode voltage *)
    rEscClampVoltageNeg_V : REAL; (* [V] Bipolar electrostatic chuck negative electrode voltage *)
    rEscLeakageCurrent_uA : REAL; (* [uA] Bipolar ESC dielectric ceramic leakage current *)
    rCounterMassPosX_mm : REAL; (* [mm] Reaction force counter-mass linear encoder X position *)
    rCounterMassPosY_mm : REAL; (* [mm] Reaction force counter-mass linear encoder Y position *)
    rCounterMassVelX_mms : REAL; (* [mm/s] Reaction force counter-mass tachometer velocity X *)
    rCounterMassVelY_mms : REAL; (* [mm/s] Reaction force counter-mass tachometer velocity Y *)

    (* ====================================================================================================
       SETPOINT TRAJECTORY PROFILE GENERATOR INPUTS (UP TO 15g ACCELERATION = 150 m/s2)
       ==================================================================================================== *)
    rTargetPosX_nm : LREAL; (* [nm] Trajectory profile generator target position X *)
    rTargetPosY_nm : LREAL; (* [nm] Trajectory profile generator target position Y *)
    rTargetPosZ_nm : LREAL; (* [nm] Trajectory profile generator target position Z *)
    rTargetVelX_mms : REAL; (* [mm/s] Trajectory profile generator target scanning velocity X *)
    rTargetVelY_mms : REAL; (* [mm/s] Trajectory profile generator target stepping velocity Y *)
    rTargetAccX_mps2 : REAL; (* [m/s2] Trajectory profile generator scanning acceleration X up to 150 m/s2 *)
    rTargetAccY_mps2 : REAL; (* [m/s2] Trajectory profile generator stepping acceleration Y up to 150 m/s2 *)
    rTargetJerkX_mps3 : REAL; (* [m/s3] Trajectory profile generator jerk feedforward X *)

    (* ====================================================================================================
       TWINSCAN DUAL STAGE SEPARATION & INTERFEROMETER HARDWARE INTERRUPTS
       ==================================================================================================== *)
    rTwinScanStageDistance_mm : REAL; (* [mm] Real-time laser distance between Wafer Stage 1 and Wafer Stage 2 *)
    bFringeSlipDetected_Ext : BOOL; (* [bool] External FPGA optical fringe slip detection pulse *)
    tCycleTime_ms : REAL; (* [ms] Discrete PLC execution scan cycle time (nominal 1.0 ms) *)
END_VAR"""

def get_var_output():
    return """VAR_OUTPUT
    (* ====================================================================================================
       SYSTEM PERMISSIVES & PROCESS STATUS FLAGS
       ==================================================================================================== *)
    bServoReady : BOOL; (* [bool] Wafer stage 6-DOF magnetic levitation closed-loop ready *)
    bInPositionNanometer : BOOL; (* [bool] Stage in-target nanometer window (3-sigma < 1.2 nm) *)
    bExposurePermissive : BOOL; (* [bool] EUV dose trigger permissive to illumination source *)
    bRobotLoadPermissive : BOOL; (* [bool] End-effector vacuum robot permissive to load wafer *)
    bRobotUnloadPermissive : BOOL; (* [bool] End-effector vacuum robot permissive to unload wafer *)
    bTwinScanSwapPermissive : BOOL; (* [bool] Stage exchange trajectory clearance handshake *)
    bEscClamped : BOOL; (* [bool] Wafer electrostatic chuck fully clamped with verified force *)
    bHeThermalStabilized : BOOL; (* [bool] Backside helium pressure and chuck temperature stabilized *)
    nActiveFsmStage : INT; (* [enum] Current active stage in deterministic 14-stage FSM (0-14) *)

    (* ====================================================================================================
       6-DOF LORENTZ ACTUATOR ARRAY COIL COMMANDS (8 CHANNELS: 2 X, 2 Y, 4 Z)
       ==================================================================================================== *)
    rActuatorCurrent_X1_A : REAL; (* [A] Commanded Lorentz actuator coil current X1 *)
    rActuatorCurrent_X2_A : REAL; (* [A] Commanded Lorentz actuator coil current X2 *)
    rActuatorCurrent_Y1_A : REAL; (* [A] Commanded Lorentz actuator coil current Y1 *)
    rActuatorCurrent_Y2_A : REAL; (* [A] Commanded Lorentz actuator coil current Y2 *)
    rActuatorCurrent_Z1_A : REAL; (* [A] Commanded Lorentz actuator coil current Z1 *)
    rActuatorCurrent_Z2_A : REAL; (* [A] Commanded Lorentz actuator coil current Z2 *)
    rActuatorCurrent_Z3_A : REAL; (* [A] Commanded Lorentz actuator coil current Z3 *)
    rActuatorCurrent_Z4_A : REAL; (* [A] Commanded Lorentz actuator coil current Z4 *)

    (* ====================================================================================================
       DYNAMIC REACTION FORCE COUNTER-MASS MOMENTUM BALANCING COMMANDS
       ==================================================================================================== *)
    rCounterMassForceCmdX_N : REAL; (* [N] Momentum balancing force command X to counter-mass linear motors *)
    rCounterMassForceCmdY_N : REAL; (* [N] Momentum balancing force command Y to counter-mass linear motors *)

    (* ====================================================================================================
       WAFER CHUCK HELIUM THERMAL & BIPOLAR ESC VOLTAGE DEMANDS
       ==================================================================================================== *)
    rHeGasSupplyValveCmd_pct : REAL; (* [%] Wafer backside helium gas proportional piezo-valve demand *)
    rHeGasVentValveCmd_pct : REAL; (* [%] Wafer backside helium gas exhaust turbo-drag valve demand *)
    rEscHighVoltageSupplyCmd_V : REAL; (* [V] Commanded bipolar electrostatic clamping power supply *)
    rCalculatedClampForce_N : REAL; (* [N] Real-time calculated electrostatic clamping force *)

    (* ====================================================================================================
       OBSERVER ESTIMATED STATES & METROLOGY STATISTICAL JITTER
       ==================================================================================================== *)
    rEstimatedPosErrorX_nm : REAL; (* [nm] Real-time tracking error X estimated by Kalman observer *)
    rEstimatedPosErrorY_nm : REAL; (* [nm] Real-time tracking error Y estimated by Kalman observer *)
    rEstimatedPosErrorZ_nm : REAL; (* [nm] Real-time tracking error Z estimated by Kalman observer *)
    rEstimatedTiltRx_urad : REAL; (* [urad] Estimated wafer chuck tilt Rx around X axis *)
    rEstimatedTiltRy_urad : REAL; (* [urad] Estimated wafer chuck tilt Ry around Y axis *)
    rEstimatedYawRz_urad : REAL; (* [urad] Estimated wafer chuck yaw Rz around Z axis *)
    rMovingStdDevX_3Sigma_nm : REAL; (* [nm] Statistical 3-sigma dynamic overlay jitter along scanning axis *)
    rMovingStdDevY_3Sigma_nm : REAL; (* [nm] Statistical 3-sigma dynamic overlay jitter along cross-stepping axis *)

    (* ====================================================================================================
       BIT-PACKED PROCESS STATUS & ISA-18.2 MULTI-TIER PROCESS ALARM WORDS
       ==================================================================================================== *)
    dwMasterStatusWord : DWORD; (* [bitfield] 32-bit packed stage status word *)
    dwIsaAlarmTripHH : DWORD; (* [bitfield] ISA-18.2 Priority 1 High-High trip alarm word *)
    dwIsaAlarmWarnH : DWORD; (* [bitfield] ISA-18.2 Priority 2 High warning alarm word *)
    dwIsaAlarmTripLL : DWORD; (* [bitfield] ISA-18.2 Priority 1 Low-Low trip alarm word *)
    dwIsaAlarmWarnL : DWORD; (* [bitfield] ISA-18.2 Priority 3 Low warning alarm word *)
    dwSensorTmrFaultWord : DWORD; (* [bitfield] 2oo3 TMR voting discrepancy and fault status word *)
END_VAR"""

def get_var():
    return """VAR
    (* ====================================================================================================
       GENERAL SYSTEM SEQUENCER & LOOP VARIABLES
       ==================================================================================================== *)
    bFirstScanDone : BOOL := FALSE; (* First execution cycle initialization flag *)
    i : INT := 0; (* Primary matrix/vector row iterator *)
    j : INT := 0; (* Primary matrix/vector column iterator *)
    k : INT := 0; (* Secondary vector iterator *)
    m : INT := 0; (* Tertiary dimension iterator *)
    n : INT := 0; (* Quaternary iterator *)
    p : INT := 0; (* Prediction horizon step iterator *)
    iter : INT := 0; (* PGD optimization iteration iterator *)

    (* ====================================================================================================
       CYBER-PHYSICAL CONSTANTS & MECHATRONIC PARAMETERS
       ==================================================================================================== *)
    cStageMass_kg : REAL := 32.500; (* High-NA wafer chuck moving mass [kg] *)
    cCounterMass_kg : REAL := 260.000; (* Reaction force counter-mass moving mass [kg] *)
    cInertiaIxx : REAL := 0.420; (* Rotational moment of inertia around X axis [kg*m2] *)
    cInertiaIyy : REAL := 0.450; (* Rotational moment of inertia around Y axis [kg*m2] *)
    cInertiaIzz : REAL := 0.850; (* Rotational moment of inertia around Z axis [kg*m2] *)
    cActuatorConstantKf : REAL := 28.500; (* Lorentz motor force constant [N/A] *)
    cMaxCoilCurrent_A : REAL := 25.000; (* Lorentz coil maximum continuous current limit [A] *)
    cMinCoilCurrent_A : REAL := -25.000; (* Lorentz coil minimum continuous current limit [A] *)
    cMaxCoilSlewRate_A_ms : REAL := 5.000; (* Lorentz coil maximum current slew rate [A/ms] *)

    (* ====================================================================================================
       DISCRETE STATE-SPACE MATRICES & OBSERVER STATE VECTORS (18 STATES, 6 INPUTS, 6 OUTPUTS)
       States 1..6: Rigid body positions (X, Y, Z, Rx, Ry, Rz)
       States 7..12: Rigid body velocities (Vx, Vy, Vz, Wx, Wy, Wz)
       States 13..14: Flexible mirror structural bending mode 1 (450 Hz)
       States 15..16: Flexible mirror structural bending mode 2 (820 Hz)
       States 17..18: Flexible mirror structural bending mode 3 (1250 Hz)
       ==================================================================================================== *)
    aMatA : ARRAY[1..18, 1..18] OF REAL; (* Discrete state transition matrix A at Ts = 1.0 ms *)
    aMatB : ARRAY[1..18, 1..6] OF REAL; (* Discrete input distribution matrix B *)
    aMatC : ARRAY[1..6, 1..18] OF REAL; (* Discrete measurement output matrix C *)
    aMatD : ARRAY[1..6, 1..6] OF REAL; (* Discrete direct feedthrough matrix D *)
    aMatL : ARRAY[1..18, 1..6] OF REAL; (* Steady-state Kalman observer gain matrix L *)
    aMatAlloc : ARRAY[1..8, 1..6] OF REAL; (* Generalized 6-DOF force to 8 Lorentz coils allocation matrix *)
    aStateX : ARRAY[1..18] OF REAL; (* Estimated state vector at current scan step *)
    aStateX_Pred : ARRAY[1..18] OF REAL; (* A-priori state prediction vector *)
    aStateX_Next : ARRAY[1..18] OF REAL; (* Propagated next state vector *)
    aOutputY_Est : ARRAY[1..6] OF REAL; (* Estimated sensor output vector *)
    aOutputY_Meas : ARRAY[1..6] OF REAL; (* Voted sensor measurement vector *)
    aInnovResid : ARRAY[1..6] OF REAL; (* Observer innovation residual vector *)
    aForceCmd6Dof : ARRAY[1..6] OF REAL; (* Optimized 6-DOF generalized force/torque command vector *)

    (* ====================================================================================================
       MODEL PREDICTIVE CONTROL (MPC) MATRICES & RECEDING-HORIZON BUFFERS (Np = 4, Nc = 2)
       ==================================================================================================== *)
    aMatQ : ARRAY[1..6, 1..6] OF REAL; (* State error penalty weighting matrix Q *)
    aMatR : ARRAY[1..6, 1..6] OF REAL; (* Control effort penalty weighting matrix R *)
    aMatS : ARRAY[1..6, 1..6] OF REAL; (* Actuator slew rate penalty weighting matrix S *)
    aMatP : ARRAY[1..6, 1..6] OF REAL; (* Terminal state penalty weighting matrix P *)
    aMpcControlU : ARRAY[1..6] OF REAL; (* Optimal control command for current cycle *)
    aMpcControlU_Prev : ARRAY[1..6] OF REAL; (* Previous cycle control command for slew rate limiting *)
    aMpcDeltaU : ARRAY[1..6] OF REAL; (* Control rate of change vector *)
    aMpcSeqU : ARRAY[1..2, 1..6] OF REAL; (* Projected control sequence over control horizon Nc = 2 *)
    aMpcGradU : ARRAY[1..2, 1..6] OF REAL; (* Gradient of quadratic cost functional with respect to U *)
    aMpcPredX : ARRAY[1..4, 1..6] OF REAL; (* Predicted rigid body states over prediction horizon Np = 4 *)
    aMpcRefX : ARRAY[1..4, 1..6] OF REAL; (* Reference trajectory profile over prediction horizon Np = 4 *)
    rPgdStepSize : REAL := 0.00850; (* Projected Gradient Descent optimization step size *)
    nPgdIterations : INT := 6; (* Number of unrolled PGD optimization iterations per scan *)

    (* ====================================================================================================
       2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES & DISCREPANCY TIMERS
       ==================================================================================================== *)
    rTmrVoted_LaserX : REAL; (* Voted Laser Interferometer X position [nm] *)
    rTmrVoted_LaserY : REAL; (* Voted Laser Interferometer Y position [nm] *)
    rTmrVoted_LaserZ : REAL; (* Voted Laser Interferometer Z position [nm] *)
    rTmrVoted_CapZ1 : REAL; (* Voted Capacitive Gap Sensor Z1 [um] *)
    rTmrVoted_CapZ2 : REAL; (* Voted Capacitive Gap Sensor Z2 [um] *)
    rTmrVoted_CapZ3 : REAL; (* Voted Capacitive Gap Sensor Z3 [um] *)
    rTmrVoted_OptAlignX : REAL; (* Voted Optical Alignment Mark X [nm] *)
    rTmrVoted_OptAlignY : REAL; (* Voted Optical Alignment Mark Y [nm] *)
    rTmrVoted_HePress : REAL; (* Voted Backside Helium Pressure [mbar] *)

    rTmrTol_LaserPos : REAL := 1.500; (* Laser position discrepancy tolerance [nm] *)
    rTmrTol_CapGap : REAL := 0.250; (* Capacitive gap discrepancy tolerance [um] *)
    rTmrTol_OptAlign : REAL := 3.000; (* Optical mark discrepancy tolerance [nm] *)
    rTmrTol_HePress : REAL := 1.200; (* Backside helium pressure discrepancy tolerance [mbar] *)

    tTmrTimer_LaserX_A : REAL := 0.0; (* Discrepancy accumulation timer Laser X Channel A [s] *)
    tTmrTimer_LaserX_B : REAL := 0.0; (* Discrepancy accumulation timer Laser X Channel B [s] *)
    tTmrTimer_LaserX_C : REAL := 0.0; (* Discrepancy accumulation timer Laser X Channel C [s] *)
    tTmrTimer_LaserY_A : REAL := 0.0; (* Discrepancy accumulation timer Laser Y Channel A [s] *)
    tTmrTimer_LaserY_B : REAL := 0.0; (* Discrepancy accumulation timer Laser Y Channel B [s] *)
    tTmrTimer_LaserY_C : REAL := 0.0; (* Discrepancy accumulation timer Laser Y Channel C [s] *)
    tTmrTimer_LaserZ_A : REAL := 0.0; (* Discrepancy accumulation timer Laser Z Channel A [s] *)
    tTmrTimer_LaserZ_B : REAL := 0.0; (* Discrepancy accumulation timer Laser Z Channel B [s] *)
    tTmrTimer_LaserZ_C : REAL := 0.0; (* Discrepancy accumulation timer Laser Z Channel C [s] *)

    tTmrTimer_CapZ1_A : REAL := 0.0; (* Discrepancy accumulation timer Cap Z1 Channel A [s] *)
    tTmrTimer_CapZ1_B : REAL := 0.0; (* Discrepancy accumulation timer Cap Z1 Channel B [s] *)
    tTmrTimer_CapZ1_C : REAL := 0.0; (* Discrepancy accumulation timer Cap Z1 Channel C [s] *)
    tTmrTimer_CapZ2_A : REAL := 0.0; (* Discrepancy accumulation timer Cap Z2 Channel A [s] *)
    tTmrTimer_CapZ2_B : REAL := 0.0; (* Discrepancy accumulation timer Cap Z2 Channel B [s] *)
    tTmrTimer_CapZ2_C : REAL := 0.0; (* Discrepancy accumulation timer Cap Z2 Channel C [s] *)
    tTmrTimer_CapZ3_A : REAL := 0.0; (* Discrepancy accumulation timer Cap Z3 Channel A [s] *)
    tTmrTimer_CapZ3_B : REAL := 0.0; (* Discrepancy accumulation timer Cap Z3 Channel B [s] *)
    tTmrTimer_CapZ3_C : REAL := 0.0; (* Discrepancy accumulation timer Cap Z3 Channel C [s] *)

    tTmrTimer_OptX_A : REAL := 0.0; (* Discrepancy accumulation timer Opt Align X Channel A [s] *)
    tTmrTimer_OptX_B : REAL := 0.0; (* Discrepancy accumulation timer Opt Align X Channel B [s] *)
    tTmrTimer_OptX_C : REAL := 0.0; (* Discrepancy accumulation timer Opt Align X Channel C [s] *)
    tTmrTimer_OptY_A : REAL := 0.0; (* Discrepancy accumulation timer Opt Align Y Channel A [s] *)
    tTmrTimer_OptY_B : REAL := 0.0; (* Discrepancy accumulation timer Opt Align Y Channel B [s] *)
    tTmrTimer_OptY_C : REAL := 0.0; (* Discrepancy accumulation timer Opt Align Y Channel C [s] *)

    tTmrTimer_He_A : REAL := 0.0; (* Discrepancy accumulation timer Helium Pressure Channel A [s] *)
    tTmrTimer_He_B : REAL := 0.0; (* Discrepancy accumulation timer Helium Pressure Channel B [s] *)
    tTmrTimer_He_C : REAL := 0.0; (* Discrepancy accumulation timer Helium Pressure Channel C [s] *)

    cTmrMaxTripTime_s : REAL := 0.005; (* Discrepancy timer fault trip threshold [s] (5.0 ms) *)

    bTmrHealthy_LaserX_A : BOOL := TRUE;
    bTmrHealthy_LaserX_B : BOOL := TRUE;
    bTmrHealthy_LaserX_C : BOOL := TRUE;
    bTmrHealthy_LaserY_A : BOOL := TRUE;
    bTmrHealthy_LaserY_B : BOOL := TRUE;
    bTmrHealthy_LaserY_C : BOOL := TRUE;
    bTmrHealthy_LaserZ_A : BOOL := TRUE;
    bTmrHealthy_LaserZ_B : BOOL := TRUE;
    bTmrHealthy_LaserZ_C : BOOL := TRUE;

    bTmrHealthy_CapZ1_A : BOOL := TRUE;
    bTmrHealthy_CapZ1_B : BOOL := TRUE;
    bTmrHealthy_CapZ1_C : BOOL := TRUE;
    bTmrHealthy_CapZ2_A : BOOL := TRUE;
    bTmrHealthy_CapZ2_B : BOOL := TRUE;
    bTmrHealthy_CapZ2_C : BOOL := TRUE;
    bTmrHealthy_CapZ3_A : BOOL := TRUE;
    bTmrHealthy_CapZ3_B : BOOL := TRUE;
    bTmrHealthy_CapZ3_C : BOOL := TRUE;

    bTmrHealthy_OptX_A : BOOL := TRUE;
    bTmrHealthy_OptX_B : BOOL := TRUE;
    bTmrHealthy_OptX_C : BOOL := TRUE;
    bTmrHealthy_OptY_A : BOOL := TRUE;
    bTmrHealthy_OptY_B : BOOL := TRUE;
    bTmrHealthy_OptY_C : BOOL := TRUE;

    bTmrHealthy_He_A : BOOL := TRUE;
    bTmrHealthy_He_B : BOOL := TRUE;
    bTmrHealthy_He_C : BOOL := TRUE;

    (* ====================================================================================================
       GRAZING-INCIDENCE LASER FOCUS & LEVELING 9-POINT GRID REGISTERS
       ==================================================================================================== *)
    aFocusGridZ_nm : ARRAY[1..3, 1..3] OF REAL; (* 9-spot wafer surface elevation grid [nm] *)
    rFocusPolyC0 : REAL := 0.0; (* 2nd-order surface fit constant term [nm] *)
    rFocusPolyCx : REAL := 0.0; (* 2nd-order surface fit linear X gradient [nm/mm] *)
    rFocusPolyCy : REAL := 0.0; (* 2nd-order surface fit linear Y gradient [nm/mm] *)
    rFocusPolyCxx : REAL := 0.0; (* 2nd-order surface fit quadratic X curvature [nm/mm2] *)
    rFocusPolyCyy : REAL := 0.0; (* 2nd-order surface fit quadratic Y curvature [nm/mm2] *)
    rFocusPolyCxy : REAL := 0.0; (* 2nd-order surface fit cross-torsion curvature [nm/mm2] *)
    rFocusZCorrection_nm : REAL := 0.0; (* Computed focus compensation Z setpoint [nm] *)
    rFocusTiltRxCorrection_urad : REAL := 0.0; (* Computed leveling Rx tilt compensation [urad] *)
    rFocusTiltRyCorrection_urad : REAL := 0.0; (* Computed leveling Ry tilt compensation [urad] *)

    (* ====================================================================================================
       WAFER ELECTROSTATIC CHUCK (ESC) & THERMAL HELIUM BACKSIDE COOLING DYNAMICS
       ==================================================================================================== *)
    rHePressTarget_mbar : REAL := 15.000; (* Target backside helium pressure [mbar] *)
    rHePressError_mbar : REAL := 0.0; (* Backside helium pressure regulation error [mbar] *)
    rHePressIntegral_mbar_s : REAL := 0.0; (* Helium pressure PI controller anti-windup integrator *)
    rHeThermalCond_W_m2K : REAL := 1850.0; (* Effective microscopic gas gap thermal conductance [W/m2*K] *)
    rChuckTempTarget_mK : REAL := 0.000; (* Target chuck temperature deviation setpoint [mK] *)
    rChuckThermalDrift_nm : REAL := 0.0; (* Real-time wafer thermal expansion correction along diameter [nm] *)
    rEscClampingForce_N : REAL := 0.0; (* Real-time Johnsen-Rahbek electrostatic clamping force [N] *)
    rEscResidualCharge_pct : REAL := 0.0; (* Residual dielectric polarization charge percentage [%] *)
    rEscDepolarizeTimer_s : REAL := 0.0; (* ESC bipolar depolarization timer accumulator [s] *)
    rEscTargetVoltage_V : REAL := 1500.0; (* Nominal bipolar clamping voltage magnitude [V] *)

    (* ====================================================================================================
       REACTION COUNTER-MASS DYNAMIC MOMENTUM BALANCING REGISTERS
       ==================================================================================================== *)
    rCounterMassTargetPosX_mm : REAL := 0.0; (* Counter-mass nominal position setpoint X [mm] *)
    rCounterMassTargetPosY_mm : REAL := 0.0; (* Counter-mass nominal position setpoint Y [mm] *)
    rCounterMassPosErrX_mm : REAL := 0.0; (* Counter-mass position deviation X [mm] *)
    rCounterMassPosErrY_mm : REAL := 0.0; (* Counter-mass position deviation Y [mm] *)
    rCounterMassKp : REAL := 450.0; (* Counter-mass position centering proportional gain [N/mm] *)
    rCounterMassKd : REAL := 85.0; (* Counter-mass velocity damping derivative gain [N/(mm/s)] *)

    (* ====================================================================================================
       DETERMINISTIC 15-STAGE (0 TO 14) PRODUCTION LITHOGRAPHY SEQUENCER REGISTERS
       ==================================================================================================== *)
    nFsmState : INT := 0; (* Deterministic active FSM state index (0 to 14) *)
    nFsmPrevState : INT := -1; (* Previous FSM state index for transition edge detection *)
    rFsmStageTimer_s : REAL := 0.0; (* In-stage dwell and timeout accumulator timer [s] *)
    bFsmStageEntry : BOOL := TRUE; (* One-shot stage entry strobe flag *)
    nDieIndex : INT := 0; (* Active wafer exposure die field index (1 to 96) *)
    nTotalDies : INT := 96; (* Total nominal exposure fields on 300 mm wafer *)
    bScanDirForward : BOOL := TRUE; (* Scanning direction flag: TRUE = +Y forward, FALSE = -Y reverse *)
    rExposureScanDist_mm : REAL := 33.000; (* Slit scanning travel length per die [mm] *)
    rExposureScanVel_mms : REAL := 650.000; (* Constant exposure scanning velocity [mm/s] *)
    rExposureScanAcc_mps2 : REAL := 150.000; (* Scanning acceleration ramp [m/s2] (15.3g) *)
    rDieStepDistX_mm : REAL := 26.000; (* Die-to-die stepping pitch along X axis [mm] *)
    rDieStepDistY_mm : REAL := 33.000; (* Die-to-die stepping pitch along Y axis [mm] *)

    (* ====================================================================================================
       ISA-18.2 MULTI-TIER PROCESS ALARM SETPOINTS, DEADBANDS & TRIP REGISTERS
       ==================================================================================================== *)
    cPosErrTripHH_nm : REAL := 3.000; (* Laser position tracking error High-High trip threshold [nm] *)
    cPosErrWarnH_nm : REAL := 1.500; (* Laser position tracking error High warning threshold [nm] *)
    cPosErrDeadband_nm : REAL := 0.300; (* Laser position error alarm clearance deadband [nm] *)

    cCoilCurTripHH_A : REAL := 24.500; (* Lorentz coil current High-High trip threshold [A] *)
    cCoilCurWarnH_A : REAL := 20.000; (* Lorentz coil current High warning threshold [A] *)
    cCoilCurDeadband_A : REAL := 1.000; (* Lorentz coil current clearance deadband [A] *)

    cHePressTripHH_mbar : REAL := 28.000; (* Backside helium pressure High-High trip threshold [mbar] *)
    cHePressWarnH_mbar : REAL := 20.000; (* Backside helium pressure High warning threshold [mbar] *)
    cHePressWarnL_mbar : REAL := 10.000; (* Backside helium pressure Low warning threshold [mbar] *)
    cHePressTripLL_mbar : REAL := 8.000; (* Backside helium pressure Low-Low trip threshold [mbar] *)
    cHePressDeadband_mbar : REAL := 1.000; (* Backside helium pressure clearance deadband [mbar] *)

    cEscVoltTripLL_V : REAL := 1100.000; (* ESC clamping voltage Low-Low trip threshold [V] *)
    cEscVoltWarnL_V : REAL := 1300.000; (* ESC clamping voltage Low warning threshold [V] *)
    cEscVoltDeadband_V : REAL := 50.000; (* ESC clamping voltage clearance deadband [V] *)

    cTwinScanDistTripHH_mm : REAL := 2.000; (* TwinScan stage separation collision hazard HH trip [mm] *)
    cTwinScanDistWarnH_mm : REAL := 10.000; (* TwinScan stage separation proximity warning [mm] *)
    cTwinScanDeadband_mm : REAL := 1.000; (* TwinScan separation clearance deadband [mm] *)

    cCounterMassImbalTripHH_N : REAL := 250.000; (* Momentum balance deviation HH trip [N] *)
    cCounterMassImbalWarnH_N : REAL := 150.000; (* Momentum balance deviation High warning [N] *)
    cCounterMassDeadband_N : REAL := 20.000; (* Counter-mass deviation clearance deadband [N] *)

    (* ====================================================================================================
       STATISTICAL 3-SIGMA OVERLAY JITTER CIRCULAR RING BUFFER (64 SAMPLES)
       ==================================================================================================== *)
    aJitterBufferX : ARRAY[0..63] OF REAL; (* Circular ring buffer for scanning axis tracking error X [nm] *)
    aJitterBufferY : ARRAY[0..63] OF REAL; (* Circular ring buffer for cross-stepping axis tracking error Y [nm] *)
    nJitterBufferIdx : INT := 0; (* Circular ring buffer write head index (0 to 63) *)
    bJitterBufferFull : BOOL := FALSE; (* Ring buffer saturation flag *)
    rJitterSumX : REAL := 0.0; (* Running sum of tracking error X *)
    rJitterSumY : REAL := 0.0; (* Running sum of tracking error Y *)
    rJitterSumSqX : REAL := 0.0; (* Running sum-of-squares of tracking error X *)
    rJitterSumSqY : REAL := 0.0; (* Running sum-of-squares of tracking error Y *)
    rJitterMeanX : REAL := 0.0; (* Running mean tracking error X *)
    rJitterMeanY : REAL := 0.0; (* Running mean tracking error Y *)
    rJitterVarX : REAL := 0.0; (* Running variance of tracking error X *)
    rJitterVarY : REAL := 0.0; (* Running variance of tracking error Y *)

    (* Actuator previous currents for slew-rate limiter *)
    rCoilCurPrev_X1 : REAL := 0.0;
    rCoilCurPrev_X2 : REAL := 0.0;
    rCoilCurPrev_Y1 : REAL := 0.0;
    rCoilCurPrev_Y2 : REAL := 0.0;
    rCoilCurPrev_Z1 : REAL := 0.0;
    rCoilCurPrev_Z2 : REAL := 0.0;
    rCoilCurPrev_Z3 : REAL := 0.0;
    rCoilCurPrev_Z4 : REAL := 0.0;

    (* Temporary discrepancy calculation registers *)
    rDiffAB : REAL := 0.0;
    rDiffBC : REAL := 0.0;
    rDiffCA : REAL := 0.0;
END_VAR"""

print("parts_declarations.py written successfully.")
