# euv_builder/euv_vars.py

def get_var_input():
    return """VAR_INPUT
    (* ===================================================================================== *)
    (* 1. SYSTEM MASTER DIGITAL PERMISSIVES & SEMI S2 SAFETY INTERLOCKS                      *)
    (* ===================================================================================== *)
    bMasterEnable                   : BOOL;     (* Master supervisory EUV source production enable *)
    bEmergencyStop                  : BOOL;     (* SEMI S2 / SIL-3 hardwired safety relay trip circuit [active-low] *)
    bResetFaults                    : BOOL;     (* Master alarm unlatch and trip reset request *)
    bVesselSealsLocked              : BOOL;     (* Main vacuum vessel door seal clamp interlocks locked *)
    bRoughingVacuumOk               : BOOL;     (* Multi-stage dry roots roughing vacuum system online *)
    bTurbopumpsOnline               : BOOL;     (* 5x Maglev turbomolecular pumps at 100% rated speed *)
    bCoolingWaterFlowOk             : BOOL;     (* Primary closed-loop deionized cooling water flow normal *)
    bMagnetCryoPermissive           : BOOL;     (* Superconducting magnet liquid helium / cryocooler at 4.2 K *)
    bCO2LaserMOPAReady              : BOOL;     (* 40 kW CO2 MOPA drive laser master oscillator & amps online *)
    bPrePulseLaserReady             : BOOL;     (* Pulsed pre-pulse laser power supply charged and armed *)
    bManualOverride                 : BOOL;     (* Engineering manual actuator override permissive *)

    (* ===================================================================================== *)
    (* 2. TRIPLE MODULAR REDUNDANT (2oo3) DROPLET SHADOWGRAPH CAMERAS X-AXIS [um]            *)
    (* ===================================================================================== *)
    rDropletX_um_Ch1                : REAL;     (* In-line shadowgraph camera X-position channel 1 [um] *)
    rDropletX_um_Ch2                : REAL;     (* In-line shadowgraph camera X-position channel 2 [um] *)
    rDropletX_um_Ch3                : REAL;     (* In-line shadowgraph camera X-position channel 3 [um] *)

    (* ===================================================================================== *)
    (* 3. TRIPLE MODULAR REDUNDANT (2oo3) DROPLET SHADOWGRAPH CAMERAS Y-AXIS [um]            *)
    (* ===================================================================================== *)
    rDropletY_um_Ch1                : REAL;     (* In-line shadowgraph camera Y-position channel 1 [um] *)
    rDropletY_um_Ch2                : REAL;     (* In-line shadowgraph camera Y-position channel 2 [um] *)
    rDropletY_um_Ch3                : REAL;     (* In-line shadowgraph camera Y-position channel 3 [um] *)

    (* ===================================================================================== *)
    (* 4. TRIPLE MODULAR REDUNDANT (2oo3) DROPLET DOPPLER VELOCIMETERS [m/s]                 *)
    (* ===================================================================================== *)
    rDropletVel_mps_Ch1             : REAL;     (* Laser Doppler droplet flight velocity channel 1 [m/s] *)
    rDropletVel_mps_Ch2             : REAL;     (* Laser Doppler droplet flight velocity channel 2 [m/s] *)
    rDropletVel_mps_Ch3             : REAL;     (* Laser Doppler droplet flight velocity channel 3 [m/s] *)

    (* ===================================================================================== *)
    (* 5. TRIPLE MODULAR REDUNDANT (2oo3) DROPLET DIAMETER EXTINCTION SENSORS [um]           *)
    (* ===================================================================================== *)
    rDropletDiam_um_Ch1             : REAL;     (* Optical extinction droplet diameter channel 1 [um] *)
    rDropletDiam_um_Ch2             : REAL;     (* Optical extinction droplet diameter channel 2 [um] *)
    rDropletDiam_um_Ch3             : REAL;     (* Optical extinction droplet diameter channel 3 [um] *)

    (* ===================================================================================== *)
    (* 6. TRIPLE MODULAR REDUNDANT (2oo3) VESSEL VACUUM CAPACITANCE MANOMETERS [Pa]          *)
    (* ===================================================================================== *)
    rVesselPressure_Pa_Ch1          : REAL;     (* Capacitance manometer vacuum pressure channel 1 [Pa] *)
    rVesselPressure_Pa_Ch2          : REAL;     (* Capacitance manometer vacuum pressure channel 2 [Pa] *)
    rVesselPressure_Pa_Ch3          : REAL;     (* Capacitance manometer vacuum pressure channel 3 [Pa] *)

    (* ===================================================================================== *)
    (* 7. TRIPLE MODULAR REDUNDANT (2oo3) COLLECTOR MIRROR CENTER PYROMETERS [deg C]         *)
    (* ===================================================================================== *)
    rMirrorCenterTemp_DegC_Ch1      : REAL;     (* Multi-wavelength optical pyrometer Center channel 1 [deg C] *)
    rMirrorCenterTemp_DegC_Ch2      : REAL;     (* Multi-wavelength optical pyrometer Center channel 2 [deg C] *)
    rMirrorCenterTemp_DegC_Ch3      : REAL;     (* Multi-wavelength optical pyrometer Center channel 3 [deg C] *)

    (* ===================================================================================== *)
    (* 8. TRIPLE MODULAR REDUNDANT (2oo3) COLLECTOR MIRROR MID-ZONE THERMOCOUPLES [deg C]   *)
    (* ===================================================================================== *)
    rMirrorMidTemp_DegC_Ch1         : REAL;     (* Embedded thin-film RTD mid-radius zone channel 1 [deg C] *)
    rMirrorMidTemp_DegC_Ch2         : REAL;     (* Embedded thin-film RTD mid-radius zone channel 2 [deg C] *)
    rMirrorMidTemp_DegC_Ch3         : REAL;     (* Embedded thin-film RTD mid-radius zone channel 3 [deg C] *)

    (* ===================================================================================== *)
    (* 9. TRIPLE MODULAR REDUNDANT (2oo3) INTERMEDIATE FOCUS (IF) EUV POWER SENSORS [W]      *)
    (* ===================================================================================== *)
    rIFEUVPower_W_Ch1               : REAL;     (* Calibrated Zr-filtered EUV photodiode channel 1 [W] *)
    rIFEUVPower_W_Ch2               : REAL;     (* Calibrated Zr-filtered EUV photodiode channel 2 [W] *)
    rIFEUVPower_W_Ch3               : REAL;     (* Calibrated Zr-filtered EUV photodiode channel 3 [W] *)

    (* ===================================================================================== *)
    (* 10. AUXILIARY SUBSYSTEM PROCESS SENSORS                                               *)
    (* ===================================================================================== *)
    rTinReservoirTemp_DegC          : REAL;     (* Molten tin reservoir core heater temperature [deg C] *)
    rTinReservoirPress_bar          : REAL;     (* Argon backing pressure on liquid tin reservoir [bar] *)
    rH2SupplyPressure_bar           : REAL;     (* Ultra-pure H2 gas supply header pressure [bar] *)
    rH2MassFlowReadback_slpm        : REAL;     (* Thermal mass flow controller readback flow [slpm] *)
    rMagnetCurrent_A                : REAL;     (* Superconducting magnet coil power supply current [A] *)
    rMagnetField_Tesla              : REAL;     (* Hall effect magnetic flux density at plasma point [Tesla] *)
    rStannaneRGA_PartialPress_Pa    : REAL;     (* Quadrupole RGA m/z=124 SnH4 partial pressure [Pa] *)
    rHydrogenGasDetector_LEL        : REAL;     (* Enclosure safety sensor hydrogen concentration [%] *)
    rCollectorCoolingWaterTemp_DegC : REAL;     (* Closed-loop deionized cooling water inlet temperature [deg C] *)
    rPrePulseEnergyMonitor_mJ       : REAL;     (* Pre-pulse pick-off pyroelectric energy detector [mJ] *)
    rMainPulseEnergyMonitor_J       : REAL;     (* Main-pulse CO2 laser pick-off energy calorimeter [J] *)
    rBeamGalvoOffsetX_urad          : REAL;     (* Piezo fast steering mirror X-axis capacitive sensor [urad] *)
    rBeamGalvoOffsetY_urad          : REAL;     (* Piezo fast steering mirror Y-axis capacitive sensor [urad] *)
END_VAR
"""

def get_var_output():
    return """VAR_OUTPUT
    (* ===================================================================================== *)
    (* 1. SYSTEM MASTER STATUS & SUPERVISORY TELEMETRY                                       *)
    (* ===================================================================================== *)
    bSystemReady                    : BOOL;     (* Master ready permissive for EUV exposure production *)
    bSystemRunning                  : BOOL;     (* Operational state active and executing *)
    bEUVLightEmitting               : BOOL;     (* In-band 13.5 nm EUV emission confirmed at intermediate focus *)
    bPlasmaIgnited                  : BOOL;     (* High-temperature tin plasma ionization confirmed *)
    bDropletStreamLocked            : BOOL;     (* Molten tin droplet train stable and locked to laser PlaP *)
    bTMRDegradedMode                : BOOL;     (* At least one 2oo3 sensor triplet operating in degraded 1oo2 *)
    bCriticalTripActive             : BOOL;     (* SIL-3 / SEMI S2 safety interlock tripped *)

    (* ===================================================================================== *)
    (* 2. VOTED PHYSICAL PROCESS MEASUREMENTS                                                *)
    (* ===================================================================================== *)
    rMeasuredEUVPower_IF_W          : REAL;     (* Voted in-band 13.5 nm EUV power at intermediate focus [W] *)
    rCollectorCenterTemp_DegC       : REAL;     (* Voted collector mirror center zone temperature [deg C] *)
    rCollectorMidTemp_DegC          : REAL;     (* Voted collector mirror mid-radius zone temperature [deg C] *)
    rVesselVacuum_Pa                : REAL;     (* Voted vessel chamber H2 buffer gas pressure [Pa] *)
    rDropletFrequency_kHz           : REAL;     (* Measured droplet train repetition frequency [kHz] *)
    rDropletVelocity_mps            : REAL;     (* Voted droplet flight velocity [m/s] *)
    rDropletDiameter_um             : REAL;     (* Voted spherical droplet diameter [um] *)
    rDropletPosJitter_um            : REAL;     (* Root-mean-square lateral droplet position jitter [um] *)
    rPancakeDiameter_um             : REAL;     (* Calculated pre-pulse pancake expansion disc diameter [um] *)
    rConversionEfficiency_Pct       : REAL;     (* EUV in-band energy / total laser pulse energy [%] *)
    rStannaneEtchRate_nms           : REAL;     (* Collector mirror tin debris chemical etch removal rate [nm/s] *)

    (* ===================================================================================== *)
    (* 3. REAL-TIME ACTUATOR COMMANDS & CLOSED-LOOP SETPOINTS                                *)
    (* ===================================================================================== *)
    rPiezoFrequencyCmd_kHz          : REAL;     (* Commanded piezo droplet acoustic drive frequency [kHz] *)
    rPiezoVoltageCmd_V              : REAL;     (* Commanded piezo droplet acoustic drive amplitude [V] *)
    rTinPressureCmd_bar             : REAL;     (* Commanded Argon backing pressure on tin reservoir [bar] *)
    rPrePulseEnergyCmd_mJ           : REAL;     (* Commanded pre-pulse laser pulse energy [mJ] *)
    rMainPulseEnergyCmd_J           : REAL;     (* Commanded main-pulse CO2 laser pulse energy [J] *)
    rInterPulseDelayCmd_us          : REAL;     (* Commanded delay between pre-pulse and main-pulse [us] *)
    rGalvoSteerX_urad               : REAL;     (* Commanded fast piezo steering mirror X-deflection [urad] *)
    rGalvoSteerY_urad               : REAL;     (* Commanded fast piezo steering mirror Y-deflection [urad] *)
    rH2MassFlowCmd_slpm             : REAL;     (* Commanded molecular hydrogen buffer gas flow setpoint [slpm] *)
    rMagnetFieldCmd_Tesla           : REAL;     (* Commanded superconducting magnet field setpoint [Tesla] *)
    rMirrorCoolingValveCmd_Pct      : REAL;     (* Commanded collector cooling water proportional valve [%] *)

    (* ===================================================================================== *)
    (* 4. 12-STAGE OPERATIONAL STATE & BIT-PACKED TELEMETRY DWORDS                           *)
    (* ===================================================================================== *)
    iOperatingState                 : INT;      (* Current 12-stage operational state (0 to 120) *)
    dwAlarmWord_1                   : DWORD;    (* SEMI S2 SIL-3 critical plant shutdown alarms *)
    dwAlarmWord_2                   : DWORD;    (* Process parameter high-high / low-low trips *)
    dwWarningWord_1                 : DWORD;    (* Degraded 2oo3 sensor channels & fault warnings *)
    dwWarningWord_2                 : DWORD;    (* High / low process boundary pre-alarms *)
    dwDiagnosticStatus              : DWORD;    (* Internal subsystem states and ready flags *)
END_VAR
"""

def get_var():
    return """VAR
    (* ===================================================================================== *)
    (* 1. PHYSICAL CONSTANTS & EUV CYBER-PHYSICAL MODEL PARAMETERS                           *)
    (* ===================================================================================== *)
    rConst_Pi                       : REAL := 3.1415926535;
    rConst_Planck_Js                : REAL := 6.62607015E-34;  (* Planck constant [J*s] *)
    rConst_SpeedOfLight_mps         : REAL := 2.99792458E8;    (* Speed of light in vacuum [m/s] *)
    rConst_ElectronCharge_C         : REAL := 1.602176634E-19; (* Elementary electron charge [C] *)
    rConst_ElectronMass_kg          : REAL := 9.1093837E-31;   (* Electron rest mass [kg] *)
    rConst_TinDensity_kgm3          : REAL := 6980.0;          (* Molten tin density at 260 deg C [kg/m3] *)
    rConst_TinSurfaceTension_Nm     : REAL := 0.544;           (* Molten tin surface tension [N/m] *)
    rConst_TinViscosity_Pas         : REAL := 1.85E-3;         (* Dynamic viscosity [Pa*s] *)
    rConst_TinMeltingPoint_DegC     : REAL := 231.9;           (* Pure tin melting point [deg C] *)
    rConst_TinLatentHeatVap_Jkg     : REAL := 2.45E6;          (* Tin latent heat of vaporization [J/kg] *)
    rConst_MoSiBilayerPeriod_nm     : REAL := 6.90;            (* Mo/Si bilayer period d [nm] *)
    rConst_MoSiBilayerRatio         : REAL := 0.40;            (* Mo thickness fraction Gamma *)
    rConst_CriticalDensityCO2_cm3   : REAL := 1.0E19;          (* Critical plasma electron density [cm^-3] *)
    rConst_NominalRepRate_Hz        : REAL := 50000.0;         (* Nominal pulse rep rate 50 kHz [Hz] *)
    rConst_NominalIFPower_W         : REAL := 500.0;           (* Target in-band EUV power at IF [W] *)
    rConst_NominalCollectorTemp_DegC: REAL := 60.0;            (* Target collector mirror temperature [deg C] *)

    (* Cycle timing and sample rate *)
    rCycleTime_sec                  : REAL := 0.010;           (* Master task execution cycle period [s] *)
    bFirstScan                      : BOOL := TRUE;            (* Power-up initialization latch flag *)

    (* ===================================================================================== *)
    (* 2. TRIPLE MODULAR REDUNDANCY (2oo3) VOTING INTERNAL STRUCTURES & CHANNELS             *)
    (* ===================================================================================== *)
    (* Droplet X-Position Voting Channels *)
    rVotedDropletX_um               : REAL := 0.0;
    bDropletX_Dev_1_2               : BOOL := FALSE;
    bDropletX_Dev_2_3               : BOOL := FALSE;
    bDropletX_Dev_1_3               : BOOL := FALSE;
    bDropletX_Ch1_Fault             : BOOL := FALSE;
    bDropletX_Ch2_Fault             : BOOL := FALSE;
    bDropletX_Ch3_Fault             : BOOL := FALSE;
    bDropletX_Degraded_1oo2         : BOOL := FALSE;

    (* Droplet Y-Position Voting Channels *)
    rVotedDropletY_um               : REAL := 0.0;
    bDropletY_Dev_1_2               : BOOL := FALSE;
    bDropletY_Dev_2_3               : BOOL := FALSE;
    bDropletY_Dev_1_3               : BOOL := FALSE;
    bDropletY_Ch1_Fault             : BOOL := FALSE;
    bDropletY_Ch2_Fault             : BOOL := FALSE;
    bDropletY_Ch3_Fault             : BOOL := FALSE;
    bDropletY_Degraded_1oo2         : BOOL := FALSE;

    (* Droplet Velocity Voting Channels *)
    rVotedDropletVel_mps            : REAL := 75.0;
    bDropletVel_Dev_1_2             : BOOL := FALSE;
    bDropletVel_Dev_2_3             : BOOL := FALSE;
    bDropletVel_Dev_1_3             : BOOL := FALSE;
    bDropletVel_Ch1_Fault           : BOOL := FALSE;
    bDropletVel_Ch2_Fault           : BOOL := FALSE;
    bDropletVel_Ch3_Fault           : BOOL := FALSE;
    bDropletVel_Degraded_1oo2       : BOOL := FALSE;

    (* Droplet Diameter Voting Channels *)
    rVotedDropletDiam_um            : REAL := 24.0;
    bDropletDiam_Dev_1_2            : BOOL := FALSE;
    bDropletDiam_Dev_2_3            : BOOL := FALSE;
    bDropletDiam_Dev_1_3            : BOOL := FALSE;
    bDropletDiam_Ch1_Fault          : BOOL := FALSE;
    bDropletDiam_Ch2_Fault          : BOOL := FALSE;
    bDropletDiam_Ch3_Fault          : BOOL := FALSE;
    bDropletDiam_Degraded_1oo2      : BOOL := FALSE;

    (* Vessel Vacuum Pressure Voting Channels *)
    rVotedVesselPressure_Pa         : REAL := 3.5;
    bVesselPress_Dev_1_2            : BOOL := FALSE;
    bVesselPress_Dev_2_3            : BOOL := FALSE;
    bVesselPress_Dev_1_3            : BOOL := FALSE;
    bVesselPress_Ch1_Fault          : BOOL := FALSE;
    bVesselPress_Ch2_Fault          : BOOL := FALSE;
    bVesselPress_Ch3_Fault          : BOOL := FALSE;
    bVesselPress_Degraded_1oo2      : BOOL := FALSE;

    (* Collector Mirror Center Temperature Voting Channels *)
    rVotedMirrorCenterTemp_DegC     : REAL := 60.0;
    bMirrorCenterTemp_Dev_1_2       : BOOL := FALSE;
    bMirrorCenterTemp_Dev_2_3       : BOOL := FALSE;
    bMirrorCenterTemp_Dev_1_3       : BOOL := FALSE;
    bMirrorCenterTemp_Ch1_Fault     : BOOL := FALSE;
    bMirrorCenterTemp_Ch2_Fault     : BOOL := FALSE;
    bMirrorCenterTemp_Ch3_Fault     : BOOL := FALSE;
    bMirrorCenterTemp_Degraded_1oo2 : BOOL := FALSE;

    (* Collector Mirror Mid-Zone Temperature Voting Channels *)
    rVotedMirrorMidTemp_DegC        : REAL := 58.5;
    bMirrorMidTemp_Dev_1_2          : BOOL := FALSE;
    bMirrorMidTemp_Dev_2_3          : BOOL := FALSE;
    bMirrorMidTemp_Dev_1_3          : BOOL := FALSE;
    bMirrorMidTemp_Ch1_Fault        : BOOL := FALSE;
    bMirrorMidTemp_Ch2_Fault        : BOOL := FALSE;
    bMirrorMidTemp_Ch3_Fault        : BOOL := FALSE;
    bMirrorMidTemp_Degraded_1oo2    : BOOL := FALSE;

    (* Intermediate Focus (IF) EUV Power Voting Channels *)
    rVotedIFEUVPower_W              : REAL := 0.0;
    bIFEUVPower_Dev_1_2             : BOOL := FALSE;
    bIFEUVPower_Dev_2_3             : BOOL := FALSE;
    bIFEUVPower_Dev_1_3             : BOOL := FALSE;
    bIFEUVPower_Ch1_Fault           : BOOL := FALSE;
    bIFEUVPower_Ch2_Fault           : BOOL := FALSE;
    bIFEUVPower_Ch3_Fault           : BOOL := FALSE;
    bIFEUVPower_Degraded_1oo2       : BOOL := FALSE;

    (* 2oo3 Discrepancy Debounce Timers *)
    tDevTimer_DropletX              : TON;
    tDevTimer_DropletY              : TON;
    tDevTimer_DropletVel            : TON;
    tDevTimer_DropletDiam           : TON;
    tDevTimer_VesselPress           : TON;
    tDevTimer_MirrorCenter          : TON;
    tDevTimer_MirrorMid             : TON;
    tDevTimer_IFEUVPower            : TON;

    (* Master Degraded Mode Indicator *)
    bAnySensorDegraded              : BOOL := FALSE;

    (* ===================================================================================== *)
    (* 3. 16-STATE MULTIVARIABLE STATE-SPACE DISCRETE MODEL MATRICES                         *)
    (* States: x1: PosX_um, x2: PosY_um, x3: PosZ_um, x4: Vel_mps, x5: Diam_um,              *)
    (*         x6: PancakeDiam_um, x7: Te_eV, x8: ne_1e19cm3, x9: EUV_Plasma_W,             *)
    (*         x10: EUV_IF_W, x11: T_Center_DegC, x12: T_Mid_DegC, x13: T_Outer_DegC,       *)
    (*         x14: P_Vessel_Pa, x15: Sn_IonFlux, x16: SnH4_Rate                            *)
    (* Inputs: u1: PiezoFreq_kHz, u2: PiezoVolt_V, u3: ResPress_bar, u4: PrePulse_mJ,         *)
    (*         u5: MainPulse_J, u6: SteerX_urad, u7: SteerY_urad, u8: H2_Flow_slpm          *)
    (* ===================================================================================== *)
    aMatrix_A                       : ARRAY[1..16, 1..16] OF REAL;
    aMatrix_B                       : ARRAY[1..16, 1..8] OF REAL;
    aMatrix_C                       : ARRAY[1..16, 1..16] OF REAL;
    aMatrix_D                       : ARRAY[1..16, 1..8] OF REAL;

    (* State and Input Trajectory Vectors *)
    aState_x                        : ARRAY[1..16] OF REAL;
    aState_x_next                   : ARRAY[1..16] OF REAL;
    aState_y                        : ARRAY[1..16] OF REAL;
    aControl_u                      : ARRAY[1..8] OF REAL;
    aControl_u_prev                 : ARRAY[1..8] OF REAL;
    aSetpoint_ref                   : ARRAY[1..16] OF REAL;

    (* MPC Quadratic Weights & Working Arrays *)
    aWeight_Q                       : ARRAY[1..16] OF REAL;
    aWeight_R                       : ARRAY[1..8] OF REAL;
    aWeight_P                       : ARRAY[1..16] OF REAL;
    aGrad_J                         : ARRAY[1..8] OF REAL;
    aStep_u                         : ARRAY[1..8] OF REAL;

    (* ===================================================================================== *)
    (* 4. 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) VARIABLES                          *)
    (* ===================================================================================== *)
    iState                          : INT := 0;   (* 0=STANDBY ... 120=EMERGENCY_LOCKOUT *)
    iPrevState                      : INT := 0;
    bStateTransition                : BOOL := FALSE;
    bSystemTripped                  : BOOL := FALSE;

    (* Timers for Master State Sequencing *)
    tPumpDownTimer                  : TON;
    tMeltSoakTimer                  : TON;
    tPiezoTuneTimer                 : TON;
    tStreamStabilizeTimer           : TON;
    tShadowgraphCalTimer            : TON;
    tH2MagnetRampTimer              : TON;
    tPrePulseAlignTimer             : TON;
    tIgnitionTimer                  : TON;
    tPowerStabTimer                 : TON;
    tEtchCleanTimer                 : TON;
    tShutdownTimer                  : TON;
    tFaultHoldTimer                 : TON;

    (* Internal Computed Cyber-Physical Variables *)
    rRayleighWavelength_um          : REAL := 54.0;
    rDropletMass_ug                 : REAL := 0.0505;
    rEstimatedPancakeDiam_um        : REAL := 210.0;
    rCalculatedTe_eV                : REAL := 34.5;
    rCalculatedNe_cm3               : REAL := 1.05E19;
    rCalculatedPlasmaEUV_W          : REAL := 1380.0;
    rCalculatedIFEUV_W              : REAL := 502.0;
    rCalculatedCE_Pct               : REAL := 4.85;
    rCalculatedEtchRate_nms         : REAL := 0.045;
    rDropletPosJitterCalc_um        : REAL := 0.85;
    rTargetMirrorCoolingFlow_Pct    : REAL := 45.0;

    (* Internal Actuator Target Profiles before Slew Limiting *)
    rTargetPiezoFreq_kHz            : REAL := 50.0;
    rTargetPiezoVolt_V              : REAL := 32.0;
    rTargetTinPress_bar             : REAL := 82.5;
    rTargetPrePulse_mJ              : REAL := 18.5;
    rTargetMainPulse_J              : REAL := 0.95;
    rTargetInterPulseDelay_us       : REAL := 2.80;
    rTargetGalvoSteerX_urad         : REAL := 0.0;
    rTargetGalvoSteerY_urad         : REAL := 0.0;
    rTargetH2Flow_slpm              : REAL := 150.0;
    rTargetMagnetField_Tesla        : REAL := 1.20;

    (* Slew rate limiters *)
    rMaxSlewPiezoFreq_kHz_s         : REAL := 2.0;
    rMaxSlewPiezoVolt_V_s           : REAL := 10.0;
    rMaxSlewTinPress_bar_s          : REAL := 5.0;
    rMaxSlewPrePulse_mJ_s           : REAL := 5.0;
    rMaxSlewMainPulse_J_s           : REAL := 0.20;
    rMaxSlewGalvo_urad_s            : REAL := 100.0;
    rMaxSlewH2Flow_slpm_s           : REAL := 30.0;
    rMaxSlewMagnet_Tesla_s          : REAL := 0.10;

    (* Internal loop counters *)
    iIdx                            : INT := 1;
    jIdx                            : INT := 1;
    kIdx                            : INT := 1;
END_VAR
"""
