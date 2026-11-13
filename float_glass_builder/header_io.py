# header_io.py for FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling

def generate_header_io():
    return """FUNCTION_BLOCK FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling
(*
 * =========================================================================================================
 * ARCHITECTURAL SPECIFICATION: CONTINUOUS 800 METRIC TONS/DAY FLOAT GLASS MANUFACTURING FACILITY
 * SYSTEM IDENTITY: FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling
 * 
 * CORE PROCESS ENGINEERING ARCHITECTURE:
 * 1. Canal & Molten Tin Bath (Length: 65.0 m, Width: 8.2 m, Molten Pure Tin Inventory: ~220 Metric Tons):
 *    - Molten soda-lime-silica glass flows through delivery canal at 1,050 - 1,100 [deg C] over lip onto tin.
 *    - Unconstrained equilibrium natural thickness h_eq = ~6.85 [mm] dictated by three-phase contact wetting
 *      equilibrium (surface tension gamma_g_tin, gamma_g_atm, gamma_tin_atm, and buoyant density differential).
 *    - 16 Pairs of independently driven, water-cooled, knurled top-roller machines positioned along bath edges
 *      to dynamically pull, attenuate, hold, or retard the ribbon to produce calibrated thicknesses from 2.0 mm
 *      to 19.0 mm with optical distortion under 0.02 diopters.
 *    - Reducing protective atmosphere: 95.0% N2 / 5.0% H2 at +0.25 to +0.85 [mbar] positive tunnel overpressure
 *      to suppress stannous oxide (SnO) volatilization and catastrophic optical bloom / tin defect inclusions.
 *    - Multi-zone electric roof silicon carbide (SiC) radiant heaters (Zones 1-8) establishing longitudinal thermal
 *      gradient from 1,050 [deg C] at inlet down to 600 [deg C] at exit lift-out rolls.
 * 
 * 2. Lift-Out Rolls (LOR) & Annealing Lehr (Length: 120.0 m, Width: 4.2 m Ribbon Capacity):
 *    - Three high-temperature heat-resistant alloy lift-out rolls extract cooled visco-elastic ribbon (~600 [deg C],
 *      viscosity 10^7.6 dPa.s) from liquid tin onto Lehr motorized drive rollers without bottom surface marring.
 *    - Lehr cooling tunnel divided into 12 thermal conditioning zones:
 *      * Zone A1-A3: Critical rapid isothermal equilibration & annealing relaxation range (550 to 480 [deg C])
 *      * Zone B1-B3: Gradual stress setting & controlled cooling range (480 to 380 [deg C])
 *      * Zone C1-C3: Secondary cooling & cross-belt transverse gradient control (380 to 220 [deg C])
 *      * Zone F1-F3: Final forced convection atmospheric cooling (220 down to 60 [deg C]) prior to cold-end cutting.
 *    - Transverse cross-belt cooling air dampers and bottom/top electric trim elements actively eliminate parabolic
 *      and asymmetric thermal gradients across the ribbon, suppressing residual optical retardation birefringence
 *      to < 15.0 [nm/cm] (far below ASTM C1036 and ISO 16293-2 automotive safety thresholds).
 * 
 * 3. Cyber-Physical Automation & Advanced Control Modules:
 *    - Discrete 6x6 State-Space Matrix Model with discrete Kalman/Luenberger observer innovation (Ts = 10 ms).
 *    - Receding-Horizon Model Predictive Control (MPC) with 10 unrolled Projected Gradient Descent (PGD) iterations
 *      optimizing top-roller speeds, toe angles, penetration depths, roof heater duties, and Lehr damper trims.
 *    - 2oo3 Triple Modular Redundancy (TMR) voting with bumpless failover across scanning thickness gauges,
 *      tin bath pyrometers, protective atmosphere pressure transmitters, and Lehr polarimetric stress sensors.
 *    - 14-Stage Deterministic Production Finite State Machine (FSM) governing complete line lifecycle.
 *    - ISA-18.2 Compliant Multi-Tiered Alarm Hierarchy with bit-packed DWORD diagnostics.
 * =========================================================================================================
 *)

VAR_INPUT
    (* === SYSTEM SUPERVISORY & SAFETY INTERLOCK SIGNALS === *)
    bMasterEnable                   : BOOL;     (* Master Automation Enable Request [BOOL] *)
    bSafetyCircuitHealthy           : BOOL;     (* Hardwired Dual-Channel Category 4 / SIL 3 Safety Circuit [BOOL] *)
    bEmergencyStopActive            : BOOL;     (* Main Line Emergency Stop Pushbutton Circuit Active [BOOL] *)
    bAutoModeSelected               : BOOL;     (* Supervisory Automatic Line Control Mode Permissive [BOOL] *)
    bAlarmResetPushbutton           : BOOL;     (* ISA-18.2 Operator Alarm Acknowledge & Reset Command [BOOL] *)
    bCulletChuteGateManualPermit    : BOOL;     (* Manual Emergency Cullet Trapdoor Release Permissive [BOOL] *)
    bRecipeChangeRequest            : BOOL;     (* Initiate Dynamic Thickness Recipe Transition [BOOL] *)
    bControlledShutdownRequest      : BOOL;     (* Orderly Tweel Closure & Lehr Emptying Request [BOOL] *)

    (* === 2oo3 TRIPLE MODULAR REDUNDANCY SENSOR CHANNELS === *)
    (* Laser Optical Scanning Thickness Gauges [mm] *)
    rLaserThick_Sensor1             : REAL;     (* Non-contact laser thickness sensor channel 1 [mm] *)
    rLaserThick_Sensor2             : REAL;     (* Non-contact laser thickness sensor channel 2 [mm] *)
    rLaserThick_Sensor3             : REAL;     (* Non-contact laser thickness sensor channel 3 [mm] *)

    (* Tin Bath Roof Multi-Wavelength Infrared Pyrometers [deg C] *)
    rPyrometer_Bath_Zone1           : REAL;     (* Tin bath inlet roof optical pyrometer channel 1 [deg C] *)
    rPyrometer_Bath_Zone2           : REAL;     (* Tin bath inlet roof optical pyrometer channel 2 [deg C] *)
    rPyrometer_Bath_Zone3           : REAL;     (* Tin bath inlet roof optical pyrometer channel 3 [deg C] *)

    (* Tin Bath Protective Atmosphere Differential Pressure Transmitters [mbar] *)
    rBathPress_Sensor1              : REAL;     (* Bath hermetic overpressure transmitter channel 1 [mbar] *)
    rBathPress_Sensor2              : REAL;     (* Bath hermetic overpressure transmitter channel 2 [mbar] *)
    rBathPress_Sensor3              : REAL;     (* Bath hermetic overpressure transmitter channel 3 [mbar] *)

    (* Lehr Exit Polarimetric Optical Stress Birefringence Transducers [nm/cm] *)
    rLehrStress_Sensor1             : REAL;     (* Lehr exit residual birefringence retardance channel 1 [nm/cm] *)
    rLehrStress_Sensor2             : REAL;     (* Lehr exit residual birefringence retardance channel 2 [nm/cm] *)
    rLehrStress_Sensor3             : REAL;     (* Lehr exit residual birefringence retardance channel 3 [nm/cm] *)

    (* === MELTING FURNACE DELIVERY CANAL & TWEEL SENSORS === *)
    rMoltenGlassInletTemp           : REAL;     (* Canal delivery forehearth molten glass temperature [deg C] *)
    rCanalTweelPosFeedback          : REAL;     (* Canal refractory tweel flow control gate height [mm] *)
    rCanalGlassFlowRate             : REAL;     (* Continuous glass pull rate through delivery canal [tons/day] *)
    rCanalViscosityIndex            : REAL;     (* Computed glass viscosity log10(poise) in canal [dPa.s] *)

    (* === TIN BATH PROCESS & ATMOSPHERE INSTRUMENTATION === *)
    rRibbonWidthFeedback            : REAL;     (* High-speed optical CCD camera ribbon width feedback [mm] *)
    rBathExitGlassTempFeedback      : REAL;     (* Optical radiation pyrometer ribbon temp at bath exit [deg C] *)
    rMoltenTinBottomTempFeedback    : REAL;     (* Bottom casing immersion thermocouple tin pool temperature [deg C] *)
    rH2_Concentration_Feedback      : REAL;     (* Protective atmosphere hydrogen reducing gas concentration [% vol H2] *)
    rO2_Ppm_Feedback                : REAL;     (* In-situ zirconia trace oxygen sensor [ppm O2] *)
    rTotalGasInflowN2               : REAL;     (* High-purity nitrogen supply manifold flow rate [Nm3/h] *)
    rTotalGasInflowH2               : REAL;     (* Hydrogen reducing gas supply manifold flow rate [Nm3/h] *)
    rBathSealExhaustDamperPos       : REAL;     (* Exit labyrinth nitrogen gas seal exhaust damper position [%] *)

    (* === LEHR MAIN DRIVE & LIFT-OUT ROLLS FEEDBACK === *)
    rLehrDriveSpeedFeedback         : REAL;     (* Annealing Lehr main line conveyor belt actual speed [m/min] *)
    rLiftOutRollSpeedFeedback       : REAL;     (* Lift-out roll 1-3 synchronized surface drive speed [m/min] *)
    rLehrInletTempFeedback          : REAL;     (* Annealing Lehr entry zone A1 optical pyrometer [deg C] *)
    rLehrExitTempFeedback           : REAL;     (* Annealing Lehr exit cold-end cross-belt surface temp [deg C] *)

    (* === PRODUCTION RECIPE TARGET PARAMETERS === *)
    rRecipeTargetThickness          : REAL;     (* Target production glass ribbon finished thickness [mm] *)
    rRecipeTargetWidth              : REAL;     (* Target net usable ribbon ribbon width [mm] *)
    rRecipeTargetLineSpeed          : REAL;     (* Target Lehr line conveyor forward draw speed [m/min] *)
    rRecipeMaxStressLimit           : REAL;     (* Maximum allowable residual birefringence stress limit [nm/cm] *)
    rRecipeTargetTinBathInletTemp   : REAL;     (* Target tin bath entrance molten tin pool temperature [deg C] *)
    rRecipeTargetBathExitTemp       : REAL;     (* Target tin bath exit glass ribbon temperature [deg C] *)

    (* === DISCRETE CONTROLLER CYCLE TIME === *)
    tTaskCycleTime                  : TIME := T#10ms; (* Discrete controller deterministic scan task period [ms] *)
END_VAR

VAR_OUTPUT
    (* === SYSTEM OPERATIONAL STATUS & FSM INDICATORS === *)
    bSystemReady                    : BOOL;     (* System Automation Ready for Production [BOOL] *)
    bSystemActive                   : BOOL;     (* Active Dynamic Glass Ribbon Production In Progress [BOOL] *)
    bSystemDegraded                 : BOOL;     (* System Operating Under Degraded Sensor Redundancy [BOOL] *)
    bSystemFaultTrip                : BOOL;     (* System Latched in Emergency Cullet Dump State [BOOL] *)
    nOperationalState               : INT;      (* 14-Stage Operational Finite State Machine State Code [0..13] *)
    sOperationalStateName           : STRING[80]; (* Descriptive String of Active FSM Production State *)

    (* === 2oo3 TMR VOTED PROCESS SIGNALS === *)
    rVotedThickness_mm              : REAL;     (* TMR Voted Non-Contact Laser Ribbon Thickness [mm] *)
    rVotedPyrometer_degC            : REAL;     (* TMR Voted Tin Bath Roof Temperature [deg C] *)
    rVotedBathPress_mbar            : REAL;     (* TMR Voted Protective Atmosphere Overpressure [mbar] *)
    rVotedLehrStress_nm_cm          : REAL;     (* TMR Voted Residual Birefringence Stress [nm/cm] *)

    (* === TWEEL, LINE DRIVE & LIFT-OUT ROLL ACTUATOR COMMANDS === *)
    rCanalTweelCommand_mm           : REAL;     (* Refractory tweel flow control vertical height position command [mm] *)
    rLehrDriveSpeedCommand_m_min    : REAL;     (* Lehr conveyor synchronous speed setpoint [m/min] *)
    rLiftOutRollSpeedCommand_m_min  : REAL;     (* Lift-out rolls (LOR 1-3) synchronous speed setpoint [m/min] *)
    bCulletDumpGateOpen             : BOOL;     (* Emergency pneumatic cullet chute dump trapdoor actuation [BOOL] *)

    (* === TOP-ROLLER KNURL MACHINE ACTUATOR MATRICES (16 PAIRS) === *)
    arrTopRollerSpeedCmd            : ARRAY[1..16] OF REAL; (* Top-roller pairs 1..16 knurl motor rotation speed [RPM] *)
    arrTopRollerAngleCmd            : ARRAY[1..16] OF REAL; (* Top-roller pairs 1..16 knurl toe angle vs centerline [deg] *)
    arrTopRollerPenetrationCmd      : ARRAY[1..16] OF REAL; (* Top-roller pairs 1..16 vertical knurl bite penetration [mm] *)

    (* === HEATER BANK & COOLING DAMPER PWM / SERVO COMMANDS === *)
    arrTinBathRoofHeaterDuty        : ARRAY[1..8] OF REAL;  (* Tin bath roof SiC radiant heater zones 1..8 duty [%] *)
    arrLehrCoolingDamperCmd         : ARRAY[1..12] OF REAL; (* Annealing Lehr cross-belt cooling dampers 1..12 [%] *)
    arrLehrTrimHeaterDuty           : ARRAY[1..12] OF REAL; (* Annealing Lehr electric trim heater zones 1..12 [%] *)

    (* === PROTECTIVE ATMOSPHERE GAS REGULATION ACTUATION === *)
    rN2_TrimValveCmd                : REAL;     (* High-purity nitrogen supply flow trim control valve [%] *)
    rH2_TrimValveCmd                : REAL;     (* Hydrogen reducing gas scavenger ratio trim valve [%] *)
    rVentExhaustDamperCmd           : REAL;     (* Bath pressure regulating vent exhaust damper position [%] *)

    (* === ESTIMATED CYBER-PHYSICAL STATE OUTPUTS === *)
    rEstimatedThicknessDev_um       : REAL;     (* State x1: Center ribbon thickness deviation [um] *)
    rEstimatedRibbonWidth_mm        : REAL;     (* State x2: Glass ribbon width estimate [mm] *)
    rEstimatedBathTempGrad_degC_m   : REAL;     (* State x3: Tin bath longitudinal temperature gradient [deg C/m] *)
    rEstimatedAtmPress_mbar         : REAL;     (* State x4: Protective atmosphere pressure estimate [mbar] *)
    rEstimatedAnnealStress_nm_cm    : REAL;     (* State x5: Maximum internal residual thermal stress [nm/cm] *)
    rEstimatedLineSpeed_m_min       : REAL;     (* State x6: Observed lehr draw line speed [m/min] *)

    (* === ISA-18.2 ALARM & DIAGNOSTIC BIT-PACKED STATUS WORDS === *)
    dwAlarmWord1_Process            : DWORD;    (* Bit-packed Process Deviation Alarms (HH, H, L, LL) [HEX] *)
    dwAlarmWord2_Equipment          : DWORD;    (* Bit-packed Equipment Drives, Rollers & Heaters Alarms [HEX] *)
    dwAlarmWord3_SafetyTMR          : DWORD;    (* Bit-packed Safety Interlocks & TMR Sensor Failures [HEX] *)
    dwStatusWord_System             : DWORD;    (* Bit-packed Comprehensive System Operational Status [HEX] *)
END_VAR
"""

if __name__ == "__main__":
    s = generate_header_io()
    print(f"Header & IO length: {len(s)} chars")
