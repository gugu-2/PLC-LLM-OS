# cz_builder/cz_vars.py

def get_var_input():
    return """VAR_INPUT
    (* ===================================================================================== *)
    (* 1. SYSTEM MASTER DIGITAL PERMISSIVES & SUPERVISORY INTERLOCKS                         *)
    (* ===================================================================================== *)
    bMasterEnable                   : BOOL;     (* Master supervisory furnace run permissive *)
    bEmergencyStop                  : BOOL;     (* SIL-3 hardwired safety relay trip circuit [active-low] *)
    bResetFaults                    : BOOL;     (* Master alarm unlatch and trip reset *)
    bFurnaceDoorLocked              : BOOL;     (* Chamber vacuum seal and clamp interlock *)
    bVacuumPumpSkidReady            : BOOL;     (* Roots blower and dry screw vacuum pump online *)
    bArgonSupplyPermissive          : BOOL;     (* Ultra-pure 8N Argon gas supply header pressurized [bar] *)
    bCoolingWaterFlowOk             : BOOL;     (* Double-walled water cooling jacket flow switch healthy *)
    bManualOverride                 : BOOL;     (* Engineering manual actuator override permissive *)

    (* ===================================================================================== *)
    (* 2. TRIPLE MODULAR REDUNDANT (2oo3) MELT OPTICAL PYROMETERS [deg C]                    *)
    (* ===================================================================================== *)
    rMeltTempPyrometer_DegC_Ch1     : REAL;     (* Melt surface two-color optical pyrometer Ch1 [deg C] *)
    rMeltTempPyrometer_DegC_Ch2     : REAL;     (* Melt surface two-color optical pyrometer Ch2 [deg C] *)
    rMeltTempPyrometer_DegC_Ch3     : REAL;     (* Melt surface two-color optical pyrometer Ch3 [deg C] *)

    (* ===================================================================================== *)
    (* 3. TRIPLE MODULAR REDUNDANT (2oo3) MENISCUS CCD CAMERAS [mm]                          *)
    (* ===================================================================================== *)
    rMeniscusDiameter_mm_Ch1        : REAL;     (* Optical CCD meniscus ring diameter sensor Ch1 [mm] *)
    rMeniscusDiameter_mm_Ch2        : REAL;     (* Optical CCD meniscus ring diameter sensor Ch2 [mm] *)
    rMeniscusDiameter_mm_Ch3        : REAL;     (* Optical CCD meniscus ring diameter sensor Ch3 [mm] *)

    (* ===================================================================================== *)
    (* 4. TRIPLE MODULAR REDUNDANT (2oo3) CHAMBER VACUUM CAPACITANCE MANOMETERS [mbar]       *)
    (* ===================================================================================== *)
    rChamberPressure_mbar_Ch1       : REAL;     (* Capacitance manometer vacuum pressure Ch1 [mbar] *)
    rChamberPressure_mbar_Ch2       : REAL;     (* Capacitance manometer vacuum pressure Ch2 [mbar] *)
    rChamberPressure_mbar_Ch3       : REAL;     (* Capacitance manometer vacuum pressure Ch3 [mbar] *)

    (* ===================================================================================== *)
    (* 5. TRIPLE MODULAR REDUNDANT (2oo3) MELT LEVEL LASER TRIANGULATION [mm]                *)
    (* ===================================================================================== *)
    rMeltLevelLaser_mm_Ch1          : REAL;     (* Melt surface laser triangulation level sensor Ch1 [mm] *)
    rMeltLevelLaser_mm_Ch2          : REAL;     (* Melt surface laser triangulation level sensor Ch2 [mm] *)
    rMeltLevelLaser_mm_Ch3          : REAL;     (* Melt surface laser triangulation level sensor Ch3 [mm] *)

    (* ===================================================================================== *)
    (* 6. TRIPLE MODULAR REDUNDANT (2oo3) CRUCIBLE GRAPHITE SUSCEPTOR THERMOCOUPLES [deg C]  *)
    (* ===================================================================================== *)
    rCrucibleWallTemp_DegC_Ch1      : REAL;     (* Graphite susceptor Type B thermocouple Ch1 [deg C] *)
    rCrucibleWallTemp_DegC_Ch2      : REAL;     (* Graphite susceptor Type B thermocouple Ch2 [deg C] *)
    rCrucibleWallTemp_DegC_Ch3      : REAL;     (* Graphite susceptor Type B thermocouple Ch3 [deg C] *)

    (* ===================================================================================== *)
    (* 7. ACTUATOR POSITION & VELOCITY FEEDBACKS [mm/min], [rpm], [slpm], [kg]               *)
    (* ===================================================================================== *)
    rActualPullSpeed_mmpm           : REAL;     (* High-precision seed wire encoder pull velocity [mm/min] *)
    rActualCrucibleLift_mmpm        : REAL;     (* Quartz crucible servo lift velocity [mm/min] *)
    rActualSeedRotation_rpm         : REAL;     (* Seed crystal rotation rate [rpm] *)
    rActualCrucibleRotation_rpm     : REAL;     (* Quartz crucible rotation rate [rpm] *)
    rActualArgonInletFlow_slpm      : REAL;     (* Mass flow controller argon inlet gas flow [slpm] *)
    rChamberShellTemp_DegC          : REAL;     (* Water-cooled stainless steel shell outer temp [deg C] *)
    rCrystalLoadCell_kg             : REAL;     (* Seed shaft high-resolution crystal weight load cell [kg] *)

    (* ===================================================================================== *)
    (* 8. HEATER ELECTRICAL FEEDBACK TELEMETRY [A], [V], [kW]                                *)
    (* ===================================================================================== *)
    rUpperSideHeaterCurrent_A       : REAL;     (* Upper graphite resistance heater current feedback [A] *)
    rLowerSideHeaterCurrent_A       : REAL;     (* Lower graphite resistance heater current feedback [A] *)
    rBottomHeaterCurrent_A          : REAL;     (* Bottom pancake graphite heater current feedback [A] *)
    rUpperSideHeaterVoltage_V       : REAL;     (* Upper graphite heater voltage feedback [V] *)
    rLowerSideHeaterVoltage_V       : REAL;     (* Lower graphite heater voltage feedback [V] *)
    rBottomHeaterVoltage_V          : REAL;     (* Bottom heater voltage feedback [V] *)

    (* ===================================================================================== *)
    (* 9. SUPERVISORY RECIPE PARAMETERS & SYSTEM TIMING [mm], [kg], [g], [s]                 *)
    (* ===================================================================================== *)
    rTargetIngotDiameter_mm         : REAL;     (* Supervisory crystal target diameter setpoint [mm] *)
    rTargetIngotLength_mm           : REAL;     (* Supervisory target body pull length [mm] *)
    rInitialPolyCharge_kg           : REAL;     (* Initial polysilicon chunk mass charged into crucible [kg] *)
    rDopantMass_g                   : REAL;     (* Target dopant pellet mass [g] *)
    rCycleTime_sec                  : REAL;     (* Deterministic execution scan cycle time [s] *)
END_VAR
"""

def get_var_output():
    return """VAR_OUTPUT
    (* ===================================================================================== *)
    (* 1. SYSTEM DISCRETE STATUS WORDS & HEALTH FLAGS                                        *)
    (* ===================================================================================== *)
    bSystemRunning                  : BOOL;     (* Furnace in active operational growth cycle *)
    bSystemReady                    : BOOL;     (* Polysilicon molten, stabilized, and ready for dipping *)
    bSystemTripped                  : BOOL;     (* Latched emergency safety trip condition *)
    bDiameterLockEngaged            : BOOL;     (* Closed-loop optical meniscus diameter lock active *)
    bDislocationFreeStructure       : BOOL;     (* Dash necking dislocation suppression confirmed *)
    bDegradedSensorMode             : BOOL;     (* Operating under 1oo2 or 1oo1 fallback sensor voting *)
    bVoronkovRatioOutOfBounds       : BOOL;     (* Ingot defect ratio v/G deviation alarm *)
    bCrucibleLeakHazard             : BOOL;     (* Catastrophic crucible melt breach warning *)

    (* ===================================================================================== *)
    (* 2. ACTUATOR VELOCITY & MOTION COMMANDS [mm/min], [rpm]                                *)
    (* ===================================================================================== *)
    rSeedPullSpeedDemand_mmpm       : REAL;     (* Seed lift servo speed setpoint [mm/min] *)
    rCrucibleLiftDemand_mmpm        : REAL;     (* Crucible lift servo speed setpoint [mm/min] *)
    rSeedRotationDemand_rpm         : REAL;     (* Seed crystal rotation velocity command [rpm] *)
    rCrucibleRotationDemand_rpm     : REAL;     (* Quartz crucible rotation velocity command [rpm] *)

    (* ===================================================================================== *)
    (* 3. MULTI-ZONE HEATER POWER COMMANDS [kW]                                              *)
    (* ===================================================================================== *)
    rUpperHeaterPowerDemand_kW      : REAL;     (* Upper side heater SCR thyristor power demand [kW] *)
    rLowerHeaterPowerDemand_kW      : REAL;     (* Lower side heater SCR thyristor power demand [kW] *)
    rBottomHeaterPowerDemand_kW     : REAL;     (* Bottom heater power demand [kW] *)

    (* ===================================================================================== *)
    (* 4. GAS & VACUUM CONDUCTANCE COMMANDS [%], [slpm]                                      *)
    (* ===================================================================================== *)
    rArgonPurgeValveDemand_pct      : REAL;     (* Argon purge gas mass flow setpoint [%] *)
    rThrottleValveDemand_pct        : REAL;     (* Vacuum throttle valve conductance setpoint [%] *)

    (* ===================================================================================== *)
    (* 5. PROCESS OBSERVER ESTIMATES & CRYSTALLIZATION TELEMETRY                             *)
    (* ===================================================================================== *)
    rEstimatedCrystalDiameter_mm    : REAL;     (* Filtered solid crystal diameter estimate [mm] *)
    rEstimatedMeltLevel_mm          : REAL;     (* Crucible melt surface level relative to reference [mm] *)
    rMeniscusHeight_mm              : REAL;     (* Calculated bright capillary meniscus height [mm] *)
    rMeniscusGrowthAngle_deg        : REAL;     (* Calculated solid-liquid growth contact angle [deg] *)
    rAxialThermalGradient_Kcm       : REAL;     (* Estimated axial temperature gradient G0 [K/cm] *)
    rVoronkovRatio_vG               : REAL;     (* Calculated Voronkov defect ratio v/G [mm2/(min*K)] *)
    rCrystalLength_mm               : REAL;     (* Cumulative pulled crystal length [mm] *)
    rCrystalMass_kg                 : REAL;     (* Integrated solid ingot mass [kg] *)
    rRemainingMeltMass_kg           : REAL;     (* Calculated remaining molten silicon mass in crucible [kg] *)
    iOperatingStage                 : INT;      (* Current FSM stage (0 to 11) *)

    (* ===================================================================================== *)
    (* 6. BIT-PACKED STATUS & ALARM TELEMETRY REGISTERS (DWORD)                              *)
    (* ===================================================================================== *)
    dwSystemStatusWord              : DWORD;    (* Bit-packed operational state and status flags *)
    dwAlarmWord1                    : DWORD;    (* Critical SIL-3 process safety and hardware trips *)
    dwAlarmWord2                    : DWORD;    (* Process out-of-spec, optical lock, and drive trips *)
    dwWarningWord                   : DWORD;    (* Predictive, sensor degraded, and maintenance alerts *)
END_VAR
"""

def get_var():
    return """VAR
    (* ===================================================================================== *)
    (* 1. PHYSICAL, THERMODYNAMIC & MULTIPHYSICS SILICON CONSTANTS                           *)
    (* ===================================================================================== *)
    rConst_MeltTemp_DegC            : REAL := 1414.0;       (* Silicon melting temperature [deg C] *)
    rConst_MeltTemp_K               : REAL := 1687.15;      (* Silicon melting temperature [K] *)
    rConst_LatentHeat_Jkg           : REAL := 1800000.0;    (* Silicon latent heat of fusion [J/kg] *)
    rConst_RhoSolid_kgm3            : REAL := 2330.0;       (* Solid silicon density at melting point [kg/m3] *)
    rConst_RhoLiquid_kgm3           : REAL := 2570.0;       (* Liquid molten silicon density [kg/m3] *)
    rConst_CondSolid_WmK            : REAL := 22.0;         (* Solid silicon thermal conductivity [W/(m*K)] *)
    rConst_CondLiquid_WmK           : REAL := 64.0;         (* Liquid silicon thermal conductivity [W/(m*K)] *)
    rConst_SurfaceTension_Nm        : REAL := 0.720;        (* Molten silicon surface tension [N/m] *)
    rConst_Gravity_ms2              : REAL := 9.80665;      (* Gravitational acceleration [m/s2] *)
    rConst_CapillaryConst_mm        : REAL := 7.56;         (* Capillary constant a = SQRT(2*sigma/(rho*g)) [mm] *)
    rConst_NominalContactAngle_deg  : REAL := 11.0;         (* Equilibrium wetting growth contact angle [deg] *)
    rConst_CrucibleRadius_mm        : REAL := 406.4;        (* Inner radius of 32-inch quartz crucible [mm] *)
    rConst_CrucibleArea_mm2         : REAL := 518882.0;     (* Cross-sectional melt area of 32-inch crucible [mm2] *)
    rConst_TargetRadius_mm          : REAL := 150.0;        (* Nominal ingot body radius (300 mm diameter) [mm] *)
    rConst_TargetArea_mm2           : REAL := 70685.8;      (* Cross-sectional area of 300 mm ingot [mm2] *)
    rConst_VoronkovCrit_mm2minK     : REAL := 0.220;        (* Critical Voronkov ratio v/G [mm2/(min*K)] *)
    rConst_VoronkovMin_mm2minK      : REAL := 0.200;        (* Minimum defect-free Voronkov ratio [mm2/(min*K)] *)
    rConst_VoronkovMax_mm2minK      : REAL := 0.240;        (* Maximum defect-free Voronkov ratio [mm2/(min*K)] *)
    rConst_StefanBoltzmann          : REAL := 5.67037E-8;   (* Stefan-Boltzmann radiation constant [W/(m2*K4)] *)
    rConst_Pi                       : REAL := 3.14159265;   (* Archimedes mathematical constant Pi [-] *)

    (* ===================================================================================== *)
    (* 2. TRIPLE MODULAR REDUNDANCY (2oo3) VOTING INTERNAL REGISTERS                         *)
    (* ===================================================================================== *)
    (* Melt Surface Pyrometer Voting Channels *)
    rVotedMeltTemp_DegC             : REAL := 1420.0;
    bMeltTemp_Dev_1_2               : BOOL := FALSE;
    bMeltTemp_Dev_2_3               : BOOL := FALSE;
    bMeltTemp_Dev_1_3               : BOOL := FALSE;
    bMeltTemp_Ch1_Fault             : BOOL := FALSE;
    bMeltTemp_Ch2_Fault             : BOOL := FALSE;
    bMeltTemp_Ch3_Fault             : BOOL := FALSE;
    bMeltTemp_Degraded_1oo2         : BOOL := FALSE;

    (* Meniscus Camera Diameter Voting Channels *)
    rVotedMeniscusDiam_mm           : REAL := 0.0;
    bMeniscusDiam_Dev_1_2           : BOOL := FALSE;
    bMeniscusDiam_Dev_2_3           : BOOL := FALSE;
    bMeniscusDiam_Dev_1_3           : BOOL := FALSE;
    bMeniscusDiam_Ch1_Fault         : BOOL := FALSE;
    bMeniscusDiam_Ch2_Fault         : BOOL := FALSE;
    bMeniscusDiam_Ch3_Fault         : BOOL := FALSE;
    bMeniscusDiam_Degraded_1oo2     : BOOL := FALSE;

    (* Chamber Vacuum Pressure Voting Channels *)
    rVotedChamberPress_mbar         : REAL := 20.0;
    bChamberPress_Dev_1_2           : BOOL := FALSE;
    bChamberPress_Dev_2_3           : BOOL := FALSE;
    bChamberPress_Dev_1_3           : BOOL := FALSE;
    bChamberPress_Ch1_Fault         : BOOL := FALSE;
    bChamberPress_Ch2_Fault         : BOOL := FALSE;
    bChamberPress_Ch3_Fault         : BOOL := FALSE;
    bChamberPress_Degraded_1oo2     : BOOL := FALSE;

    (* Melt Surface Level Laser Voting Channels *)
    rVotedMeltLevel_mm              : REAL := 0.0;
    bMeltLevel_Dev_1_2              : BOOL := FALSE;
    bMeltLevel_Dev_2_3              : BOOL := FALSE;
    bMeltLevel_Dev_1_3              : BOOL := FALSE;
    bMeltLevel_Ch1_Fault            : BOOL := FALSE;
    bMeltLevel_Ch2_Fault            : BOOL := FALSE;
    bMeltLevel_Ch3_Fault            : BOOL := FALSE;
    bMeltLevel_Degraded_1oo2        : BOOL := FALSE;

    (* Crucible Graphite Susceptor Thermocouple Voting Channels *)
    rVotedCrucibleTemp_DegC         : REAL := 1480.0;
    bCrucibleTemp_Dev_1_2           : BOOL := FALSE;
    bCrucibleTemp_Dev_2_3           : BOOL := FALSE;
    bCrucibleTemp_Dev_1_3           : BOOL := FALSE;
    bCrucibleTemp_Ch1_Fault         : BOOL := FALSE;
    bCrucibleTemp_Ch2_Fault         : BOOL := FALSE;
    bCrucibleTemp_Ch3_Fault         : BOOL := FALSE;
    bCrucibleTemp_Degraded_1oo2     : BOOL := FALSE;

    (* ===================================================================================== *)
    (* 3. 12-STATE MULTIVARIABLE STATE-SPACE DISCRETE MODEL MATRICES                         *)
    (* States: x1: Delta D_c [mm], x2: Delta h_m [mm], x3: Delta phi_L [deg],                *)
    (*         x4: T_melt [deg C], x5: T_bulk [deg C], x6: T_h_up [deg C],                   *)
    (*         x7: T_h_low [deg C], x8: T_h_bot [deg C], x9: T_cruc [deg C],                 *)
    (*         x10: Delta z_melt [mm], x11: G_0 [K/cm], x12: M_xtal [kg]                     *)
    (* Inputs: u1: v_pull [mm/min], u2: v_cruc [mm/min], u3: P_h_up [kW],                    *)
    (*         u4: P_h_low [kW], u5: P_h_bot [kW], u6: omega_seed [rpm],                     *)
    (*         u7: omega_cruc [rpm], u8: Q_Ar [slpm]                                         *)
    (* ===================================================================================== *)
    aMatrix_A                       : ARRAY[1..12, 1..12] OF REAL;
    aMatrix_B                       : ARRAY[1..12, 1..8] OF REAL;
    aMatrix_C                       : ARRAY[1..12, 1..12] OF REAL;
    aMatrix_D                       : ARRAY[1..12, 1..8] OF REAL;

    (* State and Input Trajectory Vectors *)
    aState_x                        : ARRAY[1..12] OF REAL;
    aState_x_next                   : ARRAY[1..12] OF REAL;
    aState_y                        : ARRAY[1..12] OF REAL;
    aControl_u                      : ARRAY[1..8] OF REAL;
    aControl_u_prev                 : ARRAY[1..8] OF REAL;
    aSetpoint_ref                   : ARRAY[1..12] OF REAL;

    (* MPC Quadratic Weights & Working Arrays *)
    aWeight_Q                       : ARRAY[1..12] OF REAL;
    aWeight_R                       : ARRAY[1..8] OF REAL;
    aWeight_P                       : ARRAY[1..12] OF REAL;
    aGrad_J                         : ARRAY[1..8] OF REAL;
    aStep_u                         : ARRAY[1..8] OF REAL;
    aHessian_Diag                   : ARRAY[1..8] OF REAL;
    rMpcObjectiveValue              : REAL := 0.0;
    iMpcIterCount                   : INT := 0;
    bMpcOptimalConverged            : BOOL := FALSE;

    (* ===================================================================================== *)
    (* 4. FINITE STATE MACHINE (FSM) & OPERATIONAL TIMERS                                    *)
    (* ===================================================================================== *)
    iState                          : INT := 0;
    tPumpDownTimer                  : TON;
    tArgonPurgeTimer                : TON;
    tPolyMeltingTimer               : TON;
    tMeltStabilizeTimer             : TON;
    tDashNeckingTimer               : TON;
    tCrownGrowthTimer               : TON;
    tBodyStabilizeTimer             : TON;
    tTailOffTimer                   : TON;
    tIngotLiftTimer                 : TON;
    tCoolDownTimer                  : TON;
    tFaultHoldTimer                 : TON;
    tMeniscusLostTimer              : TON;

    (* Internal Actuator Ramping Variables *)
    rTargetPullSpeedInternal        : REAL := 0.0;
    rTargetCrucibleLiftInternal     : REAL := 0.0;
    rTargetUpperPowerInternal       : REAL := 0.0;
    rTargetLowerPowerInternal       : REAL := 0.0;
    rTargetBottomPowerInternal      : REAL := 0.0;
    rTargetSeedRotInternal          : REAL := 0.0;
    rTargetCrucibleRotInternal      : REAL := 0.0;
    rTargetArgonFlowInternal        : REAL := 0.0;
    rTargetThrottleInternal         : REAL := 0.0;

    (* ===================================================================================== *)
    (* 5. MENISCUS OPTICS, STEFAN KINEMATICS & PROCESS CALCULATIONS                          *)
    (* ===================================================================================== *)
    rSolidificationRate_kgs         : REAL := 0.0;
    rLatentHeatRelease_kW           : REAL := 0.0;
    rMeltLevelDropVelocity_mmpm     : REAL := 0.0;
    rCalculatedMeniscusHeight_mm    : REAL := 4.50;
    rCalculatedGrowthAngle_deg      : REAL := 11.0;
    rRadialGrowthRate_mmpm          : REAL := 0.0;
    rAxialGradient_Kcm              : REAL := 35.0;
    rNeckLength_mm                  : REAL := 0.0;
    rCrownLength_mm                 : REAL := 0.0;
    rBodyLength_mm                  : REAL := 0.0;
    rTailLength_mm                  : REAL := 0.0;
    rMeltRemaining_kg               : REAL := 350.0;
    rCumulativeMass_kg              : REAL := 0.0;
    rCrucibleLiftError_mm           : REAL := 0.0;
    rVoronkovCorrection_mmpm        : REAL := 0.0;

    (* ===================================================================================== *)
    (* 6. ISA-18.2 ALARM TRIP POINTS, DEAD-BANDS & STATUS FLAGS                              *)
    (* ===================================================================================== *)
    rTrip_CrucibleWallTemp_HH       : REAL := 1580.0;
    rTrip_MeltTemp_HH               : REAL := 1460.0;
    rTrip_MeltTemp_LL               : REAL := 1410.0;
    rTrip_ChamberPress_HH           : REAL := 45.0;
    rTrip_ChamberPress_LL           : REAL := 5.0;
    rTrip_ArgonFlow_LL              : REAL := 25.0;
    rTrip_ShellTemp_HH              : REAL := 65.0;
    rWarn_ShellTemp_H               : REAL := 50.0;
    rTrip_UpperPower_HH             : REAL := 160.0;
    rTrip_LowerPower_HH             : REAL := 140.0;
    rTrip_BottomPower_HH            : REAL := 80.0;
    rHysteresis_Temp                : REAL := 5.0;
    rHysteresis_Press               : REAL := 1.5;
    bAnySensorDegraded              : BOOL := FALSE;
    bMeniscusSignalValid            : BOOL := FALSE;
END_VAR
"""
