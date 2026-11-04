# part2_var.py

def get_part2_var():
    return """VAR
    (* -----------------------------------------------------------------------------------------------------------------
     * 1. SYSTEM TIMING, PHYSICAL PARAMETERS & CYBER-PHYSICAL CONSTANTS
     * ----------------------------------------------------------------------------------------------------------------- *)
    c_rTs                               : REAL := 0.050;        (* Discrete Execution Cycle Period 50.0 ms [s] *)
    c_rGasConstant_R                    : REAL := 8.31446;      (* Universal Ideal Gas Constant [J/(mol*K)] *)
    c_rFurnaceVolume_m3                 : REAL := 2850.0;       (* Primary Combustion Chamber Net Enclosure Volume [m3] *)
    c_rPostCombZoneVolume_m3            : REAL := 920.0;        (* Post-Combustion Secondary Air to Boiler Radiant Entrance [m3] *)
    c_rGrateTotalActiveArea_m2          : REAL := 145.0;        (* Total 4-Zone Moving Grate Active Surface Area [m2] *)
    c_rNominalFlueGasSpecificVol_Nm3_kg : REAL := 4.85;         (* Flue Gas Volume Produced per kg Wet Raw MSW [Nm3/kg] *)
    c_rMolarMass_NO_kgkmol              : REAL := 30.006;       (* Nitric Oxide Molar Mass [kg/kmol] *)
    c_rMolarMass_NO2_kgkmol             : REAL := 46.005;       (* Nitrogen Dioxide Molar Mass [kg/kmol] *)
    c_rMolarMass_NH3_kgkmol             : REAL := 17.031;       (* Ammonia Molecular Weight [kg/kmol] *)
    c_rMolarMass_Urea_kgkmol            : REAL := 60.056;       (* Aqueous Urea Solute Molecular Weight [kg/kmol] *)
    c_rMolarMass_SO2_kgkmol             : REAL := 64.066;       (* Sulfur Dioxide Molecular Weight [kg/kmol] *)
    c_rMolarMass_HCl_kgkmol             : REAL := 36.461;       (* Hydrogen Chloride Molecular Weight [kg/kmol] *)
    c_rMolarMass_CaOH2_kgkmol           : REAL := 74.093;       (* Slaked Lime Calcium Hydroxide Molecular Weight [kg/kmol] *)

    (* -----------------------------------------------------------------------------------------------------------------
     * 2. 8x8 MULTIVARIABLE DISCRETE STATE-SPACE CYBER-PHYSICAL ENGINE ARRAYS
     * -----------------------------------------------------------------------------------------------------------------
     * State Vector x[1..8]:
     *   x[1]: Bed Moisture Evaporation Deficit Delta X_moist [%]
     *   x[2]: Pyrolysis & Char Bed Core Temperature Delta T_bed [deg C]
     *   x[3]: Primary Combustion Chamber Gas Temperature Delta T_comb [deg C]
     *   x[4]: Post-Combustion 2-Second Temperature Delta T_post [deg C]
     *   x[5]: Boiler Superheated Steam Evaporation Deviation Delta m_steam [t/h]
     *   x[6]: Raw First-Pass Flue Gas NOx Concentration Delta C_NOx [mg/Nm3]
     *   x[7]: Semi-Dry Absorber Acid Gas (SO2 + HCl) Equivalent Concentration Delta C_acid [mg/Nm3]
     *   x[8]: Semi-Dry Absorber Droplet Evaporative Neutralization Efficiency Delta eta_scrub [%]
     * Control Vector u[1..8]:
     *   u[1]: Grate Zone 1 Drying Stroke Speed Trim [strokes/h]
     *   u[2]: Grate Zone 2/3 Combustion Stroke Speed Trim [strokes/h]
     *   u[3]: Grate Zone 4 Char Burnout Stroke Speed Trim [strokes/h]
     *   u[4]: Primary Air Flow Trim [Nm3/h]
     *   u[5]: Secondary Air Flow Trim [Nm3/h]
     *   u[6]: SNCR Urea Injection Solution Mass Flow Trim [kg/h]
     *   u[7]: Semi-Dry Absorber Lime Slurry Feed Flow Trim [kg/h]
     *   u[8]: Powdered Activated Carbon Pneumatic Dosing Trim [kg/h]
     * ----------------------------------------------------------------------------------------------------------------- *)
    bStateSpaceInitialized              : BOOL := FALSE;        (* First-Scan State-Space Matrices Loaded Latch *)
    aA                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Matrix A (8x8) *)
    aB                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete Input Coupling Matrix B (8x8) *)
    aC                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete Output Measurement Matrix C (8x8) *)
    aD                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete Direct Feedthrough Matrix D (8x8) *)
    ax_state                            : ARRAY[1..8] OF REAL;  (* Current Cyber-Physical Estimated State Vector *)
    ax_next                             : ARRAY[1..8] OF REAL;  (* Next Predicted State Vector x[k+1] *)
    ax_ref                              : ARRAY[1..8] OF REAL;  (* State Target Equilibrium Reference Vector *)
    au_control                          : ARRAY[1..8] OF REAL;  (* Optimal Control Actuator Input Vector u[k] *)
    au_prev                             : ARRAY[1..8] OF REAL;  (* Previous Scan Actuator Input Vector u[k-1] *)
    au_delta                            : ARRAY[1..8] OF REAL;  (* Actuator Slew Rate Vector Delta_u[k] = u[k] - u[k-1] *)
    ay_output                           : ARRAY[1..8] OF REAL;  (* Simulated Sensor Output Measurement Vector *)

    (* -----------------------------------------------------------------------------------------------------------------
     * 3. MODEL PREDICTIVE CONTROL (MPC) RECEDING-HORIZON COST FUNCTION ARRAYS
     * ----------------------------------------------------------------------------------------------------------------- *)
    aWeightQ                            : ARRAY[1..8] OF REAL;  (* State Error Penalty Diagonal Diag(Q) *)
    aWeightR                            : ARRAY[1..8] OF REAL;  (* Actuator Effort Penalty Diagonal Diag(R) *)
    aWeightS                            : ARRAY[1..8] OF REAL;  (* Actuator Rate-of-Change Slew Penalty Diag(S) *)
    aWeightP                            : ARRAY[1..8] OF REAL;  (* Terminal Prediction State Cost Diag(P) *)
    au_min                              : ARRAY[1..8] OF REAL;  (* Hard Lower Actuator Dynamic Bounds *)
    au_max                              : ARRAY[1..8] OF REAL;  (* Hard Upper Actuator Dynamic Bounds *)
    adelta_u_max                        : ARRAY[1..8] OF REAL;  (* Slew Rate Bounds per 50 ms Execution Cycle *)
    aGrad_u                             : ARRAY[1..8] OF REAL;  (* Analytical Cost Gradient dJ/du *)
    aPredictedState                     : ARRAY[1..8] OF REAL;  (* 1-Step Horizon State Extrapolation *)
    c_rPGD_Alpha                        : REAL := 0.00035;      (* Projected Gradient Descent Optimization Step Size *)

    (* -----------------------------------------------------------------------------------------------------------------
     * 4. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINE & DIAGNOSTIC REGISTERS
     * ----------------------------------------------------------------------------------------------------------------- *)
    c_rTMR_PersistencyTimeout_s         : REAL := 0.050;        (* Fault Qualification Persistence Filter (50 ms) [s] *)
    
    (* Discrepancy Tolerance Limits *)
    c_rTol_CombustionTemp_degC          : REAL := 20.0;         (* Max Permissible Difference on Flame Core Triplet [deg C] *)
    c_rTol_PostCombTemp_degC            : REAL := 15.0;         (* 2-Second Acoustic Temperature Discrepancy Tol [deg C] *)
    c_rTol_GrateStroke_strokes_h        : REAL := 2.50;         (* Stoker Stroke Speed Discrepancy Tolerance [strokes/h] *)
    c_rTol_PrimaryAir_Nm3h              : REAL := 650.0;        (* Primary Underfire Air Flow Tol [Nm3/h] *)
    c_rTol_SecondaryAir_Nm3h            : REAL := 450.0;        (* Secondary Overfire Air Flow Tol [Nm3/h] *)
    c_rTol_NOx_mgNm3                    : REAL := 5.00;         (* Raw Boiler Inlet NOx Discrepancy Tol [mg/Nm3] *)
    c_rTol_StackNOx_mgNm3               : REAL := 3.00;         (* CEMS Stack Clean NOx Discrepancy Tol [mg/Nm3] *)
    c_rTol_StackNH3_mgNm3               : REAL := 0.25;         (* TDLAS Ammonia Slip Discrepancy Tol [mg/Nm3] *)
    c_rTol_UreaFlow_kgh                 : REAL := 4.50;         (* Aqueous Urea Injection Flow Tol [kg/h] *)
    c_rTol_AbsorberHCl_mgNm3            : REAL := 12.0;         (* Absorber Inlet Raw HCl Discrepancy Tol [mg/Nm3] *)
    c_rTol_AbsorberSO2_mgNm3            : REAL := 3.00;         (* Absorber Inlet Raw SO2 Discrepancy Tol [mg/Nm3] *)
    c_rTol_LimeSlurryFlow_kgh           : REAL := 7.50;         (* Ca(OH)2 Slurry Feed Flow Tol [kg/h] *)
    c_rTol_PACFlow_kgh                  : REAL := 1.20;         (* PAC Dosing Mass Flow Tol [kg/h] *)
    c_rTol_SuperheaterAcoustic_mm       : REAL := 0.10;         (* Superheater Tube Acoustic Thickness Tol [mm] *)
    c_rTol_FurnaceDraft_mbar            : REAL := 0.20;         (* Furnace Draft Negative Pressure Tol [mbar] *)
    c_rTol_SteamFlow_th                 : REAL := 1.20;         (* Main Boiler Steam Evaporation Tol [t/h] *)
    c_rTol_StackO2_pct                  : REAL := 0.20;         (* Stack Residual Oxygen Discrepancy Tol [vol%] *)

    (* Discrepancy Timers for 18 Banks *)
    rTimer_TMR_CombTemp_s               : REAL := 0.0;
    rTimer_TMR_PostCombTemp_s           : REAL := 0.0;
    rTimer_TMR_Zone1Stroke_s            : REAL := 0.0;
    rTimer_TMR_Zone4Stroke_s            : REAL := 0.0;
    rTimer_TMR_PrimAir_s                : REAL := 0.0;
    rTimer_TMR_SecAir_s                 : REAL := 0.0;
    rTimer_TMR_RawNOx_s                 : REAL := 0.0;
    rTimer_TMR_StackNOx_s               : REAL := 0.0;
    rTimer_TMR_StackNH3_s               : REAL := 0.0;
    rTimer_TMR_UreaFlow_s               : REAL := 0.0;
    rTimer_TMR_RawHCl_s                 : REAL := 0.0;
    rTimer_TMR_RawSO2_s                 : REAL := 0.0;
    rTimer_TMR_LimeFlow_s               : REAL := 0.0;
    rTimer_TMR_PACFlow_s                : REAL := 0.0;
    rTimer_TMR_Superheater_s            : REAL := 0.0;
    rTimer_TMR_Draft_s                  : REAL := 0.0;
    rTimer_TMR_SteamFlow_s              : REAL := 0.0;
    rTimer_TMR_StackO2_s                : REAL := 0.0;

    (* Channel Isolation Flags *)
    bIso_CombTemp_A, bIso_CombTemp_B, bIso_CombTemp_C : BOOL := FALSE;
    bIso_PostComb_A, bIso_PostComb_B, bIso_PostComb_C : BOOL := FALSE;
    bIso_Zone1_A, bIso_Zone1_B, bIso_Zone1_C : BOOL := FALSE;
    bIso_Zone4_A, bIso_Zone4_B, bIso_Zone4_C : BOOL := FALSE;
    bIso_PrimAir_A, bIso_PrimAir_B, bIso_PrimAir_C : BOOL := FALSE;
    bIso_SecAir_A, bIso_SecAir_B, bIso_SecAir_C : BOOL := FALSE;
    bIso_RawNOx_A, bIso_RawNOx_B, bIso_RawNOx_C : BOOL := FALSE;
    bIso_StackNOx_A, bIso_StackNOx_B, bIso_StackNOx_C : BOOL := FALSE;
    bIso_StackNH3_A, bIso_StackNH3_B, bIso_StackNH3_C : BOOL := FALSE;
    bIso_UreaFlow_A, bIso_UreaFlow_B, bIso_UreaFlow_C : BOOL := FALSE;
    bIso_RawHCl_A, bIso_RawHCl_B, bIso_RawHCl_C : BOOL := FALSE;
    bIso_RawSO2_A, bIso_RawSO2_B, bIso_RawSO2_C : BOOL := FALSE;
    bIso_LimeFlow_A, bIso_LimeFlow_B, bIso_LimeFlow_C : BOOL := FALSE;
    bIso_PACFlow_A, bIso_PACFlow_B, bIso_PACFlow_C : BOOL := FALSE;
    bIso_Superheater_A, bIso_Superheater_B, bIso_Superheater_C : BOOL := FALSE;
    bIso_Draft_A, bIso_Draft_B, bIso_Draft_C : BOOL := FALSE;
    bIso_Steam_A, bIso_Steam_B, bIso_Steam_C : BOOL := FALSE;
    bIso_StackO2_A, bIso_StackO2_B, bIso_StackO2_C : BOOL := FALSE;

    (* Stuck Sensor Detection Previous History and Counters *)
    rPrev_PostCombTemp_A                : REAL := 965.0;
    rPrev_PostCombTemp_B                : REAL := 965.0;
    rPrev_PostCombTemp_C                : REAL := 965.0;
    iStuckCount_PostComb_A              : INT := 0;
    iStuckCount_PostComb_B              : INT := 0;
    iStuckCount_PostComb_C              : INT := 0;

    rPrev_StackNOx_A                    : REAL := 64.0;
    rPrev_StackNOx_B                    : REAL := 64.0;
    rPrev_StackNOx_C                    : REAL := 64.0;
    iStuckCount_StackNOx_A              : INT := 0;
    iStuckCount_StackNOx_B              : INT := 0;
    iStuckCount_StackNOx_C              : INT := 0;

    (* -----------------------------------------------------------------------------------------------------------------
     * 5. THERMODYNAMIC, KINETIC & MASS TRANSFER REACTION PARAMETERS
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Bed Combustion & Heat Release *)
    rSolidWasteMassFlow_kgh             : REAL := 62500.0;      (* Total MSW Incineration Rate 1,500 t/d = 62.5 t/h [kg/h] *)
    rNetThermalHeatRelease_MW           : REAL := 170.14;       (* Thermal Input Power = (Mass * LHV) / 3600 [MW] *)
    rCalculatedFlueGasFlow_Nm3h         : REAL := 125000.0;     (* Wet Raw Flue Gas Production Rate [Nm3/h] *)
    rFlueGasMeanVelocity_ms             : REAL := 4.25;         (* Flue Gas Velocity in Post-Combustion Duct [m/s] *)
    rResidenceTimeCalculated_s          : REAL := 2.45;         (* Aerodynamic Physical Residence Time (>= 2.0 s) [s] *)

    (* Arrhenius Thermal NOx & Fuel NOx Kinetic Parameters *)
    c_rZeldovich_Ea                     : REAL := 318000.0;     (* Zeldovich Mechanism Activation Energy [J/mol] *)
    c_rZeldovich_k0                     : REAL := 1.85E14;      (* Pre-Exponential Kinetic Factor [1/(s*(mol/m3)^0.5)] *)
    c_rFuelNitrogenWeightFraction       : REAL := 0.0085;       (* Fuel Nitrogen Fraction in Dry MSW (0.85 wt%) *)
    c_rFuelNitrogenConversionRatio      : REAL := 0.165;        (* Fractional Conversion of Bound Fuel N into NOx *)
    rArrheniusReactionRate_NOx          : REAL := 0.0;          (* Instantaneous Thermal NOx Formation Rate [mg/(Nm3*s)] *)
    rPredictedRawInletNOx_mgNm3         : REAL := 385.0;        (* Calculated Baseline First-Pass NOx Inlet [mg/Nm3] *)

    (* SNCR Urea Temperature Selectivity Window (850 °C to 1,050 °C) *)
    c_rSNCR_OptimumTemp_degC            : REAL := 965.0;        (* Peak Selective DeNOx Temperature [deg C] *)
    c_rSNCR_WindowHalfWidth_degC        : REAL := 75.0;         (* Gaussian Kinetic Selectivity Half-Width [deg C] *)
    c_rUreaStoichiometricRatio_NSR      : REAL := 1.45;         (* Normalized Stoichiometric Ratio (Moles NH2 / Moles NOx) *)
    rTempSelectivityFactor              : REAL := 0.0;          (* Normalized Temperature Kinetic Selectivity [0..1] *)
    rPredictedDeNOxConversion_pct       : REAL := 0.0;          (* Calculated SNCR Reduction Yield [%] *)
    rPredictedNH3Slip_mgNm3             : REAL := 0.0;          (* Modeled Unreacted Ammonia Slip [mg/Nm3] *)

    (* Semi-Dry Spray Absorber Droplet Mass Transfer & Acid Neutralization *)
    c_rStoich_CaOH2_HCl                 : REAL := 1.05;         (* Slaked Lime to HCl Over-Stoichiometry Ratio *)
    c_rStoich_CaOH2_SO2                 : REAL := 1.35;         (* Slaked Lime to SO2 Over-Stoichiometry Ratio *)
    rSlurryDropletSauterMeanDiam_um     : REAL := 42.0;         (* Rotary Atomizer Droplet SMD d32 [um] *)
    rDropletEvaporationTime_s           : REAL := 0.85;         (* Slurry Droplet Liquid Film Evaporation Time [s] *)
    rAbsorberApproachToSaturation_degC  : REAL := 18.5;         (* Temperature Margin Above Dew Point [deg C] *)
    rPredictedHClNeutralization_pct     : REAL := 99.2;         (* High-Efficiency HCl Absorption Yield [%] *)
    rPredictedSO2Neutralization_pct     : REAL := 92.5;         (* High-Efficiency SO2 Absorption Yield [%] *)

    (* Powdered Activated Carbon (PAC) Dioxin & Mercury Adsorption *)
    c_rPAC_DioxinCapacity_ug_g          : REAL := 185.0;        (* Adsorption Equilibrium Capacity PCDD/PCDF [ug/g] *)
    c_rPAC_MercuryCapacity_mg_g         : REAL := 12.5;         (* Adsorption Equilibrium Capacity Gaseous Hg [mg/g] *)
    rPAC_SpecificDosing_mg_Nm3          : REAL := 260.0;        (* Paced Pneumatic PAC Injection Concentration [mg/Nm3] *)

    (* Boiler Superheater Chlorine Eutectic Corrosion Observer *)
    c_rCorrosionBaseRate_um_h           : REAL := 0.038;        (* Baseline Tube Thinning at 420 °C Steam [um/h] *)
    c_rCorrosionChlorineEa              : REAL := 88500.0;      (* Activation Energy for FeCl2 Volatilization [J/mol] *)
    rInstantaneousCorrosionRate_um_h    : REAL := 0.0;          (* Real-Time Wall Metal Loss Rate [um/h] *)
    rAccumulatedTubeLoss_um             : REAL := 0.0;          (* Integrated Cumulative Metal Loss [um] *)

    (* -----------------------------------------------------------------------------------------------------------------
     * 6. HYDRAULIC STOKER JAM DETECTION & FAST REVERSE CLEARANCE SUBROUTINE
     * ----------------------------------------------------------------------------------------------------------------- *)
    c_rGrateHydraulicJamPressure_bar    : REAL := 205.0;        (* High-Pressure Threshold Indicating Mechanical Jam [bar] *)
    c_rGrateReverseStrokeTime_s         : REAL := 12.0;         (* Reverse Motion Duration to Clear Foreign Objects [s] *)
    rGrateReverseTimer_Zone1_s          : REAL := 0.0;
    rGrateReverseTimer_Zone2_s          : REAL := 0.0;
    rGrateReverseTimer_Zone3_s          : REAL := 0.0;
    rGrateReverseTimer_Zone4_s          : REAL := 0.0;
    iGrateJamRetryCount_Zone1           : INT := 0;
    iGrateJamRetryCount_Zone2           : INT := 0;
    iGrateJamRetryCount_Zone3           : INT := 0;
    iGrateJamRetryCount_Zone4           : INT := 0;
    bGrateInReverse_Zone1               : BOOL := FALSE;
    bGrateInReverse_Zone2               : BOOL := FALSE;
    bGrateInReverse_Zone3               : BOOL := FALSE;
    bGrateInReverse_Zone4               : BOOL := FALSE;

    (* -----------------------------------------------------------------------------------------------------------------
     * 7. MULTI-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) TIMERS & MEMORY
     * ----------------------------------------------------------------------------------------------------------------- *)
    iFSM_State                          : INT := 1;             (* Active FSM State: 1..12 *)
    iFSM_PrevState                      : INT := 1;             (* Previous FSM State *)
    rStateTimer_s                       : REAL := 0.0;          (* Continuous Active State Dwell Accumulator [s] *)
    bStateEntry                         : BOOL := TRUE;         (* Single-Cycle Pulse on State Transition *)
    rPreheatRampTimer_s                 : REAL := 0.0;          (* Aux Burner Refractory Soak Timer [s] *)
    rFeedChutePrimeTimer_s              : REAL := 0.0;          (* Chute MSW Sealing & Ram Feeding Timer [s] *)
    rBedIgnitionDwellTimer_s            : REAL := 0.0;          (* Bed Combustion Layer Stabilization Timer [s] *)
    rControlledShutdownTimer_s          : REAL := 0.0;          (* Grate Burnout Cool-Down Sequence Timer [s] *)
    rEmergencySafeStopTimer_s           : REAL := 0.0;          (* Emergency Feed Cut Smoke Evacuation Timer [s] *)

    (* -----------------------------------------------------------------------------------------------------------------
     * 8. ISA-18.2 MULTI-TIERED PROCESS ALARM LADDER & LEGAL BREACH REGISTERS
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Alarm Threshold Constants *)
    c_rTrip_PostCombTemp_LO_LO          : REAL := 850.0;        (* Statutory EU Directive 2010/75/EU Floor [deg C] *)
    c_rWarn_PostCombTemp_LO             : REAL := 875.0;        (* Aux Burner Early Intervention Setpoint [deg C] *)
    c_rWarn_PostCombTemp_HI             : REAL := 1050.0;       (* High Temperature Refractory Warning [deg C] *)
    c_rTrip_PostCombTemp_HI_HI          : REAL := 1120.0;       (* Refractory Slagging Redline Trip [deg C] *)

    c_rTrip_StackNOx_HI_HI              : REAL := 80.00;        (* Legal Maximum Statutory NOx Emission Limit [mg/Nm3] *)
    c_rWarn_StackNOx_HI                 : REAL := 72.00;        (* DeNOx High Warning Escalation Setpoint [mg/Nm3] *)
    c_rTrip_StackNH3_HI_HI              : REAL := 3.00;         (* Legal Maximum Ammonia Slip Limit [mg/Nm3] *)
    c_rWarn_StackNH3_HI                 : REAL := 2.50;         (* Ammonia Slip Advisory Setpoint [mg/Nm3] *)
    c_rTrip_StackSO2_HI_HI              : REAL := 50.00;        (* Legal Maximum SO2 Emission Limit [mg/Nm3] *)
    c_rWarn_StackSO2_HI                 : REAL := 38.00;        (* Absorber SO2 Warning Escalation [mg/Nm3] *)
    c_rTrip_StackHCl_HI_HI              : REAL := 10.00;        (* Legal Maximum HCl Emission Limit [mg/Nm3] *)
    c_rWarn_StackHCl_HI                 : REAL := 8.00;         (* Absorber HCl Warning Escalation [mg/Nm3] *)

    c_rTrip_FurnaceDraft_HI_HI          : REAL := 1.50;         (* Positive Pressure Blowout Risk Trip [mbar] *)
    c_rWarn_FurnaceDraft_HI             : REAL := 0.20;         (* High Draft Warning [mbar] *)
    c_rWarn_FurnaceDraft_LO             : REAL := -4.50;        (* Low Draft Negative Pressure Warning [mbar] *)
    c_rTrip_FurnaceDraft_LO_LO          : REAL := -8.50;        (* Severe Implosion Negative Pressure Trip [mbar] *)

    c_rTrip_SuperheaterWall_LO_LO       : REAL := 2.80;         (* Critical Minimum Wall Thickness Tube Rupture [mm] *)
    c_rWarn_SuperheaterWall_LO          : REAL := 3.50;         (* Tube Thinning Maintenance Required [mm] *)

    (* Emission Legal Breach Accumulation Timers (< 1.0 s Latching) *)
    rBreachAccumulator_NOx_s            : REAL := 0.0;
    rBreachAccumulator_SO2_s            : REAL := 0.0;
    rBreachAccumulator_HCl_s            : REAL := 0.0;
    rBreachAccumulator_NH3_s            : REAL := 0.0;
    rBreachAccumulator_Temp_s           : REAL := 0.0;

    (* Prior Values for Rate-of-Change (ROC) Calculation *)
    rPrevROC_CombTemp                   : REAL := 1020.0;
    rPrevROC_PostCombTemp               : REAL := 965.0;
    rPrevROC_StackNOx                   : REAL := 64.0;
    rPrevROC_Draft                      : REAL := -2.50;
    rROC_CombTemp_degCs                 : REAL := 0.0;
    rROC_PostCombTemp_degCs             : REAL := 0.0;
    rROC_StackNOx_mgNm3s                : REAL := 0.0;
    rROC_Draft_mbars                    : REAL := 0.0;

    (* Internal Trip & Warning Latches *)
    bTripLatch_PostComb_LO_LO           : BOOL := FALSE;
    bTripLatch_PostComb_HI_HI           : BOOL := FALSE;
    bTripLatch_StackNOx_HI_HI           : BOOL := FALSE;
    bTripLatch_StackNH3_HI_HI           : BOOL := FALSE;
    bTripLatch_StackSO2_HI_HI           : BOOL := FALSE;
    bTripLatch_StackHCl_HI_HI           : BOOL := FALSE;
    bTripLatch_Draft_HI_HI              : BOOL := FALSE;
    bTripLatch_Draft_LO_LO              : BOOL := FALSE;
    bTripLatch_Superheater_LO_LO        : BOOL := FALSE;
    bTripLatch_GrateJam_Zone1           : BOOL := FALSE;
    bTripLatch_GrateJam_Zone2           : BOOL := FALSE;
    bTripLatch_GrateJam_Zone3           : BOOL := FALSE;
    bTripLatch_GrateJam_Zone4           : BOOL := FALSE;

    bWarnLatch_PostComb_LO              : BOOL := FALSE;
    bWarnLatch_PostComb_HI              : BOOL := FALSE;
    bWarnLatch_StackNOx_HI              : BOOL := FALSE;
    bWarnLatch_StackNH3_HI              : BOOL := FALSE;
    bWarnLatch_StackSO2_HI              : BOOL := FALSE;
    bWarnLatch_StackHCl_HI              : BOOL := FALSE;
    bWarnLatch_Draft_HI                 : BOOL := FALSE;
    bWarnLatch_Draft_LO                 : BOOL := FALSE;
    bWarnLatch_Superheater_LO           : BOOL := FALSE;
    bWarnLatch_TMR_Discrepancy          : BOOL := FALSE;

    (* -----------------------------------------------------------------------------------------------------------------
     * 9. TEMPORARY MATHEMATICAL & ITERATION REGISTERS
     * ----------------------------------------------------------------------------------------------------------------- *)
    iIdx_i                              : INT := 0;
    iIdx_j                              : INT := 0;
    iIdx_k                              : INT := 0;
    rMathTemp_A                         : REAL := 0.0;
    rMathTemp_B                         : REAL := 0.0;
    rMathTemp_C                         : REAL := 0.0;
    rDiff_12                            : REAL := 0.0;
    rDiff_23                            : REAL := 0.0;
    rDiff_13                            : REAL := 0.0;
    bMatch_12                           : BOOL := FALSE;
    bMatch_23                           : BOOL := FALSE;
    bMatch_13                           : BOOL := FALSE;
END_VAR
"""
