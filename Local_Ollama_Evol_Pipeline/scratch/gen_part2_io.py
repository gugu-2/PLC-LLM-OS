# Generator part 2: VAR_INPUT and VAR_OUTPUT
def get_io():
    return """VAR_INPUT
    (* ========================================================================================= *)
    (* PRIMARY INDUSTRIAL P&ID PROCESS TRANSMITTER TELEMETRY (TRIPLE REDUNDANT CHANNELS)       *)
    (* ========================================================================================= *)
    (* Fresh SAG Mill Feed Ore Conveyor Weightometers [t/h] - 2oo3 Triple Redundant Triplet *)
    WT_SAG_FEED_CONVEYOR_101A       : REAL := 2850.0;   (* Fresh feed conveyor belt scale 101A [t/h] (0..4000 t/h) *)
    WT_SAG_FEED_CONVEYOR_101B       : REAL := 2850.0;   (* Fresh feed conveyor belt scale 101B [t/h] (0..4000 t/h) *)
    WT_SAG_FEED_CONVEYOR_101C       : REAL := 2850.0;   (* Fresh feed conveyor belt scale 101C [t/h] (0..4000 t/h) *)

    (* Pebble Recycle Return Conveyor Weightometers [t/h] *)
    WT_PEBBLE_RECYCLE_CONVEYOR_102A : REAL := 280.0;    (* Recycle pebble return belt scale 102A [t/h] (0..800 t/h) *)
    WT_PEBBLE_RECYCLE_CONVEYOR_102B : REAL := 280.0;    (* Recycle pebble return belt scale 102B [t/h] (0..800 t/h) *)

    (* Mill Feed Chute Dilution Water Flowmeters [m3/h] *)
    FT_MILL_FEED_WATER_103A         : REAL := 850.0;    (* Mill inlet water electromagnetic flowmeter 103A [m3/h] *)
    FT_MILL_FEED_WATER_103B         : REAL := 850.0;    (* Mill inlet water electromagnetic flowmeter 103B [m3/h] *)

    (* Inlet Trunnion Hydrostatic Bearing Jacking Lift Oil Film Pressure [bar] - 2oo3 Triplet *)
    PT_TRUNNION_INLET_BEARING_201A  : REAL := 168.5;    (* Inlet trunnion jacking oil pad pressure 201A [bar] (0..250 bar) *)
    PT_TRUNNION_INLET_BEARING_201B  : REAL := 168.5;    (* Inlet trunnion jacking oil pad pressure 201B [bar] (0..250 bar) *)
    PT_TRUNNION_INLET_BEARING_201C  : REAL := 168.5;    (* Inlet trunnion jacking oil pad pressure 201C [bar] (0..250 bar) *)

    (* Outlet Trunnion Hydrostatic Bearing Jacking Lift Oil Film Pressure [bar] - 2oo3 Triplet *)
    PT_TRUNNION_OUTLET_BEARING_202A : REAL := 174.2;    (* Outlet trunnion jacking oil pad pressure 202A [bar] (0..250 bar) *)
    PT_TRUNNION_OUTLET_BEARING_202B : REAL := 174.2;    (* Outlet trunnion jacking oil pad pressure 202B [bar] (0..250 bar) *)
    PT_TRUNNION_OUTLET_BEARING_202C : REAL := 174.2;    (* Outlet trunnion jacking oil pad pressure 202C [bar] (0..250 bar) *)

    (* Trunnion Bearing Babbitt / White Metal Pad Temperature Telemetry [deg C] *)
    TT_TRUNNION_INLET_BEARING_PAD_203A  : REAL := 58.5; (* Inlet trunnion Babbitt metal RTD sensor [deg C] *)
    TT_TRUNNION_OUTLET_BEARING_PAD_204A : REAL := 61.2; (* Outlet trunnion Babbitt metal RTD sensor [deg C] *)

    (* Shell Acoustic Ear Microphone Array - Dynamic Grinding Toe Station [dB / % Impact Energy] *)
    AIT_ACOUSTIC_EAR_TOE_301A       : REAL := 24.5;     (* Acoustic ear toe sensor 301A [0..100%] (4..20mA / high frequency) *)
    AIT_ACOUSTIC_EAR_TOE_301B       : REAL := 24.5;     (* Acoustic ear toe sensor 301B [0..100%] (4..20mA / high frequency) *)
    AIT_ACOUSTIC_EAR_TOE_301C       : REAL := 24.5;     (* Acoustic ear toe sensor 301C [0..100%] (4..20mA / high frequency) *)

    (* Shell Acoustic Ear Microphone Array - Charge Shoulder Station [dB / % Noise Power] *)
    AIT_ACOUSTIC_EAR_SHOULDER_302A  : REAL := 78.2;     (* Acoustic ear shoulder sensor 302A [0..100%] (4..20mA / low freq) *)
    AIT_ACOUSTIC_EAR_SHOULDER_302B  : REAL := 78.2;     (* Acoustic ear shoulder sensor 302B [0..100%] (4..20mA / low freq) *)
    AIT_ACOUSTIC_EAR_SHOULDER_302C  : REAL := 78.2;     (* Acoustic ear shoulder sensor 302C [0..100%] (4..20mA / low freq) *)

    (* 28 MW Gearless Ring Motor Rotational Speed Telemetry [RPM] - 2oo3 Triplet *)
    ST_SAG_RING_MOTOR_RPM_401A      : REAL := 9.15;     (* Ring motor pulse encoder tachometer 401A [RPM] (0..15 RPM) *)
    ST_SAG_RING_MOTOR_RPM_401B      : REAL := 9.15;     (* Ring motor pulse encoder tachometer 401B [RPM] (0..15 RPM) *)
    ST_SAG_RING_MOTOR_RPM_401C      : REAL := 9.15;     (* Ring motor resolver sensor tachometer 401C [RPM] (0..15 RPM) *)

    (* 28 MW Gearless Ring Motor Active Electrical Power [MW] - 2oo3 Triplet *)
    IT_SAG_MOTOR_POWER_402A         : REAL := 23.45;    (* High-voltage drive active power meter 402A [MW] (0..35 MW) *)
    IT_SAG_MOTOR_POWER_402B         : REAL := 23.45;    (* High-voltage drive active power meter 402B [MW] (0..35 MW) *)
    IT_SAG_MOTOR_POWER_402C         : REAL := 23.45;    (* High-voltage drive active power meter 402C [MW] (0..35 MW) *)

    (* Ring Motor Direct Torque Feedback [kNm] *)
    QT_SAG_MOTOR_TORQUE_403A        : REAL := 24450.0;  (* Direct torque controller internal flux observer [kNm] *)

    (* Cyclone Feed Slurry Sump Level Telemetry [%] - 2oo3 Triplet *)
    LT_CYCLONE_SUMP_LEVEL_501A      : REAL := 58.5;     (* Radar level transmitter 501A [%] (0..100% of 140 m3 sump) *)
    LT_CYCLONE_SUMP_LEVEL_501B      : REAL := 58.5;     (* Ultrasonic level transmitter 501B [%] (0..100% of 140 m3 sump) *)
    LT_CYCLONE_SUMP_LEVEL_501C      : REAL := 58.5;     (* Hydrostatic pressure level transmitter 501C [%] (0..100%) *)

    (* Cyclone Feed Slurry Nuclear Gamma Density Gauges [SG] - 2oo3 Triplet *)
    DT_CYCLONE_FEED_DENSITY_502A    : REAL := 1.540;    (* Cs-137 nuclear gamma densitometer 502A [SG] (1.0..2.2 SG) *)
    DT_CYCLONE_FEED_DENSITY_502B    : REAL := 1.540;    (* Cs-137 nuclear gamma densitometer 502B [SG] (1.0..2.2 SG) *)
    DT_CYCLONE_FEED_DENSITY_502C    : REAL := 1.540;    (* Cs-137 nuclear gamma densitometer 502C [SG] (1.0..2.2 SG) *)

    (* Cyclone Feed Distributor Manifold Slurry Pressure [kPa] - 2oo3 Triplet *)
    PT_CYCLONE_MANIFOLD_503A        : REAL := 92.5;     (* Diaphragm seal pressure transmitter 503A [kPa] (0..250 kPa) *)
    PT_CYCLONE_MANIFOLD_503B        : REAL := 92.5;     (* Diaphragm seal pressure transmitter 503B [kPa] (0..250 kPa) *)
    PT_CYCLONE_MANIFOLD_503C        : REAL := 92.5;     (* Diaphragm seal pressure transmitter 503C [kPa] (0..250 kPa) *)

    (* Cyclone Feed Slurry Volumetric Discharge Flow [m3/h] *)
    FT_CYCLONE_FEED_FLOW_504A       : REAL := 3450.0;   (* Magnetic slurry flowmeter 504A [m3/h] (0..6000 m3/h) *)
    FT_CYCLONE_FEED_FLOW_504B       : REAL := 3450.0;   (* Magnetic slurry flowmeter 504B [m3/h] (0..6000 m3/h) *)

    (* Cyclone Sump Dilution Trim Water Flow [m3/h] *)
    FT_SUMP_DILUTION_WATER_505A     : REAL := 420.0;    (* Sump water addition flowmeter [m3/h] (0..1200 m3/h) *)

    (* Ro-Tap Particle Size Laser Diffraction Analyzer Overflow P80 Telemetry [um] *)
    AT_CYCLONE_OVERFLOW_P80_506     : REAL := 148.5;    (* Online particle size analyzer PSI-300 P80 [um] (target: 150 um) *)

    (* 12-Hydrocyclone Battery Cluster Knife-Gate Valve Open Feedback Signals *)
    abCyclone_ValveOpen_Feedback    : ARRAY[1..12] OF BOOL := [12(TRUE)]; (* Discrete open limit switch feedbacks *)

    (* 12-Hydrocyclone Battery Cluster Roping / Flare Acoustic Sensor Warnings *)
    abCyclone_RopingWarning_Feedback: ARRAY[1..12] OF BOOL := [12(FALSE)]; (* Cyclone underflow roping detected *)

    (* Supervisory, Analytical & Functional Safety Discrete Controls *)
    bEnable                         : BOOL := TRUE;     (* Master functional block execution permissive *)
    bEmergencyStop                  : BOOL := TRUE;     (* Hardwired emergency stop relay healthy (Active Low) *)
    bAcknowledgeAlarms              : BOOL := FALSE;    (* Operator alarm acknowledge push button *)
    bAutoMode                       : BOOL := TRUE;     (* Plant DCS supervisory auto control mode selector *)
    bAcousticMitigationPermissive   : BOOL := TRUE;     (* Enable automated shell liner impact mitigation override *)
    bMPC_Permissive                 : BOOL := TRUE;     (* Enable multivariable state-space MPC optimizer *)
    bJackingOilPumpsRunning         : BOOL := TRUE;     (* High-pressure hydraulic lift pumps running healthy *)
    tScanTime_s                     : REAL := 0.010;    (* Deterministic execution task period [s] (10 ms cycle) *)
END_VAR

VAR_OUTPUT
    (* ========================================================================================= *)
    (* ACTUATOR DEMANDS & CYBER-PHYSICAL REGULATING SIGNALS                                      *)
    (* ========================================================================================= *)
    (* SAG Fresh Ore Feed Rate Demand [t/h] *)
    rSAG_FreshFeedRateCmd_tph       : REAL := 2850.0;   (* Fresh feed conveyor VFD speed demand [t/h] (0..3600 t/h) *)

    (* Mill Feed Chute Dilution Water Flow Demand [m3/h] *)
    rMillInletWaterFlowCmd_m3h      : REAL := 850.0;    (* Water control valve flow setpoint [m3/h] (0..1500 m3/h) *)

    (* Gearless Ring Motor Rotational Speed Setpoint [RPM] *)
    rRingMotorSpeedCmd_RPM          : REAL := 9.15;     (* Ring motor variable speed drive reference [RPM] (6.5..10.2 RPM) *)

    (* Gearless Ring Motor Direct Torque Operational Limit [kNm] *)
    rRingMotorTorqueLimit_kNm       : REAL := 28500.0;  (* Direct torque controller dynamic torque ceiling [kNm] *)

    (* Cyclone Feed Slurry Pump Speed Demand [RPM] *)
    rCyclonePumpSpeedCmd_RPM        : REAL := 520.0;    (* Warman 650 MCR slurry pump VFD speed demand [RPM] (350..750 RPM) *)

    (* Cyclone Feed Sump Dilution Trim Water Valve Command [%] *)
    rCycloneSumpWaterValveCmd_Pct   : REAL := 38.5;     (* Sump water control valve stroke position demand [%] (0..100%) *)

    (* 12-Hydrocyclone Battery Cluster Pneumatic Knife-Gate Valve Open Commands *)
    abCycloneValveOpen_Cmd          : ARRAY[1..12] OF BOOL := [12(TRUE)]; (* Individual cyclone isolation valve commands *)

    (* Target Active Operating Cyclone Count Demand *)
    iActiveCyclonesTargetCount      : INT := 9;         (* Recommended active cyclone count for optimal manifold pressure *)

    (* Pebble Crusher Feed Diverter Gate Position Demand [%] *)
    rPebbleCrusherFeedDiverter_Pct  : REAL := 100.0;    (* Pebble bypass diverter: 100% = crushers, 0% = recycle direct *)

    (* High-Pressure Trunnion Jacking Oil Lift Pump Start Command *)
    bJackingOilPumpStart_Cmd        : BOOL := TRUE;     (* Run permissive for auxiliary high-pressure hydraulic pumps *)

    (* Auxiliary Inching Drive Engagement Command *)
    bInchingDriveEngage_Cmd         : BOOL := FALSE;    (* Mechanical clutch command for mill maintenance inching drive *)

    (* ========================================================================================= *)
    (* RECONSTRUCTED PROCESS VARIABLES, CYBER-PHYSICAL ESTIMATORS & OBSERVERS                   *)
    (* ========================================================================================= *)
    rVoted_TotalMillWeight_tons     : REAL := 1320.5;   (* 2oo3 voted total live mill mass [tons] (0.1 ton precision) *)
    rEstimated_OreHoldUp_tons       : REAL := 380.0;    (* Observer reconstructed coarse and fine ore hold-up [tons] *)
    rEstimated_WaterHoldUp_m3       : REAL := 165.0;    (* Observer reconstructed internal slurry water volume [m3] *)
    rEstimated_SlurryHoldUp_m3      : REAL := 245.0;    (* Total internal slurry hold-up volume inside mill shell [m3] *)
    rEstimated_ToeAngle_deg         : REAL := 135.2;    (* Dynamic charge toe contact angle [deg] relative to vertical *)
    rEstimated_ShoulderAngle_deg    : REAL := 315.8;    (* Dynamic charge shoulder departure angle [deg] relative to vert *)
    rCalculated_LinerImpactIndex    : REAL := 24.5;     (* Direct ball-on-liner impact severity index [%] (0..100%) *)
    rCalculated_SpecificEnergy_kWh_t: REAL := 8.23;     (* Specific grinding energy consumption [kWh/t dry ore] *)
    rCalculated_Plitt_d50c_um       : REAL := 148.5;    (* Online Plitt hydrocyclone corrected cut size d50c [um] *)
    rCalculated_CirculatingLoad_Pct : REAL := 225.0;    (* Cyclone underflow circulating load ratio [% of fresh feed] *)
    rSlurryVolumetricFilling_Jpz    : REAL := 28.5;     (* Total mill volumetric charge filling fraction Jc [% volume] *)

    (* ========================================================================================= *)
    (* 32-BIT PACKED SYSTEM OPERATING & DIAGNOSTIC WORDS                                         *)
    (* ========================================================================================= *)
    dwSystemStatusWord              : DWORD := 16#0000_0000; (* 32-bit packed overall system operating status word *)
    dwAlarmWord_HighTrip            : DWORD := 16#0000_0000; (* 32-bit packed critical trip alarms (HI_HI severity) *)
    dwAlarmWord_LowWarning          : DWORD := 16#0000_0000; (* 32-bit packed warning alarms (HI/LO/ROC severity) *)
    dwTMR_Diagnostic_Weight         : DWORD := 16#0000_0000; (* 32-bit trunnion bearing pressure & weight TMR status *)
    dwTMR_Diagnostic_Acoustic       : DWORD := 16#0000_0000; (* 32-bit acoustic ear toe/shoulder sensor TMR status *)
    dwTMR_Diagnostic_Density        : DWORD := 16#0000_0000; (* 32-bit cyclone feed density gauge TMR status word *)
    dwTMR_Diagnostic_Power          : DWORD := 16#0000_0000; (* 32-bit ring motor power and speed sensor TMR word *)

    (* ========================================================================================= *)
    (* SAFETY INSTRUMENTED PERMISSIVES & PROCESS INTERLOCK FEEDBACKS                            *)
    (* ========================================================================================= *)
    iOperatingState                 : INT := 0;         (* Current FSM active state (0..999) *)
    bCriticalImpactEmergencyActive  : BOOL := FALSE;    (* Ball-on-liner severe direct impact protection active *)
    bMillOverfillingSlurrySpillTrip : BOOL := FALSE;    (* Mill weight > 1550 t overfilling slurry spill fast trip *)
    bSumpCavitationProtectionActive : BOOL := FALSE;    (* Cyclone feed sump level < 18% pump cavitation interlock *)
    bMPC_ControllerActive           : BOOL := FALSE;    (* Multivariable model predictive control optimizer active *)
    bGracefulDegradationActive      : BOOL := FALSE;    (* Sensor triplet degraded from 2oo3 to 1oo2 or 1oo1 mode *)
END_VAR
"""

print("IO module loaded.")
