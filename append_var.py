# append_var.py
def generate_var_block():
    return """VAR
    (* ================================================================================================================ *)
    (* DISCRETE STATE-SPACE INTERNAL DYNAMICS MATRICES (16x16 State Matrix A, 16x8 Input Matrix B)                     *)
    (* State Vector x: [ 1: T_inlet_oil (deg C),       2: T_outlet_oil (deg C),      3: T_shelf_plate (deg C),         *)
    (*                   4: T_vial_base (deg C),       5: T_sublim_front (deg C),    6: T_dried_cake (deg C),          *)
    (*                   7: P_vapor_H2O (mbar),        8: P_inert_N2 (mbar),         9: P_chamber_total (mbar),        *)
    (*                  10: P_pirani_apparent (mbar), 11: T_condenser_surface (deg C), 12: Delta_ice_frost (mm),      *)
    (*                  13: mdot_sublimation (kg/h),  14: C_bound_moisture (%),     15: Pos_hydraulic_ram (mm),        *)
    (*                  16: Force_stoppering (kN) ]                                                                    *)
    (* Input Vector u: [ 1: Duty_SCR_Heater (%),       2: SlideValve_ScrewComp (%),  3: Valve_LN2_Booster (%),         *)
    (*                   4: Speed_Roots_Blower (%),    5: Valve_N2_MicroBleed (%),   6: TXV_Condenser_Coil (%),        *)
    (*                   7: Servo_Hydraulic_Ram (%),   8: Valve_Nucleation_Pulse (%) ]                                 *)
    (* Equation: x[k+1] = A * x[k] + B * u[k]                                                                          *)
    (* ================================================================================================================ *)
    aA_Lyo                            : ARRAY[1..16, 1..16] OF REAL;
    aB_Lyo                            : ARRAY[1..16, 1..8] OF REAL;
    ax_LyoState                       : ARRAY[1..16] OF REAL;
    ax_LyoPredicted                   : ARRAY[1..16] OF REAL;
    au_LyoInput                       : ARRAY[1..8] OF REAL;
    au_LyoPrevious                    : ARRAY[1..8] OF REAL;
    aDelta_u_Lyo                      : ARRAY[1..8] OF REAL;
    aStateTrajectoryTarget            : ARRAY[1..16] OF REAL;
    aStateTrackingError               : ARRAY[1..16] OF REAL;

    (* ================================================================================================================ *)
    (* RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) COST MATRICES & ACTUATOR CONSTRAINTS                            *)
    (* Cost Function: J = sum_{j=1}^Np [ (x - r)' * Q * (x - r) + delta_u' * R * delta_u ] + (x_Np - r)' * P * (x_Np - r) *)
    (* ================================================================================================================ *)
    aQ_LyoDiag                        : ARRAY[1..16] OF REAL;
    aR_LyoDiag                        : ARRAY[1..8] OF REAL;
    aP_LyoDiag                        : ARRAY[1..16] OF REAL;
    aActuatorSlewRateLimit            : ARRAY[1..8] OF REAL;
    aActuatorLowerLimit               : ARRAY[1..8] OF REAL;
    aActuatorUpperLimit               : ARRAY[1..8] OF REAL;

    (* ================================================================================================================ *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURES & PERSISTENT DISCREPANCY TIMERS                              *)
    (* ================================================================================================================ *)
    (* Shelf Silicone Oil Inlet & Outlet RTD Transducers *)
    rTMR_Shelf_Diff_AB                : REAL := 0.0;
    rTMR_Shelf_Diff_BC                : REAL := 0.0;
    rTMR_Shelf_Diff_CA                : REAL := 0.0;
    bTMR_Shelf_Fault_A                : BOOL := FALSE;
    bTMR_Shelf_Fault_B                : BOOL := FALSE;
    bTMR_Shelf_Fault_C                : BOOL := FALSE;
    rTMR_Shelf_Timer_A                : REAL := 0.0;
    rTMR_Shelf_Timer_B                : REAL := 0.0;
    rTMR_Shelf_Timer_C                : REAL := 0.0;

    (* Product Vial Center Sublimation Thermocouple Clusters *)
    rTMR_Prod_Diff_AB                 : REAL := 0.0;
    rTMR_Prod_Diff_BC                 : REAL := 0.0;
    rTMR_Prod_Diff_CA                 : REAL := 0.0;
    bTMR_Prod_Fault_A                 : BOOL := FALSE;
    bTMR_Prod_Fault_B                 : BOOL := FALSE;
    bTMR_Prod_Fault_C                 : BOOL := FALSE;
    rTMR_Prod_Timer_A                 : REAL := 0.0;
    rTMR_Prod_Timer_B                 : REAL := 0.0;
    rTMR_Prod_Timer_C                 : REAL := 0.0;

    (* Heated Capacitance Manometer Absolute Vacuum Baratrons *)
    rTMR_CM_Diff_AB                   : REAL := 0.0;
    rTMR_CM_Diff_BC                   : REAL := 0.0;
    rTMR_CM_Diff_CA                   : REAL := 0.0;
    bTMR_CM_Fault_A                   : BOOL := FALSE;
    bTMR_CM_Fault_B                   : BOOL := FALSE;
    bTMR_CM_Fault_C                   : BOOL := FALSE;
    rTMR_CM_Timer_A                   : REAL := 0.0;
    rTMR_CM_Timer_B                   : REAL := 0.0;
    rTMR_CM_Timer_C                   : REAL := 0.0;

    (* Pirani Thermal Conductivity Vacuum Gauges *)
    rTMR_Pirani_Diff_AB               : REAL := 0.0;
    rTMR_Pirani_Diff_BC               : REAL := 0.0;
    rTMR_Pirani_Diff_CA               : REAL := 0.0;
    bTMR_Pirani_Fault_A               : BOOL := FALSE;
    bTMR_Pirani_Fault_B               : BOOL := FALSE;
    bTMR_Pirani_Fault_C               : BOOL := FALSE;
    rTMR_Pirani_Timer_A               : REAL := 0.0;
    rTMR_Pirani_Timer_B               : REAL := 0.0;
    rTMR_Pirani_Timer_C               : REAL := 0.0;

    (* Ice Condenser Refrigeration Surface RTDs *)
    rTMR_Cond_Diff_AB                 : REAL := 0.0;
    rTMR_Cond_Diff_BC                 : REAL := 0.0;
    rTMR_Cond_Diff_CA                 : REAL := 0.0;
    bTMR_Cond_Fault_A                 : BOOL := FALSE;
    bTMR_Cond_Fault_B                 : BOOL := FALSE;
    bTMR_Cond_Fault_C                 : BOOL := FALSE;
    rTMR_Cond_Timer_A                 : REAL := 0.0;
    rTMR_Cond_Timer_B                 : REAL := 0.0;
    rTMR_Cond_Timer_C                 : REAL := 0.0;

    (* Hydraulic Shelf Stoppering Compaction Load Cells *)
    rTMR_Ram_Diff_AB                  : REAL := 0.0;
    rTMR_Ram_Diff_BC                  : REAL := 0.0;
    rTMR_Ram_Diff_CA                  : REAL := 0.0;
    bTMR_Ram_Fault_A                  : BOOL := FALSE;
    bTMR_Ram_Fault_B                  : BOOL := FALSE;
    bTMR_Ram_Fault_C                  : BOOL := FALSE;
    rTMR_Ram_Timer_A                  : REAL := 0.0;
    rTMR_Ram_Timer_B                  : REAL := 0.0;
    rTMR_Ram_Timer_C                  : REAL := 0.0;

    (* ================================================================================================================ *)
    (* PHYSICAL LYOPHILIZER SYSTEM CONSTANTS & FORMULATION GEOMETRY                                                     *)
    (* ================================================================================================================ *)
    c_rShelfAreaTotal_m2              : REAL := 50.0;     (* Total Usable Heat Transfer Shelf Area [m2] *)
    c_rVialCount                      : REAL := 150000.0; (* Standard Production Vial Batch Quantity [count] *)
    c_rVialOuterDiameter_mm           : REAL := 24.0;     (* 10R Borosilicate Glass Vial Outer Diameter [mm] *)
    c_rVialCrossSectionArea_m2        : REAL := 0.000452; (* Cross-Sectional Area per Vial Base (pi*r^2) [m2] *)
    c_rInitialCakeFillDepth_mm        : REAL := 12.5;     (* Initial Liquid Drug Fill Layer Depth [mm] *)
    c_rLatentHeatSublimation_J_g      : REAL := 2835.0;   (* Enthalpy of Sublimation of Ice (Delta H_sub) [J/g] *)
    c_rLatentHeatDesorption_J_g       : REAL := 3150.0;   (* Heat of Desorption of Chemically Bound Water [J/g] *)
    c_rCondenserTotalArea_m2          : REAL := 42.0;     (* Condenser Coil Total Heat Transfer Surface [m2] *)
    c_rIceDensity_kg_m3               : REAL := 918.0;    (* Crystalline Water Ice Frost Density [kg/m3] *)
    c_rIceThermalConductivity_W_mK    : REAL := 2.25;     (* Thermal Conductivity of Condensed Ice Frost [W/m*K] *)
    c_rUniversalGasConstant_R         : REAL := 8314.5;   (* Universal Ideal Gas Constant [J/kmol*K] *)
    c_rWaterMolecularWeight           : REAL := 18.015;   (* Molecular Weight of H2O [kg/kmol] *)
    c_rNitrogenMolecularWeight        : REAL := 28.013;   (* Molecular Weight of N2 [kg/kmol] *)
    c_rChamberFreeVolume_m3           : REAL := 18.5;     (* Process Chamber Net Evacuated Free Volume [m3] *)
    c_rPiraniSensitivityRatio         : REAL := 1.62;     (* Thermal Conductivity Relative Sensitivity Factor H2O/N2 *)

    (* ================================================================================================================ *)
    (* BIOPROCESS OBSERVER VARIABLES, KINETICS & ENDPOINT METROLOGY REGISTERS                                          *)
    (* ================================================================================================================ *)
    rKv_VialHeatTransferCoeff         : REAL := 18.5;     (* Overall Vial Heat Transfer Coefficient (Kv) [W/m2*K] *)
    rRp_CakeMassTransferResistance    : REAL := 125000.0; (* Dry Cake Vapor Transport Resistance (Rp) [m2*s*Pa/kg] *)
    rSaturationVaporPressure_Pice     : REAL := 0.285;    (* Ice Interface Saturation Equilibrium Vapor Pressure [mbar] *)
    rCalculatedWaterVaporPartialPres  : REAL := 0.0;      (* Sublimated Water Vapor Partial Pressure [mbar] *)
    rCalculatedNitrogenPartialPres    : REAL := 0.0;      (* Inert Gas Dosing Nitrogen Partial Pressure [mbar] *)
    rGasCompositionWaterVaporFraction : REAL := 0.0;      (* Molar Fraction of Sublimating Water Vapor [0..1] *)
    rCondenserFrostThickness_mm       : REAL := 0.0;      (* Accumulated Condensed Ice Layer Thickness [mm] *)
    rCondenserFrostThermalDeltaT      : REAL := 0.0;      (* Thermal Conduction Gradient Across Frost Layer [deg C] *)
    rEndpointConvergenceTimer_s       : REAL := 0.0;      (* Dual-Gauge Delta-P Sublimation Endpoint Timer [s] *)
    rPRT_PressureRiseStart_mbar       : REAL := 0.0;      (* Pressure Rise Test Baseline Trapped Vacuum [mbar] *)
    rPRT_PressureRiseElapsed_s        : REAL := 0.0;      (* Duration of Chamber Isolation PRT Test [s] *)
    bPRT_ActiveInProgress             : BOOL := FALSE;    (* Active Chamber Manometric Pressure Rise Test [BOOL] *)
    rSublimationHeatFluxWatts         : REAL := 0.0;      (* Total Instantaneous Sublimation Latent Heat Demand [W] *)
    rShelfOilEnergyFluxWatts          : REAL := 0.0;      (* Net Thermal Energy Inflow from Circulation Skid [W] *)
    rVialBaseTemperatureEstimate      : REAL := 0.0;      (* Estimated Vial Outer Base Glass Temperature [deg C] *)
    rSublimationDrivingForce          : REAL := 0.0;      (* Sublimation Vapor Pressure Gradient (P_ice - P_ch) [mbar] *)
    rDesorptionDrivingForce           : REAL := 0.0;      (* Bound Water Chemical Desorption Driving Gradient [%] *)
    rDryingProgressRatio              : REAL := 0.0;      (* Primary Sublimation Completion Ratio [0..1] *)
    rActiveRampSlope                  : REAL := 0.0;      (* Dynamic Thermal Ramp Rate Setpoint [deg C/s] *)
    rShelfDeltaT_InletOutlet          : REAL := 0.0;      (* Thermal Spread between Shelf Fluid Inlet and Outlet [deg C] *)

    (* ================================================================================================================ *)
    (* MASTER 12-STAGE FINITE STATE MACHINE (FSM) STEP REGISTERS & PROCESS TIMERS                                      *)
    (* ================================================================================================================ *)
    eCurrentState                     : INT := 0;         (* Active Operational State Index (0..120, 999) *)
    eNextState                        : INT := 0;         (* Pending Next State Transition Index *)
    nSubPhaseStep                     : INT := 0;         (* Internal Step Sub-Sequence Counter within Active State *)
    rStateTimerAccumulator_s          : REAL := 0.0;      (* Elapsed Dwell Time in Current State [s] *)
    rShelfRampSetpointActual          : REAL := 20.0;     (* Interpolated Dynamic Shelf Temperature Setpoint [deg C] *)
    rChamberPresSetpointActual        : REAL := 1013.25;  (* Dynamic Chamber Operating Vacuum Setpoint [mbar] *)
    rAnnealingHoldTimer_s             : REAL := 0.0;      (* Crystalline Ice Annealing Dwell Timer [s] *)
    rFreezingHoldTimer_s              : REAL := 0.0;      (* Deep Freezing Eutectic Solidification Timer [s] *)
    rNucleationPulseTimer_s           : REAL := 0.0;      (* Rapid Controlled Ice Fog Depressurization Timer [s] *)
    rPrimaryDryingHoldTimer_s         : REAL := 0.0;      (* Primary Drying Sublimation Plateau Timer [s] *)
    rSecondaryDryingHoldTimer_s       : REAL := 0.0;      (* Secondary Drying Desorption Hold Timer [s] *)
    rStopperingCompactionTimer_s      : REAL := 0.0;      (* Hydraulic Shelf Compression Dwell Timer [s] *)
    rDefrostTimer_s                   : REAL := 0.0;      (* Condenser Steam/Hot Water Ice Melting Timer [s] *)
    rTotalBatchSecondsAccum           : REAL := 0.0;      (* Cumulative Batch Runtime Seconds [s] *)
    bFirstScanInitDone                : BOOL := FALSE;    (* Deterministic System Matrix Initialization Done Flag *)
    bLeakRateTestPassed               : BOOL := FALSE;    (* Chamber High-Vacuum Leak Rate Test Handshake Flag *)
    rLeakRateObserved_mbar_L_s        : REAL := 0.0;      (* Measured Chamber Evacuated Integrity Leak Rate [mbar*L/s] *)
    rLeakRateTestTimer_s              : REAL := 0.0;      (* Chamber Vacuum Integrity Test Elapsed Duration [s] *)
    rLeakRateStartPressure_mbar       : REAL := 0.0;      (* Baseline Chamber Vacuum at Start of Leak Test [mbar] *)

    (* ================================================================================================================ *)
    (* ISA-18.2 MULTI-TIERED ALARM SETPOINTS, HYSTERESIS DEADBANDS & TRIP REGISTERS                                     *)
    (* ================================================================================================================ *)
    rAlarmSet_ProductCollapse_HH      : REAL := -29.0;    (* Critical Formulation Cake Viscoelastic Collapse Trip [deg C] *)
    rAlarmSet_ProductTempHigh_H       : REAL := -30.0;    (* Product Sublimation High Temperature Alert [deg C] *)
    rAlarmSet_ProductTempDeadband     : REAL := 0.50;     (* Product Temperature Alarm Reset Hysteresis [deg C] *)

    rAlarmSet_VacuumLost_HH           : REAL := 0.400;    (* Critical Sublimation Loss of Vacuum Trip Limit [mbar] *)
    rAlarmSet_VacuumHigh_H            : REAL := 0.200;    (* Chamber Vacuum Deviation Alert Setpoint [mbar] *)
    rAlarmSet_VacuumDeadband          : REAL := 0.020;    (* Chamber Vacuum Alarm Reset Hysteresis [mbar] *)

    rAlarmSet_CondenserTempHigh_HH    : REAL := -65.0;    (* Critical Condenser Coil Loss of Cryogenic Trapping [deg C] *)
    rAlarmSet_CondenserTempHigh_H     : REAL := -72.0;    (* Condenser Surface Temperature Degradation Alert [deg C] *)
    rAlarmSet_CondenserDeadband       : REAL := 1.50;     (* Condenser Temperature Reset Hysteresis [deg C] *)

    rAlarmSet_SiliconeOilFlow_LL      : REAL := 180.0;    (* Shelf Circulation Pump Cavitation / Flow Loss Trip [l/min] *)
    rAlarmSet_SiliconeOilFlowDeadband : REAL := 15.0;     (* Thermal Fluid Flow Rate Reset Hysteresis [l/min] *)

    rAlarmSet_ShelfThermalRunaway_HH  : REAL := 65.0;     (* Shelf Electric Heater Runaway Upper Safety Limit [deg C] *)
    rAlarmSet_ShelfTempDeadband       : REAL := 1.00;     (* Shelf Temperature Reset Hysteresis [deg C] *)

    rAlarmSet_ShelfSpread_H           : REAL := 1.20;     (* Shelf Spatial Thermal Gradient Non-Uniformity Alert [deg C] *)
    rAlarmSet_ShelfSpreadDeadband     : REAL := 0.20;     (* Shelf Temperature Spread Reset Hysteresis [deg C] *)

    rAlarmSet_CompressorHead_HH       : REAL := 26.0;     (* Dual-Stage Refrigeration Head High Discharge Pressure [bar] *)
    rAlarmSet_CompressorDeadband      : REAL := 1.00;     (* Compressor Head Pressure Reset Hysteresis [bar] *)

    rAlarmSet_StopperingForce_LL      : REAL := 180.0;    (* Rubber Stopper Incomplete Sealing Compaction Shortfall [kN] *)
    rAlarmSet_StopperingForceDeadband : REAL := 10.0;     (* Stoppering Force Reset Hysteresis [kN] *)

    rAlarmSet_HydraulicOilPres_HH     : REAL := 265.0;    (* Hydraulic Power Unit Ram Overpressure Safety Relief [bar] *)
    rAlarmSet_HydraulicDeadband       : REAL := 5.00;     (* Hydraulic Pressure Reset Hysteresis [bar] *)

    rAlarmSet_SterileN2Supply_L       : REAL := 4.00;     (* High-Purity Inert Gas Inflow Header Pressure Low [bar] *)
    rAlarmSet_SterileN2Deadband       : REAL := 0.30;     (* Inert Gas Supply Pressure Reset Hysteresis [bar] *)

    (* ISA-18.2 Latched Alarms *)
    bAlarm_ProductCollapseRisk_HH     : BOOL := FALSE;
    bAlarm_ProductTempHigh_H          : BOOL := FALSE;
    bAlarm_VacuumLost_HH              : BOOL := FALSE;
    bAlarm_VacuumHigh_H               : BOOL := FALSE;
    bAlarm_CondenserTempHigh_HH       : BOOL := FALSE;
    bAlarm_CondenserTempHigh_H        : BOOL := FALSE;
    bAlarm_SiliconeOilFlow_LL         : BOOL := FALSE;
    bAlarm_ShelfThermalRunaway_HH     : BOOL := FALSE;
    bAlarm_ShelfSpread_H              : BOOL := FALSE;
    bAlarm_CompressorHead_HH          : BOOL := FALSE;
    bAlarm_StopperingForce_LL         : BOOL := FALSE;
    bAlarm_HydraulicOilPres_HH        : BOOL := FALSE;
    bAlarm_DoorInterlockViolated_HH   : BOOL := FALSE;
    bAlarm_EmergencyStopTripped_HH    : BOOL := FALSE;
    bAlarm_SensorTMR_Discrepancy_H    : BOOL := FALSE;
    bAlarm_SterileN2Supply_L          : BOOL := FALSE;

    (* Calculation Indices, Polynomial Approximations & Temporary Storage *)
    nRowIdx                           : INT := 1;
    nColIdx                           : INT := 1;
    nInputIdx                         : INT := 1;
    rMPC_GradientAcc                  : REAL := 0.0;
    rMPC_HessianTerm                  : REAL := 0.0;
    rClausiusExponent                 : REAL := 0.0;
    rTenPowerTerm                     : REAL := 0.0;
    rTempLogCalc                      : REAL := 0.0;
    rExpSeriesTerm                    : REAL := 0.0;
    rVialBaseTemperatureEstimate      : REAL := 0.0;
    rSublimationDrivingForce          : REAL := 0.0;
    rDesorptionDrivingForce           : REAL := 0.0;
    rDryingProgressRatio              : REAL := 0.0;
    rActiveRampSlope                  : REAL := 0.0;
    rShelfDeltaT_InletOutlet          : REAL := 0.0;
END_VAR
"""

print("generate_var_block defined.")
