# Generator part 3: VAR ... END_VAR
def get_vars():
    return """VAR
    (* ========================================================================================= *)
    (* INTERNAL CYBER-PHYSICAL STATE REGISTERS, VECTORS, MATRICES & CONTROL MEMORY              *)
    (* ========================================================================================= *)
    bFirstScanDone                  : BOOL := FALSE;    (* Deterministic cold-start memory allocation flag *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 1. SAG MILL MECHANICAL GEOMETRY, INERTIA & HYDRAULIC LIFT CALIBRATION CONSTANTS           *)
    (* ----------------------------------------------------------------------------------------- *)
    rMillInsideDiameter_m           : REAL := 12.192;   (* 40.0 ft internal diameter inside new Cr-Mo shell liners [m] *)
    rMillEffectiveLength_m          : REAL := 7.620;    (* 25.0 ft effective grinding length between head liners [m] *)
    rMillInternalVolume_m3          : REAL := 889.65;   (* Total cylindrical internal volume inside shell liners [m3] *)
    rMillCriticalSpeed_RPM          : REAL := 12.112;   (* Theoretical critical centrifuging rotational speed [RPM] *)
    rMillShellTareMass_tons         : REAL := 640.00;   (* Structural deadweight of shell, trunnions, and liners [tons] *)
    rNominalBallChargeMass_tons     : REAL := 240.00;   (* 15.0% volumetric filling of 125mm forged alloy steel balls [tons] *)
    rMaxAllowableTotalWeight_tons   : REAL := 1550.00;  (* Structural and trunnion hydraulic bearing design limit [tons] *)

    (* Trunnion Hydrostatic Bearing Jacking Pad Effective Areas & Hydraulic Pressure Calibration *)
    rTrunnionInletPadArea_m2        : REAL := 0.4150;   (* High-pressure hydraulic lift pad effective area inlet [m2] *)
    rTrunnionOutletPadArea_m2       : REAL := 0.4450;   (* High-pressure hydraulic lift pad effective area outlet [m2] *)
    rHydraulicLiftForceFactor_Inlet : REAL := 4.2304;   (* Tons lift per bar oil pressure on inlet bearing [tons/bar] *)
    rHydraulicLiftForceFactor_Outlet: REAL := 4.5362;   (* Tons lift per bar oil pressure on outlet bearing [tons/bar] *)
    rTrunnionHydraulicTareOffset_tons:REAL := 148.50;   (* Hydrodynamic wedge bias correction at rated speed [tons] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 2. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) DISCREPANCY LIMITS, FILTERS & FAULT REGISTERS    *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Discrepancy Tolerances Across Channels *)
    rTol_TrunnionPress_bar          : REAL := 1.80;     (* Max permissible deviation between trunnion pressure sensors [bar] *)
    rTol_AcousticEar_Pct            : REAL := 4.00;     (* Max permissible deviation between acoustic ear sensors [%] *)
    rTol_SumpLevel_Pct              : REAL := 3.50;     (* Max permissible deviation between sump level transmitters [%] *)
    rTol_SlurryDensity_SG           : REAL := 0.025;    (* Max permissible deviation between nuclear density gauges [SG] *)
    rTol_ManifoldPress_kPa          : REAL := 5.00;     (* Max permissible deviation between manifold pressure sensors [kPa] *)
    rTol_RingMotorRPM               : REAL := 0.080;    (* Max permissible deviation between motor tachometers [RPM] *)
    rTol_RingMotorPower_MW          : REAL := 0.350;    (* Max permissible deviation between motor power meters [MW] *)
    rTol_FeedConveyor_tph           : REAL := 35.00;    (* Max permissible deviation between feed weightometers [t/h] *)

    (* Voted Sensor Values for Process Computation *)
    rVoted_InletTrunnionPress_bar   : REAL := 168.5;
    rVoted_OutletTrunnionPress_bar  : REAL := 174.2;
    rVoted_AcousticToe_Pct          : REAL := 24.5;
    rVoted_AcousticShoulder_Pct     : REAL := 78.2;
    rVoted_SumpLevel_Pct            : REAL := 58.5;
    rVoted_SlurryDensity_SG         : REAL := 1.540;
    rVoted_ManifoldPress_kPa        : REAL := 92.5;
    rVoted_RingMotorRPM             : REAL := 9.15;
    rVoted_RingMotorPower_MW        : REAL := 23.45;
    rVoted_FreshFeedRate_tph        : REAL := 2850.0;

    (* Historical Memory Registers for Frozen/Stuck Sensor Detection *)
    rPrev_PT_Inlet_A   : REAL := 168.5; rPrev_PT_Inlet_B   : REAL := 168.5; rPrev_PT_Inlet_C   : REAL := 168.5;
    rPrev_PT_Outlet_A  : REAL := 174.2; rPrev_PT_Outlet_B  : REAL := 174.2; rPrev_PT_Outlet_C  : REAL := 174.2;
    rPrev_AIT_Toe_A    : REAL := 24.5;  rPrev_AIT_Toe_B    : REAL := 24.5;  rPrev_AIT_Toe_C    : REAL := 24.5;
    rPrev_AIT_Shldr_A  : REAL := 78.2;  rPrev_AIT_Shldr_B  : REAL := 78.2;  rPrev_AIT_Shldr_C  : REAL := 78.2;
    rPrev_LT_Sump_A    : REAL := 58.5;  rPrev_LT_Sump_B    : REAL := 58.5;  rPrev_LT_Sump_C    : REAL := 58.5;
    rPrev_DT_Dens_A    : REAL := 1.540; rPrev_DT_Dens_B    : REAL := 1.540; rPrev_DT_Dens_C    : REAL := 1.540;
    rPrev_PT_Manif_A   : REAL := 92.5;  rPrev_PT_Manif_B   : REAL := 92.5;  rPrev_PT_Manif_C   : REAL := 92.5;
    rPrev_ST_RPM_A     : REAL := 9.15;  rPrev_ST_RPM_B     : REAL := 9.15;  rPrev_ST_RPM_C     : REAL := 9.15;
    rPrev_IT_MW_A      : REAL := 23.45; rPrev_IT_MW_B      : REAL := 23.45; rPrev_IT_MW_C      : REAL := 23.45;
    rPrev_WT_Feed_A    : REAL := 2850.0;rPrev_WT_Feed_B    : REAL := 2850.0;rPrev_WT_Feed_C    : REAL := 2850.0;

    (* Stuck Channel Counters (Number of Scans with Identical Floating Value) *)
    iStuck_PT_Inlet_A   : INT := 0; iStuck_PT_Inlet_B   : INT := 0; iStuck_PT_Inlet_C   : INT := 0;
    iStuck_PT_Outlet_A  : INT := 0; iStuck_PT_Outlet_B  : INT := 0; iStuck_PT_Outlet_C  : INT := 0;
    iStuck_AIT_Toe_A    : INT := 0; iStuck_AIT_Toe_B    : INT := 0; iStuck_AIT_Toe_C    : INT := 0;
    iStuck_AIT_Shldr_A  : INT := 0; iStuck_AIT_Shldr_B  : INT := 0; iStuck_AIT_Shldr_C  : INT := 0;
    iStuck_LT_Sump_A    : INT := 0; iStuck_LT_Sump_B    : INT := 0; iStuck_LT_Sump_C    : INT := 0;
    iStuck_DT_Dens_A    : INT := 0; iStuck_DT_Dens_B    : INT := 0; iStuck_DT_Dens_C    : INT := 0;
    iStuck_PT_Manif_A   : INT := 0; iStuck_PT_Manif_B   : INT := 0; iStuck_PT_Manif_C   : INT := 0;
    iStuck_ST_RPM_A     : INT := 0; iStuck_ST_RPM_B     : INT := 0; iStuck_ST_RPM_C     : INT := 0;
    iStuck_IT_MW_A      : INT := 0; iStuck_IT_MW_B      : INT := 0; iStuck_IT_MW_C      : INT := 0;
    iStuck_WT_Feed_A    : INT := 0; iStuck_WT_Feed_B    : INT := 0; iStuck_WT_Feed_C    : INT := 0;

    (* Channel Health Indicators *)
    bHealth_PT_Inlet_A  : BOOL := TRUE; bHealth_PT_Inlet_B  : BOOL := TRUE; bHealth_PT_Inlet_C  : BOOL := TRUE;
    bHealth_PT_Outlet_A : BOOL := TRUE; bHealth_PT_Outlet_B : BOOL := TRUE; bHealth_PT_Outlet_C : BOOL := TRUE;
    bHealth_AIT_Toe_A   : BOOL := TRUE; bHealth_AIT_Toe_B   : BOOL := TRUE; bHealth_AIT_Toe_C   : BOOL := TRUE;
    bHealth_AIT_Shldr_A : BOOL := TRUE; bHealth_AIT_Shldr_B : BOOL := TRUE; bHealth_AIT_Shldr_C : BOOL := TRUE;
    bHealth_LT_Sump_A   : BOOL := TRUE; bHealth_LT_Sump_B   : BOOL := TRUE; bHealth_LT_Sump_C   : BOOL := TRUE;
    bHealth_DT_Dens_A   : BOOL := TRUE; bHealth_DT_Dens_B   : BOOL := TRUE; bHealth_DT_Dens_C   : BOOL := TRUE;
    bHealth_PT_Manif_A  : BOOL := TRUE; bHealth_PT_Manif_B  : BOOL := TRUE; bHealth_PT_Manif_C  : BOOL := TRUE;
    bHealth_ST_RPM_A    : BOOL := TRUE; bHealth_ST_RPM_B    : BOOL := TRUE; bHealth_ST_RPM_C    : BOOL := TRUE;
    bHealth_IT_MW_A     : BOOL := TRUE; bHealth_IT_MW_B     : BOOL := TRUE; bHealth_IT_MW_C     : BOOL := TRUE;
    bHealth_WT_Feed_A   : BOOL := TRUE; bHealth_WT_Feed_B   : BOOL := TRUE; bHealth_WT_Feed_C   : BOOL := TRUE;

    (* Degraded 1oo2 or 1oo1 Status Indicators *)
    bDegraded_PT_Inlet  : BOOL := FALSE; bDegraded_PT_Outlet : BOOL := FALSE;
    bDegraded_AIT_Toe   : BOOL := FALSE; bDegraded_AIT_Shldr  : BOOL := FALSE;
    bDegraded_LT_Sump   : BOOL := FALSE; bDegraded_DT_Dens    : BOOL := FALSE;
    bDegraded_PT_Manif  : BOOL := FALSE; bDegraded_ST_RPM     : BOOL := FALSE;
    bDegraded_IT_MW     : BOOL := FALSE; bDegraded_WT_Feed    : BOOL := FALSE;

    (* ----------------------------------------------------------------------------------------- *)
    (* 3. DISCRETE 8x8 CYBER-PHYSICAL STATE-SPACE FORMULATION (EVALUATED AT Ts = 0.010 s)        *)
    (* ----------------------------------------------------------------------------------------- *)
    (* State Vector x[0..7]:
         x[0]: Coarse Ore Hold-up Mass Deviation Delta M_ore_coarse [tons] (Nominal: 380.0 t)
         x[1]: Fine Slurry Ore Hold-up Mass Deviation Delta M_ore_fine [tons] (Nominal: 220.0 t)
         x[2]: Slurry Water Hold-up Volume Deviation Delta V_water [m3] (Nominal: 165.0 m3)
         x[3]: Dynamic Grinding Toe Angle Deviation Delta theta_toe [deg] (Nominal: 135.0 deg)
         x[4]: Direct Shell Liner Impact Severity Index Deviation Delta E_impact [%] (Nominal: 25.0%)
         x[5]: Cyclone Feed Sump Slurry Volume Deviation Delta V_sump [m3] (Nominal: 85.0 m3)
         x[6]: Cyclone Feed Slurry Solids Density Deviation Delta rho_sump [SG] (Nominal: 1.540 SG)
         x[7]: Gearless Ring Motor Rotor Speed Slip Deviation Delta omega_m [RPM] (Nominal: 0.0 RPM) *)
    aState_x                    : ARRAY[0..7] OF REAL := [8(0.0)];
    aState_x_hat                : ARRAY[0..7] OF REAL := [8(0.0)];
    aState_x_pred               : ARRAY[0..7] OF REAL := [8(0.0)];

    (* Manipulated Control Vector u[0..5]:
         u[0]: Fresh SAG Ore Feed Rate Demand Deviation Delta W_feed [t/h] (Nominal: 2850.0 t/h)
         u[1]: Mill Feed Chute Dilution Water Flow Deviation Delta Q_water [m3/h] (Nominal: 850.0 m3/h)
         u[2]: Ring Motor Rotational Speed Setpoint Deviation Delta N_mill [RPM] (Nominal: 9.15 RPM)
         u[3]: Cyclone Feed Slurry Pump Speed Deviation Delta N_pump [RPM] (Nominal: 520.0 RPM)
         u[4]: Cyclone Sump Dilution Trim Water Valve Stroke Delta V_water_sump [%] (Nominal: 38.0%)
         u[5]: Target Active Operating Cyclone Count Deviation Delta N_cyc [count] (Nominal: 9) *)
    aControl_u                  : ARRAY[0..5] OF REAL := [2850.0, 850.0, 9.15, 520.0, 38.0, 9.0];
    aControl_u_prev             : ARRAY[0..5] OF REAL := [2850.0, 850.0, 9.15, 520.0, 38.0, 9.0];
    aControl_du                 : ARRAY[0..5] OF REAL := [6(0.0)];
    aControl_u_base             : ARRAY[0..5] OF REAL := [2850.0, 850.0, 9.15, 520.0, 38.0, 9.0];

    (* Disturbance Vector d[0..2]:
         d[0]: Ore Hardness / Drop Weight A*b Resistance Index Deviation Delta (A*b) [-]
         d[1]: Pebble Crusher Recycle Return Feed Rate Surge Delta W_pebble [t/h] (Nominal: 280.0 t/h)
         d[2]: Fresh Ore Top Size F80 Granulometry Deviation Delta F80 [mm] (Nominal: 125.0 mm) *)
    aDisturb_d                  : ARRAY[0..2] OF REAL := [3(0.0)];

    (* Output Process Measurement Vector y[0..7]:
         y[0]: Total Mill Live Mass [tons]
         y[1]: Internal Slurry Volume [m3]
         y[2]: Dynamic Grinding Toe Position [deg]
         y[3]: Direct Shell Liner Impact Severity Index [%]
         y[4]: Cyclone Feed Sump Level [%]
         y[5]: Cyclone Feed Slurry Density [SG]
         y[6]: Cyclone Feed Manifold Pressure [kPa]
         y[7]: Ring Motor Active Electrical Power [MW] *)
    aOutput_y                   : ARRAY[0..7] OF REAL := [1320.5, 245.0, 135.2, 24.5, 58.5, 1.540, 92.5, 23.45];
    aOutput_y_sp                : ARRAY[0..7] OF REAL := [1320.5, 245.0, 135.0, 22.0, 58.0, 1.540, 92.0, 23.50];
    aOutput_y_error             : ARRAY[0..7] OF REAL := [8(0.0)];

    (* Continuous-to-Discrete State Matrix A (8x8) at Ts = 0.010 s *)
    aMatrix_A                   : ARRAY[0..7, 0..7] OF REAL;
    (* Input Coupling Matrix B (8x6) *)
    aMatrix_B                   : ARRAY[0..7, 0..5] OF REAL;
    (* Output Mapping Matrix C (8x8) *)
    aMatrix_C                   : ARRAY[0..7, 0..7] OF REAL;
    (* Direct Feedthrough Matrix D (8x6) *)
    aMatrix_D                   : ARRAY[0..7, 0..5] OF REAL;
    (* Disturbance Coupling Matrix E (8x3) *)
    aMatrix_E                   : ARRAY[0..7, 0..2] OF REAL;
    (* Kalman Observer Innovation Gain Matrix K_obs (8x8) *)
    aMatrix_K_obs               : ARRAY[0..7, 0..7] OF REAL;

    (* ----------------------------------------------------------------------------------------- *)
    (* 4. MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST MATRICES & QP CONSTRAINTS                *)
    (* ----------------------------------------------------------------------------------------- *)
    (* State Tracking Cost Penalty Matrix Q (8x8 Diagonal) *)
    aWeight_Q                   : ARRAY[0..7] OF REAL := [0.850, 0.650, 1.200, 2.400, 8.500, 1.100, 4.500, 1.800];
    (* Actuator Expenditure Penalty Matrix R (6x6 Diagonal) *)
    aWeight_R                   : ARRAY[0..5] OF REAL := [0.045, 0.035, 0.250, 0.080, 0.020, 0.150];
    (* Actuator Slew Rate Rate-of-Change Penalty Matrix S (6x6 Diagonal) *)
    aWeight_S                   : ARRAY[0..5] OF REAL := [0.350, 0.220, 1.850, 0.450, 0.120, 0.850];
    (* Terminal Riccati Cost Matrix P (8x8 Symmetric Full Solution) *)
    aMatrix_P                   : ARRAY[0..7, 0..7] OF REAL;

    (* Actuator Envelope Physical Saturation Limits *)
    aLimit_u_Max                : ARRAY[0..5] OF REAL := [3600.0, 1500.0, 10.20, 750.0, 100.0, 12.0];
    aLimit_u_Min                : ARRAY[0..5] OF REAL := [0.0,    0.0,    6.50,  300.0, 0.0,   6.0];
    (* Actuator Dynamic Slew Rate Limits per 10 ms execution cycle *)
    aLimit_du_Max               : ARRAY[0..5] OF REAL := [0.800,  0.450,  0.002, 0.250, 0.200, 0.020];
    aLimit_du_Min               : ARRAY[0..5] OF REAL := [-0.800, -0.450, -0.002,-0.250,-0.200,-0.020];

    (* Projected Gradient Descent Numerical Optimizer Workspace *)
    aGrad_g                     : ARRAY[0..5] OF REAL := [6(0.0)];
    aStep_du                    : ARRAY[0..5] OF REAL := [6(0.0)];
    aHessian_diag               : ARRAY[0..5] OF REAL := [6(0.0)];
    iIterQP                     : INT := 0;
    iMaxIterQP                  : INT := 8;         (* Active QP iterations per 10 ms task scan *)
    rAlphaStep                  : REAL := 0.0285;   (* Gradient step learning rate parameter *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 5. AUSTIN-HERBST COMMINUTION BREAKAGE KINETICS & ERGUN SLURRY RHEOLOGY REGISTERS          *)
    (* ----------------------------------------------------------------------------------------- *)
    rAustin_SpecificBreakage_S0 : REAL := 0.485;    (* Base specific breakage rate S0 [1/s] *)
    rAustin_Alpha_Power         : REAL := 0.950;    (* Breakage rate power index alpha [-] *)
    rAustin_Lambda_Decay        : REAL := 1.250;    (* Critical size breakage rate decay index Lambda [-] *)
    rAustin_CriticalSize_dcrit_m: REAL := 0.065;    (* Critical particle top size for peak breakage [m] *)
    rAustin_Phi_FinesFraction   : REAL := 0.320;    (* Primary breakage distribution fine split phi [-] *)
    rAustin_Gamma_Distribution  : REAL := 0.850;    (* Cumulative breakage distribution slope gamma [-] *)
    rAustin_Beta_Distribution   : REAL := 4.200;    (* Breakage distribution truncation exponent beta [-] *)

    (* Slurry Rheology & Pulp Lifter Hydraulic Hold-up Constants *)
    rSolidSpecificGravity_Ore   : REAL := 2.850;    (* Dry mineral ore particle density [g/cm3] *)
    rWaterSpecificGravity       : REAL := 1.000;    (* Process water fluid density [g/cm3] *)
    rGrateDischargeArea_m2      : REAL := 1.850;    (* Total open slot area of discharge grate pulp lifters [m2] *)
    rGrateDischargeCoeff        : REAL := 0.620;    (* Hydraulic orifice flow discharge coefficient Cd [-] *)
    rPulpLifterEfficiency_eta   : REAL := 0.885;    (* Pulp lifter slurry scoop carry-over efficiency [-] *)
    rSlurryViscosity_Pa_s       : REAL := 0.045;    (* Apparent dynamic slurry viscosity inside mill charge [Pa*s] *)
    rYieldStress_Bingham_Pa     : REAL := 8.500;    (* Bingham plastic yield stress of high-density slurry [Pa] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 6. PLITT HYDROCYCLONE BATTERY CLASSIFICATION GEOMETRY & HYDRAULIC PARAMETERS              *)
    (* ----------------------------------------------------------------------------------------- *)
    rPlitt_CycloneDiameter_Dc_m : REAL := 0.650;    (* Hydrocyclone internal barrel diameter Dc [m] *)
    rPlitt_InletDiameter_Di_m   : REAL := 0.160;    (* Hydrocyclone feed inlet nozzle diameter Di [m] *)
    rPlitt_VortexFinder_Do_m    : REAL := 0.220;    (* Hydrocyclone vortex finder overflow diameter Do [m] *)
    rPlitt_ApexDiameter_Du_m    : REAL := 0.125;    (* Hydrocyclone spigot apex underflow diameter Du [m] *)
    rPlitt_FreeVortexHeight_h_m : REAL := 1.450;    (* Hydrocyclone cylinder-cone transition height h [m] *)
    rPlitt_SharpnessIndex_m     : REAL := 2.850;    (* Plitt classification sharpness of separation m [-] *)
    rPlitt_WaterSplit_Rw        : REAL := 0.385;    (* Fractional recovery of feed water to underflow Rw [-] *)
    rPlitt_VolumetricSolids_Cv  : REAL := 0.345;    (* Feed slurry volumetric solids fraction Cv [-] *)
    rTargetManifoldPress_Min_kPa: REAL := 75.0;     (* Minimum operating manifold pressure to prevent collapse [kPa] *)
    rTargetManifoldPress_Max_kPa: REAL := 110.0;    (* Maximum operating manifold pressure to prevent roping [kPa] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 7. GEARLESS RING MOTOR ELECTROMECHANICAL DRIVE & DIRECT TORQUE MODEL                      *)
    (* ----------------------------------------------------------------------------------------- *)
    rMillTotalInertia_J_kgm2    : REAL := 4.850E6;  (* Total rotational polar moment of inertia [kg*m2] *)
    rMotorNominalTorque_kNm     : REAL := 26500.0;  (* Continuous motor torque capability at rated current [kNm] *)
    rMotorPeakTorqueLimit_kNm   : REAL := 31500.0;  (* Absolute transient thermal peak torque limit [kNm] *)
    rMotorElectromechanicalPoleP: INT := 34;        (* Stator pole pairs for 68-pole synchronous ring motor *)
    rMotorBaseFrequency_Hz      : REAL := 5.185;    (* Fundamental stator excitation frequency at 9.15 RPM [Hz] *)
    rTorsionalDamping_B_Nms     : REAL := 18500.0;  (* Hydrodynamic charge cascading viscous damping [N*m*s/rad] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 8. FINITE STATE MACHINE (12 INDUSTRIAL STATES) & TRANSITION TIMERS                        *)
    (* ----------------------------------------------------------------------------------------- *)
    iMachineState               : INT := 0;         (* Active execution state *)
    iPreviousState              : INT := 0;         (* Historical state tracker *)
    rStateTimer_s               : REAL := 0.0;      (* Monotonic elapsed state timer [s] *)
    rLubeWarmupTimer_s          : REAL := 0.0;      (* Hydraulic jacking lift oil warm-up timer [s] *)
    rInchingAlignmentTimer_s    : REAL := 0.0;      (* Inching drive mechanical alignment timer [s] *)
    rMotorAccelRampTimer_s      : REAL := 0.0;      (* Ring motor synchronous acceleration ramp timer [s] *)
    rWaterFlushTimer_s          : REAL := 0.0;      (* Mill feed water flush startup timer [s] *)
    rHomogenizationTimer_s      : REAL := 0.0;      (* Low-feed charge bedding homogenization timer [s] *)
    rImpactMitigationTimer_s    : REAL := 0.0;      (* High-energy acoustic impact mitigation hold timer [s] *)
    rCycloneReconfigTimer_s     : REAL := 0.0;      (* Knife-gate valve staging transition timer [s] *)
    rSumpSurgeTimer_s           : REAL := 0.0;      (* Sump surge damping and decoupling timer [s] *)
    rGrindOutTimer_s            : REAL := 0.0;      (* Controlled grind-out ore depletion timer [s] *)
    rCradleParkTimer_s          : REAL := 0.0;      (* Mill cradle parking brake engagement timer [s] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 9. ISA-18.2 MULTI-TIERED ALARM SETPOINTS, HYSTERESIS DEADBANDS & DEBOUNCE TIMERS          *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Total Mill Weight Trip & Warning Limits [tons] *)
    rWeightTrip_HH_tons         : REAL := 1550.0;   (* HI_HI: Slurry spill / overfill emergency fast trip [tons] *)
    rWeightWarn_H_tons          : REAL := 1450.0;   (* HI: High mill load warning / feed reduction trim [tons] *)
    rWeightWarn_L_tons          : REAL := 1050.0;   (* LO: Low mill load warning / steel liner impact alert [tons] *)
    rWeightTrip_LL_tons         : REAL := 900.0;    (* LO_LO: Empty mill runout danger trip [tons] *)
    rWeightDeadband_tons        : REAL := 10.0;     (* ISA-18.2 hysteresis deadband [tons] *)

    (* Acoustic Ear Direct Shell Liner Impact Severity Limits [%] *)
    rImpactTrip_HH_Pct          : REAL := 70.0;     (* HI_HI: Catastrophic liner cracking hazard emergency trim [%] *)
    rImpactWarn_H_Pct           : REAL := 55.0;     (* HI: Elevated shell liner impact warning [%] *)
    rImpactDeadband_Pct         : REAL := 2.0;      (* ISA-18.2 hysteresis deadband [%] *)

    (* Cyclone Feed Sump Slurry Level Limits [%] *)
    rSumpTrip_HH_Pct            : REAL := 92.0;     (* HI_HI: Sump overflow environmental containment trip [%] *)
    rSumpWarn_H_Pct             : REAL := 80.0;     (* HI: High sump surge alert [%] *)
    rSumpWarn_L_Pct             : REAL := 30.0;     (* LO: Low sump level warning [%] *)
    rSumpTrip_LL_Pct            : REAL := 18.0;     (* LO_LO: Pump cavitation & air ingestion trip [%] *)
    rSumpDeadband_Pct           : REAL := 2.0;      (* ISA-18.2 hysteresis deadband [%] *)

    (* Cyclone Feed Slurry Density Limits [SG] *)
    rDensityTrip_HH_SG          : REAL := 1.720;    (* HI_HI: Cyclone roping & pluggage imminent trip [SG] *)
    rDensityWarn_H_SG           : REAL := 1.620;    (* HI: High slurry density alert [SG] *)
    rDensityWarn_L_SG           : REAL := 1.420;    (* LO: Low slurry density / water diluting warning [SG] *)
    rDensityTrip_LL_SG          : REAL := 1.320;    (* LO_LO: Extreme slurry under-density wash-out trip [SG] *)
    rDensityDeadband_SG         : REAL := 0.015;    (* ISA-18.2 hysteresis deadband [SG] *)

    (* Cyclone Feed Manifold Pressure Limits [kPa] *)
    rManifoldTrip_HH_kPa        : REAL := 135.0;    (* HI_HI: Cyclone battery over-pressure safety trip [kPa] *)
    rManifoldWarn_H_kPa         : REAL := 115.0;    (* HI: High classification cut pressure warning [kPa] *)
    rManifoldWarn_L_kPa         : REAL := 65.0;     (* LO: Low cut pressure / vortex collapse warning [kPa] *)
    rManifoldTrip_LL_kPa        : REAL := 45.0;     (* LO_LO: Severe cyclone starvation / air ingestion [kPa] *)
    rManifoldDeadband_kPa       : REAL := 3.0;      (* ISA-18.2 hysteresis deadband [kPa] *)

    (* Ring Motor Active Electrical Power Limits [MW] *)
    rPowerTrip_HH_MW            : REAL := 27.50;    (* HI_HI: Ring motor inverter electrical overload trip [MW] *)
    rPowerWarn_H_MW             : REAL := 26.20;    (* HI: Motor continuous thermal warning [MW] *)
    rPowerDeadband_MW           : REAL := 0.30;     (* ISA-18.2 hysteresis deadband [MW] *)

    (* Alarm Debounce Timers [s] *)
    rDebounce_WeightHH_s        : REAL := 0.0;
    rDebounce_ImpactHH_s        : REAL := 0.0;
    rDebounce_SumpLL_s          : REAL := 0.0;
    rDebounce_ManifoldHH_s      : REAL := 0.0;
    rDebounce_PowerHH_s         : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 10. GENERAL ITERATION INDICES, TEMPORARY SUMS & MATHEMATICAL REGISTERS                    *)
    (* ----------------------------------------------------------------------------------------- *)
    iIdx                        : INT := 0;         (* Outer loop counter *)
    jIdx                        : INT := 0;         (* Inner loop counter *)
    kIdx                        : INT := 0;         (* Matrix multiplication accumulator index *)
    iCycloneIdx                 : INT := 0;         (* Cyclone valve sequencing index *)
    rTmpSum                     : REAL := 0.0;      (* Scalar floating-point accumulator *)
    rTmpVal                     : REAL := 0.0;      (* Temporary scalar register *)
    rDelta                      : REAL := 0.0;      (* Discrepancy temporary delta *)
    rMaxDiscrepancy             : REAL := 0.0;      (* Peak discrepancy among sensor triplet *)
    rSlurryDensity_kgm3         : REAL := 1540.0;   (* Cyclone feed slurry density in metric units [kg/m3] *)
    rTotalFeedRate_tph          : REAL := 3130.0;   (* Fresh feed + pebble recycle sum [t/h] *)
    rSolidsVolumetricFlow_m3h   : REAL := 1098.2;   (* Dry ore volumetric flow rate [m3/h] *)
    rWaterVolumetricFlow_m3h    : REAL := 2351.8;   (* Liquid water volumetric flow rate [m3/h] *)
    rCalculatedGrateDischarge_m3h:REAL := 3450.0;   (* Estimated discharge pulp lifter capacity [m3/h] *)
    rAcousticDirectImpactRaw    : REAL := 24.5;     (* Raw calculated acoustic ratio *)
    rDynamicToeEstimated_deg    : REAL := 135.2;    (* Charge toe angle estimate *)
    rDynamicShoulderEstimated_deg:REAL := 315.8;    (* Charge shoulder angle estimate *)
END_VAR
"""

print("Vars module loaded.")
