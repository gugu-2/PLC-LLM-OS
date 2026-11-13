# rail_emu_builder/part1_decl.py

def get_part1():
    return '''FUNCTION_BLOCK FB_Rail_HighSpeed_EMU_TractionBraking_WSSP
(*
========================================================================================================================
  LUMINA AI CYBER-PHYSICAL SYSTEMS & ADVANCED INDUSTRIAL AUTOMATION ARCHITECTURE GROUP
  CRITICAL HIGH-SPEED RAIL TRANSIT & TRACTION SYSTEMS REFERENCE IMPLEMENTATION — SYNTHETIC DATASET ENGINE V7
  
  SYSTEM DESIGNATION : 350 KM/H HIGH-SPEED ELECTRIC MULTIPLE UNIT (EMU) TRACTION & BRAKING CONTROL UNIT (TCU/BCU)
  TRACTION ARCHITECTURE: DUAL 4-QUADRANT AC/DC LINE CONVERTERS & 4x 1200 kW ASYNCHRONOUS TRACTION MOTORS (FOC)
  ADHESION SUBSYSTEM   : MICROPROCESSOR WHEEL SLIP-SLIDE PROTECTION (WSSP) WITH CURTIUS-KNIFFLER NON-LINEAR OBSERVER
  CURRENT COLLECTION   : ACTIVE PNEUMATIC PANTOGRAPH CATENARY CONTACT FORCE REGULATION WITH AERODYNAMIC UPLIFT COMPENSATION
  BRAKING MANAGEMENT   : BLENDED REGENERATIVE ELECTRO-DYNAMIC (ED) & ELECTRO-PNEUMATIC (EP) BRAKING WITH AXLE DYNAMIC SHIFT
  SAFETY INTEGRITY     : IEC 61508 / EN 50126 / EN 50128 / EN 50129 SIL-4 CERTIFIED RAIL VEHICLE CONTROL ARCHITECTURE
  APPLICABLE STANDARDS : EN 50367 (CURRENT COLLECTION SYSTEMS), EN 15595 (WHEEL SLIDE PROTECTION), EN 13452 (RAILWAY BRAKING),
                         EN 50388 (POWER SUPPLY & ROLLING STOCK), UIC 541-05 (BRAKES - SPECIFICATIONS FOR WSP),
                         IEC 61375 (TRAIN COMMUNICATION NETWORK - TCN), IEC 60349 (ELECTRIC TRACTION MOTORS),
                         ISA-18.2 / IEC 62682 (MANAGEMENT OF ALARM SYSTEMS FOR THE PROCESS INDUSTRIES).
  AUTHOR               : 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
========================================================================================================================

  THEORETICAL & CYBER-PHYSICAL RAILWAY VEHICLE DYNAMICS:
  ----------------------------------------------------------------------------------------------------------------------
  1. TRAIN LONGITUDINAL MOTION & EXTENDED DAVIS RESISTANCE EQUATION:
     - The longitudinal translational dynamics of a 350 km/h High-Speed EMU trainset of total gross mass M_train [kg]
       governed by Newton's second law on arbitrary track grades and curves:
           M_eff * (dv_train / dt) = F_traction - F_braking - F_resistance - F_grade - F_curve
       where:
           M_eff = M_train * (1 + delta_rot)  (Effective inertia including rotating masses: wheelsets, gears, rotors)
           delta_rot = 0.08 to 0.12 (Rotational mass coefficient, nominal 0.10)
     - The aerodynamic and rolling mechanical resistance is formulated via the empirical Davis Equation:
           F_resistance(v) = A_davis + B_davis * v_train + C_davis * (v_train + v_wind)^2   [kN]
       where:
           A_davis : Mechanical rolling friction of steel wheel on steel rail plus bearing seal resistance [kN]
           B_davis : Flange mechanical friction, wheel-rail hunting dissipation, and track deformation losses [kN/(km/h)]
           C_davis : High-speed aerodynamic skin friction and form drag coefficient [kN/(km/h)^2]
           v_wind  : Longitudinal headwind component measured by nose cone multi-port Pitot tubes [km/h]
     - Track gradient force: F_grade = M_train * g * sin(theta_grade) approx M_train * g * (i_permille / 1000) [kN]
     - Track curvature resistance: F_curve = (6.86 / R_curve_m) * M_train * g * 10^-3 [kN] (per von Roeckl formulation).

  2. NON-LINEAR WHEEL-RAIL ADHESION MECHANICS & CURTIUS-KNIFFLER EXTENSION:
     - The tangential tractive or braking force F_adhesion transmissible at the wheel-rail contact patch (Hertzian ellipse)
       is constrained by the dynamic normal axle load F_z and the instantaneous adhesion coefficient mu(s, v):
           F_adhesion_i = mu_i(s_i, v_train) * F_z_i   [kN]
     - Relative wheel slip ratio s_i during traction and skid ratio during braking are defined as:
           s_traction_i = (omega_i * R_wheel - v_train) / max(omega_i * R_wheel, v_train, 0.1)
           s_braking_i  = (v_train - omega_i * R_wheel) / max(v_train, 0.1)
     - The classical Curtius-Kniffler empirical adhesion characteristic gives the maximum available adhesion ceiling:
           mu_max(v) = (c1 / (v_kmh + c2)) + c3
       where for dry, clean rails: c1 = 7.5, c2 = 44.0, c3 = 0.161.
       At v = 0 km/h: mu_max = 0.331; at v = 350 km/h: mu_max = 0.180.
       Under degraded rail conditions (precipitation, dew, fallen leaves, oil, crushed oxide layer), the adhesion
       boundary collapses drastically to mu_degraded in [0.03, 0.08].
     - Polach Non-Linear Micro-Slip Creep Formulation:
       The complete tangential adhesion force versus creepage curve exhibits three distinct physical regimes:
       * Stable Micro-Slip Linear Elastic Regime (s < s_crit, approx 1.0% to 2.5%):
           dmu / ds > 0; Tangential creep forces rise linearly through shear deformation of the microscopic asperities.
       * Peak Adhesion Optimum Operating Point (s = s_crit):
           dmu / ds = 0; Maximum tractive or braking effort is transmitted without macroscopic slip/slide.
       * Unstable Macroscopic Slip/Spin / Wheel Slide Skid Regime (s > s_crit):
           dmu / ds < 0; Negative slope induces runaway axle rotational acceleration (traction spin: domega/dt >> 0)
           or catastrophic wheel locking (braking lockup: omega -> 0, causing severe wheel tread flat spots).
     - The cyber-physical WSSP observer executes real-time gradient search (Extremum Seeking Control / PGD)
       to locate and track s_crit, maximizing power transfer while preventing wheel degradation.

  3. 4-QUADRANT CONVERTER (4QC) & DYNAMIC INDUCTION MOTOR VECTOR CONTROL (FOC):
     - The high-speed traction converter comprises a primary 4-Quadrant AC/DC active line converter connected to
       the 25 kV / 50 Hz secondary transformer winding, maintaining a regulated DC link bus voltage U_dc = 3000 V DC,
       followed by two high-power 3-phase PWM inverter modules driving asynchronous cage induction traction motors.
     - Synchronous d-q Frame Rotor Flux Oriented Vector Control (FOC):
       The stator currents are transformed from 3-phase stationary coordinates to orthogonal rotor-flux-aligned (d-q) frame:
           I_sd : Magnetizing flux-producing current component
           I_sq : Electromagnetic torque-producing current component
       Electromagnetic torque is decoupled:
           T_em = (3 / 2) * p * (L_m / L_r) * psi_r * I_sq   [Nm]
       where:
           p    : Motor pole pair count (p = 2)
           L_m  : Mutual magnetizing inductance [H]
           L_r  : Rotor total inductance [H]
           psi_r: Rotor flux linkage magnitude [Wb]
     - Rotor Flux Linkage Dynamics & Slip Angular Frequency:
           d(psi_r) / dt + (R_r / L_r) * psi_r = (R_r * L_m / L_r) * I_sd
           omega_slip = (R_r * L_m * I_sq) / (L_r * psi_r)   [rad/s]
           theta_e = integral(p * omega_mech + omega_slip) dt  [rad]
     - Dynamic Field Weakening Regime (Base speed v_base = 120 km/h up to maximum 350 km/h):
       Above rated base speed, the stator voltage reaches inverter saturation limit (U_s = U_s_max = sqrt(2/3) * U_dc).
       The rotor flux reference is progressively attenuated inversely with motor angular velocity:
           psi_r_ref = psi_r_nom * (v_base / max(v_train, v_base))
       This preserves inverter current controllability while operating at constant power (P = T_em * omega_mech = const).

  4. ACTIVE PNEUMATIC PANTOGRAPH-CATENARY CONTACT FORCE REGULATION:
     - High-speed current collection (EN 50367 / TSI High Speed) requires the pantograph collector head to exert a dynamic
       vertical contact force F_cat on the overhead contact wire strictly bounded between 120 N and 180 N (nominal 145 N).
     - Forces acting on the pantograph collector head:
           F_cat = F_static + F_bellows + F_aero_uplift - M_pan * (d2z_pan / dt2) - C_damp * (dz_pan / dt)
       where:
           F_static      : Calibrated static uplift preload at standstill (approx 70 N)
           F_bellows     : Pneumatic active bellows cylinder force = P_bellows * A_bellows [N]
           F_aero_uplift : Non-linear aerodynamic lift force induced by 350 km/h airflow over bow profile:
                           F_aero_uplift = 0.5 * rho_air * C_lift * A_frontal * (v_train / 3.6)^2   [N]
           M_pan         : Equivalent collector head lumped mass (approx 12.5 kg)
     - Contact Loss & Electrical Arcing Hazards:
       If F_cat drops below 60 N, microscopic contact separation occurs, triggering severe electrical arcing that
       vaporizes contact wire copper and carbon collector strips.
     - Catenary Uplift & Structural Hazards:
       If F_cat exceeds 220 N, excessive vertical uplift bends droppers, risks pantograph entanglement, and crushes wire.
     - The active electro-pneumatic pressure regulator continuously compensates aerodynamic uplift feedforward
       and regulates bellows air pressure via high-speed proportional valves.

  5. BLENDED BRAKING & DYNAMIC AXLE LOAD REDISTRIBUTION:
     - Deceleration from 350 km/h requires coordinated management of three distinct brake systems:
       1) Regenerative Electro-Dynamic (ED) Brake: Traction motors act as induction generators, returning energy to catenary.
       2) Pneumatic Friction Disc Brake: Wheel-mounted and axle-mounted ventilated sintered metal discs with calipers.
       3) Magnetic Track Brake: Auxiliary emergency high-speed eddy-current / friction rail brake.
     - Blending Hierarchy:
       Priority is given 100% to Regenerative ED braking. The pneumatic friction brake only fills the deficit
       between required total deceleration force and maximum ED capacity:
           F_ed_available = min(F_brake_demand, P_ed_max / v_train, mu_adh * F_z)
           F_ep_supplement = max(0.0, F_brake_demand - F_ed_available)
     - Dynamic Axle Load Shift (Weight Transfer):
       During deceleration a_brake [m/s2], carbody inertia induces longitudinal pitch moment transferring weight
       from the trailing axles to the leading axles:
           F_z1_dyn = F_z1_stat + M_car * abs(a_brake) * (h_cg / L_wheelbase)   [kN]  (Leading Axle Loaded)
           F_z2_dyn = F_z2_stat - M_car * abs(a_brake) * (h_cg / L_wheelbase)   [kN]  (Trailing Axle Unloaded)
       where:
           h_cg        : Center of gravity height above rail plane (approx 1.65 m)
           L_wheelbase : Bogie center-to-center distance (approx 17.5 m)
       Without dynamic load compensation, the unloaded trailing axle slips immediately into catastrophic slide!
       The BCU dynamically redistributes braking torque commands proportional to instantaneous normal load F_z_i.

  6. 8-STATE DISCRETE STATE-SPACE MODEL & EMBEDDED RECEDING-HORIZON MPC:
     - Discrete-time state-space system formulated at scan interval Ts = 5 ms (0.005 s):
           x[k+1] = A * x[k] + B * u[k] + E * d[k]
           y[k]   = C * x[k] + D * u[k]
       State Vector x (8x1):
         x[1]: Train Longitudinal True Ground Velocity                         [m/s]
         x[2]: Bogie Leading Axle 1 Angular Velocity (Linear Equivalent)       [m/s]
         x[3]: Bogie Trailing Axle 2 Angular Velocity (Linear Equivalent)      [m/s]
         x[4]: Pantograph-Catenary Dynamic Contact Force                       [N]
         x[5]: DC Link Intermediate Bus Filter Voltage                         [V]
         x[6]: Traction Motor Electromagnetic Torque Output                    [kNm]
         x[7]: Bogie Brake Cylinder Pneumatic Pressure                         [bar]
         x[8]: Dynamic Rail-Wheel Contact Patch Adhesion Coefficient           [-] (0.0 to 0.40)
       Manipulated Control Input Vector u (8x1):
         u[1]: Traction Motor d-Axis Flux Current Reference I_sd*              [A]
         u[2]: Traction Motor q-Axis Torque Current Reference I_sq*            [A]
         u[3]: 4-Quadrant AC/DC Converter PWM Pulse Modulation Depth           [%] (0.0 to 100.0)
         u[4]: Pantograph Pneumatic Bellows Pressure Regulator Servo Valve     [%] (0.0 to 100.0)
         u[5]: Regenerative Dynamic Braking Torque Command T_ed*               [kNm]
         u[6]: Electro-Pneumatic Brake Cylinder Proportional Pilot Valve       [%] (0.0 to 100.0)
         u[7]: WSSP High-Speed Pneumatic Vent / Dump Solenoid PWM Duty         [%] (0.0 to 100.0)
         u[8]: WSSP High-Speed Pneumatic Re-Apply / Charge Solenoid PWM Duty   [%] (0.0 to 100.0)
       External Disturbance Vector d (4x1):
         d[1]: Track Topographic Gradient Slope Gravity Force                  [kN]
         d[2]: Aerodynamic Relative Headwind Aerodynamic Velocity              [m/s]
         d[3]: Catenary Supply AC Line Voltage Fluctuation                     [kV]
         d[4]: Railhead Surface Contamination Adhesion Suppression Factor      [-] (0.0=Wet/Leaves, 1.0=Dry)
*)
VAR_INPUT
    (* ============================================================================================== *)
    (* MASTER SYSTEM ENABLES, RUN COMMANDS & SIL-4 SAFETY SIGNALS                                     *)
    (* ============================================================================================== *)
    bSystemEnable                       : BOOL;     (* Master Control Power Permissive & Hardware Interlock *)
    bTractionEnableCmd                  : BOOL;     (* Driver / ATO Master Traction Enable Demand *)
    bBrakingEnableCmd                   : BOOL;     (* Driver / ATO Master Braking Enable Demand *)
    bEmergencyBrakeLoop                 : BOOL;     (* Hardwired SIL-4 Safety Loop (1=Healthy, 0=De-energized Trip) *)
    bAlarmAcknowledge                   : BOOL;     (* Operator Alarm Acknowledge Pushbutton / HMI Trigger *)
    bAlarmReset                         : BOOL;     (* Master Alarm Reset Pushbutton / HMI Trigger *)
    
    (* ============================================================================================== *)
    (* DRIVER CABIN & AUTOMATIC TRAIN OPERATION (ATO) COMMANDS WITH BRACKETED UNITS                  *)
    (* ============================================================================================== *)
    rDriverTractionNotch_pct            : REAL;     (* Driver Cab Master Controller Traction Notch Demand [%] *)
    rDriverBrakeNotch_pct               : REAL;     (* Driver Cab Master Controller Braking Notch Demand [%] *)
    rATOSpeedSetpoint_kmh               : REAL;     (* Automatic Train Operation (ATO) Cruise Speed Target [km/h] *)
    rCatenaryLineVoltage_kV             : REAL;     (* 25 kV AC 50 Hz Overhead Catenary Supply Voltage [kV] *)
    rCatenaryLineFrequency_Hz           : REAL;     (* Catenary Supply AC Fundamental Frequency [Hz] *)
    rMainReservoirPressure_bar          : REAL;     (* Pneumatic Supply Main Air Reservoir (MR) Pressure [bar] *)
    rBrakePipePressure_bar              : REAL;     (* UIC Pneumatic Brake Pipe (BP) Continuous Pressure [bar] *)
    rTrackGradient_permille             : REAL;     (* Track Topography Elevation Gradient / Slope [permille] *)
    rAmbientAirTemp_degC                : REAL;     (* External Ambient Trackside Air Temperature [deg C] *)
    rRelativeHeadwindSpeed_ms           : REAL;     (* Nose Cone Pitot Tube Relative Aerodynamic Wind Velocity [m/s] *)
    bNeutralSectionBeaconDetected       : BOOL;     (* Trackside Balise / Transponder Neutral Section Approach Signal *)
    bTrackSandingManualCmd              : BOOL;     (* Driver Cab Manual Railhead Sanding Injection Request *)
    
    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) PRIMARY INSTRUMENTATION CHANNELS                           *)
    (* ============================================================================================== *)
    (* Train Ground Velocity Triplicate Sources *)
    rDopplerRadarSpeed_kmh              : REAL;     (* True Ground Velocity Non-Contact Doppler Microwave Radar [km/h] *)
    rWheelTachoSpeed_W1_kmh             : REAL;     (* Bogie Leading Axle 1 High-Resolution Optical Pulse Encoder [km/h] *)
    rWheelTachoSpeed_W2_kmh             : REAL;     (* Bogie Trailing Axle 2 High-Resolution Optical Pulse Encoder [km/h] *)
    
    (* Bogie Leading Axle 1 Speed Sensor Triplet *)
    rAxleSpeed_A1_ChA_rpm               : REAL;     (* Axle 1 Optical Tacho Encoder Sensor Channel A [rpm] *)
    rAxleSpeed_A1_ChB_rpm               : REAL;     (* Axle 1 Optical Tacho Encoder Sensor Channel B [rpm] *)
    rAxleSpeed_A1_ChC_rpm               : REAL;     (* Axle 1 Optical Tacho Encoder Sensor Channel C [rpm] *)
    
    (* Bogie Trailing Axle 2 Speed Sensor Triplet *)
    rAxleSpeed_A2_ChA_rpm               : REAL;     (* Axle 2 Optical Tacho Encoder Sensor Channel A [rpm] *)
    rAxleSpeed_A2_ChB_rpm               : REAL;     (* Axle 2 Optical Tacho Encoder Sensor Channel B [rpm] *)
    rAxleSpeed_A2_ChC_rpm               : REAL;     (* Axle 2 Optical Tacho Encoder Sensor Channel C [rpm] *)
    
    (* Pantograph Catenary Dynamic Contact Force Triplet *)
    rPantoContactForce_ChA_N            : REAL;     (* Pantograph Carbon Collector Head Load Cell A [N] *)
    rPantoContactForce_ChB_N            : REAL;     (* Pantograph Carbon Collector Head Load Cell B [N] *)
    rPantoContactForce_ChC_N            : REAL;     (* Pantograph Carbon Collector Head Load Cell C [N] *)
    
    (* DC Link Intermediate Bus Differential Voltage Triplet *)
    rDCLinkVoltage_ChA_V                : REAL;     (* DC Link Capacitor Bank Differential Voltage Probe A [V] *)
    rDCLinkVoltage_ChB_V                : REAL;     (* DC Link Capacitor Bank Differential Voltage Probe B [V] *)
    rDCLinkVoltage_ChC_V                : REAL;     (* DC Link Capacitor Bank Differential Voltage Probe C [V] *)
    
    (* Bogie Brake Cylinder Pneumatic Pressure Transducer Triplet *)
    rBrakeCylinderPressure_ChA_bar      : REAL;     (* Bogie Brake Cylinder Pressure Transducer Channel A [bar] *)
    rBrakeCylinderPressure_ChB_bar      : REAL;     (* Bogie Brake Cylinder Pressure Transducer Channel B [bar] *)
    rBrakeCylinderPressure_ChC_bar      : REAL;     (* Bogie Brake Cylinder Pressure Transducer Channel C [bar] *)
    
    (* ============================================================================================== *)
    (* TRACTION MOTOR & CONVERTER THERMAL MONITORING CHANNELS                                         *)
    (* ============================================================================================== *)
    rTractionMotorTemp_U_degC           : REAL;     (* Asynchronous Traction Motor Stator Phase U RTD [deg C] *)
    rTractionMotorTemp_V_degC           : REAL;     (* Asynchronous Traction Motor Stator Phase V RTD [deg C] *)
    rTractionMotorTemp_W_degC           : REAL;     (* Asynchronous Traction Motor Stator Phase W RTD [deg C] *)
    rInverterIGBTTemp_Max_degC          : REAL;     (* Power Traction Converter Heat Pipe Heat Sink Peak Temp [deg C] *)
    rTransformerOilTemp_degC            : REAL;     (* Main 25 kV Traction Transformer Oil Sump Temperature [deg C] *)
END_VAR
VAR_OUTPUT
    (* ============================================================================================== *)
    (* MASTER SYSTEM STATUS & PRODUCTION SUPERVISORY FLAGS                                           *)
    (* ============================================================================================== *)
    bTCUReady                           : BOOL;     (* Traction Control Unit Master Permissive Ready Status *)
    bBCUReady                           : BOOL;     (* Brake Control Unit Master Permissive Ready Status *)
    bEmergencyTripActive                : BOOL;     (* SIL-4 Emergency Brake Hardware Trip Latched Status *)
    nOperationalState                   : INT;      (* Current 14-Stage Master FSM Operational Stage Code (0 to 13) *)
    
    (* ============================================================================================== *)
    (* 2oo3 TMR VALIDATED SENSOR VALUES & INTEGRATED METRICS                                          *)
    (* ============================================================================================== *)
    rVotedTrainSpeed_kmh                : REAL;     (* 2oo3 TMR Voted Master True Ground Longitudinal Velocity [km/h] *)
    rVotedAxleSpeed_A1_rpm              : REAL;     (* 2oo3 TMR Voted Bogie Axle 1 Rotational Velocity [rpm] *)
    rVotedAxleSpeed_A2_rpm              : REAL;     (* 2oo3 TMR Voted Bogie Axle 2 Rotational Velocity [rpm] *)
    rVotedPantoForce_N                  : REAL;     (* 2oo3 TMR Voted Pantograph Catenary Dynamic Contact Force [N] *)
    rVotedDCLinkVoltage_V               : REAL;     (* 2oo3 TMR Voted DC Link Intermediate Capacitor Bus Voltage [V] *)
    rVotedBrakeCylPressure_bar          : REAL;     (* 2oo3 TMR Voted Bogie Brake Cylinder Pneumatic Pressure [bar] *)
    rObservedAdhesionCoeff              : REAL;     (* Curtius-Kniffler Dynamic Rail-Wheel Friction Observer Output [-] *)
    rEstimatedWheelSlip_A1_pct          : REAL;     (* Bogie Axle 1 Real-Time Slip / Skid Ratio [%] (-100 to +100) *)
    rEstimatedWheelSlip_A2_pct          : REAL;     (* Bogie Axle 2 Real-Time Slip / Skid Ratio [%] (-100 to +100) *)
    rTrainAcceleration_ms2              : REAL;     (* Real-Time Differentiated Vehicle Acceleration [m/s2] *)
    
    (* ============================================================================================== *)
    (* TRACTION INVERTER & 4-QUADRANT CONVERTER ACTUATOR COMMANDS                                     *)
    (* ============================================================================================== *)
    rTractionTorqueCommand_kNm          : REAL;     (* Traction Inverter Total Electromagnetic Torque Command [kNm] *)
    rRegenerativeBrakeTorque_kNm        : REAL;     (* Dynamic Blended Regenerative ED Brake Torque Command [kNm] *)
    rInverterModulationIndex_pct        : REAL;     (* 4-Quadrant Line Converter PWM Modulation Depth [%] (0 to 100) *)
    rInverterFundamentalFreq_Hz         : REAL;     (* Traction Inverter Stator Fundamental Drive Frequency [Hz] *)
    rFluxCurrentCommand_Isd_A           : REAL;     (* Vector Control Magnetizing Direct Axis Current Command [A] *)
    rTorqueCurrentCommand_Isq_A         : REAL;     (* Vector Control Torque Quadrature Axis Current Command [A] *)
    
    (* ============================================================================================== *)
    (* BLENDED PNEUMATIC BRAKE & PANTOGRAPH ACTUATOR COMMANDS                                         *)
    (* ============================================================================================== *)
    rPneumaticBrakePressure_SP_bar      : REAL;     (* Electro-Pneumatic Relay Valve Cylinder Pressure Target [bar] *)
    rPantoBellowsPressure_bar           : REAL;     (* Active Pantograph Pneumatic Upward Lift Bellows Pressure [bar] *)
    bWSSPDumpValveCmd_A1                : BOOL;     (* WSSP High-Speed Pneumatic Vent / Dump Solenoid Axle 1 *)
    bWSSPApplyValveCmd_A1               : BOOL;     (* WSSP High-Speed Pneumatic Re-Apply Solenoid Axle 1 *)
    bWSSPDumpValveCmd_A2                : BOOL;     (* WSSP High-Speed Pneumatic Vent / Dump Solenoid Axle 2 *)
    bWSSPApplyValveCmd_A2               : BOOL;     (* WSSP High-Speed Pneumatic Re-Apply Solenoid Axle 2 *)
    bRailheadSandingActive              : BOOL;     (* Pneumatic Railhead Sand Delivery Solenoid Valve Command *)
    bVCBCloseCommand                    : BOOL;     (* 25 kV Vacuum Circuit Breaker (VCB) Main High-Voltage Switch Cmd *)
    bPantographRaiseCommand             : BOOL;     (* Electro-Pneumatic Pantograph Upward Raise Solenoid Cmd *)
    
    (* ============================================================================================== *)
    (* BIT-PACKED STATUS WORDS & ISA-18.2 ALARM GROUPS                                               *)
    (* ============================================================================================== *)
    dwTractionStatusWord                : DWORD;    (* 32-Bit TCU Subsystem Status & Control Mode Bitmask *)
    dwBrakingStatusWord                 : DWORD;    (* 32-Bit BCU Blended Brake Status & EP Actuator Bitmask *)
    dwWSSPStatusWord                    : DWORD;    (* 32-Bit Wheel Slip-Slide Protection State & Diagnostics *)
    dwAlarmDiagnostics_1                : DWORD;    (* 32-Bit ISA-18.2 Priority 1 & 2 Critical Alarm Bitmask *)
    dwAlarmDiagnostics_2                : DWORD;    (* 32-Bit ISA-18.2 Priority 3 Advisory & Warning Bitmask *)
    bAlarmGroupHighHigh_DCOvervoltage   : BOOL;     (* Priority 1 DC Link Bus Voltage Exceeds Upper Trip Limit *)
    bAlarmGroupLowLow_DCUndervoltage    : BOOL;     (* Priority 1 DC Link Bus Voltage Collapsed Below Minimum *)
    bAlarmGroupHigh_InverterOvercurrent : BOOL;     (* Priority 1 Inverter Stator Output Phase Peak Overcurrent *)
    bAlarmGroupHigh_MotorOvertemp       : BOOL;     (* Priority 2 Traction Motor Winding High-Temp Trip *)
    bAlarmGroup_WheelSlipSlideExcessive : BOOL;     (* Priority 2 Wheel Macro-Slip / Skid Runaway Trip *)
    bAlarmGroup_PantographContactLost   : BOOL;     (* Priority 2 Catenary Contact Force Loss / Arcing Warning *)
    bAlarmGroup_BrakePneumaticDepleted  : BOOL;     (* Priority 1 Main Reservoir Air Pressure Depleted Below Safety *)
END_VAR
VAR
    (* ============================================================================================== *)
    (* SYSTEM CONSTANTS & TIMING PARAMETERS                                                           *)
    (* ============================================================================================== *)
    T_CYCLE_SEC                         : REAL := 0.005;    (* Discrete TCU/BCU Fast Scan Interval Ts = 5 ms [s] *)
    NUM_STATES                          : INT := 8;         (* Cyber-Physical State Vector Dimension *)
    NUM_INPUTS                          : INT := 8;         (* Manipulated Control Actuator Dimension *)
    NUM_DISTURBANCES                    : INT := 4;         (* External Disturbance Input Dimension *)
    HORIZON_NP                          : INT := 5;         (* Receding-Horizon Prediction Horizon Steps *)
    
    TRAIN_MASS_TARE_KG                  : REAL := 420000.0; (* 8-Car EMU Empty Tare Weight [kg] *)
    TRAIN_MASS_FULL_KG                  : REAL := 475000.0; (* 8-Car EMU Crush Load Passenger Weight [kg] *)
    BOGIE_AXLE_LOAD_STAT_KN             : REAL := 150.0;    (* Static Nominal Axle Load [kN] (approx 15.3 tonnes) *)
    WHEEL_RADIUS_NOM_M                  : REAL := 0.460;    (* New Monobloc Steel Wheel Nom Radius [m] (worn: 0.430) *)
    GEAR_RATIO                          : REAL := 2.65;     (* Traction Motor to Axle Helical Gearbox Ratio *)
    MOTOR_POLE_PAIRS                    : INT := 2;         (* Induction Motor Pole Pairs (4-pole motor) *)
    BOGIE_WHEELBASE_M                   : REAL := 2.50;     (* Bogie Axle-to-Axle Wheelbase Distance [m] *)
    CARBODY_CG_HEIGHT_M                 : REAL := 1.65;     (* Center of Gravity Height Above Rail Plane [m] *)
    
    (* ============================================================================================== *)
    (* DISCRETE STATE-SPACE MATRICES & OBSERVER VARIABLES                                             *)
    (* x[k+1] = A * x[k] + B * u[k] + E * d[k]                                                        *)
    (* y[k]   = C * x[k] + D * u[k]                                                                   *)
    (* ============================================================================================== *)
    a_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* State Transition Matrix A (8x8) *)
    b_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* Input Coupling Matrix B (8x8) *)
    c_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* State Output Matrix C (8x8) *)
    d_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* Direct Feedthrough Matrix D (8x8) *)
    e_mat                               : ARRAY[1..8, 1..4] OF REAL;    (* Disturbance Coupling Matrix E (8x4) *)
    l_observer_gain                     : ARRAY[1..8] OF REAL;          (* Luenberger Observer Correction Gains *)
    
    x_state                             : ARRAY[1..8] OF REAL;          (* Estimated Cyber-Physical State x[k] *)
    x_next                              : ARRAY[1..8] OF REAL;          (* Predicted Next State Vector x[k+1] *)
    y_meas                              : ARRAY[1..8] OF REAL;          (* Filtered Output Measurement Vector y[k] *)
    u_ctrl                              : ARRAY[1..8] OF REAL;          (* Manipulated Control Input Vector u[k] *)
    d_dist                              : ARRAY[1..4] OF REAL;          (* Estimated External Disturbance Vector *)
    x_ref                               : ARRAY[1..8] OF REAL;          (* Reference State Setpoint Trajectory *)
    u_ref                               : ARRAY[1..8] OF REAL;          (* Nominal Equilibrium Actuator Command *)
    u_prev                              : ARRAY[1..8] OF REAL;          (* Previous Step Actuator Command u[k-1] *)
    bInitDone                           : BOOL := FALSE;                (* First-Scan Matrix Initialization Flag *)
    
    (* ============================================================================================== *)
    (* MODEL PREDICTIVE CONTROL (MPC) COST MATRICES & PROJECTION BOUNDS                               *)
    (* J = sum( (x - x_ref)'*Q*(x - x_ref) + (u - u_ref)'*R*(u - u_ref) + du'*S*du ) + x_N'*P*x_N     *)
    (* ============================================================================================== *)
    q_diag                              : ARRAY[1..8] OF REAL;          (* State Tracking Penalty Diagonal Q *)
    r_diag                              : ARRAY[1..8] OF REAL;          (* Actuator Effort Penalty Diagonal R *)
    s_diag                              : ARRAY[1..8] OF REAL;          (* Actuator Slew Rate Penalty Diagonal S *)
    p_diag                              : ARRAY[1..8] OF REAL;          (* Terminal State Penalty Diagonal P *)
    u_box_min                           : ARRAY[1..8] OF REAL;          (* Actuator Physical Lower Bound Box Sat *)
    u_box_max                           : ARRAY[1..8] OF REAL;          (* Actuator Physical Upper Bound Box Sat *)
    du_slew_max                         : ARRAY[1..8] OF REAL;          (* Max Allowable Actuator Slew [units/step] *)
    
    u_mpc_traj                          : ARRAY[1..5, 1..8] OF REAL;    (* Predicted Control Trajectory *)
    grad_u                              : ARRAY[1..8] OF REAL;          (* Computed Projected Gradient Vector *)
    u_tentative                         : ARRAY[1..8] OF REAL;          (* Candidate Actuator Command *)
    rMpcAlphaStep                       : REAL := 0.050;                (* PGD Optimization Gradient Step Length *)
    rTotalCostFunctional                : REAL;                         (* Accumulated Quadratic Cost J *)
    
    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT ISOLATION STRUCTURES                       *)
    (* ============================================================================================== *)
    (* Train True Ground Velocity Voting (Radar vs Wheel Tachos) *)
    rSpeed_Delta_AB                     : REAL;     (* |Radar - Wheel 1| [km/h] *)
    rSpeed_Delta_BC                     : REAL;     (* |Wheel 1 - Wheel 2| [km/h] *)
    rSpeed_Delta_CA                     : REAL;     (* |Wheel 2 - Radar| [km/h] *)
    rSpeed_DiscrepancyLimit_kmh         : REAL := 6.5;      (* Permissible Speed Discrepancy Band [km/h] *)
    rSpeed_DiscrepancyTimer_s           : REAL := 0.0;      (* Cumulative Speed Discrepancy Integrator [s] *)
    bSpeed_ChannelA_Valid               : BOOL := TRUE;     (* Radar Sensor Health Flag *)
    bSpeed_ChannelB_Valid               : BOOL := TRUE;     (* Wheel 1 Tacho Sensor Health Flag *)
    bSpeed_ChannelC_Valid               : BOOL := TRUE;     (* Wheel 2 Tacho Sensor Health Flag *)
    nSpeed_DegradedVotingMode           : INT := 3;         (* 3=2oo3, 2=1oo2 Average, 1=Single, 0=Fail-Safe *)
    
    (* Bogie Leading Axle 1 Speed Sensor Triplet *)
    rAxle1_Delta_AB                     : REAL;     (* |Encoder A - Encoder B| [rpm] *)
    rAxle1_Delta_BC                     : REAL;     (* |Encoder B - Encoder C| [rpm] *)
    rAxle1_Delta_CA                     : REAL;     (* |Encoder C - Encoder A| [rpm] *)
    rAxle1_DiscrepancyLimit_rpm         : REAL := 25.0;     (* Axle 1 Discrepancy Margin [rpm] *)
    rAxle1_DiscrepancyTimer_s           : REAL := 0.0;      (* Axle 1 Discrepancy Integrator [s] *)
    bAxle1_ChannelA_Valid               : BOOL := TRUE;     (* Axle 1 Channel A Health Flag *)
    bAxle1_ChannelB_Valid               : BOOL := TRUE;     (* Axle 1 Channel B Health Flag *)
    bAxle1_ChannelC_Valid               : BOOL := TRUE;     (* Axle 1 Channel C Health Flag *)
    nAxle1_DegradedVotingMode           : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)
    
    (* Bogie Trailing Axle 2 Speed Sensor Triplet *)
    rAxle2_Delta_AB                     : REAL;     (* |Encoder A - Encoder B| [rpm] *)
    rAxle2_Delta_BC                     : REAL;     (* |Encoder B - Encoder C| [rpm] *)
    rAxle2_Delta_CA                     : REAL;     (* |Encoder C - Encoder A| [rpm] *)
    rAxle2_DiscrepancyLimit_rpm         : REAL := 25.0;     (* Axle 2 Discrepancy Margin [rpm] *)
    rAxle2_DiscrepancyTimer_s           : REAL := 0.0;      (* Axle 2 Discrepancy Integrator [s] *)
    bAxle2_ChannelA_Valid               : BOOL := TRUE;     (* Axle 2 Channel A Health Flag *)
    bAxle2_ChannelB_Valid               : BOOL := TRUE;     (* Axle 2 Channel B Health Flag *)
    bAxle2_ChannelC_Valid               : BOOL := TRUE;     (* Axle 2 Channel C Health Flag *)
    nAxle2_DegradedVotingMode           : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)
    
    (* Pantograph Catenary Dynamic Contact Force Load Cells Triplet *)
    rPanto_Delta_AB                     : REAL;     (* |Load Cell A - Load Cell B| [N] *)
    rPanto_Delta_BC                     : REAL;     (* |Load Cell B - Load Cell C| [N] *)
    rPanto_Delta_CA                     : REAL;     (* |Load Cell C - Load Cell A| [N] *)
    rPanto_DiscrepancyLimit_N           : REAL := 20.0;     (* Panto Load Cell Margin [N] *)
    rPanto_DiscrepancyTimer_s           : REAL := 0.0;      (* Panto Discrepancy Integrator [s] *)
    bPanto_ChannelA_Valid               : BOOL := TRUE;     (* Panto Channel A Health Flag *)
    bPanto_ChannelB_Valid               : BOOL := TRUE;     (* Panto Channel B Health Flag *)
    bPanto_ChannelC_Valid               : BOOL := TRUE;     (* Panto Channel C Health Flag *)
    nPanto_DegradedVotingMode           : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)
    
    (* DC Link Intermediate Bus Differential Voltage Probes Triplet *)
    rDCLink_Delta_AB                    : REAL;     (* |Voltage Probe A - Probe B| [V] *)
    rDCLink_Delta_BC                    : REAL;     (* |Voltage Probe B - Probe C| [V] *)
    rDCLink_Delta_CA                    : REAL;     (* |Voltage Probe C - Probe A| [V] *)
    rDCLink_DiscrepancyLimit_V          : REAL := 75.0;     (* DC Link Probe Margin [V] *)
    rDCLink_DiscrepancyTimer_s          : REAL := 0.0;      (* DC Link Discrepancy Integrator [s] *)
    bDCLink_ChannelA_Valid              : BOOL := TRUE;     (* DC Link Probe A Health Flag *)
    bDCLink_ChannelB_Valid              : BOOL := TRUE;     (* DC Link Probe B Health Flag *)
    bDCLink_ChannelC_Valid              : BOOL := TRUE;     (* DC Link Probe C Health Flag *)
    nDCLink_DegradedVotingMode          : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)
    
    (* Bogie Brake Cylinder Pressure Transducer Triplet *)
    rBrakeCyl_Delta_AB                  : REAL;     (* |Pressure A - Pressure B| [bar] *)
    rBrakeCyl_Delta_BC                  : REAL;     (* |Pressure B - Pressure C| [bar] *)
    rBrakeCyl_Delta_CA                  : REAL;     (* |Pressure C - Pressure A| [bar] *)
    rBrakeCyl_DiscrepancyLimit_bar      : REAL := 0.25;     (* Brake Pressure Margin [bar] *)
    rBrakeCyl_DiscrepancyTimer_s        : REAL := 0.0;      (* Brake Pressure Discrepancy Integrator [s] *)
    bBrakeCyl_ChannelA_Valid            : BOOL := TRUE;     (* Brake Pressure Channel A Health *)
    bBrakeCyl_ChannelB_Valid            : BOOL := TRUE;     (* Brake Pressure Channel B Health *)
    bBrakeCyl_ChannelC_Valid            : BOOL := TRUE;     (* Brake Pressure Channel C Health *)
    nBrakeCyl_DegradedVotingMode        : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)
    
    (* ============================================================================================== *)
    (* CURTIUS-KNIFFLER ADHESION OBSERVER & MICRO-SLIP EXTREMUM SEEKING                               *)
    (* ============================================================================================== *)
    rCurtius_c1                         : REAL := 7.5;      (* Curtius-Kniffler Constant c1 *)
    rCurtius_c2                         : REAL := 44.0;     (* Curtius-Kniffler Constant c2 *)
    rCurtius_c3                         : REAL := 0.161;    (* Curtius-Kniffler Constant c3 *)
    rTheoreticalAdhesionLimit           : REAL := 0.33;     (* Maximum Theoretical Available Adhesion [-] *)
    rObservedAdhesionRaw                : REAL := 0.25;     (* Instantaneous Observed Adhesion Ratio [-] *)
    rAdhesionFilterCoeff                : REAL := 0.12;     (* Low-Pass Filter Weight for Adhesion Observer *)
    rAxle1_LinearVelocity_ms            : REAL := 0.0;      (* Bogie Axle 1 Linear Peripheral Speed [m/s] *)
    rAxle2_LinearVelocity_ms            : REAL := 0.0;      (* Bogie Axle 2 Linear Peripheral Speed [m/s] *)
    rTrainSpeed_ms                      : REAL := 0.0;      (* True Ground Velocity in SI Units [m/s] *)
    rAxle1_SlipVelocity_ms              : REAL := 0.0;      (* Peripheral Velocity Delta Axle 1 [m/s] *)
    rAxle2_SlipVelocity_ms              : REAL := 0.0;      (* Peripheral Velocity Delta Axle 2 [m/s] *)
    rAxle1_SlipRatio                    : REAL := 0.0;      (* Dimensionless Slip Ratio s1 [-] *)
    rAxle2_SlipRatio                    : REAL := 0.0;      (* Dimensionless Slip Ratio s2 [-] *)
    rSlipRatio_Prev_A1                  : REAL := 0.0;      (* Previous Scan Slip Ratio Axle 1 *)
    rAdhesion_Prev_A1                   : REAL := 0.0;      (* Previous Scan Adhesion Axle 1 *)
    rAdhesionGradient_dMu_ds_A1         : REAL := 0.0;      (* Numerical Gradient dMu / ds Axle 1 *)
    rMicroSlipTarget                    : REAL := 0.018;    (* Optimal Micro-Slip Operating Target (1.8%) *)
    
    (* ============================================================================================== *)
    (* ASYNCHRONOUS TRACTION MOTOR VECTOR CONTROL (FOC) PARAMETERS                                    *)
    (* ============================================================================================== *)
    MOTOR_STATOR_RES_OHM                : REAL := 0.0245;   (* Stator Winding Phase Resistance Rs [Ohm] *)
    MOTOR_ROTOR_RES_OHM                 : REAL := 0.0192;   (* Rotor Cage Winding Resistance Rr [Ohm] *)
    MOTOR_MUTUAL_IND_H                  : REAL := 0.0084;   (* Magnetizing Inductance Lm [H] *)
    MOTOR_STATOR_IND_H                  : REAL := 0.0089;   (* Stator Total Inductance Ls [H] *)
    MOTOR_ROTOR_IND_H                   : REAL := 0.0088;   (* Rotor Total Inductance Lr [H] *)
    MOTOR_SIGMA_LEAKAGE                 : REAL := 0.065;    (* Total Leakage Factor sigma = 1 - Lm^2/(Ls*Lr) *)
    MOTOR_RATED_CURRENT_RMS_A           : REAL := 520.0;    (* Rated Stator Phase Current [A rms] *)
    MOTOR_PEAK_TORQUE_KNM               : REAL := 6.80;     (* Maximum Transient Motoring Torque per Axle [kNm] *)
    MOTOR_BASE_SPEED_KMH                : REAL := 120.0;    (* Field Weakening Base Speed Corner [km/h] *)
    
    rRotorFluxEstimate_Wb               : REAL := 1.25;     (* Estimated Rotor Flux Magnitude psi_r [Wb] *)
    rRotorFluxTarget_Wb                 : REAL := 1.25;     (* Rotor Flux Command psi_r* [Wb] *)
    rSlipAngularFreq_rads               : REAL := 0.0;      (* Slip Angular Frequency omega_slip [rad/s] *)
    rElectricalStatorFreq_rads          : REAL := 0.0;      (* Stator Electrical Frequency omega_e [rad/s] *)
    rRotorMechanicalSpeed_rads          : REAL := 0.0;      (* Rotor Mechanical Angular Velocity [rad/s] *)
    rStatorElectricalAngle_rad          : REAL := 0.0;      (* Integrated Rotor Flux Field Angle theta_e [rad] *)
    
    (* Stator d-q Current PI Regulators *)
    rIsd_IntegralError                  : REAL := 0.0;      (* Direct Axis Current PI Integrator [A*s] *)
    rIsq_IntegralError                  : REAL := 0.0;      (* Quadrature Axis Current PI Integrator [A*s] *)
    rKp_Isd                             : REAL := 1.45;     (* Direct Axis Current Proportional Gain *)
    rKi_Isd                             : REAL := 45.0;     (* Direct Axis Current Integral Gain *)
    rKp_Isq                             : REAL := 1.45;     (* Quadrature Axis Current Proportional Gain *)
    rKi_Isq                             : REAL := 45.0;     (* Quadrature Axis Current Integral Gain *)
    rVsd_Decoupled_V                    : REAL := 0.0;      (* Direct Axis Stator Voltage Demand [V] *)
    rVsq_Decoupled_V                    : REAL := 0.0;      (* Quadrature Axis Stator Voltage Demand [V] *)
    
    (* 4QC DC Link Voltage PI Regulator *)
    rDCLink_VoltageTarget_V             : REAL := 3000.0;   (* Regulated Intermediate DC Bus Voltage [V] *)
    rDCLink_VoltageError                : REAL := 0.0;      (* DC Link Error Voltage [V] *)
    rDCLink_IntegralError               : REAL := 0.0;      (* DC Link PI Voltage Integrator [V*s] *)
    rKp_DCLink                          : REAL := 0.85;     (* DC Link Proportional Voltage Gain *)
    rKi_DCLink                          : REAL := 12.0;     (* DC Link Integral Voltage Gain *)
    
    (* ============================================================================================== *)
    (* ACTIVE PANTOGRAPH PNEUMATIC FORCE REGULATION PARAMETERS                                        *)
    (* ============================================================================================== *)
    PANTO_BELLOWS_AREA_M2               : REAL := 0.0314;   (* Pneumatic Upward Lift Bellows Area [m2] *)
    PANTO_HEAD_MASS_KG                  : REAL := 12.5;     (* Lumped Pantograph Collector Head Mass [kg] *)
    PANTO_AERO_DRAG_AREA_M2             : REAL := 0.420;    (* Pantograph Head Frontal Aerodynamic Area [m2] *)
    PANTO_AERO_LIFT_COEFF               : REAL := 0.285;    (* Dynamic Aerodynamic Lift Coefficient C_lift *)
    AIR_DENSITY_KG_M3                   : REAL := 1.205;    (* Standard Ambient Air Density rho [kg/m3] *)
    
    rPantoTargetForce_N                 : REAL := 145.0;    (* High-Speed TSI Nominal Contact Force Target [N] *)
    rPantoAeroUplift_N                  : REAL := 0.0;      (* Calculated High-Speed Aerodynamic Lift [N] *)
    rPantoForceError_N                  : REAL := 0.0;      (* Contact Force Closed-Loop Error [N] *)
    rPantoForceIntegral_Ns              : REAL := 0.0;      (* Contact Force PI Integrator [N*s] *)
    rKp_PantoForce                      : REAL := 0.42;     (* Pantograph Proportional Gain [bar/N] *)
    rKi_PantoForce                      : REAL := 1.85;     (* Pantograph Integral Gain [bar/(N*s)] *)
    rPantoOutputPressure_bar            : REAL := 3.20;     (* Command Pressure to Proportional Pneumatic Valve [bar] *)
    
    (* ============================================================================================== *)
    (* BLENDED BRAKING & DYNAMIC AXLE LOAD REDISTRIBUTION VARIABLES                                   *)
    (* ============================================================================================== *)
    rTotalBrakingDemand_kN              : REAL := 0.0;      (* Master Trainset Total Braking Force Demand [kN] *)
    rED_BrakeAvailable_kN               : REAL := 0.0;      (* Real-Time Available Regenerative Dynamic Braking [kN] *)
    rED_BrakeDelivered_kN               : REAL := 0.0;      (* Actual Commanded Regenerative Braking Effort [kN] *)
    rEP_BrakeRequired_kN                : REAL := 0.0;      (* Pneumatic Friction Brake Required Supplement [kN] *)
    rAxle1_DynamicLoad_kN               : REAL := 150.0;    (* Dynamic Vertical Normal Load Axle 1 [kN] *)
    rAxle2_DynamicLoad_kN               : REAL := 150.0;    (* Dynamic Vertical Normal Load Axle 2 [kN] *)
    rAxleWeightShift_kN                 : REAL := 0.0;      (* Calculated Inertial Dynamic Axle Load Transfer [kN] *)
    rAxle1_BrakeForce_Target_kN         : REAL := 0.0;      (* Axle 1 Dynamic Normal Load Proportional Brake Force [kN] *)
    rAxle2_BrakeForce_Target_kN         : REAL := 0.0;      (* Axle 2 Dynamic Normal Load Proportional Brake Force [kN] *)
    rBrakeCylinder_SP_Axle1_bar         : REAL := 0.0;      (* Commanded Pressure Brake Cylinder Axle 1 [bar] *)
    rBrakeCylinder_SP_Axle2_bar         : REAL := 0.0;      (* Commanded Pressure Brake Cylinder Axle 2 [bar] *)
    
    (* ============================================================================================== *)
    (* WHEEL SLIP-SLIDE PROTECTION (WSSP) 4-PHASE STATE VARIABLES PER AXLE (UIC 541-05 / EN 15595)   *)
    (* Phase 0: Normal Adhesion, Phase 1: Pressure Hold, Phase 2: Rapid Vent, Phase 3: Stepped Apply   *)
    (* ============================================================================================== *)
    nWSSP_Phase_Axle1                   : INT := 0;         (* Axle 1 WSSP Valve Cycle State (0 to 3) *)
    nWSSP_Phase_Axle2                   : INT := 0;         (* Axle 2 WSSP Valve Cycle State (0 to 3) *)
    rWSSP_PhaseTimer_A1_s               : REAL := 0.0;      (* Axle 1 State Dwell Timer [s] *)
    rWSSP_PhaseTimer_A2_s               : REAL := 0.0;      (* Axle 2 State Dwell Timer [s] *)
    rAxle1_AngularDecel_rads2           : REAL := 0.0;      (* Axle 1 Instantaneous Angular Deceleration [rad/s2] *)
    rAxle2_AngularDecel_rads2           : REAL := 0.0;      (* Axle 2 Instantaneous Angular Deceleration [rad/s2] *)
    rAxle1_LinearDecel_ms2              : REAL := 0.0;      (* Axle 1 Equivalent Linear Peripheral Decel [m/s2] *)
    rAxle2_LinearDecel_ms2              : REAL := 0.0;      (* Axle 2 Equivalent Linear Peripheral Decel [m/s2] *)
    rAxle1_DecelThreshold_ms2           : REAL := 3.80;     (* WSSP Trigger Deceleration Limit (EN 15595) [m/s2] *)
    rAxle1_SlipThreshold_ms             : REAL := 1.80;     (* WSSP Trigger Slip Velocity Limit [m/s] (approx 6.5 km/h) *)
    nWSSP_InterventionCount_A1          : DINT := 0;        (* Cumulative Anti-Skid Intervention Counter Axle 1 *)
    nWSSP_InterventionCount_A2          : DINT := 0;        (* Cumulative Anti-Skid Intervention Counter Axle 2 *)
    rLowAdhesionAccumulator_s           : REAL := 0.0;      (* Persistent Low Adhesion Integrator for Sanding [s] *)
    
    (* ============================================================================================== *)
    (* DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM) VARIABLES                                    *)
    (* ============================================================================================== *)
    nFSM_CurrentState                   : INT := 0;         (* Current 14-Stage FSM State Code (0 to 13) *)
    nFSM_PreviousState                  : INT := 0;         (* Previous Scan FSM State Code *)
    rFSM_StateTimer_s                   : REAL := 0.0;      (* Time Spent in Current FSM Stage [s] *)
    bStateTransitionTrigger             : BOOL := FALSE;    (* One-Shot State Transition Handshake Flag *)
    
    (* ============================================================================================== *)
    (* ISA-18.2 MULTI-TIERED ALARM THRESHOLDS & HYSTERESIS                                            *)
    (* ============================================================================================== *)
    ALARM_HH_DC_VOLTAGE_V               : REAL := 3800.0;   (* DC Link Overvoltage High-High SIL-4 Trip [V] *)
    ALARM_H_DC_VOLTAGE_V                : REAL := 3550.0;   (* DC Link Overvoltage High Warning [V] *)
    ALARM_L_DC_VOLTAGE_V                : REAL := 2500.0;   (* DC Link Undervoltage Low Warning [V] *)
    ALARM_LL_DC_VOLTAGE_V               : REAL := 2200.0;   (* DC Link Undervoltage Low-Low Traction Trip [V] *)
    ALARM_HYST_DC_VOLTAGE_V             : REAL := 40.0;     (* DC Link Voltage Clearance Deadband [V] *)
    
    ALARM_H_STATOR_CURRENT_A            : REAL := 1150.0;   (* Peak Stator Phase Current High Limit [A] *)
    ALARM_HH_STATOR_CURRENT_A           : REAL := 1350.0;   (* Peak Stator Current High-High Instantaneous Trip [A] *)
    
    ALARM_H_MOTOR_TEMP_DEGC             : REAL := 165.0;    (* Traction Motor Winding High Temp Warning [deg C] *)
    ALARM_HH_MOTOR_TEMP_DEGC            : REAL := 185.0;    (* Traction Motor Winding High-High Thermal Trip [deg C] *)
    ALARM_HYST_MOTOR_TEMP_DEGC          : REAL := 8.0;      (* Motor Temperature Clearance Deadband [deg C] *)
    
    ALARM_HH_PANTO_FORCE_N              : REAL := 220.0;    (* Catenary Uplift High-High Safety Limit [N] *)
    ALARM_LL_PANTO_FORCE_N              : REAL := 55.0;     (* Catenary Contact Loss Arcing Low-Low Trip [N] *)
    ALARM_HYST_PANTO_FORCE_N            : REAL := 12.0;     (* Pantograph Force Clearance Deadband [N] *)
    
    ALARM_LL_MAIN_RES_BAR               : REAL := 6.50;     (* Main Reservoir Low-Low Pressure Braking Trip [bar] *)
    ALARM_L_MAIN_RES_BAR                : REAL := 7.20;     (* Main Reservoir Low Pressure Compressor Start [bar] *)
    ALARM_HYST_MAIN_RES_BAR             : REAL := 0.35;     (* Main Reservoir Pressure Deadband [bar] *)
    
    rPrevTrainSpeed_kmh                 : REAL := 0.0;      (* Previous Scan Train Speed for Acceleration Deriv *)
    rPrevAxleSpeed_A1_rpm               : REAL := 0.0;      (* Previous Scan Axle 1 Speed for Decel Deriv *)
    rPrevAxleSpeed_A2_rpm               : REAL := 0.0;      (* Previous Scan Axle 2 Speed for Decel Deriv *)
    
    (* Internal Loop Iterators & Diagnostic Scratchpad *)
    i                                   : INT := 1;         (* General Purpose Inner Loop Matrix Row Index *)
    j                                   : INT := 1;         (* General Purpose Inner Loop Matrix Col Index *)
    k                                   : INT := 1;         (* General Purpose Prediction Horizon Horizon Index *)
    rScratchAccum                       : REAL := 0.0;      (* Matrix Math Scalar Accumulator Variable *)
    rScratchDiff                        : REAL := 0.0;      (* Temporary Floating Point Math Scratchpad *)
    rScratchNorm                        : REAL := 0.0;      (* Euclidean Norm Evaluation Scratchpad *)
END_VAR
'''
