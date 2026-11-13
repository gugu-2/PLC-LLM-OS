# subsea_boosting_builder/st_header_and_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_OilGas_Subsea_MultiphaseTwinScrew_Boosting_AntiSurge
(* ==================================================================================================== *)
(* LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - V7 MAX-PERSONA                                       *)
(* SUBSEA 3,000-METER DEEPWATER MULTIPHASE BOOSTING & FAST HYDRAULIC ANTI-SURGE STATION                 *)
(* Dual 4.5 MW Twin-Screw Multiphase Boosting System with 2oo3 TMR Voting, Receding-Horizon MPC,        *)
(* Pressurized Barrier Fluid Closed-Loop (Plan 53B/C), Dynamic MEG Hydrate Inhibition,                  *)
(* Screw Differential Thermal Expansion Compensation, and 14-Stage Deterministic Production FSM.        *)
(* ==================================================================================================== *)

VAR_INPUT
    (* Master Execution & Supervisory Commands *)
    bEnable                                     : BOOL := FALSE;    (* Master subsea boosting station enable command *)
    bReset                                      : BOOL := FALSE;    (* Master fault and ESD safety latch trip reset *)
    bEmergencyStop_SubseaESD                    : BOOL := FALSE;    (* Subsea umbilical high-integrity ESD hard trip *)
    bAutoMode                                   : BOOL := TRUE;     (* Automatic supervisory MPC closed-loop selector *)
    bProductionPermissive                       : BOOL := FALSE;    (* Topside host platform production flow permissive *)

    (* 2oo3 Triple Modular Redundant (TMR) Suction Header Pressure Transmitters [bar] *)
    rSuctionPress_PT1_bar                       : REAL := 45.0;     (* Subsea suction header quartz transmitter PT-101 [bar] *)
    rSuctionPress_PT2_bar                       : REAL := 45.0;     (* Subsea suction header quartz transmitter PT-102 [bar] *)
    rSuctionPress_PT3_bar                       : REAL := 45.0;     (* Subsea suction header quartz transmitter PT-103 [bar] *)

    (* 2oo3 Triple Modular Redundant (TMR) Discharge Header Pressure Transmitters [bar] *)
    rDischargePress_PT1_bar                     : REAL := 115.0;    (* Subsea discharge header quartz transmitter PT-201 [bar] *)
    rDischargePress_PT2_bar                     : REAL := 115.0;    (* Subsea discharge header quartz transmitter PT-202 [bar] *)
    rDischargePress_PT3_bar                     : REAL := 115.0;    (* Subsea discharge header quartz transmitter PT-203 [bar] *)

    (* 2oo3 Triple Modular Redundant (TMR) Gamma-Ray Multiphase Gas Volume Fraction (GVF) Meters [%] *)
    rGVF_Sensor1_pct                            : REAL := 65.0;     (* Inline gamma-ray water-liquid-gas fraction meter GVF-301 [%] *)
    rGVF_Sensor2_pct                            : REAL := 65.0;     (* Inline gamma-ray water-liquid-gas fraction meter GVF-302 [%] *)
    rGVF_Sensor3_pct                            : REAL := 65.0;     (* Inline gamma-ray water-liquid-gas fraction meter GVF-303 [%] *)

    (* 2oo3 Triple Modular Redundant (TMR) Barrier Fluid Mechanical Seal Differential Pressure Transmitters [bar] *)
    rSealDP_Sensor1_bar                         : REAL := 42.0;     (* Subsea mechanical seal pressurized barrier DP PDT-401 [bar] *)
    rSealDP_Sensor2_bar                         : REAL := 42.0;     (* Subsea mechanical seal pressurized barrier DP PDT-402 [bar] *)
    rSealDP_Sensor3_bar                         : REAL := 42.0;     (* Subsea mechanical seal pressurized barrier DP PDT-403 [bar] *)

    (* Process Temperature & Ambient Seabed Telemetry Transducers *)
    rSuctionTemp_degC                           : REAL := 58.0;     (* Suction manifold multiphase temperature TT-105 [deg C] *)
    rDischargeTemp_degC                         : REAL := 82.0;     (* Discharge manifold boosted temperature TT-205 [deg C] *)
    rBarrierFluidTemp_degC                      : REAL := 48.0;     (* Closed-loop barrier fluid reservoir temperature TT-405 [deg C] *)
    rSeabedAmbientPress_bar                     : REAL := 302.0;    (* 3,000-meter hydrostatic seabed ambient pressure [bar] *)
    rSeabedAmbientTemp_degC                     : REAL := 3.2;      (* Seabed ambient seawater bottom temperature [deg C] *)

    (* 4.5 MW Subsea Variable Speed Drive (VFD) & Twin-Screw Motor Feedback *)
    rMotorVFD_SpeedFeedback_RPM                 : REAL := 0.0;      (* Subsea motor resolver/encoder shaft speed feedback [RPM] *)
    rMotorVFD_ShaftTorque_kNm                   : REAL := 0.0;      (* Subsea motor absorbed electromagnetic airgap torque [kNm] *)
    rMotorStatorWindingTemp_degC                : REAL := 62.0;     (* Subsea motor high-voltage stator winding RTD [deg C] *)
    rMotorCurrentRMS_A                          : REAL := 0.0;      (* Subsea motor 6.6 kV 3-phase RMS current telemetry [A] *)

    (* Subsea Cartridge Mechanical Dynamics & Structural Transducers *)
    rPumpRadialVibration_DE_RMS_mps2            : REAL := 0.85;     (* Twin-screw drive-end accelerometer RMS vibration [m/s2] *)
    rPumpRadialVibration_NDE_RMS_mps2           : REAL := 0.92;     (* Non-drive-end accelerometer RMS vibration [m/s2] *)
    rPumpThrustBearingDisplacement_um           : REAL := 22.0;     (* Active hydrodynamic thrust collar proximity gap [um] *)
    rBarrierFluidLeakRate_mLmin                 : REAL := 1.8;      (* Subsea API 53B/C barrier circuit flow leak meter [mL/min] *)
    rMEG_InhibitorSupplyPress_bar               : REAL := 380.0;    (* Subsea chemical injection umbilical MEG line pressure [bar] *)

    (* Actuator Position Telemetry Feedbacks *)
    rKickbackValvePosition_Feedback_pct         : REAL := 100.0;    (* Fast hydraulic anti-surge valve LVDT position feedback [%] *)
    rChokeTrimPosition_Feedback_pct             : REAL := 0.0;      (* Subsea production choke stepping actuator feedback [%] *)
    rMEG_ValvePosition_Feedback_pct             : REAL := 0.0;      (* Mono-ethylene glycol injection throttling valve LVDT [%] *)
    rBarrierAccumulatorPress_bar                : REAL := 365.0;    (* Subsea barrier fluid piston accumulator pressure [bar] *)

    (* Operator & Topside Supervisory Setpoints *)
    rTargetDischargePress_Setpoint_bar          : REAL := 115.0;    (* Topside SCADA boosted header export pressure target setpoint [bar] *)
    rTargetSuctionPress_Setpoint_bar            : REAL := 45.0;     (* Wellhead suction manifold target pressure setpoint [bar] *)
    rMaxAllowableDiffPress_bar                  : REAL := 95.0;     (* Maximum twin-screw allowable differential pressure limit [bar] *)
    rTargetMEG_DosingRatio_pct                  : REAL := 35.0;     (* Target MEG thermodynamic hydrate inhibitor mass fraction [%] *)
    rCycleTime_s                                : REAL := 0.020;    (* Deterministic discrete task execution scan cycle time [s] *)
END_VAR

VAR_OUTPUT
    (* Station Operating States & Supervisory Interlocks *)
    bStationReady                               : BOOL := FALSE;    (* Subsea station armed, seal pressurized, ready for start *)
    bStationRunning                             : BOOL := FALSE;    (* Subsea station in active nominal multiphase boosting run *)
    bStationTripped                             : BOOL := FALSE;    (* Subsea emergency shutdown ESD latch active *)
    bStationWarning                             : BOOL := FALSE;    (* Operational warning or degraded sensor channel active *)
    nActiveStateIndex                           : INT := 0;         (* Active 14-stage deterministic FSM state index (0..13) *)

    (* Actuator Output Demand Setpoints *)
    rVFD_SpeedDemand_RPM                        : REAL := 0.0;      (* Commanded subsea 4.5 MW VFD motor speed setpoint [RPM] *)
    rKickbackValveDemand_pct                    : REAL := 100.0;    (* Fast subsea hydraulic anti-surge recycle valve command [%] *)
    rMEG_InhibitorValveDemand_pct               : REAL := 0.0;      (* Mono-ethylene glycol chemical dosing valve command [%] *)
    rBarrierFluidChargeDemand_pct               : REAL := 0.0;      (* Barrier accumulator hydraulic charge valve command [%] *)
    rChokeTrimDemand_pct                        : REAL := 0.0;      (* Subsea production export choke valve position demand [%] *)
    rMistCoolingRecycleDemand_pct               : REAL := 0.0;      (* High-GVF mist cooling liquid injection valve command [%] *)

    (* Synthesized 2oo3 TMR Validated Telemetry Outputs *)
    rVotedSuctionPress_bar                      : REAL := 45.0;     (* 2oo3 voted suction manifold quartz pressure [bar] *)
    rVotedDischargePress_bar                    : REAL := 115.0;    (* 2oo3 voted discharge manifold quartz pressure [bar] *)
    rVotedGVF_pct                               : REAL := 65.0;     (* 2oo3 voted multiphase mixture gas volume fraction [%] *)
    rVotedSealDP_bar                            : REAL := 42.0;     (* 2oo3 voted barrier fluid overpressure differential [bar] *)

    (* Cyber-Physical Thermodynamic & Observer Estimates *)
    rTwinScrewDifferentialPress_bar             : REAL := 70.0;     (* Active pump differential pressure (P_dis - P_suc) [bar] *)
    rEstimatedThermalGrowth_um                  : REAL := 0.0;      (* Estimated twin-screw differential rotor/casing expansion [um] *)
    rDynamicClearance_um                        : REAL := 110.0;    (* Estimated remaining screw-to-screw running clearance [um] *)
    rHydrateSubcoolingMargin_degC               : REAL := 18.5;     (* Thermodynamic hydrate formation safety temperature margin [deg C] *)
    rMixtureAcousticSpeed_mps                   : REAL := 185.0;    (* Estimated multiphase acoustic mixture sonic velocity [m/s] *)
    rSurgeProximityMargin_pct                   : REAL := 45.0;     (* Anti-surge safety operating margin to dynamic surge line [%] *)
    rMultiphaseMixtureDensity_kgm3              : REAL := 340.0;    (* Homogeneous multiphase mixture bulk fluid density [kg/m3] *)
    rHydraulicAbsorbedPower_kW                  : REAL := 2850.0;   (* Estimated shaft absorbed hydraulic power [kW] *)

    (* ISA-18.2 Bit-Packed 32-Bit Alarm & Diagnostic Status Words *)
    dwAlarmWord1                                : DWORD := 16#00000000; (* Process alarms: Suction/Discharge/DP/GVF trip latches *)
    dwAlarmWord2                                : DWORD := 16#00000000; (* Mechanical & Seal alarms: Seal DP/Leak/Growth/Vibration *)
    dwStatusWord1                               : DWORD := 16#00000000; (* Operating status: TMR health, FSM phase flags, MPC active *)
    dwStatusWord2                               : DWORD := 16#00000000; (* Diagnostics: Sensor degradation, subsea umbilical link *)
END_VAR
"""
