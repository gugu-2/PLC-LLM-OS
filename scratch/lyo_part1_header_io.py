# Module 1: Header and I/O Variable Declarations
def get_part1():
    return '''FUNCTION_BLOCK FB_Pharma_BulkLyophilizer_CapacitanceManometer_Pirani
(* ==========================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - IEC 61131-3 HIGH-PERFORMANCE STRUCTURED TEXT
 * ARCHITECTURE: PRODUCTION-SCALE STERILE BULK LYOPHILIZER (FREEZE DRYER) (40 m2 SHELF AREA)
 * SYSTEM: 16-SHELF MULTI-ZONE THERMAL FLUID CASSETTE WITH DUAL COMPARATIVE VACUUM GAUGES
 * 
 * CORE SUBSYSTEMS INTEGRATED:
 *  1. Multi-Zone Thermal Fluid Shelf Heat Exchanger: Silicone oil circulation (-55.0 deg C to
 *     +80.0 deg C) with dynamic heating/cooling cascade PID, thyristor SCR power control (120 kW),
 *     cryogenic expansion cooling, and active thermal balancing across 16 shelves within +/-0.5 deg C.
 *  2. Dual Mechanical Condenser Refrigeration Circuit: Cascaded twin-screw compressors operating
 *     down to -85.0 deg C ice coil condensing temperature, 600 kg sublimation ice loading capacity,
 *     and proportional hot-gas bypass defrosting heat recovery circuit.
 *  3. Ultra-High Vacuum Sublimation Control: Two-stage dry screw backing pumps backed by Roots
 *     booster blower (0.010 to 1013 mbar), high-speed butterfly isolation valve (DN500), and
 *     comparative pressure sublimation end-point detection (MKS Baratron vs Pirani thermal ratio).
 *  4. Nitrogen Micro-Bleed Pressure Regulation: Controlled sterile-filtered dry nitrogen gas
 *     micro-dosing bleed valve (0.05 to 0.20 mbar) for precise convective sublimation heat transfer.
 *  5. Automatic Clean-in-Place (CIP) & Steam-in-Place (SIP) Sterilization: Saturated pure steam
 *     injection at 121.1 deg C and 2.1 bar abs with real-time F0 thermal lethality integration.
 *  6. Hydraulic Shelf Stoppering Mechanism: Bottom-up hydraulic cylinder ram with dynamic
 *     tonnage monitoring (0 to 60 metric tons) and linear transducer displacement profile tracking.
 *  7. Full 2oo3 Triple Modular Redundancy (TMR) Architecture on 6 Critical Sensor Clusters:
 *     Shelf Product RTDs, Capacitance Manometers, Condenser Suction Pressure, Silicone Oil Supply
 *     Temperature, Chamber Pirani Gauges, and Hydraulic Stoppering Cylinder Pressure Transducers.
 *  8. 8-State Cyber-Physical Discrete State-Space Model: x[k+1] = A*x[k] + B*u[k] with Luenberger
 *     state reconstruction of sublimation drying front kinetics, ice thickness, and cake resistance.
 *  9. Model Predictive Control (MPC) Receding-Horizon Quadratic Cost Optimization (Q, R, P Matrices).
 * 10. 12-Stage Deterministic Finite State Machine (FSM): Idle Sterile Hold, Vial Loading Chilled
 *     Hold, Atmospheric Freezing, Annealing Crystallization, Deep Evacuation, Primary Sublimation,
 *     Comparative End-Point Verification, Secondary Desorption, Hydraulic Stoppering, Chamber
 *     Aeration, Product Unloading, and Automated CIP/SIP Sterilization with F0 lethality tracking.
 * 11. ISA-18.2 Multi-Tiered Alarm Hierarchy with High-High, High, Low, Low-Low Trip Points,
 *     Rate-of-Change Detectors, Eutectic Melt Collapse Interlocks, and 32-bit Status Serialization.
 * ========================================================================================== *)

VAR_INPUT
    (* Master Operational Supervisory Controls *)
    bEnable                         : BOOL;     (* Master Freeze Dryer System Enable Command [TRUE=Enable, FALSE=Safe Halt] *)
    bReset                          : BOOL;     (* Global System Fault Reset & Latched Alarm Clear Command [pulse] *)
    bAutoMode                       : BOOL;     (* Autonomous Recipe Automation Mode [TRUE=Auto, FALSE=Manual Maintenance] *)
    bEmergencyStop                  : BOOL;     (* Hardware E-Stop Safety Circuit [FALSE=Active Emergency Stop, TRUE=Healthy] *)
    bStartCycle                     : BOOL;     (* Batch Process Lyophilization Cycle Start Command [pulse] *)
    bDoorClosed_Locked              : BOOL;     (* Autoclave Chamber Door Sealed & Pneumatically Clamped [TRUE=Locked] *)
    bAckAlarms                      : BOOL;     (* ISA-18.2 Alarm Acknowledgment Supervisory Command [pulse] *)
    bTransferPermissive             : BOOL;     (* Isolator / Barrier System Transfer Infeed/Outfeed Permissive [TRUE=Permitted] *)

    (* Batch Recipe Parameters & Process Targets *)
    rRecipe_ShelfTemp_Freezing_degC : REAL;     (* Target Shelf Freezing Temperature Setpoint [deg C] (Range -55.0..-40.0, Nom -45.0) *)
    rRecipe_ShelfTemp_Primary_degC  : REAL;     (* Target Shelf Primary Sublimation Temperature [deg C] (Range -30.0..+10.0, Nom -15.0) *)
    rRecipe_ShelfTemp_Secondary_degC: REAL;     (* Target Shelf Secondary Desorption Temperature [deg C] (Range +20.0..+50.0, Nom +35.0) *)
    rRecipe_ChamberPress_Primary_mbar:REAL;     (* Target Primary Sublimation Vacuum Pressure [mbar] (Range 0.050..0.300, Nom 0.120) *)
    rRecipe_ChamberPress_Secondary_mbar:REAL;   (* Target Secondary Desorption Deep Vacuum [mbar] (Range 0.005..0.050, Nom 0.015) *)
    rRecipe_FreezingRampRate_degC_min:REAL;    (* Commanded Freezing Thermal Ramp Rate [deg C/min] (Range 0.1..2.0, Nom 0.5) *)
    rRecipe_SublimationRampRate_degC_min:REAL; (* Commanded Primary Drying Heating Ramp Rate [deg C/min] (Range 0.05..1.0, Nom 0.25) *)
    rRecipe_StopperingForce_kN      : REAL;     (* Target Final Hydraulic Shelf Compression Force [kN] (Range 100.0..600.0, Nom 350.0) *)
    rRecipe_StopperingHoldTime_s    : REAL;     (* Stoppering Target Tonnage Compression Dwell Time [s] (Range 60.0..600.0, Nom 180.0) *)
    rRecipe_SIP_TargetTemp_degC     : REAL;     (* Saturated Pure Steam Sterilization Temperature [deg C] (Nom 121.1, Range 121.0..124.0) *)
    rRecipe_SIP_MinF0_min           : REAL;     (* Minimum Required Equivalent Lethality Integration F0 [min] (Nom 30.0, Range 20.0..60.0) *)
    rRecipe_VialCollapseTemp_degC   : REAL;     (* Critical Formulation Eutectic / Glass Collapse Temp [deg C] (Nom -32.0, Range -45.0..-15.0) *)

    (* 2oo3 TMR Group 1: Shelf Product Core Temperature Probes (RTD Pt100 Class 1/10 DIN) [deg C] *)
    rTemp_Product_TE101A            : REAL;     (* Product Vial Core Temperature Probe A [deg C] (Range -60.0..+90.0) *)
    rTemp_Product_TE101B            : REAL;     (* Product Vial Core Temperature Probe B [deg C] (Range -60.0..+90.0) *)
    rTemp_Product_TE101C            : REAL;     (* Product Vial Core Temperature Probe C [deg C] (Range -60.0..+90.0) *)

    (* 2oo3 TMR Group 2: Chamber Absolute Capacitance Manometers (MKS Baratron Heated Head) [mbar] *)
    rPress_Chamber_Baratron_PT201A  : REAL;     (* Absolute Capacitance Manometer A [mbar] (Gas-Independent, Range 0.001..10.000) *)
    rPress_Chamber_Baratron_PT201B  : REAL;     (* Absolute Capacitance Manometer B [mbar] (Gas-Independent, Range 0.001..10.000) *)
    rPress_Chamber_Baratron_PT201C  : REAL;     (* Absolute Capacitance Manometer C [mbar] (Gas-Independent, Range 0.001..10.000) *)

    (* 2oo3 TMR Group 3: Condenser Refrigeration Low-Stage Suction Pressure Transmitters [bar] *)
    rPress_Suction_PT301A           : REAL;     (* Cascade Low-Stage Compressor Suction Pressure A [bar] (Range 0.0..30.0) *)
    rPress_Suction_PT301B           : REAL;     (* Cascade Low-Stage Compressor Suction Pressure B [bar] (Range 0.0..30.0) *)
    rPress_Suction_PT301C           : REAL;     (* Cascade Low-Stage Compressor Suction Pressure C [bar] (Range 0.0..30.0) *)

    (* 2oo3 TMR Group 4: Shelf Silicone Oil Circulation Supply Temperature Probes [deg C] *)
    rTemp_OilSupply_TE401A          : REAL;     (* Silicone Oil Primary Supply Temperature Probe A [deg C] (Range -60.0..+100.0) *)
    rTemp_OilSupply_TE401B          : REAL;     (* Silicone Oil Primary Supply Temperature Probe B [deg C] (Range -60.0..+100.0) *)
    rTemp_OilSupply_TE401C          : REAL;     (* Silicone Oil Primary Supply Temperature Probe C [deg C] (Range -60.0..+100.0) *)

    (* 2oo3 TMR Group 5: Chamber Thermal Conductivity Vacuum Pirani Gauges [mbar] *)
    rPress_Chamber_Pirani_PT501A    : REAL;     (* Chamber Pirani Gauge A (Thermal Convection, Range 0.001..1000.0) [mbar] *)
    rPress_Chamber_Pirani_PT501B    : REAL;     (* Chamber Pirani Gauge B (Thermal Convection, Range 0.001..1000.0) [mbar] *)
    rPress_Chamber_Pirani_PT501C    : REAL;     (* Chamber Pirani Gauge C (Thermal Convection, Range 0.001..1000.0) [mbar] *)

    (* 2oo3 TMR Group 6: Hydraulic Shelf Stoppering Cylinder Pressure Transducers [bar] *)
    rPress_Hydraulic_PT601A         : REAL;     (* Hydraulic Stoppering Ram Cylinder Pressure A [bar] (Range 0.0..250.0) *)
    rPress_Hydraulic_PT601B         : REAL;     (* Hydraulic Stoppering Ram Cylinder Pressure B [bar] (Range 0.0..250.0) *)
    rPress_Hydraulic_PT601C         : REAL;     (* Hydraulic Stoppering Ram Cylinder Pressure C [bar] (Range 0.0..250.0) *)

    (* 16-Zone Individual Shelf Temperature Array (Active Uniformity Monitoring) [deg C] *)
    rTemp_Shelf_Zones               : ARRAY[1..16] OF REAL; (* RTD Pt100 Sensors Embedded in Shelves 1 to 16 [deg C] *)

    (* Auxiliary Process Analog Sensors *)
    rTemp_OilReturn_degC            : REAL;     (* Silicone Oil Return Collector Temperature [deg C] (Range -60.0..+100.0) *)
    rTemp_CondenserSurface_degC     : REAL;     (* Ice Condenser Tube Surface Temperature [deg C] (Range -95.0..+50.0) *)
    rTemp_SIP_DrainTrap_degC        : REAL;     (* Chamber Lowest Condensate Drain Steam Trap Temp [deg C] (Range 20.0..150.0) *)
    rPress_SteamSupply_bar          : REAL;     (* Plant Pure Saturated Steam Header Pressure [bar] (Range 0.0..6.0, Nom 2.5) *)
    rPress_CondenserChamber_mbar    : REAL;     (* Dedicated Condenser Vessel Vacuum Pressure [mbar] (Range 0.001..1000.0) *)
    rFlow_SiliconeOil_m3h           : REAL;     (* Silicone Oil Recirculation Flow Rate [m3/h] (Range 0.0..50.0, Nom 32.0) *)
    rFlow_N2Bleed_sccm              : REAL;     (* Sterile Nitrogen Mass Flow Meter Bleed Rate [sccm] (Range 0.0..500.0) *)
    rFlow_CIPWater_m3h              : REAL;     (* Clean-in-Place Spray Water Flowmeter [m3/h] (Range 0.0..40.0) *)
    rPos_StopperingRam_mm           : REAL;     (* Magnetostrictive Linear Transducer Ram Position [mm] (Range 0.0..1800.0) *)
    rTonnage_LoadCells_kN           : REAL;     (* Multi-Point Strain Gauge Load Cell Total Compression Force [kN] (0.0..700.0) *)

    (* Equipment Digital Status Feedbacks & Limit Switches *)
    bIsolationValve_Open_LS         : BOOL;     (* Main Butterfly Vacuum Isolation Valve Fully Open Limit Switch [TRUE=Open] *)
    bIsolationValve_Closed_LS       : BOOL;     (* Main Butterfly Vacuum Isolation Valve Fully Closed Limit Switch [TRUE=Closed] *)
    bVacuumPump1_Running            : BOOL;     (* Two-Stage Dry Screw Vacuum Backing Pump 1 Contactor Auxiliary [TRUE=Running] *)
    bVacuumPump2_Running            : BOOL;     (* Two-Stage Dry Screw Vacuum Backing Pump 2 Contactor Auxiliary [TRUE=Running] *)
    bRootsBlower_Running            : BOOL;     (* High-Vacuum Roots Blower Booster VFD Run Feedback [TRUE=Running] *)
    bRefrigComp1_Running            : BOOL;     (* Cascade Refrigeration High-Stage Compressor 1 Run Feedback [TRUE=Running] *)
    bRefrigComp2_Running            : BOOL;     (* Cascade Refrigeration Low-Stage Compressor 2 Run Feedback [TRUE=Running] *)
    bOilPump1_Running               : BOOL;     (* Silicone Oil Canned Motor Recirculation Pump 1 Run Feedback [TRUE=Running] *)
    bOilPump2_Running               : BOOL;     (* Silicone Oil Canned Motor Recirculation Pump 2 Run Feedback [TRUE=Running] *)
    bCondensateDrain_Open_LS        : BOOL;     (* Pneumatic Sanitary Condensate Drain Angle Valve Open Feedback [TRUE=Open] *)
    bPureSteamValve_Open_LS         : BOOL;     (* Pure Steam Sanitary Inflow Isolation Valve Open Feedback [TRUE=Open] *)
    bInflatableSeal_Pressurized     : BOOL;     (* Chamber Door Silicone Gasket Inflatable Seal Pressure Switch [TRUE=Inflated] *)
    rDeltaTime_s                    : REAL;     (* Cyclic Execution Task Delta Time [s] (Nominal 0.020 s, range 0.005..0.100) *)
END_VAR

VAR_OUTPUT
    (* Modulating Analog Actuator Command Outputs *)
    rCmd_ShelfHeater_SCR_pct        : REAL;     (* 120 kW Electric Circulation Heater Thyristor SCR Duty Cycle [%] (0.0..100.0) *)
    rCmd_ShelfCooling_Valve_pct     : REAL;     (* Cryogenic Brine Heat Exchanger Proportional Expansion Valve [%] (0.0..100.0) *)
    rCmd_N2MicroBleed_Piezo_pct     : REAL;     (* Piezo-Electric Proportional Micro-Dosing Bleed Valve [%] (0.0..100.0) *)
    rCmd_VacuumButterfly_pct        : REAL;     (* Main Vacuum Isolation Butterfly Valve Modulating Throttle [%] (0.0..100.0) *)
    rCmd_RefrigCap_Comp1_pct        : REAL;     (* Cascade Refrigeration Compressor 1 Slide Valve Capacity [%] (0.0..100.0) *)
    rCmd_RefrigCap_Comp2_pct        : REAL;     (* Cascade Refrigeration Compressor 2 Slide Valve Capacity [%] (0.0..100.0) *)
    rCmd_HotGasDefrost_pct          : REAL;     (* Modulating Hot-Gas Bypass Defrosting Condenser Valve [%] (0.0..100.0) *)
    rCmd_HydraulicPressure_bar      : REAL;     (* Hydraulic Stoppering Proportional Pressure Relief Valve [bar] (0.0..250.0) *)
    rCmd_HydraulicSpeed_mms         : REAL;     (* Hydraulic Proportional Flow Directional Valve Ram Speed [mm/s] (0.0..50.0) *)
    rCmd_SiliconePumpVFD_pct        : REAL;     (* Silicone Oil Recirculation Twin Pump VFD Speed Setpoint [%] (0.0..100.0) *)

    (* Discrete Digital Actuator Solenoids & Motor Commands *)
    bCmd_IsolationValve_Open        : BOOL;     (* Command: Main Butterfly Vacuum Isolation Valve Solenoid Open [TRUE=Open] *)
    bCmd_IsolationValve_Close       : BOOL;     (* Command: Main Butterfly Vacuum Isolation Valve Solenoid Close [TRUE=Close] *)
    bCmd_VacuumPump1_Start          : BOOL;     (* Command: Two-Stage Dry Screw Vacuum Backing Pump 1 Contactor [TRUE=Run] *)
    bCmd_VacuumPump2_Start          : BOOL;     (* Command: Two-Stage Dry Screw Vacuum Backing Pump 2 Contactor [TRUE=Run] *)
    bCmd_RootsBlower_Start          : BOOL;     (* Command: Roots Blower High-Vacuum Booster Drive Start [TRUE=Run] *)
    bCmd_RefrigComp1_Start          : BOOL;     (* Command: Cascade Refrigeration High-Stage Compressor Start [TRUE=Run] *)
    bCmd_RefrigComp2_Start          : BOOL;     (* Command: Cascade Refrigeration Low-Stage Compressor Start [TRUE=Run] *)
    bCmd_OilPump1_Start             : BOOL;     (* Command: Silicone Oil Circulation Duty Pump 1 Contactor [TRUE=Run] *)
    bCmd_OilPump2_Start             : BOOL;     (* Command: Silicone Oil Circulation Standby Pump 2 Contactor [TRUE=Run] *)
    bCmd_PureSteam_Valve_Open       : BOOL;     (* Command: Pure Steam Injection Sanitary Valve Actuator [TRUE=Open] *)
    bCmd_CondensateDrain_Open       : BOOL;     (* Command: Chamber Condensate Sanitary Drain Angle Valve [TRUE=Open] *)
    bCmd_CIP_SupplyPump_Start       : BOOL;     (* Command: Clean-in-Place Multi-Axis Spray Ball Feed Pump [TRUE=Run] *)
    bCmd_N2_SterileVent_Open        : BOOL;     (* Command: 0.2 um Hydrophobic Filter Sterile N2 Aeration Valve [TRUE=Open] *)
    bCmd_InflatableSeal_Inflate     : BOOL;     (* Command: Door Silicone Seal Inflatable Gasket Pressurize [TRUE=Inflate] *)
    bCmd_HydraulicDump_SlamOpen     : BOOL;     (* Command: Emergency Hydraulic Pressure Fast Slam-Dump Valve [TRUE=Dump] *)

    (* Cyber-Physical Observers & Key Process Indicators *)
    iCurrentState                   : INT;      (* 12-Stage Operational FSM Active State Enumeration [1..12] *)
    sCurrentStateName               : STRING(32);(* Descriptive Text of Active Operational Lyophilization Phase *)
    rObs_CompPressureRatio          : REAL;     (* Comparative Vacuum Ratio: Pirani / Baratron [-] (Nom 1.6..1.8 wet -> 1.00 dry) *)
    rObs_SublimationRate_kgh        : REAL;     (* Instantaneous Batch Ice Sublimation Mass Flow Rate [kg/h] *)
    rObs_DryLayerThickness_mm       : REAL;     (* Observed Porous Cake Dry Layer Front Propagation Thickness [mm] (0.0..25.0) *)
    rObs_ProductIceInterfaceTemp_degC:REAL;    (* Pikal Model Calculated Sublimation Front Interface Temperature [deg C] *)
    rObs_CalculatedF0_min           : REAL;     (* Cumulative Thermal Lethality Sterilization Integral F0 [min] *)
    rObs_StopperingTonnage_ton      : REAL;     (* Measured Real-Time Hydraulic Stoppering Total Compaction Force [metric tons] *)
    rObs_ShelfTempUniformity_degC   : REAL;     (* Maximum Temperature Spread Across 16 Monitored Shelf Zones [deg C] (Target <= 0.5) *)
    rObs_CondenserIceThickness_mm   : REAL;     (* Estimated Sublimated Ice Layer Depth on Condenser Surface [mm] (0.0..35.0) *)
    rObs_CycleRemainingTime_h       : REAL;     (* Estimated Remaining Total Batch Lyophilization Duration [hours] *)
    bPrimaryDryingComplete          : BOOL;     (* Flag: Comparative Pressure Ratio & Core Temperature Sublimation End Met [TRUE] *)
    bSecondaryDryingComplete        : BOOL;     (* Flag: Bound Moisture Desorption & Deep Vacuum Equilibrated [TRUE] *)
    bStopperingComplete             : BOOL;     (* Flag: Hydraulic Tonnage Profile & Ram Position Dwell Satisfied [TRUE] *)
    bSterilizationComplete          : BOOL;     (* Flag: Steam-in-Place F0 Lethality Integral Exceeds Recipe Threshold [TRUE] *)
    bCycleComplete                  : BOOL;     (* Flag: Entire Lyophilization Recipe Cycle Finished Successfully [pulse] *)
    bReadyForLoading                : BOOL;     (* Flag: Machine Sterilized, Chilled & Ready to Accept Fresh Vials [TRUE] *)

    (* ISA-18.2 Alarms & Serialized Status Words *)
    dwSystemStatusWord              : DWORD;    (* Overall Operational Machine Subsystem Interlock Bitmask *)
    dwTMRStatusWord                 : DWORD;    (* 2oo3 Triple Modular Redundancy Health Bitmask Across 6 Sensor Groups *)
    dwISAAlarm_Critical             : DWORD;    (* Priority 1 Critical Safety & Product Collapse Trip Alarms *)
    dwISAAlarm_Warning              : DWORD;    (* Priority 2 Process Deviation & Sensor Discrepancy Warnings *)
    dwISAAlarm_Advisory             : DWORD;    (* Priority 3 Advisory Maintenance & Calibration Reminders *)
    dwActuatorStatusWord            : DWORD;    (* Actuator Command Echo & Contactor Feedback Bitmask *)
    bAlarm_AnyCritical              : BOOL;     (* Master Critical Trip Active Flag [TRUE=Emergency Abort] *)
    bAlarm_AnyWarning               : BOOL;     (* Master Warning Active Flag [TRUE=Degraded Operation] *)
END_VAR
'''

if __name__ == "__main__":
    print(f"Part 1 length: {len(get_part1())} characters")
