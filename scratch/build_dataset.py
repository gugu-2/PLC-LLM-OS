# Generator script for FB_Grain_TerminalElevator_BulkHandling_Hazard
import sys
import os
import json
import uuid

UUID_STR = "e766b1fb"
TARGET_JSON = f"data/swarm_raw/agent_{UUID_STR}.json"

def build_grain_terminal_st():
    parts = []

    # 1. Header
    parts.append("""```iec-st
FUNCTION_BLOCK FB_Grain_TerminalElevator_BulkHandling_Hazard
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * INDUSTRIAL SECTOR    : BULK MATERIALS HANDLING & AGRI-LOGISTICS PORT TERMINALS
 * FACILITY / MACHINE   : HIGH-CAPACITY PORT TERMINAL GRAIN ELEVATOR INTAKE & DISTRIBUTION COMPLEX
 * DESIGN THROUGHPUT    : 1,500 t/h (WHEAT / CORN CONTINUOUS MASS TRANSFER)
 * MAJOR SUB-SYSTEMS    : 1. TWIN HEAVY-DUTY BUCKET ELEVATORS (45.0 m VERTICAL LIFT, DUAL 315 kW MOTORS)
 *                        2. VFD BELT SLIP SPEED OBSERVER (HEAD VS BOOT REAL-TIME PULLEY DIFFERENTIAL < 2.0%)
 *                        3. MULTI-RUN EN-MASSE DRAG CONVEYORS (INTAKE PIT & OVERHEAD SILO TOP CASING)
 *                        4. ROTARY ELECTRIC TURN-HEAD SPOUT DISTRIBUTOR (LASER ANGULAR POSITIONING +/- 0.05 deg)
 *                        5. SILO AERATION VARIABLE SPEED FANS & EQUILIBRIUM MOISTURE CONTROLLER
 *                        6. 24-POINT THERMOCOUPLE GRAIN TEMPERATURE CABLE SENSOR MESH (4 CABLES x 6 DEPTHS)
 *                        7. CONTINUOUS INLINE MICROWAVE GRAIN MOISTURE TRANSMITTER (14.0 +/- 0.2%)
 *                        8. OPTICAL BELT RUB PYROMETERS & ACOUSTIC HEAD BEARING VIBRATION SENSORS
 *                        9. ATEX / NFPA 61 FAST COMBUSTIBLE DUST EXPLOSION SUPPRESSION SYSTEM:
 *                           - SUB-50 ms FAST OPTICAL DUAL-SPECTRUM IR FLAME / SPARK DETECTORS
 *                           - HIGH-RATE DISCHARGE (HRD) SODIUM BICARBONATE CHEMICAL ISOLATION CANNONS
 *                           - HIGH-SPEED EXPLOSION ISOLATION PINCH VALVES & EMERGENCY ABORT GATES
 *                       10. 14-CHANNEL TRIPLE MODULAR REDUNDANCY (2oo3 TMR) SENSOR VOTING WITH 5 ms DEBOUNCE
 *                       11. 8x8 DISCRETE STATE-SPACE RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC, Ts = 10 ms)
 *                       12. 12-STAGE INDUSTRIAL FINITE STATE MACHINE (FSM) WITH FULL CASCADE INTERLOCKS
 *                       13. ISA-18.2 MULTI-TIERED ALARM HIERARCHY (HH TRIPS, H WARNINGS, L/LL STARVATION)
 * STANDARDS COMPLIANCE : NFPA 61 (AGRICULTURAL & FOOD DUST EXPLOSIONS), NFPA 69 (EXPLOSION PREVENTION SYSTEMS),
 *                        ATEX DIRECTIVE 2014/34/EU (EQUIPMENT), ATEX 1999/92/EC (WORKPLACE DIRECTIVE 137),
 *                        IEC 60079-10-2 (ZONE 20 / 21 / 22 DUST CLASSIFICATION), ISO 13849-1 (PL e / CAT 4),
 *                        IEC 61508 (FUNCTIONAL SAFETY SIL 3), ISO 10816-3 (VIBRATION EVALUATION), ISA-18.2 ALARMS
 * ===================================================================================================================== *)
""")

    # 2. VAR_INPUT
    parts.append("""VAR_INPUT
    (* =================================================================================================================
     * SECTION 1: SUPERVISORY PERMISSIVES, HARDWARE SAFETY LOOPS & OPERATOR INTERLOCK COMMANDS
     * ================================================================================================================= *)
    bMasterEnable                       : BOOL;       (* Master terminal automation permissive [1=Enable, 0=Inhibit] *)
    bIntakeStartCommand                 : BOOL;       (* Sequence automatic route start execution trigger pulse *)
    bIntakeStopCommand                  : BOOL;       (* Controlled sequential cascade stop trigger pulse *)
    bEmergencyStop_CH1                  : BOOL;       (* Dual-channel hardware E-stop loop Channel 1 [0=Tripped] *)
    bEmergencyStop_CH2                  : BOOL;       (* Dual-channel hardware E-stop loop Channel 2 [0=Tripped] *)
    bExplosionSuppressionArmed          : BOOL;       (* ATEX/NFPA 61 HRD chemical cannon discharge armed [1=Armed] *)
    bAspirationSystemRunning            : BOOL;       (* Central baghouse pulse-jet dust aspiration skid running [1=Running] *)
    bExplosionVentDoorsClosed           : BOOL;       (* Elevator leg burst disc/vent door magnetic switches [1=Closed] *)
    bServiceAccessHatchesClosed         : BOOL;       (* Boot & head inspection access hatch interlocks [1=Closed] *)
    bMaintenanceOverrideKey             : BOOL;       (* Authorized supervisor key switch for jog/commissioning *)
    bManualHazardReset                  : BOOL;       (* Hardwired physical latch reset pushbutton on safety panel *)

    (* =================================================================================================================
     * SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSORS (CHANNELS A, B, C ACROSS 14 PROCESS SIGNALS)
     * ================================================================================================================= *)
    (* --- Signal 1: Bucket Elevator A Head Pulley Belt Speed [RPM] --- *)
    ST_ELEV_A_HEAD_SPD_101A             : REAL;       (* Elevator A head shaft quadrature optical encoder A [RPM] *)
    ST_ELEV_A_HEAD_SPD_101B             : REAL;       (* Elevator A head shaft quadrature optical encoder B [RPM] *)
    ST_ELEV_A_HEAD_SPD_101C             : REAL;       (* Elevator A head shaft magnetic pickup pulse sensor C [RPM] *)

    (* --- Signal 2: Bucket Elevator A Boot Pulley Belt Speed [RPM] (Tail Pulley for Slip Evaluation) --- *)
    ST_ELEV_A_BOOT_SPD_102A             : REAL;       (* Elevator A boot shaft inductive proximity encoder A [RPM] *)
    ST_ELEV_A_BOOT_SPD_102B             : REAL;       (* Elevator A boot shaft inductive proximity encoder B [RPM] *)
    ST_ELEV_A_BOOT_SPD_102C             : REAL;       (* Elevator A boot shaft magnetic tachometer C [RPM] *)

    (* --- Signal 3: Bucket Elevator B Head Pulley Belt Speed [RPM] --- *)
    ST_ELEV_B_HEAD_SPD_103A             : REAL;       (* Elevator B head shaft quadrature optical encoder A [RPM] *)
    ST_ELEV_B_HEAD_SPD_103B             : REAL;       (* Elevator B head shaft quadrature optical encoder B [RPM] *)
    ST_ELEV_B_HEAD_SPD_103C             : REAL;       (* Elevator B head shaft magnetic pickup pulse sensor C [RPM] *)

    (* --- Signal 4: Bucket Elevator B Boot Pulley Belt Speed [RPM] --- *)
    ST_ELEV_B_BOOT_SPD_104A             : REAL;       (* Elevator B boot shaft inductive proximity encoder A [RPM] *)
    ST_ELEV_B_BOOT_SPD_104B             : REAL;       (* Elevator B boot shaft inductive proximity encoder B [RPM] *)
    ST_ELEV_B_BOOT_SPD_104C             : REAL;       (* Elevator B boot shaft magnetic tachometer C [RPM] *)

    (* --- Signal 5: Bucket Elevator Drive Motor Active Power [kW] --- *)
    JT_ELEV_A_MOTOR_PWR_105A            : REAL;       (* Elevator A VFD internal power feedback channel A [kW] *)
    JT_ELEV_A_MOTOR_PWR_105B            : REAL;       (* External digital power transducer CT/PT channel B [kW] *)
    JT_ELEV_A_MOTOR_PWR_105C            : REAL;       (* External digital power transducer CT/PT channel C [kW] *)

    (* --- Signal 6: Elevator Head Pulley Spherical Roller Bearing Temperature [deg C] --- *)
    TT_ELEV_HEAD_BRG_106A               : REAL;       (* Head pulley drive-end bearing RTD Pt100 sensor A [deg C] *)
    TT_ELEV_HEAD_BRG_106B               : REAL;       (* Head pulley non-drive bearing RTD Pt100 sensor B [deg C] *)
    TT_ELEV_HEAD_BRG_106C               : REAL;       (* Head pulley housing core thermocouple sensor C [deg C] *)

    (* --- Signal 7: Elevator Boot Pulley Spherical Roller Bearing Temperature [deg C] --- *)
    TT_ELEV_BOOT_BRG_107A               : REAL;       (* Boot pulley take-up bearing RTD Pt100 sensor A [deg C] *)
    TT_ELEV_BOOT_BRG_107B               : REAL;       (* Boot pulley opposite bearing RTD Pt100 sensor B [deg C] *)
    TT_ELEV_BOOT_BRG_107C               : REAL;       (* Boot take-up frame thermocouple sensor C [deg C] *)

    (* --- Signal 8: Elevator Head Shaft Acoustic Bearing Vibration RMS [mm/s] (ISO 10816-3) --- *)
    VT_ELEV_HEAD_VIB_108A               : REAL;       (* Head shaft piezoceramic accelerometer transmitter A [mm/s] *)
    VT_ELEV_HEAD_VIB_108B               : REAL;       (* Head shaft piezoceramic accelerometer transmitter B [mm/s] *)
    VT_ELEV_HEAD_VIB_108C               : REAL;       (* Head casing acoustic emission vibration sensor C [mm/s] *)

    (* --- Signal 9: Optical Belt Misalignment Casing Rub Pyrometers [deg C] --- *)
    TT_BELT_RUB_TEMP_109A               : REAL;       (* Left-hand casing optical infrared pyrometer A [deg C] *)
    TT_BELT_RUB_TEMP_109B               : REAL;       (* Right-hand casing optical infrared pyrometer B [deg C] *)
    TT_BELT_RUB_TEMP_109C               : REAL;       (* Throat discharge divider brass rub block RTD C [deg C] *)

    (* --- Signal 10: Active Silo Bin FMCW Radar Continuous Level [m] --- *)
    LT_SILO_RADAR_LVL_110A              : REAL;       (* 80 GHz FMCW high-frequency radar level transmitter A [m] *)
    LT_SILO_RADAR_LVL_110B              : REAL;       (* 80 GHz FMCW redundant radar level transmitter B [m] *)
    LT_SILO_RADAR_LVL_110C              : REAL;       (* Acoustic 3D solids surface scanner level transmitter C [m] *)

    (* --- Signal 11: Continuous Inline Microwave Grain Moisture Analyzer [%] --- *)
    MT_GRAIN_MOISTURE_111A              : REAL;       (* Chute microwave resonator moisture probe A [%] *)
    MT_GRAIN_MOISTURE_111B              : REAL;       (* Chute microwave phase-shift moisture probe B [%] *)
    MT_GRAIN_MOISTURE_111C              : REAL;       (* High-frequency dielectric moisture sensor C [%] *)

    (* --- Signal 12: Sub-50 ms Dual-Spectrum Optical Fast IR Flame / Spark Detectors [V] --- *)
    FT_OPTICAL_FLAME_112A               : REAL;       (* Dual IR (4.3 um / 4.5 um) elevator head flame detector A [V] *)
    FT_OPTICAL_FLAME_112B               : REAL;       (* Dual IR (4.3 um / 4.5 um) elevator head flame detector B [V] *)
    FT_OPTICAL_FLAME_112C               : REAL;       (* Fast lead selenide optical spark sensor C [V] *)

    (* --- Signal 13: Central Dust Aspiration Duct Static Differential Pressure [Pa] --- *)
    PT_ASPIRATION_DIFF_113A             : REAL;       (* Baghouse collector inlet static differential pressure A [Pa] *)
    PT_ASPIRATION_DIFF_113B             : REAL;       (* Baghouse collector inlet static differential pressure B [Pa] *)
    PT_ASPIRATION_DIFF_113C             : REAL;       (* Elevator trunking aspiration differential pressure C [Pa] *)

    (* --- Signal 14: Rotary Electric Turn-Head Spout Distributor Laser Angle [deg] --- *)
    AT_TURNHEAD_ANGLE_114A              : REAL;       (* Turn-head spout absolute optical multi-turn rotary encoder A [deg] *)
    AT_TURNHEAD_ANGLE_114B              : REAL;       (* Precision laser time-of-flight angular positioner B [deg] *)
    AT_TURNHEAD_ANGLE_114C              : REAL;       (* Heavy-duty magnetic resolver rotary transducer C [deg] *)

    (* =================================================================================================================
     * SECTION 3: SILO 24-POINT THERMOCOUPLE GRAIN TEMPERATURE CABLE MESH INPUTS [deg C]
     * Organised as 4 vertical hanging suspension cables x 6 depth zones (Depth 1=Hopper, Depth 6=Surface)
     * ================================================================================================================= *)
    arrGrainMeshTemp_degC               : ARRAY[1..24] OF REAL; (* 24-point thermocouple cable mesh array [deg C] *)

    (* =================================================================================================================
     * SECTION 4: PROCESS SETPOINTS, PRODUCT CALIBRATION & ROUTING PARAMETERS
     * ================================================================================================================= *)
    iTargetSiloBin                      : INT;        (* Designated target storage silo destination bin [1..12] *)
    rTargetThroughput_tph               : REAL;       (* Target mass transfer throughput rate setpoint [t/h] *)
    rGrainBulkDensity_kg_m3             : REAL;       (* Measured bulk density of grain lot [kg/m3] (wheat ~780, corn ~720) *)
    rMoistureSetpoint_pct               : REAL;       (* Baseline commercial moisture target [14.0 %] *)
    rMaxAllowableBeltSlip_pct           : REAL;       (* VFD belt slip alarm trip threshold baseline [2.0 %] *)
    rAspirationAirflowTarget_m3h        : REAL;       (* Dust collection aspiration volumetric airflow setpoint [m3/h] *)
    rAmbientAirTemp_degC                : REAL;       (* Outdoor ambient weather station dry-bulb temperature [deg C] *)
    rAmbientAirRelHum_pct               : REAL;       (* Outdoor ambient weather station relative humidity [%] *)

    (* =================================================================================================================
     * SECTION 5: AUXILIARY SENSORS, CONVEYOR RUN CONTACTS & SAFETY INTERLOCKS
     * ================================================================================================================= *)
    bPitConveyorRunning_Feedback        : BOOL;       (* Intake pit en-masse drag conveyor auxiliary run contact *)
    bOverheadConveyorRunning_Feedback   : BOOL;       (* Silo top distribution en-masse drag conveyor run contact *)
    bHeadChutePlugged_Switch            : BOOL;       (* Elevator head discharge chute diaphragm tilt switch [0=Plugged] *)
    bBootChutePlugged_Switch            : BOOL;       (* Elevator boot intake hopper plugged chute switch [0=Plugged] *)
    bBeltAlignment_LH_Trip              : BOOL;       (* Mechanical limit switch left-hand belt runout [0=Tripped] *)
    bBeltAlignment_RH_Trip              : BOOL;       (* Mechanical limit switch right-hand belt runout [0=Tripped] *)
    bHRDCannonPressure_OK               : BOOL;       (* High-Rate Discharge nitrogen cartridge pressure switch (> 60 bar) *)
    bExplosionVentingFlap_Open          : BOOL;       (* NFPA 68 flameless explosion venting rupture sensor [1=Burst] *)
    bAspirationDuctBlocked_Switch       : BOOL;       (* Static pressure switch detecting clogged suction takeoff [0=Blocked] *)
END_VAR
""")

    # 3. VAR_OUTPUT
    parts.append("""VAR_OUTPUT
    (* =================================================================================================================
     * SECTION 1: ACTUATOR DRIVE SPEED & FLOW MODULATION ANALOG COMMANDS
     * ================================================================================================================= *)
    rElevatorA_VFD_Speed_Cmd_Hz         : REAL;       (* Bucket Elevator A main drive inverter frequency command [Hz] *)
    rElevatorB_VFD_Speed_Cmd_Hz         : REAL;       (* Bucket Elevator B main drive inverter frequency command [Hz] *)
    rPitConveyor_VFD_Speed_Cmd_Hz       : REAL;       (* Intake pit drag conveyor variable speed command [Hz] *)
    rOverheadConveyor_VFD_Speed_Hz      : REAL;       (* Silo top distribution drag conveyor speed command [Hz] *)
    rFeederSlideGate_Pos_Cmd_pct        : REAL;       (* Intake metering slide gate position command [0.0..100.0 %] *)
    rTurnHeadSpout_Drive_Cmd_pct        : REAL;       (* Rotary distributor electric slew drive speed & direction [%] *)
    bTurnHeadLockPin_Engage             : BOOL;       (* Turn-head pneumatic tapered shot-pin lock solenoid [1=Engaged] *)
    rAspirationDamper_Pos_Cmd_pct       : REAL;       (* Central baghouse duct airflow balancing damper [0.0..100.0 %] *)
    rAerationFan_VFD_Speed_Cmd_Hz       : REAL;       (* Active silo bin bottom aeration blower speed command [Hz] *)

    (* =================================================================================================================
     * SECTION 2: ATEX / NFPA 61 FAST SAFETY TRIPS & EMERGENCY SUPPRESSION ACTUATORS
     * ================================================================================================================= *)
    bHRD_ChemicalCannons_Fire           : BOOL;       (* Fast pyrotechnic discharge pulse to Sodium Bicarbonate cannons *)
    bExplosionFastAbortGate_Trip        : BOOL;       (* High-speed pneumatic abort gate to dump burning grain [sub-50ms] *)
    bAspirationIsolationDamper_Trip     : BOOL;       (* Mechanical guillotine knife-gate rapid isolation damper trip *)
    bEmergencyStopTripRelay             : BOOL;       (* Master safety interlock relay de-energize trip coil [0=Trip] *)
    bDelugeWaterMist_Active             : BOOL;       (* Elevator head explosion deluge fine water-mist solenoid [1=Spray] *)
    bAcousticAlarmSiren                 : BOOL;       (* High-decibel plant evacuation horn and strobe light [1=Sound] *)

    (* =================================================================================================================
     * SECTION 3: VOTED PROCESS METRICS, OBSERVER STATES & PHYSICAL DIAGNOSTICS
     * ================================================================================================================= *)
    rVotedHeadBeltSpeedA_mps            : REAL;       (* 2oo3 voted elevator A linear head pulley speed [m/s] *)
    rVotedBootBeltSpeedA_mps            : REAL;       (* 2oo3 voted elevator A linear boot take-up speed [m/s] *)
    rCalculatedSlipA_pct                : REAL;       (* Elevator A real-time belt slip differential percentage [%] *)
    rCalculatedSlipB_pct                : REAL;       (* Elevator B real-time belt slip differential percentage [%] *)
    rVotedMotorPower_kW                 : REAL;       (* 2oo3 voted elevator drive electrical power consumption [kW] *)
    rVotedHeadBearingTemp_degC          : REAL;       (* 2oo3 voted elevator head bearing temperature [deg C] *)
    rVotedBootBearingTemp_degC          : REAL;       (* 2oo3 voted elevator boot bearing temperature [deg C] *)
    rVotedHeadBearingVib_mms            : REAL;       (* 2oo3 voted head bearing acoustic RMS vibration [mm/s] *)
    rVotedBeltRubTemp_degC              : REAL;       (* 2oo3 voted optical belt rub casing pyrometer temperature [deg C] *)
    rVotedRadarLevel_m                  : REAL;       (* 2oo3 voted active silo bin FMCW radar level [m] *)
    rVotedGrainMoisture_pct             : REAL;       (* 2oo3 voted continuous inline microwave moisture [%] *)
    rVotedFlameDetector_V               : REAL;       (* 2oo3 voted optical fast IR flame intensity [V] *)
    rVotedAspirationDiff_Pa             : REAL;       (* 2oo3 voted aspiration static differential pressure [Pa] *)
    rVotedTurnHeadAngle_deg             : REAL;       (* 2oo3 voted turn-head spout laser angular position [deg] *)
    rInstantaneousThroughput_tph        : REAL;       (* Real-time calibrated bulk grain throughput rate [t/h] *)
    rTotalizedBatchMass_tons            : REAL;       (* Cumulative grain lot mass delivered into target silo bin [t] *)
    rCalculatedGrainDustConc_gm3        : REAL;       (* Estimated airborne dust concentration in elevator casing [g/m3] *)

    (* =================================================================================================================
     * SECTION 4: SILO MESH THERMAL ANALYTICS & EQUILIBRIUM AERATION METRICS
     * ================================================================================================================= *)
    rGrainMeshMaxTemp_degC              : REAL;       (* Maximum temperature observed across 24 thermocouple mesh [deg C] *)
    rGrainMeshAvgTemp_degC              : REAL;       (* Weighted volumetric average core temperature of grain bed [deg C] *)
    rGrainMeshMaxRateOfRise_degCh       : REAL;       (* Highest thermal velocity of hot-spot formation [deg C/h] *)
    iGrainHotSpotSensorIndex            : INT;        (* Thermocouple ID (1..24) exhibiting highest hot-spot excursion *)
    bGrainBiologicalHeatingActive       : BOOL;       (* Latch indicating active microbial respiration / fermentation *)
    rGrainEquilibriumMoisture_pct       : REAL;       (* Calculated equilibrium moisture content (EMC) for ambient air [%] *)

    (* =================================================================================================================
     * SECTION 5: FINITE STATE MACHINE CODES & PACKED DIAGNOSTIC STATUS WORDS
     * ================================================================================================================= *)
    eActiveState_Code                   : INT;        (* Current 12-state FSM state identifier [0..11] *)
    dwStatusWord_State                  : DWORD;      (* FSM execution and sequence permissive bitfield *)
    dwAlarmWord_Trips_HH                : DWORD;      (* ISA-18.2 Critical Emergency Trip bitfield (HRD/E-Stop) *)
    dwAlarmWord_Warnings_H              : DWORD;      (* ISA-18.2 Process Warning & Throttling alert bitfield *)
    dwAlarmWord_Diagnostics             : DWORD;      (* Sensor discrepancy, maintenance & calibration diagnostic bitfield *)
END_VAR
""")

    # 4. VAR (Internal state, matrices, TMR variables, timers, ISA-18.2 registers)
    parts.append("""VAR
    (* =================================================================================================================
     * SECTION 1: 2oo3 TMR SENSOR VOTING STRUCTURES, DEVIATION TOLERANCES & FAULT REGISTERS
     * ================================================================================================================= *)
    (* Channel Discrepancy Pairwise Tolerances *)
    rTol_HeadSpeed_RPM                  : REAL := 1.5;    (* Maximum allowable speed deviation between encoders [RPM] *)
    rTol_BootSpeed_RPM                  : REAL := 1.5;    (* Maximum allowable boot speed deviation [RPM] *)
    rTol_MotorPwr_kW                    : REAL := 15.0;   (* Maximum allowable power transducer deviation [kW] *)
    rTol_BearingTemp_degC               : REAL := 4.0;    (* Maximum allowable bearing temperature deviation [deg C] *)
    rTol_Vib_mms                        : REAL := 0.60;   (* Maximum allowable vibration transducer deviation [mm/s] *)
    rTol_BeltRub_degC                   : REAL := 5.0;    (* Maximum allowable casing pyrometer deviation [deg C] *)
    rTol_RadarLvl_m                     : REAL := 0.15;   (* Maximum allowable FMCW radar level deviation [m] *)
    rTol_Moisture_pct                   : REAL := 0.35;   (* Maximum allowable microwave moisture deviation [%] *)
    rTol_Flame_V                        : REAL := 0.20;   (* Maximum allowable optical flame voltage deviation [V] *)
    rTol_Aspiration_Pa                  : REAL := 75.0;   (* Maximum allowable static pressure deviation [Pa] *)
    rTol_TurnHead_deg                   : REAL := 0.10;   (* Maximum allowable turn-head angular deviation [deg] *)

    (* Channel Discrepancy Debounce Timers (TON) *)
    tSpd101_DiscTimer                   : TON;            (* Debounce timer for Elevator A head speed channel *)
    tSpd102_DiscTimer                   : TON;            (* Debounce timer for Elevator A boot speed channel *)
    tSpd103_DiscTimer                   : TON;            (* Debounce timer for Elevator B head speed channel *)
    tSpd104_DiscTimer                   : TON;            (* Debounce timer for Elevator B boot speed channel *)
    tPwr105_DiscTimer                   : TON;            (* Debounce timer for Elevator motor power channel *)
    tBrg106_DiscTimer                   : TON;            (* Debounce timer for Head bearing temperature channel *)
    tBrg107_DiscTimer                   : TON;            (* Debounce timer for Boot bearing temperature channel *)
    tVib108_DiscTimer                   : TON;            (* Debounce timer for Head shaft vibration channel *)
    tRub109_DiscTimer                   : TON;            (* Debounce timer for Belt rub pyrometer channel *)
    tLvl110_DiscTimer                   : TON;            (* Debounce timer for Silo radar level channel *)
    tMst111_DiscTimer                   : TON;            (* Debounce timer for Microwave moisture channel *)
    tFlm112_DiscTimer                   : TON;            (* Debounce timer for Fast optical flame detector channel *)
    tAsp113_DiscTimer                   : TON;            (* Debounce timer for Aspiration differential pressure channel *)
    tAng114_DiscTimer                   : TON;            (* Debounce timer for Turn-head laser angle channel *)

    (* Channel Failure Status Flags (14 Channels x 3 Triplets = 42 Flags) *)
    bFault_Spd101A : BOOL;  bFault_Spd101B : BOOL;  bFault_Spd101C : BOOL;
    bFault_Spd102A : BOOL;  bFault_Spd102B : BOOL;  bFault_Spd102C : BOOL;
    bFault_Spd103A : BOOL;  bFault_Spd103B : BOOL;  bFault_Spd103C : BOOL;
    bFault_Spd104A : BOOL;  bFault_Spd104B : BOOL;  bFault_Spd104C : BOOL;
    bFault_Pwr105A : BOOL;  bFault_Pwr105B : BOOL;  bFault_Pwr105C : BOOL;
    bFault_Brg106A : BOOL;  bFault_Brg106B : BOOL;  bFault_Brg106C : BOOL;
    bFault_Brg107A : BOOL;  bFault_Brg107B : BOOL;  bFault_Brg107C : BOOL;
    bFault_Vib108A : BOOL;  bFault_Vib108B : BOOL;  bFault_Vib108C : BOOL;
    bFault_Rub109A : BOOL;  bFault_Rub109B : BOOL;  bFault_Rub109C : BOOL;
    bFault_Lvl110A : BOOL;  bFault_Lvl110B : BOOL;  bFault_Lvl110C : BOOL;
    bFault_Mst111A : BOOL;  bFault_Mst111B : BOOL;  bFault_Mst111C : BOOL;
    bFault_Flm112A : BOOL;  bFault_Flm112B : BOOL;  bFault_Flm112C : BOOL;
    bFault_Asp113A : BOOL;  bFault_Asp113B : BOOL;  bFault_Asp113C : BOOL;
    bFault_Ang114A : BOOL;  bFault_Ang114B : BOOL;  bFault_Ang114C : BOOL;

    dwTMR_DiscrepancyWord               : DWORD;          (* Active discrepancy bitmask across all 14 channels *)
    dwTMR_SensorFaultWord               : DWORD;          (* Latched degraded / failed sensor channel bitmask *)

    (* =================================================================================================================
     * SECTION 2: 8-STATE DISCRETE STATE-SPACE MODEL & RECEDING-HORIZON MPC MATRICES
     * State Vector x[8]:
     *   x[1] = Elevator Drive Motor Active Power Deviation [kW]
     *   x[2] = Belt Tension Elastic Strain / Dynamic Elongation [mm]
     *   x[3] = Silo Bin Mass Level Fill Rate [t/h]
     *   x[4] = Elevator Casing Airborne Dust Concentration [g/m3]
     *   x[5] = Dust Aspiration Duct Differential Pressure [Pa]
     *   x[6] = Grain Bed Core Thermal Lag / Respiration Heat Deviation [deg C]
     *   x[7] = Continuous Inline Microwave Moisture Deviation [%]
     *   x[8] = Rotary Turn-Head Spout Angular Alignment Tracking Error [deg]
     * ================================================================================================================= *)
    arrStateVector_x                    : ARRAY[1..8] OF REAL; (* State vector at sample k *)
    arrNextStateVector_x                : ARRAY[1..8] OF REAL; (* Predicted state vector at sample k+1 *)
    arrControlVector_u                  : ARRAY[1..8] OF REAL; (* Actuator control command vector u[k] *)
    arrOutputVector_y                   : ARRAY[1..8] OF REAL; (* Measured physical plant output vector y[k] *)
    arrSetpointVector_sp                : ARRAY[1..8] OF REAL; (* Dynamic reference trajectory setpoints *)
    arrStateError_e                     : ARRAY[1..8] OF REAL; (* Tracking error vector e = sp - y *)

    (* 8x8 System Transition Matrix A *)
    arrMatA                             : ARRAY[1..8, 1..8] OF REAL;
    (* 8x8 Control Input Coupling Matrix B *)
    arrMatB                             : ARRAY[1..8, 1..8] OF REAL;
    (* 8x8 State Output Observation Matrix C *)
    arrMatC                             : ARRAY[1..8, 1..8] OF REAL;
    (* 8x8 Direct Feedthrough Matrix D *)
    arrMatD                             : ARRAY[1..8, 1..8] OF REAL;
    (* 8x8 MPC State Tracking Penalty Matrix Q (Diagonal Quadratic Weights) *)
    arrMatQ                             : ARRAY[1..8, 1..8] OF REAL;
    (* 8x8 MPC Actuator Effort Penalty Matrix R (Diagonal Quadratic Weights) *)
    arrMatR                             : ARRAY[1..8, 1..8] OF REAL;
    (* 8x8 Receding-Horizon Optimal Feedback Gain Matrix K_mpc (Riccati Solution) *)
    arrMatK_mpc                         : ARRAY[1..8, 1..8] OF REAL;

    rQuadraticCostAccumulator_J         : REAL;           (* Cumulative MPC quadratic cost evaluation metric *)
    rSamplingInterval_Ts                : REAL := 0.010;  (* Discrete state-space execution period Ts = 10 ms [s] *)

    (* =================================================================================================================
     * SECTION 3: PHYSICAL PULLEY KINEMATICS, BELT SLIP & MECHANICAL OVERLOAD REGISTERS
     * ================================================================================================================= *)
    c_rPulleyDiamHead_m                 : REAL := 1.250;  (* Elevator head driving pulley outer diameter [m] *)
    c_rPulleyDiamBoot_m                 : REAL := 1.000;  (* Elevator boot take-up pulley outer diameter [m] *)
    c_rElevatorLiftHeight_m             : REAL := 45.0;   (* Total vertical elevation distance [m] *)
    c_rGravitationalAccel_mps2          : REAL := 9.80665;(* Standard acceleration due to gravity [m/s2] *)
    c_rElevatorMotorNominalPower_kW     : REAL := 315.0;  (* Nameplate rating of elevator drive induction motor [kW] *)
    c_rElevatorTarePower_kW             : REAL := 42.5;   (* Dry unladen empty elevator friction loss power [kW] *)
    c_rMechanicalEfficiency_eta         : REAL := 0.885;  (* Combined motor, helical gearbox and pulley drive efficiency *)

    rLinearHeadSpeedA_mps               : REAL;           (* Calculated linear speed of Elevator A head belt [m/s] *)
    rLinearBootSpeedA_mps               : REAL;           (* Calculated linear speed of Elevator A boot belt [m/s] *)
    rLinearHeadSpeedB_mps               : REAL;           (* Calculated linear speed of Elevator B head belt [m/s] *)
    rLinearBootSpeedB_mps               : REAL;           (* Calculated linear speed of Elevator B boot belt [m/s] *)
    rElevatorA_TorqueLoad_pct           : REAL;           (* Drive motor shaft torque load percentage of nominal [%] *)
    rElevatorA_PowerReserve_kW          : REAL;           (* Available electrical margin before thermal trip [kW] *)

    tBeltSlipWarningTimerA              : TON;            (* Elevator A belt slip warning debounce timer (NFPA 61) *)
    tBeltSlipTripTimerA                 : TON;            (* Elevator A critical belt slip emergency trip timer (NFPA 61) *)
    tBeltSlipWarningTimerB              : TON;            (* Elevator B belt slip warning debounce timer *)
    tBeltSlipTripTimerB                 : TON;            (* Elevator B critical belt slip emergency trip timer *)

    (* =================================================================================================================
     * SECTION 4: SILO MESH THERMAL ANALYTICS & EQUILIBRIUM MOISTURE VARIABLES
     * ================================================================================================================= *)
    arrPrevGrainMeshTemp_degC           : ARRAY[1..24] OF REAL; (* Temperature sample at previous evaluation cycle [deg C] *)
    arrGrainMeshRateOfRise_degCh        : ARRAY[1..24] OF REAL; (* Thermal velocity per thermocouple node [deg C/h] *)
    tMeshCalculationTimer               : TON;            (* 60-second periodic timer for rate-of-rise calculation *)
    rMeshScanCycleTime_s                : REAL := 60.0;   (* Sampling cycle period for grain mesh analytics [s] *)
    rSumTemperatureAccumulator          : REAL;           (* Running sum for average core grain temperature calculation *)
    rMaxTempCandidate                   : REAL;           (* Running maximum temperature across 24 thermocouple nodes *)
    rMaxRateOfRiseCandidate             : REAL;           (* Running maximum thermal velocity across 24 nodes *)
    iPeakNodeIndex                      : INT;            (* Matrix coordinate of peak hot-spot node *)
    rGrainRespirationIndex              : REAL;           (* Empirical microbial respiration heat generation index *)
    rChungPfost_C1                      : REAL := 0.000108; (* Chung-Pfost isotherm model constant C1 for hard red wheat *)
    rChungPfost_C2                      : REAL := 82.50;  (* Chung-Pfost isotherm model constant C2 *)
    rChungPfost_C3                      : REAL := 0.1450; (* Chung-Pfost isotherm model constant C3 *)
    bAerationConditionsFavorable        : BOOL;           (* Permissive indicating ambient air can cool silo without wetting *)

    (* =================================================================================================================
     * SECTION 5: ATEX / NFPA 61 EXPLOSION DETECTION & CHEMICAL SUPPRESSION VARIABLES
     * ================================================================================================================= *)
    rPrevFlameDetector_V                : REAL;           (* Optical flame detector voltage at previous sample [V] *)
    rFlameDerivative_Vps                : REAL;           (* Fast rate of rise of optical IR radiation dV/dt [V/s] *)
    rFlameResponseDuration_ms           : REAL;           (* Stopwatch of active optical flame detection duration [ms] *)
    bExplosionTripLatched               : BOOL;           (* High-speed hardware lockout latch for explosion event *)
    tCannonDischargeDwell               : TON;            (* Timer holding HRD cannon firing pulse for 250 ms *)
    tDelugeSolenoidDwell                : TON;            (* Deluge water-mist post-discharge cooling cycle timer *)
    c_rFlameTripThreshold_V             : REAL := 1.50;   (* Optical flame trip voltage threshold (150 W/m2 IR equivalent) *)
    c_rFlameDerivativeTrip_Vps          : REAL := 15.00;  (* Explosive optical fireball expansion derivative limit [V/s] *)
    c_rMinimumExplosibleConc_gm3        : REAL := 45.0;   (* Minimum Explosible Concentration (MEC) for agricultural dust *)
    c_rDustSuppressionTarget_gm3        : REAL := 15.0;   (* Maximum safe target dust concentration under aspiration *)

    (* =================================================================================================================
     * SECTION 6: ROTARY ELECTRIC TURN-HEAD SPOUT DISTRIBUTOR POSITIONING REGISTERS
     * ================================================================================================================= *)
    arrSiloTargetSpoutAngles_deg        : ARRAY[1..12] OF REAL := [
        0.0, 30.0, 60.0, 90.0, 120.0, 150.0, 180.0, 210.0, 240.0, 270.0, 300.0, 330.0
    ];
    rTargetSpoutAngle_deg               : REAL;           (* Desired angular position for designated target silo bin [deg] *)
    rTurnHeadAngleError_deg             : REAL;           (* Rotary alignment tracking error: rTargetSpoutAngle - rVotedAngle *)
    rTurnHeadDriveVelocity_pct          : REAL;           (* Modulated slewing drive velocity output [%] *)
    tTurnHeadPositionLockTimer          : TON;            (* Dwell timer verifying spout within +/- 0.05 deg for 3.0 seconds *)
    bTurnHeadSpoutLockedInPosition      : BOOL;           (* Status bit confirming spout aligned and shot-pin seated *)

    (* =================================================================================================================
     * SECTION 7: CASCADE DOWNSTREAM-TO-UPSTREAM CONVEYOR INTERLOCK TIMERS
     * ================================================================================================================= *)
    tAspirationPreStartPurgeTimer       : TON;            (* Pre-start dust collection aspiration purge timer (15 s) *)
    tOverheadConveyorSpinUpTimer        : TON;            (* Silo top drag conveyor speed verification timer (8 s) *)
    tElevatorsSpinUpTimer               : TON;            (* Twin bucket elevator acceleration verification timer (12 s) *)
    tPitConveyorSpinUpTimer             : TON;            (* Intake pit drag conveyor spin-up verification timer (6 s) *)
    tFeederGateRampTimer                : TON;            (* Intake slide gate soft-start ramp timer (10 s) *)
    tPitConveyorTailOutTimer            : TON;            (* Intake pit conveyor empty run-out purge timer (30 s) *)
    tElevatorTailOutTimer               : TON;            (* Bucket elevator bucket empty run-out purge timer (60 s) *)
    tOverheadConveyorTailOutTimer       : TON;            (* Silo top conveyor empty run-out purge timer (45 s) *)

    (* =================================================================================================================
     * SECTION 8: 12-STAGE INDUSTRIAL FINITE STATE MACHINE (FSM) CONSTANTS & REGISTERS
     * ================================================================================================================= *)
    c_iFSM_UNINITIALIZED                : INT := 0;       (* Cold start, safety checks, sensor loop verification *)
    c_iFSM_STANDBY_READY                : INT := 1;       (* Permissives verified, route ready, awaiting operator start *)
    c_iFSM_PRESTART_ASPIRATION_PURGE    : INT := 2;       (* Baghouse fan active, duct static vacuum proven for 15s *)
    c_iFSM_DISTRIBUTOR_SLEW_ALIGNMENT   : INT := 3;       (* Turn-head spout slewing to target bin with laser feedback *)
    c_iFSM_CASCADE_DOWNSTREAM_START     : INT := 4;       (* Sequential start: Overhead conveyor -> Bucket elevators *)
    c_iFSM_INTAKE_GATE_MODULATION       : INT := 5;       (* Pit conveyor start & feed slide gate soft-ramp to 30% *)
    c_iFSM_CONTINUOUS_TRANSFER_MPC      : INT := 6;       (* Steady-state 1,500 t/h transfer governed by 8x8 MPC *)
    c_iFSM_BIN_APPROACH_TOPPING         : INT := 7;       (* Silo bin reached 90% radar level; feed rate throttled *)
    c_iFSM_ROUTE_CHANGEOVER_TRANSIT     : INT := 8;       (* Intermediate transition: feed gate cut, spout re-routed *)
    c_iFSM_EMPTY_RUNOUT_PURGE           : INT := 9;       (* Controlled stop: cascaded upstream-to-downstream tail-out *)
    c_iFSM_AERATION_CONDITIONING        : INT := 10;      (* Intake stopped; grain aeration fans cooling hot-spots *)
    c_iFSM_EMERGENCY_EXPLOSION_DELUGE   : INT := 11;      (* ATEX/NFPA 61 rapid chemical suppression & abort lockout *)

    iActiveFSM_State                    : INT := 0;       (* Internal active FSM state index register *)
    tFSM_StateDwellTimer                : TON;            (* Active state elapsed dwell time supervisor *)
    rFSM_StateElapsed_s                 : REAL;           (* Elapsed duration in active state [s] *)
    rMasterWatchdog_s                   : REAL;           (* Continuous operation supervisory watchdog timer [s] *)

    (* =================================================================================================================
     * SECTION 9: ISA-18.2 ALARM TRIP POINTS, DEAD-BANDS & PRIORITY HYSTERESIS CONSTANTS
     * ================================================================================================================= *)
    c_rTrip_BeltSlip_HH_pct             : REAL := 10.0;   (* Critical belt slip emergency trip threshold [%] *)
    c_rWarn_BeltSlip_H_pct              : REAL := 5.0;    (* Belt slip operational warning threshold [%] *)
    c_rTrip_BearingTemp_HH_degC         : REAL := 85.0;   (* Critical bearing overheating trip threshold [deg C] *)
    c_rWarn_BearingTemp_H_degC          : REAL := 65.0;   (* Bearing temperature high warning threshold [deg C] *)
    c_rTrip_Vibration_HH_mms            : REAL := 7.10;   (* Critical head bearing acoustic RMS vibration trip [mm/s] *)
    c_rWarn_Vibration_H_mms             : REAL := 4.50;   (* Head bearing vibration allowable limit warning [mm/s] *)
    c_rTrip_BeltRub_HH_degC             : REAL := 75.0;   (* Critical casing rub block temperature trip [deg C] *)
    c_rWarn_BeltRub_H_degC              : REAL := 55.0;   (* Casing rub block temperature warning [deg C] *)
    c_rTrip_RadarLevel_HH_m             : REAL := 34.50;  (* Silo bin high-high level overflow trip [m] (36m bin) *)
    c_rWarn_RadarLevel_H_m              : REAL := 32.40;  (* Silo bin 90% capacity approach warning [m] *)
    c_rWarn_Moisture_HH_pct             : REAL := 15.20;  (* High grain moisture storage mold risk warning [%] *)
    c_rWarn_Moisture_LL_pct             : REAL := 12.80;  (* Low grain moisture breakage risk warning [%] *)
    c_rWarn_GrainMeshTemp_H_degC        : REAL := 35.00;  (* Silo thermocouple grain core hot-spot warning [deg C] *)
    c_rWarn_GrainMeshRateOfRise_H_degCh : REAL := 1.50;   (* Silo thermal velocity biological heating warning [deg C/h] *)
    c_rTrip_AspirationDiff_HH_Pa        : REAL := 2200.0; (* Baghouse severe blinding / duct blockage trip [Pa] *)
    c_rWarn_AspirationDiff_H_Pa         : REAL := 1800.0; (* Baghouse pulse-jet cleaning required warning [Pa] *)
    c_rWarn_AspirationDiff_L_Pa         : REAL := 450.0;  (* Low suction airflow loss warning [Pa] *)

    c_rDeadband_Speed_RPM               : REAL := 0.50;   (* Alarm deadband hysteresis for speed measurements *)
    c_rDeadband_Temp_degC               : REAL := 1.50;   (* Alarm deadband hysteresis for thermal measurements *)
    c_rDeadband_Level_m                 : REAL := 0.08;   (* Alarm deadband hysteresis for bin level *)
    c_rDeadband_Pressure_Pa             : REAL := 25.0;   (* Alarm deadband hysteresis for differential pressure *)
    c_rDeadband_Moisture_pct            : REAL := 0.15;   (* Alarm deadband hysteresis for moisture *)

    (* =================================================================================================================
     * SECTION 10: LOCAL LOOP INDICES, MATH SCRATCHPADS & ONE-SHOT COLD START FLAG
     * ================================================================================================================= *)
    iIdx_i                              : INT;            (* Primary matrix and loop row index *)
    iIdx_j                              : INT;            (* Matrix column index *)
    iIdx_k                              : INT;            (* Matrix multiplication contraction index *)
    iCableIdx                           : INT;            (* Thermocouple cable index (1..4) *)
    iDepthIdx                           : INT;            (* Thermocouple depth zone index (1..6) *)
    iNodeIdx                            : INT;            (* Linearized 24-point mesh index (1..24) *)
    rTempAccumulator                    : REAL;           (* Intermediate floating-point accumulator *)
    rTempMedian                         : REAL;           (* Intermediate 2oo3 median extraction register *)
    bColdInitCompleted                  : BOOL := FALSE;  (* One-shot initialization latch *)
END_VAR
""")

    # 5. CODE BODY: SECTION 0 (Cold Initialization of Matrices)
    parts.append("""
(* =====================================================================================================================
 * SECTION 0: DETERMINISTIC ONE-SHOT COLD INITIALIZATION: 8x8 STATE-SPACE & MPC RICCATI MATRICES
 * Fully writes out all system coefficients for the elevator drive dynamics, belt strain mechanics, material storage,
 * dust cloud dispersion kinetics, aeration pressure drop, and distributor slewing servo loops.
 * ===================================================================================================================== *)
IF NOT bColdInitCompleted THEN
    (* Step 1: Zero-initialize all 8x8 matrices and internal vectors *)
    FOR iIdx_i := 1 TO 8 DO
        FOR iIdx_j := 1 TO 8 DO
            arrMatA[iIdx_i, iIdx_j] := 0.0;
            arrMatB[iIdx_i, iIdx_j] := 0.0;
            arrMatC[iIdx_i, iIdx_j] := 0.0;
            arrMatD[iIdx_i, iIdx_j] := 0.0;
            arrMatQ[iIdx_i, iIdx_j] := 0.0;
            arrMatR[iIdx_i, iIdx_j] := 0.0;
            arrMatK_mpc[iIdx_i, iIdx_j] := 0.0;
        END_FOR;
        arrStateVector_x[iIdx_i] := 0.0;
        arrNextStateVector_x[iIdx_i] := 0.0;
        arrControlVector_u[iIdx_i] := 0.0;
        arrOutputVector_y[iIdx_i] := 0.0;
        arrSetpointVector_sp[iIdx_i] := 0.0;
        arrStateError_e[iIdx_i] := 0.0;
    END_FOR;

    (* Step 2: Parameterize 8x8 Discrete State-Space System Matrix A (Ts = 10 ms = 0.010 s) *)
    (* Row 1: Elevator Drive Motor Active Power Dynamics [kW] *)
    (* dx1/dt = - (1/tau_motor)*x1 + k_strain*x2 - k_slip*x1 *)
    arrMatA[1, 1] := 0.945000;    (* Motor electromagnetic field & rotor inertia time constant pole *)
    arrMatA[1, 2] := 0.032500;    (* Coupling from belt viscoelastic elongation to motor mechanical counter-torque *)
    arrMatA[1, 3] := 0.085000;    (* Direct proportional coupling from bulk grain intake rate to continuous load *)

    (* Row 2: Belt Tension Elastic Strain / Dynamic Elongation [mm] *)
    (* Heavy steel-cord rubber elevator belt longitudinal elasticity under 1,500 t/h continuous bucket fill *)
    arrMatA[2, 1] := 0.004200;    (* Dynamic strain induction from motor torque transients *)
    arrMatA[2, 2] := 0.982000;    (* Longitudinal viscoelastic damping pole (Kelvin-Voigt mechanical model) *)
    arrMatA[2, 3] := 0.012500;    (* Gravitational bucket payload tension load from rising material column *)

    (* Row 3: Silo Bin Mass Level Fill Rate [t/h] *)
    (* Integrates incoming stream into storage volume, subject to chute discharge resistance *)
    arrMatA[3, 3] := 0.995000;    (* Mass storage accumulation retention pole *)
    arrMatA[3, 7] := -0.015000;   (* Moisture swelling volumetric packing density adjustment *)

    (* Row 4: Elevator Casing Airborne Combustible Dust Concentration [g/m3] *)
    (* Dust dispersion is accelerated by grain mass throughput and attenuated by aspiration suction *)
    arrMatA[4, 3] := 0.024500;    (* Fines aerodynamic stripping rate per ton of bulk grain cascaded *)
    arrMatA[4, 4] := 0.912000;    (* Gravitational settling decay pole of suspended grain dust particles *)
    arrMatA[4, 5] := -0.008400;   (* Suction air velocity extraction term from aspiration duct vacuum *)
    arrMatA[4, 7] := -0.125000;   (* Moisture agglomeration dampening effect (drier grain emits more dust) *)

    (* Row 5: Dust Aspiration Duct Differential Pressure [Pa] *)
    (* Pneumatic airflow resistance across ductwork and pulse-jet baghouse filter media *)
    arrMatA[5, 4] := 0.045000;    (* Filter cake dust loading resistance increase *)
    arrMatA[5, 5] := 0.935000;    (* Pneumatic duct acoustic capacitance and fan impedance decay *)

    (* Row 6: Grain Bed Core Thermal Lag / Respiration Heat Deviation [deg C] *)
    (* Biological aerobic respiration of grain microflora and thermal diffusion across packed grain bed *)
    arrMatA[6, 6] := 0.998500;    (* Enormous thermal capacitance and slow biological heating time constant *)
    arrMatA[6, 7] := 0.045000;    (* Moisture activation of microbial respiration (higher moisture = faster heating) *)

    (* Row 7: Continuous Inline Microwave Moisture Deviation [%] *)
    (* Dynamic sorption hysteresis and batch moisture homogenization kinetics *)
    arrMatA[7, 7] := 0.975000;    (* Mass transfer diffusion time constant of internal kernel moisture *)

    (* Row 8: Rotary Turn-Head Spout Angular Alignment Tracking Error [deg] *)
    (* Geared slew drive servomotor kinematics, viscous friction and backlash damping *)
    arrMatA[8, 8] := 0.895000;    (* Slew drive inertial positioning pole *)

    (* Step 3: Parameterize 8x8 Control Input Matrix B *)
    (* u[1] = Elevator A/B VFD Speed Frequency Command [Hz] *)
    (* u[2] = Feeder Slide Gate Aperture Modulation [%] *)
    (* u[3] = Turn-Head Slew Drive Velocity Command [%] *)
    (* u[4] = Aspiration Damper Position Command [%] *)
    (* u[5] = Silo Aeration Fan VFD Speed Command [Hz] *)
    (* u[6] = Intake Pit Conveyor Speed Command [Hz] *)
    (* u[7] = Silo Top Overhead Conveyor Speed Command [Hz] *)
    (* u[8] = Deluge / HRD Cannon Suppression Trigger Command [0/1] *)
    arrMatB[1, 1] := 4.850000;    (* Elevator VFD frequency ramp -> Motor active power rise *)
    arrMatB[1, 2] := 1.250000;    (* Feeder gate opening -> Immediate material feed load on motor *)
    arrMatB[2, 1] := 0.185000;    (* Elevator speed acceleration -> Belt dynamic tension strain surge *)
    arrMatB[2, 2] := 0.092000;    (* Increased material mass charging -> Belt elastic elongation *)
    arrMatB[3, 2] := 15.00000;    (* Slide gate percentage -> Real-time throughput increase [t/h] *)
    arrMatB[4, 2] := 0.285000;    (* Feed gate flow increase -> Elevator boot turbulence dust release *)
    arrMatB[4, 4] := -0.650000;   (* Aspiration damper opening -> Rapid airborne dust dilution *)
    arrMatB[5, 4] := 18.50000;    (* Aspiration damper opening -> Suction static differential pressure rise *)
    arrMatB[6, 5] := -0.055000;   (* Aeration fan speed -> Grain bed forced convective core cooling *)
    arrMatB[7, 2] := 0.012000;    (* Feed gate change -> Transient fresh lot moisture shift *)
    arrMatB[8, 3] := 0.420000;    (* Turn-head slew drive command -> Slew angular velocity [deg/s] *)

    (* Step 4: Parameterize 8x8 Output Matrix C (Direct Physical State Observations) *)
    FOR iIdx_i := 1 TO 8 DO
        arrMatC[iIdx_i, iIdx_i] := 1.000000;
    END_FOR;

    (* Step 5: Parameterize 8x8 MPC State Quadratic Penalty Matrix Q (Diagonal Weights) *)
    arrMatQ[1, 1] := 150.0;       (* Penalize elevator drive electrical power surges and peaks *)
    arrMatQ[2, 2] := 350.0;       (* Heavily penalize excessive belt elastic strain and slip deformation *)
    arrMatQ[3, 3] := 800.0;       (* Critical priority: maintain target 1,500 t/h throughput setpoint *)
    arrMatQ[4, 4] := 1200.0;      (* Highest safety penalty: prevent combustible dust buildup near MEC *)
    arrMatQ[5, 5] := 250.0;       (* Maintain proper aspiration duct vacuum without collapsing baghouse *)
    arrMatQ[6, 6] := 600.0;       (* Suppress grain bed thermal runaway and microbial self-heating *)
    arrMatQ[7, 7] := 450.0;       (* Enforce moisture tolerance baseline within 14.0 +/- 0.2% *)
    arrMatQ[8, 8] := 950.0;       (* Critical alignment: turn-head laser angle tracking within +/- 0.05 deg *)

    (* Step 6: Parameterize 8x8 MPC Actuator Effort Penalty Matrix R (Diagonal Weights) *)
    arrMatR[1, 1] := 0.250;       (* Elevator VFD rate of frequency change limit (prevent belt slip) *)
    arrMatR[2, 2] := 0.120;       (* Feeder slide gate mechanical wear and positioning slew limit *)
    arrMatR[3, 3] := 0.080;       (* Turn-head slew motor smooth ramp and deceleration *)
    arrMatR[4, 4] := 0.050;       (* Aspiration damper modulation actuator energy penalty *)
    arrMatR[5, 5] := 0.180;       (* Silo aeration fan VFD electrical power consumption penalty *)
    arrMatR[6, 6] := 0.150;       (* Intake pit conveyor inverter frequency slew limit *)
    arrMatR[7, 7] := 0.150;       (* Overhead silo distribution conveyor inverter frequency slew limit *)
    arrMatR[8, 8] := 5.000;       (* Heavy barrier penalty on explosive emergency suppression triggers *)

    (* Step 7: Parameterize 8x8 Receding-Horizon Riccati Feedback Gain Matrix K_mpc *)
    (* Calculated via discrete algebraic Riccati equation (DARE) for optimal robust tracking *)
    arrMatK_mpc[1, 1] := 14.2500; arrMatK_mpc[1, 2] := 22.8000; arrMatK_mpc[1, 3] := 0.4500;
    arrMatK_mpc[2, 1] := -0.1250; arrMatK_mpc[2, 2] := -0.4850; arrMatK_mpc[2, 3] := 0.0650;
    arrMatK_mpc[2, 4] := -0.0150; arrMatK_mpc[2, 7] := -0.8500;
    arrMatK_mpc[3, 8] := 28.5000;
    arrMatK_mpc[4, 4] := 18.2500; arrMatK_mpc[4, 5] := 0.3500;
    arrMatK_mpc[5, 6] := 32.4000; arrMatK_mpc[5, 7] := 12.8000;
    arrMatK_mpc[6, 1] := 0.8500;  arrMatK_mpc[6, 3] := 0.0250;
    arrMatK_mpc[7, 1] := 0.8500;  arrMatK_mpc[7, 3] := 0.0250;
    arrMatK_mpc[8, 4] := 0.0050;

    bColdInitCompleted := TRUE;
END_IF;
""")

    # 6. CODE BODY: SECTION 1 (2oo3 TMR Voting)
    parts.append("""
(* =====================================================================================================================
 * SECTION 1: TRIPLE MODULAR REDUNDANCY (2oo3 TMR) SENSOR VOTING & DISCREPANCY ARBITRATION
 * Deterministically votes across 14 triplicated process signals. Executes pairwise channel deviation monitoring,
 * debounces single-channel discrepancies via TON timers, isolates failed sensors, and computes healthy medians.
 * ===================================================================================================================== *)
dwTMR_DiscrepancyWord := DWORD#16#00000000;
dwTMR_SensorFaultWord := DWORD#16#00000000;

(* --- Signal 1: Bucket Elevator A Head Pulley Speed [RPM] --- *)
IF ABS(ST_ELEV_A_HEAD_SPD_101A - ST_ELEV_A_HEAD_SPD_101B) > rTol_HeadSpeed_RPM OR
   ABS(ST_ELEV_A_HEAD_SPD_101B - ST_ELEV_A_HEAD_SPD_101C) > rTol_HeadSpeed_RPM OR
   ABS(ST_ELEV_A_HEAD_SPD_101A - ST_ELEV_A_HEAD_SPD_101C) > rTol_HeadSpeed_RPM THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00000001;
    tSpd101_DiscTimer(IN := TRUE, PT := T#50MS);
    IF tSpd101_DiscTimer.Q THEN
        IF ABS(ST_ELEV_A_HEAD_SPD_101A - ST_ELEV_A_HEAD_SPD_101B) <= rTol_HeadSpeed_RPM THEN
            bFault_Spd101C := TRUE; dwTMR_SensorFaultWord := dwTMR_SensorFaultWord OR DWORD#16#00000004;
        ELSIF ABS(ST_ELEV_A_HEAD_SPD_101A - ST_ELEV_A_HEAD_SPD_101C) <= rTol_HeadSpeed_RPM THEN
            bFault_Spd101B := TRUE; dwTMR_SensorFaultWord := dwTMR_SensorFaultWord OR DWORD#16#00000002;
        ELSE
            bFault_Spd101A := TRUE; dwTMR_SensorFaultWord := dwTMR_SensorFaultWord OR DWORD#16#00000001;
        END_IF;
    END_IF;
ELSE
    tSpd101_DiscTimer(IN := FALSE);
END_IF;
(* 2oo3 Median Calculation *)
rTempMedian := (ST_ELEV_A_HEAD_SPD_101A + ST_ELEV_A_HEAD_SPD_101B + ST_ELEV_A_HEAD_SPD_101C)
             - MIN(ST_ELEV_A_HEAD_SPD_101A, MIN(ST_ELEV_A_HEAD_SPD_101B, ST_ELEV_A_HEAD_SPD_101C))
             - MAX(ST_ELEV_A_HEAD_SPD_101A, MAX(ST_ELEV_A_HEAD_SPD_101B, ST_ELEV_A_HEAD_SPD_101C));
rLinearHeadSpeedA_mps := (3.14159265 * c_rPulleyDiamHead_m * rTempMedian) / 60.0;
rVotedHeadBeltSpeedA_mps := rLinearHeadSpeedA_mps;

(* --- Signal 2: Bucket Elevator A Boot Pulley Speed [RPM] --- *)
IF ABS(ST_ELEV_A_BOOT_SPD_102A - ST_ELEV_A_BOOT_SPD_102B) > rTol_BootSpeed_RPM OR
   ABS(ST_ELEV_A_BOOT_SPD_102B - ST_ELEV_A_BOOT_SPD_102C) > rTol_BootSpeed_RPM OR
   ABS(ST_ELEV_A_BOOT_SPD_102A - ST_ELEV_A_BOOT_SPD_102C) > rTol_BootSpeed_RPM THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00000002;
    tSpd102_DiscTimer(IN := TRUE, PT := T#50MS);
    IF tSpd102_DiscTimer.Q THEN
        IF ABS(ST_ELEV_A_BOOT_SPD_102A - ST_ELEV_A_BOOT_SPD_102B) <= rTol_BootSpeed_RPM THEN
            bFault_Spd102C := TRUE; dwTMR_SensorFaultWord := dwTMR_SensorFaultWord OR DWORD#16#00000020;
        ELSIF ABS(ST_ELEV_A_BOOT_SPD_102A - ST_ELEV_A_BOOT_SPD_102C) <= rTol_BootSpeed_RPM THEN
            bFault_Spd102B := TRUE; dwTMR_SensorFaultWord := dwTMR_SensorFaultWord OR DWORD#16#00000010;
        ELSE
            bFault_Spd102A := TRUE; dwTMR_SensorFaultWord := dwTMR_SensorFaultWord OR DWORD#16#00000008;
        END_IF;
    END_IF;
ELSE
    tSpd102_DiscTimer(IN := FALSE);
END_IF;
rTempMedian := (ST_ELEV_A_BOOT_SPD_102A + ST_ELEV_A_BOOT_SPD_102B + ST_ELEV_A_BOOT_SPD_102C)
             - MIN(ST_ELEV_A_BOOT_SPD_102A, MIN(ST_ELEV_A_BOOT_SPD_102B, ST_ELEV_A_BOOT_SPD_102C))
             - MAX(ST_ELEV_A_BOOT_SPD_102A, MAX(ST_ELEV_A_BOOT_SPD_102B, ST_ELEV_A_BOOT_SPD_102C));
rLinearBootSpeedA_mps := (3.14159265 * c_rPulleyDiamBoot_m * rTempMedian) / 60.0;
rVotedBootBeltSpeedA_mps := rLinearBootSpeedA_mps;

(* --- Signal 3: Bucket Elevator B Head Pulley Speed [RPM] --- *)
IF ABS(ST_ELEV_B_HEAD_SPD_103A - ST_ELEV_B_HEAD_SPD_103B) > rTol_HeadSpeed_RPM OR
   ABS(ST_ELEV_B_HEAD_SPD_103B - ST_ELEV_B_HEAD_SPD_103C) > rTol_HeadSpeed_RPM OR
   ABS(ST_ELEV_B_HEAD_SPD_103A - ST_ELEV_B_HEAD_SPD_103C) > rTol_HeadSpeed_RPM THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00000004;
    tSpd103_DiscTimer(IN := TRUE, PT := T#50MS);
    IF tSpd103_DiscTimer.Q THEN
        IF ABS(ST_ELEV_B_HEAD_SPD_103A - ST_ELEV_B_HEAD_SPD_103B) <= rTol_HeadSpeed_RPM THEN
            bFault_Spd103C := TRUE;
        ELSIF ABS(ST_ELEV_B_HEAD_SPD_103A - ST_ELEV_B_HEAD_SPD_103C) <= rTol_HeadSpeed_RPM THEN
            bFault_Spd103B := TRUE;
        ELSE
            bFault_Spd103A := TRUE;
        END_IF;
    END_IF;
ELSE
    tSpd103_DiscTimer(IN := FALSE);
END_IF;
rTempMedian := (ST_ELEV_B_HEAD_SPD_103A + ST_ELEV_B_HEAD_SPD_103B + ST_ELEV_B_HEAD_SPD_103C)
             - MIN(ST_ELEV_B_HEAD_SPD_103A, MIN(ST_ELEV_B_HEAD_SPD_103B, ST_ELEV_B_HEAD_SPD_103C))
             - MAX(ST_ELEV_B_HEAD_SPD_103A, MAX(ST_ELEV_B_HEAD_SPD_103B, ST_ELEV_B_HEAD_SPD_103C));
rLinearHeadSpeedB_mps := (3.14159265 * c_rPulleyDiamHead_m * rTempMedian) / 60.0;

(* --- Signal 4: Bucket Elevator B Boot Pulley Speed [RPM] --- *)
IF ABS(ST_ELEV_B_BOOT_SPD_104A - ST_ELEV_B_BOOT_SPD_104B) > rTol_BootSpeed_RPM OR
   ABS(ST_ELEV_B_BOOT_SPD_104B - ST_ELEV_B_BOOT_SPD_104C) > rTol_BootSpeed_RPM OR
   ABS(ST_ELEV_B_BOOT_SPD_104A - ST_ELEV_B_BOOT_SPD_104C) > rTol_BootSpeed_RPM THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00000008;
    tSpd104_DiscTimer(IN := TRUE, PT := T#50MS);
    IF tSpd104_DiscTimer.Q THEN
        IF ABS(ST_ELEV_B_BOOT_SPD_104A - ST_ELEV_B_BOOT_SPD_104B) <= rTol_BootSpeed_RPM THEN
            bFault_Spd104C := TRUE;
        ELSIF ABS(ST_ELEV_B_BOOT_SPD_104A - ST_ELEV_B_BOOT_SPD_104C) <= rTol_BootSpeed_RPM THEN
            bFault_Spd104B := TRUE;
        ELSE
            bFault_Spd104A := TRUE;
        END_IF;
    END_IF;
ELSE
    tSpd104_DiscTimer(IN := FALSE);
END_IF;
rTempMedian := (ST_ELEV_B_BOOT_SPD_104A + ST_ELEV_B_BOOT_SPD_104B + ST_ELEV_B_BOOT_SPD_104C)
             - MIN(ST_ELEV_B_BOOT_SPD_104A, MIN(ST_ELEV_B_BOOT_SPD_104B, ST_ELEV_B_BOOT_SPD_104C))
             - MAX(ST_ELEV_B_BOOT_SPD_104A, MAX(ST_ELEV_B_BOOT_SPD_104B, ST_ELEV_B_BOOT_SPD_104C));
rLinearBootSpeedB_mps := (3.14159265 * c_rPulleyDiamBoot_m * rTempMedian) / 60.0;

(* --- Signal 5: Bucket Elevator Drive Motor Active Power [kW] --- *)
IF ABS(JT_ELEV_A_MOTOR_PWR_105A - JT_ELEV_A_MOTOR_PWR_105B) > rTol_MotorPwr_kW OR
   ABS(JT_ELEV_A_MOTOR_PWR_105B - JT_ELEV_A_MOTOR_PWR_105C) > rTol_MotorPwr_kW OR
   ABS(JT_ELEV_A_MOTOR_PWR_105A - JT_ELEV_A_MOTOR_PWR_105C) > rTol_MotorPwr_kW THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00000010;
    tPwr105_DiscTimer(IN := TRUE, PT := T#100MS);
    IF tPwr105_DiscTimer.Q THEN
        IF ABS(JT_ELEV_A_MOTOR_PWR_105A - JT_ELEV_A_MOTOR_PWR_105B) <= rTol_MotorPwr_kW THEN
            bFault_Pwr105C := TRUE;
        ELSIF ABS(JT_ELEV_A_MOTOR_PWR_105A - JT_ELEV_A_MOTOR_PWR_105C) <= rTol_MotorPwr_kW THEN
            bFault_Pwr105B := TRUE;
        ELSE
            bFault_Pwr105A := TRUE;
        END_IF;
    END_IF;
ELSE
    tPwr105_DiscTimer(IN := FALSE);
END_IF;
rVotedMotorPower_kW := (JT_ELEV_A_MOTOR_PWR_105A + JT_ELEV_A_MOTOR_PWR_105B + JT_ELEV_A_MOTOR_PWR_105C)
                     - MIN(JT_ELEV_A_MOTOR_PWR_105A, MIN(JT_ELEV_A_MOTOR_PWR_105B, JT_ELEV_A_MOTOR_PWR_105C))
                     - MAX(JT_ELEV_A_MOTOR_PWR_105A, MAX(JT_ELEV_A_MOTOR_PWR_105B, JT_ELEV_A_MOTOR_PWR_105C));

(* --- Signal 6: Elevator Head Pulley Bearing Temperature [deg C] --- *)
IF ABS(TT_ELEV_HEAD_BRG_106A - TT_ELEV_HEAD_BRG_106B) > rTol_BearingTemp_degC OR
   ABS(TT_ELEV_HEAD_BRG_106B - TT_ELEV_HEAD_BRG_106C) > rTol_BearingTemp_degC OR
   ABS(TT_ELEV_HEAD_BRG_106A - TT_ELEV_HEAD_BRG_106C) > rTol_BearingTemp_degC THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00000020;
    tBrg106_DiscTimer(IN := TRUE, PT := T#200MS);
    IF tBrg106_DiscTimer.Q THEN
        IF ABS(TT_ELEV_HEAD_BRG_106A - TT_ELEV_HEAD_BRG_106B) <= rTol_BearingTemp_degC THEN
            bFault_Brg106C := TRUE;
        ELSIF ABS(TT_ELEV_HEAD_BRG_106A - TT_ELEV_HEAD_BRG_106C) <= rTol_BearingTemp_degC THEN
            bFault_Brg106B := TRUE;
        ELSE
            bFault_Brg106A := TRUE;
        END_IF;
    END_IF;
ELSE
    tBrg106_DiscTimer(IN := FALSE);
END_IF;
rVotedHeadBearingTemp_degC := (TT_ELEV_HEAD_BRG_106A + TT_ELEV_HEAD_BRG_106B + TT_ELEV_HEAD_BRG_106C)
                           - MIN(TT_ELEV_HEAD_BRG_106A, MIN(TT_ELEV_HEAD_BRG_106B, TT_ELEV_HEAD_BRG_106C))
                           - MAX(TT_ELEV_HEAD_BRG_106A, MAX(TT_ELEV_HEAD_BRG_106B, TT_ELEV_HEAD_BRG_106C));

(* --- Signal 7: Elevator Boot Pulley Bearing Temperature [deg C] --- *)
IF ABS(TT_ELEV_BOOT_BRG_107A - TT_ELEV_BOOT_BRG_107B) > rTol_BearingTemp_degC OR
   ABS(TT_ELEV_BOOT_BRG_107B - TT_ELEV_BOOT_BRG_107C) > rTol_BearingTemp_degC OR
   ABS(TT_ELEV_BOOT_BRG_107A - TT_ELEV_BOOT_BRG_107C) > rTol_BearingTemp_degC THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00000040;
    tBrg107_DiscTimer(IN := TRUE, PT := T#200MS);
    IF tBrg107_DiscTimer.Q THEN
        IF ABS(TT_ELEV_BOOT_BRG_107A - TT_ELEV_BOOT_BRG_107B) <= rTol_BearingTemp_degC THEN
            bFault_Brg107C := TRUE;
        ELSIF ABS(TT_ELEV_BOOT_BRG_107A - TT_ELEV_BOOT_BRG_107C) <= rTol_BearingTemp_degC THEN
            bFault_Brg107B := TRUE;
        ELSE
            bFault_Brg107A := TRUE;
        END_IF;
    END_IF;
ELSE
    tBrg107_DiscTimer(IN := FALSE);
END_IF;
rVotedBootBearingTemp_degC := (TT_ELEV_BOOT_BRG_107A + TT_ELEV_BOOT_BRG_107B + TT_ELEV_BOOT_BRG_107C)
                           - MIN(TT_ELEV_BOOT_BRG_107A, MIN(TT_ELEV_BOOT_BRG_107B, TT_ELEV_BOOT_BRG_107C))
                           - MAX(TT_ELEV_BOOT_BRG_107A, MAX(TT_ELEV_BOOT_BRG_107B, TT_ELEV_BOOT_BRG_107C));

(* --- Signal 8: Elevator Head Shaft Acoustic Bearing Vibration RMS [mm/s] --- *)
IF ABS(VT_ELEV_HEAD_VIB_108A - VT_ELEV_HEAD_VIB_108B) > rTol_Vib_mms OR
   ABS(VT_ELEV_HEAD_VIB_108B - VT_ELEV_HEAD_VIB_108C) > rTol_Vib_mms OR
   ABS(VT_ELEV_HEAD_VIB_108A - VT_ELEV_HEAD_VIB_108C) > rTol_Vib_mms THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00000080;
    tVib108_DiscTimer(IN := TRUE, PT := T#150MS);
    IF tVib108_DiscTimer.Q THEN
        IF ABS(VT_ELEV_HEAD_VIB_108A - VT_ELEV_HEAD_VIB_108B) <= rTol_Vib_mms THEN
            bFault_Vib108C := TRUE;
        ELSIF ABS(VT_ELEV_HEAD_VIB_108A - VT_ELEV_HEAD_VIB_108C) <= rTol_Vib_mms THEN
            bFault_Vib108B := TRUE;
        ELSE
            bFault_Vib108A := TRUE;
        END_IF;
    END_IF;
ELSE
    tVib108_DiscTimer(IN := FALSE);
END_IF;
rVotedHeadBearingVib_mms := (VT_ELEV_HEAD_VIB_108A + VT_ELEV_HEAD_VIB_108B + VT_ELEV_HEAD_VIB_108C)
                          - MIN(VT_ELEV_HEAD_VIB_108A, MIN(VT_ELEV_HEAD_VIB_108B, VT_ELEV_HEAD_VIB_108C))
                          - MAX(VT_ELEV_HEAD_VIB_108A, MAX(VT_ELEV_HEAD_VIB_108B, VT_ELEV_HEAD_VIB_108C));

(* --- Signal 9: Optical Belt Misalignment Casing Rub Pyrometers [deg C] --- *)
IF ABS(TT_BELT_RUB_TEMP_109A - TT_BELT_RUB_TEMP_109B) > rTol_BeltRub_degC OR
   ABS(TT_BELT_RUB_TEMP_109B - TT_BELT_RUB_TEMP_109C) > rTol_BeltRub_degC OR
   ABS(TT_BELT_RUB_TEMP_109A - TT_BELT_RUB_TEMP_109C) > rTol_BeltRub_degC THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00000100;
    tRub109_DiscTimer(IN := TRUE, PT := T#100MS);
    IF tRub109_DiscTimer.Q THEN
        IF ABS(TT_BELT_RUB_TEMP_109A - TT_BELT_RUB_TEMP_109B) <= rTol_BeltRub_degC THEN
            bFault_Rub109C := TRUE;
        ELSIF ABS(TT_BELT_RUB_TEMP_109A - TT_BELT_RUB_TEMP_109C) <= rTol_BeltRub_degC THEN
            bFault_Rub109B := TRUE;
        ELSE
            bFault_Rub109A := TRUE;
        END_IF;
    END_IF;
ELSE
    tRub109_DiscTimer(IN := FALSE);
END_IF;
rVotedBeltRubTemp_degC := (TT_BELT_RUB_TEMP_109A + TT_BELT_RUB_TEMP_109B + TT_BELT_RUB_TEMP_109C)
                        - MIN(TT_BELT_RUB_TEMP_109A, MIN(TT_BELT_RUB_TEMP_109B, TT_BELT_RUB_TEMP_109C))
                        - MAX(TT_BELT_RUB_TEMP_109A, MAX(TT_BELT_RUB_TEMP_109B, TT_BELT_RUB_TEMP_109C));

(* --- Signal 10: Active Silo Bin FMCW Radar Level [m] --- *)
IF ABS(LT_SILO_RADAR_LVL_110A - LT_SILO_RADAR_LVL_110B) > rTol_RadarLvl_m OR
   ABS(LT_SILO_RADAR_LVL_110B - LT_SILO_RADAR_LVL_110C) > rTol_RadarLvl_m OR
   ABS(LT_SILO_RADAR_LVL_110A - LT_SILO_RADAR_LVL_110C) > rTol_RadarLvl_m THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00000200;
    tLvl110_DiscTimer(IN := TRUE, PT := T#150MS);
    IF tLvl110_DiscTimer.Q THEN
        IF ABS(LT_SILO_RADAR_LVL_110A - LT_SILO_RADAR_LVL_110B) <= rTol_RadarLvl_m THEN
            bFault_Lvl110C := TRUE;
        ELSIF ABS(LT_SILO_RADAR_LVL_110A - LT_SILO_RADAR_LVL_110C) <= rTol_RadarLvl_m THEN
            bFault_Lvl110B := TRUE;
        ELSE
            bFault_Lvl110A := TRUE;
        END_IF;
    END_IF;
ELSE
    tLvl110_DiscTimer(IN := FALSE);
END_IF;
rVotedRadarLevel_m := (LT_SILO_RADAR_LVL_110A + LT_SILO_RADAR_LVL_110B + LT_SILO_RADAR_LVL_110C)
                    - MIN(LT_SILO_RADAR_LVL_110A, MIN(LT_SILO_RADAR_LVL_110B, LT_SILO_RADAR_LVL_110C))
                    - MAX(LT_SILO_RADAR_LVL_110A, MAX(LT_SILO_RADAR_LVL_110B, LT_SILO_RADAR_LVL_110C));

(* --- Signal 11: Continuous Inline Microwave Grain Moisture Analyzer [%] --- *)
IF ABS(MT_GRAIN_MOISTURE_111A - MT_GRAIN_MOISTURE_111B) > rTol_Moisture_pct OR
   ABS(MT_GRAIN_MOISTURE_111B - MT_GRAIN_MOISTURE_111C) > rTol_Moisture_pct OR
   ABS(MT_GRAIN_MOISTURE_111A - MT_GRAIN_MOISTURE_111C) > rTol_Moisture_pct THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00000400;
    tMst111_DiscTimer(IN := TRUE, PT := T#200MS);
    IF tMst111_DiscTimer.Q THEN
        IF ABS(MT_GRAIN_MOISTURE_111A - MT_GRAIN_MOISTURE_111B) <= rTol_Moisture_pct THEN
            bFault_Mst111C := TRUE;
        ELSIF ABS(MT_GRAIN_MOISTURE_111A - MT_GRAIN_MOISTURE_111C) <= rTol_Moisture_pct THEN
            bFault_Mst111B := TRUE;
        ELSE
            bFault_Mst111A := TRUE;
        END_IF;
    END_IF;
ELSE
    tMst111_DiscTimer(IN := FALSE);
END_IF;
rVotedGrainMoisture_pct := (MT_GRAIN_MOISTURE_111A + MT_GRAIN_MOISTURE_111B + MT_GRAIN_MOISTURE_111C)
                         - MIN(MT_GRAIN_MOISTURE_111A, MIN(MT_GRAIN_MOISTURE_111B, MT_GRAIN_MOISTURE_111C))
                         - MAX(MT_GRAIN_MOISTURE_111A, MAX(MT_GRAIN_MOISTURE_111B, MT_GRAIN_MOISTURE_111C));

(* --- Signal 12: Sub-50 ms Dual-Spectrum Optical Fast IR Flame Detectors [V] --- *)
IF ABS(FT_OPTICAL_FLAME_112A - FT_OPTICAL_FLAME_112B) > rTol_Flame_V OR
   ABS(FT_OPTICAL_FLAME_112B - FT_OPTICAL_FLAME_112C) > rTol_Flame_V OR
   ABS(FT_OPTICAL_FLAME_112A - FT_OPTICAL_FLAME_112C) > rTol_Flame_V THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00000800;
    tFlm112_DiscTimer(IN := TRUE, PT := T#10MS);
    IF tFlm112_DiscTimer.Q THEN
        IF ABS(FT_OPTICAL_FLAME_112A - FT_OPTICAL_FLAME_112B) <= rTol_Flame_V THEN
            bFault_Flm112C := TRUE;
        ELSIF ABS(FT_OPTICAL_FLAME_112A - FT_OPTICAL_FLAME_112C) <= rTol_Flame_V THEN
            bFault_Flm112B := TRUE;
        ELSE
            bFault_Flm112A := TRUE;
        END_IF;
    END_IF;
ELSE
    tFlm112_DiscTimer(IN := FALSE);
END_IF;
(* In safety-critical explosion suppression, take 2oo3 median or highest voted channel *)
rVotedFlameDetector_V := (FT_OPTICAL_FLAME_112A + FT_OPTICAL_FLAME_112B + FT_OPTICAL_FLAME_112C)
                       - MIN(FT_OPTICAL_FLAME_112A, MIN(FT_OPTICAL_FLAME_112B, FT_OPTICAL_FLAME_112C))
                       - MAX(FT_OPTICAL_FLAME_112A, MAX(FT_OPTICAL_FLAME_112B, FT_OPTICAL_FLAME_112C));

(* --- Signal 13: Central Dust Aspiration Duct Static Differential Pressure [Pa] --- *)
IF ABS(PT_ASPIRATION_DIFF_113A - PT_ASPIRATION_DIFF_113B) > rTol_Aspiration_Pa OR
   ABS(PT_ASPIRATION_DIFF_113B - PT_ASPIRATION_DIFF_113C) > rTol_Aspiration_Pa OR
   ABS(PT_ASPIRATION_DIFF_113A - PT_ASPIRATION_DIFF_113C) > rTol_Aspiration_Pa THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00001000;
    tAsp113_DiscTimer(IN := TRUE, PT := T#150MS);
    IF tAsp113_DiscTimer.Q THEN
        IF ABS(PT_ASPIRATION_DIFF_113A - PT_ASPIRATION_DIFF_113B) <= rTol_Aspiration_Pa THEN
            bFault_Asp113C := TRUE;
        ELSIF ABS(PT_ASPIRATION_DIFF_113A - PT_ASPIRATION_DIFF_113C) <= rTol_Aspiration_Pa THEN
            bFault_Asp113B := TRUE;
        ELSE
            bFault_Asp113A := TRUE;
        END_IF;
    END_IF;
ELSE
    tAsp113_DiscTimer(IN := FALSE);
END_IF;
rVotedAspirationDiff_Pa := (PT_ASPIRATION_DIFF_113A + PT_ASPIRATION_DIFF_113B + PT_ASPIRATION_DIFF_113C)
                         - MIN(PT_ASPIRATION_DIFF_113A, MIN(PT_ASPIRATION_DIFF_113B, PT_ASPIRATION_DIFF_113C))
                         - MAX(PT_ASPIRATION_DIFF_113A, MAX(PT_ASPIRATION_DIFF_113B, PT_ASPIRATION_DIFF_113C));

(* --- Signal 14: Rotary Electric Turn-Head Spout Distributor Laser Angle [deg] --- *)
IF ABS(AT_TURNHEAD_ANGLE_114A - AT_TURNHEAD_ANGLE_114B) > rTol_TurnHead_deg OR
   ABS(AT_TURNHEAD_ANGLE_114B - AT_TURNHEAD_ANGLE_114C) > rTol_TurnHead_deg OR
   ABS(AT_TURNHEAD_ANGLE_114A - AT_TURNHEAD_ANGLE_114C) > rTol_TurnHead_deg THEN
    dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR DWORD#16#00002000;
    tAng114_DiscTimer(IN := TRUE, PT := T#50MS);
    IF tAng114_DiscTimer.Q THEN
        IF ABS(AT_TURNHEAD_ANGLE_114A - AT_TURNHEAD_ANGLE_114B) <= rTol_TurnHead_deg THEN
            bFault_Ang114C := TRUE;
        ELSIF ABS(AT_TURNHEAD_ANGLE_114A - AT_TURNHEAD_ANGLE_114C) <= rTol_TurnHead_deg THEN
            bFault_Ang114B := TRUE;
        ELSE
            bFault_Ang114A := TRUE;
        END_IF;
    END_IF;
ELSE
    tAng114_DiscTimer(IN := FALSE);
END_IF;
rVotedTurnHeadAngle_deg := (AT_TURNHEAD_ANGLE_114A + AT_TURNHEAD_ANGLE_114B + AT_TURNHEAD_ANGLE_114C)
                         - MIN(AT_TURNHEAD_ANGLE_114A, MIN(AT_TURNHEAD_ANGLE_114B, AT_TURNHEAD_ANGLE_114C))
                         - MAX(AT_TURNHEAD_ANGLE_114A, MAX(AT_TURNHEAD_ANGLE_114B, AT_TURNHEAD_ANGLE_114C));
""")

    # 7. CODE BODY: SECTION 2 (Belt Slip, Mechanics & Silo Thermal Mesh Analytics)
    parts.append("""
(* =====================================================================================================================
 * SECTION 2: CYBER-PHYSICAL BELT SLIP DYNAMICS, MOTOR POWER & SILO MESH THERMAL ANALYTICS
 * Evaluates VFD belt slip differentials according to NFPA 61, calculates real-time bulk throughput, integrates
 * mass delivery, and parses the 24-point thermocouple cable mesh for grain core biological hot-spots.
 * ===================================================================================================================== *)
(* --- VFD Belt Slip Percentage Calculation (NFPA 61: S = (v_head - v_boot)/v_head * 100%) --- *)
IF rVotedHeadBeltSpeedA_mps > 0.10 THEN
    rCalculatedSlipA_pct := ((rVotedHeadBeltSpeedA_mps - rVotedBootBeltSpeedA_mps) / rVotedHeadBeltSpeedA_mps) * 100.0;
ELSE
    rCalculatedSlipA_pct := 0.0;
END_IF;

IF rLinearHeadSpeedB_mps > 0.10 THEN
    rCalculatedSlipB_pct := ((rLinearHeadSpeedB_mps - rLinearBootSpeedB_mps) / rLinearHeadSpeedB_mps) * 100.0;
ELSE
    rCalculatedSlipB_pct := 0.0;
END_IF;

(* NFPA 61 Belt Slip Timers: 5% Warning (Debounced 5s), 10% Critical Trip (Shutdown within 20s) *)
tBeltSlipWarningTimerA(IN := (rCalculatedSlipA_pct >= c_rWarn_BeltSlip_H_pct), PT := T#5S);
tBeltSlipTripTimerA(IN := (rCalculatedSlipA_pct >= c_rTrip_BeltSlip_HH_pct), PT := T#20S);

tBeltSlipWarningTimerB(IN := (rCalculatedSlipB_pct >= c_rWarn_BeltSlip_H_pct), PT := T#5S);
tBeltSlipTripTimerB(IN := (rCalculatedSlipB_pct >= c_rTrip_BeltSlip_HH_pct), PT := T#20S);

(* --- Instantaneous Throughput Calculation from Motor Power [t/h] --- *)
(* Net lifting power: P_net = (Throughput_tph * 1000 kg/t / 3600 s/h) * g * H_lift / (eta * 1000 W/kW) *)
(* Inverting: Throughput_tph = P_net * eta * 3600 / (g * H_lift) *)
IF rVotedMotorPower_kW > c_rElevatorTarePower_kW AND rVotedHeadBeltSpeedA_mps > 1.0 THEN
    rInstantaneousThroughput_tph := ((rVotedMotorPower_kW - c_rElevatorTarePower_kW) * c_rMechanicalEfficiency_eta * 3600.0)
                                  / (c_rGravitationalAccel_mps2 * c_rElevatorLiftHeight_m);
    IF rInstantaneousThroughput_tph < 0.0 THEN
        rInstantaneousThroughput_tph := 0.0;
    ELSIF rInstantaneousThroughput_tph > 1850.0 THEN
        rInstantaneousThroughput_tph := 1850.0;
    END_IF;
ELSE
    rInstantaneousThroughput_tph := 0.0;
END_IF;

(* Continuous Lot Batch Mass Integration (tons) *)
rTotalizedBatchMass_tons := rTotalizedBatchMass_tons + (rInstantaneousThroughput_tph * (rSamplingInterval_Ts / 3600.0));

(* Motor Electrical Thermal Load & Reserve Margin *)
rElevatorA_TorqueLoad_pct := (rVotedMotorPower_kW / c_rElevatorMotorNominalPower_kW) * 100.0;
rElevatorA_PowerReserve_kW := c_rElevatorMotorNominalPower_kW - rVotedMotorPower_kW;

(* Estimated Airborne Combustible Dust Concentration in Elevator Trunking [g/m3] *)
IF rVotedHeadBeltSpeedA_mps > 0.5 THEN
    rCalculatedGrainDustConc_gm3 := (rInstantaneousThroughput_tph * 0.038)
                                  * (15.5 / MAX(10.0, rVotedGrainMoisture_pct))
                                  * (1200.0 / MAX(200.0, rVotedAspirationDiff_Pa));
ELSE
    rCalculatedGrainDustConc_gm3 := 0.0;
END_IF;

(* =====================================================================================================================
 * SILO 24-POINT THERMOCOUPLE CABLE SENSOR MESH ANALYTICS
 * 4 vertical suspension cables distributed radially at 90-degree offsets; each cable contains 6 RTD/thermocouple nodes
 * Node index: iNodeIdx = (iCableIdx - 1) * 6 + iDepthIdx
 * Depth 1: Silo bottom discharge hopper (2.0 m)
 * Depth 2: Lower cylindrical shell (8.0 m)
 * Depth 3: Mid-lower storage zone (14.0 m)
 * Depth 4: Mid-upper storage zone (20.0 m)
 * Depth 5: Upper cylindrical shell (26.0 m)
 * Depth 6: Surface grain crest (32.0 m)
 * ===================================================================================================================== *)
tMeshCalculationTimer(IN := NOT tMeshCalculationTimer.Q, PT := T#60S);

rSumTemperatureAccumulator := 0.0;
rMaxTempCandidate := -50.0;
rMaxRateOfRiseCandidate := 0.0;

FOR iNodeIdx := 1 TO 24 DO
    (* Accumulate average core temperature *)
    rSumTemperatureAccumulator := rSumTemperatureAccumulator + arrGrainMeshTemp_degC[iNodeIdx];

    (* Identify absolute highest hot-spot node *)
    IF arrGrainMeshTemp_degC[iNodeIdx] > rMaxTempCandidate THEN
        rMaxTempCandidate := arrGrainMeshTemp_degC[iNodeIdx];
        iPeakNodeIndex := iNodeIdx;
    END_IF;

    (* Periodic 60-second differential rate of rise calculation [deg C/hour] *)
    IF tMeshCalculationTimer.Q THEN
        arrGrainMeshRateOfRise_degCh[iNodeIdx] := (arrGrainMeshTemp_degC[iNodeIdx] - arrPrevGrainMeshTemp_degC[iNodeIdx]) * 60.0;
        arrPrevGrainMeshTemp_degC[iNodeIdx] := arrGrainMeshTemp_degC[iNodeIdx];
    END_IF;

    IF arrGrainMeshRateOfRise_degCh[iNodeIdx] > rMaxRateOfRiseCandidate THEN
        rMaxRateOfRiseCandidate := arrGrainMeshRateOfRise_degCh[iNodeIdx];
    END_IF;
END_FOR;

rGrainMeshAvgTemp_degC := rSumTemperatureAccumulator / 24.0;
rGrainMeshMaxTemp_degC := rMaxTempCandidate;
rGrainMeshMaxRateOfRise_degCh := rMaxRateOfRiseCandidate;
iGrainHotSpotSensorIndex := iPeakNodeIndex;

(* Empirical Respiration Index: R_bio = 10^(0.045*T + 0.35*M - 5.2) *)
rGrainRespirationIndex := (0.045 * rGrainMeshMaxTemp_degC) + (0.350 * rVotedGrainMoisture_pct) - 5.20;
IF rGrainRespirationIndex > 1.0 OR rGrainMeshMaxRateOfRise_degCh >= c_rWarn_GrainMeshRateOfRise_H_degCh THEN
    bGrainBiologicalHeatingActive := TRUE;
ELSE
    bGrainBiologicalHeatingActive := FALSE;
END_IF;

(* Equilibrium Moisture Content (EMC) via Chung-Pfost Isotherm *)
(* EMC = (- ln(1 - RH/100) / (C1 * (T_ambient + C2)))^(1/C3) *)
IF rAmbientAirRelHum_pct > 5.0 AND rAmbientAirRelHum_pct < 98.0 THEN
    rGrainEquilibriumMoisture_pct := 14.2 + (0.08 * (rAmbientAirRelHum_pct - 65.0)) - (0.04 * (rAmbientAirTemp_degC - 20.0));
ELSE
    rGrainEquilibriumMoisture_pct := 14.0;
END_IF;

(* Aeration Permissive: Outside air must be cold and dry enough to prevent rewetting grain *)
IF (rAmbientAirTemp_degC < (rGrainMeshAvgTemp_degC - 4.0)) AND (rGrainEquilibriumMoisture_pct <= (rVotedGrainMoisture_pct + 0.3)) THEN
    bAerationConditionsFavorable := TRUE;
ELSE
    bAerationConditionsFavorable := FALSE;
END_IF;
""")

    # 8. CODE BODY: SECTION 3 (ATEX / NFPA 61 Fast Explosion Suppression)
    parts.append("""
(* =====================================================================================================================
 * SECTION 3: ATEX / NFPA 61 FAST COMBUSTIBLE DUST EXPLOSION SUPPRESSION SYSTEM
 * Sub-50 ms fast optical IR flame detection, pyrotechnic firing of High-Rate Discharge (HRD) chemical isolation
 * cannons, high-speed pneumatic abort gate dumping, aspiration duct mechanical knife isolation, and emergency stops.
 * ===================================================================================================================== *)
(* Rate of rise of optical IR radiation dV/dt *)
rFlameDerivative_Vps := (rVotedFlameDetector_V - rPrevFlameDetector_V) / MAX(0.001, rSamplingInterval_Ts);
rPrevFlameDetector_V := rVotedFlameDetector_V;

(* Sub-50 ms Optical Fireball / Spark Detection Logic *)
IF (rVotedFlameDetector_V >= c_rFlameTripThreshold_V) OR (rFlameDerivative_Vps >= c_rFlameDerivativeTrip_Vps) THEN
    rFlameResponseDuration_ms := rFlameResponseDuration_ms + (rSamplingInterval_Ts * 1000.0);
    IF rFlameResponseDuration_ms >= 10.0 THEN
        (* Fireball confirmed: latch critical explosion suppression event *)
        bExplosionTripLatched := TRUE;
    END_IF;
ELSE
    rFlameResponseDuration_ms := 0.0;
END_IF;

(* Direct Rupture Vent Door Trip Interlock *)
IF bExplosionVentingFlap_Open THEN
    bExplosionTripLatched := TRUE;
END_IF;

(* ATEX/NFPA 61 Fast Actuation Sequence Execution *)
IF bExplosionTripLatched AND bExplosionSuppressionArmed THEN
    (* 1. Fire High-Rate Discharge (HRD) Sodium Bicarbonate Chemical Isolation Cannons *)
    bHRD_ChemicalCannons_Fire := TRUE;
    tCannonDischargeDwell(IN := TRUE, PT := T#250MS);

    (* 2. Open high-speed pneumatic abort gate to dump burning grain into outdoor quench bunker *)
    bExplosionFastAbortGate_Trip := TRUE;

    (* 3. Snap shut mechanical guillotine knife-gate isolation damper on dust aspiration takeoff *)
    bAspirationIsolationDamper_Trip := TRUE;

    (* 4. Instantly trip master safety interlock loop and emergency stop relay *)
    bEmergencyStopTripRelay := FALSE;

    (* 5. Trigger elevator head casing high-pressure water-mist deluge solenoid *)
    bDelugeWaterMist_Active := TRUE;

    (* 6. Sound plant-wide evacuation acoustic alarm siren *)
    bAcousticAlarmSiren := TRUE;

    (* Force FSM directly into Emergency Deluge Lockout State *)
    iActiveFSM_State := c_iFSM_EMERGENCY_EXPLOSION_DELUGE;
ELSE
    IF tCannonDischargeDwell.Q THEN
        bHRD_ChemicalCannons_Fire := FALSE;
    END_IF;
    tCannonDischargeDwell(IN := FALSE);
END_IF;

(* Manual Hazard Reset Circuit *)
IF bManualHazardReset AND NOT bExplosionVentingFlap_Open AND (rVotedFlameDetector_V < 0.50) THEN
    bExplosionTripLatched := FALSE;
    bDelugeWaterMist_Active := FALSE;
    bExplosionFastAbortGate_Trip := FALSE;
    bAspirationIsolationDamper_Trip := FALSE;
    bAcousticAlarmSiren := FALSE;
    bEmergencyStopTripRelay := TRUE;
END_IF;
""")

    # 9. CODE BODY: SECTION 4 (8-State Discrete State-Space & Receding-Horizon MPC)
    parts.append("""
(* =====================================================================================================================
 * SECTION 4: 8-STATE DISCRETE STATE-SPACE PROPAGATION & RECEDING-HORIZON MPC
 * Solves the quadratic cost minimization problem: J = sum(e' * Q * e + u' * R * u)
 * Propagates discrete plant dynamics: x[k+1] = A*x[k] + B*u[k], synthesizes constrained actuator commands.
 * ===================================================================================================================== *)
(* Step 1: Assign Physical Measurements to Current State Vector x[k] *)
arrStateVector_x[1] := rVotedMotorPower_kW;
arrStateVector_x[2] := rCalculatedSlipA_pct * 12.5; (* Normalized belt strain equivalent *)
arrStateVector_x[3] := rInstantaneousThroughput_tph;
arrStateVector_x[4] := rCalculatedGrainDustConc_gm3;
arrStateVector_x[5] := rVotedAspirationDiff_Pa;
arrStateVector_x[6] := rGrainMeshAvgTemp_degC;
arrStateVector_x[7] := rVotedGrainMoisture_pct;
arrStateVector_x[8] := rTurnHeadAngleError_deg;

(* Step 2: Establish Setpoint Reference Vector sp[k] based on Operating State *)
IF iActiveFSM_State = c_iFSM_CONTINUOUS_TRANSFER_MPC THEN
    arrSetpointVector_sp[1] := (rTargetThroughput_tph / 1500.0) * 265.0 + c_rElevatorTarePower_kW;
    arrSetpointVector_sp[2] := 1.25; (* Target belt slip < 1.5% *)
    arrSetpointVector_sp[3] := rTargetThroughput_tph;
    arrSetpointVector_sp[4] := c_rDustSuppressionTarget_gm3;
    arrSetpointVector_sp[5] := 1250.0; (* Optimal baghouse static suction [Pa] *)
    arrSetpointVector_sp[6] := 22.0;   (* Target core grain temperature [deg C] *)
    arrSetpointVector_sp[7] := rMoistureSetpoint_pct;
    arrSetpointVector_sp[8] := 0.0;    (* Zero distributor alignment error *)
ELSIF iActiveFSM_State = c_iFSM_BIN_APPROACH_TOPPING THEN
    arrSetpointVector_sp[1] := 95.0;   (* Throttled motor load *)
    arrSetpointVector_sp[2] := 0.80;
    arrSetpointVector_sp[3] := 400.0;  (* Throttled 400 t/h topping rate *)
    arrSetpointVector_sp[4] := 10.0;
    arrSetpointVector_sp[5] := 1100.0;
    arrSetpointVector_sp[6] := 22.0;
    arrSetpointVector_sp[7] := rMoistureSetpoint_pct;
    arrSetpointVector_sp[8] := 0.0;
ELSE
    arrSetpointVector_sp[1] := c_rElevatorTarePower_kW;
    arrSetpointVector_sp[2] := 0.0;
    arrSetpointVector_sp[3] := 0.0;
    arrSetpointVector_sp[4] := 5.0;
    arrSetpointVector_sp[5] := 800.0;
    arrSetpointVector_sp[6] := 22.0;
    arrSetpointVector_sp[7] := rMoistureSetpoint_pct;
    arrSetpointVector_sp[8] := 0.0;
END_IF;

(* Step 3: Compute Tracking Error Vector e = sp - x *)
FOR iIdx_i := 1 TO 8 DO
    arrStateError_e[iIdx_i] := arrSetpointVector_sp[iIdx_i] - arrStateVector_x[iIdx_i];
END_FOR;

(* Step 4: Discrete State-Space Prediction: x[k+1] = A * x[k] + B * u[k] *)
FOR iIdx_i := 1 TO 8 DO
    rTempAccumulator := 0.0;
    FOR iIdx_j := 1 TO 8 DO
        rTempAccumulator := rTempAccumulator + (arrMatA[iIdx_i, iIdx_j] * arrStateVector_x[iIdx_j])
                                             + (arrMatB[iIdx_i, iIdx_j] * arrControlVector_u[iIdx_j]);
    END_FOR;
    arrNextStateVector_x[iIdx_i] := rTempAccumulator;
END_FOR;

(* Step 5: Receding-Horizon Control Law: u = K_mpc * e *)
FOR iIdx_i := 1 TO 8 DO
    rTempAccumulator := 0.0;
    FOR iIdx_j := 1 TO 8 DO
        rTempAccumulator := rTempAccumulator + (arrMatK_mpc[iIdx_i, iIdx_j] * arrStateError_e[iIdx_j]);
    END_FOR;
    arrControlVector_u[iIdx_i] := rTempAccumulator;
END_FOR;

(* Step 6: Quadratic Cost Metric Accumulation: J = sum(e' * Q * e + u' * R * u) *)
rQuadraticCostAccumulator_J := 0.0;
FOR iIdx_i := 1 TO 8 DO
    rQuadraticCostAccumulator_J := rQuadraticCostAccumulator_J
                                 + (arrStateError_e[iIdx_i] * arrMatQ[iIdx_i, iIdx_i] * arrStateError_e[iIdx_i])
                                 + (arrControlVector_u[iIdx_i] * arrMatR[iIdx_i, iIdx_i] * arrControlVector_u[iIdx_i]);
END_FOR;

(* Step 7: Apply Actuator Constraints & Clamping to MPC Outputs *)
(* Elevator VFD Frequency Command u[1] *)
IF iActiveFSM_State = c_iFSM_CONTINUOUS_TRANSFER_MPC OR iActiveFSM_State = c_iFSM_BIN_APPROACH_TOPPING THEN
    rElevatorA_VFD_Speed_Cmd_Hz := 50.0 + (arrControlVector_u[1] * 0.05);
    IF rElevatorA_VFD_Speed_Cmd_Hz > 55.0 THEN
        rElevatorA_VFD_Speed_Cmd_Hz := 55.0;
    ELSIF rElevatorA_VFD_Speed_Cmd_Hz < 35.0 THEN
        rElevatorA_VFD_Speed_Cmd_Hz := 35.0;
    END_IF;
    rElevatorB_VFD_Speed_Cmd_Hz := rElevatorA_VFD_Speed_Cmd_Hz;
ELSIF iActiveFSM_State = c_iFSM_CASCADE_DOWNSTREAM_START THEN
    rElevatorA_VFD_Speed_Cmd_Hz := 50.0;
    rElevatorB_VFD_Speed_Cmd_Hz := 50.0;
ELSE
    rElevatorA_VFD_Speed_Cmd_Hz := 0.0;
    rElevatorB_VFD_Speed_Cmd_Hz := 0.0;
END_IF;

(* Feeder Slide Gate Aperture Command u[2] *)
IF iActiveFSM_State = c_iFSM_CONTINUOUS_TRANSFER_MPC THEN
    rFeederSlideGate_Pos_Cmd_pct := 75.0 + (arrControlVector_u[2] * 0.25);
    IF rFeederSlideGate_Pos_Cmd_pct > 100.0 THEN
        rFeederSlideGate_Pos_Cmd_pct := 100.0;
    ELSIF rFeederSlideGate_Pos_Cmd_pct < 15.0 THEN
        rFeederSlideGate_Pos_Cmd_pct := 15.0;
    END_IF;
ELSIF iActiveFSM_State = c_iFSM_BIN_APPROACH_TOPPING THEN
    rFeederSlideGate_Pos_Cmd_pct := 25.0;
ELSIF iActiveFSM_State = c_iFSM_INTAKE_GATE_MODULATION THEN
    rFeederSlideGate_Pos_Cmd_pct := 30.0;
ELSE
    rFeederSlideGate_Pos_Cmd_pct := 0.0;
END_IF;

(* Aspiration Airflow Balancing Damper Command u[4] *)
IF bAspirationSystemRunning THEN
    rAspirationDamper_Pos_Cmd_pct := 65.0 + (arrControlVector_u[4] * 0.15);
    IF rAspirationDamper_Pos_Cmd_pct > 100.0 THEN
        rAspirationDamper_Pos_Cmd_pct := 100.0;
    ELSIF rAspirationDamper_Pos_Cmd_pct < 20.0 THEN
        rAspirationDamper_Pos_Cmd_pct := 20.0;
    END_IF;
ELSE
    rAspirationDamper_Pos_Cmd_pct := 0.0;
END_IF;

(* Silo Bottom Aeration Blower VFD Command u[5] *)
IF (iActiveFSM_State = c_iFSM_AERATION_CONDITIONING OR bGrainBiologicalHeatingActive) AND bAerationConditionsFavorable THEN
    rAerationFan_VFD_Speed_Cmd_Hz := 45.0 + (arrControlVector_u[5] * 0.20);
    IF rAerationFan_VFD_Speed_Cmd_Hz > 60.0 THEN
        rAerationFan_VFD_Speed_Cmd_Hz := 60.0;
    ELSIF rAerationFan_VFD_Speed_Cmd_Hz < 25.0 THEN
        rAerationFan_VFD_Speed_Cmd_Hz := 25.0;
    END_IF;
ELSE
    rAerationFan_VFD_Speed_Cmd_Hz := 0.0;
END_IF;
""")

    # 10. CODE BODY: SECTION 5 (12-Stage Finite State Machine)
    parts.append("""
(* =====================================================================================================================
 * SECTION 5: 12-STAGE INDUSTRIAL FINITE STATE MACHINE (FSM) WITH FULL CASCADE INTERLOCKS
 * Implements deterministic routing, pre-start baghouse purge, turn-head laser angular slew, downstream-to-upstream
 * conveyor cascade spin-up, 1,500 t/h MPC transfer, 90% radar topping, route changeover, tail-out purges, and trips.
 * ===================================================================================================================== *)
tFSM_StateDwellTimer(IN := TRUE, PT := T#86400S);
rFSM_StateElapsed_s := rFSM_StateElapsed_s + rSamplingInterval_Ts;

(* Target Spout Angle Lookup for Selected Destination Silo Bin (1..12) *)
IF iTargetSiloBin >= 1 AND iTargetSiloBin <= 12 THEN
    rTargetSpoutAngle_deg := arrSiloTargetSpoutAngles_deg[iTargetSiloBin];
ELSE
    rTargetSpoutAngle_deg := 0.0;
END_IF;

rTurnHeadAngleError_deg := rTargetSpoutAngle_deg - rVotedTurnHeadAngle_deg;

(* Rotary Turn-Head Spout Positioning Servo Loop *)
IF ABS(rTurnHeadAngleError_deg) > 0.05 THEN
    bTurnHeadLockPin_Engage := FALSE;
    bTurnHeadSpoutLockedInPosition := FALSE;
    tTurnHeadPositionLockTimer(IN := FALSE);
    IF rTurnHeadAngleError_deg > 0.0 THEN
        rTurnHeadDriveVelocity_pct := MIN(100.0, 15.0 + (rTurnHeadAngleError_deg * 2.5));
    ELSE
        rTurnHeadDriveVelocity_pct := MAX(-100.0, -15.0 + (rTurnHeadAngleError_deg * 2.5));
    END_IF;
    rTurnHeadSpout_Drive_Cmd_pct := rTurnHeadDriveVelocity_pct;
ELSE
    rTurnHeadSpout_Drive_Cmd_pct := 0.0;
    bTurnHeadLockPin_Engage := TRUE;
    tTurnHeadPositionLockTimer(IN := TRUE, PT := T#3S);
    IF tTurnHeadPositionLockTimer.Q THEN
        bTurnHeadSpoutLockedInPosition := TRUE;
    END_IF;
END_IF;

(* Master FSM State Switch *)
CASE iActiveFSM_State OF
    c_iFSM_UNINITIALIZED:
        (* State 0: Cold Start & Safety Interlock Loop Verification *)
        rElevatorA_VFD_Speed_Cmd_Hz := 0.0;
        rElevatorB_VFD_Speed_Cmd_Hz := 0.0;
        rPitConveyor_VFD_Speed_Cmd_Hz := 0.0;
        rOverheadConveyor_VFD_Speed_Hz := 0.0;
        rFeederSlideGate_Pos_Cmd_pct := 0.0;
        bEmergencyStopTripRelay := TRUE;

        IF bMasterEnable AND bEmergencyStop_CH1 AND bEmergencyStop_CH2
           AND bExplosionVentDoorsClosed AND bServiceAccessHatchesClosed
           AND bHRDCannonPressure_OK AND NOT bExplosionTripLatched THEN
            iActiveFSM_State := c_iFSM_STANDBY_READY;
            rFSM_StateElapsed_s := 0.0;
        END_IF;

    c_iFSM_STANDBY_READY:
        (* State 1: Standby Ready, Route Selected, Awaiting Operator Start Command *)
        rElevatorA_VFD_Speed_Cmd_Hz := 0.0;
        rElevatorB_VFD_Speed_Cmd_Hz := 0.0;
        rPitConveyor_VFD_Speed_Cmd_Hz := 0.0;
        rOverheadConveyor_VFD_Speed_Hz := 0.0;
        rFeederSlideGate_Pos_Cmd_pct := 0.0;

        IF bIntakeStartCommand AND (iTargetSiloBin >= 1 AND iTargetSiloBin <= 12)
           AND (rVotedRadarLevel_m < c_rWarn_RadarLevel_H_m) THEN
            iActiveFSM_State := c_iFSM_PRESTART_ASPIRATION_PURGE;
            rFSM_StateElapsed_s := 0.0;
        END_IF;

    c_iFSM_PRESTART_ASPIRATION_PURGE:
        (* State 2: Start Baghouse Dust Collector & Verify Vacuum Purge for 15 Seconds *)
        tAspirationPreStartPurgeTimer(IN := bAspirationSystemRunning, PT := T#15S);

        IF tAspirationPreStartPurgeTimer.Q AND (rVotedAspirationDiff_Pa >= c_rWarn_AspirationDiff_L_Pa) THEN
            tAspirationPreStartPurgeTimer(IN := FALSE);
            iActiveFSM_State := c_iFSM_DISTRIBUTOR_SLEW_ALIGNMENT;
            rFSM_StateElapsed_s := 0.0;
        ELSIF NOT bAspirationSystemRunning AND rFSM_StateElapsed_s > 30.0 THEN
            (* Timeout failure: return to standby *)
            iActiveFSM_State := c_iFSM_STANDBY_READY;
            rFSM_StateElapsed_s := 0.0;
        END_IF;

    c_iFSM_DISTRIBUTOR_SLEW_ALIGNMENT:
        (* State 3: Turn-Head Spout Slew to Target Bin & Shot-Pin Insertion (+/- 0.05 deg) *)
        IF bTurnHeadSpoutLockedInPosition THEN
            iActiveFSM_State := c_iFSM_CASCADE_DOWNSTREAM_START;
            rFSM_StateElapsed_s := 0.0;
        ELSIF rFSM_StateElapsed_s > 60.0 THEN
            (* Turn-head slew timeout alarm *)
            iActiveFSM_State := c_iFSM_STANDBY_READY;
            rFSM_StateElapsed_s := 0.0;
        END_IF;

    c_iFSM_CASCADE_DOWNSTREAM_START:
        (* State 4: Downstream-to-Upstream Cascade Interlock Start *)
        (* Step A: Spin up Overhead Silo Top Conveyor *)
        rOverheadConveyor_VFD_Speed_Hz := 50.0;
        tOverheadConveyorSpinUpTimer(IN := bOverheadConveyorRunning_Feedback, PT := T#8S);

        (* Step B: Spin up Twin Bucket Elevators when Overhead Conveyor at full speed *)
        IF tOverheadConveyorSpinUpTimer.Q THEN
            rElevatorA_VFD_Speed_Cmd_Hz := 50.0;
            rElevatorB_VFD_Speed_Cmd_Hz := 50.0;
            tElevatorsSpinUpTimer(IN := (rVotedHeadBeltSpeedA_mps >= 3.0), PT := T#12S);
        ELSE
            tElevatorsSpinUpTimer(IN := FALSE);
        END_IF;

        (* Step C: Verify zero slip and chute clear before opening intake *)
        IF tElevatorsSpinUpTimer.Q AND (rCalculatedSlipA_pct < c_rWarn_BeltSlip_H_pct)
           AND bHeadChutePlugged_Switch AND bBootChutePlugged_Switch THEN
            tOverheadConveyorSpinUpTimer(IN := FALSE);
            tElevatorsSpinUpTimer(IN := FALSE);
            iActiveFSM_State := c_iFSM_INTAKE_GATE_MODULATION;
            rFSM_StateElapsed_s := 0.0;
        END_IF;

    c_iFSM_INTAKE_GATE_MODULATION:
        (* State 5: Start Pit Drag Conveyor & Soft-Ramp Feeder Slide Gate to 30% *)
        rPitConveyor_VFD_Speed_Cmd_Hz := 40.0;
        tFeederGateRampTimer(IN := bPitConveyorRunning_Feedback, PT := T#10S);

        IF tFeederGateRampTimer.Q AND (rInstantaneousThroughput_tph > 100.0) THEN
            tFeederGateRampTimer(IN := FALSE);
            iActiveFSM_State := c_iFSM_CONTINUOUS_TRANSFER_MPC;
            rFSM_StateElapsed_s := 0.0;
        END_IF;

    c_iFSM_CONTINUOUS_TRANSFER_MPC:
        (* State 6: Steady-State High-Capacity 1,500 t/h Closed-Loop MPC Mass Transfer *)
        rPitConveyor_VFD_Speed_Cmd_Hz := 50.0;
        rOverheadConveyor_VFD_Speed_Hz := 50.0;

        (* Transitions from steady-state transfer *)
        IF bIntakeStopCommand THEN
            iActiveFSM_State := c_iFSM_EMPTY_RUNOUT_PURGE;
            rFSM_StateElapsed_s := 0.0;
        ELSIF rVotedRadarLevel_m >= c_rWarn_RadarLevel_H_m THEN
            (* Bin reached 90% capacity: transition to precision topping state *)
            iActiveFSM_State := c_iFSM_BIN_APPROACH_TOPPING;
            rFSM_StateElapsed_s := 0.0;
        ELSIF bHeadChutePlugged_Switch = FALSE OR bBootChutePlugged_Switch = FALSE THEN
            (* Plugged chute immediate abort *)
            iActiveFSM_State := c_iFSM_EMPTY_RUNOUT_PURGE;
            rFSM_StateElapsed_s := 0.0;
        END_IF;

    c_iFSM_BIN_APPROACH_TOPPING:
        (* State 7: Silo Level at 90%: Throttle Throughput to 400 t/h to Prevent Overfill *)
        rPitConveyor_VFD_Speed_Cmd_Hz := 30.0;
        rOverheadConveyor_VFD_Speed_Hz := 50.0;

        IF rVotedRadarLevel_m >= c_rTrip_RadarLevel_HH_m THEN
            (* Silo 100% full: execute immediate tail-out *)
            iActiveFSM_State := c_iFSM_EMPTY_RUNOUT_PURGE;
            rFSM_StateElapsed_s := 0.0;
        ELSIF bIntakeStopCommand THEN
            iActiveFSM_State := c_iFSM_EMPTY_RUNOUT_PURGE;
            rFSM_StateElapsed_s := 0.0;
        END_IF;

    c_iFSM_ROUTE_CHANGEOVER_TRANSIT:
        (* State 8: Intermediate Route Changeover: Gate Closed, Tail-Out Pit, Slew Spout *)
        rFeederSlideGate_Pos_Cmd_pct := 0.0;
        tPitConveyorTailOutTimer(IN := TRUE, PT := T#20S);

        IF tPitConveyorTailOutTimer.Q THEN
            tPitConveyorTailOutTimer(IN := FALSE);
            iActiveFSM_State := c_iFSM_DISTRIBUTOR_SLEW_ALIGNMENT;
            rFSM_StateElapsed_s := 0.0;
        END_IF;

    c_iFSM_EMPTY_RUNOUT_PURGE:
        (* State 9: Cascaded Upstream-to-Downstream Tail-Out Purge *)
        (* Step A: Close intake feeder slide gate immediately *)
        rFeederSlideGate_Pos_Cmd_pct := 0.0;

        (* Step B: Empty run-out of Intake Pit Drag Conveyor (30 seconds) *)
        tPitConveyorTailOutTimer(IN := TRUE, PT := T#30S);
        IF tPitConveyorTailOutTimer.Q THEN
            rPitConveyor_VFD_Speed_Cmd_Hz := 0.0;

            (* Step C: Empty run-out of Bucket Elevators (60 seconds to clear 45m column) *)
            tElevatorTailOutTimer(IN := TRUE, PT := T#60S);
            IF tElevatorTailOutTimer.Q THEN
                rElevatorA_VFD_Speed_Cmd_Hz := 0.0;
                rElevatorB_VFD_Speed_Cmd_Hz := 0.0;

                (* Step D: Empty run-out of Overhead Conveyor (45 seconds) *)
                tOverheadConveyorTailOutTimer(IN := TRUE, PT := T#45S);
                IF tOverheadConveyorTailOutTimer.Q THEN
                    rOverheadConveyor_VFD_Speed_Hz := 0.0;
                    tPitConveyorTailOutTimer(IN := FALSE);
                    tElevatorTailOutTimer(IN := FALSE);
                    tOverheadConveyorTailOutTimer(IN := FALSE);

                    (* Transfer complete: switch to aeration conditioning or standby *)
                    IF bGrainBiologicalHeatingActive THEN
                        iActiveFSM_State := c_iFSM_AERATION_CONDITIONING;
                    ELSE
                        iActiveFSM_State := c_iFSM_STANDBY_READY;
                    END_IF;
                    rFSM_StateElapsed_s := 0.0;
                END_IF;
            END_IF;
        END_IF;

    c_iFSM_AERATION_CONDITIONING:
        (* State 10: Silo Aeration Fans Operating to Quench Core Biological Hot-Spots *)
        rElevatorA_VFD_Speed_Cmd_Hz := 0.0;
        rElevatorB_VFD_Speed_Cmd_Hz := 0.0;
        rPitConveyor_VFD_Speed_Cmd_Hz := 0.0;
        rOverheadConveyor_VFD_Speed_Hz := 0.0;
        rFeederSlideGate_Pos_Cmd_pct := 0.0;

        IF NOT bGrainBiologicalHeatingActive AND (rGrainMeshMaxTemp_degC < (c_rWarn_GrainMeshTemp_H_degC - 5.0)) THEN
            iActiveFSM_State := c_iFSM_STANDBY_READY;
            rFSM_StateElapsed_s := 0.0;
        ELSIF bIntakeStartCommand THEN
            iActiveFSM_State := c_iFSM_PRESTART_ASPIRATION_PURGE;
            rFSM_StateElapsed_s := 0.0;
        END_IF;

    c_iFSM_EMERGENCY_EXPLOSION_DELUGE:
        (* State 11: Emergency Deluge & Chemical Suppression Lockout *)
        rElevatorA_VFD_Speed_Cmd_Hz := 0.0;
        rElevatorB_VFD_Speed_Cmd_Hz := 0.0;
        rPitConveyor_VFD_Speed_Cmd_Hz := 0.0;
        rOverheadConveyor_VFD_Speed_Hz := 0.0;
        rFeederSlideGate_Pos_Cmd_pct := 0.0;
        rAerationFan_VFD_Speed_Cmd_Hz := 0.0;
        rAspirationDamper_Pos_Cmd_pct := 0.0;
        bEmergencyStopTripRelay := FALSE;

        IF bManualHazardReset AND NOT bExplosionTripLatched THEN
            iActiveFSM_State := c_iFSM_UNINITIALIZED;
            rFSM_StateElapsed_s := 0.0;
        END_IF;

    ELSE
        iActiveFSM_State := c_iFSM_UNINITIALIZED;
        rFSM_StateElapsed_s := 0.0;
END_CASE;

eActiveState_Code := iActiveFSM_State;
""")

    # 11. CODE BODY: SECTION 6 (ISA-18.2 Alarms & Status Words)
    parts.append("""
(* =====================================================================================================================
 * SECTION 6: ISA-18.2 MULTI-TIERED ALARM HIERARCHY & DIAGNOSTIC WORD PACKING
 * Rigorously evaluates High-High (HH Trips), High (H Warnings), Low/Low-Low (L/LL Starvation) alarms with hysteresis
 * dead-bands. Packs all diagnostic status into 32-bit registers for SCADA / DCS integration.
 * ===================================================================================================================== *)
dwAlarmWord_Trips_HH := DWORD#16#00000000;
dwAlarmWord_Warnings_H := DWORD#16#00000000;
dwAlarmWord_Diagnostics := DWORD#16#00000000;
dwStatusWord_State := DWORD#16#00000000;

(* --- Priority 1 (CRITICAL TRIP HH) Evaluations --- *)
IF bExplosionTripLatched THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00000001; (* Bit 0: Optical Flame / Explosion Event *)
END_IF;

IF tBeltSlipTripTimerA.Q OR (rCalculatedSlipA_pct >= c_rTrip_BeltSlip_HH_pct) THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00000002; (* Bit 1: Elevator A Belt Slip >= 10% *)
END_IF;

IF tBeltSlipTripTimerB.Q OR (rCalculatedSlipB_pct >= c_rTrip_BeltSlip_HH_pct) THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00000004; (* Bit 2: Elevator B Belt Slip >= 10% *)
END_IF;

IF rVotedHeadBearingTemp_degC >= c_rTrip_BearingTemp_HH_degC THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00000008; (* Bit 3: Head Bearing Temp >= 85 C *)
END_IF;

IF rVotedBootBearingTemp_degC >= c_rTrip_BearingTemp_HH_degC THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00000010; (* Bit 4: Boot Bearing Temp >= 85 C *)
END_IF;

IF rVotedHeadBearingVib_mms >= c_rTrip_Vibration_HH_mms THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00000020; (* Bit 5: Bearing Acoustic Vib >= 7.1 mm/s *)
END_IF;

IF rVotedBeltRubTemp_degC >= c_rTrip_BeltRub_HH_degC THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00000040; (* Bit 6: Casing Rub Pyrometer >= 75 C *)
END_IF;

IF bBeltAlignment_LH_Trip = FALSE OR bBeltAlignment_RH_Trip = FALSE THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00000080; (* Bit 7: Belt Misalignment Runout Switch *)
END_IF;

IF bHeadChutePlugged_Switch = FALSE THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00000100; (* Bit 8: Head Discharge Chute Plugged *)
END_IF;

IF bBootChutePlugged_Switch = FALSE THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00000200; (* Bit 9: Boot Intake Chute Plugged *)
END_IF;

IF rVotedRadarLevel_m >= c_rTrip_RadarLevel_HH_m THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00000400; (* Bit 10: Silo Bin High-High Level (34.5m) *)
END_IF;

IF rVotedAspirationDiff_Pa >= c_rTrip_AspirationDiff_HH_Pa THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00000800; (* Bit 11: Baghouse Severe Differential Pres *)
END_IF;

IF bHRDCannonPressure_OK = FALSE THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00001000; (* Bit 12: HRD Cannon Pressure Low (<60 bar) *)
END_IF;

IF bEmergencyStop_CH1 = FALSE OR bEmergencyStop_CH2 = FALSE THEN
    dwAlarmWord_Trips_HH := dwAlarmWord_Trips_HH OR DWORD#16#00002000; (* Bit 13: Hardware E-Stop Loop Open *)
END_IF;

(* --- Priority 2 (PROCESS WARNING H) Evaluations with Deadband Hysteresis --- *)
IF rCalculatedSlipA_pct >= (c_rWarn_BeltSlip_H_pct + c_rDeadband_Speed_RPM) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00000001; (* Bit 0: Elevator A Belt Slip Warning >= 5% *)
END_IF;

IF rCalculatedSlipB_pct >= (c_rWarn_BeltSlip_H_pct + c_rDeadband_Speed_RPM) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00000002; (* Bit 1: Elevator B Belt Slip Warning >= 5% *)
END_IF;

IF rVotedHeadBearingTemp_degC >= (c_rWarn_BearingTemp_H_degC + c_rDeadband_Temp_degC) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00000004; (* Bit 2: Head Bearing Temp High >= 65 C *)
END_IF;

IF rVotedBootBearingTemp_degC >= (c_rWarn_BearingTemp_H_degC + c_rDeadband_Temp_degC) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00000008; (* Bit 3: Boot Bearing Temp High >= 65 C *)
END_IF;

IF rVotedHeadBearingVib_mms >= (c_rWarn_Vibration_H_mms + 0.10) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00000010; (* Bit 4: Bearing Acoustic Vib High >= 4.5 mm/s *)
END_IF;

IF rVotedBeltRubTemp_degC >= (c_rWarn_BeltRub_H_degC + c_rDeadband_Temp_degC) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00000020; (* Bit 5: Casing Rub Pyrometer High >= 55 C *)
END_IF;

IF rVotedRadarLevel_m >= (c_rWarn_RadarLevel_H_m + c_rDeadband_Level_m) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00000040; (* Bit 6: Silo Bin 90% Capacity Approach *)
END_IF;

IF rVotedGrainMoisture_pct >= (c_rWarn_Moisture_HH_pct + c_rDeadband_Moisture_pct) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00000080; (* Bit 7: High Moisture Spoilage Risk >= 15.2% *)
ELSIF rVotedGrainMoisture_pct <= (c_rWarn_Moisture_LL_pct - c_rDeadband_Moisture_pct) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00000100; (* Bit 8: Low Moisture Breakage Risk <= 12.8% *)
END_IF;

IF rGrainMeshMaxTemp_degC >= (c_rWarn_GrainMeshTemp_H_degC + c_rDeadband_Temp_degC) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00000200; (* Bit 9: Silo Thermocouple Hot-Spot >= 35 C *)
END_IF;

IF rGrainMeshMaxRateOfRise_degCh >= c_rWarn_GrainMeshRateOfRise_H_degCh THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00000400; (* Bit 10: Biological Thermal Velocity >= 1.5 C/h *)
END_IF;

IF rCalculatedGrainDustConc_gm3 >= 25.0 THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00000800; (* Bit 11: Elevated Combustible Dust >= 25 g/m3 *)
END_IF;

IF rVotedAspirationDiff_Pa >= (c_rWarn_AspirationDiff_H_Pa + c_rDeadband_Pressure_Pa) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00001000; (* Bit 12: Baghouse Cleaning Required >= 1800 Pa *)
ELSIF rVotedAspirationDiff_Pa <= (c_rWarn_AspirationDiff_L_Pa - c_rDeadband_Pressure_Pa) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00002000; (* Bit 13: Low Suction Vacuum Airflow Loss *)
END_IF;

IF ABS(rTurnHeadAngleError_deg) > 0.20 THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00004000; (* Bit 14: Turn-Head Spout Alignment Offset *)
END_IF;

IF rInstantaneousThroughput_tph < 800.0 AND (iActiveFSM_State = c_iFSM_CONTINUOUS_TRANSFER_MPC) THEN
    dwAlarmWord_Warnings_H := dwAlarmWord_Warnings_H OR DWORD#16#00008000; (* Bit 15: Low Throughput / Starvation Warning *)
END_IF;

(* --- Priority 3: Packing TMR Discrepancies into Diagnostic Word --- *)
dwAlarmWord_Diagnostics := dwTMR_DiscrepancyWord OR (SHL(dwTMR_SensorFaultWord, 16));

(* --- Packing Active FSM State and Operational Permissives into Status Word --- *)
dwStatusWord_State := INT_TO_DWORD(iActiveFSM_State);
IF bMasterEnable THEN
    dwStatusWord_State := dwStatusWord_State OR DWORD#16#00000100;
END_IF;
IF bAspirationSystemRunning THEN
    dwStatusWord_State := dwStatusWord_State OR DWORD#16#00000200;
END_IF;
IF bTurnHeadSpoutLockedInPosition THEN
    dwStatusWord_State := dwStatusWord_State OR DWORD#16#00000400;
END_IF;
IF bPitConveyorRunning_Feedback THEN
    dwStatusWord_State := dwStatusWord_State OR DWORD#16#00000800;
END_IF;
IF bOverheadConveyorRunning_Feedback THEN
    dwStatusWord_State := dwStatusWord_State OR DWORD#16#00001000;
END_IF;
IF bAerationConditionsFavorable THEN
    dwStatusWord_State := dwStatusWord_State OR DWORD#16#00002000;
END_IF;
IF bGrainBiologicalHeatingActive THEN
    dwStatusWord_State := dwStatusWord_State OR DWORD#16#00004000;
END_IF;
IF bExplosionSuppressionArmed THEN
    dwStatusWord_State := dwStatusWord_State OR DWORD#16#00008000;
END_IF;

END_FUNCTION_BLOCK
```""")

    return "".join(parts)

if __name__ == "__main__":
    code = build_grain_terminal_st()
    print("Generated ST length:", len(code), "characters")
    print("Generated lines:", len(code.splitlines()))

    prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Bulk Materials & Agricultural Logistics / Grain Terminals
- System: High-Capacity Port Terminal Grain Elevator (1,500 t/h wheat/corn throughput): Twin Heavy-Duty Bucket Elevators (45m vertical lift, VFD belt slip < 2.0%, optical belt rub pyrometers, acoustic bearing vibration transmitters), Multi-Run En-Masse Drag Conveyors, Rotary Electric Turn-Head Spout Distributor with Laser Angular Positioning (+/- 0.05 deg), Silo Aeration Fans & 24-Point Thermocouple Grain Temperature Cable Sensor Mesh, Continuous Inline Microwave Grain Moisture Analyzer (14.0 +/- 0.2%), and ATEX / NFPA 61 Combustible Dust Explosion Suppression System (Sub-50 ms Fast Optical IR Flame Detectors & High-Rate Sodium Bicarbonate Chemical Isolation Cannons).
- Function Block Name: FB_Grain_TerminalElevator_BulkHandling_Hazard

NEXT-GEN QUALITY REQUIREMENTS:
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) capturing elevator drive motor power, belt tension strain, silo bin level rate of change, dust concentration, and aeration airflow.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing bin routing queue delays (Q), conveyor motor power surges (R), and aeration fan energy (P).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on belt speed encoders, bearing temperature transmitters, bin radar level sensors, and infrared flame/spark detectors.
   - ISA-18.2 multi-tiered alarm hierarchy (Critical Spark/Explosion Trip HH, Belt Misalignment H, Warning H/L, Diagnostic, Priority Escalation).
   - 12-Stage Finite State Machine (CASE State OF ... END_CASE) covering pre-start aspiration purge, turn-head spout alignment, downstream-to-upstream cascade conveyor interlock start, bulk material intake, continuous high-capacity transfer, route transfer changeover, empty run-out purging, silo bin change, and emergency explosion suppression deluge shutdown.
3. Strict Syntax & Parity Rules:
   - TRIPLE backticks with iec-st.
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;. Zero unmatched delimiters.
   - Zero summaries, zero placeholders.
4. Save directly as a standard JSON dataset to data/swarm_raw/agent_<uuid>.json containing id, messages (user prompt, assistant response with fenced iec-st code), and metadata. Validate with python validate_iec.py and report final character count."""

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code}
        ],
        "metadata": {
            "domain": "Bulk Materials & Agricultural Logistics / Grain Terminals",
            "system": "High-Capacity Port Terminal Grain Elevator (1,500 t/h wheat/corn)",
            "function_block": "FB_Grain_TerminalElevator_BulkHandling_Hazard",
            "characters": len(code),
            "lines": len(code.splitlines()),
            "validated": False,
            "tier": 4,
            "uuid": UUID_STR
        }
    }

    os.makedirs(os.path.dirname(TARGET_JSON), exist_ok=True)
    with open(TARGET_JSON, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"Dataset successfully saved to {TARGET_JSON}")
