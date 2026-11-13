# lng_reliquefaction_builder/declarations.py

def get_declarations():
    return """FUNCTION_BLOCK FB_Marine_LNG_BoilOffGas_Reliquefaction_Cascade
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * ARCHITECTURAL GRADE : Commercial Marine & Clean Energy Shipping (Tier 1 Priority Heavy Industrial Sector)
 * COMMERCIAL SYSTEM   : 174,000 m3 Membrane LNG Carrier Boil-Off Gas (BOG) Subcooler Re-Liquefaction Plant &
 *                       Cryogenic Fuel Gas Supply System (FGSS), Nitrogen Reverse Brayton Cycle Compander Train,
 *                       Dynamic Anti-Surge Bypass Cascade (< 800 ms full stroke), Low-Pressure Dual-Fuel Engine
 *                       (WinGD X-DF / MAN ME-GA) Coordinated Sendout, Gas Combustion Unit (GCU) Fast Thermal Dump,
 *                       Marine 6-DOF Hull Sloshing Dynamic Pressure Surge Damping, and SIL-3 Quick-Closing ESD.
 * APPLICABLE CODES    : IMO IGC Code (International Gas Carrier Code), SIGTTO Cryogenic Gas Guidelines,
 *                       API 617 (Centrifugal Compressors), API 521 (Depressurization & Flare/Mast Venting),
 *                       ISO 13623 / ISO 13709, IEC 61508 / IEC 61511 (SIL-3 Certified Emergency Shutdown),
 *                       ISA-18.2 (Alarm Systems Management), DNV-GL Clean Design & Gas Fuelled Ship Rules.
 * ===================================================================================================================== *)

VAR_INPUT
    (* =================================================================================================================
     * SECTION 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) CRITICAL SAFETY SENSOR TRIPLET CHANNELS
     * ================================================================================================================= *)
    rCargoUllagePres_PT101A_In      : REAL;    (* Cargo Tank 1 Ullage Vapor Pressure Transmitter Channel A [kPa] *)
    rCargoUllagePres_PT101B_In      : REAL;    (* Cargo Tank 1 Ullage Vapor Pressure Transmitter Channel B [kPa] *)
    rCargoUllagePres_PT101C_In      : REAL;    (* Cargo Tank 1 Ullage Vapor Pressure Transmitter Channel C [kPa] *)

    rBOGSuctionPres_PT201A_In       : REAL;    (* BOG Compressor Stage 1 Suction Pressure Transmitter Channel A [kPa] *)
    rBOGSuctionPres_PT201B_In       : REAL;    (* BOG Compressor Stage 1 Suction Pressure Transmitter Channel B [kPa] *)
    rBOGSuctionPres_PT201C_In       : REAL;    (* BOG Compressor Stage 1 Suction Pressure Transmitter Channel C [kPa] *)

    rBOGDischargeDP_PDT301A_In      : REAL;    (* BOG Compressor Stage 2 Venturi Flow Differential Pressure Channel A [kPa] *)
    rBOGDischargeDP_PDT301B_In      : REAL;    (* BOG Compressor Stage 2 Venturi Flow Differential Pressure Channel B [kPa] *)
    rBOGDischargeDP_PDT301C_In      : REAL;    (* BOG Compressor Stage 2 Venturi Flow Differential Pressure Channel C [kPa] *)

    rColdBoxN2ExpTemp_TT401A_In     : REAL;    (* Nitrogen Compander Cryogenic Expander Discharge Temp Channel A [deg C] *)
    rColdBoxN2ExpTemp_TT401B_In     : REAL;    (* Nitrogen Compander Cryogenic Expander Discharge Temp Channel B [deg C] *)
    rColdBoxN2ExpTemp_TT401C_In     : REAL;    (* Nitrogen Compander Cryogenic Expander Discharge Temp Channel C [deg C] *)

    rCondensateFlow_FT501A_In       : REAL;    (* Subcooled Cryogenic LNG Condensate Coriolis Mass Flow Channel A [kg/h] *)
    rCondensateFlow_FT501B_In       : REAL;    (* Subcooled Cryogenic LNG Condensate Coriolis Mass Flow Channel B [kg/h] *)
    rCondensateFlow_FT501C_In       : REAL;    (* Subcooled Cryogenic LNG Condensate Coriolis Mass Flow Channel C [kg/h] *)

    (* =================================================================================================================
     * SECTION 2: PROCESS MONITORS, TANK LIQUID INVENTORY & PROPULSION DEMAND SIGNALS
     * ================================================================================================================= *)
    rCargoUllagePres_Tank4_In       : REAL;    (* Cargo Tank 4 Ullage Vapor Pressure Transmitter [kPa] *)
    rCargoLiquidTemp_Tank1_In       : REAL;    (* Cargo Tank 1 Bulk Liquid LNG Saturated Temperature [deg C] *)
    rCargoLiquidTemp_Tank4_In       : REAL;    (* Cargo Tank 4 Bulk Liquid LNG Saturated Temperature [deg C] *)
    rCargoLiquidLevel_Tank1_In      : REAL;    (* Cargo Tank 1 Radar Liquid Filling Level [m] *)
    rCargoLiquidLevel_Tank4_In      : REAL;    (* Cargo Tank 4 Radar Liquid Filling Level [m] *)
    rBOGStage1SuctTemp_In           : REAL;    (* BOG Compressor Stage 1 Suction Header Temperature [deg C] *)
    rBOGStage1DischPres_In          : REAL;    (* BOG Compressor Stage 1 Intermediate Discharge Pressure [kPa] *)
    rBOGStage2DischPres_In          : REAL;    (* BOG Compressor Stage 2 Final Discharge Pressure [kPa] *)
    rBOGStage2DischTemp_In          : REAL;    (* BOG Compressor Stage 2 Final Discharge Temperature [deg C] *)
    rColdBoxLNGOutTemp_In           : REAL;    (* Vacuum Cold Box Subcooled LNG Condensate Outlet Temperature [deg C] *)
    rN2CompSuctPres_In              : REAL;    (* Nitrogen Refrigeration Cycle Compander Suction Pressure [kPa] *)
    rN2CompDischPres_In             : REAL;    (* Nitrogen Refrigeration Cycle Compander Discharge Pressure [kPa] *)
    rN2CompanderSpeed_In            : REAL;    (* Nitrogen Compander Magnetic Bearing High-Speed Tachometer [rpm] *)
    rN2InventoryMass_In             : REAL;    (* Nitrogen Refrigeration Circuit Active Loop Mass Inventory [kg] *)
    rFuelGasEngineDem_In            : REAL;    (* Dual-Fuel Propulsion Main Engines (X-DF/ME-GA) BOG Demand [kg/h] *)
    rFuelGasEnginePres_In           : REAL;    (* Dual-Fuel Propulsion Engine Fuel Gas Regulated Supply Pressure [bar] *)
    rFuelGasAuxGenDem_In            : REAL;    (* Auxiliary Dual-Fuel Diesel Generators (DFDG) Fuel Gas Demand [kg/h] *)
    rAmbientAirTemp_In              : REAL;    (* Ambient Weather Deck Air Temperature [deg C] *)
    rSeaWaterCoolingTemp_In         : REAL;    (* Central Sea Water Intercooler Inflow Temperature [deg C] *)

    (* =================================================================================================================
     * SECTION 3: MARINE HULL 6-DOF HYDRODYNAMIC MOTION & SLOSHING ACCELERATION
     * ================================================================================================================= *)
    rShipRollAngle_In               : REAL;    (* Hull Gyro Roll Motion Angular Inclinometer [deg] *)
    rShipPitchAngle_In              : REAL;    (* Hull Gyro Pitch Motion Angular Inclinometer [deg] *)
    rShipHeaveAcc_In                : REAL;    (* Hull Central Rigid-Body Vertical Heave Acceleration [m/s2] *)
    rWaveSignificantHeight_In       : REAL;    (* Marine Hydrodynamic Wave Radar Significant Wave Height Hs [m] *)

    (* =================================================================================================================
     * SECTION 4: ROTATING MACHINERY AUXILIARIES & BEARING HEALTH TELEMETRY
     * ================================================================================================================= *)
    rLubeOilPres_In                 : REAL;    (* BOG Compressor Mechanical Bearing Lube Oil Supply Pressure [bar] *)
    rLubeOilTemp_In                 : REAL;    (* BOG Compressor Mechanical Bearing Lube Oil Supply Temperature [deg C] *)
    rSealGasSupplyDP_In             : REAL;    (* Dry Gas Seal N2 Buffer Differential Pressure Over Suction [bar] *)
    rMotorCurrent_In                : REAL;    (* BOG Compressor 3.5 MW Drive Motor Stator Phase RMS Current [A] *)
    rMotorVibration_In              : REAL;    (* BOG Compressor Drive Radial Shaft Shaft Vibration Probe [um] *)
    rCompanderVibration_In          : REAL;    (* Nitrogen Compander Active Magnetic Bearing Radial Displacement [um] *)

    (* =================================================================================================================
     * SECTION 5: OPERATIONAL PERMISSIVES, OPERATOR SETPOINTS & SIL-3 EMERGENCY SIGNALS
     * ================================================================================================================= *)
    bEnablePlant_In                 : REAL;    (* Re-Liquefaction Plant Master Supervisory Run Permissive (1.0=Run, 0.0=Stop) [-] *)
    bResetFaults_In                 : REAL;    (* Supervisory Master Alarm and Trip Reset Command (1.0=Pulse Reset) [-] *)
    bDualFuelEngineOnline_In        : REAL;    (* Dual-Fuel Propulsion Engines Gas-Mode Online Active Permissive [-] *)
    bGCUReady_In                    : REAL;    (* Gas Combustion Unit (GCU) Burner Ready & Permissive Verified [-] *)
    bInertGasPermissive_In          : REAL;    (* Cargo Compressor Casing & Cold Box Dry Nitrogen Inert Purge Verified [-] *)
    bESD1_Trip_In                   : REAL;    (* SIL-3 Safety Instrumented System ESD-1 Ship Emergency Trip (1.0=Trip) [-] *)
    bESD2_CargoTrip_In              : REAL;    (* SIL-3 Safety Instrumented System ESD-2 Cargo Tank Quick Isolation [-] *)
    rUllageTargetPres_SP_In         : REAL;    (* Operator Master Cargo Tank Ullage Target Working Setpoint [kPa] *)
    rSubcoolingDeltaT_SP_In         : REAL;    (* Target LNG Subcooling Margin Below Saturation Temperature [deg C] *)
    rMaxAllowableFuelGasFlow_In     : REAL;    (* Engine Room Maximum Safe Continuous Gas Delivery Limit [kg/h] *)
END_VAR

VAR_OUTPUT
    (* =================================================================================================================
     * SECTION 1: FAST CRYOGENIC ACTUATOR DEMANDS & MOTOR SPEED CONTROLS
     * ================================================================================================================= *)
    rASV1_Demand_Out                : REAL;    (* BOG Stage 1 Anti-Surge Bypass Valve Modulation Demand [0..100 %] *)
    rASV2_Demand_Out                : REAL;    (* BOG Stage 2 Anti-Surge Bypass Valve Modulation Demand [0..100 %] *)
    rN2_IGV_Demand_Out              : REAL;    (* Nitrogen Compander Variable Inlet Guide Vanes Position [0..100 %] *)
    rCondReturnValv_Demand_Out      : REAL;    (* Subcooled LNG Condensate Tank Bottom Return Control Valve [0..100 %] *)
    rGCU_DumpValve_Demand_Out       : REAL;    (* Gas Combustion Unit (GCU) Fast-Dump Throttle Valve Demand [0..100 %] *)
    rBOG_VFD_Speed_Demand_Out       : REAL;    (* BOG Compressor 3.5 MW Electric Motor VFD Speed Reference [0..100 %] *)
    rFuelGasSupplyValv_Demand_Out   : REAL;    (* Dual-Fuel Propulsion Header Delivery Pressure Control Valve [0..100 %] *)
    rMastVentValv_Demand_Out        : REAL;    (* Emergency Atmospheric Mast Vent Fast Quick-Opening Valve [0..100 %] *)
    rN2MakeupValve_Demand_Out       : REAL;    (* Nitrogen Cycle High-Pressure Mass Inventory Makeup Valve [0..100 %] *)
    rN2VentValve_Demand_Out         : REAL;    (* Nitrogen Cycle Low-Pressure Mass Inventory Vent Valve [0..100 %] *)

    (* =================================================================================================================
     * SECTION 2: 2oo3 VOTED CRYOGENIC PROCESS FEEDBACK SIGNALS
     * ================================================================================================================= *)
    rVoted_TankUllagePres_Out       : REAL;    (* 2oo3 Triple Modular Redundant Voted Tank 1 Ullage Pressure [kPa] *)
    rVoted_BOGSuctionPres_Out       : REAL;    (* 2oo3 Triple Modular Redundant Voted BOG Stage 1 Suction Pressure [kPa] *)
    rVoted_BOGDischargeDP_Out       : REAL;    (* 2oo3 Triple Modular Redundant Voted Stage 2 Flow Venturi DP [kPa] *)
    rVoted_N2ExpTemp_Out            : REAL;    (* 2oo3 Triple Modular Redundant Voted N2 Expander Outlet Temp [deg C] *)
    rVoted_CondensateFlow_Out       : REAL;    (* 2oo3 Triple Modular Redundant Voted LNG Condensate Coriolis Flow [kg/h] *)

    (* =================================================================================================================
     * SECTION 3: REAL-TIME CYBER-PHYSICAL COMPUTED PROCESS METRICS & THERMODYNAMICS
     * ================================================================================================================= *)
    rReliquefiedRate_kg_h_Out       : REAL;    (* Real-Time Mass Flow Rate of Reliquefied Subcooled LNG Condensate [kg/h] *)
    rBOGStage1SurgeMargin_Out       : REAL;    (* Compressor Stage 1 Dynamic Anti-Surge Operational Margin Ratio [-] *)
    rBOGStage2SurgeMargin_Out       : REAL;    (* Compressor Stage 2 Dynamic Anti-Surge Operational Margin Ratio [-] *)
    rColdBoxLMTD_Out                : REAL;    (* Cryogenic Vacuum Cold Box Logarithmic Mean Temperature Difference [deg C] *)
    rTotalCoolingPower_kW_Out       : REAL;    (* Real-Time Net Cryogenic Refrigeration Thermal Duty Delivered [kW] *)
    rEstimatedBOR_PctPerDay_Out     : REAL;    (* Derived Real-Time Tank Cargo Daily Boil-Off Rate Equivalent [%/day] *)
    rSloshingPressurePeak_Out       : REAL;    (* Hydrodynamic Hull Sloshing Dynamic Ullage Pressure Perturbation [kPa] *)
    rN2CompanderPressureRatio_Out   : REAL;    (* Nitrogen Cycle Compander Compressor Pressure Ratio [-] *)
    rCompressorPolytropicHead_Out   : REAL;    (* Centrifugal BOG Compressor Stage 2 Polytropic Head [kJ/kg] *)
    rFuelGasMassDelivered_kg_h_Out  : REAL;    (* Instantaneous BOG Mass Flow Delivered to Dual-Fuel Propulsion [kg/h] *)

    (* =================================================================================================================
     * SECTION 4: SAFETY INSTRUMENTED SYSTEM, FSM STATUS & 32-BIT BIT-PACKED TELEMETRY
     * ================================================================================================================= *)
    bPlantRunning_Out               : BOOL;    (* Re-Liquefaction Cascade Full Plant Active Online Status [-] *)
    bGCU_Active_Out                 : BOOL;    (* Gas Combustion Unit Excess Methane Thermal Disposal Active [-] *)
    bMastVentActive_Out             : BOOL;    (* Atmospheric Relief Mast Vent Actively Depressurizing Cargo Tanks [-] *)
    bPlantTripped_Out               : BOOL;    (* Plant SIL-3 Quick Safety Instrumented Protective Trip Active [-] *)
    eCurrentState_Out               : INT;     (* Deterministic Cryogenic FSM Operational State Index (0..13) [-] *)
    dwStatusWord1_Out               : DWORD;   (* 32-Bit Bit-Packed System Operational Status Register 1 [DWORD] *)
    dwStatusWord2_Out               : DWORD;   (* 32-Bit Bit-Packed Marine Hull & Auxiliary Status Register 2 [DWORD] *)
    dwAlarmWord1_Out                : DWORD;   (* 32-Bit Bit-Packed Critical Safety Trip Interlock Register 1 [DWORD] *)
    dwAlarmWord2_Out                : DWORD;   (* 32-Bit Bit-Packed Warning Advisory Process Alarm Register 2 [DWORD] *)
    dwFirstOutWord_Out              : DWORD;   (* 32-Bit Bit-Packed Root-Cause Safety Trip First-Out Latch Register [DWORD] *)
END_VAR

VAR
    (* =================================================================================================================
     * SECTION 1: GLOBAL CONSTANTS & EXECUTION CYCLE PARAMETERS
     * ================================================================================================================= *)
    dtCycle                         : REAL := 0.020;  (* Continuous Execution Time-Step Delta Ts = 20 ms [s] *)
    rGasConstant_R_Methane          : REAL := 0.5182; (* Specific Gas Constant for Pure Methane Vapor [kJ/(kg*K)] *)
    rGasConstant_R_Nitrogen         : REAL := 0.2968; (* Specific Gas Constant for Pure Nitrogen Gas [kJ/(kg*K)] *)
    rMethane_Isentropic_k           : REAL := 1.310;  (* Methane Vapor Ratio of Specific Heats Cp/Cv [-] *)
    rNitrogen_Isentropic_k          : REAL := 1.400;  (* Nitrogen Gas Ratio of Specific Heats Cp/Cv [-] *)
    rLNG_LatentHeatVap              : REAL := 510.5;  (* Latent Heat of Vaporization of Cryogenic LNG at Saturation [kJ/kg] *)
    rLNG_LiquidDensity              : REAL := 450.0;  (* Density of Saturated Liquid LNG Condensate [kg/m3] *)
    rColdBox_HeatTransferCoeff_UA   : REAL := 125.8;  (* Cryogenic Plate-Fin Subcooler Overall Conductance [kW/K] *)
    rTankUllageVolume_Total         : REAL := 24500.0;(* Combined Cryogenic Ullage Gas Volume Tanks 1 to 4 [m3] *)
    rSurgeMarginSetPoint            : REAL := 1.150;  (* Mandatory Dynamic Anti-Surge Control Margin Factor [-] *)
    rSurgeTripThreshold             : REAL := 1.050;  (* Emergency Rapid Blow-Off Surge Trip Margin Threshold [-] *)

    (* =================================================================================================================
     * SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) INTERNAL STRUCTURES & ACCUMULATION TIMERS
     * ================================================================================================================= *)
    (* Channel A/B/C Pairwise Differences & Discrepancy Fault Timers (250 ms Trip Threshold) *)
    rDiff_PT101_AB                  : REAL := 0.0;    (* Ullage PT-101 |Channel A - Channel B| [kPa] *)
    rDiff_PT101_BC                  : REAL := 0.0;    (* Ullage PT-101 |Channel B - Channel C| [kPa] *)
    rDiff_PT101_CA                  : REAL := 0.0;    (* Ullage PT-101 |Channel C - Channel A| [kPa] *)
    tTimer_PT101_Discrepancy        : REAL := 0.0;    (* Ullage PT-101 Accumulated Discrepancy Fault Timer [s] *)
    bFault_PT101A                   : BOOL := FALSE;  (* Ullage PT-101 Channel A Isolated Fault Flag [-] *)
    bFault_PT101B                   : BOOL := FALSE;  (* Ullage PT-101 Channel B Isolated Fault Flag [-] *)
    bFault_PT101C                   : BOOL := FALSE;  (* Ullage PT-101 Channel C Isolated Fault Flag [-] *)
    iDegradationState_PT101         : INT := 3;       (* Ullage PT-101 Health: 3=3oo3, 2=2oo2, 1=1oo1, 0=Tripped [-] *)

    rDiff_PT201_AB                  : REAL := 0.0;    (* Suction PT-201 |Channel A - Channel B| [kPa] *)
    rDiff_PT201_BC                  : REAL := 0.0;    (* Suction PT-201 |Channel B - Channel C| [kPa] *)
    rDiff_PT201_CA                  : REAL := 0.0;    (* Suction PT-201 |Channel C - Channel A| [kPa] *)
    tTimer_PT201_Discrepancy        : REAL := 0.0;    (* Suction PT-201 Accumulated Discrepancy Fault Timer [s] *)
    bFault_PT201A                   : BOOL := FALSE;  (* Suction PT-201 Channel A Isolated Fault Flag [-] *)
    bFault_PT201B                   : BOOL := FALSE;  (* Suction PT-201 Channel B Isolated Fault Flag [-] *)
    bFault_PT201C                   : BOOL := FALSE;  (* Suction PT-201 Channel C Isolated Fault Flag [-] *)
    iDegradationState_PT201         : INT := 3;       (* Suction PT-201 Health: 3=3oo3, 2=2oo2, 1=1oo1, 0=Tripped [-] *)

    rDiff_PDT301_AB                 : REAL := 0.0;    (* Venturi PDT-301 |Channel A - Channel B| [kPa] *)
    rDiff_PDT301_BC                 : REAL := 0.0;    (* Venturi PDT-301 |Channel B - Channel C| [kPa] *)
    rDiff_PDT301_CA                 : REAL := 0.0;    (* Venturi PDT-301 |Channel C - Channel A| [kPa] *)
    tTimer_PDT301_Discrepancy       : REAL := 0.0;    (* Venturi PDT-301 Accumulated Discrepancy Fault Timer [s] *)
    bFault_PDT301A                  : BOOL := FALSE;  (* Venturi PDT-301 Channel A Isolated Fault Flag [-] *)
    bFault_PDT301B                  : BOOL := FALSE;  (* Venturi PDT-301 Channel B Isolated Fault Flag [-] *)
    bFault_PDT301C                  : BOOL := FALSE;  (* Venturi PDT-301 Channel C Isolated Fault Flag [-] *)
    iDegradationState_PDT301        : INT := 3;       (* Venturi PDT-301 Health: 3=3oo3, 2=2oo2, 1=1oo1, 0=Tripped [-] *)

    rDiff_TT401_AB                  : REAL := 0.0;    (* Expander TT-401 |Channel A - Channel B| [deg C] *)
    rDiff_TT401_BC                  : REAL := 0.0;    (* Expander TT-401 |Channel B - Channel C| [deg C] *)
    rDiff_TT401_CA                  : REAL := 0.0;    (* Expander TT-401 |Channel C - Channel A| [deg C] *)
    tTimer_TT401_Discrepancy        : REAL := 0.0;    (* Expander TT-401 Accumulated Discrepancy Fault Timer [s] *)
    bFault_TT401A                   : BOOL := FALSE;  (* Expander TT-401 Channel A Isolated Fault Flag [-] *)
    bFault_TT401B                   : BOOL := FALSE;  (* Expander TT-401 Channel B Isolated Fault Flag [-] *)
    bFault_TT401C                   : BOOL := FALSE;  (* Expander TT-401 Channel C Isolated Fault Flag [-] *)
    iDegradationState_TT401         : INT := 3;       (* Expander TT-401 Health: 3=3oo3, 2=2oo2, 1=1oo1, 0=Tripped [-] *)

    rDiff_FT501_AB                  : REAL := 0.0;    (* Condensate FT-501 |Channel A - Channel B| [kg/h] *)
    rDiff_FT501_BC                  : REAL := 0.0;    (* Condensate FT-501 |Channel B - Channel C| [kg/h] *)
    rDiff_FT501_CA                  : REAL := 0.0;    (* Condensate FT-501 |Channel C - Channel A| [kg/h] *)
    tTimer_FT501_Discrepancy        : REAL := 0.0;    (* Condensate FT-501 Accumulated Discrepancy Fault Timer [s] *)
    bFault_FT501A                   : BOOL := FALSE;  (* Condensate FT-501 Channel A Isolated Fault Flag [-] *)
    bFault_FT501B                   : BOOL := FALSE;  (* Condensate FT-501 Channel B Isolated Fault Flag [-] *)
    bFault_FT501C                   : BOOL := FALSE;  (* Condensate FT-501 Channel C Isolated Fault Flag [-] *)
    iDegradationState_FT501         : INT := 3;       (* Condensate FT-501 Health: 3=3oo3, 2=2oo2, 1=1oo1, 0=Tripped [-] *)

    (* Tolerances for 2oo3 Sensor Voting *)
    rTol_PT101                      : REAL := 0.850;  (* Cargo Ullage Pressure Discrepancy Tolerance Threshold [kPa] *)
    rTol_PT201                      : REAL := 1.250;  (* Compressor Suction Discrepancy Tolerance Threshold [kPa] *)
    rTol_PDT301                     : REAL := 0.650;  (* Compressor Discharge Venturi DP Discrepancy Tolerance [kPa] *)
    rTol_TT401                      : REAL := 2.500;  (* Expander Discharge Temp Discrepancy Tolerance [deg C] *)
    rTol_FT501                      : REAL := 65.00;  (* Condensate Coriolis Flow Discrepancy Tolerance [kg/h] *)

    (* =================================================================================================================
     * SECTION 3: 8-STATE CYBER-PHYSICAL DISCRETE STATE-SPACE MATRICES & LUENBERGER OBSERVER
     *
     * States:
     *   x1: LNG Cargo Tank 1 Ullage Vapor Pressure Deviation [kPa]
     *   x2: LNG Cargo Tank 4 Ullage Vapor Pressure Deviation [kPa]
     *   x3: BOG Compressor Stage 1 Suction Temperature Deviation [deg C]
     *   x4: BOG Compressor Stage 2 Discharge Pressure Deviation [kPa]
     *   x5: Nitrogen Compander Expander Outlet Temperature Deviation [deg C]
     *   x6: Cold Box Subcooled LNG Condensate Temperature Deviation [deg C]
     *   x7: Subcooled LNG Return Header Flow Rate Deviation [kg/h]
     *   x8: Nitrogen Cycle Refrigeration Loop Mass Inventory Deviation [kg]
     *
     * Control Actuators u (6 inputs):
     *   u1: BOG Stage 1 Anti-Surge Bypass Valve Modulation Demand [0..100 %]
     *   u2: BOG Stage 2 Anti-Surge Bypass Valve Modulation Demand [0..100 %]
     *   u3: Nitrogen Compander Variable Inlet Guide Vanes (IGV) [0..100 %]
     *   u4: Subcooled LNG Condensate Return Header Valve Demand [0..100 %]
     *   u5: Gas Combustion Unit (GCU) Fast-Dump Throttle Valve Demand [0..100 %]
     *   u6: BOG Compressor Variable Frequency Drive (VFD) Speed [0..100 %]
     *
     * Measured Process Outputs y (6 outputs):
     *   y1: Voted Cargo Tank 1 Ullage Pressure [kPa]
     *   y2: Cargo Tank 4 Ullage Pressure [kPa]
     *   y3: BOG Compressor Stage 2 Discharge Pressure [kPa]
     *   y4: Voted Nitrogen Compander Expander Discharge Temp [deg C]
     *   y5: Cold Box Subcooled LNG Condensate Outlet Temp [deg C]
     *   y6: Voted Subcooled LNG Condensate Return Flow Rate [kg/h]
     * ================================================================================================================= *)
    matA                            : ARRAY[1..8, 1..8] OF REAL := [
        (* Row 1: x1 Tank 1 Ullage Pres *)
        [0.9882, 0.0042, -0.0018, -0.0025, 0.0000, -0.0012, -0.0035, 0.0000],
        (* Row 2: x2 Tank 4 Ullage Pres *)
        [0.0039, 0.9885, -0.0015, -0.0022, 0.0000, -0.0011, -0.0032, 0.0000],
        (* Row 3: x3 Stage 1 Suct Temp *)
        [0.0012, 0.0010, 0.9765, 0.0045, 0.0000, 0.0024, 0.0008, 0.0000],
        (* Row 4: x4 Stage 2 Disch Pres *)
        [0.0055, 0.0048, 0.0125, 0.9620, 0.0000, 0.0000, 0.0015, 0.0000],
        (* Row 5: x5 N2 Expander Temp *)
        [0.0000, 0.0000, 0.0000, 0.0000, 0.9680, 0.0145, 0.0000, -0.0058],
        (* Row 6: x6 Condensate Temp *)
        [0.0000, 0.0000, 0.0028, 0.0032, 0.0385, 0.9520, 0.0012, -0.0034],
        (* Row 7: x7 Condensate Flow *)
        [-0.0150, -0.0125, -0.0450, 0.1250, -0.2850, -0.4200, 0.9410, 0.0210],
        (* Row 8: x8 N2 Loop Inventory *)
        [0.0000, 0.0000, 0.0000, 0.0000, -0.0012, 0.0000, 0.0000, 0.9995]
    ];

    matB                            : ARRAY[1..8, 1..6] OF REAL := [
        (* Row 1: x1 *) [ 0.0048,  0.0035,  0.0000, -0.0082, -0.0245, -0.0315],
        (* Row 2: x2 *) [ 0.0042,  0.0031,  0.0000, -0.0078, -0.0238, -0.0302],
        (* Row 3: x3 *) [-0.0185, -0.0120,  0.0000,  0.0000,  0.0000,  0.0085],
        (* Row 4: x4 *) [-0.1450, -0.2150,  0.0000,  0.0000, -0.0420,  0.3850],
        (* Row 5: x5 *) [ 0.0000,  0.0000, -0.1650,  0.0000,  0.0000,  0.0000],
        (* Row 6: x6 *) [ 0.0000,  0.0000, -0.0820,  0.0240,  0.0000,  0.0115],
        (* Row 7: x7 *) [-0.2500, -0.3800,  1.4200,  1.8500, -0.1200,  2.1500],
        (* Row 8: x8 *) [ 0.0000,  0.0000,  0.0045,  0.0000,  0.0000,  0.0000]
    ];

    matC                            : ARRAY[1..6, 1..8] OF REAL := [
        (* y1: x1 Tank 1 Pres *)     [1.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        (* y2: x2 Tank 4 Pres *)     [0.0000, 1.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        (* y3: x4 Stg 2 Disch Pres*)[0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        (* y4: x5 N2 Exp Temp *)     [0.0000, 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000, 0.0000],
        (* y5: x6 Condensate Temp *) [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000],
        (* y6: x7 Condensate Flow *) [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000, 0.0000]
    ];

    matD                            : ARRAY[1..6, 1..6] OF REAL := [
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]
    ];

    matL                            : ARRAY[1..8, 1..6] OF REAL := [
        (* Row 1: x1 *) [0.1850, 0.0210, 0.0045, 0.0000, 0.0000, -0.0008],
        (* Row 2: x2 *) [0.0195, 0.1820, 0.0038, 0.0000, 0.0000, -0.0007],
        (* Row 3: x3 *) [0.0085, 0.0072, 0.0240, 0.0000, 0.0125,  0.0015],
        (* Row 4: x4 *) [0.0120, 0.0110, 0.2250, 0.0000, 0.0000,  0.0042],
        (* Row 5: x5 *) [0.0000, 0.0000, 0.0000, 0.2450, 0.0380,  0.0000],
        (* Row 6: x6 *) [0.0000, 0.0000, 0.0085, 0.0420, 0.2150,  0.0028],
        (* Row 7: x7 *) [-0.0450, -0.0380, 0.1150, -0.0850, -0.1450, 0.2680],
        (* Row 8: x8 *) [0.0000, 0.0000, 0.0000, -0.0055, 0.0000, 0.0085]
    ];

    (* Real-Time State Vectors *)
    x_StateEst                      : ARRAY[1..8] OF REAL := [8(0.0)]; (* Estimated Current State Vector x_hat[k] *)
    x_StatePred                     : ARRAY[1..8] OF REAL := [8(0.0)]; (* A-priori Predicted State Vector x_pred[k+1] *)
    y_ModelOutput                   : ARRAY[1..6] OF REAL := [6(0.0)]; (* Model Estimated Process Output y_hat[k] *)
    y_MeasuredSensors               : ARRAY[1..6] OF REAL := [6(0.0)]; (* True Measured Physical Output y[k] *)
    innov_ObserverResidual          : ARRAY[1..6] OF REAL := [6(0.0)]; (* Kalman/Luenberger Innovation Residual e[k] *)
    u_ActuatorCurrent               : ARRAY[1..6] OF REAL := [6(0.0)]; (* Currently Applied Plant Inputs u[k] *)
    u_ActuatorPrevious              : ARRAY[1..6] OF REAL := [6(0.0)]; (* Previous Cycle Applied Inputs u[k-1] *)

    (* Baseline Operating Point Bias Constants *)
    rNominal_UllagePres_Tank1       : REAL := 108.50; (* Nominal Base Tank 1 Ullage Operating Pressure [kPa] *)
    rNominal_UllagePres_Tank4       : REAL := 108.45; (* Nominal Base Tank 4 Ullage Operating Pressure [kPa] *)
    rNominal_Stage1SuctTemp         : REAL := -125.0; (* Nominal Stage 1 Cryogenic Suction Temperature [deg C] *)
    rNominal_Stage2DischPres        : REAL := 580.00; (* Nominal Stage 2 Compressor Discharge Pressure [kPa] *)
    rNominal_N2ExpanderTemp         : REAL := -165.5; (* Nominal Nitrogen Expander Cryogenic Outlet Temp [deg C] *)
    rNominal_CondensateTemp         : REAL := -161.8; (* Nominal Plate-Fin Subcooled LNG Condensate Temp [deg C] *)
    rNominal_CondensateFlow         : REAL := 3250.0; (* Nominal Subcooled Condensate Coriolis Flow [kg/h] *)
    rNominal_N2LoopMassInventory    : REAL := 2050.0; (* Nominal Nitrogen Loop Closed Mass Inventory [kg] *)

    (* =================================================================================================================
     * SECTION 4: MODEL PREDICTIVE CONTROL (MPC) & PROJECTED GRADIENT DESCENT (PGD) ARRAYS
     * Horizon Np = 5 steps, Nu = 5 steps, 6 Iterations of Projected Gradient Descent
     * ================================================================================================================= *)
    weightQ_State                   : ARRAY[1..8] OF REAL := [
        185.0,  (* Q1: Tank 1 Ullage Pressure Deviation Penalty *)
        185.0,  (* Q2: Tank 4 Ullage Pressure Deviation Penalty *)
        12.5,   (* Q3: Stage 1 Suction Temp Penalty *)
        45.0,   (* Q4: Stage 2 Discharge Pressure Penalty *)
        65.0,   (* Q5: N2 Expander Temp Penalty *)
        85.0,   (* Q6: Condensate Subcooled Temp Penalty *)
        35.0,   (* Q7: Condensate Flow Penalty *)
        20.0    (* Q8: N2 Inventory Balance Penalty *)
    ];

    weightR_Actuator                : ARRAY[1..6] OF REAL := [
        25.0,   (* R1: ASV1 Bypass Movement Penalty *)
        25.0,   (* R2: ASV2 Bypass Movement Penalty *)
        15.0,   (* R3: N2 IGV Vane Modulating Penalty *)
        10.0,   (* R4: Condensate Valve Modulating Penalty *)
        75.0,   (* R5: GCU Dump Valve Opening Cost Penalty (Fuel Loss) *)
        18.0    (* R6: Compressor VFD Speed Modulation Penalty *)
    ];

    weightP_TerminalState           : ARRAY[1..8] OF REAL := [
        285.0, 285.0, 18.0, 65.0, 95.0, 125.0, 50.0, 30.0
    ];

    (* Dynamic Surge Penalty Gain *)
    rSurgeBarrierGain               : REAL := 450.0;  (* Asymmetric Barrier Penalty for SLL Proximity *)

    (* MPC Trajectory Storage Arrays [Horizon 1..5, Elements] *)
    u_MpcHorizon                    : ARRAY[1..5, 1..6] OF REAL := [5([6(0.0)])];
    x_MpcHorizon                    : ARRAY[1..5, 1..8] OF REAL := [5([8(0.0)])];
    grad_CostFunction               : ARRAY[1..5, 1..6] OF REAL := [5([6(0.0)])];
    x_MpcTargetTrajectory           : ARRAY[1..5, 1..8] OF REAL := [5([8(0.0)])];

    (* Actuator Slew Rate Limiters (% per cycle) *)
    rMaxSlew_ASV_Open               : REAL := 5.000;  (* Anti-Surge Fast Open Limit = 250 %/s [5.0% per 20 ms] *)
    rMaxSlew_ASV_Close              : REAL := 0.250;  (* Anti-Surge Safe Slow Close Limit = 12.5 %/s [0.25% per 20 ms] *)
    rMaxSlew_IGV                    : REAL := 0.100;  (* Nitrogen Compander Guide Vane Limit = 5.0 %/s [0.10% per 20 ms] *)
    rMaxSlew_CondValve              : REAL := 0.200;  (* Condensate Control Valve Limit = 10.0 %/s [0.20% per 20 ms] *)
    rMaxSlew_GCU_Valve              : REAL := 1.500;  (* GCU Thermal Fast Dump Opening = 75 %/s [1.5% per 20 ms] *)
    rMaxSlew_VFD                    : REAL := 0.150;  (* BOG Compressor VFD Speed Ramp Limit = 7.5 %/s [0.15% per 20 ms] *)

    (* PGD Step Size Alpha *)
    rPGD_StepSize                   : REAL := 0.00085;(* Gradient Descent Convergence Step Size *)

    (* =================================================================================================================
     * SECTION 5: MARINE HYDRODYNAMICS, ULLAGE COMPRESSION & SLOSHING DAMPING
     * ================================================================================================================= *)
    rSloshingWaveInertialGain       : REAL := 0.245;  (* Hydrodynamic Transfer Function Peak Gain [kPa/(deg*m/s2)] *)
    rHullPitchFilterMemory          : REAL := 0.0;    (* Infinite Impulse Response (IIR) Filter Pitch State [deg] *)
    rHullRollFilterMemory           : REAL := 0.0;    (* Infinite Impulse Response (IIR) Filter Roll State [deg] *)
    rDynamicSloshingDeltaPres       : REAL := 0.0;    (* Instantaneous Ullage Hydrodynamic Sloshing Pressure Peak [kPa] *)
    rUllageCompressibilityFactor    : REAL := 0.982;  (* Real Methane Superheated Gas Compressibility Z [-] *)
    rDynamicBOR_Compensation        : REAL := 0.0;    (* Derived Boil-Off Rate Mass Generation Trim [kg/h] *)

    (* =================================================================================================================
     * SECTION 6: CENTRIFUGAL COMPRESSOR POLYTROPIC THERMODYNAMICS & SURGE LINES
     * ================================================================================================================= *)
    rStg1_SurgeLineSlope_K1         : REAL := 0.185;  (* Stage 1 Surge Limit Line Orifice Slope K_surge1 *)
    rStg2_SurgeLineSlope_K2         : REAL := 0.242;  (* Stage 2 Surge Limit Line Orifice Slope K_surge2 *)
    rStg1_EquivalentFlowDP          : REAL := 0.0;    (* Calculated Stage 1 Suction Flow Differential Pressure [kPa] *)
    rStg2_EquivalentFlowDP          : REAL := 0.0;    (* Calculated Stage 2 Flow Venturi Differential Pressure [kPa] *)
    rStg1_SurgeLimitDP              : REAL := 0.0;    (* Stage 1 Orifice Surge Limit DP at Current Compression Ratio [kPa] *)
    rStg2_SurgeLimitDP              : REAL := 0.0;    (* Stage 2 Orifice Surge Limit DP at Current Compression Ratio [kPa] *)
    rStg1_SurgeMarginRatio          : REAL := 1.250;  (* Stage 1 Instantaneous Surge Margin Ratio Ss1 [-] *)
    rStg2_SurgeMarginRatio          : REAL := 1.250;  (* Stage 2 Instantaneous Surge Margin Ratio Ss2 [-] *)
    rCompressorPolytropicEfficiency : REAL := 0.785;  (* Stage 2 Centrifugal Impeller Polytropic Efficiency [-] *)

    (* =================================================================================================================
     * SECTION 7: NITROGEN REVERSE BRAYTON CRYOGENIC EXPANDER & COLD BOX BALANCE
     * ================================================================================================================= *)
    rN2ExpanderIsentropicEfficiency : REAL := 0.845;  (* Cryogenic Inflow Radial Expander Efficiency [-] *)
    rColdBoxLMTD_Calculated         : REAL := 8.450;  (* Plate-Fin Heat Exchanger Cryogenic LMTD [deg C] *)
    rNetReliquefactionMassFlow      : REAL := 0.0;    (* Net Reliquefied Saturated LNG Condensate Generated [kg/h] *)
    rCryogenicCoolingDuty           : REAL := 0.0;    (* Plate-Fin Subcooler Total Heat Extraction Duty [kW] *)

    (* =================================================================================================================
     * SECTION 8: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
     * ================================================================================================================= *)
    eState                          : INT := 0;       (* Current Discrete Cryogenic State Index (0..13) *)
    ePreviousState                  : INT := 0;       (* Previous Execution Cycle State Index *)
    tStateStepTimer                 : REAL := 0.0;    (* Internal State Dwell Accumulation Timer [s] *)
    bStateInitialized               : BOOL := FALSE;  (* State Entry Action Execution Latch *)
    bPlantTripLatched               : BOOL := FALSE;  (* Master Plant Safety Trip Latch *)
    bGCU_RequiredActive             : BOOL := FALSE;  (* Gas Combustion Unit Interlock Fire Permissive *)
    bMastVentPermitted              : BOOL := FALSE;  (* Emergency Atmospheric Mast Vent Permissive *)

    (* =================================================================================================================
     * SECTION 9: ISA-18.2 PROCESS ALARM TRIP POINTS, DEADBANDS & INTERLOCK REGISTERS
     * ================================================================================================================= *)
    (* Cargo Tank Ullage Pressure Alarms (Nominal 108.5 kPa) *)
    rSP_Ullage_HH                   : REAL := 125.00; (* Trip: Automatic GCU Fire & Emergency Mast Vent Permissive [kPa] *)
    rSP_Ullage_H                    : REAL := 115.00; (* Warning: High Cargo Tank Ullage Vapor Accumulation [kPa] *)
    rSP_Ullage_L                    : REAL := 102.00; (* Warning: Low Cargo Ullage Pressure (Vacuum Hazard) [kPa] *)
    rSP_Ullage_LL                   : REAL := 99.00;  (* Trip: Severe Vacuum Threat - Compressor Fast Trip [kPa] *)
    rDB_Ullage                      : REAL := 0.75;   (* Ullage Pressure Clearance Deadband [kPa] *)

    (* BOG Stage 2 Discharge Pressure Alarms (Nominal 580 kPa) *)
    rSP_DischPres_HH                : REAL := 680.00; (* Trip: High Compressor Discharge Overpressure Trip [kPa] *)
    rSP_DischPres_H                 : REAL := 630.00; (* Warning: Compressor Discharge Throttle Back [kPa] *)
    rSP_DischPres_L                 : REAL := 450.00; (* Warning: Compressor Low Head Advisory [kPa] *)
    rSP_DischPres_LL                : REAL := 380.00; (* Trip: Compressor Loss of Head / Blowby Trip [kPa] *)
    rDB_DischPres                   : REAL := 5.00;   (* Discharge Pressure Clearance Deadband [kPa] *)

    (* Nitrogen Expander Cryogenic Outlet Temperature Alarms (Nominal -165.5 deg C) *)
    rSP_N2ExpTemp_HH                : REAL := -120.0; (* Trip: Loss of Cryogenic Refrigeration Trip [deg C] *)
    rSP_N2ExpTemp_H                 : REAL := -145.0; (* Warning: Insufficient Subcooling Temperature [deg C] *)
    rSP_N2ExpTemp_L                 : REAL := -178.0; (* Warning: Expander Excessive Chilldown Warning [deg C] *)
    rSP_N2ExpTemp_LL                : REAL := -188.0; (* Trip: Solid Freezing Threat / Dryness Limit Trip [deg C] *)
    rDB_N2ExpTemp                   : REAL := 2.00;   (* Expander Temperature Clearance Deadband [deg C] *)

    (* Mechanical Health & Bearing Alarms *)
    rSP_Vibration_HH                : REAL := 55.0;   (* Trip: Drive Motor Shaft Vibration High Trip [um] *)
    rSP_Vibration_H                 : REAL := 38.0;   (* Warning: High Shaft Radial Vibration Advisory [um] *)
    rSP_LubeOilPres_LL              : REAL := 1.80;   (* Trip: Severe Low Bearing Lube Oil Pressure Trip [bar] *)
    rSP_LubeOilPres_L               : REAL := 2.40;   (* Warning: Low Lube Oil Pressure Warning [bar] *)
    rSP_SealGasDP_LL                : REAL := 0.85;   (* Trip: Loss of Dry Gas Seal Nitrogen Barrier Trip [bar] *)

    (* ISA-18.2 Latched Alarm Bit Status Registers *)
    bAlarm_Ullage_HH                : BOOL := FALSE;
    bAlarm_Ullage_H                 : BOOL := FALSE;
    bAlarm_Ullage_L                 : BOOL := FALSE;
    bAlarm_Ullage_LL                : BOOL := FALSE;
    bAlarm_DischPres_HH             : BOOL := FALSE;
    bAlarm_DischPres_H              : BOOL := FALSE;
    bAlarm_DischPres_L              : BOOL := FALSE;
    bAlarm_DischPres_LL             : BOOL := FALSE;
    bAlarm_N2ExpTemp_HH             : BOOL := FALSE;
    bAlarm_N2ExpTemp_H              : BOOL := FALSE;
    bAlarm_N2ExpTemp_L              : BOOL := FALSE;
    bAlarm_N2ExpTemp_LL             : BOOL := FALSE;
    bAlarm_Vibration_HH             : BOOL := FALSE;
    bAlarm_Vibration_H              : BOOL := FALSE;
    bAlarm_LubeOilPres_LL           : BOOL := FALSE;
    bAlarm_LubeOilPres_L            : BOOL := FALSE;
    bAlarm_SealGasDP_LL             : BOOL := FALSE;
    bAlarm_Surge_Stg1_Trip          : BOOL := FALSE;
    bAlarm_Surge_Stg2_Trip          : BOOL := FALSE;

    (* 32-Bit Telemetry DWORD Bitfields *)
    dwStatusWord1                   : DWORD := 16#00000000;
    dwStatusWord2                   : DWORD := 16#00000000;
    dwAlarmWord1                    : DWORD := 16#00000000;
    dwAlarmWord2                    : DWORD := 16#00000000;
    dwFirstOutWord                  : DWORD := 16#00000000;

    (* Temporary Loop Variables & Accumulators *)
    idxLoop                         : INT := 0;
    jdxLoop                         : INT := 0;
    kdxLoop                         : INT := 0;
    iterPGD                         : INT := 0;
    rTempSum                        : REAL := 0.0;
    rTempCost                       : REAL := 0.0;
    rSlewDelta                      : REAL := 0.0;
    rTargetInput                    : REAL := 0.0;
END_VAR
"""
