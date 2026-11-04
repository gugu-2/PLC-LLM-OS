# Builder for FB_Mining_SAG_BallMill_GrindingCircuit
import os, sys, json, re, uuid

def generate_header():
    return """FUNCTION_BLOCK FB_Mining_SAG_BallMill_GrindingCircuit
(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - V7 MAX-PERSONA SPECIFICATION
  CORE SECTOR    : MINING, MINERAL BENEFICIATION & HEAVY ORE COMMINUTION CIRCUITS
  APPLICATION    : COPPER-GOLD PORPHYRY PRIMARY & SECONDARY WET GRINDING CIRCUIT (4,000 DRY METRIC TONS PER HOUR)
  MILL SYSTEM    : 40-FOOT DIAMETER (12.192 m) x 25-FOOT LENGTH (7.620 m) SAG MILL WITH 28.0 MW GEARLESS RING MOTOR
  SECONDARY MILLS: TWIN 26-FOOT DIAMETER (7.925 m) x 40-FOOT LENGTH (12.192 m) OVERFLOW BALL MILLS (2 x 16.5 MW)
  FUNCTION BLOCK : FB_Mining_SAG_BallMill_GrindingCircuit
  P&ID TAGGING   : ISA-5.1 STANDARD DESIGNATION (WT, PT, TT, JT, ST, AT, LT, DT, FT SERIES 100-500)
  REDUNDANCY     : 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ACROSS PRIMARY TRANSDUCER TRIPLETS WITH DISCREPANCY TIMERS
  CYBER-PHYSICS  : 8x8 DISCRETE STATE-SPACE (Ts = 50 ms) COUPLED WITH RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC)
  ACOUSTICS      : DUAL-BAND SHELL ACOUSTIC EAR & INFRARED PYROMETRY ARRAY (TOE/SHOULDER TRAJECTORY & IMPACT ANGLE)
  BEARING LUBE   : HIGH-PRESSURE HYDROSTATIC JACKING OIL LIFT WITH DIFFERENTIAL PRESSURE CHARGE WEIGHT OBSERVER
  CLASSIFICATION : 16-HYDROCYCLONE CLUSTER MANIFOLD WITH INDIVIDUAL PNEUMATIC KNIFE-GATES & PLITT CLASSIFIER MODEL
  PARTICLE SIZE  : IN-LINE ULTRASONIC ATTENUATION SPECTROMETRY (CONTINUOUS P80 CLOSED-LOOP TARGET AT 75.0 MICRONS)
  RECIRCULATION  : PEBBLE CRUSHER CIRCUIT WITH VARIABLE-SPEED CONVEYOR & SURGE BIN MASS-BALANCE CONTROL
  SAFETY & ALARM : ISA-18.2 FIVE-TIER MULTI-PARAMETRIC ALARM ENGINE WITH 32-BIT PACKED FAULT & DIAGNOSTIC WORDS
  FSM TOPOLOGY   : 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM) WITH FROZEN CHARGE DROP PROTECTION
========================================================================================================================
  THEORETICAL AND MATHEMATICAL FOUNDATION:
  
  1. COMMINUTION MECHANICS & POWER DRAW (AUSTIN, MORRELL & BOND FORMULATIONS):
     The comminution of run-of-mine (ROM) copper-gold porphyry ore in a 40-ft SAG mill involves simultaneous impact
     breakage (cataracting charge) and attrition/abrasion (cascading charge). The gross mechanical power draw
     P_SAG (MW) of the 28 MW gearless wrap-around synchronous motor is governed by Morrell's charge motion equation:
         P_SAG = K_p * D_inside^2.5 * L_eff * rho_charge * alpha(J_c, phi_c) * sin(theta_toe)
     Where:
         D_inside    = 12.192 m (Internal diameter inside shell liners)
         L_eff       = 7.620 m (Effective grinding length)
         rho_charge  = Effective density of the dynamic charge (ore, steel balls, water slurry) [t/m3]
         J_c         = Total volumetric charge filling fraction (nominal 28.0% to 32.0% of internal volume)
         phi_c       = Fraction of theoretical critical rotational centrifuging speed N_c (68.0% to 78.0% N_c)
         theta_toe   = Grinding charge dynamic toe impact angle (rad) measured from bottom dead center (BDC).
         
  2. SHELL ACOUSTIC EAR SPECTRAL ANALYSIS & CHARGE TRAJECTORY:
     Piezoelectric dynamic acoustic transmitters positioned radially along the mill shell track sound pressure level (SPL):
     - Low-Frequency Grinding Churning Band (1.0 kHz to 3.0 kHz): Measures rock-on-rock cascading slurry bed friction.
     - High-Frequency Direct Impact Spike Band (8.0 kHz to 12.0 kHz): Measures steel ball (125 mm) direct impact on Cr-Mo
       shell liners. Excessive energy in this band (> 45 dB) causes immediate liner fracture and lifter bolt shear.
     The dynamic toe angle theta_toe and shoulder angle theta_shoulder are reconstructed online via acoustic phase:
         theta_toe = theta_toe_base + K_toe_speed * (N_mill / N_c) + K_toe_load * (W_total - W_nominal)
     Target toe angle for optimal impact-in-bed without liner damage is maintained between 40.0 deg and 45.0 deg.

  3. HYDROSTATIC TRUNNION BEARING OIL FILM LIFT & DYNAMIC CHARGE WEIGHT OBSERVER:
     The 40-ft SAG mill shell is supported by dual hydrostatic/hydrodynamic trunnion bearings. High-pressure jacking oil
     is injected through four recessed pads per trunnion at 180 to 240 bar, establishing a 140 um hydrostatic oil film:
         h_film = [ (3 * mu_oil * Q_oil * R_pad) / (P_jacking * W_pad) ]^(1/3)
     Dynamic differential pressure sensors on the feed and discharge lift pads measure total live mill mass W_SAG [tons]:
         W_SAG = (K_lift_feed * Delta_P_feed) + (K_lift_disch * Delta_P_disch) - W_tare_tare - W_hydrodynamic_wedge(N_mill)
     Permissible operating mass range: 800.0 tonnes (minimum bed protection) to 1,500.0 tonnes (structural trip limit).

  4. PLITT HYDROCYCLONE CLUSTER CLASSIFICATION & IN-LINE ULTRASONIC P80 SPECTROMETRY:
     A radial cluster of 16 Cavex 650CVX hydrocyclones classifies slurry into coarse underflow (recirculated to twin ball
     mills) and fine overflow (flotation feed). The cut size d_50c (microns) is modeled via Plitt's empirical formulation:
         d_50c = [ 50.5 * D_c^0.46 * D_i^0.60 * D_o^1.21 * exp(0.063 * C_v) ] /
                 [ D_u^0.71 * h_cyclone^0.38 * Q_slurry^0.45 * (rho_solids - rho_liq)^0.50 ]
     Where C_v is the volumetric solids concentration, Q_slurry is total cluster throughput, and D_c, D_i, D_o, D_u
     are cyclone diameter, inlet diameter, vortex finder diameter, and apex nozzle diameter.
     An in-line multi-frequency ultrasonic attenuation spectrometer measures the particle size distribution (PSD):
         ln(I_0 / I) = alpha_total(f) * x_path = sum_i [ alpha_viscous(f, r_i) + alpha_thermal(f, r_i) + alpha_scat(f, r_i) ] * V_i
     The 80% passing size P80 is continuously estimated and regulated to 75.0 um via cyclone manifold pressure and dilution.

  5. FROZEN CHARGE DETECTION & CATASTROPHIC SLUMP TRIP:
     If the mill stops with a wet ore bed, the fine slime can cement the rock/ball charge into a rigid mass adhering to
     the shell lining. Upon restarting, the "frozen charge" rides up without tumbling past the shoulder angle (310 deg)
     to the top apex (360 deg / 0 deg) before detaching and plummeting 12 meters, shattering bearings, shell, and trunnions.
     The block integrates angular rotation theta(t), motor active power, direct torque, and acoustic silence:
         IF (theta_mill > 35.0 deg) AND (rMotorTorque > 115.0%) AND (Acoustic_Toe_RMS < 5.0 dB) THEN
             TRIGGER EMERGENCY COUNTER-TORQUE FLUX BRAKE & MECHANICAL CALIPER TRIP;
         END_IF;

  6. DISCRETE 8x8 STATE-SPACE MODEL & RECEDING-HORIZON MPC:
     Sampling period Ts = 50 ms.
     State vector x = [ x1: W_SAG [t], x2: V_slurry [m3], x3: theta_toe [deg], x4: P_SAG [MW],
                        x5: L_sump [%], x6: rho_ovf [t/m3], x7: W_BM_circ [t/h], x8: P80 [um] ]^T
     Control input u = [ u1: FreshFeed [t/h], u2: FeedWater [m3/h], u3: MillSpeed [RPM], u4: PebbleFeed [t/h],
                         u5: CyclonePump [RPM], u6: SumpDilution [%], u7: ActiveCyclones [cnt], u8: BM_FeedSplit [t/h] ]^T
     Receding-horizon quadratic cost objective function:
         J = sum_{k=0}^{N_p} [ (x_{k} - x_{ref})^T Q (x_{k} - x_{ref}) ] +
             sum_{k=0}^{N_u-1} [ Delta u_{k}^T R Delta u_{k} ] +
             [ (x_{N_p} - x_{ref})^T P_term (x_{N_p} - x_{ref}) ]
     Where Q penalizes throughput loss and P80 off-spec deviation, R penalizes actuator slew rate, and P_term
     penalizes high-frequency shell liner impact damage severity.
========================================================================================================================
*)
"""

def generate_io():
    return """VAR_INPUT
    (* ========================================================================================= *)
    (* SECTION 1: TRUNNION BEARING HYDROSTATIC LIFT SENSORS (2oo3 TRIPLE MODULAR REDUNDANCY)     *)
    (* ========================================================================================= *)
    PT_FEED_TRUNNION_LIFT_101A        : REAL := 182.50;   (* Feed Trunnion Hydrostatic Lift Pad Pressure Ch A [bar] *)
    PT_FEED_TRUNNION_LIFT_101B        : REAL := 182.50;   (* Feed Trunnion Hydrostatic Lift Pad Pressure Ch B [bar] *)
    PT_FEED_TRUNNION_LIFT_101C        : REAL := 182.50;   (* Feed Trunnion Hydrostatic Lift Pad Pressure Ch C [bar] *)

    PT_DISCH_TRUNNION_LIFT_102A       : REAL := 194.20;   (* Discharge Trunnion Hydrostatic Lift Pad Pressure Ch A [bar] *)
    PT_DISCH_TRUNNION_LIFT_102B       : REAL := 194.20;   (* Discharge Trunnion Hydrostatic Lift Pad Pressure Ch B [bar] *)
    PT_DISCH_TRUNNION_LIFT_102C       : REAL := 194.20;   (* Discharge Trunnion Hydrostatic Lift Pad Pressure Ch C [bar] *)

    TT_FEED_BEARING_BABBITT_103A      : REAL := 54.80;    (* Feed Trunnion Babbitt White Metal Temp Ch A [deg C] *)
    TT_FEED_BEARING_BABBITT_103B      : REAL := 54.80;    (* Feed Trunnion Babbitt White Metal Temp Ch B [deg C] *)
    TT_FEED_BEARING_BABBITT_103C      : REAL := 54.80;    (* Feed Trunnion Babbitt White Metal Temp Ch C [deg C] *)

    TT_DISCH_BEARING_BABBITT_104A     : REAL := 58.20;    (* Discharge Trunnion Babbitt White Metal Temp Ch A [deg C] *)
    TT_DISCH_BEARING_BABBITT_104B     : REAL := 58.20;    (* Discharge Trunnion Babbitt White Metal Temp Ch B [deg C] *)
    TT_DISCH_BEARING_BABBITT_104C     : REAL := 58.20;    (* Discharge Trunnion Babbitt White Metal Temp Ch C [deg C] *)

    (* ========================================================================================= *)
    (* SECTION 2: 28 MW GEARLESS RING MOTOR (GMD) TRANSDUCERS (2oo3 TRIPLE MODULAR REDUNDANCY)  *)
    (* ========================================================================================= *)
    JT_SAG_MOTOR_POWER_MW_105A        : REAL := 22.85;    (* 28 MW Synchronous Ring Motor Active Power Ch A [MW] *)
    JT_SAG_MOTOR_POWER_MW_105B        : REAL := 22.85;    (* 28 MW Synchronous Ring Motor Active Power Ch B [MW] *)
    JT_SAG_MOTOR_POWER_MW_105C        : REAL := 22.85;    (* 28 MW Synchronous Ring Motor Active Power Ch C [MW] *)

    ST_SAG_MOTOR_SPEED_RPM_106A       : REAL := 9.18;     (* Ring Motor Dual-Channel Pulse Tachometer Ch A [rpm] *)
    ST_SAG_MOTOR_SPEED_RPM_106B       : REAL := 9.18;     (* Ring Motor Dual-Channel Pulse Tachometer Ch B [rpm] *)
    ST_SAG_MOTOR_SPEED_RPM_106C       : REAL := 9.18;     (* Ring Motor Optical Resolver Tachometer Ch C [rpm] *)

    JT_SAG_MOTOR_TORQUE_PCT_107A      : REAL := 78.40;    (* Ring Motor Direct Torque Control Telemetry Ch A [%] *)
    JT_SAG_MOTOR_TORQUE_PCT_107B      : REAL := 78.40;    (* Ring Motor Direct Torque Control Telemetry Ch B [%] *)
    JT_SAG_MOTOR_TORQUE_PCT_107C      : REAL := 78.40;    (* Ring Motor Direct Torque Control Telemetry Ch C [%] *)

    TT_SAG_STATOR_TEMP_MAX_108A       : REAL := 82.50;    (* Ring Motor Stator Winding Platinum RTD Ch A [deg C] *)
    TT_SAG_STATOR_TEMP_MAX_108B       : REAL := 82.50;    (* Ring Motor Stator Winding Platinum RTD Ch B [deg C] *)
    TT_SAG_STATOR_TEMP_MAX_108C       : REAL := 82.50;    (* Ring Motor Stator Winding Platinum RTD Ch C [deg C] *)

    ZT_SAG_WRAP_AROUND_AIRGAP_MM_109A : REAL := 14.20;    (* Rotor-Stator Electromagnetic Airgap Laser Sensor Ch A [mm] *)
    ZT_SAG_WRAP_AROUND_AIRGAP_MM_109B : REAL := 14.20;    (* Rotor-Stator Electromagnetic Airgap Laser Sensor Ch B [mm] *)
    ZT_SAG_WRAP_AROUND_AIRGAP_MM_109C : REAL := 14.20;    (* Rotor-Stator Electromagnetic Airgap Laser Sensor Ch C [mm] *)

    (* ========================================================================================= *)
    (* SECTION 3: SHELL ACOUSTIC EAR & PYROMETRY SENSORS (2oo3 TRIPLE MODULAR REDUNDANCY)       *)
    (* ========================================================================================= *)
    AT_SHELL_ACOUSTIC_TOE_DB_110A     : REAL := 74.20;    (* Shell Acoustic Microphone Array Toe Station Ch A [dB] *)
    AT_SHELL_ACOUSTIC_TOE_DB_110B     : REAL := 74.20;    (* Shell Acoustic Microphone Array Toe Station Ch B [dB] *)
    AT_SHELL_ACOUSTIC_TOE_DB_110C     : REAL := 74.20;    (* Shell Acoustic Microphone Array Toe Station Ch C [dB] *)

    AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111A:REAL := 26.50;    (* Shell Acoustic Liner Direct Impact Band (8-12 kHz) Ch A [dB] *)
    AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111B:REAL := 26.50;    (* Shell Acoustic Liner Direct Impact Band (8-12 kHz) Ch B [dB] *)
    AT_SHELL_ACOUSTIC_HIGH_FREQ_DB_111C:REAL := 26.50;    (* Shell Acoustic Liner Direct Impact Band (8-12 kHz) Ch C [dB] *)

    AT_SHELL_ACOUSTIC_LOW_FREQ_DB_112A: REAL := 84.80;    (* Shell Acoustic Grinding Churning Band (1-3 kHz) Ch A [dB] *)
    AT_SHELL_ACOUSTIC_LOW_FREQ_DB_112B: REAL := 84.80;    (* Shell Acoustic Grinding Churning Band (1-3 kHz) Ch B [dB] *)
    AT_SHELL_ACOUSTIC_LOW_FREQ_DB_112C: REAL := 84.80;    (* Shell Acoustic Grinding Churning Band (1-3 kHz) Ch B [dB] *)

    TT_SHELL_INFRARED_PYRO_113A       : REAL := 48.60;    (* Shell Surface Thermal Infrared Pyrometer Ch A [deg C] *)
    TT_SHELL_INFRARED_PYRO_113B       : REAL := 48.60;    (* Shell Surface Thermal Infrared Pyrometer Ch B [deg C] *)
    TT_SHELL_INFRARED_PYRO_113C       : REAL := 48.60;    (* Shell Surface Thermal Infrared Pyrometer Ch C [deg C] *)

    (* ========================================================================================= *)
    (* SECTION 4: COARSE ORE FEEDERS & TRUNNION PROCESS WATER INSTRUMENTATION                    *)
    (* ========================================================================================= *)
    WT_FEEDER_1_ORE_TONS_HR_114       : REAL := 1950.00;  (* Coarse Ore Stockpile Feeder #1 Weightometer [t/h] *)
    WT_FEEDER_2_ORE_TONS_HR_115       : REAL := 1950.00;  (* Coarse Ore Stockpile Feeder #2 Weightometer [t/h] *)
    FT_SAG_FEED_WATER_FLOW_M3H_116    : REAL := 1150.00;  (* SAG Mill Inlet Trunnion Process Water Magmeter [m3/h] *)
    DT_SAG_FEED_WATER_PRESS_BAR_117   : REAL := 6.20;     (* Process Water Supply Header Pressure [bar] *)

    (* ========================================================================================= *)
    (* SECTION 5: PEBBLE RECYCLE & SECONDARY CONE CRUSHER CIRCUIT                                *)
    (* ========================================================================================= *)
    WT_PEBBLE_RECYCLE_TONS_HR_118     : REAL := 380.00;   (* Pebble Port Discharge Recycle Belt Scale [t/h] *)
    ZT_PEBBLE_CONVEYOR_SPEED_MS_119   : REAL := 2.45;     (* Pebble Recycle Conveyor Belt Linear Speed [m/s] *)
    JT_PEBBLE_CRUSHER_POWER_KW_120    : REAL := 680.00;   (* Pebble Secondary Cone Crusher Motor Power [kW] *)
    ZT_PEBBLE_CRUSHER_CSS_MM_121      : REAL := 13.50;    (* Pebble Crusher Hydraulic Closed-Side Setting (CSS) [mm] *)

    (* ========================================================================================= *)
    (* SECTION 6: CYCLONE FEED SUMP & PUMP TELEMETRY (2oo3 TRIPLE MODULAR REDUNDANCY)            *)
    (* ========================================================================================= *)
    LT_CYCLONE_SUMP_LEVEL_PCT_201A    : REAL := 62.40;    (* Cyclone Feed Slurry Sump Level Radar Ch A [%] *)
    LT_CYCLONE_SUMP_LEVEL_PCT_201B    : REAL := 62.40;    (* Cyclone Feed Slurry Sump Level Guided Wave Ch B [%] *)
    LT_CYCLONE_SUMP_LEVEL_PCT_201C    : REAL := 62.40;    (* Cyclone Feed Slurry Sump Level Hydrostatic Ch C [%] *)

    DT_CYCLONE_FEED_DENSITY_SG_202A   : REAL := 1.585;    (* Cyclone Feed Slurry Nuclear Gamma Gauge Ch A [t/m3] *)
    DT_CYCLONE_FEED_DENSITY_SG_202B   : REAL := 1.585;    (* Cyclone Feed Slurry Nuclear Gamma Gauge Ch B [t/m3] *)
    DT_CYCLONE_FEED_DENSITY_SG_202C   : REAL := 1.585;    (* Cyclone Feed Slurry Nuclear Gamma Gauge Ch C [t/m3] *)

    FT_CYCLONE_FEED_SLURRY_FLOW_M3H_203A:REAL := 4650.00; (* Warman 650 MCR Pump Slurry Discharge Flow Ch A [m3/h] *)
    FT_CYCLONE_FEED_SLURRY_FLOW_M3H_203B:REAL := 4650.00; (* Warman 650 MCR Pump Slurry Discharge Flow Ch B [m3/h] *)
    FT_CYCLONE_FEED_SLURRY_FLOW_M3H_203C:REAL := 4650.00; (* Warman 650 MCR Pump Slurry Discharge Flow Ch C [m3/h] *)

    PT_CYCLONE_MANIFOLD_PRESS_KPA_204A: REAL := 105.40;   (* 16-Cyclone Cluster Manifold Slurry Pressure Ch A [kPa] *)
    PT_CYCLONE_MANIFOLD_PRESS_KPA_204B: REAL := 105.40;   (* 16-Cyclone Cluster Manifold Slurry Pressure Ch B [kPa] *)
    PT_CYCLONE_MANIFOLD_PRESS_KPA_204C: REAL := 105.40;   (* 16-Cyclone Cluster Manifold Slurry Pressure Ch C [kPa] *)

    ST_CYCLONE_FEED_PUMP_RPM_205      : REAL := 580.00;   (* Variable-Frequency Slurry Pump Shaft Tachometer [rpm] *)
    FT_SUMP_DILUTION_WATER_FLOW_M3H_206:REAL := 480.00;   (* Cyclone Feed Sump Dilution Trim Water Flowmeter [m3/h] *)

    (* 16-Cyclone Cluster Pneumatic Knife-Gate Open Feedbacks *)
    abCyclone_ValveOpen_Feedback      : ARRAY[1..16] OF BOOL := [16(TRUE)]; (* Individual knife-gate open limit switches *)
    abCyclone_RopingWarning_Feedback  : ARRAY[1..16] OF BOOL := [16(FALSE)];(* Individual cyclone underflow roping sensors *)

    (* ========================================================================================= *)
    (* SECTION 7: SECONDARY TWIN BALL MILL CIRCUITS                                              *)
    (* ========================================================================================= *)
    JT_BALLMILL_1_POWER_MW_301        : REAL := 14.85;    (* Ball Mill #1 Synchronous Motor Active Power [MW] *)
    JT_BALLMILL_2_POWER_MW_302        : REAL := 14.80;    (* Ball Mill #2 Synchronous Motor Active Power [MW] *)
    WT_BALLMILL_1_FEED_TONS_HR_303    : REAL := 1850.00;  (* Ball Mill #1 Cyclone Underflow Slurry Mass Feed [t/h] *)
    WT_BALLMILL_2_FEED_TONS_HR_304    : REAL := 1850.00;  (* Ball Mill #2 Cyclone Underflow Slurry Mass Feed [t/h] *)
    FT_BALLMILL_1_WATER_FLOW_M3H_305  : REAL := 310.00;   (* Ball Mill #1 Feed Chute Process Water Flow [m3/h] *)
    FT_BALLMILL_2_WATER_FLOW_M3H_306  : REAL := 310.00;   (* Ball Mill #2 Feed Chute Process Water Flow [m3/h] *)
    PT_BALLMILL_1_TRUNNION_LIFT_307   : REAL := 165.40;   (* Ball Mill #1 Hydrostatic Trunnion Oil Lift Pressure [bar] *)
    PT_BALLMILL_2_TRUNNION_LIFT_308   : REAL := 164.80;   (* Ball Mill #2 Hydrostatic Trunnion Oil Lift Pressure [bar] *)

    (* ========================================================================================= *)
    (* SECTION 8: PARTICLE SIZE DISTRIBUTION & PRODUCT QUALITY (2oo3 REDUNDANT TELEMETRY)        *)
    (* ========================================================================================= *)
    AT_OVERFLOW_P80_MICRONS_401A      : REAL := 75.20;    (* In-Line Ultrasonic Attenuation P80 Spectrometer Ch A [um] *)
    AT_OVERFLOW_P80_MICRONS_401B      : REAL := 75.20;    (* In-Line Ultrasonic Attenuation P80 Spectrometer Ch B [um] *)
    AT_OVERFLOW_P80_MICRONS_401C      : REAL := 75.20;    (* In-Line Ultrasonic Attenuation P80 Spectrometer Ch C [um] *)

    DT_OVERFLOW_DENSITY_SG_402A       : REAL := 1.285;    (* Final Cyclone Overflow Slurry Density Gauge Ch A [t/m3] *)
    DT_OVERFLOW_DENSITY_SG_402B       : REAL := 1.285;    (* Final Cyclone Overflow Slurry Density Gauge Ch B [t/m3] *)
    DT_OVERFLOW_DENSITY_SG_402C       : REAL := 1.285;    (* Final Cyclone Overflow Slurry Density Gauge Ch C [t/m3] *)

    FT_FINAL_PRODUCT_FLOW_M3H_403     : REAL := 3850.00;  (* Final Cyclone Overflow Slurry Flotation Feed Flow [m3/h] *)
    AT_SLURRY_PH_VALUE_404            : REAL := 10.45;    (* Comminution Pulp Lime Conditioning Slurry pH [pH] *)

    (* ========================================================================================= *)
    (* SECTION 9: DISCRETE SAFETY INTERLOCKS, PERMISSIVES & SUPERVISORY COMMANDS                 *)
    (* ========================================================================================= *)
    bEmergencyStop                    : BOOL := TRUE;     (* Plant Emergency Stop Safety Relay Chain (Active High = Healthy) *)
    bAutoSequenceEnable               : BOOL := TRUE;     (* Supervisory DCS Sequence Auto Enable Permissive *)
    bResetAlarms                      : BOOL := FALSE;    (* Operator Alarm Reset Pushbutton Command *)
    bMillGrindOutFlushCmd             : BOOL := FALSE;    (* Scheduled Charge Grind-Out & Slurry Flush Command *)
    bInchingDriveDisengaged           : BOOL := TRUE;     (* Mechanical Inching Clutch Limit Switch (TRUE = Disengaged) *)
    bLubeJackingPumpsRunning          : BOOL := TRUE;     (* High-Pressure Trunnion Jacking Oil Pumps Healthy *)
    bBallMill1Ready                   : BOOL := TRUE;     (* Secondary Ball Mill #1 Operational Permissive *)
    bBallMill2Ready                   : BOOL := TRUE;     (* Secondary Ball Mill #2 Operational Permissive *)
    bPebbleCrusherReady               : BOOL := TRUE;     (* Secondary Pebble Cone Crusher Operational Permissive *)
    bCycloneKnifeGatesPermissive      : BOOL := TRUE;     (* Compressed Air Header Pressure Permissive for Knife-Gates *)

    (* Supervisory Process Setpoints *)
    rTargetThroughput_tph             : REAL := 3900.00;  (* Supervisory Plant Fresh Ore Throughput Target [t/h] *)
    rTargetP80_microns                : REAL := 75.00;    (* Target Final Product Fineness 80% Passing Size [um] *)
    rTargetSolidsFraction_pct         : REAL := 72.50;    (* Target SAG Mill Internal Pulp Solids Weight Percentage [%] *)
    tExecutionScanTime_s              : REAL := 0.050;    (* Deterministic Task Execution Period [s] (Ts = 50 ms) *)
END_VAR
"""

def generate_output():
    return """VAR_OUTPUT
    (* ========================================================================================= *)
    (* SECTION 1: PRIMARY ACTUATOR COMMANDS & SPEED DEMANDS                                      *)
    (* ========================================================================================= *)
    rSagFeederTotalSpeedRef_pct       : REAL := 85.50;    (* Total Coarse Ore Feeder Belt VFD Speed Demand [%] *)
    rSagFeeder1SpeedCmd_pct           : REAL := 85.50;    (* Feeder #1 Variable Speed Drive Reference [%] *)
    rSagFeeder2SpeedCmd_pct           : REAL := 85.50;    (* Feeder #2 Variable Speed Drive Reference [%] *)
    rSagFeedWaterFlowSp_m3h           : REAL := 1150.00;  (* SAG Mill Feed Trunnion Water Flow Control Setpoint [m3/h] *)
    rSagMotorSpeedRef_rpm             : REAL := 9.18;     (* 28 MW Gearless Ring Motor VFD Speed Reference [rpm] *)
    rSagMotorTorqueLimit_kNm          : REAL := 29500.00; (* 28 MW Ring Motor Direct Torque Control Ceiling [kNm] *)
    rPebbleCrusherFeedSp_tph          : REAL := 380.00;   (* Pebble Recycle Surge Bin Vibratory Feeder Setpoint [t/h] *)
    rCyclonePumpSpeedRef_pct          : REAL := 74.20;    (* Warman 650 MCR Variable Frequency Drive Speed Demand [%] *)
    rSumpDilutionValveCmd_pct         : REAL := 42.50;    (* Sump Water Addition Linear Control Valve Position [%] *)
    iActiveCycloneValvesCount         : INT := 12;        (* Number of Hydrocyclones Commanded Open (1..16) *)
    wCycloneValveMask                 : WORD := 16#0FFF;  (* 16-Bit Solenoid Output Mask for Pneumatic Knife-Gates *)
    abCycloneValveOpen_Cmd            : ARRAY[1..16] OF BOOL := [12(TRUE), 4(FALSE)]; (* Individual Solenoid Commands *)
    rBallMill1FeedSp_tph              : REAL := 1850.00;  (* Ball Mill #1 Cyclone Underflow Slurry Feed Split [t/h] *)
    rBallMill2FeedSp_tph              : REAL := 1850.00;  (* Ball Mill #2 Cyclone Underflow Slurry Feed Split [t/h] *)
    rBallMill1WaterSp_m3h             : REAL := 310.00;   (* Ball Mill #1 Feed Chute Process Water Flow Setpoint [m3/h] *)
    rBallMill2WaterSp_m3h             : REAL := 310.00;   (* Ball Mill #2 Feed Chute Process Water Flow Setpoint [m3/h] *)

    (* ========================================================================================= *)
    (* SECTION 2: CYBER-PHYSICAL OBSERVER ESTIMATES & RECONSTRUCTED PROCESS STATES               *)
    (* ========================================================================================= *)
    rEstimatedChargeWeight_tons       : REAL := 1285.50;  (* Total SAG Mill Live Weight from Dynamic Oil Lift [t] *)
    rEstimatedSlurryVolume_m3         : REAL := 265.40;   (* Reconstructed Slurry Liquid-Solid Volume Hold-Up [m3] *)
    rEstimatedToeAngle_deg            : REAL := 42.80;    (* Acoustic Array Estimated Charge Toe Impact Angle [deg] *)
    rEstimatedShoulderAngle_deg       : REAL := 318.50;   (* Acoustic Array Estimated Charge Shoulder Departure Angle [deg] *)
    rEstimatedImpactVelocity_ms       : REAL := 11.45;    (* Steel Ball Parabolic Flight Impact Velocity [m/s] *)
    rGrindingEfficiencyIndex_pct      : REAL := 88.40;    (* Austin Breakage Specific Grinding Rate Index [%] *)
    rEstimatedP80_microns             : REAL := 75.20;    (* Ultrasonic Inversion Product Particle 80% Passing Size [um] *)
    rCirculatingLoadRatio_pct         : REAL := 245.50;   (* Twin Ball Mill Grinding Circuit Circulating Load [%] *)
    rMillFractionCriticalSpeed_pct    : REAL := 75.80;    (* Instantaneous SAG Mill Rotational Speed / N_c [%] *)
    rEstimatedOilFilmThickness_um     : REAL := 142.50;   (* Hydrostatic Bearing Dynamic Reynolds Oil Film [um] *)

    (* ========================================================================================= *)
    (* SECTION 3: SYSTEM STATUS, FSM STATE & CRITICAL SAFETY TRIP FLAGS                          *)
    (* ========================================================================================= *)
    iCurrentFsmState                  : INT := 1;         (* Deterministic 12-Stage Operational FSM Active State (1..12) *)
    bSystemRunning                    : BOOL := FALSE;    (* Overall Grinding Circuit In Production State *)
    bFrozenChargeTrip                 : BOOL := FALSE;    (* Emergency Trip: Compacted Ore Bed Adhering to Mill Shell *)
    bDirectLinerImpactTrip            : BOOL := FALSE;    (* Emergency Trip: Destructive Steel-on-Steel Liner Impact *)
    bTrunnionLubeInterlockTrip        : BOOL := FALSE;    (* Emergency Trip: Low Jacking Oil Pressure / Babbitt Overheat *)
    bSumpOverflowAlarm                : BOOL := FALSE;    (* High Priority Alarm: Slurry Sump Level > 88% *)
    bSumpCavitationInterlock          : BOOL := FALSE;    (* Interlock: Slurry Sump Level < 18% Pump Protection *)
    bProductOffSpecAlarm              : BOOL := FALSE;    (* Quality Alarm: Product P80 > 85.0 um or Density Off-Spec *)
    bGracefulDegradationActive        : BOOL := FALSE;    (* Sensor Fault: Operating in 1oo2 or 1oo1 Degraded Mode *)

    (* ========================================================================================= *)
    (* SECTION 4: ISA-18.2 32-BIT PACKED DIAGNOSTIC & ALARM WORDS                                *)
    (* ========================================================================================= *)
    wAlarmWord1_Process               : DWORD := 16#0000_0000; (* Process Variable Range & Rate-of-Change Alarms *)
    wAlarmWord2_Mechanical            : DWORD := 16#0000_0000; (* Bearing, Motor, Drive & Crusher Mechanical Alarms *)
    wAlarmWord3_Sensors               : DWORD := 16#0000_0000; (* 2oo3 TMR Sensor Discrepancy & Health Bitmask *)
    wAlarmWord4_Trips                 : DWORD := 16#0000_0000; (* Safety Instrumented System Fast Trip Initiators *)

    (* ========================================================================================= *)
    (* SECTION 5: MODEL PREDICTIVE CONTROL OPTIMIZER PERFORMANCE METRICS                         *)
    (* ========================================================================================= *)
    rMpcOptimizationCost              : REAL := 0.00;     (* Quadratic Receding-Horizon Objective Function Cost *)
    iMpcIterationsCount               : INT := 0;         (* Projected Gradient Descent Solver Iteration Counter *)
    bMpcSolutionFeasible              : BOOL := TRUE;     (* MPC KKT Convergence & Constraint Feasibility Flag *)
END_VAR
"""

print("Base modules written.")
