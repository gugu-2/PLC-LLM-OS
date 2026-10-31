# build_full_lyophilizer.py
import json
import os
import sys

import gen_st_code
import append_var
import gen_phase0
import gen_phase1
import gen_phase2
import gen_phase3_4
import gen_phase5
import gen_phase6
import validate_iec

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Pharmaceuticals & Bioprocess: Large-Scale Industrial Production Lyophilizer (Freeze Dryer, 50 m2 Shelf Area) with Dual-Stage Sublimation, Pirani-Capacitance End-Point Metrology & Automated Hydraulic Vial Stoppering**

Task: Implement the production-grade Function Block `FB_Pharma_Lyophilizer_FreezeDrying_Sublimation` governing:
1. Discrete State-Space Matrices (A, B, C, D) 16x16 state matrix A, 16x8 matrix B, C, D incorporating ice sublimation heat of vaporization, shelf silicone oil convective heat transfer, ice condenser frosting layer thickness thermal resistance, and Pirani gas composition dynamics: x_{k+1} = A*x_k + B*u_k.
2. Model Predictive Control (MPC) quadratic cost optimization governing shelf thermal fluid heating/cooling, refrigeration screw compressor slide valve, and sterile nitrogen micro-bleed dosing to maximize sublimation rate while strictly preventing product cake collapse (T_prod < T_collapse).
3. 2oo3 Triple Modular Redundancy (TMR) voting logic on shelf RTDs, vial thermocouple clusters, capacitance manometers (Baratron), Pirani gauges, condenser coil RTDs, and hydraulic load cells with bumpless degradation.
4. Dual-gauge endpoint determination metrology comparing thermal conductivity Pirani indication with absolute capacitance manometer readings (Delta_P < 0.005 mbar) combined with dynamic pressure rise test verification.
5. 12-Stage Operational Finite State Machine (CIP_SIP_VERIFICATION, AUTO_VIAL_LOADING, CONTROLLED_FREEZING_ANNEAL, CONTROLLED_ICE_NUCLEATION_PULSE, VACUUM_PUMPDOWN, PRIMARY_DRYING_SUBLIMATION, PIRANI_CM_ENDPOINT_DETECTION, SECONDARY_DRYING_DESORPTION, CHAMBER_BACKFILL_STERILE_N2, HYDRAULIC_SHELF_STOPPERING, AUTO_VIAL_UNLOADING, CONDENSER_ICE_DEFROST_CYCLE).
6. ISA-18.2 multi-tiered alarm matrix (Product collapse danger HH, vacuum loss HH, condenser high temp H/HH, compressor discharge head, hydraulic stoppering force shortfall) with bit-packed telemetry DWORDs.

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

header = gen_st_code.generate_header()

var_input = """VAR_INPUT
    (* Master Automation Supervisory Permissives & Safety Interlocks *)
    bMasterBatchRunPermissive          : BOOL := FALSE;    (* Global Lyophilizer Batch Execution Permissive [BOOL] *)
    bEmergencyStopCircuit_NC          : BOOL := TRUE;     (* Dual-Channel Safety E-Stop Circuit Normally Closed [BOOL] *)
    bCleanInPlaceVerified_NC          : BOOL := TRUE;     (* CIP Validated Sanitization Completion Interlock [BOOL] *)
    bSteamInPlaceVerified_NC          : BOOL := TRUE;     (* SIP Validated Thermal Sterilization Completion Interlock [BOOL] *)
    bChamberDoorClosedLocked_NC       : BOOL := TRUE;     (* Chamber Main Aseptic Loading Door Sealed & Latched [BOOL] *)
    bCondenserDoorClosedLocked_NC     : BOOL := TRUE;     (* Condenser Vessel Maintenance Hatch Latched [BOOL] *)
    bResetFaultLatches                : BOOL := FALSE;    (* Unified Operator Alarm Acknowledge & Reset [BOOL] *)
    bManualInterventionMode           : BOOL := FALSE;    (* Semi-Automatic Manual Engineering Mode Override [BOOL] *)
    bDryCycleTestPermissive           : BOOL := FALSE;    (* Mechanical Dry-Cycle Test Mode Permissive [BOOL] *)

    (* 2oo3 Triple Modular Redundant (TMR) Shelf Silicone Oil Temperature RTD Channels [deg C] *)
    rShelfTempInlet_ChA               : REAL := 20.0;     (* Shelf Silicone Oil Inlet RTD Transducer Ch A [deg C] *)
    rShelfTempInlet_ChB               : REAL := 20.0;     (* Shelf Silicone Oil Inlet RTD Transducer Ch B [deg C] *)
    rShelfTempInlet_ChC               : REAL := 20.0;     (* Shelf Silicone Oil Inlet RTD Transducer Ch C [deg C] *)
    rShelfTempOutlet_ChA              : REAL := 20.0;     (* Shelf Silicone Oil Outlet RTD Transducer Ch A [deg C] *)
    rShelfTempOutlet_ChB              : REAL := 20.0;     (* Shelf Silicone Oil Outlet RTD Transducer Ch B [deg C] *)
    rShelfTempOutlet_ChC              : REAL := 20.0;     (* Shelf Silicone Oil Outlet RTD Transducer Ch C [deg C] *)

    (* 2oo3 Triple Modular Redundant (TMR) Product Vial Thermocouple Clusters [deg C] *)
    rProductVialTemp_ChA              : REAL := 20.0;     (* Representative Vial Center Sublimation Front TC Cluster A [deg C] *)
    rProductVialTemp_ChB              : REAL := 20.0;     (* Representative Vial Center Sublimation Front TC Cluster B [deg C] *)
    rProductVialTemp_ChC              : REAL := 20.0;     (* Representative Vial Center Sublimation Front TC Cluster C [deg C] *)

    (* 2oo3 Triple Modular Redundant (TMR) Heated Capacitance Manometer Absolute Vacuum Gauges [mbar] *)
    rChamberPressure_CM_ChA           : REAL := 1013.25;  (* MKS Baratron Heated Capacitance Manometer Ch A [mbar] *)
    rChamberPressure_CM_ChB           : REAL := 1013.25;  (* MKS Baratron Heated Capacitance Manometer Ch B [mbar] *)
    rChamberPressure_CM_ChC           : REAL := 1013.25;  (* MKS Baratron Heated Capacitance Manometer Ch C [mbar] *)

    (* 2oo3 Triple Modular Redundant (TMR) Pirani Thermal Conductivity Vacuum Transducers [mbar] *)
    rChamberPressure_Pirani_ChA       : REAL := 1013.25;  (* Pirani Thermal Conductivity Vacuum Gauge Ch A [mbar] *)
    rChamberPressure_Pirani_ChB       : REAL := 1013.25;  (* Pirani Thermal Conductivity Vacuum Gauge Ch B [mbar] *)
    rChamberPressure_Pirani_ChC       : REAL := 1013.25;  (* Pirani Thermal Conductivity Vacuum Gauge Ch C [mbar] *)

    (* 2oo3 Triple Modular Redundant (TMR) Ice Condenser Coil Temperature RTDs [deg C] *)
    rCondenserCoilTemp_ChA            : REAL := 20.0;     (* Ice Condenser Refrigeration Surface RTD Ch A [deg C] *)
    rCondenserCoilTemp_ChB            : REAL := 20.0;     (* Ice Condenser Refrigeration Surface RTD Ch B [deg C] *)
    rCondenserCoilTemp_ChC            : REAL := 20.0;     (* Ice Condenser Refrigeration Surface RTD Ch C [deg C] *)

    (* 2oo3 Triple Modular Redundant (TMR) Hydraulic Shelf Stoppering Load Cells [kN] *)
    rHydraulicRamForce_ChA            : REAL := 0.0;      (* Shelf Compaction Load Cell Force Transducer Ch A [kN] *)
    rHydraulicRamForce_ChB            : REAL := 0.0;      (* Shelf Compaction Load Cell Force Transducer Ch B [kN] *)
    rHydraulicRamForce_ChC            : REAL := 0.0;      (* Shelf Compaction Load Cell Force Transducer Ch C [kN] *)

    (* Auxiliary Thermal Fluid, Vacuum Skid & Hydraulic Instrumentation *)
    rSiliconeOilCirculationFlowRate   : REAL := 420.0;    (* Silicone Oil Circuit Volumetric Inflow Rate [l/min] *)
    rSiliconeOilCirculationPressure   : REAL := 4.2;      (* Silicone Oil Circulation Skid Supply Header Pressure [bar] *)
    rSterileN2HeaderSupplyPressure    : REAL := 6.2;      (* High-Purity Dry N2 Inflow Header Supply Pressure [bar] *)
    rCleanSteamSupplyPressure         : REAL := 2.8;      (* SIP Sanitization Clean Steam Header Pressure [bar] *)
    rHydraulicSystemLinePressure      : REAL := 220.0;    (* Stoppering Electro-Hydraulic Skid Supply Pressure [bar] *)
    rHydraulicRamLinearPosition_mm    : REAL := 0.0;      (* Stoppering Ram Absolute Linear Stroke Position [mm] *)
    rCondenserFrostThicknessOptical   : REAL := 0.0;      (* Optical/Capacitive Condenser Coil Frost Thickness [mm] *)
    rRootsVacuumBlowerSpeedActual     : REAL := 0.0;      (* Primary Mechanical Booster Roots Blower VFD Speed [rpm] *)
    rScrewVacuumPumpSpeedActual       : REAL := 0.0;      (* Rotary Screw Dry Backing Pump Inverter Speed [rpm] *)
    rCompressor1_DischargePressure    : REAL := 18.5;     (* Dual-Stage Refrigeration Compressor 1 Discharge Head [bar] *)
    rCompressor2_DischargePressure    : REAL := 18.2;     (* Dual-Stage Refrigeration Compressor 2 Discharge Head [bar] *)
    rLN2_BoosterSkidInletPressure     : REAL := 4.5;      (* Cryogenic Liquid Nitrogen Skid Inflow Pressure [bar] *)

    (* Master Lyophilization Batch Recipe Targets & Kinetics Setpoints *)
    rSet_ProductCollapseTemp_Tc       : REAL := -28.5;    (* Critical Formulation Product Collapse Temperature [deg C] *)
    rSet_PrimaryDryingShelfTemp       : REAL := -15.0;    (* Target Primary Drying Sublimation Shelf Temperature [deg C] *)
    rSet_PrimaryDryingChamberPres     : REAL := 0.120;    (* Controlled Chamber Operating Pressure via N2 Bleed [mbar] *)
    rSet_SecondaryDryingShelfTemp     : REAL := 35.0;     (* Target Secondary Drying Desorption Temperature [deg C] *)
    rSet_SecondaryDryingChamberPres   : REAL := 0.015;    (* Secondary Drying Maximum Deep Vacuum Setpoint [mbar] *)
    rSet_ShelfRampRateFreezing        : REAL := 0.80;     (* Controlled Freezing Shelf Cooling Ramp Rate [deg C/min] *)
    rSet_ShelfRampRatePrimaryDry      : REAL := 0.25;     (* Primary Drying Sublimation Shelf Heating Ramp Rate [deg C/min] *)
    rSet_ShelfRampRateSecondaryDry    : REAL := 0.20;     (* Secondary Desorption Shelf Heating Ramp Rate [deg C/min] *)
    rSet_StopperingHoldForceTarget    : REAL := 240.0;    (* Commanded Final Validated Stoppering Compaction Force [kN] *)
    rSet_StopperingHoldDuration_s     : REAL := 180.0;    (* Dwell Duration at Peak Stoppering Force [s] *)
    rCycleScanDeltaTime               : REAL := 0.010;    (* Deterministic PLC Execution Scan Interval (10ms) [s] *)
END_VAR
"""

var_output = """VAR_OUTPUT
    (* Continuous Actuator Speed, Frequency, Valve & Duty Commands *)
    rCmd_ShelfHeaterSCR_DutyPct       : REAL := 0.0;      (* 72kW Silicone Oil Modulated SCR Electric Heater Duty [%] *)
    rCmd_ScrewCompressorSlideValvePct : REAL := 0.0;      (* Refrigeration Screw Compressor Capacity Slide Valve [%] *)
    rCmd_LN2_BoosterCoolingValvePct   : REAL := 0.0;      (* Cryogenic Liquid Nitrogen Injection Proportional Valve [%] *)
    rCmd_RootsVacuumBlowerSpeedPct    : REAL := 0.0;      (* High-Vacuum Dry Roots Booster Blower VFD Speed Ref [%] *)
    rCmd_SterileN2_MicroBleedDosingPct: REAL := 0.0;      (* Dynamic Pressure Regulating Piezo Bleed Valve Duty [%] *)
    rCmd_CondenserRefrigExpansionValvePct: REAL := 0.0;   (* Ice Condenser Direct Expansion Refrigeration TXV [%] *)
    rCmd_HydraulicStopperingServoPct  : REAL := 0.0;      (* Electro-Hydraulic Directional Proportional Servo Valve [%] *)
    rCmd_NucleationDepressPulseValvePct: REAL := 0.0;     (* Controlled Ice Fog Depressurization Pulse Valve [%] *)

    (* Discrete Aseptic Pneumatic, Solenoid & Motor Output Commands *)
    bCmd_MainIsolationMushroomValveOpen: BOOL := FALSE;   (* DN600 Process Chamber-to-Condenser Isolation Poppet [BOOL] *)
    bCmd_ChamberVentSterileN2ValveOpen: BOOL := FALSE;    (* Sterile Nitrogen Backfill Chamber Equalization Valve [BOOL] *)
    bCmd_CondenserDefrostSteamValveOpen: BOOL := FALSE;   (* Condenser Hot Water / Clean Steam Defrost Inflow Valve [BOOL] *)
    bCmd_CondenserCondensateDrainPumpRun: BOOL := FALSE;  (* Condenser Melted Ice Condensate Discharge Pump [BOOL] *)
    bCmd_ChamberDoorPneumaticSealInflate: BOOL := TRUE;   (* Inflatable Infeed/Unload Door Aseptic Gasket Pressurize [BOOL] *)

    (* Transducer 2oo3 Voted Feedbacks & Comprehensive Thermodynamic Telemetry *)
    wAutomationStatusWord             : WORD := 16#0000;  (* Unified Freeze Dryer Automation State Bitfield [WORD] *)
    dwAlarms_ISA18_EmergencyTrips     : DWORD := 16#00000000; (* ISA-18.2 Priority 1 Safety Trip Alarm Bitfield [DWORD] *)
    dwAlarms_ISA18_ProcessWarnings    : DWORD := 16#00000000; (* ISA-18.2 Priority 2 Process Alert Bitfield [DWORD] *)
    dwSensorHealth_TMR_Status         : DWORD := 16#00000000; (* 2oo3 TMR Transducer Discrepancy Health Matrix [DWORD] *)
    dwActuatorStatusWord              : DWORD := 16#00000000; (* Real-Time Field Actuator Energized Status Word [DWORD] *)
    dwBatchCycleTelemetry             : DWORD := 16#00000000; (* Sublimation Physics & Metrology Status Word [DWORD] *)
    nActiveBatchStepState             : INT := 0;         (* Active Primary Finite State Machine State Code [count] *)
    rVotedShelfTemperatureActual      : REAL := 0.0;      (* 2oo3 TMR Validated Shelf Plate Average Temperature [deg C] *)
    rVotedProductTemperatureActual    : REAL := 0.0;      (* 2oo3 TMR Validated Product Sublimation Interface [deg C] *)
    rVotedChamberPressure_CM_Actual   : REAL := 0.0;      (* 2oo3 TMR Validated Baratron Absolute Chamber Pressure [mbar] *)
    rVotedChamberPressure_Pirani_Actual: REAL := 0.0;     (* 2oo3 TMR Validated Pirani Apparent Vacuum Pressure [mbar] *)
    rVotedCondenserCoilTempActual     : REAL := 0.0;      (* 2oo3 TMR Validated Ice Condenser Surface Temperature [deg C] *)
    rVotedHydraulicRamForceActual     : REAL := 0.0;      (* 2oo3 TMR Validated Shelf Stoppering Compaction Force [kN] *)
    rDualGaugeDifferentialPressure    : REAL := 0.0;      (* Pirani vs Capacitance Manometer Delta (P_pirani - P_CM) [mbar] *)
    rSublimationRateInstantaneous     : REAL := 0.0;      (* Calculated Instantaneous Sublimation Mass Flux [kg/h] *)
    rCumulativeSublimatedIceMass      : REAL := 0.0;      (* Integrated Total Mass of Sublimated Ice on Condenser [kg] *)
    rRemainingIceCakeThickness_mm     : REAL := 0.0;      (* Estimated Remaining Frozen Matrix Cake Thickness [mm] *)
    rDesorptionMoistureEstimate_Pct   : REAL := 0.0;      (* Secondary Drying Residual Bound Moisture Estimate [%] *)
    rProductCollapseMarginActual      : REAL := 0.0;      (* Thermal Safety Headroom to Cake Collapse (Tc - T_prod) [deg C] *)
    rChamberPressureRiseRate_mbar_s   : REAL := 0.0;      (* Manometric Endpoint Verification Pressure Rise Slope [mbar/s] *)
    bPrimaryDryingEndpointDetected    : BOOL := FALSE;    (* Metrological Primary Drying Complete Flag [BOOL] *)
    bSecondaryDryingCompleteFlag      : BOOL := FALSE;    (* Residual Moisture Specification Attained Flag [BOOL] *)
    bStopperingCompleteFlag           : BOOL := FALSE;    (* All 150,000 Vials Sealed Under Validated Force [BOOL] *)
    bBatchCycleSuccessfullyComplete   : BOOL := FALSE;    (* Complete 12-Stage Cycle Normal Termination Handshake [BOOL] *)
    bEmergencySafetyInterlockTripped  : BOOL := FALSE;    (* Critical Emergency Trip Fail-Safe Safe State Latched [BOOL] *)
    tCurrentBatchDuration             : TIME := T#0S;     (* Total Elapsed Time in Active Lyophilization Batch [ms] *)
END_VAR
"""

var_block = append_var.generate_var_block()
phase0 = gen_phase0.generate_phase0()
phase1 = gen_phase1.generate_phase1()
phase2 = gen_phase2.generate_phase2()
phase3_4 = gen_phase3_4.generate_phase3_4()
phase5 = gen_phase5.generate_phase5()
phase6 = gen_phase6.generate_phase6()

code_st = "".join([
    header,
    var_input,
    var_output,
    var_block,
    phase0,
    phase1,
    phase2,
    phase3_4,
    phase5,
    phase6
])

assistant_content = f"```iec-st\n{code_st}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

target_file = "data/swarm_raw/agent_5c4019ae.json"
os.makedirs("data/swarm_raw", exist_ok=True)

with open(target_file, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Successfully wrote {len(assistant_content)} characters to {target_file}")
