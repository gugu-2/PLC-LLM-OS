# Section 2: Variable Declarations (VAR_INPUT, VAR_OUTPUT, VAR)
def get_sec2_vars():
    return """VAR_INPUT
    (* ================================================================================================= *)
    (* PRIMARY FUNCTIONAL SAFETY & HARDWIRED INTERLOCK INPUTS (SIL-3 / 1oo2D / 2oo3 ARCHITECTURE)      *)
    (* ================================================================================================= *)
    bEmergencyStop_CH1              : BOOL;     (* SIL-3 Active-low emergency shutdown loop channel 1 *)
    bEmergencyStop_CH2              : BOOL;     (* SIL-3 Active-low emergency shutdown loop channel 2 *)
    bMasterSystemEnable             : BOOL;     (* Master cyber-physical supervision permissive command *)
    bReactorScramPermissive         : BOOL;     (* Plant Protection System (PPS) core fast trip permissive *)
    bSafetyFreezePlugHealthy        : BOOL;     (* Passive molten salt freeze plug thermal margin healthy *)
    bContainmentIsolationClosed     : BOOL;     (* Reactor containment secondary barrier boundary isolated *)
    bMaintenanceOverrideKey         : BOOL;     (* Hardwired trapped-key maintenance override interlock *)

    (* ================================================================================================= *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) FUEL SALT CORE TEMPERATURE SENSORS [deg C]                      *)
    (* ================================================================================================= *)
    rSaltCoreTemp_A_degC            : REAL;     (* Fast reactor fuel salt core temperature Channel A [deg C] *)
    rSaltCoreTemp_B_degC            : REAL;     (* Fast reactor fuel salt core temperature Channel B [deg C] *)
    rSaltCoreTemp_C_degC            : REAL;     (* Fast reactor fuel salt core temperature Channel C [deg C] *)
    rBypassLoopTemp_degC            : REAL;     (* Pyrochemical redox bypass loop entrance temperature [deg C] *)

    (* ================================================================================================= *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) ONLINE REDOX POTENTIOMETRY SENSORS [mV]                          *)
    (* ================================================================================================= *)
    rRedoxPotential_A_mV            : REAL;     (* Electrochemical cell potential vs Ni/NiF2 ref Channel A [mV] *)
    rRedoxPotential_B_mV            : REAL;     (* Electrochemical cell potential vs Ni/NiF2 ref Channel B [mV] *)
    rRedoxPotential_C_mV            : REAL;     (* Electrochemical cell potential vs Ni/NiF2 ref Channel C [mV] *)
    rRedoxRatioTarget_mol_mol       : REAL;     (* Desired U4+/U3+ molar redox equilibrium setpoint [mol/mol] *)

    (* ================================================================================================= *)
    (* COVER GAS & SPARGER CARRIER GAS SUPPLY PRESSURES [bar]                                            *)
    (* ================================================================================================= *)
    rCoverGasPressure_bar           : REAL;     (* Core plenum helium blanket static cover gas pressure [bar] *)
    rSpargerInletPress_A_bar        : REAL;     (* Reduction sparger header manifold supply pressure A [bar] *)
    rSpargerInletPress_B_bar        : REAL;     (* Reduction sparger header manifold supply pressure B [bar] *)
    rCycloneOutletPress_bar         : REAL;     (* Centrifugal bubble separator discharge salt pressure [bar] *)

    (* ================================================================================================= *)
    (* GAS MASS FLOW CONTROLLER (MFC) PROCESS FEEDBACK SIGNALS [sccm]                                    *)
    (* ================================================================================================= *)
    rH2SpargerFlowFeedback_sccm     : REAL;     (* Active hydrogen reductant gas mass flow rate feedback [sccm] *)
    rHeStrippingFlowFeedback_sccm   : REAL;     (* Fission gas stripping helium bubble injection rate [sccm] *)
    rHePurgeBlanketFlow_sccm        : REAL;     (* Auxiliary seal housing inert helium sweep gas flow [sccm] *)

    (* ================================================================================================= *)
    (* OFF-GAS RADIOCHEMICAL INVENTORIES & FISSION GAS DETECTION [Bq/m3]                                 *)
    (* ================================================================================================= *)
    rOffGasXe135Activity_A_Bq_m3    : REAL;     (* Separator off-gas duct Xe-135 gamma activity Channel A [Bq/m3] *)
    rOffGasXe135Activity_B_Bq_m3    : REAL;     (* Separator off-gas duct Xe-135 gamma activity Channel B [Bq/m3] *)
    rOffGasXe135Activity_C_Bq_m3    : REAL;     (* Separator off-gas duct Xe-135 gamma activity Channel C [Bq/m3] *)
    rOffGasKr88Activity_Bq_m3       : REAL;     (* Separator off-gas duct Kr-88 gamma activity Channel [Bq/m3] *)

    (* ================================================================================================= *)
    (* HASTELLOY-N BOUNDARY MICROSTRAIN & STRUCTURAL INTEGRITY [microstrain]                             *)
    (* ================================================================================================= *)
    rVesselWallMicrostrain_CH1      : REAL;     (* High-temperature fiber-optic vessel hoop microstrain 1 [microstrain] *)
    rVesselWallMicrostrain_CH2      : REAL;     (* High-temperature fiber-optic vessel hoop microstrain 2 [microstrain] *)

    (* ================================================================================================= *)
    (* ELECTRICAL HEATING LOAD & AUXILIARY POWER [kW]                                                    *)
    (* ================================================================================================= *)
    rTraceHeatingPower_kW           : REAL;     (* Bypass salt line inductive/resistive heating power [kW] *)
    rCycloneMotorPower_kW           : REAL;     (* Centrifugal separator vortex booster electrical power [kW] *)

    (* ================================================================================================= *)
    (* ADDITIONAL PROCESS & HYDRODYNAMIC PROCESS INPUTS                                                  *)
    (* ================================================================================================= *)
    rSaltBypassMassFlow_kg_s        : REAL;     (* Pyrochemical bypass salt mass flow rate [kg/s] *)
    rSaltBypassVolFlow_m3_h         : REAL;     (* Pyrochemical bypass salt volumetric flow rate [m3/h] *)
    rTotalOffGasFlow_Nm3_h          : REAL;     (* Normalized volumetric off-gas flow to charcoal beds [Nm3/h] *)
    rEIS_SolutionResistance_Ohm     : REAL;     (* High-frequency bulk fluoride salt solution resistance Rs [Ohm] *)
    rEIS_PolarizationResist_Ohm     : REAL;     (* Low-frequency alloy corrosion polarization resistance Rp [Ohm] *)
    rEIS_DoubleLayerCap_uF          : REAL;     (* High-temperature electrochemical double layer capacitance [uF] *)
    rDissolvedChromium_ppm          : REAL;     (* Chemical leached chromium impurity concentration in salt [ppm] *)
    rSaltVoidFractionSensor_pct     : REAL;     (* Ultrasonic/impedance core inlet gas void fraction [%] *)
    rBeRodPositionFeedback_mm       : REAL;     (* Metallic beryllium immersion rod actual encoder position [mm] *)
END_VAR

VAR_OUTPUT
    (* ================================================================================================= *)
    (* PRIMARY PYROCHEMICAL & HYDRODYNAMIC ACTUATOR COMMANDS                                             *)
    (* ================================================================================================= *)
    rBeRodPositionCmd_mm            : REAL;     (* Metallic beryllium rod linear immersion command [mm] *)
    rH2MassFlowCmd_sccm             : REAL;     (* Reductant hydrogen mass flow controller setpoint [sccm] *)
    rHeStrippingFlowCmd_sccm        : REAL;     (* Helium bubble stripping mass flow controller setpoint [sccm] *)
    rCycloneThrottleCmd_pct         : REAL;     (* Centrifugal separator vortex gas extraction throttle [%] *)
    rTraceHeatingTarget_kW          : REAL;     (* Closed-loop trace heating electrical power command [kW] *)

    (* ================================================================================================= *)
    (* ESTIMATED PROCESS STATES & PHYSICAL THERMODYNAMIC VARIABLES                                       *)
    (* ================================================================================================= *)
    rCalculatedU4U3Ratio            : REAL;     (* Online electrochemical Nernstian U4+/U3+ molar ratio [mol/mol] *)
    rCorrosionRate_um_yr            : REAL;     (* Hastelloy-N structural alloy estimated corrosion rate [um/yr] *)
    rCalculatedVoidFraction_pct     : REAL;     (* Downstream salt loop entrained gas void fraction [%] *)
    rXeExtractionEfficiency_pct     : REAL;     (* Online Xe-135 noble gas bubble extraction efficiency [%] *)
    rVotedRedoxPotential_mV         : REAL;     (* Triple modular redundancy 2oo3 voted cell potential [mV] *)
    rVotedSaltCoreTemp_degC         : REAL;     (* Triple modular redundancy 2oo3 voted core temperature [deg C] *)

    (* ================================================================================================= *)
    (* SYSTEM SAFETY INTERLOCKS & OPERATIONAL PERMISSIVES                                                *)
    (* ================================================================================================= *)
    bSystemReady                    : BOOL;     (* Subsystem operational readiness and closed-loop permissive *)
    bEmergencyTripActive            : BOOL;     (* Hardwired SIL-3 functional safety trip asserted *)
    bBeRodFastEjectionActive        : BOOL;     (* Beryllium rod pneumatic safety retraction actively fired *)
    bH2SupplyIsolated               : BOOL;     (* Redundant fast-acting hydrogen supply isolation valves closed *)
    bDegradedModeActive             : BOOL;     (* System running under degraded sensor/actuator fault tolerance *)

    (* ================================================================================================= *)
    (* DETERMINISTIC 32-BIT BIT-PACKED STATUS & ALARM WORDS                                              *)
    (* ================================================================================================= *)
    dwSystemStatusWord              : DWORD;    (* Comprehensive 32-bit cyber-physical operational status *)
    dwWarningWord                   : DWORD;    (* Diagnostic warning status word (minor faults, sensor drift) *)
    dwCriticalAlarmWord             : DWORD;    (* SIL-3 Critical plant protection trip and interlock word *)
    dwFSMStateWord                  : DWORD;    (* Multi-stage finite state machine current execution state word *)
END_VAR

VAR
    (* ================================================================================================= *)
    (* INTERNAL PHYSICAL & CHEMICAL THERMODYNAMIC CONSTANTS                                              *)
    (* ================================================================================================= *)
    R_GAS_CONST                     : REAL := 8.314462;     (* Universal Ideal Gas Constant [J/(mol*K)] *)
    FARADAY_CONST                   : REAL := 96485.332;    (* Faraday Electrochemical Constant [C/mol] *)
    PI_CONST                        : REAL := 3.14159265;   (* Archimedes mathematical constant Pi *)
    STEFAN_BOLTZ                    : REAL := 5.670374e-8;  (* Stefan-Boltzmann radiation constant [W/(m2*K4)] *)
    STANDARD_TEMP_K                 : REAL := 273.15;       (* Zero Celsius absolute temperature offset [K] *)
    NOMINAL_CORE_TEMP_K             : REAL := 923.15;       (* MSFR nominal 650°C fuel salt temperature [K] *)
    
    (* Molten Salt Matrix & Electrochemical Reference Parameters *)
    E0_REF_POTENTIAL_V              : REAL := -1.4250;      (* U4+/U3+ standard reduction potential vs Ni/NiF2 at 650°C [V] *)
    D_E0_DT_COEFF                   : REAL := 0.000350;     (* Temperature coefficient of standard potential dE0/dT [V/K] *)
    ACTIVITY_COEFF_RATIO            : REAL := 1.0250;       (* Activity coefficient ratio gamma_UF4 / gamma_UF3 in LiF-ThF4 *)
    STERN_GEARY_B_VOLT              : REAL := 0.02162;      (* Stern-Geary constant B = (beta_a * beta_c)/(2.303*(beta_a+beta_c)) [V] *)
    HASTELLOY_EQUIV_WEIGHT          : REAL := 28.520;       (* Effective electrochemical equivalent weight of Hastelloy-N [g/eq] *)
    HASTELLOY_DENSITY_G_CM3         : REAL := 8.860;        (* Density of Hastelloy-N structural alloy [g/cm3] *)
    HENRY_CONST_XE_MOL_M3_PA        : REAL := 1.650e-8;     (* Henry's law solubility constant of Xenon in LiF-ThF4 at 650°C *)
    DIFFUSIVITY_XE_SALT_M2_S        : REAL := 3.850e-9;     (* Molecular diffusion coefficient of Xe in molten fluoride [m2/s] *)
    DIFFUSIVITY_BE_SALT_M2_S        : REAL := 5.200e-9;     (* Molecular diffusion coefficient of Be in molten fluoride [m2/s] *)
    BE_ROD_DIAMETER_M               : REAL := 0.02540;      (* Metallic beryllium immersion rod outer diameter (1 inch) [m] *)
    BE_ROD_MAX_STROKE_MM            : REAL := 250.0;        (* Maximum mechanical immersion stroke of Beryllium rod drive [mm] *)
    SAUTER_BUBBLE_DIAM_M            : REAL := 0.00085;      (* Sauter mean bubble diameter d32 of helium stripping bubbles [m] *)
    CYCLONE_RADIUS_M                : REAL := 0.0750;       (* Centrifugal bubble separator barrel inner radius [m] *)

    (* ================================================================================================= *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) VOTING & SENSOR HEALTH VARIABLES                                 *)
    (* ================================================================================================= *)
    rPot_Diff_AB                    : REAL := 0.0;
    rPot_Diff_BC                    : REAL := 0.0;
    rPot_Diff_CA                    : REAL := 0.0;
    rTemp_Diff_AB                   : REAL := 0.0;
    rTemp_Diff_BC                   : REAL := 0.0;
    rTemp_Diff_CA                   : REAL := 0.0;
    rPress_Diff_AB                  : REAL := 0.0;
    rXe_Diff_AB                     : REAL := 0.0;
    rXe_Diff_BC                     : REAL := 0.0;
    rXe_Diff_CA                     : REAL := 0.0;
    
    bPot_Healthy_A                  : BOOL := TRUE;
    bPot_Healthy_B                  : BOOL := TRUE;
    bPot_Healthy_C                  : BOOL := TRUE;
    bTemp_Healthy_A                 : BOOL := TRUE;
    bTemp_Healthy_B                 : BOOL := TRUE;
    bTemp_Healthy_C                 : BOOL := TRUE;
    bPress_Healthy_A                : BOOL := TRUE;
    bPress_Healthy_B                : BOOL := TRUE;
    bXe_Healthy_A                   : BOOL := TRUE;
    bXe_Healthy_B                   : BOOL := TRUE;
    bXe_Healthy_C                   : BOOL := TRUE;
    
    iPot_Healthy_Count              : INT := 3;
    iTemp_Healthy_Count             : INT := 3;
    iXe_Healthy_Count               : INT := 3;
    
    rVotedSpargerPress_bar          : REAL := 2.50;
    rVotedXe135Activity_Bq_m3       : REAL := 0.0;

    (* ================================================================================================= *)
    (* DIGITAL FILTERS, EXPONENTIAL SMOOTHERS & MOVING ACCUMULATORS                                      *)
    (* ================================================================================================= *)
    rFiltRedoxPotential_mV          : REAL := -380.0;
    rFiltSaltCoreTemp_degC          : REAL := 650.0;
    rFiltVesselMicrostrain          : REAL := 450.0;
    rFiltVoidFraction_pct           : REAL := 0.025;
    rFiltOffGasXe_Bq_m3             : REAL := 0.0;
    rFiltCorrosionRate_um_yr        : REAL := 4.50;
    
    alpha_RedoxFilter               : REAL := 0.1250;
    alpha_TempFilter                : REAL := 0.0800;
    alpha_StrainFilter              : REAL := 0.0500;
    alpha_VoidFilter                : REAL := 0.2000;
    alpha_XeFilter                  : REAL := 0.1000;
    alpha_CorrosionFilter           : REAL := 0.0500;

    (* History buffer for rate-of-change (derivative) tracking *)
    rHistRedox_1                    : REAL := -380.0;
    rHistRedox_2                    : REAL := -380.0;
    rHistRedox_3                    : REAL := -380.0;
    rRedoxRateOfChange_mV_s         : REAL := 0.0;

    (* ================================================================================================= *)
    (* MULTIVARIABLE 6-STATE STATE-SPACE MATRICES & EMBEDDED REAL-TIME MPC ENGINE                       *)
    (*   x[k+1] = A * x[k] + B * u[k]                                                                    *)
    (*   y[k]   = C * x[k] + D * u[k]                                                                    *)
    (*   min J  = (x - x_ref)^T * Q * (x - x_ref) + (u - u_ref)^T * R * (u - u_ref) + du^T * S * du      *)
    (* ================================================================================================= *)
    bMatricesInitialized            : BOOL := FALSE;
    A_mat                           : ARRAY[1..6, 1..6] OF REAL;
    B_mat                           : ARRAY[1..6, 1..4] OF REAL;
    C_mat                           : ARRAY[1..4, 1..6] OF REAL;
    D_mat                           : ARRAY[1..4, 1..4] OF REAL;
    
    Q_diag                          : ARRAY[1..6] OF REAL;
    R_diag                          : ARRAY[1..4] OF REAL;
    S_diag                          : ARRAY[1..4] OF REAL;
    
    x_state                         : ARRAY[1..6] OF REAL;
    x_ref                           : ARRAY[1..6] OF REAL;
    x_pred                          : ARRAY[1..6] OF REAL;
    x_error                         : ARRAY[1..6] OF REAL;
    
    u_ctrl                          : ARRAY[1..4] OF REAL;
    u_ref                           : ARRAY[1..4] OF REAL;
    u_prev                          : ARRAY[1..4] OF REAL;
    delta_u                         : ARRAY[1..4] OF REAL;
    
    u_min                           : ARRAY[1..4] OF REAL;
    u_max                           : ARRAY[1..4] OF REAL;
    delta_u_max                     : ARRAY[1..4] OF REAL;
    
    grad_J                          : ARRAY[1..4] OF REAL;
    inv_Hessian_diag                : ARRAY[1..4] OF REAL;
    
    iMPC_Iter                       : INT := 0;
    iRow                            : INT := 1;
    iCol                            : INT := 1;
    rTempSum                        : REAL := 0.0;

    (* ================================================================================================= *)
    (* FINITE STATE MACHINE (FSM) GOVERNOR & FUNCTIONAL TIMER INSTANCES                                  *)
    (* ================================================================================================= *)
    iState                          : INT := 0;
    iPreviousState                  : INT := -1;
    bStateFirstScan                 : BOOL := TRUE;
    
    tStateTimer                     : TON;
    tPreheatDwellTimer              : TON;
    tCalibrationDwellTimer          : TON;
    tInertPurgeDwellTimer           : TON;
    tBaselineAcqTimer               : TON;
    tScramDebounceTimer             : TON;
    tWatchdogHeartbeatTimer         : TON;
    
    tSampleTaskInterval_s           : REAL := 0.200;    (* 200 ms task execution period (5 Hz) *)
    rTotalOperatingHours            : REAL := 0.0;
    rCumulativeBerylliumBurn_grams  : REAL := 0.0;
    rCumulativeOffGasVolume_Nm3     : REAL := 0.0;

    (* Internal Safety Flags *)
    bHardwareTripCondition          : BOOL := FALSE;
    bThermalFreezeHazard            : BOOL := FALSE;
    bOverTemperatureHazard          : BOOL := FALSE;
    bOxidizingRunawayHazard         : BOOL := FALSE;
    bReducingPrecipitationHazard    : BOOL := FALSE;
    bGasVoidReactivityHazard        : BOOL := FALSE;
    bVesselRuptureStrainHazard      : BOOL := FALSE;
    bContainmentBreachHazard        : BOOL := FALSE;
    bCorrosionRateExceededHazard    : BOOL := FALSE;

    (* Real-Time Computational & Hydrodynamic Evaluation Registers *)
    rT_Kelvin                       : REAL := 923.15;
    rE0_T_Volt                      : REAL := -1.4250;
    rNernstSlope_V                  : REAL := 0.07955;
    rDelta_E_Volt                   : REAL := 0.0;
    rLnRatio                        : REAL := 4.605;
    rRedoxError                     : REAL := 0.0;
    
    rRe_rod                         : REAL := 1250.0;
    rSc_Be                          : REAL := 289.0;
    rSh_rod                         : REAL := 48.50;
    rk_L_Be                         : REAL := 9.93e-6;
    rMassFlux_Be                    : REAL := 0.0;
    rBeImmersionTarget_mm           : REAL := 0.0;
    
    ra_sparge                       : REAL := 176.5;
    rk_L_H2                         : REAL := 1.45e-4;
    rFlux_H2                        : REAL := 0.0;
    rH2FlowTarget_sccm              : REAL := 0.0;
    
    rk_L_Xe                         : REAL := 8.20e-5;
    ra_bubble                       : REAL := 211.8;
    rXeRemovalRate                  : REAL := 0.0;
    rCentrifugalG                   : REAL := 85.0;
    rSepEfficiency                  : REAL := 0.985;
    rGasVoidCalculated              : REAL := 0.025;
    
    rSternGeary_B                   : REAL := 0.02162;
    rI_corr_A_cm2                   : REAL := 4.5e-7;
    rI_corr_uA_cm2                  : REAL := 0.45;
    rCorrosionRate_calc             : REAL := 4.50;
    rCreepStrainRate                : REAL := 0.0;
    
    rGradNorm                       : REAL := 0.0;
    rCost_k                         : REAL := 0.0;
    rDeltaCost                      : REAL := 0.0;
    iGradIter                       : INT := 0;
    rStepSize                       : REAL := 0.050;
    
    rWorkVal1                       : REAL := 0.0;
    rWorkVal2                       : REAL := 0.0;
    rWorkVal3                       : REAL := 0.0;
    rWorkVal4                       : REAL := 0.0;
END_VAR
"""

if __name__ == "__main__":
    s = get_sec2_vars()
    print("Section 2 Length:", len(s))
