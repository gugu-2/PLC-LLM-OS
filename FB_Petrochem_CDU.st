FUNCTION_BLOCK FB_Petrochem_CDU_MultiDraw_PumparoundCascade
(*
========================================================================================================================
  LUMINA PETROCHEMICAL AUTOMATION ARCHITECTURE - V7 MAX-PERSONA CYBER-PHYSICAL SPECIFICATION
  SECTOR         : Chemical & Petrochemical Refining (Tier 1 Priority Sector)
  COMPLEX        : Atmospheric Crude Distillation Unit (CDU) & Multi-Draw Fractionator Complex (350,000 BPSD Capacity)
  SUBSYSTEMS     : 
    1. Atmospheric Crude Distillation Tower (50-Tray Complex Main Fractionator)
    2. 4-Side-Stream Strippers: Heavy Naphtha (HN), Kerosene/Jet-A1, Light Diesel (LDO), Atmospheric Gas Oil (AGO)
    3. Dual Pumparound Circuits: Top Pumparound (TPA, Tray 18->14) & Middle Pumparound (MPA, Tray 30->26)
    4. Two-Stage Electrostatic Desalter with Capacitive Emulsion Interface & Brine Dump Cascade Control
    5. 4-Pass Fired Pipestill Heater with Dynamic Pass Balancing & Two-Phase Flash Vaporization Observer
    6. Overhead Vapor Condenser, Acid Water Dew-Point Corrosion Observer, & Filming/Neutralizing Amine Dosing
    7. Multi-Objective Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD)
    8. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting across 10 Critical Process Transmitters
    9. 12-Stage Deterministic Production Finite State Machine (FSM) from N2 Inerting to Emergency Hot Vapor Depressurization
    10. ISA-18.2 Multi-Tiered Alarm Hierarchy (HH, H, L, LL, ROC) with 32-Bit Bit-Packed Diagnostic Words
========================================================================================================================
  THERMODYNAMIC & REFINERY PROCESS PRINCIPLES:
  - The Atmospheric Distillation Column operates at a top pressure of ~1.35 bar(a) and bottom flash zone pressure ~1.95 bar(a).
  - Preheated crude enters the two-stage electrostatic desalter at 125-145 deg C to remove inorganic salts (NaCl, MgCl2, CaCl2)
    and suspended solids by electrostatic coalescence under high-voltage alternating electric field grids (15-25 kV AC).
  - The desalted crude passes through the second preheat train before entering the fired pipestill heater, reaching a Coil
    Outlet Temperature (COT) of 360 to 372 deg C. Superheated velocity steam is injected into each radiant pass to suppress
    coking and enhance heat transfer.
  - The two-phase crude oil enters the column Flash Zone (Trays 3-4), where 50-60 vol% vaporizes instantaneously. The heavy
    liquid fraction drops to the bottom stripping section, where superheated 10 bar stripping steam strips residual light ends,
    producing Atmospheric Residue (Reduced Crude Oil, RCO / AR).
  - The vapor travels upward through the wash section (Trays 5-6), where an overflash internal liquid reflux (2.5 to 4.5% of
    fresh crude feed) washes entrained asphaltenes, heavy metals (Vanadium, Nickel), and micro-carbon residue out of the
    ascending vapor stream before it enters the Atmospheric Gas Oil (AGO) tray.
  - Four side-stream stripper columns withdraw liquid fractions:
      * Atmospheric Gas Oil (AGO)    : Tray 42 draw -> Steam stripper -> ASTM D86 95% point ~380-400 deg C
      * Light Diesel Oil (LDO)       : Tray 32 draw -> Steam stripper -> ASTM D86 95% point ~355-365 deg C, Cetane Index >= 51
      * Kerosene / Jet-A1           : Tray 22 draw -> Steam stripper -> Freeze Point <= -47 deg C, Flash Point >= 38 deg C
      * Heavy Naphtha (HN)           : Tray 12 draw -> Reboiled stripper -> Initial Boiling Point ~90-110 deg C, RVP <= 0.7 bar
  - Dual Pumparound (PA) heat integration:
      * Top Pumparound (TPA): Extracts liquid from Tray 18, routes through crude preheat exchangers and air trim coolers,
        and returns subcooled liquid to Tray 14.
      * Middle Pumparound (MPA): Extracts liquid from Tray 30, routes through crude preheat exchangers and reboilers,
        and returns subcooled liquid to Tray 26.
      * Pumparounds reduce tower diameter requirements by condensing vapor internally and maximize thermal efficiency by
        transferring high-grade heat into the incoming crude oil feed train, while strictly regulating the tower internal
        liquid-to-vapor (L/V) hydraulic traffic.
  - Overhead Dew-Point Acid Corrosion Neutralization:
      * Hydrolysis of MgCl2 and CaCl2 produces volatile HCl gas that travels overhead with steam.
      * When water vapor reaches its acid dew point (~95-105 deg C), dilute hydrochloric acid condenses, causing catastrophic
        corrosion on air-cooler tube bundles and accumulator boots.
      * The cyber-physical observer calculates the instantaneous thermodynamic dew point, regulates overhead water wash
        injection to dilute acidity, commands neutralizing amine injection (morpholine / methoxypropylamine) via a dedicated
        pH feedback loop (maintaining pH 5.8 - 6.5 in the sour water accumulator boot), and modulates filming polyamine dosing
        proportional to overhead vapor velocity and real-time electrical resistance (ER) corrosion probe data.
========================================================================================================================
*)
VAR_INPUT
    (* Master Execution Permissives & Supervisory Interlocks *)
    bEnable                         : BOOL;     (* Master execution permissive enable flag *)
    bReset                          : BOOL;     (* System trip and alarm latch reset command *)
    bEmergencyTripCmd               : BOOL;     (* Hardwired emergency column depressurization / flare trip ESD command *)
    bAutoMPC_Permissive             : BOOL;     (* Supervisory Model Predictive Control closed-loop auto permissive *)
    bDesalterGridEnergized          : BOOL;     (* High-voltage electrostatic desalter transformer grid energized state *)
    tCycleTime                      : TIME := T#20MS; (* Task scan cycle execution interval [ms] *)

    (* 2oo3 TMR Channel 1: Column Tray Section Differential Pressure (Flood/Weep Detector) *)
    rPDT_ColTrayDP_101A             : REAL;     (* Column Tray Section Differential Pressure Channel A [bar] *)
    rPDT_ColTrayDP_101B             : REAL;     (* Column Tray Section Differential Pressure Channel B [bar] *)
    rPDT_ColTrayDP_101C             : REAL;     (* Column Tray Section Differential Pressure Channel C [bar] *)

    (* 2oo3 TMR Channel 2: Flash Zone Multipoint Pyrometric Temperature *)
    rTT_FlashZoneTemp_102A          : REAL;     (* Flash Zone Multivariable Temperature Channel A [deg C] *)
    rTT_FlashZoneTemp_102B          : REAL;     (* Flash Zone Multivariable Temperature Channel B [deg C] *)
    rTT_FlashZoneTemp_102C          : REAL;     (* Flash Zone Multivariable Temperature Channel C [deg C] *)

    (* 2oo3 TMR Channel 3: Column Overhead Vapor Space Static Pressure *)
    rPT_OverheadPress_103A          : REAL;     (* Column Overhead Vapor Space Static Pressure Channel A [bar] *)
    rPT_OverheadPress_103B          : REAL;     (* Column Overhead Vapor Space Static Pressure Channel B [bar] *)
    rPT_OverheadPress_103C          : REAL;     (* Column Overhead Vapor Space Static Pressure Channel C [bar] *)

    (* 2oo3 TMR Channel 4: Overhead Accumulator Hydrocarbon Liquid Level *)
    rLT_OvhdAccumLevel_104A         : REAL;     (* Overhead Reflux Accumulator HC Liquid Level Channel A [%] *)
    rLT_OvhdAccumLevel_104B         : REAL;     (* Overhead Reflux Accumulator HC Liquid Level Channel B [%] *)
    rLT_OvhdAccumLevel_104C         : REAL;     (* Overhead Reflux Accumulator HC Liquid Level Channel C [%] *)

    (* 2oo3 TMR Channel 5: Column Bottom Residue (RCO) Sump Liquid Level *)
    rLT_BtmResidueLevel_105A        : REAL;     (* Column Bottom Stripping Sump Liquid Level Channel A [%] *)
    rLT_BtmResidueLevel_105B        : REAL;     (* Column Bottom Stripping Sump Liquid Level Channel B [%] *)
    rLT_BtmResidueLevel_105C        : REAL;     (* Column Bottom Stripping Sump Liquid Level Channel C [%] *)

    (* 2oo3 TMR Channel 6: Desalter Brine/Oil Emulsion Interface Level *)
    rLT_DesaltInterface_106A        : REAL;     (* Desalter Capacitive Emulsion Interface Level Channel A [%] *)
    rLT_DesaltInterface_106B        : REAL;     (* Desalter Capacitive Emulsion Interface Level Channel B [%] *)
    rLT_DesaltInterface_106C        : REAL;     (* Desalter Capacitive Emulsion Interface Level Channel C [%] *)

    (* 2oo3 TMR Channel 7: Overhead Condensate Sour Water Boot pH *)
    rAT_SourWaterPH_107A            : REAL;     (* Overhead Accumulator Sour Water Boot pH Channel A [pH] *)
    rAT_SourWaterPH_107B            : REAL;     (* Overhead Accumulator Sour Water Boot pH Channel B [pH] *)
    rAT_SourWaterPH_107C            : REAL;     (* Overhead Accumulator Sour Water Boot pH Channel C [pH] *)

    (* 2oo3 TMR Channel 8: Kerosene Side-Stream Coriolis Mass Flowmeter *)
    rFT_KeroDrawFlow_108A           : REAL;     (* Kerosene Stripper Draw Coriolis Mass Flow Channel A [kg/h] *)
    rFT_KeroDrawFlow_108B           : REAL;     (* Kerosene Stripper Draw Coriolis Mass Flow Channel B [kg/h] *)
    rFT_KeroDrawFlow_108C           : REAL;     (* Kerosene Stripper Draw Coriolis Mass Flow Channel C [kg/h] *)

    (* 2oo3 TMR Channel 9: Light Diesel Side-Stream Coriolis Mass Flowmeter *)
    rFT_DieselDrawFlow_109A         : REAL;     (* Light Diesel Stripper Draw Coriolis Mass Flow Channel A [kg/h] *)
    rFT_DieselDrawFlow_109B         : REAL;     (* Light Diesel Stripper Draw Coriolis Mass Flow Channel B [kg/h] *)
    rFT_DieselDrawFlow_109C         : REAL;     (* Light Diesel Stripper Draw Coriolis Mass Flow Channel C [kg/h] *)

    (* 2oo3 TMR Channel 10: Atmospheric Gas Oil (AGO) Coriolis Mass Flowmeter *)
    rFT_AGODrawFlow_110A            : REAL;     (* Atmospheric Gas Oil Stripper Draw Coriolis Mass Flow Channel A [kg/h] *)
    rFT_AGODrawFlow_110B            : REAL;     (* Atmospheric Gas Oil Stripper Draw Coriolis Mass Flow Channel B [kg/h] *)
    rFT_AGODrawFlow_110C            : REAL;     (* Atmospheric Gas Oil Stripper Draw Coriolis Mass Flow Channel C [kg/h] *)

    (* Auxiliary Refinery Process Telemetry & Stream Sensors *)
    rFT_HeavyNaphthaFlow_111        : REAL;     (* Heavy Naphtha Stripper Product Draw Mass Flow [kg/h] *)
    rFT_CrudeFeedCharge_112         : REAL;     (* Total Crude Feed Volumetric Charge to Preheat Train [m3/h] *)
    rDT_CrudeDensity_113            : REAL;     (* In-Line Coriolis Crude Density at Battery Limit [kg/m3] *)
    rTT_CrudePreheatOutlet_114      : REAL;     (* Desalter Outlet / Fired Heater Inlet Temperature [deg C] *)
    rTT_FurnaceCoilOutlet_115       : REAL;     (* Fired Pipestill Transfer Line Coil Outlet Temperature COT [deg C] *)
    rFT_FurnacePassFlow_1_116       : REAL;     (* Fired Heater Radiant Pass 1 Charge Flow [m3/h] *)
    rFT_FurnacePassFlow_2_117       : REAL;     (* Fired Heater Radiant Pass 2 Charge Flow [m3/h] *)
    rFT_FurnacePassFlow_3_118       : REAL;     (* Fired Heater Radiant Pass 3 Charge Flow [m3/h] *)
    rFT_FurnacePassFlow_4_119       : REAL;     (* Fired Heater Radiant Pass 4 Charge Flow [m3/h] *)
    rFT_OverflashFlow_120           : REAL;     (* Overflash Tray Liquid Gravity Return Internal Flow [m3/h] *)
    rTT_TopPumparoundDraw_121       : REAL;     (* Top Pumparound (TPA) Tray 18 Draw Temperature [deg C] *)
    rTT_TopPumparoundReturn_122     : REAL;     (* Top Pumparound (TPA) Tray 14 Return Temperature [deg C] *)
    rFT_TopPumparoundFlow_123       : REAL;     (* Top Pumparound (TPA) Circulation Volumetric Flow [m3/h] *)
    rTT_MidPumparoundDraw_124       : REAL;     (* Middle Pumparound (MPA) Tray 30 Draw Temperature [deg C] *)
    rTT_MidPumparoundReturn_125     : REAL;     (* Middle Pumparound (MPA) Tray 26 Return Temperature [deg C] *)
    rFT_MidPumparoundFlow_126       : REAL;     (* Middle Pumparound (MPA) Circulation Volumetric Flow [m3/h] *)
    rAT_CorrosionRateProbe_127      : REAL;     (* Overhead Vapor Line Electrical Resistance ER Corrosion Probe [mpy] *)
    rPT_OverheadFlareHeader_128     : REAL;     (* Refinery High-Pressure Flare Knock-Out Header Backpressure [bar] *)
    rTT_OverheadVaporLine_129       : REAL;     (* Column Top Tray Overhead Vapor Transfer Line Temperature [deg C] *)
    rFT_StrippingSteamBottom_130    : REAL;     (* Column Bottom Stripping Superheated Steam Flow [kg/h] *)

    (* Supervisory Setpoints & Optimization Targets *)
    rSP_CrudeThroughputTarget       : REAL;     (* Supervisory Crude Throughput Target [m3/h] *)
    rSP_FurnaceCOTTarget            : REAL;     (* Target Fired Heater Coil Outlet Temperature [deg C] *)
    rSP_OverheadPressTarget         : REAL;     (* Target Column Overhead Operating Pressure [bar] *)
    rSP_SourWaterPHTarget           : REAL;     (* Target Overhead Accumulator Sour Water Boot pH [pH] *)
    rSP_OverflashTargetRatio        : REAL;     (* Target Overflash Reflux Percentage of Fresh Crude Feed [%] *)
    rSP_TPA_DutyTarget_MW           : REAL;     (* Target Top Pumparound Heat Extraction Duty [kW] *)
    rSP_MPA_DutyTarget_MW           : REAL;     (* Target Middle Pumparound Heat Extraction Duty [kW] *)
END_VAR
VAR_OUTPUT
    (* Actuator Control Valve Commands (0.0 to 100.0%) *)
    rCV_OverheadReflux_Cmd          : REAL;     (* Column Top Tray Reflux Flow Control Valve Position [%] *)
    rCV_HeaterFuelGas_Cmd           : REAL;     (* Fired Pipestill Master Fuel Gas Pressure Control Valve [%] *)
    rCV_OverheadOffgas_Cmd          : REAL;     (* Overhead Accumulator Offgas Split-Range Pressure Control Valve [%] *)
    rCV_LightNaphthaRundown_Cmd     : REAL;     (* Net Overhead Light Naphtha Product Rundown Flow Control Valve [%] *)
    rCV_HeavyNaphthaDraw_Cmd        : REAL;     (* Heavy Naphtha Side-Stream Draw Stripper Flow Control Valve [%] *)
    rCV_KeroDraw_Cmd                : REAL;     (* Kerosene/Jet-A1 Side-Stream Draw Stripper Flow Control Valve [%] *)
    rCV_DieselDraw_Cmd              : REAL;     (* Light Diesel Side-Stream Draw Stripper Flow Control Valve [%] *)
    rCV_AGODraw_Cmd                 : REAL;     (* Atmospheric Gas Oil Side-Stream Draw Stripper Flow Control Valve [%] *)
    rCV_TopPumparound_Cmd           : REAL;     (* Top Pumparound Circulation Pump VFD / Return Control Valve [%] *)
    rCV_MidPumparound_Cmd           : REAL;     (* Middle Pumparound Circulation Pump VFD / Return Control Valve [%] *)
    rCV_BottomResidue_Cmd           : REAL;     (* Column Bottom Atmospheric Residue (RCO) Sump Level Control Valve [%] *)
    rCV_DesalterBrine_Cmd           : REAL;     (* Desalter Capacitive Emulsion Interface Brine Dump Valve [%] *)
    rCV_NeutralizingAmine_Cmd       : REAL;     (* Overhead Neutralizing Amine Chemical Metering Pump Stroke [%] *)
    rCV_FilmingAmine_Cmd            : REAL;     (* Overhead Filming Polyamine Corrosion Inhibitor Pump Stroke [%] *)
    rCV_OverheadWaterWash_Cmd       : REAL;     (* Overhead Vapor Acid Dilution Wash Water Injection Valve [%] *)
    rCV_EmergencyDepressFlare_Cmd   : REAL;     (* Emergency Hot Vapor Depressurization Blowdown to Flare Valve [%] *)
    rCV_FurnacePassTrim1_Cmd        : REAL;     (* Fired Pipestill Radiant Pass 1 Flow Trim Actuator [%] *)
    rCV_FurnacePassTrim2_Cmd        : REAL;     (* Fired Pipestill Radiant Pass 2 Flow Trim Actuator [%] *)
    rCV_FurnacePassTrim3_Cmd        : REAL;     (* Fired Pipestill Radiant Pass 3 Flow Trim Actuator [%] *)
    rCV_FurnacePassTrim4_Cmd        : REAL;     (* Fired Pipestill Radiant Pass 4 Flow Trim Actuator [%] *)

    (* Finite State Machine Operational Diagnostics *)
    iCurrentState                   : INT;      (* Active FSM Operational State Number (0..11) *)
    sCurrentStateName               : STRING(40); (* Human-Readable FSM State Name *)
    bEmergencyTripActive            : BOOL;     (* True if Emergency Column Depressurization / Flare ESD Tripped *)
    bMPC_ClosedLoopActive           : BOOL;     (* True if Multivariable Receding-Horizon MPC Engaged *)
    bTMR_SensorsAllHealthy          : BOOL;     (* True if All 10 Triplicated Channels Have Zero Detected Faults *)

    (* Bit-Packed 32-Bit Diagnostic Status & Alarm Words *)
    dwStatusWord_Process            : DWORD;    (* Bit-Packed Unit Operational Mode & Subsystem Active Flags *)
    dwAlarmWord1_HighSeverity       : DWORD;    (* Bit-Packed Priority 1 Critical Alarms, Trips & ESD Interlocks *)
    dwAlarmWord2_ProcessAlarms      : DWORD;    (* Bit-Packed Priority 2/3 Process Operational Deviations (HH/LL/H/L) *)
    dwAlarmWord3_Sensors            : DWORD;    (* Bit-Packed TMR Discrepancy & Sensor Channel Failures *)
    dwAlarmWord4_Actuators          : DWORD;    (* Bit-Packed Actuator Saturation, Slew Clamps & Position Discrepancies *)

    (* Cyber-Physical Calculated Observers & Thermodynamic Metrics *)
    rOverflashRefluxRatio_Calc      : REAL;     (* Calculated Internal Overflash Wash Ratio to Fresh Crude Feed [%] *)
    rTopPumparoundDuty_MW           : REAL;     (* Real-Time Enthalpy Heat Removal Rate in Top Pumparound [kW] *)
    rMidPumparoundDuty_MW           : REAL;     (* Real-Time Enthalpy Heat Removal Rate in Middle Pumparound [kW] *)
    rEstimatedAcidDewPoint_C        : REAL;     (* Thermodynamic Real-Time Water-HCl Acidic Condensation Point [deg C] *)
    rInferredKeroFlashPoint_C       : REAL;     (* Inferred Kerosene Product Closed-Cup Flash Point [deg C] *)
    rInferredDieselD86_95_C         : REAL;     (* Inferred Light Diesel ASTM D86 95% Evaporation Temperature [deg C] *)
    rColumnInternalRefluxRatio      : REAL;     (* Internal Reflux to Overhead Distillate Ratio L/D [-] *)
    rFurnaceTwoPhaseVaporFrac       : REAL;     (* Furnace Transfer Line Equilibrium Flash Vaporization Fraction [%] *)
    rDesalterSaltRemovalEff_Pct     : REAL;     (* Estimated Desalter Inorganic Salt Extraction Efficiency [%] *)
END_VAR
VAR
    (* Execution Timing & Scan Prescalers *)
    rTs                             : REAL := 0.020; (* Internal execution scan period [s] *)
    rTimer_FSM_State                : REAL := 0.0;   (* Operational state elapsed residency timer [s] *)
    rTimer_PurgePhase               : REAL := 0.0;   (* Nitrogen purge stabilization timer [s] *)
    rTimer_WarmCircPhase            : REAL := 0.0;   (* Warm flush circulation stabilization timer [s] *)
    rTimer_HeaterRampPhase          : REAL := 0.0;   (* Fired heater ramping elapsed timer [s] *)
    rTimer_HydraulicEquilPhase      : REAL := 0.0;   (* Column hydraulic holdup equilibration timer [s] *)
    rTimer_DesalterStartup          : REAL := 0.0;   (* Desalter electrostatic grid startup timer [s] *)
    udiScanCounter                  : UDINT := 0;    (* Master cyclic scan execution counter *)
    bFirstScan                      : BOOL := TRUE;  (* First scan initialization flag *)

    (* 2oo3 Triple Modular Redundancy (TMR) Data Structures for 10 Sensor Channels *)
    (* Channel 1: PDT_ColTrayDP *)
    rTMR_ValA_1                     : REAL;
    rTMR_ValB_1                     : REAL;
    rTMR_ValC_1                     : REAL;
    bTMR_DevAB_1                    : BOOL;
    bTMR_DevBC_1                    : BOOL;
    bTMR_DevCA_1                    : BOOL;
    rTMR_TimerAB_1                  : REAL := 0.0;
    rTMR_TimerBC_1                  : REAL := 0.0;
    rTMR_TimerCA_1                  : REAL := 0.0;
    bTMR_FaultA_1                   : BOOL := FALSE;
    bTMR_FaultB_1                   : BOOL := FALSE;
    bTMR_FaultC_1                   : BOOL := FALSE;
    bTMR_Degraded_1                 : BOOL := FALSE;
    rTMR_Voted_1                    : REAL := 0.25;
    rTMR_Tol_1                      : REAL := 0.080; (* Tolerance threshold [bar] *)

    (* Channel 2: TT_FlashZoneTemp *)
    rTMR_ValA_2                     : REAL;
    rTMR_ValB_2                     : REAL;
    rTMR_ValC_2                     : REAL;
    bTMR_DevAB_2                    : BOOL;
    bTMR_DevBC_2                    : BOOL;
    bTMR_DevCA_2                    : BOOL;
    rTMR_TimerAB_2                  : REAL := 0.0;
    rTMR_TimerBC_2                  : REAL := 0.0;
    rTMR_TimerCA_2                  : REAL := 0.0;
    bTMR_FaultA_2                   : BOOL := FALSE;
    bTMR_FaultB_2                   : BOOL := FALSE;
    bTMR_FaultC_2                   : BOOL := FALSE;
    bTMR_Degraded_2                 : BOOL := FALSE;
    rTMR_Voted_2                    : REAL := 365.0;
    rTMR_Tol_2                      : REAL := 8.0;   (* Tolerance threshold [deg C] *)

    (* Channel 3: PT_OverheadPress *)
    rTMR_ValA_3                     : REAL;
    rTMR_ValB_3                     : REAL;
    rTMR_ValC_3                     : REAL;
    bTMR_DevAB_3                    : BOOL;
    bTMR_DevBC_3                    : BOOL;
    bTMR_DevCA_3                    : BOOL;
    rTMR_TimerAB_3                  : REAL := 0.0;
    rTMR_TimerBC_3                  : REAL := 0.0;
    rTMR_TimerCA_3                  : REAL := 0.0;
    bTMR_FaultA_3                   : BOOL := FALSE;
    bTMR_FaultB_3                   : BOOL := FALSE;
    bTMR_FaultC_3                   : BOOL := FALSE;
    bTMR_Degraded_3                 : BOOL := FALSE;
    rTMR_Voted_3                    : REAL := 1.35;
    rTMR_Tol_3                      : REAL := 0.120; (* Tolerance threshold [bar] *)

    (* Channel 4: LT_OvhdAccumLevel *)
    rTMR_ValA_4                     : REAL;
    rTMR_ValB_4                     : REAL;
    rTMR_ValC_4                     : REAL;
    bTMR_DevAB_4                    : BOOL;
    bTMR_DevBC_4                    : BOOL;
    bTMR_DevCA_4                    : BOOL;
    rTMR_TimerAB_4                  : REAL := 0.0;
    rTMR_TimerBC_4                  : REAL := 0.0;
    rTMR_TimerCA_4                  : REAL := 0.0;
    bTMR_FaultA_4                   : BOOL := FALSE;
    bTMR_FaultB_4                   : BOOL := FALSE;
    bTMR_FaultC_4                   : BOOL := FALSE;
    bTMR_Degraded_4                 : BOOL := FALSE;
    rTMR_Voted_4                    : REAL := 50.0;
    rTMR_Tol_4                      : REAL := 6.0;   (* Tolerance threshold [%] *)

    (* Channel 5: LT_BtmResidueLevel *)
    rTMR_ValA_5                     : REAL;
    rTMR_ValB_5                     : REAL;
    rTMR_ValC_5                     : REAL;
    bTMR_DevAB_5                    : BOOL;
    bTMR_DevBC_5                    : BOOL;
    bTMR_DevCA_5                    : BOOL;
    rTMR_TimerAB_5                  : REAL := 0.0;
    rTMR_TimerBC_5                  : REAL := 0.0;
    rTMR_TimerCA_5                  : REAL := 0.0;
    bTMR_FaultA_5                   : BOOL := FALSE;
    bTMR_FaultB_5                   : BOOL := FALSE;
    bTMR_FaultC_5                   : BOOL := FALSE;
    bTMR_Degraded_5                 : BOOL := FALSE;
    rTMR_Voted_5                    : REAL := 50.0;
    rTMR_Tol_5                      : REAL := 6.0;   (* Tolerance threshold [%] *)

    (* Channel 6: LT_DesaltInterface *)
    rTMR_ValA_6                     : REAL;
    rTMR_ValB_6                     : REAL;
    rTMR_ValC_6                     : REAL;
    bTMR_DevAB_6                    : BOOL;
    bTMR_DevBC_6                    : BOOL;
    bTMR_DevCA_6                    : BOOL;
    rTMR_TimerAB_6                  : REAL := 0.0;
    rTMR_TimerBC_6                  : REAL := 0.0;
    rTMR_TimerCA_6                  : REAL := 0.0;
    bTMR_FaultA_6                   : BOOL := FALSE;
    bTMR_FaultB_6                   : BOOL := FALSE;
    bTMR_FaultC_6                   : BOOL := FALSE;
    bTMR_Degraded_6                 : BOOL := FALSE;
    rTMR_Voted_6                    : REAL := 45.0;
    rTMR_Tol_6                      : REAL := 7.0;   (* Tolerance threshold [%] *)

    (* Channel 7: AT_SourWaterPH *)
    rTMR_ValA_7                     : REAL;
    rTMR_ValB_7                     : REAL;
    rTMR_ValC_7                     : REAL;
    bTMR_DevAB_7                    : BOOL;
    bTMR_DevBC_7                    : BOOL;
    bTMR_DevCA_7                    : BOOL;
    rTMR_TimerAB_7                  : REAL := 0.0;
    rTMR_TimerBC_7                  : REAL := 0.0;
    rTMR_TimerCA_7                  : REAL := 0.0;
    bTMR_FaultA_7                   : BOOL := FALSE;
    bTMR_FaultB_7                   : BOOL := FALSE;
    bTMR_FaultC_7                   : BOOL := FALSE;
    bTMR_Degraded_7                 : BOOL := FALSE;
    rTMR_Voted_7                    : REAL := 6.2;
    rTMR_Tol_7                      : REAL := 0.60;  (* Tolerance threshold [pH] *)

    (* Channel 8: FT_KeroDrawFlow *)
    rTMR_ValA_8                     : REAL;
    rTMR_ValB_8                     : REAL;
    rTMR_ValC_8                     : REAL;
    bTMR_DevAB_8                    : BOOL;
    bTMR_DevBC_8                    : BOOL;
    bTMR_DevCA_8                    : BOOL;
    rTMR_TimerAB_8                  : REAL := 0.0;
    rTMR_TimerBC_8                  : REAL := 0.0;
    rTMR_TimerCA_8                  : REAL := 0.0;
    bTMR_FaultA_8                   : BOOL := FALSE;
    bTMR_FaultB_8                   : BOOL := FALSE;
    bTMR_FaultC_8                   : BOOL := FALSE;
    bTMR_Degraded_8                 : BOOL := FALSE;
    rTMR_Voted_8                    : REAL := 45000.0;
    rTMR_Tol_8                      : REAL := 3000.0; (* Tolerance threshold [kg/h] *)

    (* Channel 9: FT_DieselDrawFlow *)
    rTMR_ValA_9                     : REAL;
    rTMR_ValB_9                     : REAL;
    rTMR_ValC_9                     : REAL;
    bTMR_DevAB_9                    : BOOL;
    bTMR_DevBC_9                    : BOOL;
    bTMR_DevCA_9                    : BOOL;
    rTMR_TimerAB_9                  : REAL := 0.0;
    rTMR_TimerBC_9                  : REAL := 0.0;
    rTMR_TimerCA_9                  : REAL := 0.0;
    bTMR_FaultA_9                   : BOOL := FALSE;
    bTMR_FaultB_9                   : BOOL := FALSE;
    bTMR_FaultC_9                   : BOOL := FALSE;
    bTMR_Degraded_9                 : BOOL := FALSE;
    rTMR_Voted_9                    : REAL := 75000.0;
    rTMR_Tol_9                      : REAL := 4500.0; (* Tolerance threshold [kg/h] *)

    (* Channel 10: FT_AGODrawFlow *)
    rTMR_ValA_10                    : REAL;
    rTMR_ValB_10                    : REAL;
    rTMR_ValC_10                    : REAL;
    bTMR_DevAB_10                   : BOOL;
    bTMR_DevBC_10                   : BOOL;
    bTMR_DevCA_10                   : BOOL;
    rTMR_TimerAB_10                 : REAL := 0.0;
    rTMR_TimerBC_10                 : REAL := 0.0;
    rTMR_TimerCA_10                 : REAL := 0.0;
    bTMR_FaultA_10                  : BOOL := FALSE;
    bTMR_FaultB_10                  : BOOL := FALSE;
    bTMR_FaultC_10                  : BOOL := FALSE;
    bTMR_Degraded_10                : BOOL := FALSE;
    rTMR_Voted_10                   : REAL := 32000.0;
    rTMR_Tol_10                     : REAL := 2500.0; (* Tolerance threshold [kg/h] *)

    rTMR_DiscrepancyLimit_Sec       : REAL := 0.500;  (* 500 ms qualification timer before declaring sensor channel fault *)

    (* First-Principles Thermodynamic & Cyber-Physical Observers *)
    (* Overhead Acid Water Dew-Point & Neutralization *)
    rWaterVaporPartialPress_bar     : REAL := 0.085;
    rHCl_PartialPress_bar           : REAL := 0.00012;
    rAminePID_Integral              : REAL := 0.0;
    rAminePID_PrevError             : REAL := 0.0;
    rAminePID_Derivative            : REAL := 0.0;
    rAminePID_Kp                    : REAL := 8.5;
    rAminePID_Ki                    : REAL := 0.45;
    rAminePID_Kd                    : REAL := 1.2;
    rAminePID_WindupLimit           : REAL := 100.0;
    rFilmingAmineRatioFactor        : REAL := 0.00042; (* L amine per kg overhead vapor *)
    rFilmingAmineProbeBias          : REAL := 1.0;

    (* Desalter Emulsion Interface Controller *)
    rDesaltPI_Integral              : REAL := 0.0;
    rDesaltPI_Kp                    : REAL := 1.85;
    rDesaltPI_Ki                    : REAL := 0.055;
    rDesaltWashWaterRatio           : REAL := 0.052; (* 5.2 vol% wash water injection *)

    (* Fired Heater Pass Balancing Observer *)
    rFurnacePassTotal_m3h           : REAL := 0.0;
    rFurnacePassMean_m3h            : REAL := 0.0;
    rFurnacePassDev_1               : REAL := 0.0;
    rFurnacePassDev_2               : REAL := 0.0;
    rFurnacePassDev_3               : REAL := 0.0;
    rFurnacePassDev_4               : REAL := 0.0;
    rFurnacePassInt_1               : REAL := 0.0;
    rFurnacePassInt_2               : REAL := 0.0;
    rFurnacePassInt_3               : REAL := 0.0;
    rFurnacePassInt_4               : REAL := 0.0;
    rFurnacePassGain_Kp             : REAL := 0.12;
    rFurnacePassGain_Ki             : REAL := 0.008;

    (* Pumparound Enthalpy Heat Integration Balances *)
    rCp_TPA_kJ_kgK                  : REAL := 2.45;  (* Specific heat capacity Top Pumparound [kJ/kg.K] *)
    rCp_MPA_kJ_kgK                  : REAL := 2.68;  (* Specific heat capacity Middle Pumparound [kJ/kg.K] *)
    rDensity_TPA_kg_m3              : REAL := 765.0; (* Density of TPA liquid [kg/m3] *)
    rDensity_MPA_kg_m3              : REAL := 815.0; (* Density of MPA liquid [kg/m3] *)

    (* 8x8 Cyber-Physical Discrete State-Space System Matrices (Ts = 20 ms) *)
    (* x = [dT_top, dT_fz, dP_ovhd, dL_acc, dF_overflash, dL_btm, dQ_TPA, dL_desalt]^T *)
    (* u = [u_Reflux, u_FuelGas, u_Offgas, u_LightNaphtha, u_TPA, u_MPA, u_Residue, u_Brine]^T *)
    (* d = [dF_crude, dRho_crude, dTamb, dTCIT]^T *)
    mA                              : ARRAY[1..8, 1..8] OF REAL;
    mB                              : ARRAY[1..8, 1..8] OF REAL;
    mC                              : ARRAY[1..8, 1..8] OF REAL;
    mD                              : ARRAY[1..8, 1..8] OF REAL;
    mBd                             : ARRAY[1..8, 1..4] OF REAL;

    (* State-Space Vectors *)
    vX                              : ARRAY[1..8] OF REAL; (* Current state estimation vector *)
    vX_prev                         : ARRAY[1..8] OF REAL; (* Previous state vector *)
    vX_next                         : ARRAY[1..8] OF REAL; (* Predicted state vector *)
    vX_ref                          : ARRAY[1..8] OF REAL; (* State reference trajectory setpoints *)
    vY_est                          : ARRAY[1..8] OF REAL; (* Estimated cyber-physical plant outputs *)
    vU                              : ARRAY[1..8] OF REAL; (* Current manipulated actuator vector *)
    vU_prev                         : ARRAY[1..8] OF REAL; (* Previous scan actuator commands *)
    vU_target                       : ARRAY[1..8] OF REAL; (* Nominal target actuator positions *)
    vDist                           : ARRAY[1..4] OF REAL; (* Disturbance feedforward vector *)

    (* Model Predictive Control (MPC) Cost Weight Matrices & Workspace *)
    mQ                              : ARRAY[1..8, 1..8] OF REAL; (* State tracking penalty matrix *)
    mR                              : ARRAY[1..8, 1..8] OF REAL; (* Actuator control effort penalty matrix *)
    mS                              : ARRAY[1..8, 1..8] OF REAL; (* Actuator slew rate delta penalty matrix *)
    mP                              : ARRAY[1..8, 1..8] OF REAL; (* Terminal Lyapunov stability matrix *)
    vGrad                           : ARRAY[1..8] OF REAL; (* Projected Gradient Descent gradient vector *)
    vU_opt                          : ARRAY[1..8] OF REAL; (* MPC candidate optimization vector *)
    vU_min                          : ARRAY[1..8] OF REAL; (* Physical actuator minimum box bounds [%] *)
    vU_max                          : ARRAY[1..8] OF REAL; (* Physical actuator maximum box bounds [%] *)
    vDeltaU_max                     : ARRAY[1..8] OF REAL; (* Maximum allowable actuator slew per scan cycle [%] *)
    rStepSize_PGD                   : REAL := 0.015;       (* PGD constant gradient descent step size *)
    iMPC_Iter                       : INT := 0;            (* MPC solver iteration loop index *)
    iState_Idx                      : INT := 0;            (* State matrix row index *)
    jState_Idx                      : INT := 0;            (* State matrix column index *)
    kInput_Idx                      : INT := 0;            (* Input actuator loop index *)
    rCost_J                         : REAL := 0.0;         (* Instantaneous MPC quadratic cost functional *)

    (* Operational Finite State Machine Variables *)
    iFSM_NextState                  : INT := 0;
    bStateTransitionReq             : BOOL := FALSE;
    bPermissive_WarmCirc            : BOOL := FALSE;
    bPermissive_CrudeCutIn          : BOOL := FALSE;
    bPermissive_HeaterRamp          : BOOL := FALSE;
    bPermissive_HydraulicEquil      : BOOL := FALSE;
    bPermissive_SideDrawCutIn       : BOOL := FALSE;
    bPermissive_PA_Opt              : BOOL := FALSE;
    bPermissive_SteadyState         : BOOL := FALSE;

    (* ISA-18.2 Multi-Tiered Alarm Thresholds & Hysteresis Deadbands *)
    (* Flash Zone Temperature Thresholds [deg C] *)
    rLim_FZ_Temp_HH                 : REAL := 385.0;
    rLim_FZ_Temp_H                  : REAL := 375.0;
    rLim_FZ_Temp_L                  : REAL := 345.0;
    rLim_FZ_Temp_LL                 : REAL := 330.0;
    rDeadband_FZ_Temp               : REAL := 2.0;

    (* Overhead Pressure Thresholds [bar] *)
    rLim_OvhdPress_HH               : REAL := 2.50;
    rLim_OvhdPress_H                : REAL := 2.00;
    rLim_OvhdPress_L                : REAL := 1.05;
    rLim_OvhdPress_LL               : REAL := 0.85;
    rDeadband_OvhdPress             : REAL := 0.050;

    (* Overhead Accumulator Level Thresholds [%] *)
    rLim_AccumLevel_HH              : REAL := 88.0;
    rLim_AccumLevel_H               : REAL := 78.0;
    rLim_AccumLevel_L               : REAL := 22.0;
    rLim_AccumLevel_LL              : REAL := 12.0;
    rDeadband_AccumLevel            : REAL := 2.0;

    (* Bottom Residue Sump Level Thresholds [%] *)
    rLim_BtmLevel_HH                : REAL := 90.0;
    rLim_BtmLevel_H                 : REAL := 80.0;
    rLim_BtmLevel_L                 : REAL := 20.0;
    rLim_BtmLevel_LL                : REAL := 10.0;
    rDeadband_BtmLevel              : REAL := 2.0;

    (* Desalter Interface Level Thresholds [%] *)
    rLim_DesaltLevel_HH             : REAL := 85.0;
    rLim_DesaltLevel_H              : REAL := 75.0;
    rLim_DesaltLevel_L              : REAL := 25.0;
    rLim_DesaltLevel_LL             : REAL := 15.0;
    rDeadband_DesaltLevel           : REAL := 2.0;

    (* Sour Water Boot pH Thresholds [pH] *)
    rLim_SourWaterPH_HH             : REAL := 8.50;
    rLim_SourWaterPH_H              : REAL := 7.50;
    rLim_SourWaterPH_L              : REAL := 5.50;
    rLim_SourWaterPH_LL             : REAL := 4.80;
    rDeadband_SourWaterPH           : REAL := 0.20;

    (* Column Tray Differential Pressure [bar] (Flooding / Weeping) *)
    rLim_TrayDP_Flooding_HH         : REAL := 0.650;
    rLim_TrayDP_Weeping_LL          : REAL := 0.075;
    rDeadband_TrayDP                : REAL := 0.020;

    (* Alarm Latches & State Flags *)
    bAlarm_FZ_Temp_HH               : BOOL := FALSE;
    bAlarm_FZ_Temp_H                : BOOL := FALSE;
    bAlarm_FZ_Temp_L                : BOOL := FALSE;
    bAlarm_FZ_Temp_LL               : BOOL := FALSE;
    bAlarm_OvhdPress_HH             : BOOL := FALSE;
    bAlarm_OvhdPress_H              : BOOL := FALSE;
    bAlarm_OvhdPress_L              : BOOL := FALSE;
    bAlarm_OvhdPress_LL             : BOOL := FALSE;
    bAlarm_AccumLevel_HH            : BOOL := FALSE;
    bAlarm_AccumLevel_H             : BOOL := FALSE;
    bAlarm_AccumLevel_L             : BOOL := FALSE;
    bAlarm_AccumLevel_LL            : BOOL := FALSE;
    bAlarm_BtmLevel_HH              : BOOL := FALSE;
    bAlarm_BtmLevel_H               : BOOL := FALSE;
    bAlarm_BtmLevel_L               : BOOL := FALSE;
    bAlarm_BtmLevel_LL              : BOOL := FALSE;
    bAlarm_DesaltLevel_HH           : BOOL := FALSE;
    bAlarm_DesaltLevel_H            : BOOL := FALSE;
    bAlarm_DesaltLevel_L            : BOOL := FALSE;
    bAlarm_DesaltLevel_LL           : BOOL := FALSE;
    bAlarm_SourWaterPH_HH           : BOOL := FALSE;
    bAlarm_SourWaterPH_H            : BOOL := FALSE;
    bAlarm_SourWaterPH_L            : BOOL := FALSE;
    bAlarm_SourWaterPH_LL           : BOOL := FALSE;
    bAlarm_TrayDP_Flooding          : BOOL := FALSE;
    bAlarm_TrayDP_Weeping           : BOOL := FALSE;
    bAlarm_FurnacePassUnbalance     : BOOL := FALSE;
    bAlarm_DesalterGridTripped      : BOOL := FALSE;
    bAlarm_CorrosionHighRate        : BOOL := FALSE;

    (* Previous Measurements for Rate-of-Change (ROC) Detection *)
    rPrev_FZ_Temp                   : REAL := 365.0;
    rPrev_OvhdPress                 : REAL := 1.35;
    rROC_FZ_Temp                    : REAL := 0.0;
    rROC_OvhdPress                  : REAL := 0.0;
    rLim_ROC_FZ_Temp                : REAL := 1.50;  (* Max allowable rate of change [deg C / s] *)
    rLim_ROC_OvhdPress              : REAL := 0.100; (* Max allowable rate of change [bar / s] *)
    bAlarm_ROC_FZ_Temp              : BOOL := FALSE;
    bAlarm_ROC_OvhdPress            : BOOL := FALSE;
END_VAR

(* ====================================================================================================================
   SECTION 0: SCAN CYCLE MANAGEMENT, MATRIX INITIALIZATION & CLOCK PRESCALERS
   ==================================================================================================================== *)
udiScanCounter := udiScanCounter + 1;
rTs := TIME_TO_REAL(tCycleTime) / 1000.0;
IF rTs < 0.001 OR rTs > 0.500 THEN
    rTs := 0.020; (* Clamp to nominal 20 ms scan period *)
END_IF;

IF bFirstScan THEN
    bFirstScan := FALSE;
    iCurrentState := 0; (* Start at Nitrogen Purge / Inerting *)
    sCurrentStateName := 'NITROGEN_INERTING_PURGE';
    rTimer_FSM_State := 0.0;

    (* State-Space Matrix Initialization (A: 8x8 Continuous-to-Discrete Ts=20ms) *)
    (* State vector: [T_top, T_fz, P_ovhd, L_acc, F_overflash, L_btm, Q_TPA, L_desalt] *)
    mA[1,1] := 0.9850; mA[1,2] := 0.0035; mA[1,3] := 0.0120; mA[1,4] := 0.0000; mA[1,5] := 0.0000; mA[1,6] := 0.0000; mA[1,7] := -0.0045; mA[1,8] := 0.0000;
    mA[2,1] := 0.0012; mA[2,2] := 0.9910; mA[2,3] := 0.0040; mA[2,4] := 0.0000; mA[2,5] := -0.0085; mA[2,6] := 0.0000; mA[2,7] := -0.0020; mA[2,8] := 0.0000;
    mA[3,1] := 0.0045; mA[3,2] := 0.0028; mA[3,3] := 0.9780; mA[3,4] := 0.0010; mA[3,5] := 0.0000; mA[3,6] := 0.0000; mA[3,7] := -0.0015; mA[3,8] := 0.0000;
    mA[4,1] := 0.0080; mA[4,2] := 0.0000; mA[4,3] := 0.0050; mA[4,4] := 0.9950; mA[4,5] := 0.0000; mA[4,6] := 0.0000; mA[4,7] := 0.0035; mA[4,8] := 0.0000;
    mA[5,1] := -0.0020; mA[5,2] := 0.0150; mA[5,3] := 0.0000; mA[5,4] := 0.0000; mA[5,5] := 0.9650; mA[5,6] := 0.0000; mA[5,7] := -0.0180; mA[5,8] := 0.0000;
    mA[6,1] := 0.0000; mA[6,2] := 0.0080; mA[6,3] := 0.0000; mA[6,4] := 0.0000; mA[6,5] := 0.0120; mA[6,6] := 0.9960; mA[6,7] := 0.0000; mA[6,8] := 0.0000;
    mA[7,1] := 0.0050; mA[7,2] := 0.0000; mA[7,3] := 0.0000; mA[7,4] := 0.0000; mA[7,5] := 0.0000; mA[7,6] := 0.0000; mA[7,7] := 0.9820; mA[7,8] := 0.0000;
    mA[8,1] := 0.0000; mA[8,2] := 0.0000; mA[8,3] := 0.0000; mA[8,4] := 0.0000; mA[8,5] := 0.0000; mA[8,6] := 0.0000; mA[8,7] := 0.0000; mA[8,8] := 0.9940;

    (* Control Input Matrix B: 8x8 (Manipulated Variables to States) *)
    (* u = [Reflux, FuelGas, Offgas, LN_Draw, TPA_Flow, MPA_Flow, Residue_Draw, Brine_Dump] *)
    mB[1,1] := -0.0450; mB[1,2] := 0.0180; mB[1,3] := 0.0050; mB[1,4] := 0.0020; mB[1,5] := -0.0220; mB[1,6] := -0.0120; mB[1,7] := 0.0000; mB[1,8] := 0.0000;
    mB[2,1] := 0.0000; mB[2,2] := 0.0650; mB[2,3] := 0.0000; mB[2,4] := 0.0000; mB[2,5] := -0.0080; mB[2,6] := -0.0150; mB[2,7] := 0.0000; mB[2,8] := 0.0000;
    mB[3,1] := 0.0080; mB[3,2] := 0.0350; mB[3,3] := -0.0580; mB[3,4] := 0.0000; mB[3,5] := -0.0040; mB[3,6] := -0.0020; mB[3,7] := 0.0000; mB[3,8] := 0.0000;
    mB[4,1] := -0.0380; mB[4,2] := 0.0220; mB[4,3] := 0.0000; mB[4,4] := -0.0480; mB[4,5] := 0.0050; mB[4,6] := 0.0000; mB[4,7] := 0.0000; mB[4,8] := 0.0000;
    mB[5,1] := 0.0120; mB[5,2] := 0.0450; mB[5,3] := 0.0000; mB[5,4] := 0.0000; mB[5,5] := -0.0320; mB[5,6] := -0.0250; mB[5,7] := 0.0000; mB[5,8] := 0.0000;
    mB[6,1] := 0.0000; mB[6,2] := -0.0150; mB[6,3] := 0.0000; mB[6,4] := 0.0000; mB[6,5] := 0.0080; mB[6,6] := 0.0120; mB[6,7] := -0.0550; mB[6,8] := 0.0000;
    mB[7,1] := 0.0020; mB[7,2] := 0.0000; mB[7,3] := 0.0000; mB[7,4] := 0.0000; mB[7,5] := 0.0680; mB[7,6] := 0.0050; mB[7,7] := 0.0000; mB[7,8] := 0.0000;
    mB[8,1] := 0.0000; mB[8,2] := 0.0000; mB[8,3] := 0.0000; mB[8,4] := 0.0000; mB[8,5] := 0.0000; mB[8,6] := 0.0000; mB[8,7] := 0.0000; mB[8,8] := -0.0420;

    (* Disturbance Matrix Bd: 8x4 *)
    (* d = [F_crude, Rho_crude, Tamb, TCIT] *)
    mBd[1,1] := 0.0120; mBd[1,2] := -0.0040; mBd[1,3] := -0.0150; mBd[1,4] := 0.0080;
    mBd[2,1] := -0.0350; mBd[2,2] := 0.0180; mBd[2,3] := 0.0000; mBd[2,4] := 0.0420;
    mBd[3,1] := 0.0180; mBd[3,2] := 0.0000; mBd[3,3] := -0.0220; mBd[3,4] := 0.0150;
    mBd[4,1] := 0.0250; mBd[4,2] := -0.0080; mBd[4,3] := -0.0120; mBd[4,4] := 0.0050;
    mBd[5,1] := 0.0480; mBd[5,2] := -0.0220; mBd[5,3] := 0.0000; mBd[5,4] := 0.0280;
    mBd[6,1] := 0.0380; mBd[6,2] := 0.0150; mBd[6,3] := 0.0000; mBd[6,4] := -0.0120;
    mBd[7,1] := 0.0150; mBd[7,2] := 0.0000; mBd[7,3] := -0.0180; mBd[7,4] := 0.0050;
    mBd[8,1] := 0.0220; mBd[8,2] := -0.0150; mBd[8,3] := 0.0000; mBd[8,4] := 0.0000;

    (* Output Matrix C (Direct Identity Mapping for Linearized State Observables) *)
    FOR iState_Idx := 1 TO 8 DO
        FOR jState_Idx := 1 TO 8 DO
            IF iState_Idx = jState_Idx THEN
                mC[iState_Idx, jState_Idx] := 1.0;
                mQ[iState_Idx, jState_Idx] := 10.0; (* State error penalty *)
                mP[iState_Idx, jState_Idx] := 25.0; (* Terminal cost penalty *)
                mR[iState_Idx, jState_Idx] := 1.0;  (* Actuator effort penalty *)
                mS[iState_Idx, jState_Idx] := 5.0;  (* Slew rate penalty *)
            ELSE
                mC[iState_Idx, jState_Idx] := 0.0;
                mQ[iState_Idx, jState_Idx] := 0.0;
                mP[iState_Idx, jState_Idx] := 0.0;
                mR[iState_Idx, jState_Idx] := 0.0;
                mS[iState_Idx, jState_Idx] := 0.0;
            END_IF;
            mD[iState_Idx, jState_Idx] := 0.0;
        END_FOR;
    END_FOR;

    (* Emphasize critical state penalties *)
    mQ[2,2] := 28.0; (* Flash zone temperature tracking critical for yields *)
    mQ[3,3] := 35.0; (* Column overhead pressure critical for hydraulic stability *)
    mQ[5,5] := 20.0; (* Overflash wash ratio critical for preventing heavy metal entrainment *)
    mQ[8,8] := 22.0; (* Desalter emulsion interface critical to prevent water carryover *)

    (* Actuator Box Bounds & Slew Limits *)
    FOR kInput_Idx := 1 TO 8 DO
        vU_min[kInput_Idx] := 5.0;    (* Minimum actuator position 5.0% *)
        vU_max[kInput_Idx] := 95.0;   (* Maximum actuator position 95.0% *)
        vDeltaU_max[kInput_Idx] := 0.25; (* Slew limit 0.25% per 20 ms scan -> max 12.5% per second *)
        vU_target[kInput_Idx] := 50.0;
        vU[kInput_Idx] := 50.0;
        vU_prev[kInput_Idx] := 50.0;
    END_FOR;
    vU_min[2] := 10.0; (* Fired heater fuel gas minimum firing 10.0% to prevent flameout *)
END_IF;

(* Master Reset Logic *)
IF bReset THEN
    bEmergencyTripActive := FALSE;
    bAlarm_FZ_Temp_HH := FALSE;
    bAlarm_FZ_Temp_LL := FALSE;
    bAlarm_OvhdPress_HH := FALSE;
    bAlarm_OvhdPress_LL := FALSE;
    bAlarm_AccumLevel_HH := FALSE;
    bAlarm_AccumLevel_LL := FALSE;
    bAlarm_BtmLevel_HH := FALSE;
    bAlarm_BtmLevel_LL := FALSE;
    bAlarm_DesaltLevel_HH := FALSE;
    bAlarm_DesaltLevel_LL := FALSE;
    bAlarm_SourWaterPH_HH := FALSE;
    bAlarm_SourWaterPH_LL := FALSE;
    bAlarm_TrayDP_Flooding := FALSE;
    bAlarm_TrayDP_Weeping := FALSE;
    bAlarm_ROC_FZ_Temp := FALSE;
    bAlarm_ROC_OvhdPress := FALSE;
    dwAlarmWord1_HighSeverity := 16#00000000;
    dwAlarmWord2_ProcessAlarms := 16#00000000;
    dwAlarmWord3_Sensors := 16#00000000;
    dwAlarmWord4_Actuators := 16#00000000;
END_IF;

(* ====================================================================================================================
   SECTION 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS
   ==================================================================================================================== *)
(* --- Channel 1: Column Tray Differential Pressure (PDT_ColTrayDP) --- *)
rTMR_ValA_1 := rPDT_ColTrayDP_101A;
rTMR_ValB_1 := rPDT_ColTrayDP_101B;
rTMR_ValC_1 := rPDT_ColTrayDP_101C;
bTMR_DevAB_1 := ABS(rTMR_ValA_1 - rTMR_ValB_1) > rTMR_Tol_1;
bTMR_DevBC_1 := ABS(rTMR_ValB_1 - rTMR_ValC_1) > rTMR_Tol_1;
bTMR_DevCA_1 := ABS(rTMR_ValC_1 - rTMR_ValA_1) > rTMR_Tol_1;
IF bTMR_DevAB_1 THEN rTMR_TimerAB_1 := rTMR_TimerAB_1 + rTs; ELSE rTMR_TimerAB_1 := 0.0; END_IF;
IF bTMR_DevBC_1 THEN rTMR_TimerBC_1 := rTMR_TimerBC_1 + rTs; ELSE rTMR_TimerBC_1 := 0.0; END_IF;
IF bTMR_DevCA_1 THEN rTMR_TimerCA_1 := rTMR_TimerCA_1 + rTs; ELSE rTMR_TimerCA_1 := 0.0; END_IF;
IF (rTMR_TimerAB_1 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_1 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultA_1 := TRUE; END_IF;
IF (rTMR_TimerAB_1 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerBC_1 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultB_1 := TRUE; END_IF;
IF (rTMR_TimerBC_1 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_1 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultC_1 := TRUE; END_IF;

IF NOT bTMR_FaultA_1 AND NOT bTMR_FaultB_1 AND NOT bTMR_FaultC_1 THEN
    IF (rTMR_ValA_1 >= rTMR_ValB_1 AND rTMR_ValA_1 <= rTMR_ValC_1) OR (rTMR_ValA_1 <= rTMR_ValB_1 AND rTMR_ValA_1 >= rTMR_ValC_1) THEN
        rTMR_Voted_1 := rTMR_ValA_1;
    ELSIF (rTMR_ValB_1 >= rTMR_ValA_1 AND rTMR_ValB_1 <= rTMR_ValC_1) OR (rTMR_ValB_1 <= rTMR_ValA_1 AND rTMR_ValB_1 >= rTMR_ValC_1) THEN
        rTMR_Voted_1 := rTMR_ValB_1;
    ELSE
        rTMR_Voted_1 := rTMR_ValC_1;
    END_IF;
    bTMR_Degraded_1 := FALSE;
ELSIF bTMR_FaultA_1 AND NOT bTMR_FaultB_1 AND NOT bTMR_FaultC_1 THEN
    rTMR_Voted_1 := 0.5 * (rTMR_ValB_1 + rTMR_ValC_1);
    bTMR_Degraded_1 := TRUE;
ELSIF bTMR_FaultB_1 AND NOT bTMR_FaultA_1 AND NOT bTMR_FaultC_1 THEN
    rTMR_Voted_1 := 0.5 * (rTMR_ValA_1 + rTMR_ValC_1);
    bTMR_Degraded_1 := TRUE;
ELSIF bTMR_FaultC_1 AND NOT bTMR_FaultA_1 AND NOT bTMR_FaultB_1 THEN
    rTMR_Voted_1 := 0.5 * (rTMR_ValA_1 + rTMR_ValB_1);
    bTMR_Degraded_1 := TRUE;
ELSE
    bTMR_Degraded_1 := TRUE;
END_IF;

(* --- Channel 2: Flash Zone Multipoint Temperature (TT_FlashZoneTemp) --- *)
rTMR_ValA_2 := rTT_FlashZoneTemp_102A;
rTMR_ValB_2 := rTT_FlashZoneTemp_102B;
rTMR_ValC_2 := rTT_FlashZoneTemp_102C;
bTMR_DevAB_2 := ABS(rTMR_ValA_2 - rTMR_ValB_2) > rTMR_Tol_2;
bTMR_DevBC_2 := ABS(rTMR_ValB_2 - rTMR_ValC_2) > rTMR_Tol_2;
bTMR_DevCA_2 := ABS(rTMR_ValC_2 - rTMR_ValA_2) > rTMR_Tol_2;
IF bTMR_DevAB_2 THEN rTMR_TimerAB_2 := rTMR_TimerAB_2 + rTs; ELSE rTMR_TimerAB_2 := 0.0; END_IF;
IF bTMR_DevBC_2 THEN rTMR_TimerBC_2 := rTMR_TimerBC_2 + rTs; ELSE rTMR_TimerBC_2 := 0.0; END_IF;
IF bTMR_DevCA_2 THEN rTMR_TimerCA_2 := rTMR_TimerCA_2 + rTs; ELSE rTMR_TimerCA_2 := 0.0; END_IF;
IF (rTMR_TimerAB_2 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_2 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultA_2 := TRUE; END_IF;
IF (rTMR_TimerAB_2 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerBC_2 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultB_2 := TRUE; END_IF;
IF (rTMR_TimerBC_2 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_2 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultC_2 := TRUE; END_IF;

IF NOT bTMR_FaultA_2 AND NOT bTMR_FaultB_2 AND NOT bTMR_FaultC_2 THEN
    IF (rTMR_ValA_2 >= rTMR_ValB_2 AND rTMR_ValA_2 <= rTMR_ValC_2) OR (rTMR_ValA_2 <= rTMR_ValB_2 AND rTMR_ValA_2 >= rTMR_ValC_2) THEN
        rTMR_Voted_2 := rTMR_ValA_2;
    ELSIF (rTMR_ValB_2 >= rTMR_ValA_2 AND rTMR_ValB_2 <= rTMR_ValC_2) OR (rTMR_ValB_2 <= rTMR_ValA_2 AND rTMR_ValB_2 >= rTMR_ValC_2) THEN
        rTMR_Voted_2 := rTMR_ValB_2;
    ELSE
        rTMR_Voted_2 := rTMR_ValC_2;
    END_IF;
    bTMR_Degraded_2 := FALSE;
ELSIF bTMR_FaultA_2 AND NOT bTMR_FaultB_2 AND NOT bTMR_FaultC_2 THEN
    rTMR_Voted_2 := 0.5 * (rTMR_ValB_2 + rTMR_ValC_2);
    bTMR_Degraded_2 := TRUE;
ELSIF bTMR_FaultB_2 AND NOT bTMR_FaultA_2 AND NOT bTMR_FaultC_2 THEN
    rTMR_Voted_2 := 0.5 * (rTMR_ValA_2 + rTMR_ValC_2);
    bTMR_Degraded_2 := TRUE;
ELSIF bTMR_FaultC_2 AND NOT bTMR_FaultA_2 AND NOT bTMR_FaultC_2 THEN
    rTMR_Voted_2 := 0.5 * (rTMR_ValA_2 + rTMR_ValB_2);
    bTMR_Degraded_2 := TRUE;
ELSE
    bTMR_Degraded_2 := TRUE;
END_IF;

(* --- Channel 3: Column Overhead Vapor Pressure (PT_OverheadPress) --- *)
rTMR_ValA_3 := rPT_OverheadPress_103A;
rTMR_ValB_3 := rPT_OverheadPress_103B;
rTMR_ValC_3 := rPT_OverheadPress_103C;
bTMR_DevAB_3 := ABS(rTMR_ValA_3 - rTMR_ValB_3) > rTMR_Tol_3;
bTMR_DevBC_3 := ABS(rTMR_ValB_3 - rTMR_ValC_3) > rTMR_Tol_3;
bTMR_DevCA_3 := ABS(rTMR_ValC_3 - rTMR_ValA_3) > rTMR_Tol_3;
IF bTMR_DevAB_3 THEN rTMR_TimerAB_3 := rTMR_TimerAB_3 + rTs; ELSE rTMR_TimerAB_3 := 0.0; END_IF;
IF bTMR_DevBC_3 THEN rTMR_TimerBC_3 := rTMR_TimerBC_3 + rTs; ELSE rTMR_TimerBC_3 := 0.0; END_IF;
IF bTMR_DevCA_3 THEN rTMR_TimerCA_3 := rTMR_TimerCA_3 + rTs; ELSE rTMR_TimerCA_3 := 0.0; END_IF;
IF (rTMR_TimerAB_3 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_3 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultA_3 := TRUE; END_IF;
IF (rTMR_TimerAB_3 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerBC_3 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultB_3 := TRUE; END_IF;
IF (rTMR_TimerBC_3 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_3 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultC_3 := TRUE; END_IF;

IF NOT bTMR_FaultA_3 AND NOT bTMR_FaultB_3 AND NOT bTMR_FaultC_3 THEN
    IF (rTMR_ValA_3 >= rTMR_ValB_3 AND rTMR_ValA_3 <= rTMR_ValC_3) OR (rTMR_ValA_3 <= rTMR_ValB_3 AND rTMR_ValA_3 >= rTMR_ValC_3) THEN
        rTMR_Voted_3 := rTMR_ValA_3;
    ELSIF (rTMR_ValB_3 >= rTMR_ValA_3 AND rTMR_ValB_3 <= rTMR_ValC_3) OR (rTMR_ValB_3 <= rTMR_ValA_3 AND rTMR_ValB_3 >= rTMR_ValC_3) THEN
        rTMR_Voted_3 := rTMR_ValB_3;
    ELSE
        rTMR_Voted_3 := rTMR_ValC_3;
    END_IF;
    bTMR_Degraded_3 := FALSE;
ELSIF bTMR_FaultA_3 AND NOT bTMR_FaultB_3 AND NOT bTMR_FaultC_3 THEN
    rTMR_Voted_3 := 0.5 * (rTMR_ValB_3 + rTMR_ValC_3);
    bTMR_Degraded_3 := TRUE;
ELSIF bTMR_FaultB_3 AND NOT bTMR_FaultA_3 AND NOT bTMR_FaultC_3 THEN
    rTMR_Voted_3 := 0.5 * (rTMR_ValA_3 + rTMR_ValC_3);
    bTMR_Degraded_3 := TRUE;
ELSIF bTMR_FaultC_3 AND NOT bTMR_FaultA_3 AND NOT bTMR_FaultB_3 THEN
    rTMR_Voted_3 := 0.5 * (rTMR_ValA_3 + rTMR_ValB_3);
    bTMR_Degraded_3 := TRUE;
ELSE
    bTMR_Degraded_3 := TRUE;
END_IF;

(* --- Channel 4: Overhead Accumulator Level (LT_OvhdAccumLevel) --- *)
rTMR_ValA_4 := rLT_OvhdAccumLevel_104A;
rTMR_ValB_4 := rLT_OvhdAccumLevel_104B;
rTMR_ValC_4 := rLT_OvhdAccumLevel_104C;
bTMR_DevAB_4 := ABS(rTMR_ValA_4 - rTMR_ValB_4) > rTMR_Tol_4;
bTMR_DevBC_4 := ABS(rTMR_ValB_4 - rTMR_ValC_4) > rTMR_Tol_4;
bTMR_DevCA_4 := ABS(rTMR_ValC_4 - rTMR_ValA_4) > rTMR_Tol_4;
IF bTMR_DevAB_4 THEN rTMR_TimerAB_4 := rTMR_TimerAB_4 + rTs; ELSE rTMR_TimerAB_4 := 0.0; END_IF;
IF bTMR_DevBC_4 THEN rTMR_TimerBC_4 := rTMR_TimerBC_4 + rTs; ELSE rTMR_TimerBC_4 := 0.0; END_IF;
IF bTMR_DevCA_4 THEN rTMR_TimerCA_4 := rTMR_TimerCA_4 + rTs; ELSE rTMR_TimerCA_4 := 0.0; END_IF;
IF (rTMR_TimerAB_4 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_4 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultA_4 := TRUE; END_IF;
IF (rTMR_TimerAB_4 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerBC_4 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultB_4 := TRUE; END_IF;
IF (rTMR_TimerBC_4 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_4 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultC_4 := TRUE; END_IF;

IF NOT bTMR_FaultA_4 AND NOT bTMR_FaultB_4 AND NOT bTMR_FaultC_4 THEN
    IF (rTMR_ValA_4 >= rTMR_ValB_4 AND rTMR_ValA_4 <= rTMR_ValC_4) OR (rTMR_ValA_4 <= rTMR_ValB_4 AND rTMR_ValA_4 >= rTMR_ValC_4) THEN
        rTMR_Voted_4 := rTMR_ValA_4;
    ELSIF (rTMR_ValB_4 >= rTMR_ValA_4 AND rTMR_ValB_4 <= rTMR_ValC_4) OR (rTMR_ValB_4 <= rTMR_ValA_4 AND rTMR_ValB_4 >= rTMR_ValC_4) THEN
        rTMR_Voted_4 := rTMR_ValB_4;
    ELSE
        rTMR_Voted_4 := rTMR_ValC_4;
    END_IF;
    bTMR_Degraded_4 := FALSE;
ELSIF bTMR_FaultA_4 AND NOT bTMR_FaultB_4 AND NOT bTMR_FaultC_4 THEN
    rTMR_Voted_4 := 0.5 * (rTMR_ValB_4 + rTMR_ValC_4);
    bTMR_Degraded_4 := TRUE;
ELSIF bTMR_FaultB_4 AND NOT bTMR_FaultA_4 AND NOT bTMR_FaultC_4 THEN
    rTMR_Voted_4 := 0.5 * (rTMR_ValA_4 + rTMR_ValC_4);
    bTMR_Degraded_4 := TRUE;
ELSIF bTMR_FaultC_4 AND NOT bTMR_FaultA_4 AND NOT bTMR_FaultB_4 THEN
    rTMR_Voted_4 := 0.5 * (rTMR_ValA_4 + rTMR_ValB_4);
    bTMR_Degraded_4 := TRUE;
ELSE
    bTMR_Degraded_4 := TRUE;
END_IF;

(* --- Channel 5: Bottom Residue Sump Level (LT_BtmResidueLevel) --- *)
rTMR_ValA_5 := rLT_BtmResidueLevel_105A;
rTMR_ValB_5 := rLT_BtmResidueLevel_105B;
rTMR_ValC_5 := rLT_BtmResidueLevel_105C;
bTMR_DevAB_5 := ABS(rTMR_ValA_5 - rTMR_ValB_5) > rTMR_Tol_5;
bTMR_DevBC_5 := ABS(rTMR_ValB_5 - rTMR_ValC_5) > rTMR_Tol_5;
bTMR_DevCA_5 := ABS(rTMR_ValC_5 - rTMR_ValA_5) > rTMR_Tol_5;
IF bTMR_DevAB_5 THEN rTMR_TimerAB_5 := rTMR_TimerAB_5 + rTs; ELSE rTMR_TimerAB_5 := 0.0; END_IF;
IF bTMR_DevBC_5 THEN rTMR_TimerBC_5 := rTMR_TimerBC_5 + rTs; ELSE rTMR_TimerBC_5 := 0.0; END_IF;
IF bTMR_DevCA_5 THEN rTMR_TimerCA_5 := rTMR_TimerCA_5 + rTs; ELSE rTMR_TimerCA_5 := 0.0; END_IF;
IF (rTMR_TimerAB_5 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_5 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultA_5 := TRUE; END_IF;
IF (rTMR_TimerAB_5 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerBC_5 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultB_5 := TRUE; END_IF;
IF (rTMR_TimerBC_5 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_5 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultC_5 := TRUE; END_IF;

IF NOT bTMR_FaultA_5 AND NOT bTMR_FaultB_5 AND NOT bTMR_FaultC_5 THEN
    IF (rTMR_ValA_5 >= rTMR_ValB_5 AND rTMR_ValA_5 <= rTMR_ValC_5) OR (rTMR_ValA_5 <= rTMR_ValB_5 AND rTMR_ValA_5 >= rTMR_ValC_5) THEN
        rTMR_Voted_5 := rTMR_ValA_5;
    ELSIF (rTMR_ValB_5 >= rTMR_ValA_5 AND rTMR_ValB_5 <= rTMR_ValC_5) OR (rTMR_ValB_5 <= rTMR_ValA_5 AND rTMR_ValB_5 >= rTMR_ValC_5) THEN
        rTMR_Voted_5 := rTMR_ValB_5;
    ELSE
        rTMR_Voted_5 := rTMR_ValC_5;
    END_IF;
    bTMR_Degraded_5 := FALSE;
ELSIF bTMR_FaultA_5 AND NOT bTMR_FaultB_5 AND NOT bTMR_FaultC_5 THEN
    rTMR_Voted_5 := 0.5 * (rTMR_ValB_5 + rTMR_ValC_5);
    bTMR_Degraded_5 := TRUE;
ELSIF bTMR_FaultB_5 AND NOT bTMR_FaultA_5 AND NOT bTMR_FaultC_5 THEN
    rTMR_Voted_5 := 0.5 * (rTMR_ValA_5 + rTMR_ValC_5);
    bTMR_Degraded_5 := TRUE;
ELSIF bTMR_FaultC_5 AND NOT bTMR_FaultA_5 AND NOT bTMR_FaultB_5 THEN
    rTMR_Voted_5 := 0.5 * (rTMR_ValA_5 + rTMR_ValB_5);
    bTMR_Degraded_5 := TRUE;
ELSE
    bTMR_Degraded_5 := TRUE;
END_IF;

(* --- Channel 6: Desalter Emulsion Interface Level (LT_DesaltInterface) --- *)
rTMR_ValA_6 := rLT_DesaltInterface_106A;
rTMR_ValB_6 := rLT_DesaltInterface_106B;
rTMR_ValC_6 := rLT_DesaltInterface_106C;
bTMR_DevAB_6 := ABS(rTMR_ValA_6 - rTMR_ValB_6) > rTMR_Tol_6;
bTMR_DevBC_6 := ABS(rTMR_ValB_6 - rTMR_ValC_6) > rTMR_Tol_6;
bTMR_DevCA_6 := ABS(rTMR_ValC_6 - rTMR_ValA_6) > rTMR_Tol_6;
IF bTMR_DevAB_6 THEN rTMR_TimerAB_6 := rTMR_TimerAB_6 + rTs; ELSE rTMR_TimerAB_6 := 0.0; END_IF;
IF bTMR_DevBC_6 THEN rTMR_TimerBC_6 := rTMR_TimerBC_6 + rTs; ELSE rTMR_TimerBC_6 := 0.0; END_IF;
IF bTMR_DevCA_6 THEN rTMR_TimerCA_6 := rTMR_TimerCA_6 + rTs; ELSE rTMR_TimerCA_6 := 0.0; END_IF;
IF (rTMR_TimerAB_6 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_6 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultA_6 := TRUE; END_IF;
IF (rTMR_TimerAB_6 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerBC_6 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultB_6 := TRUE; END_IF;
IF (rTMR_TimerBC_6 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_6 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultC_6 := TRUE; END_IF;

IF NOT bTMR_FaultA_6 AND NOT bTMR_FaultB_6 AND NOT bTMR_FaultC_6 THEN
    IF (rTMR_ValA_6 >= rTMR_ValB_6 AND rTMR_ValA_6 <= rTMR_ValC_6) OR (rTMR_ValA_6 <= rTMR_ValB_6 AND rTMR_ValA_6 >= rTMR_ValC_6) THEN
        rTMR_Voted_6 := rTMR_ValA_6;
    ELSIF (rTMR_ValB_6 >= rTMR_ValA_6 AND rTMR_ValB_6 <= rTMR_ValC_6) OR (rTMR_ValB_6 <= rTMR_ValA_6 AND rTMR_ValB_6 >= rTMR_ValC_6) THEN
        rTMR_Voted_6 := rTMR_ValB_6;
    ELSE
        rTMR_Voted_6 := rTMR_ValC_6;
    END_IF;
    bTMR_Degraded_6 := FALSE;
ELSIF bTMR_FaultA_6 AND NOT bTMR_FaultB_6 AND NOT bTMR_FaultC_6 THEN
    rTMR_Voted_6 := 0.5 * (rTMR_ValB_6 + rTMR_ValC_6);
    bTMR_Degraded_6 := TRUE;
ELSIF bTMR_FaultB_6 AND NOT bTMR_FaultA_6 AND NOT bTMR_FaultC_6 THEN
    rTMR_Voted_6 := 0.5 * (rTMR_ValA_6 + rTMR_ValC_6);
    bTMR_Degraded_6 := TRUE;
ELSIF bTMR_FaultC_6 AND NOT bTMR_FaultA_6 AND NOT bTMR_FaultB_6 THEN
    rTMR_Voted_6 := 0.5 * (rTMR_ValA_6 + rTMR_ValB_6);
    bTMR_Degraded_6 := TRUE;
ELSE
    bTMR_Degraded_6 := TRUE;
END_IF;

(* --- Channel 7: Sour Water Boot pH (AT_SourWaterPH) --- *)
rTMR_ValA_7 := rAT_SourWaterPH_107A;
rTMR_ValB_7 := rAT_SourWaterPH_107B;
rTMR_ValC_7 := rAT_SourWaterPH_107C;
bTMR_DevAB_7 := ABS(rTMR_ValA_7 - rTMR_ValB_7) > rTMR_Tol_7;
bTMR_DevBC_7 := ABS(rTMR_ValB_7 - rTMR_ValC_7) > rTMR_Tol_7;
bTMR_DevCA_7 := ABS(rTMR_ValC_7 - rTMR_ValA_7) > rTMR_Tol_7;
IF bTMR_DevAB_7 THEN rTMR_TimerAB_7 := rTMR_TimerAB_7 + rTs; ELSE rTMR_TimerAB_7 := 0.0; END_IF;
IF bTMR_DevBC_7 THEN rTMR_TimerBC_7 := rTMR_TimerBC_7 + rTs; ELSE rTMR_TimerBC_7 := 0.0; END_IF;
IF bTMR_DevCA_7 THEN rTMR_TimerCA_7 := rTMR_TimerCA_7 + rTs; ELSE rTMR_TimerCA_7 := 0.0; END_IF;
IF (rTMR_TimerAB_7 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_7 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultA_7 := TRUE; END_IF;
IF (rTMR_TimerAB_7 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerBC_7 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultB_7 := TRUE; END_IF;
IF (rTMR_TimerBC_7 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_7 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultC_7 := TRUE; END_IF;

IF NOT bTMR_FaultA_7 AND NOT bTMR_FaultB_7 AND NOT bTMR_FaultC_7 THEN
    IF (rTMR_ValA_7 >= rTMR_ValB_7 AND rTMR_ValA_7 <= rTMR_ValC_7) OR (rTMR_ValA_7 <= rTMR_ValB_7 AND rTMR_ValA_7 >= rTMR_ValC_7) THEN
        rTMR_Voted_7 := rTMR_ValA_7;
    ELSIF (rTMR_ValB_7 >= rTMR_ValA_7 AND rTMR_ValB_7 <= rTMR_ValC_7) OR (rTMR_ValB_7 <= rTMR_ValA_7 AND rTMR_ValB_7 >= rTMR_ValC_7) THEN
        rTMR_Voted_7 := rTMR_ValB_7;
    ELSE
        rTMR_Voted_7 := rTMR_ValC_7;
    END_IF;
    bTMR_Degraded_7 := FALSE;
ELSIF bTMR_FaultA_7 AND NOT bTMR_FaultB_7 AND NOT bTMR_FaultC_7 THEN
    rTMR_Voted_7 := 0.5 * (rTMR_ValB_7 + rTMR_ValC_7);
    bTMR_Degraded_7 := TRUE;
ELSIF bTMR_FaultB_7 AND NOT bTMR_FaultA_7 AND NOT bTMR_FaultC_7 THEN
    rTMR_Voted_7 := 0.5 * (rTMR_ValA_7 + rTMR_ValC_7);
    bTMR_Degraded_7 := TRUE;
ELSIF bTMR_FaultC_7 AND NOT bTMR_FaultA_7 AND NOT bTMR_FaultB_7 THEN
    rTMR_Voted_7 := 0.5 * (rTMR_ValA_7 + rTMR_ValB_7);
    bTMR_Degraded_7 := TRUE;
ELSE
    bTMR_Degraded_7 := TRUE;
END_IF;

(* --- Channel 8: Kerosene Stripper Draw Mass Flow (FT_KeroDrawFlow) --- *)
rTMR_ValA_8 := rFT_KeroDrawFlow_108A;
rTMR_ValB_8 := rFT_KeroDrawFlow_108B;
rTMR_ValC_8 := rFT_KeroDrawFlow_108C;
bTMR_DevAB_8 := ABS(rTMR_ValA_8 - rTMR_ValB_8) > rTMR_Tol_8;
bTMR_DevBC_8 := ABS(rTMR_ValB_8 - rTMR_ValC_8) > rTMR_Tol_8;
bTMR_DevCA_8 := ABS(rTMR_ValC_8 - rTMR_ValA_8) > rTMR_Tol_8;
IF bTMR_DevAB_8 THEN rTMR_TimerAB_8 := rTMR_TimerAB_8 + rTs; ELSE rTMR_TimerAB_8 := 0.0; END_IF;
IF bTMR_DevBC_8 THEN rTMR_TimerBC_8 := rTMR_TimerBC_8 + rTs; ELSE rTMR_TimerBC_8 := 0.0; END_IF;
IF bTMR_DevCA_8 THEN rTMR_TimerCA_8 := rTMR_TimerCA_8 + rTs; ELSE rTMR_TimerCA_8 := 0.0; END_IF;
IF (rTMR_TimerAB_8 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_8 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultA_8 := TRUE; END_IF;
IF (rTMR_TimerAB_8 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerBC_8 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultB_8 := TRUE; END_IF;
IF (rTMR_TimerBC_8 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_8 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultC_8 := TRUE; END_IF;

IF NOT bTMR_FaultA_8 AND NOT bTMR_FaultB_8 AND NOT bTMR_FaultC_8 THEN
    IF (rTMR_ValA_8 >= rTMR_ValB_8 AND rTMR_ValA_8 <= rTMR_ValC_8) OR (rTMR_ValA_8 <= rTMR_ValB_8 AND rTMR_ValA_8 >= rTMR_ValC_8) THEN
        rTMR_Voted_8 := rTMR_ValA_8;
    ELSIF (rTMR_ValB_8 >= rTMR_ValA_8 AND rTMR_ValB_8 <= rTMR_ValC_8) OR (rTMR_ValB_8 <= rTMR_ValA_8 AND rTMR_ValB_8 >= rTMR_ValC_8) THEN
        rTMR_Voted_8 := rTMR_ValB_8;
    ELSE
        rTMR_Voted_8 := rTMR_ValC_8;
    END_IF;
    bTMR_Degraded_8 := FALSE;
ELSIF bTMR_FaultA_8 AND NOT bTMR_FaultB_8 AND NOT bTMR_FaultC_8 THEN
    rTMR_Voted_8 := 0.5 * (rTMR_ValB_8 + rTMR_ValC_8);
    bTMR_Degraded_8 := TRUE;
ELSIF bTMR_FaultB_8 AND NOT bTMR_FaultA_8 AND NOT bTMR_FaultC_8 THEN
    rTMR_Voted_8 := 0.5 * (rTMR_ValA_8 + rTMR_ValC_8);
    bTMR_Degraded_8 := TRUE;
ELSIF bTMR_FaultC_8 AND NOT bTMR_FaultA_8 AND NOT bTMR_FaultB_8 THEN
    rTMR_Voted_8 := 0.5 * (rTMR_ValA_8 + rTMR_ValB_8);
    bTMR_Degraded_8 := TRUE;
ELSE
    bTMR_Degraded_8 := TRUE;
END_IF;

(* --- Channel 9: Light Diesel Stripper Draw Mass Flow (FT_DieselDrawFlow) --- *)
rTMR_ValA_9 := rFT_DieselDrawFlow_109A;
rTMR_ValB_9 := rFT_DieselDrawFlow_109B;
rTMR_ValC_9 := rFT_DieselDrawFlow_109C;
bTMR_DevAB_9 := ABS(rTMR_ValA_9 - rTMR_ValB_9) > rTMR_Tol_9;
bTMR_DevBC_9 := ABS(rTMR_ValB_9 - rTMR_ValC_9) > rTMR_Tol_9;
bTMR_DevCA_9 := ABS(rTMR_ValC_9 - rTMR_ValA_9) > rTMR_Tol_9;
IF bTMR_DevAB_9 THEN rTMR_TimerAB_9 := rTMR_TimerAB_9 + rTs; ELSE rTMR_TimerAB_9 := 0.0; END_IF;
IF bTMR_DevBC_9 THEN rTMR_TimerBC_9 := rTMR_TimerBC_9 + rTs; ELSE rTMR_TimerBC_9 := 0.0; END_IF;
IF bTMR_DevCA_9 THEN rTMR_TimerCA_9 := rTMR_TimerCA_9 + rTs; ELSE rTMR_TimerCA_9 := 0.0; END_IF;
IF (rTMR_TimerAB_9 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_9 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultA_9 := TRUE; END_IF;
IF (rTMR_TimerAB_9 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerBC_9 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultB_9 := TRUE; END_IF;
IF (rTMR_TimerBC_9 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_9 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultC_9 := TRUE; END_IF;

IF NOT bTMR_FaultA_9 AND NOT bTMR_FaultB_9 AND NOT bTMR_FaultC_9 THEN
    IF (rTMR_ValA_9 >= rTMR_ValB_9 AND rTMR_ValA_9 <= rTMR_ValC_9) OR (rTMR_ValA_9 <= rTMR_ValB_9 AND rTMR_ValA_9 >= rTMR_ValC_9) THEN
        rTMR_Voted_9 := rTMR_ValA_9;
    ELSIF (rTMR_ValB_9 >= rTMR_ValA_9 AND rTMR_ValB_9 <= rTMR_ValC_9) OR (rTMR_ValB_9 <= rTMR_ValA_9 AND rTMR_ValB_9 >= rTMR_ValC_9) THEN
        rTMR_Voted_9 := rTMR_ValB_9;
    ELSE
        rTMR_Voted_9 := rTMR_ValC_9;
    END_IF;
    bTMR_Degraded_9 := FALSE;
ELSIF bTMR_FaultA_9 AND NOT bTMR_FaultB_9 AND NOT bTMR_FaultC_9 THEN
    rTMR_Voted_9 := 0.5 * (rTMR_ValB_9 + rTMR_ValC_9);
    bTMR_Degraded_9 := TRUE;
ELSIF bTMR_FaultB_9 AND NOT bTMR_FaultA_9 AND NOT bTMR_FaultC_9 THEN
    rTMR_Voted_9 := 0.5 * (rTMR_ValA_9 + rTMR_ValC_9);
    bTMR_Degraded_9 := TRUE;
ELSIF bTMR_FaultC_9 AND NOT bTMR_FaultA_9 AND NOT bTMR_FaultB_9 THEN
    rTMR_Voted_9 := 0.5 * (rTMR_ValA_9 + rTMR_ValB_9);
    bTMR_Degraded_9 := TRUE;
ELSE
    bTMR_Degraded_9 := TRUE;
END_IF;

(* --- Channel 10: Atmospheric Gas Oil Stripper Draw Flow (FT_AGODrawFlow) --- *)
rTMR_ValA_10 := rFT_AGODrawFlow_110A;
rTMR_ValB_10 := rFT_AGODrawFlow_110B;
rTMR_ValC_10 := rFT_AGODrawFlow_110C;
bTMR_DevAB_10 := ABS(rTMR_ValA_10 - rTMR_ValB_10) > rTMR_Tol_10;
bTMR_DevBC_10 := ABS(rTMR_ValB_10 - rTMR_ValC_10) > rTMR_Tol_10;
bTMR_DevCA_10 := ABS(rTMR_ValC_10 - rTMR_ValA_10) > rTMR_Tol_10;
IF bTMR_DevAB_10 THEN rTMR_TimerAB_10 := rTMR_TimerAB_10 + rTs; ELSE rTMR_TimerAB_10 := 0.0; END_IF;
IF bTMR_DevBC_10 THEN rTMR_TimerBC_10 := rTMR_TimerBC_10 + rTs; ELSE rTMR_TimerBC_10 := 0.0; END_IF;
IF bTMR_DevCA_10 THEN rTMR_TimerCA_10 := rTMR_TimerCA_10 + rTs; ELSE rTMR_TimerCA_10 := 0.0; END_IF;
IF (rTMR_TimerAB_10 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_10 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultA_10 := TRUE; END_IF;
IF (rTMR_TimerAB_10 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerBC_10 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultB_10 := TRUE; END_IF;
IF (rTMR_TimerBC_10 >= rTMR_DiscrepancyLimit_Sec) AND (rTMR_TimerCA_10 >= rTMR_DiscrepancyLimit_Sec) THEN bTMR_FaultC_10 := TRUE; END_IF;

IF NOT bTMR_FaultA_10 AND NOT bTMR_FaultB_10 AND NOT bTMR_FaultC_10 THEN
    IF (rTMR_ValA_10 >= rTMR_ValB_10 AND rTMR_ValA_10 <= rTMR_ValC_10) OR (rTMR_ValA_10 <= rTMR_ValB_10 AND rTMR_ValA_10 >= rTMR_ValC_10) THEN
        rTMR_Voted_10 := rTMR_ValA_10;
    ELSIF (rTMR_ValB_10 >= rTMR_ValA_10 AND rTMR_ValB_10 <= rTMR_ValC_10) OR (rTMR_ValB_10 <= rTMR_ValA_10 AND rTMR_ValB_10 >= rTMR_ValC_10) THEN
        rTMR_Voted_10 := rTMR_ValB_10;
    ELSE
        rTMR_Voted_10 := rTMR_ValC_10;
    END_IF;
    bTMR_Degraded_10 := FALSE;
ELSIF bTMR_FaultA_10 AND NOT bTMR_FaultB_10 AND NOT bTMR_FaultC_10 THEN
    rTMR_Voted_10 := 0.5 * (rTMR_ValB_10 + rTMR_ValC_10);
    bTMR_Degraded_10 := TRUE;
ELSIF bTMR_FaultB_10 AND NOT bTMR_FaultA_10 AND NOT bTMR_FaultC_10 THEN
    rTMR_Voted_10 := 0.5 * (rTMR_ValA_10 + rTMR_ValC_10);
    bTMR_Degraded_10 := TRUE;
ELSIF bTMR_FaultC_10 AND NOT bTMR_FaultA_10 AND NOT bTMR_FaultB_10 THEN
    rTMR_Voted_10 := 0.5 * (rTMR_ValA_10 + rTMR_ValB_10);
    bTMR_Degraded_10 := TRUE;
ELSE
    bTMR_Degraded_10 := TRUE;
END_IF;

(* Evaluate Global Sensor Health Status *)
bTMR_SensorsAllHealthy := NOT bTMR_FaultA_1 AND NOT bTMR_FaultB_1 AND NOT bTMR_FaultC_1 AND
                          NOT bTMR_FaultA_2 AND NOT bTMR_FaultB_2 AND NOT bTMR_FaultC_2 AND
                          NOT bTMR_FaultA_3 AND NOT bTMR_FaultB_3 AND NOT bTMR_FaultC_3 AND
                          NOT bTMR_FaultA_4 AND NOT bTMR_FaultB_4 AND NOT bTMR_FaultC_4 AND
                          NOT bTMR_FaultA_5 AND NOT bTMR_FaultB_5 AND NOT bTMR_FaultC_5 AND
                          NOT bTMR_FaultA_6 AND NOT bTMR_FaultB_6 AND NOT bTMR_FaultC_6 AND
                          NOT bTMR_FaultA_7 AND NOT bTMR_FaultB_7 AND NOT bTMR_FaultC_7 AND
                          NOT bTMR_FaultA_8 AND NOT bTMR_FaultB_8 AND NOT bTMR_FaultC_8 AND
                          NOT bTMR_FaultA_9 AND NOT bTMR_FaultB_9 AND NOT bTMR_FaultC_9 AND
                          NOT bTMR_FaultA_10 AND NOT bTMR_FaultB_10 AND NOT bTMR_FaultC_10;

(* ====================================================================================================================
   SECTION 2: FIRST-PRINCIPLES CYBER-PHYSICAL PROCESS OBSERVERS
   ==================================================================================================================== *)
(* --- 2.1 Overhead Acid Water Dew-Point & Neutralizing/Filming Amine Kinetics --- *)
(* Estimate water vapor partial pressure from overhead pressure and bottom stripping steam *)
rWaterVaporPartialPress_bar := rTMR_Voted_3 * 0.065;
IF rWaterVaporPartialPress_bar < 0.020 THEN
    rWaterVaporPartialPress_bar := 0.020;
END_IF;

(* Thermodynamic acidic dew point calculation using modified Antoine & HCl equilibrium correlation *)
rEstimatedAcidDewPoint_C := (3816.44 / (18.3036 - LN(rWaterVaporPartialPress_bar * 750.062))) - 227.02 + 8.5;

(* Wash water injection control to ensure condensed water phase is maintained above 5% of vapor overhead *)
IF rTT_OverheadVaporLine_129 <= (rEstimatedAcidDewPoint_C + 15.0) THEN
    rCV_OverheadWaterWash_Cmd := 45.0 + (rEstimatedAcidDewPoint_C + 15.0 - rTT_OverheadVaporLine_129) * 2.5;
ELSE
    rCV_OverheadWaterWash_Cmd := 25.0;
END_IF;
IF rCV_OverheadWaterWash_Cmd > 85.0 THEN rCV_OverheadWaterWash_Cmd := 85.0; END_IF;

(* Neutralizing Amine Closed-Loop pH Feedback Controller *)
VAR_TEMP
    rPHError : REAL;
    rAmineCmd : REAL;
END_VAR
rPHError := rSP_SourWaterPHTarget - rTMR_Voted_7;
rAminePID_Integral := rAminePID_Integral + (rPHError * rAminePID_Ki * rTs);
IF rAminePID_Integral > rAminePID_WindupLimit THEN
    rAminePID_Integral := rAminePID_WindupLimit;
ELSIF rAminePID_Integral < 0.0 THEN
    rAminePID_Integral := 0.0;
END_IF;
rAminePID_Derivative := (rPHError - rAminePID_PrevError) / rTs;
rAminePID_PrevError := rPHError;

rAmineCmd := (rPHError * rAminePID_Kp) + rAminePID_Integral + (rAminePID_Derivative * rAminePID_Kd);
IF rAmineCmd < 0.0 THEN
    rCV_NeutralizingAmine_Cmd := 5.0;
ELSIF rAmineCmd > 100.0 THEN
    rCV_NeutralizingAmine_Cmd := 100.0;
ELSE
    rCV_NeutralizingAmine_Cmd := rAmineCmd;
END_IF;

(* Filming Amine Dosing: Proportional to Total Overhead Vapor Rate + Trimmed by ER Corrosion Probe *)
IF rAT_CorrosionRateProbe_127 > 3.0 THEN
    rFilmingAmineProbeBias := 1.0 + (rAT_CorrosionRateProbe_127 - 3.0) * 0.25;
ELSE
    rFilmingAmineProbeBias := 1.0;
END_IF;
rCV_FilmingAmine_Cmd := (rCV_OverheadReflux_Cmd * 0.45 + rFT_CrudeFeedCharge_112 * 0.08) * rFilmingAmineProbeBias;
IF rCV_FilmingAmine_Cmd < 10.0 THEN rCV_FilmingAmine_Cmd := 10.0; END_IF;
IF rCV_FilmingAmine_Cmd > 90.0 THEN rCV_FilmingAmine_Cmd := 90.0; END_IF;

(* --- 2.2 Desalter Electrostatic Emulsion Interface & Brine Dump Cascade --- *)
VAR_TEMP
    rDesaltErr : REAL;
    rBrineCmd : REAL;
END_VAR
rDesaltErr := rTMR_Voted_6 - 45.0; (* Setpoint fixed at 45% interface *)
rDesaltPI_Integral := rDesaltPI_Integral + (rDesaltErr * rDesaltPI_Ki * rTs);
IF rDesaltPI_Integral > 80.0 THEN
    rDesaltPI_Integral := 80.0;
ELSIF rDesaltPI_Integral < 0.0 THEN
    rDesaltPI_Integral := 0.0;
END_IF;

rBrineCmd := 40.0 + (rDesaltErr * rDesaltPI_Kp) + rDesaltPI_Integral;
IF rBrineCmd < 5.0 THEN
    rCV_DesalterBrine_Cmd := 5.0;
ELSIF rBrineCmd > 95.0 THEN
    rCV_DesalterBrine_Cmd := 95.0;
ELSE
    rCV_DesalterBrine_Cmd := rBrineCmd;
END_IF;

(* Desalter Salt Extraction Efficiency Model *)
IF bDesalterGridEnergized THEN
    rDesalterSaltRemovalEff_Pct := 96.5 - (rTMR_Voted_6 - 45.0) * 0.35;
    IF rDesalterSaltRemovalEff_Pct > 99.0 THEN rDesalterSaltRemovalEff_Pct := 99.0; END_IF;
    IF rDesalterSaltRemovalEff_Pct < 85.0 THEN rDesalterSaltRemovalEff_Pct := 85.0; END_IF;
ELSE
    rDesalterSaltRemovalEff_Pct := 42.0; (* Severe degradation without electrostatic coalescence *)
END_IF;

(* --- 2.3 Fired Heater 4-Pass Dynamic Balancing & Two-Phase Flash Vaporization Observer --- *)
rFurnacePassTotal_m3h := rFT_FurnacePassFlow_1_116 + rFT_FurnacePassFlow_2_117 + rFT_FurnacePassFlow_3_118 + rFT_FurnacePassFlow_4_119;
rFurnacePassMean_m3h := rFurnacePassTotal_m3h * 0.25;

IF rFurnacePassMean_m3h > 10.0 THEN
    rFurnacePassDev_1 := rFurnacePassMean_m3h - rFT_FurnacePassFlow_1_116;
    rFurnacePassDev_2 := rFurnacePassMean_m3h - rFT_FurnacePassFlow_2_117;
    rFurnacePassDev_3 := rFurnacePassMean_m3h - rFT_FurnacePassFlow_3_118;
    rFurnacePassDev_4 := rFurnacePassMean_m3h - rFT_FurnacePassFlow_4_119;

    rFurnacePassInt_1 := rFurnacePassInt_1 + (rFurnacePassDev_1 * rFurnacePassGain_Ki * rTs);
    rFurnacePassInt_2 := rFurnacePassInt_2 + (rFurnacePassDev_2 * rFurnacePassGain_Ki * rTs);
    rFurnacePassInt_3 := rFurnacePassInt_3 + (rFurnacePassDev_3 * rFurnacePassGain_Ki * rTs);
    rFurnacePassInt_4 := rFurnacePassInt_4 + (rFurnacePassDev_4 * rFurnacePassGain_Ki * rTs);

    rCV_FurnacePassTrim1_Cmd := 50.0 + (rFurnacePassDev_1 * rFurnacePassGain_Kp) + rFurnacePassInt_1;
    rCV_FurnacePassTrim2_Cmd := 50.0 + (rFurnacePassDev_2 * rFurnacePassGain_Kp) + rFurnacePassInt_2;
    rCV_FurnacePassTrim3_Cmd := 50.0 + (rFurnacePassDev_3 * rFurnacePassGain_Kp) + rFurnacePassInt_3;
    rCV_FurnacePassTrim4_Cmd := 50.0 + (rFurnacePassDev_4 * rFurnacePassGain_Kp) + rFurnacePassInt_4;
ELSE
    rCV_FurnacePassTrim1_Cmd := 50.0;
    rCV_FurnacePassTrim2_Cmd := 50.0;
    rCV_FurnacePassTrim3_Cmd := 50.0;
    rCV_FurnacePassTrim4_Cmd := 50.0;
END_IF;

(* Equilibrium Flash Vaporization (EFV) Two-Phase Quality in Transfer Line *)
IF rTT_FurnaceCoilOutlet_115 > 320.0 THEN
    rFurnaceTwoPhaseVaporFrac := (rTT_FurnaceCoilOutlet_115 - 320.0) / (375.0 - 320.0) * 58.0;
    IF rFurnaceTwoPhaseVaporFrac > 65.0 THEN rFurnaceTwoPhaseVaporFrac := 65.0; END_IF;
ELSE
    rFurnaceTwoPhaseVaporFrac := 0.0;
END_IF;

(* --- 2.4 Side-Stream Strippers Mass & Energy Hydraulics & Inferred Cut Points --- *)
(* Inferred Kerosene Flash Point (Pensky-Martens closed-cup correlation) *)
rInferredKeroFlashPoint_C := 0.22 * rTT_TopPumparoundDraw_121 + 0.18 * rTT_FlashZoneTemp_102A - 0.00015 * rTMR_Voted_8 + 12.0;

(* Inferred Light Diesel ASTM D86 95% Cut Point *)
rInferredDieselD86_95_C := 0.72 * rTT_MidPumparoundDraw_124 + 0.28 * rTMR_Voted_2 - 0.00022 * rTMR_Voted_9 + 45.0;

(* --- 2.5 Dual Pumparounds Enthalpy Extraction & Overflash Reflux Ratio --- *)
(* Top Pumparound Duty [kW]: Q = m_dot * Cp * delta_T *)
rTopPumparoundDuty_MW := (rFT_TopPumparoundFlow_123 * rDensity_TPA_kg_m3 / 3600.0) * 
                         rCp_TPA_kJ_kgK * 
                         (rTT_TopPumparoundDraw_121 - rTT_TopPumparoundReturn_122);
IF rTopPumparoundDuty_MW < 0.0 THEN rTopPumparoundDuty_MW := 0.0; END_IF;

(* Middle Pumparound Duty [kW] *)
rMidPumparoundDuty_MW := (rFT_MidPumparoundFlow_126 * rDensity_MPA_kg_m3 / 3600.0) * 
                         rCp_MPA_kJ_kgK * 
                         (rTT_MidPumparoundDraw_124 - rTT_MidPumparoundReturn_125);
IF rMidPumparoundDuty_MW < 0.0 THEN rMidPumparoundDuty_MW := 0.0; END_IF;

(* Overflash Reflux Percentage of Crude Feed *)
IF rFT_CrudeFeedCharge_112 > 10.0 THEN
    rOverflashRefluxRatio_Calc := (rFT_OverflashFlow_120 / rFT_CrudeFeedCharge_112) * 100.0;
ELSE
    rOverflashRefluxRatio_Calc := 0.0;
END_IF;

(* Column Internal Reflux Ratio L/D *)
IF rCV_LightNaphthaRundown_Cmd > 5.0 THEN
    rColumnInternalRefluxRatio := rCV_OverheadReflux_Cmd / rCV_LightNaphthaRundown_Cmd;
ELSE
    rColumnInternalRefluxRatio := 1.5;
END_IF;

(* ====================================================================================================================
   SECTION 3: CYBER-PHYSICAL DISCRETE 8x8 STATE-SPACE PROPAGATION (x[k+1] = A*x[k] + B*u[k] + Bd*d[k])
   ==================================================================================================================== *)
(* Reconstruct continuous state deviation vector from voted sensor channels *)
vX[1] := rTT_OverheadVaporLine_129 - 110.0;     (* Tray 50 temperature deviation [deg C] *)
vX[2] := rTMR_Voted_2 - rSP_FurnaceCOTTarget;   (* Flash zone temperature deviation [deg C] *)
vX[3] := rTMR_Voted_3 - rSP_OverheadPressTarget;(* Column top pressure deviation [bar] *)
vX[4] := rTMR_Voted_4 - 50.0;                   (* Accumulator level deviation [%] *)
vX[5] := rFT_OverflashFlow_120 - (rFT_CrudeFeedCharge_112 * (rSP_OverflashTargetRatio / 100.0)); (* Overflash [m3/h] *)
vX[6] := rTMR_Voted_5 - 50.0;                   (* Column bottom residue level deviation [%] *)
vX[7] := rTopPumparoundDuty_MW - rSP_TPA_DutyTarget_MW; (* TPA duty deviation [kW] *)
vX[8] := rTMR_Voted_6 - 45.0;                   (* Desalter emulsion interface deviation [%] *)

(* Actuator command deviation vector *)
vU[1] := rCV_OverheadReflux_Cmd - 50.0;
vU[2] := rCV_HeaterFuelGas_Cmd - 50.0;
vU[3] := rCV_OverheadOffgas_Cmd - 50.0;
vU[4] := rCV_LightNaphthaRundown_Cmd - 50.0;
vU[5] := rCV_TopPumparound_Cmd - 50.0;
vU[6] := rCV_MidPumparound_Cmd - 50.0;
vU[7] := rCV_BottomResidue_Cmd - 50.0;
vU[8] := rCV_DesalterBrine_Cmd - 50.0;

(* Disturbance vector *)
vDist[1] := rFT_CrudeFeedCharge_112 - rSP_CrudeThroughputTarget;
vDist[2] := rDT_CrudeDensity_113 - 850.0;
vDist[3] := 25.0 - 20.0; (* Ambient temperature baseline shift *)
vDist[4] := rTT_CrudePreheatOutlet_114 - 280.0;

(* State Propagation Matrix Equations *)
FOR iState_Idx := 1 TO 8 DO
    vX_next[iState_Idx] := 0.0;
    FOR jState_Idx := 1 TO 8 DO
        vX_next[iState_Idx] := vX_next[iState_Idx] + (mA[iState_Idx, jState_Idx] * vX[jState_Idx]);
    END_FOR;
    FOR kInput_Idx := 1 TO 8 DO
        vX_next[iState_Idx] := vX_next[iState_Idx] + (mB[iState_Idx, kInput_Idx] * vU[kInput_Idx]);
    END_FOR;
    FOR kInput_Idx := 1 TO 4 DO
        vX_next[iState_Idx] := vX_next[iState_Idx] + (mBd[iState_Idx, kInput_Idx] * vDist[kInput_Idx]);
    END_FOR;
END_FOR;

(* Plant Output Estimation y = C*x + D*u *)
FOR iState_Idx := 1 TO 8 DO
    vY_est[iState_Idx] := 0.0;
    FOR jState_Idx := 1 TO 8 DO
        vY_est[iState_Idx] := vY_est[iState_Idx] + (mC[iState_Idx, jState_Idx] * vX[jState_Idx]);
    END_FOR;
END_FOR;

(* ====================================================================================================================
   SECTION 4: RECEDING-HORIZON MPC OPTIMIZATION WITH PROJECTED GRADIENT DESCENT (PGD)
   ==================================================================================================================== *)
IF bAutoMPC_Permissive AND (iCurrentState = 7 OR iCurrentState = 8) AND NOT bEmergencyTripActive THEN
    bMPC_ClosedLoopActive := TRUE;

    (* Initialize candidate vector with current actuator values *)
    FOR kInput_Idx := 1 TO 8 DO
        vU_opt[kInput_Idx] := vU[kInput_Idx];
    END_FOR;

    (* Projected Gradient Descent Solver (12 Iterations) *)
    FOR iMPC_Iter := 1 TO 12 DO
        (* Calculate gradient: grad_J = R*(u - u_target) + S*(u - u_prev) + B^T * Q * (x_next - x_ref) *)
        FOR kInput_Idx := 1 TO 8 DO
            vGrad[kInput_Idx] := (mR[kInput_Idx, kInput_Idx] * (vU_opt[kInput_Idx] - (vU_target[kInput_Idx] - 50.0))) +
                                 (mS[kInput_Idx, kInput_Idx] * (vU_opt[kInput_Idx] - vU_prev[kInput_Idx]));
            
            FOR iState_Idx := 1 TO 8 DO
                vGrad[kInput_Idx] := vGrad[kInput_Idx] + 
                                     (mB[iState_Idx, kInput_Idx] * mQ[iState_Idx, iState_Idx] * (vX_next[iState_Idx] - vX_ref[iState_Idx]));
            END_FOR;

            (* Gradient update step *)
            vU_opt[kInput_Idx] := vU_opt[kInput_Idx] - (rStepSize_PGD * vGrad[kInput_Idx]);

            (* Projection onto physical box boundaries [u_min - 50, u_max - 50] *)
            IF vU_opt[kInput_Idx] < (vU_min[kInput_Idx] - 50.0) THEN
                vU_opt[kInput_Idx] := vU_min[kInput_Idx] - 50.0;
            ELSIF vU_opt[kInput_Idx] > (vU_max[kInput_Idx] - 50.0) THEN
                vU_opt[kInput_Idx] := vU_max[kInput_Idx] - 50.0;
            END_IF;

            (* Projection onto dynamic slew rate limiters *)
            IF (vU_opt[kInput_Idx] - vU_prev[kInput_Idx]) > vDeltaU_max[kInput_Idx] THEN
                vU_opt[kInput_Idx] := vU_prev[kInput_Idx] + vDeltaU_max[kInput_Idx];
            ELSIF (vU_opt[kInput_Idx] - vU_prev[kInput_Idx]) < -vDeltaU_max[kInput_Idx] THEN
                vU_opt[kInput_Idx] := vU_prev[kInput_Idx] - vDeltaU_max[kInput_Idx];
            END_IF;
        END_FOR;
    END_FOR;

    (* Apply MPC Optimized Control Demands *)
    rCV_OverheadReflux_Cmd := vU_opt[1] + 50.0;
    rCV_HeaterFuelGas_Cmd := vU_opt[2] + 50.0;
    rCV_OverheadOffgas_Cmd := vU_opt[3] + 50.0;
    rCV_LightNaphthaRundown_Cmd := vU_opt[4] + 50.0;
    rCV_TopPumparound_Cmd := vU_opt[5] + 50.0;
    rCV_MidPumparound_Cmd := vU_opt[6] + 50.0;
    rCV_BottomResidue_Cmd := vU_opt[7] + 50.0;
    rCV_DesalterBrine_Cmd := vU_opt[8] + 50.0;

    (* Store previous control vector for rate-of-change penalties *)
    FOR kInput_Idx := 1 TO 8 DO
        vU_prev[kInput_Idx] := vU_opt[kInput_Idx];
    END_FOR;
ELSE
    bMPC_ClosedLoopActive := FALSE;
    (* In manual/startup FSM modes, MPC tracks actual actuator outputs bumplessly *)
    FOR kInput_Idx := 1 TO 8 DO
        vU_prev[kInput_Idx] := vU[kInput_Idx];
        vU_opt[kInput_Idx] := vU[kInput_Idx];
    END_FOR;
END_IF;

(* ====================================================================================================================
   SECTION 5: DETERMINISTIC 12-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
   ==================================================================================================================== *)
rTimer_FSM_State := rTimer_FSM_State + rTs;

(* Emergency Interlock Override Check *)
IF bEmergencyTripCmd OR bEmergencyTripActive THEN
    iCurrentState := 10; (* Force state to EMERGENCY_COLUMN_DEPRESSURIZATION *)
END_IF;

CASE iCurrentState OF
    0: (* STATE_00: NITROGEN_INERTING_PURGE *)
        sCurrentStateName := 'NITROGEN_INERTING_PURGE';
        rCV_OverheadReflux_Cmd := 0.0;
        rCV_HeaterFuelGas_Cmd := 0.0;
        rCV_OverheadOffgas_Cmd := 35.0; (* Purge vent open to gas flare header *)
        rCV_LightNaphthaRundown_Cmd := 0.0;
        rCV_HeavyNaphthaDraw_Cmd := 0.0;
        rCV_KeroDraw_Cmd := 0.0;
        rCV_DieselDraw_Cmd := 0.0;
        rCV_AGODraw_Cmd := 0.0;
        rCV_TopPumparound_Cmd := 0.0;
        rCV_MidPumparound_Cmd := 0.0;
        rCV_BottomResidue_Cmd := 0.0;
        rCV_DesalterBrine_Cmd := 0.0;
        rCV_EmergencyDepressFlare_Cmd := 0.0;

        (* Check oxygen displacement and positive nitrogen pad pressure *)
        IF (rTimer_FSM_State >= 18.0) AND (rTMR_Voted_3 >= 0.25) AND bEnable THEN
            bPermissive_WarmCirc := TRUE;
            iCurrentState := 1;
            rTimer_FSM_State := 0.0;
        END_IF;

    1: (* STATE_01: WARM_CIRCULATION *)
        sCurrentStateName := 'WARM_CIRCULATION';
        (* Circulate light gas oil flush to warm column and preheat train *)
        rCV_HeaterFuelGas_Cmd := 15.0; (* Pilot and low firing to maintain COT ~ 125 deg C *)
        rCV_BottomResidue_Cmd := 25.0; (* Bottom circulation pump return *)
        rCV_TopPumparound_Cmd := 20.0;
        rCV_MidPumparound_Cmd := 20.0;
        rCV_OverheadOffgas_Cmd := 20.0;

        IF (rTimer_FSM_State >= 25.0) AND (rTT_CrudePreheatOutlet_114 >= 110.0) AND bEnable THEN
            bPermissive_CrudeCutIn := TRUE;
            iCurrentState := 2;
            rTimer_FSM_State := 0.0;
        END_IF;

    2: (* STATE_02: CRUDE_OIL_CUT_IN *)
        sCurrentStateName := 'CRUDE_OIL_CUT_IN';
        (* Switch crude charge header valve, fill desalter, establish interface *)
        rCV_HeaterFuelGas_Cmd := 20.0;
        rCV_BottomResidue_Cmd := 35.0;
        rCV_DesalterBrine_Cmd := 40.0;

        IF (rTimer_FSM_State >= 20.0) AND (rFT_CrudeFeedCharge_112 >= 50.0) AND (rTMR_Voted_6 >= 35.0) THEN
            bPermissive_HeaterRamp := TRUE;
            iCurrentState := 3;
            rTimer_FSM_State := 0.0;
        END_IF;

    3: (* STATE_03: FIRED_HEATER_RAMP_UP *)
        sCurrentStateName := 'FIRED_HEATER_RAMP_UP';
        (* Ramp furnace firing at 25 deg C / hr to target COT 365 deg C *)
        IF rCV_HeaterFuelGas_Cmd < 55.0 THEN
            rCV_HeaterFuelGas_Cmd := rCV_HeaterFuelGas_Cmd + (0.05 * rTs);
        END_IF;
        rCV_BottomResidue_Cmd := 45.0;
        rCV_OverheadOffgas_Cmd := 28.0;

        IF (rTMR_Voted_2 >= 340.0) AND (rTT_FurnaceCoilOutlet_115 >= 350.0) THEN
            bPermissive_HydraulicEquil := TRUE;
            iCurrentState := 4;
            rTimer_FSM_State := 0.0;
        END_IF;

    4: (* STATE_04: TRAY_HYDRAULIC_EQUILIBRATION *)
        sCurrentStateName := 'TRAY_HYDRAULIC_EQUILIBRATION';
        (* Establish overhead condensation and top tray reflux flow to wet trays *)
        rCV_OverheadReflux_Cmd := 35.0;
        rCV_LightNaphthaRundown_Cmd := 20.0;
        rCV_BottomResidue_Cmd := 50.0;
        rCV_OverheadOffgas_Cmd := 30.0;

        (* Check tray pressure drop to ensure no weeping or flooding *)
        IF (rTimer_FSM_State >= 20.0) AND (rTMR_Voted_1 >= 0.12) AND (rTMR_Voted_1 <= 0.45) AND (rTMR_Voted_4 >= 40.0) THEN
            bPermissive_SideDrawCutIn := TRUE;
            iCurrentState := 5;
            rTimer_FSM_State := 0.0;
        END_IF;

    5: (* STATE_05: SIDE_DRAW_CUT_IN *)
        sCurrentStateName := 'SIDE_DRAW_CUT_IN';
        (* Sequentially open side-stream strippers: HN, Kero, Diesel, AGO *)
        rCV_HeavyNaphthaDraw_Cmd := 25.0;
        rCV_KeroDraw_Cmd := 35.0;
        rCV_DieselDraw_Cmd := 45.0;
        rCV_AGODraw_Cmd := 30.0;
        rCV_OverheadReflux_Cmd := 45.0;

        IF (rTimer_FSM_State >= 20.0) AND (rTMR_Voted_8 >= 15000.0) AND (rTMR_Voted_9 >= 25000.0) THEN
            bPermissive_PA_Opt := TRUE;
            iCurrentState := 6;
            rTimer_FSM_State := 0.0;
        END_IF;

    6: (* STATE_06: PUMPAROUND_OPTIMIZATION *)
        sCurrentStateName := 'PUMPAROUND_OPTIMIZATION';
        (* Ramp Top Pumparound and Middle Pumparound duties *)
        rCV_TopPumparound_Cmd := 48.0;
        rCV_MidPumparound_Cmd := 52.0;

        IF (rTimer_FSM_State >= 15.0) AND (rOverflashRefluxRatio_Calc >= 2.0) AND (rTopPumparoundDuty_MW >= 5000.0) THEN
            bPermissive_SteadyState := TRUE;
            iCurrentState := 7;
            rTimer_FSM_State := 0.0;
        END_IF;

    7: (* STATE_07: STEADY_STATE_FRACTIONATING *)
        sCurrentStateName := 'STEADY_STATE_FRACTIONATING';
        (* Normal multivariable MPC Closed-Loop Production *)
        (* Handled by Section 4 MPC when bAutoMPC_Permissive is active *)
        IF NOT bAutoMPC_Permissive THEN
            (* Base regulatory fallback setpoints *)
            rCV_OverheadReflux_Cmd := 52.0;
            rCV_HeaterFuelGas_Cmd := 58.0;
            rCV_OverheadOffgas_Cmd := 32.0;
            rCV_LightNaphthaRundown_Cmd := 45.0;
            rCV_HeavyNaphthaDraw_Cmd := 38.0;
            rCV_KeroDraw_Cmd := 55.0;
            rCV_DieselDraw_Cmd := 65.0;
            rCV_AGODraw_Cmd := 42.0;
            rCV_TopPumparound_Cmd := 55.0;
            rCV_MidPumparound_Cmd := 58.0;
            rCV_BottomResidue_Cmd := 52.0;
        END_IF;

    8: (* STATE_08: SWING_FEED_CRUDE_TRANSITION *)
        sCurrentStateName := 'SWING_FEED_CRUDE_TRANSITION';
        (* Dynamic feedforward transition for density/API shift *)
        IF ABS(rDT_CrudeDensity_113 - 850.0) < 5.0 AND (rTimer_FSM_State >= 45.0) THEN
            iCurrentState := 7; (* Return to steady-state fractionating *)
            rTimer_FSM_State := 0.0;
        END_IF;

    9: (* STATE_09: CONTROLLED_RAMP_DOWN *)
        sCurrentStateName := 'CONTROLLED_RAMP_DOWN';
        (* Orderly reduction of throughput and furnace firing *)
        rCV_HeaterFuelGas_Cmd := 25.0;
        rCV_HeavyNaphthaDraw_Cmd := 10.0;
        rCV_KeroDraw_Cmd := 10.0;
        rCV_DieselDraw_Cmd := 15.0;
        rCV_AGODraw_Cmd := 10.0;
        rCV_TopPumparound_Cmd := 25.0;
        rCV_MidPumparound_Cmd := 25.0;

        IF (rTimer_FSM_State >= 60.0) AND (rTT_FurnaceCoilOutlet_115 <= 250.0) THEN
            iCurrentState := 1; (* Transition to warm circulation flush *)
            rTimer_FSM_State := 0.0;
        END_IF;

    10: (* STATE_10: EMERGENCY_COLUMN_DEPRESSURIZATION (Hot Vapor Flaring Trip) *)
        sCurrentStateName := 'EMERGENCY_DEPRESS_FLARING';
        bEmergencyTripActive := TRUE;
        (* Critical Safety Postures *)
        rCV_HeaterFuelGas_Cmd := 0.0;          (* Trip fuel gas shutoff valve tight shut *)
        rCV_EmergencyDepressFlare_Cmd := 100.0; (* Full open hot vapor blowdown to flare *)
        rCV_OverheadOffgas_Cmd := 100.0;        (* Dump offgas to flare header *)
        rCV_OverheadReflux_Cmd := 0.0;          (* Stop reflux pumps to prevent tower overfill *)
        rCV_LightNaphthaRundown_Cmd := 0.0;     (* Isolate product rundown to tank farm *)
        rCV_HeavyNaphthaDraw_Cmd := 0.0;
        rCV_KeroDraw_Cmd := 0.0;
        rCV_DieselDraw_Cmd := 0.0;
        rCV_AGODraw_Cmd := 0.0;
        rCV_TopPumparound_Cmd := 0.0;           (* Trip pumparound pumps *)
        rCV_MidPumparound_Cmd := 0.0;
        rCV_BottomResidue_Cmd := 0.0;           (* Isolate hot residue to prevent air ingress *)
        rCV_NeutralizingAmine_Cmd := 0.0;
        rCV_FilmingAmine_Cmd := 0.0;

        IF bReset AND NOT bEmergencyTripCmd THEN
            iCurrentState := 11; (* Proceed to E-Stop isolation for manual inspection *)
            rTimer_FSM_State := 0.0;
        END_IF;

    11: (* STATE_11: TOTAL_E_STOP_ISOLATION *)
        sCurrentStateName := 'TOTAL_E_STOP_ISOLATION';
        rCV_EmergencyDepressFlare_Cmd := 0.0; (* Close flare valve once pressure < 0.2 bar *)
        rCV_HeaterFuelGas_Cmd := 0.0;
        rCV_OverheadOffgas_Cmd := 15.0;       (* Nitrogen blanket pad *)
        rCV_OverheadReflux_Cmd := 0.0;
        rCV_BottomResidue_Cmd := 0.0;

        IF bReset AND bEnable THEN
            iCurrentState := 0; (* Re-enter nitrogen inerting purge *)
            rTimer_FSM_State := 0.0;
            bEmergencyTripActive := FALSE;
        END_IF;
ELSE
    iCurrentState := 10; (* Unrecognized state safety fallback *)
END_CASE;

(* ====================================================================================================================
   SECTION 6: ACTUATOR OUTPUT LIMITING, RATE CLAMPING & BUMPLESS TRANSFER
   ==================================================================================================================== *)
(* Clamp all control valve positions to physical boundaries [0.0% to 100.0%] *)
IF rCV_OverheadReflux_Cmd < 0.0 THEN rCV_OverheadReflux_Cmd := 0.0; ELSIF rCV_OverheadReflux_Cmd > 100.0 THEN rCV_OverheadReflux_Cmd := 100.0; END_IF;
IF rCV_HeaterFuelGas_Cmd < 0.0 THEN rCV_HeaterFuelGas_Cmd := 0.0; ELSIF rCV_HeaterFuelGas_Cmd > 100.0 THEN rCV_HeaterFuelGas_Cmd := 100.0; END_IF;
IF rCV_OverheadOffgas_Cmd < 0.0 THEN rCV_OverheadOffgas_Cmd := 0.0; ELSIF rCV_OverheadOffgas_Cmd > 100.0 THEN rCV_OverheadOffgas_Cmd := 100.0; END_IF;
IF rCV_LightNaphthaRundown_Cmd < 0.0 THEN rCV_LightNaphthaRundown_Cmd := 0.0; ELSIF rCV_LightNaphthaRundown_Cmd > 100.0 THEN rCV_LightNaphthaRundown_Cmd := 100.0; END_IF;
IF rCV_HeavyNaphthaDraw_Cmd < 0.0 THEN rCV_HeavyNaphthaDraw_Cmd := 0.0; ELSIF rCV_HeavyNaphthaDraw_Cmd > 100.0 THEN rCV_HeavyNaphthaDraw_Cmd := 100.0; END_IF;
IF rCV_KeroDraw_Cmd < 0.0 THEN rCV_KeroDraw_Cmd := 0.0; ELSIF rCV_KeroDraw_Cmd > 100.0 THEN rCV_KeroDraw_Cmd := 100.0; END_IF;
IF rCV_DieselDraw_Cmd < 0.0 THEN rCV_DieselDraw_Cmd := 0.0; ELSIF rCV_DieselDraw_Cmd > 100.0 THEN rCV_DieselDraw_Cmd := 100.0; END_IF;
IF rCV_AGODraw_Cmd < 0.0 THEN rCV_AGODraw_Cmd := 0.0; ELSIF rCV_AGODraw_Cmd > 100.0 THEN rCV_AGODraw_Cmd := 100.0; END_IF;
IF rCV_TopPumparound_Cmd < 0.0 THEN rCV_TopPumparound_Cmd := 0.0; ELSIF rCV_TopPumparound_Cmd > 100.0 THEN rCV_TopPumparound_Cmd := 100.0; END_IF;
IF rCV_MidPumparound_Cmd < 0.0 THEN rCV_MidPumparound_Cmd := 0.0; ELSIF rCV_MidPumparound_Cmd > 100.0 THEN rCV_MidPumparound_Cmd := 100.0; END_IF;
IF rCV_BottomResidue_Cmd < 0.0 THEN rCV_BottomResidue_Cmd := 0.0; ELSIF rCV_BottomResidue_Cmd > 100.0 THEN rCV_BottomResidue_Cmd := 100.0; END_IF;
IF rCV_DesalterBrine_Cmd < 0.0 THEN rCV_DesalterBrine_Cmd := 0.0; ELSIF rCV_DesalterBrine_Cmd > 100.0 THEN rCV_DesalterBrine_Cmd := 100.0; END_IF;
IF rCV_EmergencyDepressFlare_Cmd < 0.0 THEN rCV_EmergencyDepressFlare_Cmd := 0.0; ELSIF rCV_EmergencyDepressFlare_Cmd > 100.0 THEN rCV_EmergencyDepressFlare_Cmd := 100.0; END_IF;
IF rCV_FurnacePassTrim1_Cmd < 0.0 THEN rCV_FurnacePassTrim1_Cmd := 0.0; ELSIF rCV_FurnacePassTrim1_Cmd > 100.0 THEN rCV_FurnacePassTrim1_Cmd := 100.0; END_IF;
IF rCV_FurnacePassTrim2_Cmd < 0.0 THEN rCV_FurnacePassTrim2_Cmd := 0.0; ELSIF rCV_FurnacePassTrim2_Cmd > 100.0 THEN rCV_FurnacePassTrim2_Cmd := 100.0; END_IF;
IF rCV_FurnacePassTrim3_Cmd < 0.0 THEN rCV_FurnacePassTrim3_Cmd := 0.0; ELSIF rCV_FurnacePassTrim3_Cmd > 100.0 THEN rCV_FurnacePassTrim3_Cmd := 100.0; END_IF;
IF rCV_FurnacePassTrim4_Cmd < 0.0 THEN rCV_FurnacePassTrim4_Cmd := 0.0; ELSIF rCV_FurnacePassTrim4_Cmd > 100.0 THEN rCV_FurnacePassTrim4_Cmd := 100.0; END_IF;

(* Actuator Saturation Bit Diagnostic Word *)
dwAlarmWord4_Actuators := 16#00000000;
IF (rCV_OverheadReflux_Cmd >= 98.0) OR (rCV_OverheadReflux_Cmd <= 2.0) THEN dwAlarmWord4_Actuators := dwAlarmWord4_Actuators OR 16#00000001; END_IF;
IF (rCV_HeaterFuelGas_Cmd >= 98.0) OR (rCV_HeaterFuelGas_Cmd <= 2.0) THEN dwAlarmWord4_Actuators := dwAlarmWord4_Actuators OR 16#00000002; END_IF;
IF (rCV_OverheadOffgas_Cmd >= 98.0) OR (rCV_OverheadOffgas_Cmd <= 2.0) THEN dwAlarmWord4_Actuators := dwAlarmWord4_Actuators OR 16#00000004; END_IF;
IF (rCV_LightNaphthaRundown_Cmd >= 98.0) OR (rCV_LightNaphthaRundown_Cmd <= 2.0) THEN dwAlarmWord4_Actuators := dwAlarmWord4_Actuators OR 16#00000008; END_IF;
IF (rCV_TopPumparound_Cmd >= 98.0) OR (rCV_TopPumparound_Cmd <= 2.0) THEN dwAlarmWord4_Actuators := dwAlarmWord4_Actuators OR 16#00000010; END_IF;
IF (rCV_MidPumparound_Cmd >= 98.0) OR (rCV_MidPumparound_Cmd <= 2.0) THEN dwAlarmWord4_Actuators := dwAlarmWord4_Actuators OR 16#00000020; END_IF;
IF (rCV_BottomResidue_Cmd >= 98.0) OR (rCV_BottomResidue_Cmd <= 2.0) THEN dwAlarmWord4_Actuators := dwAlarmWord4_Actuators OR 16#00000040; END_IF;
IF (rCV_DesalterBrine_Cmd >= 98.0) OR (rCV_DesalterBrine_Cmd <= 2.0) THEN dwAlarmWord4_Actuators := dwAlarmWord4_Actuators OR 16#00000080; END_IF;

(* ====================================================================================================================
   SECTION 7: ISA-18.2 MULTI-TIERED ALARM HIERARCHY & BIT-PACKED STATUS WORDS
   ==================================================================================================================== *)
(* Rate of Change (ROC) Calculations *)
rROC_FZ_Temp := ABS(rTMR_Voted_2 - rPrev_FZ_Temp) / rTs;
rROC_OvhdPress := ABS(rTMR_Voted_3 - rPrev_OvhdPress) / rTs;
rPrev_FZ_Temp := rTMR_Voted_2;
rPrev_OvhdPress := rTMR_Voted_3;
IF rROC_FZ_Temp > rLim_ROC_FZ_Temp THEN bAlarm_ROC_FZ_Temp := TRUE; END_IF;
IF rROC_OvhdPress > rLim_ROC_OvhdPress THEN bAlarm_ROC_OvhdPress := TRUE; END_IF;

(* --- Flash Zone Temperature Alarms (ISA-18.2 Deadband Hysteresis) --- *)
IF rTMR_Voted_2 >= rLim_FZ_Temp_HH THEN
    bAlarm_FZ_Temp_HH := TRUE;
ELSIF rTMR_Voted_2 < (rLim_FZ_Temp_HH - rDeadband_FZ_Temp) THEN
    bAlarm_FZ_Temp_HH := FALSE;
END_IF;

IF rTMR_Voted_2 >= rLim_FZ_Temp_H THEN
    bAlarm_FZ_Temp_H := TRUE;
ELSIF rTMR_Voted_2 < (rLim_FZ_Temp_H - rDeadband_FZ_Temp) THEN
    bAlarm_FZ_Temp_H := FALSE;
END_IF;

IF rTMR_Voted_2 <= rLim_FZ_Temp_LL THEN
    bAlarm_FZ_Temp_LL := TRUE;
ELSIF rTMR_Voted_2 > (rLim_FZ_Temp_LL + rDeadband_FZ_Temp) THEN
    bAlarm_FZ_Temp_LL := FALSE;
END_IF;

IF rTMR_Voted_2 <= rLim_FZ_Temp_L THEN
    bAlarm_FZ_Temp_L := TRUE;
ELSIF rTMR_Voted_2 > (rLim_FZ_Temp_L + rDeadband_FZ_Temp) THEN
    bAlarm_FZ_Temp_L := FALSE;
END_IF;

(* --- Column Overhead Pressure Alarms --- *)
IF rTMR_Voted_3 >= rLim_OvhdPress_HH THEN
    bAlarm_OvhdPress_HH := TRUE;
ELSIF rTMR_Voted_3 < (rLim_OvhdPress_HH - rDeadband_OvhdPress) THEN
    bAlarm_OvhdPress_HH := FALSE;
END_IF;

IF rTMR_Voted_3 >= rLim_OvhdPress_H THEN
    bAlarm_OvhdPress_H := TRUE;
ELSIF rTMR_Voted_3 < (rLim_OvhdPress_H - rDeadband_OvhdPress) THEN
    bAlarm_OvhdPress_H := FALSE;
END_IF;

IF rTMR_Voted_3 <= rLim_OvhdPress_LL THEN
    bAlarm_OvhdPress_LL := TRUE;
ELSIF rTMR_Voted_3 > (rLim_OvhdPress_LL + rDeadband_OvhdPress) THEN
    bAlarm_OvhdPress_LL := FALSE;
END_IF;

IF rTMR_Voted_3 <= rLim_OvhdPress_L THEN
    bAlarm_OvhdPress_L := TRUE;
ELSIF rTMR_Voted_3 > (rLim_OvhdPress_L + rDeadband_OvhdPress) THEN
    bAlarm_OvhdPress_L := FALSE;
END_IF;

(* --- Overhead Accumulator Level Alarms --- *)
IF rTMR_Voted_4 >= rLim_AccumLevel_HH THEN
    bAlarm_AccumLevel_HH := TRUE;
ELSIF rTMR_Voted_4 < (rLim_AccumLevel_HH - rDeadband_AccumLevel) THEN
    bAlarm_AccumLevel_HH := FALSE;
END_IF;

IF rTMR_Voted_4 <= rLim_AccumLevel_LL THEN
    bAlarm_AccumLevel_LL := TRUE;
ELSIF rTMR_Voted_4 > (rLim_AccumLevel_LL + rDeadband_AccumLevel) THEN
    bAlarm_AccumLevel_LL := FALSE;
END_IF;

(* --- Column Bottom Residue Level Alarms --- *)
IF rTMR_Voted_5 >= rLim_BtmLevel_HH THEN
    bAlarm_BtmLevel_HH := TRUE;
ELSIF rTMR_Voted_5 < (rLim_BtmLevel_HH - rDeadband_BtmLevel) THEN
    bAlarm_BtmLevel_HH := FALSE;
END_IF;

IF rTMR_Voted_5 <= rLim_BtmLevel_LL THEN
    bAlarm_BtmLevel_LL := TRUE;
ELSIF rTMR_Voted_5 > (rLim_BtmLevel_LL + rDeadband_BtmLevel) THEN
    bAlarm_BtmLevel_LL := FALSE;
END_IF;

(* --- Desalter Emulsion Interface Level Alarms --- *)
IF rTMR_Voted_6 >= rLim_DesaltLevel_HH THEN
    bAlarm_DesaltLevel_HH := TRUE;
ELSIF rTMR_Voted_6 < (rLim_DesaltLevel_HH - rDeadband_DesaltLevel) THEN
    bAlarm_DesaltLevel_HH := FALSE;
END_IF;

IF rTMR_Voted_6 <= rLim_DesaltLevel_LL THEN
    bAlarm_DesaltLevel_LL := TRUE;
ELSIF rTMR_Voted_6 > (rLim_DesaltLevel_LL + rDeadband_DesaltLevel) THEN
    bAlarm_DesaltLevel_LL := FALSE;
END_IF;

(* --- Sour Water Boot pH Alarms --- *)
IF rTMR_Voted_7 >= rLim_SourWaterPH_HH THEN
    bAlarm_SourWaterPH_HH := TRUE;
ELSIF rTMR_Voted_7 < (rLim_SourWaterPH_HH - rDeadband_SourWaterPH) THEN
    bAlarm_SourWaterPH_HH := FALSE;
END_IF;

IF rTMR_Voted_7 <= rLim_SourWaterPH_LL THEN
    bAlarm_SourWaterPH_LL := TRUE;
ELSIF rTMR_Voted_7 > (rLim_SourWaterPH_LL + rDeadband_SourWaterPH) THEN
    bAlarm_SourWaterPH_LL := FALSE;
END_IF;

(* --- Column Tray DP Flooding / Weeping Alarms --- *)
IF rTMR_Voted_1 >= rLim_TrayDP_Flooding_HH THEN
    bAlarm_TrayDP_Flooding := TRUE;
ELSIF rTMR_Voted_1 < (rLim_TrayDP_Flooding_HH - rDeadband_TrayDP) THEN
    bAlarm_TrayDP_Flooding := FALSE;
END_IF;

IF (rTMR_Voted_1 <= rLim_TrayDP_Weeping_LL) AND (iCurrentState >= 4) THEN
    bAlarm_TrayDP_Weeping := TRUE;
ELSIF rTMR_Voted_1 > (rLim_TrayDP_Weeping_LL + rDeadband_TrayDP) THEN
    bAlarm_TrayDP_Weeping := FALSE;
END_IF;

(* Furnace Pass Mismatch & Desalter Grid Interlocks *)
bAlarm_FurnacePassUnbalance := (ABS(rFurnacePassDev_1) > 15.0) OR (ABS(rFurnacePassDev_2) > 15.0) OR
                               (ABS(rFurnacePassDev_3) > 15.0) OR (ABS(rFurnacePassDev_4) > 15.0);
bAlarm_DesalterGridTripped := NOT bDesalterGridEnergized AND (iCurrentState >= 2);
bAlarm_CorrosionHighRate := rAT_CorrosionRateProbe_127 > 5.0;

(* Auto-Trip Interlock Evaluation *)
IF bAlarm_OvhdPress_HH OR bAlarm_FZ_Temp_HH OR bAlarm_AccumLevel_HH OR bAlarm_TrayDP_Flooding THEN
    bEmergencyTripActive := TRUE;
END_IF;

(* --- Bit-Packed Diagnostic Words --- *)
(* Status Word *)
dwStatusWord_Process := 16#00000000;
IF bEnable THEN dwStatusWord_Process := dwStatusWord_Process OR 16#00000001; END_IF;
IF bEmergencyTripActive THEN dwStatusWord_Process := dwStatusWord_Process OR 16#00000002; END_IF;
IF bMPC_ClosedLoopActive THEN dwStatusWord_Process := dwStatusWord_Process OR 16#00000004; END_IF;
IF bTMR_SensorsAllHealthy THEN dwStatusWord_Process := dwStatusWord_Process OR 16#00000008; END_IF;
IF bDesalterGridEnergized THEN dwStatusWord_Process := dwStatusWord_Process OR 16#00000010; END_IF;
IF iCurrentState = 7 THEN dwStatusWord_Process := dwStatusWord_Process OR 16#00000020; END_IF; (* Steady-state *)
IF iCurrentState = 8 THEN dwStatusWord_Process := dwStatusWord_Process OR 16#00000040; END_IF; (* Swing transition *)
dwStatusWord_Process := dwStatusWord_Process OR SHL(INT_TO_DWORD(iCurrentState), 8);

(* Priority 1 High Severity Alarm Word *)
dwAlarmWord1_HighSeverity := 16#00000000;
IF bEmergencyTripActive THEN dwAlarmWord1_HighSeverity := dwAlarmWord1_HighSeverity OR 16#00000001; END_IF;
IF bAlarm_FZ_Temp_HH THEN dwAlarmWord1_HighSeverity := dwAlarmWord1_HighSeverity OR 16#00000002; END_IF;
IF bAlarm_OvhdPress_HH THEN dwAlarmWord1_HighSeverity := dwAlarmWord1_HighSeverity OR 16#00000004; END_IF;
IF bAlarm_AccumLevel_HH THEN dwAlarmWord1_HighSeverity := dwAlarmWord1_HighSeverity OR 16#00000008; END_IF;
IF bAlarm_BtmLevel_HH THEN dwAlarmWord1_HighSeverity := dwAlarmWord1_HighSeverity OR 16#00000010; END_IF;
IF bAlarm_TrayDP_Flooding THEN dwAlarmWord1_HighSeverity := dwAlarmWord1_HighSeverity OR 16#00000020; END_IF;
IF bAlarm_ROC_FZ_Temp THEN dwAlarmWord1_HighSeverity := dwAlarmWord1_HighSeverity OR 16#00000040; END_IF;
IF bAlarm_ROC_OvhdPress THEN dwAlarmWord1_HighSeverity := dwAlarmWord1_HighSeverity OR 16#00000080; END_IF;

(* Priority 2/3 Process Operational Alarm Word *)
dwAlarmWord2_ProcessAlarms := 16#00000000;
IF bAlarm_FZ_Temp_H THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00000001; END_IF;
IF bAlarm_FZ_Temp_L THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00000002; END_IF;
IF bAlarm_FZ_Temp_LL THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00000004; END_IF;
IF bAlarm_OvhdPress_H THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00000008; END_IF;
IF bAlarm_OvhdPress_L THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00000010; END_IF;
IF bAlarm_OvhdPress_LL THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00000020; END_IF;
IF bAlarm_AccumLevel_H THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00000040; END_IF;
IF bAlarm_AccumLevel_L THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00000080; END_IF;
IF bAlarm_AccumLevel_LL THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00000100; END_IF;
IF bAlarm_BtmLevel_H THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00000200; END_IF;
IF bAlarm_BtmLevel_L THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00000400; END_IF;
IF bAlarm_BtmLevel_LL THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00000800; END_IF;
IF bAlarm_DesaltLevel_HH THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00001000; END_IF;
IF bAlarm_DesaltLevel_LL THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00002000; END_IF;
IF bAlarm_SourWaterPH_HH THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00004000; END_IF;
IF bAlarm_SourWaterPH_LL THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00008000; END_IF;
IF bAlarm_TrayDP_Weeping THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00010000; END_IF;
IF bAlarm_FurnacePassUnbalance THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00020000; END_IF;
IF bAlarm_DesalterGridTripped THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00040000; END_IF;
IF bAlarm_CorrosionHighRate THEN dwAlarmWord2_ProcessAlarms := dwAlarmWord2_ProcessAlarms OR 16#00080000; END_IF;

(* Sensor Health & TMR Degradation Alarm Word *)
dwAlarmWord3_Sensors := 16#00000000;
IF bTMR_Degraded_1 THEN dwAlarmWord3_Sensors := dwAlarmWord3_Sensors OR 16#00000001; END_IF;
IF bTMR_Degraded_2 THEN dwAlarmWord3_Sensors := dwAlarmWord3_Sensors OR 16#00000002; END_IF;
IF bTMR_Degraded_3 THEN dwAlarmWord3_Sensors := dwAlarmWord3_Sensors OR 16#00000004; END_IF;
IF bTMR_Degraded_4 THEN dwAlarmWord3_Sensors := dwAlarmWord3_Sensors OR 16#00000008; END_IF;
IF bTMR_Degraded_5 THEN dwAlarmWord3_Sensors := dwAlarmWord3_Sensors OR 16#00000010; END_IF;
IF bTMR_Degraded_6 THEN dwAlarmWord3_Sensors := dwAlarmWord3_Sensors OR 16#00000020; END_IF;
IF bTMR_Degraded_7 THEN dwAlarmWord3_Sensors := dwAlarmWord3_Sensors OR 16#00000040; END_IF;
IF bTMR_Degraded_8 THEN dwAlarmWord3_Sensors := dwAlarmWord3_Sensors OR 16#00000080; END_IF;
IF bTMR_Degraded_9 THEN dwAlarmWord3_Sensors := dwAlarmWord3_Sensors OR 16#00000100; END_IF;
IF bTMR_Degraded_10 THEN dwAlarmWord3_Sensors := dwAlarmWord3_Sensors OR 16#00000200; END_IF;

END_FUNCTION_BLOCK
